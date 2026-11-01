"""17 - The avalanche effect.

Hashes a value and paints its SHA-256 digest across the NeoPixels (3 bytes ->
one RGB pixel). Button A increments a counter and re-hashes; button B hashes the
SAME counter plus one extra character. Watch how a tiny input change scrambles
the whole output -- that's the avalanche effect that makes hashes useful.

SHA-256 is pure Python here (the SAMD21 build has no hashlib/binascii), using a
memory-optimized 16-word rolling schedule. Verified against CPython's hashlib.
Full hex prints to serial.
"""

import gc
import time
from adafruit_circuitplayground import cp

_M = 0xffffffff
_K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
)


def _rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & _M


def sha256(msg):
    h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
         0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    ml = len(msg) * 8
    msg = bytearray(msg)
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += ml.to_bytes(8, "big")
    for i in range(0, len(msg), 64):
        w = [int.from_bytes(msg[i + j:i + j + 4], "big") for j in range(0, 64, 4)]
        a, b, c, d, e, f, g, hh = h
        for j in range(64):
            if j >= 16:
                x1 = w[(j + 1) & 15]
                x14 = w[(j + 14) & 15]
                s0 = _rotr(x1, 7) ^ _rotr(x1, 18) ^ (x1 >> 3)
                s1 = _rotr(x14, 17) ^ _rotr(x14, 19) ^ (x14 >> 10)
                w[j & 15] = (w[j & 15] + s0 + w[(j + 9) & 15] + s1) & _M
            wj = w[j & 15]
            S1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
            t1 = (hh + S1 + ((e & f) ^ ((e ^ _M) & g)) + _K[j] + wj) & _M
            S0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
            t2 = (S0 + ((a & b) ^ (a & c) ^ (b & c))) & _M
            hh, g, f, e = g, f, e, (d + t1) & _M
            d, c, b, a = c, b, a, (t1 + t2) & _M
        for n, v in enumerate((a, b, c, d, e, f, g, hh)):
            h[n] = (h[n] + v) & _M
    return b"".join(x.to_bytes(4, "big") for x in h)


def show(text):
    gc.collect()
    d = sha256(text.encode())
    for i in range(10):
        cp.pixels[i] = (d[3 * i], d[3 * i + 1], d[3 * i + 2])
    print("%-10s -> %s" % (text, "".join("%02x" % b for b in d)))


n = 0
show(str(n))
while True:
    if cp.button_a:
        n += 1
        show(str(n))                       # consecutive ints look totally different
        while cp.button_a:
            time.sleep(0.02)
    if cp.button_b:
        show(str(n) + "x")                 # same n + 1 char -> fully scrambled
        while cp.button_b:
            time.sleep(0.02)
    time.sleep(0.05)
