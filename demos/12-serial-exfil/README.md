# 12 · serial-exfil

**What:** When armed, streams a fake (clearly synthetic) datastore out over the USB serial
console — the same port you read debug output on.

**Run:** open the serial console (`screen /dev/tty.usbmodem* 115200`), then arm with the slide
switch and watch the records stream.

**Lesson:** Any readable channel is an exfil channel. The "debug" serial port is a data path out,
not just in.

**Defense:** treat debug/console interfaces as attack surface; disable them in production builds.
