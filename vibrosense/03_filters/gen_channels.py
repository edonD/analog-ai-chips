#!/usr/bin/env python3
"""Generate pseudo-differential BPF subcircuit files for all 5 channels."""

channels = {
    1: {'f0': 224,   'Q': 0.75, 'c1': 77,  'c2': 137, 'iref': 50},
    2: {'f0': 1000,  'Q': 0.67, 'c1': 22,  'c2': 48,  'iref': 70},
    3: {'f0': 3162,  'Q': 1.05, 'c1': 23,  'c2': 21,  'iref': 150},
    4: {'f0': 7071,  'Q': 1.41, 'c1': 40,  'c2': 20,  'iref': 440},
    5: {'f0': 14142, 'Q': 1.41, 'c1': 40,  'c2': 20,  'iref': 870},
}

for ch, spec in channels.items():
    content = f"""* VibroSense Block 03 — Channel {ch} Pseudo-Differential BPF
* Tow-Thomas biquad, real SKY130 transistor-level OTA
* f0={spec['f0']}Hz, Q={spec['Q']}, Iref={spec['iref']}nA
* C1={spec['c1']}pF, C2={spec['c2']}pF
*
* Pseudo-differential: two mirrored single-ended paths
* HD2 cancels in differential output → THD < -30 dBc at 200mVpp
*
* Ports:
*   vinp/vinn: differential input
*   bp_outp/bp_outn: differential bandpass output
*   vdd/vss/vcm: supply and common mode
*   vbn/vbcn/vbp/vbcp: bias from ota_bias_dist

.subckt bpf_ch{ch}_real vinp vinn bp_outp bp_outn vdd vss vcm vbn vbcn vbp vbcp

* ============================
* Positive path (input = vinp)
* ============================

* OTA1+: Input + feedback
Xota1p vinp int2p int1p vdd vss vbn vbcn vbp vbcp ota_foldcasc

* C1 at V1+ node
C1p int1p vss {spec['c1']}p

* Pseudo-resistor DC bias for V1+
Xpr1p int1p vcm pseudo_res

* OTA2+: Forward integrator
Xota2p int1p vcm int2p vdd vss vbn vbcn vbp vbcp ota_foldcasc

* C2 at V2+ node
C2p int2p vss {spec['c2']}p

* Pseudo-resistor DC bias for V2+
Xpr2p int2p vcm pseudo_res

* OTA3+: Damping
Xota3p vcm int1p int1p vdd vss vbn vbcn vbp vbcp ota_foldcasc

* ============================
* Negative path (input = vinn)
* ============================

* OTA1-: Input + feedback
Xota1n vinn int2n int1n vdd vss vbn vbcn vbp vbcp ota_foldcasc

* C1 at V1- node
C1n int1n vss {spec['c1']}p

* Pseudo-resistor DC bias for V1-
Xpr1n int1n vcm pseudo_res

* OTA2-: Forward integrator
Xota2n int1n vcm int2n vdd vss vbn vbcn vbp vbcp ota_foldcasc

* C2 at V2- node
C2n int2n vss {spec['c2']}p

* Pseudo-resistor DC bias for V2-
Xpr2n int2n vcm pseudo_res

* OTA3-: Damping
Xota3n vcm int1n int1n vdd vss vbn vbcn vbp vbcp ota_foldcasc

* ============================
* Differential output taps
* ============================
Routp bp_outp int1p 1m
Routn bp_outn int1n 1m

.ends bpf_ch{ch}_real
"""
    fname = f'bpf_ch{ch}_real.spice'
    with open(fname, 'w') as f:
        f.write(content)
    print(f'  Created {fname}: f0={spec["f0"]}Hz Q={spec["Q"]} '
          f'C1={spec["c1"]}p C2={spec["c2"]}p Iref={spec["iref"]}nA')

print('All 5 pseudo-differential BPF subcircuits generated.')
