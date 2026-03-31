#!/usr/bin/env python3
"""Generate pvdd_03_compensation.sch — Miller Cc, Rz, and output Cout."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sch_lib import Schematic

S = Schematic()
S.header(
    "Block 03: Compensation Network",
    "Miller Cc ~ 30 pF  |  Rz ~ 5 kOhm  |  Cout ~ 70 pF",
    ".subckt compensation vout_gate pvdd gnd",
    "PVDD LDO — Compensation"
)

# === Ports ===
S.section("Ports", -250, -900)
S.ipin(-250, -850, "vout_gate")
S.iopin(-250, -800, "pvdd")
S.iopin(-250, -750, "gnd")

# === Miller comp: Cc → Rz → pvdd (left group) ===
cc_x = 100
rz_x = 550
cout_x = 1050
cy = -200

S.section("Miller Compensation: Cc + Rz", cc_x - 80, cy - 250)

# Cc: MIM cap, top=vout_gate, bottom=cc_mid
S.mim("XCc", cc_x, cy,
      c0="vout_gate", c1="cc_mid",
      w=122, l=122, mf=1)
S.T("Cc ~ 30 pF", cc_x - 30, cy + 90, xm=0.28, ym=0.28, attrs="layer=4")

# Rz: res_xhigh_po, P=cc_mid, M=pvdd, B=gnd
S.rxh("XRz", rz_x, cy,
      p="cc_mid", m_net="pvdd", b="gnd",
      w=4, l=10)
S.T("Rz ~ 5 kOhm", rz_x - 20, cy + 90, xm=0.28, ym=0.28, attrs="layer=4")

# Wire: Cc bottom (cc_mid) to Rz top (cc_mid) — horizontal
S.N(cc_x, cy + 65, cc_x, cy + 120, lab="cc_mid")
S.N(cc_x, cy + 120, rz_x, cy + 120, lab="cc_mid")
S.N(rz_x, cy + 120, rz_x, cy + 65, lab="cc_mid")
# Flip: actually Cc bottom goes down, Rz P goes up. Let's use shared label.
# The labels on the components already connect them via "cc_mid" net name.

# === Output cap: Cout from pvdd to gnd (right group) ===
S.section("Output Capacitor: Cout", cout_x - 80, cy - 250)

S.mim("XCout", cout_x, cy,
      c0="pvdd", c1="gnd",
      w=187, l=187, mf=1)
S.T("Cout ~ 70 pF", cout_x - 30, cy + 90, xm=0.28, ym=0.28, attrs="layer=4")

# === Signal flow annotation ===
S.T("vout_gate (ea_out)", cc_x - 40, cy - 130, xm=0.25, ym=0.25, attrs="layer=8")

# Arrow-like annotation: Cc → Rz → pvdd
S.T("Cc  ──►  Rz  ──►  pvdd", (cc_x + rz_x) // 2 - 50, cy + 180,
    xm=0.3, ym=0.3, attrs="layer=8")
S.T("Miller compensation with zero-nulling resistor", (cc_x + rz_x) // 2 - 80, cy + 220,
    xm=0.25, ym=0.25, attrs="layer=8")

# Dashed boxes
S.rect_dash(cc_x - 80, cy - 200, rz_x + 100, cy + 150)
S.rect_dash(cout_x - 80, cy - 200, cout_x + 100, cy + 150)

S.write("pvdd_03_compensation.sch")
print("Done: pvdd_03_compensation.sch")
