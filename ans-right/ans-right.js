/* Show answer on the right (CJ, Nov 25 2026): "the Show Answer button needs to be with the buttons to the right.
   Only Pause/Resume and Back should be on the left under the tool. And make Pause/Resume the main button that has the bold yellow color."
   dguAnsRight(root, {play: ()=>bool, keepMain: bool})
   - moves #nextBtn (Show answer / Next / Skip / Go again) to the front of the right-hand toolbar while the exercise runs
   - #pauseBtn is the yellow main button while it can be used; when Pause can't be used (round over: "Go again") #nextBtn is the main one
   - play(): true while the exercise screen shows (Find the Note keeps its big Start in #bigrow on the Settings screen)
   - keepMain false: #nextBtn never yellow during play (Find the Note: its round-over has its own Play again screen) */
function dguAnsRight(root, o){
  o = o || {};
  const nb = root.getElementById('nextBtn'), pb = root.getElementById('pauseBtn');
  const right = root.querySelectorAll('.controls .toolbar')[1];
  if (!nb || !pb || !right) return;
  const home = nb.parentNode, after = nb.nextSibling;
  const st = document.createElement('style');
  st.textContent = '.controls .toolbar #nextBtn.ar-r{min-width:9.3em;text-align:center}'
    + '@media (max-width:560px){.controls .toolbar:has(> #nextBtn.ar-r){gap:6px!important}.controls .toolbar:has(> #nextBtn.ar-r) > .btn{padding:8px 9px!important;font-size:14px!important;min-width:0!important}.controls .toolbar #nextBtn.ar-r{min-width:7.9em!important}}';
  root.appendChild(st);
  const sync = () => {
    const play = o.play ? o.play() : true;
    if (play && nb.parentNode !== right) { right.prepend(nb); nb.classList.add('ar-r'); }
    if (!play && nb.parentNode !== home) { home.insertBefore(nb, after && after.parentNode === home ? after : null); nb.classList.remove('ar-r'); }
    const can = !pb.disabled;
    pb.classList.toggle('primary', play && (can || o.keepMain === false));
    nb.classList.toggle('primary', !play || (!can && o.keepMain !== false));
  };
  const mo = new MutationObserver(sync);
  mo.observe(pb, {attributes: true, attributeFilter: ['disabled']});
  if (o.watch) mo.observe(o.watch, {attributes: true, attributeFilter: ['class']});
  sync();
}
