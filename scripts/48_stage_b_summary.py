#!/usr/bin/env python3
"""Write focused_review/fullread2/stage_b_summary.md (Stage B, 2026-11-13): tier, setups and grades of the
20 Stage B papers, from the grades files and tier_changes.csv; the narrative part is kept below in NOTES."""
import csv

G = 'focused_review/fullread2'
IDS = 'S019 S026 S031 S033 S036 S039 S043 S161 S205 S206 S239 S260 S264 S269 S296 S302 T0351 T0608 T0615 T1044'.split()
tiers = {r['rec_id']: r for r in csv.DictReader(open(f'{G}/tier_changes.csv', encoding='utf-8'))}
scr = {r['rec_id']: r for r in csv.DictReader(open('focused_review/screening.csv', encoding='utf-8'))}

out = ['# Stage B summary (2026-11-13): the 20 core papers that had no grades', '',
       'Every paper was read once, in full for core papers and through the methods for papers that failed eligibility, '
       'by one Opus reader subagent following `READER_B.md` (two at a time). The lead reviewer checked each reader\'s grades '
       'against the rubric and the setup-splitting rule; no grade needed a page check. Result: **15 core papers (32 setups), '
       '5 moved to context.** With Stage A: 47 graded core papers, 107 setups, 105 independent setups.', '',
       '## Papers moved to context', '', '| rec_id | Paper | Reason (logged in tier_changes.csv) |', '|---|---|---|']
for i in IDS:
    if i in tiers:
        s = scr[i]
        out.append(f"| {i} | {s['first_author'].split(' ')[-1]} {s['year']} | {tiers[i]['reason']} |")
out += ['', 'Each has a "background use" note in its `.md` file. They may be cited as background in the Introduction or '
        'Section 6, never as evidence, and they are in no figure, table or count.', '',
        '## Core papers: setups and grades', '',
        '| Setup | Plant | Evidence | Authority | Outcome | C1-C6 | Operation | Adjacent | Duplicate of |', '|---|---|---|---|---|---|---|---|---|']
for i in IDS:
    if i in tiers:
        continue
    for k, r in enumerate(csv.DictReader(open(f'{G}/grades/{i}.csv', encoding='utf-8')), 1):
        cs = ' '.join(r[f'C{j}'] for j in range(1, 7))
        out.append(f"| {i}.{k} {r['setup'][:70]} | {r['domain'][:45]} | {r['evidence']} | {r['authority']} | {r['outcome']} | "
                   f"{cs} | {r['operation']} | {r['adjacent']} | {r['duplicate_of']} |")
out += ['', open(__file__.replace('48_stage_b_summary.py', '48_stage_b_notes.md'), encoding='utf-8').read()]
open(f'{G}/stage_b_summary.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('wrote', f'{G}/stage_b_summary.md')
