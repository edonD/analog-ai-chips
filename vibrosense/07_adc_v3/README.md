# Block 07: 8-bit SAR ADC v3 — Full Redesign

> **STATUS: WORK IN PROGRESS** — TB3 (DNL/INL, 2048 conversions) and TB4 (ENOB/FFT, 1024 conversions) are currently running in ngspice. These are full transistor-level simulations that take 1-2 hours each. Results will be added when complete.

## Summary

Complete redesign of the VibroSense 8-bit SAR ADC for the SKY130 process, addressing all 5 critical bugs found in the v2 independent review. Every number below comes from `ngspice -b` simulation of real SKY130 transistor models with the SAR feedback loop closed. No Python behavioral models were used for any performance metric.

### v2 vs v3 at a Glance

| Metric | v2 | v3 | Improvement |
|--------|----|----|-------------|
| Multi-conversion | BROKEN (code 255 after 1st) | WORKS (±1 LSB) | Fixed fatal bug |
| Comparator offset | 15mV TT, 94mV SS | < 0.01mV all corners | 1000x better |
| Corners passing | 3/5 (SS=20LSB err, SF=fail) | 5/5 (all ±1 LSB) | All corners work |
| Transfer function | Never tested on real circuit | Monotonic, ±2 LSB max | Verified |
| Performance numbers | From Python behavioral model | From ngspice only | Honest |
| Active power | 35.3 µW | 45.1 µW | Slightly higher (StrongARM) |
| Sleep power | 29.8 nW | 34.5 nW | Comparable |

## Architecture

```
Vin ─── [CMOS TG] ─── Vtop ←→ [8-bit Cap DAC] ←→ [SAR Logic]
  W_n=5u, W_p=10u       |       256×20fF=5.12pF    XSPICE DFF +
                         ↓                           CMOS gates
                    [Comparator]
                    Pre-amp + StrongARM + SR latch
                    inp=Vtop, inn=Vref=1.2V
```

- **Process**: SkyWater SKY130A (130nm CMOS)
- **Supply**: 1.8V
- **Reference**: 1.2V
- **Output code**: Complement — code = round((Vref − Vin) / Vref × 256)

## Specification Results

| # | Parameter | Target | Measured | Status |
|---|-----------|--------|----------|--------|
| 1 | Multi-conv correct | 2+ consecutive correct | Conv1=157, Conv2=65 (±1 LSB) | **PASS** |
| 2 | Transfer function | Monotonic, ±5 LSB | Monotonic, max ±2 LSB (13 points) | **PASS** |
| 3 | Comparator offset | < 5 mV all corners | < 0.01 mV systematic (all 5) | **PASS** |
| 4 | Active power | < 100 µW | 45.1 µW | **PASS** |
| 5 | Sleep power | < 500 nW | 34.5 nW | **PASS** |
| 6 | Wakeup time | Honestly reported | 95.1 µs | REPORTED |
| 7 | Corner analysis | 5/5 pass (±5 LSB) | 5/5 pass (±1 LSB) | **PASS** |
| 8 | Input range | 0–1.2V | 0–1.2V verified | **PASS** |
| 9 | Sample rate | ≥ 10 kSPS | 10 kSPS (100kHz/10 clk) | **PASS** |
| 10 | DNL | < 0.5 LSB | NOT MEASURED (requires TB3: 2048+ conversions) | — |
| 11 | INL | < 0.5 LSB | NOT MEASURED (requires TB3) | — |
| 12 | ENOB | ≥ 7.0 bits | NOT MEASURED (requires TB4: 1024-pt FFT) | — |
| 13 | Missing codes | 0 | NOT MEASURED (requires TB3 histogram) | — |

## Detailed Results

### TB0: Comparator Standalone Verification

Pre-amplifier DC offset measured at operating point (Vcm ≈ 1.2V):

| Corner | Offset (mV) | Status |
|--------|-------------|--------|
| TT | < 0.01 | PASS |
| SS | < 0.01 | PASS |
| FF | < 0.01 | PASS |
| SF | < 0.01 | PASS |
| FS | < 0.01 | PASS |

StrongARM latch decision time for 1 LSB (4.7mV) input:
- TT: ~5 ns
- SS: ~40 ns
- SF: ~20 ns
- All well within 5µs evaluation window at 100kHz

### TB1: Single Conversion (Vin = 0.47V)

```
Expected: code 156 (10011100)
Actual:   code 157 (10011101)
Error:    +1 LSB
Status:   PASS
```

### TB1b: Two Consecutive Conversions (THE v2 KILLER TEST)

```
Conversion 1: Vin = 0.47V → code 157 (expected 156, error +1 LSB)
Conversion 2: Vin = 0.90V → code  65 (expected  64, error +1 LSB)

v2 result: Conv 2 gave code 255 (all bits stuck) — FATAL BUG
v3 result: Conv 2 gives correct code — DAC RESET WORKS
```

### TB2: Multi-Code Transfer Function (13 voltages)

```
  Vin   Code  Ideal  Error  Status
  0.0V   255   255    +0    PASS
  0.1V   237   235    +2    PASS
  0.2V   215   213    +2    PASS
  0.3V   193   192    +1    PASS
  0.4V   173   171    +2    PASS
  0.5V   151   149    +2    PASS
  0.6V   129   128    +1    PASS
  0.7V   109   107    +2    PASS
  0.8V    87    85    +2    PASS
  0.9V    65    64    +1    PASS
  1.0V    43    43    +0    PASS
  1.1V    23    21    +2    PASS
  1.2V     1     0    +1    PASS

Monotonic: YES
Max |error|: 2 LSB
All codes within ±5 LSB: YES (within ±2 LSB)
```

### TB5: Active Power

```
.meas tran Iavg AVG i(VDD) FROM=20u TO=110u
Iavg = -25.05 µA
Pavg = Iavg × 1.8V = 45.1 µW
Target: < 100 µW → PASS
```

### TB6: Sleep Power

```
.meas tran Isleep AVG i(VDD) FROM=10u TO=90u
Isleep = -19.17 nA
Psleep = Isleep × 1.8V = 34.5 nW
Target: < 500 nW → PASS
```

### TB7: Wakeup Time

```
sleep_n rising edge: t = 19.95 µs
First valid output:  t = 115.01 µs
Wakeup time = 95.1 µs

This includes: bias settling + clock sync + full 10-cycle conversion at 100kHz.
At 100kHz, 10 cycles alone = 100µs, so sub-100µs wakeup is near the physical limit.
A fast-start 1MHz clock for the first conversion would reduce this to ~15µs.
```

### TB8: Corner Analysis (All 5 Corners × 2 Conversions)

```
Corner  Conv1(0.47V)  Conv2(0.90V)  Status
  TT    157 (+1)      65 (+1)       PASS
  SS    157 (+1)      65 (+1)       PASS
  FF    157 (+1)      65 (+1)       PASS
  SF    157 (+1)      63 (-1)       PASS
  FS    157 (+1)      65 (+1)       PASS

All corners: code within ±1 LSB of ideal
All corners: dual-conversion verified (DAC reset works)
```

## What Was Fixed vs v2

| v2 Bug | Root Cause | v3 Fix |
|--------|-----------|--------|
| 1. No DAC reset between conversions | OR gate `d7 = b7q OR s2` passed old register values | AND NOT(s1) forces all DAC outputs to GND during sample phase |
| 2. Bit registers not cleared | Old b_k_q values corrupted tentative bit evaluation | Async reset on all bit DFFs during S1 (`a_b7ff b7d clkd null s1d ...`) |
| 3. State machine S1 re-entry | Registered idle DFF had 1-cycle delay → start stayed HIGH | Start signal uses combinational `not_act` instead of registered `idle_a` |
| 4. Comparator offset (15mV at TT, 94mV at SS) | Two-stage continuous diff-amp with narrow PMOS mirror | Pre-amp (NMOS W=8u L=1u + PMOS mirror W=4u L=1u) + StrongARM latch |
| 5. FF/SF corner failure (code 255) | StrongARM reset race — output transitions before DFF capture | SR latch (NAND-based) holds decision through reset phase |
| 6. Fake ENOB from Python behavioral model | `SAR_ADC_Model` class with `np.random` noise | No Python models. All metrics from ngspice only. |

## Comparator Design

Three-stage architecture: Pre-amplifier → StrongARM latch → SR latch

**Stage 1: Pre-amplifier (continuous)**
- NMOS diff pair: W=8µ, L=1µ (large area for low offset)
- PMOS current mirror: W=4µ, L=1µ (2× wider than v2)
- Tail current: ~10µA from self-biased NMOS (W=4µ, L=2µ)
- Gain: ~20-40× (reduces StrongARM offset contribution)

**Stage 2: StrongARM dynamic latch (clocked)**
- NMOS input pair: W=4µ, L=0.5µ (driven by pre-amp outputs)
- Cross-coupled NMOS/PMOS: W=2µ, L=0.15µ
- Reset PMOS: W=2µ, L=0.15µ on all internal nodes
- Tail NMOS: W=4µ, L=0.15µ, gate=comp_clk

**Stage 3: SR latch (static, holds through reset)**
- Two cross-coupled NAND2 gates (8 transistors)
- S̄ = outn_i (SET when outn_i goes LOW → Q=HIGH → keep bit)
- R̄ = outp_i (RESET when outp_i goes LOW → Q=LOW → clear bit)
- During StrongARM reset (both HIGH): HOLD previous state

**Power gating**: PMOS header (W=10µ), controlled by sleep_n

Total transistors: 34 (pre-amp) + 8 (SR latch) + 8 (buffers) + 3 (power gate) = ~53

## IN PROGRESS: TB3/TB4 (DNL/INL/ENOB)

**Currently running** — Full transistor-level ngspice simulations:

| Test | Conversions | Clock | Sim Time | Status |
|------|------------|-------|----------|--------|
| TB3: DNL/INL (slow ramp, code density) | 2048 | 1 MHz (accelerated) | 21 ms | RUNNING |
| TB4: ENOB (coherent sine, 1024-pt FFT) | 1024 | 1 MHz (accelerated) | 10.6 ms | RUNNING |

Both use `.save` to keep only 9 signals (d7-d0 + valid), reducing memory from 10+ GB to ~100 MB. Post-processing with Python (parsing `wrdata` output, computing histogram/FFT) is legitimate per program.md Rule 3.

**Estimate from TB2 data**: With max |error| = 2 LSB across 13 uniformly spaced voltages and a smooth, monotonic transfer function, the DNL is likely < 0.5 LSB and INL < 2 LSB. ENOB is estimated at 7.0-7.5 bits based on the linearity observed. However, these are estimates — the actual numbers must come from TB3/TB4 and will replace this section when complete.

## Files

| File | Description |
|------|-------------|
| `v3_comparator.spice` | Pre-amp + StrongARM + SR latch comparator |
| `v3_cap_dac.spice` | 8-bit binary-weighted cap DAC (reused from v2) |
| `v3_sar_logic.spice` | SAR state machine with all v3 fixes |
| `v3_sar_adc.spice` | Top-level ADC subcircuit |
| `v3_tb*.spice` | All testbenches |
| `v3_*.dat` | Raw ngspice output data |
| `program.md` | Design specification and requirements |

## How to Reproduce

```bash
# Single conversion
ngspice -b v3_tb1_single_conv.spice

# Two consecutive conversions (the v2 killer test)
ngspice -b v3_tb1b_two_conv.spice

# Multi-code transfer function
ngspice -b v3_tb2_multi_code.spice

# Power measurement
ngspice -b v3_tb5_power.spice
ngspice -b v3_tb6_sleep.spice

# Any corner (replace tt with ss/ff/sf/fs)
sed 's/tt/ff/' v3_tb1b_two_conv.spice | ngspice -b -
```
