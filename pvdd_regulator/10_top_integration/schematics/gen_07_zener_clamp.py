#!/usr/bin/env python3
"""Generate pvdd_07_zener_clamp.sch — Zener Clamp
Block 07 of PVDD 5V LDO Regulator."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sch_lib import Schematic

s = Schematic()

# ── Header ──────────────────────────────────────────────────────────────
s.header(
    title="ZENER CLAMP — Precision N-P-N-P-N Stack + Fast Diode Clamp",
    subtitle="Block 07 — 12 MOSFETs + 1 Resistor",
    info="pvdd, gnd  |  design.cir .subckt zener_clamp",
    author="Claude / analog-ai-chips"
)

# ── Port Pins ───────────────────────────────────────────────────────────
px, py = -600, -900
s.section("PORT PINS", px, py - 40)
s.iopin(px,       py,      "pvdd")
s.iopin(px,       py + 40, "gnd")

# ════════════════════════════════════════════════════════════════════════
# SECTION 1: Precision N-P-N-P-N stack (left column)
# XMd1(N)→XMd2(P)→XMd3(N)→XMd4(P)→XMd5(N) → Rpd → gnd
# All diode-connected. pvdd at top, vg at bottom.
# ════════════════════════════════════════════════════════════════════════
lcx = -200  # left column x
s.section("PRECISION N-P-N-P-N STACK", lcx - 120, -750)

# Spacing: each FET occupies ~130 vertical units in stacked config
# y positions top-to-bottom
ys = [-600, -440, -280, -120, 40]

# XMd1: NFET diode, D=pvdd, G=pvdd, S=n4, B=n4
s.fet_stacked("XMd1", "nh", lcx, ys[0],
    d="pvdd", g="pvdd", s="n4", b="n4",
    w=2.2e-6, l=4e-6, top_len=70, bot_len=50)

# XMd2: PFET diode, D=n4, G=n3, S=n3, B=n4  (diode: G=D tied=n3; S tied to n4 for PFET top=S)
# PFET: top=S=n4, bottom=D=n3; G=n3, B=n4
s.fet_stacked("XMd2", "ph", lcx, ys[1],
    d="n3", g="n3", s="n4", b="n4",
    w=20e-6, l=4e-6, top_len=50, bot_len=50)

# XMd3: NFET diode, D=n3, G=n3, S=n2, B=n2
s.fet_stacked("XMd3", "nh", lcx, ys[2],
    d="n3", g="n3", s="n2", b="n2",
    w=2.2e-6, l=4e-6, top_len=50, bot_len=50)

# XMd4: PFET diode, D=n1, G=n1, S=n2, B=n2
s.fet_stacked("XMd4", "ph", lcx, ys[3],
    d="n1", g="n1", s="n2", b="n2",
    w=20e-6, l=4e-6, top_len=50, bot_len=50)

# XMd5: NFET diode, D=n1, G=n1, S=vg, B=vg
s.fet_stacked("XMd5", "nh", lcx, ys[4],
    d="n1", g="n1", s="vg", b="vg",
    w=2.2e-6, l=4e-6, top_len=50, bot_len=50)

# Rpd: vg → gnd, 500k
s.bare_R("Rpd", lcx, 230, "vg", "gnd", "500k")

# ════════════════════════════════════════════════════════════════════════
# SECTION 2: Clamp NFET (center column)
# XMclamp: D=pvdd, G=vg, S=gnd, B=gnd, W=100u L=0.5u m=4
# ════════════════════════════════════════════════════════════════════════
ccx = 250
s.section("CLAMP NFET", ccx - 80, -750)

s.fet("XMclamp", "nh", ccx, -200,
    d="pvdd", g="vg", s="gnd", b="gnd",
    w=100e-6, l=0.5e-6, m=4)

# ════════════════════════════════════════════════════════════════════════
# SECTION 3: Fast diode stack (right column)
# 7 NFETs: pvdd→nf6→nf5→nf4→nf3→nf2→nf1→gnd
# All diode-connected (D=G tied), B=gnd
# ════════════════════════════════════════════════════════════════════════
rcx = 650
s.section("FAST DIODE STACK (7x)", rcx - 120, -750)

fast_nets = ["pvdd", "nf6", "nf5", "nf4", "nf3", "nf2", "nf1", "gnd"]
fast_names = ["XMf1", "XMf2", "XMf3", "XMf4", "XMf5", "XMf6", "XMf7"]
fast_ys = [-600, -460, -320, -180, -40, 100, 240]

for i, (name, fy) in enumerate(zip(fast_names, fast_ys)):
    top = fast_nets[i]      # drain
    bot = fast_nets[i + 1]  # source
    # NFET diode-connected: D=G=top, S=bot, B=gnd
    s.fet_stacked(name, "nh", rcx, fy,
        d=top, g=top, s=bot, b="gnd",
        w=10e-6, l=0.5e-6, top_len=50, bot_len=50)

# ── Dashed outlines ────────────────────────────────────────────────────
s.rect_dash(-350, -700, 0, 350, layer=5)     # precision stack
s.rect_dash(100, -350, 420, -50, layer=4)     # clamp FET
s.rect_dash(500, -700, 850, 410, layer=7)     # fast stack

# ── Write ───────────────────────────────────────────────────────────────
sch_path = os.path.join(os.path.dirname(__file__), "pvdd_07_zener_clamp.sch")
s.write(sch_path)
print("Done:", sch_path)
