/* Record note (CJ, Nov 22 2026): with Record picked, a small line beside the Practice | Record switch:
   "*Play your answer to get a score."  dguRecNote(modeEl, belowEl?) - modeEl holds buttons data-m="prac" / data-m="rec", the picked one has class "on".
   Without belowEl the switch and the note share a wrapping row (note to the right, drops under it on a phone); with belowEl the note goes on its own line after belowEl. */
function dguRecNote(m,below,text){ if(!m) return; const d=m.ownerDocument, n=d.createElement('span'); n.className='dgu-recnote';
  n.textContent=text||'*Play your answer to get a score.';
  n.style.cssText='font-size:14px;font-weight:400;line-height:1.35;color:var(--muted,#a69b8d)';
  if(below){ n.style.display='block'; n.style.margin='8px 0 0'; below.after(n); }
  else { const row=d.createElement('div'); row.style.cssText='display:flex;align-items:center;flex-wrap:wrap;gap:8px 14px'; m.before(row); row.append(m,n);
    const cs=getComputedStyle(m); row.style.marginTop=cs.marginTop; row.style.marginBottom=cs.marginBottom; m.style.margin='0'; }
  const sync=()=>{ const r=m.querySelector('[data-m="rec"]'); const on=!!(r&&r.classList.contains('on')); n.hidden=!on; };
  new MutationObserver(sync).observe(m,{subtree:true,attributes:true,attributeFilter:['class']}); sync(); }
