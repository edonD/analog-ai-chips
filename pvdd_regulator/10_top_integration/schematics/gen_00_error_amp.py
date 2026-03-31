#!/usr/bin/env python3
"""Generate pvdd_00_error_amp.sch — Error Amplifier (Two-Stage Miller OTA)
Block 00 of PVDD 5V LDO Regulator."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sch_lib import Schematic

s = Schematic()

# ── Header ──────────────────────────────────────────────────────────────
s.header(
    title="ERROR AMPLIFIER — Two-Stage Miller OTA",
    subtitle="Block 00 — 12 MOSFETs + Cc + Rc",
    info="vref(+), vfb(-), vout_gate(out), pvdd, gnd, ibias, en  |  design.cir .subckt error_amp",
    author="Claude / analog-ai-chips"
)

# ── Port Pins ───────────────────────────────────────────────────────────
px, py = -600, -900
s.section("PORT PINS", px, py - 40)
s.ipin(px,      py,      "vref")
s.ipin(px,      py + 40, "vfb")
s.ipin(px,      py + 80, "ibias")
s.ipin(px,      py + 120,"en")
s.ipin(px,      py + 160,"pvdd")
s.ipin(px,      py + 200,"gnd")
s.opin(px + 200,py,      "vout_gate")

# ════════════════════════════════════════════════════════════════════════
# SECTION 1: Enable Logic  (top band, y ~ -600)
# ════════════════════════════════════════════════════════════════════════
en_y = -600
s.section("ENABLE LOGIC", -300, en_y - 80)

# XMen  — NMOS pass gate: passes ibias when en=high → ibias_en
#   D=ibias_en  G=en  S=ibias  B=gnd
s.fet("XMen", "nh", -100, en_y,
      d="ibias_en", g="en", s="ibias", b="gnd",
      w=20, l=1, m=1)

# XMpu  — PMOS pull-up: pulls vout_gate to pvdd when en=low (shutdown)
#   D=vout_gate  G=en  S=pvdd  B=pvdd
s.fet("XMpu", "ph", 350, en_y,
      d="vout_gate", g="en", s="pvdd", b="pvdd",
      w=20, l=1, m=1)

# ════════════════════════════════════════════════════════════════════════
# SECTION 2: Bias Chain  (left column, x ~ -400)
# ════════════════════════════════════════════════════════════════════════
bx = -400
s.section("BIAS CHAIN", bx - 100, -350)

# XMbn0 — NMOS diode-connected bias (ibias_en mirror input)
#   D=ibias_en  G=ibias_en  S=gnd  B=gnd
s.fet("XMbn0", "nh", bx, -200,
      d="ibias_en", g="ibias_en", s="gnd", b="gnd",
      w=20, l=8, m=1)

# XMbn_pb — NMOS mirror: ibias_en → pb_tail (wide mirror m=200)
#   D=pb_tail  G=ibias_en  S=gnd  B=gnd
s.fet("XMbn_pb", "nh", bx, 200,
      d="pb_tail", g="ibias_en", s="gnd", b="gnd",
      w=20, l=8, m=200)

# XMbp0 — PMOS diode-connected (pb_tail mirror input)
#   D=pb_tail  G=pb_tail  S=pvdd  B=pvdd
s.fet("XMbp0", "ph", bx + 400, -200,
      d="pb_tail", g="pb_tail", s="pvdd", b="pvdd",
      w=20, l=4, m=4)

# ════════════════════════════════════════════════════════════════════════
# SECTION 3: Stage 1 — Differential Pair + Mirror Load  (center)
# ════════════════════════════════════════════════════════════════════════
# Layout:      XMtail (PMOS tail) at top center
#              XM1      XM2  (PMOS diff pair) below
#              XMn_l    XMn_r (NMOS mirror load) at bottom

cx = 400   # center X for diff pair
s.section("STAGE 1 — DIFF PAIR", cx - 200, -380)

# XMtail — PMOS tail current source
#   D=tail_s  G=pb_tail  S=pvdd  B=pvdd
tail_y = -250
s.fet("XMtail", "ph", cx, tail_y,
      d="tail_s", g="pb_tail", s="pvdd", b="pvdd",
      w=20, l=4, m=4)

# XM1 — PMOS diff input (+), gate = vref
#   D=d1  G=vref  S=tail_s  B=pvdd
dp_y = 100
dp_sep = 400  # horizontal separation between M1 and M2
m1x = cx - dp_sep // 2   # 200
m2x = cx + dp_sep // 2   # 600

s.fet("XM1", "ph", m1x, dp_y,
      d="d1", g="vref", s="tail_s", b="pvdd",
      w=80, l=4, m=2)

# XM2 — PMOS diff input (-), gate = vfb
#   D=d2  G=vfb  S=tail_s  B=pvdd
s.fet("XM2", "ph", m2x, dp_y,
      d="d2", g="vfb", s="tail_s", b="pvdd",
      w=80, l=4, m=2)

# XMn_l — NMOS mirror load (diode-connected, left)
#   D=d1  G=d1  S=gnd  B=gnd
load_y = 450
s.fet("XMn_l", "nh", m1x, load_y,
      d="d1", g="d1", s="gnd", b="gnd",
      w=20, l=8, m=2)

# XMn_r — NMOS mirror load (right)
#   D=d2  G=d1  S=gnd  B=gnd
s.fet("XMn_r", "nh", m2x, load_y,
      d="d2", g="d1", s="gnd", b="gnd",
      w=20, l=8, m=2)

# ── Wires: diff pair drains → mirror load drains ──
# M1 drain (d1): from PFET bottom (m1x+20, dp_y+70) down to NFET top (m1x+20, load_y-70)
s.N(m1x + 20, dp_y + 70, m1x + 20, load_y - 70, lab="d1")
s.net_text("d1", m1x + 30, (dp_y + 70 + load_y - 70) // 2)

# M2 drain (d2): from PFET bottom (m2x+20, dp_y+70) down to NFET top (m2x+20, load_y-70)
s.N(m2x + 20, dp_y + 70, m2x + 20, load_y - 70, lab="d2")
s.net_text("d2", m2x + 30, (dp_y + 70 + load_y - 70) // 2)

# ════════════════════════════════════════════════════════════════════════
# SECTION 4: Stage 2 — Common-Source Gain  (right column)
# ════════════════════════════════════════════════════════════════════════
s2x = 1050
s.section("STAGE 2 — CS GAIN", s2x - 150, -380)

# XMp_ld — PMOS active load for stage 2
#   D=vout_gate  G=pb_tail  S=pvdd  B=pvdd
s.fet("XMp_ld", "ph", s2x, -200,
      d="vout_gate", g="pb_tail", s="pvdd", b="pvdd",
      w=20, l=4, m=8)

# XMcs — NMOS common-source amp
#   D=vout_gate  G=d2  S=gnd  B=gnd
s.fet("XMcs", "nh", s2x, 200,
      d="vout_gate", g="d2", s="gnd", b="gnd",
      w=20, l=1, m=1)

# Wire: XMp_ld drain → XMcs drain (vout_gate)
s.N(s2x + 20, -200 + 70, s2x + 20, 200 - 70, lab="vout_gate")
s.net_text("vout_gate", s2x + 30, 0)

# ════════════════════════════════════════════════════════════════════════
# SECTION 5: Miller Compensation  (far right)
# ════════════════════════════════════════════════════════════════════════
comp_x = 1450
s.section("MILLER COMP", comp_x - 100, -380)

# Cc — 30pF cap: d2 to comp_mid
s.bare_C("Cc", comp_x, -100, "d2", "comp_mid", "30p")

# Rc — 25k resistor: comp_mid to vout_gate
s.bare_R("Rc", comp_x, 200, "comp_mid", "vout_gate", "25k")

# Wire: Cc bottom → Rc top (comp_mid)
s.N(comp_x, -100 + 65, comp_x, 200 - 65, lab="comp_mid")
s.net_text("comp_mid", comp_x + 15, 50)

# ── Dashed section boxes ───────────────────────────────────────────────
s.rect_dash(-350, en_y - 120, 600, en_y + 120)       # enable logic
s.rect_dash(bx - 150, -350, bx + 550, 350)            # bias chain
s.rect_dash(cx - 350, -380, cx + 450, 600)            # stage 1
s.rect_dash(s2x - 200, -380, s2x + 200, 350)         # stage 2
s.rect_dash(comp_x - 120, -380, comp_x + 120, 350)   # compensation

# ── Write ───────────────────────────────────────────────────────────────
out = os.path.join(os.path.dirname(__file__), "pvdd_00_error_amp.sch")
s.write(out)
print(f"Done: {out}")
