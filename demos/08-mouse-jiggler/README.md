# 08 · mouse-jiggler

**What:** Presents as a USB mouse and nudges the pointer back and forth while armed, so the host
never goes idle.

**Arm:** slide switch to the left — jiggles until you flip it back.

**Lesson:** HID isn't just keyboards. A "mouse" that keeps a session alive is why idle-lock
timeouts (and requiring re-auth) matter.

**Defense:** short screen-lock timeout; lock on walk-away (not just on idle).
