"""19 - Hardware passphrase key.

Hold button A and the board types a long, strong passphrase for you -- the same
idea as a hardware password key. The flip side is the lesson: whoever holds the
device can type the secret, so possession == the password.

Single-file + memory-lean: adafruit_hid imported only at type time.
DEMO passphrase only -- never store a real secret here in plaintext.
"""

import gc
import time
from adafruit_circuitplayground import cp

PASSPHRASE = "correct-horse-battery-staple-7f3Q!demo"  # DEMO ONLY


def type_passphrase():
    gc.collect()
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    time.sleep(0.3)
    layout.write(PASSPHRASE)
    kbd.send(Keycode.ENTER)
    cp.pixels.fill((0, 40, 0))
    time.sleep(0.3)
    cp.pixels.fill((0, 0, 0))


while True:
    if cp.button_a:                        # require an ~0.8s hold, not a tap
        start = time.monotonic()
        while cp.button_a:
            if time.monotonic() - start > 0.8:
                type_passphrase()
                while cp.button_a:
                    time.sleep(0.02)
                break
            time.sleep(0.02)
    else:
        cp.pixels.brightness = 0.1
        cp.pixels.fill((0, 10, 10))
    time.sleep(0.05)
