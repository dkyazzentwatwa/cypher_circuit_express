"""04 - IR capture & replay.

Capture the raw IR burst from any remote on the board's IR receiver, then replay
it from the board's IR LED. A plain replay attack against a protocol with no
authentication or rolling code -- which is most consumer IR.

BUTTON A: capture  (point your remote at the board and press a remote button)
BUTTON B: replay   (point the board at the TV/device)
LEDS:     dim=idle · yellow=listening · green=captured · blue=transmitting · red=nothing

Note: this replays RAW pulse timings, so it works without knowing the protocol.
Rolling-code systems (modern garage doors, cars) defeat naive replay -- that's
the point of rolling codes, and a good thing to mention on camera.
"""

import array
import time

import board
import pulseio
import pwmio

from adafruit_circuitplayground import cp

pulsein = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)
pulsein.pause()
pwm = pwmio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
pulseout = pulseio.PulseOut(pwm)

captured = None


def capture():
    global captured
    cp.pixels.fill((40, 40, 0))          # yellow: listening
    pulsein.clear()
    pulsein.resume()
    start = time.monotonic()
    while time.monotonic() - start < 5:  # listen up to 5s
        if len(pulsein) > 10:
            time.sleep(0.2)              # let the rest of the frame arrive
            break
        time.sleep(0.01)
    pulsein.pause()
    n = len(pulsein)
    if n < 4:
        cp.pixels.fill((40, 0, 0))       # red: nothing
        return
    captured = array.array("H", [pulsein[i] for i in range(n)])
    cp.pixels.fill((0, 40, 0))           # green: got it


def replay():
    if not captured:
        cp.pixels.fill((40, 0, 0))
        return
    cp.pixels.fill((0, 0, 60))           # blue: transmitting
    pulseout.send(captured)
    time.sleep(0.2)
    cp.pixels.fill((0, 40, 0))


cp.pixels.fill((5, 5, 5))                # dim idle
while True:
    if cp.button_a:
        capture()
        while cp.button_a:
            time.sleep(0.02)
    if cp.button_b:
        replay()
        while cp.button_b:
            time.sleep(0.02)
    time.sleep(0.05)
