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
  // CJ Nov 22: never a separate Ready screen. The tool stays visible; "Ready" + dots only cover the prompt line
  // (Steps Drill / Find the Number #ask, Numbers Play Along #main, Chord Trainer chord name .nm), like Find the Note.
  var t=host.querySelector('#ask, #main, .nm, .prompt')||null, hr=host.getBoundingClientRect();
  o.style.cssText='background:'+bg;
  if(t&&t.getBoundingClientRect().height){ var r=t.getBoundingClientRect(), h=Math.max(58,r.height), col=h>=76;
    o.style.cssText+=';inset:auto;left:'+(r.left-hr.left+r.width/2)+'px;top:'+(r.top-hr.top+r.height/2)+'px;transform:translate(-50%,-50%);'+
      'min-width:'+r.width+'px;height:'+h+'px;padding:0 18px;white-space:nowrap;flex-direction:'+(col?'column':'row')+';gap:'+(col?'10px':'16px')+
      ';font-size:'+Math.round(col?Math.min(68,h-28):Math.min(48,h*.78))+'px;background:'+bg; }
  else o.style.cssText+=';inset:auto;left:50%;top:12px;transform:translateX(-50%);height:auto;padding:6px 18px;flex-direction:row;font-size:34px;border-radius:12px'; // no prompt found: a small strip at the top, tool stays visible
  // CJ Nov 23: once Ready starts, nothing from the how-to demo stays (its timer bar is reset here; demo boxes are hidden by space.js)
  (rt.querySelectorAll?rt:d).querySelectorAll('#timerBar, .timer > i').forEach(function(b){ b.style.transition='none'; b.style.width='0%'; });
  prepCancel(host); o.innerHTML='Ready<span class="cin" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'; void o.offsetWidth; o.classList.add('on');
  var ds=o.querySelectorAll('.cin i'); o._t=[0,1,2,3].map(function(i){ return setTimeout(function(){ ds[i].classList.add('on'); },i*800); });
  o._t.push(setTimeout(function(){ o.className='prep'; if(done) done(); },4*800+250)); }
