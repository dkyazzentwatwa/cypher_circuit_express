# 04 · ir-replay

**What:** Captures a remote's raw IR burst (button A), then replays it from the board's IR LED
(button B). A no-protocol-needed replay attack.

**Run:** Button A → point your remote at the board, press a key. LEDs go green when captured.
Button B → point the board at the TV/device to replay.

**Lesson:** Most consumer IR has no authentication, so capture-and-replay just works. Systems
that resist it (rolling codes) exist for exactly this reason — a great on-camera contrast.

**Caveat:** raw replay suits simple one-shot codes; some devices expect repeat frames. If
replay is flaky, capture again holding the remote key a touch longer.
