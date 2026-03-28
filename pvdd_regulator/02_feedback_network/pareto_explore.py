#!/usr/bin/env python3
"""Explore Pareto front: area vs MC 3sigma for different W values.
For each W, find optimal l_top, l_bot, then estimate MC sigma.
Uses 100-run MC at each W value to get actual sigma (not just Pelgrom theory).
"""
import subprocess
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_ngspice(code, timeout=30):
    with open('/tmp/_pareto.spice', 'w') as f:
        f.write(code)
    r = subprocess.run(['ngspice', '-b', '/tmp/_pareto.spice'],
                      capture_output=True, text=True, timeout=timeout)
    return r.stdout + r.stderr

def find_optimal_lbot(w, l_top, l_bot_init):
    """Binary search for l_bot that gives VFB closest to 1.226V."""
    lo, hi = l_bot_init * 0.95, l_bot_init * 1.05
    for _ in range(15):
        mid = (lo + hi) / 2
        code = f"""
.include "sky130_res_models.spice"
.subckt fb pvdd vfb gnd
XR_TOP pvdd vfb gnd sky130_fd_pr__res_xhigh_po w={w} l={l_top}
XR_BOT vfb  gnd gnd sky130_fd_pr__res_xhigh_po w={w} l={mid}
.ends
Vpvdd pvdd 0 DC 5.0
Xfb pvdd vfb 0 fb
.control
op
echo "VFB: $&v(vfb)"
echo "IDIV: $&i(Vpvdd)"
quit
.endc
.end
"""
        out = run_ngspice(code)
        vfb = None
        for line in out.split('\n'):
            if line.startswith('VFB:'):
                vfb = float(line.split(':')[1].strip())
        if vfb is None:
            return None, None
        if vfb < 1.226:
            lo = mid
        else:
            hi = mid
    return mid, vfb

def run_mc(w, l_top, l_bot, n_runs=100):
    """Run MC and return sigma."""
    code = f"""
.include "sky130_res_models.spice"
.subckt fb pvdd vfb gnd
XR_TOP pvdd vfb gnd sky130_fd_pr__res_xhigh_po w={w} l={l_top}
XR_BOT vfb  gnd gnd sky130_fd_pr__res_xhigh_po w={w} l={l_bot}
.ends
Vpvdd pvdd 0 DC 5.0
Xfb pvdd vfb 0 fb
.control
alterparam MC_MM_SWITCH = 1
let vfb_results = vector({n_runs})
let run = 0
repeat {n_runs}
  reset
  op
  let vfb_results[run] = v(vfb)
  let run = run + 1
end
let vfb_std = stddev(vfb_results)
let sig3 = vfb_std * 3 * 1000
echo "MC_3SIGMA_MV: $&sig3"
quit
.endc
.end
"""
    out = run_ngspice(code, timeout=120)
    for line in out.split('\n'):
        if line.startswith('MC_3SIGMA_MV:'):
            return float(line.split(':')[1].strip())
    return None

print("=== Pareto Exploration: Area vs MC 3σ ===")
print(f"{'W':>5} {'l_top':>7} {'l_bot':>7} {'Area':>8} {'MC_3σ':>8} {'I_div':>8}")

results = []
for w in [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]:
    # Estimate initial l_top/l_bot for ~10 µA divider current
    weff = w - 0.056
    r_total = 482000
    l_top_est = r_total * 0.755 * weff / 2000
    l_bot_est = r_total * 0.245 * weff / 2000

    l_bot, vfb = find_optimal_lbot(w, l_top_est, l_bot_est)
    if l_bot is None:
        print(f"  w={w}: FAILED to find optimal l_bot")
        continue

    area = w * (l_top_est + l_bot)
    sig3 = run_mc(w, l_top_est, l_bot, 100)
    if sig3 is None:
        print(f"  w={w}: MC FAILED")
        continue

    # Get divider current
    code = f"""
.include "sky130_res_models.spice"
.subckt fb pvdd vfb gnd
XR_TOP pvdd vfb gnd sky130_fd_pr__res_xhigh_po w={w} l={l_top_est}
XR_BOT vfb  gnd gnd sky130_fd_pr__res_xhigh_po w={w} l={l_bot}
.ends
Vpvdd pvdd 0 DC 5.0
Xfb pvdd vfb 0 fb
.control
op
echo "IDIV: $&i(Vpvdd)"
quit
.endc
.end
"""
    out = run_ngspice(code)
    idiv = 0
    for line in out.split('\n'):
        if line.startswith('IDIV:'):
            idiv = abs(float(line.split(':')[1].strip())) * 1e6

    pass_mc = "PASS" if sig3 < 10 else "FAIL"
    print(f"  {w:5.1f} {l_top_est:7.1f} {l_bot:7.2f} {area:7.0f}um² {sig3:7.2f}mV {idiv:7.2f}uA  {pass_mc}")
    results.append((w, l_top_est, l_bot, area, sig3, idiv))

print("\n=== Summary ===")
for w, lt, lb, area, sig3, idiv in results:
    print(f"w={w:.1f}: area={area:.0f}µm², 3σ={sig3:.1f}mV, Idiv={idiv:.1f}µA")
