# 03 · acoustic-exfil

**What:** Sends the fake secret as on-off-keyed buzzer tones. A mic recovers it.

**Arm:** slide switch left → 3-beep countdown → transmit (pixels go red). Toggle off/on to resend.

**Decode:** `python tools/decode_acoustic.py --baud 10 --hz 2000 --seconds 8`, or just watch it in
any phone spectrogram app (the tone pattern is the data).

**Lesson:** Covert channels don't need a network card — a speaker is enough. This is why
high-security rooms restrict audio devices.

**Tip:** quiet room, board near the mic. `sound.send_acoustic_fsk` is an alternative that's
easier to read in a noisy spectrogram.
