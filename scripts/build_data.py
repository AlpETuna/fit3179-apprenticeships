"""Published NCVER chart/table values, transcribed from the official December 2025 release.
No simulated records. See dist/data/README.md for figure references and transformations.
Run from site/: python3 scripts/build_data.py
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]/'dist'
def save(name,rows): (ROOT/'data'/name).write_text(json.dumps(rows,indent=2)+'\n')
state_names=['New South Wales','Victoria','Queensland','South Australia','Western Australia','Tasmania','Northern Territory','Australian Capital Territory']
short=['NSW','VIC','QLD','SA','WA','TAS','NT','ACT']
counts=[[107100,111645,100725,90630,84340],[73350,77495,70930,64400,57015],[80440,90450,81820,76375,69925],[24915,28040,23845,22130,21235],[40385,44060,40950,38880,35760],[11100,11475,10220,8970,7375],[3220,3160,3240,3170,3035],[7150,6550,5515,4525,3745]]
pop=[8641100,7121900,5712100,1910600,3076500,579100,267500,487200]
# Cartographic label/symbol anchors, not the locations of contracts.
anchors=[[146,-32],[144.5,-37],[144,-22.5],[135.5,-30],[122,-25],[146.5,-42],[133.5,-19.5],[149.1,-35.4]]
tiles=[[3,2],[3,3],[3,1],[2,2],[1,2],[3,4],[2,1],[4,3]]
changes=[-6.9,-11.5,-8.4,-4.1,-8,-17.8,-4.4,-17.3]
states=[]
for i,name in enumerate(state_names):
 states.append(dict(State=name,Code=str(i+1),Short=short[i],Contracts=counts[i][-1],Previous=counts[i][-2],Population=pop[i],Rate=round(counts[i][-1]/pop[i]*1000,5),Change=changes[i],Longitude=anchors[i][0],Latitude=anchors[i][1],Column=tiles[i][0],Row=tiles[i][1]))
save('states.json',states)
save('state-history.json',[dict(State=n,Year=2021+j,Contracts=v) for n,vs in zip(state_names,counts) for j,v in enumerate(vs)])
save('population.json',[dict(State=n,Year=2025,Population=p,Unit='persons; published in thousands to one decimal') for n,p in zip(state_names,pop)])
trade=[('Automotive & engineering','Automotive and Engineering Trades Workers',[53575,56980,60460,61000,58350]),('Construction','Construction Trades Workers',[65565,66795,67140,63610,59355]),('Electrical & telecoms','Electrotechnology and Telecommunications Trades Workers',[47475,50795,53175,54685,53845]),('Engineering, ICT & science','Engineering, ICT and Science Technicians',[8440,10050,6650,5720,5145]),('Food trades','Food Trades Workers',[12810,13745,11955,11230,9970]),('Other technicians & trades','Other Technicians and Trades Workers',[19230,19720,17595,15840,14330]),('Animal, agricultural & horticultural','Skilled Animal, Agricultural and Horticultural Workers',[9730,9960,9165,8370,7950])]
non=[('Clerical & administrative','Clerical and Administrative Workers',[35995,40565,21665,13010,10155]),('Community & personal service','Community and Personal Service Workers',[39335,43855,44240,40405,35915]),('Labourers','Labourers',[13225,13285,10790,9710,8350]),('Machinery operators & drivers','Machinery Operators and Drivers',[14710,16710,15270,13565,11555]),('Managers','Managers',[5120,4275,2355,1320,980]),('Professionals','Professionals',[2365,3525,2210,1170,955]),('Sales workers','Sales Workers',[19985,22525,14555,9425,5570])]
occupations=[]
for group,items in [('Trade',trade),('Non-trade',non)]:
 for label,full,vs in items:
  for j,v in enumerate(vs):occupations.append(dict(Group=group,Occupation=label,FullName=full,Year=2021+j,Contracts=v,ChangeFrom2021=round((v/vs[0]-1)*100,3)))
save('occupations.json',occupations)
# Leaf sums differ slightly from published trade total through independent rounding.
save('trade-tree.json',[dict(id='root',parent=None,Occupation='All shown trade groups',Contracts=0,Label=[])] + [dict(id=str(i),parent='root',Occupation=label,FullName=full,Contracts=vs[-1],Label=label.replace(' & ',' &|').replace(' technicians ','|technicians ').split('|')) for i,(label,full,vs) in enumerate(trade)])
top=[('Child carers',[14390,15975,21225,21175,18820]),('Earthmoving plant operators',[5505,5650,5520,5490,4895]),('Hospitality workers (nfd)',[11235,11180,7995,6055,4620]),('Aged & disabled carers',[505,910,2850,4185,3770]),('General clerks',[14290,15980,8185,5280,3735]),('Drillers, miners & shot firers',[3605,4750,4025,2805,2370]),('Real estate sales agents',[5020,6510,4205,2800,2175]),('Truck drivers',[2680,3175,3065,2795,2145]),('Welfare support workers',[2375,2835,2220,1745,2125]),('Purchasing & supply clerks',[5165,5770,3685,2330,2050])]
rank=[]
for j in range(5):
 order=sorted(top,key=lambda row:row[1][j],reverse=True)
 for i,(name,vs) in enumerate(order):rank.append(dict(Occupation=name,Year=2021+j,Contracts=vs[j],Rank=i+1))
save('occupation-ranks.json',rank)
cohorts=[('People with disability',[9340,11095,11110,10900,10695]),('Indigenous Australians',[18585,20585,20535,19840,19170]),('Language other than English',[35180,39765,33115,29380,26635]),('Females',[98355,110350,92540,79175,69440]),('Regional & remote',[129310,137490,129490,121235,111875])]
save('cohorts.json',[dict(Cohort=n,Year=2021+j,Contracts=v,Share=round(v/t*100,3)) for n,vs in cohorts for j,(v,t) in enumerate(zip(vs,[347660,372885,337245,309080,282430]))])
save('cohort-change.json',[dict(Cohort=n,Before=vs[3],After=vs[4],Change=round((vs[4]/vs[3]-1)*100,1)) for n,vs in cohorts])
save('annual-activity.json',[dict(Activity=a,Group=g,Contracts=v) for a,ts in [('Commencements',[76585,59715]),('Recommencements',[22885,5490]),('Completions',[53390,42670]),('Cancellations / withdrawals',[52380,33035])] for g,v in zip(['Trade','Non-trade'],ts)])
save('employment-pattern.json',[dict(Group=g,Contracts=total,Arrangement=arr,Percent=p) for g,total,parts in [('Trade',208950,[92.0,8.0]),('Non-trade',73475,[55.7,44.3])] for arr,p in zip(['Full-time','Part-time'],parts)])
save('national-total.json',[dict(Year=2016+i,Contracts=v) for i,v in enumerate([263960,261660,262740,259785,297670,347660,372885,337245,309080,282430])])
save('national-series.json',json.loads((ROOT/'specs/01-trend.json').read_text())['data']['values'])
print('Saved auditable data tables')
