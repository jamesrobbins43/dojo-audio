"""Settings screen for every Dojo tool (CJ, Nov 21 2026).
Applies ss.js + a per-tool config ON TOP of each tool's LIVE code block (verified identical to the live page Nov 21).
Run: python3 patch.py [tool ...]   -> out/<tool>-codeblock.html (paste into Squarespace) + out/<tool>-preview.html"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
P = '/mnt/project-files/'
SS = open(os.path.join(here, 'ss.js'), encoding='utf-8').read()
GUITAR = P + 'top3-workout/guitar-acoustic.js'
# Space bar (CJ, Nov 22 2026): space starts / pauses / resumes every tool and never scrolls the page. Shared add-on, see space-bar/README.md
SP = open(P + 'space-bar/space.js', encoding='utf-8').read()
FTNC = open(P + 'space-bar/ftn-compact.js', encoding='utf-8').read()
RN = open(P + 'space-bar/recnote.js', encoding='utf-8').read()
CIN = open(P + 'space-bar/countin.js', encoding='utf-8').read()
SSON = "const ssOn=()=>ssInit.o&&!ssInit.o.wrap.classList.contains('ss-play');\n"

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
    # CJ Nov 22: no separate Ready screen. During the count-in the drill stays on screen with its first note drawn; "Ready" covers only the prompt line
    p.rep("audio(); demoStop(); $('nextBtn').disabled=true; prep($('session'),()=>{", "audio(); demoStop(); $('progress').innerHTML=''; start.seq=buildSequence(settings.perRound); { const c0=start.seq[0]; if(c0.mode==='scale') drawScale(c0,false); else drawPair(c0,false); } $('session').classList.add('cinb'); $('nextBtn').disabled=true; prep($('session'),()=>{ $('session').classList.remove('cinb');")
    p.rep("S={seq:buildSequence(settings.perRound), i:0", "S={seq:start.seq||buildSequence(settings.perRound), i:0"); p.rep("$('pauseBtn').textContent='Pause';\n  enter(true);\n}", "$('pauseBtn').textContent='Pause';\n  start.seq=null; enter(true);\n}")
    p.rep("coach($('ask').closest('.wrap'),$('nextBtn'),DEMO_END)", "coach($('ask').closest('.wrap'),ssGo($('nextBtn')),DEMO_END)")
    p.rep("function start(){\n  if(!start.go){", "function start(){\n  ssPlay();\n  if(!start.go){")
    p.rep("function idle(over){\n  demoStop();", "function idle(over){\n  if(!over) ssSetup();\n  demoStop();")
    p.rep(p.s[p.s.index('// space bar: pause / resume (starts when nothing is running)'):p.s.index("window.addEventListener('keyup',e=>{ if(spaceKey(e)) e.preventDefault(); });")+77], '')
    p.rep("renderSets(); renderChroma(); syncChroma(); syncSteps(); syncMute(); idle();\n})();",
      SS + SP + CIN + SSON + """dguNoFooter(root.host, root.querySelector('.wrap'), ()=>root.querySelector('.wrap').classList.contains('ss-play'));
dguSpace({host:root.host, act:()=>{ if(ssOn()) return dguTap(ssInit.o.go); if(!S||S.over) dguTap($('nextBtn')); else togglePause(); }});
{ const st=document.createElement('style'); st.textContent='.cinb #board g,.cinb #board path{visibility:hidden}.wrap.ss-play .ss-top{margin-bottom:-53px;position:relative;z-index:2;pointer-events:none}.wrap.ss-play .ss-top>*{pointer-events:auto}.wrap.ss-play #progress{padding-left:132px;min-height:37px;display:flex;align-items:center}'; root.appendChild(st); } // counter on the Settings button's row (CJ Nov 22: fit under the header)
ssInit({root, wrap:root.querySelector('.wrap'), play:['header','#setup'], setup:['.controls'],
  placeTop:t=>$('session').prepend(t), startBtn:$('nextBtn'), placeGo:g=>$('session').appendChild(g),
  stop:()=>{ prepCancel($('session')); $('nextBtn').disabled=false; idle(); }});
renderSets(); renderChroma(); syncChroma(); syncSteps(); syncMute(); idle();
})();""")

@tool('find-the-number', P + 'chord-numbers/dojo/number-the-chords-codeblock.html')
def ftnum(p):
    p.rep("stopDemo(); audio(); drawRow(null); drawChart(null); syncKey(); $('nextBtn').disabled=true;", "stopDemo(); audio(); drawRow(null); drawChart(null); syncKey(); $('progress').innerHTML=''; $('nextBtn').disabled=true;")  # no "Example" tag during the count-in
    p.rep("tip('Press Start when ready',$('nextBtn'),", "tip('Press Start when ready',ssGo($('nextBtn')),")
    p.rep("function start(){\n  if(!start.go){", "function start(){\n  ssPlay();\n  if(!start.go){")
    p.rep("function idle(over){\n  if(S) clearT();", "function idle(over){\n  if(!over) ssSetup();\n  if(S) clearT();")
    p.rep("renderSets(); syncMute(); idle();\n})();",
      SS + SP + CIN + SSON + """dguNoFooter(root.host, root.querySelector('.wrap'), ()=>root.querySelector('.wrap').classList.contains('ss-play'));
dguSpace({host:root.host, act:()=>{ if(ssOn()) return dguTap(ssInit.o.go); if(!S||S.over) dguTap($('nextBtn')); else togglePause(); }});
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
    i = p.s.index('// space bar: pause / resume (starts when nothing is playing).'); j = p.s.index('\n});\n', i) + 4
    p.rep(p.s[i:j], '')
    p.rep("renderSetup(); syncMute(); idleView();\n})();",
      SS + SP + CIN + SSON + """dguNoFooter(root.host, root.querySelector('.wrap'), ()=>root.querySelector('.wrap').classList.contains('ss-play'));
{ const st=document.createElement('style'); st.textContent='.ss-play .coach{display:none!important}'; root.appendChild(st); } // the hidden demo box made the page taller while running
dguSpace({host:root.host, act:()=>{ if(ssOn()) return dguTap(ssInit.o.go); if(!S||S.over) dguTap($('nextBtn')); else togglePause(); }});
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
      "\n" + SS + SP + SSON + """dguNoFooter(root.host, root.querySelector('.wrap'), ()=>root.querySelector('.wrap').classList.contains('ss-play'));
dguSpace({host:root.host, act:()=>{ if(ssOn()) return dguTap(ssInit.o.go); dguTap($('go')); }});
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
    i = p.s.index('  // Space bar starts and stops the metronome'); j = p.s.index('    run ? stop() : start();\n  });\n', i) + 34
    p.rep(p.s[i:j], '''  // Space bar (CJ Nov 22): starts / stops the metronome, stops a take or sync, plays a take's results; never scrolls the page
  dguNoFooter(root.host, root.querySelector('.w'), function () { return root.querySelector('.w').classList.contains('ss-play'); });
  dguSpace({ host: root.host, act: function () {
    var w = root.querySelector('.w');
    if (busy()) { if (rec.state === 'rec' || rec.state === 'end') stop(); return; }
    if (w.classList.contains('gate')) return;
    if (chartOn()) { if (run) stop(); listen(); return; }
    if (!w.classList.contains('ss-play')) { dguTap(ssInit.o && ssInit.o.go); return; }
    if (w.classList.contains('m-rec')) { if (run) stop(); return; }
    run ? stop() : start();
  } });
''')
    p.rep("  setBpm(st.bpm); refresh(); timer(-1);\n  DMok = true; demoGo();\n})();",
      "  setBpm(st.bpm); refresh(); timer(-1);\n  DMok = true; demoGo();\n" + SS + SP + CIN + RN + """  dguRecNote($('mode'), root.querySelector('.hd'));
  (function () { var st = document.createElement('style'); st.textContent = '.w.ss-play .bt{height:28px!important;font-size:15px!important}.w.ss-play .btns{gap:6px}.w.ss-play .btns .btn{padding-top:7px!important;padding-bottom:7px!important}'; root.appendChild(st); })(); // compact under the diagram (CJ Nov 22)

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

    p.rep("settings.tone='acoustic';\nrenderInst();", SP + RN + FTNC + """dguRecNote($('mode'));
// Space bar (CJ Nov 22): Start on the settings screen, pause / resume while running, Play again at the end; never scrolls the page
dguNoFooter(root.host, root.querySelector('.wrap'), ()=>/w-play|w-done/.test(root.querySelector('.wrap').className));
dguSpace({host:root.host, act:()=>{ if(S&&S.lead) return; if(!S||S.over){ dguTap($('dnAgain'))||dguTap($('nextBtn')); } else togglePause(); }});
settings.tone='acoustic';
renderInst();""")

def build(name):
    src, f = TOOLS[name]
    p = Patch(open(src, encoding='utf-8').read())
    f(p)
    # Remember the audio input the member used last, shared by every tool (localStorage 'dgu-mic', CJ Nov 22)
    MIC = open(P + 'space-bar/mic.js', encoding='utf-8').read().split('*/', 1)[1].strip()  # self-defining window.dguMic
    M = 'window.dguMic'
    if name == 'find-the-note':
        p.rep("dev:store.get('dev','')", "dev:store.get('dev','')||" + MIC + ".id()")
        p.rep("R.dev=st.deviceId||R.dev;", "R.dev=st.deviceId||R.dev; if(R.dev){ store.set('dev',R.dev); " + M + ".save(tr); }")
        p.rep("openStream(R.dev).then(()=>{ R.state='idle'", M + ".pick(R.dev).then(id=>{ R.dev=id; return openStream(id); }).then(()=>{ R.state='idle'")
    if name == 'chord-trainer':
        p.rep("} catch (e) {}\n  MEAS = st.bars; BPC", "} catch (e) {}\n  if (!st.dev) st.dev = " + MIC + ".id();\n  MEAS = st.bars; BPC")
        p.rep("rec.dev = set.deviceId || '';", "rec.dev = set.deviceId || ''; if (rec.dev) { st.dev = rec.dev; save(); " + M + ".save(tr); }")
        p.rep("openStream(st.dev).then(function () {", M + ".pick(st.dev).then(function (id) { st.dev = id; return openStream(id); }).then(function () {")
    if name == 'chord-quality-evaluator':
        p.rep("const save = () => { try { localStorage.setItem('dgu-nqe', JSON.stringify(st)); } catch (e) {} };",
              "try { if (!('input' in JSON.parse(localStorage.getItem('dgu-nqe') || '{}'))) st.input = " + MIC + ".id(); } catch (e) {}\n"
              "const save = () => { try { localStorage.setItem('dgu-nqe', JSON.stringify(st)); } catch (e) {} };")
        p.rep("stream = await navigator.mediaDevices.getUserMedia({ audio: st.input ?", "st.input = await " + M + ".pick(st.input, true);\n      stream = await navigator.mediaDevices.getUserMedia({ audio: st.input ?")
        p.rep("    fillInputs();\n  } catch (e) {\n    stream = null;", "    if (st.input) { " + M + ".save(stream.getAudioTracks()[0]); save(); }\n    fillInputs();\n  } catch (e) {\n    stream = null;")
    # Back button: simple clean arrow instead of the circular undo arrow (CJ Nov 22)
    p.s = p.s.replace('<path d=\\"M3 12a9 9 0 1 0 3-6.7\\"/><path d=\\"M3 4v5h5\\"/>', '<path d=\\"M19 12H5\\"/><path d=\\"M11 18l-6-6 6-6\\"/>')
    os.makedirs(os.path.join(here, 'out'), exist_ok=True)
    open(os.path.join(here, 'out', name + '-codeblock.html'), 'w', encoding='utf-8').write(p.s)
    prev = ('<!doctype html><meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>' + name + '</title>\n'
            '<style>html,body{margin:0;background:#000}</style>\n<script>' + open(GUITAR, encoding='utf-8').read() + '</script>\n' + p.s)
    open(os.path.join(here, 'out', name + '-preview.html'), 'w', encoding='utf-8').write(prev)
    print('ok', name, len(p.s) // 1024, 'KB')

for n in (sys.argv[1:] or TOOLS): build(n)
