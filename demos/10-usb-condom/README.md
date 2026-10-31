# 10 · usb-condom

**What:** Proves a "charge" cable is a live data link — without typing anything. The board reads
the host's Caps Lock LED state over USB and mirrors it on the ring (red = caps on, green = off).

**Arm:** slide switch to the left, then toggle **Caps Lock** on your Mac — watch the ring flip.

**Lesson:** Data vs. power. If the data lines are connected, the device has a two-way link to
your machine. This is why "USB condoms" (power-only adapters) and not trusting random chargers
matter.

**Note:** macOS may need the keyboard "identified" once before Caps Lock LED reports flow.
