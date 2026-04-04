#!/usr/bin/env python3
"""Expert 05: Post-Envelope Gain Stage — amplify millivolt envelope differences."""

import os

OUTDIR = os.path.dirname(os.path.abspath(__file__))

report = """# Expert Report 05: Post-Envelope Gain Stage

## Problem Analysis

The current envelope detector WORKS CORRECTLY — it produces DC offsets proportional
to BPF amplitude. The problem is these offsets are only 1-10 mV on a 900 mV common-mode.

**The simplest fix**: add a high-gain amplifier after the envelope LPF to amplify
the millivolt differences to hundreds of millivolts.

Required gain:
- Current envelope spread: ~7 mV (best channel)
- Needed spread: ~500 mV (for good classifier discrimination)
- Required gain: 500/7 = **~70x**

## Proposed Architecture

### Block Diagram
```
BPF_out --[Existing Envelope Det]-- V_env (~0.9V + 1-10mV)
                                        |
                              [DC subtract VCM]
                                        |
                              [Gain = 50-100x]
                                        |
                              [Add back VCM]
                                        |
                                    V_amplified (~0.9V + 50-700mV)
```

### The AC-Coupling Problem

We need to amplify (V_env - VCM) by 70x and add it back to VCM:
    V_out = VCM + 70 * (V_env - VCM)

This is a DIFFERENTIAL amplifier with VCM reference. We can use:

1. **Capacitive-feedback amplifier** (like the PGA): AC-coupled, gain = C_in/C_fb
2. **Resistive-feedback OTA**: gain = R_f/R_in, need precise resistors
3. **Behavioral**: V_out = VCM + G*(V_env - VCM)

### Challenge: DC Amplification

The envelope output IS a DC signal. We cannot AC-couple it.
We need true DC amplification of (V_env - VCM).

Options:
- Instrumentation amplifier topology (three OTA)
- Single OTA with matched resistor ratio
- Behavioral B-source (for proof of concept)

### SPICE Subcircuit

```spice
* Post-Envelope DC Gain Stage
* Amplifies (V_env - VCM) by gain G, output = VCM + G*(V_env - VCM)

.subckt env_post_gain vin vcm vout vdd gnd vbn

* Parameters: Target gain = 70x
* Using behavioral source for proof-of-concept
* Real implementation would use instrumentation amplifier

* Compute amplified signal with rail clipping
B_gain vout gnd V = {
+   max(0.05, min(1.75,
+   v(vcm) + 70.0 * (v(vin) - v(vcm))
+   )) }

.ends env_post_gain

* Alternative: OTA-based implementation
* Uses two-stage OTA with resistive feedback
* Gain = R2/R1 = 7M / 100k = 70x

.subckt env_post_gain_ota vin vcm vout vdd gnd vbn

* Input resistor: R1 = 100k
R_in vin vm 100k

* Feedback resistor: R2 = 7M
R_fb vout vm 7000k

* Reference: VCM to virtual ground
R_ref vcm vm_ref 100k
R_ref_fb vout_ref vm_ref 7000k

* OTA (high-gain, drives output)
* Inverting config: V(vm) is virtual ground at VCM
* V_out = VCM - (R2/R1)*(V_in - VCM) ... but we want non-inverting

* For non-inverting: use instrumentation amp topology
* Simpler: use the behavioral version above for now

* Fallback: behavioral with gain
B_gain vout gnd V = {
+   max(0.05, min(1.75,
+   v(vcm) + 70.0 * (v(vin) - v(vcm))
+   )) }

.ends env_post_gain_ota
```

## Expected Output Levels with 70x Gain

| Channel | Normal (mV from VCM) | Inner (mV) | Outer (mV) | Ball (mV) | Spread (mV) |
|---------|---------------------|-----------|-----------|----------|-------------|
| ENV1    | +304               | +304      | +285      | +310     | 25          |
| ENV2    | +449               | +616      | +599      | +559     | 167         |
| ENV3    | +227               | +678      | +657      | +568     | 451         |
| ENV4    | +135               | +595      | +479      | +536     | 460         |
| ENV5    | +102               | +447      | +297      | +375     | 345         |

**Total feature range: 0.80-1.58 V** — spans most of the 0-1.8V range!

However: ENV1 gain of 70x on 4.3 mV = 301 mV for ALL cases. ENV1 has only
0.35 mV raw spread -> 24.5 mV amplified spread. Still marginal for ENV1.

## Offset Problem

The critical challenge: OTA input offset voltage.
- Typical OTA offset in SKY130: 5-20 mV
- After 70x gain: 350-1400 mV offset error!
- This is LARGER than the signal we're trying to amplify.

**Offset cancellation is essential:**
- Chopper stabilization: chop at ~1 kHz, but envelope is DC... can't chop DC
- Auto-zeroing: sample offset in reset phase, subtract during measurement
- Trim: laser trim or digital calibration of offset

Without offset cancellation, the post-gain approach is UNRELIABLE.

## Power Estimate
- Behavioral: 0 uW (ideal)
- OTA-based instrumentation amp: ~15-30 uW per channel (3 OTAs)
- With offset cancellation: add ~5 uW for auto-zero logic
- **Total: ~20-35 uW per channel** (DOUBLES the current power)
- 5 channels: 100-175 uW additional

## Pros
1. Simplest conceptual fix (just add gain)
2. Preserves existing envelope detector (no redesign)
3. Directly maps millivolt features to hundreds of millivolts
4. With behavioral model, immediately testable

## Cons
1. **OTA offset at 70x gain is catastrophic** (5 mV offset -> 350 mV error)
2. High power if using real OTAs (doubles total envelope power budget)
3. Output clips at rails for large inputs (gain * 10 mV = 700 mV, OK; gain * 100 mV = clipped)
4. Amplifies noise as well as signal (70x noise amplification)
5. Requires precision gain setting (1% resistor matching for 1% gain accuracy)
6. Only works if envelope offsets are well-controlled (they have ~2-5 mV std dev ripple)

## Verdict

**NOT RECOMMENDED as primary approach** due to the offset problem.
At 70x gain, offset cancellation is mandatory but hard to implement for DC signals.

However, a MODERATE gain (5-10x) combined with classifier retraining could work:
- 5x gain: envelope spread 7 mV -> 35 mV, offset error 5*20 = 100 mV (manageable)
- 10x gain: envelope spread 7 mV -> 70 mV, offset error 10*20 = 200 mV (marginal)

**Useful as a supplementary technique, not standalone.**

## Implementation Effort
- **Low** (behavioral): 1 day, just add B-source after each envelope
- **High** (transistor-level with offset cancellation): 3-4 weeks
- Risk: High (offset is the dominant error source)
"""

with open(os.path.join(OUTDIR, 'expert_05_post_gain.md'), 'w') as f:
    f.write(report)

print("Expert 05 (Post-Envelope Gain) report written.")
