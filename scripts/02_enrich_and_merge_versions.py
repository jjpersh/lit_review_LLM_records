"""Stage A.2 — enrich seed records via OpenAlex (abstract, date, OA locations, ids) and detect
preprint -> published versions (OpenAlex title search + arXiv API journal DOI).

Writes corpus/seed_enriched.csv and logs/version_merges.csv. Responses are cached in logs/raw_search/openalex/.
"""
import json
import re
import time
import xml.etree.ElementTree as ET

import pandas as pd
from rapidfuzz import fuzz

from common import CORPUS, LOGS, RAW, get, norm_doi, norm_title, is_preprint_doi, arxiv_id_from_doi

OA = "https://api.openalex.org"
CACHE = RAW / "openalex"
CACHE.mkdir(parents=True, exist_ok=True)


def cached(key, fn):
    p = CACHE / (re.sub(r"[^A-Za-z0-9._-]", "_", key)[:180] + ".json")
    if p.exists():
        return json.loads(p.read_text())
    data = fn()
    p.write_text(json.dumps(data))
    return data


def oa_by_doi(doi):
    def f():
        r = get(f"{OA}/works/doi:{doi}", ok=(200, 404))
        return r.json() if r is not None and r.status_code == 200 else None
    return cached(f"doi_{doi}", f)


def oa_title_search(title):
    def f():
        r = get(f"{OA}/works", params={"search": title[:250], "per_page": 10})
        return r.json().get("results", []) if r is not None and r.status_code == 200 else []
    return cached(f"ts_{norm_title(title)[:150]}", f)


def abstract_from_inverted(inv):
    if not inv:
        return ""
    pos = [(p, w) for w, ps in inv.items() for p in ps]
    return " ".join(w for _, w in sorted(pos))


def arxiv_meta(aid):
    p = RAW / "arxiv_meta" / f"{aid.replace('/', '_')}.xml"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        r = get("https://export.arxiv.org/api/query", params={"id_list": aid})
        time.sleep(3)
        p.write_text(r.text if r is not None else "")
    txt = p.read_text()
    if not txt:
        return {}
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    try:
        e = ET.fromstring(txt).find("a:entry", ns)
    except ET.ParseError:
        return {}
    if e is None:
        return {}
    g = lambda tag: (e.findtext(tag, default="", namespaces=ns) or "").strip()
    return {"journal_doi": norm_doi(g("arxiv:doi")), "journal_ref": g("arxiv:journal_ref"),
            "published": g("a:published")[:10], "abstract": re.sub(r"\s+", " ", g("a:summary"))}


def oa_fields(w):
    if not w:
        return {}
    best = w.get("best_oa_location") or {}
    locs = w.get("locations") or []
    pdfs = [l.get("pdf_url") for l in locs if l.get("pdf_url")]
    return {
        "openalex_id": w.get("id", "").rsplit("/", 1)[-1],
        "pub_date": w.get("publication_date") or "",
        "oa_status": (w.get("open_access") or {}).get("oa_status", ""),
        "is_oa": (w.get("open_access") or {}).get("is_oa", False),
        "best_oa_pdf": best.get("pdf_url") or "",
        "best_oa_landing": best.get("landing_page_url") or "",
        "all_pdf_urls": " | ".join(dict.fromkeys(pdfs)),
        "publisher": ((w.get("primary_location") or {}).get("source") or {}).get("host_organization_name") or "",
        "venue_oa": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
        "oa_type": w.get("type", ""),
        "abstract_oa": abstract_from_inverted(w.get("abstract_inverted_index")),
        "authors_oa": "; ".join(a["author"]["display_name"] for a in (w.get("authorships") or [])[:6]),
        "cited_by_count": w.get("cited_by_count", ""),
    }


def find_published_version(title, preprint_doi):
    """Return (doi, how) of a peer-reviewed version with near-identical title, else ("", "")."""
    nt = norm_title(title)
    for w in oa_title_search(title):
        d = norm_doi(w.get("doi") or "")
        if not d or d == preprint_doi or is_preprint_doi(d):
            continue
        if w.get("type") not in ("article", "proceedings-article", "book-chapter"):
            continue
        if fuzz.ratio(nt, norm_title(w.get("display_name") or "")) >= 92:
            return d, "openalex_title_match"
    return "", ""


def main():
    df = pd.read_csv(CORPUS / "seed_records.csv", keep_default_na=False)
    enrich, merges = [], []
    for i, r in df.iterrows():
        doi = r["doi"]
        e = oa_fields(oa_by_doi(doi))
        pub_doi, how = "", ""
        if is_preprint_doi(doi):
            aid = arxiv_id_from_doi(doi)
            if aid:
                am = arxiv_meta(aid)
                if am.get("journal_doi") and not is_preprint_doi(am["journal_doi"]):
                    pub_doi, how = am["journal_doi"], "arxiv_journal_doi"
                if not e.get("abstract_oa") and am.get("abstract"):
                    e["abstract_oa"] = am["abstract"]
                e.setdefault("pub_date", am.get("published", ""))
                e["arxiv_id"] = aid
            if not pub_doi:
                pub_doi, how = find_published_version(r["title"], doi)
        if pub_doi:
            merges.append({"title": r["title"], "preprint_doi": doi, "published_doi": pub_doi, "how": how})
        e["published_version_doi"] = pub_doi
        enrich.append(e)
        if i % 25 == 0:
            print(i, flush=True)
    out = pd.concat([df, pd.DataFrame(enrich)], axis=1)
    out.to_csv(CORPUS / "seed_enriched.csv", index=False)
    pd.DataFrame(merges).to_csv(LOGS / "version_merges.csv", index=False)
    print("enriched", len(out), "| openalex hits", out["openalex_id"].astype(bool).sum(),
          "| preprint->published found", len(merges))


if __name__ == "__main__":
    main()
