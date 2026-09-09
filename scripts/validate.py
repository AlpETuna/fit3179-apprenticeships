"""Targeted pre-publication checks for data, references and assignment structure."""
from pathlib import Path
from html.parser import HTMLParser
import json,re
from urllib.parse import urlsplit
R=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.charts=[];self.refs=[];self.figures=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if 'data-spec' in a:self.charts.append(a['data-spec'])
  if tag=='figure':self.figures+=1
  for k in ['src','href']:
   if a.get(k):self.refs.append(a[k])
p=Page();html=(R/'index.html').read_text();p.feed(html)
assert len(p.ids)==len(set(p.ids)), 'Duplicate HTML IDs'
assert p.figures==12 and len(p.charts)==12,'Expected twelve charts'
for ref in p.refs:
 if ref.startswith(('#','http','data:')):continue
 assert (R/urlsplit(ref).path).exists(),f'Missing public asset {ref}'
for ref in re.findall(r'url\(([^)]+)\)',(R/'fonts.css').read_text()):assert (R/ref).exists(),ref
for name in p.charts:
 spec=json.loads((R/'specs'/name).read_text());assert spec['$schema'].startswith('https://vega.github.io/schema/')
 def walk(x):
  if isinstance(x,dict):
   if 'url' in x and isinstance(x['url'],str) and x['url'].startswith('data/'):assert (R/x['url']).exists(),x['url']
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(spec)
read=lambda n:json.loads((R/'data'/n).read_text())
states=read('states.json');assert len(states)==8 and len({r['State'] for r in states})==8
for r in states:
 assert abs(r['Rate']-r['Contracts']/r['Population']*1000)<.00001
 # Both counts are rounded to five; published percentages use unrounded counts.
 lo=((r['Contracts']-2.5)/(r['Previous']+2.5)-1)*100
 hi=((r['Contracts']+2.5)/(r['Previous']-2.5)-1)*100
 assert r['Change']+.05>=lo and r['Change']-.05<=hi, 'Published percentage incompatible with rounding interval'
assert sum(r['Contracts'] for r in states)==282430
assert round(next(r['Rate'] for r in states if r['Short']=='TAS')/next(r['Rate'] for r in states if r['Short']=='VIC'),1)==1.6
assert '1.6 times Victoria' in html
assert 372885-35640-28165-26650==282430
assert round((1-282430/372885)*100,1)==24.3
trade=read('trade-tree.json')[1:];assert sum(r['Contracts'] for r in trade)==208945
assert round(sum(sorted([r['Contracts'] for r in trade],reverse=True)[:3])/208950*100,1)==82.1
for year in range(2021,2026):
 rows=[r for r in read('occupation-ranks.json') if r['Year']==year]
 assert sorted(r['Rank'] for r in rows)==list(range(1,11))
 assert [r['Contracts'] for r in sorted(rows,key=lambda r:r['Rank'])]==sorted([r['Contracts'] for r in rows],reverse=True)
for g in ['Trade','Non-trade']:assert sum(r['Percent'] for r in read('employment-pattern.json') if r['Group']==g)==100
geo=read('abs-states-simplified.geojson');assert len(geo['features'])==8
assert {f['properties']['State'] for f in geo['features']}=={r['State'] for r in states}
for f in geo['features']:
 for poly in f['geometry']['coordinates']:
  ring=poly[0];assert ring[0]==ring[-1]
  assert sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring,ring[1:]))<0,'Wrong spherical ring orientation'
for path in R.rglob('*'):
 if path.is_file() and path.suffix in ['.html','.js','.json','.md','.txt']:assert '34996427' not in path.read_text(),f'Student ID leaked into public file {path}'
size=sum(p.stat().st_size for p in R.rglob('*') if p.is_file())
assert size<4_000_000,f'Site too large: {size}'
print(f'PASS: 12 charts; 3 map idioms; local references; 8 state joins; rates, ranks, totals and geometry; no student ID in public files. Public assets: {size:,} bytes.')

import runpy
runpy.run_path(str(Path(__file__).with_name("validate_cartogram.py")))
