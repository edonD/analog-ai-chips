# Block 04: Precision Rectifier + LPF Envelope Detector (5 Channels)

## Design Program — Complete Specification and Verification Plan

---

## 1. Context and Motivation

Each of the 5 band-pass filters (Block 03) outputs an AC signal at the band's center
frequency, with amplitude proportional to the vibration energy in that band. The
downstream charge-domain MAC classifier requires DC voltages. The envelope detector
bridges this gap: it extracts the amplitude envelope of each BPF output, producing a
slowly-varying DC signal (~10 Hz bandwidth) that represents the RMS energy in the band.

This is analogous to computing |FFT bin magnitude| in a digital system — but done in
continuous time at microwatt power.

### Why Not Just Use a Diode Rectifier?

A simple diode rectifier (pn junction or MOS diode) has a threshold voltage of 0.3-0.7V.
The BPF outputs can be as small as 5-10 mVpp (healthy machine, low vibration). A diode
rectifier would produce zero output for any signal below ~300 mVpp — completely useless
for our application.

An OTA-based precision rectifier has no threshold voltage. It can rectify signals down to
millivolts because the OTA's gain forces the virtual ground to track the input. The
minimum detectable signal is limited only by the OTA's input offset voltage (typically
1-5 mV in SKY130) and noise.

---

## 2. State of the Art Comparison

| Parameter | Wouters JSSC'20 | Sarpeshkar RMS | Harrison TBCAS'07 | **This Work** |
|-----------|-----------------|----------------|-------------------|---------------|
| Application | Neural spike env. | General RMS | Biopotential | Vibration |
| Topology | Log-domain rect. | Translinear RMS | OTA rect + LPF | OTA rect + Gm-C LPF |
| Min detectable | 50 uVpp | 1 mVpp | 100 uVpp | 5 mVpp |
| Bandwidth (input) | 300 Hz-10 kHz | DC-1 MHz | 100 Hz-5 kHz | 100 Hz-20 kHz |
| LPF cutoff | 50 Hz | N/A | 100 Hz | 5-20 Hz |
| Power/channel | 0.5 uW | 50 uW | 7.8 uW | <10 uW |
| Supply | 0.8V | 3.3V | 2.8V | 1.8V |
| Process | 28nm CMOS | Discrete | 1.5um CMOS | SKY130 130nm |
| Rectification error | +/-3% at 1mVpp | +/-1% (RMS) | +/-5% at 100uVpp | +/-5% at 100mVpp |

### Analysis of Prior Art

**Wouters et al. (JSSC 2020):** State-of-the-art neural spike envelope detector at 0.5 uW
using log-domain processing in 28nm. The log-domain approach provides wide dynamic range
but requires matched transistors operating in weak inversion. In SKY130 (130nm), the
transistor matching is worse and the minimum feature size is larger, making it harder to
achieve the same efficiency.

**Sarpeshkar RMS Detector:** Classic translinear circuit for true RMS detection. Requires
bipolar transistors or BJTs for accurate translinear operation. SKY130 has parasitic
vertical PNP but no high-quality NPN. Not directly applicable, but the concept of using
transistor I-V characteristics for rectification is relevant.

**Harrison (TBCAS 2007):** The closest prior art for our application. Uses an OTA-based
precision rectifier feeding a Gm-C low-pass filter. 7.8 uW per channel at 2.8V supply.
Scaling to 1.8V and 130nm, we expect 3-5 uW — within our 10 uW budget with margin.

**Our position:** We target <10 uW per channel (conservative) using the OTA-based
precision rectifier from Harrison's approach, adapted for SKY130. This is 20x more power
than Wouters but uses a simpler, more robust topology that works reliably in 130nm.

---

## 3. Topology: OTA-Based Precision Rectifier + Gm-C LPF

### 3.1 Architecture Overview

```
                        Envelope Detector (One Channel)
    ┌────────────────────────────────────────────────────────────┐
    │                                                            │
    │   ┌──────────────────────┐    ┌──────────────────────┐    │
    │   │  PRECISION RECTIFIER │    │     Gm-C LPF         │    │
    │   │                      │    │     fc = 10 Hz        │    │
    │   │   OTA1 (half-wave)   │    │                      │    │
    │   │   + current mirror   ├───►│  OTA3 ──► C_lpf     ├───►│ Vout (DC)
    │   │   + OTA2 (full-wave) │    │  (integrator)        │    │
    │   │                      │    │                      │    │
    │   └──────────────────────┘    └──────────────────────┘    │
    │                                                            │
    └────────────────────────────────────────────────────────────┘
          AC input (from BPF)                         DC output (~10 Hz BW)
          10-200 mVpp                                 0.1-1.5V
          100-20000 Hz
```

### 3.2 Precision Rectifier — Detailed Circuit

The precision rectifier uses two OTAs and a current mirror to produce a full-wave
rectified output:

```
    Half-Wave Rectifier (positive half):

                              ┌──── Iout+ (positive half-wave current)
                              │
    Vin ──►(+) OTA1 (-) ◄── Vfb
                    │
                    └── Vfb is clamped to Vcm by the diode-connected load
                        during negative half-cycles (OTA output saturates low)

    Full-Wave Operation:

    Vin ──►(+) OTA1 (-)──┬──► M1 (PMOS diode) ──► Iout+
                          │
                          └──► M2 (PMOS mirror) ──► Iout- (inverted copy)

    Iout_rectified = |Iout+| + |Iout-| = |gm × Vin| (full-wave rectified current)
```

More precisely, the full-wave precision rectifier operates as follows:

**Positive half-cycle (Vin > Vcm):**
- OTA1 output current is positive (sources current)
- Current flows through PMOS diode M1
- PMOS mirror M2 copies the current

**Negative half-cycle (Vin < Vcm):**
- OTA1 output current is negative (sinks current)
- Current flows through NMOS diode M3 (second diode pair)
- NMOS mirror M4 copies the current with inverted sign

**Result:** The output current is always positive and proportional to |Vin - Vcm|.

### 3.3 Alternative: Dual-OTA Full-Wave Rectifier

A cleaner implementation uses two OTAs:

```
                    ┌─────────┐
    Vin ──────────►│  OTA1   │──► I1 = gm × (Vin - Vcm)
    Vcm ──────────►│  (-)    │
                    └─────────┘

                    ┌─────────┐
    Vcm ──────────►│  OTA2   │──► I2 = gm × (Vcm - Vin) = -I1
    Vin ──────────►│  (-)    │
                    └─────────┘

    I_rect = max(I1, 0) + max(I2, 0) = max(I1, -I1) = |I1| = gm × |Vin - Vcm|
```

OTA1 and OTA2 have swapped inputs. Each OTA naturally clips at zero current when its
input goes negative (subthreshold OTA output current cannot reverse beyond the bias
current). The two half-wave currents sum to produce a full-wave rectified signal.

**This is the recommended topology.** It uses 2 OTAs per channel and relies on the
natural current-limiting behavior of the OTA (output current saturates at +/-Ibias).

### 3.4 Current-to-Voltage Conversion

The rectified current must be converted to a voltage for the LPF. Options:

1. **Resistive load:** I_rect flows through a resistor R → V = I_rect × R.
   Problem: R must be large (1-10 MOhm) for small currents, consuming area.

2. **Diode-connected MOS load:** V = Vgs of diode. Provides logarithmic I-to-V conversion.
   Advantage: compresses dynamic range.

3. **Direct integration by LPF:** Feed I_rect directly into the Gm-C LPF's capacitor.
   The LPF integrates the current, producing a voltage proportional to the average.

**Recommended:** Option 3 — direct current integration into the LPF. This eliminates
one conversion stage and reduces noise.

### 3.5 Gm-C Low-Pass Filter (fc = 10 Hz)

The LPF smooths the rectified signal, extracting the envelope. The cutoff frequency must
be well below the lowest filter band's center frequency (224 Hz for Channel 1) to avoid
passing the carrier through:

```
    fc_lpf = 10 Hz << f0_min = 224 Hz
```

This gives >23 dB of carrier rejection at 224 Hz (first-order rolloff) and >46 dB at
1 kHz.

**Implementation:**

```
                    ┌─────────┐
    I_rect ────────►│  OTA3   │──┬──► Vout (envelope)
                    │  gm3    │  │
    Vout ─────────►│  (-)    │  C_lpf
                    └─────────┘  │
                                GND
```

This is a first-order Gm-C LPF (lossy integrator):

```
    fc = gm3 / (2 × pi × C_lpf)
```

For fc = 10 Hz with C_lpf = 50 pF:
```
    gm3 = 2 × pi × 10 × 50e-12 = 3.14 nS
```

This requires an OTA with gm = 3.14 nS, which corresponds to Ibias ~ 100 nA in
subthreshold. Very low power.

**Large capacitor concern:** 50 pF is feasible in SKY130 MIM (~50,000 um^2 = 224 um x
224 um). For a more area-efficient design, use C_lpf = 10 pF with gm3 = 0.63 nS
(Ibias ~ 20 nA). The trade-off is that lower gm means more noise and more susceptibility
to leakage currents.

**Recommended:** C_lpf = 50 pF, gm3 = 3.14 nS. The area cost is acceptable given the
5-channel total, and the higher gm gives better noise performance.

### 3.6 Second-Order LPF Option

If first-order rolloff (-20 dB/decade) provides insufficient carrier rejection for
Channel 1 (fc_carrier = 224 Hz, only 27 dB rejection), add a second OTA-C stage:

```
    I_rect → OTA3/C3 (1st order, fc=10Hz) → OTA4/C4 (2nd order, fc=10Hz) → Vout
```

Second-order gives -40 dB/decade: 64 dB rejection at 224 Hz. This adds one OTA per
channel (5 total) and 50 pF of capacitance (250,000 um^2 = 0.25 mm^2).

**Decision: Start with first-order LPF. Upgrade to second-order only if ripple
measurement (TB4) fails the <5% specification for Channel 1.**

---

## 4. PASS/FAIL Criteria

### 4.1 Rectification Accuracy

| Parameter | Specification | Condition | PASS/FAIL |
|-----------|--------------|-----------|-----------|
| Rectification accuracy | +/-5% | Vin = 100 mVpp, f = f0_ch | MUST PASS |
| Rectification accuracy | +/-15% | Vin = 10 mVpp, f = f0_ch | MUST PASS |
| Minimum detectable signal | 5 mVpp | Output distinguishable from noise floor | MUST PASS |

### 4.2 LPF Performance

| Parameter | Specification | Condition | PASS/FAIL |
|-----------|--------------|-----------|-----------|
| LPF cutoff frequency | 5-20 Hz | TT corner, 27C | MUST PASS |
| Output ripple | <5% of DC value | At 100 mVpp input, any carrier freq | MUST PASS |
| Settling time | <200 ms | To 90% of final value after step input | MUST PASS |

### 4.3 System Specs

| Parameter | Specification | Condition | PASS/FAIL |
|-----------|--------------|-----------|-----------|
| Power per channel | <10 uW | At 1.8V, TT 27C | MUST PASS |
| Total power (5 channels) | <50 uW | At 1.8V, TT 27C | SHOULD PASS |
| Output DC range | 0.1-1.5V | For 5 mV-500 mV input range | SHOULD PASS |
| Output impedance | <100 kOhm | At DC (for classifier sampling) | SHOULD PASS |

### 4.4 Derived Specifications

**Dynamic range:**
- Maximum input: 500 mVpp (from PGA at 1x gain with 2g vibration)
- Minimum input: 5 mVpp (barely detectable signal in any band)
- Required dynamic range: 500/5 = 100 = 40 dB

**Rectification accuracy at minimum input (5 mVpp):**
At 5 mVpp, the OTA input differential is +/-2.5 mV. The OTA's input offset voltage
(typically 1-5 mV in SKY130) is comparable to the signal. This is the fundamental limit.

If the offset is 3 mV, the positive half-cycle sees (2.5+3) = 5.5 mV and the negative
half-cycle sees (2.5-3) = -0.5 mV (barely negative). The rectified output is dominated
by one half — poor accuracy but still detectable above the noise floor.

**Mitigation for offset:** Use input-offset cancellation or auto-zeroing. However, this
adds complexity. For the initial design, accept that accuracy at 5 mVpp will be poor
(+/-30-50%) but the signal is still detectable (nonzero output).

---

## 5. Detailed Design Procedure

### Step 1: Design the Dual-OTA Rectifier

**OTA1 and OTA2 specifications:**
- gm = 2.5 uS (same as standard OTA from Block 01)
- Ibias = 500 nA (from Block 00)
- Must handle input frequency range 100 Hz - 20 kHz
- Output current range: 0 to +/-Ibias (natural clipping)

**Subcircuit interface:**
```spice
.subckt precision_rect vin vcm iout_pos iout_neg vdd vss
* vin: AC input from BPF
* vcm: common-mode reference (0.9V)
* iout_pos: rectified current (positive)
* iout_neg: always 0 (or use for differential output)

Xota1 vin vcm n_rect1 vdd vss ota_foldcasc
Xota2 vcm vin n_rect2 vdd vss ota_foldcasc

* PMOS diode loads to convert current to single-ended
M1 n_rect1 n_rect1 vdd vdd sky130_fd_pr__pfet_01v8 W=2u L=1u
M2 iout_pos n_rect1 vdd vdd sky130_fd_pr__pfet_01v8 W=2u L=1u
M3 n_rect2 n_rect2 vdd vdd sky130_fd_pr__pfet_01v8 W=2u L=1u
M4 iout_pos n_rect2 vdd vdd sky130_fd_pr__pfet_01v8 W=2u L=1u

.ends
```

### Step 2: Design the Gm-C LPF

**OTA3 specifications:**
- gm = 3.14 nS
- Ibias = ~100 nA (subthreshold, gm/Ibias ~ 30 V^-1)
- C_lpf = 50 pF (MIM capacitor)
- fc = gm/(2*pi*C) = 3.14n/(2*pi*50p) = 10 Hz

**Subcircuit interface:**
```spice
.subckt gmc_lpf iin vout vcm vdd vss
* iin: input current (from rectifier)
* vout: filtered DC output

* Convert current to voltage via OTA feedback
Xota3 vcm vout n_int vdd vss ota_foldcasc
* Integration capacitor
C_lpf n_int vss 50p
* DC bias path
R_bias n_int vcm 100G  ; pseudo-resistor for DC bias

.ends
```

Actually, the LPF should be configured as a voltage-mode filter with the rectifier
output converted to a voltage first. Revised approach:

```
    V_rect (voltage-mode rectified signal) → OTA3(+) → C_lpf → Vout
                                              OTA3(-) ← Vout (feedback)
```

This forms a unity-gain LPF:
```
    H(s) = gm3 / (s × C_lpf + gm3) = 1 / (1 + s × C_lpf / gm3)
    fc = gm3 / (2*pi*C_lpf)
```

### Step 3: Combine Rectifier + LPF into Single Channel

**Full envelope detector subcircuit:**
```spice
.subckt envelope_det vin vcm vout vdd vss
* vin: AC input from band-pass filter
* vcm: common-mode voltage (0.9V)
* vout: DC envelope output

* Precision rectifier
Xrect vin vcm v_rect vdd vss precision_rect

* Gm-C low-pass filter
Xlpf v_rect vout vcm vdd vss gmc_lpf

.ends
```

### Step 4: Instantiate 5 Channels

```spice
* 5-channel envelope detector bank
Xenv1 vbpf1 vcm venv1 vdd vss envelope_det
Xenv2 vbpf2 vcm venv2 vdd vss envelope_det
Xenv3 vbpf3 vcm venv3 vdd vss envelope_det
Xenv4 vbpf4 vcm venv4 vdd vss envelope_det
Xenv5 vbpf5 vcm venv5 vdd vss envelope_det
```

All 5 channels are identical (same topology, same bias). The only difference is the
input frequency, which the circuit handles automatically (the LPF extracts the envelope
regardless of carrier frequency).

### Step 5: Simulate with Behavioral OTA, then Real OTA

First pass: use behavioral OTA model:
```spice
.subckt ota_behavioral vip vim vout vdd vss
G1 vout vss cur='2.5e-6 * (v(vip) - v(vim))'
Rout vout vss 400Meg
Cout vout vss 50f
.ends
```

Second pass: replace with real OTA from Block 01.

---

## 6. Testbench Specifications

### 6.1 TB1: Amplitude Sweep (`tb_env_amp_sweep.spice`)

**Purpose:** Characterize rectification accuracy across the full input amplitude range.

**Setup:**
```
Vdd = 1.8V
Vcm = 0.9V
Input: sine wave at f = 1 kHz (Channel 2 center frequency)
Amplitude sweep: 5 mVpp, 10 mVpp, 20 mVpp, 50 mVpp, 100 mVpp, 200 mVpp, 500 mVpp
Each amplitude: run transient for 500 ms (allow settling), measure final DC output
Load: CL = 10 pF
```

**For each amplitude, run separate simulations or use .STEP:**
```spice
.param amp_mv = 100
Vin vcm vin AC 0 SIN(0.9 {amp_mv*1e-3/2} 1k)

.step param amp_mv list 5 10 20 50 100 200 500
.tran 100u 500m
```

**Measurements per amplitude:**
- DC output voltage (average of last 100 ms)
- Expected DC output: Vout_dc = Vcm + (2/pi) × gm × R_load × (Vpk - Voffset)
  For ideal rectifier: Vout_dc proportional to input amplitude
- Rectification error = |Vout_measured - Vout_ideal| / Vout_ideal × 100%
- Output ripple (peak-to-peak variation in last 100 ms)

**PASS criteria:**
- Error < +/-5% at 100 mVpp
- Error < +/-15% at 10 mVpp
- Output at 5 mVpp is distinguishable from zero-input baseline (>3x noise floor)

**Also run at f = 224 Hz (Ch1), 3162 Hz (Ch3), 7071 Hz (Ch4), 14142 Hz (Ch5):**
The rectifier should work at all carrier frequencies. At higher frequencies, the LPF
provides better carrier rejection (more decades between carrier and fc_lpf = 10 Hz).
At 224 Hz (Channel 1), carrier rejection is only ~27 dB (first-order) — check if
ripple is acceptable.

### 6.2 TB2: AM Signal Tracking (`tb_env_am_track.spice`)

**Purpose:** Verify that the envelope detector correctly tracks a modulated signal —
this is the actual use case (vibration amplitude changes over time as machine
condition changes).

**Setup:**
```
Input: AM-modulated signal
  Vin(t) = Vcm + A(t) × sin(2*pi*1000*t)
  A(t) = 100mV × (0.5 + 0.5 × sin(2*pi*2*t))  ; 2 Hz modulation
  → Amplitude varies from 0 to 100 mVpk at 2 Hz rate

Simulation: Transient, 2 seconds (4 modulation cycles), step = 10 us
```

**Implementation in SPICE:**
```spice
* AM signal: carrier 1kHz, modulation 2Hz, depth 100%
* V(t) = Vcm + Vpk × (1 + m×sin(2π×fm×t)) × sin(2π×fc×t) / 2
B_am vin vss V = '0.9 + 0.05*(1 + sin(2*3.14159*2*time))*sin(2*3.14159*1000*time)'
```

**Measurements:**
- Overlay: input envelope (computed as |Vin - Vcm| after ideal rectification) vs
  detector output
- Amplitude tracking error: peak-to-peak of (Vout - Venvelope_ideal)
- Phase lag between input envelope and output (expect ~16 ms for 10 Hz LPF = fc)
- Frequency response of envelope tracking: should be flat to ~5 Hz, -3 dB at ~10 Hz

**PASS criteria:**
- Envelope tracking error < 10% of envelope amplitude
- Output clearly follows the 2 Hz modulation pattern
- No carrier feedthrough visible in output

### 6.3 TB3: Burst Detection (`tb_env_burst.spice`)

**Purpose:** Verify transient response to sudden vibration events — this simulates
a fault onset (machine starts vibrating suddenly in a new frequency band).

**Setup:**
```
Input: burst signal
  t = 0 to 200 ms: Vin = Vcm (silence, no vibration)
  t = 200 ms to 700 ms: Vin = Vcm + 100mVpk × sin(2*pi*1000*t) (fault appears)
  t = 700 ms to 1200 ms: Vin = Vcm (fault disappears)
  t = 1200 ms to 1500 ms: Vin = Vcm + 50mVpk × sin(2*pi*1000*t) (smaller fault)

Simulation: Transient, 1.5 seconds, step = 10 us
```

**Measurements:**
- Rise time (10% to 90% of final value) after burst onset at t = 200 ms
- Settling time to within 5% of final value
- Fall time (90% to 10%) after burst ends at t = 700 ms
- Output level during silence (should be near Vcm or baseline)
- Output level during 100 mVpk burst (should be proportional to amplitude)
- Output level during 50 mVpk burst (should be half of 100 mVpk burst level)

**PASS criteria:**
- Settling time < 200 ms (to 90% of final value)
- Rise time < 100 ms (10% to 90%)
- Ratio of 100mV burst output to 50mV burst output = 2.0 +/-20%
- Baseline output during silence < 10% of 100mV burst output

**Expected settling time analysis:**
For a first-order LPF with fc = 10 Hz:
- Time constant tau = 1/(2*pi*10) = 16 ms
- 90% settling = 2.3 × tau = 37 ms
- 99% settling = 4.6 × tau = 74 ms

These are well within the 200 ms specification. The concern is that the actual OTA-based
LPF may have additional poles (from OTA output impedance interacting with parasitic
capacitance) that slow the response.

### 6.4 TB4: Ripple Measurement (`tb_env_ripple.spice`)

**Purpose:** Verify that carrier-frequency ripple at the output is below 5% of the
DC envelope value. This is critical because the classifier samples the envelope output
and needs a clean DC value.

**Setup:**
```
Input: steady-state sine waves at each channel's center frequency
  Amplitude: 100 mVpp for all tests
  Frequencies: 224 Hz, 1000 Hz, 3162 Hz, 7071 Hz, 14142 Hz (one test per frequency)
  Simulation: transient, 500 ms (settle) + 200 ms (measure), step = 1 us
```

**Measurements per carrier frequency:**
- DC value: mean of Vout over measurement window
- Ripple: peak-to-peak of Vout over measurement window
- Ripple percentage: ripple_pp / DC_value × 100%
- Ripple frequency (should be 2× carrier frequency for full-wave rectifier)

**PASS criteria:** Ripple < 5% of DC value at ALL carrier frequencies

**Expected ripple analysis (first-order LPF, fc = 10 Hz):**
The ripple frequency is 2× carrier (full-wave rectifier). The LPF attenuation at the
ripple frequency is:

| Channel | Carrier | Ripple freq | Attenuation at ripple freq | Expected ripple |
|---------|---------|-------------|---------------------------|-----------------|
| 1 | 224 Hz | 448 Hz | -33 dB (0.022) | 2.2% |
| 2 | 1000 Hz | 2000 Hz | -46 dB (0.005) | 0.5% |
| 3 | 3162 Hz | 6324 Hz | -56 dB (0.0016) | 0.16% |
| 4 | 7071 Hz | 14142 Hz | -63 dB (0.0007) | 0.07% |
| 5 | 14142 Hz | 28284 Hz | -69 dB (0.00035) | 0.035% |

Channel 1 is the worst case at 2.2% — within the 5% spec. If the real circuit shows
higher ripple due to nonideal LPF behavior or OTA finite output impedance, consider:
- Increasing C_lpf for Channel 1 (100 pF instead of 50 pF → fc = 5 Hz)
- Adding second-order LPF section for Channel 1 only

### 6.5 TB5: Corner and Temperature Sweep (`tb_env_corners.spice`)

**Purpose:** Verify performance across PVT.

**Setup:**
```
5 process corners × 3 temperatures = 15 conditions
At each condition:
  - Input: 100 mVpp at 1 kHz
  - Measure: DC output level, ripple, settling time
  - Also: 10 mVpp at 1 kHz (sensitivity check)
```

**Measurements per condition:**
- DC output voltage at 100 mVpp input
- DC output voltage at 10 mVpp input
- Ripple at 100 mVpp
- Settling time at 100 mVpp
- LPF cutoff frequency (derived from settling time: fc = 1/(2*pi*tau))

**Expected PVT effects:**
- OTA gm variation → rectification gain changes → DC output level shifts
  This is acceptable as long as the relationship remains monotonic (larger input →
  larger output)
- LPF fc shifts with gm variation → ripple may increase (if fc goes up) or settling
  may slow (if fc goes down)
- OTA offset voltage varies with process → minimum detectable signal changes

**PASS criteria:**
- DC output within +/-30% of TT value across all corners (wide tolerance because
  the classifier can be recalibrated for absolute levels)
- Ripple < 5% at all corners
- Settling < 200 ms at all corners
- Monotonic input-output relationship maintained at all corners

---

## 7. OTA Usage and Count

### 7.1 OTA Count per Channel

| Component | OTAs | Function |
|-----------|------|----------|
| Rectifier (OTA1) | 1 | Positive half-wave |
| Rectifier (OTA2) | 1 | Negative half-wave (swapped inputs) |
| LPF (OTA3) | 1 | Gm-C integrator, fc = 10 Hz |
| **Total per channel** | **3** | |
| **Total (5 channels)** | **15** | |

If second-order LPF is needed for Channel 1: add 1 OTA → 16 total.

### 7.2 Bias Current Requirements

| Component | Ibias per OTA | OTAs | Total Ibias |
|-----------|-------------|------|-------------|
| Rectifier OTAs | 500 nA | 10 (2 per ch × 5 ch) | 5 uA |
| LPF OTAs | 100 nA | 5 | 500 nA |
| **Total** | | **15** | **5.5 uA** |

Supply current (6x Ibias estimate): ~33 uA → ~59 uW at 1.8V.

This exceeds the 50 uW target (5 channels × 10 uW). Options to reduce:
1. Reduce rectifier OTA bias to 250 nA (halves power but reduces linearity)
2. Share LPF OTAs across channels (time-multiplex — adds complexity)
3. Accept 12 uW per channel (total 60 uW) — within the system's 25 uW envelope
   budget from the README

**Recommended:** Start with 500 nA per rectifier OTA and optimize later if needed.
The system-level budget (25 uW for all 5 envelope detectors, from README) may require
reducing to 250 nA.

### 7.3 Behavioral vs Real OTA Impact

The precision rectifier is sensitive to OTA characteristics:
- **Input offset:** Directly limits minimum detectable signal. Behavioral model has
  zero offset; real OTA will have 1-5 mV offset.
- **Finite gain:** Real OTA has finite gain (~60 dB). At the zero-crossing of the
  input signal, the rectifier has a "dead zone" of approximately Vpk/A_OL. At 60 dB
  gain and 100 mVpk input: dead zone ~ 0.1 mV — negligible. At 5 mVpk: dead zone ~
  5 uV — still negligible.
- **Slew rate:** At 14142 Hz (Channel 5), the OTA must slew fast enough to track
  the rectified waveform. Required slew rate: 2*pi*f*Vpk = 2*pi*14142*0.1 = 8.9 V/ms.
  OTA slew rate = Ibias/CL = 500n/10p = 50 V/ms — adequate.

**MUST verify:** After swapping behavioral → real OTA, re-run TB1 (amplitude sweep)
and compare. Flag any degradation >10% in rectification accuracy.

---

## 8. Power Budget

### 8.1 Per-Channel Breakdown

| Component | Current (supply) | Power at 1.8V |
|-----------|-----------------|---------------|
| OTA1 (rectifier +) | 3 uA | 5.4 uW |
| OTA2 (rectifier -) | 3 uA | 5.4 uW |
| OTA3 (LPF) | 600 nA | 1.1 uW |
| Bias circuits | 200 nA | 0.4 uW |
| **Total per channel** | **~6.8 uA** | **~12.3 uW** |

### 8.2 Five-Channel Total

| | Current | Power |
|---|---------|-------|
| 5 channels | 34 uA | 61.2 uW |
| Shared bias/reference | 2 uA | 3.6 uW |
| **Total** | **36 uA** | **~65 uW** |

**Above the 50 uW target.** To meet 50 uW:
- Reduce rectifier OTA bias from 500 nA to 300 nA → total ~ 40 uW
- Trade-off: reduced linearity at large input amplitudes and slower slew rate

### 8.3 Power Optimization Strategies

1. **Scale rectifier bias per channel:** Higher-frequency channels (4, 5) need more
   bias for slew rate. Lower-frequency channels (1, 2) can use less.

| Channel | f_carrier | Min slew rate | Min Ibias | Proposed Ibias |
|---------|-----------|---------------|-----------|----------------|
| 1 | 224 Hz | 0.14 V/ms | 3 nA | 200 nA |
| 2 | 1000 Hz | 0.63 V/ms | 13 nA | 200 nA |
| 3 | 3162 Hz | 2.0 V/ms | 40 nA | 300 nA |
| 4 | 7071 Hz | 4.4 V/ms | 88 nA | 500 nA |
| 5 | 14142 Hz | 8.9 V/ms | 178 nA | 500 nA |

With optimized per-channel biasing:
Total rectifier Ibias: 2 × (200+200+300+500+500) nA = 3.4 uA
Total supply current: ~20 uA → ~36 uW at 1.8V
Add LPF (5 × 600 nA = 3 uA → 6 uA supply → 10.8 uW)
**Optimized total: ~47 uW** — within budget.

2. **Time-multiplexed LPF:** Share one LPF OTA across all 5 channels using sample-and-hold.
   Saves 4 OTAs but adds switches and timing complexity. Not recommended for initial design.

---

## 9. Layout Considerations

### 9.1 Area Estimate

| Component | Area per unit | Count | Total |
|-----------|-------------|-------|-------|
| OTA (rectifier) | 2,000 um^2 | 10 | 20,000 um^2 |
| OTA (LPF) | 2,000 um^2 | 5 | 10,000 um^2 |
| 50 pF MIM cap | 50,000 um^2 | 5 | 250,000 um^2 |
| Current mirrors/bias | 500 um^2 | 10 | 5,000 um^2 |
| Routing, guards | | | ~30,000 um^2 |
| **Total** | | | **~315,000 um^2 = 0.315 mm^2** |

The 50 pF LPF capacitors dominate the area. If area is critical, reduce to C_lpf = 20 pF
(fc = 25 Hz) and accept higher ripple, or use a second-order LPF with two 10 pF caps
(same fc, 80% less area).

### 9.2 Matching Requirements

The two rectifier OTAs (OTA1, OTA2) within a channel must match well for accurate
full-wave rectification. Mismatched gm causes asymmetric half-wave rectification
(different amplitude for positive vs negative half-cycles), introducing a DC error
proportional to the mismatch.

**Matching target:** gm mismatch < 2% → rectification error < 1% (contribution to
total error budget).

**Layout technique:** Place OTA1 and OTA2 in common-centroid arrangement. Use
interdigitated input pair transistors. Surround with dummy structures.

---

## 10. Integration with Upstream and Downstream Blocks

### 10.1 Input Interface (from Block 03 Filters)

| Parameter | Value |
|-----------|-------|
| Signal type | AC, narrow-band |
| Amplitude range | 5-200 mVpp |
| DC bias | Vcm = 0.9V |
| Source impedance | ~1/(gm_filter) ≈ 1-100 kOhm |
| Frequency | Band-dependent (224 Hz to 14.1 kHz) |

The envelope detector input impedance is capacitive (OTA gate input) — essentially
infinite at DC, ~10 pF at AC. No loading concerns.

### 10.2 Output Interface (to Block 06 Classifier)

| Parameter | Value |
|-----------|-------|
| Signal type | DC (slowly varying, ~10 Hz BW) |
| Voltage range | 0.1-1.5V |
| Source impedance | ~1/gm_lpf ≈ 300 MOhm (but with 50 pF cap → low Z at any freq > DC) |
| Load | Classifier sampling capacitor (~1 pF, sampled every 100 ms) |
| Settling after sampling | <1 ms (LPF replenishes charge) |

The classifier samples each envelope output for ~100 ns every 100 ms. The charge removed
per sample: Q = C_sample × Vout = 1p × 1V = 1 pC. This causes a voltage droop on the
50 pF LPF cap: dV = Q/C_lpf = 1p/50p = 20 mV. The LPF OTA restores this in:
t_recover = C_lpf × dV / (gm × Vin) ≈ 50p × 20m / (3n × 100m) ≈ 3.3 ms.
Well within the 100 ms sampling period.

### 10.3 Behavioral vs Real OTA Comparison Matrix

| Parameter | Behavioral | Real OTA | Delta | Flag if >10% |
|-----------|-----------|----------|-------|-------------|
| DC output at 100mVpp | | | | |
| DC output at 10mVpp | | | | |
| DC output at 5mVpp | | | | |
| Ripple at Ch1 freq | | | | |
| Ripple at Ch5 freq | | | | |
| Settling time | | | | |
| Power per channel | | | | |
| Min detectable signal | | | | |

---

## 11. Known Risks and Mitigations

### Risk 1: OTA Input Offset Limits Minimum Detectable Signal
**Likelihood:** Certain. SKY130 OTA offset is 1-5 mV without trimming.
**Impact:** At 5 mVpp input (2.5 mVpk), a 3 mV offset makes one half-cycle ~5.5 mV
and the other ~-0.5 mV. Rectification is asymmetric; accuracy degrades to ~50%.
**Mitigation:** Accept degraded accuracy at 5 mVpp (still detectable above noise).
For better performance, add auto-zeroing (chopper): store offset on a capacitor during
a calibration phase, subtract during operation. This adds one switch and one cap per
channel.

### Risk 2: Dead Zone at Input Zero-Crossing
**Likelihood:** Medium. When Vin crosses Vcm, both OTAs have near-zero differential
input, and their output currents approach zero. The transition between positive and
negative half-cycles is not instantaneous.
**Impact:** The effective threshold voltage of the rectifier is ~kT/q ≈ 26 mV (thermal
voltage), creating a dead zone of ~52 mVpp. Signals below this are rectified with
significant distortion.
**Mitigation:** This is a fundamental limit of OTA-based rectifiers in subthreshold.
For our minimum signal of 5 mVpp, the dead zone dominates. Solutions: (a) increase OTA
bias into moderate inversion (improves dead zone but increases power), (b) accept
nonlinear rectification at small signals (the classifier can learn this nonlinearity).

### Risk 3: Temperature Sensitivity of LPF Cutoff
**Likelihood:** High. LPF fc = gm/(2*pi*C). gm varies with temperature.
**Impact:** At 85C, gm drops → fc drops → slower settling (but less ripple). At -40C,
gm increases → fc increases → more ripple (but faster settling).
**Mitigation:** The spec allows fc = 5-20 Hz. Since gm varies ~+/-50% across temp,
fc will vary from ~5 Hz (-40C) to ~20 Hz (85C, if nominal is 10 Hz). This is exactly
within spec. Verify in TB5.

### Risk 4: Charge Sharing Between Channels
**Likelihood:** Low. All 5 channels share Vdd and Vss rails.
**Impact:** A large signal in one channel could cause supply bounce that couples into
other channels.
**Mitigation:** Decoupling capacitors on supply rails (10 pF per channel). The slow
LPF bandwidth (10 Hz) provides significant rejection of supply-coupled interference
(>60 dB at any frequency >1 kHz).

### Risk 5: Parasitic Capacitance on Rectifier Output Node
**Likelihood:** Medium. Routing from rectifier to LPF adds parasitic cap.
**Impact:** Creates an unwanted pole that could cause peaking or ringing.
**Mitigation:** Keep rectifier and LPF physically close in layout. The parasitic cap
(~0.1-0.5 pF) is small compared to C_lpf (50 pF) and has negligible effect.

---

## 12. Deliverable Sequence

| Step | Action | Depends On | Est. Time |
|------|--------|------------|-----------|
| 1 | Design dual-OTA rectifier schematic | Nothing | 2 hours |
| 2 | Design Gm-C LPF schematic | Nothing | 1 hour |
| 3 | Combine into `envelope_det.sch` | Steps 1, 2 | 1 hour |
| 4 | Extract `envelope_det.spice` | Step 3 | 15 min |
| 5 | Write TB1 (amplitude sweep) | Step 4 | 1 hour |
| 6 | Simulate TB1 with behavioral OTA | Step 5 | 1 hour |
| 7 | Evaluate min detectable signal | Step 6 | 30 min |
| 8 | Write TB2 (AM tracking) | Step 4 | 1 hour |
| 9 | Write TB3 (burst detection) | Step 4 | 1 hour |
| 10 | Write TB4 (ripple measurement) | Step 4 | 1 hour |
| 11 | Simulate TB2-TB4 | Steps 8-10 | 2 hours |
| 12 | Write TB5 (corners) | Step 4 | 1 hour |
| 13 | Run corner analysis | Step 12 | 2 hours |
| 14 | Record all results in `results.md` | Step 13 | 1 hour |
| 15 | Swap to real OTA, re-run all TBs | Block 01 done | 3 hours |
| 16 | Layout `envelope_det.mag` | Step 14 | 4-6 hours |
| 17 | PEX and post-layout simulation | Step 16 | 2 hours |
| 18 | Final results update | Step 17 | 30 min |

---

## 13. Simulation Commands Reference

```bash
# Amplitude sweep (single frequency)
ngspice -b tb_env_amp_sweep.spice -o amp_sweep.log

# AM tracking
ngspice -b tb_env_am_track.spice -o am_track.log

# Burst detection
ngspice -b tb_env_burst.spice -o burst.log

# Ripple measurement (loop over carrier frequencies)
for freq in 224 1000 3162 7071 14142; do
    ngspice -b -D CARRIER_FREQ=$freq tb_env_ripple.spice -o ripple_${freq}.log
done

# Corner analysis
for corner in tt ff ss fs sf; do
    for temp in -40 27 85; do
        ngspice -b -D CORNER=$corner -D TEMP=$temp \
            tb_env_corners.spice -o corners_${corner}_${temp}.log
    done
done

# Post-process: extract DC levels and ripple from raw data
python3 scripts/analyze_envelope.py amp_sweep.raw

# Plot amplitude sweep transfer curve
python3 scripts/plot_env_transfer.py

# Plot burst response overlay (input envelope vs detector output)
python3 scripts/plot_burst.py burst.raw
```

---

## 14. Results Template

### Rectification Accuracy (TB1)

| Input (mVpp) | Expected Vout (V) | Measured Vout (V) | Error (%) | PASS/FAIL |
|-------------|-------------------|-------------------|-----------|-----------|
| 5 | | | (±15%) | |
| 10 | | | (±15%) | |
| 20 | | | (±10%) | |
| 50 | | | (±5%) | |
| 100 | | | (±5%) | |
| 200 | | | (±5%) | |
| 500 | | | (±5%) | |

### Ripple Measurement (TB4)

| Channel | Carrier (Hz) | DC output (V) | Ripple (mVpp) | Ripple (%) | PASS (<5%) |
|---------|-------------|---------------|---------------|------------|------------|
| 1 | 224 | | | | |
| 2 | 1000 | | | | |
| 3 | 3162 | | | | |
| 4 | 7071 | | | | |
| 5 | 14142 | | | | |

### Transient Performance (TB3)

| Parameter | Spec | Measured | PASS/FAIL |
|-----------|------|----------|-----------|
| Rise time (10-90%) | <100 ms | | |
| Settling time (to 90%) | <200 ms | | |
| Fall time (90-10%) | <200 ms | | |
| 100mV/50mV ratio | 2.0 ±20% | | |
| Baseline (silence) | <10% of signal | | |

### Power

| Condition | Current (uA) | Power (uW) | PASS (<10 uW/ch) |
|-----------|-------------|-----------|-------------------|
| Per channel (TT 27C) | | | |
| Total 5 channels | | | |
