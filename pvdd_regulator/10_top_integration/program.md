# Block 10: Top Integration — Design Program

## Absolute Rules

1. **Real Sky130 PDK only.** The top-level design contains ONLY `.include` references to block-level `design.cir` files, which contain ONLY Sky130 PDK device instantiations. No behavioral models anywhere in the hierarchy.
2. **No behavioral models.** The ONLY ideal components allowed in the top-level netlist are:
   - `V_AVBG` (bandgap reference, 1.226V) -- external chip block
   - `I_BIAS` (current reference, 1uA) -- external chip block
   - `V_BVDD` (battery supply for testbenches)
   - `V_SVDD` (2.2V supply for testbenches)
   - Testbench stimulus sources (pulse, sine, PWL)
   - Load resistors/capacitors in testbenches
3. **ngspice only.** Fix convergence with `.option` settings.
4. **Every spec verified by simulation.** Run all 18 verification tests. Every number must come from a re-runnable `.spice` testbench.
5. **Push through difficulty.** Top-level integration will expose problems invisible at block level: loading effects, supply coupling, race conditions, convergence failures. Fix them in the block designs or integration netlist.

---

## Purpose

Block 10 connects all sub-blocks (00-09) into the complete PVDD 5V LDO regulator and runs the full 18-point verification plan. This is where the design is proven or broken. Every specification from the master `program.md` must be verified here with full Sky130 PDK simulations in ngspice.

**This block produces the final deliverable:** a complete, re-runnable SPICE netlist of the PVDD regulator that meets all specifications.

---

## Interface (Top-Level Regulator)

| Pin | Direction | Voltage Domain | Description |
|-----|-----------|---------------|-------------|
| `bvdd` | Input | 5.4-10.5V | Battery supply input |
| `pvdd` | Output | 5.0V +/-3.5% | Regulated 5V output |
| `gnd` | Supply | 0V | Ground |
| `avbg` | Input | 1.226V | Bandgap reference (ideal source) |
| `ibias` | Input | 1uA | Bias current reference (ideal source) |
| `svdd` | Supply | 2.2V | Low-voltage digital supply |
| `en` | Input | SVDD domain | Master enable |
| `en_ret` | Input | SVDD domain | Retention mode enable |
| `uv_flag` | Output | SVDD domain | Undervoltage flag (level-shifted) |
| `ov_flag` | Output | SVDD domain | Overvoltage flag (level-shifted) |
| `mode[1:0]` | Output | SVDD domain | Operating mode status |

---

## Target Specifications (Full Regulator)

These are the master specs. Every row must be verified.

| # | Parameter | Min | Typ | Max | Unit | Notes |
|---|-----------|-----|-----|-----|------|-------|
| 1 | Input voltage (BVDD) | 5.4 | 7.0 | 10.5 | V | |
| 2 | Output voltage (PVDD) | 4.8 | 5.0 | 5.17 | V | +/-3.5% over PVT and load |
| 3 | Dropout voltage | -- | 400 | -- | mV | At BVDD=5.4V, 50 mA |
| 4 | Load current (active) | 0 | -- | 50 | mA | |
| 5 | Load transient undershoot | -- | -- | 150 | mV | 1mA->10mA, 1us |
| 6 | Load transient overshoot | -- | -- | 150 | mV | 10mA->1mA, 1us |
| 7 | Internal load cap | -- | 200 | -- | pF | |
| 8 | Line regulation | -- | -- | 5 | mV/V | |
| 9 | Load regulation | -- | -- | 2 | mV/mA | |
| 10 | Quiescent current (active) | -- | -- | 300 | uA | |
| 11 | Quiescent current (retention) | -- | -- | 10 | uA | |
| 12 | UV threshold | 4.0 | 4.3 | 4.5 | V | |
| 13 | OV threshold | 5.25 | 5.5 | 5.7 | V | |
| 14 | Phase margin | 45 | -- | -- | deg | All conditions |
| 15 | Gain margin | 10 | -- | -- | dB | All conditions |
| 16 | PSRR @ DC | 40 | -- | -- | dB | |
| 17 | PSRR @ 10kHz | 20 | -- | -- | dB | |
| 18 | Temperature range | -40 | 27 | 150 | C | |

---

## Integration Architecture

The top-level netlist connects all blocks:

```
    V_BVDD (5.4-10.5V)
      |
      +--------[Block 07: Zener Clamp]--------+
      |                                        |
      +--------[Block 09: Startup]-------+     |
      |                                  |     |
      +--S [Block 01: Pass Device] D-----+-----+--- PVDD (5.0V)
      |        |G                        |         |
      |        |                    [Block 04:   [200pF Cload]
      |        |                   Current Lim]    |
      |   [Block 03:                               GND
      |   Compensation]                   |
      |        |                    [Block 02: Feedback]
      |   [Block 00:                      |
      |   Error Amp] <---vfb--------+--GND
      |        |
      |   V_REF (1.226V)
      |        |
      |   [Block 05: UV/OV]
      |        |
      +---[Block 06: Level Shifter]
      |        |
      +---[Block 08: Mode Control]
               |
          SVDD domain signals
```

The top-level subcircuit `.includes` all block `design.cir` files and wires them together.

---

## 18-Point Verification Plan

**Every test must pass. No exceptions.**

### Test 1: DC Regulation
- **Setup:** BVDD=7V, sweep Iload 0 to 50mA
- **Measure:** VPVDD at each load point
- **Pass:** VPVDD = 5.0V +/-3.5% (4.825V to 5.175V) at all loads

### Test 2: Line Regulation
- **Setup:** Iload=10mA, sweep BVDD 5.4 to 10.5V
- **Measure:** dVPVDD / dVBVDD
- **Pass:** < 5 mV/V

### Test 3: Load Regulation
- **Setup:** BVDD=7V, sweep Iload 0 to 50mA
- **Measure:** dVPVDD / dILOAD
- **Pass:** < 2 mV/mA

### Test 4: Load Transient (Undershoot)
- **Setup:** 1mA -> 10mA step in 1us, BVDD=7V
- **Measure:** Max undershoot on PVDD
- **Pass:** < 150 mV

### Test 5: Load Transient (Overshoot)
- **Setup:** 10mA -> 1mA step in 1us, BVDD=7V
- **Measure:** Max overshoot on PVDD
- **Pass:** < 150 mV

### Test 6: Loop Stability
- **Setup:** Break loop at vfb, AC sweep, at Iload = 0, 1mA, 10mA, 50mA
- **Measure:** Phase margin and gain margin
- **Pass:** PM > 45 deg, GM > 10 dB at ALL load points

### Test 7: PSRR
- **Setup:** AC source on BVDD (DC=7V + AC=1), measure at PVDD
- **Measure:** PSRR = 20*log10(Vac_pvdd / Vac_bvdd)
- **Pass:** > 40 dB @ DC, > 20 dB @ 10 kHz

### Test 8: Startup (Normal)
- **Setup:** BVDD ramp 0 -> 10.5V at 1 V/us
- **Measure:** PVDD waveform
- **Pass:** Monotonic, no oscillation, settle < 100 us

### Test 9: Startup (Fast)
- **Setup:** BVDD ramp 0 -> 10.5V at 10 V/us
- **Measure:** Max PVDD overshoot
- **Pass:** No overshoot > 5.5V

### Test 10: Dropout
- **Setup:** Iload=50mA, sweep BVDD 4.5 -> 6V
- **Measure:** VPVDD vs VBVDD
- **Pass:** Regulated at BVDD > 5.4V

### Test 11: Current Limit
- **Setup:** Rload=0.1 ohm (near short), BVDD=7V
- **Measure:** Output current
- **Pass:** Iout clamped < 80 mA

### Test 12: UV Threshold
- **Setup:** Sweep PVDD externally (disconnect regulator, force PVDD)
- **Measure:** UV flag trip point
- **Pass:** Trip at 4.3V +/-0.3V

### Test 13: OV Threshold
- **Setup:** Sweep PVDD externally
- **Measure:** OV flag trip point
- **Pass:** Trip at 5.5V +/-0.2V

### Test 14: Mode Transitions
- **Setup:** BVDD ramp through all thresholds (0 -> 10.5V -> 0)
- **Measure:** All mode output signals
- **Pass:** Clean transitions, no glitches, correct sequence

### Test 15: PVT Corners
- **Setup:** Tests 1-8 at SS/FF/SF/FS corners and -40/27/150C
- **Measure:** All parameters
- **Pass:** All specs met at every corner/temperature combination

### Test 16: Quiescent Current
- **Setup:** BVDD=7V, no load
- **Measure:** Total current from BVDD
- **Pass:** Iq < 300 uA (active), < 10 uA (retention)

### Test 17: Retention Mode
- **Setup:** BVDD=3.5V, Iload=0.5mA
- **Measure:** PVDD voltage
- **Pass:** PVDD tracks BVDD (bypass mode)

### Test 18: Power Consumption
- **Setup:** All operating modes
- **Measure:** Total power from BVDD in each mode
- **Pass:** Report total (document, no specific limit)

---

## Integration Procedure

1. **Verify all block `design.cir` files exist and simulate.** Run a smoke test: include all files, run `.op`, confirm no errors.

2. **Connect all blocks.** Wire the top-level netlist following the architecture. Pay attention to:
   - Net names match across block interfaces
   - Supply domains are correct (which blocks from PVDD, which from BVDD)
   - Enable signals properly connected
   - No floating nodes

3. **Incremental integration (recommended order):**
   - First: Block 00 + 01 + 02 + 03 (core regulation loop). Run Tests 1-6.
   - Second: Add Block 04 (current limiter). Run Test 11. Re-verify Tests 1-6.
   - Third: Add Block 05 (UV/OV). Run Tests 12-13.
   - Fourth: Add Block 06 + 08 (level shifter + mode control). Run Test 14.
   - Fifth: Add Block 07 (zener clamp). Run Test 9.
   - Sixth: Add Block 09 (startup). Run Tests 8-9.
   - Final: Run ALL 18 tests on the complete regulator, then Test 15 (PVT corners).

4. **Fix failures** by returning to the relevant block, modifying its design, and re-running top-level tests.

---

## Pass/Fail Criteria

**ALL 18 tests must pass.**

| Test # | Parameter | Pass Condition |
|--------|-----------|---------------|
| 1 | DC regulation | VPVDD = 5.0V +/-3.5% at 0-50 mA |
| 2 | Line regulation | < 5 mV/V |
| 3 | Load regulation | < 2 mV/mA |
| 4 | Load transient undershoot | < 150 mV |
| 5 | Load transient overshoot | < 150 mV |
| 6 | Phase margin | > 45 deg at all loads |
| 6 | Gain margin | > 10 dB at all loads |
| 7 | PSRR @ DC | > 40 dB |
| 7 | PSRR @ 10 kHz | > 20 dB |
| 8 | Startup (1 V/us) | Monotonic, settle < 100 us |
| 9 | Startup (10 V/us) | No overshoot > 5.5V |
| 10 | Dropout | Regulated at BVDD=5.4V, 50mA |
| 11 | Current limit | Iout < 80 mA at short |
| 12 | UV threshold | 4.3V +/-0.3V |
| 13 | OV threshold | 5.5V +/-0.2V |
| 14 | Mode transitions | Clean, glitch-free |
| 15 | PVT corners | All above pass at all corners/temps |
| 16 | Quiescent current | < 300 uA active, < 10 uA retention |
| 17 | Retention mode | PVDD tracks BVDD at 3.5V |
| 18 | Power consumption | Documented |

---

## Dependencies

**Wave 3 block -- requires ALL other blocks (00-09) to be complete.**

| Block | Required Deliverable |
|-------|---------------------|
| Block 00 | `00_error_amp/design.cir` |
| Block 01 | `01_pass_device/design.cir` |
| Block 02 | `02_feedback_network/design.cir` |
| Block 03 | `03_compensation/design.cir` |
| Block 04 | `04_current_limiter/design.cir` |
| Block 05 | `05_uv_ov_comparators/design.cir` |
| Block 06 | `06_level_shifter/design.cir` |
| Block 07 | `07_zener_clamp/design.cir` |
| Block 08 | `08_mode_control/design.cir` |
| Block 09 | `09_startup/design.cir` |

---

## Deliverables

1. `design.cir` -- Complete PVDD regulator top-level subcircuit (`.subckt pvdd_regulator ...`). **This is the primary deliverable of the entire project.**
2. 18 testbench files (one per verification test, or combined where appropriate):
   - `tb_top_dc_reg.spice` (Test 1)
   - `tb_top_line_reg.spice` (Test 2)
   - `tb_top_load_reg.spice` (Test 3)
   - `tb_top_load_tran.spice` (Tests 4-5)
   - `tb_top_lstb.spice` (Test 6)
   - `tb_top_psrr.spice` (Test 7)
   - `tb_top_startup.spice` (Test 8)
   - `tb_top_startup_fast.spice` (Test 9)
   - `tb_top_dropout.spice` (Test 10)
   - `tb_top_ilim.spice` (Test 11)
   - `tb_top_uv.spice` (Test 12)
   - `tb_top_ov.spice` (Test 13)
   - `tb_top_modes.spice` (Test 14)
   - `tb_top_pvt.spice` (Test 15)
   - `tb_top_iq.spice` (Test 16)
   - `tb_top_retention.spice` (Test 17)
   - `tb_top_power.spice` (Test 18)
3. `README.md` -- Final design report: complete spec table with simulated values, pass/fail for all 18 tests, design choices summary, known limitations
4. `verification_summary.md` -- Machine-readable: 18 rows with test name, measured value, spec, pass/fail
5. `*.png` -- Plots for every test
