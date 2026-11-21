"""Settings screen for every Dojo tool (CJ, Nov 21 2026).
Applies ss.js + a per-tool config ON TOP of each tool's LIVE code block (verified identical to the live page Nov 21).
Run: python3 patch.py [tool ...]   -> out/<tool>-codeblock.html (paste into Squarespace) + out/<tool>-preview.html"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
P = '/mnt/project-files/'
SS = open(os.path.join(here, 'ss.js'), encoding='utf-8').read()
GUITAR = P + 'top3-workout/guitar-acoustic.js'

class Patch:
    def __init__(self, s): self.s = s
    def rep(self, a, b, n=1):
        c = self.s.count(a)
        assert c == n, (c, a[:100])
        self.s = self.s.replace(a, b)

TOOLS = {}
def tool(name, src):
    def d(f): TOOLS[name] = (src, f); return f
    return d

@tool('steps-drill', P + 'steps-drill/dojo/steps-drill-codeblock.html')
def steps(p):
    p.rep("coach($('ask').closest('.wrap'),$('nextBtn'),DEMO_END)", "coach($('ask').closest('.wrap'),ssGo($('nextBtn')),DEMO_END)")
    p.rep("function start(){\n  if(!start.go){", "function start(){\n  ssPlay();\n  if(!start.go){")
    p.rep("function idle(over){\n  demoStop();", "function idle(over){\n  if(!over) ssSetup();\n  demoStop();")
    p.rep("renderSets(); renderChroma(); syncChroma(); syncSteps(); syncMute(); idle();\n})();",
      SS + """
ssInit({root, wrap:root.querySelector('.wrap'), play:['header','#setup'], setup:['.controls'],
  placeTop:t=>$('session').prepend(t), startBtn:$('nextBtn'), placeGo:g=>$('session').appendChild(g),
  stop:()=>{ prepCancel($('session')); $('nextBtn').disabled=false; idle(); }});
renderSets(); renderChroma(); syncChroma(); syncSteps(); syncMute(); idle();
})();""")

@tool('find-the-number', P + 'chord-numbers/dojo/number-the-chords-codeblock.html')
def ftnum(p):
    p.rep("tip('Press Start when ready',$('nextBtn'),", "tip('Press Start when ready',ssGo($('nextBtn')),")
    p.rep("function start(){\n  if(!start.go){", "function start(){\n  ssPlay();\n  if(!start.go){")
    p.rep("function idle(over){\n  if(S) clearT();", "function idle(over){\n  if(!over) ssSetup();\n  if(S) clearT();")
    p.rep("renderSets(); syncMute(); idle();\n})();",
      SS + """
ssInit({root, wrap:root.querySelector('.wrap'), play:['header','#setup'], setup:['.controls'],
  placeTop:t=>$('session').prepend(t), startBtn:$('nextBtn'), placeGo:g=>$('session').appendChild(g),
  stop:()=>idle()});
renderSets(); syncMute(); idle();
})();""")

@tool('numbers-play-along', P + 'numbers-play-along/dojo/numbers-play-along-codeblock.html')
def npa(p):
    p.rep("coach(host,$('nextBtn'),'Press Start when ready')", "coach(host,ssGo($('nextBtn')),'Press Start when ready')")
    p.rep("async function start(){\n", "async function start(){\n  ssPlay();\n")
    p.rep("function idleView(state){\n", "function idleView(state){\n  if(!state) ssSetup();\n")
    p.rep("renderSetup(); syncMute(); idleView();\n})();",
      SS + """
ssInit({root, wrap:root.querySelector('.wrap'), play:['header','#setup'], setup:['.controls'],
  placeTop:t=>root.querySelector('.session').prepend(t), startBtn:$('nextBtn'), placeGo:g=>root.querySelector('.session').appendChild(g),
  stop:()=>{ prepCancel($('card')); stop(); }});
renderSetup(); syncMute(); idleView();
})();""")

@tool('chord-quality-evaluator', P + 'note-quality/dojo/note-quality-codeblock.html')
def cq(p):
    p.rep("coach(H, $('go'), 'Press Start when ready')", "coach(H, ssGo($('go')), 'Press Start when ready')")
    p.rep("  if (running) return stopAll();\n  strum = null;", "  if (running) return stopAll();\n  ssPlay();\n  strum = null;")
    p.rep("function reset() {\n", "function reset() {\n  ssSetup();\n")
    p.rep("\nreset();\n})();",
      "\n" + SS + """
ssInit({root, wrap:root.querySelector('.wrap'), play:['header','.sets'], setup:['.stage .toolbar'],
  placeTop:t=>root.querySelector('.main').before(t), startBtn:$('go'), placeGo:g=>root.querySelector('.stage .toolbar').after(g),
  css:'.ss-go{background:var(--brand);color:#001218;margin-top:4px}',
  stop:()=>{ stopAll(true); reset(); }});
reset();
})();""")

@tool('chord-trainer', P + 'chord-trainer/chord-trainer-codeblock.html')
def ct(p):
    p.rep("coach($('play'), 'Press Start when ready')", "coach(ssGo($('play')), 'Press Start when ready')")
    p.rep("  function start() {\n    demoStop(true);", "  function start() {\n    ssPlay();\n    demoStop(true);")
    p.rep("    if (mode === 'take' && !rec.synced) mode = 'cal';\n    if (run) stop();", "    if (mode === 'take' && !rec.synced) mode = 'cal';\n    if (mode === 'take') ssPlay();\n    if (run) stop();")
    p.rep("  setBpm(st.bpm); refresh(); timer(-1);\n  DMok = true; demoGo();\n})();",
      "  setBpm(st.bpm); refresh(); timer(-1);\n  DMok = true; demoGo();\n" + SS + """
  (function () {
    var W = root.querySelector('.w'), isRec = function () { return W.classList.contains('m-rec'); };
    ssInit({ root: root, wrap: W, play: ['.top', '.stage > .side', '#tuner'], setup: ['.stage > .btns'],
      css: '.ss-top{margin:62px 0 22px}.stage > .ss-go{grid-column:1 / -1;background:var(--blue);color:#000}.w.m-rec .stage > .ss-go{order:4}.w.gate .ss-go,.w.res-on .ss-go{display:none!important}.w.ss-wrap:not(.ss-play):not(.gate) .stage > .rp .rrow > #go{display:none!important}.w.ss-wrap:not(.ss-play) .stage > .rp .rinfo{display:none}',
      placeTop: function (t) { root.querySelector('.stage').before(t); },
      startBtn: $('play'), watch: [W, $('rp')], placeGo: function (g) { root.querySelector('.stage').appendChild(g); },
      goLabel: function () { return isRec() ? ($('go') ? $('go').textContent : 'Record') : $('play').textContent.trim() || 'Start'; },
      goDisabled: function () { return isRec() ? !!($('go') && $('go').disabled) : $('play').disabled; },
      onGo: function () { if (isRec() && $('go')) $('go').click(); else $('play').click(); },
      stop: function () {
        if (rec.state === 'rec' || rec.state === 'end') stop();
        if (run) stop();
        if (resOn()) { stopPlay(); var el = $('res'); el.hidden = true; el.innerHTML = ''; W.classList.remove('res-on'); }
        if (isRec()) recInfo(); else demoGo();
      } });
  })();
})();""")

@tool('find-the-note', P + 'find-the-note-redesign/live/find-the-note-v2-codeblock.html')
def ftn(p):
    # the round's X becomes the same labeled "Settings" button the other tools use
    p.rep('<button type="button" class="tb-x" id="endBtn" aria-label="End the round and go back to settings">✕</button>',
          '<button type="button" class="tb-x" id="endBtn" aria-label="Stop and go back to Settings"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>Settings</button>')
    p.rep(".tb-x{width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:transparent;color:var(--muted);font-size:16px;display:grid;place-items:center;flex:none;padding:0}\n.tb-x:hover{color:var(--fg);border-color:var(--muted)}",
          ".tb-x{display:inline-flex;align-items:center;gap:6px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--fg);font-size:16px;font-weight:600;line-height:1.2;padding:8px 18px 8px 12px;flex:none}\n.tb-x svg{width:18px;height:18px;flex:none}\n.tb-x:hover{border-color:var(--muted)}")

def build(name):
    src, f = TOOLS[name]
    p = Patch(open(src, encoding='utf-8').read())
    f(p)
    os.makedirs(os.path.join(here, 'out'), exist_ok=True)
    open(os.path.join(here, 'out', name + '-codeblock.html'), 'w', encoding='utf-8').write(p.s)
    prev = ('<!doctype html><meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>' + name + '</title>\n'
            '<style>html,body{margin:0;background:#000}</style>\n<script>' + open(GUITAR, encoding='utf-8').read() + '</script>\n' + p.s)
    open(os.path.join(here, 'out', name + '-preview.html'), 'w', encoding='utf-8').write(prev)
    print('ok', name, len(p.s) // 1024, 'KB')

for n in (sys.argv[1:] or TOOLS): build(n)
