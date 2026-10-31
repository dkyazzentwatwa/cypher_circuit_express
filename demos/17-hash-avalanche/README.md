# 17 · hash-avalanche

**What:** Paints a SHA-256 digest across the ring (3 bytes → one RGB pixel). Button A increments
a counter and re-hashes; button B hashes the same counter plus one extra character.

**Run:** power it, open serial for the full hex, and mash A/B — the colors reshuffle completely
on the tiniest input change.

**Lesson:** The avalanche effect: flipping one input bit flips ~half the output bits. It's why you
can't guess an input from a hash, and why hashes detect tampering.
