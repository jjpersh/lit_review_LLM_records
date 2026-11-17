"""Stage C patch (2026-11-16): adjacent marker column in the safeguards table of 32_manuscript_tables.py."""
import shutil
p = 'scripts/32_manuscript_tables.py'
shutil.copy(p, 'scripts/32_manuscript_tables.before_stagec.py')
t = open(p, encoding='utf-8').read()
a = """table(['Study', 'Type', 'Safeguard', 'Challenged'],
      [[f"{g[0]['study']} {g[0]['cite']}", t, d, f"{sum(x['C6'] == 'Y' for x in g)} of {len(g)}"]
       for (rid, (t, d)), g in groups.items()])"""
b = """# Stage C (2026-11-16): adjacent marker column; process papers listed before adjacent ones within each type
table(['Study', 'P/A', 'Type', 'Safeguard', 'Challenged'],
      [[f"{g[0]['study']} {g[0]['cite']}", 'P' if g[0]['process'] else 'A', t, d, f"{sum(x['C6'] == 'Y' for x in g)} of {len(g)}"]
       for (rid, (t, d)), g in sorted(groups.items(), key=lambda kv: (kv[1][0]['C6'] != 'Y', kv[0][1][0], not kv[1][0]['process'], kv[1][0]['study']))])
md += ['P process system, A adjacent domain. Challenged: setups in which the safeguard faced bad proposals, of the setups that use it.', '']
psg = [r for r in sg if r['process']]
md += [f'Process systems only: {len(psg)} setups from {len({r["rec_id"] for r in psg})} papers describe a safeguard; challenged in '
       f'{sum(r["C6"] == "Y" for r in psg)} setups from {len({r["rec_id"] for r in psg if r["C6"] == "Y"})} papers.', '']"""
assert a in t
t = t.replace(a, b)
open(p, 'w', encoding='utf-8').write(t)
print('patched')
