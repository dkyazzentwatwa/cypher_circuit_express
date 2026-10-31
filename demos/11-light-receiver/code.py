"""11 - Optical receiver (the other end of demo 02).

Uses the light sensor to RECEIVE the optical bytes that demo 02 blinks out. Aim
a second CPX running demo 02 at this board's light sensor (or flash the pattern
with a phone), and this decodes it on-device and prints the recovered bytes.

Same wire format as demo 02, inlined below. This is a tunable baseline -- on-
device optical sync is finicky; calibrate in a dark-ish room, sensors facing.

ARM: slide switch left to start listening. BAUD must match the transmitter (5).
"""

import time
from adafruit_circuitplayground import cp

BAUD = 5
PREAMBLE = [1, 0, 1, 0, 1, 0, 1, 0]
NBITS = len(PREAMBLE) + 8 * 10          # preamble + up to 8 framed bytes


def bytes_from_bits(bits):
    n = len(PREAMBLE)
    start = -1
    for k in range(len(bits) - n + 1):
        if bits[k:k + n] == PREAMBLE:
            start = k
            break
    if start < 0:
        return b""
    i = start + n
    out = bytearray()
    while i + 10 <= len(bits):
        if bits[i] != 1:
            break
        v = 0
        for j in range(8):
            v |= (bits[i + 1 + j] & 1) << j
        out.append(v)
        i += 10
    return bytes(out)


def listen():
    base = 0.0                            # calibrate ambient light
    for _ in range(20):
        base += cp.light
        time.sleep(0.01)
    thresh = base / 20 + 20               # tune this margin to your setup
    cp.pixels.fill((0, 0, 10))            # blue = listening

    t0 = time.monotonic()                 # wait for the first bright bit
    while cp.light < thresh:
        if time.monotonic() - t0 > 10:
            cp.pixels.fill((40, 0, 0))    # red = timed out
            time.sleep(1)
            return
    bit_time = 1.0 / BAUD
    time.sleep(bit_time / 2)              # sample mid-bit
    bits = []
    for _ in range(NBITS):
        bits.append(1 if cp.light >= thresh else 0)
        time.sleep(bit_time)

    data = bytes_from_bits(bits)
    print("RX:", data)
    cp.pixels.fill((0, 40, 0) if data else (40, 20, 0))
    time.sleep(1.5)


while True:
    if cp.switch:
        listen()
        while cp.switch:
            time.sleep(0.2)
    else:
        cp.pixels.fill((0, 0, 0))
    time.sleep(0.1)
