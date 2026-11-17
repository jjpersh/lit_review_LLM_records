#!/usr/bin/env python3
"""Prepare a clean, page-marked text file for each core paper, so a reader loads a paper in one or two steps.

For each rec_id (default: every core paper with a PDF in focused_review/screening.csv):
  - pdftotext (reading order) split by page, each page headed by a [p.N] marker
  - running headers/footers removed (lines repeated on at least half the pages)
  - words hyphenated across line ends rejoined, runs of blank lines collapsed
  - the reference list removed (kept separately in <rec_id>.refs.txt); appendices after it are kept
Writes focused_review/fullread/clean/<rec_id>.txt and prints a one-line summary per paper.
Usage: .venv/bin/python -I scripts/41_prep_text.py [REC_ID ...]
"""
import collections
import csv
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "focused_review", "fullread", "clean")
REF_HEAD = re.compile(r"^\s*(\d+\.?\s*)?(references|bibliography|literature cited|reference list)\s*:?\s*$", re.I)
APPX_HEAD = re.compile(r"^\s*(appendix|appendices|supplementary (material|information)|supporting information)\b", re.I)


def pdf_pages(pdf):
    txt = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf, "-"], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout
    pages = txt.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    return pages


def norm(line):
    return re.sub(r"\d+", "#", line.strip().lower())


def clean(pages):
    counts = collections.Counter()
    for p in pages:
        counts.update({norm(l) for l in p.splitlines() if 0 < len(l.strip()) < 120})
    repeated = {k for k, c in counts.items() if len(pages) >= 4 and c >= len(pages) / 2 and k not in ("#", "")}
    out = []
    for i, p in enumerate(pages, 1):
        lines = [l.rstrip() for l in p.splitlines() if norm(l) not in repeated and not re.fullmatch(r"\s*\d{1,3}\s*", l)]
        body = "\n".join(lines)
        body = re.sub(r"(\w)-\n(\w)", r"\1\2", body)
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        out.append((i, body))
    return out


def split_refs(pages):
    """Return (kept_text, refs_text). Cut from the last reference heading in the back half to an appendix heading or the end."""
    flat = []
    for i, body in pages:
        flat.append(f"[p.{i}]")
        flat.extend(body.splitlines())
    n = len(flat)
    start = None
    for k in range(n - 1, int(n * 0.4), -1):
        if REF_HEAD.match(flat[k]):
            start = k
            break
    if start is None:
        return "\n".join(flat), ""
    end = n
    for k in range(start + 1, n):
        if APPX_HEAD.match(flat[k]):
            end = k
            break
    refs = flat[start:end]
    # keep page markers that fall inside the cut so page numbering of later text stays visible
    markers = [l for l in refs if re.fullmatch(r"\[p\.\d+\]", l)]
    kept = flat[:start] + [f"[reference list removed; see {{rec_id}}.refs.txt]"] + markers + flat[end:]
    return "\n".join(kept), "\n".join(refs)


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(ROOT, "focused_review", "screening.csv"), encoding="utf-8")))
    want = set(sys.argv[1:])
    for r in rows:
        if want and r["rec_id"] not in want:
            continue
        if not want and r["tier"] != "core":
            continue
        pdf = r.get("pdf", "")
        if pdf and not os.path.isabs(pdf):
            pdf = os.path.join(ROOT, pdf)
        if not pdf or not os.path.exists(pdf):
            print(f"{r['rec_id']}: no PDF, skipped")
            continue
        pages = pdf_pages(pdf)
        cleaned = clean(pages)
        kept, refs = split_refs(cleaned)
        kept = kept.replace("{rec_id}", r["rec_id"])
        chars_raw = sum(len(p) for p in pages)
        header = f"# {r['rec_id']}: {r['title']}\n# source PDF: {os.path.relpath(pdf, ROOT)} ({len(pages)} pages)\n\n"
        open(os.path.join(OUT, f"{r['rec_id']}.txt"), "w", encoding="utf-8").write(header + kept + "\n")
        if refs:
            open(os.path.join(OUT, f"{r['rec_id']}.refs.txt"), "w", encoding="utf-8").write(refs + "\n")
        sparse = " LOW TEXT (scanned?)" if chars_raw < 800 * max(1, len(pages)) * 0.25 else ""
        print(f"{r['rec_id']}: {len(pages)} pages, raw {chars_raw} chars, kept {len(kept)}, refs {len(refs)}{sparse}")


if __name__ == "__main__":
    main()
