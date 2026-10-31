# 14 · captouch-trust

**What:** Touch pads A1–A7 light their pixel and print their name. Pad **A7** is a "secret" that
turns the ring green — a stand-in for a physical unlock.

**Run:** just power it and touch the pads.

**Lesson:** Physical input is trusted implicitly — if an attacker can touch it, they can drive it.
Touch/console/jumper access is a trust boundary people forget about.

**Defense:** don't treat "requires physical access" as "safe"; protect debug pads and headers.
