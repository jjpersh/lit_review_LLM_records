# Synthesis tables

Source: extraction/extraction.csv (106 graded setups; 104 independent setups after counting 2 duplicate-experiment setups once (S203.2 = S033.1, S203.3 = S033.2); 47 papers; every paper read in full). Process systems only (sensitivity): 56 setups from 28 papers. Counts are per tested setup unless stated.

## Table 0. Headline counts: all graded setups and process systems only

| Count | All graded | Process systems only |
|---|---|---|
| Setups | 104 | 56 |
| Papers | 47 | 28 |
| E1 | 76 | 42 |
| E2 | 14 | 9 |
| E3 | 12 | 3 |
| E4 | 0 | 0 |
| E5 | 2 | 2 |
| Act | 15 | 7 |
| Succeeded | 37 | 17 |
| Conditional | 51 | 28 |
| Failed | 12 | 10 |
| Not shown | 4 | 1 |
| C1 = Y | 50 | 29 |
| Direct LLM vs non-LLM | 49 | 28 |
| Non-LLM better | 17 | 13 |
| Tie | 5 | 4 |
| Mixed | 11 | 6 |
| LLM better | 14 | 4 |
| Not quantified | 2 | 1 |
| C6 = Y | 29 | 18 |
| Safeguard described | 54 | 29 |
| Real time on hardware or plant | 14 | 5 |

Adjacent (excluded from the process-only column): robotics 7; motor drive 5; greenhouse 5; barn climate 4; mechatronic benchmark 3; building/thermal energy 2; battery charging 2; vehicle 2; home energy 2; inventory management 2; water reservoir network 2; marine vehicle 2; mechanical (crane) 2; traffic 1; grid / building energy 1; abstract symbolic planning 1; discrete manufacturing automation 1; discrete manufacturing 1; manufacturing machine HMI 1; manufacturing robotics 1; building energy 1.

## Table 1. Authority by evidence level (setups)

| Authority | E0 | E1 | E2 | E3 | E4 | E5 | Total |
|---|---|---|---|---|---|---|---|
| Advise | · | 3 | 5 | 1 | · | 2 | 11 |
| Propose | · | 25 | 6 | 1 | · | · | 32 |
| Set targets | · | 39 | 2 | 5 | · | · | 46 |
| Act | · | 9 | 1 | 5 | · | · | 15 |
| **Total** | · | 76 | 14 | 12 | · | 2 | 104 |

## Table 2. Outcome by authority (setups)

| Authority | Succeeded | Conditional | Failed | Not shown | Total |
|---|---|---|---|---|---|
| Advise | 3 | 2 | 3 | 3 | 11 |
| Propose | 12 | 18 | 2 | · | 32 |
| Set targets | 18 | 23 | 4 | 1 | 46 |
| Act | 4 | 8 | 3 | · | 15 |
| **Total** | 37 | 51 | 12 | 4 | 104 |

## Table 3. Outcome by theme (setups)

| Theme | Succeeded | Conditional | Failed | Not shown | Total | Papers |
|---|---|---|---|---|---|---|
| Language to MPC or tuning | 11 | 28 | 3 | 2 | 44 | 17 |
| LLM in or above the loop | 9 | 11 | 6 | · | 26 | 12 |
| LLM-facilitated hybrid control | 6 | 2 | · | 1 | 9 | 4 |
| SCADA, MCP and OPC integration | 9 | 4 | 1 | 1 | 15 | 9 |
| Recovery and safeguards | 2 | 6 | 2 | · | 10 | 5 |

## Table 3b. Outcome by control layer (setups)

| Layer | Succeeded | Conditional | Failed | Not shown | Total | Process only |
|---|---|---|---|---|---|---|
| operator | 6 | 6 | 1 | 3 | 16 | 8 |
| design | 12 | 13 | 4 | · | 29 | 19 |
| supervisory | 12 | 24 | 4 | 1 | 41 | 21 |
| actuation | 7 | 8 | 3 | · | 18 | 8 |

## Table 4. Appraisal criteria met (% of setups scored Y)

C1 right comparator · C2 control metrics · C3 off-nominal · C4 repeatable · C5 decision quality measured · C6 safeguards challenged.

| Theme | n | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|---|
| Language to MPC or tuning | 44 | 45% | 70% | 30% | 61% | 52% | 14% |
| LLM in or above the loop | 26 | 69% | 85% | 65% | 42% | 58% | 38% |
| LLM-facilitated hybrid control | 9 | 100% | 89% | 67% | 44% | 11% | 0% |
| SCADA, MCP and OPC integration | 15 | 20% | 40% | 60% | 47% | 60% | 47% |
| Recovery and safeguards | 10 | 0% | 50% | 100% | 80% | 100% | 60% |
| **All setups** | 104 | 48% | 69% | 53% | 55% | 56% | 28% |
| **Process systems only** | 56 | 52% | 66% | 71% | 57% | 61% | 32% |

Counts of Y (all setups): C1 50, C2 72, C3 55, C4 57, C5 58, C6 29.

## Table 4b. Domain (process type) by operation (setups)

| Domain | continuous | batch | not applicable or NR | Total | Papers |
|---|---|---|---|---|---|
| Reactors | 11 | 3 | 1 | 15 | 11 |
| Tanks and level | 7 | 2 | · | 9 | 6 |
| Separation and crystallization | 5 | 3 | 1 | 9 | 4 |
| Thermal and heating | 7 | · | · | 7 | 6 |
| Plant-wide and utilities | 2 | 2 | 2 | 6 | 5 |
| Generic process models | 6 | · | 4 | 10 | 8 |
| Climate (adjacent) | 12 | · | · | 12 | 6 |
| Machines and manufacturing (adjacent) | · | 1 | 25 | 26 | 12 |
| Energy, traffic and logistics (adjacent) | 5 | 2 | 3 | 10 | 4 |
| **Total** | 55 | 13 | 36 | 104 | 47 |

## Table 4c. Operation by theme (setups)

| Theme | continuous | batch | not applicable or NR |
|---|---|---|---|
| Language to MPC or tuning | 18 | 3 | 23 |
| LLM in or above the loop | 22 | 2 | 2 |
| LLM-facilitated hybrid control | 6 | · | 3 |
| SCADA, MCP and OPC integration | 4 | 5 | 6 |
| Recovery and safeguards | 5 | 3 | 2 |

## Table 5. Setups with a non-LLM comparator (C1 = Y)

| Study | Key | Setup | Evidence | Adjacent | Comparator | Class | Result |
|---|---|---|---|---|---|---|---|
| Shou 2026 | S002.1 | Hosted/unadapted LLM iterative PID tuning with dynamic prompts, gated  | E1 |  | Balanced IMC tuning, but only on 4 representative cases; IMC lowest IAE in all 4 | Non-LLM better | IMC lowest IAE in all 4 worked cases; LLMs pass acceptance in 75-89% of 200 cases |
| Shou 2026 | S002.2 | Qwen3-0.6B fine-tuned by SFT + PI-GRPO (stability-gated reward), same  | E1 |  | IMC on 4 representative cases only, IMC lowest IAE in 3 of 4 (Table S2 p.54-55); | Non-LLM better | IMC lowest IAE in all 4 worked cases;fine-tuned 0.6B passes 94% vs 56-71% hosted |
| Narimani‎ 2025 | S007.2 | Ball and beam: LLM agents tune FSF gains over 3 scenarios | E1 | mechatronic benchmark | LQR Q=diag(100,100,10,10) R=1, weights author-chosen, tuning not described (p.7) | Mixed | Lower MSE than LQR but overshoot 12-14% vs 0-3% |
| Narimani‎ 2025 | S007.3 | Inverted pendulum: LLM agents tune PID, Juror switches to FSF; 3 scena | E1 | mechatronic benchmark | LQR Q=diag(10,0) R=0.1 and MATLAB PIDTuner; PIDTuner settings not reported, mayb | Tie | FSF matches LQR (MSE 0.2531 vs 0.2529); beats MATLAB PID Tuner (settings not given) |
| Narimani‎ 2025 | S007.4 | Double inverted pendulum: FSF gain tuning by 5 different LLMs | E1 | mechatronic benchmark | LQR Q=diag(1,1,10,10) R=10; compared to best-of-10 LLM runs (Table 4 p.10) | Mixed | Best of 10 runs beats LQR on MSE; all models miss the overshoot target |
| Nozari 2026 | S016.1 | Full framework: GPT-4.1 supervisory agent proposes setpoints, Safety G | E1 |  | Deterministic MPC (same model, nominal params; tuning not detailed) and No-LLM f | LLM better | Robustness 0.893 vs 0.858 without the LLM and 0.812 for MPC |
| Nozari 2026 | S016.2 | No-Safety ablation: LLM agent proposal sent to regulatory layer withou | E1 |  | Same Table 7 comparison vs deterministic MPC and No-LLM (p.39) | Mixed | Higher productivity than MPC but DO limit crossed three times |
| Nogueira 2026 | S017.1 | Arch C: Qwen operator agents in ARC selector chain + Claude orchestrat | E1 | barn climate | SIMC-tuned PI ARC chain and no-LLM rule MAS (p.23) | Non-LLM better | CO2 above limit 2.42 h vs 0.33 h for PI selector control |
| Nogueira 2026 | S017.2 | Arch B: Qwen operator agents in ARC selector chain, rule orchestrator, | E1 | barn climate | SIMC-tuned PI ARC chain at 2 s (p.28) | Mixed | Less time below 0 C than PI (3.38 vs 3.62 h); colder minimum |
| Nogueira 2026 | S017.3 | Arch C: Qwen operators + Claude orchestrator tuner, Case IIB ramp | E1 | barn climate | SIMC-tuned PI ARC chain at 2 s (p.28) | Mixed | Less time below 0 C than PI (3.40 vs 3.62 h); colder minimum |
| Nogueira 2026 | S017.4 | Arch D ablation: single Qwen model sets fan and heater directly, Case  | E1 | barn climate | SIMC-tuned PI ARC chain (p.28) | Non-LLM better | Barn fell to -32.6 C vs -6.1 C for PI selector control |
| Wang 2026 | S019.1 | Closed-loop sim: fine-tuned SLM picks heater power, rule-equality vali | E1 | building/thermal energy | HRBC rule table shown as trajectory overlay only; it is also ground truth/ceilin | Not quantified | Trajectory close to the rule table it imitates (91.5% agreement); overlay only |
| Papacharalampopoulos 2026 | S020.1 | LLM selects bounded controller mode over residual-based switched LQI,  | E1 |  | Riccati-tuned LQI, MPC (same costs), CFG, SIGS, RLS adaptive FTC, and no-LLM cog | Tie | LLM changed IAE 2.313 to 2.312 |
| Papacharalampopoulos 2026 | S020.2 | LLM selects bounded PI mode for 1-D thermal steel-sheet heating with r | E1 |  | nominal PI (gains given, tuning not stated), SIGS, CFG 0.5x gains (p.13-14) | Mixed | Framework better than PI on power loss, worse on phase change |
| Papacharalampopoulos 2026 | S020.3 | LLM audit call on RLS adaptive fault-tolerant controller (AFTC+LLM) | E1 |  | compared with cognitive switched LQI and standalone LQI (p.16-17) | Tie | No IAE change (2.364) |
| He 2026 | S026.1 | LLM sets per-ramp hysteresis-band modes for 8 ramp-metering gates (SUM | E1 | traffic | published feedback controller, PPO end-to-end, Hierarchical RL with grid-searche | LLM better | Throughput +6.62% vs feedback control, +3.06% vs hierarchical RL |
| He 2026 | S026.2 | LLM sets per-resource cost-weight modes for MILP dispatch of a VPP (Op | E1 | grid / building energy | MPC-MILP fixed conventional coefficients, PPO end-to-end, Hierarchical RL, exhau | LLM better | Cost -4.37% vs MPC-MILP, -2.49% vs hierarchical RL |
| Rosenthal 2026 | S032.1 | C2: ungated LLM supervisor sets composition setpoints over linear-MPC  | E1 |  | Pareto-swept linear MPC x100 ref and TL-tuned PID by pre-registered shootout (p. | Mixed | Better than tuned MPC at re-targeting; about 10x worse at disturbance rejection |
| Rosenthal 2026 | S032.2 | C3: LLM supervisor plus forked-twin counterfactual safety gate over MP | E1 |  | vs C2 ungated, with C1 MPC (~0.38 IAE) and C0/C1 nominal refs (p.11, p.14) | With vs without gate | Gate cuts attractor P95 IAE 11.46 to 0.77; makes one operating point run-fatal |
| Rosenthal 2026 | S032.3 | C2_pid: ungated LLM supervisor directly over unmodified PID regulatory | E1 |  | vs C0 TL-tuned PID, C1 MPC and C2-over-MPC (p.22-23) | Non-LLM better | PID alone better on every disturbance arm |
| Wen 2026 | S033.1 | Direct LLM actuation: LLM writes pump valve opening each step (clamped | E1 |  | vs ZN-refined PID and MATLAB PID Tuner autotuned PID (p.5) | Non-LLM better | IAE 510.7 vs 60.3 for autotuned PID; level 8.5 m short |
| Wen 2026 | S033.2 | Hybrid LLM-PID: LLM retunes PID gains (Kp Ki Kd N) every 0.5 s with fo | E1 |  | vs ZN-refined PID and MATLAB PID Tuner autotuned PID; no adaptive or high-gain P | Mixed | Nominal IAE 49.2 vs 60.3 for autotuned PID; worst under sensor drift (538.1 vs 452.6) |
| Li 2025 | S036.1 | LLM agents select/tune PID-MPC-LQR, then propose LQR gain updates gate | E1 |  | MPC baseline beaten on RMSE; its tuning NR and not adapted to plant, so uneven ( | LLM better | Tension RMSE 1.04 vs 1.62 N and 0.29 vs 1.01 N vs MPC (tuning not reported) |
| Mercangöz 2025 | S037.2 | Physical dual-TCLab, fan disturbance: LLM sets continuous q1,q2 via LL | E3 |  | PID on same hardware; tuning method not reported (p.15 Table 5, Fig. 8) | Non-LLM better | PID error 0.76 vs LLM 1.03 on hardware (time-weighted MAE) |
| Mercangöz 2025 | S037.3 | Digital twin of dual-TCLab, same disturbance: LLM sets continuous q1,q | E1 |  | PID on twin, tuning not reported; PID run ~1200 s vs LLM ~1800 s (Table 5, Fig.  | Non-LLM better | PID error 0.21 vs best LLM 0.62 on the twin (time-weighted MAE) |
| Zhang 2025 | S041.1 | Numerical 10-condition system: LLM picks stored SINDy model for MPC af | E1 |  | DTW numerical similarity, ETASI online update, retraining; tuning not described  | LLM better | Identification 87.9% vs 61.1% for numerical similarity (DTW) |
| Zhang 2025 | S041.2 | CSTR (feed-flow conditions): LLM picks stored SINDy model for MPC, 1-> | E1 |  | DTW and ETASI with identical MPC settings Np=10 Nc=5 (p.12) | Not quantified | Better tracking than DTW in a figure; no numbers |
| Rojas-Ordoñez 2025 | S048.1 | LLM as direct on/off relay controller with schema validator + retry +  | E1 |  | Coded relay with hysteresis, same rule and timing (p.9-10); not PID/MPC but exac | Tie | 100% agreement with the coded relay; 73% under noise |
| Ibáñez-Espinel 2026 | S178.1 | CSTR: fine-tuned LLM estimates model parameters for NMPC (8 LLM/hybrid | E1 |  | CasADi/IPOPT multistart NLS estimator, GWO, MLP baselines (p.2, p.9) | Tie | LLM estimates give ISE 0.278 vs IPOPT 0.283, statistically equivalent |
| Ibáñez-Espinel 2026 | S178.2 | WWTP (MIMO): fine-tuned LLM estimates model parameters for NMPC (8 LLM | E1 |  | IPOPT, GWO, MLP baselines; Powell/SR ablations (p.9, p.13) | Non-LLM better | LLM-only IAE 0.882 vs IPOPT 0.807; LLM plus Powell ties IPOPT |
| Lima 2026 | S180.2 | CS2: LLMs build/calibrate/update moment PBMs from lab crystallization  | E2 |  | compared with human-built literature PBM of Moraes et al. (Figs 4-8, p.7-12) | Mixed | One LLM model matched the literature PBM in the data window; another was more consistent at equilibrium |
| Chen 2026 | S193.1 | LLM ranks two PI gain sets by IAE (quadruple tank); Q/E/T/X/S info var | E2 |  | Non-LLM numerical oracle on displayed rows 96.7% vs LLM ~51%; magnitude rules (p | Non-LLM better | Numerical rule 96.7% correct vs LLM pairwise ranking 46.8% |
| Chen 2026 | S193.2 | LLM ranks two PI gain sets by IAE (series CSTR with recycle); Q/E/T/X/ | E2 |  | Non-LLM numerical oracle on displayed rows 49/50 correct vs LLM near/below chanc | Non-LLM better | Numerical rule 49/50 vs LLM 31.8% |
| Chen 2026 | S193.3 | LLM ranks two PI gain sets by IAE (synthetic 3x3 cyclic plant); Q/E/T/ | E2 |  | Non-LLM numerical oracle on displayed rows 47/50 correct vs LLM near chance (p.8 | Non-LLM better | Numerical rule 47/50 vs LLM 53.2% |
| Shu 2026 | S195.1 | CSTR single loop: scaffolded LLM iteratively proposes PI gains with cl | E1 |  | relay-feedback ZN (tuned auto-tuner) and multi-start optimum (p.12) | Non-LLM better | Relay-ZN IAE 0.106 vs LLM 0.162 |
| Shu 2026 | S195.2 | Quadruple-tank 2x2: scaffolded LLM proposes PI gains over 18 rounds, t | E1 |  | relay-ZN, NM, LHS-NM, DE, BO, decoupler, grid and VRFT; VRFT beats hybrid (p.6,  | Mixed | Beats naive search (10/10 vs 0/10); VRFT better (J 11.12 vs 12.0) |
| Shu 2026 | S195.3 | Synthetic 3x3 cyclic coupled plant: scaffolded LLM gains plus Nelder-M | E1 |  | DE (10 runs per budget), naive NM 20 starts, inverse-gain heuristic; no VRFT (p. | LLM better | Same cost as DE (J 2.17) with about 8x fewer evaluations |
| Shu 2026 | S195.4 | Quadruple-tank: LLM proposes VRFT reference time constant tau from ris | E1 |  | 11-point tau grid scan and median rise-time rule; median rule wins (p.21) | Non-LLM better | Median rule 10/10 seeds vs LLM 8/10, equal J |
| Wen 2026 | S203.1 | Trial 1: LLM as direct controller, free-text output (water tank) | E1 |  | conventional PID in Fig.3, tuning not reported, ~25% overshoot (p.3-4) | Non-LLM better | LLM produced text, not commands |
| Caracciolo 2026 | S205.1 | MCP-DT: LLM iteratively writes charging-controller code with constrain | E1 | battery charging | CC-CV industry rule (untuned) and CMA-ES optimizer, but CMA-ES unconstrained so  | Mixed | Safe controller in 7/10 runs with fewer evaluations than CMA-ES; target met in 2/10; best beats CC-CV |
| Caracciolo 2026 | S205.2 | Zero-shot: LLM writes one charging algorithm without simulation feedba | E1 | battery charging | same CC-CV and unconstrained CMA-ES comparators (p.5-6) | Non-LLM better | 0/10 feasible controllers vs CC-CV rule |
| Wu 2025 | T0532.1 | LLM (L2D) forecasts wind disturbance from text for MPC; 2D robot astro | E1 | robotics | Classic MPC with zero disturbance forecast (=LQR) (p.5); no non-LLM forecaster b | LLM better | Closer tracking than MPC without forecasts (plots only) |
| Wu 2025 | T0532.2 | LLM (L2D) forecasts PV/demand disturbance from text for battery-chargi | E1 | building energy | Classic MPC with zero disturbance forecast (p.6); no non-LLM forecaster or oracl | LLM better | Cost $380 vs $911 for MPC without forecasts |
| Raghavan 2025 | T0615.1 | LLM tool-calling benchmark: 30 curated HEMS prompts mapped to JSON too | E2 | home energy | Keyword parser baseline (70% tool acc, 77.78% F1); rule baseline for parsing, no | LLM better | Tool accuracy 96.67% vs 70% for a keyword parser |
| Raghavan 2025 | T0615.2 | Integrated LLM-MPC HEMS: LLM invokes economic MPC/appliance tool on si | E1 | home energy | Price-blind and heuristic price-aware rule controllers; no arm isolating LLM vs  | Non-LLM better | Heuristic price-aware rule earned 25.69 vs 19.26 rupees/day for the LLM-called MPC |
| Naagarajan 2025 | T0665.1 | ARAG chatbot (RAG + GPT-4o) explaining offline greenhouse MPC trajecto | E1 | greenhouse | Keyword/template non-LLM baseline, deliberately simple strawman (p.6-7); no cont | LLM better | Better text metrics than keyword retrieval (BERTScore 0.79 vs 0.68) |
| Krishna 2026 | T0779.1 | point-to-disk, LLM-evolved MSC designs trained by MSC-PPO (CostlyGPS/C | E1 | robotics | 10 monolith seed frontier (Table 4, p.24) and BayesOpt on 4 MSC templates (BO-MS | LLM better | BO on templates matched at 2 of 3 targets, never at the third |
| Krishna 2026 | T0779.2 | RF-DMC rangefinder cartpole/cup-catch/finger-spin, LLM-evolved MSC + M | E1 | robotics | 11 monolithic rangefinder configurations spanning cost range (Table 7, p.26); no | LLM better | At least 20% lower resource cost than single-mode designs |
| Krishna 2026 | T0779.3 | clutter-nav: LLM-designed multi-mode radar + MPPI planner configuratio | E1 | robotics | dense sweep of 768 monolithic sensor+MPPI configurations (p.28-29) | LLM better | About 10x lower resource cost than single-mode designs |
| Šmídl 2026 | T1053.1 | Claude agent via MCP server + CLAUDE.md, engineer gate; tunes FCS-MPC/ | E1 | motor drive | single author hand-tune of lambda_sw (Table II p.6); no optimizer or systematic  | LLM better | Ripple 0.85 vs 0.90 A at lower switching frequency than one hand tune |

Direct LLM-versus-non-LLM comparisons: 49 setups from 24 papers: Non-LLM better 17, Tie 5, Mixed 11, LLM better 14, Not quantified 2.
Process systems only: 28 setups from 14 papers: Non-LLM better 13, Tie 4, Mixed 6, LLM better 4, Not quantified 1.

## Table 6. Safeguard architectures (setups that describe one)

| Study | Key | Type | Safeguard | Challenged (C6) | What was tested |
|---|---|---|---|---|---|
| He 2026 | S026.2 | Bounds | MILP hard bounds, feeder curtailment, schema check | Y | MILP hard bounds, schema fallback, feeder curtailment gate counted: 5.2 vs 9.4 MPC violati |
| Nerantzis 2026 | S315.1 | Data-quality gate | Trust gate on sensor-data quality (MCP) | Y | Gate blocked all 8 aggressive proposals made under low trust (8/8, p.3-4); natural, not in |
| Vyas 2026 | S022.1 | Simulation gate | Simulation validation, reprompt limit, deterministic fallback | Y | Validator rejected bad LLM plans -> reprompt; recovery 33-100% (p.10); gate misses not aud |
| Vyas 2026 | S022.2 | Simulation gate | Simulation validation, reprompt limit, deterministic fallback | Y | Validator rejected setpoints; ~2 reprompts typical; 4o-mini hit limit -> fallback (p.11) |
| Rosenthal 2026 | S032.2 | Simulation gate | Forked-twin gate, 9 constraints | Y | Gate challenged by real bad proposals: follower tails blocked, but onset false negatives ( |
| Gill 2025 | S043.1 | Simulation gate | Digital-twin simulation and rule validator, reprompt | Y | Twin sim + validation script rejected proposals 1-10 reprompts/run (p.7); forced execution |
| Caracciolo 2026 | S205.1 | Simulation gate | Constraint layer in digital twin, feedback to LLM | Y | constraint layer rejected 125 unsafe LLM candidates; all 7 final controllers 0 violations  |
| Caccia 2026 | T1044.2 | Simulation gate | Nominal-model simulation check of the LLM cost, retries | Y | gate faced real bad LLM costs; 3B task 3 fell 26%->0% (false rejects), 3B task 2 aborted 2 |
| Caccia 2026 | T1044.4 | Simulation gate | Nominal-model simulation check of the LLM cost, retries | Y | gate faced real bad costs; still passed failing ones: 7B task 1 86% success with 100% vali |
| Caccia 2026 | T1044.6 | Simulation gate | Nominal-model simulation check of the LLM cost, retries | Y | gate faced real bad costs; 7B task 3 32%->97%, but 3B passed many failing costs (28-48%) ( |
| Caccia 2026 | T1044.8 | Simulation gate | Nominal-model simulation check of the LLM cost, retries | Y | gate faced real bad costs; 3B still 52-74% success after gate (p.9) |
| Khan 2026 | T1046.1 | Simulation gate | Shadow-plant check with correction loop | Y | Gate challenged: 1,490 violating proposals blocked, 0 reached plant (p.8); all caught by r |
| Khan 2026 | T1046.2 | Simulation gate | Shadow-plant check with correction loop | Y | Gate challenged: 62 violating proposals blocked across tiers (p.8); 0 violations reached p |
| Shou 2026 | S002.1 | Validator | Closed-loop acceptance criteria | Y | Sim acceptance gate rejected failing proposals, e.g. aggressive 45.78% overshoot (p.26); g |
| Shou 2026 | S002.2 | Validator | Closed-loop acceptance criteria | Y | Routh-Hurwitz/phase-margin gate in reward plus sim acceptance; failing outputs rejected (p |
| Nozari 2026 | S016.1 | Validator | Independent safety governor | Y | Governor repaired up to 19.8% and fell back on 1.8% of proposals in S6, 0 residual violati |
| Wang 2026 | S019.1 | Validator | Rule-equality validator, reprompt, rule fallback | Y | gate challenged by real wrong actions (Fig 5 reprompts/failures); validator is the oracle; |
| Wang 2026 | S019.2 | Validator | Rule-equality validator, reprompt, rule fallback | Y | avg reprompts per step 0.16/0.09/0.38 show gate catching mismatches (p.5) |
| He 2026 | S026.1 | Validator | Schema check, hold previous mode | Y | schema validator with hold-previous fallback, triggered by real malformed outputs; format  |
| Schall 2026 | S030.1 | Validator | P&ID-grounded deterministic validator | Y | 43 injected proposals (35 unsafe), FN=0 across all scenarios; all flagged in variance runs |
| Schall 2026 | S030.2 | Validator | P&ID-grounded deterministic validator | Y | Error injection FN=0 pooled over 5 scenarios; 10/10 WARNs here were false positives on val |
| Schall 2026 | S030.3 | Validator | P&ID-grounded deterministic validator | Y | Error injection FN=0 pooled; 20/20 invalid proposals flagged in variance runs (p.12-13) |
| Mercangöz 2025 | S037.1 | Validator | Path simulator, LLM validator and reprompter | Y | Simulation agent/validator caught real invalid paths; LLaMA still 0.30 valid at 25 nodes ( |
| Mercangöz 2025 | S037.2 | Validator | LLM validator and reprompter agents | Y | Power gate rejected 20 out-of-range proposals; but best action applied after iteration cap |
| Mercangöz 2025 | S037.3 | Validator | LLM validator and reprompter agents | Y | Power/temp gates rejected real proposals (LLaMA 9 and 6 power reprompts); gates are LLMs;  |
| Mercangöz 2025 | S038.1 | Validator | LLM validator and reprompter agents | Y | Validator rejected real bad actions (e.g. 169 of 423 GPT-3.5); validator itself is an LLM, |
| Xue 2026 | S239.1 | Validator | LLM guardrail classifies each tool call | Y | gate challenged with 424 unsafe proposals incl. injected and malicious (p.7-8) |
| Silva 2025 | S264.1 | Validator | Tool argument assertions | Y | Tool assertions rejected bad user inputs (p.3-4); no LLM-generated bad proposals tested |
| Kasai 2026 | S302.1 | Validator | STAMP/CAST safety-constraint stage | Y | constraint stage challenged by unsafe 3.0 MPa manual instruction; rejected 10/10 (p.3) |
| Narimani‎ 2025 | S007.1 | Bounds | Gain ranges, simulation scoring | N | Only prompt-stated gain ranges and simulation scoring; never challenged with bad proposals |
| Narimani‎ 2025 | S007.2 | Bounds | Gain ranges, simulation scoring | N | Gain ranges + simulation only; not challenged with bad proposals (p.5) |
| Narimani‎ 2025 | S007.3 | Bounds | Gain ranges, simulation scoring | N | Gain ranges + simulation only; not challenged with bad proposals (p.5) |
| Narimani‎ 2025 | S007.4 | Bounds | Gain ranges, simulation scoring | N | Gain ranges + simulation only; not challenged with bad proposals (p.5) |
| Nogueira 2026 | S017.1 | Bounds | Schema, clip-and-slew clamp, more layers | N | schema, clamp, Lever A, fallback, freeze guard described (p.18); never challenged, 0 fallt |
| Nogueira 2026 | S017.2 | Bounds | Schema, clip-and-slew clamp, more layers | N | direction guard, move suppression, MIN/MAX chain (p.28); not challenged with bad proposals |
| Nogueira 2026 | S017.3 | Bounds | Schema, clip-and-slew clamp, more layers | N | schema-validated bounded supervisor outputs, freeze guard (p.18-19); not challenged |
| Papacharalampopoulos 2026 | S020.1 | Bounds | Bounded mode set, dwell time, fallback | N | bounded action set and timeout fallback described but never challenged with invalid/failed |
| Papacharalampopoulos 2026 | S020.2 | Bounds | Bounded mode set, dwell time, fallback | N | fallbacks described but not challenged (p.9) |
| Song 2026 | S031.1 | Bounds | CBF constraint in MPC; LLM sets gamma | N | CBF is the safety layer but LLM sets gamma; gamma=1 collides; not challenged with bad prop |
| Song 2026 | S031.3 | Bounds | CBF constraint in MPC; LLM sets gamma | N | CBF present; not challenged with bad LLM proposals; 22% still collide (p.11) |
| Wen 2026 | S033.1 | Bounds | Command clamped to 0-1 | N | Only clamping to [0;1]; no gate challenged (p.5) |
| Rojas-Ordoñez 2025 | S048.1 | Bounds | Output schema, retries, coded fallback | N | Validator/retry/fallback described (p.7) but never triggered (0 failures, p.14); not chall |
| Miyaoka 2026 | S272.1 | Bounds | Constrained tool set | N | tool set restricted and mandatory cost term (p.2-3) but never challenged |
| Miyaoka 2026 | S272.2 | Bounds | Constrained tool set | N | restricted tools described (p.2) but no bad proposals tested |
| Arif 2025 | T1042.1 | Bounds | Safe gain range stated in the prompt; voltage clip | N | Prompt-stated safe gain range and ±8 V clip (pp.7,19); never challenged with bad proposals |
| Arif 2025 | T1042.2 | Bounds | Safe gain range stated in the prompt; voltage clip | N | Prompt-stated safe range and ±8 V clip (pp.7,20); agent self-aborted once (App. B.1) but b |
| Tohma 2025 | S013.1 | Human approval | User accepts the design | N | User 'Accept Design' button described (p.2), never challenged; no validator for LLM target |
| Pershing 2026 | S262.1 | Human approval | Operator approves each LLM command (y/n) | N | Human y/n approval present (p.3) but never challenged with bad proposals |
| González 2026 | S156.1 | Separation | Deterministic supervisor between LLM and equipment | N | Deterministic Supervisor/read-only LLM described (pp.17-18) but never challenged with bad  |
| Šmídl 2026 | T1053.1 | Separation | Argument checks and engineer approval in MCP server; current clamp in the drive layer | N | clamp, arg validation, approval gate described (p.4-5); no bad proposals injected to test  |
| Li 2025 | S036.1 | Simulation gate | Simulation safety filter on gain updates | N | Sim safety filter (limits, improvement, robustness) described; no rejected proposals repor |
| Wen 2026 | S033.2 | Validator | Format and finite-value check only | N | Parser rejects malformed/non-finite gains (p.12); no bound on size/rate; aggressive gains  |
| Christofides 2026 | S269.1 | Validator | Branch, unit and read-back checks in tool server | N | Gates (branch, unit, read-back) described; challenged only by pre-existing model faults, n |
| Christofides 2026 | S269.2 | Validator | Branch, unit and read-back checks in tool server | N | Unit-mismatch catch was in model vs reference, not an LLM bad proposal; no ablation (p.47) |

Setups describing a safeguard: 54; challenged (C6 = Y): 29 setups from 17 papers. By type: Validator 19, Bounds 18, Simulation gate 12, Human approval 2, Separation 2, Data-quality gate 1.

## Table 7. Timing (descriptive)

| Study | Key | LLM latency | Loop timing | Plant timing |
|---|---|---|---|---|
| Shou 2026 | S002.1 | NR | Up to 8 tuning rounds per case; sim Δt 0.1 s, 4000 s horizon (p.16) | NR |
| Shou 2026 | S002.2 | NR | Pass@1 single recommendation, up to 8 rounds; sim Δt 0.1 s (p.16,p.29) | NR |
| Rueda 2026 | S004.1 | NR | Control interval 0.25 s; LLM used offline for design (p.5) | NR |
| Narimani‎ 2025 | S007.1 | NR | NR (offline design; 27 iterations p.6) | NR |
| Narimani‎ 2025 | S007.2 | NR | NR (offline; 14/5/47 iterations p.7) | NR |
| Narimani‎ 2025 | S007.3 | NR | NR (offline; capped at 4 iterations per cycle p.7) | NR |
| Narimani‎ 2025 | S007.4 | NR | NR (offline; convergence ~50-120 iterations, p.9) | NR |
| Nozari 2026 | S016.1 | 2.9 s per decision (p.29) | 5 min supervisory interval (p.25) | NR |
| Nozari 2026 | S016.2 | 2.9 s per decision (p.29) | 5 min supervisory interval (p.25) | NR |
| Nogueira 2026 | S017.1 | ~1 s per sample on GPU (p.28); 100-500 ms per Qwen call (p.35) | operators 5 min; Claude supervisor 600 s (p.13, 18) | NR |
| Nogueira 2026 | S017.2 | ~1 s per sample (p.28) | 60 s operator cadence (p.28) | NR |
| Nogueira 2026 | S017.3 | ~1 s per operator sample (p.28); Claude NR | 60 s operators (p.28); supervisor period NR for this case | NR |
| Nogueira 2026 | S017.4 | ~1 s per sample (p.28) | 60 s (p.21) | NR |
| Wang 2026 | S019.1 | 3.84 s mean (Table IV); 4.84 s and 5.28 s in figure captions | one LLM decision per sim step; step length NR | NR |
| Wang 2026 | S019.2 | 3.84 s SLM, 4.50 s GPT-4o, 6.28 s DeepSeek-V3 | NR | NR |
| Papacharalampopoulos 2026 | S020.1 | NR (LLM called 0.4 s after detection by design; p.27 calls it 0.4 s audit delay) | dt = 0.01 s; LLM once per fault event, 0.4 s after detection (p.11, p.24) | NR |
| Papacharalampopoulos 2026 | S020.2 | NR | PI at 1 ms; LLM 0.4 s after detection (p.13 p.22) | NR |
| Vyas 2026 | S022.1 | Planning 2.4 s; action 2.2 s (4.1-mini), 3.0 s (4o-mini); wall-clock 32.7/40.7 s per run ( | Agents invoked at each discrete supervisory step needing a state transition (p.11) | NR |
| Vyas 2026 | S022.2 | Action agent mean 2.1 s (4.1-mini) vs 2.7 s (4o-mini), range 1.9-3.5 s; wall-clock 51.9/43 | Decision loop typically triggered once per run after fault detection (p.11) | NR |
| He 2026 | S026.1 | ~1.6 s per decision (p.20) | LLM every 3 min; gate rule every 1 min (p.5) | NR |
| He 2026 | S026.2 | ~0.4 s per decision (p.20) | LLM every 30 min; MILP every 5 min (p.5) | NR |
| Hidalgo-Castelo 2026 | S028.1 | mean 9.84/11.23/16.47 s simple/moderate/complex (p.8) | n8n 20 s cycle; full context regeneration every 30 min (p.6) | real time (plant) |
| Schall 2026 | S030.1 | approx. 2-8 s per LLM call (p.16) | NR (static snapshot; Monitor cycle Δt configurable p.4) | NR |
| Schall 2026 | S030.2 | approx. 2-8 s per LLM call (p.16) | NR (static snapshot) | NR |
| Schall 2026 | S030.3 | approx. 2-8 s per LLM call (p.16) | NR (static snapshot) | NR |
| Song 2026 | S031.1 | NR | MPC step 0.04 s; obstacle sensing 0.67 s; LLM called per subtask (p.8-9) | NR |
| Song 2026 | S031.2 | NR | not applicable | not applicable |
| Song 2026 | S031.3 | 2.4 s mean OpenAI API round trip over 50 episodes (p.11) | MPC step 0.04 s; sensing 0.67 s; LLM on demand at user feedback (p.8-11) | NR |
| Rosenthal 2026 | S032.1 | median 15.3 s, IQR 11.3-21.0, max 278 s per cycle (Fig.5 p.14) | 5 min supervisory; 1-5 s regulatory (p.4) | NR |
| Rosenthal 2026 | S032.2 | median 18.6 s, IQR 15.2-23.3, max 63 s per cycle (Fig.5 p.14) | 5 min supervisory; gate 30-min fork horizon (p.7) | NR |
| Rosenthal 2026 | S032.3 | NR | 5 min supervisory; 1-5 s regulatory (p.4) | NR |
| Wen 2026 | S033.1 | ~0.3 s per query (p.6) | Every simulation step (0.1 s solver) (p.5) | NR |
| Wen 2026 | S033.2 | ~0.3 s per query (p.6) | LLM gain update 0.5 s, held by ZOH; PID on 0.1 s solver (p.6) | NR |
| Li 2025 | S036.1 | NR | Iterative offline adaptation cycles (Adapt1-3); up to 50 tuning iterations (p.5) | NR |
| Mercangöz 2025 | S037.1 | Avg 1.66-4.28 s per cycle (GPT), up to 36.86 s (LLaMA) (pp.10-12) | Up to 5 reprompt cycles per FSM (p.9) | NR |
| Mercangöz 2025 | S037.2 | Mean 34.18 s, SD 16.86, 10.58-72.69 s, n=53 (Table 4 p.13) | Powers held 30 s per decision (p.22); real cycle set by inference | real time (hardware) |
| Mercangöz 2025 | S037.3 | Mean 12.49 s, SD 8.85, 5.12-93.00 s, n=148 (Table 4 p.13) | Fixed 30-s planning interval, twin paused for inference (p.12) | NR |
| Mercangöz 2025 | S038.1 | NR | Event-paced by inference; 128-554 decisions per 40-min run (Table 1 p.5) | real time (hardware) |
| Zhang 2025 | S041.1 | 47.3 s per query (p.10) | ApEn window 50, step 20 (p.9) | NR |
| Zhang 2025 | S041.2 | NR | sampling 0.015 h (p.12) | NR |
| Rasheed 2025 | S042.1 | NR | NR (training data sampled at 60 s, p.3) | real time (hardware) |
| Rasheed 2025 | S042.2 | NR | NR (training data sampled at 60 s, p.3) | real time (hardware) |
| Rasheed 2025 | S042.3 | NR | NR (training data sampled at 60 s, p.3) | real time (hardware) |
| Rojas-Ordoñez 2025 | S048.1 | NR | Ts = 1 s per step, LLM queried every step (Table 1 p.6) | NR |
| González 2026 | S156.1 | LLM query median 1-2 s (Table 7, p.30); few seconds end-to-end (p.40) | Sensors 100-1000 ms; logged 1 s; enriched data 1-5 s; LLM on operator query (pp.18-19, 33) | real time (plant) |
| Ibáñez-Espinel 2026 | S178.1 | 2.183 s/call Qwen2.5-0.5B, 2.602 s Qwen-Math, 4.5-5.6 s dual (p.11) | estimation at scheduled instants after full window; NMPC solve ~0.23 s; sampling time in s | NR |
| Ibáñez-Espinel 2026 | S178.2 | 3.89-6.94 s/call LLM variants (p.14) | parameter update every 60 steps (p.16); NMPC solve 0.13-0.15 s (p.14) | NR |
| Lima 2026 | S180.1 | NR | 1 min NMPC sampling; LLM offline design (p.14) | NR |
| Lima 2026 | S180.2 | Claude Opus >=2 h per prompt; others ~15-20 min per prompt (p.10) | NR | NR |
| Chen 2026 | S193.1 | median 0.18-0.64 s per request (p.27) | PI: 120 control intervals over horizon 400 (p.25); LLM offline | NR |
| Chen 2026 | S193.2 | median 0.18-0.64 s per request (p.27) | PI: 120 control intervals over horizon 240 (p.25); LLM offline | NR |
| Chen 2026 | S193.3 | median 0.18-0.64 s per request (p.27) | discrete plant dt 0.2; 120 steps (p.5; p.26); LLM offline | NR |
| Chen 2026 | S193.4 | NR | PI: 120 control intervals over horizon 400 (p.25); LLM proposes offline per episode | NR |
| Shu 2026 | S195.2 | NR | 120 control steps over 400 s episode; LLM offline, 18 rounds per run (p.5) | NR |
| Shu 2026 | S195.3 | NR | dt=0.2 s, 120 steps; LLM offline, 18 rounds (p.19) | NR |
| Caracciolo 2026 | S205.1 | NR | offline synthesis, up to 20 iterations per run; LLM not in real-time loop (p.4,p.7) | NR |
| Caracciolo 2026 | S205.2 | NR | single generation, offline (p.6) | NR |
| Pershing 2026 | S262.1 | NR | MPC 5 s sample (p.2); LLM on operator request | real time (hardware) |
| Christofides 2026 | S269.1 | NR | LLM offline; history 0.02 h (p.33) | NR |
| Christofides 2026 | S269.3 | NR | 0.5 s controller sampling; LLM not in loop (p.38) | NR |
| Miyaoka 2026 | S272.1 | NR | MPC dt=0.04 s; agent event-triggered, asynchronous (p.4-5) | NR |
| Miyaoka 2026 | S272.2 | NR | MPC dt=0.04 s; agent event-triggered, asynchronous (p.4-5) | NR |
| Kasai 2026 | S302.1 | mean 4:38, max 4:55 end-to-end per procedure (p.3) | NR | NR |
| Kasai 2026 | S302.2 | not recorded (Table II, p.3) | NR | NR |
| Nerantzis 2026 | S315.1 | NR | one decision step per simulated day; 7 steps per scenario, 56 total (p.3-4) | NR |
| Wu 2025 | T0532.1 | NR | LLM forecast every MPC step (p.2 fn3); DPO batch update at |D|=240 (p.5) | NR |
| Wu 2025 | T0532.2 | NR | DPO batch update at |D|=500 (p.5); control step NR | NR |
| Naagarajan 2025 | T0608.1 | NR | 5-min trajectory points; day-ahead summary (p.3) | NR |
| Raghavan 2025 | T0615.1 | 0.703 s Phi-3 Mini; 1.634-2.801 s other LLMs (p.10) | Per user query | NR |
| Raghavan 2025 | T0615.2 | 0.703 s Phi-3 Mini (p.10) | MPC 15-min interval, 8 h horizon, 1.82 s solve (p.10, p.13) | NR |
| Naagarajan 2025 | T0665.1 | GPT-4o 2.17 s (Table 2, p.4); ARAG 21.1 s per query vs baseline 8.4 s (Fig. 8, p.10) | On-demand queries; MPC data at 5-min intervals (p.3) | NR |
| Krishna 2026 | T0779.1 | NR | controller 50 Hz (p.22); LLM once per design, 8 generations (p.24) | NR |
| Krishna 2026 | T0779.2 | NR | cartpole 100 Hz, cup/finger 50 Hz (pp.24-25); 10 generations (p.26) | NR |
| Krishna 2026 | T0779.3 | NR | 20 Hz, MPPI re-plan period 1-20 steps (pp.27-28); up to 20 generations (p.29) | NR |
| Arif 2025 | T1042.1 | NR | PID 500 Hz, logging 50 Hz; metrics updated after each positive step of a 12 s square wave  | real time (hardware) |
| Arif 2025 | T1042.2 | NR | PID 500 Hz, logging 50 Hz; metrics updated after each positive square-wave step (pp.5,7,9) | real time (hardware) |
| Caccia 2026 | T1044.1 | t_gen 5.72 s (7B), 4.57 s (3B) mean (p.10) | LLM called once per user goal; MPC horizon N=3, T=20 stages (pp.6,10) | NR |
| Caccia 2026 | T1044.2 | t_full 6.17 s (7B), 4.89 s (3B) per step (p.10) | LLM called once per user goal, up to 20 retries; MPC N=3 (pp.5-6) | NR |
| Caccia 2026 | T1044.3 | t_gen 4.94 s (7B), 3.38 s (3B) mean (p.10) | LLM once per goal; MPC N=3, T=50 stages (pp.6,11) | NR |
| Caccia 2026 | T1044.4 | t_full 9.89 s (7B), 6.63 s (3B) (p.10) | LLM once per goal, up to 20 retries; MPC N=3 (pp.5-6) | NR |
| Caccia 2026 | T1044.5 | t_gen 4.26 s (7B), 3.55 s (3B) mean (p.10) | LLM once per goal; MPC N=3, T=50-100 stages (pp.6,11) | NR |
| Caccia 2026 | T1044.6 | t_full 9.70 s (7B), 7.51 s (3B) (p.10) | LLM once per goal, up to 20 retries; MPC N=3 (pp.5-6) | NR |
| Caccia 2026 | T1044.7 | t_gen 4.52 s (7B), 3.85 s (3B) mean (p.10) | LLM once per goal; MPC N=3, T=500-1000 stages (pp.6,12) | NR |
| Caccia 2026 | T1044.8 | t_full 9.71 s (7B), 7.80 s (3B) (p.10) | LLM once per goal, up to 20 retries; MPC N=3 (pp.5-6) | NR |
| Khan 2026 | T1046.1 | NR per call; episode wall 1835 s Gemini (p.9) | 10 s step, 5-step (50 s) shadow horizon; 15/10/50-step episodes (pp.3,6) | NR |
| Khan 2026 | T1046.2 | NR per call; episode wall 60 s Gemini (p.10) | 10 s step, 5-step shadow horizon; 15/10/50-step episodes (pp.3,6) | NR |
| Khan 2026 | T1046.3 | NR per call; episode wall 885 s Gemini (p.9) | 10 s step; 15/10/50-step episodes (pp.3,6) | NR |
| Khan 2026 | T1046.4 | NR per call; episode wall 23 s Gemini (p.9) | 10 s step; 15/10/50-step episodes (pp.3,6) | NR |
| Šmídl 2026 | T1053.1 | NR (generic 'hundreds of ms to seconds', p.4) | episodic request-response, no streaming; controller rate NR (p.4-5) | NR |

Setups that ran in real time on hardware or in a plant: 14 (S028.1, S037.2, S038.1, S042.1, S042.2, S042.3, S156.1, S262.1, S264.1, S282.1, S282.2, T1042.1, T1042.2, T1042.3).
