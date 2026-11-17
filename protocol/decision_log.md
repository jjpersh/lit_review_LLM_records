# Decisions log (audit trail)

Every inclusion/exclusion decision, coding judgment and change of plan, with a date.

## 2026-10-27
- Seed set loaded from `example_reviews/LLM_process_control_systematic_search.xlsx` (14 Oct 2026 screen):
  212 included primary studies + 22 reviews = 234 records -> `corpus/seed_records.csv`.
- Spreadsheet categories C1–C8 mapped to *provisional* roles (C1->R4, C2->R1/R2, C3->R5, C4/C5->R6, C6->M,
  C7->BENCH, C8->R7; C2/C4/C5 titles mentioning recovery/fault-tolerance -> "R3?"). Final roles are coded from
  full text in Stage B.

## 2026-10-28
- Session of 2026-10-27 ended mid-enrichment with no status record. Added `STATUS.md` as the resume point for
  any future session or agent.
- Search update date set to 2026-10-28 (the day the searches are actually run), replacing 2026-10-27 in `scripts/common.py`.
- **Search update design (A.3).** Window 2022-11-01 to 2026-10-28 (full window, not just since 14 Oct), so that the
  new sources also catch records the 14 Oct scite search missed. Hits are de-duplicated against *every* record in the
  14 Oct screening record (included, reviews, adjacent, excluded at T/A, excluded by keyword) by DOI and fuzzy title
  (ratio >= 93); only records not screened before are screened now. "New since 14 Oct" = publication date > 2026-10-14.
- Queries: the 25 distinct Boolean strings from the 14 Oct Search log (rows 1–32, duplicates removed). Rows 33–51
  (title-anchored queries) did not record their title term, so they cannot be re-run exactly; omitted.
- Per-source handling: OpenAlex `search` (Boolean, title+abstract+fulltext), top 200 by relevance; IFAC-PapersOnLine
  via OpenAlex ISSN filter 2405-8963 (ScienceDirect returns 403 to scripts); arXiv API (all: fields), top 200 by
  relevance; Semantic Scholar bulk Boolean search, first 1000; PSE Press via Crossref DOI prefix 10.69997 with the
  query reduced to keywords (Crossref has no Boolean), top 100.
- LAPSE (psecommunity.org) has no searchable API; the site search covers web pages, not the archive. Not searched
  directly; PSE Press proceedings (the main LAPSE-linked venue) are covered via Crossref. Flag for manual check.
- Semantic Scholar answered 429 to the first unauthenticated test call; the script retries with backoff. Any query that
  still fails is logged as ERROR in `logs/search_queries.csv`.
- Unpaywall not used (needs a contact email in each request); OpenAlex carries the same OA-location data.
- Seed set preprint->published merges (4, OpenAlex title match >= 92): arXiv 2512.07261 -> 10.2197/ipsjjip.34.569;
  arXiv 2512.23292 -> 10.1038/s44387-026-00142-x; arXiv 2511.22975 -> 10.1016/j.jmsy.2026.04.005;
  arXiv 2605.10480 -> 10.1109/lcsys.2026.3717047. Published version kept as primary; preprint in other_version_dois.
- **OpenAlex quota.** OpenAlex returned 429 with `Retry-After: 7346` s (free daily credit limit, list/search calls
  cost 10 credits) at about 15:53 MDT. `common.get` now gives up when Retry-After > 120 s instead of sleeping, so the
  run finishes and the failed calls are logged as ERROR (not cached). Affected: OpenAlex IFAC search for query 25, and
  all 11 OpenAlex forward-citation chases. Forward citations were instead chased in **Semantic Scholar** (citations
  endpoint, added to script 03): 10/11 seed records resolved; Vyas et al. 2026 JPC DOI failed (its arXiv version
  resolved, 2 citing papers). TODO: re-run script 03 after the OpenAlex quota resets to fill the OpenAlex citation
  chase; cached calls are not repeated.
- **Search update result.** 11,316 hits -> 6,336 unique -> 1,918 pass the keyword pre-filter -> 371 already in the
  14 Oct record -> **1,547 new candidates** (`corpus/new_candidates.csv`, ordered by number of queries that hit them).
- **Screening of the 1,547 (single AI screener, title then abstract).** Title pass (`logs/screening/title_pass_*.txt`):
  1,287 excluded, 58 adjacent, 202 to abstract. Abstract decisions (`logs/screening/abstract_decisions_20261028.txt`):
  101 include, 9 reviews, 33 adjacent, 58 exclude, 1 new published version of a seed record. Table:
  `corpus/new_screening.csv` (script 03b). Many includes carry a "scope check" note and a role with "?"; those are
  borderline on domain or on whether the task is control-layer, and are decided at full text in Stage B.
- Screening rules made explicit (consistent with how the 14 Oct record treated the same topics): HAZOP / process
  safety documentation, P&ID digitization or generation, and process design = exclude; ICS cybersecurity (intrusion
  detection, honeypots), machinery PHM/predictive maintenance, discrete-manufacturing machines and robots, buildings,
  grid, vehicles, medical = adjacent; PLC / IEC 61131-3 / IEC 61499 code generation included whatever the plant type
  (as the 14 Oct C3 category did). Nuclear plant operation / control rooms included as thermal-power process
  (one nuclear reactor control study was already in the seed set).
- Notable exclusion: N0280 "Multidimensional Evaluation of LLM-Generated MPC Programs" — MPC here is secure
  multi-party computation, not model predictive control.
- Version merge from screening: IEEE TASE 10.1109/tase.2026.3700674 is the published version of seed S046
  (arXiv 2507.20509); published version now primary.
- Du & Chan 2026 survey (arXiv 2609.16599, named in brief §2) was not in the 14 Oct reviews tab; added as a review (N0015).
- **Known items (brief §2) not returned by any search** added from `corpus/known_items.csv`: Zhou et al. 2026 FCSE
  (DOI not yet in Crossref), Clean Energy zkag033, Baldea et al. 2026 IECR. Woo et al. 2025 KJChE was already in the
  seed set (S230). Brief §2 reviews are now all in the corpus.
- **Full-text download (A.5).** 129 of 347 records have a verified PDF (title words checked on page 1–2): 91 via arXiv
  (including arXiv author copies found by exact-title search), the rest via OpenAlex OA locations. MDPI, ScienceDirect
  (incl. open-access IFAC-PapersOnLine) and some IEEE OA PDFs return HTTP 403 to scripts; these are listed as
  "open access but blocked to scripts" in `corpus/missing_fulltext.csv` (free to download in a browser). No paywall
  was worked around. Zenodo records found are code/data packages, not papers.
- Fixed in script 04: carrying full-text status over by DOI duplicated rows for records without a DOI; now keyed on
  DOI, or title when there is no DOI.

## 2026-11-06 — Change of plan: focused critical review
- User dropped PRISMA. Protocol: `focused_review/protocol.md`. Rubric: 7 criteria (C1-C7) plus evidence level, authority, outcome and who issued commands.
- Prefilter: R5, R6 and M records with no control-related keyword in title or abstract set to out (125 records). The other 222 were judged by title and abstract, single AI screener.
- Decisions live in `scripts/10_focus_filter.py`. `corpus/metadata.csv` was not edited; S262 and S180 author fixes are applied in the script output.
- 2026-11-06: Dropped the commands-issued-by field. User testing with operators is out of scope for this phase. Precedent exists in human factors and nuclear control rooms, but none was found in LLM control work. Rubric is C1-C7 plus evidence level, authority and outcome.
- 2026-11-06: Targeted searches run (`scripts/12` to `15`, log in `focused_review/search_log.csv`). Sources: OpenAlex, arXiv, Semantic Scholar, plus forward citations from priority-1 core papers. Failed: Semantic Scholar SW1, OP3, CR3 (rate limit); no OpenAlex record for S262. OpenAlex CR1 failed in the main run and was rerun in full by script 14. S033, S161, S239 and S026 moved to priority 2 to keep the scored set focused. Noise-filter rule is in `scripts/13_targeted_prefilter.py`; shortlist chosen from titles, then abstracts.
- 2026-11-09: Scopus searches run in the user's Chrome through BYU access (4 strings; MCP string narrowed from 603 to 46 hits). Results read from the results pages, no exports. Added core SC01 (Miyaoka 2026 TCST, ChatMPC) and SC02 (Arjunan 2026, closed-loop agentic refiner control, three-month mill study; LLM role to verify at full text); SC03 to context. All other Scopus hits were already in the corpus, already screened in the targeted search, or off-topic (wind turbines, power grid, robotics, energetic material LLM-105, MOF synthesis, network management).
- 2026-11-09: User downloaded 17 core PDFs (S013, S178, S193, SC01, T0665, T1042, S016, S048, T0302, S020, S041, S028, S030, S315, T1053, S156, T1046); titles checked against page 1-3 text. S294 and T0373 moved to context because full text was not obtained.
- 2026-11-09: User downloaded 8 core PDFs (S034, S031, T0608, T1044, S269, T0351, S206, S296); titles checked against page 1-3 text. S294 and T0373 moved to context because full text was not obtained.
- 2026-11-09: User downloaded 6 core PDFs (T0615, S033, S205, S239, S161, S302); titles checked against page 1-3 text. S294 and T0373 moved to context because full text was not obtained.
- 2026-11-09: SC02 (Arjunan 2026) requested through BYU interlibrary loan, ILLiad request 2807237. Kept as priority-1 core pending full text; score with a vendor-authored flag, or drop if no LLM is in the loop.
- 2026-11-09: Calibration complete on S262, S203, S032, SC01, S020 with the user. C6 tightened to "LLM decision quality measured" (old wording was Y for all 9 setups). Eligibility now requires a generative LLM. SC01 (ChatMPC, Sentence-BERT + k-NN) moved to context and flagged key_reference. Scores saved to extraction/extraction.csv (calibration=yes).
- 2026-11-09: Priority-1 scoring complete from page-tagged digests (scripts/19_digests.py). S034 and T0302 moved to context (RL, no LLM). S037/S038 flagged as overlapping. SC02 (Arjunan) awaits ILL.
- 2026-11-10: Spot check of 4 digest-scored papers against full text (S195, S048, S041, T1046): 35/40 fields agreed (87.5%). Errors: S195 outcome (one row split into 3 setups); S041 C4 (N, not Y) and C5 (Y, not N); T1046 outcome (Succeeded, not Conditional) and C4 (Y, not N). Pattern: digests miss latency comparisons and repeated-run designs stated in results/discussion text, and flatten mixed outcomes. Corrections applied (calibration=spotcheck).
- 2026-11-10: User dropped the latency criterion (old C4): working architectures already absorb their latency, and simulations usually pause for the LLM. Latency kept as descriptive fields (llm_latency, loop_timing, plant_timing) for the timescale discussion. Criteria renumbered: old C5-C7 are now C4-C6.
- 2026-11-10: Targeted recheck of C4 (repeatable) and outcome for 24 digest-scored papers against full text. Changes: C4 1 (T0532 N to Y); outcome 0; evidence 2 (T0665 NR to E1, S156 NR to E4); C5 1 (S156 N to Y); models and timing fields filled for T1042, S022, S017, S037.
- 2026-11-10: Synthesis started: scripts/30_synthesis.py writes synthesis/tables.md (7 tables), fig1_timescale, fig2_authority_evidence; findings.md (F1-F14, gap check G1-G5) and outline.md written. STOP for user review of the outline.
- 2026-11-10: Added figures (scripts/31_figures.py): control hierarchy, head-to-head, gap map, papers per year (full corpus), appraisal profile. Outline revised: forward-looking thesis (LLM as interface/orchestration layer coupled to optimization and control tools, bounded by evidence); agenda cut to open problems + evaluation protocol with one crystallization paragraph.
- 2026-11-10: Drafting handed off to an unattended remote run (DRAFTING_BRIEF.md, run_drafting.sh).
- 2026-11-11: Built a journal-style PDF of the draft (draft/_latex/build_pdf.py, pandoc + pdflatex, article class with Times; elsarticle not installed). Output draft/_latex/manuscript.pdf, 18 pages. Rebuild after any edit to manuscript.md.
- 2026-11-12: Reader model test. Sonnet 5.5 read S038, S041, S315 and T1046 blind with the lean setup (scripts/41_prep_text.py clean text, focused_review/fullread/READER_LEAN.md); compared with the Opus full reads by scripts/42_compare_readers.py: 40 of 45 scored fields agreed on paired setups (89%); differences were outcome Succeeded vs Conditional (S041 x3, S315) and C4 (S041). One Opus lean read of T1046 for cost. Outputs in focused_review/fullread_sonnet_test/ and fullread_opuslean_test/. Added a setup-splitting rule (split by architecture, not by model) after both lean reads split T1046 by model. Found that the author correction on [11] (continuous heater power) matches S037, not S038 (on/off); noted in REVISION_BRIEF.md.

## 2026-11-12 — Revision run, Stage A1: full reads, adjudication, merge
- Tier changes (scripts/40_fullread_merge.py from focused_review/fullread2/tier_changes.csv): SC02 Arjunan to context (full text not obtainable, interlibrary loan failed); S040, T0380, T0392 to context (full text not obtainable, Zenodo deposit only). Core now 52.
- All 32 scored papers read in full by blind Opus readers (focused_review/fullread2/). Setups 39 to 75 (21 papers split by plant, architecture or gate). Agreement with the first-pass grades on 39 paired setups: 294/351 fields (83.8%) (agreement.md).
- S037/S038: full texts show no shared experiment (S038 on/off thermostat on one TCLab; S037 FSM planning plus continuous heater power on dual TCLab and twin). Both counted; duplicate flag dropped.
- Grade changes (old to final; page and basis in focused_review/fullread2/adjudication.md):
  - S004 setup 1→1: authority Propose -> Set targets (p.6)
  - S004 setup 1→1: outcome Not shown -> Succeeded (pp.6, 8)
  - S007 setup 1→3: authority Propose -> Set targets (pp.4-5)
  - S007 setup 1→3: outcome Succeeded -> Conditional (p.8)
  - S007 setup 1→3: C4 Y -> N (pp.7-9)
  - S013 setup 1→1: outcome Not shown -> Conditional (p.5)
  - S013 setup 1→1: C2 N -> Y (p.5)
  - S016 setup 1→1: outcome Conditional -> Succeeded (p.39)
  - S016 setup 1→1: C6 N -> Y (p.37)
  - S020 setup 1→1: outcome Not shown -> Conditional (pp.16, 19)
  - S022 setup 1→1: authority Set targets -> Propose (pp.5-7)
  - S028 setup 1→1: evidence E4 -> E5 (pp.1, 8)
  - S028 setup 1→1: C1 Y -> N (p.11)
  - S028 setup 1→1: C5 Y -> N (pp.7, 10)
  - S030 setup 1→1: evidence E1 -> E2 (pp.3, 9)
  - S030 setup 1→1: C1 Y -> N (pp.9, 12)
  - S032 setup 2→2: authority Set targets -> Propose (pp.1-2)
  - S032 setup 3→3: C5 Y -> N (p.23)
  - S037 setup 1→2: C1 N -> Y (p.15)
  - S037 setup 1→2: C2 N -> Y (p.15)
  - S037 setup 1→2: C4 Y -> N (pp.15, 22)
  - S042 setup 1→1: outcome Conditional -> Succeeded (p.5)
  - S048 setup 1→1: outcome Succeeded -> Conditional (pp.12-15)
  - S156 setup 1→1: evidence E4 -> E5 (pp.1, 37)
  - S156 setup 1→1: outcome Conditional -> Succeeded (pp.40-41)
  - S156 setup 1→1: C2 N -> Y (pp.37-39)
  - S178 setup 1→1: outcome Conditional -> Succeeded (pp.12, 16)
  - S193 setup 1→1: evidence E1 -> E2 (p.11)
  - S193 setup 1→1: C2 Y -> N (p.11)
  - S195 setup 1→1: authority Propose -> Set targets (p.12)
  - S195 setup 1→1: outcome Failed -> Conditional (p.12)
  - S195 setup 1→1: C5 Y -> N (p.12)
  - S195 setup 2→2: authority Propose -> Set targets (pp.7-10)
  - S195 setup 3→4: authority Propose -> Set targets (p.21)
  - S195 setup 3→4: outcome Failed -> Conditional (p.21)
  - S203 setup 4→4: C1 NR -> N (pp.4-5)
  - S272 setup 1→1: outcome Conditional -> Succeeded (p.5)
  - S315 setup 1→1: authority Act -> Propose (pp.3-4)
  - S315 setup 1→1: C1 Y -> N (pp.3-4)
  - T0532 setup 1→1: outcome Conditional -> Succeeded (pp.5-6)
  - T0532 setup 1→1: C2 Y -> N (pp.5-6)
  - T0665 setup 1→1: outcome Succeeded -> Not shown (p.9)
  - T0665 setup 1→1: C5 Y -> N (p.9)
  - T0779 setup 1→1: authority Propose -> Set targets (pp.2-6)
  - T0779 setup 1→1: C3 Y -> N (p.22)
  - T1042 setup 1→1: C5 N -> Y (p.15)
  - T1046 setup 1→1: authority Set targets -> Propose (pp.4-5)
  - T1046 setup 1→1: outcome Succeeded -> Conditional (pp.7-8, 15)
  - T1046 setup 1→1: C1 Y -> N (p.5)
  - T1053 setup 1→1: authority Set targets -> Propose (pp.2-3)
  - T1053 setup 1→1: outcome Conditional -> Succeeded (p.6)
  - T1053 setup 1→1: C1 N -> Y (p.6)
  - T1053 setup 1→1: C2 N -> Y (pp.5-6)
  - T1053 setup 1→1: C3 N -> Y (p.5)
- Old value kept after adjudication: S002 C4 (Y), S020 C4 (N), S262 outcome (Conditional).

## 2026-11-13 — Stage B (20 ungraded core papers, full reads)
- Tier changes (core to context, set by scripts/40_fullread_merge.py from focused_review/fullread2/tier_changes.csv): S161 (3D-printer fault-diagnosis user study, no control action); S206 (process-fault diagnosis for operators, no control action; reader said borderline core, lead reviewer applied the screening rule; author to confirm); S260 (tutorial, no test of its own); S296 (practitioner perspective, composite scenarios, no test); T0351 (MCP-to-SQL infrastructure, no control layer).
- New grades: 32 setups from 15 papers (S019, S026, S031, S033, S036, S039, S043, S205, S239, S264, S269, S302, T0608, T0615, T1044), blind full reads, calibration = fullread, date 2026-11-13. No overrides.
- Duplicate experiment: S033 = S203 water tank; S203.2 and S203.3 are not counted (scripts/synth_maps.py DUP).
- New domain class for figures and tables: "Energy, traffic and logistics (adjacent)".

- 2026-11-17 (Stage C): S002 (Shou et al.) grade-file note says "IMC lowest IAE in 3 of 4 (Table S2)"; the paper Table S2 (pp.54-55) shows IMC lowest in all 4 cases for SFT/GRPO-0.6B (C1 214.58 vs 217.27/236.33; C2 92.65 vs 111.63/106.03; C3 176.05 vs 185.05/196.11; C4 16.20 vs 17.95/18.27). Note only, no scored field changes; manuscript text ("all four") is correct. Fig. E note in scripts/synth_maps.py no longer cites the paper-internal table.
