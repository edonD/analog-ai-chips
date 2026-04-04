# Expert Report 09: Current-Mode Envelope Detector

## Problem Analysis

The current envelope detector operates in voltage mode throughout:
- BPF output: voltage signal on VCM
- Rectifier: voltage follower (OTA + PMOS)
- LPF: Gm-C (voltage in, voltage out)
- Output: voltage near VCM

The voltage-mode approach has a fundamental headroom problem:
- VCM = 0.9V uses half the 1.8V supply
- Envelope output is VCM + small offset
- The useful signal range is compressed

In current mode:
- Signal is represented as a current (not voltage)
- No common-mode voltage to waste headroom
- Current can be easily rectified, summed, and integrated
- Final conversion to voltage only at the output (charge on cap)

## Proposed Architecture

### Block Diagram
```
BPF_out --[OTA: V-to-I]--[Current Mirror Rectifier]--[Integration Cap]-- V_out
                |                   |                        |
                +--[gm*(Vin-VCM)]--+--[|I| = gm*|Vin-VCM|]--+-- Q = integral(|I|)dt
                                                              V = Q/C = (gm/C)*integral(|V|)dt
```

### Key Insight

The OTA already produces a current proportional to (Vin - VCM).
Instead of feeding this into a voltage-mode LPF, we integrate
the RECTIFIED current directly onto a capacitor:

    V_out = (1/C) * integral(gm * |Vin - VCM|) dt

Over integration time T (200 ms):
    V_out = (gm * T / C) * mean(|Vin - VCM|)

The "gain" is gm * T / C. With gm = 10 uA/V, T = 200 ms, C = 1 nF:
    Gain = 10e-6 * 0.2 / 1e-9 = 2000 V/V!

We can choose C to set any gain we want. For reasonable output:
- C = 100 nF: Gain = 20 V/V (feasible, 100 nF is large but possible)
- C = 10 nF: Gain = 200 V/V (too high, clips)
- C = 50 nF: Gain = 40 V/V (good range)

### SPICE Subcircuit

```spice
* Current-Mode Envelope Detector
* V-to-I (OTA) -> Current Rectifier -> Charge Integration

.subckt envelope_current vin vcm vout vdd gnd vbn vbn_lpf

* === Stage 1: V-to-I Conversion (OTA as transconductor) ===
* OTA output current: I = gm * (vin - vcm)
* gm = 10 uA/V (moderate, achievable with ~500 nA bias)

* Positive half: I+ = max(0, gm*(vin-vcm))
B_ipos gnd ipos I = max(0, 10e-6 * (v(vin) - v(vcm)))

* Negative half: I- = max(0, gm*(vcm-vin))
B_ineg gnd ineg I = max(0, 10e-6 * (v(vcm) - v(vin)))

* Full-wave rectified current: |I| = I+ + I-
* Both charge the integration cap

* === Stage 2: Current Integration ===
* Charge integration cap with rectified current
* V_out rises from 0 toward (gm/C) * integral(|Vin-VCM|)dt

* Current from ipos and ineg nodes onto integration cap
* Using B-source for ideal current summing
B_rect gnd vout I = max(0, 10e-6 * abs(v(vin) - v(vcm)))

* Integration capacitor (starting from VCM)
C_int vout gnd 50n
R_leak vout gnd 100Meg

* Initial condition: start at 0V (output RISES proportional to envelope energy)
* After 200ms: V_out = (10e-6 / 50e-9) * 0.2 * mean(|Vin-VCM|)
*            = 40 * mean(|Vin-VCM|)

.ends envelope_current
```

## Expected Output Levels

With gm = 10 uA/V, C = 50 nF, T = 200 ms:
Effective gain = gm * T / C = 40 V/V on mean(|Vin - VCM|)

For BPF output with amplitude A: mean(|sin|) = (2/pi)*A = 0.637*A

| BPF (mVpp) | Vpeak | mean(|V|) (mV) | V_out = 40*mean(|V|) (mV) | Current env (mV) |
|------------|-------|----------------|---------------------------|------------------|
| 10         | 5     | 3.2            | 127                       | 1.6              |
| 50         | 25    | 15.9           | 637                       | 8.0              |
| 100        | 50    | 31.8           | 1273 (clipped)            | 16.0             |

**For the typical BPF range (20-200 mVpp), output spans 250-1800 mV!**

Cross-case spread estimate:
- Normal BPF3 (28 mVpk): V_out = 40 * 0.637 * 14 = 356 mV
- Inner BPF3 (91 mVpk): V_out = 40 * 0.637 * 46 = 1171 mV (may clip)
- Spread: ~815 mV!

**With C = 100 nF (gain = 20x):**
- Normal BPF3: 178 mV
- Inner BPF3: 586 mV
- Spread: ~408 mV — EXCELLENT

## The Leakage/Reset Problem

The integration cap accumulates charge continuously. After 200 ms, it may
saturate at the rail. Solutions:
1. **Periodic reset** (use phi_r from FSM): reset cap to 0V, integrate for one window
2. **Resistive leak** (R_leak = 100 Meg): provides slow discharge, creates effective LPF
   with tau = R*C = 100M * 50n = 5 seconds (too slow for 200 ms window)
3. **Active discharge**: NMOS switch controlled by reset clock

With periodic reset (recommended):
- Reset cap to 0V at start of measurement window
- Integrate for 20-50 ms (5-10 time constants of BPF envelope)
- Sample output at end of integration window
- V_out is proportional to average BPF amplitude during window

## Power Estimate
- V-to-I OTA: ~1 uA = 1.8 uW
- Current mirrors/rectifier: ~0.5 uA = 0.9 uW
- Integration (passive cap): 0 uW
- **Total: ~3 uW per channel** (current: 20 uW)
- **7x power reduction!**

## Pros
1. **Natural gain from integration** (gm*T/C can be very large)
2. **No headroom problem** (output starts from 0V, uses full rail)
3. **Full-wave rectification built-in** (two half-wave current sources)
4. **Low power** (no LPF OTA needed, passive integration)
5. **Process-insensitive gain** (gm*T/C, T is from clock, C is accurate)
6. **Wide output range** (0 to 1.8V, not stuck near VCM)

## Cons
1. Needs periodic reset (tied to FSM timing)
2. B-sources are behavioral — transistor-level current mirror rectifier needs design
3. Integration time must be controlled precisely (gain depends on T)
4. Cap leakage in real silicon (charge loss during integration)
5. Output is single-shot (one measurement per reset cycle, not continuous)
6. Need large cap (50-100 nF) — may need off-chip or MIM cap stack

## Verdict

**RECOMMENDED as a strong candidate.** The current-mode approach solves BOTH
major problems:
1. No VCM offset (output starts from 0V or near ground)
2. Built-in gain from integration (40x with reasonable C)

The main implementation challenge is building a transistor-level current
rectifier, but this is a well-known circuit (current mirror full-wave rectifier).

## Implementation Effort
- **Medium**: Current mirrors are standard, integration cap is passive
  The B-source version works immediately for simulation.
  Transistor-level: 2-3 weeks for current mirror rectifier + verification
- Risk: Medium (large cap value, need periodic reset)
- Timeline: 2 weeks with behavioral, 4 weeks with transistor-level
