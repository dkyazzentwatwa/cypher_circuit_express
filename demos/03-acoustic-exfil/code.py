"""03 - Acoustic exfiltration.

Same fake secret as demo 02, but sent as sound: on-off-keyed tones from the
buzzer. A phone mic + spectrogram app (or tools/decode_acoustic.py) recovers it.
The sibling of the optical channel -- data leaves as audio.

Single-file + self-contained. Same inlined wire format as demo 02, matched by
tools/decode_acoustic.py.

ARM:  slide switch left. A 3-beep countdown, then transmit. Toggle off/on to resend.
DATA: hardcoded demo string only.
"""

import time
from adafruit_circuitplayground import cp

MESSAGE = b"CPX-SECRET"
BAUD = 10        # bits/sec
HZ = 2000        # carrier tone
PREAMBLE = [1, 0, 1, 0, 1, 0, 1, 0]


def bits_from_bytes(data):
    bits = list(PREAMBLE)
    for byte in data:
        bits.append(1)
        for i in range(8):
            bits.append((byte >> i) & 1)
        bits.append(0)
    return bits


def transmit():
    for _ in range(3):                    # countdown beeps
        cp.pixels.fill((0, 0, 40))
        cp.play_tone(880, 0.1)
        cp.pixels.fill((0, 0, 0))
        time.sleep(0.2)
    cp.pixels.fill((40, 0, 0))            # red = transmitting
    bit_time = 1.0 / BAUD
    for bit in bits_from_bytes(MESSAGE):
        if bit:
            cp.start_tone(HZ)
        else:
            cp.stop_tone()
        time.sleep(bit_time)
    cp.stop_tone()
    cp.pixels.fill((0, 0, 0))


while True:
    if cp.switch:
        transmit()
        while cp.switch:
            time.sleep(0.2)
    else:
        time.sleep(0.1)
