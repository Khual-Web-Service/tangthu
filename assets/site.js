window.addEventListener('DOMContentLoaded',function(){
  // open the collapsed source list when a footnote is followed
  function openRefs(){var h=location.hash;if(h&&h.indexOf('#ref-')===0){var d=document.getElementById('sources');if(d&&!d.open){d.open=true;}var t=document.getElementById(h.slice(1));if(t)t.scrollIntoView({block:'center'});}}
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('sup.fn a');if(a){var d=document.getElementById('sources');if(d)d.open=true;}});
  window.addEventListener('hashchange',openRefs);openRefs();
  var hd=document.querySelector('header.site');function setH(){if(hd)document.documentElement.style.setProperty('--hdr',hd.offsetHeight+'px');}setH();window.addEventListener('resize',setH);
  // sticky section menu: highlight the section being read
  var op=document.querySelector('.onpage');
  if(op){
    var links=[].slice.call(op.querySelectorAll('a')),heads=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1));}),ul=op.querySelector('ul'),cur=-1,tick=false;
    function spy(){tick=false;var line=(hd?hd.offsetHeight:60)+op.offsetHeight+40,i=-1;
      heads.forEach(function(h,k){if(h&&h.getBoundingClientRect().top<=line)i=k;});
      if(i===cur)return;cur=i;links.forEach(function(l,k){if(k===i)l.setAttribute('aria-current','true');else l.removeAttribute('aria-current');});
      if(i>=0){var a=links[i];ul.scrollTo({left:a.offsetLeft-ul.offsetLeft-12,behavior:'smooth'});}}
    window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(spy);}},{passive:true});spy();
  }
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

  // map
  var m=document.getElementById('map');
  if(m&&!window.L){m.innerHTML='<p class="small" style="padding:1rem">The interactive map could not load. Places covered: '+(window.ZO_PLACES||[]).map(function(p){return p.n}).join(', ')+'.</p>';m.style.height='auto';}
  if(m&&window.L){
    var map=L.map(m,{scrollWheelZoom:false,tap:false,keyboard:true}).setView([23.0,93.1],7);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:12,attribution:'© OpenStreetMap contributors'}).addTo(map);
    (window.ZO_REGIONS||[]).forEach(function(r){L.polygon(r.p,{color:r.c,weight:1.5,fillOpacity:.18,dashArray:'4 4'}).addTo(map).bindTooltip(r.n+' (approximate)',{sticky:true});});
    (window.ZO_PLACES||[]).forEach(function(p){L.circleMarker(p.ll,{radius:6,color:'#2b2118',weight:1,fillColor:'#c58b3a',fillOpacity:.95}).addTo(map).bindPopup('<strong>'+p.n+'</strong><br>'+p.d);});
  }
});
