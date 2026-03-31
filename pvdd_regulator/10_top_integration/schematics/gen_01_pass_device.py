#!/usr/bin/env python3
"""Generate pvdd_01_pass_device.sch — 10x parallel PMOS pass transistor array."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sch_lib import Schematic

S = Schematic()
S.header(
    "Block 01: Pass Device",
    "10x PMOS pfet_g5v0d10v5  W=100u L=0.5u  |  Total W = 1 mm",
    ".subckt pass_device gate bvdd pvdd",
    "PVDD LDO — Pass Device Array"
)

# === Port pins (top-left) ===
S.section("Ports", -250, -900)
S.ipin(-250, -850, "gate")
S.iopin(-250, -800, "bvdd")
S.opin(-250, -750, "pvdd")

# === Layout: two rows of 5 PFETs ===
# Row 1: XM1..XM5   Row 2: XM6..XM10
# Spacing 400 between devices horizontally, 450 between rows vertically
x0, y_r1, y_r2 = 0, -400, 100
dx = 400

S.section("Row 1: XM1 – XM5", x0 - 50, y_r1 - 200)
for i in range(5):
    cx = x0 + i * dx
    S.fet(f"XM{i+1}", "ph", cx, y_r1,
          d="pvdd", g="gate", s="bvdd", b="bvdd",
          w=100, l=0.5)

S.section("Row 2: XM6 – XM10", x0 - 50, y_r2 - 200)
for i in range(5):
    cx = x0 + i * dx
    S.fet(f"XM{i+6}", "ph", cx, y_r2,
          d="pvdd", g="gate", s="bvdd", b="bvdd",
          w=100, l=0.5)

# === Shared supply rails (horizontal wires) ===
S.blank()
S.section("Supply Rails", x0 - 100, -650)

# bvdd rail across top
rail_x1 = x0 + 20 - 50
rail_x2 = x0 + 4 * dx + 20 + 50
S.N(rail_x1, y_r1 - 70, rail_x2, y_r1 - 70, lab="bvdd")
S.N(rail_x1, y_r2 - 70, rail_x2, y_r2 - 70, lab="bvdd")

# pvdd rail across bottom
S.N(rail_x1, y_r1 + 70, rail_x2, y_r1 + 70, lab="pvdd")
S.N(rail_x1, y_r2 + 70, rail_x2, y_r2 + 70, lab="pvdd")

# gate bus
gate_x1 = x0 - 60 - 30
gate_x2 = x0 + 4 * dx - 60 + 30
S.N(gate_x1, y_r1, gate_x2, y_r1, lab="gate")
S.N(gate_x1, y_r2, gate_x2, y_r2, lab="gate")
# vertical gate bus connecting two rows
S.N(gate_x1, y_r1, gate_x1, y_r2, lab="gate")

# === Title annotation ===
S.T("10x PMOS  W=100u  L=0.5u", x0, y_r2 + 200, xm=0.4, ym=0.4, attrs="layer=4")
S.T("Total W = 1 mm  —  Pass Device for PVDD 5V LDO", x0, y_r2 + 250, xm=0.3, ym=0.3, attrs="layer=8")

# Dashed bounding box
S.rect_dash(x0 - 150, y_r1 - 280, x0 + 4 * dx + 120, y_r2 + 170)

S.write("pvdd_01_pass_device.sch")
print("Done: pvdd_01_pass_device.sch")
