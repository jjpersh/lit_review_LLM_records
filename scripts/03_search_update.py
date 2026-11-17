"""Stage A.3 — search update to SEARCH_DATE across reachable sources, plus forward citation chasing.

Sources: OpenAlex (all + IFAC-PapersOnLine ISSN filter), arXiv API, Semantic Scholar bulk search,
Crossref (PSE Press prefix 10.69997, keyword form of each query). Window: WINDOW_START .. SEARCH_DATE.

Every query is logged to logs/search_queries.csv (date, source, query, total hits reported, retrieved).
All hits -> logs/search_update_hits.csv. Raw responses cached under logs/raw_search/<source>/.
De-duplicated hits that pass the keyword pre-filter and were NOT in the 14 Oct screening record
-> corpus/new_candidates.csv (to be title/abstract screened).
"""
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz, process

from common import (CORPUS, LOGS, RAW, SEARCH_DATE, WINDOW_START, PRIOR_SEARCH_DATE, SEED_XLSX, get,
                    norm_doi, norm_title, prefilter, arxiv_id_from_doi)

IFAC_ISSN = "2405-8963"
PSE_PREFIX = "10.69997"
SEEDS = {  # forward citation chasing; DOIs of the core seeds named in the brief §4.3
    "Vyas & Mercangoz 2025 (IFAC)": "10.1016/j.ifacol.2025.07.170",
    "Vyas & Mercangoz 2025 (arXiv version)": "10.48550/arxiv.2411.05904",
    "Vyas et al. 2026 (JPC 103855)": "10.1016/j.jprocont.2026.103855",
    "Vyas et al. 2026 (arXiv version)": "10.48550/arxiv.2606.28011",
    "FaultExplainer (CCE 109152)": "10.1016/j.compchemeng.2025.109152",
    "Kevian et al. 2024": "10.48550/arxiv.2404.03647",
    "LLM4PLC": "10.1145/3639477.3639743",
    "LLM4PLC (arXiv version)": "10.48550/arxiv.2401.05443",
    "Shu et al. 2026": "10.48550/arxiv.2606.11015",
    "Rosenthal 2026": "10.48550/arxiv.2607.27849",
    "Nogueira & Skogestad 2026": "10.48550/arxiv.2606.30877",
}
SEED_TITLES = {"Kevian et al. 2024": "Capabilities of Large Language Models in Control Engineering",
               "LLM4PLC": "LLM4PLC: Harnessing Large Language Models for Verifiable Programming of PLCs"}

QLOG, HITS = [], []


def cache(source, key, fn, text=False):
    d = RAW / source
    d.mkdir(parents=True, exist_ok=True)
    p = d / (re.sub(r"[^A-Za-z0-9._-]", "_", key)[:180] + (".xml" if text else ".json"))
    if p.exists():
        return p.read_text() if text else json.loads(p.read_text())
    data = fn()
    if data is None:  # do not cache failures, so a re-run retries them
        return None
    p.write_text(data if text else json.dumps(data))
    return data


def log_query(source, query, total, retrieved, note=""):
    QLOG.append({"date": SEARCH_DATE, "source": source, "query": query, "total_hits_reported": total,
                 "retrieved": retrieved, "note": note})
    print(f"[{source}] {total} hits, {retrieved} kept :: {query[:90]}", flush=True)


def hit(source, query, title, doi="", year="", date="", venue="", abstract="", arxiv_id="", ext_id=""):
    HITS.append({"source": source, "query": query, "title": title or "", "doi": norm_doi(doi), "year": year,
                 "pub_date": date, "venue": venue or "", "abstract": abstract or "", "arxiv_id": arxiv_id,
                 "ext_id": ext_id})


# ---------- OpenAlex ----------
def inv_abs(inv):
    if not inv:
        return ""
    return " ".join(w for _, w in sorted((p, w) for w, ps in inv.items() for p in ps))


def openalex(query, extra_filter="", label="OpenAlex", n=200):
    flt = f"from_publication_date:{WINDOW_START},to_publication_date:{SEARCH_DATE}" + extra_filter
    key = f"{label}_{query}_{flt}"

    def f():
        r = get("https://api.openalex.org/works", params={"search": query, "filter": flt, "per_page": n})
        return r.json() if r is not None and r.status_code == 200 else None
    data = cache("openalex_search", key, f)
    if data is None:
        log_query(label, query, "ERROR", 0, "request failed")
        return
    res = data.get("results", [])
    log_query(label, query, data.get("meta", {}).get("count", ""), len(res), f"filter={flt}; top {n} by relevance")
    for w in res:
        loc = (w.get("primary_location") or {}).get("source") or {}
        hit(label, query, w.get("display_name"), w.get("doi") or "", w.get("publication_year"),
            w.get("publication_date"), loc.get("display_name"), inv_abs(w.get("abstract_inverted_index")),
            ext_id=w.get("id", "").rsplit("/", 1)[-1])


def openalex_cites(label, wid):
    out, cursor, total = [], "*", ""
    while cursor:
        def f(c=cursor):
            r = get("https://api.openalex.org/works", params={"filter": f"cites:{wid}", "per_page": 200, "cursor": c})
            return r.json() if r is not None and r.status_code == 200 else None
        data = cache("openalex_cites", f"{wid}_{cursor[:40]}_{SEARCH_DATE}", f)
        if data is None:
            if not out:
                log_query("OpenAlex citations", f"forward citations of {label} ({wid})", "ERROR", 0, "request failed")
                return
            break
        total = data.get("meta", {}).get("count", "")
        out += data.get("results", [])
        cursor = data.get("meta", {}).get("next_cursor")
    q = f"forward citations of {label} ({wid})"
    log_query("OpenAlex citations", q, total, len(out), "all citing works, no date filter")
    for w in out:
        loc = (w.get("primary_location") or {}).get("source") or {}
        hit("OpenAlex citations", q, w.get("display_name"), w.get("doi") or "", w.get("publication_year"),
            w.get("publication_date"), loc.get("display_name"), inv_abs(w.get("abstract_inverted_index")),
            ext_id=w.get("id", "").rsplit("/", 1)[-1])


def openalex_id(doi="", title=""):
    if doi:
        r = get(f"https://api.openalex.org/works/doi:{doi}", ok=(200, 404))
        if r is not None and r.status_code == 200:
            return r.json()["id"].rsplit("/", 1)[-1]
    if title:
        r = get("https://api.openalex.org/works", params={"search": title, "per_page": 5})
        for w in (r.json().get("results", []) if r is not None and r.status_code == 200 else []):
            if fuzz.ratio(norm_title(title), norm_title(w.get("display_name"))) >= 90:
                return w["id"].rsplit("/", 1)[-1]
    return ""


# ---------- arXiv ----------
def to_arxiv(q):
    """Prefix every term or quoted phrase with all: (the Boolean strings contain no NOT)."""
    term = lambda m: m.group(0) if m.group(0) in ("AND", "OR") else "all:" + m.group(0)
    q = re.sub(r'"[^"]+"|\bAND\b|\bOR\b|[A-Za-z0-9\-]+', term, q)
    return f"({q}) AND submittedDate:[{WINDOW_START.replace('-', '')}0000 TO {SEARCH_DATE.replace('-', '')}2359]"


def arxiv(query, n=200):
    sq = to_arxiv(query)

    def f():
        r = get("https://export.arxiv.org/api/query", params={"search_query": sq, "max_results": n,
                                                              "sortBy": "relevance"}, timeout=120)
        time.sleep(3.1)
        return r.text if r is not None and r.status_code == 200 else None
    txt = cache("arxiv_search", f"{query}_{SEARCH_DATE}", f, text=True)
    if not txt:
        log_query("arXiv", sq, "ERROR", 0, "request failed")
        return
    ns = {"a": "http://www.w3.org/2005/Atom", "os": "http://a9.com/-/spec/opensearch/1.1/",
          "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(txt)
    entries = root.findall("a:entry", ns)
    log_query("arXiv", sq, root.findtext("os:totalResults", default="", namespaces=ns), len(entries),
              f"top {n} by relevance")
    for e in entries:
        aid = re.sub(r"v\d+$", "", (e.findtext("a:id", default="", namespaces=ns)).rsplit("/abs/", 1)[-1])
        pub = e.findtext("a:published", default="", namespaces=ns)[:10]
        jdoi = e.findtext("arxiv:doi", default="", namespaces=ns) or ""
        hit("arXiv", query, re.sub(r"\s+", " ", e.findtext("a:title", default="", namespaces=ns)).strip(),
            jdoi or f"10.48550/arxiv.{aid}", pub[:4], pub, "arXiv",
            re.sub(r"\s+", " ", e.findtext("a:summary", default="", namespaces=ns)).strip(), arxiv_id=aid)


# ---------- Semantic Scholar ----------
def s2(query, cap=1000):
    sq = query.replace(" AND ", " + ").replace(" OR ", " | ")
    y0, y1 = WINDOW_START[:4], SEARCH_DATE[:4]

    def f():
        time.sleep(1.5)
        r = get("https://api.semanticscholar.org/graph/v1/paper/search/bulk",
                params={"query": sq, "year": f"{y0}-{y1}", "fields": "title,externalIds,year,publicationDate,venue,abstract"},
                tries=8)
        return r.json() if r is not None and r.status_code == 200 else None
    data = cache("s2_search", f"{query}_{SEARCH_DATE}", f)
    if data is None:
        log_query("Semantic Scholar", sq, "ERROR", 0, "request failed (rate limit)")
        return
    res = (data.get("data") or [])[:cap]
    log_query("Semantic Scholar", sq, data.get("total", ""), len(res),
              f"bulk boolean search, year {y0}-{y1}, first {cap}")
    for p in res:
        ids = p.get("externalIds") or {}
        doi = ids.get("DOI") or (f"10.48550/arxiv.{ids['ArXiv']}" if ids.get("ArXiv") else "")
        date = p.get("publicationDate") or ""
        if date and date < WINDOW_START:
            continue
        hit("Semantic Scholar", query, p.get("title"), doi, p.get("year"), date, p.get("venue"),
            p.get("abstract"), arxiv_id=ids.get("ArXiv", ""), ext_id=p.get("paperId", ""))


def s2_cites(label, doi):
    pid = f"ARXIV:{arxiv_id_from_doi(doi)}" if arxiv_id_from_doi(doi) else f"DOI:{doi}"

    def f():
        time.sleep(1.5)
        r = get(f"https://api.semanticscholar.org/graph/v1/paper/{pid}/citations",
                params={"fields": "title,externalIds,year,publicationDate,venue,abstract", "limit": 1000}, tries=8)
        return r.json() if r is not None and r.status_code == 200 else None
    data = cache("s2_cites", f"{pid}_{SEARCH_DATE}", f)
    q = f"forward citations of {label} ({pid})"
    if data is None:
        log_query("Semantic Scholar citations", q, "ERROR", 0, "request failed")
        return
    res = [c.get("citingPaper") or {} for c in data.get("data") or []]
    log_query("Semantic Scholar citations", q, len(res), len(res), "all citing papers (max 1000)")
    for p in res:
        ids = p.get("externalIds") or {}
        d = ids.get("DOI") or (f"10.48550/arxiv.{ids['ArXiv']}" if ids.get("ArXiv") else "")
        hit("Semantic Scholar citations", q, p.get("title"), d, p.get("year"), p.get("publicationDate") or "",
            p.get("venue"), p.get("abstract"), arxiv_id=ids.get("ArXiv", ""), ext_id=p.get("paperId", ""))


# ---------- Crossref ----------
def keywords(q):
    return re.sub(r"\s+", " ", re.sub(r'\bAND\b|\bOR\b|\bNOT\b|[()"]', " ", q)).strip()


def crossref(query, prefix="", n=100):
    kw = keywords(query)
    url = f"https://api.crossref.org/prefixes/{prefix}/works" if prefix else "https://api.crossref.org/works"
    flt = f"from-pub-date:{WINDOW_START},until-pub-date:{SEARCH_DATE}"
    label = "Crossref (PSE Press 10.69997)" if prefix else "Crossref"

    def f():
        r = get(url, params={"query.bibliographic": kw, "filter": flt, "rows": n,
                             "select": "DOI,title,issued,container-title,abstract,type"})
        return r.json() if r is not None and r.status_code == 200 else None
    data = cache("crossref", f"{label}_{kw}_{SEARCH_DATE}", f)
    if data is None:
        log_query(label, kw, "ERROR", 0, "request failed")
        return
    m = data.get("message", {})
    items = m.get("items", [])
    log_query(label, kw, m.get("total-results", ""), len(items),
              f"keyword relevance (Crossref has no Boolean); {flt}; top {n}")
    for it in items:
        dp = ((it.get("issued") or {}).get("date-parts") or [[None]])[0]
        hit(label, query, (it.get("title") or [""])[0], it.get("DOI"), dp[0] if dp else "",
            "-".join(str(x) for x in dp if x), (it.get("container-title") or [""])[0],
            re.sub(r"<[^>]+>", " ", it.get("abstract") or ""))


# ---------- main ----------
def boolean_queries():
    s = pd.read_csv(LOGS / "search_log_20261014.csv")
    qs = s[s["Source"].str.startswith("Database")]["Query string"].tolist()
    # keep the explicit Boolean strings (1–32); the title-anchored rows (33–51) did not record their title word
    qs = [q for q in qs if " AND " in q and not q.startswith("(LLM OR LLMs OR \"large language model\" OR \"large language models\" OR agentic)")]
    return list(dict.fromkeys(qs))


def screened_index():
    x = pd.ExcelFile(SEED_XLSX)
    frames = []
    for sh in ["Included studies", "Reviews & perspectives", "Adjacent (not included)",
               "Excluded at title-abstract", "Excluded by keyword filter"]:
        d = pd.read_excel(x, sh)
        frames.append(pd.DataFrame({"doi": d["DOI"].map(norm_doi), "ntitle": d["Title"].map(norm_title), "sheet": sh}))
    return pd.concat(frames, ignore_index=True)


def main():
    qs = boolean_queries()
    print(len(qs), "Boolean queries")
    only = set(sys.argv[1:])  # optional: run a subset of sources, e.g. `openalex arxiv`
    run = lambda s: not only or s in only
    for q in qs:
        if run("openalex"):
            openalex(q)
            openalex(q, f",primary_location.source.issn:{IFAC_ISSN}", label="OpenAlex (IFAC-PapersOnLine)")
        if run("arxiv"):
            arxiv(q)
        if run("s2"):
            s2(q)
        if run("crossref"):
            crossref(q, prefix=PSE_PREFIX)
    if run("cites"):
        for label, doi in SEEDS.items():
            wid = openalex_id(doi, SEED_TITLES.get(label, ""))
            if wid:
                openalex_cites(label, wid)
            else:
                log_query("OpenAlex citations", f"forward citations of {label}", "ERROR", 0, "seed not resolved")
            if doi:
                s2_cites(label, doi)

    pd.DataFrame(QLOG).to_csv(LOGS / "search_queries.csv", index=False)
    h = pd.DataFrame(HITS)
    h.to_csv(LOGS / "search_update_hits.csv", index=False)

    # de-duplicate hits: DOI (arXiv DOIs map to their arXiv id), then normalized title
    h["ntitle"] = h["title"].map(norm_title)
    h["key"] = h["doi"].where(h["doi"] != "", "t:" + h["ntitle"])
    agg = h.groupby("key").agg(title=("title", "first"), doi=("doi", "first"), year=("year", "first"),
                               pub_date=("pub_date", "max"), venue=("venue", "first"),
                               abstract=("abstract", lambda s: max(s, key=len)), arxiv_id=("arxiv_id", "max"),
                               ntitle=("ntitle", "first"),
                               sources=("source", lambda s: "; ".join(sorted(set(s)))),
                               n_queries=("query", "nunique")).reset_index(drop=True)
    agg = agg.drop_duplicates("ntitle")
    agg["prefilter"] = [prefilter(t, a) for t, a in zip(agg["title"], agg["abstract"])]

    scr = screened_index()
    sdois = set(scr["doi"]) - {""}
    stitles = scr["ntitle"].tolist()
    prev = []
    for d, t in zip(agg["doi"], agg["ntitle"]):
        if d and d in sdois:
            prev.append("doi")
            continue
        m = process.extractOne(t, stitles, scorer=fuzz.ratio, score_cutoff=93) if t else None
        prev.append("title" if m else "")
    agg["in_20261014_record"] = prev
    agg["after_prior_search"] = agg["pub_date"].astype(str) > PRIOR_SEARCH_DATE
    agg.to_csv(LOGS / "search_update_unique.csv", index=False)
    new = agg[(agg["in_20261014_record"] == "") & agg["prefilter"]]
    new.to_csv(CORPUS / "new_candidates.csv", index=False)
    print(f"hits {len(h)} | unique {len(agg)} | pass prefilter {agg.prefilter.sum()} | "
          f"not in 14 Oct record & pass prefilter {len(new)} (published after {PRIOR_SEARCH_DATE}: "
          f"{new.after_prior_search.sum()})")


if __name__ == "__main__":
    main()
