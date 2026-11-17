#!/usr/bin/env python3
"""Focused critical review: sort corpus/metadata.csv into core / context / out.
Decisions were made by reading titles and abstracts (2026-11-06). Run from lit_review_LLM/."""
import collections
import csv
import os

csv.field_size_limit(10**7)

T = {
    'T1': 'Operator language to MPC/controller tuning',
    'T2': 'LLM in or above the loop',
    'T3': 'Mode or controller switching and coordination',
    'T4': 'SCADA/MCP/OPC integration',
    'T5': 'Fault recovery, safeguards and operator trust',
}
CORE = {  # rec_id: (theme, priority)
    'S262': ('T1', 1), 'S272': ('T1', 1), 'S178': ('T1', 1), 'S180': ('T1', 1), 'S002': ('T1', 1),
    'S004': ('T1', 1), 'S195': ('T1', 1), 'S193': ('T1', 1), 'S007': ('T1', 1), 'S013': ('T1', 1),
    'S031': ('T1', 2), 'S278': ('T1', 2),
    'S032': ('T2', 1), 'S017': ('T2', 1), 'S203': ('T2', 1), 'S033': ('T2', 2), 'S042': ('T2', 1),
    'S038': ('T2', 1), 'S037': ('T2', 1), 'S048': ('T2', 1), 'S016': ('T2', 1), 'S026': ('T2', 2),
    'S019': ('T2', 2), 'S039': ('T2', 2),
    'S041': ('T3', 1), 'S034': ('T3', 1), 'S020': ('T3', 1), 'S036': ('T3', 2), 'S040': ('T3', 2),
    'S030': ('T4', 1), 'S028': ('T4', 1), 'S282': ('T4', 1), 'S294': ('T4', 1), 'S315': ('T4', 1),
    'S239': ('T4', 2), 'S264': ('T4', 2), 'S205': ('T4', 2), 'S292': ('T4', 2), 'S269': ('T4', 2),
    'S022': ('T5', 1), 'S161': ('T5', 2), 'S156': ('T5', 1), 'S260': ('T5', 2), 'S043': ('T5', 2),
    'S302': ('T5', 2), 'S206': ('T5', 2), 'S296': ('T5', 2),
}
ADJACENT = {'S031': 'robotics, kept for the language-to-MPC method'}
CONTEXT = {
    'prior review': 'S215 S221 S227 S225 S226 S240 S217 S230 S233 S238 S345 S229 S214 S286',
    'crystallization or batch modeling': 'S270 S174 S168 S183',
    'adjacent control method or evidence': 'S211 S027 S044 S046 S304 S250 S300 S317 S146 S047 S029 S279 S202 S301 S204 S293 S159 S313',
}
OUT_REASON = {
    'R5': 'PLC or automation code generation',
    'R6': 'monitoring or diagnosis with no control action',
    'M': 'modeling not used in a controller',
    'REVIEW': 'review outside the control focus',
    'BENCH': 'general benchmark or education, no control-loop test',
    'R7': 'security or validation not specific to control authority',
    'R4': 'design method outside process control',
    'R1/R2': 'outside process control or no control-layer test',
    'R2': 'outside process control or no control-layer test',
    'R3': 'outside process control or no control-layer test',
}
FIX = {
    'S262': {'first_author': 'Jonathan Pershing', 'venue': 'American Control Conference 2026'},
    'S180': {'first_author': 'Fernando Arrais R.D. Lima'},
}

ctx = {i: why for why, ids in CONTEXT.items() for i in ids.split()}
assert not set(ctx) & set(CORE)

rows = list(csv.DictReader(open('corpus/metadata.csv', encoding='utf-8', newline='')))
ids = {r['rec_id'] for r in rows}
assert (set(CORE) | set(ctx)) <= ids, (set(CORE) | set(ctx)) - ids
consensus = {
    r['corpus_rec_id']: 'consensus_papers/' + r['file']
    for r in csv.DictReader(open('consensus_papers/index.csv', encoding='utf-8', newline=''))
    if r['corpus_rec_id']
}
missing = {r['rec_id']: r for r in csv.DictReader(open('corpus/missing_fulltext.csv', encoding='utf-8', newline=''))}


def find_pdf(r):
    if r['rec_id'] in consensus and os.path.isfile(consensus[r['rec_id']]):
        return consensus[r['rec_id']]
    name = r['fulltext_file'].strip()
    for c in (name, 'corpus/pdfs/' + os.path.basename(name)):
        if name and os.path.isfile(c):
            return c
    return ''


os.makedirs('focused_review', exist_ok=True)
out = []
for r in rows:
    r.update(FIX.get(r['rec_id'], {}))
    i = r['rec_id']
    if i in CORE:
        tier, (th, pr) = 'core', CORE[i]
        reason = T[th]
    elif i in ctx:
        tier, th, pr, reason = 'context', '', '', ctx[i]
    else:
        tier, th, pr = 'out', '', ''
        reason = OUT_REASON.get(r['role_provisional'].rstrip('?'), 'outside focus')
    p = find_pdf(r)
    out.append({
        'rec_id': i, 'tier': tier, 'priority': pr, 'theme': th, 'reason': reason,
        'screened_on': 'title and abstract' if r['abstract'].strip() else 'title only',
        'adjacent_domain': ADJACENT.get(i, ''), 'first_author': r['first_author'], 'year': r['year'],
        'title': r['title'], 'venue': r['venue'], 'doi': r['doi'], 'pub_status': r['pub_status'], 'pdf': p,
        'access': '' if p else missing.get(i, {}).get('access', 'unknown'),
    })

rank = {'core': 0, 'context': 1, 'out': 2}
out.sort(key=lambda x: (rank[x['tier']], str(x['priority']), x['theme'], x['rec_id']))
with open('focused_review/screening.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, list(out[0]))
    w.writeheader()
    w.writerows(out)

core = [x for x in out if x['tier'] == 'core']
need = [x for x in core if not x['pdf']]
fields = ['priority', 'rec_id', 'theme', 'first_author', 'year', 'title', 'doi', 'venue', 'access']
with open('focused_review/pdfs_needed.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    w.writerows({k: x[k] for k in fields} for x in need)

print('tiers', collections.Counter(x['tier'] for x in out))
print('core by priority', collections.Counter(x['priority'] for x in core))
print('core by theme', sorted(collections.Counter(x['theme'] for x in core).items()))
print('core with PDF', len(core) - len(need), '| need', len(need))
print('need by priority/access', collections.Counter((x['priority'], x['access']) for x in need))
print('title-only core', [x['rec_id'] for x in core if x['screened_on'] == 'title only'])
for x in core:
    print(f"P{x['priority']} {x['theme']} {x['rec_id']} {'PDF' if x['pdf'] else '---'} "
          f"{x['first_author'].split(' ')[-1][:16]} {x['year']} {x['title'][:72]} [{x['access'][:30]}]")
