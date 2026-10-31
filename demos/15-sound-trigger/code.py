"""15 - Acoustic trigger.

Arm it, then clap (or any loud sound). The microphone detects the spike and fires
a benign action -- a green flash. In a real attack that "fire" is where a payload
would run; a clap, a specific tone, or ultrasound could all be triggers.

NOTE: cp.loud_sound() is NOT supported on the Circuit Playground Express, so this
reads the PDM mic directly via audiobusio and uses peak-to-peak amplitude.

ARM: slide switch left (blue = listening). Clap to fire. Toggle off to disarm.
"""

import array
import time
import board
import audiobusio
from adafruit_circuitplayground import cp

THRESHOLD = 10000   # peak-to-peak PDM amplitude counted as "loud" -- tune this
SAMPLES = 64

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)
_buf = array.array("H", [0] * SAMPLES)


def level():
    mic.record(_buf, len(_buf))
    return max(_buf) - min(_buf)


def fire():
    # A real payload would run here. We just make it obvious instead.
    cp.pixels.fill((0, 60, 0))
    print("triggered by sound")
    time.sleep(0.6)
    cp.pixels.fill((0, 0, 0))


while True:
    if cp.switch:
        cp.pixels.fill((0, 0, 15))         # listening
        pp = level()
        # print(pp)                        # uncomment to tune THRESHOLD via serial
        if pp > THRESHOLD:
            fire()
    else:
        cp.pixels.fill((0, 0, 0))
    time.sleep(0.03)
