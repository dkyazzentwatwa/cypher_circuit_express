# 11 · light-receiver

**What:** The receiving end of the optical channel. Uses the light sensor to decode the bytes
demo 02 blinks out, on-device, and prints them over serial.

**Run:** arm with the slide switch, then aim a second CPX running **demo 02** at this board's
light sensor (sensors facing, dark-ish room). Open the serial console to see `RX: ...`.

**Lesson:** Covert channels have two ends — if light can carry data out, a cheap sensor can read
it back in. `BAUD` must match the transmitter; tune the brightness margin in `code.py`.
