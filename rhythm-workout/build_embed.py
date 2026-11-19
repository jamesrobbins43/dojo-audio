"""Squarespace Code Block for Rhythm Workout (Shadow DOM). Run: python3 build_embed.py <dojo-audio commit sha>
Audio streams from raw.githubusercontent.com (jsDelivr refuses this repo: over its 50 MB limit)."""
import json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
sha = sys.argv[1]
AUDIO_BASE = f'https://raw.githubusercontent.com/jamesrobbins43/dojo-audio/{sha}/rhythm-workout/'
src = open(os.path.join(here, '..', 'rhythm-workout.src.html'), encoding='utf-8').read()
src = src.replace('/*DIGITS*/', open(os.path.join(here, '..', 'digits-fontface.css')).read().strip(), 1)
css = src[src.index('<style>') + 7: src.index('</style>')]
html = src[src.index('</style>') + 8: src.index('<script>')].strip()
main = src[src.index('<script>') + 8: src.rindex('</script>')]
faces = ''.join(re.findall(r'@font-face\{[^}]*\}', css))
css = re.sub(r'@font-face\{[^}]*\}', '', css)
css = css.replace(':root{', ':host{', 1)
assert 'html,body{background:var(--bg)}' in css
css = css.replace('html,body{background:var(--bg)}\n', '', 1)
css = re.sub(r'(?m)^body\{', ':host{display:block;background:var(--bg);', css, count=1)
css = css.replace('  body{padding-block:20px 40px}', '  :host{padding-block:20px 40px}', 1)
css = css.replace('*{box-sizing:border-box}', '*,*::before,*::after{box-sizing:border-box}', 1)
css += '\nbutton{font:inherit}\nh1,h2,p{margin:0}\n.sub{margin-top:8px}\n'
assert main.count('const $=id=>document.getElementById(id);') == 1
main = main.replace('const $=id=>document.getElementById(id);', 'const $=id=>root.getElementById(id);', 1)
assert main.count("const AUDIO_BASE='audio/';") == 1
main = main.replace("const AUDIO_BASE='audio/';", 'const AUDIO_BASE=' + json.dumps(AUDIO_BASE) + ';', 1)
main = main.encode('ascii', 'backslashreplace').decode('ascii')
html = html.encode('ascii', 'xmlcharrefreplace').decode('ascii')
fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap">'
out = f'''<!-- Don't Give Up Dojo: Rhythm Workout. Paste this whole block into a Squarespace Code Block (Display Source off). -->
{fonts}
<style>{faces}</style>
<div id="dgu-rhythm-workout" style="background:#000"></div>
<script>
(function(){{
  var host = document.getElementById('dgu-rhythm-workout');
  if (!host || host.shadowRoot) return;
  var sec = host.closest('section');
  if (sec) {{ sec.style.background = '#000'; var sb = sec.querySelector('.section-background'); if (sb) {{ sb.style.background = '#000'; sb.innerHTML = ''; }} }}
  var blk = host.closest('.fe-block'); if (blk) {{ blk.style.gridColumn = '2 / -2'; }}
  var root = host.attachShadow({{mode:'open'}});
  root.innerHTML = '<style>' + {json.dumps(css)} + '</style>' + {json.dumps(html)};
  {main.strip()}
}})();
</script>
'''
dst = os.path.join(here, 'rhythm-workout-codeblock.html')
open(dst, 'w', encoding='utf-8').write(out)
print(dst, len(out.encode()) // 1024, 'KB')
