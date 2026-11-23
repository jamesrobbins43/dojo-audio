/* ===== Space bar (CJ, Nov 22 2026): space starts / pauses / resumes the tool and NEVER scrolls the page.
   dguSpace({host, act, visible?})  host = the tool's outer element (code block div or iframe), act = what space does.
   One shared listener per window: with several tools on one page, space goes to the one last touched,
   else the one most on screen. Typing in a text box keeps a normal space. Shared file: /mnt/project-files/space-bar/space.js ===== */
function dguSpace(o){
  const W=window, R=W.__dguSpace||(W.__dguSpace={v:1,list:[],last:null});
  const me={host:o.host,act:o.act,vis:o.visible};
  R.list.push(me);
  o.host.addEventListener('pointerdown',()=>{ R.last=me; },true);
  if(R.on) return; R.on=1;
  const isSp=e=>(e.code==='Space'||e.key===' '||e.key==='Spacebar')&&!e.metaKey&&!e.ctrlKey&&!e.altKey;
  const typing=e=>{ const t=(e.composedPath&&e.composedPath()[0])||e.target; if(!t) return false;
    if(t.isContentEditable||t.tagName==='TEXTAREA') return true;
    return t.tagName==='INPUT'&&!/^(button|checkbox|radio|range|submit|reset|color|file|image)$/i.test(t.type||''); };
  const box=m=>{ const h=m.host; if(h.getBoundingClientRect().height) return h; // the code block's div can be display:contents on the site
    const sr=h.shadowRoot; return (sr&&(sr.querySelector('.wrap,.w')||sr.firstElementChild&&[...sr.children].find(e=>e.getBoundingClientRect().height)))||h; };
  const shown=m=>{ if(!m.host.isConnected||(m.vis&&!m.vis())) return 0; const r=box(m).getBoundingClientRect();
    const h=Math.min(r.bottom,W.innerHeight)-Math.max(r.top,0); return r.width>0&&r.height>0&&h>0?h:0; };
  R.pick=()=>{ if(R.last&&shown(R.last)) return R.last; let b=null,bh=0; R.list.forEach(m=>{ const h=shown(m); if(h>bh){ bh=h; b=m; } }); return b; };
  R.press=()=>{ const m=R.pick(); if(m) try{ m.act(); }catch(err){ console.warn('space',err); } };
  // capture on window: runs first, stops the page scroll, the focused button's own click and any older space handlers
  W.addEventListener('keydown',e=>{ if(!isSp(e)||typing(e)) return; e.preventDefault(); e.stopImmediatePropagation(); if(!e.repeat) R.press(); },true);
  W.addEventListener('keyup',e=>{ if(!isSp(e)||typing(e)) return; e.preventDefault(); e.stopImmediatePropagation(); },true);
  W.addEventListener('keypress',e=>{ if(!isSp(e)||typing(e)) return; e.preventDefault(); e.stopImmediatePropagation(); },true);
}
// press a button only when it's on screen and enabled; true if pressed
function dguTap(b){ if(!b||b.disabled||!b.getClientRects().length) return false; b.click(); return true; }
/* No footer, no empty space below the tool (CJ, Nov 22 2026): the site footer and any page sections below the tool never show,
   the section's bottom padding / spare grid rows are removed, and while running the credit line hides and the page scrolls
   so the tool sits right under the fixed site header. dguNoFooter(host, wrap, isRunning) */
function dguNoFooter(host,wrap,on){
  const d=document, de=d.documentElement;
  if(!d.getElementById('dgu-nofoot')){ const s=d.createElement('style'); s.id='dgu-nofoot';
    s.textContent='html[data-dgu-tool],html[data-dgu-tool] body,html[data-dgu-tool] #siteWrapper,html[data-dgu-tool] .site-wrapper,html[data-dgu-tool] main,html[data-dgu-tool] #page{background:#000!important}'+
      'html[data-dgu-tool] footer,html[data-dgu-tool] #footer-sections,html[data-dgu-tool] .dgu-below{display:none!important}'+
      'html[data-dgu-tool] .dgu-sec{min-height:0!important}html[data-dgu-tool] .dgu-sec .content-wrapper{padding-bottom:0!important}'+
      'html[data-dgu-tool] .dgu-sec .fluid-engine{grid-template-rows:none!important;grid-auto-rows:auto!important}';
    d.head.appendChild(s); }
  de.setAttribute('data-dgu-tool',''); host.style.setProperty('padding-bottom','12px','important');
  const sec=host.closest('section,.page-section');
  if(sec){ sec.classList.add('dgu-sec'); let n=sec.nextElementSibling; while(n){ n.classList.add('dgu-below'); n=n.nextElementSibling; } }
  const sr=host.shadowRoot; let was=null;
  // the demo's hidden instruction box must not add page height while the exercise runs
  if(sr){ const cs=d.createElement('style'); cs.textContent='.ss-play .coach,.w-play .coach,.w-done .coach{display:none!important}'; sr.appendChild(cs); }
  const headerBottom=()=>{ const h=d.querySelector('header,#header'); if(!h) return 0; const p=getComputedStyle(h).position; if(p!=='fixed'&&p!=='sticky') return 0; return Math.max(0,h.getBoundingClientRect().bottom); };
  // while running, pull the tool's section up so nothing empty sits above it: at the top of the page the tool
  // is right under the header and you can't scroll up into blank space (CJ Nov 22, Steps Drill)
  const lift=sec||host; let lifted=0;
  const headerDocBottom=()=>{ const h=d.querySelector('header,#header'); if(!h) return 0; const p=getComputedStyle(h).position, b=h.getBoundingClientRect().bottom;
    return Math.max(0,(p==='fixed'||p==='sticky')?b:b+window.scrollY); };
  // settings screen too (CJ Nov 23 "too much unused space at the top"): the tool's title sits 24px under the header
  const fit=()=>{ const run=!!was, t=wrap.getBoundingClientRect().top+window.scrollY, want=headerDocBottom()+(run?8:24);
    lifted=Math.min(0,lifted-(t-want)); lift.style.setProperty('margin-top',lifted+'px','important'); if(run) window.scrollTo(0,0); };
  const sync=()=>{ const r=!!on(); if(r===was) return; was=r;
    if(sr) sr.querySelectorAll('.credit').forEach(c=>{ c.style.display=r?'none':''; });
    requestAnimationFrame(fit); };
  window.addEventListener('resize',()=>requestAnimationFrame(fit));
  window.addEventListener('load',()=>requestAnimationFrame(fit)); setTimeout(fit,1500); setTimeout(fit,4000);
  new MutationObserver(sync).observe(wrap,{attributes:true,attributeFilter:['class']}); sync();
}
