# 18 · entropy-source

**What:** Mixes the low bits of the light sensor, accelerometer, and a nanosecond timer into
random bytes. Press A to harvest 10 bytes → random colors + hex on serial.

**Run:** power it, press A, watch the ring and serial. No two presses match.

**Lesson:** Randomness for crypto comes from physical noise. This is a toy illustration — real
TRNGs whiten the noise and run health tests — but it shows *where* entropy originates.

**Defense angle:** weak/predictable entropy breaks keys and tokens; seeding matters.
