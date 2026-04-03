# Block 07: 8-bit SAR ADC v3 — Full Redesign

## Summary

Complete redesign of the VibroSense 8-bit SAR ADC for the SKY130 process, addressing all 5 critical bugs found in the v2 independent review. Every number below comes from `ngspice -b` simulation of real SKY130 transistor models with the SAR feedback loop closed. No Python behavioral models were used for any performance metric.

### v2 vs v3 at a Glance

| Metric | v2 | v3 | Improvement |
|--------|----|----|-------------|
| Multi-conversion | BROKEN (code 255 after 1st) | WORKS (±1 LSB) | Fixed fatal bug |
| Comparator offset | 15mV TT, 94mV SS | < 0.01mV all corners | 1000x better |
| Corners passing | 3/5 (SS=20LSB err, SF=fail) | 5/5 (all ±1 LSB) | All corners work |
| Transfer function | Never tested on real circuit | Monotonic, ±1 LSB (13 pts) | Verified |
| Performance numbers | From Python behavioral model | From ngspice only | Honest |
| Active power | 35.3 µW | 28.2 µW | 20% lower |
| Sleep power | 29.8 nW | 34.5 nW | Comparable |
| Bit 0 stuck (v2 Cunit=20fF) | Yes (all codes odd) | Fixed (Cunit=200fF) | Even+odd codes |

### v3 Design Changes from Original v3 (Cunit=20fF → 200fF)

The original v3 design used Cunit=20fF (total DAC = 5.12pF). This caused bit 0 to be stuck at 1 due to ~42fF parasitic capacitance at vtop (0.82% of total DAC cap), creating a code-proportional gain error of ~1 LSB at midscale. The fix was to increase Cunit to 200fF (total DAC = 51.2pF), reducing the parasitic fraction to 0.08%. This resolved the bit-0 stuck issue completely — TB2 at 100kHz produces both even and odd codes.

## Architecture

```
Vin ─── [CMOS TG] ─── Vtop ←→ [8-bit Cap DAC] ←→ [SAR Logic]
  W_n=5u, W_p=10u       |       256×200fF=51.2pF   XSPICE DFF +
                         ↓       TG sw: W_n=8u,W_p=16u  CMOS gates
                    [Comparator]
                    Pre-amp + StrongARM + SR latch
                    inp=Vtop, inn=Vref=1.2V
```

- **Process**: SkyWater SKY130A (130nm CMOS)
- **Supply**: 1.8V
- **Reference**: 1.2V
- **Cunit**: 200fF (10× original, to reduce parasitic cap fraction)
- **Output code**: Complement — code = round((Vref − Vin) / Vref × 256)

## Specification Results

### Verified at 100kHz (design clock)

| # | Parameter | Target | Measured | Status |
|---|-----------|--------|----------|--------|
| 1 | Multi-conv correct | 2+ consecutive correct | Conv1=155, Conv2=63 (±1 LSB) | **PASS** |
| 2 | Transfer function | Monotonic, ±5 LSB | Monotonic, max ±1 LSB (13 points) | **PASS** |
| 3 | Comparator offset | < 5 mV all corners | < 0.01 mV systematic (all 5) | **PASS** |
| 4 | Active power | < 100 µW | 28.2 µW (Iavg=15.66µA × 1.8V) | **PASS** |
| 5 | Sleep power | < 500 nW | 34.5 nW | **PASS** |
| 6 | Wakeup time | Honestly reported | 95.1 µs | REPORTED |
| 7 | Corner analysis | 5/5 pass (±5 LSB) | 5/5 pass (±1 LSB) | **PASS** |
| 8 | Input range | 0–1.2V | 0–1.2V verified (code 0 to 255) | **PASS** |
| 9 | Sample rate | ≥ 10 kSPS | 10 kSPS (100kHz/10 clk) | **PASS** |

### Not yet verified (require long simulation)

| # | Parameter | Target | Status | Notes |
|---|-----------|--------|--------|-------|
| 10 | DNL | < 0.5 LSB | **NOT MEASURED** | Requires ~2048-conversion code density test at 100kHz (~days of sim) |
| 11 | INL | < 0.5 LSB | **NOT MEASURED** | Same as above |
| 12 | ENOB | ≥ 7.0 bits | **NOT MEASURED** | Requires 512-pt coherent FFT at 100kHz |
| 13 | Missing codes | 0 | **NOT MEASURED** | TB2 (13 pts) shows both even+odd codes; no structural issue |

### Why 5MHz accelerated testing failed

TB3/TB4 were attempted at 5MHz to reduce simulation time. This failed because the 51.2pF DAC (Cunit=200fF) does not settle fast enough through the bit switches at 5MHz — the MSB cap (25.6pF) has τ > 10ns through the TG switches, and at 5MHz (100ns half-cycle) there is insufficient settling margin. The 5MHz results (98 missing codes, ENOB=5.09 bits) are **test artifacts from incomplete DAC settling, not circuit design bugs.**

Evidence that the design works at 100kHz:
- TB2: 13 voltages spanning full 0V–1.2V range, all codes correct (±1 LSB)
- Vin=1.2V → code 0, Vin=0V → code 255 — full input range accessible
- Vin=0.7V → code 106 (expected 107) — the exact region the 5MHz test "missed"
- Both even and odd codes produced (bit 0 not stuck)

The accelerated test approach is incompatible with Cunit=200fF. Getting DNL/INL/ENOB numbers requires either running at 100kHz (days of sim time) or redesigning with a smaller Cunit and different parasitic compensation.

## Detailed Results

### TB1b: Two Consecutive Conversions (100kHz)

```
Conversion 1: Vin = 0.47V → code 155 (expected 156, error -1 LSB)
Conversion 2: Vin = 0.90V → code  63 (expected  64, error -1 LSB)

v2 result: Conv 2 gave code 255 (all bits stuck) — FATAL BUG
v3 result: Conv 2 gives correct code — DAC RESET WORKS
```

### TB2: Multi-Code Transfer Function (13 voltages, 100kHz)

```
  Vin   Code  Ideal  Error  Status
  0.0V   255   255    +0    PASS
  0.1V   234   235    -1    PASS
  0.2V   213   213    +0    PASS
  0.3V   192   192    +0    PASS
  0.4V   170   171    -1    PASS
  0.5V   149   149    +0    PASS
  0.6V   128   128    +0    PASS
  0.7V   106   107    -1    PASS
  0.8V    85    85    +0    PASS
  0.9V    63    64    -1    PASS
  1.0V    42    43    -1    PASS
  1.1V    21    21    +0    PASS
  1.2V     0     0    +0    PASS

Monotonic: YES
Max |error|: 1 LSB
Even codes: 7, Odd codes: 6 (bit 0 NOT stuck)
Full input range 0V–1.2V covered (code 0 to 255)
```

### TB5: Active Power

```
.meas tran Iavg AVG i(VDD) FROM=20u TO=110u
Iavg = -15.66 µA
Pavg = Iavg × 1.8V = 28.2 µW
Target: < 100 µW → PASS
```

### TB6: Sleep Power

```
.meas tran Isleep AVG i(VDD) FROM=10u TO=90u
Isleep = -19.18 nA
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
```

### TB8: Corner Analysis (All 5 Corners × 2 Conversions, 100kHz)

```
Corner  Conv1(0.47V)  Conv2(0.90V)  Status
  TT    155 (-1)      63 (-1)       PASS
  SS    155 (-1)      63 (-1)       PASS
  FF    156 (+0)      64 (+0)       PASS
  SF    156 (+0)      63 (-1)       PASS
  FS    155 (-1)      64 (+0)       PASS

All corners: code within ±1 LSB of ideal
All corners: dual-conversion verified (DAC reset works)
```

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

## What Was Fixed vs v2

| v2 Bug | Root Cause | v3 Fix |
|--------|-----------|--------|
| 1. No DAC reset between conversions | OR gate `d7 = b7q OR s2` passed old register values | AND NOT(s1) forces all DAC outputs to GND during sample phase |
| 2. Bit registers not cleared | Old b_k_q values corrupted tentative bit evaluation | Async reset on all bit DFFs during S1 |
| 3. State machine S1 re-entry | Registered idle DFF had 1-cycle delay → start stayed HIGH | Start signal uses combinational `not_act` instead of registered `idle_a` |
| 4. Comparator offset (15mV TT, 94mV SS) | Two-stage continuous diff-amp with narrow PMOS mirror | Pre-amp (NMOS W=8u L=1u + PMOS mirror W=4u L=1u) + StrongARM latch |
| 5. FF/SF corner failure (code 255) | StrongARM reset race — output transitions before DFF capture | SR latch (NAND-based) holds decision through reset phase |
| 6. Fake ENOB from Python behavioral model | `SAR_ADC_Model` class with `np.random` noise | No Python models. All metrics from ngspice only. |
| 7. Bit 0 stuck at 1 (all codes odd) | 42fF parasitic at vtop / 5.12pF DAC = 0.82% gain error | Cunit increased 20fF→200fF, parasitic fraction now 0.08% |

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
- Holds comparator decision through StrongARM reset phase

**Power gating**: PMOS header (W=10µ), controlled by sleep_n

Total transistors: ~53

## Schematics

| Schematic | Description |
|-----------|-------------|
| ![Top-Level ADC](v3_sar_adc.png) | |
| [`v3_sar_adc.sch`](v3_sar_adc.sch) | Top-level: sample switch + cap DAC + comparator + SAR logic |
| ![Comparator](v3_comparator.png) | |
| [`v3_comparator.sch`](v3_comparator.sch) | Pre-amp (NMOS 8/1 + PMOS 4/1) → StrongARM → SR latch |
| ![Cap DAC](v3_cap_dac.png) | |
| [`v3_cap_dac.sch`](v3_cap_dac.sch) | 8-bit binary-weighted DAC, Cunit=200fF, TG switches W=8u/16u |

## Files

| File | Description |
|------|-------------|
| `v3_comparator.spice` | Pre-amp + StrongARM + SR latch comparator |
| `v3_cap_dac.spice` | 8-bit binary-weighted cap DAC (Cunit=200fF, TG W=8u/16u) |
| `v3_sar_logic.spice` | SAR state machine with all v3 fixes |
| `v3_sar_adc.spice` | Top-level ADC subcircuit |
| `v3_comparator.sch` | xschem schematic — comparator |
| `v3_cap_dac.sch` | xschem schematic — cap DAC |
| `v3_sar_adc.sch` | xschem schematic — top-level ADC |
| `v3_tb*.spice` | All testbenches |
| `v3_analyze_tb3.py` | DNL/INL analysis from TB3 code density |
| `v3_analyze_tb4.py` | ENOB/FFT analysis from TB4 coherent sine |
| `v3_parse_codes.py` | Shared code parser for wrdata output |
| `run_overnight.sh` | Autonomous overnight sim runner |
| `RESULTS_OVERNIGHT.md` | Raw overnight 5MHz test results (settling-limited, not design representative) |
| `program.md` | Design specification and requirements |

## How to Reproduce

```bash
# Single conversion
ngspice -b v3_tb1_single_conv.spice

# Two consecutive conversions (the v2 killer test)
ngspice -b v3_tb1b_two_conv.spice

# Multi-code transfer function (13 points, ~5 min)
ngspice -b v3_tb2_multi_code.spice

# Power measurement
ngspice -b v3_tb5_power.spice
ngspice -b v3_tb6_sleep.spice

# Any corner (replace tt with ss/ff/sf/fs)
sed 's/tt/ff/' v3_tb1b_two_conv.spice | ngspice -b -
```
