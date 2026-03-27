# PVDD 5V LDO Regulator

**Automotive-grade low-dropout regulator for BLDC motor controller ICs.**

> Input: 2.5-40V automotive battery (BVDD) | Output: 5.0V +/-3.5% | Load: 50 mA | Dropout: 400 mV | Temp: -40 to 175C

Based on the HVC 3rd-generation power system architecture (TDK-Micronas HVCM family).

---

## System Context

The PVDD regulator is one of four internal regulators in the HVCM motor controller chip. It supplies 5V to the power bridge gate drivers and analog subsystems. The chip operates from an automotive 12V battery (6-18V nominal, 2.5-40V transient range including cold-crank and load dump).

```
    BVDD (automotive battery, 2.5-40V)
     |
     +--[Zener Clamp]--+
     |                 |
     +--[Pass Device]--+---> PVDD (5.0V, 50mA)
     |   40V PDMOS     |        |
     |   W=11mm        |     [200pF internal Cload]
     |                 |        |
     +--[Level Shifter]|       GND
     |   SVDD<->BVDD   |
     |                 |
  [Error Amp] <--- [Feedback Divider] <--- PVDD
     |                                      |
  [AVBG Ref]                          [UV/OV Comparators]
  (1.226V)                                  |
     |                              [Mode Control Logic]
  [Compensation]                   bypass / retention / active
     |
  [Current Limiter]
     |
  [Startup Circuit]
```

---

## Specifications (from concept documentation)

| Parameter | Min | Typ | Max | Unit | Condition |
|-----------|-----|-----|-----|------|-----------|
| Supply voltage (BVDD) | 2.5 | 12 | 40 | V | Full operating range |
| Output voltage (PVDD) | 4.8 | 5.0 | 5.17 | V | +/-3.5% over PVT & load |
| Output voltage (HTOL) | -- | 6.5 | -- | V | Accelerated test mode |
| Load current (active) | -- | -- | 50 | mA | Active mode |
| Load current (retention) | -- | -- | 0.5 | mA | Retention mode |
| Dropout voltage | -- | 400 | -- | mV | BVDD_min = 5.4V |
| Load transient undershoot | -- | 110 | -- | mV | 1mA -> 10mA in 1us |
| Load capacitor | -- | 200 | -- | pF | Internal (capless to pin) |
| Quiescent current (active) | -- | 268 | -- | uA | From BVDD |
| Quiescent current (retention) | -- | 3 | -- | uA | From BVDD |
| UV threshold | 4.2 | -- | 4.5 | V | |
| OV threshold | 5.25 | -- | 5.7 | V | |
| Reference input (AVBG) | 1.218 | 1.226 | 1.246 | V | Bandgap reference |
| Load regulation | -- | -- | 2 | mV/mA | |
| Line regulation | -- | -- | 1 | mV/V | |
| Phase margin | 53 | -- | -- | deg | MC 500 runs, sigma x2 |
| Junction temperature | -40 | -- | 175 | C | Automotive grade |
| Total area | -- | 0.065 | -- | mm^2 | Including pass device |

---

## Operating Modes

The regulator operates in 5 modes depending on BVDD voltage, managed by the mode control logic:

| # | Mode | BVDD Range | PVDD Output | Max Load | Description |
|---|------|-----------|-------------|----------|-------------|
| 1 | **POR** | 0 - 2.5V | OFF | -- | Power system off |
| 2 | **Retention bypass** | 2.5 - 4.2V | BVDD | 0.5 mA | Pass device fully on, PVDD tracks BVDD |
| 3 | **Retention regulate** | 4.2 - 4.5V | 4.1V | 0.5 mA | Regulates to 4.1V to limit overshoot on fast BVDD ramps |
| 4 | **Power-up bypass** | 4.5 - 5.0V | BVDD | 10 mA | Bypass for power bridge startup |
| 5 | **Active regulate** | > 5.6V | 5.0V | 50 mA | Full regulation, all specs guaranteed |

UV is released at BVDD = 3.73V.

---

## Design Blocks

```
Wave 1 (independent):  00_error_amp | 01_pass_device | 05_uv_ov_comparators | 06_level_shifter
Wave 2 (needs amp):    02_feedback_network | 03_compensation | 04_current_limiter
Wave 3 (needs all):    07_zener_clamp | 08_mode_control | 09_startup | 10_top_integration
```

### Block 00: Error Amplifier (`00_error_amp/`)
The core OTA that compares the feedback voltage to the AVBG reference and drives the pass device gate. Must operate across the full BVDD range (5.4-40V) in the BVDD domain. Key challenge: high gain for tight load/line regulation while maintaining >53 deg phase margin with 200 pF internal load cap and large pass device gate capacitance.

### Block 01: Pass Device (`01_pass_device/`)
40V PDMOS pass transistor. W/L = 11mm / 0.3um. Must deliver 50 mA with <400 mV dropout at BVDD = 5.4V across PVT corners. The pass device is the dominant pole in the loop — its gate capacitance and transconductance set the loop bandwidth. SOA (Safe Operating Area) verification required for all transient conditions.

### Block 02: Feedback Network (`02_feedback_network/`)
Resistive voltage divider that scales the 5.0V output down to the 1.226V AVBG reference level. Divider ratio = 1.226/5.0 = 0.2452. Two monitor ratios exist: 0.252 (retention) and 0.198 (active) for the test mux. Must be high-impedance to minimize quiescent current but low enough for noise immunity.

### Block 03: Compensation (`03_compensation/`)
Frequency compensation network to ensure >53 deg phase margin across all operating conditions. The LDO has two main poles: the output pole (set by 200 pF Cload and load impedance) and the error amp output pole (set by pass device Cgs). Miller compensation, pole-zero cancellation, or adaptive biasing may be needed. Must be stable from no-load (100k ohm) to full-load (100 ohm).

### Block 04: Current Limiter (`04_current_limiter/`)
Overcurrent protection that limits PVDD output current. Prevents pass device destruction during short-circuit or overload. Must not interfere with normal 50 mA operation but must clamp hard above the limit. Fold-back characteristic preferred to reduce pass device power dissipation during sustained shorts.

### Block 05: UV/OV Comparators (`05_uv_ov_comparators/`)
Undervoltage (4.2-4.5V) and overvoltage (5.25-5.7V) threshold comparators monitoring PVDD output. UV triggers mode transitions and system resets. OV flags abnormal conditions. Both need hysteresis for noise immunity. Design was improved in CR-4 (HVCM-4-1 and above).

### Block 06: Level Shifter (`06_level_shifter/`)
Translates control signals between the SVDD domain (~2.5V) and the BVDD domain (up to 40V). Required because the error amplifier and pass device operate in the BVDD domain while the digital control and reference come from the SVDD domain. Must work across the full 2.5-40V BVDD range.

### Block 07: Zener Clamp (`07_zener_clamp/`)
ESD and transient protection. Zener diode array (32x32 um x 4 = 4096 um^2) clamping PVDD during load dump and transient events. Rated for 400 mA RMS / 600 mA peak. Located under the PVDD bond pad for area efficiency.

### Block 08: Mode Control (`08_mode_control/`)
State machine that manages transitions between POR, retention bypass, retention regulate, power-up bypass, and active regulate modes. Inputs: BVDD threshold comparators (bvdd_4v5, bvdd_uv), enable signals (en_ret_i). Outputs: bypass switch control, error amp enable, reference select, UV/OV enable. Critical for clean power-up without oscillation (known issue #m3: PVDD oscillation after AVDD ramp-up).

### Block 09: Startup (`09_startup/`)
Startup sequencing circuit that ensures monotonic PVDD ramp-up for all BVDD slew rates (1 V/us to 12 V/us). Must handle cold-crank scenarios where BVDD drops below regulation threshold and recovers. Coordinates with the retention-to-active mode transition.

### Block 10: Top Integration (`10_top_integration/`)
Full regulator assembly connecting all blocks. Verification plan:
- Startup and power-down (BVDD ramps at 0.1, 1, 12 V/us)
- Stability (LSTB PVT + 500-run Monte Carlo)
- Load transient (0-10 mA, 0-50 mA step response)
- UV/OV detection thresholds
- Regulated voltage Monte Carlo
- Active/retention mode transitions
- PVDD + AVDD co-simulation (cross-regulator interaction)
- RCX post-layout parasitic extraction (~220 fF)
- SOA verification for pass device

---

## Known Issues from Silicon

| Issue | Description | Status |
|-------|-------------|--------|
| #m3 | PVDD oscillation after AVDD ramp-up | Fixed in HVCM-2-1 |
| #m4 | PVDD over/undershoot when switching AVDD mode | Fixed in HVCM-2-1 |
| CR-4 item 7 | UV/OV comparator improvement for PVDD | Fixed in HVCM-5-1 |
| CR-5 | Zener current reduction concept | Documented |

---

## Reference Documents

| Document | Location |
|----------|----------|
| PVDD Concept (45 slides) | `Power_system/PVDD/PVDD_Regulator_Concept_Documentation.pptx` |
| Zener current reduction | `Power_system/PVDD/PVDD_Reg_Zener_Current_Reduction_concept.pptx` |
| Architecture review | `Power_system/PVDD/ArcRev_PVDD.xlsx` |
| Simulation results | `Power_system/PVDD/Simulation Results/` |
| Power system concept | `Power_system/Psys_concept_HVC3rd_gen_v_0_1.pptx` |
| Electrical performance | `Power_system/Power_System_Electrical_Performance_Simulations.xlsx` |
| LDO literature | `Power_system/Literature/` (capless LDOs, OTA topologies, compensation) |
| HVCM DES rev 10.5 | `HVCM-1x2x3x4x5x_DES_rev10.5_M6_release.pdf` |

---

## Log

| Date | What |
|------|------|
| 2026-03-27 | Project created. Specs extracted from PVDD concept documentation and HVCM DES. 11 design blocks defined. |
