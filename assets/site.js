window.addEventListener('DOMContentLoaded',function(){
  // open the collapsed source list when a footnote is followed
  function openRefs(){var h=location.hash;if(h&&h.indexOf('#ref-')===0){var d=document.getElementById('sources');if(d&&!d.open){d.open=true;}var t=document.getElementById(h.slice(1));if(t)t.scrollIntoView({block:'center'});}}
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('sup.fn a');if(a){var d=document.getElementById('sources');if(d)d.open=true;}});
  window.addEventListener('hashchange',openRefs);openRefs();
  var hd=document.querySelector('header.site');function setH(){if(hd)document.documentElement.style.setProperty('--hdr',hd.offsetHeight+'px');}setH();window.addEventListener('resize',setH);
  // sticky section menu: highlight the section being read. One nav for both layouts.
  var op=document.querySelector('.onpage');
  if(op&&'IntersectionObserver' in window){
    var links=[].slice.call(op.querySelectorAll('a')),ul=op.querySelector('ul'),cur=-1,seen={};
    var targets=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1));});
    function mark(i){links.forEach(function(l,k){if(k===i)l.setAttribute('aria-current','true');else l.removeAttribute('aria-current');});
      if(ul.scrollWidth>ul.clientWidth){var a=links[i],still=matchMedia('(prefers-reduced-motion: reduce)').matches;ul.scrollTo({left:a.offsetLeft-ul.offsetLeft-(ul.clientWidth-a.offsetWidth)/2,behavior:still?'auto':'smooth'});}}
    var band=(hd?hd.offsetHeight:60)+24;
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){seen[e.target.id]=e.isIntersecting?e.boundingClientRect.top:null;});
      var best=null,bestTop=Infinity;
      targets.forEach(function(t,k){if(t&&seen[t.id]!=null&&seen[t.id]<bestTop){bestTop=seen[t.id];best=k;}});
      if(best!==null&&best!==cur){cur=best;mark(best);}
    },{rootMargin:'-'+band+'px 0px -70% 0px'});
    targets.forEach(function(t){if(t)io.observe(t);});
  }
  // Pau Cin Hau chart: once fonts have settled, show the note if neither our font nor the Google one loaded
  var pf=document.querySelector('.pch-fallback');
  if(pf&&document.fonts){window.addEventListener('load',function(){document.fonts.ready.then(function(){var ok=false;document.fonts.forEach(function(f){if(/Pau Cin Hau/.test(f.family)&&f.status==='loaded')ok=true;});if(!ok)pf.hidden=false;});});}
  // "/" jumps to search (unless typing in a field)
  document.addEventListener('keydown',function(e){if(e.key!=='/'||e.ctrlKey||e.metaKey||e.altKey)return;var t=e.target;if(t&&(t.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)))return;e.preventDefault();var f=document.getElementById('q')||document.getElementById('hq');if(f&&f.offsetParent!==null)f.focus();else if(window.ZoOverlay)ZoOverlay.open();else location.href='/search';});
  // mobile nav
  var b=document.querySelector('.navtoggle'), n=document.querySelector('nav.main');
  if(b&&n){
    function setNav(o){n.classList.toggle('open',o);b.setAttribute('aria-expanded',o);}
    b.addEventListener('click',function(){setNav(!n.classList.contains('open'));if(n.classList.contains('open')){var f=n.querySelector('a');if(f)f.focus();}});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){setNav(false);b.focus();}});
    n.addEventListener('click',function(e){if(e.target.closest('a'))setNav(false);});
    document.addEventListener('click',function(e){if(n.classList.contains('open')&&!n.contains(e.target)&&!b.contains(e.target))setNav(false);});
    window.matchMedia('(min-width:1101px)').addEventListener('change',function(m){if(m.matches)setNav(false);});
  }

  // timeline
  var tl=document.getElementById('timeline');
  if(tl&&window.ZO_TIMELINE){
    var themes={all:"All",origins:"Origins",colonial:"Colonial",faith:"Faith & literacy",identity:"Identity",modern:"Modern",diaspora:"Diaspora"};
    var evs={all:"All evidence",oral:"Oral tradition",sch:"Scholarly",doc:"Documented"};
    var st={th:"all",ev:"all"};
    var bar=document.createElement('div');bar.className='filters';
    function mk(group,obj){var g=document.createElement('div');g.className='fgroup';g.setAttribute('role','group');g.setAttribute('aria-label',group==='th'?'Filter by theme':'Filter by evidence');
      Object.keys(obj).forEach(function(k){var x=document.createElement('button');x.type='button';x.textContent=obj[k];x.dataset.k=k;x.setAttribute('aria-pressed',k==='all'?'true':'false');
        if(k==='all')x.classList.add('on');
        x.onclick=function(){st[group]=k;g.querySelectorAll('button').forEach(function(z){z.classList.toggle('on',z===x);z.setAttribute('aria-pressed',z===x?'true':'false')});draw();};
        g.appendChild(x);});bar.appendChild(g);}
    mk('th',themes);mk('ev',evs);tl.appendChild(bar);
    var live=document.createElement('p');live.className='small';live.setAttribute('aria-live','polite');tl.appendChild(live);var list=document.createElement('ol');list.className='tl-list';tl.appendChild(list);
    var lab={oral:"Oral tradition",doc:"Documented",sch:"Scholarly"};
    function draw(){list.innerHTML='';
      window.ZO_TIMELINE.filter(function(e){return(st.th==='all'||e.th===st.th)&&(st.ev==='all'||e.ev===st.ev)})
      .sort(function(a,b){return a.s-b.s}).forEach(function(e){
        var li=document.createElement('li');li.className='tl-item ev-'+e.ev;
        var srcs=e.src.map(function(k){return '<a class="cite" href="/sources#'+k+'">'+((window.ZO_SRC||{})[k]||k)+'</a>'}).join(' ');
        var bid='tl-'+Math.random().toString(36).slice(2,8);li.innerHTML='<button type="button" class="tl-head" aria-expanded="false" aria-controls="'+bid+'"><span class="tl-year">'+e.y+'</span><span class="tl-title">'+e.t+'</span><span class="tag '+e.ev+'">'+lab[e.ev]+'</span></button><div class="tl-body" id="'+bid+'"><p>'+e.d+'</p><p class="small">Sources: '+srcs+'</p></div>';
        var h=li.querySelector('.tl-head');h.onclick=function(){var o=li.classList.toggle('open');h.setAttribute('aria-expanded',o)};
        list.appendChild(li);});
      live.textContent=list.children.length+' event'+(list.children.length===1?'':'s')+' shown';if(!list.children.length)list.innerHTML='<li class="small">No events match.</li>';}
    draw();
  }

  // map: Leaflet loads only when the map comes near the screen (not on the hero)
  var m=document.getElementById('map');
  function fallback(){m.innerHTML='<p class="small" style="padding:1rem">The interactive map could not load. Places covered: '+(window.ZO_PLACES||[]).map(function(p){return p.n}).join(', ')+'.</p>';m.style.height='auto';}
  function initMap(){
    var map=L.map(m,{scrollWheelZoom:false,tap:false,keyboard:true}).setView([23.0,93.1],7);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:12,attribution:'© OpenStreetMap contributors'}).addTo(map);
    (window.ZO_REGIONS||[]).forEach(function(r){L.polygon(r.p,{color:r.c,weight:1.5,fillOpacity:.18,dashArray:'4 4'}).addTo(map).bindTooltip(r.n+' (approximate)',{sticky:true});});
    (window.ZO_PLACES||[]).forEach(function(p){L.circleMarker(p.ll,{radius:6,color:'#2b2118',weight:1,fillColor:'#c58b3a',fillOpacity:.95}).addTo(map).bindPopup('<strong>'+p.n+'</strong><br>'+p.d);});
  }
  function loadLeaflet(){
    var css=document.createElement('link');css.rel='stylesheet';css.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';document.head.appendChild(css);
    var js=document.createElement('script');js.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';js.onload=initMap;js.onerror=fallback;document.head.appendChild(js);
  }
  if(m){
    if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es,o){if(es[0].isIntersecting){o.disconnect();loadLeaflet();}},{rootMargin:'300px'});io.observe(m);}
    else loadLeaflet();
  }
});
