#!/usr/bin/env python3
"""Apply the 2026-11-09 calibration decisions and save the calibrated scores. Safe to rerun. Run from lit_review_LLM/."""
import csv
import os

DATE = '2026-11-09'

# 1. Protocol: tighter C6 and the eligibility rule
p = 'focused_review/protocol.md'
s = open(p, encoding='utf-8').read()
old_c6 = "- C6 Failures characterized, and did actions match the operator's intent?"
new_c6 = ('- C6 LLM decision quality measured? Y if the paper reports how often LLM outputs were correct, invalid, unsafe or '
          'off-intent across multiple decisions (a rate or count, not anecdotes). (Tightened 2026-11-09: the earlier '
          '"failures characterized" wording was Y for every calibration setup.)')
if old_c6 in s:
    s = s.replace(old_c6, new_c6)
rule = '- Eligibility requires a generative LLM (or LLM agent or VLM). Encoder-only language models with classifiers are context.'
if rule not in s:
    s = s.replace('- Abstracts select papers.', rule + '\n- Abstracts select papers.', 1)
if 'Score one row per tested setup' not in s:
    s += ('\n## Calibration notes (2026-11-09)\n'
          '- Score one row per tested setup; papers reporting the same experiment (e.g. S203 and S033) are counted once in synthesis.\n'
          '- Partial evidence counts as Y, with the gap written in the note.\n'
          '- C5 needs repeated runs or variance as well as model details.\n'
          '- C7 needs the safeguard to be tested with bad proposals, not only described.\n')
open(p, 'w', encoding='utf-8').write(s)

# Keep script 11 from overwriting the protocol on a rerun
p11 = 'scripts/11_record_scope.py'
t = open(p11, encoding='utf-8').read()
old = "open('focused_review/protocol.md', 'w', encoding='utf-8').write("
if old in t and "if not os.path.exists('focused_review/protocol.md'): " + old not in t:
    t = t.replace(old, "if not os.path.exists('focused_review/protocol.md'): " + old, 1)
    open(p11, 'w', encoding='utf-8').write(t)

# 2. ChatMPC to context, flagged as a key reference
rows = list(csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline='')))
fields = list(rows[0])
if 'key_reference' not in fields:
    fields.append('key_reference')
for r in rows:
    r.setdefault('key_reference', '')
    if r['rec_id'] == 'SC01' and r['tier'] == 'core':
        r.update({'tier': 'context', 'priority': '', 'theme': '',
                  'reason': 'language interface is a non-generative encoder (Sentence-BERT) plus k-NN classifier; cited as the non-LLM comparator for language-to-MPC',
                  'key_reference': 'yes: non-LLM baseline for language-to-MPC; candidate baseline for crystallization experiments'})
rank = {'core': 0, 'context': 1, 'out': 2}
rows.sort(key=lambda x: (rank[x['tier']], str(x['priority']), x['theme'], x['rec_id']))
with open('focused_review/screening.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    w.writerows(rows)

# 3. Calibrated scores
COLS = ['rec_id', 'setup', 'evidence', 'authority', 'outcome'] + [f'C{i}' for i in range(1, 8)] + \
       [f'C{i}_note' for i in range(1, 8)] + ['llm_model', 'key_result', 'limitation', 'calibration', 'date']
S = []


def add(rec, setup, ev, au, out, scores, notes, model, result, limit):
    row = {'rec_id': rec, 'setup': setup, 'evidence': ev, 'authority': au, 'outcome': out, 'llm_model': model,
           'key_result': result, 'limitation': limit, 'calibration': 'yes', 'date': DATE}
    for i, (sc, nt) in enumerate(zip(scores, notes), 1):
        row[f'C{i}'], row[f'C{i}_note'] = sc, nt
    S.append(row)


add('S262', 'LLM proposes GEKKO MPC tuning from operator language, operator approves (TCLab 2x2)', 'E3', 'Propose', 'Conditional',
    ['N', 'Y', 'N', 'NR', 'N', 'N', 'N'],
    ['only untuned default MPC (Fig. 3, p.2)', 'rise time and overshoot for some scenarios; no IAE (pp.3-4)',
     'nominal conditions only (p.6)', '5 s sampling given; LLM response time not reported (pp.2-3)',
     'one run per command; model named, full prompt and temperature not given (p.3)',
     'intent discussed per scenario, not counted (pp.4-5)', 'operator approval and hard MV bounds not tested with bad proposals'],
    'gemma3:12b (local)', 'Each of four language requests produced the intended trade-off, e.g. T1 rise time 78 to 53 s (p.4)',
    'Nominal conditions, single runs, untuned baseline (p.6)')
for setup, au, out, c1, c1n, c4, c4n, res in [
    ('T1 direct LLM control, water tank', 'Act', 'Failed', 'Y', 'fixed PID, tuning not stated (Fig. 3, p.4)', 'NR', '', 'Produced text, not commands (p.4)'),
    ('T2 numeric-constrained direct control, water tank', 'Act', 'Failed', 'Y', 'fixed PID, tuning not stated (Fig. 3, p.4)', 'NR', '', 'Valid numbers but unstable, incoherent control (p.4)'),
    ('T3 LLM tunes PID gains, water tank (SISO)', 'Set targets', 'Conditional', 'Y', 'fixed PID, tuning not stated (Fig. 3, p.4)', 'Y',
     'mean 0.30 s (0.13-3.01 s) over 600 updates vs 0.5 s update interval (p.7, Table 3)', 'Stable tracking under nominal conditions; irregular, abrupt gain updates (p.4)'),
    ('T4 LLM tunes PID gains, CSTR (MIMO)', 'Set targets', 'Failed', 'NR', 'no comparator described', 'NR', '', 'Inconsistent, unstable recommendations; poor loop coordination (pp.4-5)')]:
    add('S203', setup, 'E1', au, out, [c1, 'N', 'N', c4, 'N', 'N', 'N'],
        [c1n, 'plots only, no IAE/overshoot numbers', 'nominal tracking only (p.4)', c4n,
         'temperature 0.7, top-p 0.9, prompts in appendix (pp.11-12) but no repeated runs', 'failures described, not counted', 'no safeguard tested'],
        'Llama 3.2 3B (local, Ollama)', res,
        'E1 inferred from MATLAB benchmark (hardware never mentioned); trials partly reported in Wen et al. 2025/2026 (S033): count once')
ros = ['relay-tuned PID and Pareto-tuned MPC (pp.2, 9)', 'IAE with bootstrap CIs (p.9)', '16-point off-nominal grid with disturbances (pp.9-10)',
       '600 cycles vs 5-min cadence, P95 <= 60 s (Fig. 5, p.14)', '10 seeds, pre-registration, model and temperature, code on GitHub (pp.9, 27-28)',
       'protocol-attrition rates and counted harmful proposals (pp.14, 22)']
add('S032', 'C2 ungated agent writes composition setpoints over linear MPC (Column A)', 'E1', 'Set targets', 'Conditional',
    ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'N'], ros + ['no safeguard by design'], 'DeepSeek-V4-Flash (T=1.0)',
    'Beats Pareto MPC on off-nominal target acquisition (P95 IAE 58.6 vs 162.1) but about 10x worse on disturbance rejection (p.10)',
    'Single column, single-author preprint, model-conditional; no setpoint-tracking arm exercised (s6.8)')
add('S032', 'C3 gated agent: forked-twin counterfactual gate, 9 constraints', 'E1', 'Set targets', 'Conditional',
    ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'], ros + ['590 gate interventions, 318 harmful proposals corrected (pp.1, 14)'], 'DeepSeek-V4-Flash (T=1.0)',
    'Gate contains spec-abandonment attractor (P95 IAE 11.5 to 0.77); 534 of 590 blocks are spec-on-bound geometry (pp.1, 14)',
    'Single column, single-author preprint, model-conditional')
add('S032', 'Agent over PID with no MPC layer (demonstration scope)', 'E1', 'Set targets', 'Failed',
    ['Y', 'Y', 'Y', 'NR', 'Y', 'Y', 'N'],
    [ros[0], ros[1], 'disturbance arms at nominal operating point only', 'not reported for this branch', ros[4], 'operable in 50/50 cells (p.2)', 'no safeguard'],
    'DeepSeek-V4-Flash (T=1.0)', 'Below PID-only on every disturbance arm (p.2, s6.5)', 'Demonstration scope, nominal OP only')
add('S020', 'LLM selects controller mode from bounded set and writes audit rationale; rule-based dwell-time switching', 'E1', 'Set targets', 'Not shown',
    ['Y', 'Y', 'Y', 'NR', 'N', 'N', 'N'],
    ['LQI, MPC, CFG and a no-LLM ablation (Table 1, p.9)', 'IAE and overshoot', '75% actuator loss, damping drift, noise, six sensitivity sweeps',
     'non-blocking call; response time not reported', 'temperature 0, prompt in appendix; only 3 LLM calls, no repeats, model version not given',
     'only 3 decisions, checked against risk score (Table 5)', 'bounded action set and fallback not tested with invalid outputs'],
    'Claude Sonnet (version not stated)', 'Identical IAE with and without the LLM (2.313 vs 2.313, Table 1); the LLM adds audit records only',
    'Simulation only (4th-order benchmark, 1-D thermal model); audit quality not evaluated')

os.makedirs('extraction', exist_ok=True)
path = 'extraction/extraction.csv'
existing = list(csv.DictReader(open(path, encoding='utf-8', newline=''))) if os.path.exists(path) and os.path.getsize(path) else []
keep = [r for r in existing if r.get('calibration') != 'yes']
with open(path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, COLS)
    w.writeheader()
    w.writerows(S + keep)

# 4. Log
d = open('logs/decisions.md', encoding='utf-8').read()
if 'Calibration complete' not in d:
    with open('logs/decisions.md', 'a', encoding='utf-8') as f:
        f.write(f'- {DATE}: Calibration complete on S262, S203, S032, SC01, S020 with the user. C6 tightened to "LLM decision quality measured" '
                f'(old wording was Y for all 9 setups). Eligibility now requires a generative LLM. SC01 (ChatMPC, Sentence-BERT + k-NN) moved to context '
                f'and flagged key_reference. Scores saved to extraction/extraction.csv (calibration=yes).\n')
st = open('STATUS.md', encoding='utf-8').read()
if 'Calibration done' not in st:
    st = st.replace('## Current stage\n', f'Calibration done {DATE} (extraction/extraction.csv). Next: score remaining priority-1 core papers.\n\n## Current stage\n', 1)
    open('STATUS.md', 'w', encoding='utf-8').write(st)
core = [r for r in rows if r['tier'] == 'core']
print('rows saved', len(S), '| core', len(core), '| P1', sum(str(r['priority']) == '1' for r in core),
      '| P1 with PDF', sum(bool(r['pdf']) for r in core if str(r['priority']) == '1'))
print('remaining P1 to score:', sorted(r['rec_id'] for r in core if str(r['priority']) == '1' and r['rec_id'] not in {'S262', 'S203', 'S032', 'S020'}))
