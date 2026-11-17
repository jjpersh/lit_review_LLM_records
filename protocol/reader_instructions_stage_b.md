# Reader instructions for Stage B: screen first, read once, write the manuscript text in the same pass

Follow `focused_review/fullread/READER_LEAN.md` (rules, rubric, setup-splitting rule, output file, grades file), with the changes below. The output folder `<OUT>` is `focused_review/fullread2`. This is the only time this paper will be read, so everything the manuscript needs must come out of this pass.

## Step 1: eligibility screen
Read the clean text from the start through the end of the methods or system description (and the experiments section's opening, if needed to see whether anything was tested). Decide:

- **Core** if a generative LLM (or LLM agent or VLM) acts on, advises, tunes or connects to a control layer, and the paper reports at least one tested setup or a deployment of its own. Then continue to step 2 and read the rest of the paper.
- **Context** otherwise: a tutorial, perspective or position paper with no test of its own; no control layer (for example data management or tool-call infrastructure with no control action tested); or no generative LLM. Then stop reading and write a short `<OUT>/<rec_id>.md` with:
  1. Identity (as in READER_LEAN, plus the pages read).
  2. Why it is context, in two or three sentences, with a page.
  3. **Background use:** two or three sentences on what the paper argues or provides that a review could cite as background or context (never as evidence of effectiveness), with pages. For example: a tutorial's architecture, a practitioner's design principles, an infrastructure pattern.
  4. Duplicates (for example S260 with S022, S033 with S203).
  5. The last line `STATUS: complete`.

  Also write `<OUT>/grades/<rec_id>.csv` with the standard header and a single row: setup "not graded", the reason in `key_result`, `recommend_tier` = `context`, grade fields empty.

## Step 2 (core papers only): read the rest, grade, and write the manuscript text
Read the remaining text in full and write the `.md` file and grades CSV exactly as READER_LEAN asks. Then add these two parts to the `.md` file, before the `STATUS: complete` line:

**9. Manuscript text.** Text ready to insert into the review, written in the author's voice (plain, direct, short sentences, active voice, counts with denominators, the comparator named, every system name explained, page references as `<!-- p.N -->` comments). For each section of the review where the paper belongs (4.1 operator interface and explanation; 4.2 design and tuning; 4.3 supervisory and advanced control, including LLM-facilitated hybrid control; 4.4 direct actuation; 5.1 head-to-head evidence; 5.2 safeguards; 5.3 timing; 5.4 local and open-weight models), write:
- a **short version** of one or two sentences: the plant, what the LLM did, and the main result with its number; and
- a **long version** of at most 120 words, only if the paper carries a finding (it beats or loses to a fair non-LLM method, challenges a safeguard with bad proposals, runs on hardware or in a plant, or fills or contradicts a stated gap). Otherwise write "long version: not needed".

**10. Summary-table row.** One line for a supplementary study-summary table: `rec_id | plant (sim or hardware) | what the LLM does | comparator | main result with number | evidence level`. Each cell under about 15 words.
