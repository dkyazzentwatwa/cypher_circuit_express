#!/usr/bin/env python3
"""Host-side decoder for the optical-exfil demo (STRETCH / starting point).

Point a webcam (or a phone video file) at the board while it runs
demos/02-optical-exfil. This samples the brightness of the board region over
time, slices it at the baud rate, and recovers the bytes.

The wire format (preamble + per-byte framing) is inlined below and matches
demos/02-optical-exfil/code.py byte-for-byte.

Deps (optional): opencv-python, numpy     ->  pip install opencv-python numpy

Usage:
    python tools/decode_optical.py --source 0 --baud 5
    python tools/decode_optical.py --source clip.mov --baud 5

Tunable baseline, not turnkey: lighting, framing, and the brightness threshold
all matter. Start with a low baud (5) and a dark room.
"""

import argparse
import sys

try:
    import cv2
    import numpy as np
except ImportError:
    sys.exit("Needs opencv-python + numpy:  pip install opencv-python numpy")

PREAMBLE = [1, 0, 1, 0, 1, 0, 1, 0]


def bytes_from_bits(bits):
    """Find the preamble, then read framed bytes (best-effort)."""
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
        if bits[i] != 1:                       # lost framing
            break
        value = 0
        for j in range(8):
            value |= (bits[i + 1 + j] & 1) << j
        out.append(value)
        i += 10
    return bytes(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="0", help="webcam index or video file path")
    ap.add_argument("--baud", type=float, default=5.0)
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="normalized brightness cutoff for a '1' bit (0-1)")
    args = ap.parse_args()

    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        sys.exit("Could not open source: %s" % args.source)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    samples = []
    print("Sampling brightness (Ctrl-C to stop)... fps=%.1f baud=%.1f" % (fps, args.baud))
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            flat = np.sort(gray.ravel())          # brightest 5% ~ the lit pixels
            samples.append(float(flat[int(len(flat) * 0.95):].mean()))
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()

    if not samples:
        sys.exit("No frames captured.")

    arr = np.array(samples)
    norm = (arr - arr.min()) / max(1.0, (arr.max() - arr.min()))
    step = fps / args.baud
    bits = []
    i = step / 2.0
    while i < len(norm):
        bits.append(1 if norm[int(i)] >= args.threshold else 0)
        i += step

    print("Recovered %d bits -> %r" % (len(bits), bytes_from_bits(bits)))


if __name__ == "__main__":
    main()
