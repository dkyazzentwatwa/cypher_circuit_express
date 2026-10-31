"""18 - Harvesting entropy from physical noise.

The SAMD21 has no hardware RNG, so where does randomness come from? Physical
noise. This mixes the low bits of the light sensor, the accelerometer, and a
nanosecond timer into random bytes. Press A to harvest 10 bytes -> colors + hex.

Educational, not cryptographic-grade -- a real TRNG whitens and health-tests its
noise. The point is *where* entropy comes from.
"""

import time
from adafruit_circuitplayground import cp


def harvest_byte():
    b = 0
    for _ in range(8):
        x, y, z = cp.acceleration
        noise = (int(cp.light)
                 ^ int(abs(x) * 1000) ^ int(abs(y) * 1000) ^ int(abs(z) * 1000)
                 ^ time.monotonic_ns())
        b = (b << 1) | (noise & 1)
        time.sleep(0.002)
    return b & 0xFF


while True:
    if cp.button_a:
        data = bytes(harvest_byte() for _ in range(10))
        for i in range(10):
            v = data[i]
            cp.pixels[i] = (v, (v * 7) & 255, (v * 13) & 255)
        print("entropy:", "".join("%02x" % x for x in data))
        while cp.button_a:
            time.sleep(0.02)
    else:
        cp.pixels.brightness = 0.1
        cp.pixels.fill((5, 5, 5))
    time.sleep(0.05)
