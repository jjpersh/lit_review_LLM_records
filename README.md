# Records and data: LLMs as an interface to process control (focused critical review)

This repository holds the records behind the review *Large language models as an interface to process control: what has been shown, and what has not*: the protocol, searches, screening decisions, the per-paper full-read records, the extraction table, the grade checks and the scripts that produce every table and figure. It lets a reader trace any count in the manuscript to the setups behind it, and any grade to a page of the source paper.

It does not contain the papers themselves or their full texts (copyright), or the manuscript.

## The review in numbers

| Stage | Count |
|---|---|
| Records screened (titles and abstracts) | 383 |
| Core at title and abstract | 56 |
| Moved to context: no full text obtainable | 4 |
| Read in full | 52 |
| Moved to context at full text (no tested setup, no control action, or no control layer) | 5 |
| **Graded papers** | **47** |
| **Tested setups** (one row per setup) | **106** (104 independent; one water-tank experiment appears in two papers and is counted once) |
| Process-system setups / adjacent-domain setups | 58 / 48 |

## Layout

| Folder | What it holds |
|---|---|
| `protocol/` | `protocol.md` (scope, selection rule, appraisal instrument); `reader_instructions*.md` (the instructions every full read followed); `claim_audit_instructions.md` (how manuscript statements were checked against the papers); `decision_log.md` (dated audit trail of every inclusion, exclusion, rubric and method decision) |
| `search/` | Query strings, dates and hit counts for the initial search, the search update, the targeted searches and the database (Scopus) searches |
| `screening/` | `screening.csv`: every record with its tier (core, context, out), theme, reason, bibliographic data and DOI; `tier_changes_at_full_text.csv` |
| `extraction/extraction.csv` | The extraction table: one row per tested setup with evidence level (E0–E5), authority (advise, propose, set targets, act), outcome, criteria C1–C6 with page-referenced notes, timing fields, model, key result, stated limitation, operation (batch or continuous), domain and an adjacent-domain flag |
| `extraction/fullread/` | One record per paper read in full: identity, eligibility, a plain-language description of what was built, each tested setup, results with page numbers and short verbatim quotes, duplicates, and terms. Context papers have a short record with the reason |
| `extraction/grades/` | The grades each full read produced, before merging |
| `extraction/grade_check/` | Agreement between the first-pass grades and the blind full-read grades (294 of 351 paired fields, 83.8%), and how each of the 57 disagreements was settled against the paper's text |
| `synthesis/` | Tables, findings and the data behind each figure; `figures/` holds the figures as PNG and SVG |
| `scripts/` | The Python scripts for searching, screening, merging, synthesis and figures |

## Appraisal instrument (short form)

Each tested setup is graded for **evidence level** (E0 concept, E1 simulation, E2 benchmark or offline data, E3 laboratory hardware, E4 pilot or industrial data, E5 operating plant), the **authority** given to the LLM, the **outcome** (succeeded, conditional, failed, not shown) and six criteria, each Y, N or NR with a page reference:

- C1 compared against the right non-LLM alternative
- C2 control metrics reported
- C3 off-nominal conditions tested
- C4 repeated runs and enough detail to reproduce
- C5 LLM decision quality measured as a rate or count
- C6 safeguards present and challenged with bad proposals

The full definitions are in `protocol/protocol.md` and `protocol/reader_instructions.md`.

## Regenerating the tables and figures

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/30_synthesis.py
.venv/bin/python scripts/31_figures.py
```

The scripts were written for the project layout they ran in; paths may need adjusting. The search and download scripts (`01`–`17`) query public APIs and will return different results on a later date; their logged outputs are in `search/`.

## How the grading was done

Screening, full reads and grading were done by a single AI-assisted extractor (Claude, Anthropic) supervised by the first author. The rubric was calibrated with the first author on five papers. Every graded paper was read in full. The 32 papers graded in the first pass were graded again blind from a fresh full read, and each disagreement was settled against the cited page. No second human extractor coded the papers; this is the main limitation, and it is why the per-paper records are public.

## Acknowledgments

The authors thank management at Takeda Development Center Americas for financial and technical support.

## Citation and licence

[Add the article citation and DOI once published.]

The authors' own content (scripts, records, tables and figures) is released under the MIT License (see `LICENSE`). Short passages quoted from the reviewed papers in `extraction/fullread/` remain the property of their authors and publishers and are not covered by this licence.
