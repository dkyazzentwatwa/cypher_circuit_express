"""14 - Capacitive-touch trust.

The 7 touch pads (A1-A7) are input the board trusts just because something
touched them. Touch a pad -> its pixel lights and the pad name prints. Pad A7 is
a "secret" that turns the whole ring green -- a stand-in for a physical unlock.

ARM: no arming needed -- touch the pads.
"""

import time
from adafruit_circuitplayground import cp

PADS = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]


while True:
    cp.pixels.fill((0, 0, 0))
    secret = getattr(cp, "touch_A7")
    if secret:
        cp.pixels.fill((0, 50, 0))         # "unlocked"
        print("touch A7 -> SECRET pad (unlock)")
        time.sleep(0.2)
    else:
        for i, pad in enumerate(PADS):
            if getattr(cp, "touch_" + pad):
                cp.pixels[i] = (0, 40, 40)
                print("touch", pad)
    time.sleep(0.1)
