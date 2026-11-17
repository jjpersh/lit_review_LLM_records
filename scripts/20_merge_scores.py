#!/usr/bin/env python3
"""Append scored rows (TSV batches) to extraction/extraction.csv, move non-LLM papers to context, and print a tally. Run from lit_review_LLM/."""
import collections
import csv
import glob
import sys

DATE = '2026-11-09'
COLS = ['rec_id', 'setup', 'evidence', 'authority', 'outcome'] + [f'C{i}' for i in range(1, 8)] + \
       [f'C{i}_note' for i in range(1, 8)] + ['llm_model', 'key_result', 'limitation', 'calibration', 'date']
NON_LLM = {'S034': 'no LLM: PPO supervisor and SAC residual controllers (RL); cited as RL mode-switching comparator on TEP',
           'T0302': 'no LLM: safe PPO with behaviour cloning (RL) for EAF steelmaking'}
DUP = {'S037': 'overlaps S038 (same group, temperature rig)', 'S038': 'preliminary version of S037'}

rows = list(csv.DictReader(open('extraction/extraction.csv', encoding='utf-8', newline='')))
have = {(r['rec_id'], r['setup']) for r in rows}
added = 0
for path in sorted(glob.glob(sys.argv[1] + '/scores_b*.tsv')):
    for line in open(path, encoding='utf-8'):
        f = line.rstrip('\n').split('\t')
        if len(f) != 22:
            raise SystemExit(f'bad line in {path}: {len(f)} fields: {f[:2]}')
        r = dict(zip(COLS[:19], f[:12] + f[12:19]))
        r.update({'llm_model': f[19], 'key_result': f[20], 'limitation': f[21], 'calibration': 'no', 'date': DATE})
        if r['rec_id'] in DUP:
            r['limitation'] += '; ' + DUP[r['rec_id']]
        if (r['rec_id'], r['setup']) not in have:
            rows.append(r)
            added += 1
with open('extraction/extraction.csv', 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, COLS)
    w.writeheader()
    w.writerows(rows)

scr = list(csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline='')))
fields = list(scr[0])
for r in scr:
    if r['rec_id'] in NON_LLM and r['tier'] == 'core':
        r.update({'tier': 'context', 'priority': '', 'theme': '', 'reason': NON_LLM[r['rec_id']] + ' (failed generative-LLM rule at full text)'})
rank = {'core': 0, 'context': 1, 'out': 2}
scr.sort(key=lambda x: (rank[x['tier']], str(x['priority']), x['theme'], x['rec_id']))
with open('focused_review/screening.csv', 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fields)
    w.writeheader()
    w.writerows(scr)
with open('logs/decisions.md', encoding='utf-8') as fh:
    logged = 'Priority-1 scoring complete' in fh.read()
if not logged:
    with open('logs/decisions.md', 'a', encoding='utf-8') as fh:
        fh.write(f'- {DATE}: Priority-1 scoring complete from page-tagged digests (scripts/19_digests.py). S034 and T0302 moved to context (RL, no LLM). '
                 f'S037/S038 flagged as overlapping. SC02 (Arjunan) awaits ILL.\n')

themes = {r['rec_id']: r['theme'] for r in scr}
print('added', added, '| total rows', len(rows), '| papers', len({r['rec_id'] for r in rows}))
for k in ['evidence', 'authority', 'outcome'] + [f'C{i}' for i in range(1, 8)]:
    print(k, dict(collections.Counter(r[k] for r in rows)))
print('outcome x authority', dict(collections.Counter((r['authority'], r['outcome']) for r in rows)))
print('by theme', dict(collections.Counter((themes.get(r['rec_id'], '?'), r['outcome']) for r in rows)))
