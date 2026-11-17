# Claim-audit instructions (revision run 2026-11-12, step A3)

You check what the first draft of a review manuscript says about specific studies against those studies' full texts. Project root: `/home/jp/projects/lit_review_LLM`. Work only inside it; do not download or contact anything. Your caller gives you a list of rec_ids.

## Inputs, per rec_id
- `draft/_work/audit_input/<rec_id>.md`: every first-draft passage that mentions the paper (paragraphs and table rows, with section names). Some passages mention the paper only by a shared surname or as one of several citations; audit only the statements about this paper.
- `focused_review/fullread2/<rec_id>.md`: a full-read summary of the paper with page-cited quotes. Use it first.
- `focused_review/fullread/clean/<rec_id>.txt`: the paper's full text with `[p.N]` page markers. **Open it (Grep for the number or phrase, then Read the surrounding lines) for every number, and whenever the summary does not settle a statement.** The full text is the reference, not the summary.
- `focused_review/fullread2/grades/<rec_id>.csv`: the graded setups (for evidence level, authority, outcome, comparator).

## What to audit
Every statement that says what a study built, tested, compared or found: setups, plants, models, actuation, comparators, numbers, denominators, attributions, and characterizations ("the success belongs to the gate", "the one clear LLM win"). Ignore statements that are only the review's own opinion and do not describe the study. Also audit table rows (Tables 5–7) that describe the paper.

Classify each statement:
- **accurate**: matches the paper.
- **inaccurate**: wrong fact, number, denominator, scope or attribution (for example a number that applies to one model or one fault presented as the study's overall result; a claim attributed to the wrong paper).
- **oversimplified**: a reader who has not read the paper could not tell what was done, or the wording implies something the paper does not show (an undefined term, an unexplained metric such as "J" or "TW-MAE", a comparison whose comparator is not named, a result whose denominator is missing).

For each statement that is not accurate, write corrected wording: plain, short sentences for a process-control engineer who has not read the paper; name the comparator; give counts with denominators; define any term at first use; keep page references as `<!-- p.N -->`. Never invent a number or quote; if the paper does not report something, say so.

## Output: `draft/_work/audit/<rec_id>.md`
```
# Claim audit: <rec_id> (<first author year>)

| # | Section | Statement (verbatim, shortened with … if long) | Page | Verdict | Corrected wording (if not accurate) |
|---|---|---|---|---|---|
```
Then a short section **"Notes for the reviser"** (at most 8 bullets) with what a reviser must know to describe this paper correctly: the setup in plain words, what the comparator is, what the key numbers mean, and any internal inconsistency in the paper.

Last line, exactly: `STATUS: complete`

## Return value
Return only one line per rec_id: `<rec_id>: <n> statements, <a> accurate, <i> inaccurate, <o> oversimplified`.
