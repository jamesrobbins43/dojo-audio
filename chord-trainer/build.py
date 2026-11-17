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
os.makedirs(os.path.join(H, 'preview'), exist_ok=True)
open(os.path.join(H, 'chord-trainer-codeblock.html'), 'w', encoding='utf-8').write(s)
open(os.path.join(H, 'preview', 'index.html'), 'w', encoding='utf-8').write(
    '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<title>Chord Trainer</title>\n<style>html,body{margin:0;background:#141414}body{padding:56px 0 40px}</style></head><body>\n' + s + '\n</body></html>\n')
print('ok', len(s) // 1024, 'KB')
