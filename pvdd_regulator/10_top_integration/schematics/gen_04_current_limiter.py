#!/usr/bin/env python3
"""Generate pvdd_04_current_limiter.sch — OCP sense, detect, clamp, flag."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sch_lib import Schematic

S = Schematic()
S.header(
    "Block 04: Current Limiter",
    "Sense PMOS + Rs  |  Detect NFET + Rpu  |  Gate Clamp  |  Flag Inverter",
    ".subckt current_limiter gate bvdd pvdd gnd ilim_flag",
    "PVDD LDO — Over-Current Protection"
)

# === Ports ===
S.section("Ports", -300, -950)
S.ipin(-300, -900, "gate")
S.iopin(-300, -850, "bvdd")
S.iopin(-300, -800, "pvdd")
S.iopin(-300, -750, "gnd")
S.opin(-300, -700, "ilim_flag")

# Layout coordinates — 4 columns, ~400px spacing
col1 = 100    # Sense PMOS + Rs
col2 = 550    # Detect NFET + Rpu
col3 = 1000   # Gate clamp PMOS
col4 = 1450   # Flag inverter

y_fet = -350   # upper devices
y_res = 200    # lower devices / resistors

# ================================================================
# Column 1: XMs (sense PMOS) + XRs (sense resistor)
# ================================================================
S.section("Sense: XMs + XRs", col1 - 100, -600)

# XMs: pfet_g5v0d10v5 w=2 l=0.5 — D=sense_n, G=gate, S=bvdd, B=bvdd
S.fet("XMs", "ph", col1, y_fet,
      d="sense_n", g="gate", s="bvdd", b="bvdd",
      w=2, l=0.5)

# XRs: res_xhigh_po — P=sense_n, M=gnd, B=gnd
S.rxh("XRs", col1 + 20, y_res,
      p="sense_n", m_net="gnd", b="gnd",
      w=1, l=3.12)
S.T("Rs (sense)", col1 + 50, y_res - 10, xm=0.22, ym=0.22, attrs="layer=4")

# Wire: XMs drain (sense_n) down to XRs top (sense_n)
S.N(col1 + 20, y_fet + 70, col1 + 20, y_res - 65, lab="sense_n")

# ================================================================
# Column 2: XMdet (detect NFET) + XRpu (pull-up resistor)
# ================================================================
S.section("Detect: XMdet + XRpu", col2 - 100, -600)

# XMdet: nfet_g5v0d10v5 w=5 l=1 — D=det_n, G=sense_n, S=gnd, B=gnd
S.fet("XMdet", "nh", col2, y_fet,
      d="det_n", g="sense_n", s="gnd", b="gnd",
      w=5, l=1)

# XRpu: res_xhigh_po — P=bvdd, M=det_n, B=gnd
S.rxh("XRpu", col2 + 20, y_fet - 250,
      p="bvdd", m_net="det_n", b="gnd",
      w=1, l=5)
S.T("Rpu (pull-up)", col2 + 50, y_fet - 260, xm=0.22, ym=0.22, attrs="layer=4")

# Wire: XRpu bottom (det_n) to XMdet drain (det_n) — already connected via net name

# ================================================================
# Column 3: XMclamp (gate clamp PMOS)
# ================================================================
S.section("Clamp: XMclamp", col3 - 100, -600)

# XMclamp: pfet_g5v0d10v5 w=20 l=1 — D=gate, G=det_n, S=bvdd, B=bvdd
S.fet("XMclamp", "ph", col3, y_fet,
      d="gate", g="det_n", s="bvdd", b="bvdd",
      w=20, l=1)
S.T("Gate clamp", col3 - 30, y_fet + 100, xm=0.25, ym=0.25, attrs="layer=4")
S.T("Pulls gate toward bvdd", col3 - 50, y_fet + 135, xm=0.2, ym=0.2, attrs="layer=8")
S.T("when Ilim tripped", col3 - 50, y_fet + 165, xm=0.2, ym=0.2, attrs="layer=8")

# ================================================================
# Column 4: Flag inverter (XMfp + XMfn)
# ================================================================
S.section("Flag Inverter: XMfp / XMfn", col4 - 100, -600)

y_pflag = y_fet - 50
y_nflag = y_fet + 400

# XMfp: pfet_g5v0d10v5 w=2 l=1 — D=ilim_flag, G=det_n, S=pvdd, B=pvdd
S.fet("XMfp", "ph", col4, y_pflag,
      d="ilim_flag", g="det_n", s="pvdd", b="pvdd",
      w=2, l=1)

# XMfn: nfet_g5v0d10v5 w=2 l=1 — D=ilim_flag, G=det_n, S=gnd, B=gnd
S.fet("XMfn", "nh", col4, y_nflag,
      d="ilim_flag", g="det_n", s="gnd", b="gnd",
      w=2, l=1)

# Wire: XMfp drain to XMfn drain (ilim_flag) — vertical connection
S.N(col4 + 20, y_pflag + 70, col4 + 20, y_nflag - 70, lab="ilim_flag")

S.T("ilim_flag", col4 + 50, (y_pflag + y_nflag) // 2, xm=0.28, ym=0.28, attrs="layer=4")
S.T("HIGH = current limit active", col4 - 20, y_nflag + 130, xm=0.22, ym=0.22, attrs="layer=8")

# === Bounding boxes per section ===
S.rect_dash(col1 - 130, y_fet - 150, col1 + 160, y_res + 120)
S.rect_dash(col2 - 130, y_fet - 380, col2 + 160, y_fet + 120)
S.rect_dash(col3 - 130, y_fet - 150, col3 + 160, y_fet + 120)
S.rect_dash(col4 - 130, y_pflag - 150, col4 + 160, y_nflag + 120)

# === Overall annotation ===
S.T("OCP: If load current causes Vs(sense_n) > Vth(XMdet), det_n goes LOW,",
    col1 - 100, y_res + 250, xm=0.25, ym=0.25, attrs="layer=8")
S.T("XMclamp turns ON pulling gate toward bvdd (limiting Ids), flag goes HIGH.",
    col1 - 100, y_res + 290, xm=0.25, ym=0.25, attrs="layer=8")

S.write("pvdd_04_current_limiter.sch")
print("Done: pvdd_04_current_limiter.sch")
