#!/usr/bin/env python3
"""Claim-audit inputs (revision run 2026-11-12, step A3).
For each graded paper, collect every paragraph or table row of draft_v1's master copy (manuscript_keys.md)
that cites the paper or names its first author, with the section heading. Output: draft/_work/audit_input/<rec_id>.md"""
import os
import re

KEYS = {
    'Pershing2026HumanLoop': ('S262', 'Pershing'), 'Vyas2025AutonomousIndustrial': ('S038', 'Vyas and Mercang'),
    'Vyas2025AutonomousControl': ('S037', 'Vyas and Mercang'), 'Wen2026Risks': ('S203', 'Wen'), 'Arif2025Agentic': ('T1042', 'Arif'),
    'Rasheed2025LLMControl': ('S042', 'Rasheed'), 'Hofmann2025BeyondTouch': ('S282', 'Hofmann'),
    'HidalgoCastelo2026Local': ('S028', 'Hidalgo'), 'GonzalezPotes2026Hybrid': ('S156', 'González'),
    'Lima2026Specialized': ('S180', 'Lima'), 'Zhang2025Operating': ('S041', 'Zhang'),
    'Papacharalampopoulos2026Cognitive': ('S020', 'Papacharalampopoulos'), 'Krishna2026LEMCA': ('T0779', 'Krishna'),
    'Rosenthal2026SafetyGated': ('S032', 'Rosenthal'), 'Schall2026Safe': ('S030', 'Schall'),
    'Naagarajan2025Greenhouse': ('T0665', 'Naagarajan'), 'Shu2026Numbers': ('S195', 'Shu'),
    'Shou2026PhysicsInformed': ('S002', 'Shou'), 'Chen2026Benchmarking': ('S193', 'Chen'),
    'LunaRueda2026Workflow': ('S004', 'Luna Rueda'), 'Narimani2025AgenticControl': ('S007', 'Narimani'),
    'Tohma2025SmartControl': ('S013', 'Tohma'), 'Wu2025InstructMPC': ('T0532', 'InstructMPC'),
    'Miyaoka2026Agentic': ('S272', 'Agentic MPC'), 'IbanezEspinel2026Generative': ('S178', 'Ibáñez'),
    'Nozari2026SafetyAware': ('S016', 'Nozari'), 'Vyas2026Detection': ('S022', 'Vyas et al'),
    'Khan2026PVC': ('T1046', 'Khan'), 'RojasOrdonez2025Relay': ('S048', 'Rojas'),
    'Nogueira2026Systematic': ('S017', 'Nogueira'), 'Nerantzis2026Sensor': ('S315', 'Nerantzis'),
    'Smidl2026Drive': ('T1053', 'Šmídl'),
}
src = open('draft_v1/_work/manuscript_keys.md', encoding='utf-8').read() if os.path.exists('draft_v1/_work/manuscript_keys.md') \
    else open('draft/_work/manuscript_keys.md', encoding='utf-8').read()
os.makedirs('draft/_work/audit_input', exist_ok=True)
blocks, sec = [], ''
for para in re.split(r'\n\s*\n', src):
    for line in para.split('\n'):
        if line.startswith('#'):
            sec = line.strip('# ').strip()
    if para.lstrip().startswith('|'):
        blocks += [(sec, ln) for ln in para.split('\n') if ln.startswith('| ') and '---' not in ln]
    else:
        blocks.append((sec, para))
by = {}
for key, (rid, name) in KEYS.items():
    hits = [(s, b) for s, b in blocks if f'@{key}' in b or (name in b and not b.startswith('#'))]
    by.setdefault(rid, []).extend(h for h in hits if h not in by.get(rid, []))
for rid, hits in by.items():
    with open(f'draft/_work/audit_input/{rid}.md', 'w', encoding='utf-8') as f:
        f.write(f'# First-draft passages that mention {rid}\n\n')
        for i, (s, b) in enumerate(hits, 1):
            f.write(f'## Passage {i} (Section: {s})\n\n{b.strip()}\n\n')
    print(rid, len(hits))
