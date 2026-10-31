"""10 - Data vs. power ("USB condom").

You plugged in a "charger" -- but the data lines are live. This demo proves it
without typing a thing: it reads the HOST's keyboard-LED state (Caps Lock) over
USB and mirrors it on the NeoPixels. Toggle Caps Lock on your Mac and the ring
changes color -- that's a two-way data link on a cable you thought was power.

Single-file + memory-lean: adafruit_hid imported only when armed. No keystrokes
are ever sent.

ARM:  slide the switch left, then press Caps Lock on the host a few times.
"""

import gc
import time
from adafruit_circuitplayground import cp


def monitor():
    gc.collect()
    import usb_hid
    from adafruit_hid.keyboard import Keyboard

    kbd = Keyboard(usb_hid.devices)
    time.sleep(1)
    while cp.switch:
        caps = kbd.led_on(Keyboard.LED_CAPS_LOCK)
        cp.pixels.fill((60, 0, 0) if caps else (0, 30, 0))  # red=caps on, green=off
        time.sleep(0.1)
    cp.pixels.fill((0, 0, 0))


while True:
    if cp.switch:
        monitor()
    else:
        cp.pixels.brightness = 0.2
        cp.pixels.fill((20, 10, 0))
        time.sleep(0.1)
