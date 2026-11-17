#!/usr/bin/env python3
"""Build extraction/extraction.csv from the full-read grades (revision run, 2026-11-12).

Inputs
  focused_review/fullread2/grades/<rec_id>.csv     one row per tested setup (blind full read)
  focused_review/fullread2/overrides.csv           adjudicated corrections: rec_id,setup_no,field,value,page,reason
                                                   (setup_no is 1-based within the paper's grades file)
  focused_review/fullread2/tier_changes.csv        rec_id,tier,reason   (screening.csv tier changes)
Outputs
  extraction/extraction.csv   (only papers whose grades say recommend_tier = core)
  focused_review/screening.csv (tier and reason updated for the rec_ids in tier_changes.csv)
No hand edits to either CSV: rerun this script after changing the inputs.
Usage: .venv/bin/python -I scripts/40_fullread_merge.py
"""
import csv
import glob
import os
import sys

DATE = "2026-11-12"
# Stage B papers (graded 2026-11-13) get their own date
STAGE_B = {"S019", "S026", "S031", "S033", "S036", "S039", "S043", "S161", "S205", "S206", "S239",
           "S260", "S264", "S269", "S296", "S302", "T0351", "T0608", "T0615", "T1044"}
DATE_B = "2026-11-13"
G = "focused_review/fullread2"
COLS = ["rec_id", "setup", "evidence", "authority", "outcome", "C1", "C2", "C3", "C4", "C5", "C6",
        "C1_note", "C2_note", "C3_note", "C4_note", "C5_note", "C6_note", "llm_latency", "loop_timing",
        "plant_timing", "llm_model", "key_result", "limitation", "operation", "domain", "adjacent",
        "duplicate_of", "calibration", "date"]
VALID = {
    "evidence": {"E0", "E1", "E2", "E3", "E4", "E5"},
    "authority": {"Advise", "Propose", "Set targets", "Act"},
    "outcome": {"Succeeded", "Conditional", "Failed", "Not shown"},
    **{f"C{i}": {"Y", "N", "NR"} for i in range(1, 7)},
}


def read(p):
    return list(csv.DictReader(open(p, encoding="utf-8", newline=""))) if os.path.exists(p) else []


def main():
    overrides = read(f"{G}/overrides.csv")
    tiers = {r["rec_id"]: r for r in read(f"{G}/tier_changes.csv")}
    out, errors = [], []
    for p in sorted(glob.glob(f"{G}/grades/*.csv")):
        rid = os.path.basename(p)[:-4]
        if rid in tiers and tiers[rid]["tier"] != "core":
            continue
        rows = read(p)
        if not rows or rows[0].get("recommend_tier", "core").strip() == "context":
            if rid not in tiers:
                errors.append(f"{rid}: reader recommends context but no tier_changes entry")
            continue
        for k, r in enumerate(rows, 1):
            if None in r:  # unquoted comma in a reader's CSV shifts columns
                errors.append(f"{rid} setup {k}: extra columns {r[None]!r}")
            r = {c: (r.get(c) or "").strip() for c in COLS}
            drop = False
            for o in overrides:
                if o["rec_id"] == rid and int(o["setup_no"]) == k:
                    if o["field"] == "drop":  # setup described but not tested: not a graded setup
                        drop = o["value"].strip().lower() == "yes"
                    else:
                        r[o["field"]] = o["value"]
            if drop:
                continue
            r["calibration"], r["date"] = "fullread", (DATE_B if rid in STAGE_B else DATE)
            for f, ok in VALID.items():
                if r[f] not in ok:
                    errors.append(f"{rid} setup {k}: {f}={r[f]!r}")
            out.append(r)
    for o in overrides:  # every override must hit a row
        if not any(r["rec_id"] == o["rec_id"] for r in out) and o["rec_id"] not in tiers:
            errors.append(f"override for {o['rec_id']} matched no paper")
    if errors:
        print("ERRORS:\n  " + "\n  ".join(errors))
        sys.exit(1)
    with open("extraction/extraction.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)
    scr = read("focused_review/screening.csv")
    for r in scr:
        if r["rec_id"] in tiers:
            r["tier"], r["reason"] = tiers[r["rec_id"]]["tier"], tiers[r["rec_id"]]["reason"]
    with open("focused_review/screening.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(scr[0].keys()))
        w.writeheader()
        w.writerows(scr)
    print(f"extraction.csv: {len(out)} setups from {len({r['rec_id'] for r in out})} papers; "
          f"{len(overrides)} overrides; {len(tiers)} tier changes")


if __name__ == "__main__":
    main()
