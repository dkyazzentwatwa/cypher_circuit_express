"""15 - Acoustic trigger.

Arm it, then clap (or any loud sound). The microphone detects the spike and fires
a benign action -- a green flash + beep. In a real attack that "fire" is where a
payload would run; a clap, a specific tone, or ultrasound could all be triggers.

ARM: slide switch left (blue = listening). Clap to fire. Toggle off to disarm.
"""

import time
from adafruit_circuitplayground import cp

THRESHOLD = 200   # mic level that counts as "loud"; lower = more sensitive


def fire():
    # A real payload would run here. We just make it obvious instead.
    cp.pixels.fill((0, 60, 0))
    cp.play_tone(1000, 0.2)
    print("triggered by sound")
    time.sleep(0.6)
    cp.pixels.fill((0, 0, 0))


while True:
    if cp.switch:
        cp.pixels.fill((0, 0, 15))         # listening
        if cp.loud_sound(sound_threshold=THRESHOLD):
            fire()
    else:
        cp.pixels.fill((0, 0, 0))
    time.sleep(0.03)
