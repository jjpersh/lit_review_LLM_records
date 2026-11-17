"""Stage A.2 — load the 14 Oct 2026 screening record (212 included + 22 reviews) into corpus/seed_records.csv.

Maps the spreadsheet's C1–C8 categories to a *provisional* R-role (final role is coded from full text in Stage B).
"""
import re

import pandas as pd
from rapidfuzz import fuzz

from common import SEED_XLSX, CORPUS, norm_doi, norm_title, is_preprint_doi

CAT_TO_ROLE = {
    "C1": "R4", "C2": "R1/R2", "C3": "R5", "C4": "R6", "C5": "R6",
    "C6": "M", "C7": "BENCH", "C8": "R7",
}
RECOVERY_RE = re.compile(r"fault[- ]tolerant|recover|mitigat|self[- ]heal|reconfigur|corrective action", re.I)


def provisional_role(cat, title):
    role = CAT_TO_ROLE.get(cat, "?")
    if cat in ("C2", "C4", "C5") and RECOVERY_RE.search(title or ""):
        role = "R3?"
    return role


def main():
    inc = pd.read_excel(SEED_XLSX, sheet_name="Included studies")
    rev = pd.read_excel(SEED_XLSX, sheet_name="Reviews & perspectives")

    rows = []
    for _, r in inc.iterrows():
        rows.append({
            "record_type": "primary",
            "title": r["Title"], "year": r["Year"], "authors": r["Authors (first 3)"], "venue": r["Venue"],
            "doi": norm_doi(r["DOI"]),
            "other_version_dois": "; ".join(norm_doi(x) for x in str(r["Duplicate versions merged"]).split(";")
                                            if pd.notna(r["Duplicate versions merged"]) and norm_doi(x)),
            "pub_status": "preprint" if r["Pub. status"] == "Preprint" else "peer-reviewed",
            "cat_20261014": r["Cat"],
            "role_provisional": provisional_role(r["Cat"], r["Title"]),
            "scope_flag_20261014": r["Scope uncertain – check full text"] if pd.notna(r["Scope uncertain – check full text"]) else "",
            "abstract": r["Abstract"] if pd.notna(r["Abstract"]) else "",
            "source": "seed_20261014",
        })
    for _, r in rev.iterrows():
        rows.append({
            "record_type": "review",
            "title": r["Title"], "year": r["Year"], "authors": r["Authors"], "venue": r["Venue"],
            "doi": norm_doi(r["DOI"]), "other_version_dois": "",
            "pub_status": "preprint" if is_preprint_doi(r["DOI"]) else "peer-reviewed",
            "cat_20261014": "R", "role_provisional": "REVIEW", "scope_flag_20261014": "",
            "abstract": r["Abstract"] if pd.notna(r["Abstract"]) else "",
            "source": "seed_20261014",
        })
    df = pd.DataFrame(rows)
    df["ntitle"] = df["title"].map(norm_title)

    # In-set duplicate check (exact DOI, then fuzzy title >= 93)
    dups = []
    seen_doi = df["doi"].duplicated(keep=False) & (df["doi"] != "")
    for d in df.loc[seen_doi, "doi"].unique():
        dups.append(("doi", d, list(df.index[df["doi"] == d])))
    t = df["ntitle"].tolist()
    for i in range(len(t)):
        for j in range(i + 1, len(t)):
            if fuzz.ratio(t[i], t[j]) >= 93:
                dups.append(("title", f"{df.at[i, 'title']} || {df.at[j, 'title']}", [i, j]))
    print(f"loaded {len(df)} records ({(df.record_type == 'primary').sum()} primary, "
          f"{(df.record_type == 'review').sum()} reviews); in-set duplicate candidates: {len(dups)}")
    for d in dups:
        print("  DUP?", d)
    df.to_csv(CORPUS / "seed_records.csv", index=False)


if __name__ == "__main__":
    main()
