/* "Ready" count-in, same as Find the Note (CJ, Nov 22 2026): replaces the old full Ready / Begin overlay.
   "Ready" sits in the exercise area with four dots that light up one per beat (800 ms); the run starts after the 4th.
   Overrides the older prep(host,done) (a later function declaration wins); prepCancel(host) still works. */
function prep(host,done){ if(getComputedStyle(host).position==='static') host.style.position='relative';
  var rt=host.getRootNode(), d=host.ownerDocument;
  if(!(rt.querySelector?rt:d).querySelector('#dgu-cin-css')){ var st=d.createElement('style'); st.id='dgu-cin-css';
    st.textContent='div.prep{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;background:rgba(0,0,0,.96);color:#fff;font-size:clamp(40px,7vw,68px);font-weight:700;line-height:1;transition:opacity .2s}'+
      'div.prep.go{color:#fff}div.prep .cin{display:flex;gap:12px;justify-content:center}div.prep .cin i{width:12px;height:12px;border-radius:50%;background:#2a2520;transition:background .08s,box-shadow .08s}'+
      'div.prep .cin i.on{background:var(--accent,#e09a3e);box-shadow:0 0 9px var(--accent,#e09a3e)}';
    (rt.host?rt:d.head).appendChild(st); }
  var o=host.querySelector(':scope > .prep'); if(!o){ o=d.createElement('div'); o.className='prep'; o.setAttribute('aria-live','assertive'); host.appendChild(o); }
  // background = the tool's own colour behind it (CJ: Chord Trainer's Ready box must match the tool)
  var bg='#000', e=host; while(e&&e.nodeType===1){ var c=getComputedStyle(e).backgroundColor; if(c&&c!=='transparent'&&!/rgba\([^)]*,\s*0\)$/.test(c)){ bg=c; break; } e=e.parentElement||(e.getRootNode()&&e.getRootNode().host); }
  o.style.background=bg;
  prepCancel(host); o.innerHTML='Ready<span class="cin" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'; void o.offsetWidth; o.classList.add('on');
  var ds=o.querySelectorAll('.cin i'); o._t=[0,1,2,3].map(function(i){ return setTimeout(function(){ ds[i].classList.add('on'); },i*800); });
  o._t.push(setTimeout(function(){ o.className='prep'; if(done) done(); },4*800+250)); }
