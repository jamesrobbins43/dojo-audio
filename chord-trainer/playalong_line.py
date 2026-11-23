"""Chord Trainer play-along like Numbers Play Along (CJ Nov 23).

1. The stage shows a line of 4 measures (2 x 2 on phones). Each measure: chord diagram, chord name, a small number line,
   and one blue beat number under the measure being played (placed like Numbers Play Along). 2 s look before the count-in.
   The old big chord, the Next chord and the row of beat boxes are hidden (kept in the page so other code still works).
   The 1-2-3-4 count-in (Practice and Record) shows big in the middle of the line, with the line dimmed behind it.
2. Settings: "Test these chords" pills, one per chord of the chosen key + chord type (triads: one per chord name,
   covering every voicing). Same on/off as the round check on the cards below.

apply(s) runs on build.py's string BEFORE card_sound (and before settings-screen/patch.py); idempotent.
"""

MARK = '// 4-measure play-along line (CJ Nov 23)'


def apply(s):
    if MARK in s:
        return s

    def rep(a, b):
        nonlocal s
        assert s.count(a) == 1, ('anchor', a[:80], s.count(a))
        s = s.replace(a, b)

    # ---- CSS ----
    rep('.pills { display: flex; flex-wrap: wrap; gap: 6px; }\\\n',
        '.pills { display: flex; flex-wrap: wrap; gap: 6px; }\\\n'
        '.stage > .now { grid-column: 2 / -1; align-self: start; }\\\n.stage > .nxt, .stage > .timer { display: none !important; }\\\n'
        '.w.ss-play .stage > .now { grid-column: 1 / -1; }\\\n'
        '.plw { display: grid; grid-template-columns: minmax(0,1fr) minmax(110px,170px); gap: 0 24px; width: 100%; max-width: none; margin: 0 auto; align-items: start; transition: opacity .2s; }\\\n'
        '.pl { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 18px 14px; min-width: 0; }\\\n'
        '.pslot { position: relative; display: grid; justify-items: start; align-content: start; gap: 4px; min-width: 0; padding: 0; }\\\n'
        
        '.ptop { display: grid; justify-items: center; gap: 4px; width: 82%; max-width: 230px; min-width: 0; }\\\n'
        '.pslot svg, .pnx svg { width: 100%; height: auto; display: block; }\\\n'
        '.pslot .nm { font-size: 42px !important; font-weight: 600; line-height: 1; white-space: nowrap; }\\\n'
        '.pslot .fn { font-size: 12px; color: var(--mute); text-align: center; min-height: 1.3em; white-space: nowrap; }\\\n'
        '.pslot .pc { position: relative; width: 100%; height: 30px; margin-top: 4px; }\\\n'
        '.pslot .pc span { position: absolute; top: 0; transform: translateX(-50%); font-size: 22px; font-weight: 600; color: var(--blue); font-variant-numeric: tabular-nums; line-height: 1; }\\\n'
        '.pnx { display: grid; justify-items: center; align-content: start; gap: 4px; padding: 8px 0 0 18px; border-left: 1px solid var(--line); min-width: 0; opacity: .75; }\\\n'
        '.pnx .tag { font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--mute); }\\\n'
        '.pnx .nm { font-size: 28px !important; font-weight: 600; line-height: 1; white-space: nowrap; }\\\n'
        '.pnx .pnd { width: 100%; max-width: 140px; }\\\n'
        '.now.cin #cur .plw { opacity: .3; }\\\n'
        '.now .cnt.pcin { left: 50% !important; top: 42% !important; transform: translate(-50%,-50%) !important; z-index: 3; }\\\n'
        '@media (max-width: 560px) { .stage > .now { grid-column: 1 / -1; } .plw { grid-template-columns: minmax(0,1fr); gap: 12px; } .pl { grid-template-columns: repeat(2, minmax(0,1fr)); gap: 14px 12px; } .ptop { width: 86%; } .pslot { gap: 2px; } .pslot .nm { font-size: 28px !important; } .pslot .pc { height: 26px; } .pslot .pc span { font-size: 20px; } .pnx { grid-auto-flow: column; justify-content: start; align-items: center; gap: 12px; border-left: 0; border-top: 1px solid var(--line); padding: 8px 0 0; } .pnx .pnd { width: 56px; } .pnx .nm { font-size: 24px !important; } }\\\n'
        '.f.chf { max-width: 300px; } .f.chf .pills button { padding: 5px 9px; } .f.chf .pills button * { color: inherit !important; opacity: 1 !important; }\\\n')

    # ---- Settings: Chord type above Key (CJ Nov 23) ----
    import re
    mk = re.search(r'    <label class="f"><span>Key</span>.*?\n', s); mt = re.search(r'    <label class="f"><span>Chord type</span>.*?\n', s)
    assert mk and mt and mt.start() == mk.end(), 'key/type rows'
    s = s[:mk.start()] + mt.group(0) + mk.group(0) + s[mt.end():]

    # ---- Settings: "Test these chords" ----
    rep('    <label class="f"><span>Order</span>',
        '    <div class="f chf"><span>Test these chords</span><div class="pills" id="chp"></div></div>\\\n    <label class="f"><span>Order</span>')
    rep('  function board() {\n',
        '  // "Test these chords" pills (CJ Nov 23): one per chord name; same on/off as the round check on each card\n'
        '  function chPills() {\n'
        '    var el = $(\'chp\'); if (!el) return;\n'
        '    var v = vis(), names = [], by = {};\n'
        '    v.forEach(function (c) { var k = c.name + \'|\' + (st.key === \'all\' ? c.key : \'\'); if (!by[k]) { by[k] = []; names.push(k); } by[k].push(c); });\n'
        '    el.closest(\'.f\').hidden = names.length < 2;\n'
        '    el.innerHTML = names.map(function (k) { var cs = by[k], on = cs.some(function (c) { return !st.off[c.id]; });\n'
        '      return \'<button type="button" data-ch="\' + esc(k) + \'" aria-pressed="\' + on + \'">\' + nm(cs[0].name, cs[0].type === \'tw\') + (st.key === \'all\' ? \' <small style="font-weight:500;opacity:.7">in \' + cs[0].key + \'</small>\' : \'\') + \'</button>\'; }).join(\'\');\n'
        '    el.onclick = function (e) { var b = e.target.closest(\'[data-ch]\'); if (!b) return; var cs = by[b.dataset.ch] || [], on = b.getAttribute(\'aria-pressed\') === \'true\';\n'
        '      cs.forEach(function (c) { if (on) st.off[c.id] = 1; else delete st.off[c.id]; }); refresh(); };\n'
        '  }\n'
        '  function board() {\n    chPills();\n')

    # ---- the 4-measure line ----
    rep('    root.querySelectorAll(\'.card\').forEach(function (el) { el.classList.toggle(\'cur\', !!c && el.dataset.id === c.id); });\n  }\n  function move(d) {',
        '    root.querySelectorAll(\'.card\').forEach(function (el) { el.classList.toggle(\'cur\', !!c && el.dataset.id === c.id); });\n'
        '    if (c) { PL.key = \'\'; plBeat(-1); }\n'
        '  }\n'
        '  ' + MARK + ': like Numbers Play Along, diagram above each chord, a blue 1 2 3 4 walks across the bar being played\n'
        '  var PL = { key: \'\', ls: 0 };\n'
        '  function plAt(x) { return seq[Math.floor(x / MEAS) % seq.length]; }\n'
        '  function plDraw(g) {\n'
        '    var ls = Math.floor(g / 4) * 4, key = ls + \'|\' + MEAS + \'|\' + seq.map(function (c) { return c.id; }).join(\',\');\n'
        '    if (key === PL.key && root.querySelector(\'#cur .pl\')) return;\n'
        '    PL.key = key; PL.ls = ls;\n'
        '    var h = \'<div class="plw"><div class="pl">\';\n'
        '    for (var i = 0; i < 4; i++) { var c = plAt(ls + i);\n'
        '      h += \'<div class="pslot"><div class="ptop"><span class="fn">\' + esc(fnText(c)) + \'</span><div class="pdg">\' + diagram(c) + \'</div><span class="nm">\' + nm(c.name, c.type === \'tw\') + \'</span></div><div class="pc"><span></span></div></div>\'; }\n'
        '    $(\'cur\').innerHTML = h + \'</div><div class="pnx"></div></div>\'; PL.np = -1;\n'
        '  }\n'
        '  // placed like Numbers Play Along (CJ Nov 23): only the beat being played shows; beat 1 under the chord name, then 2 3 4 walk right\n'
        '  function plPlace(el, bib) {\n'
        '    var W = el.clientWidth, t = el.querySelector(\'.ptop\'), sp = el.querySelector(\'.pc span\'); if (!W || !t || !sp || bib < 0) return;\n'
        '    var x0 = t.offsetLeft + t.offsetWidth / 2, hw = sp.offsetWidth / 2 || 6;\n'
        '    sp.style.left = (bib === 0 ? x0 : Math.min(W - hw, Math.max(x0 + bib * hw * 3, (bib + .5) / 4 * W))).toFixed(1) + \'px\';\n'
        '  }\n'
        '  function plBeat(on) {\n'
        '    if (!seq.length || !seq[pos]) return;\n'
        '    var g = pos * MEAS + (on >= 0 ? Math.floor(on / BEATS) : 0), bib = on >= 0 ? on % BEATS : -1;\n'
        '    plDraw(g);\n'
        '    var si = g - PL.ls;\n'
        '    root.querySelectorAll(\'#cur .pslot\').forEach(function (el, i) {\n'
        '      var sp = el.querySelector(\'.pc span\'), b = i === si ? bib : -1; el.classList.toggle(\'on\', i === si);\n'
        '      if (sp) { sp.textContent = b >= 0 ? b + 1 : \'\'; plPlace(el, b); }\n'
        '    });\n'
        '    // Next chord (CJ Nov 23): the chord after the one being played\n'
        '    var nx = root.querySelector(\'#cur .pnx\');\n'
        '    if (nx && PL.np !== pos) { PL.np = pos; var n = seq.length > 1 ? seq[(pos + 1) % seq.length] : null;\n'
        '      nx.innerHTML = n ? \'<span class="tag">Next</span><span class="nm">\' + nm(n.name, n.type === \'tw\') + \'</span><div class="pnd">\' + diagram(n) + \'</div>\' : \'\'; nx.style.visibility = n ? \'\' : \'hidden\'; }\n'
        '  }\n'
        '  function move(d) {')
    rep('    t.innerHTML = h;\n  }\n',
        '    t.innerHTML = h;\n    plBeat(on);\n    if (on >= 0) cntShow(null);\n  }\n')

    # ---- count-in: big in the middle of the line (Practice too) ----
    rep("    var sv = nw && nw.querySelector('svg'), nx = root.querySelector('.stage > .nxt');\n",
        "    c.classList.add('pcin'); var sv = null, nx = null;\n")
    rep("    if (k < BEATS && rec.state === 'rec' && rec.mode === 'take') { cntShow(k); return; }",
        "    if (k < BEATS && !(rec.state === 'rec' && rec.mode === 'cal')) { cntShow(k); return; }")

    # ---- how-to demo: "the next chord shows here" points at the next chord in the line ----
    rep('  function coach(el, text, side) {\n',
        '  function coach(el, text, side) {\n'
        '    if (el && el.classList && el.classList.contains(\'nxt\')) el = root.querySelector(\'#cur .pnx .pnd\') || root.querySelector(\'#cur .pnx\') || $(\'cur\');\n')
    # ---- Practice order (CJ Nov 23: "Ready starts before the instructions"): Diamond strum instructions first, then Ready ----
    RD = ("    // Practice: 4 s Ready / Begin first (CJ Nov 18)\n"
          "    if (!start.rd && !start.go && !root.querySelector('.w').classList.contains('m-rec')) { run = true; $('play').textContent = 'Stop';\n"
          "      prep(root.querySelector('.stage .now'), function () { if (!run) return; run = false; start.rd = true; start(); start.rd = false; }); return; }\n")
    DMD = ("    // Diamond: say how to strum for a few seconds before the click starts\n"
           "    if (st.strum === 0 && !start.go && !(rec.state === 'rec' && rec.mode === 'cal')) { run = true; dmShow(true); $('play').textContent = 'Stop';\n"
           "      tos.push(setTimeout(function () { if (!run) return; dmShow(false); run = false; start.go = true; start(); start.go = false; }, 4000)); return; }\n")
    DMD2 = ("    // Diamond: say how to strum for a few seconds before the click starts (before Ready, CJ Nov 23)\n"
            "    if (st.strum === 0 && !start.dm && !start.rd && !start.go && !(rec.state === 'rec' && rec.mode === 'cal')) { run = true; dmShow(true); $('play').textContent = 'Stop';\n"
            "      tos.push(setTimeout(function () { if (!run) return; dmShow(false); run = false; start.dm = true; start(); start.dm = false; }, 4000)); return; }\n")
    # 2 s to look at the chords right before the count-in (CJ Nov 23), after the strum instructions and Ready
    LOOK = ("    // 2 s to look at the chords before the count-in (CJ Nov 23)\n"
            "    if (!start.lk && !start.go && !(rec.state === 'rec' && rec.mode === 'cal')) { run = true; $('play').textContent = 'Stop'; dmShow(false);\n"
            "      tos.push(setTimeout(function () { if (!run) return; run = false; start.lk = true; start(); start.lk = false; }, 2000)); return; }\n")
    rep(RD + DMD, DMD2.replace('!start.dm && ', '!start.dm && !start.lk && ') + RD.replace('!start.rd && ', '!start.rd && !start.lk && ') + LOOK)
    return s


if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]:
        t = open(p, encoding='utf-8').read()
        open(p, 'w', encoding='utf-8').write(apply(t))
        print('ok', p)
