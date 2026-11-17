"""Stage A.6 — logs/prisma.json (PRISMA 2020 counts for both search rounds) and logs/stage_A_report.md.

Round 1 counts come from the 14 Oct screening record (PRISMA summary tab); round 2 (28 Oct update) counts are
recomputed from logs/search_update_hits.csv, logs/search_update_unique.csv and corpus/new_screening.csv.
Full-text availability comes from corpus/metadata.csv (script 05).
"""
import json

import pandas as pd

from common import CORPUS, LOGS, SEARCH_DATE, PRIOR_SEARCH_DATE, WINDOW_START


def main():
    q = pd.read_csv(LOGS / "search_queries.csv", keep_default_na=False)
    hits = pd.read_csv(LOGS / "search_update_hits.csv", keep_default_na=False)
    uniq = pd.read_csv(LOGS / "search_update_unique.csv", keep_default_na=False)
    scr = pd.read_csv(CORPUS / "new_screening.csv", keep_default_na=False)
    md = pd.read_csv(CORPUS / "metadata.csv", keep_default_na=False)

    in_prev = uniq["in_20261014_record"] != ""
    not_prefilter = (~in_prev) & (uniq["prefilter"].astype(str) != "True")
    by_src = hits.groupby("source").size().to_dict()
    failed = q[q["total_hits_reported"] == "ERROR"][["source", "query", "note"]].to_dict("records")
    dec = scr.groupby(["stage", "decision"]).size()
    get = lambda st, d: int(dec.get((st, d), 0))

    prisma = {
        "window": [WINDOW_START, SEARCH_DATE],
        "round_1_20261014": {
            "records_identified": 2816, "duplicates_removed": 159, "unique_screened": 2657,
            "excluded_keyword_filter": 1539, "title_abstract_screened": 1118, "excluded_title_abstract": 638,
            "adjacent": 246, "reviews": 22, "included_primary": 212,
            "source": "example_reviews/LLM_process_control_systematic_search.xlsx, PRISMA summary tab",
        },
        "round_2_20261028": {
            "queries_run": int(len(q)), "queries_failed": failed,
            "records_identified": int(len(hits)), "records_by_source": by_src,
            "unique_after_dedup": int(len(uniq)), "duplicates_removed": int(len(hits) - len(uniq)),
            "already_in_round_1_record": int(in_prev.sum()),
            "excluded_keyword_filter": int(not_prefilter.sum()),
            "title_screened": int(len(scr)),
            "excluded_title": get("title", "exclude"), "adjacent_title": get("title", "adjacent"),
            "abstract_screened": int((scr["stage"] == "abstract").sum()),
            "excluded_abstract": get("abstract", "exclude"), "adjacent_abstract": get("abstract", "adjacent"),
            "new_version_of_round_1_record": get("abstract", "version"),
            "reviews": get("abstract", "review"), "included_primary": get("abstract", "include"),
            "included_published_after_prior_search": int(
                ((scr["decision"] == "include") & (scr["pub_date"].astype(str) > PRIOR_SEARCH_DATE)).sum()),
        },
        "combined": {
            "primary_studies": int((md["record_type"] == "primary").sum()),
            "reviews": int((md["record_type"] == "review").sum()),
            "full_text_have": int((md["fulltext_status"] == "have").sum()),
            "full_text_missing": int((md["fulltext_status"] != "have").sum()),
        },
        "note": "Single AI screener (Claude) for both rounds; eligibility at full text pending (Stage B). "
                "Scopus / WoS / IEEE Xplore not yet searched (logs/manual_searches.md).",
    }
    (LOGS / "prisma.json").write_text(json.dumps(prisma, indent=2))

    prim = md[md["record_type"] == "primary"].copy()
    prim["role"] = prim["role_provisional"].str.replace("?", "", regex=False)
    prim["year4"] = prim["year"].astype(str).str[:4]
    role_year = pd.crosstab(prim["role"], prim["year4"], margins=True, margins_name="Total")
    ft = pd.crosstab(md["role_provisional"].str.replace("?", "", regex=False), md["fulltext_status"].replace("", "missing"),
                     margins=True, margins_name="Total")
    new = md[(md["source"] != "seed_20261014") & (md["record_type"] == "primary")]
    after = new[new["published_after_20261014"].astype(str) == "True"]

    lines = [f"# Stage A report ({SEARCH_DATE})", "",
             "Counts are provisional: roles come from the 14 Oct categories or from the 28 Oct title/abstract screen; "
             "final roles are coded from full text in Stage B.", "",
             "## Corpus", "",
             f"- Primary studies: **{len(prim)}** ({(prim.source == 'seed_20261014').sum()} from the 14 Oct screen + "
             f"{len(new)} new from the 28 Oct update)",
             f"- Reviews / perspectives: **{(md.record_type == 'review').sum()}**",
             f"- New primary studies published after {PRIOR_SEARCH_DATE}: **{len(after)}**; the other {len(new) - len(after)} new "
             "records were published earlier but missed by the 14 Oct search", "",
             "## Primary studies by provisional role and year", "", role_year.to_markdown(), "",
             "## Full text by provisional role (all records)", "", ft.to_markdown(), "",
             "## Search update (round 2)", "", "```", json.dumps(prisma["round_2_20261028"], indent=2), "```", ""]
    (LOGS / "stage_A_report.md").write_text("\n".join(lines))
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()
