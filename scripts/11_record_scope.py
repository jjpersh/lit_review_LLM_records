#!/usr/bin/env python3
"""One-time record of the 2026-11-06 change to a focused critical review. Safe to rerun."""
import csv
import os

ACC = 'LLM-Enhanced_Human-in-the-Loop_MPC_TCLab_Demonstration_for_Pharma_4.0.pdf'
index = 'consensus_papers/index.csv'
raw = open(index, 'rb').read().decode('utf-8')
if ACC not in raw:
    eol = '\r\n' if '\r\n' in raw else '\n'
    row = (f'{ACC},Jonathan Pershing,2026,"LLM-Enhanced Human-in-the-Loop MPC: TCLab Demonstration for Pharma 4.0",'
           f'American Control Conference 2026,,S262,{ACC},author is the project user; added 2026-11-06')
    open(index, 'wb').write((raw.rstrip('\r\n') + eol + row + eol).encode('utf-8'))
assert len(list(csv.DictReader(open(index, encoding='utf-8', newline='')))) == 9

os.makedirs('focused_review', exist_ok=True)
if not os.path.exists('focused_review/protocol.md'): open('focused_review/protocol.md', 'w', encoding='utf-8').write("""# Focused critical review: protocol (2026-11-06)

This replaces the PRISMA systematic review in the handoff brief. It is not a PRISMA review and should not claim to be.

## Selection rule
- Core: an LLM acts on, advises, tunes or connects to a control layer, in process control or a standard process benchmark.
- Context: prior reviews and related methods, cited for background and never scored.
- Out: PLC code generation, monitoring or diagnosis with no control action, modeling not used in a controller.
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
- C4 Latency compared with sampling time?
- C5 Repeated runs reported, and enough detail to reproduce?
- C6 Failures characterized, and did actions match the operator's intent?
- C7 Safeguards present and actually challenged?

## Next steps
1. Targeted searches: controller switching, MCP/SCADA, operator-to-MPC, crystallization. Citation chasing from core papers.
2. User pulls missing PDFs from pdfs_needed.csv.
3. Calibrate on about 5 papers with the user, then score the rest.
""")

status = open('STATUS.md', encoding='utf-8').read()
if 'CURRENT DIRECTION (2026-11-06)' not in status:
    note = """## CURRENT DIRECTION (2026-11-06): read this first
The project is now a **focused critical review, not PRISMA**. `focused_review/protocol.md` supersedes the handoff brief and
the sections below where they conflict. Selection is in `focused_review/screening.csv` (script `scripts/10_focus_filter.py`).
Missing core PDFs are in `focused_review/pdfs_needed.csv`. Next: targeted searches, then calibrate scoring on about 5 papers.

"""
    log = ("- **2026-11-06** — User chose a focused critical review. Rubric reduced to 7 criteria plus evidence, authority and "
           "outcome labels. All 347 records re-sorted into core/context/out. ACC paper (S262) added to consensus_papers.\n")
    assert '## Current stage\n' in status and '## Session log (newest first)\n' in status
    status = status.replace('## Current stage\n', note + '## Current stage\n', 1)
    status = status.replace('## Session log (newest first)\n', '## Session log (newest first)\n' + log, 1)
    open('STATUS.md', 'w', encoding='utf-8').write(status)

decisions = open('logs/decisions.md', encoding='utf-8').read()
if '2026-11-06' not in decisions:
    open('logs/decisions.md', 'a', encoding='utf-8').write("""
## 2026-11-06 — Change of plan: focused critical review
- User dropped PRISMA. Protocol: `focused_review/protocol.md`. Rubric: 7 criteria (C1-C7) plus evidence level, authority, outcome and who issued commands.
- Prefilter: R5, R6 and M records with no control-related keyword in title or abstract set to out (125 records). The other 222 were judged by title and abstract, single AI screener.
- Decisions live in `scripts/10_focus_filter.py`. `corpus/metadata.csv` was not edited; S262 and S180 author fixes are applied in the script output.
""")
print('recorded')
