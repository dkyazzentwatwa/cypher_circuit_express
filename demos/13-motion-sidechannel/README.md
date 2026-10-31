# 13 · motion-sidechannel

**What:** Counts "keystroke-like" events from desk vibration picked up by the accelerometer —
tap near the board or type on the same surface and watch it register (pixels + serial).

**Run:** just power it; tap the desk near the board. Tune `THRESHOLD` in `code.py`.

**Lesson:** Motion sensors are a side channel. Real research has recovered typed text from phone
accelerometers sitting next to a keyboard — sensors you don't think of as "input" can leak it.

**Defense:** rate-limit / gate motion-sensor access; be wary of untrusted apps reading them.
