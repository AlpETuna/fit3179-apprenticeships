'use strict';
const theme={background:'transparent',font:'Source Sans 3',view:{stroke:null},axis:{labelFontSize:14,titleFontSize:14,labelColor:'#506172',titleColor:'#506172',titleFontWeight:400,gridColor:'#e6ecf0',domain:false,ticks:false,labelPadding:10,titlePadding:14},legend:{labelFontSize:14,titleFontSize:14,labelColor:'#132a40',titleColor:'#132a40',orient:'top',symbolType:'stroke',padding:8},text:{font:'Source Sans 3',fontSize:14,color:'#132a40'}};
const views=new Map(), specs=new Map(), dataCache=new Map();
const settings={focusState:'All',occupationGroup:'All',rankFocus:'Aged & disabled carers',cohortFocus:'Females'};
const nf=new Intl.NumberFormat('en-AU');
async function getData(name){if(!dataCache.has(name)){dataCache.set(name,fetch('data/'+name).then(r=>{if(!r.ok)throw new Error('Data unavailable');return r.json();}));}return dataCache.get(name);}
async function renderChart(el){
 try{
  if(!specs.has(el.dataset.spec)){const r=await fetch('specs/'+el.dataset.spec);if(!r.ok)throw new Error('Chart specification unavailable');specs.set(el.dataset.spec,await r.json());}
  const spec=structuredClone(specs.get(el.dataset.spec));
  const w=Math.max(230,Math.floor(el.clientWidth));const narrow=w<500;const small=w<380;
  spec.config={...theme,...spec.config};
  spec.width=w;spec.autosize={type:'fit',contains:'padding'};
  if(spec.$schema.includes('vega-lite')){
   if(spec.params)spec.params.forEach(p=>{if(p.name in settings)p.value=settings[p.name];});
   if(['choropleth','symbols'].includes(el.id)){spec.height=small?355:420;}
   if(el.id==='heatmap'){
    spec.encoding.y.axis.labelLimit=small?115:narrow?190:280;
    spec.encoding.y.axis.labelFontSize=small?11:13;
    spec.height=settings.occupationGroup==='All'?480:280;
   }
   if(el.id==='cohort-change'){
    spec.encoding.y.axis.labelLimit=narrow?120:210;
    spec.encoding.y.axis.labelFontSize=small?11:13;
    if(small){spec.layer[3].mark.dx=7;spec.layer[3].mark.align='left';spec.layer[3].mark.dy=-12;}
   }
   if(el.id==='waterfall'){
    spec.layer[0].mark.size=small?32:narrow?50:70;
    spec.encoding.x.axis.labelAngle=narrow?-30:0;
    if(small)spec.layer[1].mark.fontSize=11;
   }
   if(el.id==='activity'){spec.encoding.y.axis.labelLimit=narrow?145:230;if(small)spec.encoding.y.axis.labelFontSize=11;}
   if(['heatmap','cohort-change','activity'].includes(el.id)){spec.encoding.y.axis.minExtent=spec.encoding.y.axis.labelLimit+12;spec.encoding.y.axis.maxExtent=spec.encoding.y.axis.labelLimit+12;}
   if(el.id==='mosaic'&&narrow){spec.layer[1].mark.fontSize=small?10:12;spec.transform[5].calculate="format(datum.Percent, '.1f') + '%'";}
   if(el.id==='waffle')spec.height=Math.round(w/4);
  }else if(el.id==='treemap'){spec.height=narrow?440:360;}
  const prior=views.get(el.id);if(prior)prior.finalize();
  const result=await vegaEmbed(el,spec,{actions:false,renderer:'svg'});views.set(el.id,result.view);
  el.dataset.loaded='true';delete el.dataset.error;el.dataset.renderWidth=String(w);
 }catch(e){el.textContent='This chart could not load. Refresh the page or use “Read the data” below.';el.classList.add('chart-error');el.dataset.error=e.message;console.error(el.id,e);}
}
async function setSignal(ids,name,value){settings[name]=value;await Promise.all(ids.map(async id=>{const view=views.get(id);if(view){view.signal(name,value);await view.runAsync();}}));}
async function updateState(){
 const value=document.getElementById('state-focus').value;
 await setSignal(['choropleth','symbols','tile-map'],'focusState',value);
 const rows=await getData('states.json'),s=rows.find(d=>d.State===value);
 document.getElementById('state-name').textContent=s?s.State:'Australia';
 document.getElementById('state-rate').textContent=s?s.Rate.toFixed(1):'10.2';
 document.getElementById('state-count').textContent=nf.format(s?s.Contracts:282430);
 document.getElementById('state-description').textContent=s?`${nf.format(s.Contracts)} active contracts at the end of 2025, down ${Math.abs(s.Change).toFixed(1)}% from ${nf.format(s.Previous)} in 2024.`:'282,430 active contracts across Australia at the end of 2025, down 8.6% in one year.';
}
async function updateCohort(){
 const value=document.getElementById('cohort-focus').value;
 await setSignal(['waffle'],'cohortFocus',value);
 const row=(await getData('cohorts.json')).find(d=>d.Cohort===value&&d.Year===2025);
 const target=document.getElementById('cohort-stat');target.replaceChildren();
 const strong=document.createElement('strong');strong.textContent=row.Share.toFixed(1)+'%';target.append(strong,document.createTextNode(` · ${nf.format(row.Contracts)} active contracts`));
 document.querySelector('#waffle').closest('figure').querySelector('h3').textContent=value==='Females'?'About one in four contracts was held by a female':`${value}: ${row.Share.toFixed(1)}% of active contracts`;
}
async function updateRank(){
 const value=document.getElementById('rank-focus').value;await setSignal(['bump'],'rankFocus',value);
 const rows=(await getData('occupation-ranks.json')).filter(d=>d.Year===2025).sort((a,b)=>a.Rank-b.Rank);
 const target=document.getElementById('rank-key');target.replaceChildren();
 rows.forEach(r=>{const span=document.createElement('span');if(r.Occupation===value)span.className='active';const b=document.createElement('b');b.textContent=r.Rank;span.append(b,document.createTextNode(r.Occupation));target.append(span);});
}
async function loadTable(container){
 if(container.dataset.loaded)return;
 try{
  let rows=await getData(container.dataset.table);const id=container.closest('figure').querySelector('[data-spec]').id;
  if(id==='treemap')rows=rows.filter(d=>d.Group==='Trade'&&d.Year===2025);
  if(id==='waffle')rows=rows.filter(d=>d.Year===2025);
  let fields=Object.keys(rows[0]).filter(k=>!['Longitude','Latitude','Column','Row','Code','Label'].includes(k));
  const table=document.createElement('table');const cap=document.createElement('caption');cap.textContent=container.closest('figure').querySelector('h3').textContent;table.append(cap);
  const head=document.createElement('thead'),hr=document.createElement('tr');
  fields.forEach(k=>{const th=document.createElement('th');th.scope='col';th.textContent=k.replace(/([a-z])([A-Z])/g,'$1 $2');hr.append(th);});head.append(hr);table.append(head);
  const tbody=document.createElement('tbody');rows.forEach(r=>{const tr=document.createElement('tr');fields.forEach(k=>{const td=document.createElement('td');td.textContent=typeof r[k]==='number'?nf.format(r[k]):r[k];tr.append(td);});tbody.append(tr);});table.append(tbody);container.append(table);container.dataset.loaded='true';
 }catch(e){container.textContent='Data could not load. Please use the linked source.';}
}
document.addEventListener('DOMContentLoaded',async()=>{
 await document.fonts.ready;
 await Promise.all([...document.querySelectorAll('[data-spec]')].map(renderChart));
 document.getElementById('state-focus').addEventListener('change',updateState);
 document.getElementById('reset-state').addEventListener('click',()=>{document.getElementById('state-focus').value='All';updateState();});
 document.getElementById('occupation-group').addEventListener('change',async e=>{settings.occupationGroup=e.target.value;await renderChart(document.getElementById('heatmap'));});
 document.getElementById('rank-focus').addEventListener('change',updateRank);
 document.getElementById('cohort-focus').addEventListener('change',updateCohort);
 document.querySelectorAll('.data-details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)loadTable(d.querySelector('.data-table'));}));
 await updateRank();
 let timer;const ro=new ResizeObserver(entries=>{if(entries.some(({target})=>Math.abs(target.clientWidth-Number(target.dataset.renderWidth||0))>2)){clearTimeout(timer);timer=setTimeout(()=>{document.querySelectorAll('[data-spec]').forEach(el=>{if(Math.abs(el.clientWidth-Number(el.dataset.renderWidth||0))>2)renderChart(el);});},180);}});
 document.querySelectorAll('[data-spec]').forEach(el=>ro.observe(el));
});
