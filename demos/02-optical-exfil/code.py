"""02 - Optical exfiltration.

Blinks a (fake) secret out of the NeoPixels as light. A camera across the room
can recover it even if the machine has no network -- the classic air-gap
covert-channel idea. Decode with tools/decode_optical.py or a phone video.

Single-file + self-contained. The wire format (preamble + per-byte framing) is
inlined here and matched byte-for-byte in tools/decode_optical.py.

ARM:  slide switch left. A 3-blink countdown gives you time to start recording,
      then the message transmits. Toggle off/on to send again.
DATA: hardcoded demo string only -- nothing is read off the host.
"""

import time
from adafruit_circuitplayground import cp

MESSAGE = b"CPX-SECRET"       # fake "stolen" data
BAUD = 5                      # bits/sec -- low so a 30fps camera catches every bit
ON_COLOR = (255, 255, 255)
PREAMBLE = [1, 0, 1, 0, 1, 0, 1, 0]


def bits_from_bytes(data):
    """preamble, then per byte: start-bit(1) + 8 data bits LSB-first + stop-bit(0)."""
    bits = list(PREAMBLE)
    for byte in data:
        bits.append(1)
        for i in range(8):
            bits.append((byte >> i) & 1)
        bits.append(0)
    return bits


def transmit():
    for _ in range(3):                    # countdown: start your camera
        cp.pixels.fill((40, 20, 0))
        time.sleep(0.3)
        cp.pixels.fill((0, 0, 0))
        time.sleep(0.3)
    bit_time = 1.0 / BAUD
    for bit in bits_from_bytes(MESSAGE):
        cp.pixels.fill(ON_COLOR if bit else (0, 0, 0))
        time.sleep(bit_time)
    cp.pixels.fill((0, 0, 0))


while True:
    if cp.switch:                         # armed
        transmit()
        while cp.switch:                  # idle green until re-armed
            cp.pixels.fill((0, 8, 0))
            time.sleep(0.2)
    else:
        cp.pixels.fill((0, 0, 0))
    time.sleep(0.1)
