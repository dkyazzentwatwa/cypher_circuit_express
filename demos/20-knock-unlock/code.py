"""20 - Knock-code unlock.

Tap a secret rhythm on the board and it "unlocks" (ring turns green); wrong
rhythm turns red. Uses the accelerometer's tap detection and compares the gaps
between taps as short/long -- a physical knock code.

Default secret: 5 taps with the rhythm quick, quick, PAUSE, quick  (S S L S).
ARM: no arming -- just tap. Pause ~1.5s after your knock to evaluate.
"""

import time
from adafruit_circuitplayground import cp

cp.detect_taps = 1
SECRET = ["S", "S", "L", "S"]   # gaps between 5 taps
GAP = 0.45                      # seconds: above this is a "long" gap


def classify(gaps):
    return ["L" if g > GAP else "S" for g in gaps]


times = []
last = time.monotonic()
cp.pixels.fill((0, 0, 20))              # blue = waiting
while True:
    if cp.tapped:
        now = time.monotonic()
        times.append(now)
        last = now
        cp.pixels.fill((20, 20, 0))
        time.sleep(0.03)
        cp.pixels.fill((0, 0, 20))
    if times and time.monotonic() - last > 1.5:
        gaps = [times[i + 1] - times[i] for i in range(len(times) - 1)]
        pattern = classify(gaps)
        if pattern == SECRET:
            print("UNLOCKED")
            cp.pixels.fill((0, 60, 0))
        else:
            print("denied:", pattern)
            cp.pixels.fill((60, 0, 0))
        time.sleep(1.5)
        times = []
        cp.pixels.fill((0, 0, 20))
    time.sleep(0.02)
