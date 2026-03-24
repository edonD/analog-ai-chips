#!/usr/bin/env python3
"""Extract bias voltages from Block 00 generator at all corners/temps."""
import subprocess
import re
import json

corners = ['tt', 'ss', 'ff', 'sf', 'fs']
temps = [-40, 27, 85]

results = {}
for corner in corners:
    for temp in temps:
        spice = f"""* Bias gen at {corner} {temp}C
.lib "/home/ubuntu/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice" {corner}
.include "../00_bias/bias_distribution/design_full.cir"
.option scale=1e-6
.temp {temp}
Vdd vdd 0 dc 1.8
Xbias vdd 0 iref_out vbn vbcn vbp vbcp bias_generator_full
.control
op
print v(vbn) v(vbcn) v(vbp) v(vbcp) @vdd[i]
.endc
.end
"""
        with open('/tmp/tb_bias_ext.spice', 'w') as f:
            f.write(spice)

        result = subprocess.run(['ngspice', '-b', '/tmp/tb_bias_ext.spice'],
                              capture_output=True, text=True, timeout=60)

        # Parse output
        out = result.stdout + result.stderr
        vals = {}
        for var in ['vbn', 'vbcn', 'vbp', 'vbcp']:
            m = re.search(rf'v\({var}\)\s*=\s*([0-9eE.+-]+)', out)
            if m:
                vals[var] = float(m.group(1))

        m = re.search(r'@vdd\[i\]\s*=\s*([0-9eE.+-]+)', out)
        if m:
            vals['isup'] = -float(m.group(1))

        key = f'{corner}_{temp}'
        results[key] = vals
        if vals.get('vbn'):
            print(f'{key:>8}: VBN={vals["vbn"]:.4f} VBCN={vals.get("vbcn",0):.4f} '
                  f'VBP={vals.get("vbp",0):.4f} VBCP={vals.get("vbcp",0):.4f} '
                  f'Isup={vals.get("isup",0)*1e6:.2f}µA')
        else:
            print(f'{key:>8}: FAILED')

with open('bias_corners.json', 'w') as f:
    json.dump(results, f, indent=2)
