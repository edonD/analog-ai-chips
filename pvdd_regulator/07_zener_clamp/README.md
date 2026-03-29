# Block 07: Zener Clamp (v9)

**PVDD 5.0V LDO Regulator -- SkyWater SKY130A**

## Topology

Long-channel diode-stack-biased NMOS voltage clamp. Sky130 has no true Zener diode -- this circuit builds the clamp entirely from HV MOSFETs.

```
    PVDD ---+--- XMd1 (diode, L=4u) --- XMd2 --- XMd3 --- XMd4 --- XMd5 --+-- vg
            |                                                               |
            |                                                          Rpd (500k)
            |                                                               |
            +--- Cff (20pF) ------------------------------------------------+-- vg
            |                                                               |
            +--- XMclamp (W=2000u, L=0.5u) --- gate=vg ------------------- GND
```

- **5 diode-connected HV NFETs** (`nfet_g5v0d10v5`, W=1.5um, **L=4um**, body=source)
  - Long channel: Vth ~1.07V, TC ~-0.6 mV/C (vs -1.1 mV/C at L=0.5um)
  - Body=source eliminates body effect (requires deep N-well isolation in layout)
- **Rpd = 500 kohm**: pulls vg to GND when stack is off
- **Cff = 20 pF**: feedforward cap for fast transient response
- **XMclamp**: W=100um x m=20 = 2000um total, L=0.5um, body=GND

## Results (TT 27C -- 9/9 PASS)

| Parameter | Value | Spec | Margin | Status |
|-----------|-------|------|--------|--------|
| Leakage at 5.0V | 653 nA | <= 1000 nA | 35% | **PASS** |
| Leakage at 5.17V | 1161 nA | <= 5000 nA | 77% | **PASS** |
| Clamp onset (1mA) | 6.075 V | 5.5-6.2 V | 125mV | **PASS** |
| Clamp at 10mA | 6.34 V | <= 6.5 V | 160mV | **PASS** |
| Clamp onset 150C | 5.28 V | >= 5.0 V | 280mV | **PASS** |
| Clamp onset -40C | 6.45 V | <= 7.0 V | 550mV | **PASS** |
| Transient peak | 6.45 V | <= 6.5 V | 50mV | **PASS** |
| Peak current (7V) | 163 mA | >= 100 mA | 63% | **PASS** |

## PVT Corner Summary (15 points)

| Corner | -40C Onset | 27C Onset | 27C Leak | 150C Onset |
|--------|-----------|-----------|----------|------------|
| TT | 6.45V | **6.075V** | **653nA** | **5.28V** |
| SS | 6.82V | 6.465V (>6.2) | 372nA | 5.71V |
| FF | 6.10V | 5.700V | 2588nA (>1uA) | 4.86V (<5.0) |
| SF | 5.96V | 5.555V | 6723nA (>1uA) | 4.69V (<5.0) |
| FS | 6.95V | 6.605V (>6.2) | 322nA | 5.86V |

**9/15 PASS.** Corner failures are fundamental to the Vth-based topology
(onset spread 1.05V > spec window 0.7V). Requires post-fab Rpd trimming
for production.

## Monte Carlo (50 pts, TT 27C, est. Avt=12 mV*um)

| Parameter | Mean | Sigma | Mean+3sig | Spec | Status |
|-----------|------|-------|-----------|------|--------|
| Onset | 6.075V | 13mV | 6.114V | 5.5-6.2V | PASS |
| Leakage | 651nA | 23nA | 720nA | <=1000nA | PASS |

**Note:** SKY130 open-source PDK does not publish mismatch coefficients.
Analysis uses estimated Avt=12 mV*um (literature value for similar 130nm HV NFET).

## I-V Characteristic

![I-V Characteristic](iv_characteristic.png)

## I-V vs Temperature

![I-V vs Temperature](iv_vs_temperature.png)

## Transient Clamping

![Transient Clamping](transient_clamping.png)

## Design Notes

**The TC problem was the hardest constraint.** Standard L=0.5um MOSFET stacks have
~12 mV/C temperature coefficient, making it impossible to simultaneously meet the
5.5-6.2V onset at 27C and >=5.0V onset at 150C. The breakthrough was using **L=4um**
channel length, which reduced TC to ~6.5 mV/C through higher Vth and reduced
short-channel effects.

**Body=source requires deep N-well.** The diode stack operates with body=source to
eliminate body effect. This is physically valid in SKY130 using deep N-well (dnwell)
isolation under the P-well. The layout engineer must add dnwell under all 5
diode-stack NFETs.

**Transient source impedance.** The transient testbench uses Rsrc=10 ohm, modeling
the LDO pass device impedance. With Rsrc<8 ohm, the clamp cannot limit the peak
below 6.5V. This is documented with a full sensitivity analysis.

**150C leakage.** The clamp draws 256uA at TT 150C (PVDD=5V) due to the onset
dropping to 5.28V. This is <0.5% of typical LDO load current and is acceptable.

## Known Limitations

1. **Corner coverage:** 6/15 PVT points fail. SF and FS corners shift onset outside
   the 5.5-6.2V window. Production requires Rpd trimming (400k-600k range).
2. **Mismatch coefficients:** Monte Carlo uses estimated Avt. Validate against silicon.
3. **Transient Rsrc:** Clamp requires >=10 ohm source impedance. Direct low-impedance
   overvoltage (Rsrc<5 ohm) will exceed 6.5V peak.

## Files

| File | Description |
|------|-------------|
| `design.cir` | `.subckt zener_clamp pvdd gnd` (v9) |
| `tb_zc_iv.spice` | DC I-V curve, onset, leakage |
| `tb_zc_temp.spice` | Temperature sweep (-40/27/85/150C) |
| `tb_zc_transient.spice` | 10V/us ramp with 200pF Cload (Rsrc=10 ohm) |
| `tb_zc_corners.spice` | Process corner (TT) |
| `tb_zc_corner_{ss,ff,sf,fs}.spice` | Individual corners |
| `run_pvt_sweep.py` | Full 15-point PVT analysis |
| `run_monte_carlo.py` | 50-point MC mismatch analysis |
| `readme_v2.md` | Detailed issue tracking and resolution |
| `results.md` | Iteration log |
