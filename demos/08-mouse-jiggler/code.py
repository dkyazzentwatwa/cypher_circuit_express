"""08 - Mouse jiggler.

Presents as a USB mouse and nudges the pointer back and forth so the host never
idles. Sysadmins use these to stop screensavers; attackers use them to keep a
session alive. Either way it shows why idle-lock matters.

Single-file + memory-lean: adafruit_hid imported only when armed. The Mouse HID
device is much lighter than the keyboard, so this one is easy on RAM.

ARM: slide the switch to the left -- jiggles while armed, stops when you flip it back.
"""

import gc
import time
from adafruit_circuitplayground import cp


def jiggle():
    gc.collect()
    import usb_hid
    from adafruit_hid.mouse import Mouse

    mouse = Mouse(usb_hid.devices)
    time.sleep(1)
    n = 0
    while cp.switch:
        mouse.move(3, 0, 0)
        time.sleep(0.2)
        mouse.move(-3, 0, 0)
        cp.pixels.fill((0, 0, 0))
        cp.pixels[n] = (0, 0, 40)          # a little "activity" chaser
        n = (n + 1) % 10
        time.sleep(0.6)
    cp.pixels.fill((0, 0, 0))


while True:
    if cp.switch:
        jiggle()
    else:
        cp.pixels.brightness = 0.1
        cp.pixels.fill((0, 0, 20))
        time.sleep(0.1)
