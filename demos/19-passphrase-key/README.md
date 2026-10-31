# 19 · passphrase-key

**What:** Hold button A for ~0.8s and the board types a long passphrase + Enter — a hardware
password key. (The HID attack, used *for* you.)

**Run:** click into a text field, then hold A. Edit `PASSPHRASE` in `code.py` — **demo value
only, never a real secret in plaintext.**

**Lesson:** The same keystroke-injection that powers BadUSB also makes a handy passphrase typer.
The catch: possession of the device = the secret, and it's stored in the clear here.

**Defense:** real hardware keys (e.g. FIDO) keep the secret in a secure element and require a
user-presence tap; a plaintext passphrase on a dev board does neither.
