"""12 - Exfiltration over the USB serial console.

When armed, the board "drains" a fake datastore line-by-line over the USB CDC
serial console -- the same console you read tracebacks on. Any readable channel
is an exfil channel. All records here are synthetic and labelled.

ARM: slide switch left. Open the serial console to watch it stream.
"""

import time
from adafruit_circuitplayground import cp

FAKE_RECORDS = [
    "DEMO user=alice role=admin  (synthetic)",
    "DEMO token=sk-demo-0000-not-a-real-key  (synthetic)",
    "DEMO card=XXXX-XXXX-XXXX-1234 exp=12/30  (synthetic)",
    "DEMO note=this all came out over the serial 'debug' port  (synthetic)",
]


def drain():
    print("[exfil] draining fake datastore over USB serial...")
    for i, row in enumerate(FAKE_RECORDS):
        print("[exfil]", row)
        cp.pixels.fill((0, 0, 0))
        cp.pixels[i % 10] = (40, 0, 0)
        time.sleep(0.6)
    print("[exfil] done -- %d records.\n" % len(FAKE_RECORDS))
    cp.pixels.fill((0, 0, 0))


done = False
while True:
    if cp.switch:
        if not done:
            drain()
            done = True
    else:
        done = False
        cp.pixels.brightness = 0.1
        cp.pixels.fill((10, 0, 0))
    time.sleep(0.1)
