#!/usr/bin/env python3
"""Fine-tune 2N3P stack: sweep NFET W and PFET W."""
import subprocess, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def make_2n3p(wn, wp):
    return f""".subckt zener_clamp pvdd gnd
XMd1 n4   n4   pvdd pvdd sky130_fd_pr__pfet_g5v0d10v5 w={wp}e-6 l=4e-6
XMd2 n3   n3   n4 n4 sky130_fd_pr__nfet_g5v0d10v5 w={wn}e-6 l=4e-6
XMd3 n2   n2   n3 n3 sky130_fd_pr__pfet_g5v0d10v5 w={wp}e-6 l=4e-6
XMd4 n2   n2   n1 n1 sky130_fd_pr__nfet_g5v0d10v5 w={wn}e-6 l=4e-6
XMd5 vg   vg   n1 n1 sky130_fd_pr__pfet_g5v0d10v5 w={wp}e-6 l=4e-6
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

configs = [
    (2.2, 20), (2.5, 20), (2.8, 20), (3.0, 20),
    (2.2, 25), (2.5, 25), (2.8, 25), (3.0, 25),
    (2.2, 30), (2.5, 30), (3.0, 30),
    (3.5, 25), (3.5, 30),
]

for wn, wp in configs:
    with open("design.cir", "w") as f:
        f.write(make_2n3p(wn, wp))

    n_pass = 0
    d = {}
    for corner in CORNERS:
        for temp in TEMPS:
            with open("_s4.spice", "w") as f:
                f.write(TB_TEMPLATE.format(corner=corner, temp=temp))
            proc = subprocess.run(["ngspice", "-b", "_s4.spice"], capture_output=True, text=True, timeout=60)
            out = proc.stdout + proc.stderr
            onset = leak = None
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
            if ok: n_pass += 1
            d[f"{corner.upper()}{temp}"] = (onset, leak, ok)

    ss27 = d["SS27"]; ff27 = d["FF27"]; sf27 = d["SF27"]; fs27 = d["FS27"]
    tt27 = d["TT27"]; tt150 = d["TT150"]; ff150 = d["FF150"]; sf150 = d["SF150"]
    ss_m40 = d["SS-40"]
    print(f"Wn={wn} Wp={wp}: {n_pass}/15 | TT27={tt27[0]:.3f} | SS27={ss27[0]:.3f} SS-40={ss_m40[0]:.3f} | FF27leak={ff27[1]:.0f} | SF27={sf27[0]:.3f} FS27={fs27[0]:.3f} | FF150={ff150[0]:.3f} SF150={sf150[0]:.3f}")

os.remove("_s4.spice")
