#!/usr/bin/env python3
"""Export the pre-revision grades (extraction/extraction_v1.csv) to <out>/grades/<rec_id>.csv,
in the reader-file format, so scripts/42_compare_readers.py can compare them with the full reads.
Usage: .venv/bin/python -I scripts/43_export_old_grades.py <out_dir>"""
import csv
import os
import sys

HEADER = ("rec_id,setup,evidence,authority,outcome,C1,C2,C3,C4,C5,C6,C1_note,C2_note,C3_note,C4_note,"
          "C5_note,C6_note,llm_latency,loop_timing,plant_timing,llm_model,key_result,limitation,operation,"
          "domain,adjacent,duplicate_of,recommend_tier").split(",")


def main():
    out = sys.argv[1]
    os.makedirs(os.path.join(out, "grades"), exist_ok=True)
    rows = list(csv.DictReader(open("extraction/extraction_v1.csv", encoding="utf-8")))
    by = {}
    for r in rows:
        by.setdefault(r["rec_id"], []).append(r)
    for rid, rs in by.items():
        with open(os.path.join(out, "grades", f"{rid}.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=HEADER, extrasaction="ignore")
            w.writeheader()
            for r in rs:
                r = dict(r)
                r.setdefault("recommend_tier", "core")
                w.writerow(r)
    print(f"exported {len(by)} papers, {len(rows)} setups to {out}/grades")


if __name__ == "__main__":
    main()
