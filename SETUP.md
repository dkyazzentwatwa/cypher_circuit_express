# Setup

Everything here targets **macOS** (the HID demos use Spotlight and Mac keycodes). Windows /
Linux notes are in code comments where they differ.

## 1. Flash CircuitPython

1. Grab the latest **CircuitPython 9.x** `.uf2` for the Circuit Playground Express from
   <https://circuitpython.org/board/circuitplayground_express/>.
2. Double-tap the board's **RESET** button — a `CPLAYBOOT` drive appears.
3. Drag the `.uf2` onto `CPLAYBOOT`. The board reboots and a **`CIRCUITPY`** drive appears at
   `/Volumes/CIRCUITPY`.

## 2. Install the libraries (circup — recommended)

The demos use prebuilt libraries (HID, IR, etc.) that don't ship with CircuitPython.
[`circup`](https://github.com/adafruit/circup) is the easiest way — it auto-matches your
CircuitPython version, installs packages correctly, and pulls dependencies:

```bash
pip install circup
circup --path /Volumes/CIRCUITPY install adafruit_hid adafruit_circuitplayground
```

Those two cover every demo. Everything else the demos use (`pulseio`, `audiobusio`,
`board`, `usb_hid`, `os`) is built into CircuitPython, and SHA-1/SHA-256 are implemented
in pure Python in demos 05/17 (the SAMD21 build has no `hashlib`/`binascii`).

Each demo's `requires.txt` lists exactly what it needs; `tools/deploy.py` prints the precise
`circup` command for anything still missing on the board.

<details><summary>Alternative: the bundle + CP_BUNDLE workflow</summary>

Download the bundle matching CircuitPython 9.x from <https://circuitpython.org/libraries>,
unzip it, and point `deploy.py` at its `lib/` folder:

```bash
export CP_BUNDLE=~/cp-bundle/lib
```

`deploy.py` will then copy any missing libs from there instead of asking you to run circup.
</details>

## 3. Deploy a demo

```bash
python tools/deploy.py 01-obvious-badusb
```

Each demo is a self-contained `code.py` (single-file, to fit the SAMD21's ~32KB RAM), so this
just copies the demo's files (`code.py`, and `boot.py` / `payload.txt` if present) onto
`/Volumes/CIRCUITPY` and confirms the libraries it needs are installed. The board auto-reloads
when the copy finishes. List what's available:

```bash
python tools/deploy.py --list
```

> **`boot.py` note:** some demos include a `boot.py` (e.g. to enable the HID keyboard or to
> demonstrate hiding the drive). `boot.py` only runs on a **power cycle / hard reset**, not on
> a normal file-save reload. After deploying a demo that has one, press **RESET** once.

## 4. Run / film it

Each `demos/NN-name/README.md` says how the demo is **armed** — almost always the **slide
switch** or **holding a button** — so nothing fires the instant you plug in. Arm it, and film.

### macOS gotchas (HID demos)

- **First plug-in:** macOS may pop the *Keyboard Setup Assistant* ("identify your keyboard").
  Dismiss it / press the key it asks for once; it won't ask again for that board.
- **Timing:** the code waits a couple of seconds after boot before typing, so USB fully
  enumerates first. If keystrokes get dropped, increase the `time.sleep()` at the top of `code.py`.
- **Spotlight:** demos open apps via `cmd-space`. If you've remapped Spotlight, adjust the
  `kbd.send(Keycode.GUI, Keycode.SPACE)` line in the demo's `code.py`.

## Troubleshooting

- **`Read-only file system` when copying (macOS 26):** the new `fskit` FAT driver often flips
  CIRCUITPY to read-only after a write. **Unplug/replug the board or tap RESET once**, then retry.
  `deploy.py` detects this and tells you. It's a macOS quirk, not a board fault.
- **`MemoryError` on the board:** the SAMD21 has only ~32KB RAM. These demos are single-file and
  lean for that reason — if you add imports, import heavy libs lazily (inside the function that
  uses them) and call `gc.collect()` first, as demo 01 does.
- **`ImportError` on the board:** a required library isn't installed — run the `circup` command
  `deploy.py` prints (or check the demo's `requires.txt`).
- **Nothing happens:** confirm the demo is armed (slide switch / button), and that you pressed
  RESET if it ships a `boot.py`.
- **See errors:** open the serial console — `screen /dev/tty.usbmodem* 115200`, or use the Mu
  editor / `tio`. CircuitPython prints tracebacks there.
