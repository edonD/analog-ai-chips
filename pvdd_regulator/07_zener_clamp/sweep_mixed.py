#!/usr/bin/env python3
"""Sweep NFET width for mixed stack to find optimal PVT coverage."""
import subprocess, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE = """\
.subckt zener_clamp pvdd gnd
XMd1 pvdd pvdd n4 n4 sky130_fd_pr__nfet_g5v0d10v5 w={wn}e-6 l=4e-6
XMd2 n3   n3   n4 n4 sky130_fd_pr__pfet_g5v0d10v5 w={wp}e-6 l=4e-6
XMd3 n3   n3   n2 n2 sky130_fd_pr__nfet_g5v0d10v5 w={wn}e-6 l=4e-6
XMd4 n1   n1   n2 n2 sky130_fd_pr__pfet_g5v0d10v5 w={wp}e-6 l=4e-6
XMd5 n1   n1   vg vg sky130_fd_pr__nfet_g5v0d10v5 w={wn}e-6 l=4e-6
Rpd vg gnd 500k
Cff n2 vg 30p
XMclamp pvdd vg gnd gnd sky130_fd_pr__nfet_g5v0d10v5 w=100e-6 l=0.5e-6 m=20
XMf1 pvdd pvdd nf6 gnd sky130_fd_pr__nfet_g5v0d10v5 w=10e-6 l=0.5e-6
XMf2 nf6  nf6  nf5 gnd sky130_fd_pr__nfet_g5v0d10v5 w=10e-6 l=0.5e-6
XMf3 nf5  nf5  nf4 gnd sky130_fd_pr__nfet_g5v0d10v5 w=10e-6 l=0.5e-6
XMf4 nf4  nf4  nf3 gnd sky130_fd_pr__nfet_g5v0d10v5 w=10e-6 l=0.5e-6
XMf5 nf3  nf3  nf2 gnd sky130_fd_pr__nfet_g5v0d10v5 w=10e-6 l=0.5e-6
XMf6 nf2  nf2  nf1 gnd sky130_fd_pr__nfet_g5v0d10v5 w=10e-6 l=0.5e-6
XMf7 nf1  nf1  gnd gnd sky130_fd_pr__nfet_g5v0d10v5 w=10e-6 l=0.5e-6
.ends zener_clamp
"""

CORNERS = ["tt", "ss", "ff", "sf", "fs"]
TEMPS = [-40, 27, 150]

TB_TEMPLATE = """\
.lib "../sky130.lib.spice" {corner}
.include "design.cir"
Vpvdd pvdd 0 DC 0
Xclamp pvdd 0 zener_clamp
.option reltol=1e-4
.control
set temp = {temp}
dc Vpvdd 0 8 0.005
let i_clamp = -i(Vpvdd)
let idx = 0
let v_1ma = 0
dowhile idx < length(i_clamp)
  if i_clamp[idx] >= 1m
    let v_1ma = v(pvdd)[idx]
    let idx = length(i_clamp)
  end
  let idx = idx + 1
end
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
echo "onset_V: $&v_1ma"
echo "leak_nA: $&leak_5v_nA"
quit
.endc
.end
"""

def temp_label(t):
    return f"m{abs(t)}c" if t < 0 else f"{t}c"

# Sweep NFET width from 1.8 to 2.6, PFET width = 20u
for wn in [1.8, 2.0, 2.1, 2.2, 2.3, 2.4]:
    wp = 20
    with open("design.cir", "w") as f:
        f.write(TEMPLATE.format(wn=wn, wp=wp))

    n_pass = 0
    fails = []
    for corner in CORNERS:
        for temp in TEMPS:
            tb_name = f"_sweep_tb.spice"
            with open(tb_name, "w") as f:
                f.write(TB_TEMPLATE.format(corner=corner, temp=temp))
            proc = subprocess.run(["ngspice", "-b", tb_name], capture_output=True, text=True, timeout=60)
            out = proc.stdout + proc.stderr
            onset = None
            leak = None
            for line in out.split("\n"):
                m = re.search(r"onset_V:\s+([\d.e+-]+)", line)
                if m: onset = float(m.group(1))
                m = re.search(r"leak_nA:\s+([\d.e+-]+)", line)
                if m: leak = float(m.group(1))

            ok = True
            if temp == 27:
                if onset is None or onset < 5.5 or onset > 6.2: ok = False
                if leak is None or leak > 1000: ok = False
            elif temp == 150:
                if onset is None or onset < 5.0: ok = False
            elif temp == -40:
                if onset is None or onset > 7.0: ok = False

            if ok:
                n_pass += 1
            else:
                fails.append(f"{corner.upper()}{temp}C:onset={onset:.3f}" if onset else f"{corner.upper()}{temp}C:N/A")

    print(f"Wn={wn:.1f}u Wp={wp}u: {n_pass}/15 PASS  fails={','.join(fails[:6])}")

os.remove("_sweep_tb.spice")
