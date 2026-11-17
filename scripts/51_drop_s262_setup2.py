"""2026-11-17 author decision: S262 setup 2 (automated text analysis) is described but untested; drop it.
Adds a 'drop' override type to scripts/40_fullread_merge.py and the override row. Run from the project root."""
import pathlib

m = pathlib.Path('scripts/40_fullread_merge.py')
s = m.read_text(encoding='utf-8')
old = """            for o in overrides:
                if o["rec_id"] == rid and int(o["setup_no"]) == k:
                    r[o["field"]] = o["value"]
"""
new = """            drop = False
            for o in overrides:
                if o["rec_id"] == rid and int(o["setup_no"]) == k:
                    if o["field"] == "drop":  # setup described but not tested: not a graded setup
                        drop = o["value"].strip().lower() == "yes"
                    else:
                        r[o["field"]] = o["value"]
            if drop:
                continue
"""
if 'o["field"] == "drop"' not in s:
    assert s.count(old) == 1
    m.write_text(s.replace(old, new), encoding='utf-8')

o = pathlib.Path('focused_review/fullread2/overrides.csv')
t = o.read_text(encoding='utf-8')
row = ('S262,2,drop,yes,p.3,"automated text analysis is described but no output, measure or count is reported; '
       'not a tested setup (author decision 2026-11-17)"\n')
if 'S262,2,drop' not in t:
    o.write_text(t if t.endswith('\n') else t + '\n', encoding='utf-8')
    with o.open('a', encoding='utf-8') as f:
        f.write(row)
print('drop override in place')
