# 02 · optical-exfil

**What:** Blinks a fake secret (`CPX-SECRET`) out of the NeoPixels as light, using the shared
`codec` framing. A camera recovers the bytes.

**Arm:** slide switch left → 3-blink countdown (start recording) → transmit. Toggle off/on to resend.

**Decode:** `python tools/decode_optical.py --source 0 --baud 5`, or record video and run with `--source clip.mov`.

**Lesson:** An air-gapped machine with no network can still leak data — as light. Covering a
status LED isn't paranoia.

**Tip:** darker room + steady framing = clean decode. Lower `BAUD` if bits get missed.
