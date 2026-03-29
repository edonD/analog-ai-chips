#!/usr/bin/env python3
"""
run_pvt_sweep.py — Full PVT sweep: 5 corners x 3 temps = 15 points
Generates a SPICE testbench for each (corner, temp) combination, runs it,
and collects onset (1mA) and leakage (5V) data.
"""
import subprocess, re, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CORNERS = ["tt", "ss", "ff", "sf", "fs"]
TEMPS = [-40, 27, 150]

TB_TEMPLATE = """\
* tb_pvt_{corner}_{temp_label}.spice — PVT sweep: {corner} {temp}C
.lib "../sky130.lib.spice" {corner}
.include "design.cir"

Vpvdd pvdd 0 DC 0
Xclamp pvdd 0 zener_clamp

.option reltol=1e-4

.control
set temp = {temp}
dc Vpvdd 0 8 0.005
let i_clamp = -i(Vpvdd)

* --- Onset at 1mA ---
let idx = 0
let v_1ma = 0
dowhile idx < length(i_clamp)
  if i_clamp[idx] >= 1m
    let v_1ma = v(pvdd)[idx]
    let idx = length(i_clamp)
  end
  let idx = idx + 1
end

* --- Leakage at 5.0V ---
let idx = 0
let leak_5v = 0
dowhile idx < length(i_clamp)
  if v(pvdd)[idx] >= 4.998 & v(pvdd)[idx] <= 5.002
    let leak_5v = i_clamp[idx]
    let idx = length(i_clamp)
  end
  let idx = idx + 1
end
let leak_5v_nA = leak_5v * 1e9

echo "pvt_{corner}_{temp_label}_onset_1mA_V: $&v_1ma"
echo "pvt_{corner}_{temp_label}_leakage_nA: $&leak_5v_nA"

quit
.endc
.end
"""

def temp_label(t):
    if t < 0:
        return f"m{abs(t)}c"
    else:
        return f"{t}c"

results = []
print("=" * 72)
print("Full PVT Sweep: 5 corners x 3 temps = 15 points")
print("=" * 72)

for corner in CORNERS:
    for temp in TEMPS:
        tl = temp_label(temp)
        tb_name = f"tb_pvt_{corner}_{tl}.spice"
        tb_content = TB_TEMPLATE.format(corner=corner, temp=temp, temp_label=tl)
        with open(tb_name, "w") as f:
            f.write(tb_content)

        proc = subprocess.run(
            ["ngspice", "-b", tb_name],
            capture_output=True, text=True, timeout=120
        )
        output = proc.stdout + proc.stderr

        onset = None
        leakage = None
        for line in output.split("\n"):
            m = re.search(rf"pvt_{corner}_{tl}_onset_1mA_V:\s+([\d.e+-]+)", line)
            if m:
                onset = float(m.group(1))
            m = re.search(rf"pvt_{corner}_{tl}_leakage_nA:\s+([\d.e+-]+)", line)
            if m:
                leakage = float(m.group(1))

        # Determine pass/fail for onset
        if temp == 27:
            onset_spec = "5.5-6.2V"
            if onset is not None:
                onset_pass = 5.5 <= onset <= 6.2
            else:
                onset_pass = False
        elif temp == 150:
            onset_spec = ">= 5.0V"
            if onset is not None:
                onset_pass = onset >= 5.0
            else:
                onset_pass = False
        elif temp == -40:
            onset_spec = "<= 7.0V"
            if onset is not None:
                onset_pass = onset <= 7.0
            else:
                onset_pass = False
        else:
            onset_spec = "N/A"
            onset_pass = True

        # Leakage check (only at 27C per spec)
        if temp == 27:
            leak_spec = "<= 1000 nA"
            leak_pass = leakage is not None and leakage <= 1000
        else:
            leak_spec = "info only"
            leak_pass = True

        status = "PASS" if (onset_pass and leak_pass) else "FAIL"

        results.append({
            "corner": corner.upper(),
            "temp": temp,
            "onset": onset,
            "leakage": leakage,
            "onset_spec": onset_spec,
            "onset_pass": onset_pass,
            "leak_spec": leak_spec,
            "leak_pass": leak_pass,
            "status": status,
        })

        onset_str = f"{onset:.3f}V" if onset else "N/A"
        leak_str = f"{leakage:.1f}nA" if leakage else "N/A"
        pass_str = "PASS" if onset_pass else "FAIL"
        print(f"  {corner.upper():>2s} {temp:>4d}C: onset={onset_str:>8s}  leak={leak_str:>12s}  [{pass_str}]")

        # Clean up temp file
        os.remove(tb_name)

# Summary table
print()
print("=" * 72)
print(f"{'Corner':>6s} {'Temp':>5s} {'Onset(1mA)':>11s} {'Spec':>12s} {'Status':>6s} | {'Leak@5V':>10s} {'Spec':>12s} {'Status':>6s}")
print("-" * 72)

n_pass = 0
n_fail = 0
for r in results:
    onset_str = f"{r['onset']:.3f}V" if r['onset'] else "N/A"
    leak_str = f"{r['leakage']:.1f}nA" if r['leakage'] else "N/A"
    o_stat = "PASS" if r['onset_pass'] else "FAIL"
    l_stat = "PASS" if r['leak_pass'] else "FAIL"
    overall = r['status']
    if overall == "PASS":
        n_pass += 1
    else:
        n_fail += 1
    print(f"{r['corner']:>6s} {r['temp']:>4d}C {onset_str:>11s} {r['onset_spec']:>12s} {o_stat:>6s} | {leak_str:>10s} {r['leak_spec']:>12s} {l_stat:>6s}")

print("-" * 72)
print(f"PVT Summary: {n_pass}/15 PASS, {n_fail}/15 FAIL")

# Find worst cases
worst_onset_low = min((r for r in results if r['onset']), key=lambda r: r['onset'])
worst_onset_high = max((r for r in results if r['onset']), key=lambda r: r['onset'])
worst_leak = max((r for r in results if r['leakage']), key=lambda r: r['leakage'])

print(f"\nWorst-case onset (low):  {worst_onset_low['corner']} {worst_onset_low['temp']}C = {worst_onset_low['onset']:.3f}V")
print(f"Worst-case onset (high): {worst_onset_high['corner']} {worst_onset_high['temp']}C = {worst_onset_high['onset']:.3f}V")
print(f"Worst-case leakage:      {worst_leak['corner']} {worst_leak['temp']}C = {worst_leak['leakage']:.1f}nA")
