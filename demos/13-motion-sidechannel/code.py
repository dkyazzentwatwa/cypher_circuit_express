"""13 - Motion side channel.

The accelerometer feels desk vibration. Type on the same desk (or tap near the
board) and it counts "keystroke-like" events from the vibration alone -- a crude
version of the real research where motion sensors infer what you typed.

ARM: no arming needed -- it just watches. Tap the desk near the board.
"""

import time
from adafruit_circuitplayground import cp

THRESHOLD = 3.0   # m/s^2 deviation from rest that counts as an "event"
REST = 9.8        # ~1g at rest


def magnitude():
    x, y, z = cp.acceleration
    return (x * x + y * y + z * z) ** 0.5


count = 0
last = 0.0
while True:
    if abs(magnitude() - REST) > THRESHOLD and time.monotonic() - last > 0.15:
        count += 1
        last = time.monotonic()
        print("event #%d (vibration detected)" % count)
        cp.pixels[count % 10] = (40, 0, 40)
        time.sleep(0.05)
        cp.pixels.fill((0, 0, 0))
    time.sleep(0.005)
