"""22 - USB enumeration anatomy.

Prints what the host learns the moment the board plugs in: the board identity and
the HID interfaces it exposes (usage page / usage). This is the "who are you?"
handshake every USB device goes through -- and why a device claiming to be a
keyboard is simply believed.

No arming -- it prints once over serial, then lights the ring blue.
"""

import os
import time
import usb_hid
from adafruit_circuitplayground import cp

try:
    import supervisor
except ImportError:
    supervisor = None

print("=== USB enumeration anatomy ===")
try:
    u = os.uname()
    print("board:  ", u.machine)
    print("version:", u.version)
except Exception as e:  # noqa: BLE001
    print("uname unavailable:", e)

print("HID interfaces advertised to the host:")
for d in usb_hid.devices:
    try:
        print("  usage_page=0x%02X  usage=0x%02X" % (d.usage_page, d.usage))
    except Exception as e:  # noqa: BLE001
        print("  (device)", e)

if supervisor is not None:
    try:
        print("serial/CDC connected:", supervisor.runtime.usb_connected)
    except Exception:  # noqa: BLE001
        pass

print("The host trusts all of the above on sight -- that's the lesson.\n")

cp.pixels.brightness = 0.2
cp.pixels.fill((0, 0, 30))
while True:
    time.sleep(1)
