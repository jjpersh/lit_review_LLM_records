# Stage B summary (2026-11-13): the 20 core papers that had no grades

Every paper was read once, in full for core papers and through the methods for papers that failed eligibility, by one Opus reader subagent following `READER_B.md` (two at a time). The lead reviewer checked each reader's grades against the rubric and the setup-splitting rule; no grade needed a page check. Result: **15 core papers (32 setups), 5 moved to context.** With Stage A: 47 graded core papers, 107 setups, 105 independent setups.

## Papers moved to context

| rec_id | Paper | Reason (logged in tier_changes.csv) |
|---|---|---|
| S161 | Daniele 2026 | Core paper moved to context at full text (2026-11-13): user study of fault diagnosis on a desktop 3D printer; no control layer or control action tested (pp.8-10) |
| S206 | Galitsky 2026 | Core paper moved to context at full text (2026-11-13): LLM writes process-fault diagnoses for operators; no control action generated or tested (pp.20-22); screening rule: diagnosis with no control action |
| S260 | Vyas 2026 | Core paper moved to context at full text (2026-11-13): tutorial with no tested setup of its own; reports no performance figures (pp.2, 5); builds on S022 |
| S296 | Ahmadi 2026 | Core paper moved to context at full text (2026-11-13): practitioner perspective with composite scenarios and no reported test; advisory monitoring briefs, no control action (pp.2-4, 6, 9) |
| T0351 | Hu 2026 | Core paper moved to context at full text (2026-11-13): MCP link from a local LLM to a SQL database; no control layer, one query demonstration, no numbers |

Each has a "background use" note in its `.md` file. They may be cited as background in the Introduction or Section 6, never as evidence, and they are in no figure, table or count.

## Core papers: setups and grades

| Setup | Plant | Evidence | Authority | Outcome | C1-C6 | Operation | Adjacent | Duplicate of |
|---|---|---|---|---|---|---|---|---|
| S019.1 Closed-loop sim: fine-tuned SLM picks heater power, rule-equality vali | single-zone thermal system (simulated) | E1 | Propose | Succeeded | Y Y Y Y Y Y | continuous | building/thermal energy |  |
| S019.2 Cross-model benchmark (1,500 samples): GPT-4o, DeepSeek-V3, SLM as Act | single-zone thermal system (simulated) | E2 | Propose | Succeeded | N N NR N Y Y | continuous | building/thermal energy |  |
| S026.1 LLM sets per-ramp hysteresis-band modes for 8 ramp-metering gates (SUM | freeway ramp metering (simulated SUMO) | E1 | Set targets | Succeeded | Y Y Y Y Y Y | continuous | traffic |  |
| S026.2 LLM sets per-resource cost-weight modes for MILP dispatch of a VPP (Op | virtual power plant on distribution feeder (s | E1 | Set targets | Succeeded | Y Y Y Y Y Y | continuous | grid / building energy |  |
| S031.1 LLM-configured MPC with CBF (LLM sets gamma) vs LLM-configured MPC wit | robot gripper, Safe Panda Gym (simulated) | E1 | Set targets | Succeeded | N Y Y N N N | not applicable | robotics |  |
| S031.2 Alignment of LLM-chosen CBF safety parameter with human-rated safety i | robot gripper, Safe Panda Gym (simulated) | E2 | Set targets | Succeeded | N N N N Y N | not applicable | robotics |  |
| S031.3 Interactive LaMPC-CBF: LLM re-tunes CBF gamma online from user feedbac | robot gripper, Safe Panda Gym (simulated) | E1 | Set targets | Conditional | N Y Y Y N N | not applicable | robotics |  |
| S033.1 Direct LLM actuation: LLM writes pump valve opening each step (clamped | Nonlinear water tank (simulated) | E1 | Act | Failed | Y Y N Y N N | continuous | no | S203 |
| S033.2 Hybrid LLM-PID: LLM retunes PID gains (Kp Ki Kd N) every 0.5 s with fo | Nonlinear water tank (simulated) | E1 | Set targets | Conditional | Y Y Y Y N N | continuous | no | S203 |
| S036.1 LLM agents select/tune PID-MPC-LQR, then propose LQR gain updates gate | roll-to-roll web tension (simulated) | E1 | Propose | Succeeded | Y Y Y N N N | continuous | no |  |
| S039.1 Manager/operator LLM agents issue module function calls from twin even | modular production system (physical rig, offl | E2 | Act | Conditional | N N Y N Y N | not applicable | discrete manufacturing automation |  |
| S043.1 CrewAI agent writes valve/pump commands for clog fault; digital-twin s | four-tank mixing module (simulated, OpenModel | E1 | Act | Conditional | N N Y N Y Y | batch | no |  |
| S205.1 MCP-DT: LLM iteratively writes charging-controller code with constrain | Li-ion fast charging (PyBaMM DFN, simulated) | E1 | Propose | Conditional | Y Y N Y Y Y | batch | battery charging |  |
| S205.2 Zero-shot: LLM writes one charging algorithm without simulation feedba | Li-ion fast charging (PyBaMM DFN, simulated) | E1 | Propose | Failed | Y Y N Y Y NR | batch | battery charging |  |
| S239.1 LLM as step-level safety gate on proposed PLC/SCADA tool calls (offlin | abstract PLC/SCADA tool-call environments, si | E2 | Propose | Conditional | N N Y N Y Y | not applicable | no |  |
| S264.1 Claude Sonnet 4 orchestrates MCP tools (RPM lookup, OPC UA drilling, R | lab manufacturing cell: drilling station + mo | E3 | Set targets | Succeeded | N N Y N N Y | not applicable | discrete manufacturing |  |
| S269.1 Methanol recycle plant: LLM via MCP reconfigures loops, valves, setpoi | Methanol synthesis with recycle (Aspen Dynami | E1 | Propose | Succeeded | N Y Y N N N | continuous | no |  |
| S269.2 Flash drum with PSV: LLM via MCP corrects pressure network, valve size | Flash drum with relief valve (Aspen Dynamics, | E1 | Propose | Succeeded | N Y Y N N N | continuous | no |  |
| S269.3 Flash drum TD3 RL control: LLM helps build direct COM interface; no pe | Flash drum, TD3 heater-duty control (Aspen Dy | E1 | Propose | Succeeded | N Y N N N N | continuous | no |  |
| S302.1 STAMP/CAST agent: KG-grounded LLM derives safety constraints, writes t | filter-circulation piping (text scenario on P | E1 | Propose | Succeeded | N N Y Y Y Y | not applicable | no |  |
| S302.2 Direct-generation baseline: same LLM and KG context, no safety analysi | filter-circulation piping (text scenario on P | E1 | Propose | Failed | N N Y Y Y N | not applicable | no |  |
| T0608.1 GPT-4 summarises template NLG reports of simulated MPC greenhouse refe | Venlo tomato greenhouse climate MPC (simulate | E1 | Advise | Conditional | N N N N N N | continuous | greenhouse |  |
| T0615.1 LLM tool-calling benchmark: 30 curated HEMS prompts mapped to JSON too | home energy management PV-battery (simulated) | E2 | Set targets | Conditional | Y N N N Y N | not applicable | home energy |  |
| T0615.2 Integrated LLM-MPC HEMS: LLM invokes economic MPC/appliance tool on si | home energy management PV-battery (simulated) | E1 | Set targets | Conditional | Y Y N Y N N | continuous | home energy |  |
| T1044.1 Inventory (3 items): SLM writes MPC cost, used one-shot (vanilla) | inventory model (simulated) | E1 | Set targets | Conditional | N Y N Y Y N | not applicable | inventory management |  |
| T1044.2 Inventory (3 items): SLM writes MPC cost, accepted only after nominal- | inventory model (simulated) | E1 | Propose | Conditional | N Y N Y Y Y | not applicable | inventory management |  |
| T1044.3 Water network (5 reservoirs): SLM writes MPC cost, used one-shot (vani | 5-reservoir water network (simulated) | E1 | Set targets | Conditional | N Y N Y Y N | continuous | water reservoir network |  |
| T1044.4 Water network (5 reservoirs): SLM writes MPC cost, accepted only after | 5-reservoir water network (simulated) | E1 | Propose | Conditional | N Y N Y Y Y | continuous | water reservoir network |  |
| T1044.5 Surface vessel (SWAMP USV): SLM writes MPC cost, used one-shot (vanill | marine USV SWAMP (simulated) | E1 | Set targets | Conditional | N Y N Y Y N | not applicable | marine vehicle |  |
| T1044.6 Surface vessel (SWAMP USV): SLM writes MPC cost, accepted only after s | marine USV SWAMP (simulated) | E1 | Propose | Conditional | N Y N Y Y Y | not applicable | marine vehicle |  |
| T1044.7 Crane trolley with payload: SLM writes MPC cost, used one-shot (vanill | crane trolley with payload (simulated) | E1 | Set targets | Conditional | N Y N Y Y N | not applicable | mechanical (crane) |  |
| T1044.8 Crane trolley with payload: SLM writes MPC cost, accepted only after s | crane trolley with payload (simulated) | E1 | Propose | Conditional | N Y N Y Y Y | not applicable | mechanical (crane) |  |

## Decisions the author should check

- **S206 (Galitsky and Rybalov) moved to context.** The reader called it borderline core: an LLM writes process-fault diagnoses for operators, screened by a symbolic checker, and no control action is generated or tested. The lead reviewer applied the screening rule used for all records ("monitoring or diagnosis with no control action" is not core). [CHECK]
- **Kept core although borderline:** S239 (an LLM guardrail classifies proposed PLC/SCADA tool calls offline; no plant dynamics, but the safeguard is challenged with 424 unsafe proposals); S269 (an LLM agent edits controllers and valves in Aspen Plus Dynamics models during model preparation, not in the loop); S302 (an LLM writes an emergency operating procedure, checked against safety constraints derived from a P&ID model; text scenario, no simulation); T0608 (GPT-4 summarises greenhouse MPC plans for growers; kept for consistency with T0665, same first author, a different experiment). [CHECK]
- **Duplicate experiment:** S033 and S203 (Wen et al.) report the same water-tank experiment. S033 is the fuller report (three runs, an autotuned PID baseline). The synthesis counts S033.1 and S033.2 and drops S203.2 and S203.3 from every count; S203.1 (free-text output) and S203.4 (CSTR) stay. S037 and S038 remain counted separately (different experiments, Stage A decision).
- **Setup splitting:** T1044 gives 8 setups (four plants, each one-shot and gated), following the rule that plants and gated or ungated arms are separate setups. This adds weight to adjacent, simulated, language-to-MPC work in setup counts; paper counts are unaffected.
- **Reader cautions to carry into the text:** S036's abstract claims lab-scale validation but every test is simulated; S026's prompted frontier LLMs did not beat the conventional controllers, only the fine-tuned model did; T0615's headline saving comes from the MPC, and a rule-based controller earned the most; S205's "12.9x fewer evaluations" compares unlike stopping points; S019 has three different latency figures (3.84, 4.84, 5.28 s) and results that imply non-rule actions reached the plant despite its validator.

## What the 15 new core papers change

- **Head-to-head (F3).** 8 new direct comparisons. Process systems: non-LLM better 13, LLM better 4 of 28 (was 13 vs 3 of 27); the finding holds. All graded setups: 17 vs 14 of 49 (was 15 vs 10 of 41); the balance is closer because most new LLM wins are adjacent (traffic, VPP, home-energy tool parsing). The manuscript should give both.
- **Marginal value of the LLM (F4)** is strengthened (S033.2, T0615.2).
- **Safeguards (F6, F7).** Challenged safeguards rise from 16 to 29 setups (28%), mostly from T1044's gated arms and S019, S026, S043, S205, S239, S264, S302. New evidence that gates make errors both ways (T1044) and that an LLM guardrail misses a third of unsafe calls (S239).
- **Small and local models (F10)** are strengthened (S019, S026, T0615, T1044, S033, S205).
- **LLM-facilitated hybrid control (F13)** is weakened: S036 is a process study (simulated web line) in which LLM agents choose among PID, MPC and LQR.
- **Hardware (F1).** One new hardware setup (S264, adjacent manufacturing cell, 4 scenarios). No new plant study.
- **Unchanged:** F2, F5, F8, F9, F11, F12, F14 (numbers updated), G1-G5.

