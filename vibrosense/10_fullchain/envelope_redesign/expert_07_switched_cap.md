# Expert Report 07: Switched-Capacitor Envelope Detector

## Problem Analysis

The continuous-time Gm-C LPF approach suffers from:
1. Limited output swing (envelope stuck near VCM)
2. Gm-C frequency depends on process variation
3. Cannot easily implement programmable gain or time windowing

A switched-capacitor (SC) approach operates in discrete time, using clock phases
to sample, rectify, and integrate. Key advantage: gain is set by capacitor RATIOS
(not absolute values), which are very accurate in CMOS.

## Proposed Architecture

### Correlated Double Sampling SC Integrator
```
Phase 1 (sample):
  BPF_out --> [C_s] --> virtual ground of OTA

Phase 2 (integrate):
  [C_s] charge transferred to [C_int] via OTA feedback
  If BPF > VCM: positive charge added
  If BPF < VCM: also positive charge added (rectification by sign switching)
```

### Block Diagram
```
                    phi1        phi2
BPF_out ---[Csamp]---+---[OTA]---+---[Cint]--- V_env_sc
                      |           |
VCM --------[sw]------+   [Cfb]--+
                      |           |
Sign --------[sw]-----+           |
(from comparator)                 |
                                 V_env_sc
```

### Clock: Use FSM Timing

The existing digital_wrapper provides phi_s, phi_e, phi_r clocks.
The SC rectifier can use phi_s for sampling and phi_e for integration.
This provides natural TIME WINDOWING of the envelope measurement.

### SPICE Subcircuit

```spice
* Switched-Capacitor Envelope Detector
* Uses SC integrator with sign-switching for rectification
* Compatible with FSM clocking

.subckt envelope_sc vin vcm vout vdd gnd phi1 phi2

* === Comparator (sign detection) ===
B_sign sign gnd V = { v(vin) > v(vcm) ? v(vdd) : 0 }
B_signb signb gnd V = { v(vin) > v(vcm) ? 0 : v(vdd) }

* === Sampling capacitor ===
* During phi1: C_s charges to (vin - vcm) or (vcm - vin)
* During phi2: charge transferred to C_int

* Behavioral SC rectifier + integrator
* Each clock cycle adds |vin - vcm| * C_s / C_int to output
* With C_s = 1 pF, C_int = 10 pF: gain = 0.1 per sample
* Over N samples: V_out = VCM + (C_s/C_int) * sum(|vin - vcm|)

* For simplicity, use behavioral model:
* V_out = VCM + G * mean(|vin - vcm|) where G = N * Cs/Cint

* Behavioral with rectification + integration (continuous-time approximation)
* The SC nature is captured by the gain ratio
B_sc vout gnd V = {
+   max(0.05, min(1.75,
+   v(vcm) + 10.0 * abs(v(vin) - v(vcm))
+   )) }

* NOTE: This behavioral model approximates the SC behavior.
* A true SC implementation would use switched capacitor networks
* with actual MOSFET switches and non-overlapping clocks.
* The gain of 10x comes from: N_cycles * C_s/C_int
* With f_sample = 50 kHz, integration window = 10 ms:
*   N = 500 cycles, C_s/C_int = 0.1, effective gain = 50x
*   But averaging: gain = C_s/C_int * (1/duty) ~ 10x net

.ends envelope_sc
```

## Expected Output Levels

With effective gain of 10x on rectified signal:
- Full-wave rectified: DC = (2/pi)*Vpeak = 0.637*Vpeak

| BPF (mVpp) | Vpeak | Rectified DC (mV) | With 10x SC gain (mV) | Current env (mV) |
|------------|-------|--------------------|----------------------|------------------|
| 10         | 5     | 3.2                | 32                   | 1.6              |
| 50         | 25    | 15.9               | 159                  | 8.0              |
| 100        | 50    | 31.8               | 318                  | 16.0             |
| 200        | 100   | 63.7               | 637 (clipped to rail)| 32.0             |

Cross-case spread with 10x gain: 6.6 * 10 = **66 mV** (vs current 6.6 mV)

## Pros
1. Gain set by capacitor ratios (process-insensitive)
2. Natural integration/windowing (compatible with FSM timing)
3. Programmable gain by changing C_s/C_int ratio
4. Can combine rectification + gain in one stage
5. No DC offset problem (auto-zeroing inherent in SC circuits)
6. Well-established methodology in SKY130

## Cons
1. Needs non-overlapping clocks (available from digital wrapper)
2. Clock feedthrough / charge injection at switches
3. Sampling rate must be > 2x BPF frequency (Nyquist)
4. For BPF5 at 15 kHz: need f_sample > 30 kHz (achievable)
5. kT/C noise: with 1 pF sampling cap, noise = sqrt(kT/C) = 64 uV (acceptable)
6. More complex layout (switched networks)
7. The behavioral model above is a placeholder — real SC needs clock phases

## Power Estimate
- OTA (for integrator): ~2 uW
- Comparator: ~1 uW
- Switch drivers: ~0.5 uW
- **Total: ~3.5 uW per channel**

## Verdict

**MODERATELY RECOMMENDED.** The SC approach provides:
- Built-in gain from capacitor ratios (no separate amplifier)
- Auto-zeroing eliminates offset
- Compatible with existing FSM clocking

But the behavioral model used here doesn't capture SC dynamics accurately.
A proper SC design requires careful switch sizing and clock generation.

The main advantage over post-gain (Expert 05) is the inherent auto-zeroing
of SC circuits, which solves the offset problem.

## Implementation Effort
- **High**: SC design requires careful switch sizing, clock generation, and
  attention to charge injection. The behavioral model above is a gross
  simplification.
- Risk: Medium (well-known methodology but complex implementation)
- Timeline: 3-4 weeks for proper SC design
