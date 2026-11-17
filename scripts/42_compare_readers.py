#!/usr/bin/env python3
"""Compare two readers' blind grades (e.g. Opus vs Sonnet) for the same papers.
Usage: .venv/bin/python -I scripts/42_compare_readers.py <dirA> <dirB> REC_ID ...
Each dir holds grades/<rec_id>.csv. Setups are paired in order; a differing setup count is reported.
Prints per-paper field tables and an overall agreement figure on the scored fields."""
import csv
import json
import os
import sys

SCORED = ["evidence", "authority", "outcome", "C1", "C2", "C3", "C4", "C5", "C6"]
DESCR = ["llm_latency", "loop_timing", "plant_timing", "operation", "adjacent", "recommend_tier"]


def load(d, rid):
    p = os.path.join(d, "grades", f"{rid}.csv")
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else None


def main():
    a, b, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
    tot = agree = 0
    for rid in ids:
        ra, rb = load(a, rid), load(b, rid)
        print(f"\n=== {rid}: A {len(ra) if ra else 'missing'} setups, B {len(rb) if rb else 'missing'} setups")
        if not ra or not rb:
            continue
        for k in range(max(len(ra), len(rb))):
            x = ra[k] if k < len(ra) else {}
            y = rb[k] if k < len(rb) else {}
            print(f"--- setup {k + 1}\n  A: {x.get('setup', '(none)')}\n  B: {y.get('setup', '(none)')}")
            for f in SCORED + DESCR:
                va, vb = (x.get(f) or "").strip(), (y.get(f) or "").strip()
                same = va.split(" ")[0].lower() == vb.split(" ")[0].lower()
                if f in SCORED and x and y:
                    tot += 1
                    agree += same
                if not same:
                    na, nb = x.get(f + "_note", ""), y.get(f + "_note", "")
                    print(f"  DIFF {f}: A={va!r} B={vb!r}" + (f"\n     A note: {na}\n     B note: {nb}" if na or nb else ""))
    if tot:
        print(f"\nScored fields compared (paired setups only): {tot}, agreed {agree} ({100 * agree / tot:.0f}%)")
    usage_dir = os.path.join(b, "usage")
    if os.path.isdir(usage_dir):
        print("\nUsage for B:")
        for rid in ids:
            p = os.path.join(usage_dir, f"{rid}.json")
            try:
                d = json.load(open(p))
                u = d["usage"]
                print(f"  {rid}: turns {d.get('num_turns')}, cache_write {u.get('cache_creation_input_tokens')}, "
                      f"cache_read {u.get('cache_read_input_tokens')}, output {u.get('output_tokens')}, "
                      f"api-equivalent ${d.get('total_cost_usd', 0):.2f}, {d.get('duration_ms', 0) / 60000:.1f} min")
            except Exception as e:
                print(f"  {rid}: no usage ({e})")


if __name__ == "__main__":
    main()
