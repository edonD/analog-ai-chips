# Block 00: Bias Generator — Program

## 1. Mission

Design a beta-multiplier self-biased current reference producing **Iref = 500 nA** on the
SkyWater SKY130A process. The circuit must start up reliably in every process corner,
operate from a 1.8 V nominal supply, and achieve a temperature coefficient below
150 ppm/C from -40 C to +85 C. This block is the root of the analog signal chain:
every other block in the VibroSense design depends on it, so robustness is paramount.

Target supply: **VDD = 1.8 V** (valid range 1.6 V to 2.0 V).

---

## 2. State of the Art

Before designing, we acknowledge what the literature has achieved so that we can
honestly evaluate our own result.

### 2.1 Banba Bandgap Reference (JSSC 1999)

Banba's architecture produces a 1.2 V voltage reference with ~30 ppm/C temperature
coefficient at 3 uW total power. It uses resistor-ratio-based PTAT and CTAT summation.
This is the gold standard for voltage references but is overkill for a simple current
reference — it requires two matched resistor types and careful layout. Power consumption
is acceptable but the area is significant due to the resistors.

### 2.2 Camacho-Galeano Beta-Multiplier (TCAS-II 2005)

Camacho-Galeano demonstrated a beta-multiplier current reference producing 170 nA with
a temperature coefficient of 36 ppm/C. The key insight was biasing the NMOS pair at the
boundary between weak and moderate inversion, where the PTAT behavior of mobility
partially cancels the CTAT behavior of threshold voltage. This is the most directly
relevant prior work to our design. Achieving 36 ppm/C required careful optimization
of the W/L ratio K between the two NMOS devices and the resistor value.

### 2.3 Vittoz Self-Biased Current Reference

Eric Vittoz's treatment in Chapter 4 of "Analog VLSI" (later expanded in "Low-Power
Crystal and MEMS Oscillators") provides the theoretical foundation. The beta-multiplier
exploits the square-law (strong inversion) or exponential (weak inversion) relationship
between drain current and gate-source voltage. When two transistors of different W/L
share the same Vgs but carry the same current, the current is set by the resistance
and the ratio K. In strong inversion:

    Iref = (1 / R^2) * (2 / (mu_n * Cox)) * (1 - 1/sqrt(K))^2

In weak inversion (subthreshold), the relationship changes to:

    Iref = (n * Vt / R) * ln(K)

where n is the subthreshold slope factor and Vt = kT/q. Our target of 500 nA at the
chosen sizing lands us in moderate inversion, which is harder to model analytically
but simulatable.

### 2.4 Modern Ultra-Low-Power References

Recent publications (2020-2025) have demonstrated sub-100 nW current references using
subthreshold operation and native NMOS devices. These achieve remarkable TC values
(10-20 ppm/C) but universally require one-time trimming or calibration. Since the
VibroSense system targets a self-contained analog front-end without trimming
infrastructure, we do not pursue this path.

### 2.5 Honest Assessment

Our target of <150 ppm/C is modest compared to state-of-the-art (10-30 ppm/C). This is
a deliberate choice: on SKY130, the available resistor options (polysilicon high-res)
have their own TC of roughly 1000-2000 ppm/C, and the SPICE models for PMOS devices
in subthreshold are known to have accuracy issues. Achieving <50 ppm/C would require
PTAT+CTAT compensation with two resistor types, which SKY130 does support
(diffusion + poly), but at significant area cost. We may iterate to add curvature
correction if the initial design exceeds 150 ppm/C.

---

## 3. Circuit Topology

### 3.1 Core: Beta-Multiplier

The beta-multiplier is a positive-feedback current mirror that locks onto a non-zero
operating point determined by a resistor and a transistor size ratio.

```
        VDD
         |
    +----+----+
    |         |
   M3        M4          PMOS current mirror (1:1)
   (P)       (P)         W=4u L=4u each
    |         |
    +--+--+   +---> Iref output (to other blocks)
       |      |
      M1     M2          NMOS pair (1:K, K=4)
      (N)    (N)
       |      |
       |     R1           2 Mohm poly resistor
       |      |
      GND    GND
```

**Operating principle:**
- M3 and M4 form a 1:1 PMOS mirror, forcing Id(M1) = Id(M2) = Iref.
- M1 is diode-connected (gate = drain), so Vgs1 is set by Iref and M1's W/L.
- M2 has W/L = K times that of M1 (K=4). For the same current, Vgs2 < Vgs1.
- The voltage difference Vgs1 - Vgs2 drops across R1.
- This creates a self-consistent equation that fixes Iref.

In strong inversion:

    Vgs1 - Vgs2 = Iref * R1
    sqrt(2*Iref / (mu*Cox*(W/L)_1)) - sqrt(2*Iref / (mu*Cox*(W/L)_2)) = Iref * R1

Since (W/L)_2 = K * (W/L)_1:

    Iref = (1/R1^2) * (2 / (mu*Cox*(W/L)_1)) * (1 - 1/sqrt(K))^2

### 3.2 Startup Circuit

The beta-multiplier has two stable states: the desired operating point and a
degenerate zero-current state where all transistors are off. A startup circuit
is mandatory.

```
        VDD
         |
        M5        PMOS (optional cascode, also used for startup sensing)
        (P)       W=4u L=2u
         |
         +----+
              |
             M6        NMOS startup device
             (N)       W=0.5u L=0.5u
              |
             GND

    C_startup: 100 fF MIM cap from gate of M6 to VDD
```

**Startup sequence:**
1. At power-on, VDD ramps from 0 V. All nodes are at 0 V.
2. C_startup couples the rising VDD edge to the gate of M6, turning M6 on transiently.
3. M6 pulls current from the M3/M4 mirror drain node, injecting current into the loop.
4. Once the loop settles at the desired operating point, the gate of M6 is pulled
   low by the established bias voltages, and M6 turns off permanently.
5. M6 off means the startup circuit has zero steady-state power overhead.

**Why not a simpler startup?** A resistive pullup to VDD would work but adds DC power.
The capacitive startup is cleaner but must be verified across all corners and
temperature — the coupling may be too weak in slow corners with low VDD ramp rates.

### 3.3 Device List

| Device | Type | W (um) | L (um) | Multiplier | Role |
|--------|------|--------|--------|------------|------|
| M1 | sky130_fd_pr__nfet_01v8 | 2 | 4 | 1 | Diode-connected NMOS |
| M2 | sky130_fd_pr__nfet_01v8 | 8 | 4 | 1 | Mirror NMOS (K=4) |
| M3 | sky130_fd_pr__pfet_01v8 | 4 | 4 | 1 | PMOS mirror input |
| M4 | sky130_fd_pr__pfet_01v8 | 4 | 4 | 1 | PMOS mirror output |
| M5 | sky130_fd_pr__pfet_01v8 | 4 | 2 | 1 | PMOS cascode (optional) |
| M6 | sky130_fd_pr__nfet_01v8 | 0.5 | 0.5 | 1 | Startup NMOS |
| M7 | sky130_fd_pr__pfet_01v8 | 4 | 4 | 1 | Output mirror copy 1 (spare) |
| M8 | sky130_fd_pr__pfet_01v8 | 4 | 4 | 1 | Output mirror copy 2 (spare) |
| R1 | sky130_fd_pr__res_xhigh_po | — | — | 1000 sq | 2 Mohm resistor |
| C_startup | sky130_fd_pr__cap_mim_m3_1 | — | — | 1 | 100 fF MIM cap |

**Note on R1:** The sky130_fd_pr__res_xhigh_po has a sheet resistance of approximately
2000 ohm/sq. To achieve 2 Mohm, we need 1000 squares. At a width of 2 um, the
resistor length is 2000 um = 2 mm. This is large and will dominate the block area.
In layout, it must be routed as a serpentine.

**Note on M7/M8:** These are additional output mirror copies that distribute Iref to
downstream blocks. They are identical to M4 and source matched 500 nA currents.
If not needed in initial testing, their drains can be left floating or tied to VDD
through a load.

---

## 4. Transistor Sizing Rationale

### 4.1 Why L=4u for M1-M4

Long channel lengths serve three purposes:
1. **High output resistance:** ro = VA*L / Id. At L=4u, the Early voltage is large
   enough to keep the current mirror accurate across Vds variations.
2. **Better matching:** Pelgrom's law says sigma(Vth) proportional to 1/sqrt(W*L).
   At W=4u, L=4u, we get 16 um^2 area per device, reducing Vth mismatch.
3. **Reduce channel-length modulation:** The Iref depends on the mirror ratio. Any
   systematic or random mismatch in M3/M4 directly modulates Iref.

### 4.2 Why K=4

The ratio K = (W/L)_M2 / (W/L)_M1 = (8/4) / (2/4) = 4.

In the strong-inversion formula, the term (1 - 1/sqrt(K))^2:
- K=4: (1 - 1/2)^2 = 0.25
- K=9: (1 - 1/3)^2 = 0.44
- K=16: (1 - 1/4)^2 = 0.56

Higher K gives more current for the same R, or allows a smaller R for the same current.
But higher K also means M2 is physically larger, worsening layout matching. K=4 is the
classic compromise: the factor is 0.25, so with R1=2M and reasonable mobility values,
we land near 500 nA.

### 4.3 Why W=0.5u L=0.5u for M6

The startup device must be small. It only needs to inject a few nanoamps to kick the
loop. A minimum-size device is fine. L=0.5u keeps it fast (high gm/Id for transient
response). W=0.5u limits the charge injection when M6 turns off.

### 4.4 Why C_startup = 100 fF

The startup capacitor must couple enough charge to turn M6 on during the VDD ramp.
With a 10 us ramp time and 1.8 V swing, the slew rate is 1.8V/10us = 180 kV/s.
The current injected through C_startup is:

    I_cap = C * dV/dt = 100e-15 * 180e3 = 18 pA

This is small, but M6's Vth is around 0.4-0.5V, and the capacitive divider between
C_startup and M6's gate capacitance (~5 fF) means the gate voltage rises close to
VDD initially. The transient Vgs of M6 easily exceeds Vth, and M6 can source
significant current (hundreds of nA) during the startup transient. The 100 fF value
provides margin.

---

## 5. PASS/FAIL Criteria

Every specification below must be met for the design to be accepted. If any single
criterion fails, the design must be iterated.

| # | Parameter | Condition | Min | Typical | Max | Unit | Priority |
|---|-----------|-----------|-----|---------|-----|------|----------|
| 1 | Iref | TT, 27C, VDD=1.8V | 400 | 500 | 600 | nA | CRITICAL |
| 2 | Temp coefficient | -40C to 85C, TT | — | — | 150 | ppm/C | CRITICAL |
| 3 | Supply sensitivity | VDD 1.6-2.0V, TT, 27C | — | — | 2 | %/V | HIGH |
| 4 | PSRR @ 1kHz | TT, 27C, VDD=1.8V | 40 | — | — | dB | HIGH |
| 5 | Startup time | VDD ramp 0-1.8V in 10us | — | — | 10 | us | CRITICAL |
| 6 | Zero-current state | All corners, all temps | — | NONE | — | — | CRITICAL |
| 7 | Total power | TT, 27C, VDD=1.8V | — | — | 15 | uW | MEDIUM |
| 8 | Monte Carlo 3-sigma Iref | 200 runs, TT, 27C | -40 | — | +40 | % | HIGH |

### 5.1 Notes on Criteria

**Criterion 1 (Iref):** The 400-600 nA range is deliberately wide (+-20%) because the
beta-multiplier current depends on mobility and threshold voltage, both of which
shift significantly across corners. The downstream blocks must tolerate this range.

**Criterion 2 (TC):** 150 ppm/C over 125C range means Iref can drift by
150e-6 * 125 * 500e-9 = 9.375 nA, or about 1.9% total. This is adequate for bias
currents but would be poor for a voltage reference. State-of-the-art is 10-30 ppm/C.
We acknowledge falling short.

**Criterion 5 (Startup):** The circuit must reach within 10% of final Iref within 10 us
of VDD reaching 1.8 V. This means the startup circuit must work, and the loop must
settle quickly.

**Criterion 6 (Zero-current):** This is the single most critical criterion. If the
startup circuit fails in even one corner/temperature combination, the chip is dead.
We must verify across all 5 corners x at least 3 temperatures = 15 combinations.

**Criterion 8 (Monte Carlo):** 200 runs with both mismatch and process variation
enabled. The 3-sigma spread must be within +-40% of the nominal 500 nA. This means
the 3-sigma boundaries are 300-700 nA.

---

## 6. Simulation Testbenches

All testbenches use the following header:

```spice
** Testbench header for Block 00: Bias Generator
** SKY130A PDK

.param mc_mm_switch=0
.param mc_pr_switch=0

.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt

.include "bias_generator.spice"

Vdd vdd gnd 1.8
```

Replace `<PDK_PATH>` with the actual SKY130A PDK installation path, e.g.,
`/usr/share/pdk/sky130A` or `$PDK_ROOT/sky130A`.

---

### 6.1 Testbench 1: DC Operating Point (tb_bias_dc.spice)

**Purpose:** Verify that the circuit is alive and all transistors are in the expected
operating region. Print every node voltage and every device's operating point
parameters.

```spice
** tb_bias_dc.spice — DC operating point

.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt
.include "bias_generator.spice"

Vdd vdd gnd 1.8
Vgnd gnd 0 0

.control
    op

    echo "=== Node Voltages ==="
    print all

    echo ""
    echo "=== Iref (current through R1) ==="
    print @r1[i]
    print i(Vdd)

    echo ""
    echo "=== M1 Operating Point ==="
    print @m.xm1.msky130_fd_pr__nfet_01v8[vgs]
    print @m.xm1.msky130_fd_pr__nfet_01v8[vth]
    print @m.xm1.msky130_fd_pr__nfet_01v8[vds]
    print @m.xm1.msky130_fd_pr__nfet_01v8[id]
    print @m.xm1.msky130_fd_pr__nfet_01v8[gm]
    print @m.xm1.msky130_fd_pr__nfet_01v8[region]

    echo ""
    echo "=== M2 Operating Point ==="
    print @m.xm2.msky130_fd_pr__nfet_01v8[vgs]
    print @m.xm2.msky130_fd_pr__nfet_01v8[vth]
    print @m.xm2.msky130_fd_pr__nfet_01v8[vds]
    print @m.xm2.msky130_fd_pr__nfet_01v8[id]
    print @m.xm2.msky130_fd_pr__nfet_01v8[gm]
    print @m.xm2.msky130_fd_pr__nfet_01v8[region]

    echo ""
    echo "=== M3 Operating Point ==="
    print @m.xm3.msky130_fd_pr__pfet_01v8[vgs]
    print @m.xm3.msky130_fd_pr__pfet_01v8[vth]
    print @m.xm3.msky130_fd_pr__pfet_01v8[vds]
    print @m.xm3.msky130_fd_pr__pfet_01v8[id]
    print @m.xm3.msky130_fd_pr__pfet_01v8[gm]
    print @m.xm3.msky130_fd_pr__pfet_01v8[region]

    echo ""
    echo "=== M4 Operating Point ==="
    print @m.xm4.msky130_fd_pr__pfet_01v8[vgs]
    print @m.xm4.msky130_fd_pr__pfet_01v8[vth]
    print @m.xm4.msky130_fd_pr__pfet_01v8[vds]
    print @m.xm4.msky130_fd_pr__pfet_01v8[id]
    print @m.xm4.msky130_fd_pr__pfet_01v8[gm]
    print @m.xm4.msky130_fd_pr__pfet_01v8[region]

    echo ""
    echo "=== Startup Device M6 ==="
    print @m.xm6.msky130_fd_pr__nfet_01v8[vgs]
    print @m.xm6.msky130_fd_pr__nfet_01v8[vth]
    print @m.xm6.msky130_fd_pr__nfet_01v8[id]
    echo "M6 should be OFF (Id ~ 0) at steady state"

    echo ""
    echo "=== CRITICAL CHECK: PMOS Vgs - Vth ==="
    let m3_overdrive = @m.xm3.msky130_fd_pr__pfet_01v8[vgs] - @m.xm3.msky130_fd_pr__pfet_01v8[vth]
    let m4_overdrive = @m.xm4.msky130_fd_pr__pfet_01v8[vgs] - @m.xm4.msky130_fd_pr__pfet_01v8[vth]
    print m3_overdrive
    print m4_overdrive
    echo "Both must be > 150 mV (SKY130 PMOS subthreshold models unreliable)"

    echo ""
    echo "=== Power ==="
    let power = -i(Vdd) * 1.8
    print power
.endc

.end
```

**What to look for:**
- Iref should be close to 500 nA.
- M1 and M2 should be in saturation (region = 2) or moderate inversion.
- M3 and M4 should be in saturation with |Vgs - Vth| > 150 mV.
- M6 drain current should be negligible (< 1 pA).
- Total power should be below 15 uW.

---

### 6.2 Testbench 2: Temperature Sweep (tb_bias_temp.spice)

**Purpose:** Measure Iref across temperature from -40C to 85C and compute the
temperature coefficient.

```spice
** tb_bias_temp.spice — Temperature sweep

.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt
.include "bias_generator.spice"

Vdd vdd gnd 1.8
Vgnd gnd 0 0

.control
    let temps = ( -40 -20 0 20 27 40 60 85 )
    let iref_vals = vector(8)
    let idx = 0

    foreach temp_val $&temps
        set temp = $temp_val
        op
        let iref_vals[idx] = @r1[i]
        let idx = idx + 1
    end

    echo "=== Iref vs Temperature ==="
    echo "Temp(C)  Iref(nA)"
    let idx = 0
    foreach temp_val $&temps
        let iref_na = iref_vals[idx] * 1e9
        echo "$temp_val  $&iref_na"
        let idx = idx + 1
    end

    echo ""
    echo "=== Temperature Coefficient Calculation ==="
    let iref_min = minimum(iref_vals)
    let iref_max = maximum(iref_vals)
    let iref_nom = iref_vals[4]
    let tc_ppm = (iref_max - iref_min) / iref_nom / 125 * 1e6
    echo "Iref_min = $&iref_min"
    echo "Iref_max = $&iref_max"
    echo "Iref_nom (27C) = $&iref_nom"
    echo "TC = $&tc_ppm ppm/C"

    if tc_ppm > 150
        echo "*** FAIL: TC exceeds 150 ppm/C ***"
    else
        echo "PASS: TC within spec"
    end
.endc

.end
```

**What to look for:**
- The Iref vs T curve should be relatively flat, ideally with a slight bow shape.
- TC must be below 150 ppm/C.
- If TC is too high, note whether Iref increases or decreases with temperature.
  - Iref increasing with T: dominated by mobility decrease (PTAT component too strong).
  - Iref decreasing with T: dominated by Vth decrease (CTAT component too strong).
  - This guides the design iteration: adjust K or R1 to rebalance.

---

### 6.3 Testbench 3: Supply Sweep (tb_bias_supply.spice)

**Purpose:** Measure Iref sensitivity to supply voltage variations.

```spice
** tb_bias_supply.spice — Supply sensitivity

.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt
.include "bias_generator.spice"

Vdd vdd gnd dc 1.8
Vgnd gnd 0 0

.control
    dc Vdd 1.4 2.2 0.05

    echo "=== Iref vs VDD ==="
    print @r1[i]

    let iref = @r1[i]
    plot iref title "Iref vs VDD" xlabel "VDD (V)" ylabel "Iref (A)"

    echo ""
    echo "=== Supply Sensitivity ==="
    meas dc iref_1p6 find @r1[i] at=1.6
    meas dc iref_2p0 find @r1[i] at=2.0
    meas dc iref_1p8 find @r1[i] at=1.8
    let supply_sens = (iref_2p0 - iref_1p6) / iref_1p8 / 0.4 * 100
    echo "Iref at 1.6V = $&iref_1p6"
    echo "Iref at 1.8V = $&iref_1p8"
    echo "Iref at 2.0V = $&iref_2p0"
    echo "Supply sensitivity = $&supply_sens %/V"

    if supply_sens > 2
        echo "*** FAIL: Supply sensitivity exceeds 2%/V ***"
    else
        echo "PASS: Supply sensitivity within spec"
    end
.endc

.end
```

**What to look for:**
- Iref should be nearly flat from about 1.5 V to 2.2 V.
- Below ~1.4 V, the circuit will lose headroom and Iref will drop — this is expected.
- Supply sensitivity in the 1.6-2.0 V range must be below 2%/V.
- If supply sensitivity is poor, the PMOS mirror output resistance is too low.
  Solution: add cascode M5 or increase L of M3/M4.

---

### 6.4 Testbench 4: Transient Startup (tb_bias_startup.spice)

**Purpose:** Prove that the circuit starts up from zero and does not get stuck in the
degenerate zero-current state.

```spice
** tb_bias_startup.spice — Power-on transient

.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt
.include "bias_generator.spice"

** VDD ramps from 0 to 1.8V in 10us
Vdd vdd gnd pwl(0 0 10u 1.8 50u 1.8)
Vgnd gnd 0 0

** Initial conditions: everything at zero
.ic v(gate_p)=0 v(gate_n)=0 v(drain_m1)=0 v(drain_m4)=0

.control
    tran 10n 50u uic

    echo "=== Startup Transient ==="
    echo "Checking Iref at t=20us (10us after VDD fully on)"

    meas tran iref_final find @r1[i] at=20u
    meas tran iref_end find @r1[i] at=50u
    echo "Iref at 20us = $&iref_final"
    echo "Iref at 50us = $&iref_end"

    if iref_end < 100e-9
        echo "*** FAIL: Circuit stuck in zero-current state! ***"
        echo "*** Startup circuit is not working! ***"
    else
        echo "PASS: Circuit started up successfully"
    end

    ** Measure startup time (time to reach 90% of final value)
    let target = iref_end * 0.9
    meas tran t_startup when @r1[i] = target rise=1
    let startup_time = t_startup - 10u
    echo "Startup time (from VDD=1.8V to 90% Iref) = $&startup_time"

    if startup_time > 10u
        echo "*** FAIL: Startup time exceeds 10us ***"
    else
        echo "PASS: Startup time within spec"
    end

    plot @r1[i] v(vdd)/1e3 title "Startup: Iref and VDD vs time"
.endc

.end
```

**What to look for:**
- Iref must rise to the expected ~500 nA after VDD reaches 1.8 V.
- If Iref stays at zero, the startup circuit has failed. This is the most common
  failure mode. Check that C_startup is large enough and M6 is sized correctly.
- The startup time (from VDD reaching 1.8 V to Iref reaching 90% of final) must be
  less than 10 us.
- Look for ringing or overshoot — excessive overshoot could indicate the positive
  feedback loop is underdamped.

---

### 6.5 Testbench 5: Five-Corner Analysis (tb_bias_corners.spice)

**Purpose:** Verify Iref across all 5 process corners: TT, SS, FF, SF, FS.

```spice
** tb_bias_corners.spice — 5-corner analysis
** This file must be run 5 times with different .lib corner selections.
** Use a wrapper script or ngspice batch mode.

** --- Corner: TT ---
.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt
.include "bias_generator.spice"

Vdd vdd gnd 1.8
Vgnd gnd 0 0

.control
    op

    echo "=== Corner: TT ==="
    echo "Iref = $&@r1[i]"
    let iref_tt = @r1[i]

    ** Print all transistor operating points for this corner
    echo "M1: Vgs=$&@m.xm1.msky130_fd_pr__nfet_01v8[vgs] Vth=$&@m.xm1.msky130_fd_pr__nfet_01v8[vth] Id=$&@m.xm1.msky130_fd_pr__nfet_01v8[id]"
    echo "M2: Vgs=$&@m.xm2.msky130_fd_pr__nfet_01v8[vgs] Vth=$&@m.xm2.msky130_fd_pr__nfet_01v8[vth] Id=$&@m.xm2.msky130_fd_pr__nfet_01v8[id]"
    echo "M3: Vgs=$&@m.xm3.msky130_fd_pr__pfet_01v8[vgs] Vth=$&@m.xm3.msky130_fd_pr__pfet_01v8[vth] Id=$&@m.xm3.msky130_fd_pr__pfet_01v8[id]"
    echo "M4: Vgs=$&@m.xm4.msky130_fd_pr__pfet_01v8[vgs] Vth=$&@m.xm4.msky130_fd_pr__pfet_01v8[vth] Id=$&@m.xm4.msky130_fd_pr__pfet_01v8[id]"
.endc

.end
```

**Run as a batch with a shell script:**

```bash
#!/bin/bash
for corner in tt ss ff sf fs; do
    sed "s/\.lib.*sky130.lib.spice.*/\.lib \"<PDK_PATH>\/libs.tech\/ngspice\/sky130.lib.spice\" $corner/" \
        tb_bias_corners.spice > tb_bias_corners_${corner}.spice
    ngspice -b tb_bias_corners_${corner}.spice > results_${corner}.txt 2>&1
    echo "Corner $corner: $(grep 'Iref' results_${corner}.txt)"
done
```

**What to look for:**
- SS corner will have the lowest Iref (slow NMOS, higher Vth, lower mobility).
- FF corner will have the highest Iref.
- All 5 corners must produce Iref within 400-600 nA. If not, adjust sizing.
- Run startup testbench at SS corner — this is where startup is most likely to fail.

---

### 6.6 Testbench 6: Monte Carlo (tb_bias_mc.spice)

**Purpose:** Statistical analysis of Iref spread due to process variation and
device mismatch.

```spice
** tb_bias_mc.spice — Monte Carlo analysis (200 runs)

.lib "<PDK_PATH>/libs.tech/ngspice/sky130.lib.spice" tt
.include "bias_generator.spice"

.param mc_mm_switch=1
.param mc_pr_switch=1

Vdd vdd gnd 1.8
Vgnd gnd 0 0

.control
    let num_runs = 200
    let iref_results = vector(200)
    let run = 0

    repeat 200
        reset
        op
        let iref_results[run] = @r1[i]
        let run = run + 1
    end

    echo ""
    echo "=== Monte Carlo Results (200 runs) ==="

    let iref_mean = mean(iref_results)
    let iref_std = stddev(iref_results)
    let iref_min = minimum(iref_results)
    let iref_max = maximum(iref_results)
    let iref_3sig_lo = iref_mean - 3*iref_std
    let iref_3sig_hi = iref_mean + 3*iref_std

    echo "Mean Iref = $&iref_mean"
    echo "Std Dev   = $&iref_std"
    echo "Min       = $&iref_min"
    echo "Max       = $&iref_max"
    echo "3-sigma low  = $&iref_3sig_lo"
    echo "3-sigma high = $&iref_3sig_hi"

    let spread_lo = (iref_3sig_lo - iref_mean) / iref_mean * 100
    let spread_hi = (iref_3sig_hi - iref_mean) / iref_mean * 100
    echo "3-sigma spread: $&spread_lo % to $&spread_hi %"

    if spread_hi > 40
        echo "*** FAIL: 3-sigma spread exceeds +40% ***"
    end
    if spread_lo < -40
        echo "*** FAIL: 3-sigma spread exceeds -40% ***"
    end

    plot iref_results title "Monte Carlo: Iref distribution (200 runs)"

    echo ""
    echo "=== Histogram ==="
    ** ngspice does not have a built-in histogram, export to file for Python
    wrdata mc_iref_results.csv iref_results
    echo "Data written to mc_iref_results.csv — use Python to plot histogram"
.endc

.end
```

**Post-processing with Python:**

```python
#!/usr/bin/env python3
"""Plot Monte Carlo histogram for Iref."""

import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("mc_iref_results.csv", skiprows=1)
iref = data[:, 1] * 1e9  # Convert to nA

mean_val = np.mean(iref)
std_val = np.std(iref)

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(iref, bins=30, edgecolor='black', alpha=0.7)
ax.axvline(mean_val, color='red', linestyle='--', label=f'Mean = {mean_val:.1f} nA')
ax.axvline(mean_val - 3*std_val, color='orange', linestyle=':', label=f'3-sigma low = {mean_val - 3*std_val:.1f} nA')
ax.axvline(mean_val + 3*std_val, color='orange', linestyle=':', label=f'3-sigma high = {mean_val + 3*std_val:.1f} nA')
ax.set_xlabel('Iref (nA)')
ax.set_ylabel('Count')
ax.set_title('Monte Carlo: Bias Generator Iref (200 runs)')
ax.legend()
plt.tight_layout()
plt.savefig('mc_iref_histogram.png', dpi=150)
plt.show()

print(f"Mean:  {mean_val:.2f} nA")
print(f"Sigma: {std_val:.2f} nA")
print(f"3-sigma range: {mean_val - 3*std_val:.2f} to {mean_val + 3*std_val:.2f} nA")
print(f"3-sigma spread: {(mean_val - 3*std_val - mean_val)/mean_val*100:.1f}% to {(mean_val + 3*std_val - mean_val)/mean_val*100:.1f}%")
```

---

## 7. Honesty Rules

These rules are non-negotiable. They exist to prevent the most common failure mode in
analog design: convincing yourself the circuit works when it does not.

### 7.1 Print Every Transistor's Operating Point

For every simulation, print the following for each of M1 through M8:
- Vgs (gate-source voltage)
- Vth (threshold voltage, extracted by the model)
- Vds (drain-source voltage)
- Id (drain current)
- gm (transconductance)
- region (0=cutoff, 1=linear, 2=saturation, 3=subthreshold)

Do not skip any device. If a device is supposed to be off (M6 at steady state), confirm
it by printing Id and verifying it is below 1 pA.

### 7.2 Verify PMOS Overdrive

The SKY130 PMOS models are known to have accuracy issues in subthreshold. PMOS devices
in the bias generator must operate with |Vgs - Vth| > 150 mV. If any PMOS device
has overdrive below 150 mV, the simulation results cannot be trusted.

**How to check:** After op analysis, compute |Vgs| - |Vth| for M3, M4, M5, M7, M8.
If below 150 mV, increase the PMOS W/L to push the device deeper into strong inversion,
or increase Iref to raise Vgs.

### 7.3 Startup Verification Is Not Optional

The startup circuit must be verified across ALL of:
- 5 process corners (TT, SS, FF, SF, FS)
- 3 temperatures (-40C, 27C, 85C)
- 2 supply voltages (1.6V, 1.8V)

That is 30 simulations. If the circuit fails to start up in even ONE of these 30
conditions, it is a FAIL. Do not rationalize ("it only fails at SS/-40C/1.6V which is
unlikely"). A chip that doesn't turn on is worthless.

### 7.4 Report Raw Numbers

Never round a simulation result to make it look better. If TC is 148.7 ppm/C, report
148.7 ppm/C — do not write "approximately 150 ppm/C" or "about 100 ppm/C." If a
number is borderline (e.g., TC = 149 ppm/C), flag it as at risk and consider whether
the design has adequate margin.

### 7.5 Iterate When Specs Fail

If any spec fails, do not move on. The design iteration loop is:

1. Identify the failing spec.
2. Understand the root cause (which device, which parameter dominates).
3. Propose a sizing change or topology modification.
4. Re-simulate.
5. Check that fixing one spec did not break another.

Common iterations:
- **TC too high:** Adjust K ratio or change operating region. If in strong inversion
  and TC is PTAT-dominated (Iref rises with T), reduce K or increase R1. If CTAT-
  dominated, do the opposite. Consider adding a series PTAT resistor (n-well diffusion
  resistor has positive TC that partially cancels poly-res negative TC).
- **Supply sensitivity too high:** Add cascode M5 in the PMOS mirror. Increase L of
  M3/M4.
- **Startup fails:** Increase C_startup. Increase M6 W. Add a second startup path
  (resistive pullup to VDD on the mirror gate, disconnected by a series PMOS once
  the loop is active).
- **Monte Carlo spread too wide:** Increase device area (W*L) for all matched pairs.
  Consider adding degeneration resistors in the NMOS sources.

### 7.6 Compare to State of the Art

After obtaining the final TC value, write a comparison:

| Metric | This Design | Camacho-Galeano (2005) | Banba (1999) | Target |
|--------|-------------|------------------------|--------------|--------|
| TC (ppm/C) | ??? | 36 | 30 | <150 |
| Power | ??? | ~300nW | 3uW | <15uW |
| Iref | 500nA | 170nA | N/A (voltage ref) | 500nA |
| Process | SKY130 | 0.35um | 0.6um | SKY130 |

Be honest about where this design falls relative to published work. If TC is 120 ppm/C,
state clearly: "This design achieves 120 ppm/C, which is 3-4x worse than the best
published beta-multiplier references. The primary limitation is the SKY130 poly
resistor TC and the moderate-inversion operating region."

---

## 8. Layout Guidelines

### 8.1 Matched PMOS Pair (M3/M4)

M3 and M4 must be matched to better than 0.5% for the mirror to be accurate.

- **Common centroid layout:** Use ABBA arrangement. Split each device into 2 fingers:
  M3_A, M4_A, M4_B, M3_B, arranged along a single axis.
- **Same orientation:** Both devices must have the same source/drain orientation
  relative to the wafer flat.
- **Symmetric routing:** Metal connections to gates, drains, and sources must be
  mirror-symmetric.
- **Dummy devices:** Place dummy PMOS fingers at both ends of the array to absorb
  etch proximity effects. Tie dummy gates to VDD (off).

### 8.2 Matched NMOS Pair (M1/M2)

M1 and M2 have different W/L ratios (K=4), so simple interdigitation is not
straightforward. Options:

- **Finger decomposition:** M1 = 1 finger of W=2u. M2 = 4 fingers of W=2u each.
  Arrange as: D M1 M2a M2b M2c M2d D (with dummies D).
- **Or:** M1 = 2 fingers of W=1u. M2 = 8 fingers of W=1u. Interdigitate as
  M1a M2a M2b M2c M2d M1b M2e M2f M2g M2h with dummies. This gives better matching
  but is more complex to route.

### 8.3 Resistor R1

The 2 Mohm poly resistor is the dominant area element.

- **Serpentine layout:** Route as a back-and-forth serpentine with 180-degree turns.
- **Width:** Use the minimum width for sky130_fd_pr__res_xhigh_po (typically 0.35 um
  or 1 um depending on the variant). Wider is better for matching but increases area.
  A width of 2 um is a good compromise.
- **Dummy segments:** Add at least one dummy resistor segment at each end of the
  serpentine. These are connected to the resistor body but do not carry signal current.
  They ensure the end segments see the same etch environment as the interior segments.
- **Head/tail symmetry:** The two terminals of R1 should emerge from the same end of
  the serpentine (U-shaped routing) to minimize systematic resistance gradients.
- **Distance from transistors:** Keep R1 at least 10 um from any transistor to avoid
  thermal coupling. The resistor's TC is its own worst enemy — don't add self-heating
  from nearby devices.

### 8.4 Guard Rings

- **N-well guard ring:** Surround the entire PMOS section with a continuous n-well
  ring tied to VDD.
- **P-sub guard ring:** Surround the entire NMOS section and the resistor with a
  p-substrate ring tied to GND.
- **Full block guard ring:** Surround the entire bias generator block with an
  additional p-sub ring to isolate from neighboring digital or switching circuits.

### 8.5 Placement Strategy

```
+--------------------------------------------------+
|  p-sub guard ring (GND)                          |
|  +----------------------------------------------+|
|  |  PMOS section (M3/M4/M5/M7/M8)              ||
|  |  [n-well guard ring around this section]     ||
|  +----------------------------------------------+|
|  |  NMOS section (M1/M2/M6)                     ||
|  |  [p-sub guard ring around this section]      ||
|  +----------------------------------------------+|
|  |  Resistor R1 (serpentine)                     ||
|  |  [p-sub guard ring around this section]      ||
|  +----------------------------------------------+|
|  |  MIM cap C_startup                            ||
|  +----------------------------------------------+|
+--------------------------------------------------+
```

### 8.6 Metal Stack Usage

- **M1:** Local interconnect within device arrays.
- **M2:** Horizontal routing (gates, source/drain connections).
- **M3:** Vertical routing (power distribution, inter-section connections).
- **M4:** VDD and GND power rails (wide traces for low IR drop).
- **M3-M4:** MIM capacitor plates (C_startup).

### 8.7 DRC/LVS Checklist

Before declaring layout complete:

1. Run Magic DRC — zero violations.
2. Run KLayout DRC as cross-check — zero violations.
3. Extract parasitics with Magic (`extract all`, `ext2spice`).
4. Run Netgen LVS against the schematic netlist — zero mismatches.
5. Re-simulate with extracted parasitics — verify all specs still pass.
6. Particular attention: parasitic resistance in the mirror gate connection can
   degrade matching. Verify that the gate resistance is less than 100 ohm.

---

## 9. What to Do When Stuck

### 9.1 Convergence Failure

If ngspice reports "no convergence" during DC operating point:

1. Add `.ic` statements to guide the solver to the correct operating point:
   ```spice
   .ic v(gate_p)=1.0 v(gate_n)=0.6
   ```
2. Add `.nodeset` for critical nodes:
   ```spice
   .nodeset v(gate_p)=1.0 v(gate_n)=0.6 v(drain_m1)=0.8
   ```
3. Reduce `gmin` convergence parameter:
   ```spice
   .option gmin=1e-15
   ```
4. Try the `source stepping` method:
   ```spice
   .option method=gear
   ```
5. As a last resort, run a transient simulation from a known state (all zeros) and
   let the circuit settle. Use the final node voltages as `.ic` for the DC analysis.

### 9.2 Temperature Coefficient Too High

If TC exceeds 150 ppm/C:

1. **Identify the dominant mechanism.** Run simulations at -40C, 27C, and 85C. If Iref
   increases monotonically with T, mobility decrease dominates (PTAT). If Iref
   decreases, Vth decrease dominates (CTAT).

2. **Adjust the operating region.** The TC zero-crossing occurs at a specific inversion
   level. In strong inversion, TC is typically PTAT-dominated. In weak inversion, TC
   is CTAT-dominated. The minimum TC occurs at the boundary (moderate inversion).
   Adjust Iref, K, or R1 to shift the operating point.

3. **Add a compensating resistor.** SKY130 offers:
   - `res_xhigh_po`: ~2000 ohm/sq, TC approximately -200 to -500 ppm/C (negative TC)
   - `res_high_po`: ~350 ohm/sq, different TC
   - n-well resistor (`res_generic_nd`): positive TC (~1500 ppm/C)
   By combining a poly resistor (negative TC) with a diffusion resistor (positive TC),
   the net TC can be reduced. This requires R1 to be split into two series components.

4. **Curvature correction.** If the TC is parabolic (good at 27C but drifts at
   extremes), a curvature correction circuit can help. This adds a nonlinear current
   that compensates the T^2 term. However, this significantly increases complexity
   and is typically not worth it for a 150 ppm/C target.

### 9.3 Supply Sensitivity Too High

If supply sensitivity exceeds 2%/V:

1. **Add cascode M5.** A PMOS cascode between M4 and the output increases the output
   impedance of the mirror by a factor of gm5*ro5, dramatically reducing the
   sensitivity of Iref to VDD variations.

2. **Increase L of M3/M4.** Longer channels have higher Early voltage, increasing
   ro and reducing the VDD sensitivity.

3. **Add a regulated cascode (gain-boosted mirror).** This is overkill for most
   applications but achieves >80 dB PSRR. It requires an additional amplifier and
   is not recommended for this design unless simpler approaches fail.

### 9.4 Startup Fails in Some Corner

If the circuit gets stuck at zero current in any corner:

1. **Increase C_startup.** Try 200 fF or 500 fF. Larger C means more charge injected
   during VDD ramp, but also more parasitic load on the node.

2. **Increase M6 width.** A wider M6 can source more current during startup. But a
   wider M6 also has more gate capacitance, which can load the startup node.

3. **Add a resistive startup path.** Connect a high-value resistor (10 Mohm+) from VDD
   to the PMOS mirror gate. This provides a DC path to charge the gate even without
   C_startup. The resistor must be large enough that its steady-state current is
   negligible (<10 nA).

4. **Two-stage startup.** Use an inverter chain: VDD powers an inverter whose input is
   the bias output. When bias is zero, the inverter output is high, enabling a startup
   PMOS. When bias establishes, the inverter output goes low, disabling the startup
   PMOS. This is robust but adds devices.

5. **Verify with slow VDD ramp.** The worst case for capacitive startup is a very slow
   VDD ramp (dV/dt is small, so the coupled current is small). Test with a 1 ms ramp
   time. If startup fails, the capacitive approach alone is insufficient and a resistive
   or active backup is needed.

### 9.5 Monte Carlo Spread Too Wide

If the 3-sigma spread exceeds +-40%:

1. **Increase matched device area.** Pelgrom's law: sigma(Vth) = A_VT / sqrt(W*L).
   Doubling the area of M1, M2, M3, M4 reduces mismatch by sqrt(2).

2. **Add source degeneration.** Small resistors (10-50 kohm) in the sources of M1 and
   M2 linearize the mirror and reduce sensitivity to Vth mismatch. But this requires
   additional headroom.

3. **Use a more robust topology.** If matching is fundamentally limited by the process,
   consider switching to a bandgap-like architecture with better inherent matching
   properties.

---

## 10. Deliverables Checklist

When this block is complete, the following files must exist and all criteria must pass:

- [ ] `bias_generator.sch` — Xschem schematic, DRC-clean
- [ ] `bias_generator.spice` — Extracted netlist from schematic
- [ ] `tb_bias_dc.spice` — Runs clean, Iref within 400-600 nA
- [ ] `tb_bias_temp.spice` — TC < 150 ppm/C
- [ ] `tb_bias_supply.spice` — Supply sensitivity < 2%/V
- [ ] `tb_bias_startup.spice` — Starts up in all corners/temps
- [ ] `tb_bias_corners.spice` — Iref within spec at all 5 corners
- [ ] `tb_bias_mc.spice` — 3-sigma spread < +-40%
- [ ] `results.md` — All measured specs with PASS/FAIL, raw numbers, honest comparison
- [ ] `bias_generator.mag` — Magic layout, DRC clean, LVS clean
- [ ] Post-layout simulation passes all specs

---

## 11. References

1. Banba, H. et al., "A CMOS Bandgap Reference Circuit with Sub-1-V Operation,"
   IEEE JSSC, vol. 34, no. 5, pp. 670-674, May 1999.

2. Camacho-Galeano, E.M. et al., "A 2-nW 1.1-V Self-Biased Current Reference in CMOS
   Technology," IEEE TCAS-II, vol. 52, no. 2, pp. 61-65, Feb. 2005.

3. Vittoz, E. and Fellrath, J., "CMOS Analog Integrated Circuits Based on Weak
   Inversion Operation," IEEE JSSC, vol. 12, no. 3, pp. 224-231, June 1977.

4. Razavi, B., "Design of Analog CMOS Integrated Circuits," 2nd Edition, McGraw-Hill,
   2017. Chapter 11: Bandgap References.

5. SkyWater SKY130 PDK documentation:
   https://skywater-pdk.readthedocs.io/en/main/

6. Jespers, P. and Murmann, B., "Systematic Design of Analog CMOS Circuits: Using
   Pre-Computed Lookup Tables," Cambridge University Press, 2017.

---

*End of Block 00 program. No shortcuts. Every number verified. Every failure investigated.*
