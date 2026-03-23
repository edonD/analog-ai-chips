#!/usr/bin/env python3
"""Optimize OTA sizing for maximum gain while meeting all constraints.

Strategy: sweep key parameters, run ngspice, parse results.
Focus on M1/M2 L (dominates gain via ro), M3/M4 L, and cascode L.
"""
import subprocess
import re
import os
import json

SPICE_TEMPLATE = """
.lib "sky130_minimal.lib.spice" tt
.include "ota_foldcasc_opt.spice"

Vdd vdd 0 dc 1.8
Vss vss 0 dc 0
Mbn vbn vbn 0 0 sky130_fd_pr__nfet_01v8__model W=4u L=4u nf=1
Ibias vdd vbn dc 500n
Vbcn vbcn 0 dc 0.80
Mbp vbp vbp vdd vdd sky130_fd_pr__pfet_01v8__model W=8u L=1u nf=2
Ibp vbp 0 dc 500n
Vbcp vbcp 0 dc 0.70

Vinp vinp 0 dc 0.9
Lfb vout vinn 1T

Xota vinp vinn vout vdd vss vbn vbcn vbp vbcp ota_foldcasc
CL vout 0 10p

.tf v(vout) Vinp

.control
  run
  let cl_gain = transfer_function
  let rout_cl = output_impedance_at_v(vout)
  let A = cl_gain / (1 - cl_gain)
  let A_db = 20*log(abs(A))/log(10)
  let rout_ol = rout_cl * (1 + A)

  op

  echo "RESULT: A=$&A A_db=$&A_db Rout_cl=$&rout_cl Rout_ol=$&rout_ol"
  echo "RESULT: Vout=$&v(vout)"
  echo "RESULT: M1_gm=$&@m.xota.m1[gm] M1_gds=$&@m.xota.m1[gds] M1_Id=$&@m.xota.m1[id]"
  echo "RESULT: M2_gm=$&@m.xota.m2[gm] M2_gds=$&@m.xota.m2[gds] M2_Id=$&@m.xota.m2[id]"
  echo "RESULT: M4_Vds=$&@m.xota.m4[vds] M4_Vdsat=$&@m.xota.m4[vdsat]"
  echo "RESULT: M6_Vds=$&@m.xota.m6[vds] M8_Vds=$&@m.xota.m8[vds]"
  echo "RESULT: M10_Vds=$&@m.xota.m10[vds] M11_Id=$&@m.xota.m11[id]"
  quit
.endc
.end
"""

OTA_TEMPLATE = """
.param W1  = {W1}   L1  = {L1}  nf1  = {nf1}
.param W2  = {W1}   L2  = {L1}  nf2  = {nf1}
.param W3  = {W3}   L3  = {L3}  nf3  = 2
.param W4  = {W3}   L4  = {L3}  nf4  = 2
.param W5  = {W5}   L5  = {L5}  nf5  = 2
.param W6  = {W5}   L6  = {L5}  nf6  = 2
.param W7  = {W7}   L7  = {L7}  nf7  = 2
.param W8  = {W7}   L8  = {L7}  nf8  = 2
.param W9  = 2u   L9  = 4.0u  nf9  = 1
.param W10 = 2u   L10 = 4.0u  nf10 = 1
.param W11 = 4u   L11 = 4.0u  nf11 = 1
.param W12 = 0.42u L12 = 4.0u  nf12 = 1
.param W13 = 0.42u L13 = 4.0u  nf13 = 1

.subckt ota_foldcasc vinp vinn vout vdd vss vbn vbcn vbp vbcp
M1 fold_p vinp tail vss sky130_fd_pr__nfet_01v8__model W={{W1}} L={{L1}} nf={{nf1}}
M2 vout   vinn tail vss sky130_fd_pr__nfet_01v8__model W={{W2}} L={{L2}} nf={{nf2}}
M11 tail vbn vss vss sky130_fd_pr__nfet_01v8__model W={{W11}} L={{L11}} nf={{nf11}}
M3  mid_p vbp vdd vdd sky130_fd_pr__pfet_01v8__model W={{W3}} L={{L3}} nf={{nf3}}
M4  mid_n vbp vdd vdd sky130_fd_pr__pfet_01v8__model W={{W4}} L={{L4}} nf={{nf4}}
M12 mid_p vbp vdd vdd sky130_fd_pr__pfet_01v8__model W={{W12}} L={{L12}} nf={{nf12}}
M13 mid_n vbp vdd vdd sky130_fd_pr__pfet_01v8__model W={{W13}} L={{L13}} nf={{nf13}}
M5  fold_p vbcp mid_p vdd sky130_fd_pr__pfet_01v8__model W={{W5}} L={{L5}} nf={{nf5}}
M6  vout   vbcp mid_n vdd sky130_fd_pr__pfet_01v8__model W={{W6}} L={{L6}} nf={{nf6}}
M7  fold_p vbcn src_n7 vss sky130_fd_pr__nfet_01v8__model W={{W7}} L={{L7}} nf={{nf7}}
M8  vout   vbcn src_n8 vss sky130_fd_pr__nfet_01v8__model W={{W8}} L={{L8}} nf={{nf8}}
M9  src_n7 vbn vss vss sky130_fd_pr__nfet_01v8__model W={{W9}} L={{L9}} nf={{nf9}}
M10 src_n8 vbn vss vss sky130_fd_pr__nfet_01v8__model W={{W10}} L={{L10}} nf={{nf10}}
.ends ota_foldcasc
"""

def run_sim(params):
    """Run simulation with given parameters and return results."""
    # Write OTA file
    ota = OTA_TEMPLATE.format(**params)
    with open('ota_foldcasc_opt.spice', 'w') as f:
        f.write(ota)

    # Write testbench
    with open('opt_tb.spice', 'w') as f:
        f.write(SPICE_TEMPLATE)

    # Run ngspice
    result = subprocess.run(['/usr/bin/ngspice', '-b', 'opt_tb.spice'],
                          capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr

    # Parse results
    data = {}
    for line in output.split('\n'):
        if line.startswith('RESULT:'):
            pairs = re.findall(r'(\w+)=([\d.eE+-]+)', line)
            for k, v in pairs:
                try:
                    data[k] = float(v)
                except:
                    pass
    return data

# Parameter sweep
results = []
print(f"{'W1':>5} {'L1':>5} {'W3':>5} {'L3':>5} {'L5':>5} {'L7':>5} | {'A_db':>6} {'Vout':>6} {'M4_Vds':>7} {'M11_Id':>8} {'gm1':>8}")
print("-" * 80)

# Sweep M1/M2 L with proportional W
for L1_val in ['2.0u', '4.0u', '8.0u', '16.0u']:
    W1_num = float(L1_val.replace('u','')) * 5  # Keep W/L ratio = 5
    W1_val = f'{W1_num}u'
    nf1 = max(2, int(W1_num / 10))

    for L3_val in ['1.0u', '2.0u']:
        for L5_val in ['0.5u', '1.0u']:
            for L7_val in ['0.5u', '1.0u']:
                params = {
                    'W1': W1_val, 'L1': L1_val, 'nf1': nf1,
                    'W3': '8u', 'L3': L3_val,
                    'W5': '8u', 'L5': L5_val,
                    'W7': '4u', 'L7': L7_val,
                }
                data = run_sim(params)
                if 'A_db' in data:
                    results.append({**params, **data})
                    m4ok = 'OK' if data.get('M4_Vds', 0) > data.get('M4_Vdsat', 1) else 'TRI'
                    print(f"{W1_val:>5} {L1_val:>5} {'8u':>5} {L3_val:>5} {L5_val:>5} {L7_val:>5} | "
                          f"{data.get('A_db', 0):>6.1f} {data.get('Vout', 0):>6.3f} "
                          f"{data.get('M4_Vds', 0):>7.4f} {data.get('M11_Id', 0)*1e6:>7.2f}u "
                          f"{data.get('M1_gm', 0)*1e6:>7.2f}u {m4ok}")

# Find best
if results:
    best = max(results, key=lambda x: x.get('A_db', 0))
    print(f"\nBest: A={best.get('A_db', 0):.1f} dB with W1={best['W1']} L1={best['L1']} L3={best['L3']} L5={best['L5']} L7={best['L7']}")
    print(f"  Vout={best.get('Vout', 0):.3f}V M4_Vds={best.get('M4_Vds', 0):.4f}V M11_Id={best.get('M11_Id', 0)*1e9:.0f}nA")
