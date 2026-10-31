"""16 - Logic bomb.

Fires only when several conditions line up at once: armed, AND the board is warm
(hold it / breathe on it), AND the room is dark (cover the light sensor). Two
pixels show which conditions are met; when all are true it "detonates" (benign
rainbow + tone). That multi-condition gate is what makes logic bombs sneaky.

ARM: slide switch left. Make it warm AND dark to detonate. Toggle off to re-arm.
"""

import time
from adafruit_circuitplayground import cp

WARM_C = 29.0   # hold the board to push its temp above this
DARK = 5        # cover the light sensor to drop below this


def detonate():
    print("conditions aligned -> detonate (benign)")
    for j in range(64):
        for i in range(10):
            cp.pixels[i] = ((i * 25 + j * 4) % 255, (j * 6) % 255, (255 - j * 4) % 255)
        cp.start_tone(400 + j * 15)
        time.sleep(0.02)
    cp.stop_tone()
    cp.pixels.fill((0, 0, 0))


fired = False
while True:
    if cp.switch:
        warm = cp.temperature > WARM_C
        dark = cp.light < DARK
        cp.pixels.fill((0, 0, 0))
        cp.pixels[0] = (0, 40, 0) if warm else (40, 0, 0)   # warm?
        cp.pixels[1] = (0, 40, 0) if dark else (40, 0, 0)   # dark?
        if warm and dark and not fired:
            detonate()
            fired = True
    else:
        fired = False
        cp.pixels.fill((0, 0, 0))
    time.sleep(0.2)
