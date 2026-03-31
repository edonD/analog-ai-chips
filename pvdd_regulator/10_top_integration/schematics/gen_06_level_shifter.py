#!/usr/bin/env python3
"""Generate pvdd_06_level_shifter.sch — Level Shifter Up (1.8V -> 5V)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sch_lib import Schematic

S = Schematic()
S.header(
    "Block 06: Level Shifter Up",
    "1.8V to 5V level shift  |  HV g5v0d10v5 FETs",
    ".subckt level_shifter_up in out bvdd svdd gnd",
    "PVDD LDO — Level Shifter"
)

# === Port pins ===
S.section("Ports", -250, -900)
S.ipin(-250, -850, "in")
S.iopin(-250, -800, "bvdd")
S.iopin(-250, -750, "svdd")
S.iopin(-250, -700, "gnd")
S.opin(-250, -650, "out")

# Bounding box
S.rect_dash(-100, -620, 1150, 350)

# ================================================================
# Left: Input inverter (XMN_INV bottom, XMP_INV top) — stacked
# ================================================================
ix = 100
iy_n = 100   # NMOS
iy_p = -250  # PMOS

S.section("Input Inverter", ix - 80, -500)

S.fet("XMN_INV", "nh", ix, iy_n,
      d="in_b", g="in", s="gnd", b="gnd", w=2, l=0.5)
S.fet("XMP_INV", "ph", ix, iy_p,
      d="in_b", g="in", s="svdd", b="svdd", w=4, l=0.5)

# ================================================================
# Center: NMOS pull-downs (XMN1, XMN2 side by side)
# ================================================================
nx = 450
ny = 100

S.section("NMOS Pull-downs", nx - 80, -500)

S.fet("XMN1", "nh", nx, ny,
      d="n1", g="in", s="gnd", b="gnd", w=15, l=1)
S.fet("XMN2", "nh", nx + 280, ny,
      d="out", g="in_b", s="gnd", b="gnd", w=15, l=1)

# ================================================================
# Right: Cross-coupled PMOS (XMP1, XMP2 side by side)
# ================================================================
px = 450
py = -300

S.section("Cross-coupled PMOS", px - 80, -500)

S.fet("XMP1", "ph", px, py,
      d="n1", g="out", s="bvdd", b="bvdd", w=4, l=0.5)
S.fet("XMP2", "ph", px + 280, py,
      d="out", g="n1", s="bvdd", b="bvdd", w=5, l=0.5)

# Annotations
S.T("Cross-coupled latch: XMP1.G=out, XMP2.G=n1",
    px - 50, py + 80, xm=0.22, ym=0.22, attrs="layer=13")
S.T("Level Shifter: svdd(1.8V) -> bvdd(5V)",
    -50, 300, xm=0.3, ym=0.3, attrs="layer=8")

S.write("pvdd_06_level_shifter.sch")
print("Done: pvdd_06_level_shifter.sch")
