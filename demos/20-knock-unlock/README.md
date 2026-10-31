# 20 · knock-unlock

**What:** Tap a secret rhythm on the board to "unlock" (ring goes green); wrong rhythm → red. Uses
the accelerometer's tap detection and compares the gaps between taps.

**Run:** tap the board; default secret is 5 taps — **quick, quick, PAUSE, quick** (`S S L S`).
Pause ~1.5s after your knock to evaluate. Tune `SECRET` / `GAP` in `code.py`.

**Lesson:** Knock codes are shared-secret authentication by rhythm — memorable, but low-entropy
and observable (anyone watching can copy it).

**Defense:** don't rely on secret sequences someone can shoulder-surf; pair with a real factor.
