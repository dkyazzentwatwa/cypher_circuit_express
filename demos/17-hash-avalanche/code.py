"""17 - The avalanche effect.

Hashes a value and paints its SHA-256 digest across the NeoPixels (3 bytes ->
one RGB pixel). Button A increments a counter and re-hashes; button B hashes the
SAME counter plus one extra character. Watch how a tiny input change scrambles
the whole output -- that's the avalanche effect that makes hashes useful.

Full hex prints to serial each time.
"""

import time
import adafruit_hashlib as hashlib
from adafruit_circuitplayground import cp


def show(text):
    hexd = hashlib.sha256(text.encode()).hexdigest()
    d = bytes.fromhex(hexd)
    for i in range(10):
        cp.pixels[i] = (d[3 * i], d[3 * i + 1], d[3 * i + 2])
    print("%-10s -> %s" % (text, hexd))


n = 0
show(str(n))
while True:
    if cp.button_a:
        n += 1
        show(str(n))                       # consecutive ints look totally different
        while cp.button_a:
            time.sleep(0.02)
    if cp.button_b:
        show(str(n) + "x")                 # same n + 1 char -> fully scrambled
        while cp.button_b:
            time.sleep(0.02)
    time.sleep(0.05)
