#!/usr/bin/env python3
"""Register PDFs the user downloaded on 2026-11-09 (in corpus/pdfs/<rec_id>.pdf) and move unobtainable core papers to context.
Run from lit_review_LLM/."""
import collections
import csv
import os

NOT_OBTAINED = {
    'T0481': 'full text not obtained: not available through BYU (2026-11-09)',
    'S292': 'full text not obtained: publisher requires an account (2026-11-09)',
    'S278': 'full text not obtained: only copy found was on a repository the user judged unreliable (2026-11-09)',
    'S294': 'full text not obtained: publisher page had no PDF link (2026-11-09)',
    'T0373': 'full text not obtained: user judged the Zenodo record untrustworthy (2026-11-09)',
    'T0715': 'full text not obtained: not available through BYU (2026-11-09)',
}
screen = list(csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline='')))
fields = list(screen[0])
added = []
for r in screen:
    p = f"corpus/pdfs/{r['rec_id']}.pdf"
    if r['tier'] == 'core' and not r['pdf'] and os.path.isfile(p):
        r['pdf'], r['access'] = p, ''
        added.append(r['rec_id'])
    if r['rec_id'] in NOT_OBTAINED and r['tier'] == 'core':
        r['tier'], r['priority'], r['reason'] = 'context', '', NOT_OBTAINED[r['rec_id']] + f" (was core {r['theme']})"
        r['theme'] = ''
rank = {'core': 0, 'context': 1, 'out': 2}
screen.sort(key=lambda x: (rank[x['tier']], str(x['priority']), x['theme'], x['rec_id']))
with open('focused_review/screening.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    w.writerows(screen)
need_rows = list(csv.DictReader(open('focused_review/pdfs_needed.csv', encoding='utf-8', newline='')))
nf = list(need_rows[0])
core_missing = {r['rec_id'] for r in screen if r['tier'] == 'core' and not r['pdf']}
need_rows = [r for r in need_rows if r['rec_id'] in core_missing]
with open('focused_review/pdfs_needed.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, nf)
    w.writeheader()
    w.writerows(need_rows)
with open('logs/decisions.md', 'a', encoding='utf-8') as f:
    f.write(f"- 2026-11-09: User downloaded {len(added)} core PDFs ({', '.join(added)}); titles checked against page 1-3 text. "
            f"S294 and T0373 moved to context because full text was not obtained.\n")
core = [r for r in screen if r['tier'] == 'core']
p1 = [r for r in core if str(r['priority']) == '1']
print('registered', len(added), added)
print('core', len(core), '| P1', len(p1), 'with PDF', sum(bool(r['pdf']) for r in p1), '| P2', len(core) - len(p1), 'with PDF', sum(bool(r['pdf']) for r in core if str(r['priority']) == '2'))
print('still needed', collections.Counter((r['priority'], r['access'][:20]) for r in need_rows))
for r in need_rows:
    if r['priority'] == '1':
        print('  P1 missing:', r['rec_id'], r['first_author'].split(' ')[-1], r['year'], r['title'][:60], '|', r['access'][:30])
