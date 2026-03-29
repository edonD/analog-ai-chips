#!/usr/bin/env python3
"""Sweep NFET L and PFET W for mixed stack to find optimal PVT."""
import subprocess, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE = """\
.subckt zener_clamp pvdd gnd
XMd1 pvdd pvdd n4 n4 sky130_fd_pr__nfet_g5v0d10v5 w={wn}e-6 l={ln}e-6
XMd2 n3   n3   n4 n4 sky130_fd_pr__pfet_g5v0d10v5 w={wp}e-6 l=4e-6
XMd3 n3   n3   n2 n2 sky130_fd_pr__nfet_g5v0d10v5 w={wn}e-6 l={ln}e-6
XMd4 n1   n1   n2 n2 sky130_fd_pr__pfet_g5v0d10v5 w={wp}e-6 l=4e-6
XMd5 n1   n1   vg vg sky130_fd_pr__nfet_g5v0d10v5 w={wn}e-6 l={ln}e-6
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

CORNERS = ["tt", "ss", "ff", "sf", "fs"]
TEMPS = [-40, 27, 150]

# Try different combinations
configs = [
    # (Wn, Ln, Wp, description)
    (2.2, 4, 20, "baseline mixed"),
    (2.2, 4, 25, "wider PFET"),
    (2.2, 4, 30, "much wider PFET"),
    (3.0, 4, 20, "wider NFET Wn=3"),
    (2.2, 4, 15, "narrower PFET"),
    (1.5, 4, 20, "narrow NFET like v9"),
    (2.0, 4, 30, "Wn=2 Wp=30"),
    (2.5, 4, 25, "Wn=2.5 Wp=25"),
]

for wn, ln, wp, desc in configs:
    with open("design.cir", "w") as f:
        f.write(TEMPLATE.format(wn=wn, ln=ln, wp=wp))

    n_pass = 0
    details = {}
    for corner in CORNERS:
        for temp in TEMPS:
            tb_name = "_sweep2_tb.spice"
            with open(tb_name, "w") as f:
                f.write(TB_TEMPLATE.format(corner=corner, temp=temp))
            proc = subprocess.run(["ngspice", "-b", tb_name], capture_output=True, text=True, timeout=60)
            out = proc.stdout + proc.stderr
            onset = None; leak = None
            for line in out.split("\n"):
                m = re.search(r"onset_V:\s+([\d.e+-]+)", line)
                if m: onset = float(m.group(1))
                m = re.search(r"leak_nA:\s+([\d.e+-]+)", line)
                if m: leak = float(m.group(1))

            ok = True; key = f"{corner.upper()}{temp}"
            if temp == 27:
                if onset is None or onset < 5.5 or onset > 6.2: ok = False
                if leak is None or leak > 1000: ok = False
            elif temp == 150:
                if onset is None or onset < 5.0: ok = False
            elif temp == -40:
                if onset is None or onset > 7.0: ok = False
            if ok: n_pass += 1
            details[key] = (onset, leak, ok)

    # Show key corners
    ss27 = details.get("SS27", (None,None,False))
    ff27 = details.get("FF27", (None,None,False))
    ff150 = details.get("FF150", (None,None,False))
    sf150 = details.get("SF150", (None,None,False))
    print(f"Wn={wn} Ln={ln} Wp={wp} ({desc}): {n_pass}/15 | SS27={ss27[0]:.3f}V FF27leak={ff27[1]:.0f}nA FF150={ff150[0]:.3f}V SF150={sf150[0]:.3f}V")

os.remove("_sweep2_tb.spice")
