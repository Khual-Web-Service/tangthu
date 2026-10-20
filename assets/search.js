// Zogam History site search. Index: /assets/search-index.json (built by build.py) + timeline events from data.js.
(function(){
  var q=document.getElementById('q'), out=document.getElementById('search-results'), status=document.getElementById('search-status'),
      clear=document.getElementById('q-clear'), fbar=document.querySelector('.search-filters');
  if(!q||!out) return;
  var KINDS={all:'All',section:'Pages',glossary:'Glossary',timeline:'Timeline',source:'Sources'}, kind='all', idx=null, timer;
  // Normalise: lower-case, strip accents and apostrophes, collapse doubled vowels so "Ciimnuai" ~ "Cimnuai", "Kamhau" ~ "Kam Hau"
  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[’‘'`ʼ]/g,'').replace(/([aeiou])\1+/g,'$1');}
  function squash(s){return norm(s).replace(/[^a-z0-9]+/g,'');}
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  Object.keys(KINDS).forEach(function(k){var b=document.createElement('button');b.type='button';b.textContent=KINDS[k];b.setAttribute('aria-pressed',k==='all'?'true':'false');
    b.onclick=function(){kind=k;[].forEach.call(fbar.children,function(z){z.setAttribute('aria-pressed',z===b?'true':'false');});run();};fbar.appendChild(b);});
  fetch('/assets/search-index.json?v='+(document.currentScript&&document.currentScript.src.split('v=')[1]||Date.now()),{cache:'no-cache'}).then(function(r){return r.json();}).then(function(data){
    (window.ZO_TIMELINE||[]).forEach(function(e){data.push({t:e.y+': '+e.t,p:'Timeline',u:'/timeline',x:e.d,k:'timeline',e:[e.ev]});});
    data.forEach(function(d){d.p==='Home'&&(d.k=d.k==='page'?'section':d.k);if(d.k==='page')d.k='section';d._t=norm(d.t);d._x=norm(d.x);d._s=squash(d.t+' '+d.x);});
    idx=data; var u=new URLSearchParams(location.search).get('q'); if(u){q.value=u;} run(); if(!u)q.focus();
  }).catch(function(){status.textContent='Search could not load. Please try again, or browse the site map.';});
  function snippet(text,terms){
    var n=norm(text),pos=-1;for(var i=0;i<terms.length&&pos<0;i++)pos=n.indexOf(terms[i]);
    var start=Math.max(0,pos-70),s=text.slice(start,start+230);if(start>0)s='… '+s.replace(/^\S*\s/,'');if(start+230<text.length)s=s.replace(/\s\S*$/,'')+' …';
    var h=esc(s);terms.forEach(function(t){if(t.length<2)return;var pat=t.split('').map(function(c){c=c.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');return /[aeiou]/.test(c)?c+'+':c;}).join("[’']?");var re=new RegExp('('+pat+')','gi');h=h.split(/(<[^>]+>)/).map(function(seg){return seg.charAt(0)==='<'?seg:seg.replace(re,'<mark>$1</mark>');}).join('');});
    return h;}
  function run(){
    if(!idx) return; var raw=q.value.trim(); clear.hidden=!raw;
    var url=new URL(location);if(raw)url.searchParams.set('q',raw);else url.searchParams.delete('q');history.replaceState(null,'',url);
    out.innerHTML='';
    if(raw.length<2){status.textContent=raw?'Type at least two letters.':'';return;}
    var terms=norm(raw).split(/\s+/).filter(Boolean), sq=squash(raw);
    var res=[];
    idx.forEach(function(d){
      if(kind!=='all'&&d.k!==kind)return;
      var score=0,ok=true;
      terms.forEach(function(t){var inT=d._t.indexOf(t)>-1,inX=d._x.indexOf(t)>-1;if(!inT&&!inX)ok=false;else score+=(inT?10:0)+(inX?Math.min(5,d._x.split(t).length-1):0)+(new RegExp('\\b'+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\b').test(d._t+' '+d._x)?2:0);});
      if(!ok&&sq.length>3&&d._s.indexOf(sq)>-1){ok=true;score+=6;} // "kam hau" ~ "kamhau"
      if(!ok)return; if(d._t===norm(raw))score+=25; if(d.k==='glossary')score+=3; if(d.k==='source')score-=2;
      res.push({d:d,s:score});});
    res.sort(function(a,b){return b.s-a.s;});
    var shown=res.slice(0,60);
    status.textContent=res.length?(res.length+' result'+(res.length===1?'':'s')+' for “'+raw+'”'+(res.length>60?' (showing the top 60)':'')):'No results for “'+raw+'”. Try a shorter word or another spelling.';
    var LBL={oral:'Oral tradition',doc:'Documented',sch:'Scholarly interpretation',contested:'Contested'};
    out.innerHTML=shown.map(function(r){var d=r.d;
      var tags=(d.e||[]).map(function(e){return '<span class="tag '+e+'">'+LBL[e]+'</span>';}).join(' ');
      return '<li><a href="'+d.u+'"><span class="sr-where">'+esc(d.p)+(d.k==='source'?' · source':d.k==='glossary'?' · glossary':d.k==='timeline'?' · event':'')+'</span><strong>'+snippet(d.t,terms)+'</strong></a> '+tags+'<p>'+snippet(d.x,terms)+'</p></li>';}).join('');
  }
  q.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(run,120);});
  q.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();var a=out.querySelector('a');if(a)a.focus();}});
  clear.addEventListener('click',function(){q.value='';run();q.focus();});
})();
