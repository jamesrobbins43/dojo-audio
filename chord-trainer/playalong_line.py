"""Chord Trainer play-along like Numbers Play Along (CJ Nov 23).

1. The stage shows a line of 4 measures (2 x 2 on phones). Each measure: chord diagram, chord name, a small number line,
   and a blue beat number that walks 1 2 3 4 across the measure being played. A chord held from the bar before is dimmed.
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
        '.pl { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 18px 14px; width: 100%; max-width: 920px; margin: 0 auto; transition: opacity .2s; }\\\n'
        '.pslot { position: relative; display: grid; justify-items: center; align-content: start; gap: 4px; min-width: 0; padding: 8px 4px 0; border-top: 3px solid var(--line); }\\\n'
        '.pslot.on { border-top-color: var(--blue); }\\\n'
        '.pslot svg { width: 100%; max-width: 160px; height: auto; display: block; }\\\n'
        '.pslot .nm { font-size: 40px !important; font-weight: 600; line-height: 1; }\\\n'
        '.pslot .fn { font-size: 12px; color: var(--mute); text-align: center; min-height: 1.3em; }\\\n'
        '.pslot.rep > .pdg, .pslot.rep > .nm, .pslot.rep > .fn { opacity: .28; }\\\n'
        '.pslot .pc { position: relative; width: 100%; height: 30px; }\\\n'
        '.pslot .pc span { position: absolute; top: 0; transform: translateX(-50%); font-size: 22px; font-weight: 700; color: var(--blue); font-variant-numeric: tabular-nums; }\\\n'
        '.now.cin #cur .pl { opacity: .15; }\\\n'
        '.now .cnt.pcin { left: 50% !important; top: 42% !important; transform: translate(-50%,-50%) !important; z-index: 3; }\\\n'
        '@media (max-width: 560px) { .stage > .now { grid-column: 1 / -1; } .pl { grid-template-columns: repeat(2, minmax(0,1fr)); gap: 14px 12px; } .pslot svg { max-width: 108px; } .pslot { padding-top: 6px; gap: 2px; } .pslot .nm { font-size: 30px !important; } .pslot .pc { height: 26px; } .pslot .pc span { font-size: 19px; } }\\\n'
        '.f.chf { max-width: 300px; } .f.chf .pills button { padding: 5px 9px; } .f.chf .pills button * { color: inherit !important; opacity: 1 !important; }\\\n')

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
        '    var h = \'<div class="pl">\';\n'
        '    for (var i = 0; i < 4; i++) { var c = plAt(ls + i), rp = i > 0 && plAt(ls + i - 1) === c;\n'
        '      h += \'<div class="pslot\' + (rp ? \' rep\' : \'\') + \'"><div class="pdg">\' + diagram(c) + \'</div><span class="nm">\' + nm(c.name, c.type === \'tw\') + \'</span><span class="fn">\' + (rp ? \'\' : esc(fnText(c))) + \'</span><div class="pc"></div></div>\'; }\n'
        '    $(\'cur\').innerHTML = h + \'</div>\';\n'
        '  }\n'
        '  function plBeat(on) {\n'
        '    if (!seq.length || !seq[pos]) return;\n'
        '    var g = pos * MEAS + (on >= 0 ? Math.floor(on / BEATS) : 0), bib = on >= 0 ? on % BEATS : -1;\n'
        '    plDraw(g);\n'
        '    var si = g - PL.ls;\n'
        '    root.querySelectorAll(\'#cur .pslot\').forEach(function (el, i) {\n'
        '      el.classList.toggle(\'on\', i === si);\n'
        '      el.querySelector(\'.pc\').innerHTML = i === si && bib >= 0 ? \'<span style="left:\' + ((bib + .5) / BEATS * 100).toFixed(1) + \'%">\' + (bib + 1) + \'</span>\' : \'\';\n'
        '    });\n'
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
        '    if (el && el.classList && el.classList.contains(\'nxt\')) { var ps = root.querySelectorAll(\'#cur .pslot\'); el = null; for (var q = 1; q < ps.length; q++) if (!ps[q].classList.contains(\'rep\')) { el = ps[q].querySelector(\'.pdg\'); break; } el = el || (ps[1] && ps[1].querySelector(\'.pdg\')) || $(\'cur\'); }\n')
    return s


if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]:
        t = open(p, encoding='utf-8').read()
        open(p, 'w', encoding='utf-8').write(apply(t))
        print('ok', p)
