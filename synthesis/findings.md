# Findings (evidence-backed)

Basis (revision of 2026-11-12): 75 tested setups from 32 papers, every paper read in full and every grade checked against the text (`extraction/extraction.csv`; adjudication in `focused_review/fullread2/adjudication.md`). Process systems only (sensitivity): 49 setups from 22 papers. IDs in brackets are record IDs, with `.k` for the k-th setup of a paper. Tables: `synthesis/tables.md`.

Each finding states whether it still holds after the full reads ("Status").

## What has been shown

**F1. The evidence is almost entirely simulation, and no LLM has closed a loop in an operating plant.** Status: **holds, with one correction.** Of 75 setups, 52 are simulation (E1), 9 use benchmark datasets or offline snapshots (E2), 12 ran on laboratory hardware (E3) and 2 ran live in operating plants (E5). Process only: 35 E1, 8 E2, 4 E3, 2 E5.
- Correction: the two plant studies are E5 by the protocol's definition (operating plant), not E4. Both are advisory (a query assistant in a precast concrete plant [S028]; a read-only diagnostic assistant on a beverage plant's CIP system for six months [S156]). Neither lets the LLM act on the plant.
- E3 setups: TCLab rigs [S262 (2), S037.2, S038], a greenhouse testbed [S042 (3)], a servo motor [T1042 (3)], and a PLC demonstrator and coating cell [S282 (2)]. Only the four TCLab setups are process systems.
- 14 setups ran in real time on hardware or in a plant; 6 of them are process systems.

**F2. Outcomes are mostly conditional.** Status: **holds.** 35 of 75 setups are Conditional, 25 Succeeded, 10 Failed and 5 Not shown (process only: 26, 12, 9, 2).
- Direct actuation (Act, 13 setups): 4 succeeded, 6 conditional, 3 failed [S203.1, S203.2, S017.4].
- Successes are mostly narrow or adjacent: tool calls on a PLC [S282.1], vehicle MPC primitives [S272], robot architecture design [T0779], greenhouse prompts [S042.1-2], a gated bioreactor agent [S315], advisory plant assistants [S028, S156].

**F3. When a fair non-LLM alternative is run, it usually matches or beats the LLM.** Status: **holds, stronger in process systems.** 41 setups compare an LLM directly against a non-LLM method: non-LLM better 15, tie 5, mixed 9, LLM better 10, not quantified 2. Process only (27): non-LLM better 13, tie 4, mixed 5, LLM better 3, not quantified 2.
- Relay-ZN beats the LLM tuner on a CSTR (IAE 0.106 vs 0.162) [S195.1]; a median rule matches the LLM's VRFT choice (10/10 vs 8/10 seeds) [S195.4].
- IMC gives the lowest IAE in the worked cases against hosted and fine-tuned LLM tuners [S002].
- A numerical rule ranks PI gain sets far better than LLMs (96.7% vs 46.8% on the quadruple tank) [S193.1-3].
- PID beats every LLM on TCLab hardware and its twin (TW-MAE 0.76 vs 1.03; 0.21 vs 0.62) [S037.2-3]. (New from the full read.)
- PID alone beats the agent over PID on every disturbance [S032.3]; PI selector control beats LLM operator agents over a four-day scenario [S017.1].
- The three process-system LLM wins: regime identification (87.9% vs 61.1%) [S041.1], an LLM supervisory layer that improved robustness over MPC and over the same framework without the LLM [S016.1] (new: the full read found a No-LLM ablation), and an LLM-plus-Nelder–Mead hybrid that matched differential evolution with about 8x fewer evaluations [S195.3]. The other 7 LLM wins are adjacent (robotics, vehicles, building, greenhouse explanation, motor drive).

**F4. Where the LLM's marginal contribution is isolated, it is usually small.** Status: **holds, with one exception.** Identical IAE with and without the LLM (2.313 vs 2.312) [S020.1]; 100% agreement with the relay it imitates [S048]; an agent over PID worse than PID alone [S032.3]. Exception: removing the LLM from a fed-batch supervisory framework lowered robustness (0.893 to 0.858) and doubled recovery time (2 to 4 cycles) [S016.1].

**F5. The value that survives is structural and semantic, not numerical.** Status: **holds.** Structural prior on coupled plants refined by Nelder–Mead [S195.2-3]; choosing a stored operating regime from text descriptions of trajectories after a KNN shortlist [S041]; translating operator language into MPC settings [S262.1] or MPC primitives and forecasts [S272, T0532]; generating a control design pipeline [S004]. Nuance from the full read: in [S041] most of the gain depends on converting trajectories into text (raw numbers to the LLM: 68.5%), and KNN alone was never tested.

## Safeguards and integration

**F6. Safeguards are widely described but rarely challenged.** Status: **holds.** 35 setups describe a safeguard; 16 (21%) challenged one with bad proposals (C6; process only 15 of 49, 31%). Five papers contribute 11 of the 16 [S022 (2), S030 (3), S037 (3), S038, T1046 (2)]; the others are S002 (2), S016.1, S032.2, S315.
- Simulation gates: a shadow plant gave 0 violations against 10.4 per episode without it; completion 0.571 vs 0.584, and equivalence was not shown (p = 0.079) [T1046]. In those scenarios a simple range check on the inputs caught every violation; the five-step look-ahead added nothing (T1046 pp.12-14). (New.)
- Limits: the correction loop salvaged 40.3% of rejected proposals in setpoint-change scenarios and 0% in disturbance scenarios [T1046]; 534 of 590 gate interventions came from a specification on a safety bound [S032.2].
- Several validators are themselves LLMs, and in [S037] the best proposal is applied after the iteration cap even if rejected. (New.)

**F7. Unsafe proposals are common enough that validation is needed.** Status: **holds, numbers corrected.**
- [S030]: forbidden actions in 1 of 10 runs in each TEP scenario, 0 of 10 for the batch reactor and 7 of 10 for the dryer; the validator flagged all of them. (The first draft's "10–70% regardless of context" is the abstract's range; per scenario it is 0–70%.)
- [S022]: "52% of iterations fully correct" applies to one model in one fault (GPT-4o-mini, pump degradation), not to the study. Run-level success: 60/60 and 51/60 (mixing module), 28/30 and 23/30 (CSTR).
- [T1046]: without the gate, violations per cell ranged from 5.3 (Gemini 2.5 Flash) to 25.9 (Mistral 7B).

**F8. Integration studies agree on the architecture: the LLM sits outside the real-time loop and writes pass through a deterministic layer.** Status: **holds.** [T1053, S315, S282, S156, S028]. New detail: [T1053] places the current limit both in the MCP server and as a plant clamp (inconsistent text); the engineer approval gate's status during the 21-trial studies is not stated.

## Timing and transfer

**F9. LLM response times are seconds to minutes; only slow supervisory loops fit.** Status: **holds; Khan's loop timing corrected.** 0.13–3.0 s against a 0.5 s update [S203.3]; 1.9–3.5 s per recovery action [S022]; 2.9 s against a 5 min supervisory interval [S016]; median 15 s (max 278 s) against a 5 min cadence [S032.1]; 47 s identification [S041.1]; 10.6–72.7 s per decision on TCLab hardware against a 30 s hold, with the plant not waiting [S037.2]. [T1046] uses a 10 s step (the first draft's "1–10 s typical loops" is not the study's own timing).

**F10. Small open-weight models are viable for bounded tasks.** Status: **holds.** A fine-tuned 0.6B model reached 94% first-try PID tuning success against 56.5–71% for hosted models [S002.2]; local 7–14B models ran operator agents, tuners and advisers [S017, S195, S262, S028, S156]; open-weight models reached 90% on PLC commands vs 96–98% for GPT-5-family [S282.1]; small models were the most violation-prone without a gate [T1046].

## Gaps

**F11. Operator language to MPC has no process validation beyond TCLab** [S262.1]. Status: **holds.** Related work is vehicles, robots and buildings [S272, T0532] or explanation [T0665]. No study compares an LLM against an engineer or a fixed intent-to-parameter rule. ChatMPC [SC01, context] shows a classifier can do this mapping with guarantees.

**F12. No study puts an LLM in the loop for crystallization control.** Status: **holds.** [S180] has LLMs design NMPCs offline (compared only LLM against LLM), build population balance models and soft sensors.

**F13. LLM-facilitated hybrid control (an LLM choosing among controllers, modes or models) is essentially open in process control.** Status: **holds.** [S041] selects a stored model for MPC; [S020] selects pre-verified modes with no control benefit from the LLM; [T0779] designs mode-switching architectures for robots.

**F14. Reporting quality is uneven.** Status: **holds, numbers changed.** C1 56%, C2 67%, C3 53%, C4 51%, C5 49%, C6 21% of 75 setups (process only: 57%, 63%, 65%, 57%, 61%, 31%). Pre-registration once [S032].

## Gap check (G1–G5)
- G1 scope, G2 control-specific appraisal, G3 head-to-head (now 41 direct comparisons), G4 hardware and timescale (no LLM closed loop in a plant; two advisory plant deployments), G5 batch and crystallization: all hold.

## Stage B update (2026-11-13): all 47 graded core papers

Basis: 107 graded setups from 47 papers (15 papers added in Stage B), 105 independent setups after counting the shared water-tank experiment of S033 and S203 once (S203.2 = S033.1, S203.3 = S033.2). Process systems only: 57 setups from 28 papers. Five Stage B papers moved to context at full text (S161, S206, S260, S296, T0351; reasons in `focused_review/fullread2/stage_b_summary.md`). Counts below supersede the counts in F1–F14 above.

- **F1 holds.** 76 of 105 setups are simulation (E1), 14 benchmark data (E2), 13 laboratory hardware (E3), 2 operating plant (E5). Process only: 42, 9, 4, 2. The one new hardware setup is a manufacturing cell (S264, adjacent; 4 scenarios, no comparator).
- **F2 holds.** Conditional 51, Succeeded 37, Failed 12, Not shown 5 (process only 28, 17, 10, 2).
- **F3 holds for process systems, weaker across all graded setups.** 49 direct comparisons: non-LLM better 17, tie 5, mixed 11, LLM better 14, not quantified 2. Process only (28): 13, 4, 6, 4, 1. Three of the four new LLM wins are adjacent (S026 ramp metering and VPP, T0615.1 tool parsing); the process one is S036 (web line), whose MPC baseline has unreported tuning. New non-LLM wins: S033.1 (direct pump command, IAE 510.7 vs 60.3), S205.2 (zero-shot charging code, 0/10 feasible), T0615.2 (a rule-based controller earned more than the LLM-called MPC). The head-to-head balance across all graded setups is now 17 non-LLM vs 14 LLM wins; the manuscript must report this and not only the process-only figure.
- **F4 holds and is strengthened.** In S033.2 the authors attribute the nominal gain to higher gains, not to LLM reasoning, and the hybrid was worst under sensor drift. In T0615 the bill saving comes from the MPC's own slot search, and no arm isolates the LLM.
- **F5 holds.** New semantic roles: an LLM sets mode choices for conventional gates and an MILP (S026), writes MPC cost functions from plain-language goals (T1044, local 3B-7B models), sets a CBF safety parameter from text (S031), and writes operating procedures checked against safety constraints (S302).
- **F6 changes in size, not in direction.** 54 setups describe a safeguard and 29 of 105 (28%) challenged one with bad proposals (process only 18 of 57, 32%). Stage B adds challenged safeguards in S019, S026, S043, S205, S239, S264, S302 and T1044 (4 gated setups). Several challenges are weak (format checks, user-input errors rather than LLM errors in S264).
- **F7 holds, with new evidence that gates can fail both ways.** S205's constraint layer rejected 125 unsafe LLM candidates; S302's direct-generation baseline copied an unsafe manual step in 10 of 10 runs; S239's best LLM guardrail caught 64% of unsafe tool calls; T1044's simulation gate passed cost functions that missed the goal and, on one 3B task, rejected every usable one (success 26% to 0%).
- **F8 holds.** MCP and OPC UA integration with deterministic checks below the LLM recurs in S264, S269 and S205.
- **F9 holds.** New latencies: 0.3 s per query (S033, local 3B), 0.4-1.6 s per decision against 3-30 min decision periods (S026), 2.4 s (S031), 3.8-5.3 s per step (S019), 3.4-9.9 s per goal (T1044), about 4.6 min per procedure (S302). None closes a fast loop.
- **F10 is strengthened.** Fine-tuned small models matched or beat hosted ones on bounded tasks: a 1.5B model 96.67% vs GPT-4o 93.07% (S019.2), a fine-tuned Qwen3-8B beat prompted frontier models that did not beat conventional control (S026), Phi-3 Mini 96.67% tool accuracy (T0615.1), local Qwen 7B 96% with a gate vs 3B 57% (T1044).
- **F11 holds for process systems.** New language-to-MPC work is adjacent: robotics (S031), home energy (T0615), inventory, water network, vessel and crane (T1044). None compares against an engineer or a fixed rule.
- **F12 holds.** No new crystallization study.
- **F13 is weakened.** S036 has LLM agents choose among PID, MPC and LQR for a simulated roll-to-roll web line and then adapt LQR gains through a simulation filter (process; MPC baseline tuning not reported). S026 has an LLM choose operating modes of conventional controllers (adjacent). LLM-facilitated hybrid control is no longer "essentially open" in process control; it is thinly tested (one process study, simulation only).
- **F14 holds.** C1 48%, C2 69%, C3 52%, C4 54%, C5 55%, C6 28% of 105 setups (process only 51%, 65%, 70%, 56%, 60%, 32%).
- **Batch versus continuous:** 56 continuous, 13 batch, 36 not applicable or not reported.
- **Gap check:** G1-G5 hold; G3 now has 49 direct comparisons.
