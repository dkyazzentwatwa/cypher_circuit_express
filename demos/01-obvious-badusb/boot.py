# boot.py - runs ONCE on power-up / hard reset (press RESET after deploying).
#
# TEACHING EXHIBIT: this is how a *real* BadUSB hides. We ship it DISABLED
# (everything commented out) on purpose -- this demo is the most OBVIOUS BadUSB,
# not a stealth one.
#
# Uncomment the lines below to show the stealth version in your video: the
# CIRCUITPY drive disappears, so a victim never sees a suspicious removable
# disk. Keystroke injection still works, because the keyboard is a separate USB
# interface from the storage drive. That contrast -- visible disk vs hidden --
# is the detection-vs-evasion lesson.
#
# WARNING: once the drive is hidden you can't just drag files to re-deploy.
# To recover: press RESET, then press RESET again while the status LED pulses to
# enter safe mode (which skips boot.py), or re-flash CircuitPython.

# import storage
# import usb_hid
# storage.disable_usb_drive()                     # hide the CIRCUITPY disk
# usb_hid.enable((usb_hid.Device.KEYBOARD,))      # expose keyboard only
