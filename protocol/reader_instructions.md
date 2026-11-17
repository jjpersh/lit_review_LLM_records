# Reader instructions: one core paper, read in full and graded blind

You are reading ONE paper in full for a focused critical review of large language models (LLMs) in process control. Project root: `/home/jp/projects/lit_review_LLM`. Your caller tells you the rec_id and the output folder (`<OUT>`).

## Rules
- **Blind grading.** Do not open `extraction/`, `synthesis/`, `draft/`, `draft_v1/`, `focused_review/digests/`, `focused_review/recheck/`, `focused_review/scoring_summary.md`, any reader output in `focused_review/fullread/` (its `.md` files or `grades/`), `focused_review/fullread_sonnet_test/`, `focused_review/fullread_opuslean_test/`, or other papers' files in `<OUT>`. The only files you open are this one, `focused_review/protocol.md` if needed, your paper's clean text, and your paper's PDF pages. Your grades must come only from the paper. A script compares them with earlier grades afterwards.
- Work only inside the project. Do not download, install or contact anything.
- Never infer. If the paper does not report something, write NR.

## 1. Read the paper in full
- The paper's text is prepared for you at `focused_review/fullread/clean/<rec_id>.txt`, with `[p.N]` markers at the start of each PDF page and the reference list removed. Read the WHOLE file with the Read tool, from the first line to the last, in as few calls as possible (up to 2000 lines per call). Do not skim and do not keyword-search instead of reading.
- Its header names the source PDF. Open a PDF page as an image (Read tool, `pages` parameter, one page per call) only when a table, figure or algorithm box that matters for a grade or a result is garbled or missing in the text. **At most 4 page images per paper.**
- If the text file is nearly empty or unreadable, read the PDF pages instead and say so in the output.

## 2. Rubric (one grade row per tested setup)
- **What counts as a separate setup.** Split by architecture, not by model. Arms that differ in what the LLM is allowed to do or in what checks its output (for example, the same agent with and without a safety gate, or advisory versus direct actuation) are separate setups, because they get different authority and C6 grades. Different LLMs run in the same architecture are one setup; report the per-model spread in the notes and `key_result`. Different plants or case studies (a numerical example and a CSTR) are separate setups.
- **Evidence:** E0 concept (no test), E1 simulation, E2 benchmark dataset, E3 lab hardware, E4 pilot or industrial data, E5 operating plant (live closed loop or live use).
- **Authority** (highest the LLM exercises in that setup): Advise (text or explanation to a human), Propose (proposes actions or parameters that a human or gate must accept), Set targets (sets setpoints, tuning, constraints or the model choice used by a conventional controller, without human approval), Act (writes the manipulated variable or actuator command directly).
- **Outcome:** Succeeded (met its stated goal across the tests), Conditional (worked only under some conditions, models or settings, or mixed), Failed, Not shown (no result on the control task).
- **Criteria**, each Y, N or NR with a page. Partial evidence counts as Y, with the gap in the note.
  - C1 Compared against the right non-LLM alternative (tuned PID or MPC, a rule-based baseline, an optimizer)? An untuned or default baseline is N with a note. LLM-versus-LLM only is N.
  - C2 Control metrics reported (IAE, ISE, overshoot, settling time, constraint violations, cost, batch quality)? Text-quality metrics only is N.
  - C3 Off-nominal conditions tested (disturbance, model mismatch, sensor fault, fault scenario)?
  - C4 Repeated runs (or variance across runs) reported AND enough detail to reproduce (model named plus prompts or settings)? Needs both.
  - C5 LLM decision quality measured as a rate or count across multiple decisions (correct, invalid, unsafe or off-intent outputs), not anecdotes?
  - C6 Safeguards present AND actually challenged with bad proposals, not only described?
- **Descriptive fields:** `llm_latency` (reported LLM response time, else NR), `loop_timing` (sampling or LLM update interval, else NR), `plant_timing` ("real time (hardware)", "real time (plant)", or NR when a simulation may pause for the LLM), `llm_model`, `key_result` (one sentence with the number and page), `limitation` (the authors' own stated limitation, with page), `operation` (batch, continuous, or not applicable), `domain` (short phrase, e.g. "CSTR (simulated)", "TCLab thermal rig", "servo motor (adjacent)").

## 3. Output file: `<OUT>/<rec_id>.md` (aim for 900–1,500 words)
Headings `## 1. Identity` and so on, in this order:
1. **Identity:** first author, year, title as printed, venue, peer-reviewed or preprint, page count, and "All N pages were read" (only if true).
2. **Eligibility:** does a generative LLM (or LLM agent or VLM) act on, advise, tune or connect to a control layer, in at least one tested setup or reported deployment? Process system, standard process benchmark, or adjacent domain (vehicle, robot, drive, building, grid, home energy, greenhouse)? A tutorial, perspective or position paper with no tested setup of its own is not core: say so, recommend `context`, and write "not graded" for parts 4–6.
3. **What was built, in plain words** (150–250 words): the plant, and whether it is hardware or a simulation; the controller that actually moves the actuator; exactly where the LLM sits; what the LLM receives and what it produces; what happens to that output before it reaches the plant (validator, gate, simulation check, human approval, optimizer) and how those parts work together; the model and how it is prompted, fine-tuned or given tools. Say whether actuation is continuous or on/off. Write for a process-control engineer who has not read the paper; define every system name.
4. **Each tested setup:** conditions, number of runs, the comparator and whether it is a tuned non-LLM method, the metrics, what was varied.
5. **Results:** each result a review could use, with page and a short verbatim quote (under 25 words) containing the number; what it measures and its denominator; for a paper-specific metric, what it is and whether lower or higher is better. Say explicitly whether the paper shows the LLM beating a non-LLM alternative, and on what.
6. **Duplicates:** any experiment also reported in another paper (same authors, rig or data).
7. **Terms to define** for a process-control reader (term: one line, as the paper uses it).
8. Last line, exactly: `STATUS: complete`

Do not restate the rubric. Do not write a grades table in the `.md`; the grades go in the CSV.

## 4. Grades file: `<OUT>/grades/<rec_id>.csv`
Write it with the Write tool, UTF-8, standard CSV quoting (quote any field containing a comma or quote), this exact header, one row per tested setup:

`rec_id,setup,evidence,authority,outcome,C1,C2,C3,C4,C5,C6,C1_note,C2_note,C3_note,C4_note,C5_note,C6_note,llm_latency,loop_timing,plant_timing,llm_model,key_result,limitation,operation,domain,adjacent,duplicate_of,recommend_tier`

- Each note is under about 120 characters and includes the page, e.g. "tuned PI by relay-ZN (p.6)".
- `setup`: plain description under about 90 characters.
- `adjacent`: `no` for process systems and standard process benchmarks, otherwise a short phrase ("robotics", "vehicle", "motor drive", "building energy", "greenhouse").
- `duplicate_of`: rec_id of another paper reporting the same experiment, else empty.
- `recommend_tier`: `core` or `context`. For `context`, write one row with setup "not graded", the reason in `key_result`, and grade fields empty.

## 5. Return value
Return only three lines: rec_id and core/context; setups with evidence/authority/outcome and C1–C6; anything the caller must know (unreadable pages, duplicates).
