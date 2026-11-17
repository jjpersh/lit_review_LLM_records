"""Stage C patch (2026-11-16): Tables S1-S3 give 'all (process)' counts in each cell."""
p = 'scripts/32_manuscript_tables.py'
t = open(p, encoding='utf-8').read()
a = t[t.index("for title, sub in [('S1', rows)]:"):t.index("md += ['## Table S4.")]
b = '''# Stage C (2026-11-16): each cell gives all graded setups, with process systems only in parentheses


def ap(f):
    x, y = sum(f(r) for r in rows), sum(f(r) for r in proc)
    return f'{x} ({y})' if x else '·'


NOTE_AP = 'Each cell: all graded setups, with process systems only in parentheses.'
md += [f'## Table S1. Authority by evidence level (n = {len(rows)}; process systems {len(proc)})', '']
data = [[a] + [ap(lambda r, a=a, e=e: r['authority'] == a and r['evidence'] == e) for e in EVID] +
        [ap(lambda r, a=a: r['authority'] == a)] for a in AUTH]
data.append(['**Total**'] + [ap(lambda r, e=e: r['evidence'] == e) for e in EVID] + [f'{len(rows)} ({len(proc)})'])
table(['Authority'] + EVID + ['Total'], data)
md += [NOTE_AP, '']
md += [f'## Table S2. Outcome by authority (n = {len(rows)}; process systems {len(proc)})', '']
data = [[a] + [ap(lambda r, a=a, o=o: r['authority'] == a and r['outcome'] == o) for o in OUTC] +
        [ap(lambda r, a=a: r['authority'] == a)] for a in AUTH]
data.append(['**Total**'] + [ap(lambda r, o=o: r['outcome'] == o) for o in OUTC] + [f'{len(rows)} ({len(proc)})'])
table(['Authority'] + OUTC + ['Total'], data)
md += [NOTE_AP, '']
md += [f'## Table S3. Outcome by theme (n = {len(rows)}; process systems {len(proc)})', '']
data = []
for t in THEMES.values():
    sub = [r for r in rows if r['theme'] == t]
    data.append([t] + [ap(lambda r, t=t, o=o: r['theme'] == t and r['outcome'] == o) for o in OUTC] +
                [ap(lambda r, t=t: r['theme'] == t), f"{len({r['rec_id'] for r in sub})} ({len({r['rec_id'] for r in sub if r['process']})})"])
table(['Theme'] + OUTC + ['Setups', 'Papers'], data)
md += [NOTE_AP, '']
'''
t = t.replace(a, b)
open(p, 'w', encoding='utf-8').write(t)
print('patched')
