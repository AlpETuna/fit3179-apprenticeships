"""Check cartogram area encoding and that coloured state polygons do not overlap."""
import itertools,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'dist/data'
fs=json.loads((R/'cartogram-contracts.geojson').read_text())['features']
rows={r['State']:r for r in json.loads((R/'states.json').read_text())}
assert len(fs)==8 and {f['properties']['State'] for f in fs}==set(rows)
def area(p):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]))/2)
def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def bounds(p):return min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p)
def touch(a,b):return not(a[2]<b[0] or b[2]<a[0] or a[3]<b[1] or b[3]<a[1])
def inside(p,ring):
 x,y=p;result=False
 for a,b in zip(ring,ring[1:]):
  if (a[1]>y)!=(b[1]>y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:result=not result
 return result
units=[]
for f in fs:
 p=f['properties'];a=sum(area(poly[0]) for poly in f['geometry']['coordinates']);units.append(a/rows[p['State']]['Contracts'])
assert max(units)/min(units)-1<.0001,'Area proportions changed'
for a,b in itertools.combinations(fs,2):
 for pa in a['geometry']['coordinates']:
  for pb in b['geometry']['coordinates']:
   p,q=pa[0],pb[0]
   if not touch(bounds(p),bounds(q)):continue
   message='Overlapping coloured shapes: '+a['properties']['Short']+' / '+b['properties']['Short']
   assert not inside(p[0],q) and not inside(q[0],p),message
   for x,y in zip(p,p[1:]):
    for u,v in zip(q,q[1:]):
     assert not(orient(x,y,u)*orient(x,y,v)<0 and orient(u,v,x)*orient(u,v,y)<0),message
print('PASS: eight geographic cartogram areas proportional to contracts; no overlapping coloured state polygons.')
