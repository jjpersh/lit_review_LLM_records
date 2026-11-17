#!/usr/bin/env python3
"""Build page-tagged digests (abstract + criterion-relevant sentences) for core papers to score. Run from lit_review_LLM/."""
import csv
import os
import re
import subprocess
import sys

IDS = sys.argv[1].split(',')
OUT = 'focused_review/digests'
os.makedirs(OUT, exist_ok=True)
rows = {r['rec_id']: r for r in csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline=''))}
PAT = re.compile(
    r'(gpt-?\d|gpt-4o|llama|qwen|claude|gemini|mistral|deepseek|gemma|phi-\d|ollama|open-weight|temperature|top-p|seed|'
    r'latenc|inference time|response time|second|sampling (time|interval|period)|'
    r'baseline|compared (with|to|against)|outperform|ziegler|relay|tuned|ablation|without the (llm|agent)|'
    r'\biae\b|\bise\b|overshoot|settling|rise time|tracking error|constraint violation|energy|'
    r'disturbance|fault|noise|mismatch|uncertain|robust|'
    r'repeat|runs\b|trials\b|variance|standard deviation|confidence interval|'
    r'success rate|accuracy|correct|invalid|hallucinat|unsafe|fail|'
    r'safety|guard|gate|fallback|verif|approv|human-in-the-loop|operator|'
    r'hardware|physical|testbed|simulat|plant data|industrial|real-time|'
    r'limitation|future work|conclusion)', re.I)
for rid in IDS:
    r = rows[rid]
    pdf = r['pdf']
    if not pdf or not os.path.exists(pdf):
        print('NO PDF', rid)
        continue
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    pages = []
    for p in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True).stdout.decode('utf-8', 'replace')
        pages.append(re.sub(r'\s+', ' ', t))
    full = ' '.join(pages)
    cut = re.search(r'\b(References|REFERENCES|Bibliography)\b', full[len(full) // 2:])
    stop_page = n
    if cut:
        pos = len(full) // 2 + cut.start()
        acc = 0
        for i, pg in enumerate(pages):
            acc += len(pg) + 1
            if acc >= pos:
                stop_page = i + 1
                break
    head = pages[0][:1600]
    hits, seen = [], set()
    for i, pg in enumerate(pages[:stop_page], 1):
        for sent in re.split(r'(?<=[.!?])\s+', pg):
            if 40 < len(sent) < 600 and PAT.search(sent):
                key = sent[:70]
                if key not in seen:
                    seen.add(key)
                    hits.append(f'[p{i}] {sent}')
    body = '\n'.join(hits)
    if len(body) > 4200:
        # keep a spread: prioritize results/discussion pages by sampling evenly
        step = len(hits) / (4200 / (len(body) / len(hits)))
        body = '\n'.join(hits[int(k * step)] for k in range(int(len(hits) / step)))
    with open(f'{OUT}/{rid}.txt', 'w', encoding='utf-8') as f:
        f.write(f"### {rid} | {r['first_author']} {r['year']} | {r['title']}\nvenue: {r['venue']} | theme {r['theme']} | pages {n} (refs from p{stop_page})\n"
                f"--- PAGE 1 HEAD ---\n{head}\n--- KEY SENTENCES ---\n{body}\n")
    print(rid, n, 'pages', len(head) + len(body), 'chars')
