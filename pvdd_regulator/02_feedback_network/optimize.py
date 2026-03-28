#!/usr/bin/env python3
"""optimize.py — Find optimal R_TOP/R_BOT sizing for Block 02.

Objective: minimize VFB error from 1.226V target across temperature.
Constraints:
  - VFB = 1.226V ± 1 mV at TT 27°C
  - Divider current 10-15 µA
  - TC < 200 µV/°C integrated -40 to 150°C

Variables: l_top, l_bot (resistor lengths in µm)
Fixed: w (set via command line, default 3.0)

Uses ngspice for each evaluation. Typically 2-5 seconds per run.
"""

import subprocess
import re
import sys
import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0

SPICE_TEMPLATE = """
.include "sky130_res_models.spice"

.subckt fb_opt pvdd vfb gnd
XR_TOP pvdd vfb gnd sky130_fd_pr__res_xhigh_po w={w} l={{l_top}}
XR_BOT vfb  gnd gnd sky130_fd_pr__res_xhigh_po w={w} l={{l_bot}}
.ends fb_opt

Vpvdd pvdd 0 DC 5.0
Xfb pvdd vfb 0 fb_opt

.control
{{commands}}
quit
.endc
.end
""".replace('{w}', str(W))

def run_spice(l_top, l_bot, commands):
    code = SPICE_TEMPLATE.replace('{l_top}', str(l_top)).replace('{l_bot}', str(l_bot)).replace('{commands}', commands)
    with open('/tmp/_opt_tb.spice', 'w') as f:
        f.write(code)
    result = subprocess.run(['ngspice', '-b', '/tmp/_opt_tb.spice'],
                          capture_output=True, text=True, timeout=30)
    return result.stdout + result.stderr

def get_vfb_and_current(l_top, l_bot, temp=27):
    commands = f"""
set temp = {temp}
op
echo "VFB: $&v(vfb)"
echo "IDIV: $&i(Vpvdd)"
"""
    out = run_spice(l_top, l_bot, commands)
    vfb = None
    idiv = None
    for line in out.split('\n'):
        if line.startswith('VFB:'):
            vfb = float(line.split(':')[1].strip())
        elif line.startswith('IDIV:'):
            idiv = abs(float(line.split(':')[1].strip()))
    return vfb, idiv

def cost(params):
    l_top, l_bot = params
    if l_top < 10 or l_bot < 5 or l_top > 1000 or l_bot > 500:
        return 1e6

    try:
        # Get VFB at 3 temperatures
        vfb_27, idiv = get_vfb_and_current(l_top, l_bot, 27)
        if vfb_27 is None:
            return 1e6

        vfb_m40, _ = get_vfb_and_current(l_top, l_bot, -40)
        vfb_150, _ = get_vfb_and_current(l_top, l_bot, 150)

        if vfb_m40 is None or vfb_150 is None:
            return 1e6

        # Primary: VFB error at 27C
        error_27 = abs(vfb_27 - 1.226) * 1000  # mV

        # Temperature drift
        drift = max(abs(vfb_m40 - vfb_27), abs(vfb_150 - vfb_27)) * 1000  # mV

        # Penalties
        penalty = 0
        if error_27 > 1.0:
            penalty += (error_27 - 1.0) * 100
        if idiv < 10e-6:
            penalty += (10e-6 - idiv) * 1e8
        if idiv > 15e-6:
            penalty += (idiv - 15e-6) * 1e8

        total = error_27 + drift * 0.1 + penalty
        return total

    except Exception:
        return 1e6

def main():
    print(f"=== Feedback Network Optimizer (w={W} µm) ===")

    # Start from current best and do a local search
    # Current best: l_top=536, l_bot=174.30 for w=3.0
    if W == 3.0:
        l_top_init = 536
        l_bot_init = 174.30
    elif W == 2.0:
        l_top_init = 353
        l_bot_init = 114.78
    else:
        # Estimate from target current
        # I_div ≈ 10-12 µA → R_total ≈ 417-500 kΩ
        # R ≈ 2000 * l / (w - 0.056), approx
        weff = W - 0.056
        r_unit = 2000 / weff  # ohm per µm length
        r_total_target = 480000  # 480 kΩ
        l_total = r_total_target / r_unit
        l_top_init = l_total * 0.755  # ratio ~ 0.245
        l_bot_init = l_total * 0.245

    print(f"Initial: l_top={l_top_init:.2f}, l_bot={l_bot_init:.2f}")

    # Evaluate initial
    vfb, idiv = get_vfb_and_current(l_top_init, l_bot_init)
    print(f"Initial VFB={vfb:.6f}V, I_div={idiv*1e6:.2f}µA, error={abs(vfb-1.226)*1000:.3f}mV")

    # Try Nelder-Mead optimization
    try:
        from scipy.optimize import minimize
        result = minimize(cost, [l_top_init, l_bot_init], method='Nelder-Mead',
                         options={'xatol': 0.01, 'fatol': 0.001, 'maxiter': 50, 'disp': True})
        l_top_opt, l_bot_opt = result.x
        print(f"\nOptimized: l_top={l_top_opt:.2f}, l_bot={l_bot_opt:.2f}")
        vfb, idiv = get_vfb_and_current(l_top_opt, l_bot_opt)
        print(f"VFB={vfb:.6f}V, I_div={idiv*1e6:.2f}µA, error={abs(vfb-1.226)*1000:.3f}mV")

        vfb_m40, _ = get_vfb_and_current(l_top_opt, l_bot_opt, -40)
        vfb_150, _ = get_vfb_and_current(l_top_opt, l_bot_opt, 150)
        drift = (max(vfb_m40, vfb, vfb_150) - min(vfb_m40, vfb, vfb_150)) * 1000
        print(f"Temp drift: {drift:.3f}mV")

    except ImportError:
        print("scipy not available — skipping optimization")
        # Simple grid search around initial point
        best_cost = cost([l_top_init, l_bot_init])
        best = (l_top_init, l_bot_init)
        for dl_top in range(-5, 6):
            for dl_bot in [-0.5, -0.2, -0.1, 0, 0.1, 0.2, 0.5]:
                lt = l_top_init + dl_top
                lb = l_bot_init + dl_bot
                c = cost([lt, lb])
                if c < best_cost:
                    best_cost = c
                    best = (lt, lb)
        print(f"Best: l_top={best[0]:.2f}, l_bot={best[1]:.2f}, cost={best_cost:.4f}")

if __name__ == '__main__':
    main()
