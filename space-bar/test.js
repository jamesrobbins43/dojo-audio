// node test.js <dir-with-previews> <tool> : presses Space through a run, logs state + whether the page scrolled
const {chromium}=require('playwright');
const [,,dir,tool]=process.argv;
(async()=>{const b=await chromium.launch({args:['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream','--autoplay-policy=no-user-gesture-required']});
for(const [w,h] of [[1100,700]]){
  const p=await (await b.newContext({viewport:{width:w,height:h}})).newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+dir+'/'+tool+'-preview.html',{waitUntil:'domcontentloaded'});
  await p.evaluate(()=>{ const d=document.createElement('div'); d.style.height='4000px'; d.textContent='below'; const f=document.createElement('footer'); f.id='footer-sections'; f.append(d); document.body.appendChild(f); });
  await p.waitForTimeout(2500);
  const st=()=>p.evaluate(()=>{ const h=[...document.querySelectorAll('*')].find(e=>e.shadowRoot); const r=h.shadowRoot, q=s=>r.querySelector(s);
    const w=q('.wrap')||q('.w'); const t=s=>{const e=q(s); return e?(e.textContent.trim().slice(0,14)+(e.disabled?'(off)':'')):'-'};
    return `foot=${getComputedStyle(document.querySelector('footer')).display} y=${scrollY} cls=[${w.className}] pause=${t('#pauseBtn')} next=${t('#nextBtn')} go=${t('#go')} play=${t('#play')} ssgo=${t('.ss-go')} mute=${t('#muteBtn')}`; });
  console.log(tool,'0 load      ',await st());
  // focus a button (as if clicked earlier) - space must NOT press it
  await p.evaluate(()=>{ const h=[...document.querySelectorAll('*')].find(e=>e.shadowRoot); const m=h.shadowRoot.querySelector('#muteBtn')||h.shadowRoot.querySelector('button'); m.focus(); });
  await p.keyboard.press('Space'); await p.waitForTimeout(6500);
  console.log(tool,'1 space     ',await st());
  await p.keyboard.press('Space'); await p.waitForTimeout(1200);
  console.log(tool,'2 space     ',await st());
  await p.keyboard.press('Space'); await p.waitForTimeout(1200);
  console.log(tool,'3 space     ',await st());
  await p.mouse.click(5,5); await p.keyboard.press('Space'); await p.waitForTimeout(800);
  console.log(tool,'4 body+space',await st());
  // typing in a text box keeps space
  console.log(tool,'errors',errs);
}
await b.close();})();
