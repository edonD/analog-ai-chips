#!/usr/bin/env python3
"""Generate pvdd_09_startup.sch — Startup Circuit
Block 09 of PVDD 5V LDO Regulator."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sch_lib import Schematic

s = Schematic()

# ── Header ──────────────────────────────────────────────────────────────
s.header(
    title="STARTUP — Level-Shift + Detect + Inverter",
    subtitle="Block 09 — 3 MOSFETs + 3 res_xhigh_po + 2 bare R + 1 bare R(Ren)",
    info="bvdd, pvdd, gate, gnd, vref, startup_done, ea_en, ea_out  |  design.cir .subckt startup",
    author="Claude / analog-ai-chips"
)

# ── Port Pins ───────────────────────────────────────────────────────────
px, py = -700, -900
s.section("PORT PINS", px, py - 40)
s.ipin(px,       py,       "bvdd")
s.ipin(px,       py + 40,  "pvdd")
s.ipin(px,       py + 80,  "gnd")
s.ipin(px,       py + 120, "ea_out")
s.ipin(px,       py + 160, "vref")
s.opin(px + 250, py,       "gate")
s.opin(px + 250, py + 40,  "startup_done")
s.opin(px + 250, py + 80,  "ea_en")

# ════════════════════════════════════════════════════════════════════════
# SECTION 1: Bias Divider (left column)
# Rlb1: bvdd → ls_bias, 200k
# Rlb2: ls_bias → gnd, 500k
# ════════════════════════════════════════════════════════════════════════
lx = -350
s.section("BIAS DIVIDER", lx - 100, -650)

s.bare_R("Rlb1", lx, -500, "bvdd", "ls_bias", "200k")
s.bare_R("Rlb2", lx, -300, "ls_bias", "gnd", "500k")

# ════════════════════════════════════════════════════════════════════════
# SECTION 2: CG Level Shifter (center column)
# XMN_cg: NFET common-gate, D=ea_out, G=ls_bias, S=gate, B=gnd
# XR_load: res_xhigh_po bvdd→gate, W=1 L=19
# ════════════════════════════════════════════════════════════════════════
cx = 100
s.section("CG LEVEL SHIFTER", cx - 120, -650)

# XMN_cg NFET: D=ea_out, G=ls_bias, S=gate, B=gnd
s.fet("XMN_cg", "nh", cx, -300,
    d="ea_out", g="ls_bias", s="gate", b="gnd",
    w=1.2e-6, l=4e-6)

# XR_load: bvdd → gate
s.rxh("XR_load", cx + 150, -400, "bvdd", "gate", "gnd", w=1, l=19)

# ════════════════════════════════════════════════════════════════════════
# SECTION 3: EA Enable Tie
# Ren: bvdd → ea_en, 100 ohm
# ════════════════════════════════════════════════════════════════════════
ex = 100
s.section("EA ENABLE", ex - 80, -100)
s.bare_R("Ren", ex, -10, "bvdd", "ea_en", "100")

# ════════════════════════════════════════════════════════════════════════
# SECTION 4: Startup-Done Detector (right column)
# Divider: XR_top (pvdd→sense_mid), XR_bot (sense_mid→gnd)
# Detect NFET: XMN_det, D=det_n, G=sense_mid, S=gnd, B=gnd
# Pull-up: XR_pu (bvdd→det_n)
# Inverter: XMP_inv1, XMN_inv1
# ════════════════════════════════════════════════════════════════════════
rx = 500
s.section("STARTUP-DONE DETECTOR", rx - 120, -650)

# Divider
s.rxh("XR_top", rx, -500, "pvdd", "sense_mid", "gnd", w=2, l=788)
s.rxh("XR_bot", rx, -300, "sense_mid", "gnd", "gnd", w=2, l=212)

# Detect NFET
s.fet("XMN_det", "nh", rx + 200, -300,
    d="det_n", g="sense_mid", s="gnd", b="gnd",
    w=4e-6, l=1e-6)

# Pull-up resistor
s.rxh("XR_pu", rx + 200, -500, "bvdd", "det_n", "gnd", w=1, l=2000)

# Inverter
ix = rx + 450
s.section("INV", ix - 60, -480)
# XMP_inv1: PFET, D=startup_done, G=det_n, S=bvdd, B=bvdd
s.fet("XMP_inv1", "ph", ix, -400,
    d="startup_done", g="det_n", s="bvdd", b="bvdd",
    w=4e-6, l=1e-6)

# XMN_inv1: NFET, D=startup_done, G=det_n, S=gnd, B=gnd
s.fet("XMN_inv1", "nh", ix, -200,
    d="startup_done", g="det_n", s="gnd", b="gnd",
    w=2e-6, l=1e-6)

# ── Dashed outlines ────────────────────────────────────────────────────
s.rect_dash(-500, -620, -200, -200, layer=4)   # bias divider
s.rect_dash(-50, -550, 350, -100, layer=5)     # CG + Ren
s.rect_dash(350, -620, 1100, -100, layer=7)    # detector + inverter

# ── Write ───────────────────────────────────────────────────────────────
sch_path = os.path.join(os.path.dirname(__file__), "pvdd_09_startup.sch")
s.write(sch_path)
print("Done:", sch_path)
