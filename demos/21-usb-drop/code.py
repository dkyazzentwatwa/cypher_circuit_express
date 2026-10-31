"""21 - USB-drop awareness skit.

The "found a USB in the parking lot" story. No payload at all -- when armed it
just throws up a red warning animation + alarm and prints the lesson. It's the
social-engineering half of BadUSB: the attack works because a human plugs it in.

ARM: slide switch left. Toggle off to reset.
"""

import time
from adafruit_circuitplayground import cp

MSG = "You plugged in a USB you found. On a real one, the payload already ran."


def alert():
    print(MSG)
    for _ in range(3):
        for i in range(10):
            cp.pixels.fill((0, 0, 0))
            cp.pixels[i] = (60, 0, 0)
            cp.start_tone(1500)
            time.sleep(0.04)
    cp.stop_tone()
    cp.pixels.fill((0, 0, 0))


done = False
while True:
    if cp.switch:
        if not done:
            alert()
            done = True
        cp.pixels.brightness = 0.3
        cp.pixels.fill((30, 0, 0))
    else:
        done = False
        cp.pixels.fill((0, 0, 0))
    time.sleep(0.1)
