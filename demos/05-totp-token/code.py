"""05 - TOTP token (RFC 6238).

Computes the same 6-digit time-based codes your authenticator app shows, on the
board, from a shared secret: HMAC-SHA1 over a 30s time counter, truncated to 6
digits.

The SAMD21 build has no hashlib/binascii, so SHA-1 + HMAC are pure Python here,
with a memory-optimized 16-word rolling schedule (the naive 80-word version runs
out of RAM on this chip). Verified against CPython's hmac/hashlib. We drive the
NeoPixels directly via `neopixel` (not the heavier circuitplayground library) to
leave room for the HMAC.

The CPX has no clock/network, so seed the time over the USB serial console: open
it, and when prompted paste the output of `date +%s` and press Enter. NeoPixels
show the 30s window; codes print to serial. Verify with
`oathtool --totp -b JBSWY3DPEHPK3PXP` or Google Authenticator.
"""

import gc
import time
import board
import neopixel

_M = 0xffffffff


def _rol(x, n):
    return ((x << n) | (x >> (32 - n))) & _M


def sha1(msg):
    h0, h1, h2, h3, h4 = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)
    ml = len(msg) * 8
    msg = bytearray(msg)
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += ml.to_bytes(8, "big")
    for i in range(0, len(msg), 64):
        w = [int.from_bytes(msg[i + j:i + j + 4], "big") for j in range(0, 64, 4)]
        a, b, c, d, e = h0, h1, h2, h3, h4
        for j in range(80):
            if j >= 16:
                w[j & 15] = _rol(w[(j + 13) & 15] ^ w[(j + 8) & 15] ^
                                 w[(j + 2) & 15] ^ w[j & 15], 1)
            wj = w[j & 15]
            if j < 20:
                f = (b & c) | ((b ^ _M) & d); kk = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d; kk = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d); kk = 0x8F1BBCDC
            else:
                f = b ^ c ^ d; kk = 0xCA62C1D6
            t = (_rol(a, 5) + f + e + kk + wj) & _M
            e, d, c, b, a = d, c, _rol(b, 30), a, t
        h0 = (h0 + a) & _M
        h1 = (h1 + b) & _M
        h2 = (h2 + c) & _M
        h3 = (h3 + d) & _M
        h4 = (h4 + e) & _M
    return b"".join(x.to_bytes(4, "big") for x in (h0, h1, h2, h3, h4))


def hmac_sha1(key, msg):
    if len(key) > 64:
        key = sha1(key)
    key = key + b"\x00" * (64 - len(key))
    return sha1(bytes(x ^ 0x5C for x in key) + sha1(bytes(x ^ 0x36 for x in key) + msg))


SECRET = "JBSWY3DPEHPK3PXP"   # base32; swap for your own test secret
STEP = 30
DIGITS = 6
_B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"


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
    h = hmac_sha1(_b32decode(secret_b32), int(for_time // STEP).to_bytes(8, "big"))
    off = h[-1] & 0x0F
    code = ((h[off] & 0x7F) << 24 | (h[off + 1] & 0xFF) << 16 |
            (h[off + 2] & 0xFF) << 8 | (h[off + 3] & 0xFF))
    # CircuitPython str has no .rjust(), so zero-pad with % formatting.
    return ("%0" + str(DIGITS) + "d") % (code % (10 ** DIGITS))


pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.3, auto_write=True)

print("Paste current Unix time (run `date +%s`), then Enter:")
base = int(input().strip())
boot = time.monotonic()

# NOTE: on SAMD21, time.monotonic() is a float32 and the Unix epoch (~1.7e9) is
# well past its precision — adding a float delta to `base` as a float would
# corrupt `now`. So keep `now` as an int by converting the elapsed delta before
# the add.
while True:
    gc.collect()
    now = base + int(time.monotonic() - boot)
    code = totp(SECRET, now)
    remaining = STEP - (now % STEP)
    lit = max(1, round(remaining / STEP * 10))
    pixels.fill((0, 0, 0))
    color = (0, 30, 0) if remaining > 5 else (40, 20, 0)
    for i in range(lit):
        pixels[i] = color
    print("TOTP:", code, " (%2ds left)" % remaining)
    time.sleep(1)
