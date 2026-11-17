#!/usr/bin/env python3
"""Merge targeted-search decisions into focused_review/. Run after 10_focus_filter.py, from lit_review_LLM/."""
import collections
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request

csv.field_size_limit(10**7)
UA = {'User-Agent': 'lit-review-script/1.0'}
T = {'T1': 'Operator language to MPC/controller tuning', 'T2': 'LLM in or above the loop',
     'T3': 'Mode or controller switching and coordination', 'T4': 'SCADA/MCP/OPC integration',
     'T5': 'Fault recovery, safeguards and operator trust'}
CORE = {  # tid: (theme, priority, adjacent domain)
    'T0532': ('T1', 1, 'general MPC, not process'), 'T0665': ('T1', 1, 'greenhouse climate'), 'T1042': ('T1', 1, 'servo motor hardware'),
    'T0302': ('T2', 1, ''), 'T0715': ('T2', 1, ''), 'T1046': ('T5', 1, ''), 'T0779': ('T3', 1, 'robotics'),
    'T0373': ('T4', 1, ''), 'T1053': ('T4', 1, 'motor drives'),
    'T0608': ('T1', 2, 'greenhouse climate'), 'T1044': ('T1', 2, 'general dynamic systems'), 'T0615': ('T1', 2, 'home energy'),
    'T0481': ('T5', 2, 'electronics manufacturing'), 'T0380': ('T4', 2, ''), 'T0392': ('T4', 2, ''), 'T0351': ('T4', 2, ''),
}
CONTEXT = {
    'crystallization or batch modeling': 'T0148 T0278 T0233',
    'adjacent control method or evidence': 'T0435 T0454 T0419 T0405 T0360 T0536 T0544 T0540 T1021 T1009 T0610 T0671 T0967 T0472',
}
ctx = {i: why for why, ids in CONTEXT.items() for i in ids.split()}
rows = list(csv.DictReader(open('focused_review/targeted_candidates.csv', encoding='utf-8', newline='')))
by_id = {r['tid']: r for r in rows}
assert (set(CORE) | set(ctx)) <= set(by_id)
norm = lambda t: re.sub(r'[^a-z0-9]', '', (t or '').lower())[:100]
arxiv_by_title = {norm(r['title']): r['arxiv_id'] or (re.search(r'arxiv\.(\d{4}\.\d{4,5})', r['doi']) or [None, ''])[1] for r in rows
                  if r['arxiv_id'] or 'arxiv' in r['doi']}


def oa_status(doi):
    if not doi:
        return 'unknown'
    try:
        url = 'https://api.openalex.org/works/doi:' + urllib.parse.quote(doi, safe='/') + '?select=open_access'
        o = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))['open_access']
        return 'open access: download in a browser (free)' if o.get('is_oa') else 'not open access: BYU library'
    except Exception:
        return 'not open access: BYU library'


def fetch_arxiv(aid, tid):
    path = f'corpus/pdfs/{tid}_arxiv_{aid}.pdf'
    if os.path.exists(path):
        return path
    try:
        body = urllib.request.urlopen(urllib.request.Request(f'https://arxiv.org/pdf/{aid}', headers=UA), timeout=60).read()
        if body[:5] == b'%PDF-':
            open(path, 'wb').write(body)
            time.sleep(3)
            return path
    except Exception as e:
        print('arXiv download failed', aid, e)
    return ''


screen = list(csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline='')))
fields = list(screen[0])
need = list(csv.DictReader(open('focused_review/pdfs_needed.csv', encoding='utf-8', newline='')))
need_fields = list(need[0])
added = []
for tid, (theme, pr, adj) in CORE.items():
    r = by_id[tid]
    aid = arxiv_by_title.get(norm(r['title']), '')
    pdf = fetch_arxiv(aid, tid) if aid else ''
    rec = {'rec_id': tid, 'tier': 'core', 'priority': pr, 'theme': theme, 'reason': T[theme],
           'screened_on': 'title and abstract' if r['abstract'] else 'title only', 'adjacent_domain': adj,
           'first_author': r['first_author'], 'year': r['year'], 'title': r['title'], 'venue': r['venue'], 'doi': r['doi'],
           'pub_status': 'preprint' if 'arxiv' in (r['venue'] + r['doi']).lower() or 'zenodo' in r['doi'] else 'unverified',
           'pdf': pdf, 'access': '' if pdf else oa_status(r['doi'])}
    added.append(rec)
    if not pdf:
        need.append({k: rec.get(k, '') for k in need_fields})
    time.sleep(0.3)
for tid, why in ctx.items():
    r = by_id[tid]
    added.append({'rec_id': tid, 'tier': 'context', 'priority': '', 'theme': '', 'reason': why, 'screened_on': 'title and abstract',
                  'adjacent_domain': '', 'first_author': r['first_author'], 'year': r['year'], 'title': r['title'], 'venue': r['venue'],
                  'doi': r['doi'], 'pub_status': '', 'pdf': '', 'access': ''})
merged = added + screen
rank = {'core': 0, 'context': 1, 'out': 2}
merged.sort(key=lambda x: (rank[x['tier']], str(x['priority']), x['theme'], x['rec_id']))
with open('focused_review/screening.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    w.writerows(merged)
with open('focused_review/pdfs_needed.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, need_fields)
    w.writeheader()
    w.writerows(need)
with open('focused_review/targeted_decisions.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, ['tid', 'decision', 'title', 'doi'])
    w.writeheader()
    for r in rows:
        d = 'core' if r['tid'] in CORE else 'context' if r['tid'] in ctx else 'out'
        w.writerow({'tid': r['tid'], 'decision': d, 'title': r['title'], 'doi': r['doi']})

core = [x for x in merged if x['tier'] == 'core']
print('tiers', collections.Counter(x['tier'] for x in merged))
print('core priority', collections.Counter(str(x['priority']) for x in core))
print('core theme', sorted(collections.Counter(x['theme'] for x in core).items()))
print('P1 theme', sorted(collections.Counter(x['theme'] for x in core if str(x['priority']) == '1').items()))
print('have PDF', sum(bool(x['pdf']) for x in core), 'P1 have', sum(bool(x['pdf']) for x in core if str(x['priority']) == '1'))
print('need', collections.Counter((str(x['priority']), x['access'][:18]) for x in need))
for x in added:
    if x['tier'] == 'core':
        print(x['rec_id'], 'P%s' % x['priority'], x['theme'], 'PDF' if x['pdf'] else '---', x['access'][:22], x['title'][:70])

with open('logs/decisions.md', encoding='utf-8') as f:
    has = 'Targeted searches run' in f.read()
if not has:
    with open('logs/decisions.md', 'a', encoding='utf-8') as f:
        f.write('- 2026-11-06: Targeted searches run (`scripts/12` to `15`, log in `focused_review/search_log.csv`). Sources: OpenAlex, arXiv, Semantic Scholar, plus forward citations from priority-1 core papers. '
                'Failed: Semantic Scholar SW1, OP3, CR3 (rate limit); no OpenAlex record for S262. OpenAlex CR1 failed in the main run and was rerun in full by script 14. '
                'S033, S161, S239 and S026 moved to priority 2 to keep the scored set focused. Noise-filter rule is in `scripts/13_targeted_prefilter.py`; shortlist chosen from titles, then abstracts.\n')
s = open('STATUS.md', encoding='utf-8').read()
if 'Targeted searches done' not in s:
    s = s.replace('## Current stage\n', 'Targeted searches done 2026-11-06. Next: user pulls PDFs, then calibrate scoring on about 5 papers.\n\n## Current stage\n', 1)
    open('STATUS.md', 'w', encoding='utf-8').write(s)
