#!/usr/bin/env python3
"""Generate simulation data for all plots.
Runs multiple ngspice simulations and saves results as CSV files."""

import subprocess
import re
import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_ngspice(spice_code):
    """Run inline SPICE code and return stdout."""
    with open('/tmp/_plot_tb.spice', 'w') as f:
        f.write(spice_code)
    result = subprocess.run(['ngspice', '-b', '/tmp/_plot_tb.spice'],
                          capture_output=True, text=True, timeout=60)
    return result.stdout + result.stderr

HEADER = """\
.include "sky130_res_models.spice"
.include "design.cir"
Vpvdd pvdd 0 DC 5.0
Xfb pvdd vfb 0 feedback_network
"""

# --- 1. Temperature sweep ---
print("=== Generating temperature sweep data ===")
temps = list(range(-40, 155, 5))
temp_data = []
for t in temps:
    code = f"""{HEADER}
.control
set temp = {t}
op
echo "VFB: $&v(vfb)"
quit
.endc
.end
"""
    out = run_ngspice(code)
    for line in out.split('\n'):
        if line.startswith('VFB:'):
            vfb = float(line.split(':')[1].strip())
            temp_data.append((t, vfb))
            break

with open('plot_temp_data.csv', 'w') as f:
    f.write('temperature_C,vfb_V\n')
    for t, v in temp_data:
        f.write(f'{t},{v:.8f}\n')
print(f"  Saved {len(temp_data)} points to plot_temp_data.csv")

# --- 2. Corner data (bar chart) ---
print("=== Generating corner data ===")
corners_data = []
# var_mult values for corners
corner_configs = [
    ('TT', 0.0),
    ('SS', 0.05),
    ('FF', -0.05),
    ('SF', 0.025),
    ('FS', -0.025),
]
for name, vm in corner_configs:
    for t in [-40, 27, 150]:
        code = f"""\
.include "sky130_res_models.spice"
.param sky130_fd_pr__res_xhigh_po__var_mult = {vm}
.include "design.cir"
Vpvdd pvdd 0 DC 5.0
Xfb pvdd vfb 0 feedback_network
.control
set temp = {t}
op
echo "VFB: $&v(vfb)"
quit
.endc
.end
"""
        out = run_ngspice(code)
        for line in out.split('\n'):
            if line.startswith('VFB:'):
                vfb = float(line.split(':')[1].strip())
                corners_data.append((name, t, vfb))
                break

with open('plot_corners_data.csv', 'w') as f:
    f.write('corner,temperature_C,vfb_V\n')
    for name, t, v in corners_data:
        f.write(f'{name},{t},{v:.8f}\n')
print(f"  Saved {len(corners_data)} points to plot_corners_data.csv")

# --- 3. MC data already exists in mc_vfb_data.txt, just reformat ---
print("=== Processing MC data ===")
mc_vals = []
if os.path.exists('mc_vfb_data.txt'):
    with open('mc_vfb_data.txt') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    mc_vals.append(float(parts[1]))
                except ValueError:
                    pass
    with open('plot_mc_data.csv', 'w') as f:
        f.write('run,vfb_V\n')
        for i, v in enumerate(mc_vals):
            f.write(f'{i},{v:.8f}\n')
    print(f"  Saved {len(mc_vals)} MC runs to plot_mc_data.csv")
else:
    print("  WARNING: mc_vfb_data.txt not found")

print("Done generating plot data.")
