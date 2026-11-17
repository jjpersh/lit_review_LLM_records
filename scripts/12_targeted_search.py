#!/usr/bin/env python3
"""Targeted searches for the focused review, plus forward citation chasing from priority-1 core papers.
Run from lit_review_LLM/. Raw responses are cached, so reruns only repeat failed calls."""
import collections
import csv
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

csv.field_size_limit(10**7)
TODAY = datetime.date.today().isoformat()
CACHE = 'logs/raw_search/targeted'
os.makedirs(CACHE, exist_ok=True)
UA = {'User-Agent': 'lit-review-script/1.0'}

LLM = ['large language model', 'large language models', 'LLM', 'LLMs', 'language model', 'ChatGPT', 'GPT-4',
       'agentic AI', 'LLM agent']
Q = {
    'SW1': [['controller selection', 'controller switching', 'switching control', 'mode switching', 'control mode']],
    'SW2': [['gain scheduling', 'multi-mode', 'operating regime', 'operating mode'], ['control', 'controller']],
    'SW3': [['hybrid control', 'hierarchical control', 'supervisory control', 'meta-controller'],
            ['PID', 'MPC', 'reinforcement learning']],
    'SW4': [['control strategy selection', 'controller orchestration', 'adaptive control'], ['process', 'plant']],
    'MCP1': [['SCADA', 'PLC', 'OPC UA', 'industrial', 'process control', 'digital twin'], ['Model Context Protocol']],
    'MCP2': [['SCADA', 'Ignition', 'distributed control system', 'historian'],
             ['agent', 'tool calling', 'tool use', 'function calling']],
    'MCP3': [['OPC UA'], ['agent', 'control', 'operator']],
    'OP1': [['model predictive control', 'MPC', 'NMPC'], ['tuning', 'objective', 'cost function', 'weights', 'parameters']],
    'OP2': [['model predictive control', 'MPC'], ['operator', 'natural language', 'human-in-the-loop', 'interface']],
    'OP3': [['advanced process control', 'real-time optimization'], ['operator', 'engineer', 'tuning']],
    'CR1': [['crystallization', 'crystallisation', 'crystallizer']],
    'CR2': [['batch process', 'batch control', 'fed-batch', 'pharmaceutical manufacturing'], ['control', 'MPC', 'operator']],
    'CR3': [['population balance', 'supersaturation', 'direct nucleation control', 'process analytical technology']],
}

log_rows, hits = [], {}


def norm_title(t):
    return re.sub(r'[^a-z0-9]', '', (t or '').lower())[:120]


def norm_doi(d):
    return re.sub(r'^https?://(dx\.)?doi\.org/', '', (d or '').strip().lower())


def fetch(url, tries=5, wait=4, parse=json.loads):
    key = os.path.join(CACHE, hashlib.md5(url.encode()).hexdigest() + '.txt')
    if os.path.exists(key):
        return parse(open(key, encoding='utf-8').read())
    last = ''
    for k in range(tries):
        try:
            body = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45).read().decode('utf-8')
            open(key, 'w', encoding='utf-8').write(body)
            return parse(body)
        except urllib.error.HTTPError as e:
            last = f'HTTP {e.code}'
            if e.code not in (401, 429, 500, 502, 503, 504):
                break
        except Exception as e:
            last = type(e).__name__
        time.sleep(wait * (2 ** k))
    raise RuntimeError(last or 'failed')


def add(rec, source, tag):
    title = ' '.join((rec.get('title') or '').split())
    if not title:
        return
    doi, arxiv = norm_doi(rec.get('doi')), (rec.get('arxiv') or '').split('v')[0]
    key = doi or ('arxiv:' + arxiv if arxiv else 't:' + norm_title(title))
    h = hits.setdefault(key, {'title': title, 'doi': doi, 'arxiv_id': arxiv, 'year': rec.get('year') or '',
                              'venue': rec.get('venue') or '', 'abstract': '', 'first_author': rec.get('author') or '',
                              'sources': set(), 'tags': set()})
    if len(rec.get('abstract') or '') > len(h['abstract']):
        h['abstract'] = ' '.join(rec['abstract'].split())
    h['sources'].add(source)
    h['tags'].add(tag)


def inverted(inv):
    return ' '.join(w for _, w in sorted((p, w) for w, ps in (inv or {}).items() for p in ps))


def oa_record(w):
    ids = w.get('ids') or {}
    loc = (w.get('primary_location') or {}).get('source') or {}
    au = w.get('authorships') or []
    return {'title': w.get('title'), 'doi': w.get('doi') or ids.get('doi'), 'year': w.get('publication_year'),
            'venue': loc.get('display_name'), 'abstract': inverted(w.get('abstract_inverted_index')),
            'author': au[0]['author']['display_name'] if au else ''}


SELECT = 'id,title,doi,ids,publication_year,primary_location,authorships,abstract_inverted_index'


def openalex(filter_str, tag, label, cap=400):
    cursor, got, total = '*', 0, None
    while cursor and got < cap:
        url = 'https://api.openalex.org/works?' + urllib.parse.urlencode(
            {'filter': filter_str, 'per-page': 200, 'cursor': cursor, 'select': SELECT})
        data = fetch(url)
        total = data['meta']['count']
        for w in data['results']:
            add(oa_record(w), 'OpenAlex', tag)
        got += len(data['results'])
        cursor = data['meta'].get('next_cursor') if data['results'] else None
        time.sleep(0.3)
    log_rows.append({'date': TODAY, 'source': 'OpenAlex', 'tag': tag, 'query': label, 'total_hits': total,
                     'retrieved': got, 'status': 'ok'})


def quote(t):
    return f'"{t}"' if ' ' in t or '-' in t else t


def run_openalex(tag, groups):
    expr = ' AND '.join('(' + ' OR '.join(quote(t) for t in g) + ')' for g in [LLM] + groups)
    openalex(f'title_and_abstract.search:{expr},from_publication_date:2022-01-01', tag, expr)


def parse_atom(body):
    return ET.fromstring(body)


def run_arxiv(tag, groups):
    expr = ' AND '.join('(' + ' OR '.join(f'abs:{quote(t)}' for t in g) + ')' for g in [LLM] + groups)
    url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode(
        {'search_query': expr, 'start': 0, 'max_results': 200, 'sortBy': 'relevance'})
    root = fetch(url, parse=parse_atom)
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    n = 0
    for e in root.findall('a:entry', ns):
        aid = (e.findtext('a:id', '', ns)).rsplit('/abs/', 1)[-1]
        au = e.find('a:author/a:name', ns)
        add({'title': e.findtext('a:title', '', ns), 'arxiv': aid, 'year': e.findtext('a:published', '', ns)[:4],
             'venue': 'arXiv', 'abstract': e.findtext('a:summary', '', ns), 'author': au.text if au is not None else ''},
            'arXiv', tag)
        n += 1
    log_rows.append({'date': TODAY, 'source': 'arXiv', 'tag': tag, 'query': expr, 'total_hits': n, 'retrieved': n, 'status': 'ok'})
    time.sleep(3.1)


def s2_record(p):
    ext = p.get('externalIds') or {}
    au = p.get('authors') or []
    return {'title': p.get('title'), 'doi': ext.get('DOI'), 'arxiv': ext.get('ArXiv'), 'year': p.get('year'),
            'venue': p.get('venue'), 'abstract': p.get('abstract'), 'author': au[0].get('name', '') if au else ''}


def run_s2(tag, groups):
    expr = ' + '.join('(' + ' | '.join(f'"{t}"' for t in g) + ')' for g in [LLM] + groups)
    url = 'https://api.semanticscholar.org/graph/v1/paper/search/bulk?' + urllib.parse.urlencode(
        {'query': expr, 'year': '2022-', 'fields': 'title,externalIds,year,venue,abstract,authors'})
    data = fetch(url, tries=4, wait=12)
    rows = data.get('data') or []
    for p in rows:
        add(s2_record(p), 'Semantic Scholar', tag)
    log_rows.append({'date': TODAY, 'source': 'Semantic Scholar', 'tag': tag, 'query': expr, 'total_hits': data.get('total'),
                     'retrieved': len(rows), 'status': 'ok'})
    time.sleep(2)


def guarded(fn, source, tag, *args):
    try:
        fn(tag, *args)
        return True
    except Exception as e:
        log_rows.append({'date': TODAY, 'source': source, 'tag': tag, 'query': '', 'total_hits': '', 'retrieved': 0,
                         'status': f'FAILED: {e}'})
        print('FAILED', source, tag, e, flush=True)
        return False


for tag, groups in Q.items():
    guarded(run_openalex, 'OpenAlex', tag, groups)
    guarded(run_arxiv, 'arXiv', tag, groups)
print('keyword searches: OpenAlex and arXiv done', len(hits), flush=True)

s2_ok = 0
for tag, groups in Q.items():
    if guarded(run_s2, 'Semantic Scholar', tag, groups):
        s2_ok += 1
    elif s2_ok == 0 and tag == 'SW3':
        print('Semantic Scholar unavailable; stopping those calls', flush=True)
        break
print('Semantic Scholar queries ok', s2_ok, 'total', len(hits), flush=True)

# Forward citations from priority-1 core papers
core = [r for r in csv.DictReader(open('focused_review/screening.csv', encoding='utf-8', newline=''))
        if r['tier'] == 'core' and r['priority'] == '1']
meta = {r['rec_id']: r for r in csv.DictReader(open('corpus/metadata.csv', encoding='utf-8', newline=''))}
for c in core:
    rid = c['rec_id']
    wid = meta[rid].get('openalex_id', '').rsplit('/', 1)[-1]
    tag = 'CITE:' + rid
    try:
        if not wid and c['doi']:
            wid = fetch('https://api.openalex.org/works/doi:' + urllib.parse.quote(c['doi'], safe='/'), tries=2)['id'].rsplit('/', 1)[-1]
        if not wid:
            res = fetch('https://api.openalex.org/works?' + urllib.parse.urlencode(
                {'filter': 'title.search:' + re.sub(r'[,:|]', ' ', c['title'])[:150], 'per-page': 3}), tries=2)['results']
            match = [w for w in res if norm_title(w.get('title')) == norm_title(c['title'])]
            wid = match[0]['id'].rsplit('/', 1)[-1] if match else ''
        if not wid:
            log_rows.append({'date': TODAY, 'source': 'OpenAlex citations', 'tag': tag, 'query': c['title'][:80], 'total_hits': '',
                             'retrieved': 0, 'status': 'FAILED: no OpenAlex id'})
            continue
        openalex(f'cites:{wid}', tag, f'forward citations of {rid} ({wid})', cap=600)
    except Exception as e:
        log_rows.append({'date': TODAY, 'source': 'OpenAlex citations', 'tag': tag, 'query': c['title'][:80], 'total_hits': '',
                         'retrieved': 0, 'status': f'FAILED: {e}'})
print('citation chase done', len(hits), flush=True)

# Compare against the corpus and earlier screening decisions
corpus_doi, corpus_arxiv, corpus_title = set(), set(), set()
for r in meta.values():
    for d in [r['doi']] + re.split(r'[;|,\s]+', r.get('other_version_dois') or ''):
        if norm_doi(d):
            corpus_doi.add(norm_doi(d))
    for a in [r.get('arxiv_id')] + re.split(r'[;|,\s]+', r.get('other_arxiv_ids') or ''):
        if a:
            corpus_arxiv.add(a.split('v')[0])
    corpus_title.add(norm_title(r['title']))
prior = {}
for r in csv.DictReader(open('corpus/new_screening.csv', encoding='utf-8', newline='')):
    val = r['decision'] or r['prefilter'] or 'seen'
    if r['doi']:
        prior[norm_doi(r['doi'])] = val
    prior[norm_title(r['title'])] = val

llm_rx = re.compile(r'large language model|\bLLMs?\b|language model|chatgpt|\bGPT-?\d|agentic|foundation model', re.I)
ctl_rx = re.compile(r'control|\bMPC\b|\bNMPC\b|\bSCADA\b|\bPLC\b|OPC[ -]?UA|setpoint|set-point|crystalli[sz]|operator|batch', re.I)
out, counts = [], collections.Counter()
for h in hits.values():
    counts['retrieved'] += 1
    if h['doi'] in corpus_doi or h['arxiv_id'] in corpus_arxiv or norm_title(h['title']) in corpus_title:
        counts['already in corpus'] += 1
        continue
    text = h['title'] + ' ' + h['abstract']
    if not llm_rx.search(text) or not ctl_rx.search(text):
        counts['no LLM and control terms'] += 1
        continue
    try:
        if int(h['year']) < 2022:
            counts['before 2022'] += 1
            continue
    except (TypeError, ValueError):
        pass
    counts['to judge'] += 1
    out.append({**h, 'sources': ';'.join(sorted(h['sources'])), 'tags': ';'.join(sorted(h['tags'])),
                'prior_decision': prior.get(h['doi']) or prior.get(norm_title(h['title'])) or ''})
out.sort(key=lambda x: (x['tags'].startswith('CITE'), x['tags'], x['title']))
for i, r in enumerate(out, 1):
    r['tid'] = f'T{i:04d}'
cols = ['tid', 'title', 'first_author', 'year', 'venue', 'doi', 'arxiv_id', 'tags', 'sources', 'prior_decision', 'abstract']
with open('focused_review/targeted_candidates.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, cols, extrasaction='ignore')
    w.writeheader()
    w.writerows(out)
with open('focused_review/search_log.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, ['date', 'source', 'tag', 'query', 'total_hits', 'retrieved', 'status'])
    w.writeheader()
    w.writerows(log_rows)
print(counts)
print('prior decisions among to-judge', collections.Counter(r['prior_decision'] or 'new' for r in out).most_common())
print('log', collections.Counter((r['source'], r['status'][:6]) for r in log_rows))
print('abstract chars', sum(len(r['abstract']) for r in out))
