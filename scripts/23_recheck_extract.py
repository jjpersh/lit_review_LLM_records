#!/usr/bin/env python3
"""Pull repeat/reproducibility, timing and conclusion text from full PDFs for the C4/outcome recheck. Run from lit_review_LLM/."""
import csv
import os
import re
import subprocess
import sys

IDS = sys.argv[1].split(',')
scr = {r['rec_id']: r for r in csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline=''))}
ext = {}
for r in csv.DictReader(open('extraction/extraction.csv', encoding='utf-8', newline='')):
    ext.setdefault(r['rec_id'], []).append(r)
REP = re.compile(r'(repeat|repetition|\bseeds?\b|\bruns?\b|\btrials?\b|independent|monte carlo|variance|standard deviation|\bstd\b|±|confidence interval|'
                 r'temperature\s*(=|of|set|0)|top-p|prompt (is|was|template)|appendix|github|code (is|are) available|released)', re.I)
TIM = re.compile(r'(latenc|inference time|response time|wall.?clock|\bms\b|millisecond|seconds? per|per (call|query|step|cycle)|sampling (time|interval|period|rate)|update interval|real.?time)', re.I)
os.makedirs('focused_review/recheck', exist_ok=True)
for rid in IDS:
    pdf = scr[rid]['pdf']
    pages = []
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    for p in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True).stdout.decode('utf-8', 'replace')
        pages.append(re.sub(r'\s+', ' ', t))
    full = ' '.join(pages)
    ref = re.search(r'\b(References|REFERENCES|Bibliography)\b', full[len(full) // 2:])
    end_char = len(full) // 2 + ref.start() if ref else len(full)
    rep, tim, seen, acc = [], [], set(), 0
    for i, pg in enumerate(pages, 1):
        if acc > end_char:
            break
        acc += len(pg) + 1
        for s in re.split(r'(?<=[.!?])\s+', pg):
            if 30 < len(s) < 450 and s[:60] not in seen:
                if REP.search(s):
                    rep.append(f'[p{i}] {s}'); seen.add(s[:60])
                elif TIM.search(s):
                    tim.append(f'[p{i}] {s}'); seen.add(s[:60])
    body = full[:end_char]
    m = None
    for m in re.finditer(r'\b(\d+\.?\s*)?(Conclusions?|CONCLUSIONS?|Concluding remarks)\b', body):
        pass
    concl = body[m.start():m.start() + 1500] if m else body[-1500:]
    saved = ' || '.join(f"{r['setup'][:60]} => outcome {r['outcome']}, C4 {r['C4']} ({r['C4_note'][:70]})" for r in ext[rid])
    txt = (f"### {rid} | {scr[rid]['first_author']} {scr[rid]['year']} | {scr[rid]['title'][:90]}\nSAVED: {saved}\n"
           f"--- REPEAT/REPRO ---\n" + '\n'.join(rep[:14])[:1700] + f"\n--- TIMING ---\n" + '\n'.join(tim[:6])[:700] +
           f"\n--- CONCLUSION ---\n{concl}\n")
    open(f'focused_review/recheck/{rid}.txt', 'w', encoding='utf-8').write(txt)
    print(rid, len(txt))
