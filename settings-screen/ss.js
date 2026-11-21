/* ===== Settings screen (CJ, Nov 21 2026): settings + Start on their own screen; the exercise on its own screen,
   with a "Settings" button at the top to go back. Same pattern as Find the Note. Added by settings-screen/patch.py. ===== */
function ssInit(o){
  const wrap=o.wrap, hid=(l,pre)=>l&&l.length?l.map(s=>pre+' '+s).join(',')+'{display:none!important}':'';
  const st=document.createElement('style');
  st.textContent=`
.ss-top{display:none;align-items:center;gap:14px;width:100%}
.ss-play .ss-top{display:flex}
.ss-back{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line,#2e2822);background:transparent;color:var(--fg,#f1ebe2);border-radius:999px;padding:8px 18px 8px 12px;font:inherit;font-size:16px;font-weight:600;line-height:1.2;cursor:pointer;flex:none}
.ss-back svg{width:18px;height:18px;flex:none}
.ss-back:hover{border-color:var(--muted,#a69b8d)}
.ss-back:focus-visible,.ss-go:focus-visible{outline:3px solid var(--accent,#e09a3e);outline-offset:2px}
.ss-go{display:block;width:100%;border:0;border-radius:14px;padding:15px;font:inherit;font-size:19px;font-weight:600;cursor:pointer;background:var(--accent,#e09a3e);color:var(--accent-ink,#1a120a)}
.ss-go:disabled{opacity:.45;cursor:default}
.ss-play .ss-go{display:none!important}
${hid(o.play,'.ss-play')}
${hid(o.setup,'.ss-wrap:not(.ss-play)')}
${o.css||''}`;
  (o.root.host?o.root:document.head).appendChild(st);
  wrap.classList.add('ss-wrap');
  const top=document.createElement('div'); top.className='ss-top';
  top.innerHTML='<button type="button" class="ss-back" aria-label="Stop and go back to Settings"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>Settings</button>';
  o.placeTop(top);
  top.firstChild.onclick=()=>{ o.stop(); ssSetup(); };
  let go=null;
  if(o.startBtn){
    go=document.createElement('button'); go.type='button'; go.className='ss-go';
    o.placeGo(go);
    const mirror=()=>{ const t=o.goLabel?o.goLabel():o.startBtn.textContent.trim()||'Start', d=!!(o.goDisabled?o.goDisabled():o.startBtn.disabled); if(go.textContent!==t) go.textContent=t; if(go.disabled!==d) go.disabled=d; }; // only touch it when something changed (no observer loop)
    const mo=new MutationObserver(mirror); [o.startBtn].concat(o.watch||[]).forEach(el=>el&&mo.observe(el,{childList:true,characterData:true,subtree:true,attributes:true}));
    mirror();
    go.onclick=()=>{ if(o.onGo) o.onGo(); else o.startBtn.click(); };
  }
  o.go=go; ssInit.o=o;
}
// the big Start on the Settings screen (the demo's last box points at it)
function ssGo(fallback){ const g=ssInit.o&&ssInit.o.go; return g&&g.offsetParent?g:fallback; }
function ssScreen(play){
  const o=ssInit.o; if(!o) return; const w=o.wrap, was=w.classList.contains('ss-play');
  if(was===play) return;
  w.classList.toggle('ss-play',play);
  if(o.after) o.after(play);
  const r=w.getBoundingClientRect(); if(r.top<0||(play&&r.top>80)) window.scrollBy(0,r.top-12);
}
function ssPlay(){ ssScreen(true); }
function ssSetup(){ ssScreen(false); }
