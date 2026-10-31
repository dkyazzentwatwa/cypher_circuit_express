# 16 · logic-bomb

**What:** Fires only when multiple conditions align — armed **and** warm (hold the board) **and**
dark (cover the light sensor). Two pixels show which conditions are met; all three → benign
rainbow "detonation."

**Arm:** slide switch to the left, then make it warm and dark. Toggle off to re-arm. Tune
`WARM_C` / `DARK` in `code.py`.

**Lesson:** Logic bombs gate on combinations of state (date, environment, a file existing) so they
stay dormant and hard to catch until the exact trigger.

**Defense:** behavioral monitoring and triggering analysis, not one-shot "did it fire on open."
