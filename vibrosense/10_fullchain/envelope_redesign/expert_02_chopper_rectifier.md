# Expert Report 02: Chopper-Stabilized Rectifier

## Problem Analysis

The current OTA-based rectifier has two issues:
1. Dead zone of ~0.3 mV (small but contributes to loss at low amplitudes)
2. Half-wave only (loses half the signal energy)
3. OTA offset voltages add systematic errors

Chopper stabilization modulates the signal to a higher frequency, amplifies it
(free from 1/f noise and offset), then demodulates back. For a rectifier,
we can use synchronous rectification: multiply the signal by sgn(signal).

## Proposed Architecture

### Block Diagram
```
BPF_out --[Comparator]-- CLK (sign of input)
    |                       |
    +--[Chopper Switch]-----+--[LPF]-- V_env
       (multiply by +/-1)
```

The key insight: if we know the SIGN of the BPF output (above/below VCM),
we can use CMOS switches to invert the signal during negative half-cycles,
achieving ideal full-wave rectification with ZERO dead zone.

### How to Get the Sign

A fast comparator compares BPF_out vs VCM. Output is digital (0 or VDD).
This drives CMOS transmission gate switches that either pass or invert the signal.

### Clock Frequency

Not a traditional chopper clock - the "clock" IS the signal itself (zero-crossing detector).
For BPF3 at 3162 Hz: the comparator must toggle at ~6.3 kHz (twice per cycle).
For BPF5 at 14639 Hz: ~29.3 kHz. This is easily achievable in SKY130.

### SPICE Subcircuit

```spice
* Chopper-Rectified Envelope Detector
* Synchronous full-wave rectification using signal zero-crossing

.subckt envelope_chopper vin vcm vout vdd gnd vbn vbn_lpf

* === Stage 1: Zero-crossing detector (comparator) ===
* Fast comparator: high gain OTA with rail-to-rail output
* When vin > vcm: comp_out = VDD (sign = +1)
* When vin < vcm: comp_out = 0V (sign = -1)
B_comp comp_out gnd V = { v(vin) > v(vcm) ? v(vdd) : 0 }

* Inverted comparator output
B_compb comp_outb gnd V = { v(vin) > v(vcm) ? 0 : v(vdd) }

* === Stage 2: Synchronous rectifier (CMOS switches) ===
* Path A (vin > vcm): pass vin directly
* Path B (vin < vcm): pass (2*vcm - vin) = mirror around VCM

* Direct path: transmission gate passes vin when vin > vcm
XMsw1n rect_a comp_out  vin    gnd sky130_fd_pr__nfet_01v8 w=1u l=0.15u
XMsw1p rect_a comp_outb vin    vdd sky130_fd_pr__pfet_01v8 w=2u l=0.15u

* Mirror path: need to generate (2*VCM - vin)
* Use unity-gain inverting amplifier referenced to VCM
B_mirror mirror gnd V = { 2*v(vcm) - v(vin) }

* Mirrored path: transmission gate passes mirror when vin < vcm
XMsw2n rect_b comp_outb mirror gnd sky130_fd_pr__nfet_01v8 w=1u l=0.15u
XMsw2p rect_b comp_out  mirror vdd sky130_fd_pr__pfet_01v8 w=2u l=0.15u

* Sum both paths (one is always on, one off)
R_a rect_a rect_sum 1k
R_b rect_b rect_sum 1k

* === Stage 3: Gm-C LPF (same topology, fc ~ 92 Hz) ===
XM1    d1   rect_sum tail gnd sky130_fd_pr__nfet_01v8 w=2u l=4u
XM2    vout vout     tail gnd sky130_fd_pr__nfet_01v8 w=2u l=4u
XMtail tail vbn_lpf  gnd  gnd sky130_fd_pr__nfet_01v8 w=1u l=8u
XMp3   d1   d1   vdd vdd sky130_fd_pr__pfet_01v8 w=4u l=4u
XMp4   vout d1   vdd vdd sky130_fd_pr__pfet_01v8 w=4u l=4u
Clpf vout gnd 5n

.ends envelope_chopper
```

## Expected Dynamic Range Improvement

Full-wave (2x over half-wave) + zero dead zone:

| Input (mVpp) | Current (half-wave, mV) | Chopper (full-wave, mV) | Ratio |
|--------------|------------------------|------------------------|-------|
| 10           | 1.6                    | 3.2                    | 2.0x  |
| 50           | 8.0                    | 15.9                   | 2.0x  |
| 100          | 16.0                   | 31.8                   | 2.0x  |
| 200          | 32.0                   | 63.7                   | 2.0x  |

Cross-case spread: 6.6 mV -> ~13 mV (2x improvement from full-wave).

**The chopper approach only gives 2x. This is NOT enough.**
The classifier needs features spanning hundreds of mV, not tens.

## Power Estimate
- Comparator: ~1 uW (simple inverter-based)
- Switches: negligible (CMOS gates)
- Mirror amplifier: ~2 uW (if behavioral B-source, 0; if OTA-based, ~2 uW)
- LPF: ~1.2 uW (same as current)
- **Total: ~4-5 uW per channel**

## Pros
1. Zero dead zone (switches have no threshold)
2. Full-wave rectification (2x output vs half-wave)
3. Low power (no high-gain OTAs needed for rectification)
4. Simple digital logic (comparator + switches)

## Cons
1. Only 2x improvement over current design (insufficient alone)
2. B_mirror is behavioral - needs a real inverting amplifier around VCM
3. Switch charge injection at zero crossings creates glitches
4. Comparator delay at high frequencies (BPF5 at 15 kHz) may cause errors
5. Still produces small DC offsets for small BPF signals

## Implementation Effort
- **Medium**: Comparator and switches are straightforward. The mirror amplifier
  (2*VCM - Vin) is the hardest part - needs a unity-gain inverting OTA.
- Risk: charge injection from switches degrades accuracy for small signals
- Timeline: 1-2 weeks
