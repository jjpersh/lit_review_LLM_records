#!/usr/bin/env python3
"""2026-11-10: retire latency criterion (old C4) and record latency as descriptive fields; renumber C5-C7 to C4-C6.
Run from lit_review_LLM/. Safe to rerun."""
import csv
import re

DATE = '2026-11-10'
P = 'extraction/extraction.csv'
rows = list(csv.DictReader(open(P, encoding='utf-8', newline='')))
if 'llm_latency' in rows[0]:
    raise SystemExit('already applied')

# rec_id (optional setup keyword) -> (LLM latency, loop timing, plant timing)
DESIGN = ('design-time or offline (no loop)', 'n/a', 'n/a')
LAT = {
    'S262': ('NR', '5 s MPC sampling', 'real time (hardware)'),
    'S203|T3': ('0.30 s mean, 0.13-3.01 s range over 600 updates', '0.5 s supervisory update', 'NR'),
    'S203': ('NR', 'NR', 'NR'),
    'S032|C2': ('per-cycle wall-clock, P95 <= 60 s', '5 min supervisory cadence', 'NR'),
    'S032|C3': ('per-cycle wall-clock, P95 <= 60 s', '5 min supervisory cadence', 'NR'),
    'S032': ('NR', '5 min supervisory cadence', 'NR'),
    'S020': ('NR (non-blocking call)', 'NR', 'NR'),
    'S002': DESIGN, 'S004': DESIGN, 'S007': DESIGN, 'S180': DESIGN, 'T0779': DESIGN, 'S013': DESIGN,
    'S193': DESIGN, 'S195': DESIGN,
    'S178': ('2.18-2.60 s per estimation call', 'NMPC solve 0.13-0.15 s per interval', 'NR'),
    'S272': ('NR', 'NR', 'NR'), 'T0532': ('NR', 'NR', 'NR'),
    'T0665': ('discussed, not quantified', 'n/a (advisory)', 'n/a'),
    'T1042': ('NR', '500 Hz inner PID loop', 'real time (hardware)'),
    'S016': ('NR', 'NR', 'NR'), 'S017': ('NR', 'NR', 'NR'),
    'S022': ('wall-clock breakdown against a latency budget', 'NR', 'NR'),
    'S037': ('NR (state drift during inference noted)', 'NR', 'real time (hardware) and simulation'),
    'S038': ('NR (inference time limited sampling rate)', 'NR', 'real time (hardware)'),
    'S042': ('NR', '60 s sampling', 'real time (hardware)'),
    'S048': ('logged but not reported', '1 s simulated step', 'NR'),
    'S028': ('11.2 s mean query response (advisory)', 'n/a (advisory)', 'real time (plant)'),
    'S030': ('2-8 s per call (advisory)', 'n/a (advisory)', 'NR'),
    'S041': ('47.3 s condition identification', '0.015 h (54 s) sampling', 'NR'),
    'S156': ('design budgets only (<100 ms supervisor, 1-2 s LLM)', 'n/a (advisory)', 'NR'),
    'S282': ('NR', 'NR', 'real time (demonstrator)'),
    'S315': ('NR', 'NR', 'NR'),
    'T1046': ('60-1,835 s per episode (agent loop)', '1-10 s typical loops (authors)', 'NR'),
    'T1053': ('100s of ms to seconds (stated)', 'LLM kept outside the real-time loop', 'NR'),
}


def lookup(r):
    for k, v in LAT.items():
        if '|' in k:
            rid, kw = k.split('|')
            if r['rec_id'] == rid and kw in r['setup']:
                return v
    return LAT.get(r['rec_id'], ('NR', 'NR', 'NR'))


new_cols = ['rec_id', 'setup', 'evidence', 'authority', 'outcome'] + [f'C{i}' for i in range(1, 7)] + \
           [f'C{i}_note' for i in range(1, 7)] + ['llm_latency', 'loop_timing', 'plant_timing', 'llm_model', 'key_result', 'limitation', 'calibration', 'date']
out = []
for r in rows:
    n = {k: r[k] for k in ['rec_id', 'setup', 'evidence', 'authority', 'outcome', 'llm_model', 'key_result', 'limitation', 'calibration', 'date']}
    for new, old in [(1, 1), (2, 2), (3, 3), (4, 5), (5, 6), (6, 7)]:
        n[f'C{new}'], n[f'C{new}_note'] = r[f'C{old}'], r[f'C{old}_note']
    n['llm_latency'], n['loop_timing'], n['plant_timing'] = lookup(r)
    out.append(n)
with open(P, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, new_cols)
    w.writeheader()
    w.writerows(out)

pr = 'focused_review/protocol.md'
s = open(pr, encoding='utf-8').read()
s = re.sub(r'- C4 Latency compared with sampling time\?\n', '', s)
s = s.replace('- C5 Repeated runs reported', '- C4 Repeated runs reported').replace('- C6 LLM decision quality', '- C5 LLM decision quality') \
     .replace('- C7 Safeguards present', '- C6 Safeguards present')
if 'Descriptive timing fields' not in s:
    s += ('\n## Descriptive timing fields (2026-11-10, replace the old latency criterion)\n'
          'Latency is recorded, not scored: llm_latency (reported LLM response time), loop_timing (sampling or update interval), '
          'plant_timing (real time on hardware or plant, or NR when a simulation may pause for the LLM). Criteria renumbered C1-C6.\n')
open(pr, 'w', encoding='utf-8').write(s)
with open('logs/decisions.md', 'a', encoding='utf-8') as f:
    f.write(f'- {DATE}: User dropped the latency criterion (old C4): working architectures already absorb their latency, and simulations usually pause for the LLM. '
            f'Latency kept as descriptive fields (llm_latency, loop_timing, plant_timing) for the timescale discussion. Criteria renumbered: old C5-C7 are now C4-C6.\n')
print('rows', len(out), '| with any latency value', sum(o['llm_latency'] not in ('NR',) for o in out))
