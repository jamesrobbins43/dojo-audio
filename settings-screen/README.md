# Settings screen for every Dojo tool (CJ, Nov 21 2026)

CJ: "I like how Find the Note has a dedicated settings screen, as long as there's a simple way to get back to Settings. Let's add that to all tools."

## The pattern
- **Settings screen** (what the tool opens on): title, Practice | Record, the settings panel, the how-to demo, and ONE big full-width Start button (`.ss-go`, accent colour, 15px padding, 19px text, radius 14px). The tool's normal button row is hidden here.
- **Exercise screen** (after Start): title, mode switch and settings are hidden. A pill button **"‹ Settings"** (`.ss-back`) sits top-left; it stops the run and goes back to the Settings screen (the demo restarts there).
- End of a round stays on the exercise screen (Go again / results), with the Settings button still there.
- The demo's last box "Press Start when ready" points at the big Start: use `ssGo(fallbackEl)` as its target.

## How to add it to a tool
1. Paste `ss.js` into the tool's script scope (anywhere before the init line).
2. Call `ssInit({...})` before the tool's first idle()/reset() call:
   - `root` (shadowRoot or document), `wrap` (outer element),
   - `play`: selectors hidden on the exercise screen (title, settings, mode switch),
   - `setup`: selectors hidden on the Settings screen (the old button row),
   - `placeTop(el)`, `placeGo(el)`: where the Settings button row and the big Start go,
   - `startBtn` (real Start; the big one mirrors its label), optional `goLabel`, `goDisabled`, `onGo`, `watch`, `css`,
   - `stop()`: stop the run and reset to idle.
3. Call `ssPlay()` at the top of start(), and `ssSetup()` when the tool returns to idle (NOT on round-over).

`patch.py` has working examples for Steps Drill, Find the Number, Numbers Play Along, Chord Quality Evaluator, Chord Trainer (Practice + Record) and Find the Note (labeled button). `test.js <tool>` screenshots setup / play / back on desktop + phone.

Live code blocks = `out/<tool>-codeblock.html` (dojo-audio branch claude/project-thread-643tf1, settings-screen/). If you rebuild one of those tools, run `python3 patch.py <tool>` on the new block before pasting.
