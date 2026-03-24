# Block 03: 5-Channel Gm-C Tow-Thomas Band-Pass Filter Bank

## Design Program — Complete Specification and Verification Plan

---

## 1. Context and Motivation

Vibration fault diagnosis relies on identifying which frequency bands contain abnormal
energy. A digital system would sample at 50 kHz and compute a 1024-point FFT (512
frequency bins, ~10 Hz resolution). This costs 3-10 mW continuously.

VibroSense-1 replaces the digital FFT with 5 analog band-pass filters that decompose the
vibration signal into 5 frequency bands. Each band covers a range where specific mechanical
faults manifest:

| Channel | Band | Detects |
|---------|------|---------|
| 1 | 100-500 Hz | Shaft imbalance, bearing BPFO/BPFI |
| 2 | 500-2000 Hz | Gear mesh faults, bearing harmonics |
| 3 | 2-5 kHz | Bearing ball spin frequency, resonances |
| 4 | 5-10 kHz | Early bearing damage, high-freq resonances |
| 5 | 10-20 kHz | Incipient faults (broadband ultrasonic) |

This is 5 "bins" instead of 512, but it is sufficient because fault detection is a coarse
classification problem — we need to know *which band* has excess energy, not the exact
frequency to 10 Hz resolution.

---

## 2. State of the Art Comparison

| Parameter | Nauta JSSC'92 | Harrison JSSC'03 | Sawigun TCAS-I'12 | Corradi JSSC'15 | **This Work** |
|-----------|--------------|-------------------|-------------------|-----------------|---------------|
| Topology | Nauta Gm-C | OTA-C BPF | Tow-Thomas | Cochlea cascade | Tow-Thomas biquad |
| Order | 2nd | 2nd per stage | 4th | 2nd per stage | 2nd per channel |
| Channels | 1 | 1 | 1 | 16 | 5 |
| Freq range | 1-100 MHz | 80 mHz-5 kHz | 0.1-300 Hz | 100 Hz-10 kHz | 100 Hz-20 kHz |
| Power/channel | ~1 mW | 80 uW | 3.3 nW | 55 nW | 5-50 uW |
| Supply | 5V | 2.8V | 0.5V | 1.8V | 1.8V |
| THD | -40 dBc | -40 dBc | -40 dBc | N/A | <-30 dBc |
| Process | 3um CMOS | 1.5um CMOS | 0.18um CMOS | 0.18um CMOS | SKY130 130nm |
| Tuning | Bias current | Bias current | Bias current | Digital trimming | 4-bit DAC |

### Analysis of Prior Art

**Nauta (JSSC 1992):** The classic Gm-C paper. Demonstrated that transconductor-capacitor
filters can achieve high-frequency, tunable filtering. Power is 1 mW — far above our budget.
Relevant for topology understanding but not for our frequency range.

**Harrison & Charles (JSSC 2003):** Neural recording BPF designed for biopotential.
80 mHz high-pass corner demonstrates that Gm-C can work at extremely low frequencies
with subthreshold OTAs. 80 uW per channel is above our budget for the low-frequency
channels but comparable for high-frequency ones.

**Sawigun (TCAS-I 2012):** Achieves 3.3 nW per channel at 0.5V — extraordinary efficiency
by operating deep in subthreshold. However, max frequency is 300 Hz and THD degrades for
signals >50 mVpp. Not directly applicable to our 20 kHz channel but validates the Gm-C
approach at extreme low power.

**Corradi et al. (JSSC 2015):** 16-channel cochlea filterbank at 55 nW per channel. Uses
cascaded 2nd-order sections with bio-inspired frequency spacing. Demonstrates that
multi-channel filter banks are feasible at sub-microwatt power. However, uses a different
topology (cochlea cascade with exponential frequency spacing) and achieves lower Q than
our specifications.

**Our position:** We target 5 channels at 5-50 uW per channel depending on center
frequency. This is 10-100x more power than Sawigun/Corradi, but we operate at much higher
frequencies (up to 20 kHz) and need higher linearity (-30 dBc THD). The power scales with
frequency because gm must increase proportionally, and gm ~ Ibias in subthreshold.

---

## 3. Topology: Tow-Thomas Biquad

### 3.1 The Tow-Thomas Structure

Each channel uses a Tow-Thomas biquad: two integrators (gm1/C1 and gm2/C2) in a feedback
loop with a damping transconductor (gm3).

```
                              ┌────────────────────────────────┐
                              │                                │
    Vin ──────► gm1 ──────┬──┴──► C1 ──────► gm2 ──────► C2 ──┴──► Vout (BP)
                          │                                    │
                          └────────────── gm3 ◄────────────────┘
                                        (damping)
```

### 3.2 Transfer Function

The band-pass output is taken at the output of the first integrator:

```
                    (gm1/C1) × s
    H_BP(s) = ─────────────────────────────────────
              s² + (gm3/C1) × s + (gm1×gm2)/(C1×C2)
```

Note: The damping term is gm3/C1 (not gm3/C2) because OTA3 feeds into
the C1 node (V1, first integrator output where the BP output is taken).

Mapping to standard biquad parameters:

```
    Center frequency:  w0 = sqrt(gm1 × gm2 / (C1 × C2))
    Quality factor:    Q  = sqrt(gm1 × gm2 × C1 / (gm3² × C2))
    Peak gain:         G0 = gm1 / gm3
```

When gm1 = gm2 = gm3 = gm (all OTAs at same bias, Q set by cap ratio):

```
    Q  = sqrt(C1 / C2)     [not gm/gm3]
    G0 = 1  (0 dB)         [not Q]
```

When gm1 = gm2 = gm and C1 = C2 = C (symmetric design):

```
    w0 = gm / C
    Q  = gm / gm3
    G0 = gm / gm3 = Q
```

For unity peak gain: set gm3 = gm (Q = 1 has 0 dB peak gain).

### 3.3 Why Tow-Thomas

1. **Independent tuning:** f0 is set by gm/C ratio. Q is set by gm/gm3 ratio. These can
   be adjusted independently.
2. **Low sensitivity:** The Tow-Thomas has sensitivity |S| <= 1/2 for all passive elements,
   making it robust to component variation.
3. **Natural for Gm-C:** Each transconductor is a single OTA. No resistors needed.
4. **Tuning via bias current:** gm ~ Ibias (subthreshold) or gm ~ sqrt(Ibias) (strong
   inversion). Sweeping Ibias tunes f0 without changing Q (if all gm's track).

---

## 4. Channel Specifications

### 4.1 Exact Design Parameters

| Parameter | Ch 1 | Ch 2 | Ch 3 | Ch 4 | Ch 5 |
|-----------|------|------|------|------|------|
| **Band** | 100-500 Hz | 500-2 kHz | 2-5 kHz | 5-10 kHz | 10-20 kHz |
| **f0** | 224 Hz | 1000 Hz | 3162 Hz | 7071 Hz | 14142 Hz |
| **Q** | 0.75 | 0.67 | 1.05 | 1.41 | 1.41 |
| **gm_target** | 14 nS | 63 nS | 199 nS | 444 nS | 889 nS |
| **C1 = C2** | 10 pF | 10 pF | 10 pF | 10 pF | 10 pF |
| **Ibias/OTA** | 50 nA | 200 nA | 500 nA | 1.2 uA | 2.5 uA |
| **gm3 (=gm/Q)** | 18.7 nS | 94 nS | 190 nS | 315 nS | 630 nS |

### 4.2 Derivation of gm from f0 and C

For the symmetric Tow-Thomas (gm1=gm2=gm, C1=C2=C):

```
    f0 = gm / (2*pi*C)
    gm = 2*pi*f0*C
```

| Channel | f0 | C | gm = 2*pi*f0*C | Listed gm |
|---------|-----|---|----------------|-----------|
| 1 | 224 Hz | 10 pF | 14.07 nS | 14 nS |
| 2 | 1000 Hz | 10 pF | 62.83 nS | 63 nS |
| 3 | 3162 Hz | 10 pF | 198.7 nS | 199 nS |
| 4 | 7071 Hz | 10 pF | 444.3 nS | 444 nS |
| 5 | 14142 Hz | 10 pF | 888.6 nS | 889 nS |

### 4.3 Center Frequency Rationale

Each f0 is the geometric mean of the band edges:

```
    f0 = sqrt(f_low × f_high)
    Ch1: sqrt(100 × 500) = 223.6 Hz ≈ 224 Hz
    Ch2: sqrt(500 × 2000) = 1000 Hz
    Ch3: sqrt(2000 × 5000) = 3162 Hz
    Ch4: sqrt(5000 × 10000) = 7071 Hz
    Ch5: sqrt(10000 × 20000) = 14142 Hz
```

### 4.4 Q Factor Rationale

Q determines the passband width: BW_3dB = f0/Q.

| Channel | f0 | Desired BW | Q = f0/BW |
|---------|-----|-----------|-----------|
| 1 | 224 Hz | 300 Hz (100-400 Hz) | 0.75 |
| 2 | 1000 Hz | 1500 Hz (250-1750 Hz) | 0.67 |
| 3 | 3162 Hz | 3000 Hz (1660-4660 Hz) | 1.05 |
| 4 | 7071 Hz | 5000 Hz (4570-9570 Hz) | 1.41 |
| 5 | 14142 Hz | 10000 Hz (9140-19140 Hz) | 1.41 |

Channels 1-2 have low Q (broad passband) to capture a wide range of shaft and gear
frequencies. Channels 4-5 have higher Q to provide better selectivity in the
high-frequency range where spectral features are narrower.

### 4.5 Bias Current to gm Mapping

In the SKY130 subthreshold regime, gm = Ibias / (n × Vt), where n ≈ 1.3 (subthreshold
slope factor) and Vt = kT/q ≈ 26 mV at 27C.

```
    gm = Ibias / (1.3 × 26 mV) = Ibias / 33.8 mV = 29.6 × Ibias
```

| Channel | gm_target | Ibias = gm / 29.6 | Listed Ibias |
|---------|-----------|-------------------|--------------|
| 1 | 14 nS | 0.47 nA | 50 nA |
| 2 | 63 nS | 2.1 nA | 200 nA |
| 3 | 199 nS | 6.7 nA | 500 nA |
| 4 | 444 nS | 15 nA | 1.2 uA |
| 5 | 889 nS | 30 nA | 2.5 uA |

**Note:** The listed Ibias values are much higher than the theoretical minimum. This is
because:
1. The folded-cascode OTA has multiple current branches (total supply current ~ 6x Ibias)
2. Need margin for output swing and linearity
3. Higher Ibias gives better matching and noise
4. In practice, OTA gm efficiency (gm/Itotal) is 5-15 V^-1, not the ideal 29.6 V^-1

The exact Ibias will be determined by simulation with the real OTA. The values listed are
initial estimates that may need adjustment.

---

## 5. Frequency Tuning System

### 5.1 The PVT Problem

Gm-C filters have a fundamental problem: gm depends on bias current, threshold voltage,
mobility, and temperature. Across process corners and temperature:

- **Process:** gm varies +/-20-30% across TT/FF/SS corners
- **Temperature:** gm varies +/-15-20% from -40C to 85C (subthreshold: gm ~ Ibias/nVt,
  and Vt increases with T)
- **Supply:** gm varies +/-5% with +/-10% supply variation

**Combined worst case:** f0 can shift by +/-30-50% from nominal.

Without tuning, a filter designed for f0 = 1 kHz could land anywhere from 500 Hz to
1.5 kHz in production. This is unacceptable for vibration diagnosis where frequency
bands are defined by mechanical physics.

### 5.2 4-Bit Programmable Bias DAC

Each channel's bias current is set by a 4-bit binary-weighted current DAC:

```
                    ┌───────────────────────────────────────────────┐
                    │            4-Bit Bias Current DAC              │
                    │                                               │
    Iref ───────────┤    b3─► 8×Iunit ─┐                           │
    (from Block 00) │    b2─► 4×Iunit ─┤                           │
                    │    b1─► 2×Iunit ─┼──► Ibias_out ─► to OTAs  │
                    │    b0─► 1×Iunit ─┘                           │
                    │                                               │
                    │    Ibias_out = Iunit × (8×b3 + 4×b2 + 2×b1 + b0) │
                    │    Range: Iunit to 15×Iunit                   │
                    └───────────────────────────────────────────────┘
```

### 5.3 Tuning Range Calculation

The DAC provides codes 0001 to 1111 (1 to 15). Code 0000 is excluded (filter off).
The nominal code is set to the middle of the range (code 1000 = 8).

```
    Ibias_nominal = 8 × Iunit
    Ibias_min = 1 × Iunit = 0.125 × Ibias_nominal
    Ibias_max = 15 × Iunit = 1.875 × Ibias_nominal
```

Since gm ~ Ibias (subthreshold), f0 ~ Ibias:

```
    f0_min = 0.125 × f0_nominal
    f0_max = 1.875 × f0_nominal
```

**Tuning range: -87.5% to +87.5%** — far exceeds the +/-50% PVT variation.

### 5.4 Iunit Values per Channel

| Channel | Ibias_nominal | Iunit = Ibias/8 | Min Ibias (code 1) | Max Ibias (code 15) |
|---------|--------------|-----------------|--------------------|--------------------|
| 1 | 50 nA | 6.25 nA | 6.25 nA | 93.75 nA |
| 2 | 200 nA | 25 nA | 25 nA | 375 nA |
| 3 | 500 nA | 62.5 nA | 62.5 nA | 937.5 nA |
| 4 | 1.2 uA | 150 nA | 150 nA | 2.25 uA |
| 5 | 2.5 uA | 312.5 nA | 312.5 nA | 4.69 uA |

### 5.5 DAC Implementation

Each Iunit cell is a cascode current mirror driven by Iref from Block 00:

```spice
* Unit current cell
M1 (drain gate source bulk) sky130_fd_pr__nfet_01v8 W=2u L=4u
M2 (drain gate source bulk) sky130_fd_pr__nfet_01v8 W=2u L=4u  ; cascode
* Switch: NMOS in series with drain
M_sw (drain_out bit drain bulk) sky130_fd_pr__nfet_01v8 W=1u L=0.15u
```

Long-channel (L=4u) mirrors for good matching. Binary weighting achieved by parallel
unit cells: 1x, 2x, 4x, 8x.

### 5.6 Calibration Procedure

At power-on or during factory test:
1. Apply known-frequency test tone to filter input
2. Sweep DAC code from 1 to 15
3. Measure output amplitude at each code
4. Select code that maximizes output (filter tuned to test frequency)
5. Store optimal codes in on-chip registers (per channel)

For in-field recalibration (temperature compensation):
1. Periodically (every 60 seconds), the digital block can run a quick sweep
2. Use the PGA output as the reference signal
3. Adjust DAC codes to track temperature drift

---

## 6. PASS/FAIL Criteria

### 6.1 Per-Channel Specifications

| Parameter | Specification | Condition | PASS/FAIL |
|-----------|--------------|-----------|-----------|
| Center frequency f0 | +/-5% of nominal | TT corner, 27C, code=8 | MUST PASS |
| f0 after tuning | +/-10% of nominal | All corners, -40/27/85C, any code | MUST PASS |
| Quality factor Q | +/-20% of nominal | TT corner, 27C | MUST PASS |
| Peak gain (at f0) | +/-1 dB of nominal | TT corner, 27C | MUST PASS |
| Stopband rejection | >15 dB | At 0.1×f0 and 10×f0 | MUST PASS |
| In-band noise | <1 mVrms | Integrated over passband | MUST PASS |
| THD | <-30 dBc | At 200 mVpp input, f=f0 | MUST PASS |
| Power per channel | Within 2x of Table 4.1 | TT 27C | SHOULD PASS |

### 6.2 System-Level Specifications

| Parameter | Specification | PASS/FAIL |
|-----------|--------------|-----------|
| Tuning DAC covers +/-50% PVT | Proven across ALL 15 corners (5 process x 3 temp) | MUST PASS |
| Adjacent channel isolation | >10 dB between overlapping channels | SHOULD PASS |
| Total filter bank power | <250 uW | SHOULD PASS |

### 6.3 CRITICAL REQUIREMENT

**The agent MUST PROVE that the 4-bit tuning DAC can compensate +/-30-50% PVT-induced
frequency shift across ALL corners.** This means:

1. Simulate each channel at all 15 PVT conditions (5 corners x 3 temps)
2. At each condition, record f0 at DAC code = 8 (nominal)
3. Record the f0 shift from nominal as a percentage
4. Sweep DAC codes to find the code that restores f0 to within +/-10% of nominal
5. **If any corner cannot be compensated, FAIL and REDESIGN**

Specifically, the worst case is typically SS corner at -40C (slow transistors, low gm,
shifted f0 downward) and FF corner at 85C (opposite shift). The DAC must have enough
range to cover both extremes.

If the current 4-bit DAC (15:1 range) is insufficient, options include:
- Increase to 5-bit DAC (31:1 range)
- Add coarse/fine tuning (3-bit coarse × 3-bit fine)
- Reduce nominal code to 4 instead of 8 (gives more headroom upward)

---

## 7. Detailed Schematic Description

### 7.1 Single Tow-Thomas Channel

```
                    Ibias_ch (from DAC)
                         │
         ┌───────────────┼───────────────────────────────────┐
         │               │                                    │
         │   ┌───────────┼──────────┐     ┌────────────────┐ │
         │   │  OTA1     │          │     │  OTA2          │ │
    Vin ─┴──►│ gm1       ├──►(+)C1 │────►│ gm2     ──►C2 │─┴─► Vout_BP
              │ vip  vout │   10pF  │     │ vip  vout 10pF │
              │ vim ◄─────┤         │     │ vim ◄──────────┤
              └───────────┘    │    │     └────────────────┘
                               │    │              │
                               │    └──────────────┼───────────┐
                               │                   │           │
                               │              ┌────┴──────┐   │
                               │              │  OTA3      │   │
                               │              │  gm3       │   │
                               │              │  vip  vout─┘   │
                               └──────────────┤  vim ◄─────────┘
                                              └───────────────┘
                                              (damping feedback)
```

### 7.2 Capacitor Implementation

All capacitors are 10 pF MIM (`sky130_fd_pr__cap_mim_m3_1`).

10 pF at ~1 fF/um^2 requires ~10,000 um^2 = 100 um x 100 um per cap.
Per channel: 2 caps x 10 pF = 20,000 um^2.
5 channels: 100,000 um^2 = 0.1 mm^2 just for filter caps.

### 7.3 OTA Requirements per Channel

Each OTA instance needs programmable gm. Since gm ~ Ibias, the DAC controls all 3 OTAs
in a channel simultaneously. For Q adjustment, OTA3's bias can be scaled separately via
a current mirror ratio.

| OTA | Function | gm relationship | Bias |
|-----|----------|----------------|------|
| OTA1 | Input integrator | gm1 = gm | Ibias from DAC |
| OTA2 | Second integrator | gm2 = gm | Ibias from DAC |
| OTA3 | Damping | gm3 = gm/Q | Ibias_scaled = Ibias × (1/Q) |

For Q scaling, OTA3's current mirror has a programmable ratio. For example:
- Ch1 (Q=0.75): OTA3 gets Ibias × (1/0.75) = 1.33 × Ibias → mirror ratio 4:3
- Ch4 (Q=1.41): OTA3 gets Ibias × (1/1.41) = 0.71 × Ibias → mirror ratio ~5:7

In practice, implement Q via mirror W/L ratios in the schematic (fixed per channel).

### 7.4 Common-Mode Biasing

All OTAs operate with Vcm = 0.9V (mid-rail). Each integrator output needs a DC bias
path. Options:
1. Pseudo-resistor (MOS in subthreshold) to Vcm — simple but noisy
2. CMFB (common-mode feedback) circuit — power-hungry but precise
3. Rely on OTA input offset to settle the integrator — risky

**Recommended:** Pseudo-resistor to Vcm at each integrator output. The added noise is
at low frequencies (1/f) and gets filtered by the BPF's own response. For Channel 1
(f0=224 Hz), verify that pseudo-resistor noise does not dominate the in-band noise.

---

## 8. Testbench Specifications

### 8.1 TB1: AC Sweep per Channel (`tb_bpf_ac_ch1-5.spice`)

**Purpose:** Verify center frequency, Q, peak gain, and stopband rejection.

**Setup per channel:**
```
Vdd = 1.8V
Vcm = 0.9V
Vin: AC source, 10 mVpk amplitude, swept 1 Hz to 100 kHz
DAC code = 8 (nominal)
Load: CL = 10 pF (standard interface load)
```

**Measurements per channel:**
- f0: frequency of peak response (expect within +/-5% of nominal)
- Q: measure -3 dB bandwidth, compute Q = f0/BW (expect within +/-20%)
- Peak gain at f0 in dB (expect within +/-1 dB of Q in dB for unity-gain topology)
- Stopband: gain at 0.1×f0 and 10×f0 (expect <-15 dB below peak)
- Phase at f0 (expect 0 degrees for BPF)

**PASS criteria per channel:**
```
|f0_measured - f0_nominal| / f0_nominal < 5%
|Q_measured - Q_nominal| / Q_nominal < 20%
|Gain_peak - Gain_expected| < 1 dB
Gain(0.1*f0) < Gain_peak - 15 dB
Gain(10*f0) < Gain_peak - 15 dB
```

Run each channel individually and also all 5 simultaneously (verify no interaction).

### 8.2 TB2: Multi-Tone Intermodulation (`tb_bpf_intermod.spice`)

**Purpose:** Verify that one channel's strong signal does not corrupt another channel's output.

**Setup:**
```
All 5 channels active simultaneously
Vin: sum of 5 tones at f0 of each channel, 100 mVpk each
  Vin = 100m×sin(2π×224t) + 100m×sin(2π×1000t) + 100m×sin(2π×3162t)
      + 100m×sin(2π×7071t) + 100m×sin(2π×14142t)
Simulation: Transient, 50 ms, step = 1 us
Post-process: FFT of each channel's output
```

**Measurements:**
- Each channel's output should show dominant tone at its own f0
- Intermodulation products from other channels should be >20 dB below the desired signal
- Specifically check for sum/difference frequencies (f1+f2, f1-f2) at each output

**PASS criteria:** Intermodulation products >20 dB below desired signal at each output

### 8.3 TB3: THD Measurement (`tb_bpf_thd.spice`)

**Purpose:** Verify linearity at operational signal levels.

**Setup per channel:**
```
Vin: single tone at channel's f0, 200 mVpp
Simulation: Transient, duration = 20/f0 (20 cycles), step = 1/(100×f0)
Post-process: FFT, measure HD2, HD3, THD
```

**Measurements:**
- HD2, HD3, HD4, HD5 levels relative to fundamental
- THD = sqrt(HD2^2 + HD3^2 + HD4^2 + HD5^2)

**PASS criteria:** THD < -30 dBc at 200 mVpp input for all channels

**Expected THD behavior:**
- THD dominated by OTA transconductance nonlinearity (gm varies with Vdiff)
- Worse at higher input amplitudes
- Worse at higher frequencies (OTA closer to GBW limit)
- If THD fails, reduce input swing or increase OTA bias (more headroom)

### 8.4 TB4: Tuning Range Verification (`tb_bpf_tuning.spice`)

**Purpose:** PROVE that the 4-bit DAC can compensate PVT variation.

**This is the CRITICAL testbench.** Failure here requires redesign.

**Setup:**
```
For each of the 15 PVT conditions (5 corners × 3 temps):
  For each channel:
    For DAC codes 1 through 15:
      Run AC sweep, measure f0
```

Total simulations: 15 × 5 × 15 = 1125 AC sweeps. This can be scripted:

```spice
* Parametric sweep template
.param dac_code=8
.param ibias_unit=25n  ; for channel 2
.param ibias='ibias_unit * dac_code'

.control
  let codes = vector(15)
  ; ... loop over codes, corners, temperatures
  ; Record f0 at each condition
.endc
```

**Measurements per channel per PVT condition:**
- f0 at nominal code (code=8): record shift from nominal
- f0 at all codes (1-15): record full tuning curve
- Find code that brings f0 closest to nominal
- Record residual error after tuning

**PASS criteria:**
```
For EVERY channel AND EVERY PVT condition:
  EXISTS a DAC code such that |f0_tuned - f0_nominal| / f0_nominal < 10%
```

**If ANY condition fails:** Report the worst-case corner, the f0 shift, the best
achievable tuning, and the residual error. Then redesign:
- Increase DAC bits (5-bit or 6-bit)
- Adjust Iunit scaling
- Change nominal code point
- As a last resort, change capacitor values per channel

### 8.5 TB5: Corner and Temperature Sweep (`tb_bpf_corners.spice`)

**Purpose:** Full characterization across PVT without tuning (DAC at nominal code=8).

**Setup:**
```
5 process corners × 3 temperatures = 15 conditions
Per condition: AC sweep each channel, measure f0, Q, gain, stopband
```

This testbench documents the untuned variation. It pairs with TB4 which demonstrates
that tuning can correct it.

**Measurements:**
- f0 variation range per channel (max deviation from nominal)
- Q variation range
- Gain variation range
- Worst-case channel (expected: Channel 5 at highest frequency)

**Expected results:**
- f0 varies +/-25-40% untuned (dominated by gm variation)
- Q varies +/-15-25% (ratio of gm's — partially cancels)
- Gain varies +/-10-15% (same reason as Q)

### 8.6 TB6: Noise Analysis (`tb_bpf_noise.spice`)

**Purpose:** Verify that in-band integrated noise is below 1 mVrms per channel.

**Setup per channel:**
```
Noise analysis: 1 Hz to 100 kHz
Measure output noise spectral density
Integrate noise over passband (f_low to f_high of each channel)
Compute input-referred noise = output_noise / channel_gain
```

**Measurements:**
- Output noise spectral density at f0 (V/rtHz)
- Integrated output noise over passband (Vrms)
- Input-referred integrated noise (Vrms)
- Noise figure (if applicable)

**PASS criteria:** Integrated in-band output noise < 1 mVrms per channel

**Noise contributors (ranked by expected dominance):**
1. OTA transconductor noise (thermal: 4kT×gamma/gm)
2. OTA 1/f noise (dominant at low frequencies, affects Ch1 most)
3. Pseudo-resistor noise (1/f dominant, filtered by BPF shape)
4. Capacitor thermal noise (kT/C — negligible at 10 pF)

For Channel 1 (f0=224 Hz), the OTA 1/f noise corner is typically at 10-100 kHz, meaning
the entire passband (100-500 Hz) is in the 1/f regime. This is the worst-case channel
for noise. If it fails:
- Increase OTA size (larger W×L reduces 1/f)
- Accept higher power
- Use chopping (adds complexity)

---

## 9. OTA Instantiation Details

### 9.1 OTA Count

| Channel | OTA1 | OTA2 | OTA3 | Total |
|---------|------|------|------|-------|
| 1 | 1 | 1 | 1 | 3 |
| 2 | 1 | 1 | 1 | 3 |
| 3 | 1 | 1 | 1 | 3 |
| 4 | 1 | 1 | 1 | 3 |
| 5 | 1 | 1 | 1 | 3 |
| **Total** | | | | **15** |

15 OTAs is significant. Each is the same folded-cascode topology from Block 01 but
biased at a different current. The layout should tile OTA instances efficiently.

### 9.2 OTA Bias Current Distribution

Each channel needs 3 OTAs. The total supply current per channel is approximately:

| Channel | Ibias/OTA | 3 OTAs | OTA overhead (6x) | Total supply |
|---------|-----------|--------|-------------------|-------------|
| 1 | 50 nA | 150 nA | 900 nA | ~1.6 uA |
| 2 | 200 nA | 600 nA | 3.6 uA | ~6.5 uA |
| 3 | 500 nA | 1.5 uA | 9 uA | ~16 uA |
| 4 | 1.2 uA | 3.6 uA | 21.6 uA | ~39 uA |
| 5 | 2.5 uA | 7.5 uA | 45 uA | ~81 uA |

Total filter bank supply current: ~144 uA → ~260 uW at 1.8V.

This is within the 250 uW target (close — may need optimization).

### 9.3 Behavioral OTA for Filter Development

The behavioral OTA from the README needs modification for filter use because each
channel requires a different gm. Use a parameterized model:

```spice
* Parameterized behavioral OTA for Gm-C filter development
.subckt ota_gmc vip vim vout vdd vss
+ params: gm_val=63n rout_val=400Meg cout_val=50f
G1 vout vss cur='gm_val * (v(vip) - v(vim))'
Rout vout vss {rout_val}
Cout vout vss {cout_val}
.ends
```

Instantiate with per-channel gm:
```spice
Xota1_ch2 vip vim vout vdd vss ota_gmc gm_val=63n
```

---

## 10. Layout Considerations

### 10.1 Area Estimate

| Component | Area per unit | Count | Total |
|-----------|-------------|-------|-------|
| 10 pF MIM cap | 10,000 um^2 | 10 | 100,000 um^2 |
| OTA (folded-cascode) | ~2,000 um^2 | 15 | 30,000 um^2 |
| DAC (per channel) | ~1,000 um^2 | 5 | 5,000 um^2 |
| Routing, guards | | | ~50,000 um^2 |
| **Total** | | | **~185,000 um^2 = 0.185 mm^2** |

### 10.2 Matching Strategy

For accurate Q (which depends on gm1/gm3 ratio), the OTAs within a channel should be:
- Laid out in close proximity (same well, same orientation)
- Interdigitated if possible (OTA1 and OTA3 share common-centroid pattern)
- Surrounded by dummy structures

For accurate f0 (which depends on gm/C ratio), the 10 pF capacitors should be:
- Matched between C1 and C2 within a channel
- Less critical across channels (each channel is independently tuned)

---

## 11. Known Risks and Mitigations

### Risk 1: gm/C Frequency Shift Across PVT
**Likelihood:** Certain. This WILL happen.
**Impact:** f0 shifts +/-30-50% without tuning.
**Mitigation:** 4-bit tuning DAC provides +87.5% / -87.5% range. MUST be verified in TB4.

### Risk 2: Q Variation
**Likelihood:** High. Q = gm/gm3, and while the ratio tracks better than absolute gm,
mismatch between OTA instances causes Q error.
**Impact:** Passband shape distortion. Q too low = too broad, Q too high = too narrow
(and possible instability if Q >> designed value).
**Mitigation:** +/-20% Q tolerance is already specified. For Q > 2, the filter approaches
instability. Our maximum Q is 1.41 (channels 4-5) — safe margin.

### Risk 3: Channel 1 Noise (1/f Dominance)
**Likelihood:** High. At f0 = 224 Hz, OTA 1/f noise dominates.
**Impact:** In-band noise may exceed 1 mVrms.
**Mitigation:** Use large OTA transistors (W×L product) to reduce 1/f noise coefficient.
May need dedicated large-area OTAs for Channel 1 only.

### Risk 4: OTA Output Swing Limits THD at High Frequencies
**Likelihood:** Medium. At Channel 5 (Ibias = 2.5 uA), the OTA's output swing may be
limited by headroom in the folded-cascode structure.
**Impact:** THD > -30 dBc at 200 mVpp.
**Mitigation:** Reduce input swing for high-frequency channels (the envelope detector
downstream can handle smaller inputs). Alternatively, switch to a simple 5-transistor
OTA for Channel 5 (more swing, less gain, but gain is less critical at high gm).

### Risk 5: DAC INL/DNL Affects Tuning Accuracy
**Likelihood:** Medium. Current mirror mismatch in the DAC causes non-monotonic steps.
**Impact:** Cannot achieve fine tuning; some f0 values are unreachable.
**Mitigation:** Use unit-cell design with proper layout matching. At 4 bits (16 levels),
matching requirements are modest. DNL < 0.5 LSB is achievable with L=4u mirrors.

### Risk 6: Parasitic Capacitance Shifts f0
**Likelihood:** Certain. Routing and OTA parasitic caps add to the 10 pF integrating caps.
**Impact:** f0 shifts downward (more capacitance = lower frequency).
**Mitigation:** Account for ~0.5-1 pF parasitic per node. For 10 pF nominal, this is
5-10% shift — within the tuning DAC's correction range. After PEX, re-tune DAC codes.

---

## 12. Deliverable Sequence

| Step | Action | Depends On | Est. Time |
|------|--------|------------|-----------|
| 1 | Design behavioral OTA with parameterized gm | Nothing | 1 hour |
| 2 | Create bpf_ch2.sch (start with middle channel) | Step 1 | 3 hours |
| 3 | Write TB1 and TB3 for Channel 2 | Step 2 | 2 hours |
| 4 | Simulate Channel 2, verify f0/Q/THD | Step 3 | 2 hours |
| 5 | Debug and iterate Channel 2 | Step 4 | 2-4 hours |
| 6 | Copy and adapt for all 5 channels | Step 5 | 4 hours |
| 7 | Design 4-bit bias DAC | Step 1 | 2 hours |
| 8 | Write TB4 (tuning range) | Step 7 | 2 hours |
| 9 | Run full PVT tuning verification | Step 6, 8 | 4 hours |
| 10 | PROVE tuning covers all corners (CRITICAL) | Step 9 | 2 hours |
| 11 | Write TB2 (intermod), TB5 (corners), TB6 (noise) | Step 6 | 3 hours |
| 12 | Run all testbenches, record results | Step 11 | 4 hours |
| 13 | Swap behavioral OTA for real OTA | Block 01 done | 2 hours |
| 14 | Re-run all testbenches with real OTA | Step 13 | 4 hours |
| 15 | Layout all 5 channels + DAC | Step 12 | 8-12 hours |
| 16 | PEX and post-layout verification | Step 15 | 4 hours |
| 17 | Update results.md with final data | Step 16 | 1 hour |

---

## 13. Simulation Commands Reference

```bash
# AC sweep for Channel 2
ngspice -b tb_bpf_ac_ch2.spice -o ac_ch2.log

# THD for all channels (loop)
for ch in 1 2 3 4 5; do
    ngspice -b -D CHANNEL=$ch tb_bpf_thd.spice -o thd_ch${ch}.log
done

# CRITICAL: Full PVT tuning sweep
for corner in tt ff ss fs sf; do
    for temp in -40 27 85; do
        for code in $(seq 1 15); do
            ngspice -b -D CORNER=$corner -D TEMP=$temp -D DAC_CODE=$code \
                tb_bpf_tuning.spice -o tuning_${corner}_${temp}_${code}.log
        done
    done
done

# Post-process tuning results
python3 scripts/analyze_tuning.py tuning_*.log

# Plot all 5 filter responses on one graph
python3 scripts/plot_filterbank.py
```

---

## 14. Results Template

### Per-Channel Results (TT, 27C, DAC code=8)

| Parameter | Spec | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | PASS/FAIL |
|-----------|------|-----|-----|-----|-----|-----|-----------|
| f0 (Hz) | +/-5% | | | | | | |
| Q | +/-20% | | | | | | |
| Peak gain (dB) | +/-1 | | | | | | |
| Stopband 0.1×f0 (dB) | <-15 | | | | | | |
| Stopband 10×f0 (dB) | <-15 | | | | | | |
| Noise (mVrms) | <1 | | | | | | |
| THD (dBc) | <-30 | | | | | | |
| Power (uW) | budget | | | | | | |

### Tuning Verification (CRITICAL)

| Channel | Worst-case corner | f0 shift (untuned) | Best DAC code | f0 after tuning | Residual error | PASS/FAIL |
|---------|-------------------|-------------------|---------------|-----------------|----------------|-----------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

### Total Filter Bank Power

| Condition | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | Total | PASS (<250uW) |
|-----------|-----|-----|-----|-----|-----|-------|---------------|
| TT 27C | | | | | | | |
| FF 85C (max) | | | | | | | |
| SS -40C (min) | | | | | | | |
