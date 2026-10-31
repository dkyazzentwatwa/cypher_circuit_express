#!/usr/bin/env python3
"""Host-side decoder for the acoustic-exfil demo (STRETCH / starting point).

Records from the mic while demos/03-acoustic-exfil plays its OOK tone, measures
energy at the carrier frequency per bit window, and recovers the bytes.

The wire format is inlined below and matches demos/03-acoustic-exfil/code.py.

Deps (optional): sounddevice, numpy     ->  pip install sounddevice numpy

Usage:
    python tools/decode_acoustic.py --baud 10 --hz 2000 --seconds 8

Baseline, not turnkey: match --baud/--hz to the demo, record in a quiet room,
hold the board near the mic. A phone spectrogram app is often easier for a first
look; this script is for an automated recover.
"""

import argparse
import sys

try:
    import numpy as np
    import sounddevice as sd
except ImportError:
    sys.exit("Needs sounddevice + numpy:  pip install sounddevice numpy")

PREAMBLE = [1, 0, 1, 0, 1, 0, 1, 0]


def bytes_from_bits(bits):
    bits = list(bits)
    n = len(PREAMBLE)
    start = -1
    for k in range(0, len(bits) - n + 1):
        if bits[k:k + n] == PREAMBLE:
            start = k
            break
    if start < 0:
        return b""
    i = start + n
    out = bytearray()
    while i + 10 <= len(bits):
        if bits[i] != 1:
            break
        value = 0
        for j in range(8):
            value |= (bits[i + 1 + j] & 1) << j
        out.append(value)
        i += 10
    return bytes(out)


def goertzel_energy(block, hz, rate):
    """Energy at frequency `hz` in `block` (Goertzel algorithm)."""
    n = len(block)
    k = int(0.5 + (n * hz) / rate)
    w = 2.0 * np.pi * k / n
    coeff = 2.0 * np.cos(w)
    s_prev = s_prev2 = 0.0
    for x in block:
        s = x + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
    return s_prev2 ** 2 + s_prev ** 2 - coeff * s_prev * s_prev2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baud", type=float, default=10.0)
    ap.add_argument("--hz", type=float, default=2000.0)
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--rate", type=int, default=44100)
    args = ap.parse_args()

    print("Recording %.1fs... play the demo now." % args.seconds)
    rec = sd.rec(int(args.seconds * args.rate), samplerate=args.rate,
                 channels=1, dtype="float64")
    sd.wait()
    signal = rec.ravel()

    win = int(args.rate / args.baud)
    energies = []
    for start in range(0, len(signal) - win, win):
        energies.append(goertzel_energy(signal[start:start + win], args.hz, args.rate))

    e = np.array(energies)
    cutoff = (e.max() + e.min()) / 2.0 if len(e) else 0.0
    bits = [1 if v >= cutoff else 0 for v in e]

    print("Recovered %d bits -> %r" % (len(bits), bytes_from_bits(bits)))


if __name__ == "__main__":
    main()
