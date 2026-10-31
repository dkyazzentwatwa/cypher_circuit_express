# Ethics & Authorized Use

This project exists to **teach** security concepts and help people defend against them. Read
this before running anything.

## The rules

- **Your own hardware only.** Run the HID/BadUSB demos against a computer you own or a
  throwaway VM. Injecting keystrokes into someone else's machine is unauthorized access and is
  illegal in most places, regardless of intent.
- **Authorization is required** for any test against a system you don't own. "It was just a
  demo" is not a defense.
- **The payloads here are deliberately harmless** — they open a text editor and type a banner,
  blink a hardcoded demo string, or replay an IR code you captured from your own remote. They
  do **not** read, collect, or steal anything from the host. Keep it that way.
- **This is for awareness and defense.** Each demo's README includes the real-world lesson and,
  where relevant, how to defend against the technique. That's the point.

## What this project will not do

- No credential capture, no reading host files, no real data exfiltration.
- No stealth/persistence tooling. One demo *shows and explains* how a real BadUSB would hide
  its drive (`storage.disable_usb_drive()`), because understanding evasion is part of defense —
  but it ships nothing weaponized.
- Nothing targeting networks, people, or systems you aren't authorized to test.

If you adapt these demos, keep them on the right side of that line.
