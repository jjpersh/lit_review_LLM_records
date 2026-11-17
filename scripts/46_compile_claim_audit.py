"""Compile draft/claim_audit.md from draft/_work/audit/<rec_id>.md (step A3)."""
import os
import re
import sys

root = sys.argv[1] if len(sys.argv) > 1 else '.'
d = os.path.join(root, 'draft/_work/audit')
files = sorted(f for f in os.listdir(d) if f.endswith('.md'))
KEYS = ['accurate', 'inaccurate', 'oversimplified']
tot = dict.fromkeys(KEYS, 0)
rows, bodies = [], []
for f in files:
    txt = open(os.path.join(d, f), encoding='utf-8').read()
    c = dict.fromkeys(KEYS, 0)
    for line in txt.splitlines():
        if re.match(r'^\|\s*\d+\s*\|', line):
            cells = [x.strip().lower() for x in re.split(r'(?<!\\)\|', line)]
            for k in KEYS:
                if k in cells:
                    c[k] += 1
                    tot[k] += 1
                    break
    n = sum(c.values())
    rows.append('| %s | %d | %d | %d | %d |' % (f[:-3], n, c['accurate'], c['inaccurate'], c['oversimplified']))
    body = txt.replace('STATUS: complete', '').rstrip()
    body = re.sub(r'^# ', '## ', body, flags=re.M)
    bodies.append(body)
N = sum(tot.values())
head = [
    '# Claim audit of the first draft (step A3, 2026-11-12)', '',
    'Every first-draft statement that describes what a study built, tested or found, checked against the full text '
    'of that study. Verdicts: accurate; inaccurate (wrong fact, number, denominator, scope or attribution); '
    'oversimplified (a reader could not tell what was done, or the wording implies more than the paper shows). '
    'Corrected wording is given for every statement that is not accurate; the corrections were applied in the '
    'second draft (see revision_log.md).', '',
    '**Totals: %d statements from %d papers; %d accurate (%.0f%%), %d inaccurate (%.0f%%), %d oversimplified (%.0f%%).**'
    % (N, len(files), tot['accurate'], 100 * tot['accurate'] / N, tot['inaccurate'], 100 * tot['inaccurate'] / N,
       tot['oversimplified'], 100 * tot['oversimplified'] / N), '',
    '| rec_id | Statements | Accurate | Inaccurate | Oversimplified |', '|---|---|---|---|---|']
out = head + rows + ['', ''] + bodies
open(os.path.join(root, 'draft/claim_audit.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(N, tot)
