#!/usr/bin/env python3
"""Compact list of scored-field differences between old grades and full-read grades (revision run 2026-11-12).
Usage: .venv/bin/python -I scripts/44_diff_scored.py <old_dir> <new_dir> [pairs.csv] REC_ID ...
pairs.csv (optional, rec_id,old_setup_no,new_setup_no) overrides in-order pairing where the setup split differs.
Prints setup lists per paper, then each differing scored field with both notes."""
import csv
import os
import sys

SCORED = ["evidence", "authority", "outcome", "C1", "C2", "C3", "C4", "C5", "C6"]


def load(d, rid):
    p = os.path.join(d, "grades", f"{rid}.csv")
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def main():
    old, new = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    pairs = {}
    if args and args[0].endswith(".csv"):
        for r in csv.DictReader(open(args[0], encoding="utf-8")):
            pairs.setdefault(r["rec_id"], []).append((int(r["old_setup_no"]), int(r["new_setup_no"])))
        args = args[1:]
    tot = agree = 0
    per_field = {f: [0, 0] for f in SCORED}
    for rid in args:
        a, b = load(old, rid), load(new, rid)
        print(f"\n=== {rid}: old {len(a)} / new {len(b)} setups")
        for i, r in enumerate(a, 1):
            print(f"  old{i}: {r['setup'][:110]}")
        for i, r in enumerate(b, 1):
            print(f"  new{i}: {r['setup'][:110]}  [{r.get('evidence')}/{r.get('authority')}/{r.get('outcome')}]")
        pr = pairs.get(rid) or [(k, k) for k in range(1, min(len(a), len(b)) + 1)]
        for i, j in pr:
            x, y = a[i - 1], b[j - 1]
            for f in SCORED:
                va, vb = (x.get(f) or "").strip(), (y.get(f) or "").strip()
                tot += 1
                agree += va.lower() == vb.lower()
                per_field[f][0] += 1
                per_field[f][1] += va.lower() == vb.lower()
                if va.lower() != vb.lower():
                    n = f + "_note"
                    extra = f"\n      old: {x.get(n, '')[:160]}\n      new: {y.get(n, '')[:160]}" if f.startswith("C") else ""
                    print(f"  [{i}->{j}] {f}: {va} -> {vb}{extra}")
    if tot:
        print(f"\nTOTAL paired scored fields: {tot}; agreed {agree} ({100 * agree / tot:.1f}%)")
        for f, (n, k) in per_field.items():
            print(f"  {f}: {k}/{n} ({100 * k / n:.0f}%)")


if __name__ == "__main__":
    main()
