# Focused critical review: protocol (2026-11-06)

This replaces the PRISMA systematic review in the handoff brief. It is not a PRISMA review and should not claim to be.

## Selection rule
- Core: an LLM acts on, advises, tunes or connects to a control layer, in process control or a standard process benchmark.
- Context: prior reviews and related methods, cited for background and never scored.
- Out: PLC code generation, monitoring or diagnosis with no control action, modeling not used in a controller.
- Eligibility requires a generative LLM (or LLM agent or VLM). Encoder-only language models with classifiers are context.
- Abstracts select papers. Only full texts are scored or used as evidence.
- A core paper whose full text cannot be obtained moves to context.

## Scoring, one row per tested setup
- Evidence level: E0 concept, E1 simulation, E2 benchmark dataset, E3 lab hardware, E4 pilot or industrial data, E5 operating plant.
- Authority: advise, propose, set targets, act.
- Outcome: Succeeded, Conditional, Failed, Not shown.

Criteria, each Y, N or NR with a page reference. Write NR when not reported; never infer.
- C1 Compared against the right non-LLM alternative?
- C2 Control metrics reported, including batch quality where relevant?
- C3 Tested off-nominal conditions (disturbance, model mismatch, sensor fault)?
- C4 Repeated runs reported, and enough detail to reproduce?
- C5 LLM decision quality measured? Y if the paper reports how often LLM outputs were correct, invalid, unsafe or off-intent across multiple decisions (a rate or count, not anecdotes). (Tightened 2026-11-09: the earlier "failures characterized" wording was Y for every calibration setup.)
- C6 Safeguards present and actually challenged?

## Next steps
1. Targeted searches: controller switching, MCP/SCADA, operator-to-MPC, crystallization. Citation chasing from core papers.
2. User pulls missing PDFs from pdfs_needed.csv.
3. Calibrate on about 5 papers with the user, then score the rest.

## Calibration notes (2026-11-09)
- Score one row per tested setup; papers reporting the same experiment (e.g. S203 and S033) are counted once in synthesis.
- Partial evidence counts as Y, with the gap written in the note.
- C4 needs repeated runs or variance as well as model details.
- C6 needs the safeguard to be tested with bad proposals, not only described.

## Descriptive timing fields (2026-11-10, replace the old latency criterion)
Latency is recorded, not scored: llm_latency (reported LLM response time), loop_timing (sampling or update interval), plant_timing (real time on hardware or plant, or NR when a simulation may pause for the LLM). Criteria renumbered C1-C6.
