"""05 - TOTP token (RFC 6238).

Computes the same 6-digit time-based codes your authenticator app shows, on the
board, from a shared secret. Shows HOW 2FA tokens work: HMAC-SHA1 over a 30s
time counter, then truncated to 6 digits.

SHA-1 + HMAC are implemented in pure Python here, because the SAMD21 build has
no `hashlib`/`binascii` (adafruit_hashlib can't load). Verified against CPython.

The CPX has no clock or network, so seed the time over the USB serial console:
open the console, and when prompted paste the output of `date +%s` and press
Enter. NeoPixels show the 30s window counting down; codes print to serial.
Verify with `oathtool --totp -b JBSWY3DPEHPK3PXP` or Google Authenticator.
"""

import time
from adafruit_circuitplayground import cp

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
        for j in range(16, 80):
            w.append(_rol(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1))
        a, b, c, d, e = h0, h1, h2, h3, h4
        for j in range(80):
            if j < 20:
                f = (b & c) | ((b ^ _M) & d); kk = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d; kk = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d); kk = 0x8F1BBCDC
            else:
                f = b ^ c ^ d; kk = 0xCA62C1D6
            t = (_rol(a, 5) + f + e + kk + w[j]) & _M
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
    o_pad = bytes(b ^ 0x5C for b in key)
    i_pad = bytes(b ^ 0x36 for b in key)
    return sha1(o_pad + sha1(i_pad + msg))


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
    key = _b32decode(secret_b32)
    counter = int(for_time // STEP)
    h = hmac_sha1(key, counter.to_bytes(8, "big"))
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
