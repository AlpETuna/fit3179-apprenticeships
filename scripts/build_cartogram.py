"""Non-contiguous area cartogram from actual ABS outlines.
Project to spherical Albers equal-area coordinates before uniform per-state scaling.
One common area-per-contract constant applies to all eight shapes, including ACT.
ACT alone is translated east for legibility; no state is given a minimum area.
"""
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'dist'
rad=math.radians
p1,p2,p0=map(rad,[-18,-36,-27]);n=(math.sin(p1)+math.sin(p2))/2;c=math.cos(p1)**2+2*n*math.sin(p1);rho0=math.sqrt(c-2*n*math.sin(p0))/n

def project(p):
 lon,lat=map(rad,p);rho=math.sqrt(c-2*n*math.sin(lat))/n;theta=n*(lon-rad(134))
 return [6371*rho*math.sin(theta),6371*(rho0-rho*math.cos(theta))]
def ringstats(r):
 cross=[a[0]*b[1]-b[0]*a[1] for a,b in zip(r,r[1:])];area=sum(cross)/2
 return abs(area),[sum((a[i]+b[i])*k for a,b,k in zip(r,r[1:],cross))/(6*area) for i in [0,1]]
def stats(polys):
 parts=[ringstats(p[0]) for p in polys];a=sum(v[0] for v in parts)
 return a,[sum(v[0]*v[1][i] for v in parts)/a for i in [0,1]]
rows={r['State']:r for r in json.loads((R/'data/states.json').read_text())};features=json.loads((R/'data/abs-states-simplified.geojson').read_text())['features'];prepared=[]
for f in features:
 polys=[[[project(p) for p in ring] for ring in poly] for poly in f['geometry']['coordinates']];area,center=stats(polys)
 prepared.append((f['properties']['State'],polys,area,center))
nsw=next(p for p in prepared if p[0]=='New South Wales');unit=.49*nsw[2]/rows[nsw[0]]['Contracts']
back=[];front=[];labels=[];leaders=[]
for state,polys,area,center in prepared:
 row=rows[state];scale=math.sqrt(unit*row['Contracts']/area);target=center[:]
 if row['Short']=='ACT':target=project([156,-37])
 transformed=[[[[round(target[0]+(p[0]-center[0])*scale,3),round(target[1]+(p[1]-center[1])*scale,3)] for p in ring] for ring in poly] for poly in polys]
 shapearea,_=stats(transformed);assert abs(shapearea/unit-row['Contracts'])/row['Contracts']<.0001
 back.append({'type':'Feature','properties':{'State':state},'geometry':{'type':'MultiPolygon','coordinates':polys}})
 front.append({'type':'Feature','properties':{**row,'AreaPerContract':unit,'LinearScale':scale},'geometry':{'type':'MultiPolygon','coordinates':transformed}})
 x,y=target;dy=0
 if row['Short']=='NT':dy=150
 if row['Short']=='TAS':dy=-170
 if row['Short']=='ACT':dy=-210;leaders.append({'x':center[0],'y':center[1],'x2':target[0],'y2':target[1]})
 if dy:leaders.append({'x':x,'y':y,'x2':x,'y2':y+dy*.65})
 labels.append({**row,'x':round(x,3),'y':round(y+dy,3),'External':bool(dy)})
for name,obj in [('cartogram-reference.geojson',{'type':'FeatureCollection','features':back}),('cartogram-contracts.geojson',{'type':'FeatureCollection','features':front}),('cartogram-labels.json',labels),('cartogram-leaders.json',leaders)]:
 (R/'data'/name).write_text(json.dumps(obj,separators=(',',':'))+'\n')
q=lambda f:dict(field=f,type='quantitative')
s={'$schema':'https://vega.github.io/schema/vega-lite/v6.json','description':'Non-contiguous area cartogram: actual ABS state shapes are uniformly resized in Albers equal-area coordinates so their displayed areas are proportional to December 2025 active contracts. Faint outlines retain actual geography. ACT is moved east, at the same area scale, with a leader to its location. Colour shows 2024–2025 percentage change.','height':470,'params':[{'name':'focusState','value':'All'}],'projection':{'type':'identity','reflectY':True},'layer':[]}
data=lambda name:{'url':'data/'+name,'format':{'type':'json','property':'features'}}
s['layer'].append({'data':data('cartogram-reference.geojson'),'mark':{'type':'geoshape','fill':'#f5f7f9','stroke':'#b8c8d3','strokeWidth':.8}})
s['layer'].append({'data':{'url':'data/cartogram-leaders.json'},'mark':{'type':'rule','color':'#506172','strokeWidth':1,'strokeDash':[3,3]},'encoding':{'longitude':q('x'),'latitude':q('y'),'longitude2':{'field':'x2'},'latitude2':{'field':'y2'}}})
s['layer'].append({'data':data('cartogram-contracts.geojson'),'mark':{'type':'geoshape','stroke':'white','strokeWidth':1},'encoding':{'color':{**q('properties.Change'),'scale':{'domain':[-20,0],'range':['#9a381a','#fbe7db']},'legend':{'title':'Change in active contracts (%)','orient':'bottom','gradientLength':220}},'stroke':{'condition':{'test':'datum.properties.State === focusState','value':'#132a40'},'value':'white'},'strokeWidth':{'condition':{'test':'datum.properties.State === focusState','value':3},'value':1},'tooltip':[{'field':'properties.State','title':'State / territory'},{'field':'properties.Contracts','type':'quantitative','format':',','title':'2025 active contracts'},{'field':'properties.Change','type':'quantitative','format':'.1f','title':'2024–2025 change (%)'}]}})
s['layer'].append({'data':{'url':'data/cartogram-labels.json'},'mark':{'type':'text','fontSize':12,'fontWeight':700},'encoding':{'longitude':q('x'),'latitude':q('y'),'text':{'field':'Short'},'color':{'condition':{'test':'datum.Change < -10 && !datum.External','value':'white'},'value':'#132a40'}}})
(R/'specs/05-cartogram.json').write_text(json.dumps(s,indent=2)+'\n')
print('Created geographic cartogram; common area per contract:',round(unit,4))
