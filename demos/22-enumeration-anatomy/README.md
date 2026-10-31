# 22 · enumeration-anatomy

**What:** Prints what the host learns on plug-in — the board identity and the HID interfaces it
advertises (usage page / usage) — then lights the ring blue.

**Run:** open the serial console and plug in / reset. Read the handshake.

**Lesson:** Enumeration is the "who are you?" step every USB device goes through. A device that
says "I'm a keyboard" is simply believed — no proof required. That trust is what BadUSB abuses.

**Defense:** USB device allow-listing by VID/PID/usage; alerting on unexpected new HID devices.
