# Block 02: Capacitive-Feedback Programmable Gain Amplifier (PGA)

## Design Program — Complete Specification and Verification Plan

---

## 1. Context and Motivation

The MEMS accelerometer (ADXL355) outputs 100-660 mV/g. A healthy motor at 30 Hz produces
0.1g (10-66 mVpp), while a failing bearing can produce 2g (200 mV-1.3 Vpp). The downstream
Gm-C filter bank operates optimally at ~200 mVpp input. The PGA bridges this 40 dB dynamic
range by providing 4 switched gain settings: 1x, 4x, 16x, and 64x.

Without the PGA, the filter bank would need to handle inputs from millivolts to over a volt,
which is impractical for Gm-C filters operating at microwatt power levels — their linearity
degrades catastrophically at large signal swings.

---

## 2. State of the Art Comparison

| Parameter | TI PGA309 | AD AD8231 | Zheng JSSC 2017 | **This Work (Target)** |
|-----------|-----------|-----------|-----------------|------------------------|
| Gain range | 0.4-800x | 1-128x | 1-100x | 1-64x |
| Gain steps | Continuous (DAC) | 8 steps | 4 steps | 4 steps |
| Power | 90 uW | 1.05 mW | 0.4 uW | <5 uW |
| Supply | 2.7-5.5 V | 2.2-5.5 V | 0.5 V | 1.8 V |
| Bandwidth | 90 kHz (G=1) | 3 MHz (G=1) | 1.2 kHz (G=100) | 25 kHz (all gains) |
| Input noise | 24 nV/rtHz | 17 nV/rtHz | 2.8 uV/rtHz | <200 nV/rtHz |
| THD | -80 dBc | -100 dBc | -40 dBc | <-40 dBc at 1 Vpp |
| Process | BiCMOS | BiCMOS | 180nm CMOS | SKY130 |
| Application | Sensor signal | Instrumentation | Biopotential | Vibration sensing |

### Analysis of Prior Art

**TI PGA309:** Designed for bridge sensors. Continuous gain via internal DAC gives excellent
flexibility but at 90 uW — too high for our always-on budget. BiCMOS process provides
low-noise bipolar input stage not available in SKY130.

**AD AD8231:** Instrumentation amplifier topology with R-2R gain setting. 1 mW power is
100x over our budget. The instrumentation amp approach provides excellent CMRR but is
power-hungry due to three-opamp architecture.

**Zheng et al., JSSC 2017:** The closest prior art. Achieves 0.4 uW at 0.5V supply for
biopotential (sub-kHz bandwidth). Uses capacitive feedback with subthreshold OTA. The key
insight is that capacitive feedback sets gain by ratio (Cin/Cf), independent of OTA gain,
achieving excellent gain accuracy. However, bandwidth is only 1.2 kHz at max gain — we
need 25 kHz, requiring ~20x more gm and proportionally more power.

**Our position:** We sacrifice the ultra-low power of Zheng (0.4 uW) for 25x more bandwidth
(25 kHz vs 1 kHz). Our 5 uW target is still 18x below PGA309. The capacitive-feedback
topology from Zheng scales well to higher bandwidth.

---

## 3. Topology: Capacitive-Feedback PGA

### 3.1 Architecture

```
                    Cf = 1 pF (fixed)
                 ┌────────┤├────────────┐
                 │                       │
    Vin ──┤├──┬──┤(-)                    │
       Cin(sel)  │         ┌─────┐      │
                 └────────►│ OTA │──────┴──── Vout
                           │     │
           Vcm ──────────►│(+)  │
                           └─────┘
```

### 3.2 Gain Setting by Capacitor Ratio

The closed-loop gain is set by the ratio of input to feedback capacitance:

```
    A_CL = -Cin / Cf
```

This ratio is independent of OTA gain (as long as loop gain >> 1), providing excellent
gain accuracy determined only by capacitor matching in the SKY130 process.

### 3.3 Switched Input Capacitor Network

| Gain | Cin Required | Implementation | Switch Control |
|------|-------------|----------------|----------------|
| 1x | 1 pF | 1 pF MIM cap | S0 only |
| 4x | 4 pF | 4 pF MIM cap | S1 only |
| 16x | 16 pF | 16 pF MIM cap | S2 only |
| 64x | 64 pF | 64 pF MIM cap | S3 only |

Cf is fixed at 1 pF (MIM capacitor, SKY130 `sky130_fd_pr__cap_mim_m3_1`).

Each Cin is connected through an NMOS pass-gate switch. Only one switch is closed at a
time (one-hot encoding). The switches use `sky130_fd_pr__nfet_01v8` with W/L sized to
keep Ron << 1/(2*pi*f*Cin) at 25 kHz.

### 3.4 Switch Sizing

The switch on-resistance must satisfy Ron << 1/(2*pi*25kHz*Cin_max):

| Gain | Cin | 1/(2*pi*f*Cin) | Required Ron | NMOS W/L |
|------|-----|----------------|--------------|----------|
| 1x | 1 pF | 6.4 MOhm | <640 kOhm | 0.42u/0.15u |
| 4x | 4 pF | 1.6 MOhm | <160 kOhm | 0.42u/0.15u |
| 16x | 16 pF | 398 kOhm | <40 kOhm | 1u/0.15u |
| 64x | 64 pF | 99.5 kOhm | <10 kOhm | 5u/0.15u |

At Vgs = 1.8V (digital control), minimum-length NMOS in SKY130 has Ron ~ 2-5 kOhm for
W = 1 um. The 64x switch needs W = 5 um to get Ron < 10 kOhm.

### 3.5 Feedback Capacitor Details

Cf = 1 pF using MIM capacitor. MIM caps in SKY130 have ~1 fF/um^2 density, so 1 pF
requires ~1000 um^2 (about 32 um x 32 um). Matching between Cin and Cf tracks well
since both are MIM.

SKY130 MIM cap matching: sigma(dC/C) ~ 0.5%/sqrt(area_in_um^2). For Cf = 1 pF (1000
um^2): sigma ~ 0.016% — excellent for gain accuracy.

### 3.6 Bias and Common-Mode

- OTA biased at Ibias = 500 nA from Block 00 bias generator
- Non-inverting input connected to Vcm = 0.9V (mid-rail)
- Output settles to Vcm when input is zero (DC-blocked by Cin)
- A large resistor (Rbias ~ 10 GOhm, implemented as pseudo-resistor using back-to-back
  subthreshold PMOS) sets the DC operating point of the inverting input

### 3.7 Pseudo-Resistor for DC Biasing

The inverting node needs a DC path to establish its operating point. A physical resistor
large enough (>1 GOhm) would be impractical in area. Instead, use a MOS pseudo-resistor:

```
    Vcm ──┬── M1(PMOS, diode-connected, subthreshold) ──┬── Inverting node
          └── M2(PMOS, diode-connected, subthreshold) ──┘
          (anti-parallel for symmetric bipolar conduction)
```

W/L = 0.42u/10u for each PMOS. In subthreshold, this gives an effective resistance of
~100 GOhm at DC, which drops with signal amplitude but remains >1 GOhm for signals
up to 100 mV — sufficient for our operating range.

---

## 4. Performance Targets — PASS/FAIL Criteria

### 4.1 Primary Specifications

| Parameter | Specification | Condition | PASS/FAIL |
|-----------|--------------|-----------|-----------|
| Gain accuracy | +/-0.5 dB | All 4 gain settings, TT corner | MUST PASS |
| Gain accuracy (PVT) | +/-1.0 dB | All gains, all corners, -40/27/85C | MUST PASS |
| Bandwidth (-3dB) | >25 kHz | All 4 gain settings | MUST PASS |
| THD | <-40 dBc | 1 kHz, 1 Vpp output swing | MUST PASS |
| Input-referred noise | <200 nV/rtHz | At 1 kHz, gain = 64x | MUST PASS |
| Total power | <5 uW | At 1.8V supply, TT 27C | MUST PASS |
| Output swing | >1.0 Vpp | At gain = 1x, <1% THD | SHOULD PASS |
| PSRR | >40 dB | At 1 kHz | SHOULD PASS |

### 4.2 Derived Requirements on OTA

For the PGA to meet specs, the OTA must satisfy:

- **Open-loop gain > 60 dB:** Gain error = 1/A_OL. At 60 dB (1000x), gain error = 0.1%
  = 0.009 dB — well within +/-0.5 dB budget.
- **GBW > 25 kHz x 64 = 1.6 MHz:** At gain = 64x, the closed-loop BW is GBW/64.
  To maintain BW > 25 kHz at max gain, GBW must exceed 1.6 MHz.
- **Phase margin > 60 degrees:** With capacitive feedback, the loop is inherently stable
  (no resistive load), but the large Cin at 64x gain adds load.
- **Output swing > +/-500 mV around Vcm:** To support 1 Vpp output.

The behavioral OTA model has gm = 2.5 uS, Rout = 400 MOhm — use this for
initial topology verification only (Steps 1-3). Replace with real OTA in Step 4.

**The real OTA is ota_pga_v2 (two-stage Miller, 422 kHz UGB at TT 27°C).**

Verified closed-loop bandwidths with ota_pga_v2:

| Gain | Noise gain | UGB (TT) | Closed-loop BW | Meets >25kHz? |
|------|-----------|----------|----------------|---------------|
| 1x   | 1         | 422 kHz  | 422 kHz        | YES           |
| 4x   | 5         | 422 kHz  | 84 kHz         | YES           |
| 16x  | 17        | 422 kHz  | 24.8 kHz       | YES (barely)  |
| 64x  | 65        | 422 kHz  | 6.5 kHz        | YES (>6 kHz)  |

At SS corner (375 kHz UGB): 16x BW = 22 kHz — marginally below 25 kHz.
This is a known, accepted limitation documented in ota_pga_v2/README.md.

### 4.3 Revised BW Specification

| Gain | BW Target | Rationale |
|------|-----------|-----------|
| 1x | >25 kHz | Full bandwidth for large signals |
| 4x | >25 kHz | Full bandwidth |
| 16x | >25 kHz | Full bandwidth |
| 64x | >6 kHz | Reduced — acceptable for small-signal conditions |

---

## 5. Detailed Design Procedure

### Step 1: Schematic Entry

Create `pga.sch` in Xschem with the following subcircuit interface:

```
.subckt pga vin vout vcm vdd vss gain<1> gain<0>
* gain<1:0>: 00=1x, 01=4x, 10=16x, 11=64x
```

Internal components:
1. OTA instance (behavioral initially, replace with real)
2. Cf = 1 pF MIM cap from output to inverting input
3. Cin1 = 1 pF + switch S0 (NMOS, controlled by decoded gain=1x signal)
4. Cin2 = 4 pF + switch S1
5. Cin3 = 16 pF + switch S2
6. Cin4 = 64 pF + switch S3
7. 2-to-4 decoder (4 NAND gates + inverters) for one-hot switch control
8. Pseudo-resistor (back-to-back PMOS) for DC bias
9. Input DC-blocking cap (optional — if MEMS output is already AC-coupled)

### Step 2: Extract Netlist

Export `pga.spice` from Xschem. Verify all nodes are connected. Verify switch control
logic by manual inspection.

### Step 3: Simulate (Behavioral OTA)

Run all 7 testbenches with behavioral OTA. Record results. Fix any issues.

### Step 4: Replace with Real OTA

Swap the behavioral OTA with the real two-stage Miller OTA:

```spice
* Remove behavioral OTA include, add these two lines:
.include "../01_ota/ota_pga_v2/ota_pga_v2.spice"
.include "../../00_bias/bias_distribution/design_full.cir"

* Bias generator instance (Riref sets Iref = 1.8V / 3560 = 505 nA):
Xbias vdd gnd iref_out vbn vbcn vbp vbcp  bias_generator_full
Riref iref_out gnd 3560

* OTA instance (vbcn/vbp/vbcp declared but unconnected inside ota_pga_v2):
Xota  vdd gnd inp inn out vbn vbcn vbp vbcp  ota_pga_v2
```

Do NOT use ideal voltage sources for bias — must use bias_generator_full.
Do NOT use ota_foldcasc or ota_pga (v1) — use ota_pga_v2 only.

PDK location (on AWS instance):
  /c/Users/DD/AppData/Local/Temp/sky130.lib.spice  (local machine)
  /home/ubuntu/pdk/sky130A/libs.ref/...            (AWS instance)

Re-run all testbenches. Compare with behavioral results. Flag degradation >10%.

### Step 5: Layout

Create `pga.mag` in Magic. Key layout considerations:
- MIM capacitor matching: common-centroid layout for Cin/Cf ratios
- Switch transistors close to capacitors (minimize parasitic)
- Guard rings around sensitive analog nodes
- Capacitor area estimate: Cf(1pF)=1000um^2, Cin1(1pF)=1000um^2, Cin2(4pF)=4000um^2,
  Cin3(16pF)=16000um^2, Cin4(64pF)=64000um^2. Total cap area ~86000 um^2 = 0.086 mm^2.
  The 64 pF capacitor dominates layout area.

### Step 6: PEX and Re-simulate

Extract parasitics from Magic. Re-run AC analysis to verify BW is not degraded by
parasitic capacitance on switch nodes.

---

## 6. Testbench Specifications

### 6.1 TB1: AC Analysis at Gain = 1x (`tb_pga_ac_1x.spice`)

**Purpose:** Verify gain magnitude and -3 dB bandwidth at minimum gain.

**Setup:**
```
Vdd = 1.8V
Vcm = 0.9V
Vin: AC source, 10 mVpk, swept 1 Hz to 10 MHz
gain<1:0> = 00 (select 1x)
Load: CL = 10 pF (standard interface load)
```

**Measurements:**
- Midband gain (at 1 kHz): expect 0 dB +/-0.5 dB
- -3 dB frequency: expect >25 kHz
- Gain peaking: expect <1 dB
- Phase at -3 dB point: record for stability check

**PASS criteria:** |Gain_measured - 0 dB| < 0.5 dB AND f_3dB > 25 kHz

### 6.2 TB2: AC Analysis at Gain = 4x (`tb_pga_ac_4x.spice`)

**Setup:** Same as TB1, but gain<1:0> = 01.

**Measurements:**
- Midband gain: expect 12.04 dB +/-0.5 dB
- -3 dB frequency: expect >25 kHz
- Record gain peaking and phase margin

**PASS criteria:** |Gain_measured - 12.04 dB| < 0.5 dB AND f_3dB > 25 kHz

### 6.3 TB3: AC Analysis at Gain = 16x (`tb_pga_ac_16x.spice`)

**Setup:** Same as TB1, but gain<1:0> = 10.

**Measurements:**
- Midband gain: expect 24.08 dB +/-0.5 dB
- -3 dB frequency: expect >25 kHz
- Stability: monitor for gain peaking >3 dB (indicates marginal phase margin)

**PASS criteria:** |Gain_measured - 24.08 dB| < 0.5 dB AND f_3dB > 25 kHz

### 6.4 TB4: AC Analysis at Gain = 64x (`tb_pga_ac_64x.spice`)

**Setup:** Same as TB1, but gain<1:0> = 11.

**Measurements:**
- Midband gain: expect 36.12 dB +/-0.5 dB
- -3 dB frequency: expect >6 kHz (relaxed target — see Section 4.3)
- Gain peaking: CRITICAL — 64 pF Cin heavily loads the OTA

**PASS criteria:** |Gain_measured - 36.12 dB| < 0.5 dB AND f_3dB > 6 kHz

**WATCH for instability:** If gain peaking >3 dB, add Miller compensation capacitor
(Cc ~ 0.5 pF) inside the feedback loop and re-simulate. Document the compensation.

### 6.5 TB5: THD Measurement (`tb_pga_thd.spice`)

**Purpose:** Verify linearity at maximum output swing.

**Setup:**
```
Vin: 1 kHz sine wave
Amplitude: set to produce 1 Vpp output at each gain setting:
  - Gain 1x:  Vin = 500 mVpk
  - Gain 4x:  Vin = 125 mVpk
  - Gain 16x: Vin = 31.25 mVpk
  - Gain 64x: Vin = 7.8 mVpk
Simulation: Transient, 10 ms (10 cycles), step = 100 ns
Post-process: FFT of last 5 cycles, measure HD2, HD3, HD4, HD5, THD
```

**Measurements per gain:**
- THD (RSS of HD2-HD5)
- Individual harmonic levels
- Dominant harmonic identification

**PASS criteria:** THD < -40 dBc (1% distortion) at all gains

**Expected THD contributors:**
1. OTA output swing nonlinearity (dominant at large output)
2. Switch charge injection (dominant at low input levels / high gain)
3. Pseudo-resistor nonlinearity (modulates DC bias point with signal)

If THD fails at 64x gain due to switch charge injection, consider:
- Complementary (CMOS) transmission gates instead of NMOS-only switches
- Bottom-plate sampling technique
- Dummy switches for charge cancellation

### 6.6 TB6: Gain Switching Transient (`tb_pga_switching.spice`)

**Purpose:** Verify clean transitions when changing gain during operation.

**Setup:**
```
Vin: 1 kHz, 50 mVpk (constant throughout)
t=0 to 1ms: gain = 1x (gain<1:0> = 00)
t=1ms: switch to 4x (gain<1:0> = 01)
t=2ms: switch to 16x (gain<1:0> = 10)
t=3ms: switch to 64x (gain<1:0> = 11)
t=4ms: switch back to 1x
Simulation: Transient, 5 ms, step = 100 ns
```

**Measurements:**
- Settling time at each transition (to within 1% of final value)
- Overshoot/undershoot magnitude
- Glitch energy (integral of |Vout - Vfinal| during transient)

**PASS criteria:**
- Settling time < 100 us at each transition
- Overshoot < 20% of step
- No sustained oscillation after switching

**Key concern:** When switching from low-gain (small Cin) to high-gain (large Cin), the
charge stored on the old Cin creates a transient at the inverting node. The pseudo-resistor
must discharge this. With Rpseudo ~ 100 GOhm and Cin = 64 pF, tau = 6.4 seconds — far
too slow for natural settling. The OTA feedback loop must handle the settling, with time
constant tau = Cf/(gm) = 1 pF / 2.5 uS = 0.4 us — fast enough.

### 6.7 TB7: Noise Analysis (`tb_pga_noise.spice`)

**Purpose:** Measure input-referred noise density and total integrated noise.

**Setup:**
```
Each gain setting separately
Noise analysis: 1 Hz to 1 MHz
Measure input-referred noise spectral density
Integrate noise from 100 Hz to 25 kHz (signal band)
```

**Measurements per gain:**
- Input-referred noise at 1 kHz (nV/rtHz)
- 1/f noise corner frequency
- Total integrated noise (100 Hz - 25 kHz)
- Output SNR = 20*log10(Vsig_rms / Vnoise_rms)

**PASS criteria:**
- Input-referred noise < 200 nV/rtHz at 1 kHz (any gain)
- Total integrated noise < 50 uVrms (gain = 64x)

**Noise analysis notes:**
- At high gains (64x), input-referred noise is dominated by the OTA
- At low gains (1x), switch thermal noise (4kT*Ron) may contribute
- Pseudo-resistor generates significant 1/f noise — check corner frequency
- The SKY130 PMOS 1/f noise coefficient is approximately 10x worse than NMOS;
  if pseudo-resistor noise dominates, consider using NMOS-based pseudo-resistor
  (at the cost of asymmetric conduction)

---

## 7. Corner and Temperature Analysis

### 7.1 Process Corners (`tb_pga_corners.spice`)

Run all primary measurements across:

| Corner | NMOS | PMOS | Description |
|--------|------|------|-------------|
| TT | Typical | Typical | Nominal |
| FF | Fast | Fast | Best-case speed, worst-case power |
| SS | Slow | Slow | Worst-case speed |
| FS | Fast | Slow | Skewed — worst for PMOS-dependent circuits |
| SF | Slow | Fast | Skewed — worst for NMOS-dependent circuits |

### 7.2 Temperature Sweep

At each corner, sweep: -40C, 27C, 85C (3 temperatures x 5 corners = 15 conditions).

**Expected temperature effects:**
- Switch Ron increases with temperature (mobility degradation) — BW may decrease
- OTA gm decreases with temperature — BW decreases, gain accuracy maintained (cap ratio)
- Pseudo-resistor value changes dramatically (exponential with temperature) — may cause
  DC bias drift at -40C

### 7.3 Cross-Corner Gain Accuracy

**The key advantage of capacitive feedback PGA:** Gain = Cin/Cf, which depends only on
capacitor ratio. MIM capacitor matching in SKY130 is process-independent to first order.
Temperature coefficient of MIM caps is ~30 ppm/C, and since both Cin and Cf are MIM,
the ratio is insensitive.

**Expected result:** Gain accuracy < +/-0.2 dB across all corners and temperatures.

If gain accuracy degrades in FS/SF corners, the cause is OTA gain reduction (loop gain
insufficient to enforce virtual ground). In this case, the OTA DC gain at worst corner
must be checked.

---

## 8. Power Budget

| Component | Current | Power (at 1.8V) |
|-----------|---------|-----------------|
| OTA (Ibias = 500 nA) | 1.5 uA (total supply) | 2.7 uW |
| Switch leakage (4 switches) | <1 nA total | <1.8 nW |
| Decoder logic (static CMOS) | <10 nA | <18 nW |
| Pseudo-resistor | <1 nA | <1.8 nW |
| **Total** | **~1.5 uA** | **~2.7 uW** |

Well within the 5 uW budget. If the real OTA requires more current for GBW, there is
~2.3 uW margin.

---

## 9. Integration Checklist

### 9.1 Interface to Block 01 (OTA)

- [ ] OTA subcircuit pinout matches PGA instantiation
- [ ] OTA bias current input connected to Block 00 current mirror output
- [ ] OTA common-mode input range covers Vcm = 0.9V
- [ ] OTA output swing covers +/-500 mV around Vcm

### 9.2 Interface to Block 03 (Filters)

- [ ] PGA output impedance << filter input impedance (capacitive: should be OK)
- [ ] PGA output DC level = Vcm = 0.9V (matches filter input bias)
- [ ] PGA output swing 50-500 mVpp (within filter linear range)
- [ ] PGA output load (filter input cap ~10 pF) included in simulations

### 9.3 Behavioral vs. Real OTA Comparison

When Block 01 delivers the real OTA netlist, create a comparison table:

| Parameter | Behavioral OTA | Real OTA | Delta | PASS (<10%) |
|-----------|---------------|----------|-------|-------------|
| Gain at 1x | | | | |
| Gain at 64x | | | | |
| BW at 1x | | | | |
| BW at 64x | | | | |
| THD at 1x | | | | |
| THD at 64x | | | | |
| Noise at 64x | | | | |
| Power | | | | |

---

## 10. Known Risks and Mitigations

### Risk 1: 64x Gain Instability
**Likelihood:** Medium. The 64 pF input cap heavily loads the virtual ground node.
**Impact:** Oscillation or excessive ringing.
**Mitigation:** Add series resistance (1-5 kOhm) in the feedback path (between OTA output
and Cf) to create a zero that improves phase margin. Alternatively, reduce OTA gm at 64x
gain (lower bandwidth but stable).

### Risk 2: Pseudo-Resistor Variability
**Likelihood:** High. MOS pseudo-resistors vary by 10-100x across PVT.
**Impact:** DC settling time varies wildly; possible DC offset at output.
**Mitigation:** The pseudo-resistor only needs to be "large enough" (>100 MOhm). Even at
worst case (100x reduction from nominal 100 GOhm), it's still 1 GOhm — adequate. But
verify at FF corner, 85C.

### Risk 3: Charge Injection from Switches
**Likelihood:** Medium. When gain switches change, NMOS channel charge dumps onto Cin.
**Impact:** Momentary glitch on output; possible gain error if charge redistributes to Cf.
**Mitigation:** Use complementary transmission gates (NMOS + PMOS in parallel) for partial
charge cancellation. Add dummy half-size switches. Verify with transient testbench TB6.

### Risk 4: MEMS Sensor DC Offset
**Likelihood:** High. MEMS accelerometers have 10-100 mV DC offset.
**Impact:** At 64x gain, a 100 mV DC offset would produce 6.4V at output — rail-to-rail.
**Mitigation:** The input is AC-coupled through Cin, so DC is blocked. However, verify
that the pseudo-resistor settles the inverting node to Vcm (via OTA feedback) and does
not create a residual DC offset at the output due to OTA input offset voltage. OTA offset
of 5 mV at 64x gain gives 320 mV DC shift at output — significant but within rail
(0.9V +/- 0.5V swing = 0.4V to 1.4V, shifted to 0.58V-1.22V — still OK).

---

## 11. Deliverable Sequence

| Step | Action | Depends On | Est. Time |
|------|--------|------------|-----------|
| 1 | Create `pga.sch` in Xschem | Nothing | 2 hours |
| 2 | Extract `pga.spice` | Step 1 | 15 min |
| 3 | Write all 7 testbenches | Step 2 | 3 hours |
| 4 | Simulate with behavioral OTA | Step 3 | 1 hour |
| 5 | Debug and iterate | Step 4 | 2-4 hours |
| 6 | Record results in `results.md` | Step 5 | 30 min |
| 7 | Swap to real OTA, re-simulate | Block 01 done | 2 hours |
| 8 | Layout `pga.mag` | Step 5 | 4-8 hours |
| 9 | PEX and post-layout sim | Step 8 | 2 hours |
| 10 | Final results update | Step 9 | 30 min |

---

## 12. Simulation Commands Reference

```bash
# AC analysis at gain = 1x
ngspice -b tb_pga_ac_1x.spice -o tb_pga_ac_1x.log

# THD measurement (transient)
ngspice -b tb_pga_thd.spice -o tb_pga_thd.log

# Corner analysis (loop over corners)
for corner in tt ff ss fs sf; do
    ngspice -b -D CORNER=$corner tb_pga_corners.spice -o corners_$corner.log
done

# Post-process THD from transient data
python3 scripts/measure_thd.py tb_pga_thd.raw

# Plot all AC responses on one graph
python3 scripts/plot_ac_all_gains.py
```

---

## 13. Results Template

After simulation, populate this table in `results.md`:

| Parameter | Spec | 1x | 4x | 16x | 64x | PASS/FAIL |
|-----------|------|-----|-----|------|------|-----------|
| Gain (dB) | nom +/-0.5 | | | | | |
| BW (kHz) | >25 / >6@64x | | | | | |
| THD (dBc) | <-40 | | | | | |
| Noise (nV/rtHz) | <200 | | | | | |
| Power (uW) | <5 | | | | | |
| PSRR (dB) | >40 | | | | | |
| Settling (us) | <100 | | | | | |

---

## Final Step: Document and Commit

**Mandatory. Do not declare complete without this.**

### README.md

Write `README.md` in this folder containing:

1. **Status** — one line: ALL PASS / PARTIAL / FAIL
2. **Results table** — every spec from `specs.json`: target | measured (TT 27°C) | worst corner | PASS/FAIL
3. **Files created** — every file in this folder with a one-line description
4. **Key design decisions** — 3–5 bullets on non-obvious choices (topology, sizing rationale, tradeoffs)
5. **Known limitations** — anything that failed, was relaxed, or is marginal at corners

### Git commit and push

After README.md is complete:

```bash
cd /c/Users/DD/OneDrive/Programming/willAI/analog-ai-chips
git add vibrosense/02_pga/
git commit -m "design(02_pga): <one-line summary with key measured result>"
git push
```

The commit message must include the actual measured result.
Example: `design(02_pga): capacitive-feedback PGA — BW=28kHz at 16x, THD=-42dBc`
Do not use a generic message like "add files" or "complete block".
