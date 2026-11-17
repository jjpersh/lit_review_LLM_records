"""Stage A.1/A.2 — build corpus/metadata.csv: one row per study (published version primary, preprint recorded).

Inputs:
  corpus/seed_enriched.csv        14 Oct seed set, enriched (script 02)
  logs/version_merges.csv         preprint -> published matches (script 02)
  corpus/new_screening.csv        title/abstract decisions on the 28 Oct search-update candidates
                                  (decision in {include, review, adjacent, exclude}; see logs/decisions.md)
Output: corpus/metadata.csv (keeps fulltext_* columns from a previous run, so script 05 is not repeated needlessly).
"""
import importlib
import re

import pandas as pd

from common import CORPUS, LOGS, SEARCH_DATE, PRIOR_SEARCH_DATE, norm_doi, is_preprint_doi, arxiv_id_from_doi

enr = importlib.import_module("02_enrich_and_merge_versions")

COLS = ["rec_id", "record_type", "first_author", "authors", "year", "pub_date", "title", "venue", "publisher",
        "doi", "pub_status", "other_version_dois", "arxiv_id", "other_arxiv_ids", "role_provisional",
        "cat_20261014", "scope_flag_20261014", "source", "found_in_update_20261028", "published_after_20261014",
        "openalex_id", "is_oa", "oa_status", "best_oa_pdf", "all_pdf_urls", "abstract", "cited_by_count"]


def first_author(a):
    return re.split(r";", str(a or ""))[0].strip()


def published_fields(doi):
    """OpenAlex fields for the published version (venue, publisher, OA locations)."""
    return enr.oa_fields(enr.oa_by_doi(doi))


def main():
    seed = pd.read_csv(CORPUS / "seed_enriched.csv", keep_default_na=False)
    merges = pd.read_csv(LOGS / "version_merges.csv", keep_default_na=False)
    merge = dict(zip(merges["preprint_doi"], merges["published_doi"]))
    new_path = CORPUS / "new_screening.csv"
    if new_path.exists():  # screening found a published version of a seed record (decision "version", role column = seed rec_id)
        ver = pd.read_csv(new_path, keep_default_na=False)
        for _, v in ver[ver["decision"] == "version"].iterrows():
            target = int(re.match(r"S(\d+)", v["role_provisional"]).group(1)) - 1
            merge[seed.at[target, "doi"]] = norm_doi(v["doi"])

    rows = []
    for _, r in seed.iterrows():
        doi, others = r["doi"], [d for d in str(r["other_version_dois"]).split("; ") if d]
        f = {k: r.get(k, "") for k in ("openalex_id", "is_oa", "oa_status", "best_oa_pdf", "all_pdf_urls",
                                        "publisher", "pub_date", "cited_by_count")}
        venue, status, arx = r["venue"], r["pub_status"], r.get("arxiv_id", "") or arxiv_id_from_doi(doi)
        if doi in merge:  # promote the published version, keep the preprint as other version
            others.insert(0, doi)
            doi = merge[doi]
            p = published_fields(doi)
            f.update({k: p.get(k, "") or f.get(k, "") for k in f})
            # keep the preprint's OA PDF locations too, so the arXiv copy can still be downloaded
            f["all_pdf_urls"] = " | ".join(x for x in dict.fromkeys(
                (p.get("all_pdf_urls", "") + " | " + r.get("all_pdf_urls", "")).split(" | ")) if x)
            venue, status = p.get("venue_oa") or venue, "peer-reviewed"
        other_arx = [arxiv_id_from_doi(d) for d in others if arxiv_id_from_doi(d)]
        rows.append({
            "record_type": r["record_type"], "first_author": first_author(r["authors"] or r.get("authors_oa", "")),
            "authors": r["authors"] or r.get("authors_oa", ""), "year": r["year"], "title": r["title"],
            "venue": venue, "doi": doi, "pub_status": status, "other_version_dois": "; ".join(others),
            "arxiv_id": arx if is_preprint_doi(doi) else "", "other_arxiv_ids": "; ".join(other_arx),
            "role_provisional": r["role_provisional"], "cat_20261014": r["cat_20261014"],
            "scope_flag_20261014": r["scope_flag_20261014"], "source": "seed_20261014",
            "found_in_update_20261028": "", "published_after_20261014": False,
            "abstract": r["abstract"] or r.get("abstract_oa", ""), **f,
        })

    new_path = CORPUS / "new_screening.csv"
    if new_path.exists():
        new = pd.read_csv(new_path, keep_default_na=False)
        new = new[new["decision"].isin(["include", "review"])]
        for _, r in new.iterrows():
            doi = norm_doi(r["doi"])
            f = published_fields(doi) if doi else {}
            pre = is_preprint_doi(doi)
            rows.append({
                "record_type": "review" if r["decision"] == "review" else "primary",
                "first_author": first_author(f.get("authors_oa", "")), "authors": f.get("authors_oa", ""),
                "year": r["year"], "pub_date": r["pub_date"] or f.get("pub_date", ""), "title": r["title"],
                "venue": f.get("venue_oa") or r["venue"], "publisher": f.get("publisher", ""), "doi": doi,
                "pub_status": "preprint" if pre else "peer-reviewed", "other_version_dois": "",
                "arxiv_id": r.get("arxiv_id", "") or arxiv_id_from_doi(doi), "other_arxiv_ids": "",
                "role_provisional": r["role_provisional"] if r["decision"] == "include" else "REVIEW",
                "cat_20261014": "", "scope_flag_20261014": r.get("note", ""),
                "source": f"search_update_{SEARCH_DATE.replace('-', '')}",
                "found_in_update_20261028": r["sources"],
                "published_after_20261014": str(r["pub_date"]) > PRIOR_SEARCH_DATE,
                "abstract": r["abstract"] or f.get("abstract_oa", ""),
                **{k: f.get(k, "") for k in ("openalex_id", "is_oa", "oa_status", "best_oa_pdf", "all_pdf_urls",
                                             "cited_by_count")},
            })

    known_path = CORPUS / "known_items.csv"  # records named in the brief that no search returned
    if known_path.exists():
        for _, r in pd.read_csv(known_path, keep_default_na=False).iterrows():
            doi = norm_doi(r["doi"])
            if any(x["doi"] == doi for x in rows):
                continue
            f = published_fields(doi)
            rows.append({
                "record_type": r["record_type"], "first_author": first_author(r["authors"]), "authors": r["authors"],
                "year": r["year"], "pub_date": f.get("pub_date", ""), "title": r["title"],
                "venue": r["venue"], "publisher": f.get("publisher", ""), "doi": doi, "pub_status": r["pub_status"],
                "other_version_dois": "", "arxiv_id": "", "other_arxiv_ids": "",
                "role_provisional": r["role_provisional"], "cat_20261014": "", "scope_flag_20261014": r["note"],
                "source": "known_item_brief", "found_in_update_20261028": "", "published_after_20261014": False,
                "abstract": f.get("abstract_oa", ""),
                **{k: f.get(k, "") for k in ("openalex_id", "is_oa", "oa_status", "best_oa_pdf", "all_pdf_urls",
                                             "cited_by_count")},
            })

    md = pd.DataFrame(rows)
    md["rec_id"] = [f"S{i:03d}" for i in range(1, len(md) + 1)]
    old_path = CORPUS / "metadata.csv"
    if old_path.exists():  # carry over full-text results from a previous script-05 run
        old = pd.read_csv(old_path, keep_default_na=False)
        if "fulltext_file" in old:  # key = DOI, or title when there is no DOI (theses)
            key = lambda d: d["doi"].where(d["doi"] != "", "t:" + d["title"])
            old["key"], md["key"] = key(old), key(md)
            ft = old.drop_duplicates("key").set_index("key")[["fulltext_file", "fulltext_source", "fulltext_status"]]
            md = md.join(ft, on="key").drop(columns="key")
    md = md[COLS + [c for c in md.columns if c not in COLS]].fillna("")
    md.to_csv(old_path, index=False)
    print(f"metadata: {len(md)} records ({(md.record_type == 'primary').sum()} primary, "
          f"{(md.record_type == 'review').sum()} reviews); preprint->published promoted: "
          f"{seed['doi'].isin(merge).sum()}")


if __name__ == "__main__":
    main()
