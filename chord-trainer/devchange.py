"""Chord Trainer: refresh the Connect input list when a device is plugged in or out (devicechange), CJ Nov 23.
Run on the out files AFTER settings-screen/patch.py (which adds devList); idempotent.
Usage: python3 devchange.py FILE [FILE ...]
"""
import sys
MARK = '// refresh the input list on plug / unplug (CJ Nov 23)'
A = '  function devList() {\n'
ADD = ("  " + MARK + "\n  if (navigator.mediaDevices && navigator.mediaDevices.addEventListener) navigator.mediaDevices.addEventListener('devicechange', function () { try { devList(); } catch (e) {} });\n")
def apply(s):
    if MARK in s: return s
    assert s.count(A) == 1, s.count(A)
    return s.replace(A, ADD + A)
if __name__ == '__main__':
    for p in sys.argv[1:]:
        t = open(p, encoding='utf-8').read(); open(p, 'w', encoding='utf-8').write(apply(t)); print('ok', p)
