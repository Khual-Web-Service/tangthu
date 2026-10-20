// Search overlay, on every page. Opens from the header search icon, "/" and Ctrl/Cmd+K.
// The engine (assets/search.js) and the index are fetched the first time the overlay is needed,
// or when the icon is hovered or focused, so pages that are not searched never download them.
(function(){
  var VER=(document.currentScript&&document.currentScript.src.split('v=')[1])||'';
  var GROUPS=[['Pages',['section','page']],['Glossary',['glossary']],['Timeline',['timeline']],['Sources',['source']]];
  var SUGGEST=['Khan Thuam','puan','Pangpi'];
  var root=null, input, ul, empty, status, trigger=null, timer, active=-1, rows=[], ready=false, coreLoading=null;

  function ensureCore(){
    if(window.ZoSearch) return Promise.resolve(window.ZoSearch);
    if(coreLoading) return coreLoading;
    coreLoading=new Promise(function(ok,fail){
      var s=document.createElement('script');
      s.src='/assets/search.js?v='+VER;
      s.onload=function(){ok(window.ZoSearch);};
      s.onerror=function(){coreLoading=null;fail(new Error('search.js'));};
      document.head.appendChild(s);
    });
    return coreLoading;
  }
  function preload(){ ensureCore().then(function(z){return z.load();}).catch(function(){}); }

  function build(){
    root=document.createElement('div');
    root.className='zo-search-backdrop';
    root.hidden=true;
    root.innerHTML='<div class="zo-search" role="dialog" aria-modal="true" aria-label="Search Zogam History">'+
      '<div class="zo-bar"><label class="zo-label" for="zo-q">Search the site</label>'+
      '<input id="zo-q" class="zo-input" type="search" role="combobox" aria-expanded="false" aria-controls="zo-list" aria-autocomplete="list" aria-activedescendant="" autocomplete="off" spellcheck="false" placeholder="Search chapters, glossary, events, sources">'+
      '<button class="zo-close" type="button">Close</button></div>'+
      '<p class="zo-status" role="status" aria-live="polite"></p>'+
      '<div class="zo-body"><ul id="zo-list" class="zo-list" role="listbox" aria-label="Results"></ul><div class="zo-empty"></div></div></div>';
    document.body.appendChild(root);
    input=root.querySelector('#zo-q'); ul=root.querySelector('#zo-list'); empty=root.querySelector('.zo-empty'); status=root.querySelector('.zo-status');
    input.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(render,120);});
    input.addEventListener('keydown',onKey);
    root.querySelector('.zo-close').addEventListener('click',close);
    root.addEventListener('mousedown',function(e){if(e.target===root)close();});
    root.addEventListener('keydown',trap);
    ul.addEventListener('click',function(e){var li=e.target.closest('[role=option]');if(li)go(+li.getAttribute('data-i'));});
    ul.addEventListener('mousemove',function(e){var li=e.target.closest('[role=option]');if(li&&+li.getAttribute('data-i')!==active)setActive(+li.getAttribute('data-i'));});
    empty.addEventListener('click',function(e){var b=e.target.closest('button[data-q]');if(b){input.value=b.getAttribute('data-q');input.focus();render();}});
  }

  function typeLabel(d){return d.k==='glossary'?'Glossary':d.k==='timeline'?'Timeline':d.k==='source'?'Source':d.p;}
  function setActive(i){
    if(!rows.length) return;
    active=(i+rows.length)%rows.length;
    [].forEach.call(ul.querySelectorAll('[role=option]'),function(li){var on=+li.getAttribute('data-i')===active;li.setAttribute('aria-selected',on?'true':'false');if(on)input.setAttribute('aria-activedescendant',li.id);});
    var cur=document.getElementById('zo-o'+active);if(cur&&cur.scrollIntoView)cur.scrollIntoView({block:'nearest'});
  }
  function go(i){if(rows[i])location.href=rows[i].url;}

  function render(){
    var Z=window.ZoSearch, q=input.value.trim();
    rows=[]; active=-1; ul.innerHTML=''; empty.innerHTML=''; input.setAttribute('aria-activedescendant','');
    if(!ready||!Z){
      status.textContent='Loading…';
      input.setAttribute('aria-expanded','false');
      empty.innerHTML=suggestions();
      return;
    }
    status.textContent='';
    if(q.length<2){
      input.setAttribute('aria-expanded','false');
      empty.innerHTML=q?'<p>Type at least two letters.</p>':suggestions();
      return;
    }
    var res=Z.search(q,{type:'all'}), tl=Z.terms(q);
    if(!res.length){
      input.setAttribute('aria-expanded','false');
      empty.innerHTML='<p>No results for “'+Z.esc(q)+'”.</p><p>Try a shorter word or another spelling, or browse the <a href="/glossary">Glossary</a>.</p>';
      status.textContent='No results';
      return;
    }
    var top=res.slice(0,8), html='';
    GROUPS.forEach(function(g){
      var items=top.filter(function(r){return g[1].indexOf(r.d.k)>-1;});
      if(!items.length) return;
      html+='<li role="presentation" class="zo-group">'+g[0]+'</li>';
      items.forEach(function(r){
        var d=r.d, i=rows.length;
        rows.push({url:d.u});
        html+='<li role="option" id="zo-o'+i+'" data-i="'+i+'" class="zo-opt" aria-selected="false">'+
          '<span class="zo-type">'+Z.esc(typeLabel(d))+'</span>'+
          '<strong>'+Z.snippet(d.t,tl)+'</strong>'+
          '<span class="zo-snip">'+Z.snippet(d.x,tl)+'</span></li>';
      });
    });
    var all=rows.length;
    rows.push({url:'/search?q='+encodeURIComponent(q)});
    html+='<li role="option" id="zo-o'+all+'" data-i="'+all+'" class="zo-opt zo-all" aria-selected="false">See all '+res.length+' result'+(res.length===1?'':'s')+' →</li>';
    ul.innerHTML=html;
    input.setAttribute('aria-expanded','true');
    status.textContent=res.length+' result'+(res.length===1?'':'s');
    setActive(0);
  }
  function suggestions(){
    return '<p>Try one of these</p><div class="zo-chips">'+SUGGEST.map(function(s){return '<button type="button" data-q="'+s+'">'+s+'</button>';}).join('')+'</div>';
  }

  function onKey(e){
    if(e.key==='ArrowDown'){e.preventDefault();setActive(active+1);}
    else if(e.key==='ArrowUp'){e.preventDefault();setActive(active-1);}
    else if(e.key==='Enter'){if(rows.length){e.preventDefault();go(active);}}
  }
  // Focus stays inside the dialog while it is open; Esc closes it.
  function trap(e){
    if(e.key==='Escape'){e.preventDefault();close();return;}
    if(e.key!=='Tab')return;
    var f=[input].concat([].slice.call(root.querySelectorAll('.zo-close, .zo-chips button')));
    var first=f[0], last=f[f.length-1];
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
  }

  function open(from){
    if(!root) build();
    if(!root.hidden){input.focus();return;}
    trigger=from||document.activeElement;  // focus goes back to the icon that opened it
    root.hidden=false;
    document.documentElement.classList.add('zo-lock');
    input.focus();
    render();
    ensureCore().then(function(z){return z.load();}).then(function(){ready=true;render();}).catch(function(){
      status.textContent='Search could not load. Please try again, or browse the site map.';
    });
  }
  function close(){
    if(!root||root.hidden) return;
    root.hidden=true;
    document.documentElement.classList.remove('zo-lock');
    (trigger&&trigger.focus?trigger:document.body).focus();
  }

  // Header search icon (desktop nav link too): intercept the click, keep href="/search" for no-JS.
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a.searchicon, a.navsearch');
    if(!a||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button!==0) return;
    e.preventDefault(); open(a);
  });
  document.addEventListener('mouseover',function(e){var a=e.target.closest&&e.target.closest('a.searchicon, a.navsearch');if(a)preload();});
  document.addEventListener('focusin',function(e){var a=e.target.closest&&e.target.closest('a.searchicon, a.navsearch');if(a)preload();});
  // Ctrl/Cmd+K opens the overlay from anywhere. "/" is handled in site.js.
  document.addEventListener('keydown',function(e){
    if((e.ctrlKey||e.metaKey)&&!e.altKey&&e.key.toLowerCase()==='k'){e.preventDefault();open();}
  });
  window.ZoOverlay={open:open,close:close};
})();
