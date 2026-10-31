# 05 · totp-token

**What:** Generates real RFC-6238 TOTP codes (same as your authenticator app) on the board,
from the test secret `JBSWY3DPEHPK3PXP`. NeoPixels count down the 30s window; codes print to serial.

**Run:** open the serial console (`screen /dev/tty.usbmodem* 115200`), paste the output of
`date +%s` when prompted, Enter. Compare the printed code to Google Authenticator or
`oathtool --totp -b JBSWY3DPEHPK3PXP`.

**Lesson:** 2FA codes aren't magic — they're `HMAC-SHA1(secret, current_30s_window)` truncated to
6 digits. Whoever holds the secret can generate codes, which is why the secret is the crown jewel.

**Note:** the CPX has no RTC/network, so time is seeded over serial — concept demo, not a
standalone token.
