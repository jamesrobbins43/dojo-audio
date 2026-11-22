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
  const shown=m=>{ if(!m.host.isConnected||(m.vis&&!m.vis())) return 0; const r=m.host.getBoundingClientRect();
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
