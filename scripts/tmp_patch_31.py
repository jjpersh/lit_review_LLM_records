"""One-off patch of scripts/31_figures.py for the revision run (2026-11-12): figures driven by synth_maps.py."""
p = 'scripts/31_figures.py'
s = open(p, encoding='utf-8').read()
s = s.replace('import collections\nimport csv\n', 'import collections\nimport csv\nimport os\nimport sys\n', 1)
s = s.replace("THEMES = {'T1': 'Language to MPC/tuning', 'T2': 'In or above the loop', 'T3': 'Switching', 'T4': 'SCADA/MCP/OPC', 'T5': 'Recovery and safeguards'}\nrows = list(csv.DictReader(open('extraction/extraction.csv', encoding='utf-8', newline='')))",
              """sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from synth_maps import S, THEMES, DOMAINS, H2H_LABEL  # noqa: E402
rows = list(csv.DictReader(open('extraction/extraction.csv', encoding='utf-8', newline='')))
_k = collections.Counter()
for r in rows:
    _k[r['rec_id']] += 1
    r['key'] = f"{r['rec_id']}.{_k[r['rec_id']]}"
    r.update({f'm_{a}': b for a, b in S[r['key']].items()})
    r['process'] = r['adjacent'].strip().lower() == 'no'""", 1)
start = s.index('LAYERS = [')
end = s.index("assert sum(len(l[2]) for l in LAYERS)")
s = s[:start] + '''_LDEF = [('operator', 'Operator and HMI', 'explain, answer, translate commands'),
         ('design', 'Design and tuning (offline)', 'controller structure, gains, NMPC design'),
         ('supervisory', 'Supervisory and advanced control', 'setpoints, MPC settings, mode choice, recovery'),
         ('actuation', 'Regulatory control and actuation', 'LLM computes the actuator move')]
_ORD = {'Succeeded': 0, 'Conditional': 1, 'Failed': 2, 'Not shown': 3}
LAYERS = [(name, sub, sorted([(r['m_label'] + ('' if r['process'] else ' *'), r['outcome']) for r in rows if r['m_layer'] == key],
                             key=lambda x: (_ORD[x[1]], x[0]))) for key, name, sub in _LDEF]
''' + s[end:]
s = s.replace("ax.set_title('Where the LLM sits in the control hierarchy, and what happened (39 tested setups)'",
              "ax.text(LEFT, -0.6, '* adjacent domain (not a process system)', fontsize=7.8, color=INK2, va='top')\n"
              "ax.set_title(f'Where the LLM sits in the control hierarchy, and what happened ({len(rows)} tested setups)'")
start = s.index('H2H = [')
end = s.index('fig, ax = plt.subplots(figsize=(9.2, 6.4))')
s = s[:start] + '''_POS = {'nonllm': -1, 'tie': 0, 'mixed': 0, 'llm': 1, 'nq': None}
_hh = sorted([r for r in rows if r['m_h2h'] not in (None, 'gate')],
             key=lambda r: (_POS[r['m_h2h']] if _POS[r['m_h2h']] is not None else 2, r['m_label']))
H2H = [(r['m_label'] + ('' if r['process'] else ' *'), _POS[r['m_h2h']], r['m_h2h_txt'][:58]) for r in _hh]
''' + s[end:]
s = s.replace("fig, ax = plt.subplots(figsize=(9.2, 6.4))\nn = len(H2H)", "fig, ax = plt.subplots(figsize=(10.4, 0.27 * len(H2H) + 1.6))\nn = len(H2H)")
s = s.replace("ax.set_title('Head-to-head: LLM against a non-LLM method (18 comparisons)'",
              "ax.set_title(f'Head-to-head: LLM against a non-LLM method ({len(H2H)} setups; * adjacent domain)'")
s = s.replace("'Mixed or tie'", "'Tie or mixed'")
start = s.index('# ---- Fig: gap map')
end = s.index('# ---- Fig: core papers per year')
s = s[:start] + '''# ---- Fig: domain (process type) x theme, setups; second panel operation x theme -------------
DOMS = DOMAINS
c = collections.Counter((r['m_domain'], scr[r['rec_id']]['theme']) for r in rows)
M = [[c[(d, t)] for t in THEMES] for d in DOMS]
OPS = ['continuous', 'batch', 'not applicable or NR']
co = collections.Counter(((r['operation'] if r['operation'] in ('continuous', 'batch') else 'not applicable or NR'), scr[r['rec_id']]['theme']) for r in rows)
M2 = [[co[(o, t)] for t in THEMES] for o in OPS]
cmap = LinearSegmentedColormap.from_list('blue', ['#f3f7fd', '#9ec5f4', '#3987e5', '#1c5cab'])
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.8, 6.8), gridspec_kw={'height_ratios': [len(DOMS), len(OPS)], 'hspace': 0.12})
vmax = max(max(m) for m in M + M2)
XL = ['Language to\\nMPC or tuning', 'LLM in or\\nabove the loop', 'LLM-facilitated\\nhybrid control', 'SCADA, MCP\\nand OPC', 'Recovery and\\nsafeguards']
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
ax.set_xticks([])
ax2.set_xticks(range(len(THEMES)))
ax2.set_xticklabels(XL, fontsize=8.5)
ax.set_title(f'Tested setups by process type and theme (top) and by operation (bottom), n = {len(rows)}', loc='left', fontsize=11, color=INK, pad=10)
save(fig, 'fig_gap_map')

''' + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print('patched')
