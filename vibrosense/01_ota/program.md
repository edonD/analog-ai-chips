# Block 01: Folded-Cascode OTA — Program

## 1. Mission

Design a folded-cascode OTA in the SkyWater SKY130A process that serves as the
**universal analog building block** for the entire VibroSense signal path. Every
Gm-C filter, the programmable-gain amplifier (PGA), and every envelope detector
in the system will be built from instances of this single OTA. There is no
second chance here: if the OTA is marginal, every block that follows inherits
its weaknesses. If the OTA is over-designed and burns too much current, the
power budget for the full chip is blown before we even reach the ADC.

The design target is deliberately **moderate** — 65 dB gain, 50 kHz unity-gain
bandwidth, roughly 1 uA total current — because this block must work reliably
across corners and temperatures without heroic tuning. We are not chasing a
publication; we are building infrastructure.

### What "done" means

The OTA is done when:

1. A SPICE subcircuit netlist (`ota_foldcasc.spice`) passes ALL specs in
   Section 5 across 5 corners and 3 temperatures.
2. Monte Carlo analysis (200 runs) shows offset < 10 mV (3-sigma).
3. A Magic layout (`ota_foldcasc.mag`) passes DRC, and post-extraction
   simulation still meets all specs with < 10 % degradation.
4. LVS is clean (Netgen reports zero mismatches).
5. Every transistor operating point has been printed and verified — no device
   is accidentally in triode, cutoff, or deep weak inversion where the model
   is unreliable.

---

## 2. State of the Art — Where We Stand

### 2.1 Classic Bult & Wallinga (JSSC 1987)

The folded-cascode topology was formalized by Bult and Wallinga in their 1987
JSSC paper "A class of analog CMOS circuits based on the square-law
characteristic of an MOS transistor in saturation." This paper defined the
template that virtually every folded-cascode OTA since has followed: an NMOS
(or PMOS) input differential pair whose drain current is "folded" into a
complementary cascode output stage, achieving high output impedance (and
therefore high voltage gain) in a single stage without the bandwidth penalty
of a two-stage Miller-compensated design.

Key insight: the folded cascode achieves Av = gm1 * (ro_n_cascode || ro_p_cascode),
where the cascode stacking boosts the output impedance by a factor of roughly
gm*ro for each cascode device. In a reasonable process this gives 60-80 dB
from a single stage.

### 2.2 Peluso Ultra-Low-Power OTA (JSSC 1997)

Peluso et al. demonstrated an OTA in 0.5 um CMOS running from 1.5 V supply at
only 550 nA total current. They achieved 57 dB DC gain and 34 kHz UGB with a
5 pF load. This paper is important because it showed that subthreshold
operation of the input pair can deliver adequate gm/Id ratios (> 25 V^-1) to
hit audio-band UGB targets at nanoamp-level currents.

Relevance to us: our 1 uA budget is almost 2x Peluso's current, and sky130 at
130 nm has better intrinsic gain (gm*ro) than their 0.5 um process for the same
Vgs overdrive. We should comfortably exceed 57 dB.

### 2.3 Ferreira-Pinto et al. (TCAS-I 2004)

This work pushed the envelope further: 1 V supply, 120 nW total power, 62 dB
gain. The entire OTA operated in deep subthreshold. The penalty was bandwidth
(a few kHz UGB) and noise (subthreshold operation increases thermal noise
coefficient from 2/3 toward ~1 in weak inversion).

Relevance: we are NOT going this extreme. Our 1.8 V supply and 1 uA budget
put us comfortably in moderate inversion, which is the sweet spot for gain,
bandwidth, and noise simultaneously.

### 2.4 Toledo et al. Survey (2019)

Toledo published a comprehensive survey of sub-1V and ultra-low-power OTAs.
The key takeaway: in 130 nm CMOS, typical published results for folded-cascode
OTAs cluster around 60-80 dB gain, 50-200 kHz UGB, and 0.5-5 uA total current.
The figure of merit FOM = (GBW * CL) / Itotal typically ranges from 200 to
2000 MHz*pF/mA for single-stage designs.

Our target: GBW=50 kHz, CL=10 pF, Itotal=1 uA gives FOM = 500 MHz*pF/mA.
This is squarely in the middle of the published range — confirming that our
target is moderate and achievable. We are not claiming any record.

### 2.5 Honest Assessment

Our target of 65 dB gain / 50 kHz UGB / 1 uA is **unremarkable by 2025
standards**. Any competent analog designer should hit these numbers in sky130
on the first or second sizing iteration. The challenge is not in the nominal
performance but in:

- Achieving it across all 5 process corners (especially SS at -40 C)
- Keeping input-referred noise low enough for the vibration sensor front-end
- Ensuring the output swing is wide enough for 1 Vpp signals
- Making the layout compact enough that 20+ instances fit in the Gm-C filters

If the agent finds itself unable to meet these specs, the most likely cause is
incorrect biasing (devices accidentally in triode) or an error in the testbench
(measuring closed-loop instead of open-loop gain). The topology itself is
proven; the specs are well within its capability.

---

## 3. Circuit Topology

### 3.1 Why Folded Cascode

A two-stage Miller OTA would give more gain (> 80 dB easily) but requires a
compensation capacitor Cc that eats area and limits slew rate. A telescopic
cascode has the best noise and speed but severely limits output swing — with a
1.8 V supply we would lose ~0.6 V of swing. The folded cascode is the Goldilocks
topology: one stage (inherently stable, no Cc needed), reasonable output swing
(we lose only ~0.4 V per rail), and 60-70 dB gain with careful sizing.

### 3.2 Why NMOS Input Pair

In SKY130A:
- NMOS in moderate inversion: gm/Id ~ 18-22 V^-1, mu_n ~ 400 cm^2/Vs
- PMOS in moderate inversion: gm/Id ~ 14-18 V^-1, mu_p ~ 130 cm^2/Vs

The NMOS input pair gives roughly 1.5x better gm for the same bias current and
device area. Additionally, the SKY130 NMOS models are more thoroughly validated
in moderate inversion than the PMOS models (this is a known observation in the
open-source PDK community). The tradeoff is that NMOS input limits the input
common-mode range from below (need Vgs_tail + Vdsat_tail + Vgs_input above
ground), but with 1.8 V supply and moderate Vth (~0.4-0.5 V for NMOS in
sky130), we have plenty of headroom.

### 3.3 Full Transistor-Level Description

```
                       VDD (1.8V)
                        |
              +---------+---------+
              |                   |
            M12(P)             M13(P)
         (bias mirror)      (bias mirror)
              |                   |
              +---+         +-----+
              |   |         |     |
            M3(P) |       M4(P)   |
         (fold)   |    (fold)     |
              |   |         |     |
            M5(P) |       M6(P)   |
         (cascode)|    (cascode)  |
              |   |         |     |
              +---+----+----+-----+-----> Vout
                       |
              +--------+---------+
              |                  |
            M7(N)              M8(N)
         (cascode)          (cascode)
              |                  |
            M9(N)             M10(N)
         (current src)     (current src)
              |                  |
              +---------+--------+
                        |
                       VSS (GND)


         Input pair (connected at folding nodes):

                    M11(N)
                  (tail current)
                      |
              +-------+-------+
              |               |
            M1(N)           M2(N)
          (inp)            (inn)
              |               |
            Vinp            Vinn
```

### 3.4 Transistor Sizing Table

| Device | Type | W (um) | L (um) | Fingers | Multiplier | Role |
|--------|------|--------|--------|---------|------------|------|
| M1     | nfet_01v8 | 10 | 1.0 | 2 | 1 | Input diff pair (+) |
| M2     | nfet_01v8 | 10 | 1.0 | 2 | 1 | Input diff pair (-) |
| M3     | pfet_01v8 |  8 | 1.0 | 2 | 1 | PMOS fold transistor (+) |
| M4     | pfet_01v8 |  8 | 1.0 | 2 | 1 | PMOS fold transistor (-) |
| M5     | pfet_01v8 |  8 | 0.5 | 2 | 1 | PMOS cascode (+) |
| M6     | pfet_01v8 |  8 | 0.5 | 2 | 1 | PMOS cascode (-) |
| M7     | nfet_01v8 |  4 | 0.5 | 2 | 1 | NMOS cascode (+) |
| M8     | nfet_01v8 |  4 | 0.5 | 2 | 1 | NMOS cascode (-) |
| M9     | nfet_01v8 |  4 | 2.0 | 1 | 1 | NMOS current source (+) |
| M10    | nfet_01v8 |  4 | 2.0 | 1 | 1 | NMOS current source (-) |
| M11    | nfet_01v8 |  4 | 4.0 | 1 | 1 | Tail current source |
| M12    | pfet_01v8 |  8 | 2.0 | 1 | 1 | PMOS bias mirror (+) |
| M13    | pfet_01v8 |  8 | 2.0 | 1 | 1 | PMOS bias mirror (-) |

### 3.5 Sizing Rationale

**Input pair M1/M2 (W=10u, L=1u):**
The input pair dominates noise and sets the transconductance. W*L = 10 um^2
gives a large gate area to reduce 1/f noise. With L=1u, the pair operates in
moderate inversion at Id=250nA per side (half the tail current), giving
gm ~ Id * (gm/Id) ~ 250n * 20 = 5 uA/V. The UGB is then gm/(2*pi*CL) =
5u/(2*pi*10p) ~ 80 kHz — above our 50 kHz target, leaving margin for parasitics.

**PMOS fold M3/M4 (W=8u, L=1u):**
These carry the folded current. W=8u at L=1u keeps them in moderate inversion
at ~500nA. The length matches the input pair to aid symmetry. They must stay
in saturation: Vds > Vdsat. With Vdsat ~ 100-150 mV, this is easily achieved
in the folded configuration.

**PMOS cascode M5/M6 (W=8u, L=0.5u):**
Shorter L than the fold transistors because these are cascode devices — their
job is to boost output impedance, and the key parameter is gm (which benefits
from shorter L and higher current density). L=0.5u is the minimum we should use
for decent matching; going to L=0.15u would hurt matching and PSRR.

**NMOS cascode M7/M8 (W=4u, L=0.5u):**
Same rationale as M5/M6. Narrower because NMOS has higher mu and achieves
adequate gm with less width.

**NMOS current sources M9/M10 (W=4u, L=2u):**
Long L for high output impedance and good matching. These set the bias current
in the cascode branches. L=2u gives ro ~ 1/(lambda*Id) where lambda is small
due to the long channel.

**Tail current M11 (W=4u, L=4u):**
The longest device in the OTA. L=4u gives excellent output impedance for the
tail current source, which directly impacts CMRR. Vdsat is small (~80-100 mV)
at 500 nA, keeping the input CM range wide.

**PMOS bias mirrors M12/M13 (W=8u, L=2u):**
Mirror the bias current from Block 00 into the PMOS branches. L=2u for good
matching. These are not in the signal path so their gm is less critical, but
their ro contributes to PSRR.

### 3.6 Expected DC Operating Point (Hand Calculation)

Assuming Ibias = 500 nA from Block 00:

- M11 tail: Id = 500 nA, Vgs ~ 0.55 V (moderate inversion, Vth ~ 0.45 V)
- M1/M2 input: Id = 250 nA each, Vgs ~ 0.50 V, gm ~ 5 uA/V
- M3/M4 fold: Id ~ 500 nA each (fold + input current)
- M5/M6 cascode: Id ~ 500 nA each, same as M3/M4
- M7/M8 cascode: Id ~ 250 nA each
- M9/M10 current: Id ~ 250 nA each
- M12/M13 bias: Id ~ 500 nA each

Output voltage at quiescent: ~0.9 V (mid-rail)

Total current from VDD: M3+M4+M12+M13 = 500+500+500+500 = 2000 nA = 2 uA.
Wait — this exceeds our 1 uA target.

**Correction**: the folding current in M3/M4 should be set to carry only the
excess current beyond what M1/M2 provide. If the tail current is 500 nA
(250 nA per side), and M9/M10 are set to 250 nA each, then M3/M4 carry
500 nA - 250 nA = 250 nA each (from the fold) plus 250 nA from the input =
total 250 nA. Actually, let us be more precise:

In a folded cascode, M3/M4 carry current I_fold, and M9/M10 carry current
I_casc. The input pair injects Id_tail/2 = 250 nA into each fold node.
By KCL at the fold node: I_fold = I_casc + Id_input_half. So if I_fold = 500 nA,
then I_casc = 500 nA - 250 nA = 250 nA.

Total supply current = I_tail + 2*I_fold = 500 nA + 2*500 nA = 1.5 uA.
This is within our 2 uA limit. The bias mirrors M12/M13 do not draw additional
current — they ARE M3/M4 (or they mirror current into M3/M4). Let us clarify:

**Revised current budget:**
- Tail M11: 500 nA
- PMOS branch M3/M5 (and mirror M12): 500 nA
- PMOS branch M4/M6 (and mirror M13): 500 nA
- Total from VDD: 500 nA (tail) + 1000 nA (PMOS branches) = 1.5 uA
- This includes the bias mirror overhead (M12/M13 mirror current is part of
  the PMOS branch allocation)

**1.5 uA total — within the 2 uA spec.** Margin for bias generator overhead.

---

## 4. Bias Voltage Generation

The OTA needs four bias voltages:

| Bias node | Sets device | Typical value | Source |
|-----------|-------------|---------------|--------|
| Vbn       | M9/M10 gates (NMOS current source) | ~0.55 V | Block 00 mirror |
| Vbcn      | M7/M8 gates (NMOS cascode)         | ~0.75 V | Block 00 cascode |
| Vbp       | M3/M4 gates (PMOS fold/current)    | ~1.25 V | Block 00 mirror |
| Vbcp      | M5/M6 gates (PMOS cascode)         | ~1.05 V | Block 00 cascode |

For initial development, these will be set by ideal voltage sources. The agent
must sweep each bias voltage +/- 100 mV to verify the operating point is not
on a knife edge. If a 50 mV shift in any bias voltage causes a device to leave
saturation, the sizing is too aggressive and must be relaxed.

---

## 5. PASS/FAIL Criteria

These criteria are **strict**. Every line must show PASS for the block to be
considered done. "Close enough" is not acceptable — if a spec is missed by 1 dB,
resize and re-simulate.

### 5.1 AC Performance (CL = 10 pF)

| Parameter | Min | Target | Max | Unit | Testbench |
|-----------|-----|--------|-----|------|-----------|
| DC gain | 60 | 65 | — | dB | tb_ota_ac |
| Unity-gain bandwidth | 30 | 50 | 150 | kHz | tb_ota_ac |
| Phase margin | 55 | 65 | — | degrees | tb_ota_ac |
| Gain margin | 10 | 15 | — | dB | tb_ota_ac |

### 5.2 Noise

| Parameter | Min | Target | Max | Unit | Testbench |
|-----------|-----|--------|-----|------|-----------|
| Input noise @ 1 kHz | — | 150 | 200 | nV/rtHz | tb_ota_noise |
| Input noise @ 10 kHz | — | 70 | 100 | nV/rtHz | tb_ota_noise |

### 5.3 Transient

| Parameter | Min | Target | Max | Unit | Testbench |
|-----------|-----|--------|-----|------|-----------|
| Slew rate (CL=10pF) | 10 | 50 | — | mV/us | tb_ota_tran |

### 5.4 DC and Large Signal

| Parameter | Min | Target | Max | Unit | Testbench |
|-----------|-----|--------|-----|------|-----------|
| Output swing (1% THD) | 1.0 | 1.2 | — | Vpp | tb_ota_dc |
| Input CM range | 0.6 | 0.8 | — | V | tb_ota_dc |

### 5.5 Rejection

| Parameter | Min | Target | Max | Unit | Testbench |
|-----------|-----|--------|-----|------|-----------|
| CMRR at DC | 60 | 70 | — | dB | tb_ota_cmrr |
| PSRR at 1 kHz | 50 | 60 | — | dB | tb_ota_psrr |

### 5.6 Power

| Parameter | Min | Target | Max | Unit | Testbench |
|-----------|-----|--------|-----|------|-----------|
| Total current | — | 1.5 | 2.0 | uA | tb_ota_dc |

### 5.7 Corner and Temperature

| Condition | Requirement |
|-----------|-------------|
| TT/SS/FF/SF/FS at 27C | ALL specs in 5.1-5.6 must PASS |
| TT at -40C/27C/85C | Gain >= 55 dB, UGB in 20-200 kHz range |
| Monte Carlo 200 runs TT 27C | Input offset < 10 mV (3-sigma) |

---

## 6. Simulation Testbenches — Detailed Specification

All testbenches use the following common header:

```spice
* Common header for all OTA testbenches
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
.include "ota_foldcasc.spice"

.param vdd_val = 1.8
.param ibias_val = 500n
.param cl_val = 10p

Vdd vdd 0 dc {vdd_val}
Vss vss 0 dc 0
Ibias vbn 0 dc {ibias_val}

* Instantiate OTA
Xota vinp vinn vout vdd vss vbn vbcn vbp vbcp ota_foldcasc
CL vout 0 {cl_val}
```

### 6.1 TB01: AC Open-Loop Analysis (`tb_ota_ac.spice`)

**Purpose:** Measure DC gain, unity-gain bandwidth, phase margin, gain margin.

**Method:**
- Apply DC bias at mid-rail to both inputs (Vcm = 0.9 V)
- Apply AC stimulus of 1 V to the positive input
- Break the feedback loop using a large inductor (L_break = 1GH) or use the
  Middlebrook method if STB analysis is available in ngspice
- Run: `.ac dec 100 1 100Meg`

**Measurements:**
```spice
.meas ac gain_db MAX vdb(vout)
.meas ac ugb WHEN vdb(vout)=0
.meas ac phase_at_ugb FIND vp(vout) WHEN vdb(vout)=0
.meas ac pm PARAM='phase_at_ugb + 180'
.meas ac freq_at_neg180 WHEN vp(vout)=-180
.meas ac gain_at_neg180 FIND vdb(vout) WHEN vp(vout)=-180
.meas ac gm_db PARAM='-gain_at_neg180'
```

**Expected results:** Gain ~ 65 dB, UGB ~ 50-80 kHz, PM ~ 60-70 deg.

### 6.2 TB02: DC Sweep (`tb_ota_dc.spice`)

**Purpose:** Measure output swing, input-output transfer characteristic, linearity.

**Method:**
- Configure OTA in unity-gain feedback (vout connected to vinn)
- Sweep vinp from 0 to 1.8 V in 1 mV steps
- Measure vout vs vinp

**Measurements:**
```spice
.dc Vinp 0 1.8 0.001
.meas dc v_out_max MAX v(vout)
.meas dc v_out_min MIN v(vout)
.meas dc swing PARAM='v_out_max - v_out_min'
```

Also measure the derivative d(Vout)/d(Vinp) — it should be ~1.0 in the linear
region. The range where it stays within 1% of 1.0 defines the input CM range.

### 6.3 TB03: Transient Step Response (`tb_ota_tran.spice`)

**Purpose:** Measure slew rate, settling time to 0.1%.

**Method:**
- Configure OTA in unity-gain feedback
- Apply a 100 mV step at t=10us on the positive input
- Simulate for 100 us with max timestep of 10 ns

**Measurements:**
```spice
.tran 10n 100u
.meas tran sr_pos DERIV v(vout) WHEN v(vout)='0.9+0.045' RISE=1
.meas tran sr_neg DERIV v(vout) WHEN v(vout)='0.9+0.045' FALL=1
.meas tran t_settle_01 WHEN v(vout)='0.9+0.0999' RISE=1
```

Slew rate should be > 10 mV/us. For 500 nA tail current and 10 pF load:
SR = Itail / CL = 500n / 10p = 50 mV/us (theoretical). Should be close.

### 6.4 TB04: Noise Analysis (`tb_ota_noise.spice`)

**Purpose:** Measure input-referred noise spectral density and integrated noise.

**Method:**
- Same bias as AC testbench
- Run: `.noise V(vout) Vinp dec 100 1 1Meg`
- The result is output-referred; divide by gain to get input-referred,
  or use ngspice's built-in input-referred noise output

**Measurements:**
```spice
.noise V(vout) Vinp dec 100 1 1Meg
.print noise inoise_spectrum
.meas noise noise_1k FIND inoise_total AT=1000
.meas noise noise_10k FIND inoise_total AT=10000
```

**Expected:** At 1 kHz, dominated by 1/f noise of input pair. With W*L = 10 um^2,
the 1/f noise coefficient Kf for sky130 NMOS gives roughly 100-180 nV/rtHz.
At 10 kHz, thermal noise dominates: Sn = (8/3)*kT/gm * (1 + gm3/gm1) where
gm3/gm1 is the fold transistor contribution. With gm1 ~ 5 uA/V, thermal floor
is ~ 40-80 nV/rtHz.

### 6.5 TB05: PSRR (`tb_ota_psrr.spice`)

**Purpose:** Measure power supply rejection ratio.

**Method:**
- Ground both inputs at Vcm = 0.9 V (no differential input)
- Apply AC stimulus of 1 V on VDD
- Measure AC output voltage
- PSRR = 20*log10(Av_from_vdd / Av_from_input) or equivalently measure the
  gain from VDD to output and subtract from the open-loop gain

**Measurements:**
```spice
.ac dec 100 1 100Meg
.meas ac psrr_dc FIND vdb(vout) AT=1
.meas ac psrr_1k FIND vdb(vout) AT=1000
```

Negate and add DC gain to get PSRR in dB. Target: > 50 dB at 1 kHz.

### 6.6 TB06: CMRR (`tb_ota_cmrr.spice`)

**Purpose:** Measure common-mode rejection ratio.

**Method:**
- Tie both inputs together
- Apply AC stimulus of 1 V on the common input
- Measure AC output voltage
- CMRR = Adm / Acm (open-loop differential gain / common-mode gain)

**Measurements:**
```spice
.ac dec 100 1 100Meg
.meas ac acm_dc FIND vdb(vout) AT=1
.meas ac cmrr_dc PARAM='gain_db - acm_dc'
```

Target: > 60 dB at DC. Limited by tail current source output impedance and
matching (in simulation with ideal matching, CMRR will appear very high;
Monte Carlo gives realistic values).

### 6.7 TB07: Operating Point Verification (`tb_ota_op.spice`)

**Purpose:** Print Vgs, Vth, Vds, Id, gm, gds, and operating region for ALL
13 transistors. This is the most important testbench — it catches 90% of
design errors.

**Method:**
```spice
.op
.save all
.control
  run
  print @m.xota.m1[vgs] @m.xota.m1[vth] @m.xota.m1[vds]
  print @m.xota.m1[id] @m.xota.m1[gm] @m.xota.m1[gds]
  print @m.xota.m1[vdsat] @m.xota.m1[region]
  * ... repeat for all 13 transistors ...
  quit
.endc
```

**Verification rules (MANDATORY — no exceptions):**

| Check | Condition | Why |
|-------|-----------|-----|
| PMOS saturation | Vsg - abs(Vth) > 150 mV | Sky130 PMOS models unreliable below this |
| NMOS signal path saturation | Vgs - Vth > 50 mV | Need some inversion for gm |
| Cascode headroom | Vds > Vdsat + 50 mV | Ensure saturation with margin |
| Tail current accuracy | abs(Id_M11 - 500nA) < 50nA | Bias is correct |
| Current balance | abs(Id_M1 - Id_M2) < 10nA | Matched at operating point |
| Output voltage | 0.6V < Vout < 1.2V | Roughly mid-rail |

If ANY of these checks fail, the agent MUST resize the offending transistor(s)
and re-simulate. Do not proceed to other testbenches until the operating point
is clean.

### 6.8 TB08: 5-Corner Sweep (`tb_ota_corners.spice`)

**Purpose:** Verify AC specs across all process corners.

**Method:**
Run tb_ota_ac at each of: TT, SS, FF, SF, FS.

```spice
.lib "/path/to/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
* ... run AC sim, measure gain/UGB/PM ...
* Then repeat with ss, ff, sf, fs
```

In ngspice this is best done with a shell script that swaps the .lib line and
reruns, or using `.alter` blocks if supported.

**Expected behavior across corners:**

| Corner | Gain change | UGB change | PM change |
|--------|-------------|------------|-----------|
| SS | -5 to -8 dB | -30 to -40% | +5 to +10 deg |
| FF | +3 to +5 dB | +20 to +30% | -5 to -10 deg |
| SF | -2 to +2 dB | -10 to +10% | -3 to +3 deg |
| FS | -2 to +2 dB | -10 to +10% | -3 to +3 deg |

The critical corner is SS: gain drops and UGB drops. If gain at SS < 60 dB,
increase L of cascode devices. If UGB at SS < 30 kHz, increase input pair W
or increase bias current (with permission from power budget).

### 6.9 TB09: Temperature Sweep (`tb_ota_corners_temp.spice`)

**Purpose:** Verify performance at -40C, 27C, and 85C.

**Method:**
Run tb_ota_ac at TT corner with `.temp -40`, `.temp 27`, `.temp 85`.

**Expected:**
- At -40C: threshold voltages increase, mobility increases. Gain may increase
  slightly, UGB may decrease slightly. Watch for tail current accuracy (if
  biased by mirror, the reference current tracks temperature).
- At 85C: thresholds decrease, mobility decreases. gm/Id increases but gm
  may decrease due to lower mobility. UGB and gain can go either way depending
  on the bias scheme.

**PASS criteria:** Gain >= 55 dB and UGB in 20-200 kHz at all three temperatures.

### 6.10 TB10: Monte Carlo (`tb_ota_mc.spice`)

**Purpose:** Measure statistical distribution of input offset voltage.

**Method:**
- Configure OTA in unity-gain feedback with Vinp = 0.9 V
- Run 200 Monte Carlo iterations with mismatch parameters enabled
- Measure Vout - 0.9 V for each iteration (this is the input offset)

```spice
.param mc_run = 0
.control
  let offset = vector(200)
  let idx = 0
  repeat 200
    set mc_run = $&idx
    reset
    run
    let offset[idx] = v(vout) - 0.9
    let idx = idx + 1
  end
  print mean(offset) stddev(offset)
  * 3-sigma should be < 10 mV
.endc
```

Note: SKY130 Monte Carlo models include both inter-die (global) and intra-die
(mismatch) variations. The mismatch parameters are in the model files as
`delvto` and similar. Verify that the `.lib` call includes the MC models.

**PASS criteria:** 3-sigma offset < 10 mV. If offset is too high, increase
the area (W*L) of the input pair. Offset scales as 1/sqrt(W*L) — doubling
the area reduces offset by ~1.4x.

---

## 7. Operating Point Verification — The Cardinal Rule

This section exists because operating point errors are the #1 cause of analog
simulation mismatch with silicon. The agent MUST follow this procedure after
every simulation change.

### 7.1 Procedure

1. Run `.op` simulation
2. For each of the 13 transistors, extract: Vgs, Vth, Vds, Vdsat, Id, gm, gds, region
3. Compute Vov = Vgs - Vth (NMOS) or Vsg - |Vth| (PMOS)
4. Check ALL of the following:

**For PMOS devices (M3, M4, M5, M6, M12, M13):**
- Region must be "saturation" (region = 2 in ngspice)
- Vov = Vsg - |Vth| must be > 150 mV
- If Vov < 150 mV, the BSIM model for sky130 PMOS may give unreliable gm and
  gds. Increase W to push the device further into moderate/strong inversion,
  or increase the bias current through the device.

**For signal-path NMOS devices (M1, M2, M7, M8):**
- Region must be "saturation" (region = 2)
- Vov = Vgs - Vth must be > 50 mV
- M1/M2 can operate in weak-to-moderate inversion (Vov ~ 50-100 mV) for
  maximum gm/Id ratio, but going below 50 mV risks model inaccuracy

**For current-source NMOS devices (M9, M10, M11):**
- Region must be "saturation" (region = 2)
- Vds > Vdsat + 50 mV (headroom for keeping saturation across corners)
- These devices can operate anywhere from weak to strong inversion; the key
  constraint is saturation headroom, not Vov

**For all cascode devices (M5, M6, M7, M8):**
- Vds > Vdsat + 50 mV (absolute minimum)
- Preferably Vds > Vdsat + 100 mV for margin across corners
- If this is not met, the cascode device provides no impedance boost and the
  gain drops precipitously

### 7.2 What to Do When a Device Violates

| Violation | Root cause | Fix |
|-----------|-----------|-----|
| PMOS Vov < 150 mV | Device too wide for its current, or current too low | Decrease W or increase L to push Vgs higher |
| NMOS Vov < 50 mV | Device in deep subthreshold | Decrease W or increase current |
| Cascode Vds < Vdsat + 50 mV | Stacking too many devices, not enough voltage headroom | Decrease L of cascode device (reduces Vdsat) or adjust bias voltages |
| Device in triode (region = 1) | Vds too low, likely a biasing error | Check bias voltage generation, may need to adjust Vbcn or Vbcp |
| Device in cutoff (region = 3) | Vgs < Vth, no current flowing | Check connectivity, bias source, W/L ratio |

### 7.3 Operating Point Reporting Format

After every `.op` run, the agent must produce a table like this:

```
Device  | Type | W/L     | Id(nA) | Vgs(V) | Vth(V) | Vov(mV) | Vds(V) | Vdsat(V) | gm(uS) | Region | Status
--------|------|---------|--------|--------|--------|---------|--------|----------|---------|--------|-------
M1      | NMOS | 10/1    | 250    | 0.50   | 0.45   | +50     | 0.65   | 0.08     | 5.0     | Sat    | OK
M2      | NMOS | 10/1    | 250    | 0.50   | 0.45   | +50     | 0.65   | 0.08     | 5.0     | Sat    | OK
...
```

Every row must end with OK or FAIL. If any row is FAIL, do not proceed.

---

## 8. Layout Guidelines

### 8.1 Floorplan

```
+--------------------------------------------------+
|                  Guard Ring (N+)                   |
|  +----------------------------------------------+|
|  |  M12/M13 (PMOS bias)    |  Bias routing      ||
|  |__________________________|____________________||
|  |                                                ||
|  |     M3  M5  |  M6  M4    <- PMOS loads        ||
|  |     (cascode + fold)     |  matched pair       ||
|  |______________________________ _________________||
|  |                                                ||
|  |        M1   M2           <- Input pair         ||
|  |      (ABBA centroid)     |  CRITICAL match     ||
|  |______________________________ _________________||
|  |                                                ||
|  |     M9  M7  |  M8  M10   <- NMOS loads        ||
|  |     (cascode + current)  |  matched pair       ||
|  |______________________________ _________________||
|  |                                                ||
|  |          M11              <- Tail current      ||
|  |      (isolated)          |                     ||
|  +----------------------------------------------+|
|                  Guard Ring (P+)                   |
+--------------------------------------------------+
```

### 8.2 Input Pair Matching (M1/M2) — CRITICAL

The input pair M1/M2 determines offset and CMRR. Layout rules:

1. **Common centroid, ABBA interleaving:** Place M1 and M2 fingers as
   A-B-B-A, where A = M1 finger and B = M2 finger. With 2 fingers each,
   this gives exactly the 4-finger ABBA pattern.
2. **Identical orientation:** Both transistors must have the same gate
   orientation (e.g., both with gates running vertically).
3. **Dummy devices:** Place dummy transistors on both ends of the array to
   shield the active devices from edge effects (etch non-uniformity at the
   array boundary).
4. **Shared source:** The source connections of M1 and M2 connect to M11's
   drain — route this as a symmetric tree from the center.
5. **Minimal drain routing asymmetry:** The drain of M1 goes to the M3/M5
   branch and the drain of M2 goes to the M4/M6 branch. Route these
   symmetrically — same metal layer, same wire length, same number of vias.

### 8.3 PMOS Load Matching (M3/M4 and M5/M6)

1. **Common centroid:** M3/M4 as A-B-B-A, M5/M6 as A-B-B-A.
2. **Same N-well:** All PMOS devices in a single N-well to avoid well
   potential variations.
3. **Close to input pair:** Minimize wire length from input pair drains to
   fold node — parasitic capacitance here degrades phase margin.

### 8.4 NMOS Cascode and Current Sources (M7-M10)

1. **M7/M8 matched:** Common centroid like the input pair.
2. **M9/M10 matched:** These set the current — matching matters.
3. **Same P-sub potential:** All NMOS share the P-substrate; use substrate
   contacts every 15 um to keep the body potential uniform.

### 8.5 Tail Current (M11)

1. **Isolated:** Place M11 away from the signal-path devices. Its switching
   noise (from common-mode input variations) should not couple into the
   differential pair.
2. **Large area:** With W=4u, L=4u, this is a big device. Use multiple
   fingers if needed for better current distribution.

### 8.6 Guard Rings

1. **Full guard ring around the entire OTA:** N+ ring tied to VDD and P+ ring
   tied to VSS. This provides latch-up protection and isolates the OTA from
   substrate noise injected by digital circuits.
2. **Individual guard rings optional:** Around the input pair for extra
   isolation (recommended if the OTA will be placed near a switched-capacitor
   circuit or clock buffer).

### 8.7 Routing Rules

1. **Differential signals:** Route on the same metal layer, same width, same
   length. If one wire must jog, add a compensating jog to the other.
2. **Bias lines:** Route on Metal 2 or higher to avoid coupling to Metal 1
   signal routes.
3. **VDD/VSS:** Wide traces (minimum 1 um) running horizontally across the
   top and bottom of the cell. Multiple vias to lower metals at every device
   connection.
4. **Output node:** The output is the highest-impedance node. Keep the wire
   short and shield it with grounded metal on adjacent layers if possible.
5. **No floating metal:** Every piece of metal must be connected. Floating
   metal causes antenna rule violations and can couple noise.

---

## 9. Troubleshooting Guide — When Stuck

### 9.1 Gain is Low (< 60 dB)

**Likely causes:**
1. Cascode devices not providing enough impedance boost — check that M5/M6
   and M7/M8 are in saturation with adequate Vds headroom.
2. Cascode L is too short — gm*ro of the cascode is proportional to L.
   Try increasing L of M5/M6 from 0.5u to 1u or M7/M8 from 0.5u to 1u.
3. Output resistance of M9/M10 is too low — increase L of M9/M10 from 2u
   to 4u.
4. Device is accidentally in triode — run `.op` and check region flags.

**Systematic approach:**
- Compute Rout = (gm5 * ro5 * ro3) || (gm7 * ro7 * ro9)
- Av = gm1 * Rout
- Identify which side (PMOS or NMOS) has lower impedance and fix that one.

### 9.2 UGB is Low (< 30 kHz)

**Likely causes:**
1. Input pair gm is too low — either W is too small or bias current is too low.
2. Parasitic capacitance at the output node is large (bad layout, long wires).
3. Load capacitance is larger than expected.

**Fix:** UGB = gm1 / (2*pi*CL). To increase UGB:
- Increase W of input pair (increases gm at same current)
- Increase bias current (increases gm, but costs power)
- Reduce CL if the system allows it

### 9.3 Phase Margin is Low (< 55 deg)

**Likely causes:**
1. Non-dominant pole is too close to UGB. The non-dominant pole is at the
   folding nodes: f_p2 ~ gm_cascode / (2*pi*C_fold). Large parasitic
   capacitance at the fold node pushes p2 down.
2. A zero from gate-drain capacitance of the cascode devices.

**Fix:**
- Reduce parasitic at fold nodes: shorter wires, smaller cascode device widths
- Increase gm of cascode devices: increase their W or current
- As last resort, add Miller compensation (Cc between output and a
  low-impedance node), but this converts the design into a quasi-two-stage
  and reduces slew rate

### 9.4 Noise is Too High

**Likely causes:**
1. Input pair too small — 1/f noise scales as 1/(W*L*Cox*f). Increase W*L.
2. PMOS fold transistor noise contribution — gm3/gm1 ratio is too high.
   Reduce gm3 by making M3/M4 longer (increases Vov, reduces gm at same Id).

**Fix:**
- Increase W*L of input pair. Going from W=10u L=1u to W=20u L=1u halves
  the 1/f noise power (reduces noise voltage by 1.4x).
- Decrease gm of fold transistors: increase their L.
- Check that the noise simulation is input-referred, not output-referred.

### 9.5 Output Swing is Too Narrow

**Likely causes:**
1. Cascode stacking consumes too much headroom.
2. Vdsat of M5/M6 or M7/M8 is too large (devices too narrow or too much current).

**Fix:**
- Maximum output voltage: VDD - Vdsat_M3 - Vdsat_M5 = 1.8 - 0.15 - 0.10 = 1.55 V
- Minimum output voltage: Vdsat_M9 + Vdsat_M7 = 0.10 + 0.10 = 0.20 V
- Theoretical swing: 1.55 - 0.20 = 1.35 V, which is > 1.0 Vpp target.
- If swing is less, check that Vdsat values are correct. Reduce by making
  devices wider (spreads current over more W, reducing Vov/Vdsat).

### 9.6 Settling Time is Too Long

**Likely causes:**
1. Slew rate limited: SR = Itail / CL. With 500nA and 10pF, SR = 50 mV/us.
   For a 100 mV step, slewing takes ~2 us. Then linear settling takes
   several time constants tau = CL / gm ~ 10p / 5u = 2 us. Total settling
   ~ 10-15 us for 0.1%.
2. If settling is much longer than expected, look for a slow parasitic pole
   or ringing (low phase margin).

**Fix:**
- Increase tail current to improve slew rate
- Improve phase margin to reduce ringing during linear settling

### 9.7 Monte Carlo Offset is Too High

**Likely causes:**
1. Input pair area too small — offset is proportional to 1/sqrt(W*L).
2. Threshold voltage mismatch parameter (AVT) for sky130 NMOS is typically
   ~5 mV*um. For W=10u, L=1u: sigma_Vth = AVT / sqrt(W*L) = 5m/sqrt(10)
   ~ 1.6 mV per transistor. Differential pair offset sigma = 1.6*sqrt(2) ~
   2.2 mV. 3-sigma ~ 6.6 mV — within our 10 mV target.

**Fix:** If offset is too high, increase W*L of the input pair. This also
improves noise, so it is a double win.

---

## 10. Integration Notes

### 10.1 Interface to Block 00 (Bias Generator)

The OTA receives four bias voltages from Block 00:
- Vbn: gate voltage for NMOS current sources (M9/M10/M11)
- Vbcn: gate voltage for NMOS cascode (M7/M8)
- Vbp: gate voltage for PMOS current sources (M3/M4 or M12/M13)
- Vbcp: gate voltage for PMOS cascode (M5/M6)

For initial development, replace these with ideal voltage sources set to the
values from the operating point simulation. Once Block 00 is designed, replace
the ideal sources with the actual bias generator outputs and re-verify all
specs.

### 10.2 Interface to Block 02+ (Gm-C Filters)

The OTA will be used as a transconductor in Gm-C filter stages. The filter
uses the OTA's gm to set the frequency: f = gm / (2*pi*C). The OTA must have:
- Predictable gm (use moderate inversion where gm/Id is well-controlled)
- Linear gm over the signal swing (key for low distortion)
- Frequency-independent gm up to 5x the filter cutoff frequency

The Gm-C interface is: Vinp/Vinn are the filter input, and the output current
(Iout = gm * Vdiff) flows into the integration capacitor. The OTA output
node connects to the capacitor, and the voltage on that capacitor is the filter
state variable.

### 10.3 Reusability

This OTA subcircuit must be parameterizable:
- The bias current can be scaled by changing the mirror ratio in Block 00
- For higher-bandwidth filters, multiple OTAs can be paralleled (doubling gm)
- For lower-noise applications, the input pair can be upsized in a variant

The agent should write the subcircuit with `.param` statements for all device
sizes so that variants can be created by overriding parameters at instantiation.

---

## 11. Checklist Before Declaring Block 01 Complete

```
[ ] Operating point of all 13 transistors verified (Section 7)
[ ] AC gain >= 60 dB across all corners
[ ] UGB in 30-150 kHz across all corners
[ ] PM >= 55 degrees across all corners
[ ] Gain margin >= 10 dB
[ ] Slew rate >= 10 mV/us
[ ] Input noise at 1 kHz <= 200 nV/rtHz
[ ] Input noise at 10 kHz <= 100 nV/rtHz
[ ] CMRR >= 60 dB at DC
[ ] PSRR >= 50 dB at 1 kHz
[ ] Output swing >= 1.0 Vpp at 1% THD
[ ] Total current <= 2 uA
[ ] Input CM range >= 0.6 V
[ ] Temperature sweep passes (-40, 27, 85 C)
[ ] Monte Carlo 200 runs: offset 3-sigma < 10 mV
[ ] Layout DRC clean
[ ] LVS clean (Netgen zero mismatches)
[ ] Post-PEX simulation meets all specs with < 10% degradation
[ ] results.md written with all numbers and PASS/FAIL flags
[ ] Subcircuit netlist is clean, commented, and reusable
```

---

## 12. References

1. K. Bult and G. J. G. M. Geelen, "A fast-settling CMOS op amp for SC
   circuits with 90-dB DC gain," IEEE JSSC, vol. 25, no. 6, Dec. 1990.
   (The original folded-cascode paper is Bult & Wallinga, JSSC 1987.)
2. V. Peluso, P. Vancorenland, A. Marques, M. Steyaert, and W. Sansen,
   "A 900-mV low-power delta-sigma A/D converter with 77-dB dynamic range,"
   IEEE JSSC, vol. 33, no. 12, Dec. 1998. (Peluso's ultra-low-power OTA
   work was published in several papers around 1997-1998.)
3. P. M. Ferreira and S. Pinto, "A 1-V 120-nW folded-cascode OTA for
   neural signal acquisition," TCAS-I, 2004.
4. L. H. C. Toledo et al., "A review of ultra-low-voltage and ultra-low-power
   OTA topologies for analog signal processing," Journal of Integrated
   Circuits and Systems, 2019.
5. SkyWater SKY130 PDK documentation: https://skywater-pdk.readthedocs.io/
6. B. Razavi, "Design of Analog CMOS Integrated Circuits," 2nd ed.,
   McGraw-Hill, 2017. Chapters 9 (cascode stages) and 10 (differential
   amplifiers).
7. P. Allen and D. Holberg, "CMOS Analog Circuit Design," 3rd ed., Oxford
   University Press, 2012. Chapter 6 (folded-cascode OTA design procedure).

---

*End of Block 01 program. Total estimated design time: 2-4 hours for schematic
and simulation, 4-8 hours for layout and post-PEX verification.*
