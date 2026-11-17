"""Stage A.5 — download open-access full texts for corpus/metadata.csv into corpus/pdfs/.

Candidate URLs, in order: arXiv PDF (own arXiv id, recorded arXiv version, or an arXiv copy found by exact-title
search — author versions are a legitimate OA route), OpenAlex best OA PDF,
every other OpenAlex PDF location, MDPI/PSE Press direct patterns. A file is kept only if it is a real PDF
(%PDF header, opens in pypdf) whose first pages contain most of the title words. Nothing behind a paywall is
attempted beyond what the publisher serves openly.

Writes the columns fulltext_file / fulltext_source / fulltext_status back into corpus/metadata.csv and lists every
record without full text in corpus/missing_fulltext.csv (DOI, publisher, reason) for library retrieval.
Re-runnable: existing valid files are kept.
"""
import io
import re
import sys
import time
import unicodedata

import pandas as pd
from pypdf import PdfReader

from rapidfuzz import fuzz

from common import CORPUS, RAW, SESSION, get, norm_title

PDFS = CORPUS / "pdfs"
PDFS.mkdir(parents=True, exist_ok=True)
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
STOP = set("a an the of for and in on with to via using based by from as at into is are its large language model models llm llms".split())


def slug(s, n=4):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    words = [w for w in re.findall(r"[A-Za-z0-9]+", s) if w.lower() not in STOP]
    return "".join(w.capitalize() for w in words[:n]) or "Untitled"


def filename(r):
    last = re.split(r"[;,]", str(r.get("first_author") or "Anon"))[0].strip().split()[-1:] or ["Anon"]
    return f"{slug(last[0], 1)}{str(r.get('year') or '')[:4]}_{slug(r['title'])}.pdf"


def arxiv_by_title(title):
    """arXiv id of a paper with a near-identical title (ratio >= 92), cached; '' if none."""
    p = RAW / "arxiv_title" / (re.sub(r"[^a-z0-9]+", "_", norm_title(title))[:150] + ".xml")
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        words = " AND ".join([f"ti:{w}" for w in norm_title(title).split() if w not in STOP and len(w) > 2][:10])
        r = get("https://export.arxiv.org/api/query", params={"search_query": words, "max_results": 5})
        time.sleep(3.1)
        if r is None or r.status_code != 200:
            return ""
        p.write_text(r.text)
    for m in re.finditer(r"<entry>.*?<id>http://arxiv.org/abs/([^<]+?)(v\d+)?</id>.*?<title>(.*?)</title>", p.read_text(), re.S):
        if fuzz.ratio(norm_title(title), norm_title(re.sub(r"\s+", " ", m.group(3)))) >= 92:
            return m.group(1)
    return ""


def candidate_urls(r):
    urls = []
    ids = [r.get("arxiv_id"), *str(r.get("other_arxiv_ids") or "").split(";")]
    if not any(str(a).strip() for a in ids):
        ids.append(arxiv_by_title(r["title"]))
    for aid in ids:
        aid = str(aid or "").strip()
        if aid:
            urls.append(("arXiv", f"https://arxiv.org/pdf/{aid}"))
    if r.get("best_oa_pdf"):
        urls.append(("OpenAlex best OA", r["best_oa_pdf"]))
    for u in str(r.get("all_pdf_urls") or "").split(" | "):
        if u.strip():
            urls.append(("OpenAlex OA location", u.strip()))
    doi = str(r.get("doi") or "")
    if doi.startswith("10.3390/"):  # MDPI: the DOI landing page plus /pdf serves the PDF
        urls.append(("MDPI", f"https://doi.org/{doi}"))
    if doi.startswith("10.69997/"):  # PSE Press
        urls.append(("PSE Press", f"https://doi.org/{doi}"))
    seen, out = set(), []
    for s, u in urls:
        if u not in seen:
            seen.add(u)
            out.append((s, u))
    return out


def fetch_pdf(url):
    try:
        r = SESSION.get(url, headers={"User-Agent": BROWSER_UA, "Accept": "application/pdf,*/*"},
                        timeout=90, allow_redirects=True)
    except Exception as e:
        return None, f"error {type(e).__name__}"
    if r.status_code != 200:
        return None, f"http {r.status_code}"
    body = r.content
    if not body.startswith(b"%PDF"):
        # MDPI / PSE Press landing pages: follow a direct PDF link if one is on the page
        m = re.search(rb'href="([^"]+?(?:/pdf(?:\?[^"]*)?|\.pdf))"', body)
        if m and ("mdpi.com" in r.url or "psecommunity" in r.url or "lapse" in r.url):
            link = m.group(1).decode()
            if link.startswith("/"):
                link = re.match(r"https?://[^/]+", r.url).group(0) + link
            return fetch_pdf(link) if link != url else (None, "landing page loop")
        return None, "not a PDF (landing page or block)"
    return body, "ok"


def check_pdf(body, title):
    try:
        rd = PdfReader(io.BytesIO(body))
        text = " ".join((rd.pages[i].extract_text() or "") for i in range(min(2, len(rd.pages))))
    except Exception:
        return False, "unreadable PDF"
    words = [w for w in norm_title(title).split() if w not in STOP and len(w) > 2]
    if not words:
        return True, "ok"
    page = norm_title(text)
    frac = sum(w in page for w in words) / len(words)
    return (frac >= 0.6), f"title-word match {frac:.0%}"


def access(r):
    """What the user has to do to get this full text."""
    if not r["doi"]:
        return "no DOI: find via repository/title"
    if str(r["is_oa"]) == "True":
        return "open access but blocked to scripts: download in a browser (free)"
    return "not open access: BYU library"


def main():
    retry = "--no-retry" not in sys.argv  # --no-retry: only rewrite missing_fulltext.csv, skip earlier misses
    md = pd.read_csv(CORPUS / "metadata.csv", keep_default_na=False)
    for col in ("fulltext_file", "fulltext_source", "fulltext_status"):
        if col not in md:
            md[col] = ""
    for i, r in md.iterrows():
        fn = r["fulltext_file"] or filename(r)
        if (PDFS / fn).exists():
            md.at[i, "fulltext_file"], md.at[i, "fulltext_status"] = fn, "have"
            continue
        if not retry and r["fulltext_status"] == "missing":
            continue
        tried = []
        for src, url in candidate_urls(r):
            body, why = fetch_pdf(url)
            time.sleep(1.0)
            if body is None:
                tried.append(f"{src}: {why}")
                continue
            ok, why = check_pdf(body, r["title"])
            if not ok:
                tried.append(f"{src}: rejected ({why})")
                continue
            (PDFS / fn).write_bytes(body)
            md.at[i, "fulltext_file"], md.at[i, "fulltext_source"] = fn, f"{src} {url}"
            md.at[i, "fulltext_status"] = "have"
            break
        else:
            md.at[i, "fulltext_status"] = "missing"
            md.at[i, "fulltext_source"] = " || ".join(tried) if tried else "no open-access location known"
        print(i, md.at[i, "fulltext_status"], r["title"][:70], flush=True)

    md.to_csv(CORPUS / "metadata.csv", index=False)
    miss = md[md["fulltext_status"] != "have"].copy()
    miss["access"] = [access(r) for _, r in miss.iterrows()]
    miss = miss.sort_values(["access", "role_provisional"])
    miss[["rec_id", "access", "first_author", "year", "title", "doi", "publisher", "venue", "pub_status", "role_provisional",
          "fulltext_source"]].rename(columns={"fulltext_source": "attempts_or_reason"}).to_csv(
        CORPUS / "missing_fulltext.csv", index=False)
    print(f"have {len(md) - len(miss)} / {len(md)}; missing {len(miss)}")


if __name__ == "__main__":
    main()
