#!/usr/bin/env python3
"""2026-11-10 targeted recheck (C4 repeatable + outcome) of 24 digest-scored papers; apply corrections and print tallies."""
import collections
import csv

DATE = '2026-11-10'
P = 'extraction/extraction.csv'
rows = list(csv.DictReader(open(P, encoding='utf-8', newline='')))
cols = list(rows[0])
FIX = {
    'T0532': {'C4': 'Y', 'C4_note': 'variance bands across runs shown; prompt template given (p.4, 6)'},
    'T0665': {'evidence': 'E1', 'limitation_add': 'explanations generated from simulated MPC decisions, not live greenhouse measurements (p.3)'},
    'T1042': {'llm_model': 'o3-mini (control agent) and gpt-4.1-mini (optimizer agent)'},
    'S017': {'loop_timing': 'LLM operator agents at 5 min; ARC fast loop 2 s (p.9, 31)'},
    'S022': {'llm_model': 'GPT-4.1-mini, GPT-4o-mini',
             'key_result': 'GPT-4.1-mini recovered in 60/60 runs and GPT-4o-mini in 51/60 (pump degradation 50%, sensor fault 60%); only 52% of iterations gave a fully correct actuator configuration (p.10)'},
    'S037': {'llm_latency': 'inference-time statistics reported (Table 4, p.13)',
             'plant_timing': 'initial physical TCLab trials; main runs on a simulated plant for repeatable, latency-aware tests (p.12)'},
    'S156': {'evidence': 'E4', 'C5': 'Y', 'C5_note': 'median numerical error below 3% in audited conversational diagnostics (p.1)',
             'plant_timing': 'real time (operating beverage plant, advisory; six-month deployment)',
             'key_result': 'Deployed six months at an operating beverage plant without changing PLC/SCADA logic; 100% specification compliance in sanitizing stages and median diagnostic numerical error below 3% (p.1)',
             'limitation_add': '3 runs purposively selected from 24; advisory only'},
}
changed = collections.Counter()
for r in rows:
    f = FIX.get(r['rec_id'])
    if not f or r['calibration'] in ('yes', 'spotcheck'):
        continue
    for k, v in f.items():
        if k == 'limitation_add':
            if v not in r['limitation']:
                r['limitation'] += '; ' + v
        elif r[k] != v:
            r[k] = v
            changed[k] += 1
    r['calibration'] = 'rechecked'
for r in rows:
    if r['calibration'] == 'no':
        r['calibration'] = 'rechecked'
with open(P, 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, cols)
    w.writeheader()
    w.writerows(rows)
with open('logs/decisions.md', encoding='utf-8') as fh:
    done = 'Targeted recheck' in fh.read()
if not done:
    with open('logs/decisions.md', 'a', encoding='utf-8') as fh:
        fh.write(f'- {DATE}: Targeted recheck of C4 (repeatable) and outcome for 24 digest-scored papers against full text. Changes: C4 1 (T0532 N to Y); '
                 f'outcome 0; evidence 2 (T0665 NR to E1, S156 NR to E4); C5 1 (S156 N to Y); models and timing fields filled for T1042, S022, S017, S037.\n')
print('field changes', dict(changed))
print('rows', len(rows), 'papers', len({r["rec_id"] for r in rows}))
for k in ['evidence', 'authority', 'outcome', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'calibration']:
    print(k, dict(sorted(collections.Counter(r[k] for r in rows).items())))
print('outcome x authority', dict(sorted(collections.Counter((r['authority'], r['outcome']) for r in rows).items())))
print('timing reported (llm_latency not NR/design)', sum(not r['llm_latency'].startswith(('NR', 'design')) for r in rows))
print('plant real time', sum(r['plant_timing'].startswith('real time') for r in rows))
