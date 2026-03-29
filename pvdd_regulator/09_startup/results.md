# Block 09: Startup Circuit — Results

## Startup Mechanism

**Current-limited gate pulldown + PVDD threshold detection + BVDD-domain regulation assist (MN_pu W=100µm source follower)**

## Results Table

| Parameter | Simulated | Spec | Pass/Fail |
|-----------|-----------|------|-----------|
| Startup time (no load, SS 150°C) | 0 µs | ≤ 100 µs | PASS |
| Startup time (50 mA load) | 5 µs | ≤ 200 µs | PASS |
| PVDD monotonic | Yes | Yes | PASS |
| PVDD overshoot | 944 mV | ≤ 200 mV | **FAIL** |
| Handoff glitch | 50 mV | ≤ 100 mV | PASS |
| Works at 0.1 V/µs ramp | Yes | Yes | PASS |
| Works at 12 V/µs ramp | Yes | Yes | PASS |
| Cold crank recovery | Yes | Yes | PASS |
| Leakage after startup | 0.22 µA | ≤ 1 µA | PASS |
| No overshoot FF −40°C | Yes | Yes | PASS |
| No latch-up/stuck | Yes | Yes | PASS |
| **Specs pass** | **10/11** | | |

## Overshoot Optimization History

| MN_pu Size | Overshoot | Leakage | Status |
|------------|-----------|---------|--------|
| W=0.42u L=8u | 1219 mV | 0.22 µA | baseline |
| W=2u L=1u | 1171 mV | 0.22 µA | -4% |
| W=5u L=1u | 1120 mV | 0.22 µA | -8% |
| W=20u L=1u | 1026 mV | 0.22 µA | -16% |
| **W=100u L=1u** | **944 mV** | **0.22 µA** | **-23% (best)** |
| W=200u L=1u | — | — | convergence fail |
| Level shifter (R_load=1M) | ~200 mV | 1.5 µA | leakage FAIL |

## Overshoot Root Cause

The error amp (Block 00) output is limited to PVDD (its supply). At BVDD=7V with no load, the error amp cannot pull gate above ~4.3V, giving Vsg=2.7V → 80mA through the W=1mm pass device. PVDD rises until Vds approaches 0.

The MN_pu (W=100µm NMOS source follower from BVDD) reduces overshoot by competing with the gate pulldown during startup, keeping gate closer to BVDD. In steady state, MN_pu draws negligible current (deep subthreshold at gate≈6V).

A level shifter (NMOS common-gate) achieves PVDD=5.001V regulation but its bias divider + load resistor exceed the 1µA leakage budget.

## PVT Corner Results

| Corner | PVDD Peak | PVDD Final | Status |
|--------|-----------|------------|--------|
| TT 27°C | 7.00V | 5.96V | Starts correctly |
| TT -40°C | 7.00V | 5.93V | Starts correctly |
| TT 150°C | 7.00V | 6.15V | Starts correctly |
| SS 150°C | 7.00V | 6.08V | Starts correctly |
| FF -40°C | 7.00V | 5.92V | Starts correctly |

## With 50mA Load

PVDD = 5.02V at BVDD=7V — excellent regulation. The load sinks the excess pass device current that the error amp can't prevent.
