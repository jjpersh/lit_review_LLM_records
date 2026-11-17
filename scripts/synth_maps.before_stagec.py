"""Hand-written per-setup maps for the synthesis (revision run, 2026-11-12).
Keys are '<rec_id>.<k>', k = 1-based order of the setup within the paper in extraction/extraction.csv.
Each entry was set from the full-read grades file and .md in focused_review/fullread2/.

SETUP fields:
  layer   : operator | design | supervisory | actuation  (what the LLM touches; Fig. D)
  label   : short label for figures
  domain  : process type (Fig. C, setup level)
  h2h     : head-to-head class for setups with C1 = Y:
            'nonllm' (non-LLM better), 'tie', 'mixed', 'llm' (LLM better), 'nq' (not quantified),
            'gate' (the comparison is the gate or the LLM itself, not LLM vs non-LLM); None when C1 = N
  h2h_txt : one-line result for Table 5
  safe    : (type, description) of the safeguard, or None
"""

THEMES = {'T1': 'Language to MPC or tuning', 'T2': 'LLM in or above the loop', 'T3': 'LLM-facilitated hybrid control',
          'T4': 'SCADA, MCP and OPC integration', 'T5': 'Recovery and safeguards'}

DOMAINS = ['Reactors', 'Tanks and level', 'Separation and crystallization', 'Thermal and heating',
           'Plant-wide and utilities', 'Generic process models', 'Climate (adjacent)', 'Mechanical (adjacent)',
           'Energy, traffic and logistics (adjacent)']

# Setups that report the same experiment as another graded setup (counted once in every count; brief rule).
# Added 2026-11-13 (Stage B): S033 (Wen et al.) is the fuller report of the water-tank experiment in S203.
# S203 trials 2 (numeric direct actuation) and 3 (PID retuning every 0.5 s) are the same arms as S033.1 and S033.2.
DUP = {'S203.2': 'S033.1', 'S203.3': 'S033.2'}

H2H_LABEL = {'nonllm': 'Non-LLM better', 'tie': 'Tie', 'mixed': 'Mixed', 'llm': 'LLM better', 'nq': 'Not quantified'}

S = {}


def add(key, layer, label, domain, h2h=None, h2h_txt='', safe=None):
    S[key] = dict(layer=layer, label=label, domain=domain, h2h=h2h, h2h_txt=h2h_txt, safe=safe)


# ---- Language to MPC or tuning (T1) -------------------------------------------------------
add('S002.1', 'design', 'Shou 2026 hosted LLMs', 'Generic process models', 'nonllm',
    'IMC lowest IAE in all 4 worked cases; LLMs pass acceptance in 75-89% of 200 cases', ('Validator', 'Closed-loop acceptance criteria'))
add('S002.2', 'design', 'Shou 2026 fine-tuned 0.6B', 'Generic process models', 'nonllm',
    'IMC lowest IAE in all 4 worked cases (Table S2, pp.54-55); fine-tuned 0.6B passes 94% vs 56-71% hosted', ('Validator', 'Closed-loop acceptance criteria'))
add('S004.1', 'design', 'Luna Rueda 2026', 'Thermal and heating')
add('S007.1', 'design', 'Narimani 2025 DC motor', 'Mechanical (adjacent)', safe=('Bounds', 'Gain ranges, simulation scoring'))
add('S007.2', 'design', 'Narimani 2025 ball-beam', 'Mechanical (adjacent)', 'mixed',
    'Lower MSE than LQR but overshoot 12-14% vs 0-3%', ('Bounds', 'Gain ranges, simulation scoring'))
add('S007.3', 'design', 'Narimani 2025 pendulum', 'Mechanical (adjacent)', 'tie',
    'FSF matches LQR (MSE 0.2531 vs 0.2529); beats MATLAB PID Tuner (settings not given)', ('Bounds', 'Gain ranges, simulation scoring'))
add('S007.4', 'design', 'Narimani 2025 double pendulum', 'Mechanical (adjacent)', 'mixed',
    'Best of 10 runs beats LQR on MSE; all models miss the overshoot target', ('Bounds', 'Gain ranges, simulation scoring'))
add('S013.1', 'design', 'Tohma 2025', 'Generic process models', safe=('Human approval', 'User accepts the design'))
add('S178.1', 'supervisory', 'Ibáñez-Espinel 2026 CSTR', 'Reactors', 'tie',
    'LLM estimates give ISE 0.278 vs IPOPT 0.283, statistically equivalent')
add('S178.2', 'supervisory', 'Ibáñez-Espinel 2026 WWTP', 'Plant-wide and utilities', 'nonllm',
    'LLM-only IAE 0.882 vs IPOPT 0.807; LLM plus Powell ties IPOPT')
add('S180.1', 'design', 'Lima 2026 NMPC design', 'Separation and crystallization')
add('S180.2', 'design', 'Lima 2026 PBM building', 'Separation and crystallization', 'mixed',
    'One LLM model matched the literature PBM in the data window; another was more consistent at equilibrium')
add('S180.3', 'design', 'Lima 2026 soft sensor', 'Separation and crystallization')
add('S193.1', 'design', 'Chen 2026 quad tank', 'Tanks and level', 'nonllm',
    'Numerical rule 96.7% correct vs LLM pairwise ranking 46.8%')
add('S193.2', 'design', 'Chen 2026 CSTRs', 'Reactors', 'nonllm', 'Numerical rule 49/50 vs LLM 31.8%')
add('S193.3', 'design', 'Chen 2026 3x3 plant', 'Generic process models', 'nonllm', 'Numerical rule 47/50 vs LLM 53.2%')
add('S193.4', 'design', 'Chen 2026 gain proposals', 'Tanks and level')
add('S195.1', 'design', 'Shu 2026 CSTR', 'Reactors', 'nonllm', 'Relay-ZN IAE 0.106 vs LLM 0.162')
add('S195.2', 'design', 'Shu 2026 quad tank (LLM + NM)', 'Tanks and level', 'mixed',
    'Beats naive search (10/10 vs 0/10); VRFT better (J 11.12 vs 12.0)')
add('S195.3', 'design', 'Shu 2026 3x3 (LLM + NM)', 'Generic process models', 'llm',
    'Same cost as DE (J 2.17) with about 8x fewer evaluations')
add('S195.4', 'design', 'Shu 2026 VRFT time constant', 'Tanks and level', 'nonllm',
    'Median rule 10/10 seeds vs LLM 8/10, equal J')
add('S262.1', 'supervisory', 'Pershing 2026 MPC tuning', 'Thermal and heating',
    safe=('Human approval', 'Operator approves each LLM command (y/n)'))
add('S262.2', 'operator', 'Pershing 2026 log analysis', 'Thermal and heating')
add('S272.1', 'supervisory', 'Miyaoka 2026 pass side', 'Mechanical (adjacent)', safe=('Bounds', 'Constrained tool set'))
add('S272.2', 'supervisory', 'Miyaoka 2026 ambulance', 'Mechanical (adjacent)', safe=('Bounds', 'Constrained tool set'))
add('T0532.1', 'supervisory', 'Wu 2025 robot', 'Mechanical (adjacent)', 'llm',
    'Closer tracking than MPC without forecasts (plots only)')
add('T0532.2', 'supervisory', 'Wu 2025 building', 'Climate (adjacent)', 'llm',
    'Cost $380 vs $911 for MPC without forecasts')
add('T0665.1', 'operator', 'Naagarajan 2025', 'Climate (adjacent)', 'llm',
    'Better text metrics than keyword retrieval (BERTScore 0.79 vs 0.68)')  # no safeguard: explanation only; feedback re-weights retrieval (audit T0665 #6, #8)
add('T1042.1', 'supervisory', 'Arif 2025 guided', 'Mechanical (adjacent)', safe=('Bounds', 'Safe gain range stated in the prompt; voltage clip'))
add('T1042.2', 'supervisory', 'Arif 2025 unguided', 'Mechanical (adjacent)', safe=('Bounds', 'Safe gain range stated in the prompt; voltage clip'))
add('T1042.3', 'operator', 'Arif 2025 Q&A', 'Mechanical (adjacent)')

# ---- LLM in or above the loop (T2) ---------------------------------------------------------
add('S016.1', 'supervisory', 'Nozari 2026 with governor', 'Reactors', 'llm',
    'Robustness 0.893 vs 0.858 without the LLM and 0.812 for MPC', ('Validator', 'Independent safety governor'))
add('S016.2', 'supervisory', 'Nozari 2026 no governor', 'Reactors', 'mixed',
    'Higher productivity than MPC but DO limit crossed three times')
add('S017.1', 'actuation', 'Nogueira 2026 4-day', 'Climate (adjacent)', 'nonllm',
    'CO2 above limit 2.42 h vs 0.33 h for PI selector control', ('Bounds', 'Schema, clip-and-slew clamp, more layers'))
add('S017.2', 'actuation', 'Nogueira 2026 Arch B ramp', 'Climate (adjacent)', 'mixed',
    'Less time below 0 C than PI (3.38 vs 3.62 h); colder minimum', ('Bounds', 'Schema, clip-and-slew clamp, more layers'))
add('S017.3', 'actuation', 'Nogueira 2026 Arch C ramp', 'Climate (adjacent)', 'mixed',
    'Less time below 0 C than PI (3.40 vs 3.62 h); colder minimum', ('Bounds', 'Schema, clip-and-slew clamp, more layers'))
add('S017.4', 'actuation', 'Nogueira 2026 single model', 'Climate (adjacent)', 'nonllm',
    'Barn fell to -32.6 C vs -6.1 C for PI selector control')
add('S032.1', 'supervisory', 'Rosenthal ungated', 'Separation and crystallization', 'mixed',
    'Better than tuned MPC at re-targeting; about 10x worse at disturbance rejection')
add('S032.2', 'supervisory', 'Rosenthal gated', 'Separation and crystallization', 'gate',
    'Gate cuts attractor P95 IAE 11.46 to 0.77; makes one operating point run-fatal', ('Simulation gate', 'Forked-twin gate, 9 constraints'))
add('S032.3', 'supervisory', 'Rosenthal over PID', 'Separation and crystallization', 'nonllm',
    'PID alone better on every disturbance arm')
add('S037.1', 'supervisory', 'Vyas 2025 FSM planning', 'Generic process models',
    safe=('Validator', 'Path simulator, LLM validator and reprompter'))
add('S037.2', 'actuation', 'Vyas 2025 TCLab hardware', 'Thermal and heating', 'nonllm',
    'PID error 0.76 vs LLM 1.03 on hardware (time-weighted MAE)', ('Validator', 'LLM validator and reprompter agents'))
add('S037.3', 'actuation', 'Vyas 2025 TCLab twin', 'Thermal and heating', 'nonllm',
    'PID error 0.21 vs best LLM 0.62 on the twin (time-weighted MAE)', ('Validator', 'LLM validator and reprompter agents'))
add('S038.1', 'actuation', 'Vyas 2024 TCLab on/off', 'Thermal and heating',
    safe=('Validator', 'LLM validator and reprompter agents'))
add('S042.1', 'actuation', 'Rasheed 2025 prompt-only', 'Climate (adjacent)')
add('S042.2', 'actuation', 'Rasheed 2025 SQL', 'Climate (adjacent)')
add('S042.3', 'actuation', 'Rasheed 2025 predictor', 'Climate (adjacent)')
add('S048.1', 'actuation', 'Rojas-Ordoñez 2025', 'Thermal and heating', 'tie',
    '100% agreement with the coded relay; 73% under noise', ('Bounds', 'Output schema, retries, coded fallback'))
add('S203.1', 'actuation', 'Wen 2026 T1 free text', 'Tanks and level', 'nonllm', 'LLM produced text, not commands')
add('S203.2', 'actuation', 'Wen 2026 T2 numeric', 'Tanks and level', 'nonllm', 'Level reached 1.6 of 10 m')
add('S203.3', 'supervisory', 'Wen 2026 T3 retunes PID', 'Tanks and level', 'nq', 'Stable tracking, irregular gains; no numbers')
add('S203.4', 'supervisory', 'Wen 2026 T4 CSTR', 'Reactors')

# ---- LLM-facilitated hybrid control (T3) --------------------------------------------------
add('S020.1', 'supervisory', 'Papacharalampopoulos 2026 oscillator', 'Generic process models', 'tie',
    'LLM changed IAE 2.313 to 2.312', ('Bounds', 'Bounded mode set, dwell time, fallback'))
add('S020.2', 'supervisory', 'Papacharalampopoulos 2026 heating', 'Thermal and heating', 'mixed',
    'Framework better than PI on power loss, worse on phase change', ('Bounds', 'Bounded mode set, dwell time, fallback'))
add('S020.3', 'supervisory', 'Papacharalampopoulos 2026 audit', 'Generic process models', 'tie', 'No IAE change (2.364)')
add('S041.1', 'supervisory', 'Zhang 2025 numerical', 'Generic process models', 'llm',
    'Identification 87.9% vs 61.1% for numerical similarity (DTW)')
add('S041.2', 'supervisory', 'Zhang 2025 CSTR', 'Reactors', 'nq', 'Better tracking than DTW in a figure; no numbers')
add('T0779.1', 'design', 'Krishna 2026 point-to-disk', 'Mechanical (adjacent)', 'llm',
    'BO on templates matched at 2 of 3 targets, never at the third')
add('T0779.2', 'design', 'Krishna 2026 rangefinder', 'Mechanical (adjacent)', 'llm', 'At least 20% lower resource cost than single-mode designs')
add('T0779.3', 'design', 'Krishna 2026 clutter-nav', 'Mechanical (adjacent)', 'llm', 'About 10x lower resource cost than single-mode designs')

# ---- SCADA, MCP and OPC integration (T4) ---------------------------------------------------
add('S028.1', 'operator', 'Hidalgo-Castelo 2026', 'Plant-wide and utilities')
add('S030.1', 'operator', 'Schall 2026 TEP', 'Plant-wide and utilities', safe=('Validator', 'P&ID-grounded deterministic validator'))
add('S030.2', 'operator', 'Schall 2026 batch reactor', 'Reactors', safe=('Validator', 'P&ID-grounded deterministic validator'))
add('S030.3', 'operator', 'Schall 2026 dryer', 'Separation and crystallization', safe=('Validator', 'P&ID-grounded deterministic validator'))
add('S282.1', 'operator', 'Hofmann 2025 PLC', 'Mechanical (adjacent)')
add('S282.2', 'operator', 'Hofmann 2025 coating cell', 'Mechanical (adjacent)')
add('S315.1', 'actuation', 'Nerantzis 2026', 'Reactors', safe=('Data-quality gate', 'Trust gate on sensor-data quality (MCP)'))
add('T1053.1', 'design', 'Šmídl 2026', 'Mechanical (adjacent)', 'llm',
    'Ripple 0.85 vs 0.90 A at lower switching frequency than one hand tune', ('Separation', 'Argument checks and engineer approval in MCP server; current clamp in the drive layer'))

# ---- Recovery and safeguards (T5) ----------------------------------------------------------
add('S022.1', 'supervisory', 'Vyas 2026 mixing module', 'Tanks and level',
    safe=('Simulation gate', 'Simulation validation, reprompt limit, deterministic fallback'))
add('S022.2', 'supervisory', 'Vyas 2026 CSTR', 'Reactors',
    safe=('Simulation gate', 'Simulation validation, reprompt limit, deterministic fallback'))
add('S156.1', 'operator', 'González-Potes 2026', 'Plant-wide and utilities',
    safe=('Separation', 'Deterministic supervisor between LLM and equipment'))
add('T1046.1', 'supervisory', 'Khan 2026 ReAct gated', 'Reactors', safe=('Simulation gate', 'Shadow-plant check with correction loop'))
add('T1046.2', 'supervisory', 'Khan 2026 Plan-Exec gated', 'Reactors', safe=('Simulation gate', 'Shadow-plant check with correction loop'))
add('T1046.3', 'supervisory', 'Khan 2026 ReAct direct', 'Reactors')
add('T1046.4', 'supervisory', 'Khan 2026 Plan-Exec direct', 'Reactors')

# ---- Stage B papers (graded 2026-11-13 from focused_review/fullread2/<rec_id>.md) ------------
ETL = 'Energy, traffic and logistics (adjacent)'
add('S019.1', 'actuation', 'Wang 2026 SLM heater (sim)', 'Climate (adjacent)', 'nq',
    'Trajectory close to the rule table it imitates (91.5% agreement); overlay only',
    ('Validator', 'Rule-equality validator, reprompt, rule fallback'))
add('S019.2', 'actuation', 'Wang 2026 model benchmark', 'Climate (adjacent)',
    safe=('Validator', 'Rule-equality validator, reprompt, rule fallback'))
add('S026.1', 'supervisory', 'He 2026 ramp metering', ETL, 'llm',
    'Throughput +6.62% vs feedback control, +3.06% vs hierarchical RL', ('Validator', 'Schema check, hold previous mode'))
add('S026.2', 'supervisory', 'He 2026 virtual power plant', ETL, 'llm',
    'Cost -4.37% vs MPC-MILP, -2.49% vs hierarchical RL', ('Bounds', 'MILP hard bounds, feeder curtailment, schema check'))
add('S031.1', 'supervisory', 'Song 2026 CBF-MPC', 'Mechanical (adjacent)', safe=('Bounds', 'CBF constraint in MPC; LLM sets gamma'))
add('S031.2', 'supervisory', 'Song 2026 gamma alignment', 'Mechanical (adjacent)')
add('S031.3', 'supervisory', 'Song 2026 online gamma', 'Mechanical (adjacent)', safe=('Bounds', 'CBF constraint in MPC; LLM sets gamma'))
add('S033.1', 'actuation', 'Wen 2026b direct pump', 'Tanks and level', 'nonllm',
    'IAE 510.7 vs 60.3 for autotuned PID; level 8.5 m short', ('Bounds', 'Command clamped to 0-1'))
add('S033.2', 'supervisory', 'Wen 2026b retunes PID', 'Tanks and level', 'mixed',
    'Nominal IAE 49.2 vs 60.3 for autotuned PID; worst under sensor drift (538.1 vs 452.6)',
    ('Validator', 'Format and finite-value check only'))
add('S036.1', 'design', 'Li 2025 web line', 'Generic process models', 'llm',  # web tension: a process (adjacent = no), no closer domain
    'Tension RMSE 1.04 vs 1.62 N and 0.29 vs 1.01 N vs MPC (tuning not reported)',
    ('Simulation gate', 'Simulation safety filter on gain updates'))
add('S039.1', 'actuation', 'Xia 2025 production rig', 'Mechanical (adjacent)')
add('S043.1', 'actuation', 'Gill 2025 mixing module', 'Tanks and level',
    safe=('Simulation gate', 'Digital-twin simulation and rule validator, reprompt'))
add('S205.1', 'design', 'Caracciolo 2026 iterative', ETL, 'mixed',
    'Safe controller in 7/10 runs with fewer evaluations than CMA-ES; target met in 2/10; best beats CC-CV',
    ('Simulation gate', 'Constraint layer in digital twin, feedback to LLM'))
add('S205.2', 'design', 'Caracciolo 2026 zero-shot', ETL, 'nonllm', '0/10 feasible controllers vs CC-CV rule')
add('S239.1', 'operator', 'Xue 2026 tool-call guard', 'Generic process models',
    safe=('Validator', 'LLM guardrail classifies each tool call'))
add('S264.1', 'operator', 'Vieira da Silva 2025 cell', 'Mechanical (adjacent)', safe=('Validator', 'Tool argument assertions'))
add('S269.1', 'design', 'Christofides 2026 methanol', 'Reactors',
    safe=('Validator', 'Branch, unit and read-back checks in tool server'))
add('S269.2', 'design', 'Christofides 2026 flash PSV', 'Separation and crystallization',
    safe=('Validator', 'Branch, unit and read-back checks in tool server'))
add('S269.3', 'design', 'Christofides 2026 RL interface', 'Separation and crystallization')
add('S302.1', 'operator', 'Kasai 2026 STAMP agent', 'Plant-wide and utilities', safe=('Validator', 'STAMP/CAST safety-constraint stage'))
add('S302.2', 'operator', 'Kasai 2026 direct', 'Plant-wide and utilities')
add('T0608.1', 'operator', 'Naagarajan 2025b summaries', 'Climate (adjacent)')
add('T0615.1', 'operator', 'Raghavan 2025 tool calls', ETL, 'llm', 'Tool accuracy 96.67% vs 70% for a keyword parser')
add('T0615.2', 'operator', 'Raghavan 2025 home MPC', ETL, 'nonllm',
    'Heuristic price-aware rule earned 25.69 vs 19.26 rupees/day for the LLM-called MPC')
for _i, _p in enumerate(['inventory', 'water network', 'vessel', 'crane'], 0):
    _d = 'Mechanical (adjacent)' if _p in ('vessel', 'crane') else ETL
    add(f'T1044.{2 * _i + 1}', 'supervisory', f'Caccia 2026 {_p} one-shot', _d)
    add(f'T1044.{2 * _i + 2}', 'supervisory', f'Caccia 2026 {_p} gated', _d,
        safe=('Simulation gate', 'Nominal-model simulation check of the LLM cost, retries'))

# ---- Timing (Fig. F): label, loop period (s, or (lo, hi), or None), latency (lo, hi) or None, note
TIM = [
    ('Arif 2025: live PID retuning, servo (hardware)', 0.002, None, 'loop = 500 Hz inner PID'),
    ('Wen 2026: LLM retunes PID, water tank', 0.5, (0.13, 3.01), 'mean 0.30 s'),
    ('Rojas-Ordoñez 2025: LLM relay, oven (sim)', 1.0, None, ''),
    ('Šmídl 2026 / Papacharalampopoulos 2026', None, None, ''),
    ('Ibáñez-Espinel 2026: LLM estimates NMPC parameters', None, (2.18, 6.94), 'per call; NMPC solve 0.13-0.23 s'),
    ('Vyas 2026: recovery action agent (sim)', None, (1.9, 3.5), 'per action'),
    ('Schall 2026: advisory agent (offline)', None, (2, 8), 'advisory'),
    ('González-Potes 2026: CIP assistant (plant)', None, (1, 2), 'advisory, median'),
    ('Hidalgo-Castelo 2026: operator queries (plant)', 20.0, (9.84, 16.47), 'advisory; 20 s refresh cycle'),
    ('Pershing 2026: LLM tunes MPC, TCLab', 5.0, None, ''),
    ('Khan 2026: shadow-plant agents, CSTR (sim)', 10.0, (23, 1835), 'whole episode'),
    ('Vyas 2025: LLM heater power, TCLab (hardware)', 30.0, (10.58, 72.69), 'plant did not wait'),
    ('Zhang 2025: regime selection, numerical system (sim)', None, (47.3, 47.3), 'identification only'),
    ('Nozari 2026: supervisory agent, bioreactor (sim)', 300.0, (2.9, 2.9), ''),
    ('Nogueira 2026: LLM operator agents, barn (sim)', (60, 300), (0.1, 1.0), ''),
    ('Rosenthal 2026: setpoint agent, distillation (sim)', 300.0, (11.3, 278), 'median 15 s'),
    # Stage B (2026-11-13)
    ('He 2026: LLM sets ramp-metering modes (sim)', 180.0, (1.6, 1.6), 'adjacent'),
    ('He 2026: LLM sets VPP dispatch modes (sim)', 1800.0, (0.4, 0.4), 'adjacent'),
    ('Song 2026: LLM re-tunes CBF-MPC, gripper (sim)', 0.04, (2.4, 2.4), 'on demand; MPC step shown'),
    ('Wang 2026: SLM picks heater power (sim)', None, (3.84, 5.28), 'per step'),
    ('Raghavan 2025: LLM calls home-energy MPC (sim)', 900.0, (0.70, 2.80), 'per query'),
    ('Caccia 2026: local SLM writes MPC cost (sim)', None, (3.38, 9.89), 'once per goal'),
]
TIM = [t for t in TIM if t[1] is not None or t[2] is not None]

# ---- Manuscript Table 5 (setups with C1 = Y): plain setup description, named comparator, result ----
# Added 2026-11-12 (revision run, step A4) from the fullread2 files; used by scripts/32_manuscript_tables.py.
T5 = {
    'S002.1': ('Hosted LLMs propose PID gains for mistuned loops; simulation acceptance test', 'IMC tuning (4 worked cases)',
               'IMC lowest IAE in all 4 cases; LLMs passed the acceptance test in 75-89% of cases within 8 rounds'),
    'S002.2': ('Fine-tuned 0.6B model proposes PID gains; same acceptance test', 'IMC tuning (4 worked cases)',
               'IMC lowest IAE in all 4 cases; first proposal passed in 94% of 200 cases'),
    'S007.2': ('LLM agents tune state-feedback gains, ball and beam (adjacent)', "LQR (authors' weights)",
               'Lower tracking MSE than LQR, but 12-14% overshoot against 0-3%'),
    'S007.3': ('LLM agents tune PID, then state feedback, inverted pendulum (adjacent)', 'LQR; MATLAB PID Tuner (settings not given)',
               'Matches LQR (MSE 0.2531 vs 0.2529); beats PID Tuner'),
    'S007.4': ('Five LLMs tune state feedback, double inverted pendulum (adjacent)', "LQR (authors' weights)",
               'Best of 10 runs beats LQR on MSE; all models miss the overshoot target'),
    'S016.1': ('LLM picks a preference profile for fed-batch bioreactor setpoints; safety governor',
               'Deterministic MPC; same framework without the LLM',
               'Robustness index 0.893 vs 0.858 without the LLM and 0.812 for MPC; no spread reported'),
    'S016.2': ('Same, without the safety governor', 'Deterministic MPC; same framework without the LLM',
               'Higher productivity than MPC, but the dissolved-oxygen limit was crossed'),
    'S017.1': ('Local LLM agents replace PI constraint controllers, barn climate, 4-day run (adjacent)',
               'SIMC-tuned PI selector control', 'CO2 above limit 2.42 h vs 0.33 h for PI'),
    'S017.2': ('Same agents, rule orchestrator, cold ramp to -40 C (adjacent)', 'SIMC-tuned PI selector control',
               'Below 0 C for 3.38 h vs 3.62 h for PI, but a colder minimum (-8.3 vs -6.1 C)'),
    'S017.3': ('Same agents plus LLM supervisor, cold ramp (adjacent)', 'SIMC-tuned PI selector control',
               'Below 0 C for 3.40 h vs 3.62 h for PI, but a colder minimum (-7.3 vs -6.1 C)'),
    'S017.4': ('One LLM sets fan and heater directly, cold ramp (adjacent)', 'SIMC-tuned PI selector control',
               'Barn fell to -32.6 C vs -6.1 C for PI'),
    'S020.1': ('LLM picks a pre-verified controller mode after a fault, oscillator', 'LQI, MPC; same supervisor without the LLM',
               'IAE 2.313 with the LLM, 2.312 without'),
    'S020.2': ('LLM picks a PI mode after a fault, steel-sheet heating', 'Nominal PI; gain scheduling',
               'Supervisor better than PI after heater power loss, worse after a property change'),
    'S020.3': ('LLM comments on an adaptive fault-tolerant controller', 'Same controller without the LLM', 'No IAE change (2.364)'),
    'S032.1': ('LLM writes composition setpoints every 5 min over MPC, distillation column', 'Tuned linear MPC; tuned PID',
               'Better than MPC at reaching targets from off-nominal starts (P95 IAE 58.6 vs 162.1); '
               'about 10x worse at disturbance rejection'),
    'S032.2': ('Same, with a simulation gate that checks each setpoint 30 min ahead', 'Same agent without the gate',
               'Gate cut the worst-case (P95) IAE from 11.5 to 0.77 at one operating point'),
    'S032.3': ('LLM writes setpoints over PID, no MPC', 'PID alone', 'PID alone better on every disturbance'),
    'S037.2': ('LLM sets continuous heater power, two TCLab boards (hardware)', 'PID (tuning not reported)',
               'Time-weighted mean absolute error 1.03 vs 0.76 for PID'),
    'S037.3': ('Same, on a simulation model of the rig', 'PID (tuning not reported)', 'Best LLM time-weighted mean absolute error 0.62 vs 0.21 for PID'),
    'S041.1': ('LLM picks the matching stored regime model for MPC from a shortlist, numerical system', 'DTW numerical similarity',
               'Correct regime 87.9% vs 61.1% (90 switches x 100 repeats)'),
    'S041.2': ('Same, simulated CSTR', 'DTW numerical similarity; online model update', 'Better tracking in a figure; no numbers'),
    'S048.1': ('LLM acts as an on/off relay with hysteresis, simulated oven', 'Coded relay, same rule',
               'Same action at every step (100%); 73% agreement with sensor noise'),
    'S178.1': ('Fine-tuned LLM estimates model parameters for NMPC, CSTR', 'IPOPT least squares; MLP; metaheuristic',
               'Same closed-loop error as IPOPT (ISE 0.278 vs 0.283); 2.2 s per call vs 0.14 s'),
    'S178.2': ('Same, wastewater plant', 'IPOPT least squares; MLP; metaheuristic',
               'LLM alone IAE 0.882 vs 0.807 for IPOPT; MLP most accurate parameters'),
    'S180.2': ('LLM agents build crystallization population balance models from lab data', 'Published human-built model',
               'One LLM model matched it within the data; another was more consistent at equilibrium'),
    'S193.1': ('LLMs judge which of two PI gain sets gives lower IAE, quadruple tank', 'Numerical rule on the same data; chance',
               'LLM 46.8% correct vs 96.7% for the rule'),
    'S193.2': ('Same, two CSTRs with recycle', 'Numerical rule on the same data; chance', 'LLM 31.8% vs 49 of 50 for the rule'),
    'S193.3': ('Same, synthetic 3x3 plant', 'Numerical rule on the same data; chance', 'LLM 53.2% vs 47 of 50 for the rule'),
    'S195.1': ('LLM proposes PI gains from cost feedback, CSTR', 'Relay auto-tuning (Ziegler-Nichols)',
               'IAE 0.162 vs 0.106 for relay tuning'),
    'S195.2': ('LLM gives starting gains, Nelder-Mead refines, quadruple tank', 'VRFT; naive search; DE; BO',
               'Beats naive local search (10/10 vs 0/10 runs good); VRFT better (J 11.1 vs 12.0)'),
    'S195.3': ('Same, synthetic 3x3 plant', 'Differential evolution (DE); naive search',
               'Same cost as DE (J 2.17) with about 8x fewer evaluations'),
    'S195.4': ('LLM picks the VRFT time constant, quadruple tank', 'Median of measured rise times',
               'Rule usable in 10/10 runs vs LLM 8/10, equal J'),
    'S203.1': ('LLM writes the pump command as free text, water tank', 'PID (tuning not reported)', 'LLM produced text, not commands'),
    'S203.2': ('LLM writes the pump command as a number, water tank', 'PID (tuning not reported)', 'Level reached 1.6 of 10 m'),
    'S203.3': ('LLM retunes PID gains every 0.5 s, water tank', 'PID (tuning not reported)', 'Stable but irregular gains; no numbers'),
    'T0532.1': ('LLM turns text about wind into disturbance forecasts for MPC, robot (adjacent)', 'MPC with no forecast',
                'Closer tracking in plots; no numbers'),
    'T0532.2': ('Same, building battery and PV (adjacent)', 'MPC with no forecast', 'Cost $380 vs $911 over 500 days'),
    'T0665.1': ('LLM explains greenhouse MPC decisions with adaptive retrieval (adjacent)', 'Keyword retrieval with fixed templates',
                'Higher text-similarity scores (BERTScore 0.79 vs 0.68); no control effect'),
    'T0779.1': ('LLM designs mode-switching controllers, point robot (adjacent)', 'Single-mode designs; Bayesian optimization',
                'Lower sensing cost at equal performance; BO over hand-written templates matched it at 2 of 3 targets (about 30 and 48 runs), never at the third'),
    'T0779.2': ('Same, rangefinder control tasks (adjacent)', 'Single-mode designs', 'At least 20% lower resource cost'),
    'T0779.3': ('Same, cluttered navigation (adjacent)', 'Sweep of 768 single-mode designs', 'About 10x lower resource cost'),
    'T1053.1': ('LLM agent tunes a drive controller weight through an MCP server, 21 trials (adjacent)', 'One hand tune by the author',
                'Median ripple 0.85 vs 0.90 A at lower switching frequency'),
    # Stage B (2026-11-13)
    'S019.1': ('Fine-tuned 1.5B model picks heater power each step behind a rule validator, thermal zone (adjacent)',
               'The expert rule table it was trained to copy', '91.5% agreement with the rule; trajectories shown as an overlay only'),
    'S026.1': ('Fine-tuned LLM sets ramp-metering modes, freeway corridor (adjacent)', 'Published feedback controller; RL coordinators',
               'Throughput +6.62% vs feedback, +3.06% vs hierarchical RL; prompted LLMs did not beat feedback'),
    'S026.2': ('Same, cost-weight modes for virtual-power-plant dispatch (adjacent)', 'MPC-MILP with fixed weights; RL coordinators',
               'Cost -4.37% vs MPC-MILP, -2.49% vs hierarchical RL'),
    'S033.1': ('LLM writes the pump command each step, water tank', 'PID tuned with MATLAB PID Tuner',
               'Never reached the setpoint: IAE 510.7 vs 60.3 (3 runs)'),
    'S033.2': ('LLM retunes PID gains every 0.5 s, water tank', 'PID tuned with MATLAB PID Tuner',
               'IAE 49.2 vs 60.3 nominal; worst controller under sensor drift (538.1 vs 452.6)'),
    'S036.1': ('LLM agents pick and tune a controller, then adapt LQR gains through a simulation filter, web line',
               'MPC (tuning not reported)', 'Tension RMSE 1.04 vs 1.62 N and 0.29 vs 1.01 N'),
    'S205.1': ('LLM writes battery fast-charging code, refined through a constraint gate (adjacent)',
               'CC-CV rule; CMA-ES without the gate', 'Safe controller in 7/10 runs, target met in 2/10; fewer evaluations than CMA-ES'),
    'S205.2': ('Same, one shot without feedback (adjacent)', 'CC-CV rule; CMA-ES', '0/10 feasible controllers'),
    'T0615.1': ('LLM maps home-energy requests to tool calls, 30 prompts (adjacent)', 'Keyword parser',
                'Tool accuracy 96.67% vs 70%'),
    'T0615.2': ('LLM calls an economic MPC for a PV-battery home, one test day (adjacent)', 'Rule-based price-aware controller',
                'Rule earned 25.69 vs 19.26 rupees/day for the MPC'),
}
