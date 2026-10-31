"""09 - Environmental trigger.

A guarded payload that fires only when the room is dark (cover the light sensor,
or kill the lights). Real malware does this -- it waits for conditions that mean
"nobody's watching" before acting, to dodge sandboxes and onlookers.

Single-file + memory-lean: adafruit_hid imported only at fire time.

ARM:   slide the switch left (yellow = armed, waiting). It fires once the light
       sensor reads dark. Toggle off/on to re-arm.
"""

import gc
import time
from adafruit_circuitplayground import cp

DARK = 5  # cp.light is ~0-320; cover the sensor to drop below this
BANNER = "Fired only once the room went dark. Malware waits for the right moment too."


def payload():
    gc.collect()
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    time.sleep(2)
    kbd.send(Keycode.GUI, Keycode.SPACE)
    time.sleep(0.6)
    layout.write("TextEdit")
    time.sleep(0.4)
    kbd.send(Keycode.ENTER)
    time.sleep(1.5)
    kbd.send(Keycode.GUI, Keycode.N)
    time.sleep(0.8)
    layout.write(BANNER)


fired = False
while True:
    if cp.switch:
        if not fired:
            if cp.light < DARK:
                payload()
                fired = True
            else:
                cp.pixels.fill((20, 20, 0))   # armed, waiting for dark
    else:
        fired = False
        cp.pixels.fill((0, 0, 0))
    time.sleep(0.1)
