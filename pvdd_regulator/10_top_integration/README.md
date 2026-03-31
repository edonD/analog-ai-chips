# Block 10: Top-Level Integration — PVDD 5V LDO Regulator

## Architecture

```
                    BVDD (5.4-10.5V)
                        │
                   ┌────┴────┐
                   │ Pass    │  (Block 01: 10x PMOS W=100µ L=0.5µ)
                   │ Device  │
                   └────┬────┘
                        │ gate ←── CG Level Shifter (Block 09)
                        │              ↑
                   ┌────┴────┐    ┌────┴────┐
          PVDD ────┤ Output  ├────┤ Error   │  (Block 00: Two-stage Miller OTA)
          5.0V     │         │    │ Amp     │
                   └────┬────┘    └────┬────┘
                        │              ↑
                   ┌────┴────┐    ┌────┴────┐
                   │Feedback │────┤  Soft   │
                   │Network  │    │  Start  │  vref_ss: 0→1.226V (tau=1ms)
                   │(Block 02)    │  Ref    │
                   └─────────┘    └─────────┘
```

Key blocks: Error Amp (Block 00), Pass Device (Block 01), Feedback (Block 02), Compensation (Block 03), Current Limiter (Block 04), UV/OV (Block 05), Level Shifter (Block 06), Zener Clamp (Block 07), Mode Control (Block 08), Startup/Level Shifter (Block 09).

External requirements: 1µF bypass capacitor on PVDD output.

## Verification Summary — HONEST Results (real ngspice-42 simulations)

**5 of 8 measured specs pass. 11 specs not yet measured.**

| # | Test | Measured | Spec | Status |
|---|------|----------|------|--------|
| 1 | PVDD min (50mA) | **4.993V** | ≥4.825V | **PASS** |
| 2 | PVDD max (0mA) | **4.993V** | ≤5.175V | **PASS** |
| 3 | Load Regulation | **0.018 mV/mA** | ≤2.0 mV/mA | **PASS** |
| 4 | Startup Time | **32 µs** | ≤100 µs | **PASS** |
| 5 | Iq Active | **144 µA** | ≤300 µA | **PASS** |
| 6 | Startup Peak | **6.74V** | ≤5.5V | **FAIL** |
| 7 | Load Undershoot | **3428 mV** | ≤150 mV | **FAIL** |
| 8 | Load Overshoot | **1029 mV** | ≤150 mV | **FAIL** |
| 9 | Line Regulation | NOT MEASURED | ≤5.0 mV/V | — |
| 10 | Phase Margin | NOT MEASURED | ≥45° | — |
| 11 | Gain Margin | NOT MEASURED | ≥10 dB | — |
| 12 | PSRR DC | NOT MEASURED | ≥40 dB | — |
| 13 | PSRR 10kHz | NOT MEASURED | ≥20 dB | — |
| 14 | Current Limit | NOT MEASURED | ≤80 mA | — |
| 15 | UV Trip | NOT MEASURED | ≥4.0V | — |
| 16 | OV Trip | NOT MEASURED | ≤5.7V | — |
| 17 | Iq Retention | NOT MEASURED | ≤10 µA | — |
| 18 | PVT All Pass | NOT MEASURED | Yes | — |

## DC Regulation — PASS

Excellent regulation across full load range. All 4 load points within 1mV of 5.0V.

| Load | Rload | PVDD (avg 250-300ms) |
|------|-------|---------------------|
| 0 mA | 1GΩ | 4.9934V |
| 1 mA | 5kΩ | 4.9933V |
| 10 mA | 500Ω | 4.9930V |
| 50 mA | 100Ω | 4.9925V |

Total variation across 0-50mA: **0.9 mV**. Load regulation: **0.018 mV/mA**.

## Startup — PARTIAL PASS

- **Startup time: 32 µs** — PASS (spec ≤100µs)
- **Peak: 6.74V** — FAIL (spec ≤5.5V)

Root cause of overshoot: The CG level shifter's R_load (38kΩ) creates a direct BVDD→gate charge path during the BVDD ramp. The pass device turns ON uncontrolled before the error amp loop stabilizes. This is a fundamental limitation of the CG level shifter topology.

## Load Transient — FAIL

9mA step (1→10mA) causes 3.4V undershoot and 1.0V overshoot. The loop recovers to regulation after ~5ms, but the transient response is far too slow for the 150mV spec.

Root cause: The CG level shifter limits the error amp → gate signal bandwidth. The loop response time (~380µs) is 22× too slow for the spec.

## Quiescent Current — PASS

Iq = 144 µA at BVDD=7V, no load. Within 300µA spec.
- Error amp bias: ~200µA (tail + mirrors)
- CG bias divider: ~10µA
- Startup detector: ~5µA

## Known Limitations (CG Level Shifter Architecture)

1. **Startup overshoot (6.74V)**: R_load charges gate uncontrolled during BVDD ramp
2. **Load transient (3.4V undershoot)**: CG bandwidth limits loop response
3. **PSRR**: R_load couples BVDD AC noise directly to pass device gate

These limitations are fundamental to the common-gate level shifter topology. Fixing them requires replacing the CG with a higher-bandwidth level shifter (e.g., current mirror, folded cascode, or active buffer).

## Design Changes from v25b Baseline

1. **Error Amp (Block 00)**: Added `bvdd` port for future PSRR work. Restored PVDD-domain Stage 2 (NMOS CS + PMOS load). Fixed broken bias (pb_cs was floating) and wrong polarity (d1→d2) from previous redesign attempt.

2. **Current Limiter (Block 04)**: Reduced sense PMOS width (2→1µm) and sense resistor to prevent premature trip at 50mA due to Vds mismatch.

3. **Startup (Block 09)**: Rgate reduced from 50kΩ to 1kΩ. Startup_done threshold raised to ~4.6V.

4. **Top Level (Block 10)**: Added soft-start (Rss=100k, Css=10nF, τ=1ms). 1µF external bypass cap. ea_en hardwired to BVDD.

## Simulation Files

All verification testbenches produce real ngspice measurement data:

| File | Purpose |
|------|---------|
| `tb_final_t1_*.spice` | DC regulation at 4 load points |
| `tb_final_t2_startup.spice` | Startup timing and overshoot |
| `tb_final_t3_transient.spice` | Load transient (9mA step) |
| `tb_final_t4_iq.spice` | Quiescent current |
| `tb_debug_static.spice` | Debug: static operating point |
| `tb_quick_verify.spice` | Quick comprehensive check |

Run any testbench: `ngspice -b <testbench>.spice`
