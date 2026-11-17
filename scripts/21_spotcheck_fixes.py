#!/usr/bin/env python3
"""Apply 2026-11-10 spot-check corrections (full-text rescoring of S195, S048, S041, T1046). Run from lit_review_LLM/."""
import csv

DATE = '2026-11-10'
path = 'extraction/extraction.csv'
rows = list(csv.DictReader(open(path, encoding='utf-8', newline='')))
cols = list(rows[0])
out = []
for r in rows:
    rid = r['rec_id']
    if rid == 'S195' and 'spotcheck' not in r['calibration']:
        base = dict(r, calibration='spotcheck', date=DATE)
        a = dict(base, setup='Scaffolded LLM tunes single-loop CSTR PI', outcome='Failed', C1='Y', C1_note='relay-ZN (IAE 0.106) and multi-start optimum 0.102 (p.6)',
                 C3='N', C3_note='nominal set-point tracking', key_result='Relay-ZN IAE 0.106 beats the LLM tuner 0.162; LLM never better across seeds (p.6)')
        b = dict(base, setup='Scaffolded LLM proposes structural prior for coupled quad-tank PI, refined by Nelder-Mead (hybrid)', outcome='Conditional',
                 key_result='Hybrid reaches J 12.0 in 10/10 seeds vs 0/10 for naive local search and needs 8x fewer evaluations than DE at 3x3; but VRFT reaches a better J 11.1 with tighter spread (p.7-10)',
                 C6_note='10/10 seeds converge; ablation shows reliability partly due to answer-shaped prompt example (p.2, 4.11)')
        c = dict(base, setup='LLM proposes VRFT reference-model time constant from open-loop rise times', outcome='Failed',
                 key_result='LLM commits a usable tau in 8/10 seeds; the median of the same rise times succeeds 10/10 at equal quality (p.10)',
                 C6_note='8/10 committed answers; 2/10 exhausted generation budget (p.10)')
        out += [a, b, c]
        continue
    if rid == 'S048':
        r['key_result'] = r['key_result'] + '; agreement fell to 73% with sensor noise sigma=2 (Table 3, p.12)'
        r['calibration'] = 'spotcheck'
    if rid == 'S041':
        r.update({'C4': 'N', 'C4_note': 'query time 47.3 s reported (p.10) but not related to the 0.015 h (54 s) sampling time (p.12)',
                  'C5': 'Y', 'C5_note': '90 switching pairs x 100 repeats; prompt shown (Fig. 4, p.8-9)',
                  'llm_model': 'Qwen-Plus (Alibaba)', 'calibration': 'spotcheck'})
    if rid == 'T1046':
        r.update({'outcome': 'Succeeded', 'C4': 'Y', 'C4_note': 'agent-loop latency 60-1,835 s compared with 1-10 s control loop periods; supervisory use only (p.13)',
                  'key_result': 'Zero constraint violations in all 282 shadow cells (1,552 unsafe proposals intercepted) with no significant completion cost (d = -0.05); corrections succeed 40% in optimization, 0% in upsets (p.1, 7-9)',
                  'limitation': r['limitation'] + '; prompt asymmetry between shadow and direct agents may confound the effect (p.14); SPE papers are not peer-reviewed (p.1)',
                  'calibration': 'spotcheck'})
    out.append(r)
with open(path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, cols)
    w.writeheader()
    w.writerows(out)
with open('logs/decisions.md', encoding='utf-8') as f:
    done = 'Spot check' in f.read()
if not done:
    with open('logs/decisions.md', 'a', encoding='utf-8') as f:
        f.write(f'- {DATE}: Spot check of 4 digest-scored papers against full text (S195, S048, S041, T1046): 35/40 fields agreed (87.5%). '
                f'Errors: S195 outcome (one row split into 3 setups); S041 C4 (N, not Y) and C5 (Y, not N); T1046 outcome (Succeeded, not Conditional) and C4 (Y, not N). '
                f'Pattern: digests miss latency comparisons and repeated-run designs stated in results/discussion text, and flatten mixed outcomes. Corrections applied (calibration=spotcheck).\n')
print('rows', len(out))
