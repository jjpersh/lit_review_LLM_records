# Adjudication of grade differences, Stage A (2026-11-12)

Old = first-draft grades (`extraction_v1.csv`, exported to `focused_review/fullread2_old/grades/`).
New = blind full-read grades (`focused_review/fullread2/grades/`). Differences listed by `scripts/44_diff_scored.py` (output: `diff_stageA.txt`).
Pairing: in order, except S007 old 1 → new 3 (the old notes describe the inverted-pendulum case), S037 old 1 → new 2 (physical TCLab), S195 old 3 → new 4 (VRFT). Pairing file: `pairs.csv`.

Each decision was made by opening the clean text (or the PDF page where a table decided it). Rubric: `focused_review/fullread/READER_LEAN.md` §2. Final value is applied by `scripts/40_fullread_merge.py` (new value by default; old value or corrections through `overrides.csv`).

## Rubric points that decide many rows
- **Authority with a gate.** READER_LEAN defines Propose as "proposes actions or parameters that a human or gate must accept". Setups whose every LLM output passes a gate (simulation gate, validator, trust gate, engineer approval) are Propose. This decides S022, S032 setup 2, S315, T1046 (gated arms), T1053.
- **Authority with no human approval in offline design.** Where the LLM's gains, structure or model choice go into a conventional controller without approval, Set targets. This decides S004, S007, S195, T0779.
- **C1, LLM-versus-LLM.** "LLM-versus-LLM only is N." A comparison with and without a gate, or against an earlier LLM architecture, is not a non-LLM comparator. This decides S028, S030, S315, T1046.
- **Evidence E5.** The protocol defines E5 as "operating plant"; READER_LEAN adds "(live closed loop or live use)". Two advisory systems ran live in operating plants (S028, S156): E5. The first draft glossed E5 as "closed loop in an operating plant"; that gloss was not in the protocol. Consequence for the manuscript: two setups reach E5, both advisory; none closes the loop.

## Decisions (57 differences in 351 paired fields)

| rec_id | pair | field | old | new | final | page | basis |
|---|---|---|---|---|---|---|---|
| S002 | 1→1 | C4 | Y | N | **Y** (old) | p.50 | "100 FOPDT and 100 SOPDT cases generated with independent seeds 61001 and 62001 ... temperature of 0.1, top-p of 0.1 ... inference seed of 42". Rates over 200 seeded cases with full settings; no per-case repeats. Partial evidence counts as Y. Setup 2 set to Y for consistency. |
| S004 | 1→1 | authority | Propose | Set targets | Set targets | p.6 | "executed in sequence without manual modification"; LLM-generated pairing and gains go to BO and the controller without approval. |
| S004 | 1→1 | outcome | Not shown | Succeeded | Succeeded | pp.6, 8 | Stated goal (feasibility of an end-to-end generated workflow) met in its one run: "should be interpreted as a feasibility demonstration". A control result exists (BO-tuned controller, Table I p.7), so not "Not shown". |
| S007 | 1→3 | authority | Propose | Set targets | Set targets | pp.4-5 | Agents' gains are scored in simulation and adopted with no human step. |
| S007 | 1→3 | outcome | Succeeded | Conditional | Conditional | p.8 | PID "reducing PID's MSE ... from 0.4817 to 0.2694 over 44 iterations" without meeting targets; framework switched to FSF, which roughly matched LQR. Mixed. |
| S007 | 1→3 | C4 | Y | N | N | pp.7-9 | Monte Carlo (100 runs) is on the final gains, not repeated LLM design runs; one design run per scenario. Note corrected: model is named (GPT-4o mini, "selected for its lower cost", p.9). |
| S013 | 1→1 | outcome | Not shown | Conditional | Conditional | p.5 | Fig. 3: "Settling Time: 2.200 s, Rise Time: 0.800 s, Max Overshoot: 4.92%" against a rise-time target < 0.5 s: one target missed. |
| S013 | 1→1 | C2 | N | Y | Y | p.5 | Settling, rise, overshoot, PM, GM reported for the example (single run; partial). |
| S016 | 1→1 | outcome | Conditional | Succeeded | Succeeded | p.39 | Full framework 0.347 g/L·h, robustness 0.893 vs 0.858 No-LLM and 0.812 deterministic MPC; "no residual hard-constraint violations" (p.37). |
| S016 | 1→1 | C6 | N | Y | Y | p.37 | "the share of direct acceptance decreases from 96.0% in S1 to 78.4% in S6 ... The fallback rate is only 1.8%"; the governor was exercised by real out-of-bounds proposals, and the No-Safety arm (p.39) shows the excursions it prevents. |
| S020 | 1→1 | outcome | Not shown | Conditional | Conditional | pp.16, 19 | Control result exists: framework IAE 2.313 vs LQI 2.366; better than LQI in 7 of 10 fault timings (p.19). LLM override changed IAE only 2.313 → 2.312. |
| S020 | 1→1 | C4 | N | Y | **N** (old) | pp.19, 24 | Monte Carlo "N = 50 independent noise realizations per level" tests the residual-switching framework; the text does not show the LLM was called in those runs. The LLM path is one run with three calls. Never infer. |
| S022 | 1→1 | authority | Set targets | Propose | Propose | pp.5-7 | Every LLM action passes simulation and deterministic validation before it is applied; fallback otherwise. |
| S028 | 1→1 | evidence | E4 | E5 | E5 | pp.1, 8 | Live operation in an operating precast concrete plant (advisory). E5 = operating plant (protocol). |
| S028 | 1→1 | C1 | Y | N | N | p.11 | Comparison is with the authors' earlier reactive LLM architecture [10]: LLM-versus-LLM. |
| S028 | 1→1 | C5 | Y | N | N | pp.7, 10 | "success" counts non-timeout responses over 41 queries; answer correctness is not measured. |
| S030 | 1→1 | evidence | E1 | E2 | E2 | pp.3, 9 | Tests run offline on author-made JSON "SCADA snapshot" files; no simulation is run and the system "has no write access to SCADA". |
| S030 | 1→1 | C1 | Y | N | N | pp.9, 12 | Only LLM prompt levels (baseline, B0-B3) are compared; no non-LLM method. |
| S032 | 2→2 | authority | Set targets | Propose | Propose | pp.1-2 | Forked-twin gate admits or replaces every proposal. |
| S032 | 3→3 | C5 | Y | N | N | p.23 | "operable in 50/50 cells" is a cell-level operability count, not a rate of LLM decision quality. |
| S037 | 1→2 | C1 | N | Y | Y | p.15 | Table 5: PID on hardware TW-MAE 0.7605 vs GPT-3.5 1.0277. |
| S037 | 1→2 | C2 | N | Y | Y | p.15 | TW-MAE, RMSE reported. |
| S037 | 1→2 | C4 | Y | N | N | pp.15, 22 | One hardware run; repeated runs are not reported for the hardware case. |
| S042 | 1→1 | outcome | Conditional | Succeeded | Succeeded | p.5 | Prompt-only agent tracked the reference (MAE 0.321 °C; 0.285 °C with penalty prompt, Fig. 6a). The prediction-assisted arm (new setup 3) is the Conditional one. |
| S048 | 1→1 | outcome | Succeeded | Conditional | Conditional | pp.12-15 | 100% agreement with the relay in the clean run, 73.13% under measurement noise: worked under some conditions. |
| S156 | 1→1 | evidence | E4 | E5 | E5 | pp.1, 37 | Six-month live use on an operating plant's CIP system (advisory). |
| S156 | 1→1 | outcome | Conditional | Succeeded | Succeeded | pp.40-41 | Stated LLM goal (accurate read-only diagnostics) met: median numerical error < 3% in audited spot checks. Caveat recorded in limitation: 3 runs reported, sample count not given. |
| S156 | 1→1 | C2 | N | Y | Y | pp.37-39 | Stage-specification compliance and reaction time reported; they describe the deterministic layer, not an LLM effect (noted). |
| S178 | 1→1 | outcome | Conditional | Succeeded | Succeeded | pp.12, 16 | CSTR: estimates gave tracking within 5% of IPOPT; the WWTP case (new setup 2) is Conditional. |
| S193 | 1→1 | evidence | E1 | E2 | E2 | p.11 | Ranking task on a fixed dataset of simulator-labelled gain pairs: benchmark dataset. |
| S193 | 1→1 | C2 | Y | N | N | p.11 | Ranking accuracy against simulator IAE labels; no closed-loop metric of an LLM-chosen controller. |
| S195 | 1→1 | authority | Propose | Set targets | Set targets | p.12 | LLM gains go into the simulated loop without approval. |
| S195 | 1→1 | outcome | Failed | Conditional | Conditional | p.12 | Usable controller (IAE 0.162) but ~50% worse than relay-ZN 0.106. Outcome is whether the stated goal was met; the comparison belongs to C1 and Table 5. |
| S195 | 1→1 | C5 | Y | N | N | p.12 | No rate of LLM decision quality on the CSTR; the old note (8/10 seeds) belongs to the VRFT setup. |
| S195 | 2→2 | authority | Propose | Set targets | Set targets | pp.7-10 | As above. |
| S195 | 3→4 | authority | Propose | Set targets | Set targets | p.21 | As above. |
| S195 | 3→4 | outcome | Failed | Conditional | Conditional | p.21 | LLM committed a usable τ in 8/10 seeds (J 11.19 ± 0.17) vs median rule 10/10 (J 11.17 ± 0.15, p = 0.69). |
| S203 | 4→4 | C1 | NR | N | N | pp.4-5 | No comparator for the CSTR trial; absence of a comparator is N, not NR. |
| S262 | 1→1 | outcome | Conditional | Succeeded | **Conditional** (old) | p.4 | "generally tracked within the desired band of 38–42 °C but briefly exceeded the upper limit, illustrating that setpoint bounds ... are treated as soft constraints"; redundant commands issued. |
| S272 | 1→1 | outcome | Conditional | Succeeded | Succeeded | p.5 | Vehicle passed on the requested side in all trials; ambulance yielding and restoration succeeded. |
| S315 | 1→1 | authority | Act | Propose | Propose | pp.3-4 | Gate allows, restricts or overrides each LLM proposal before actuation. |
| S315 | 1→1 | C1 | Y | N | N | pp.3-4 | No non-LLM controller and no ungated arm; only the gate's behaviour is reported. |
| T0532 | 1→1 | outcome | Conditional | Succeeded | Succeeded | pp.5-6 | Robot tracking: fine-tuned InstructMPC closest to target over 20 episodes. Goal met (qualitatively). |
| T0532 | 1→1 | C2 | Y | N | N | pp.5-6 | Robot case: trajectory plot only. The MPC cost figures belong to the building case (new setup 2, C2 = Y). |
| T0665 | 1→1 | outcome | Succeeded | Not shown | Not shown | p.9 | Only explanation-text metrics; no result on a control task (rubric definition of Not shown). |
| T0665 | 1→1 | C5 | Y | N | N | p.9 | Relevance is a mean similarity-type score, not a rate of correct or incorrect explanations. |
| T0779 | 1→1 | authority | Propose | Set targets | Set targets | pp.2-6 | LLM-designed architectures are trained and evaluated with no human approval. |
| T0779 | 1→1 | C3 | Y | N | N | p.22 | Only the benchmarks' built-in sensor and actuation noise; no disturbance, mismatch or fault test. |
| T1042 | 1→1 | C5 | N | Y | Y | p.15 | About 10 runs, failures reported for the unguided arm; partial evidence counts as Y. |
| T1046 | 1→1 | authority | Set targets | Propose | Propose | pp.4-5 | Shadow-plant gate admits each proposal. |
| T1046 | 1→1 | outcome | Succeeded | Conditional | Conditional | pp.7-8, 15 | Zero violations, but the equivalence test on completion was not significant (p = 0.079) and the correction loop salvaged 0% of rejected proposals in disturbance scenarios. |
| T1046 | 1→1 | C1 | Y | N | N | p.5 | Only the same agents without the gate; no PID, MPC or optimizer baseline. |
| T1053 | 1→1 | authority | Set targets | Propose | Propose | pp.2-3 | Engineer approval gate on writes. |
| T1053 | 1→1 | outcome | Conditional | Succeeded | Succeeded | p.6 | A2: switching-frequency cap met in 21/21 trials; A1: asked a clarifying question in 21/21. |
| T1053 | 1→1 | C1 | N | Y | Y | p.6 | Compared with the author's hand-tuned λsw (Table II): an engineer's tuning, the non-LLM alternative (single hand-tune; noted). |
| T1053 | 1→1 | C2 | N | Y | Y | pp.5-6 | d-axis current ripple, switching frequency, overshoot, peak current. |
| T1053 | 1→1 | C3 | N | Y | Y | p.5 | Load-ramp profile and field-weakening condition in the sweep (a disturbance; no fault test). |

**Result:** 57 differences. The full-read value stands in 54; the old value stands in 3 (S002 C4, S020 C4, S262 outcome). Note corrections without a grade change: S007 C4 notes (model named on p.9).

## Setup splits
The full reads split 21 of the 32 papers into more setups than the first draft (split by architecture, plant or gate, per READER_LEAN). Each new split was checked against the paper's section structure; all are kept. The new, unpaired setups have no old grade to compare and take the full-read grades.

## Duplicates
- **S037 and S038 do not share an experiment** (checked in both texts). S038 (arXiv 2024): single TCLab board, LLM switches the heater on/off to hold 25–27 °C (S038 pp.4-5, Fig. 4). S037 (2025): FSM recovery planning (Case Study 1) and a dual-board TCLab with a fan disturbance where the LLM sets continuous heater power q1, q2 in 0–0.3 W, on hardware and on a digital twin, compared with PID (Case Study 2, pp.11, 15, 22). S037 states "Our architecture builds directly on" S038 (p.5). Same group, framework and rig type; different experiments. Both are counted as independent setups; no duplicate flag. This reverses the first draft's "count once" treatment [author to confirm].
- S203 with S033: handled in Stage B (S033 is read there).
- S042: the reader notes a possible companion (Rasheed, Ravik & San, arXiv:2510.23882) on the same greenhouse rig; it is not in the screening record, so no corpus paper is double-counted.

## Internal inconsistencies found in the papers (for the claim audit)
- S022: text claims 100% recovery for the fouling case with GPT-4.1-mini (pp.11-12), Table 2 shows 8/10.
- S037: abstract claims a reprompting ablation not in the body; abstract says 180 FSMs, tables imply 200.
- S048: "few mismatches" next to 100% agreement; Fig. 4 caption does not match the text.
- S315: Tables 2-3 conflict with the text on scenario S8 and on the "pass rate" row.
- T1053: the current limit is placed in the MCP server (pp.2-3) and as a plant clamp (p.4).
