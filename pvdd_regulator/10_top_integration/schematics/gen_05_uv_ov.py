#!/usr/bin/env python3
"""Generate pvdd_05_uv_ov.sch — UV/OV Comparators (both on one schematic)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sch_lib import Schematic

S = Schematic()
S.header(
    "Block 05: UV/OV Comparators",
    "Under-Voltage (trip=4.3V) + Over-Voltage (trip=5.5V)  |  1.8V FETs",
    ".subckt uv_comparator / .subckt ov_comparator  —  pvdd vref flag vdd_comp gnd en",
    "PVDD LDO — UV/OV Protection"
)

# === Port pins ===
S.section("Ports", -250, -900)
S.ipin(-250, -850, "pvdd")
S.ipin(-250, -800, "vref")
S.ipin(-250, -750, "en")
S.iopin(-250, -700, "vdd_comp")
S.iopin(-250, -650, "gnd")
S.opin(-250, -600, "uv_flag")
S.opin(-250, -550, "ov_flag")

# ================================================================
# UV COMPARATOR — left half
# ================================================================
uv_x0 = 0
uv_y0 = -400

S.section("UV Comparator (trip = 4.3V)", uv_x0 - 50, uv_y0 - 260)
S.rect_dash(uv_x0 - 150, uv_y0 - 320, uv_x0 + 1250, uv_y0 + 680)

# --- Left column: Resistor divider + hysteresis + bias ---
rx = uv_x0
S.bare_R("R_top_uv", rx, uv_y0 - 150, "pvdd", "mid_uv", "500k")
S.bare_R("R_bot_uv", rx, uv_y0 + 10,  "mid_uv", "gnd", "199.4k")
S.bare_R("R_hyst_uv", rx + 120, uv_y0 - 70, "out_n_uv", "mid_uv", "2.5Meg")
S.bare_R("R_bias_uv", rx + 240, uv_y0 - 150, "vdd_comp", "bias_n_uv", "800k")

# --- Center: Bias mirror + diff pair + PMOS load ---
bx = uv_x0 + 400
# Bias mirror: XMbias (diode-connected) + XMtail
S.fet("XMbias_uv", "n18", bx, uv_y0 + 150,
      d="bias_n_uv", g="bias_n_uv", s="gnd", b="gnd", w=1, l=4)
S.fet("XMtail_uv", "n18", bx + 200, uv_y0 + 150,
      d="tail_uv", g="bias_n_uv", s="gnd", b="gnd", w=1, l=4)

# Diff pair: XM1 (mid_uv on gate), XM2 (vref on gate)
dpx = uv_x0 + 500
S.fet("XM1_uv", "n18", dpx, uv_y0,
      d="out_p_uv", g="mid_uv", s="tail_uv", b="gnd", w=2, l=1)
S.fet("XM2_uv", "n18", dpx + 250, uv_y0,
      d="out_n_uv", g="vref", s="tail_uv", b="gnd", w=2, l=1)

# PMOS current mirror load: XM3, XM4
S.fet("XM3_uv", "p18", dpx, uv_y0 - 250,
      d="out_p_uv", g="out_p_uv", s="vdd_comp", b="vdd_comp", w=2, l=1)
S.fet("XM4_uv", "p18", dpx + 250, uv_y0 - 250,
      d="out_n_uv", g="out_p_uv", s="vdd_comp", b="vdd_comp", w=2, l=1)

# --- Right: Enable inverter + NOR gate ---
ex = uv_x0 + 900
S.fet("XMen_n_uv", "n18", ex, uv_y0 + 100,
      d="en_bar_uv", g="en", s="gnd", b="gnd", w=0.42, l=0.15)
S.fet("XMen_p_uv", "p18", ex, uv_y0 - 50,
      d="en_bar_uv", g="en", s="vdd_comp", b="vdd_comp", w=0.84, l=0.15)

# NOR gate: uv_flag = NOR(out_n_uv, en_bar_uv)
nx = uv_x0 + 1100
S.fet("XMnor_p1_uv", "p18", nx, uv_y0 - 150,
      d="nor_mid_uv", g="out_n_uv", s="vdd_comp", b="vdd_comp", w=4, l=0.15)
S.fet("XMnor_p2_uv", "p18", nx, uv_y0,
      d="uv_flag", g="en_bar_uv", s="nor_mid_uv", b="nor_mid_uv", w=4, l=0.15)
S.fet("XMnor_n1_uv", "n18", nx, uv_y0 + 200,
      d="uv_flag", g="out_n_uv", s="gnd", b="gnd", w=1, l=0.15)
S.fet("XMnor_n2_uv", "n18", nx + 200, uv_y0 + 200,
      d="uv_flag", g="en_bar_uv", s="gnd", b="gnd", w=1, l=0.15)

S.T("UV trip = 4.3V  |  R_top=500k / R_bot=199.4k  |  Vdiv = PVDD * 199.4/699.4",
    uv_x0, uv_y0 + 550, xm=0.25, ym=0.25, attrs="layer=8")

# ================================================================
# OV COMPARATOR — right half
# ================================================================
ov_x0 = 1600
ov_y0 = -400

S.section("OV Comparator (trip = 5.5V)", ov_x0 - 50, ov_y0 - 260)
S.rect_dash(ov_x0 - 150, ov_y0 - 320, ov_x0 + 1250, ov_y0 + 680)

# --- Left column: Resistor divider + hysteresis + bias ---
rx = ov_x0
S.bare_R("R_top_ov", rx, ov_y0 - 150, "pvdd", "mid_ov", "500k")
S.bare_R("R_bot_ov", rx, ov_y0 + 10,  "mid_ov", "gnd", "146k")
S.bare_R("R_hyst_ov", rx + 120, ov_y0 - 70, "ov_flag", "mid_ov", "8Meg")
S.bare_R("R_bias_ov", rx + 240, ov_y0 - 150, "vdd_comp", "bias_n_ov", "800k")

# --- Center: Bias mirror + diff pair + PMOS load ---
bx = ov_x0 + 400
S.fet("XMbias_ov", "n18", bx, ov_y0 + 150,
      d="bias_n_ov", g="bias_n_ov", s="gnd", b="gnd", w=1, l=4)
S.fet("XMtail_ov", "n18", bx + 200, ov_y0 + 150,
      d="tail_ov", g="bias_n_ov", s="gnd", b="gnd", w=1, l=4)

# Diff pair: XM1 (vref on gate!), XM2 (mid_ov on gate!) — swapped vs UV
dpx = ov_x0 + 500
S.fet("XM1_ov", "n18", dpx, ov_y0,
      d="out_p_ov", g="vref", s="tail_ov", b="gnd", w=2, l=1)
S.fet("XM2_ov", "n18", dpx + 250, ov_y0,
      d="out_n_ov", g="mid_ov", s="tail_ov", b="gnd", w=2, l=1)

# PMOS current mirror load
S.fet("XM3_ov", "p18", dpx, ov_y0 - 250,
      d="out_p_ov", g="out_p_ov", s="vdd_comp", b="vdd_comp", w=2, l=1)
S.fet("XM4_ov", "p18", dpx + 250, ov_y0 - 250,
      d="out_n_ov", g="out_p_ov", s="vdd_comp", b="vdd_comp", w=2, l=1)

# --- Right: Enable inverter + NOR gate ---
ex = ov_x0 + 900
S.fet("XMen_n_ov", "n18", ex, ov_y0 + 100,
      d="en_bar_ov", g="en", s="gnd", b="gnd", w=0.42, l=0.15)
S.fet("XMen_p_ov", "p18", ex, ov_y0 - 50,
      d="en_bar_ov", g="en", s="vdd_comp", b="vdd_comp", w=0.84, l=0.15)

# NOR gate: ov_flag = NOR(out_n_ov, en_bar_ov)
nx = ov_x0 + 1100
S.fet("XMnor_p1_ov", "p18", nx, ov_y0 - 150,
      d="nor_mid_ov", g="out_n_ov", s="vdd_comp", b="vdd_comp", w=4, l=0.15)
S.fet("XMnor_p2_ov", "p18", nx, ov_y0,
      d="ov_flag", g="en_bar_ov", s="nor_mid_ov", b="nor_mid_ov", w=4, l=0.15)
S.fet("XMnor_n1_ov", "n18", nx, ov_y0 + 200,
      d="ov_flag", g="out_n_ov", s="gnd", b="gnd", w=1, l=0.15)
S.fet("XMnor_n2_ov", "n18", nx + 200, ov_y0 + 200,
      d="ov_flag", g="en_bar_ov", s="gnd", b="gnd", w=1, l=0.15)

S.T("OV trip = 5.5V  |  R_top=500k / R_bot=146k  |  Vdiv = PVDD * 146/646",
    ov_x0, ov_y0 + 550, xm=0.25, ym=0.25, attrs="layer=8")
S.T("NOTE: Diff pair inputs swapped vs UV — vref on M1, mid_ov on M2",
    ov_x0, ov_y0 + 590, xm=0.22, ym=0.22, attrs="layer=13")

S.write("pvdd_05_uv_ov.sch")
print("Done: pvdd_05_uv_ov.sch")
