# Expert Report 03: Squarer-Based Envelope Detector

## Problem Analysis

The current rectifier has a dead zone and only produces DC = (1/pi) * Vpeak.
A squarer avoids the dead zone entirely because x^2 >= 0 for all x.
The output is proportional to the RMS power of the signal:

    V_out = K * mean(Vin^2) = K * Vpeak^2 / 2

This has TWO advantages:
1. No dead zone (x^2 is smooth through zero)
2. Output grows quadratically with input (amplifies large signals more)

But also a disadvantage: small signals get suppressed (quadratic compression).

## Proposed Architecture

### Block Diagram
```
BPF_out --[V-to-I]--[Squaring Cell]--[LPF]-- V_env_sq
  (VCM +/- sig)  (gm*(Vin-VCM))  (I^2/I_ref)  (DC proportional to power)
```

### Squaring Approaches in SKY130

**Option A: Single-pair MOSFET squarer** (same as Block 05 RMS)
- Two matched NFETs: M_sig (gate=BPF_out), M_ref (gate=VCM)
- Difference current: dI = K/2 * [2*Vov*V + V^2]
- After LPF: mean(dI) propto V_rms^2 (linear term averages to ~0)
- This is ALREADY implemented in the RMS block!

**Option B: Gilbert cell multiplier**
- Cross-coupled differential pairs
- Output current = K * V1 * V2
- With V1 = V2 = (BPF - VCM): output propto (BPF-VCM)^2
- More accurate squaring but higher power

### SPICE Subcircuit (Option A: MOSFET Squarer)

```spice
* Squarer-Based Envelope Detector
* Uses MOSFET square-law like RMS block (Block 05)

.subckt envelope_squarer vin vcm vout vdd gnd vbn vbn_lpf

* === Stage 1: MOSFET Squarer ===
* Signal NFET: gate = vin (BPF output)
* Reference NFET: gate = vcm
* Both drain to VDD through matched load resistors
* Difference = proportional to (vin-vcm)^2 after LPF

* Bias current source (sets operating point)
XMtail_sq tail_sq vbn gnd gnd sky130_fd_pr__nfet_01v8 w=2u l=4u

* Signal path
XMsig sq_sig vin tail_sq gnd sky130_fd_pr__nfet_01v8 w=2u l=1u
Rload_sig vdd sq_sig 100k

* Reference path
XMref sq_ref vcm tail_sq gnd sky130_fd_pr__nfet_01v8 w=2u l=1u
Rload_ref vdd sq_ref 100k

* Difference voltage: sq_ref - sq_sig propto (vin-vcm)^2 (after averaging)
* When vin > vcm: M_sig draws more current, sq_sig drops, diff goes positive
* When vin < vcm: M_sig draws less current, sq_sig rises, diff goes negative
* After squaring + LPF: always positive offset

* === Stage 2: Differential to single-ended + LPF ===
* Use OTA to convert differential squarer output to single-ended
* Then Gm-C LPF to average

* Simple approach: LPF on the signal path output directly
* sq_sig = VDD - R*I_sig, where I_sig depends on vin
* The DC component of sq_sig contains the envelope information

* Gm-C LPF (fc ~ 92 Hz)
XM1    d1   sq_sig tail gnd sky130_fd_pr__nfet_01v8 w=2u l=4u
XM2    vout vout   tail gnd sky130_fd_pr__nfet_01v8 w=2u l=4u
XMtail tail vbn_lpf gnd gnd sky130_fd_pr__nfet_01v8 w=1u l=8u
XMp3   d1   d1   vdd vdd sky130_fd_pr__pfet_01v8 w=4u l=4u
XMp4   vout d1   vdd vdd sky130_fd_pr__pfet_01v8 w=4u l=4u
Clpf vout gnd 5n

.ends envelope_squarer
```

## Expected Output Levels

Using MOSFET square-law with K=50 uA/V^2, R_load=100k:

| BPF Input (mVpp) | Vpeak (mV) | Squarer DC (mV) | Current Env (mV) | Ratio |
|-------------------|-----------|-----------------|------------------|-------|
| 10                | 5         | 0.06    | 1.6             | 0.0x  |
| 50                | 25        | 1.56   | 8.0             | 0.2x  |
| 100               | 50        | 6.25   | 16.0            | 0.4x  |
| 200               | 100       | 25.00  | 32.0            | 0.8x  |

**Problem**: The squarer output for small signals (5 mV) is TINY (0.062 mV),
much worse than the current rectifier. The quadratic law compresses small signals.

For the VibroSense application where BPF outputs are 10-200 mVpp, the squarer
produces 0.06-250 mV — a huge dynamic range but with VERY small outputs for
the "normal" case channels.

## Cross-Case Spread Estimate

Using actual BPF std values as proxy for amplitude:
- Normal BPF3: ~8.5 mV std -> squarer: ~0.18 mV
- Inner BPF3: ~31.9 mV std -> squarer: ~2.54 mV
- Spread: ~2.4 mV (LESS than current 6.4 mV for ENV3!)

**The squarer REDUCES discrimination for small signals.** This is worse than the current design
for the VibroSense signal levels.

## Power Estimate
- Squaring pair: ~2 uA at 1.8V = 3.6 uW
- Load resistors: negligible
- LPF: ~1.2 uW
- **Total: ~5 uW per channel** (lower than current 20 uW)

## Pros
1. No dead zone (smooth x^2 through zero)
2. Low power
3. Simple circuit (fewer transistors than OTA-based rectifier)
4. Proven topology (same as RMS block)

## Cons
1. **Quadratic compression makes small signals WORSE** — fatal for VibroSense
2. Need post-squarer gain to recover small-signal discrimination
3. Large dynamic range at output (need precision LPF)
4. Square-law only accurate for |Vin| < Vov (linearity limit)
5. Already implemented as RMS block — and RMS only shows 2.4 mV spread!

## Verdict

**NOT RECOMMENDED as standalone approach.** The RMS detector (Block 05) already
IS a squarer, and it only achieves 2.4 mV spread. A per-channel squarer would
be similarly poor. The quadratic transfer function suppresses the exact small-signal
differences we need to detect.

## Implementation Effort
- **Low**: Very similar to existing RMS block
- Risk: Low (proven topology), but improvement is negative
- Timeline: 1 week
