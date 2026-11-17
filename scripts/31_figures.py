#!/usr/bin/env python3
"""Additional review figures (2026-11-10). Run from lit_review_LLM/. Outputs in synthesis/."""
import collections
import csv
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch

OUT = 'synthesis'
INK, INK2, MUTED, GRID, SURF = '#0b0b0b', '#52514e', '#8a8984', '#e4e3df', '#fcfcfb'
BLUE = '#2a78d6'
CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4']
STATUS = {'Succeeded': ('#0ca30c', '✓'), 'Conditional': ('#fab219', '~'), 'Failed': ('#d03b3b', '✗'), 'Not shown': ('#b7b6b0', '?')}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2,
                     'xtick.color': INK2, 'ytick.color': INK, 'figure.facecolor': SURF, 'axes.facecolor': SURF})
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from synth_maps import S, THEMES, DOMAINS, H2H_LABEL, DUP  # noqa: E402
rows = list(csv.DictReader(open('extraction/extraction.csv', encoding='utf-8', newline='')))
_k = collections.Counter()
for r in rows:
    _k[r['rec_id']] += 1
    r['key'] = f"{r['rec_id']}.{_k[r['rec_id']]}"
    r.update({f'm_{a}': b for a, b in S[r['key']].items()})
    r['process'] = r['adjacent'].strip().lower() == 'no'
rows = [r for r in rows if r['key'] not in DUP]  # same experiment as another setup: counted once
scr = {r['rec_id']: r for r in csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline=''))}


def save(fig, name):
    fig.savefig(f'{OUT}/{name}.png', facecolor=SURF, dpi=200)
    fig.savefig(f'{OUT}/{name}.svg', facecolor=SURF)
    plt.close(fig)


# ---- Fig: where the LLM sits in the control hierarchy -------------------------------------
_LDEF = [('operator', 'Operator and HMI', 'explain, answer, translate commands'),
         ('design', 'Design and tuning (offline)', 'controller structure, gains, NMPC design'),
         ('supervisory', 'Supervisory and advanced control', 'setpoints, MPC settings, mode choice, recovery'),
         ('actuation', 'Regulatory control and actuation', 'LLM computes the actuator move')]
_ORD = {'Succeeded': 0, 'Conditional': 1, 'Failed': 2, 'Not shown': 3}
# Third draft (2026-11-13): one chip per paper and layer, with one coloured square per tested setup, drawn at the
# printed width (7.1 in) so that labels print at 8 pt; the per-setup version was unreadable at 105 setups.
import re as _re  # noqa: E402


def _paper_label(r):
    m = _re.match(r'^(.*?\d{4}[a-z]?)', r['m_label'])
    lab = m.group(1) if m else r['m_label'].split(' ')[0] + ' 2026'   # Rosenthal's labels carry no year
    lab = {'Wen 2026': 'Wen 2026 (W&S)', 'Wen 2026b': 'Wen 2026 (tank)',
           'Vyas 2024': 'Vyas 2025 (on/off)'}.get(lab, lab)   # Stage C: S038 is the 2025 IFAC paper
    return lab + ('' if r['process'] else '*')


LAYERS = []
for key, name, sub in _LDEF:
    g = collections.OrderedDict()
    for r in rows:
        if r['m_layer'] == key:
            g.setdefault(_paper_label(r), []).append((r['outcome'], r['process']))
    # Stage C (2026-11-16): process-system papers first, adjacent papers grouped after them
    chips = sorted(((lab, sorted(o, key=lambda x: _ORD[x[0]])) for lab, o in g.items()),
                   key=lambda x: (x[0].endswith('*'), _ORD[x[1][0][0]], x[0]))
    LAYERS.append((name, sub, chips))
assert sum(len(o) for l in LAYERS for _, o in l[2]) == len(rows)
LEFT, X0, X1, CH, RG, PAD = 1, 25.0, 99.5, 3.9, 5.0, 2.2
LAYER_TITLES = {'Operator and HMI': 'Operator and HMI', 'Design and tuning (offline)': 'Design and tuning\n(offline)',
                'Supervisory and advanced control': 'Supervisory and\nadvanced control', 'Regulatory control and actuation': 'Regulatory control\nand actuation'}
SUBS = {'explain, answer, translate commands': 'explain, answer,\ntranslate commands', 'controller structure, gains, NMPC design': 'structure, gains,\nNMPC design',
        'setpoints, MPC settings, mode choice, recovery': 'setpoints, MPC settings,\nmode choice, recovery', 'LLM computes the actuator move': 'LLM computes the\nactuator move'}


FW = 7.1                     # figure width in inches = printed width
CW = 0.60 * 8 / 72 / FW * 100  # approximate width of one 8-pt character in axis units
SQ = 1.55                    # outcome square, axis units


_mf, _ma = plt.subplots(figsize=(FW, 3))
_mf.subplots_adjust(left=0.01, right=0.99)
_ma.set_xlim(0, 100)
_mr = _mf.canvas.get_renderer()


def text_w(s):
    """Width of an 8-pt label in axis units, measured with the renderer (not estimated per character)."""
    t = _ma.text(0, 0, s, fontsize=8)
    bb = t.get_window_extent(_mr).transformed(_ma.transData.inverted())
    t.remove()
    return bb.width


def chip_rows(chips):
    x, rws, layout = X0, 0, []
    for label, outs in chips:
        w = 1.4 + text_w(label) + 0.6 + len(outs) * (SQ + 0.35)
        if x + w > X1:
            x, rws = X0, rws + 1
        layout.append((x, rws, w, label, outs))
        x += w + 0.8
    return layout, rws + 1


plans = [chip_rows(ch) for _, _, ch in LAYERS]
heights = [max(19.0, n * RG + 2 * PAD) for _, n in plans]
total = sum(heights) + 2.0 * len(heights) + 9
UH = 0.072                   # inches per vertical axis unit
fig, ax = plt.subplots(figsize=(FW, UH * total + 0.75))
fig.subplots_adjust(left=0.01, right=0.99, top=1 - 0.55 / (UH * total + 0.75), bottom=0.03)
ax.set_xlim(0, 100)
ax.set_ylim(-1, total)
ax.axis('off')
y1 = total - 2
for (name, sub, chips), (layout, n), h in zip(LAYERS, plans, heights):
    y0 = y1 - h
    ax.add_patch(FancyBboxPatch((LEFT, y0), 98.5, h, boxstyle='round,pad=0,rounding_size=1.2', fc='#f3f2ee', ec='none'))
    ax.text(LEFT + 1.0, y1 - 2.0, LAYER_TITLES[name], fontsize=8.5, weight='bold', color=INK, va='top', linespacing=1.1)
    ax.text(LEFT + 1.0, y1 - 8.6, SUBS[sub], fontsize=7.5, color=INK2, va='top', linespacing=1.1)
    nset = sum(len(o) for _, o in chips)
    ax.text(LEFT + 1.0, y0 + 1.0, f'{nset} setups, {len(chips)} papers', fontsize=7.5, color=MUTED, va='bottom')
    for x, r, w, label, outs in layout:
        yc = y1 - PAD - r * RG
        ax.add_patch(FancyBboxPatch((x, yc - CH), w, CH, boxstyle='round,pad=0,rounding_size=0.8', fc=SURF, ec=GRID, lw=0.6))
        ax.text(x + 0.7, yc - CH / 2, label, fontsize=8, color=INK, ha='left', va='center')
        sx = x + 0.7 + text_w(label) + 0.6
        for o, isproc in outs:
            ax.add_patch(FancyBboxPatch((sx, yc - CH / 2 - SQ * 0.75), SQ, SQ * 1.5, boxstyle='round,pad=0,rounding_size=0.3',
                                        fc=STATUS[o][0], ec=SURF if isproc else INK2, lw=0 if isproc else 0.5,
                                        alpha=1.0 if isproc else 0.45, hatch=None if isproc else '////'))
            sx += SQ + 0.35
    y1 = y0 - 2.0
ax.add_patch(FancyBboxPatch((LEFT, y1 - 6.0), 98.5, 6.0, boxstyle='round,pad=0,rounding_size=1.2', fc='none', ec=INK2, lw=1.0, ls=(0, (4, 3))))
ax.text(50, y1 - 3.0, 'LLM closing the loop in an operating plant: no studies yet', fontsize=8.5, color=INK2, ha='center', va='center')
handles = [Patch(fc=c, ec='none', label=k) for k, (c, g) in STATUS.items()] + [
    Patch(fc='#b7b6b0', ec=INK2, lw=0.5, alpha=0.45, hatch='////', label='Adjacent domain (*)')]
ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(0.0, 1.0), ncol=5, frameon=False, fontsize=8, handlelength=1.0,
          title=None, columnspacing=1.2)
ax.text(LEFT, -0.6, 'One box per paper and layer; one square per tested setup, coloured by outcome.\n* and light hatched squares: adjacent domain (listed after the process-system papers in each layer).',
        fontsize=7.5, color=INK2, va='top')
save(fig, 'fig_hierarchy')

# ---- Fig: head-to-head ----------------------------------------------------------------------
_POS = {'nonllm': -1, 'tie': 0, 'mixed': 0, 'llm': 1, 'nq': None}
_hh = sorted([r for r in rows if r['m_h2h'] not in (None, 'gate')],
             key=lambda r: (_POS[r['m_h2h']] if _POS[r['m_h2h']] is not None else 2, r['m_label']))
H2H = [(r['m_label'] + ('' if r['process'] else ' *'), _POS[r['m_h2h']], r['m_h2h_txt'].split(';')[0].replace('$', r'\$')) for r in _hh]
import textwrap as _tw
_wrap = lambda t: '\n'.join(_tw.wrap(t, 58))
fig, ax = plt.subplots(figsize=(8.0, 0.185 * len(H2H) + 1.3))  # Stage C: near printed width so labels stay readable
n = len(H2H)
for i, (lab, pos, note) in enumerate(H2H):
    y = n - 1 - i
    ax.axhline(y, color=GRID, lw=0.6, zorder=0)
    if pos is None:
        ax.plot(0, y, 'o', ms=6.5, mfc=SURF, mec=MUTED, mew=1.4, zorder=3)
        ax.text(0.12, y, _wrap(note), va='center', fontsize=6.6, color=INK2, linespacing=0.95)
    else:
        ax.plot(pos, y, 'o', ms=6.5, color=BLUE, mec=SURF, mew=1.5, zorder=3)
        ax.text(pos + (0.12 if pos < 1 else -0.12), y, _wrap(note) if pos == 0 else note, va='center', ha='left' if pos < 1 else 'right', fontsize=6.6, color=INK2, linespacing=0.95)
ax.set_yticks(range(n))
ax.set_yticklabels([h[0] for h in reversed(H2H)], fontsize=7.5)
ax.set_xticks([-1, 0, 1])
ax.set_xticklabels(['Non-LLM\nbetter', 'Tie or mixed', 'LLM better'], fontsize=9)
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-0.7, n - 0.3)
for x in (-0.5, 0.5):
    ax.axvline(x, color=GRID, lw=1, zorder=0)
for s in ('top', 'right', 'left', 'bottom'):
    ax.spines[s].set_visible(False)
ax.tick_params(length=0)
ax.legend(handles=[Line2D([], [], marker='o', lw=0, ms=9, color=BLUE, label='Result reported'),
                   Line2D([], [], marker='o', lw=0, ms=9, mfc=SURF, mec=MUTED, mew=1.8, label='Comparison not quantified')],
          loc='upper left', bbox_to_anchor=(0.0, -0.045), ncol=2, frameon=False, fontsize=8)
fig.tight_layout(rect=(0, 0, 1, 0.975))
fig.text(0.01, 0.995, f'Head-to-head: LLM against a non-LLM method ({len(H2H)} setups; * adjacent domain)', fontsize=10, color=INK, va='top')
save(fig, 'fig_head_to_head')

# ---- Fig: domain (process type) x theme, setups; second panel operation x theme -------------
DOMS = DOMAINS
c = collections.Counter((r['m_domain'], scr[r['rec_id']]['theme']) for r in rows)
M = [[c[(d, t)] for t in THEMES] for d in DOMS]
OPS = ['continuous', 'batch', 'not applicable or NR']
co = collections.Counter(((r['operation'] if r['operation'] in ('continuous', 'batch') else 'not applicable or NR'), scr[r['rec_id']]['theme']) for r in rows)
M2 = [[co[(o, t)] for t in THEMES] for o in OPS]
cmap = LinearSegmentedColormap.from_list('blue', ['#f3f7fd', '#9ec5f4', '#3987e5', '#1c5cab'])
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(7.1, 6.6), gridspec_kw={'height_ratios': [len(DOMS), len(OPS)], 'hspace': 0.12})
vmax = max(max(m) for m in M + M2)
XL = ['Language to\nMPC or tuning', 'LLM in or\nabove the loop', 'LLM-facilitated\nhybrid control', 'SCADA, MCP\nand OPC', 'Recovery and\nsafeguards']
for a_, MM, YL in ((ax, M, DOMS), (ax2, M2, ['Continuous operation', 'Batch or semi-batch', 'Not applicable or not reported'])):
    a_.imshow(MM, cmap=cmap, vmin=0, vmax=vmax, aspect='auto')
    for i in range(len(MM)):
        for j in range(len(THEMES)):
            v = MM[i][j]
            a_.text(j, i, v if v else '·', ha='center', va='center', fontsize=10, color='white' if v >= 0.45 * vmax else (INK if v else MUTED))
    a_.set_yticks(range(len(YL)))
    a_.set_yticklabels(YL, fontsize=8.5)
    a_.set_xticks([x - 0.5 for x in range(1, len(THEMES))], minor=True)
    a_.set_yticks([y - 0.5 for y in range(1, len(YL))], minor=True)
    a_.grid(which='minor', color=SURF, lw=2)
    a_.tick_params(which='both', length=0)
    for sp in a_.spines.values():
        sp.set_visible(False)
_na = sum('(adjacent)' in d for d in DOMS)
ax.axhline(len(DOMS) - _na - 0.5, color=INK2, lw=1.2, ls=(0, (4, 2)))
ax.set_xticks([])
ax2.set_xticks(range(len(THEMES)))
ax2.set_xticklabels(XL, fontsize=8.5)
fig.text(0.01, 0.975, f'Tested setups by process type and theme (top) and by operation (bottom), n = {len(rows)}', fontsize=10, color=INK, va='top')
fig.subplots_adjust(left=0.36, right=0.99, top=0.93, bottom=0.09)  # Stage C: left margin fits the longest adjacent label
save(fig, 'fig_gap_map')

# ---- Fig: core papers per year by theme ----------------------------------------------------
core = [r for r in scr.values() if r['tier'] == 'core']
allrec = [dict(r, year='2026' if r['year'] == '2027' else r['year']) for r in scr.values() if r['year']]
years = sorted({r['year'] for r in allrec})
TIERS = [('core', 'Core: LLM acts on or connects to the control layer', BLUE), ('context', 'Context: related methods and reviews', '#eb6834'),
         ('out', 'Other LLM-in-automation (PLC code, monitoring)', '#c9c8c2')]
cy = collections.Counter((r['year'], r['tier']) for r in allrec)
fig, ax = plt.subplots(figsize=(7.2, 4.2))
bottom = [0] * len(years)
for t, name, col in TIERS:
    vals = [cy[(y, t)] for y in years]
    ax.bar(years, vals, bottom=bottom, color=col, width=0.62, edgecolor=SURF, linewidth=2, label=name, zorder=3)
    for x, b, v in zip(years, bottom, vals):
        if v >= 12:
            ax.text(x, b + v / 2, str(v), ha='center', va='center', fontsize=8.5, color='white' if t != 'out' else INK, zorder=4)
    bottom = [b + v for b, v in zip(bottom, vals)]
for x, tot in zip(years, bottom):
    ax.text(x, tot + 3, str(tot), ha='center', va='bottom', fontsize=9, color=INK)
ax.set_ylabel('Records screened')
ax.grid(axis='y', color=GRID, lw=0.6, zorder=0)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.set_ylim(0, max(bottom) * 1.18)
ax.legend(loc='upper left', frameon=False, fontsize=8)
ax.set_title(f'LLM studies in process automation per year (n = {len(allrec)}; 2026 to November)', loc='left', fontsize=11, color=INK, pad=10)
fig.tight_layout()
save(fig, 'fig_papers_per_year')
with open(f'{OUT}/fig_papers_per_year_data.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['year'] + [t for t, _, _ in TIERS] + ['total'])
    for y, tot in zip(years, bottom):
        w.writerow([y] + [cy[(y, t)] for t, _, _ in TIERS] + [tot])

# ---- Fig: appraisal profile ----------------------------------------------------------------
CRIT = [('C1', 'Right non-LLM comparator'), ('C2', 'Control metrics reported'), ('C3', 'Off-nominal conditions tested'),
        ('C4', 'Repeated runs and reproducible'), ('C5', 'LLM decision quality measured'), ('C6', 'Safeguards challenged')]
pct = [100 * sum(r[c] == 'Y' for r in rows) / len(rows) for c, _ in CRIT]
fig, ax = plt.subplots(figsize=(7.2, 3.4))
ys = list(range(len(CRIT)))[::-1]
ax.barh(ys, pct, color=BLUE, height=0.55, zorder=3)
ax.barh(ys, [100 - p for p in pct], left=pct, color='#e9e8e4', height=0.55, zorder=2)
_pr = [r for r in rows if r['process']]
ppct = [100 * sum(r[c] == 'Y' for r in _pr) / len(_pr) for c, _ in CRIT]
ax.plot(ppct, ys, '|', ms=16, mew=2.2, color='#eb6834', zorder=5)
for y, p, pp, (c, lab) in zip(ys, pct, ppct, CRIT):
    ax.text(max(p, pp) + 1.5, y, f'{p:.0f}% (process {pp:.0f}%)', va='center', fontsize=8.5, color=INK, zorder=4)
ax.legend(handles=[Patch(fc=BLUE, label=f'All graded setups (n = {len(rows)})'),
                   Line2D([], [], marker='|', lw=0, ms=12, mew=2.2, color='#eb6834', label=f'Process systems only (n = {len(_pr)})')],
          loc='lower right', bbox_to_anchor=(1.0, 1.0), ncol=2, frameon=False, fontsize=8)
ax.set_yticks(ys)
ax.set_yticklabels([f'{c}  {lab}' for c, lab in CRIT], fontsize=9)
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0', '25', '50', '75', '100%'])
for s in ('top', 'right', 'left', 'bottom'):
    ax.spines[s].set_visible(False)
ax.tick_params(length=0)
ax.set_title(f'Setups meeting each appraisal criterion', loc='left', fontsize=11, color=INK, pad=22)
fig.tight_layout()
save(fig, 'fig_appraisal_profile')
print('done', len(core), years)
