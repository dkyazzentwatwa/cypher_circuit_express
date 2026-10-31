#!/usr/bin/env python3
"""Deploy one demo to a Circuit Playground Express.

Each demo is a self-contained code.py (single-file lean, to fit the SAMD21's
~32KB RAM), so deploy just copies the demo's files onto the CIRCUITPY drive and
makes sure the Adafruit libraries it needs are present.

Usage:
    python tools/deploy.py <demo-folder>      # e.g. 01-obvious-badusb
    python tools/deploy.py --list
    python tools/deploy.py <demo> --dest /Volumes/CIRCUITPY

Libraries:
    Install them once with circup (recommended -- it matches your CircuitPython
    version and places packages correctly):
        pip install circup
        circup --path /Volumes/CIRCUITPY install <libs from the demo's requires.txt>
    deploy.py checks what's already on the board and, for anything missing,
    prints the exact circup command. If you prefer the bundle workflow, set
    CP_BUNDLE to the bundle's lib/ folder and deploy.py will copy from there.

Config:
    CP_BUNDLE   optional path to an Adafruit bundle lib/ folder.
    CIRCUITPY   override the board mount point (else /Volumes/CIRCUITPY).

macOS 26 note: the fskit FAT driver often flips CIRCUITPY to read-only after a
write. deploy.py detects that and tells you to replug/reset the board.
"""

import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMOS = os.path.join(REPO, "demos")

DEFAULT_MOUNTS = ["/Volumes/CIRCUITPY", "/media/CIRCUITPY"]
DEFAULT_BUNDLES = [
    os.path.expanduser("~/cp-bundle/lib"),
    os.path.expanduser("~/Downloads/cp-bundle/lib"),
]
DEST = None


def list_demos():
    if not os.path.isdir(DEMOS):
        return []
    return sorted(d for d in os.listdir(DEMOS) if os.path.isdir(os.path.join(DEMOS, d)))


def find_board(override=None):
    if override:
        return override if os.path.isdir(override) else None
    env = os.environ.get("CIRCUITPY")
    if env and os.path.isdir(env):
        return env
    for m in DEFAULT_MOUNTS:
        if os.path.isdir(m):
            return m
    return None


def find_bundle():
    env = os.environ.get("CP_BUNDLE")
    if env and os.path.isdir(env):
        return env
    for b in DEFAULT_BUNDLES:
        if os.path.isdir(b):
            return b
    return None


def is_writable(board):
    probe = os.path.join(board, ".deploy_write_test")
    try:
        with open(probe, "w") as fh:
            fh.write("ok")
        os.remove(probe)
        return True
    except OSError:
        return False


def read_requires(demo_dir):
    path = os.path.join(demo_dir, "requires.txt")
    libs = []
    if os.path.isfile(path):
        with open(path) as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if line:
                    libs.append(line)
    return libs


def lib_present(board_lib, name):
    for candidate in (name, name + ".mpy", name + ".py"):
        if os.path.exists(os.path.join(board_lib, candidate)):
            return True
    return False


def copy_from_bundle(bundle, name, board_lib):
    for candidate in (name, name + ".mpy", name + ".py"):
        src = os.path.join(bundle, candidate)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(board_lib, candidate), dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            return True
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(board_lib, candidate))
            return True
    return False


def deploy(demo):
    demo_dir = os.path.join(DEMOS, demo)
    if not os.path.isdir(demo_dir):
        sys.exit("No such demo: %s\nAvailable: %s" % (demo, ", ".join(list_demos())))

    board = find_board(DEST)
    if not board:
        sys.exit("CIRCUITPY not found. Plug the board in, or set CIRCUITPY=/path.")
    if not is_writable(board):
        sys.exit("CIRCUITPY is read-only (macOS 26 fskit quirk). Unplug/replug the "
                 "board or tap RESET once, then re-run.")

    board_lib = os.path.join(board, "lib")
    os.makedirs(board_lib, exist_ok=True)

    # Libraries: copy any missing ones from a bundle if available, else report.
    libs = read_requires(demo_dir)
    bundle = find_bundle()
    missing = []
    for name in libs:
        if lib_present(board_lib, name):
            continue
        if bundle and copy_from_bundle(bundle, name, board_lib):
            continue
        missing.append(name)

    # Demo files (everything except docs/metadata).
    skip = {"README.md", "requires.txt"}
    copied = []
    for fn in sorted(os.listdir(demo_dir)):
        if fn in skip or fn.startswith("."):
            continue
        src = os.path.join(demo_dir, fn)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(board, fn))
            copied.append(fn)

    print("Deployed '%s' -> %s" % (demo, board))
    print("  files: %s" % ", ".join(copied))
    if "boot.py" in copied:
        print("  NOTE: ships boot.py -- press RESET once for it to take effect.")
    if missing:
        print("  MISSING LIBS: %s" % ", ".join(missing))
        print("  Install them with:")
        print("    circup --path %s install %s" % (board, " ".join(missing)))
    else:
        print("  libs:  all present")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if args[0] == "--list":
        print("\n".join(list_demos()) or "(no demos yet)")
        sys.exit(0)
    if "--dest" in args:
        i = args.index("--dest")
        DEST = args[i + 1]
        args = args[:i] + args[i + 2:]
    deploy(args[0])
