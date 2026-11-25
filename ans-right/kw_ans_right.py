"""Show answer on the right for the Key Workout tabs + Timed Workout parts (CJ Nov 25 2026).
Run on a dojo-audio checkout: python3 kw_ans_right.py <repo>/key-workout   (idempotent: skips files already patched)"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
AR = open(os.path.join(here, 'ans-right.js'), encoding='utf-8').read()
TAG = '<script>/* dgu-ans-right */\n'
JS = TAG + AR + """(function(){ var n=0; function go(){ var r=document;
  if(!r.getElementById('pauseBtn')){ var h=[].slice.call(document.querySelectorAll('*')).find(function(e){ return e.shadowRoot&&e.shadowRoot.getElementById('pauseBtn'); });
    if(!h){ if(++n<50) setTimeout(go,100); return; } r=h.shadowRoot; }
  dguAnsRight(r); } go(); })();
</script>
"""
FILES = ['steps-drill', 'find-the-note', 'find-the-chord', 'find-the-key', 'numbers-play-along']
base = sys.argv[1]
for d in ('tools', 'wo'):
    for n in FILES:
        f = os.path.join(base, d, n + '.html')
        if not os.path.exists(f): continue
        s = open(f, encoding='utf-8').read()
        if TAG in s: print('skip', f); continue
        i = s.rindex('</body>') if '</body>' in s else len(s)
        open(f, 'w', encoding='utf-8').write(s[:i] + JS + s[i:]); print('ok', f)
