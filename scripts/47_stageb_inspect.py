#!/usr/bin/env python3
"""Stage B helper (2026-11-13): print map usage and the new papers' key fields, to write synth_maps entries."""
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from synth_maps import S  # noqa: E402

NEW = 'S019 S026 S031 S033 S036 S039 S043 S205 S239 S264 S269 S302 T0608 T0615 T1044'.split()
print(collections.Counter(v['domain'] for v in S.values()))
print(collections.Counter(v['layer'] for v in S.values()))
print(collections.Counter(v['safe'][0] for v in S.values() if v['safe']))
scr = {r['rec_id']: r for r in csv.DictReader(open('focused_review/screening.csv'))}
k = collections.Counter()
for r in csv.DictReader(open('extraction/extraction.csv')):
    k[r['rec_id']] += 1
    if r['rec_id'] not in NEW:
        continue
    s = scr[r['rec_id']]
    if k[r['rec_id']] == 1:
        print(f"\n### {r['rec_id']} theme={s['theme']} {s['first_author']} {s['year']}")
    print(f"{r['rec_id']}.{k[r['rec_id']]} | {r['setup']} | {r['evidence']} {r['authority']} C1={r['C1']} C6={r['C6']}")
    if len(sys.argv) > 1:
        print(f"   C1: {r['C1_note']}\n   C6: {r['C6_note']}\n   KR: {r['key_result']}\n   lat: {r['llm_latency']} | loop: {r['loop_timing']} | plant: {r['plant_timing']} | model: {r['llm_model']}")
