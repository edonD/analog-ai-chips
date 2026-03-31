#!/usr/bin/env python3
"""Generate pvdd_top_interconnect.sch — Top-Level Block Interconnect
Shows all sub-blocks as labeled rectangles with inter-block wiring."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sch_lib import Schematic

s = Schematic()

# ── Header ──────────────────────────────────────────────────────────────
s.header(
    title="PVDD 5V LDO REGULATOR — Top-Level Interconnect",
    subtitle="All blocks shown as rectangles with inter-block wiring",
    info="bvdd, pvdd, gnd, avbg, ibias, svdd, en, en_ret, uv_flag, ov_flag  |  design.cir .subckt pvdd_regulator",
    author="Claude / analog-ai-chips"
)

# ── Port Pins ───────────────────────────────────────────────────────────
px, py = -1200, -1000
s.section("PORT PINS", px, py - 40)
s.ipin(px,        py,       "bvdd")
s.ipin(px,        py + 40,  "avbg")
s.ipin(px,        py + 80,  "ibias")
s.ipin(px,        py + 120, "svdd")
s.ipin(px,        py + 160, "en")
s.ipin(px,        py + 200, "en_ret")
s.iopin(px + 300, py,       "pvdd")
s.iopin(px + 300, py + 40,  "gnd")
s.opin(px + 300,  py + 80,  "uv_flag")
s.opin(px + 300,  py + 120, "ov_flag")

# ════════════════════════════════════════════════════════════════════════
# Helper: draw a labeled block rectangle
# ════════════════════════════════════════════════════════════════════════
def block(x, y, w, h, name, subtitle="", layer=8, pins_l=None, pins_r=None, pins_t=None, pins_b=None):
    """Draw a block rectangle with label. pins_X = list of (name, offset, color_layer)."""
    # Rectangle
    s.L(layer, x, y, x + w, y)
    s.L(layer, x + w, y, x + w, y + h)
    s.L(layer, x + w, y + h, x, y + h)
    s.L(layer, x, y + h, x, y)
    # Block name centered
    s.T(name, x + w // 2, y + h // 2 - 15, xm=0.35, ym=0.35, attrs=f"layer={layer}")
    if subtitle:
        s.T(subtitle, x + w // 2, y + h // 2 + 10, xm=0.2, ym=0.2, attrs=f"layer=13")
    # Pin labels on edges
    if pins_l:
        for pname, off, clr in pins_l:
            py_ = y + off
            s.T(pname, x + 5, py_, xm=0.18, ym=0.18, attrs=f"layer={clr}")
    if pins_r:
        for pname, off, clr in pins_r:
            py_ = y + off
            s.T(pname, x + w - 5, py_, xm=0.18, ym=0.18, attrs=f"layer={clr}")
    if pins_t:
        for pname, off, clr in pins_t:
            px_ = x + off
            s.T(pname, px_, y + 5, xm=0.18, ym=0.18, attrs=f"layer={clr}")
    if pins_b:
        for pname, off, clr in pins_b:
            px_ = x + off
            s.T(pname, px_, y + h - 5, xm=0.18, ym=0.18, attrs=f"layer={clr}")

# ════════════════════════════════════════════════════════════════════════
# BLOCK LAYOUT — left to right, protection above, control below
#
# Row 1 (top):    LS_EN    Soft-Start    ErrorAmp    Compensation    PassDevice   Cload
# Row 2 (mid-up): UV_Comp   OV_Comp      ZenerClamp  CurrentLimiter
# Row 3 (bottom): ModeControl                        Startup         FeedbackNet
# ════════════════════════════════════════════════════════════════════════

bw, bh = 200, 120  # default block width/height

# -- Row 1: Signal path (y = -600) --
r1y = -600

# Level Shifter (EN)
block(-900, r1y, 160, bh, "LS_EN", "level_shifter_up", layer=8,
    pins_l=[("en", 30, 7), ("svdd", 60, 7), ("gnd", 90, 8)],
    pins_r=[("en_bvdd", 60, 4)])

# Soft-Start (Rss + Css)
block(-650, r1y, 180, bh, "SOFT-START", "Rss=200k Css=30n", layer=8,
    pins_l=[("avbg", 40, 8)],
    pins_r=[("vref_ss", 60, 8)],
    pins_b=[("gnd", 90, 8)])

# Error Amplifier
block(-380, r1y, bw, bh, "ERROR AMP", "error_amp", layer=5,
    pins_l=[("vref_ss", 30, 8), ("vfb", 60, 5), ("ibias", 90, 8)],
    pins_r=[("ea_out", 40, 8)],
    pins_t=[("pvdd", 60, 5), ("ea_en", 140, 8)],
    pins_b=[("gnd", 100, 8)])

# Compensation
block(-100, r1y, 180, bh, "COMP", "compensation", layer=5,
    pins_l=[("ea_out", 40, 8)],
    pins_t=[("pvdd", 60, 5)],
    pins_b=[("gnd", 90, 8)])

# Pass Device
block(180, r1y, bw, bh, "PASS DEV", "XM_pass", layer=4,
    pins_l=[("gate", 60, 8)],
    pins_t=[("bvdd", 60, 4)],
    pins_b=[("pvdd", 100, 5)])

# Cload
block(480, r1y, 120, bh, "Cload", "200pF", layer=5,
    pins_l=[("pvdd", 40, 5)],
    pins_b=[("gnd", 60, 8)])

# -- Row 2: Protection (y = -380) --
r2y = -380

# UV Comparator
block(-700, r2y, bw, bh, "UV COMP", "uv_comparator", layer=7,
    pins_l=[("pvdd", 30, 5), ("avbg", 60, 8)],
    pins_r=[("uv_flag", 40, 7)],
    pins_t=[("svdd", 60, 7), ("uvov_en", 140, 8)],
    pins_b=[("gnd", 100, 8)])

# OV Comparator
block(-400, r2y, bw, bh, "OV COMP", "ov_comparator", layer=7,
    pins_l=[("pvdd", 30, 5), ("avbg", 60, 8)],
    pins_r=[("ov_flag", 40, 7)],
    pins_t=[("svdd", 60, 7), ("uvov_en", 140, 8)],
    pins_b=[("gnd", 100, 8)])

# Zener Clamp
block(-100, r2y, 180, bh, "ZENER", "zener_clamp", layer=4,
    pins_l=[("pvdd", 40, 5)],
    pins_b=[("gnd", 90, 8)])

# Current Limiter
block(180, r2y, bw, bh, "ILIM", "current_limiter", layer=4,
    pins_l=[("gate", 30, 8), ("bvdd", 60, 4)],
    pins_r=[("ilim_flag", 40, 8)],
    pins_t=[("pvdd", 100, 5)],
    pins_b=[("gnd", 100, 8)])

# -- Row 3: Control + Feedback (y = -160) --
r3y = -160

# Mode Control
block(-700, r3y, 350, 140, "MODE CONTROL", "mode_control", layer=8,
    pins_l=[("bvdd", 30, 4), ("pvdd", 50, 5), ("svdd", 70, 7), ("gnd", 90, 8), ("avbg", 110, 8)],
    pins_r=[("bypass_en", 25, 8), ("mc_ea_en", 45, 8), ("ref_sel", 65, 8),
            ("uvov_en", 85, 8), ("ilim_en", 105, 8), ("pass_off", 125, 8)],
    pins_t=[("en_ret", 100, 8)])

# Startup
block(-200, r3y, 220, 140, "STARTUP", "startup", layer=4,
    pins_l=[("bvdd", 30, 4), ("pvdd", 50, 5), ("gnd", 70, 8), ("ea_out", 100, 8)],
    pins_r=[("gate", 30, 8), ("startup_done", 60, 8), ("ea_en", 90, 8)],
    pins_t=[("vref", 60, 8)])

# Feedback Network
block(180, r3y, bw, 140, "FEEDBACK", "feedback_network", layer=5,
    pins_l=[("pvdd", 40, 5)],
    pins_r=[("vfb", 60, 5)],
    pins_b=[("gnd", 100, 8)])

# ════════════════════════════════════════════════════════════════════════
# INTER-BLOCK WIRING — explicit N (wire) elements
# ════════════════════════════════════════════════════════════════════════
s.section("INTER-BLOCK WIRING", -1100, -850)

# -- vref_ss: Soft-Start out → Error Amp in --
s.N(-470, r1y + 60, -380, r1y + 30, lab="vref_ss")

# -- ea_out: Error Amp → Compensation, also to Startup --
s.N(-180, r1y + 40, -100, r1y + 40, lab="ea_out")
# ea_out down to Startup
s.N(-180, r1y + 40, -180, r3y + 100, lab="ea_out")
s.N(-180, r3y + 100, -200, r3y + 100, lab="ea_out")

# -- gate: Startup → Pass Device, and to ILIM --
s.N(20, r3y + 30, 120, r3y + 30, lab="gate")
s.N(120, r3y + 30, 120, r1y + 60, lab="gate")
s.N(120, r1y + 60, 180, r1y + 60, lab="gate")
# gate to ILIM
s.N(120, r2y + 30, 180, r2y + 30, lab="gate")

# -- vfb: Feedback → Error Amp --
s.N(380, r3y + 60, 450, r3y + 60, lab="vfb")
s.N(450, r3y + 60, 450, r1y + 150, lab="vfb")
s.N(450, r1y + 150, -420, r1y + 150, lab="vfb")
s.N(-420, r1y + 150, -420, r1y + 60, lab="vfb")
s.N(-420, r1y + 60, -380, r1y + 60, lab="vfb")

# -- pvdd bus: Pass Device → Feedback, UV, OV, Zener, Cload --
s.N(280, r1y + 120, 280, r1y + 150, lab="pvdd")
# pvdd horizontal bus
s.N(-700, r1y + 170, 480, r1y + 170, lab="pvdd")
s.net_text("pvdd", -200, r1y + 160, layer=5)
# pvdd to Feedback
s.N(180, r3y + 40, 160, r3y + 40, lab="pvdd")
s.N(160, r3y + 40, 160, r1y + 170, lab="pvdd")
# pvdd to Cload
s.N(480, r1y + 40, 470, r1y + 40, lab="pvdd")
s.N(470, r1y + 40, 470, r1y + 170, lab="pvdd")
# pvdd to UV
s.N(-700, r2y + 30, -720, r2y + 30, lab="pvdd")
s.N(-720, r2y + 30, -720, r1y + 170, lab="pvdd")
# pvdd to OV
s.N(-400, r2y + 30, -420, r2y + 30, lab="pvdd")
s.N(-420, r2y + 30, -420, r1y + 170, lab="pvdd")
# pvdd to Zener
s.N(-100, r2y + 40, -120, r2y + 40, lab="pvdd")
s.N(-120, r2y + 40, -120, r1y + 170, lab="pvdd")

# -- bvdd bus: top horizontal --
s.N(-900, r1y - 30, 380, r1y - 30, lab="bvdd")
s.net_text("bvdd", -600, r1y - 40, layer=4)
# bvdd to Pass Device
s.N(280, r1y, 280, r1y - 30, lab="bvdd")
# bvdd to ILIM
s.N(240, r2y + 60, 240, r1y - 30, lab="bvdd")  # approximate via wiring
# bvdd to Startup
s.N(-200, r3y + 30, -230, r3y + 30, lab="bvdd")
s.N(-230, r3y + 30, -230, r1y - 30, lab="bvdd")
# bvdd to Mode Control
s.N(-700, r3y + 30, -720, r3y + 30, lab="bvdd")
s.N(-720, r3y + 30, -720, r1y - 30, lab="bvdd")

# -- ea_en: Startup → Error Amp --
s.N(20, r3y + 90, 60, r3y + 90, lab="ea_en")
s.N(60, r3y + 90, 60, r1y - 60, lab="ea_en")
s.N(60, r1y - 60, -240, r1y - 60, lab="ea_en")
s.N(-240, r1y - 60, -240, r1y, lab="ea_en")

# -- startup_done: out from Startup --
s.N(20, r3y + 60, 80, r3y + 60, lab="startup_done")

# -- gnd bus: bottom --
gnd_y = r3y + 200
s.N(-900, gnd_y, 600, gnd_y, lab="gnd")
s.net_text("gnd", -200, gnd_y - 10, layer=8)

# -- svdd bus --
svdd_y = r2y - 30
s.N(-700, svdd_y, -400, svdd_y, lab="svdd")
s.net_text("svdd", -550, svdd_y - 10, layer=7)
# svdd to UV
s.N(-640, r2y, -640, svdd_y, lab="svdd")
# svdd to OV
s.N(-340, r2y, -340, svdd_y, lab="svdd")

# -- uvov_en: Mode Control → UV, OV --
s.N(-350, r3y, -350, r2y + 120, lab="uvov_en")
s.N(-350, r2y + 85, -560, r2y + 85, lab="uvov_en")
s.N(-560, r2y + 85, -560, r2y, lab="uvov_en")  # to UV top
s.N(-350, r2y + 85, -260, r2y + 85, lab="uvov_en")
s.N(-260, r2y + 85, -260, r2y, lab="uvov_en")  # to OV top

# -- avbg: input to Soft-Start, UV, OV, Mode Control --
s.N(-650, r1y + 40, -670, r1y + 40, lab="avbg")
s.N(-670, r1y + 40, -670, r1y + 170, lab="avbg")
# avbg to UV
s.N(-700, r2y + 60, -740, r2y + 60, lab="avbg")
# avbg to OV
s.N(-400, r2y + 60, -440, r2y + 60, lab="avbg")

# -- ibias: to Error Amp --
s.N(-380, r1y + 90, -420, r1y + 90, lab="ibias")

# -- uv_flag, ov_flag outputs --
s.N(-500, r2y + 40, -480, r2y + 40, lab="uv_flag")
s.N(-200, r2y + 40, -180, r2y + 40, lab="ov_flag")

# -- en_bvdd: LS_EN → (used internally) --
s.N(-740, r1y + 60, -720, r1y + 60, lab="en_bvdd")

# -- en: external input to LS_EN --
s.N(-900, r1y + 30, -920, r1y + 30, lab="en")

# ── Dashed outline around entire design ─────────────────────────────────
s.rect_dash(-950, r1y - 80, 650, gnd_y + 40, layer=4)

# ── Write ───────────────────────────────────────────────────────────────
sch_path = os.path.join(os.path.dirname(__file__), "pvdd_top_interconnect.sch")
s.write(sch_path)
print("Done:", sch_path)
