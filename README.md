# cypher_circuit_express

**One $25 dev board. 20+ hands-on cybersecurity demos.**

<p align="center">
  <a href="https://www.adafruit.com/product/3333">
    <img src="https://cdn-shop.adafruit.com/970x728/3333-05.jpg" alt="Adafruit Circuit Playground Express held in a hand, NeoPixels lit in rainbow colors" width="520">
  </a>
  <br>
  <sub><i>Photo: <a href="https://www.adafruit.com/product/3333">Adafruit — Circuit Playground Express, product 3333</a>.</i></sub>
</p>

This repo turns an [Adafruit **Circuit Playground Express**](https://www.adafruit.com/product/3333)
(CPX) into a pocket security-education lab. Every demo is a short, filmable CircuitPython
program that teaches one security concept using nothing but the board's built-in hardware —
no soldering, no extra parts. Built as source material for a series of Instagram video demos.

The headline act is an intentionally ridiculous **"most obvious BadUSB ever"**: it's a real
keystroke-injection attack that also flashes police lights and screams out of the buzzer
before it types. The point is to make an invisible, scary attack *visible* — so people
actually understand it.

> ⚠️ **Read [ETHICS.md](ETHICS.md) first.** Everything here is for learning and defense, on
> hardware you own. Payloads are deliberately harmless.

## The board (why it's great for this)

<p align="center">
  <a href="https://www.adafruit.com/product/3333">
    <img src="https://cdn-shop.adafruit.com/970x728/3333-11.jpg" alt="Top-down view of the Circuit Playground Express showing NeoPixels, buttons, slide switch, buzzer, mic, light sensor, and touch pads around the edge" width="460">
  </a>
  &nbsp;
  <a href="https://www.adafruit.com/product/3333">
    <img src="https://cdn-shop.adafruit.com/970x728/3333-08.jpg" alt="Bottom view of the Circuit Playground Express next to a US quarter for scale" width="460">
  </a>
  <br>
  <sub><i>Photos: <a href="https://www.adafruit.com/product/3333">Adafruit</a>. Round, quarter-sized, and absolutely packed.</i></sub>
</p>

Microchip ATSAMD21 (Cortex-M0+), runs CircuitPython, and over USB it enumerates as a
**trusted HID device** (keyboard/mouse) — the whole basis of BadUSB. It also packs:

- 10 RGB NeoPixels · buzzer/speaker · MEMS microphone
- light sensor · temperature sensor · 3-axis accelerometer
- IR transmit **and** receive · 7 capacitive-touch pads · 2 buttons · 1 slide switch

That sensor spread is what lets us go way past BadUSB into covert channels, side channels,
and crypto demos.

## Demo catalog

All 22 demos are implemented. Flagship demos (**bold**) were built and hardware-verified first;
demo 01 is confirmed on real hardware, and the rest are written and static-checked (flash them as
you film). Each demo is a self-contained, single-file `code.py` (see Repo layout for why).

| # | Demo | Hardware | Security lesson |
|---|------|----------|-----------------|
| **01** | **obvious-badusb** | HID + NeoPixels + buzzer | HID is trusted implicitly — never plug in unknown USB |
| **02** | **optical-exfil** | NeoPixels | Data can leave an air-gapped machine as blinking light |
| **03** | **acoustic-exfil** | buzzer | Covert acoustic channels (data as sound) |
| **04** | **ir-replay** | IR TX/RX | Capture-and-replay against unauthenticated protocols |
| **05** | **totp-token** | HID/NeoPixels | How a 2FA token derives time-based codes (RFC 6238) |
| 06 | keystroke-basics | HID | Minimal keystroke injection, guarded by the slide switch |
| 07 | ducky-runner | HID + storage | A payload interpreter (`payload.txt`) — portable attacks |
| 08 | mouse-jiggler | HID mouse | Why screen-lock timeouts matter |
| 09 | env-trigger | HID + light sensor | Environmental triggers used by real malware |
| 10 | usb-condom | HID | Data-vs-power: it talks even when you "just wanted to charge" |
| 11 | light-receiver | light sensor | The receiving end of an optical link |
| 12 | serial-exfil | USB serial | Exfiltration over the USB console |
| 13 | motion-sidechannel | accelerometer | Motion/vibration side channels |
| 14 | captouch-trust | touch pads | Physical-access trust boundaries |
| 15 | sound-trigger | microphone | Acoustic triggering |
| 16 | logic-bomb | temp + light | Conditional payloads / logic bombs |
| 17 | hash-avalanche | NeoPixels | The avalanche effect in hashing |
| 18 | entropy-source | mic + light | Where randomness for crypto comes from |
| 19 | passphrase-key | HID | A button-press hardware passphrase typer |
| 20 | knock-unlock | accelerometer | Knock-code authentication |
| 21 | usb-drop | NeoPixels | The "found a USB in the parking lot" awareness skit |
| 22 | enumeration-anatomy | USB serial | What the host actually sees when a device enumerates |

### Out of scope on this board
The base CPX has **no WiFi/Bluetooth and no USB host**, so Wi-Fi/BLE/network attacks aren't
possible here. If you want those, the **Circuit Playground Bluefruit** (nRF52840) is a
drop-in upgrade that adds BLE — opening up BLE HID injection and BLE scanning demos.

## Get started

1. Read **[SETUP.md](SETUP.md)** — flash CircuitPython, install the libraries with `circup`.
2. Deploy a demo to the board:
   ```bash
   python tools/deploy.py 01-obvious-badusb
   ```
3. Follow the demo's `README.md` for which switch/button arms it, then film.

## Repo layout

- `demos/NN-name/` — one folder per demo: a **self-contained** `code.py` (+ `boot.py`/`payload.txt`
  if needed) and a short README. Each demo is single-file and memory-lean on purpose — the CPX's
  SAMD21 has only ~32KB RAM, which isn't enough to import a shared helper package *and* the HID
  libraries at once, so each demo inlines just what it needs and imports heavy libs lazily.
- `tools/` — host-side helpers: `deploy.py` and the optional exfil decoders.

---

<sub>Board photos are hotlinked from Adafruit's product CDN and are the property of <a href="https://www.adafruit.com/product/3333">Adafruit Industries</a>. This repo is not affiliated with Adafruit; it just points at a great board you can buy from them.</sub>
