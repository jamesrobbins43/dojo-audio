"""Chord Trainer: refresh the Connect input list when a device is plugged in or out (devicechange), CJ Nov 23.
Run on the out files AFTER settings-screen/patch.py (which adds devList); idempotent.
Usage: python3 devchange.py FILE [FILE ...]
"""
import sys
MARK = '// refresh the input list on plug / unplug (CJ Nov 23)'
A = '  function devList() {\n'
ADD = ("  " + MARK + "\n  if (navigator.mediaDevices && navigator.mediaDevices.addEventListener) navigator.mediaDevices.addEventListener('devicechange', function () { try { devList(); } catch (e) {} });\n")
MARK2 = '// the input last picked in any Dojo tool wins (CJ Nov 23)'
B = "      if (typeof sv.dev === 'string') st.dev = sv.dev;\n"
ADD2 = ("      " + MARK2 + "\n      try { var _m = localStorage.getItem('dgu-mic'); if (_m) st.dev = _m[0] === '{' ? (JSON.parse(_m).id || st.dev) : _m; } catch (e) {}\n")
def apply(s):
    if MARK not in s:
        assert s.count(A) == 1, s.count(A)
        s = s.replace(A, ADD + A)
    if MARK2 not in s:
        assert s.count(B) == 1, ('B', s.count(B))
        s = s.replace(B, B + ADD2)
    return s
if __name__ == '__main__':
    for p in sys.argv[1:]:
        t = open(p, encoding='utf-8').read(); open(p, 'w', encoding='utf-8').write(apply(t)); print('ok', p)
