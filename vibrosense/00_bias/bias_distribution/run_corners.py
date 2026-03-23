#!/usr/bin/env python3
"""Run 5 corners x 3 temperatures for bias_generator_full"""

import subprocess
import os
import re

CORNERS = ['tt', 'ss', 'ff', 'sf', 'fs']
TEMPS = [-40, 27, 85]
SKY130_LIB = "/home/ubuntu/.volare/sky130A/libs.tech/combined/continuous/sky130.lib.spice"

# TT 27C reference values
REF = {'vbn': 0.629, 'vbcn': 0.883, 'vbp': 0.739, 'vbcp': 0.474}
TOLERANCE = 0.100  # +/- 100mV

NETLIST_TEMPLATE = """\
** Corner sweep: {corner} {temp}C
.param mc_mm_switch=0
.param mc_pr_switch=0
.option scale=1e-6
.lib "{lib}" {corner}

.include "design_full.cir"

Xbias vdd gnd iref_out vbn vbcn vbp vbcp  bias_generator_full
Vdd vdd gnd 1.8
Riref iref_out gnd 3560

.temp {temp}

.nodeset v(vbn)=0.65 v(vbp)=0.73 v(vbcn)=0.88 v(vbcp)=0.475
.nodeset v(xbias.out_n)=0.65 v(xbias.vbias)=0.68
+ v(xbias.od1)=0.85 v(xbias.otail)=0.15 v(xbias.src_m2)=0.06 v(xbias.mid_r)=0.03

.control
op
let iref_nA = @Riref[i] * 1e9
echo "RESULT: $&v(vbn) $&v(vbcn) $&v(vbp) $&v(vbcp) $&iref_nA"
.endc

.end
"""

results = []
all_pass = True

print(f"{'Corner':>6} {'Temp':>5} {'vbn':>8} {'vbcn':>8} {'vbp':>8} {'vbcp':>8} {'Iref_nA':>8} {'Status':>6}")
print("-" * 65)

for corner in CORNERS:
    for temp in TEMPS:
        netlist = NETLIST_TEMPLATE.format(corner=corner, temp=temp, lib=SKY130_LIB)

        tmp_file = f"/tmp/tb_corner_{corner}_{temp}.spice"
        with open(tmp_file, 'w') as f:
            f.write(netlist)

        proc = subprocess.run(
            ['ngspice', '-b', tmp_file],
            capture_output=True, text=True, timeout=120
        )

        output = proc.stdout + proc.stderr

        # Parse RESULT line
        match = re.search(r'RESULT:\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)', output)
        if match:
            vbn = float(match.group(1))
            vbcn = float(match.group(2))
            vbp = float(match.group(3))
            vbcp = float(match.group(4))
            iref = float(match.group(5))

            # Check tolerances
            ok = True
            for name, val, ref in [('vbn', vbn, REF['vbn']), ('vbcn', vbcn, REF['vbcn']),
                                    ('vbp', vbp, REF['vbp']), ('vbcp', vbcp, REF['vbcp'])]:
                if abs(val - ref) > TOLERANCE:
                    ok = False

            status = "PASS" if ok else "FAIL"
            if not ok:
                all_pass = False

            print(f"{corner:>6} {temp:>5} {vbn:>8.4f} {vbcn:>8.4f} {vbp:>8.4f} {vbcp:>8.4f} {iref:>8.1f} {status:>6}")
            results.append((corner, temp, vbn, vbcn, vbp, vbcp, iref, status))
        else:
            print(f"{corner:>6} {temp:>5} {'PARSE ERROR':>40}")
            all_pass = False

print("-" * 65)
if all_pass:
    print("ALL 15 CONDITIONS PASS")
else:
    print("SOME CONDITIONS FAIL")

# Find worst-case deviations
print("\n=== WORST-CASE DEVIATIONS FROM TT 27C ===")
for sig in ['vbn', 'vbcn', 'vbp', 'vbcp']:
    idx = {'vbn': 2, 'vbcn': 3, 'vbp': 4, 'vbcp': 5}[sig]
    worst_dev = 0
    worst_cond = ""
    for r in results:
        dev = abs(r[idx] - REF[sig])
        if dev > worst_dev:
            worst_dev = dev
            worst_cond = f"{r[0]} {r[1]}C"
    print(f"  {sig}: worst = {worst_dev*1000:.1f} mV at {worst_cond} (limit: {TOLERANCE*1000:.0f} mV)")
