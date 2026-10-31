# 01 · obvious-badusb

**What:** A real HID keystroke-injection attack that flashes police lights and blares the
buzzer *before* it harmlessly opens TextEdit and types a banner.

**Arm:** slide switch to the left (speaker side). Fires once; toggle off/on to repeat.

**Lesson:** The host trusts any USB device that says "I'm a keyboard." A real BadUSB is
*silent* — this one is loud on purpose so the invisible attack becomes visible.

**Note:** ships a `boot.py` (teaching exhibit, disabled) showing how a real one would hide its
drive — press RESET after deploying if you edit it. Payload is 100% benign.
