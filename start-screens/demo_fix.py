"""How-to demo pointing fixes (CJ Nov 22: "the blue intro instructions often don't point to the correct areas").
Run AFTER patch.py:  python3 demo_fix.py [tool ...]   (patches out/<tool>-codeblock.html and out/<tool>-preview.html in place; safe to re-run)"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(here, 'out')
FIX = {}
def fix(*names):
    def d(f):
        for n in names: FIX.setdefault(n, []).append(f)
        return f
    return d

# 1. coach(): the 'below' toggle had slipped into the end of a // comment, so every arrow pointed DOWN even when the
#    box sits under its target (settings panel, prompt). Put the toggle back in front of the comment.
BAD = "// no orphan last word (CJ) c.classList.toggle('below',!!below);"
GOOD = "c.classList.toggle('below',!!below); // no orphan last word (CJ)"
@fix('steps-drill', 'find-the-note', 'numbers-play-along', 'chord-quality-evaluator')
def below_toggle(s): return s.replace(BAD, GOOD)

# 2. Phones: the close X sat on top of the last word, because the phone rule (.coach{padding:8px 11px}) wiped out the
#    room kept for the X. Keep that room on every screen size.
CT_ANCHOR = ".coach .ct{text-wrap:balance}"
PAD = ".coach{padding-right:34px!important}"
@fix('steps-drill', 'find-the-note', 'numbers-play-along', 'chord-quality-evaluator', 'chord-trainer')
def x_room(s):
    if CT_ANCHOR + PAD in s: return s
    assert s.count(CT_ANCHOR) == 1, 'anchor'
    return s.replace(CT_ANCHOR, CT_ANCHOR + PAD)

# 3. Chord Trainer: "Press Start when ready" sat above Start, so its arrow landed on the row of beat boxes.
#    Put the box under Start, arrow pointing up at it.
@fix('chord-trainer')
def ct_end(s):
    a = "coach(ssGo($('play')), 'Press Start when ready');"
    b = "coach(ssGo($('play')), 'Press Start when ready', 'below');"
    return s if b in s else s.replace(a, b)

def run(tools):
    for t in tools:
        for kind in ('codeblock', 'preview'):
            p = os.path.join(OUT, f'{t}-{kind}.html')
            if not os.path.exists(p): continue
            s = open(p, encoding='utf-8').read(); s0 = s
            for f in FIX.get(t, []): s = f(s)
            open(p, 'w', encoding='utf-8').write(s); print(t, kind, 'changed' if s != s0 else 'unchanged')
if __name__ == '__main__': run(sys.argv[1:] or sorted(FIX))
