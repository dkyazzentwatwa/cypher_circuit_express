"""05 - TOTP token (RFC 6238).

Computes the same 6-digit time-based codes your authenticator app shows, on the
board, from a shared secret. Shows HOW 2FA tokens work: HMAC-SHA1 over a 30s
time counter, then truncated to 6 digits.

The CPX has no clock or network, so seed the time over the USB serial console:
open the console, and when prompted paste the output of `date +%s` (macOS/Linux)
and press Enter. The NeoPixels show the 30s window counting down; codes print to
serial. Verify against Google Authenticator / `oathtool` with the same secret.

SECRET below is the well-known test secret "JBSWY3DPEHPK3PXP" so you can check it
against any reference TOTP tool.
"""

import time

import adafruit_hashlib as hashlib

from adafruit_circuitplayground import cp

SECRET = "JBSWY3DPEHPK3PXP"   # base32; swap for your own test secret
STEP = 30
DIGITS = 6
_B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"


def _sha1(data):
    return bytes.fromhex(hashlib.sha1(data).hexdigest())


def _hmac_sha1(key, msg):
    block = 64
    if len(key) > block:
        key = _sha1(key)
    key = key + b"\x00" * (block - len(key))
    o_pad = bytes(b ^ 0x5C for b in key)
    i_pad = bytes(b ^ 0x36 for b in key)
    return _sha1(o_pad + _sha1(i_pad + msg))


def _b32decode(s):
    s = s.strip().replace(" ", "").upper().replace("=", "")
    bits = value = 0
    out = bytearray()
    for c in s:
        value = (value << 5) | _B32.index(c)
        bits += 5
        if bits >= 8:
            bits -= 8
            out.append((value >> bits) & 0xFF)
    return bytes(out)


def totp(secret_b32, for_time):
    key = _b32decode(secret_b32)
    counter = int(for_time // STEP)
    msg = counter.to_bytes(8, "big")
    h = _hmac_sha1(key, msg)
    off = h[-1] & 0x0F
    code = ((h[off] & 0x7F) << 24 | (h[off + 1] & 0xFF) << 16 |
            (h[off + 2] & 0xFF) << 8 | (h[off + 3] & 0xFF))
    return str(code % (10 ** DIGITS)).rjust(DIGITS, "0")


print("Paste current Unix time (run `date +%s`), then Enter:")
base = int(input().strip())
boot = time.monotonic()

while True:
    now = base + (time.monotonic() - boot)
    code = totp(SECRET, now)
    remaining = STEP - int(now % STEP)
    lit = max(1, round(remaining / STEP * 10))
    cp.pixels.fill((0, 0, 0))
    color = (0, 30, 0) if remaining > 5 else (40, 20, 0)
    for i in range(lit):
        cp.pixels[i] = color
    print("TOTP:", code, " (%2ds left)" % remaining)
    time.sleep(1)
