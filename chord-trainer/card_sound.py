"""Tap a chord card at the bottom of the Chord Trainer to hear the chord (CJ Nov 22).

Recorded acoustic guitar (tonejs-instruments, CC BY 3.0, same samples as Find the Note), strummed low to high.
Skipping a chord moves to the small round check in the card's top-right corner (tapping the card used to skip it).

apply(s) works on the plain build (build.py output) AND on the live block after settings-screen/patch.py and
demo_fix.py, and is safe to run twice.   Usage: python3 card_sound.py FILE [FILE ...]   (patches in place)
"""
import sys

MARK = '// Tap a chord card to hear it (CJ Nov 22)'

CSS_A = '.card.off > * { opacity: .3; }\\\n'
CSS = ('.card .tg { position: absolute; top: 7px; right: 7px; width: 20px; height: 20px; box-sizing: border-box; border-radius: 50%; border: 1.5px solid var(--mute); display: grid; place-items: center; font-size: 12px; font-weight: 700; line-height: 1; color: #141414; }\\\n'
       '.card:not(.off) .tg { background: var(--blue); border-color: var(--blue); }\\\n.card:not(.off) .tg::after { content: "\\\\2713"; }\\\n'
       '.card.off > .tg { opacity: 1; }\\\n.card .tg::before { content: ""; position: absolute; inset: -10px; }\\\n'
       '.card:active { transform: scale(.98); }\\\n.card.hear { border-color: rgba(24,206,251,.45); }\\\n')

CLICK_A = "        el.addEventListener('click', function () { if (st.off[c.id]) delete st.off[c.id]; else st.off[c.id] = 1; refresh(); });\n"
CLICK = ("        el.insertAdjacentHTML('beforeend', '<span class=\"tg\" role=\"checkbox\" aria-checked=\"' + !st.off[c.id] + '\" aria-label=\"Include ' + c.name + ' in practice\" title=\"Include in practice\"></span>');\n"
         "        // tap the card: hear the chord; tap the round check: skip it or put it back\n"
         "        el.addEventListener('click', function (e) { if (e.target.closest('.tg')) { if (st.off[c.id]) delete st.off[c.id]; else st.off[c.id] = 1; refresh(); return; } hearChord(c, el); });\n")

JS_A = '  var seq = [], pos = 0;\n'
JS = ('  ' + MARK + ': recorded acoustic guitar (tonejs-instruments, CC BY 3.0), nearest sample pitch-shifted, strummed low to high\n'
      "  var GS = { base: 'https://cdn.jsdelivr.net/gh/nbrosowsky/tonejs-instruments@622c2f1c32c8cfce4158ddc3eb26e518ddef37e5/samples/guitar-acoustic/', lo: 38, hi: 74, nm: ['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B'], buf: {} };\n"
      "  function gsBuf(m) {\n"
      "    if (!GS.buf[m]) { GS.buf[m] = fetch(GS.base + GS.nm[m % 12] + (Math.floor(m / 12) - 1) + '.mp3').then(function (r) { if (!r.ok) throw r.status; return r.arrayBuffer(); })\n"
      "      .then(function (ab) { return new Promise(function (res, rej) { ctx.decodeAudioData(ab, res, rej); }); }); GS.buf[m].catch(function () { delete GS.buf[m]; }); }\n"
      "    return GS.buf[m];\n"
      "  }\n"
      "  function hearChord(c, el) {\n"
      "    try { ctx = ctx || new (window.AudioContext || window.webkitAudioContext)(); if (ctx.state === 'suspended') ctx.resume(); } catch (e) { return; }\n"
      "    var cp = window.KWOC_CAPO || 0, ns = [];\n"
      "    c.frets.forEach(function (f, s) { if (f >= 0) { var m = OPENM[s] + f + cp; ns.push({ m: m, k: Math.max(GS.lo, Math.min(GS.hi, m)) }); } });\n"
      "    if (el) { el.classList.add('hear'); setTimeout(function () { el.classList.remove('hear'); }, 900); }\n"
      "    Promise.all(ns.map(function (n) { return gsBuf(n.k); })).then(function (bs) {\n"
      "      var t0 = ctx.currentTime + .03;\n"
      "      bs.forEach(function (b, i) { var src = ctx.createBufferSource(), g = ctx.createGain(); src.buffer = b; src.playbackRate.value = Math.pow(2, (ns[i].m - ns[i].k) / 12);\n"
      "        g.gain.value = .5; src.connect(g); g.connect(ctx.destination); src.start(t0 + .035 * i); });\n"
      "    }).catch(function () {});\n"
      "  }\n\n" + JS_A)


def apply(s):
    if MARK in s:
        return s
    for a in (CSS_A, CLICK_A, JS_A):
        assert s.count(a) == 1, ('anchor', a[:60], s.count(a))
    return s.replace(CSS_A, CSS_A + CSS).replace(CLICK_A, CLICK).replace(JS_A, JS)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        t = open(p, encoding='utf-8').read()
        open(p, 'w', encoding='utf-8').write(apply(t))
        print('ok', p)
