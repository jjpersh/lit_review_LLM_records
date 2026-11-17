#!/usr/bin/env python3
"""Second filter on targeted_candidates.csv. Run from lit_review_LLM/. Writes the list to read and the rule outcome."""
import collections
import csv
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
csv.field_size_limit(10**7)
rows = list(csv.DictReader(open('focused_review/targeted_candidates.csv', encoding='utf-8', newline='')))

llm = re.compile(r'large language model|\bLLMs?\b|language model|chatgpt|\bGPT-?\d|agentic', re.I)
domain_out = re.compile(
    r'robot|manipulat|\bvehicle|driving|\bUAVs?\b|drone|aerial|\bdriver|traffic|railway|satellite|spacecraft|'
    r'clinical|patient|medical|health|surgical|cancer|\bdrug\b|protein|\bgenom|molecul|retrosynth|'
    r'HVAC|building|smart home|power (grid|system)|microgrid|\bgrid\b|wireless|\b6G\b|\b5G\b|network slic|'
    r'education|student|legal|finance|stock|cyber ?attack|intrusion|malware|code review|software engineer|'
    r'game|music|speech|image generation|materials? (discovery|design)|crystal structure|perovskite|'
    r'multi-?party computation|model context protocol.*(security|attack|vulnerab)', re.I)
scope = re.compile(
    r'model predictive|\bMPC\b|\bNMPC\b|process control|industrial control|control loop|closed[- ]loop|'
    r'\bPID\b|set-?point|supervisory|controller (selection|switching|tuning|design)|switching control|gain schedul|'
    r'operating (mode|regime|condition)|\bSCADA\b|OPC[ -]?UA|model context protocol|\bDCS\b|distributed control|'
    r'crystalli[sz]|batch (process|control|reactor)|fed-batch|bioreactor|chemical (process|plant)|process plant|'
    r'process (industr|engineering|systems)|distillation|\bCSTR\b|Tennessee Eastman|real-time optimi[sz]ation|'
    r'advanced process control|plant operat|control room|operator', re.I)

keep, c = [], collections.Counter()
for r in rows:
    title, text = r['title'], r['title'] + ' ' + r['abstract']
    if r['prior_decision'] == 'exclude' and not re.search(r'model predictive|\bMPC\b|crystalli[sz]|model context protocol|\bSCADA\b|switch', text, re.I):
        c['excluded earlier, no focus term'] += 1
    elif domain_out.search(title):
        c['out-of-scope domain in title'] += 1
    elif not llm.search(text):
        c['no LLM term'] += 1
    elif not scope.search(text):
        c['no scope term'] += 1
    else:
        c['to read'] += 1
        keep.append(r)
print(c)
print('to read by prior', collections.Counter(r['prior_decision'] or 'new' for r in keep))
for r in keep:
    ab = ' '.join(r['abstract'].split())[:170]
    print(f"{r['tid']} {r['year']} {r['first_author'].split(' ')[-1][:12]} [{r['tags'][:18]}] {r['title'][:105]} :: {ab}")
