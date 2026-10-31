# 07 · ducky-runner

**What:** A tiny DuckyScript-like interpreter — reads `/payload.txt` off the board and types it.
The ships-with payload harmlessly opens TextEdit and types two lines.

**Arm:** slide switch to the left. Edit `payload.txt` to change the payload — no code change needed.

**Commands:** `REM`/`#`, `DELAY <ms>`, `STRING <text>`, `STRINGLN <text>`, `ENTER`, `TAB`,
`ESCAPE`, and combos like `GUI SPACE`, `GUI N`, `CTRL ALT T`.

**Lesson:** Payloads are portable data — the same hardware runs whatever script you drop in.
Keep yours benign (see [ETHICS.md](../../ETHICS.md)).
