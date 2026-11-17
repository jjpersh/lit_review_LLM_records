"""Stage A.3 — turn the screening decision files into corpus/new_screening.csv (one row per new candidate).

Inputs:
  corpus/new_candidates.csv                         candidates from script 03 (cid N0001…)
  logs/screening/title_pass_*.txt                   title pass: I / ? / R / A / V codes; unlisted cid = exclude
  logs/screening/abstract_decisions_20261028.txt    abstract-level decision for every I / ? / R / V from the title pass
Output: corpus/new_screening.csv with stage (title / abstract), decision, role_provisional, reason, note.
"""
import re

import pandas as pd

from common import CORPUS, LOGS

SCR = LOGS / "screening"
EXCL = ("Not an LLM process-control-layer task (e.g., LLM internals, chemistry/materials, process design/simulation, "
        "education, non-process domain)")
ADJ = "Outside process industries (robotics, vehicles, grid, buildings/HVAC, machinery, ICS security, etc.)"


def main():
    cand = pd.read_csv(CORPUS / "new_candidates.csv", keep_default_na=False)
    title = {}
    for f in sorted(SCR.glob("title_pass_*.txt")):
        for line in f.read_text().splitlines():
            m = re.match(r"^(N\d{4}) (\S+)\s*(.*)$", line)
            if m:
                title[m.group(1)] = (m.group(2), m.group(3))
    abstract = {}
    for line in (SCR / "abstract_decisions_20261028.txt").read_text().splitlines():
        m = re.match(r"^(N\d{4}) (\S+) (\S+) \|\s*(.*)$", line)
        if m:
            abstract[m.group(1)] = m.groups()[1:]

    out = []
    for _, r in cand.iterrows():
        c = r["cid"]
        code, tnote = title.get(c, ("X", ""))
        if code in ("I", "?", "R", "V"):
            if c not in abstract:
                raise SystemExit(f"{c} passed the title stage but has no abstract decision")
            dec, role, note = abstract[c]
            stage = "abstract"
        elif code == "A":
            dec, role, note, stage = "adjacent", "-", tnote, "title"
        else:
            dec, role, note, stage = "exclude", "-", "", "title"
        reason = {"exclude": EXCL, "adjacent": ADJ}.get(dec, "")
        out.append({**r.to_dict(), "stage": stage, "decision": dec,
                    "role_provisional": "" if role == "-" else role, "reason": reason, "note": note})
    df = pd.DataFrame(out)
    df.to_csv(CORPUS / "new_screening.csv", index=False)
    print(df.groupby(["stage", "decision"]).size().to_string())


if __name__ == "__main__":
    main()
