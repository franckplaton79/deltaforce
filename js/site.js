/* Delta Force Ultimate Guide — script commun à toutes les pages.
   Chaque bloc vérifie la présence de son conteneur : une page ne charge que ce qu'elle utilise. */
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const money=n=>new Intl.NumberFormat('fr-FR',{maximumFractionDigits:0}).format(Math.round(Number(n)||0))+' Tekniq';

function toast(text){const el=$('#toast');if(!el)return;el.textContent=text;el.classList.add('show');clearTimeout(window._toastTimer);window._toastTimer=setTimeout(()=>el.classList.remove('show'),2100)}

/* Navigation et thème */
const themeBtn=$('#themeToggle');
if(themeBtn)themeBtn.addEventListener('click',()=>{document.body.classList.toggle('dark-mode');localStorage.setItem('dfm-theme',document.body.classList.contains('dark-mode')?'deep':'default');toast('Contraste ajusté')});
if(localStorage.getItem('dfm-theme')==='deep')document.body.classList.add('dark-mode');
/* Méga-menu : ouverture, fermeture au clic extérieur, à Échap, au clic sur un lien */
const mmenuBtn = $('#mmenuToggle');
const mmenuPanel = $('#mmenuPanel');
if (mmenuBtn && mmenuPanel) {
  const setOpen = (open) => {
    mmenuBtn.setAttribute('aria-expanded', String(open));
    mmenuPanel.hidden = !open;
    document.body.classList.toggle('mmenu-open', open);
  };
  setOpen(false);
  mmenuBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    setOpen(mmenuBtn.getAttribute('aria-expanded') !== 'true');
  });
  document.addEventListener('click', (e) => {
    if (!mmenuPanel.hidden && !mmenuPanel.contains(e.target) && !mmenuBtn.contains(e.target)) setOpen(false);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !mmenuPanel.hidden) { setOpen(false); mmenuBtn.focus(); }
  });
  mmenuPanel.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setOpen(false)));
}
const menuBtn = $('#menuToggle');
if (menuBtn) menuBtn.addEventListener('click', () => $('#navLinks').classList.toggle('open'));

/* Recherche interne : index construit à partir des cartes de la page courante.
   Les autres pages sont atteignables via le plan du site. */
const qsIndex=(()=>{
  const items=[];
  $$('main h2,main h3,main p,main li,.mini-tile,.result-row,.card').forEach(n=>{
    const txt=n.textContent.replace(/\s+/g,' ').trim();
    if(txt.length<25||txt.length>420)return;
    const sec=n.closest('section,article');
    const secName=sec?(sec.querySelector('h2')||sec.querySelector('h3')||{textContent:'Page'}).textContent.trim().slice(0,60):'Page';
    const anchor=n.id?'#'+n.id:(sec&&sec.id?'#'+sec.id:'');
    items.push({t:txt,s:secName,a:anchor});
  });
  return items;
})();
const qsInput=$('#quickSearch'),qsBox=$('#quickResults');
function qsRender(q){
  if(!qsInput||!qsBox)return;
  const key=q.toLowerCase().trim();
  if(!key){qsBox.classList.remove('show');qsBox.innerHTML='';return}
  const words=key.split(/\s+/).filter(w=>w.length>1);
  const hits=qsIndex.map(it=>{const low=it.t.toLowerCase();let sc=0;words.forEach(w=>{if(low.includes(w))sc+=1;if(it.s.toLowerCase().includes(w))sc+=2});return{...it,sc}}).filter(it=>it.sc>0).sort((a,b)=>b.sc-a.sc).slice(0,8);
  const esc=x=>x.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  const mark=txt=>{let out=esc(txt);words.forEach(w=>{out=out.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi'),'<mark>$1</mark>')});return out};
  qsBox.innerHTML=hits.length?hits.map(h=>`<a href="${h.a||'#'}"><b>${esc(h.s)}</b>${mark(h.t.slice(0,150))}${h.t.length>150?'…':''}</a>`).join(''):'<div class="qs-empty">Rien trouvé sur cette page. Essaie le <a href="plan.html">plan du site</a>.</div>';
  qsBox.classList.add('show');
}
if(qsInput){qsInput.addEventListener('input',e=>qsRender(e.target.value));qsInput.addEventListener('focus',e=>{if(e.target.value)qsRender(e.target.value)});document.addEventListener('click',e=>{if(!e.target.closest('.quick-search'))qsBox.classList.remove('show')});document.addEventListener('keydown',e=>{if(e.key==='/'&&document.activeElement!==qsInput){e.preventDefault();qsInput.focus()}})}

/* Checklist persistante (page Débuter) */
const boxes=$$('#starterChecklist input');
if(boxes.length){
  boxes.forEach(box=>{box.checked=localStorage.getItem('dfm-check-'+box.dataset.check)==='1';box.addEventListener('change',()=>{localStorage.setItem('dfm-check-'+box.dataset.check,box.checked?'1':'0');updateProgress()})});
  window.updateProgress=function(){const n=boxes.filter(b=>b.checked).length;$('#checkProgress').style.width=(n/boxes.length*100)+'%';$('#progressText').textContent=`${n} / ${boxes.length} étapes terminées`};
  updateProgress();
}

/* Calculateur de rentabilité (page Économie) */
const raidInputs=['haul','safe','survival','lostkit','missionReward','raidMinutes'];
function calcRaid(){
  if(!$('#haul'))return;
  const haul=+$('#haul').value||0,safe=+$('#safe').value||0,p=Math.max(0,Math.min(100,+$('#survival').value||0))/100,
        cost=+$('#lostkit').value||0,mission=+$('#missionReward').value||0,min=Math.max(1,+$('#raidMinutes').value||1);
  const gross=haul*p+safe+mission,ev=gross-cost;
  $('#grossResult').textContent=money(gross);
  $('#evResult').textContent=(ev<0?'−':'')+money(Math.abs(ev));
  $('#hourResult').textContent=(ev<0?'−':'')+money(Math.abs(ev)*60/min)+' / h';
  $('#evResult').style.color=ev<0?'var(--red)':'var(--lime)';
}
if($('#haul')){raidInputs.forEach(id=>$('#'+id).addEventListener('input',calcRaid));calcRaid()}

/* Comparateur marchand / hôtel des ventes (page Économie) */
function calcSale(){
  if(!$('#vendorPrice'))return;
  const vendor=+$('#vendorPrice').value||0,price=+$('#auctionPrice').value||0,
        fee=Math.max(0,Math.min(100,+$('#feePct').value||0))/100,net=price*(1-fee),diff=net-vendor;
  $('#auctionNet').textContent=money(net);
  $('#sellVerdict').textContent=(diff>=0?'+':'−')+money(Math.abs(diff))+(diff>0?' · l’enchère paie mieux':' · le marchand reste devant');
  $('#sellVerdict').style.color=diff>=0?'var(--lime)':'var(--orange)';
}
if($('#vendorPrice')){['vendorPrice','auctionPrice','feePct'].forEach(id=>$('#'+id).addEventListener('input',calcSale));calcSale()}

/* Schémas de routes (page Cartes) */
const mapData={
 zero:{name:'Zero Dam',mode:'OPERATIONS · apprendre le cycle',summary:'La carte la plus simple pour apprendre à piller puis sortir. Les sorties y sont nombreuses, avec ou sans condition : c’est là qu’on prend l’habitude de partir avec un sac à moitié plein plutôt que de mourir riche.',route:'Apparition → conteneurs proches → détour seulement si la route est calme → sortie choisie à l’avance.',caution:'Le tracé ci-dessous est un schéma pédagogique. Les sorties réellement ouvertes se lisent dans le raid.',tip:'Dès que le butin couvre le coût du kit, tu peux partir. Le dernier détour est celui qui coûte le plus cher.',water:false,points:[['Départ',16,72,'route'],['Butin proche',36,55,'route'],['Zone contestée',58,37,'danger'],['Sortie active',82,68,'extract']],lines:[[16,72,36,55],[36,55,58,37],[58,37,82,68]]},
 brakkesh:{name:'Brakkesh 2.0',mode:'OPERATIONS · refonte Aurora',summary:'Babel et le secteur central ont été refaits, et les contacts de faction ajoutent une décision à chaque raid. La carte la plus rentable en Tekniq, et la plus punitive quand on traîne.',route:'Départ → reconnaître le nouveau passage → objectif de faction seulement si la sortie reste crédible → sortie.',caution:'Un plan appris avant Aurora ne vaut plus rien à Babel. Portes, couvertures, étages et sorties ont bougé.',tip:'Avant d’activer un objectif de faction, décide par où tu repars. L’objectif attire du monde.',water:false,points:[['Départ',16,74,'route'],['Couverture',35,53,'route'],['Babel',55,35,'danger'],['Contact',70,50,'mission'],['Sortie',84,73,'extract']],lines:[[16,74,35,53],[35,53,55,35],[55,35,70,50],[70,50,84,73]]},
 layali:{name:'Layali Grove 2.0',mode:'OPERATIONS · eau et rotations',summary:'Le réseau fluvial ouvre des trajets alternatifs et les embarcations font gagner du temps, au prix d’une visibilité qui ne pardonne pas.',route:'Départ → couvert végétal → bord de l’eau uniquement avec une destination claire → objectif ou butin → extraction.',caution:'Un bateau se voit de loin. Ce n’est pas un itinéraire discret, c’est un raccourci assumé.',tip:'Choisis ta rive d’arrivée avant de monter dans le bateau.',water:true,points:[['Départ',15,70,'route'],['Couvert',36,53,'route'],['Rivière',53,40,'danger'],['Mission',68,55,'mission'],['Sortie',85,67,'extract']],lines:[[15,70,36,53],[36,53,53,40],[53,40,68,55],[68,55,85,67]]},
 space:{name:'Space City',mode:'OPERATIONS · pression maximale',summary:'Dense, verticale, et les portes à clé attirent les équipes. Les sorties à commutateur changent de place : on vérifie sur la carte à chaque raid.',route:'Apparition → voie de contournement → salle ciblée si tu as la clé → repérer le commutateur actif → extraire.',caution:'Ne pars jamais du principe que la sortie est là où elle était la dernière fois.',tip:'Décide de la salle avant d’entrer, et garde une sortie de secours en tête.',water:false,points:[['Départ',15,69,'route'],['Accès latéral',37,54,'route'],['Salle à clé',57,35,'danger'],['Commutateur',69,55,'mission'],['Sortie',84,71,'extract']],lines:[[15,69,37,54],[37,54,57,35],[57,35,69,55],[69,55,84,71]]},
 az3:{name:'AZ3 Nuclear Plant',mode:'OPERATIONS · radiations',summary:'Le danger environnemental s’ajoute au reste : chaque minute passée dans les secteurs contaminés se paie en soins et en temps de retour.',route:'Périphérie → préparation médicale → objectif à la mesure de l’équipe → vérifier l’exposition → sortie viable.',caution:'Supercritical est annoncé pour le 18 décembre 2026. Ce schéma décrit la carte actuelle, pas ce mode.',tip:'Sans consommables et sans sortie compatible avec ton exposition, le cœur de carte n’est pas une option.',water:true,points:[['Départ',15,72,'route'],['Périphérie',36,57,'route'],['Zone irradiée',57,35,'danger'],['Objectif',70,52,'mission'],['Sortie',84,70,'extract']],lines:[[15,72,36,57],[36,57,57,35],[57,35,70,52],[70,52,84,70]]},
 zenith:{name:'Zenith Port',mode:'WARFARE · Riptide',summary:'Carte Warfare, pas un parcours de farming. La vague inonde les niveaux bas au milieu de la partie et envoie tout le monde sur les toits.',route:'Plage et approche → couvrir l’objectif bas → repérer les montées avant la vague → tenir les toits.',caution:'Les bases de déploiement ont bougé le 12 novembre. Vérifie le secteur et les accès dans le client.',tip:'Mets-toi en position de monter avant que la bataille bascule. Après, c’est trop tard.',water:true,points:[['Approche',15,72,'route'],['Objectif bas',36,57,'danger'],['Montée',59,42,'mission'],['Toits',76,31,'route'],['Secteur',85,61,'extract']],lines:[[15,72,36,57],[36,57,59,42],[59,42,76,31],[76,31,85,61]]}
};
if($('#mapCanvas')){
  const mapKeys=Object.keys(mapData);let currentMap='zero';
  const tabs=$('#mapTabs');
  mapKeys.forEach((key,i)=>{const b=document.createElement('button');b.className='tab';b.type='button';b.role='tab';b.setAttribute('aria-selected',i===0?'true':'false');b.textContent=mapData[key].name;b.addEventListener('click',()=>selectMap(key));tabs.appendChild(b)});
  window.selectMap=function(key){currentMap=key;$$('#mapTabs .tab').forEach((b,i)=>b.setAttribute('aria-selected',mapKeys[i]===key?'true':'false'));renderMap()};
  window.renderMap=function(){
    const m=mapData[currentMap],canvas=$('#mapCanvas');
    $('#mapTitle').textContent=m.name;$('#mapModeLabel').textContent=m.mode;$('#mapSummary').textContent=m.summary;
    $('#routeText').textContent=m.route;$('#mapCaution').textContent=m.caution;$('#mapTip').textContent=m.tip;
    $('#mapWater').style.display=m.water?'block':'none';
    $$('.route-line,.map-node',canvas).forEach(e=>e.remove());
    const rect=canvas.getBoundingClientRect(),W=rect.width||800,H=rect.height||390;
    m.lines.forEach(([x1,y1,x2,y2])=>{const dx=(x2-x1)*W/100,dy=(y2-y1)*H/100,len=Math.sqrt(dx*dx+dy*dy),ang=Math.atan2(dy,dx)*180/Math.PI;const el=document.createElement('div');el.className='route-line';el.style.left=x1+'%';el.style.top=y1+'%';el.style.width=len+'px';el.style.transform=`rotate(${ang}deg)`;canvas.appendChild(el)});
    m.points.forEach(([label,x,y,type])=>{const n=document.createElement('div');n.className='map-node';n.dataset.type=type;n.style.left=x+'%';n.style.top=y+'%';n.textContent=label;canvas.appendChild(n)});
    applyMapLayers();
  };
  function applyMapLayers(){const on={};$$('[data-layer]').forEach(c=>on[c.dataset.layer]=c.checked);$$('#mapCanvas .map-node').forEach(n=>{const t=n.dataset.type;n.classList.toggle('is-hidden',(t==='danger'&&!on.danger)||(t==='extract'&&!on.extract)||(t==='mission'&&!on.mission))})}
  $$('[data-layer]').forEach(c=>c.addEventListener('change',applyMapLayers));
  renderMap();window.addEventListener('resize',()=>renderMap());
  if('ResizeObserver'in window)new ResizeObserver(()=>renderMap()).observe($('#mapCanvas'));
}

/* Filtres et recherche de l’arsenal (page Arsenal) */
if($('#weaponGrid')){
  let activeFilter='all';const cards=$$('#weaponGrid .weapon-card');
  function filterWeapons(){const q=$('#weaponSearch').value.trim().toLowerCase();cards.forEach(card=>{const mode=card.dataset.mode||'',text=(card.innerText+' '+card.dataset.search).toLowerCase();card.classList.toggle('hide',!(activeFilter==='all'||mode.includes(activeFilter))||!text.includes(q))})}
  $('#weaponSearch').addEventListener('input',filterWeapons);
  $$('#weaponFilters .pill').forEach(b=>b.addEventListener('click',()=>{activeFilter=b.dataset.filter;$$('#weaponFilters .pill').forEach(x=>x.classList.toggle('active',x===b));filterWeapons()}));
}

/* Balistique : modèle par paliers (pages Balistique) */
const penTiers=[[2,1],[1,0.75],[0,0.5]];
function penFactor(pen,cls){const d=pen-cls;for(const[t,f]of penTiers){if(d>=t)return f}return 0}
function calcAmmo(){
  if(!$('#dmg'))return;
  const dmg=Math.max(1,+$('#dmg').value||1),pen=Math.max(0,Math.min(5,+$('#pen').value||0)),
        cls=Math.max(1,Math.min(6,+$('#cls').value||1)),part=+$('#part').value||1,
        dura=Math.max(0,+$('#dura').value||0),hp=Math.max(1,+$('#hp').value||1);
  const f=penFactor(pen,cls),eff=dmg*part*f;
  const armorDmg=Math.max(1,dmg*0.55*(pen>=cls?1.1:pen===cls-1?0.85:0.6));
  const armorShots=f>=1?0:Math.ceil(dura/armorDmg);
  const shots=eff>0?Math.ceil(hp/eff):armorShots+Math.ceil(hp/(dmg*part));
  $('#effDmg').textContent=eff>0?eff.toFixed(1)+' PV par balle':'0 — l’armure bloque';
  $('#armorShots').textContent=f>=1?'inutile, la balle traverse':armorShots+' balle(s)';
  $('#ttkShots').textContent=shots+' balle(s)';
  const v=$('#verdict');
  if(f>=1&&shots<=2){v.textContent='Munition très au-dessus : deux balles suffisent';v.style.color='var(--lime)'}
  else if(f>=1){v.textContent='Traversée nette : '+shots+' balles';v.style.color='var(--lime)'}
  else if(f>0){v.textContent='Ça passe, mais l’armure mange la moitié : '+shots+' balles';v.style.color='var(--orange)'}
  else{v.textContent='Sous-calibrée : change de munition, ou vise les membres';v.style.color='var(--red)'}
}
if($('#dmg')){['dmg','pen','cls','part','dura','hp'].forEach(id=>$('#'+id).addEventListener('input',calcAmmo));calcAmmo()}

/* Codes de builds copiables (page Arsenal) */
$$('.copy-btn').forEach(btn=>btn.addEventListener('click',async()=>{
  const src=$('#'+btn.dataset.copy);if(!src)return;
  const txt=src.textContent.trim();
  try{await navigator.clipboard.writeText(txt);btn.textContent='Copié';toast('Code copié')}
  catch(e){const r=document.createRange();r.selectNodeContents(src);const sel=getSelection();sel.removeAllRanges();sel.addRange(r);btn.textContent='Sélectionné';toast('Copie manuelle : Ctrl+C')}
  setTimeout(()=>btn.textContent='Copier',2200);
}));

/* Planificateur de sortie (page Sorties) */
const exfilData={
 zero:{label:'Zero Dam',points:[
  {n:'West Rear Grip Road Entrance',c:'Aucune condition',t:'none'},
  {n:'East Rear Grip Tunnel',c:'Aucune condition',t:'none'},
  {n:'Dam Summit',c:'Poids total inférieur à 30 kg',t:'weight',v:30},
  {n:'River Bank',c:'Paiement d’environ 10 000 Tekniq',t:'cash',v:10000},
  {n:'Repair Pathway',c:'Aucun sac à dos équipé',t:'bag'},
  {n:'Industrial Elevator',c:'Levier à actionner sur place',t:'lever'},
  {n:'Shortcut near the road',c:'N’apparaît qu’une fois sur deux',t:'random'},
  {n:'East Rear Grip Road Entrance',c:'N’apparaît qu’une fois sur deux',t:'random'}]},
 brak:{label:'Brakkesh',points:[
  {n:'Bathhouse',c:'Levier, utilisable une seule fois',t:'lever'},
  {n:'Outside New Tower of Babel',c:'Levier à actionner',t:'lever'},
  {n:'Path to Grove',c:'Disponible après 15 min de raid, 3 joueurs maximum',t:'delay',v:15},
  {n:'East of New Tower of Babel',c:'Escorter le Dr R. jusqu’au point',t:'mission'}]},
 space:{label:'Space City',points:[
  {n:'Helicopter Landing Site',c:'Deux leviers à actionner',t:'lever'},
  {n:'Test Range',c:'Après 10 min, sans sac à dos, 3 joueurs maximum',t:'delay',v:10,bag:true},
  {n:'Rocket Extraction Point',c:'Mission de la fusée à accomplir',t:'mission'},
  {n:'Black Chamber / Buoyancy Lab',c:'Commutateur aléatoire, position variable',t:'random'},
  {n:'Central Garden',c:'Ascenseur à sens unique',t:'lever'}]},
 layali:{label:'Layali Grove',points:[
  {n:'Routes fluviales',c:'Trajet sur l’eau ou embarcation armée, selon le raid',t:'mission'},
  {n:'Sorties classiques',c:'Conditions variables selon la rotation',t:'random'}]},
 az3:{label:'AZ3',points:[
  {n:'Sorties de la centrale',c:'Conditions variables, entrée coûteuse',t:'random'}]}
};
let exfilMap='zero';
function renderExfil(){
  if(!$('#exfilOut'))return;
  const w=+$('#exWeight').value||0,bag=$('#exBag').value==='1',cash=+$('#exCash').value||0,min=+$('#exMin').value||0;
  $('#exfilOut').innerHTML=exfilData[exfilMap].points.map(pt=>{
    let ok=true,why='';
    if(pt.t==='weight'&&w>=pt.v){ok=false;why='tu es à '+w+' kg'}
    if(pt.t==='cash'&&cash<pt.v){ok=false;why='il te manque '+(pt.v-cash)+' Tekniq'}
    if((pt.bag||pt.t==='bag')&&bag){ok=false;why='ton sac est encore sur le dos'}
    if(pt.t==='delay'&&min<pt.v){ok=false;why='dans '+(pt.v-min)+' min'}
    return `<div class="exfil-row ${ok?'ok':'no'}"><span><b>${pt.n}</b></span><span class="state">${ok?'ouverte':'fermée'}</span><small>${pt.c}${why?' · '+why:''}</small></div>`;
  }).join('');
}
$$('#exfilMaps .pill').forEach(b=>b.addEventListener('click',()=>{$$('#exfilMaps .pill').forEach(x=>x.classList.remove('active'));b.classList.add('active');exfilMap=b.dataset.map;renderExfil()}));
['exWeight','exBag','exCash','exMin'].forEach(id=>{const el=$('#'+id);if(el)el.addEventListener('input',renderExfil)});
if($('#exfilOut'))renderExfil();

/* Comparateur de munitions (page Balistique) */
const ammoPresets=[
 {n:'.300BLK TTV, détonante',pen:5,mult:0.95},
 {n:'.300BLK TIV, détonante',pen:4,mult:0.95},
 {n:'5,45 SPALL, perforante',pen:4,mult:1},
 {n:'5,56 CINDER, incendiaire',pen:4,mult:1},
 {n:'9×19 7N30, perforante',pen:5,mult:0.9}
];
function renderCmp(){
  if(!$('#cmpOut'))return;
  const dmg=Math.max(1,+$('#cmpDmg').value||1),cls=Math.max(1,Math.min(6,+$('#cmpCls').value||1));
  const rows=ammoPresets.map(a=>{
    const f=penFactor(a.pen,cls),eff=dmg*a.mult*f;
    const armorDmg=Math.max(1,dmg*0.55*(a.pen>=cls?1.1:a.pen===cls-1?0.85:0.6));
    const armorShots=f>=1?0:Math.ceil(60/armorDmg);
    const shots=eff>0?Math.ceil(100/eff):armorShots+Math.ceil(100/(dmg*a.mult));
    return{n:a.n,eff,shots,f};
  }).sort((x,y)=>x.shots-y.shots);
  $('#cmpOut').innerHTML=rows.map((r,i)=>`<div class="exfil-row ${r.f>=1?'ok':'no'}"><span><b>${i+1}. ${r.n}</b></span><span class="state">${r.shots} balles</span><small>${r.f>=1?'traversée à '+Math.round(r.f*100)+' % des dégâts':'il faut d’abord casser l’armure'} · ${r.eff.toFixed(1)} PV par balle</small></div>`).join('');
}
if($('#cmpOut')){['cmpDmg','cmpCls'].forEach(id=>$('#'+id).addEventListener('input',renderCmp));renderCmp()}

/* ---------- Base de données d'objets : recherche, filtres, tri ---------- */
(function(){
  const roots = [
    {grid:'#wpnGrid', search:'#wpnSearch', cat:'#wpnCat', grade:'#wpnGrade', sort:'#wpnSort', count:'#wpnCount'},
    {grid:'#ammoGrid', search:'#ammoSearch', cat:'#ammoCat', grade:'#ammoGrade', sort:'#ammoSort', count:'#ammoCount'},
    {grid:'#gearGrid', search:'#gearSearch', cat:'#gearCat', grade:'#gearGrade', sort:'#gearSort', count:'#gearCount'},
    {grid:'#colGrid', search:'#colSearch', cat:'#colCat', grade:'#colGrade', sort:'#colSort', count:'#colCount'},
    {grid:'#keyGrid', search:'#keySearch', cat:'#keyCat', grade:'#keyGrade', sort:'#keySort', count:'#keyCount'},
    {grid:'#consGrid', search:'#consSearch', cat:'#consCat', grade:'#consGrade', sort:'#consSort', count:'#consCount'},
    {grid:'#attGrid', search:'#attSearch', cat:'#attCat', grade:'#attGrade', sort:'#attSort', count:'#attCount'}
  ];
  roots.forEach(cfg => {
    const grid = document.querySelector(cfg.grid);
    if(!grid) return;
    const cards = Array.prototype.slice.call(grid.querySelectorAll('.db-card'));
    const q = document.querySelector(cfg.search);
    const cat = document.querySelector(cfg.cat);
    const grade = document.querySelector(cfg.grade);
    const sort = document.querySelector(cfg.sort);
    const count = document.querySelector(cfg.count);

    const num = s => { const v = s.replace(/[^\d]/g,''); return v ? parseInt(v,10) : 0; };
    cards.forEach(c => {
      const val = c.querySelector('.db-val b');
      const per = c.querySelector('.db-val span');
      c.dataset.value = val ? num(val.textContent) : 0;
      c.dataset.per = per ? num(per.textContent) : 0;
    });

    function apply(){
      const term = (q && q.value || '').trim().toLowerCase();
      const wantCat = cat ? cat.value : '';
      const minG = grade ? parseInt(grade.value,10) : 0;
      let shown = 0;
      cards.forEach(c => {
        const ok = (!term || c.dataset.name.indexOf(term) > -1)
          && (!wantCat || c.dataset.cat === wantCat)
          && (parseInt(c.dataset.grade,10) >= minG);
        c.hidden = !ok;
        if(ok) shown++;
      });
      if(count){
        count.textContent = shown === cards.length
          ? cards.length + ' fiches affichées'
          : shown + ' fiche' + (shown > 1 ? 's' : '') + ' sur ' + cards.length;
      }
    }

    function resort(){
      if(!sort) return;
      const k = sort.value;
      const sorted = cards.slice().sort((a,b) => {
        if(k === 'name') return a.dataset.name.localeCompare(b.dataset.name,'fr');
        if(k === 'value') return b.dataset.value - a.dataset.value;
        if(k === 'per') return b.dataset.per - a.dataset.per;
        return b.dataset.grade - a.dataset.grade;
      });
      sorted.forEach(c => grid.appendChild(c));
    }

    [q, cat, grade].forEach(el => el && el.addEventListener('input', apply));
    sort && sort.addEventListener('change', () => { resort(); apply(); });
    apply();
  });
})();
