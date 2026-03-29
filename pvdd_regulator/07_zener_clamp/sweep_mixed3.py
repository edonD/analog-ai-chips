#!/usr/bin/env python3
"""Try different N/P ratios in the stack."""
import subprocess, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 5-device stacks with different N/P mixes
STACKS = {
    "5N0P": [
        ("n", 2.2, 4), ("n", 2.2, 4), ("n", 2.2, 4), ("n", 2.2, 4), ("n", 2.2, 4)
    ],
    "3N2P": [
        ("n", 2.2, 4), ("p", 20, 4), ("n", 2.2, 4), ("p", 20, 4), ("n", 2.2, 4)
    ],
    "2N3P": [
        ("p", 20, 4), ("n", 2.2, 4), ("p", 20, 4), ("n", 2.2, 4), ("p", 20, 4)
    ],
    "1N4P": [
        ("p", 20, 4), ("p", 20, 4), ("n", 2.2, 4), ("p", 20, 4), ("p", 20, 4)
    ],
    "4N1P": [
        ("n", 2.2, 4), ("n", 2.2, 4), ("p", 20, 4), ("n", 2.2, 4), ("n", 2.2, 4)
    ],
}

def make_design(stack_cfg):
    lines = [".subckt zener_clamp pvdd gnd"]
    nodes = ["pvdd"] + [f"n{i}" for i in range(len(stack_cfg)-1, 0, -1)] + ["vg"]
    for i, (dtype, w, l) in enumerate(stack_cfg):
        high = nodes[i]
        low = nodes[i+1]
        if dtype == "n":
            # NFET diode: D=G=high, S=B=low
            lines.append(f"XMd{i+1} {high} {high} {low} {low} sky130_fd_pr__nfet_g5v0d10v5 w={w}e-6 l={l}e-6")
        else:
            # PFET diode: S=B=high, D=G=low
            lines.append(f"XMd{i+1} {low} {low} {high} {high} sky130_fd_pr__pfet_g5v0d10v5 w={w}e-6 l={l}e-6")
    lines.append("Rpd vg gnd 500k")
    lines.append("Cff n2 vg 30p")
    lines.append("XMclamp pvdd vg gnd gnd sky130_fd_pr__nfet_g5v0d10v5 w=100e-6 l=0.5e-6 m=20")
    for j in range(7):
        h = "pvdd" if j == 0 else f"nf{7-j}"
        lo = "gnd" if j == 6 else f"nf{6-j}"
        lines.append(f"XMf{j+1} {h} {h} {lo} gnd sky130_fd_pr__nfet_g5v0d10v5 w=10e-6 l=0.5e-6")
    lines.append(".ends zener_clamp")
    return "\n".join(lines) + "\n"

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

for name, stack in STACKS.items():
    with open("design.cir", "w") as f:
        f.write(make_design(stack))

    results = {}
    n_pass = 0
    for corner in CORNERS:
        for temp in TEMPS:
            with open("_s3_tb.spice", "w") as f:
                f.write(TB_TEMPLATE.format(corner=corner, temp=temp))
            proc = subprocess.run(["ngspice", "-b", "_s3_tb.spice"], capture_output=True, text=True, timeout=60)
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
            results[f"{corner.upper()}{temp}"] = (onset, leak, ok)

    tt27 = results["TT27"]
    tt150 = results["TT150"]
    ss27 = results["SS27"]
    ff27 = results["FF27"]
    sf27 = results["SF27"]
    fs27 = results["FS27"]
    ff150 = results["FF150"]
    sf150 = results["SF150"]
    tc = (tt150[0] - results["TT-40"][0]) / 190 * 1000 if tt150[0] and results["TT-40"][0] else 0

    print(f"{name}: {n_pass}/15 | TT27={tt27[0]:.3f} TT150={tt150[0]:.3f} TC={tc:.1f}mV/C | SS27={ss27[0]:.3f} FF27={ff27[0]:.3f}(leak={ff27[1]:.0f}) | SF27={sf27[0]:.3f} FS27={fs27[0]:.3f} | FF150={ff150[0]:.3f} SF150={sf150[0]:.3f}")

os.remove("_s3_tb.spice")
