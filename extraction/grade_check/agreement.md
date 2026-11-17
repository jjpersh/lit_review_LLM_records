# Grading agreement, Stage A (2026-11-12)

**What was compared.** The first-draft grades (made from page-tagged digests with partial full-text rechecks) against blind grades made from a full read of each paper by a separate reader that never saw the earlier grades. Both used the same rubric. Scored fields: evidence, authority, outcome and C1–C6 (9 per setup).

**Pairing.** The first draft had 39 setups; the full reads produced 75 (21 of 32 papers were split more finely, by plant, architecture or gate). Each of the 39 old setups was paired with the full-read setup describing the same configuration (`pairs.csv`); the 36 extra setups have no earlier grade and are not in the figure.

**Agreement.** 351 paired fields; 294 agreed: **83.8%**.

| Field | Agreed / compared |
|---|---|
| Evidence | 35/39 (90%) |
| Authority | 28/39 (72%) |
| Outcome | 22/39 (56%) |
| C1 comparator | 32/39 (82%) |
| C2 control metrics | 33/39 (85%) |
| C3 off-nominal | 37/39 (95%) |
| C4 repeated runs | 35/39 (90%) |
| C5 decision quality | 34/39 (87%) |
| C6 safeguard challenged | 38/39 (97%) |

**How the 57 disagreements were settled.** The first author's AI-assisted extractor opened the cited page of each paper and decided each field against the text and the rubric (`adjudication.md`). The full-read grade stood in 54 cases and the earlier grade in 3. Most disagreements came from three rubric points applied inconsistently in the first pass: authority when every LLM output passes a gate (Propose), comparisons against the same LLM system without a gate (not a non-LLM comparator, C1 = N), and outcome for setups that worked but were worse than a classical method (Conditional, not Failed).

**For Methods (plain statement).** Grades were made twice: once in a first pass and once blind from a full read. The two agreed on 294 of 351 paired fields (83.8%); each of the 57 disagreements was settled against the paper's text.

Source: `scripts/44_diff_scored.py focused_review/fullread2_old focused_review/fullread2 focused_review/fullread2/pairs.csv <32 ids>` → `diff_stageA.txt`.
