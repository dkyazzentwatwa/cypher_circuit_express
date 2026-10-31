"""07 - Ducky-style payload runner.

Reads a payload script from /payload.txt on the board and types it. A tiny
DuckyScript-like interpreter -- the point is that the *same hardware* runs any
payload you drop in the file. Swap the file, swap the attack.

Supported: REM/# (comment), DELAY <ms>, STRING <text>, STRINGLN <text>, ENTER,
TAB, ESCAPE, and modifier combos like `GUI SPACE`, `GUI N`, `CTRL ALT T`.

Single-file + memory-lean: adafruit_hid imported only at fire time.
ARM: slide switch left. Keep payloads benign -- see ETHICS.md.
"""

import gc
import time
from adafruit_circuitplayground import cp

PAYLOAD_FILE = "/payload.txt"


def run_payload():
    gc.collect()
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    time.sleep(2)

    names = {
        "ENTER": Keycode.ENTER, "TAB": Keycode.TAB, "ESCAPE": Keycode.ESCAPE,
        "ESC": Keycode.ESCAPE, "SPACE": Keycode.SPACE, "GUI": Keycode.GUI,
        "COMMAND": Keycode.GUI, "CMD": Keycode.GUI, "WINDOWS": Keycode.GUI,
        "SHIFT": Keycode.SHIFT, "CTRL": Keycode.CONTROL, "CONTROL": Keycode.CONTROL,
        "ALT": Keycode.ALT, "DELETE": Keycode.DELETE,
    }
    mods = ("GUI", "COMMAND", "CMD", "WINDOWS", "CTRL", "CONTROL", "ALT", "SHIFT")

    def keyof(tok):
        tok = tok.upper()
        if tok in names:
            return names[tok]
        if len(tok) == 1 and hasattr(Keycode, tok):
            return getattr(Keycode, tok)
        return None

    try:
        f = open(PAYLOAD_FILE)
    except OSError:
        cp.pixels.fill((40, 0, 0))         # red: no payload file
        return

    for raw in f:
        line = raw.strip()
        if not line or line.startswith("#") or line.upper().startswith("REM"):
            continue
        parts = line.split(" ", 1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""
        if cmd == "STRING":
            layout.write(arg)
        elif cmd == "STRINGLN":
            layout.write(arg)
            kbd.send(Keycode.ENTER)
        elif cmd == "DELAY":
            try:
                time.sleep(int(arg) / 1000)
            except ValueError:
                pass
        elif cmd in mods:
            keys = [keyof(cmd)] + [keyof(t) for t in arg.split()]
            keys = [k for k in keys if k]
            if keys:
                kbd.send(*keys)
        else:
            k = keyof(cmd)
            if k:
                kbd.send(k)
    f.close()
    cp.pixels.fill((0, 40, 0))
    time.sleep(0.3)
    cp.pixels.fill((0, 0, 0))


fired = False
while True:
    if cp.switch:
        if not fired:
            run_payload()
            fired = True
    else:
        fired = False
        cp.pixels.brightness = 0.1
        cp.pixels.fill((20, 0, 20))
    time.sleep(0.1)
