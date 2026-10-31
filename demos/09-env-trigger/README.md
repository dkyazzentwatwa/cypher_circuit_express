# 09 · env-trigger

**What:** A payload that fires only when the light sensor reads dark — arm it, and it waits
(yellow) until you cover the sensor or kill the lights, then types a banner.

**Arm:** slide switch to the left, then darken the sensor. Toggle off/on to re-arm.

**Lesson:** Real malware gates itself on environmental conditions ("is anyone watching?",
"am I in a sandbox?") to avoid firing at the wrong time. Tune `DARK` in `code.py`.

**Defense:** behavioral analysis over time, not just "did it do something on launch."
