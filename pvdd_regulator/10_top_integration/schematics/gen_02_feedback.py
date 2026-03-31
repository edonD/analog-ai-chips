#!/usr/bin/env python3
"""Generate pvdd_02_feedback.sch — Resistive feedback divider."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sch_lib import Schematic

S = Schematic()
S.header(
    "Block 02: Feedback Network",
    "Resistive divider: R_TOP=364k, R_BOT=118k  |  vfb = 1.226 V",
    ".subckt feedback_network pvdd vfb gnd",
    "PVDD LDO — Feedback Divider"
)

# === Ports ===
S.section("Ports", -250, -900)
S.iopin(-250, -850, "pvdd")
S.opin(-250, -800, "vfb")
S.iopin(-250, -750, "gnd")

# === Resistor stack — centered at x=400 ===
cx = 400
y_top = -350   # R_TOP center
y_bot = 150    # R_BOT center

S.section("R_TOP: 364 kOhm", cx - 150, y_top - 120)
S.rxh("XR_TOP", cx, y_top,
      p="pvdd", m_net="vfb", b="gnd",
      w=3.0, l=536)

# Value annotation
S.T("R_TOP ~ 364 kOhm", cx + 60, y_top - 10, xm=0.28, ym=0.28, attrs="layer=4")

S.section("R_BOT: 118 kOhm", cx - 150, y_bot - 120)
S.rxh("XR_BOT", cx, y_bot,
      p="vfb", m_net="gnd", b="gnd",
      w=3.0, l=174.30)

S.T("R_BOT ~ 118 kOhm", cx + 60, y_bot - 10, xm=0.28, ym=0.28, attrs="layer=4")

# === Connecting wire: R_TOP bottom to R_BOT top via vfb ===
S.N(cx, y_top + 65, cx, y_bot - 65, lab="vfb")

# === pvdd rail at top ===
S.N(cx, y_top - 65, cx, y_top - 130, lab="pvdd")
S.lab(cx, y_top - 130, 2, "pvdd")

# === gnd rail at bottom ===
S.N(cx, y_bot + 65, cx, y_bot + 130, lab="gnd")
S.lab(cx, y_bot + 130, 2, "gnd")

# === vfb tap label (prominent) ===
S.T("vfb", cx + 25, (y_top + y_bot) // 2 - 15, xm=0.35, ym=0.35, attrs="layer=4")

# === Design equation annotation ===
S.T("vfb = pvdd x 118 / (364 + 118) = 1.226 V", cx - 100, y_bot + 220,
    xm=0.32, ym=0.32, attrs="layer=8")
S.T("(at pvdd = 5.0 V nominal)", cx - 100, y_bot + 260,
    xm=0.25, ym=0.25, attrs="layer=8")

# Dashed bounding box
S.rect_dash(cx - 120, y_top - 180, cx + 250, y_bot + 180)

S.write("pvdd_02_feedback.sch")
print("Done: pvdd_02_feedback.sch")
