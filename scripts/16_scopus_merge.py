#!/usr/bin/env python3
"""Record the 2026-11-09 Scopus searches (run in the user's browser via BYU access) and merge decisions. Run from lit_review_LLM/."""
import collections
import csv

DATE = '2026-11-09'
LLM = '("large language model*" OR LLM* OR "agentic AI")'
LOG = [
    ('SW', f'TITLE-ABS-KEY({LLM} AND ("controller selection" OR "controller switching" OR "switching control" OR "mode switching" OR "supervisory control")) AND PUBYEAR > 2021', 60),
    ('OP', f'TITLE-ABS-KEY({LLM} AND ("model predictive control" OR NMPC OR "advanced process control") AND (operator* OR "natural language" OR tuning OR "human-in-the-loop")) AND PUBYEAR > 2021', 34),
    ('CR', f'TITLE-ABS-KEY({LLM} AND (crystalli* OR "batch process*" OR "pharmaceutical manufacturing") AND (control* OR operator*)) AND PUBYEAR > 2021', 62),
    ('MCP-broad', f'TITLE-ABS-KEY({LLM} AND ("model context protocol" OR SCADA OR "OPC UA") AND (control* OR operator* OR agent*)) AND PUBYEAR > 2021', 603),
    ('MCP', f'TITLE-ABS-KEY({LLM} AND ("model context protocol" OR SCADA OR "OPC UA") AND ("process control" OR "industrial control" OR "control system*" OR "process plant*" OR "process industr*" OR "chemical plant*")) AND PUBYEAR > 2021', 46),
]
NEW = [  # rec_id, tier, priority, theme, reason, adjacent, first_author, year, title, venue, doi, access
    ('SC01', 'core', 1, 'T1', 'Operator language to MPC/controller tuning', 'general MPC, not process', 'Yuya Miyaoka', '2026',
     'Chat-Driven Reconfiguration of Model Predictive Control', 'IEEE Transactions on Control Systems Technology',
     '10.1109/tcst.2026.3695114', 'open access: download in a browser (free)'),
    ('SC02', 'core', 1, 'T2', 'LLM in or above the loop; check at full text whether an LLM computes the moves', '', 'P.N. Arjunan', '2026',
     'Optimizing Refining Energy and Freeness: An AI-Driven Approach to Efficient Papermaking',
     'TAPPICon 2026 / International Control Systems Conference', '', 'not open access: BYU library'),
    ('SC03', 'context', '', '', 'adjacent control method or evidence', '', 'E. Cimenoglu', '2025',
     'Seamless Agentic Commissioning: AI Enhanced Agentic Collaboration in the Loop', 'ELECO 2025', '10.1109/eleco69582.2025.11329273', ''),
]
EXCLUDE_NOTE = ('All other Scopus hits were already in the corpus, already screened in the targeted search, or off-topic '
                '(wind turbines, power grid, robotics, energetic material LLM-105, MOF synthesis, network management).')

screen = list(csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline='')))
if not any(r['rec_id'] == 'SC01' for r in screen):
    fields = list(screen[0])
    for n in NEW:
        rec = dict(zip(['rec_id', 'tier', 'priority', 'theme', 'reason', 'adjacent_domain', 'first_author', 'year', 'title', 'venue', 'doi', 'access'], n))
        rec.update({'screened_on': 'title and abstract', 'pub_status': 'peer-reviewed' if rec['tier'] == 'core' else '', 'pdf': ''})
        if rec['tier'] != 'core':
            rec['access'] = ''
        screen.append(rec)
    rank = {'core': 0, 'context': 1, 'out': 2}
    screen.sort(key=lambda x: (rank[x['tier']], str(x['priority']), x['theme'], x['rec_id']))
    with open('focused_review/screening.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        w.writerows(screen)
    need = list(csv.DictReader(open('focused_review/pdfs_needed.csv', encoding='utf-8', newline='')))
    nf = list(need[0])
    for n in NEW:
        if n[1] == 'core':
            need.append(dict(zip(['rec_id', 'priority', 'theme', 'first_author', 'year', 'title', 'doi', 'venue', 'access'],
                                 [n[0], n[2], n[3], n[6], n[7], n[8], n[10], n[9], n[11]])))
    with open('focused_review/pdfs_needed.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, nf)
        w.writeheader()
        w.writerows(need)
    with open('focused_review/search_log.csv', 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        for tag, q, n in LOG:
            w.writerow([DATE, 'Scopus (BYU access, read from results pages)', tag, q, n, n, 'ok'])
    with open('logs/decisions.md', 'a', encoding='utf-8') as f:
        f.write(f'- {DATE}: Scopus searches run in the user\'s Chrome through BYU access (4 strings; MCP string narrowed from 603 to 46 hits). '
                f'Results read from the results pages, no exports. Added core SC01 (Miyaoka 2026 TCST, ChatMPC) and SC02 (Arjunan 2026, '
                f'closed-loop agentic refiner control, three-month mill study; LLM role to verify at full text); SC03 to context. {EXCLUDE_NOTE}\n')
    s = open('STATUS.md', encoding='utf-8').read()
    s = s.replace('Targeted searches done 2026-11-06.', 'Targeted searches done 2026-11-06; Scopus done 2026-11-09.', 1)
    open('STATUS.md', 'w', encoding='utf-8').write(s)

core = [r for r in screen if r['tier'] == 'core']
print('tiers', collections.Counter(r['tier'] for r in screen))
print('core', len(core), 'P1', sum(str(r['priority']) == '1' for r in core), 'P1 with PDF', sum(bool(r['pdf']) for r in core if str(r['priority']) == '1'))
