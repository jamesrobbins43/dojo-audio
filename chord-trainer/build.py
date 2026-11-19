"""Chord Trainer (CJ Nov 17): Open Chords + Triads in one tool, play along with beats, Record score.
Built from the LIVE Open Chords code block (key-workout-page/open-chords/open-chords-live-codeblock.html; refresh it
from dontgiveup.pro/chord-learner before a live paste). The Open Chords file itself is never changed.
Out: chord-trainer-codeblock.html (Squarespace code block) and preview/index.html (stand-alone page).
"""
import os
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(H, '..', 'key-workout-page/open-chords/open-chords-live-codeblock.html'), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

# keep the live storage key and host id so members keep their settings
rep('<h1>Open Chords</h1>', '<h1>Chord Trainer</h1>')
rep("var TYPES = ['anchor', 'open']; // Triad types ('tw', 'ts') hidden for now; data kept below.", "var TYPES = ['anchor', 'open', 'ts']; // 'tw' (worship triads) still hidden")
rep('<option value="open">Open - Standard</option></select>', '<option value="open">Open - Standard</option><option value="ts">Triads</option></select>')
# triad pickers: string groups, inversions, chord kinds (several at once)
pill = lambda attr, items: ''.join('<button type="button" data-%s="%s">%s</button>' % (attr, v, t) for v, t in items)
a = s[s.index('    <label class="f" id="setf">'): s.index('</label>', s.index('<label class="f" id="setf">')) + len('</label>')]
rep(a, '    <div class="f tsf" id="setf"><span>Strings</span><div class="pills" id="tsets">' + pill('ts', [('EAD', 'E-A-D'), ('ADG', 'A-D-G'), ('DGB', 'D-G-B'), ('GBE', 'G-B-E')]) + '</div></div>'
          '<div class="f tsf"><span>Inversions</span><div class="pills" id="tinv">' + pill('ti', [('0', 'Root'), ('1', '1st'), ('2', '2nd')]) + '</div></div>'
          '<div class="f tsf"><span>Chords</span><div class="pills" id="tq">' + pill('tq', [('maj', 'Major'), ('min', 'Minor'), ('dim', 'Dim')]) + '</div></div>')
rep('</style>\\\n<div class="w">', '.pills { display: flex; flex-wrap: wrap; gap: 6px; }\\\n'
    '.pills button { border: 1px solid var(--line); background: transparent; color: var(--mute); border-radius: 8px; padding: 6px 11px; font: inherit; font-size: 15px; font-weight: 600; cursor: pointer; }\\\n'
    '.pills button:hover { color: var(--ink); }\\\n.pills button[aria-pressed=true] { background: var(--blue); border-color: var(--blue); color: #141414; }\\\n'
    '#tsets { flex-wrap: nowrap; gap: 4px; } #tsets button { flex: 0 1 auto; min-width: 0; padding: 6px 7px; font-size: 14px; white-space: nowrap; letter-spacing: -.01em; }\\\n'  # all four string groups on one line (CJ Nov 17)
    '.w:not(.t-ts) .tsf { display: none !important; }\\\n</style>\\\n<div class="w">')
rep("var st = { key: 'G', type: 'anchor', set: 'DGB',", "var st = { key: 'G', type: 'anchor', set: 'DGB', sets: ['DGB'], invs: [0, 1, 2], qs: ['maj', 'min'],")
rep("      if (SETS[sv.set] !== undefined) st.set = sv.set;",
    "      if (SETS[sv.set] !== undefined) st.set = sv.set;\n"
    "      ['sets', 'invs', 'qs'].forEach(function (k) { if (Array.isArray(sv[k]) && sv[k].length) st[k] = sv[k]; });")
# which triads show: chosen string groups, inversions and chord kinds
rep("(c.type !== 'ts' || c.set === st.set)", "(c.type !== 'ts' || (st.sets.indexOf(c.set) > -1 && st.invs.indexOf(INV.indexOf(c.inv)) > -1 && st.qs.indexOf(/°$/.test(c.name) ? 'dim' : /m$/.test(c.name) ? 'min' : 'maj') > -1))")
rep("$('setf').style.display = st.type === 'ts' ? '' : 'none';", "root.querySelector('.w').classList.toggle('t-ts', st.type === 'ts'); tsPills();")
# triad cards and the stage say which strings
rep("c.inv ? ' · ' + c.inv : ''); }", "c.inv ? ' · ' + c.inv + ' · ' + SETL[c.set] : ''); }\n  var SETL = { EAD: 'E-A-D', ADG: 'A-D-G', DGB: 'D-G-B', GBE: 'G-B-E' };")
rep("(c.shape ? c.shape + ' shape' : c.inv)", "(c.shape ? c.shape + ' shape' : c.inv + ' · ' + SETL[c.set])")
rep("$('set').value = st.set; ", "")
rep("  $('set').addEventListener('change', function () { st.set = this.value; refresh(); });\n",
    "  function tsPills() {\n"
    "    root.querySelectorAll('#tsets [data-ts]').forEach(function (b) { b.setAttribute('aria-pressed', String(st.sets.indexOf(b.dataset.ts) > -1)); });\n"
    "    root.querySelectorAll('#tinv [data-ti]').forEach(function (b) { b.setAttribute('aria-pressed', String(st.invs.indexOf(+b.dataset.ti) > -1)); });\n"
    "    root.querySelectorAll('#tq [data-tq]').forEach(function (b) { b.setAttribute('aria-pressed', String(st.qs.indexOf(b.dataset.tq) > -1)); });\n"
    "  }\n"
    "  // several string groups, inversions and chord kinds at once; at least one of each stays on\n"
    "  function tsToggle(k, v, order) { var a = st[k], i = a.indexOf(v); if (i > -1) { if (a.length > 1) a.splice(i, 1); } else { a.push(v); a.sort(function (x, y) { return order.indexOf(x) - order.indexOf(y); }); } refresh(); }\n"
    "  $('tsets').addEventListener('click', function (e) { var b = e.target.closest('[data-ts]'); if (b) tsToggle('sets', b.dataset.ts, ['EAD', 'ADG', 'DGB', 'GBE']); });\n"
    "  $('tinv').addEventListener('click', function (e) { var b = e.target.closest('[data-ti]'); if (b) tsToggle('invs', +b.dataset.ti, [0, 1, 2]); });\n"
    "  $('tq').addEventListener('click', function (e) { var b = e.target.closest('[data-tq]'); if (b) tsToggle('qs', b.dataset.tq, ['maj', 'min', 'dim']); });\n")
# Count-in like Numbers Play Along (CJ Nov 17): a big beat number with "4/4  70 BPM" under it, no row of boxes
rep('<div class="cnt" id="cnt" hidden><b>Record in:</b><div><span>1</span><span>2</span><span>3</span><span>4</span></div></div>',
    '<div class="cnt" id="cnt" hidden><b>Record in</b><div class="cbig"></div><div class="cmeter">4/4<i></i><small>BPM</small></div></div>')
rep('.cnt.wait div { visibility: hidden; }\\\n',
    '.cnt.wait div { visibility: hidden; }\\\n'
    '.cnt { flex-direction: column; gap: 2px; top: 0; left: 0; transform: translateY(-50%); }\\\n'
    '.cnt b { display: none; }\\\n'
    '.cnt div.cbig { display: block; font-size: 72px; font-weight: 700; line-height: 1; color: var(--ink); font-variant-numeric: tabular-nums; min-height: 72px; text-align: center; }\\\n'
    '.cnt div.cmeter { display: block; font-size: 20px; font-weight: 600; letter-spacing: .04em; color: var(--ink); white-space: nowrap; }\\\n'
    '.cnt .cmeter i { font-style: normal; margin-left: .7em; } .cnt .cmeter small { font-size: .8em; font-weight: 600; margin-left: .25em; }\\\n'
    '.cnt.wait div.cbig { visibility: hidden; } .cnt.wait div.cmeter { visibility: visible; }\\\n'
    '@media (max-width: 560px) { .cnt div.cbig { font-size: 44px; min-height: 44px; } .cnt div.cmeter { font-size: 13px; } }\\\n')
rep("    var sp = c.querySelectorAll('span'); for (var q = 0; q < sp.length; q++) sp[q].className = q === k ? 'on' : q < k ? 'done' : '';\n",
    "    c.querySelector('.cbig').textContent = k >= 0 ? String(k + 1) : ''; c.querySelector('.cmeter i').textContent = st.bpm;\n"
    "    // to the right of the chord diagram (CJ Nov 17); the Next chord steps aside if there's no room\n"
    "    var sv = nw && nw.querySelector('svg'), nx = root.querySelector('.stage > .nxt');\n"
    "    if (sv) { var a = sv.getBoundingClientRect(), r = nw.getBoundingClientRect(); c.style.left = (a.right - r.left + 14) + 'px'; c.style.top = (a.top - r.top + a.height / 2) + 'px';\n"
    "      if (nx) { var cr = c.getBoundingClientRect(), xr = nx.getBoundingClientRect(); nx.style.visibility = cr.right > xr.left + 4 ? 'hidden' : ''; } }\n")
rep("    if (k === null) { c.hidden = true; if (nw) nw.classList.remove('cin'); return; }\n",
    "    if (k === null) { c.hidden = true; if (nw) nw.classList.remove('cin'); var nx0 = root.querySelector('.stage > .nxt'); if (nx0) nx0.style.visibility = ''; return; }\n")
rep("    if (lbl) c.querySelector('b').textContent = lbl;\n", "    if (lbl) c.querySelector('b').textContent = lbl.replace(':', '');\n")
# the settling bar before the count-in counts 1 2 3 4 too, so the numbers show from the first click (CJ Nov 17)
rep("if (beat < -BEATS) { click(nt, (beat + 2 * BEATS) % BEATS === 0 ? 2 : 0); click(nt + 30 / st.bpm, -2); ",
    "if (beat < -BEATS) { click(nt, (beat + 2 * BEATS) % BEATS === 0 ? 2 : 0); click(nt + 30 / st.bpm, -2); if (rec.state === 'rec' && rec.mode === 'take') (function (k, t) { tos.push(setTimeout(function () { if (run) cntShow(k); }, Math.max(0, (t - ctx.currentTime) * 1000) + 5)); })(beat + 2 * BEATS, nt); ")
# Diamond = one strum down on beat 1 of every measure (CJ Nov 17): scored that way, and said on screen after Start, before the click
rep("sub: mode === 'cal' ? 1 : st.strum || 1 / BPC,", "sub: mode === 'cal' ? 1 : st.strum || 1 / BEATS,")
rep("st.strum === 0 ? 'Strum once on each chord change'", "st.strum === 0 ? 'Strum down on beat 1 of every measure'")
rep('<div class="cnt" id="cnt" hidden>', '<div class="dmsg" id="dmsg" hidden><b>Diamond strum</b><div class="dar">&darr;</div><p>Strum down once on <em>beat 1</em> of every measure</p><small>Let it ring through 2, 3, 4</small></div><div class="cnt" id="cnt" hidden>')
rep('.cnt.wait div.cbig { visibility: hidden; }', '.dmsg { position: absolute; inset: 0; display: grid; align-content: center; justify-items: center; gap: 6px; text-align: center; z-index: 2; }\\\n'
    '.dmsg[hidden] { display: none; } .now.dm > :not(.dmsg) { visibility: hidden; }\\\n'
    '.dmsg b { font-size: 13px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--blue); }\\\n'
    '.dmsg .dar { font-size: 72px; font-weight: 700; line-height: 1; color: var(--ink); }\\\n'
    '.dmsg p { margin: 0; font-size: 24px; font-weight: 600; color: var(--ink); max-width: 24em; text-wrap: balance; }\\\n.dmsg em { font-style: normal; color: var(--blue); }\\\n'
    '.dmsg small { font-size: 15px; color: var(--mute); }\\\n'
    '@media (max-width: 560px) { .dmsg .dar { font-size: 48px; } .dmsg p { font-size: 18px; } }\\\n'
    '.cnt.wait div.cbig { visibility: hidden; }')
rep("    if (!ctx) return;\n    var lead = rec.state === 'rec' && rec.mode === 'take' ? BEATS : 0;",
    "    if (!ctx) return;\n"
    "    // Diamond: say how to strum for a few seconds before the click starts\n"
    "    if (st.strum === 0 && !start.go && !(rec.state === 'rec' && rec.mode === 'cal')) { run = true; dmShow(true); $('play').textContent = 'Stop';\n"
    "      tos.push(setTimeout(function () { if (!run) return; dmShow(false); run = false; start.go = true; start(); start.go = false; }, 4000)); return; }\n"
    "    var lead = rec.state === 'rec' && rec.mode === 'take' ? BEATS : 0;")
rep("  function stop() { run = false; clearInterval(iv); tos.forEach(clearTimeout); tos = []; timer(-1); cntShow(null);",
    "  function dmShow(on) { var d = $('dmsg'); if (!d) return; d.hidden = !on; d.parentNode.classList.toggle('dm', on); }\n"
    "  function stop() { run = false; clearInterval(iv); tos.forEach(clearTimeout); tos = []; timer(-1); cntShow(null); dmShow(false);")
# opens in Practice so everything is on screen; Record sits on the right of the switch (CJ Nov 17)
rep('<button type="button" data-m="rec">Record</button><button type="button" data-m="prac">Practice</button>', '<button type="button" data-m="prac">Practice</button><button type="button" data-m="rec">Record</button>')
rep("  setMode($('go') ? 'rec' : 'prac');\n", "  setMode('prac');\n")
# ---- start screen demo (CJ Nov 17, thread "Add how-to start screens to every Dojo tool") ----
# Settings box, then two examples (play the chord with the click, beats count in blue, next chord / Record), black boxes
# with blue arrows, no sound; plays through twice, then "Press Start when ready". Stops on Start; restarts on settings changes.
CCSS = ('.coach { position: absolute; z-index: 6; max-width: min(340px, 86%); padding: 9px 14px; border-radius: 10px; background: #000; border: 2px solid #18CEFB; color: #fff; font-size: 18px; font-weight: 500; box-shadow: 0 6px 24px rgba(0,0,0,.6); line-height: 1.3; text-align: center; pointer-events: none; opacity: 0; transform: translateY(6px); transition: opacity .25s, transform .25s; font-family: inherit; }\\\n'
  '.coach.on { opacity: 1; transform: none; pointer-events: auto; } .coach .cx{position:absolute;top:2px;right:4px;width:28px;height:28px;border:0;background:none;color:#fff;font:inherit;font-size:22px;line-height:1;cursor:pointer;opacity:.75;padding:0}.coach .cx:hover{opacity:1}.coach{padding-right:34px}.coach .ct{text-wrap:balance}\\\n'
  '.coach::before { content: ""; position: absolute; left: var(--px, 50%); top: calc(100% + 2px); width: 3px; height: 22px; background: #18CEFB; transform: translateX(-50%); }\\\n'
  '.coach::after { content: ""; position: absolute; left: var(--px, 50%); top: calc(100% + 22px); transform: translateX(-50%); border: 9px solid transparent; border-bottom: 0; border-top: 11px solid #18CEFB; }\\\n'
  '.coach.below::before { top: auto; bottom: calc(100% + 2px); }\\\n'
  '.coach.below::after { top: auto; bottom: calc(100% + 22px); border-top: 0; border-bottom: 11px solid #18CEFB; }\\\n'
  '.coach.right::before { left: auto; right: calc(100% + 2px); top: 50%; width: 22px; height: 3px; transform: translateY(-50%); }\\\n'
  '.coach.right::after { left: auto; right: calc(100% + 22px); top: 50%; transform: translateY(-50%); border: 9px solid transparent; border-left: 0; border-right: 11px solid #18CEFB; }\\\n'
  '@media (max-width: 560px) { .coach { font-size: 16px; padding: 8px 11px; } }\\\n'
  '.w.demo .bt.on { background: #18CEFB; color: #141414; }\\\n')
rep('.w:not(.t-ts) .tsf { display: none !important; }\\\n</style>', '.w:not(.t-ts) .tsf { display: none !important; }\\\n' + CCSS + '</style>')
rep("  function start() {\n    if (!seq.length) return;\n", "  function start() {\n    demoStop(true);\n    if (!seq.length) return;\n")
rep("if (rec.state === 'arm' || rec.state === 'idle') recInfo(); }\n\n  // 1, 2 or 4 measures", "if (rec.state === 'arm' || rec.state === 'idle') recInfo(); if (DMok && !run && !busy() && !root.querySelector('.w').classList.contains('m-rec')) demoGo(); }\n\n  // 1, 2 or 4 measures")
rep("    if (run) stop();\n    var w = root.querySelector('.w'); w.classList.toggle('m-rec'", "    if (run) stop();\n    demoStop(true);\n    var w = root.querySelector('.w'); w.classList.toggle('m-rec'")
rep("  function tunerOpen(on) {\n", "  function tunerOpen(on) {\n    if (on) demoStop(false);\n")
DEMO = r"""  // Start screen (CJ Nov 17): settings, then two examples with a black box + blue arrow per step; twice through, then stops
  var DM = null, DMok = false;
  function coach(el, text, side) {
    var w = root.querySelector('.w'), c = w.querySelector(':scope > .coach');
    if (!el) { if (c) c.classList.remove('on'); return; }
    if (getComputedStyle(w).position === 'static') w.style.position = 'relative';
    if (!c) { c = document.createElement('div'); c.className = 'coach'; c.setAttribute('aria-live', 'polite'); w.appendChild(c);
      c.innerHTML = '<span class="ct"></span><button type="button" class="cx" aria-label="Close the how-to">&times;</button>';
      c.querySelector('.cx').onclick = function () { c.classList.remove('on'); demoX(); }; }
    c.classList.remove('on', 'below', 'right'); c.querySelector('.ct').textContent = text.replace(/ (\S+)$/, '\u00a0$1'); // no orphan last word (CJ)
    var hr = w.getBoundingClientRect(), r = el.getBoundingClientRect();
    if (side === 'right' && r.right - hr.left + 48 + Math.min(340, c.offsetWidth) > hr.width - 4) side = 'below';
    if (side) c.classList.add(side);
    var cw = c.offsetWidth, chh = c.offsetHeight;
    if (side === 'right') { c.style.left = (r.right - hr.left + 48) + 'px'; c.style.top = Math.max(4, r.top - hr.top + r.height / 2 - chh / 2) + 'px'; }
    else {
      var cx = r.left + r.width / 2 - hr.left, left = Math.max(4, Math.min(hr.width - cw - 4, cx - cw / 2));
      c.style.left = left + 'px'; c.style.top = (side === 'below' ? r.bottom - hr.top + 48 : r.top - hr.top - chh - 48) + 'px';
      c.style.setProperty('--px', Math.max(14, Math.min(cw - 14, cx - left)) + 'px');
    }
    void c.offsetWidth; c.classList.add('on');
  }
  // the X on a demo box stops the demo (CJ Nov 17)
  function demoX() { if (DM) { clearTimeout(DM.t); clearInterval(DM.iv); DM.iv = null; timer(-1); } }
  function demoBeats(on) {
    if (!DM) return; clearInterval(DM.iv); DM.iv = null; if (!on) return;
    DM.d = 0; timer(0);
    DM.iv = setInterval(function () { if (!DM) return; DM.d++; var b = DM.d % BPC; if (b === 0) move(1); timer(b); }, 25000 / st.bpm); // demo count runs fast (CJ Nov 17)
  }
  function demoStop(reset) {
    if (!DM) return; clearTimeout(DM.t); clearInterval(DM.iv); DM = null; coach(null);
    root.querySelector('.w').classList.remove('demo'); tagSet('Play'); timer(-1); if (reset) { pos = 0; stage(); }
  }
  function demoGo() { demoStop(true); if (!seq.length) return; DM = { i: 0, step: -1, d: 0, iv: null, t: null }; root.querySelector('.w').classList.add('demo'); tagSet('Example'); demoStep(); }
  function demoStep() {
    var k = DM.i, s = DM.step;
    function nx(ms, i, stp) { DM.t = setTimeout(function () { if (!DM) return; DM.i = i; DM.step = stp; demoStep(); }, ms); }
    if (k >= 2) { demoBeats(false); timer(-1); coach($('play'), 'Press Start when ready'); DM.t = setTimeout(function () { coach(null); }, 6000); return; } // plays once, then stops (CJ Nov 17: Chord Trainer only)
    if (s === -1) { demoBeats(false); timer(-1); pos = 0; stage();
      coach(root.querySelector('.stage > .bar') || $('key'), 'First pick your settings', 'right'); return nx(4000, k, 0); }
    if (s === 0) { if (!DM.iv) demoBeats(true); coach(root.querySelector('#cur .nm') || $('cur'), 'Press Start and play this chord along with the click.'); return nx(11000, k, 2); } // no beat-boxes box (CJ Nov 17)
    if (s === 1) { coach($('timer'), 'The boxes count the beats. Change chords each time it gets back to 1.', 'below'); return nx(11000, k, 2); }
    if (k % 2 === 0) coach(root.querySelector('.stage > .nxt'), 'The next chord shows here, so you can get ready for it.');
    else coach(root.querySelector('#mode [data-m="rec"]'), 'Switch to Record to play it through once and get a score for timing and chord quality.', 'below');
    nx(11000, k + 1, k % 2 ? -1 : 0);
  }
  $('prev').addEventListener('click', function () { demoStop(false); });
  $('next').addEventListener('click', function () { demoStop(false); });

  setBpm(st.bpm); refresh(); timer(-1);
  DMok = true; demoGo();
"""
rep("\n  setBpm(st.bpm); refresh(); timer(-1);\n", "\n" + DEMO)
# ---- 4 s "Ready" then "Begin" before Practice starts (CJ Nov 18); Record mode unchanged (it waits for the player) ----
rep(".coach .ct{text-wrap:balance}\\\n", ".coach .ct{text-wrap:balance}.prep{position:absolute;inset:0;z-index:7;display:grid;place-items:center;background:rgba(0,0,0,.86);color:#fff;font-size:clamp(56px,11vw,120px);font-weight:700;line-height:1;pointer-events:none;opacity:0;transition:opacity .35s}.prep.on{opacity:1}.prep.go{color:#18CEFB}.prep.out{transition:opacity .7s;opacity:0}\\\n")
rep("  function demoBeats(on) {\n",
    "  function prep(host, done) { if (getComputedStyle(host).position === 'static') host.style.position = 'relative';\n"
    "    var o = host.querySelector(':scope > .prep'); if (!o) { o = document.createElement('div'); o.className = 'prep'; o.setAttribute('aria-live', 'assertive'); host.appendChild(o); }\n"
    "    prepCancel(host); o.textContent = 'Ready'; void o.offsetWidth; o.classList.add('on');\n"
    "    o._t = [setTimeout(function () { o.textContent = 'Begin'; o.classList.add('go'); }, 2500), setTimeout(function () { o.classList.add('out'); }, 3300), setTimeout(function () { o.className = 'prep'; if (done) done(); }, 4000)]; }\n"
    "  function prepCancel(host) { var o = host && host.querySelector(':scope > .prep'); if (!o) return; (o._t || []).forEach(clearTimeout); o._t = []; o.className = 'prep'; }\n"
    "  function demoBeats(on) {\n")
rep("    // Diamond: say how to strum",
    "    // Practice: 4 s Ready / Begin first (CJ Nov 18)\n"
    "    if (!start.rd && !start.go && !root.querySelector('.w').classList.contains('m-rec')) { run = true; $('play').textContent = 'Stop';\n"
    "      prep(root.querySelector('.stage .now'), function () { if (!run) return; run = false; start.rd = true; start(); start.rd = false; }); return; }\n"
    "    // Diamond: say how to strum")
rep("  function stop() { run = false; clearInterval(iv);", "  function stop() { run = false; prepCancel(root.querySelector('.stage .now')); clearInterval(iv);")
# closed 4 (CJ Nov 17): only the 4 comes from Figtree ("DGU Digits"), first in every Outfit list; @font-face must be in the light DOM
import json
_ff = [l for l in open('/mnt/project-files/shared/closed-4-fontface.css', encoding='utf-8').read().splitlines() if l.startswith('@font-face')][0]
rep("  var root = host.attachShadow({ mode: 'open' });",
    "  if (!document.querySelector('style[data-dgu-digits]')) { var dg = document.createElement('style'); dg.setAttribute('data-dgu-digits', ''); dg.textContent = " + json.dumps(_ff) + "; document.head.appendChild(dg); }\n"
    "  var root = host.attachShadow({ mode: 'open' });")
rep('font-family: Outfit, "Helvetica Neue"', 'font-family: "DGU Digits", Outfit, "Helvetica Neue"')
rep('font: 700 30px/1 Outfit,', 'font: 700 30px/1 "DGU Digits", Outfit,')
rep('font-family="Outfit, Arial, sans-serif"', 'font-family="DGU Digits, Outfit, Arial, sans-serif"', 2)
# ---- Sync timing = visual sync (CJ Nov 19, Rhythm Workout thread): a slow bar fills to the end, the player strums down when it gets there,
# 4 times with random pauses (no rhythm needed). Middle offset = input delay; st.cal = output latency + that. Replaces the 4+8 click sync.
VS_CSS = ('.vs{margin:6px 0 4px}.vsq{font-size:clamp(20px,3vw,26px);font-weight:700;line-height:1.2;margin:4px 0 14px;text-wrap:balance}'
          '.vtw{position:relative;padding-top:40px;margin-right:30px}'
          '.vcue{position:absolute;right:0;top:0;transform:translateX(50%);display:flex;flex-direction:column;align-items:center;color:var(--mute);font-weight:700;font-size:14px;letter-spacing:.1em;line-height:1}'
          '.vcue::after{content:"";margin-top:6px;border:7px solid transparent;border-bottom:0;border-top:10px solid currentColor}'
          '.vtw.hit .vcue{color:#e09a3e}'
          '.vtr{position:relative;height:64px;border-radius:12px 0 0 12px;border:2px solid var(--line);overflow:hidden}'
          '.vfl{position:absolute;top:0;bottom:0;left:0;width:0;background:#e09a3e}'
          '.vsn{color:var(--mute);font-size:15px;margin:12px 0 0;min-height:22px}.vsn.bad{color:#ff5c5c}.vsq.ok{color:#3ccf6e}')
rep(".prep.out{transition:opacity .7s;opacity:0}", ".prep.out{transition:opacity .7s;opacity:0}" + VS_CSS)
a = s[s.index("  function syncGuide(el) {\n"): s.index("  function syncShow(k) {\n")]
rep(a, r"""  function syncGuide(el) {
    var busy = !!VS, h = '<b class="stp">Step 2 of 2: sync timing</b><div class="vs"><div class="vsq' + (rec.calOK && !busy ? ' ok' : '') + '" id="vsq">'
      + (busy ? 'Strum <b>' + VS.n + '</b> of 4' : rec.calOK ? 'Synced &#10003;' : 'Strum down when the bar reaches the end') + '</div>'
      + '<div class="vtw" id="vtw"' + (rec.calOK && !busy ? ' hidden' : '') + '><div class="vcue">STRUM</div><div class="vtr"><div class="vfl" id="vfl"></div></div></div>'
      + '<p class="vsn' + (rec.syncMsg ? ' bad' : '') + '" id="vsn">' + (rec.syncMsg || (busy || rec.calOK ? '' : 'Mute the strings with your fretting hand. No rhythm needed: just watch the bar.')) + '</p></div>';
    h += '<div class="sgb">' + (rec.calOK && !busy ? '<button class="btn" id="sagain" type="button">Sync again</button><button class="btn main" id="snext" type="button">Next</button>'
      : '<button class="btn recgo" id="sgo" type="button"' + (busy ? ' disabled>Syncing…' : '>Sync timing') + '</button>') + '</div>';
    el.innerHTML = h;
    var b1 = $('sgo'), b2 = $('sagain'), b3 = $('snext');
    if (b1) b1.addEventListener('click', function () { vsync(); });
    if (b2) b2.addEventListener('click', function () { vsync(); });
    if (b3) b3.addEventListener('click', function () {
      rec.synced = true; rec.calOK = false; rec.mode = 'take'; rec.intro = false; pos = 0; stage(); recInfo(); lockUI(false);
    });
  }
  // Visual sync (CJ Nov 19): 4 slow bars, strum when each reaches the end, random pauses so it never becomes a rhythm.
  var VS = null;
  function vsync() {
    if (!rec.stream || VS || rec.state === 'rec' || rec.state === 'end' || rec.state === 'proc') return;
    if (run) stop();
    rec.mode = 'cal'; rec.state = 'rec'; rec.chunks = []; rec.calOK = false; rec.syncMsg = '';
    VS = { res: [], ons: [], p: 0, f: 0, fl: .002, last: -1, n: 1, g: 0, miss: 0 };
    lockUI(true); recInfo(); vsRound(.8);
  }
  function vsScan() {
    var c = rec.chunks || [], sr = ctx.sampleRate; rec.chunks = [];
    for (var i = 0; i < c.length; i++) {
      var t = c[i][0], d = c[i][1];
      for (var o = 0; o + 128 <= d.length; o += 128) {
        var e = 0, pv = VS.p; for (var k = o; k < o + 128; k++) { var df = d[k] - pv; pv = d[k]; e += df * df; } VS.p = pv; e = Math.sqrt(e / 128);
        var tt = t + o / sr; if (e > Math.max(.006, VS.fl * 6) && e > VS.f * 1.8 && tt - VS.last > .15) { VS.last = tt; VS.ons.push(tt); }
        VS.f = e; VS.fl = e < VS.fl ? VS.fl * .9 + e * .1 : VS.fl * 1.0015;
      }
    }
  }
  function vsRound(pause) {
    if (!VS) return;
    var t0 = ctx.currentTime + pause, g = t0 + 2.5; VS.g = g;
    var q = $('vsq'); if (q) q.innerHTML = 'Strum <b>' + VS.n + '</b> of 4';
    (function f() {
      if (!VS || VS.g !== g) return;
      var now = ctx.currentTime, fl = $('vfl'), tw = $('vtw');
      if (fl) fl.style.width = Math.max(0, Math.min(1, (now - t0) / 2.5)) * 100 + '%';
      if (tw) tw.classList.toggle('hit', now >= g && now < g + .35);
      if (now > g + .7) { vsJudge(); return; }
      VS.raf = requestAnimationFrame(f);
    })();
  }
  function vsJudge() {
    vsScan(); var g = VS.g, hit = null, i;
    for (i = 0; i < VS.ons.length; i++) if (VS.ons[i] >= g - .6 && VS.ons[i] <= g + .7) { hit = VS.ons[i]; break; }
    VS.ons = []; var n = $('vsn'), fl = $('vfl'); if (fl) fl.style.width = '0%';
    if (hit === null) {
      if (++VS.miss >= 3) { cancelAnimationFrame(VS.raf); VS = null; rec.chunks = null; rec.state = 'arm'; rec.syncMsg = 'Couldn’t hear your strums. Check your input level and press Sync timing again.'; lockUI(false); recInfo(); return; }
      if (n) { n.className = 'vsn bad'; n.textContent = 'Didn’t hear a strum. Strum a little harder and let’s do that one again.'; } vsRound(1.2 + Math.random()); return; }
    VS.miss = 0;
    if (n) { n.className = 'vsn'; n.textContent = ''; }
    VS.res.push(hit - g);
    if (VS.res.length >= 4) { vsDone(); return; }
    VS.n++; vsRound(1 + Math.random() * 1.6);
  }
  function vsDone() {
    var r = VS.res.slice().sort(function (a, b) { return a - b; }), mid = (r[1] + r[2]) / 2;
    var dv = r.map(function (v) { return Math.abs(v - mid); }).sort(function (a, b) { return a - b; }), spread = (dv[1] + dv[2]) / 2;
    cancelAnimationFrame(VS.raf); VS = null; rec.chunks = null; rec.state = 'arm';
    if (spread > .06) rec.syncMsg = 'Those strums were pretty spread out. Press Sync timing and try again.';
    else if (Math.abs(mid) > .25) rec.syncMsg = 'That came out ' + Math.round(Math.abs(mid) * 1000) + ' ms ' + (mid > 0 ? 'late' : 'early') + '. Press Sync timing and try again.';
    else { st.cal = Math.max(0, (ctx.outputLatency || 0) + (ctx.baseLatency || 0) + Math.max(0, mid)); save(); rec.calOK = true; pos = 0; stage(); }
    lockUI(false); recInfo();
  }
""")
rep("  function doRec(mode) {\n", "  function doRec(mode) {\n    if (mode === 'cal' || (mode === 'take' && !rec.synced)) { vsync(); return; } // visual sync (CJ Nov 19)\n")
rep("  function stop() { run = false; prepCancel(", "  function stop() { if (VS) { cancelAnimationFrame(VS.raf); VS = null; } run = false; prepCancel(")
os.makedirs(os.path.join(H, 'preview'), exist_ok=True)
open(os.path.join(H, 'chord-trainer-codeblock.html'), 'w', encoding='utf-8').write(s)
open(os.path.join(H, 'preview', 'index.html'), 'w', encoding='utf-8').write(
    '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<title>Chord Trainer</title>\n<style>html,body{margin:0;background:#141414}body{padding:56px 0 40px}</style></head><body>\n' + s + '\n</body></html>\n')
print('ok', len(s) // 1024, 'KB')
