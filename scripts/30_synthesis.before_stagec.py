#!/usr/bin/env python3
"""Synthesis tables and figures for the focused review. Run from lit_review_LLM/. Outputs in synthesis/.
Revision 2026-11-12: per-setup maps live in scripts/synth_maps.py (layer, domain, head-to-head, safeguard, timing).
Every headline count is given for all graded setups and for process systems only (adjacent = no)."""
import collections
import csv
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from synth_maps import S, THEMES, DOMAINS, H2H_LABEL, TIM, DUP  # noqa: E402

OUT = 'synthesis'
os.makedirs(OUT, exist_ok=True)
rows = list(csv.DictReader(open('extraction/extraction.csv', encoding='utf-8', newline='')))
scr = {r['rec_id']: r for r in csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline=''))}
k = collections.Counter()
for r in rows:
    k[r['rec_id']] += 1
    r['key'] = f"{r['rec_id']}.{k[r['rec_id']]}"
    s = scr[r['rec_id']]
    r['theme'] = s['theme']
    r['cite'] = f"{s['first_author'].split(' ')[-1]} {s['year']}"
    r['process'] = r['adjacent'].strip().lower() == 'no'
    r['op'] = r['operation'] if r['operation'] in ('continuous', 'batch') else 'not applicable or NR'
missing = [r['key'] for r in rows if r['key'] not in S]
extra = [x for x in S if x not in {r['key'] for r in rows}]
assert not missing and not extra, (missing, extra)
for r in rows:
    r.update({f'm_{a}': b for a, b in S[r['key']].items()})
    # a head-to-head class only for setups with C1 = Y, and C1 = Y must have a class
    assert (r['C1'] == 'Y') == (r['m_h2h'] is not None), (r['key'], r['C1'], r['m_h2h'])
n_all_rows = len(rows)
rows = [r for r in rows if r['key'] not in DUP]  # same experiment as another setup: counted once (2026-11-13)

AUTH = ['Advise', 'Propose', 'Set targets', 'Act']
EVID = ['E0', 'E1', 'E2', 'E3', 'E4', 'E5']
OUTC = ['Succeeded', 'Conditional', 'Failed', 'Not shown']
LAYERS = ['operator', 'design', 'supervisory', 'actuation']
proc = [r for r in rows if r['process']]
papers = sorted({r['rec_id'] for r in rows})
ppapers = sorted({r['rec_id'] for r in proc})
md = []


def table(header, data):
    md.append('| ' + ' | '.join(header) + ' |')
    md.append('|' + '---|' * len(header))
    for d in data:
        md.append('| ' + ' | '.join(str(x) for x in d) + ' |')
    md.append('')


def pct(sub, f):
    return f"{100 * sum(r[f] == 'Y' for r in sub) / len(sub):.0f}%" if sub else '-'


md += ['# Synthesis tables', '',
       f'Source: extraction/extraction.csv ({n_all_rows} graded setups; {len(rows)} independent setups after counting '
       f'{n_all_rows - len(rows)} duplicate-experiment setups once ({", ".join(f"{a} = {b}" for a, b in DUP.items())}); '
       f'{len(papers)} papers; every paper read in full). '
       f'Process systems only (sensitivity): {len(proc)} setups from {len(ppapers)} papers. Counts are per tested setup unless stated.', '']

# ---- Headline counts, all vs process-only ------------------------------------------------
md += ['## Table 0. Headline counts: all graded setups and process systems only', '']


def headline(sub):
    h2h = [r for r in sub if r['m_h2h'] not in (None, 'gate')]
    c = collections.Counter(r['m_h2h'] for r in h2h)
    return [len(sub), len({r['rec_id'] for r in sub}),
            sum(r['evidence'] == 'E1' for r in sub), sum(r['evidence'] == 'E2' for r in sub),
            sum(r['evidence'] == 'E3' for r in sub), sum(r['evidence'] == 'E4' for r in sub), sum(r['evidence'] == 'E5' for r in sub),
            sum(r['authority'] == 'Act' for r in sub),
            sum(r['outcome'] == 'Succeeded' for r in sub), sum(r['outcome'] == 'Conditional' for r in sub),
            sum(r['outcome'] == 'Failed' for r in sub), sum(r['outcome'] == 'Not shown' for r in sub),
            sum(r['C1'] == 'Y' for r in sub), len(h2h), c['nonllm'], c['tie'], c['mixed'], c['llm'], c['nq'],
            sum(r['C6'] == 'Y' for r in sub), sum(r['m_safe'] is not None for r in sub),
            sum(r['plant_timing'].lower().startswith('real time') for r in sub)]


HL = ['Setups', 'Papers', 'E1', 'E2', 'E3', 'E4', 'E5', 'Act', 'Succeeded', 'Conditional', 'Failed', 'Not shown',
      'C1 = Y', 'Direct LLM vs non-LLM', 'Non-LLM better', 'Tie', 'Mixed', 'LLM better', 'Not quantified',
      'C6 = Y', 'Safeguard described', 'Real time on hardware or plant']
a, p = headline(rows), headline(proc)
table(['Count', 'All graded', 'Process systems only'], [[h, x, y] for h, x, y in zip(HL, a, p)])
md += ['Adjacent (excluded from the process-only column): ' + '; '.join(
    f"{k2} {v}" for k2, v in collections.Counter(r['adjacent'] for r in rows if not r['process']).most_common()) + '.', '']

md += ['## Table 1. Authority by evidence level (setups)', '']
c = collections.Counter((r['authority'], r['evidence']) for r in rows)
table(['Authority'] + EVID + ['Total'], [[a_] + [c[(a_, e)] or '·' for e in EVID] + [sum(c[(a_, e)] for e in EVID)] for a_ in AUTH] +
      [['**Total**'] + [sum(c[(a_, e)] for a_ in AUTH) or '·' for e in EVID] + [len(rows)]])

md += ['## Table 2. Outcome by authority (setups)', '']
c = collections.Counter((r['authority'], r['outcome']) for r in rows)
table(['Authority'] + OUTC + ['Total'], [[a_] + [c[(a_, o)] or '·' for o in OUTC] + [sum(c[(a_, o)] for o in OUTC)] for a_ in AUTH] +
      [['**Total**'] + [sum(c[(a_, o)] for a_ in AUTH) for o in OUTC] + [len(rows)]])

md += ['## Table 3. Outcome by theme (setups)', '']
c = collections.Counter((r['theme'], r['outcome']) for r in rows)
table(['Theme'] + OUTC + ['Total', 'Papers'], [[THEMES[t]] + [c[(t, o)] or '·' for o in OUTC] + [sum(c[(t, o)] for o in OUTC),
      len({r['rec_id'] for r in rows if r['theme'] == t})] for t in THEMES])

md += ['## Table 3b. Outcome by control layer (setups)', '']
c = collections.Counter((r['m_layer'], r['outcome']) for r in rows)
table(['Layer'] + OUTC + ['Total', 'Process only'], [[l_] + [c[(l_, o)] or '·' for o in OUTC] + [sum(c[(l_, o)] for o in OUTC),
      sum(r['m_layer'] == l_ for r in proc)] for l_ in LAYERS])

md += ['## Table 4. Appraisal criteria met (% of setups scored Y)', '',
       'C1 right comparator · C2 control metrics · C3 off-nominal · C4 repeatable · C5 decision quality measured · C6 safeguards challenged.', '']
data = []
for t in list(THEMES) + ['ALL', 'PROC']:
    sub = rows if t == 'ALL' else proc if t == 'PROC' else [r for r in rows if r['theme'] == t]
    name = {'ALL': '**All setups**', 'PROC': '**Process systems only**'}.get(t, THEMES.get(t))
    data.append([name, len(sub)] + [pct(sub, f'C{i}') for i in range(1, 7)])
table(['Theme', 'n', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6'], data)
md += ['Counts of Y (all setups): ' + ', '.join(f"C{i} {sum(r[f'C{i}'] == 'Y' for r in rows)}" for i in range(1, 7)) + '.', '']

md += ['## Table 4b. Domain (process type) by operation (setups)', '']
OPS = ['continuous', 'batch', 'not applicable or NR']
c = collections.Counter((r['m_domain'], r['op']) for r in rows)
table(['Domain'] + OPS + ['Total', 'Papers'], [[d] + [c[(d, o)] or '·' for o in OPS] + [sum(c[(d, o)] for o in OPS),
      len({r['rec_id'] for r in rows if r['m_domain'] == d})] for d in DOMAINS] +
      [['**Total**'] + [sum(c[(d, o)] for d in DOMAINS) for o in OPS] + [len(rows), len(papers)]])
md += ['## Table 4c. Operation by theme (setups)', '']
c = collections.Counter((r['theme'], r['op']) for r in rows)
table(['Theme'] + OPS, [[THEMES[t]] + [c[(t, o)] or '·' for o in OPS] for t in THEMES])

# ---- Table 5: head-to-head -------------------------------------------------------------------
h2h = [r for r in rows if r['C1'] == 'Y']
md += ['## Table 5. Setups with a non-LLM comparator (C1 = Y)', '']
table(['Study', 'Key', 'Setup', 'Evidence', 'Adjacent', 'Comparator', 'Class', 'Result'],
      [[r['cite'], r['key'], r['setup'][:70], r['evidence'], '' if r['process'] else r['adjacent'], r['C1_note'][:80],
        H2H_LABEL.get(r['m_h2h'], 'With vs without gate'), r['m_h2h_txt']] for r in h2h])
direct = [r for r in h2h if r['m_h2h'] != 'gate']
cc = collections.Counter(r['m_h2h'] for r in direct)
ccp = collections.Counter(r['m_h2h'] for r in direct if r['process'])
md += [f"Direct LLM-versus-non-LLM comparisons: {len(direct)} setups from {len({r['rec_id'] for r in direct})} papers: " +
       ', '.join(f"{H2H_LABEL[x]} {cc[x]}" for x in H2H_LABEL) + '.',
       f"Process systems only: {sum(ccp.values())} setups from {len({r['rec_id'] for r in direct if r['process']})} papers: " +
       ', '.join(f"{H2H_LABEL[x]} {ccp[x]}" for x in H2H_LABEL) + '.', '']

# ---- Table 6: safeguards ---------------------------------------------------------------------
md += ['## Table 6. Safeguard architectures (setups that describe one)', '']
srows = sorted([r for r in rows if r['m_safe']], key=lambda r: (r['C6'] != 'Y', r['m_safe'][0], r['key']))
table(['Study', 'Key', 'Type', 'Safeguard', 'Challenged (C6)', 'What was tested'],
      [[r['cite'], r['key'], r['m_safe'][0], r['m_safe'][1], r['C6'], r['C6_note'][:90]] for r in srows])
md += [f"Setups describing a safeguard: {len(srows)}; challenged (C6 = Y): {sum(r['C6'] == 'Y' for r in rows)} setups from "
       f"{len({r['rec_id'] for r in rows if r['C6'] == 'Y'})} papers. By type: " +
       ', '.join(f"{t} {n}" for t, n in collections.Counter(r['m_safe'][0] for r in srows).most_common()) + '.', '']

# ---- Table 7: timing -------------------------------------------------------------------------
md += ['## Table 7. Timing (descriptive)', '']
trows = [r for r in rows if r['llm_latency'] not in ('NR', '') or r['loop_timing'] not in ('NR', '', 'n/a')]
table(['Study', 'Key', 'LLM latency', 'Loop timing', 'Plant timing'],
      [[r['cite'], r['key'], r['llm_latency'][:90], r['loop_timing'][:90], r['plant_timing'][:40]] for r in trows])
md += [f"Setups that ran in real time on hardware or in a plant: {sum(r['plant_timing'].lower().startswith('real time') for r in rows)} "
       f"({', '.join(r['key'] for r in rows if r['plant_timing'].lower().startswith('real time'))}).", '']
open(f'{OUT}/tables.md', 'w', encoding='utf-8').write('\n'.join(md))

# ---- Figure F: timescale ---------------------------------------------------------------------
BLUE, ORANGE, INK, INK2, GRID, SURF = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2,
                     'xtick.color': INK2, 'ytick.color': INK, 'figure.facecolor': SURF, 'axes.facecolor': SURF})
fig, ax = plt.subplots(figsize=(8.8, 5.8), dpi=200)
ax.axvspan(60, 600, color='#cde2fb', alpha=0.6, lw=0, zorder=0)
ax.text(190, len(TIM) - 0.35, 'slow supervisory\nrange (1-10 min)', ha='center', va='top', fontsize=7.5, color=INK2)
for i, (lab, loop, lat, note) in enumerate(reversed(TIM)):
    y = i
    if lat:
        ax.plot([lat[0], lat[1]], [y, y], color=ORANGE, lw=4, solid_capstyle='round', zorder=3)
        if lat[0] == lat[1]:
            ax.plot(lat[0], y, 'o', ms=8, color=ORANGE, mec=SURF, mew=2, zorder=5)
    if loop:
        if isinstance(loop, tuple):
            ax.plot(list(loop), [y, y], color=BLUE, lw=4, solid_capstyle='round', zorder=4)
        else:
            ax.plot(loop, y, 'o', ms=8, color=BLUE, mec=SURF, mew=2, zorder=4)
    if note:
        xs = max([x for x in (lat or ())] + ([*loop] if isinstance(loop, tuple) else [loop] if loop else []))
        ax.text(xs * 1.6, y, note, va='center', fontsize=7.5, color=INK2)
ax.set_yticks(range(len(TIM)))
ax.set_yticklabels([t[0] for t in reversed(TIM)])
ax.set_xscale('log')
ax.set_xlim(1e-3, 1e5)
ax.set_xlabel('Time (s, log scale)')
ax.grid(axis='x', color=GRID, lw=0.6, zorder=0)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.legend(handles=[Line2D([], [], marker='o', color=BLUE, lw=0, ms=8, label='Control loop or update period'),
                   Line2D([], [], color=ORANGE, lw=4, label='Reported LLM response time')],
          loc='lower left', frameon=False, fontsize=8)
ax.set_title('LLM response time against loop timing, where reported', loc='left', fontsize=11, color=INK, pad=10)
fig.tight_layout()
fig.savefig(f'{OUT}/fig1_timescale.png', facecolor=SURF)
fig.savefig(f'{OUT}/fig1_timescale.svg', facecolor=SURF)
plt.close(fig)
with open(f'{OUT}/fig1_timescale_data.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['study_setup', 'loop_period_s', 'llm_latency_low_s', 'llm_latency_high_s', 'note'])
    for lab, loop, lat, note in TIM:
        w.writerow([lab, '-'.join(map(str, loop)) if isinstance(loop, tuple) else (loop or ''), lat[0] if lat else '', lat[1] if lat else '', note])

# ---- Figure B: authority x evidence heat map -------------------------------------------------
c = collections.Counter((r['authority'], r['evidence']) for r in rows)
M = [[c[(a_, e)] for e in EVID] for a_ in AUTH]
cmap = LinearSegmentedColormap.from_list('blue', ['#f3f7fd', '#9ec5f4', '#3987e5', '#1c5cab', '#0d366b'])
fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200)
ax.imshow(M, cmap=cmap, vmin=0, vmax=max(max(m) for m in M), aspect='auto')
vmax = max(max(m) for m in M)
for i, a_ in enumerate(AUTH):
    for j, e in enumerate(EVID):
        v = M[i][j]
        ax.text(j, i, v if v else '·', ha='center', va='center', fontsize=10, color='white' if v >= 0.45 * vmax else INK)
ax.set_xticks(range(len(EVID)))
ax.set_xticklabels(['E0\nconcept', 'E1\nsimulation', 'E2\nbenchmark data', 'E3\nlab hardware', 'E4\npilot or\nindustrial data', 'E5\noperating\nplant'], fontsize=8)
ax.set_yticks(range(len(AUTH)))
ax.set_yticklabels(AUTH)
ax.set_xticks([x - 0.5 for x in range(1, len(EVID))], minor=True)
ax.set_yticks([y - 0.5 for y in range(1, len(AUTH))], minor=True)
ax.grid(which='minor', color=SURF, lw=2)
ax.tick_params(which='both', length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title(f'Tested setups by LLM authority and evidence level (n = {len(rows)})', loc='left', fontsize=11, color=INK, pad=10)
fig.tight_layout()
fig.savefig(f'{OUT}/fig2_authority_evidence.png', facecolor=SURF)
fig.savefig(f'{OUT}/fig2_authority_evidence.svg', facecolor=SURF)
plt.close(fig)
print('setups', len(rows), 'papers', len(papers), '| process-only', len(proc), len(ppapers))
print('direct h2h', len(direct), dict(cc), '| process', dict(ccp))
