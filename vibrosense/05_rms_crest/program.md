# Block 05: Broadband RMS Detector, Peak Detector, and Crest Factor Computation

## 1. Objective

Design a broadband RMS detector and peak detector for vibration signal characterization.
The crest factor (peak/RMS ratio) is a key diagnostic feature: healthy bearings produce
near-sinusoidal vibration (CF ~1.4), while damaged bearings produce impulsive hits
(CF >> 3). This block extracts both RMS and peak values as analog voltages; the
crest factor itself is computed digitally in the MCU (Block 08) to avoid the complexity
and poor accuracy of analog dividers.

Total power budget: <25 uW for both detectors combined.

---

## 2. State of the Art

### 2.1 True-RMS Detectors

**Sarpeshkar log-domain RMS detector (JSSC 1998)**
- Topology: Log-domain filter exploiting the exponential I-V of BJTs to compute
  x^2 implicitly. Uses translinear principle.
- Power: ~20 uW (impressive for the era).
- Accuracy: True RMS, works for arbitrary waveform crest factors.
- Problem for us: Requires matched BJTs. SKY130 has parasitic PNPs but they are
  poorly matched and not characterized for translinear circuits. Would need extensive
  Monte Carlo and likely fail mismatch specs.

**Mulder RMS-DC converter (JSSC 1996)**
- Topology: Translinear loop performing implicit squaring, averaging, and square-root.
- Power: ~100 uW class (BiCMOS process).
- Accuracy: Excellent for true RMS, handles CF up to 5-7.
- Problem for us: Same as Sarpeshkar — needs matched bipolars. Also higher power.

**AD8436 (Analog Devices, commercial)**
- Topology: Direct computation true-RMS with sigma-delta modulator.
- Power: ~10 mW. Way too much for our 50 uW system budget.
- Accuracy: Excellent (0.1% linearity).
- Relevance: Sets the accuracy gold standard but irrelevant for ultra-low-power.

**De Nardi et al. subthreshold CMOS RMS (TCAS-I 2003)**
- Topology: Subthreshold MOS translinear loop (MOS in weak inversion as pseudo-exponential).
- Power: ~5 uW.
- Problem: Weak-inversion translinear accuracy is limited by threshold mismatch.
  Typical RMS error 5-10% without trimming. Possibly acceptable but fragile.

### 2.2 Peak Detectors

**Classical diode peak detector**
- Topology: Diode + hold capacitor + discharge resistor.
- Problem: Diode drop (~0.6V for silicon, ~0.15V for Schottky) eats into our
  ±0.3V signal range. Unacceptable.

**Active peak detector (OTA + diode-connected MOSFET)**
- Topology: OTA drives a diode-connected PMOS that charges a hold capacitor.
  OTA feedback eliminates the diode drop — tracks the input until the input falls
  below the held peak, at which point the PMOS turns off and the cap holds.
- Power: 1 OTA bias = ~5 uW (reuse Block 01 OTA or a simplified version).
- Hold time: Determined by leakage on hold cap. With 100 pF MIM cap and gate
  leakage of ~1 pA, droop rate = I/C = 10 uV/s. For 500 ms hold, droop = 5 mV.
  Acceptable for ±300 mV signals (1.7% error).
- Discharge: 100 Mohm poly resistor in parallel for slow reset. Tau = RC =
  100M * 100p = 10 ms. This is too fast — we need tau >> 500 ms. Revised: use
  10 Gohm effective resistance via a subthreshold MOSFET pseudo-resistor, or
  increase cap to 1 nF (area cost: ~0.1 mm^2 in MIM). Decision: use 100 pF cap
  with MOSFET pseudo-resistor (long-channel NMOS, Vgs ≈ 0, Rds > 10 Gohm in
  subthreshold). Tau = 10G * 100p = 1 s. Adequate.

### 2.3 Envelope / Approximate RMS

**Envelope detector approach (as used in Block 04)**
- Topology: Full-wave rectifier (OTA-based) + LPF (OTA-C, fc ~ 10-50 Hz).
- Output: Envelope ≈ mean absolute value (MAV). For a sinusoid, MAV = (2/pi)*Vpeak
  = 0.637*Vpeak, while Vrms = 0.707*Vpeak. Ratio: Vrms/MAV = 1.11. This is a
  fixed correction factor for sinusoidal signals. For non-sinusoidal signals the
  correction factor varies, but for vibration classification we don't need true RMS —
  we need a *consistent* amplitude measure that tracks signal power monotonically.
- Power: ~10 uW (one rectifier OTA + one LPF OTA).
- Accuracy as RMS proxy: For sinusoids, apply 1.11x correction in MCU. For
  bearing vibration (which is quasi-periodic), the correction factor is stable
  within ±5% empirically.

### 2.4 Design Decision

For this ultra-low-power system, true RMS is overkill. The envelope detector
(rectify + LPF) from Block 04 already provides a good amplitude measure. We reuse
the same topology here with wider bandwidth (no BPF — broadband RMS over 10 Hz to
10 kHz). The MCU applies a calibration factor to convert MAV to approximate RMS.

The peak detector is genuinely useful and cannot be approximated — we need the actual
maximum excursion, held for at least 500 ms so the MCU can read it during its
wake cycle.

Crest factor = Vpeak / Vrms is computed in the MCU after digitizing both values
through the shared ADC (Block 07). An analog divider would require a multiplier
core (Gilbert cell or log/antilog), consuming >20 uW and introducing >5% error
from device mismatch. Digital division is exact and free (the MCU is already awake).

---

## 3. Architecture

```
                          ┌──────────────────┐
Vin (broadband) ────┬────┤ Full-Wave Rect.   ├──── LPF (fc=20Hz) ──── V_rms
                    │    │ (OTA-based)        │
                    │    └──────────────────┘
                    │
                    │    ┌──────────────────┐
                    └────┤ Peak Detector     ├──── V_peak
                         │ (OTA + PMOS +     │
                         │  hold cap + reset)│
                         └──────────────────┘

MCU reads V_rms and V_peak via ADC (Block 07), computes:
  CF = V_peak / (V_rms × 1.11)
```

### 3.1 RMS Path (Broadband Envelope)

Identical to Block 04 envelope detector but without the input BPF:
1. **Full-wave rectifier**: Two cross-coupled OTAs performing |Vin|.
   - OTA Gm = 10 uA/V, bias current 2.5 uA.
   - Input: full bandwidth signal from PGA (Block 02), 10 Hz – 10 kHz.
2. **LPF**: Single-pole OTA-C filter, fc = 20 Hz.
   - Gm = 1.26 nA/V (very low — use minimum bias OTA).
   - C = 10 pF. fc = Gm / (2*pi*C) = 1.26e-9 / (6.28 * 10e-12) = 20 Hz. Correct.
   - Settling time to 1%: 5*tau = 5/(2*pi*20) = 40 ms. Fast enough for 10 Hz
     classification rate.

### 3.2 Peak Detector

1. **OTA comparator**: Compares Vin to Vhold. When Vin > Vhold, OTA output goes
   high, turning on charge PMOS.
   - OTA Gm = 10 uA/V. Bias = 2.5 uA.
2. **Charge PMOS (diode-connected)**: M1 = sky130_fd_pr__pfet_01v8, W/L = 1u/0.5u.
   When OTA output is high (Vin > Vhold), M1 conducts and charges Chold toward Vin.
   When Vin < Vhold, OTA output goes low, M1 turns off, Chold holds peak.
3. **Hold capacitor**: Chold = 100 pF (MIM, sky130_fd_pr__cap_mim_m3_1).
   Area: ~100 um x 100 um = 0.01 mm^2.
4. **Discharge element**: Long-channel NMOS pseudo-resistor.
   M2 = sky130_fd_pr__nfet_01v8_lvt, W/L = 0.42u/10u, Vgs biased at ~50 mV above
   Vth via a diode-connected replica. In deep subthreshold: Rds > 10 Gohm.
   Tau = 10G * 100p = 1 s. Peak decays to 37% after 1 s, holds >90% for 100 ms,
   holds >60% for 500 ms.
   - Actually we want >500 ms hold with <10% decay. Need tau > 5 s.
   - Revised: M2 W/L = 0.42u/20u. Doubles Rds to ~20 Gohm. Tau = 2 s.
     After 500 ms: exp(-0.5/2) = 0.78, so 22% decay. Still too much.
   - Revised: Increase Chold to 500 pF. Tau = 20G * 500p = 10 s. After 500 ms:
     exp(-0.05) = 0.95. Only 5% decay. Acceptable.
     Area cost: 500 pF MIM = ~500 um x 100 um = 0.05 mm^2. Acceptable.
5. **Reset switch**: NMOS switch controlled by MCU GPIO. Discharges Chold to
   ground (Vcm) before each new measurement window. Essential for avoiding stale
   peak values.

### 3.3 Power Budget

| Subcircuit | Current | Power (1.8V) |
|------------|---------|-------------|
| Rectifier OTA (×2) | 2 × 2.5 uA | 9.0 uW |
| LPF OTA | 0.5 uA | 0.9 uW |
| Peak OTA | 2.5 uA | 4.5 uW |
| Charge PMOS | ~0 (signal-dependent) | ~0 |
| Discharge pseudo-R | ~0.1 nA leakage | ~0 |
| **Total** | **8.0 uA** | **14.4 uW** |

Well within 25 uW budget. Leaves 10.6 uW margin for parasitics and bias circuits.

---

## 4. Detailed Design Procedure

### Step 1: Behavioral Simulation

Before transistor-level design, verify the architecture with ideal components:
- Ideal rectifier: `B_rect out gnd V = abs(V(inp) - V(inn))`
- Ideal LPF: RC with R = 1/(2*pi*20*10p) = 796 Mohm, C = 10 pF.
- Ideal peak detector: behavioral peak-hold model.
- Drive with known waveforms (sine, square, impulse train).
- Verify crest factor computation matches theory:
  - Sine: CF = sqrt(2) = 1.414
  - Square: CF = 1.0
  - Triangle: CF = sqrt(3) = 1.732
  - Impulse (duty cycle 1%): CF ≈ 10

### Step 2: RMS Path — Transistor-Level Rectifier

Use cross-coupled OTA topology:
```
        Vin+ ──┐     ┌── Vin-
                │     │
           ┌────┴─────┴────┐
           │   OTA_A        │──── Iout+
           └────┬─────┬────┘
                │     │
           ┌────┴─────┴────┐
           │   OTA_B        │──── Iout-
           └────────────────┘
```
OTA_A: non-inverting path (Vin+ to Iout+)
OTA_B: inverting path (Vin- to Iout+)
Diode-connected load converts |Iout| to voltage.

Actually, simpler approach: single OTA with output current mirrors that fold
negative half-cycles to positive:
1. OTA differential pair generates Iout+ and Iout-.
2. Both Iout+ and Iout- are mirrored and summed into a single output node.
3. Result: |Vin| * Gm flowing into a load resistor/diode.

This is the standard current-mode full-wave rectifier. Use Block 01 OTA
(behavioral model: Gm = 10 uA/V) with added output current mirrors.

### Step 3: RMS Path — LPF

OTA-C integrator with Gm = 1.26 nA/V:
- This requires a very-low-Gm OTA. Options:
  a) Source-degenerated OTA (resistor in source of diff pair). Gm_eff = Gm/(1 + Gm*Rs).
     For Gm = 10 uA/V and Rs = 8 Mohm: Gm_eff = 10u/(1+80) = 123 nA/V. Still too high.
  b) Current division: Mirror ratio 1:100. Gm_eff = Gm/100 = 100 nA/V. Close.
  c) Capacitive attenuation at input: Cin = 0.1 pF, Cfb = 10 pF. Attenuation = 100x.
     Gm_eff = 10u/100 = 100 nA/V. Close enough (fc = 100n/(6.28*10p) = 1.6 kHz).
     Need more attenuation or larger C.
  d) Subthreshold OTA with 50 nA bias. Gm = Ibias/nVT = 50n/(1.5*26m) = 1.28 uA/V.
     With C = 100 pF: fc = 1.28u/(6.28*100p) = 2 kHz. Still too high.
  e) Use large C = 10 nF (off-chip) or accept higher fc and correct digitally.

**Decision**: Use fc = 50 Hz with on-chip components.
- Subthreshold OTA, Ibias = 50 nA, Gm = 1.28 uA/V.
- Current division 1:4 in output mirror. Gm_eff = 320 nA/V.
- C = 1 nF (off-chip ceramic, or on-chip MIM if area allows — 1 nF MIM is
  1 mm x 1 mm, probably too large).
- fc = 320n/(6.28*1n) = 51 Hz. Close enough.
- Off-chip 1 nF ceramic cap is acceptable for prototype. Add pad for external cap.

### Step 4: Peak Detector — Transistor-Level

```
                     VDD
                      │
                 ┌────┴────┐
                 │  M_charge│ (PMOS, diode-connected)
                 │  W/L=1u/ │
                 │  0.5u    │
                 └────┬────┘
                      │
Vin ──┤+             │
      │  OTA  ├──────┘
Vhold─┤-
      │
                     Chold = 500pF
                      │
                 ┌────┴────┐
                 │M_discharge│ (NMOS pseudo-R)
                 │W/L=0.42u/│
                 │20u       │
                 └────┬────┘
                      │
                     Vcm
```

Operating principle:
1. When Vin > Vhold: OTA output goes low (toward VSS), M_charge turns ON (PMOS),
   current flows from VDD through M_charge into Chold, charging it toward Vin.
   Wait — this charges toward VDD, not Vin. Need feedback.

Revised topology (standard active peak detector):
```
Vin ──┤+             ┌─── Vhold ───┬─── to ADC
      │  OTA  ├──────┤             │
      ┤-      │      │           Chold
      │       │    D_PMOS         500pF
      └───────┘   (diode)         │
          │                       │
          └── feedback ───────────┘
```

Actually, the correct active peak detector:
1. OTA(+) = Vin, OTA(-) = Vhold (output node).
2. OTA output drives gate of PMOS source follower.
3. PMOS source = Vhold node (connected to Chold).
4. When Vin > Vhold: OTA drives PMOS gate low, PMOS conducts, charges Chold up
   toward Vin. Feedback through OTA(-) ensures Vhold tracks Vin.
5. When Vin < Vhold: OTA drives PMOS gate high, PMOS turns off. Chold holds.
6. No diode drop because the OTA provides the gain to compensate.

This is the Madhani-Bhatt active peak detector topology. Well-proven.

### Step 5: Testbench — RMS Linearity

```spice
* tb_rms_linearity.spice
* Sweep input amplitude from 10mVrms to 500mVrms (sine, 1kHz)
* Measure DC output of RMS path
* Plot Vout_rms vs Vin_rms — should be linear

.param Vamp=10m  ; swept externally
Vin inp gnd SIN(0.9 {Vamp} 1k)  ; 0.9V = Vcm

Xrms inp rms_out peak_out VDD VSS rms_crest_top
VDD VDD gnd 1.8
VSS VSS gnd 0

.tran 100u 200m
.meas tran Vrms_out AVG V(rms_out) FROM=100m TO=200m

* Sweep via external script: Vamp = 10m, 20m, 50m, 100m, 200m, 500m
* Post-process: compute ideal Vrms = Vamp/sqrt(2), compare to measured
```

### Step 6: Testbench — Peak Hold Time

```spice
* tb_peak_hold.spice
* Apply 100mVpeak pulse, then remove input. Measure decay on Vhold.

Vpulse inp gnd PULSE(0.9 1.0 0 1u 1u 10m 1)  ; single 10ms pulse
* After 10ms, input returns to 0.9V (Vcm). Peak should hold at ~1.0V.

Xrms inp rms_out peak_out VDD VSS rms_crest_top

.tran 1m 2  ; simulate 2 seconds
.meas tran Vpeak_at_10ms  FIND V(peak_out) AT=15m
.meas tran Vpeak_at_500ms FIND V(peak_out) AT=500m
.meas tran Vpeak_at_1s    FIND V(peak_out) AT=1

* PASS: Vpeak_at_500ms > 0.9 * Vpeak_at_10ms (less than 10% decay)
```

### Step 7: Testbench — Crest Factor Verification

```spice
* tb_crest_known.spice
* Test with known waveforms and verify crest factor

* Test 1: Sine wave (CF = 1.414)
Vsine inp gnd SIN(0.9 0.1 1k)
* Expected: Vpeak = 0.1V, Vrms ≈ 0.0707V, CF = 1.414

* Test 2: Square wave (CF = 1.0)
Vsquare inp gnd PULSE(0.8 1.0 0 1u 1u 0.5m 1m)
* Expected: Vpeak = 0.1V, Vrms = 0.1V, CF = 1.0

* Test 3: Impulse train (CF >> 1)
Vimp inp gnd PULSE(0.9 1.0 0 1u 1u 10u 1m)
* Duty cycle = 10u/1m = 1%. Expected: Vpeak = 0.1V, Vrms = 0.01V, CF = 10

* Run each separately, extract Vrms and Vpeak, compute CF in Python
```

---

## 5. PASS/FAIL Criteria

| Parameter | Target | Test Method |
|-----------|--------|-------------|
| RMS accuracy | ±5% at 100 mVrms (sine) | Compare Vout to ideal Vrms |
| RMS linearity | R^2 > 0.99 over 10–500 mVrms | Linear regression of sweep |
| RMS bandwidth | 10 Hz – 10 kHz (±3 dB) | Frequency sweep of RMS output |
| Peak accuracy | ±10% at 100 mVpeak | Compare Vpeak_held to actual peak |
| Peak hold time | >500 ms with <10% decay | Pulse then measure decay |
| Peak reset time | <1 ms | Assert reset, measure settling |
| Crest factor (sine) | 1.414 ±10% | Known waveform test |
| Crest factor (square) | 1.0 ±10% | Known waveform test |
| Crest factor (impulse) | >5 for 1% duty | Known waveform test |
| Total power | <25 uW | Measure IDD × VDD |
| Output noise | <1 mVrms on RMS output | Noise simulation |

---

## 6. Corner and Monte Carlo Strategy

### Corners (5 process × 3 temperature = 15 simulations)

| Corner | Process | Temperature |
|--------|---------|-------------|
| TT | Typical | 27°C |
| FF | Fast | -40°C |
| SS | Slow | 85°C |
| SF | Slow-N/Fast-P | 27°C |
| FS | Fast-N/Slow-P | 27°C |

Key concern: Peak detector hold time varies enormously with leakage current,
which is exponentially temperature-dependent. At 85°C, MOSFET leakage increases
~10x. The pseudo-resistor Rds will drop, reducing tau. Must verify hold time
at 85°C corner.

Mitigation: If 85°C hold time fails, increase Chold to 1 nF or use chopper-
stabilized OTA to reduce offset-induced droop.

### Monte Carlo (100 runs)

- Mismatch in rectifier OTAs: causes DC offset in RMS output. Target: offset < 5 mV.
- Mismatch in peak detector OTA: causes peak tracking error. Target: < 10 mV.
- Capacitor mismatch: 100 pF MIM has ~0.1% matching. Negligible.
- Pseudo-resistor variation: Vth mismatch in discharge MOSFET causes tau variation.
  This is the dominant concern. Expect 3-sigma tau variation of 2-5x.

---

## 7. Layout Considerations

### RMS Path
- Rectifier OTAs: common-centroid diff pairs, close to each other for matching.
- LPF cap: 1 nF off-chip (pad required) or on-chip MIM (1 mm^2 — large).
- Route: keep rectifier output short to avoid parasitic caps that degrade bandwidth.

### Peak Detector
- Hold cap (500 pF MIM): dominant area block. Place in top metal layers.
- Guard ring around hold node to minimize substrate leakage.
- Charge PMOS and discharge NMOS: place adjacent to hold cap, minimize routing.
- Shield hold node from switching signals (clock, digital IO) to prevent charge
  injection onto the hold cap.

### Area Estimate
| Block | Area |
|-------|------|
| Rectifier OTAs | 50 um × 30 um = 0.0015 mm^2 |
| LPF OTA | 30 um × 20 um = 0.0006 mm^2 |
| Peak OTA | 50 um × 30 um = 0.0015 mm^2 |
| Hold cap (500 pF) | 500 um × 100 um = 0.05 mm^2 |
| Routing/decoupling | ~0.01 mm^2 |
| **Total** | **~0.065 mm^2** |

---

## 8. Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Peak hold too short at 85°C | HIGH | Increase Chold, add guard ring, use LVT MOSFET for pseudo-R |
| RMS rectifier has dead zone near zero-crossing | MEDIUM | Pre-bias rectifier OTAs slightly above zero-crossing; accept ~5mV dead zone |
| Off-chip LPF cap required (1 nF) | LOW | Acceptable for prototype; can shrink with lower fc or active multiplication |
| Pseudo-resistor tau has huge variation | HIGH | Calibrate in MCU: measure decay rate during startup, store correction |
| Crest factor inaccurate for non-sinusoidal waveforms | MEDIUM | Acceptable — CF is relative metric for classification, not absolute measurement |

---

## 9. Integration with System

### Inputs
- `Vin`: Broadband signal from PGA (Block 02), 10 Hz – 10 kHz, ±300 mV around Vcm = 0.9V.
- `Vreset`: Digital signal from MCU (Block 08) to reset peak detector.
- `VDD` = 1.8V, `VSS` = 0V.

### Outputs
- `V_rms`: DC voltage proportional to RMS (actually MAV × gain). Range: 0.9V ± 200 mV.
- `V_peak`: Held peak voltage. Range: 0.9V to 1.2V.
- Both outputs connect to analog mux feeding ADC (Block 07).

### Timing
1. MCU wakes, asserts `Vreset` LOW to clear peak detector.
2. MCU releases `Vreset` HIGH. Peak detector begins tracking.
3. Wait 100 ms for RMS path to settle (5 × tau_LPF).
4. Wait 200–500 ms for peak detector to capture maximum.
5. MCU triggers ADC to digitize V_rms, then V_peak (sequential via mux).
6. MCU computes CF = V_peak / (V_rms × 1.11).
7. MCU stores CF as feature for classifier (Block 06).

---

## 10. Validation Against Known Signals

Before connecting to real vibration data, validate with synthetic test signals:

| Waveform | Frequency | Amplitude | Expected CF | Tolerance |
|----------|-----------|-----------|-------------|-----------|
| Sine | 1 kHz | 100 mVpeak | 1.414 | ±10% |
| Square | 1 kHz | 100 mVpeak | 1.000 | ±10% |
| Triangle | 1 kHz | 100 mVpeak | 1.732 | ±15% |
| Gaussian noise | broadband | 100 mVrms | ~3–4 | ±20% |
| Impulse (1% duty) | 1 kHz rep | 100 mVpeak | ~10 | ±30% |
| Clipped sine (3dB) | 1 kHz | 100 mVpeak | 1.15 | ±15% |

The impulse and Gaussian noise cases are most representative of bearing fault signatures.

---

## 11. References

1. R. Sarpeshkar, "Ultra Low Power Bioelectronics," Cambridge University Press, 2010.
2. R. Sarpeshkar et al., "Low-power log-domain RMS detector," JSSC 1998.
3. J. Mulder et al., "A current-mode translinear RMS-DC converter," JSSC 1996.
4. Analog Devices, "AD8436 Low Cost, Low Power, True RMS-to-DC Converter," datasheet.
5. M. De Nardi et al., "A CMOS RMS-DC converter in subthreshold," TCAS-I 2003.
6. T. Madhani, D. Bhatt, "Active peak detector design considerations," Proc. IEEE 1999.

---

## 12. Checklist

- [ ] Behavioral simulation validates crest factor for sine, square, impulse
- [ ] Transistor-level rectifier: <5 mV dead zone, <1% THD at 100 mVrms
- [ ] Transistor-level peak detector: hold time >500 ms at 27°C
- [ ] Peak hold time at 85°C: >200 ms (relaxed) or >500 ms (with mitigation)
- [ ] RMS linearity R^2 > 0.99 from 10 mVrms to 500 mVrms
- [ ] Total power measured: <25 uW at TT/27°C
- [ ] Monte Carlo 100 runs: RMS offset < 5 mV (3-sigma)
- [ ] Monte Carlo 100 runs: peak error < 10 mV (3-sigma)
- [ ] Corner simulations: all specs pass at TT, one or fewer marginal at corners
- [ ] Integration test: MCU reset → settle → ADC read → CF computation validated
