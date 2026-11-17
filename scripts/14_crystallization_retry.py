#!/usr/bin/env python3
"""Rerun the OpenAlex crystallization query slowly, keep process-related hits, and retry failed Semantic Scholar queries.
Run from lit_review_LLM/. Prints candidates not already in the corpus or targeted_candidates.csv."""
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

csv.field_size_limit(10**7)
UA = {'User-Agent': 'lit-review-script/1.0'}
SELECT = 'id,title,doi,publication_year,primary_location,authorships,abstract_inverted_index'
norm = lambda t: re.sub(r'[^a-z0-9]', '', (t or '').lower())[:120]
doi_n = lambda d: re.sub(r'^https?://(dx\.)?doi\.org/', '', (d or '').lower())


def get(url, tries=5):
    for k in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45))
        except urllib.error.HTTPError as e:
            print('  retry', e.code, flush=True)
            time.sleep(5 * (k + 1))
    return None


inv = lambda d: ' '.join(w for _, w in sorted((p, w) for w, ps in (d or {}).items() for p in ps))
base = ('title_and_abstract.search:("large language model" OR "large language models" OR LLM OR LLMs OR "language model" '
        'OR ChatGPT OR "GPT-4" OR "agentic AI" OR "LLM agent") AND (crystallization OR crystallisation OR crystallizer),'
        'from_publication_date:2022-01-01')
found, page, total = [], 1, None
while True:
    d = get('https://api.openalex.org/works?' + urllib.parse.urlencode({'filter': base, 'per-page': 100, 'page': page, 'select': SELECT}))
    if not d:
        print('OPENALEX FAILED at page', page)
        break
    total = d['meta']['count']
    for w in d['results']:
        loc = (w.get('primary_location') or {}).get('source') or {}
        au = w.get('authorships') or []
        found.append({'title': ' '.join((w.get('title') or '').split()), 'doi': doi_n(w.get('doi')), 'year': w.get('publication_year'),
                      'venue': loc.get('display_name') or '', 'abstract': ' '.join(inv(w.get('abstract_inverted_index')).split()),
                      'first_author': au[0]['author']['display_name'] if au else ''})
    if page * 100 >= total or not d['results']:
        break
    page += 1
    time.sleep(2)
print('OpenAlex CR1 total', total, 'retrieved', len(found))

corpus = list(csv.DictReader(open('corpus/metadata.csv', encoding='utf-8', newline='')))
seen_d = {doi_n(r['doi']) for r in corpus if r['doi']}
seen_t = {norm(r['title']) for r in corpus}
tc = list(csv.DictReader(open('focused_review/targeted_candidates.csv', encoding='utf-8', newline='')))
seen_d |= {doi_n(r['doi']) for r in tc if r['doi']}
seen_t |= {norm(r['title']) for r in tc}
proc = re.compile(r'crystalli[sz]er|cooling crystalli|antisolvent|supersaturat|nucleation|process (control|model|development|design|analytical)|'
                  r'pharmaceutical|\bAPI\b|batch|polymorph|solubility|population balance|industrial', re.I)
new = [f for f in found if f['doi'] not in seen_d and norm(f['title']) not in seen_t]
keep = [f for f in new if re.search(r'crystalli[sz]', f['title'] + f['abstract'], re.I) and proc.search(f['title'] + ' ' + f['abstract'])]
print('new', len(new), 'process-related', len(keep))
with open('focused_review/crystallization_extra.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, ['title', 'first_author', 'year', 'venue', 'doi', 'abstract'])
    w.writeheader()
    w.writerows(keep)
for k in keep:
    print(f"- {k['first_author'].split(' ')[-1][:14]} {k['year']} {k['title'][:115]} :: {k['abstract'][:150]}")
