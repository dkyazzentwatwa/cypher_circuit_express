# 15 · sound-trigger

**What:** Arm it and clap — the mic detects the spike and fires a benign action (green flash +
beep). The "fire" is where a real payload would run.

**Arm:** slide switch to the left (blue = listening). Clap to trigger. Tune `THRESHOLD` in `code.py`.

**Lesson:** Triggers don't have to be digital. A clap, a specific tone, or inaudible ultrasound
can all gate malware — covert and hard to spot in logs.

**Defense:** think beyond network/keyboard triggers when reasoning about what can set code off.
