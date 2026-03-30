#!/usr/bin/env python3
"""Generate FULL transistor-level schematic of PVDD 5V LDO Regulator.
Every MOSFET, resistor, and capacitor from all 10 block design.cir files.
Uses real SKY130 PDK symbols."""

import os

# ================================================================
# SYMBOL PATHS
# ================================================================
PDK = "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr"
XLIB = "/usr/share/xschem/xschem_library/devices"

SYM = {
    "ph":   f"{PDK}/pfet_g5v0d10v5.sym",
    "nh":   f"{PDK}/nfet_g5v0d10v5.sym",
    "p18":  f"{PDK}/pfet_01v8.sym",
    "n18":  f"{PDK}/nfet_01v8.sym",
    "rxh":  f"{PDK}/res_xhigh_po.sym",
    "mim":  f"{PDK}/cap_mim_m3_1.sym",
    "R":    f"{XLIB}/res.sym",
    "C":    f"{XLIB}/capa.sym",
}

MODEL = {
    "ph": "pfet_g5v0d10v5", "nh": "nfet_g5v0d10v5",
    "p18": "pfet_01v8", "n18": "nfet_01v8",
    "rxh": "res_xhigh_po", "mim": "cap_mim_m3_1",
}

# ================================================================
# XSCHEM OUTPUT HELPERS
# ================================================================
out = []

def T(text, x, y, rot=0, flip=0, xm=0.4, ym=0.4, attrs=""):
    out.append(f'T {{{text}}} {x} {y} {rot} {flip} {xm} {ym} {{{attrs}}}')

def N(x1, y1, x2, y2, lab=""):
    a = f"lab={lab}" if lab else ""
    out.append(f'N {x1} {y1} {x2} {y2} {{{a}}}')

def Cv(sym, x, y, rot=0, flip=0, attrs=""):
    out.append(f'C {{{sym}}} {x} {y} {rot} {flip} {{{attrs}}}')

def L(layer, x1, y1, x2, y2, attrs=""):
    out.append(f'L {layer} {x1} {y1} {x2} {y2} {{{attrs}}}')

def lab_pin(x, y, rot, name, pname):
    Cv(f"{XLIB}/lab_pin.sym", x, y, rot, 0,
       f"name={pname} sig_type=std_logic lab={name}")

def comment(text):
    out.append(f"* {text}")

def rect_dashed(x1, y1, x2, y2, layer=8):
    for args in [(x1,y1,x2,y1),(x2,y1,x2,y2),(x2,y2,x1,y2),(x1,y2,x1,y1)]:
        L(layer, *args, "dash=5")

# ================================================================
# COMPONENT PLACEMENT — cell size
# ================================================================
CW = 280   # cell width for MOSFETs
CH = 240   # cell height for MOSFETs
CW_P = 200 # cell width for passives
PIN_C = 0  # global pin counter

def next_pin():
    global PIN_C
    PIN_C += 1
    return f"p{PIN_C}"

# ================================================================
# PLACE A MOSFET (PFET or NFET)
# type_key: "ph","nh","p18","n18"
# cx,cy: center of cell
# d,g,s,b: net names for drain,gate,source,bulk
# w,l: in microns
# m: multiplier
# For PFET: symbol top=Source, bottom=Drain
# For NFET: symbol top=Drain, bottom=Source
# ================================================================
def place_fet(name, type_key, cx, cy, d, g, s, b, w, l, m=1):
    is_pfet = type_key in ("ph", "p18")
    sym = SYM[type_key]
    model = MODEL[type_key]

    # Symbol placed at (cx-20, cy) so body center is at (cx, cy)
    sx, sy = cx - 20, cy
    m_str = f" mult={m}" if m > 1 else " mult=1"
    Cv(sym, sx, sy, 0, 0,
       f"name={name} L={l} W={w} nf=1{m_str} model={model} spiceprefix=X")

    # Instance name + W/L annotation
    T(name, cx - 25, cy - 45, xm=0.18, ym=0.18, attrs="layer=13")
    wl = f"W={w} L={l}" + (f" m={m}" if m > 1 else "")
    T(wl, cx - 25, cy + 45, xm=0.15, ym=0.15, attrs="layer=5")

    # Pin connections via lab_pin + short wires
    # Gate (left)
    N(cx - 20, cy, cx - 50, cy)
    lab_pin(cx - 50, cy, 0, g, next_pin())

    # Bulk (right)
    N(cx + 20, cy, cx + 50, cy)
    lab_pin(cx + 50, cy, 2, b, next_pin())

    if is_pfet:
        # Top = Source, Bottom = Drain
        top_net, bot_net = s, d
    else:
        # Top = Drain, Bottom = Source
        top_net, bot_net = d, s

    # Top pin
    N(cx + 20, cy - 30, cx + 20, cy - 55)
    lab_pin(cx + 20, cy - 55, 3, top_net, next_pin())

    # Bottom pin
    N(cx + 20, cy + 30, cx + 20, cy + 55)
    lab_pin(cx + 20, cy + 55, 1, bot_net, next_pin())

# ================================================================
# PLACE A PDK RESISTOR (res_xhigh_po)
# Pins: P(top), M(bottom), B(body=left)
# ================================================================
def place_rxh(name, cx, cy, p_net, m_net, b_net, w, l):
    Cv(SYM["rxh"], cx, cy, 0, 0,
       f"name={name} W={w} L={l} model=res_xhigh_po spiceprefix=X")
    T(name, cx + 20, cy - 25, xm=0.17, ym=0.17, attrs="layer=13")
    T(f"W={w} L={l}", cx + 20, cy + 15, xm=0.14, ym=0.14, attrs="layer=5")
    # Top (P)
    N(cx, cy - 30, cx, cy - 55)
    lab_pin(cx, cy - 55, 3, p_net, next_pin())
    # Bottom (M)
    N(cx, cy + 30, cx, cy + 55)
    lab_pin(cx, cy + 55, 1, m_net, next_pin())
    # Body (left)
    N(cx - 20, cy, cx - 40, cy)
    lab_pin(cx - 40, cy, 0, b_net, next_pin())

# ================================================================
# PLACE A MIM CAP (cap_mim_m3_1)
# Pins: c0(top), c1(bottom)
# ================================================================
def place_mim(name, cx, cy, c0_net, c1_net, w, l, mf=1):
    Cv(SYM["mim"], cx, cy, 0, 0,
       f"name={name} W={w} L={l} MF={mf} model=cap_mim_m3_1 spiceprefix=X")
    T(name, cx + 20, cy - 25, xm=0.17, ym=0.17, attrs="layer=13")
    T(f"W={w} L={l}", cx + 20, cy + 15, xm=0.14, ym=0.14, attrs="layer=5")
    N(cx, cy - 30, cx, cy - 55)
    lab_pin(cx, cy - 55, 3, c0_net, next_pin())
    N(cx, cy + 30, cx, cy + 55)
    lab_pin(cx, cy + 55, 1, c1_net, next_pin())

# ================================================================
# PLACE A BARE RESISTOR
# ================================================================
def place_R(name, cx, cy, n1, n2, value):
    Cv(SYM["R"], cx, cy, 0, 0, f"name={name} value={value}")
    T(name, cx + 20, cy - 25, xm=0.17, ym=0.17, attrs="layer=13")
    T(value, cx + 20, cy + 10, xm=0.15, ym=0.15, attrs="layer=5")
    N(cx, cy - 30, cx, cy - 55)
    lab_pin(cx, cy - 55, 3, n1, next_pin())
    N(cx, cy + 30, cx, cy + 55)
    lab_pin(cx, cy + 55, 1, n2, next_pin())

# ================================================================
# PLACE A BARE CAPACITOR
# ================================================================
def place_C(name, cx, cy, n1, n2, value):
    Cv(SYM["C"], cx, cy, 0, 0, f"name={name} value={value}")
    T(name, cx + 20, cy - 25, xm=0.17, ym=0.17, attrs="layer=13")
    T(value, cx + 20, cy + 10, xm=0.15, ym=0.15, attrs="layer=5")
    N(cx, cy - 30, cx, cy - 55)
    lab_pin(cx, cy - 55, 3, n1, next_pin())
    N(cx, cy + 30, cx, cy + 55)
    lab_pin(cx, cy + 55, 1, n2, next_pin())

# ================================================================
# SECTION BOUNDARY + HEADER
# ================================================================
def section(title, subtitle, x1, y1, x2, y2, layer=8):
    comment("=" * 60)
    comment(title)
    comment("=" * 60)
    rect_dashed(x1, y1, x2, y2, layer)
    T(title, x1 + 15, y1 + 15, xm=0.4, ym=0.4, attrs=f"layer={layer}")
    T(subtitle, x1 + 15, y1 + 45, xm=0.22, ym=0.22, attrs="layer=13")

# ================================================================
# GRID HELPER — returns (cx, cy) for row r, col c in section
# ================================================================
def grid(x0, y0, r, c, cw=CW, ch=CH, y_off=70):
    return (x0 + c * cw + cw // 2, y0 + y_off + r * ch + ch // 2)

# ================================================================
# HEADER
# ================================================================
out.append("v {xschem version=3.4.6 file_version=1.2}")
out.append("G {}")
out.append('K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}')
out.append("V {}")
out.append("S {}")
out.append("E {}")
out.append("")

# Title
T("PVDD 5V LDO Regulator — Full Transistor-Level Schematic", -3800, -5800, xm=0.9, ym=0.9, attrs="layer=4")
T("SkyWater SKY130A  |  169 components  |  All 10 blocks flattened", -3800, -5740, xm=0.35, ym=0.35, attrs="")
T("Every MOSFET, resistor, and capacitor drawn with real PDK symbols", -3800, -5710, xm=0.3, ym=0.3, attrs="layer=13")
Cv(f"{XLIB}/title.sym", -3800, 5800, 0, 0,
   'name=l1 author="PVDD 5V LDO Regulator -- Full Transistor-Level -- Analog AI Chips"')
out.append("")

# ================================================================
# EXTERNAL PORT PINS
# ================================================================
comment("EXTERNAL PORT PINS")
for i, (name, y) in enumerate([
    ("bvdd", -5500), ("pvdd", -5400), ("gnd", -5300),
    ("avbg", -5200), ("ibias", -5100), ("svdd", -5000),
    ("en", -4900), ("en_ret", -4800),
    ("uv_flag", -4700), ("ov_flag", -4600),
    ("vref_ss", -4500), ("ea_out", -4400), ("gate", -4300),
    ("ea_en", -4200), ("startup_done", -4100),
    ("vfb", -4000), ("ilim_flag", -3900),
    ("en_bvdd", -3800), ("bypass_en", -3700),
    ("mc_ea_en", -3600), ("ref_sel", -3500),
    ("uvov_en", -3400), ("ilim_en", -3300), ("pass_off", -3200),
]):
    Cv(f"{XLIB}/iopin.sym", -3900, y, 0, 0, f"name=pp{i} lab={name}")
    T(name, -3840, y - 8, xm=0.22, ym=0.22, attrs="layer=4")
out.append("")

# ================================================================
# SECTION 1: ERROR AMPLIFIER (Block 00) — 12 FETs + 2 passives
# ================================================================
S1X, S1Y = -3700, -5600
S1W, S1H = 3700, 1600
section("Section 1: Error Amplifier (Block 00)", "Two-stage Miller OTA — 12 FETs + Cc + Rc",
        S1X, S1Y, S1X + S1W, S1Y + S1H, layer=5)

# Row 0: Enable + Bias
x, y = grid(S1X, S1Y, 0, 0)
place_fet("XMen", "nh", x, y, "b00_ibias_en", "ea_en", "ibias", "gnd", 20, 1)
x, y = grid(S1X, S1Y, 0, 1)
place_fet("XMpu", "ph", x, y, "ea_out", "ea_en", "pvdd", "pvdd", 20, 1)
x, y = grid(S1X, S1Y, 0, 2)
place_fet("XMbn0", "nh", x, y, "b00_ibias_en", "b00_ibias_en", "gnd", "gnd", 20, 8)

# Row 1: Bias mirrors
x, y = grid(S1X, S1Y, 1, 0)
place_fet("XMbn_pb", "nh", x, y, "b00_pb_tail", "b00_ibias_en", "gnd", "gnd", 20, 8, m=200)
x, y = grid(S1X, S1Y, 1, 1)
place_fet("XMbp0", "ph", x, y, "b00_pb_tail", "b00_pb_tail", "pvdd", "pvdd", 20, 4, m=4)

# Row 2: Diff pair + tail
x, y = grid(S1X, S1Y, 2, 0)
place_fet("XMtail", "ph", x, y, "b00_tail_s", "b00_pb_tail", "pvdd", "pvdd", 20, 4, m=4)
x, y = grid(S1X, S1Y, 2, 1)
place_fet("XM1", "ph", x, y, "b00_d1", "vref_ss", "b00_tail_s", "pvdd", 80, 4, m=2)
x, y = grid(S1X, S1Y, 2, 2)
place_fet("XM2", "ph", x, y, "b00_d2", "vfb", "b00_tail_s", "pvdd", 80, 4, m=2)

# Row 3: NMOS mirror load
x, y = grid(S1X, S1Y, 3, 0)
place_fet("XMn_l", "nh", x, y, "b00_d1", "b00_d1", "gnd", "gnd", 20, 8, m=2)
x, y = grid(S1X, S1Y, 3, 1)
place_fet("XMn_r", "nh", x, y, "b00_d2", "b00_d1", "gnd", "gnd", 20, 8, m=2)

# Row 4: Stage 2
x, y = grid(S1X, S1Y, 4, 0)
place_fet("XMcs", "nh", x, y, "ea_out", "b00_d2", "gnd", "gnd", 20, 1)
x, y = grid(S1X, S1Y, 4, 1)
place_fet("XMp_ld", "ph", x, y, "ea_out", "b00_pb_tail", "pvdd", "pvdd", 20, 4, m=8)

# Miller comp passives (right side of section)
x, y = grid(S1X, S1Y, 3, 3, cw=CW_P)
place_C("Cc", x + 800, y, "b00_d2", "b00_comp_mid", "30p")
x, y = grid(S1X, S1Y, 4, 3, cw=CW_P)
place_R("Rc", x + 800, y, "b00_comp_mid", "ea_out", "25k")
out.append("")

# ================================================================
# SECTION 2: PASS DEVICE (Block 01) — 10 PFETs
# ================================================================
S2X, S2Y = 500, -5600
S2W, S2H = 3000, 800
section("Section 2: Pass Device (Block 01)", "10x PMOS pfet_g5v0d10v5 W=100u L=0.5u — Total W=1mm",
        S2X, S2Y, S2X + S2W, S2Y + S2H, layer=4)

for i in range(10):
    r, c = divmod(i, 5)
    x, y = grid(S2X, S2Y, r, c)
    place_fet(f"XM{i+1}", "ph", x, y, "pvdd", "gate", "bvdd", "bvdd", 100, 0.5)
out.append("")

# ================================================================
# SECTION 3: FEEDBACK NETWORK (Block 02) — 2 resistors
# ================================================================
S3X, S3Y = 500, -4700
S3W, S3H = 800, 700
section("Section 3: Feedback Network (Block 02)", "Resistive divider — vfb = 1.226V at PVDD=5V",
        S3X, S3Y, S3X + S3W, S3Y + S3H, layer=5)

x, y = grid(S3X, S3Y, 0, 0, cw=CW_P)
place_rxh("XR_TOP", x, y, "pvdd", "vfb", "gnd", 3.0, 536)
x, y = grid(S3X, S3Y, 0, 1, cw=CW_P)
place_rxh("XR_BOT", x, y, "vfb", "gnd", "gnd", 3.0, 174.30)
out.append("")

# ================================================================
# SECTION 4: COMPENSATION (Block 03) — 2 caps + 1 resistor
# ================================================================
S4X, S4Y = -3700, -3900
S4W, S4H = 1000, 600
section("Section 4: Compensation (Block 03)", "Miller Cc + Rz + Cout",
        S4X, S4Y, S4X + S4W, S4Y + S4H, layer=5)

x, y = grid(S4X, S4Y, 0, 0, cw=CW_P)
place_mim("XCc", x, y, "ea_out", "b03_cc_mid", 122, 122)
x, y = grid(S4X, S4Y, 0, 1, cw=CW_P)
place_rxh("XRz", x, y, "b03_cc_mid", "pvdd", "gnd", 4, 10)
x, y = grid(S4X, S4Y, 0, 2, cw=CW_P)
place_mim("XCout", x, y, "pvdd", "gnd", 187, 187)
out.append("")

# ================================================================
# SECTION 5: CURRENT LIMITER (Block 04) — 5 FETs + 2 resistors
# ================================================================
S5X, S5Y = -2500, -3900
S5W, S5H = 2200, 700
section("Section 5: Current Limiter (Block 04)", "Sense mirror + Vth detect + gate clamp — Ilim~70mA",
        S5X, S5Y, S5X + S5W, S5Y + S5H, layer=4)

# Row 0: Sense + detect + clamp
x, y = grid(S5X, S5Y, 0, 0)
place_fet("XMs", "ph", x, y, "b04_sense_n", "gate", "bvdd", "bvdd", 2, 0.5)
x, y = grid(S5X, S5Y, 0, 1, cw=CW_P)
place_rxh("XRs", x, y, "b04_sense_n", "gnd", "gnd", 1, 3.12)
x, y = grid(S5X, S5Y, 0, 2)
place_fet("XMdet", "nh", x, y, "b04_det_n", "b04_sense_n", "gnd", "gnd", 5, 1)
x, y = grid(S5X, S5Y, 0, 3, cw=CW_P)
place_rxh("XRpu", x, y, "bvdd", "b04_det_n", "gnd", 1, 5)
x, y = grid(S5X, S5Y, 0, 4)
place_fet("XMclamp", "ph", x, y, "gate", "b04_det_n", "bvdd", "bvdd", 20, 1)

# Row 1: Flag output inverter
x, y = grid(S5X, S5Y, 1, 0)
place_fet("XMfp", "ph", x, y, "ilim_flag", "b04_det_n", "pvdd", "pvdd", 2, 1)
x, y = grid(S5X, S5Y, 1, 1)
place_fet("XMfn", "nh", x, y, "ilim_flag", "b04_det_n", "gnd", "gnd", 2, 1)
out.append("")

# ================================================================
# SECTION 6: UV/OV COMPARATORS (Block 05) — 24 FETs + 8 R
# ================================================================
S6X, S6Y = 1500, -4600
S6W, S6H = 5600, 2600
section("Section 6: UV/OV Comparators (Block 05)", "NMOS diff pair + PMOS mirror + NOR output — SVDD domain",
        S6X, S6Y, S6X + S6W, S6Y + S6H, layer=7)

# --- UV Comparator (left half) ---
T("UV Comparator — Trip PVDD < 4.3V", S6X + 30, S6Y + 70, xm=0.3, ym=0.3, attrs="layer=7")
UV_X = S6X
UV_Y = S6Y + 50

# UV Row 0: Resistive divider + bias
x, y = grid(UV_X, UV_Y, 0, 0, cw=CW_P)
place_R("uv_R_top", x, y, "pvdd", "b05uv_mid", "500k")
x, y = grid(UV_X, UV_Y, 0, 1, cw=CW_P)
place_R("uv_R_bot", x, y, "b05uv_mid", "gnd", "199.4k")
x, y = grid(UV_X, UV_Y, 0, 2, cw=CW_P)
place_R("uv_R_hyst", x, y, "b05uv_out_n", "b05uv_mid", "2.5Meg")
x, y = grid(UV_X, UV_Y, 0, 3, cw=CW_P)
place_R("uv_R_bias", x, y, "svdd", "b05uv_bias_n", "800k")

# UV Row 1: Bias + Tail
x, y = grid(UV_X, UV_Y, 1, 0)
place_fet("uv_XMbias", "n18", x, y, "b05uv_bias_n", "b05uv_bias_n", "gnd", "gnd", 1, 4)
x, y = grid(UV_X, UV_Y, 1, 1)
place_fet("uv_XMtail", "n18", x, y, "b05uv_tail", "b05uv_bias_n", "gnd", "gnd", 1, 4)

# UV Row 2: Diff pair
x, y = grid(UV_X, UV_Y, 2, 0)
place_fet("uv_XM1", "n18", x, y, "b05uv_out_p", "b05uv_mid", "b05uv_tail", "gnd", 2, 1)
x, y = grid(UV_X, UV_Y, 2, 1)
place_fet("uv_XM2", "n18", x, y, "b05uv_out_n", "avbg", "b05uv_tail", "gnd", 2, 1)

# UV Row 3: PMOS mirror load
x, y = grid(UV_X, UV_Y, 3, 0)
place_fet("uv_XM3", "p18", x, y, "b05uv_out_p", "b05uv_out_p", "svdd", "svdd", 2, 1)
x, y = grid(UV_X, UV_Y, 3, 1)
place_fet("uv_XM4", "p18", x, y, "b05uv_out_n", "b05uv_out_p", "svdd", "svdd", 2, 1)

# UV Row 4: Enable inverter
x, y = grid(UV_X, UV_Y, 4, 0)
place_fet("uv_XMen_n", "n18", x, y, "b05uv_en_bar", "uvov_en", "gnd", "gnd", 0.42, 0.15)
x, y = grid(UV_X, UV_Y, 4, 1)
place_fet("uv_XMen_p", "p18", x, y, "b05uv_en_bar", "uvov_en", "svdd", "svdd", 0.84, 0.15)

# UV Row 5: NOR output gate
x, y = grid(UV_X, UV_Y, 5, 0)
place_fet("uv_XMnor_p1", "p18", x, y, "b05uv_nor_mid", "b05uv_out_n", "svdd", "svdd", 4, 0.15)
x, y = grid(UV_X, UV_Y, 5, 1)
place_fet("uv_XMnor_p2", "p18", x, y, "uv_flag", "b05uv_en_bar", "b05uv_nor_mid", "b05uv_nor_mid", 4, 0.15)
x, y = grid(UV_X, UV_Y, 5, 2)
place_fet("uv_XMnor_n1", "n18", x, y, "uv_flag", "b05uv_out_n", "gnd", "gnd", 1, 0.15)
x, y = grid(UV_X, UV_Y, 5, 3)
place_fet("uv_XMnor_n2", "n18", x, y, "uv_flag", "b05uv_en_bar", "gnd", "gnd", 1, 0.15)

# --- OV Comparator (right half) ---
T("OV Comparator — Trip PVDD > 5.5V", S6X + 2800 + 30, S6Y + 70, xm=0.3, ym=0.3, attrs="layer=7")
OV_X = S6X + 2800
OV_Y = S6Y + 50

# OV Row 0: Resistive divider + bias
x, y = grid(OV_X, OV_Y, 0, 0, cw=CW_P)
place_R("ov_R_top", x, y, "pvdd", "b05ov_mid", "500k")
x, y = grid(OV_X, OV_Y, 0, 1, cw=CW_P)
place_R("ov_R_bot", x, y, "b05ov_mid", "gnd", "146k")
x, y = grid(OV_X, OV_Y, 0, 2, cw=CW_P)
place_R("ov_R_hyst", x, y, "ov_flag", "b05ov_mid", "8Meg")
x, y = grid(OV_X, OV_Y, 0, 3, cw=CW_P)
place_R("ov_R_bias", x, y, "svdd", "b05ov_bias_n", "800k")

# OV Row 1: Bias + Tail
x, y = grid(OV_X, OV_Y, 1, 0)
place_fet("ov_XMbias", "n18", x, y, "b05ov_bias_n", "b05ov_bias_n", "gnd", "gnd", 1, 4)
x, y = grid(OV_X, OV_Y, 1, 1)
place_fet("ov_XMtail", "n18", x, y, "b05ov_tail", "b05ov_bias_n", "gnd", "gnd", 1, 4)

# OV Row 2: Diff pair (note: inputs swapped vs UV)
x, y = grid(OV_X, OV_Y, 2, 0)
place_fet("ov_XM1", "n18", x, y, "b05ov_out_p", "avbg", "b05ov_tail", "gnd", 2, 1)
x, y = grid(OV_X, OV_Y, 2, 1)
place_fet("ov_XM2", "n18", x, y, "b05ov_out_n", "b05ov_mid", "b05ov_tail", "gnd", 2, 1)

# OV Row 3: PMOS mirror load
x, y = grid(OV_X, OV_Y, 3, 0)
place_fet("ov_XM3", "p18", x, y, "b05ov_out_p", "b05ov_out_p", "svdd", "svdd", 2, 1)
x, y = grid(OV_X, OV_Y, 3, 1)
place_fet("ov_XM4", "p18", x, y, "b05ov_out_n", "b05ov_out_p", "svdd", "svdd", 2, 1)

# OV Row 4: Enable inverter
x, y = grid(OV_X, OV_Y, 4, 0)
place_fet("ov_XMen_n", "n18", x, y, "b05ov_en_bar", "uvov_en", "gnd", "gnd", 0.42, 0.15)
x, y = grid(OV_X, OV_Y, 4, 1)
place_fet("ov_XMen_p", "p18", x, y, "b05ov_en_bar", "uvov_en", "svdd", "svdd", 0.84, 0.15)

# OV Row 5: NOR output gate
x, y = grid(OV_X, OV_Y, 5, 0)
place_fet("ov_XMnor_p1", "p18", x, y, "b05ov_nor_mid", "b05ov_out_n", "svdd", "svdd", 4, 0.15)
x, y = grid(OV_X, OV_Y, 5, 1)
place_fet("ov_XMnor_p2", "p18", x, y, "ov_flag", "b05ov_en_bar", "b05ov_nor_mid", "b05ov_nor_mid", 4, 0.15)
x, y = grid(OV_X, OV_Y, 5, 2)
place_fet("ov_XMnor_n1", "n18", x, y, "ov_flag", "b05ov_out_n", "gnd", "gnd", 1, 0.15)
x, y = grid(OV_X, OV_Y, 5, 3)
place_fet("ov_XMnor_n2", "n18", x, y, "ov_flag", "b05ov_en_bar", "gnd", "gnd", 1, 0.15)
out.append("")

# ================================================================
# SECTION 7: LEVEL SHIFTER UP (Block 06) — 6 FETs
# ================================================================
S7X, S7Y = -3700, -3200
S7W, S7H = 1800, 700
section("Section 7: Level Shifter (Block 06)", "SVDD->BVDD cross-coupled PMOS — 6 FETs",
        S7X, S7Y, S7X + S7W, S7Y + S7H, layer=7)

# Row 0: Input inverter
x, y = grid(S7X, S7Y, 0, 0)
place_fet("XMN_INV", "nh", x, y, "b06_in_b", "en", "gnd", "gnd", 2, 0.5)
x, y = grid(S7X, S7Y, 0, 1)
place_fet("XMP_INV", "ph", x, y, "b06_in_b", "en", "svdd", "svdd", 4, 0.5)

# Row 1: Cross-coupled + pull-downs
x, y = grid(S7X, S7Y, 1, 0)
place_fet("XMN1", "nh", x, y, "b06_n1", "en", "gnd", "gnd", 15, 1)
x, y = grid(S7X, S7Y, 1, 1)
place_fet("XMN2", "nh", x, y, "en_bvdd", "b06_in_b", "gnd", "gnd", 15, 1)
x, y = grid(S7X, S7Y, 1, 2)
place_fet("XMP1", "ph", x, y, "b06_n1", "en_bvdd", "bvdd", "bvdd", 4, 0.5)
x, y = grid(S7X, S7Y, 1, 3)
place_fet("XMP2", "ph", x, y, "en_bvdd", "b06_n1", "bvdd", "bvdd", 5, 0.5)
out.append("")

# ================================================================
# SECTION 8: ZENER CLAMP (Block 07) — 13 FETs + 1 R
# ================================================================
S8X, S8Y = -1700, -3200
S8W, S8H = 2000, 1800
section("Section 8: Zener Clamp (Block 07)", "Hybrid N-P-N-P-N stack + 7x fast diodes + clamp NFET",
        S8X, S8Y, S8X + S8W, S8Y + S8H, layer=5)

# Precision stack (column 0): XMd1..XMd5 vertical
for i, (name, d, g, s, b, w, l, typ) in enumerate([
    ("XMd1", "pvdd", "pvdd", "b07_n4", "b07_n4", 2.2, 4, "nh"),
    ("XMd2", "b07_n3", "b07_n3", "b07_n4", "b07_n4", 20, 4, "ph"),
    ("XMd3", "b07_n3", "b07_n3", "b07_n2", "b07_n2", 2.2, 4, "nh"),
    ("XMd4", "b07_n1", "b07_n1", "b07_n2", "b07_n2", 20, 4, "ph"),
    ("XMd5", "b07_n1", "b07_n1", "b07_vg", "b07_vg", 2.2, 4, "nh"),
]):
    x, y = grid(S8X, S8Y, i, 0)
    place_fet(name, typ, x, y, d, g, s, b, w, l)

# Gate pulldown + clamp
x, y = grid(S8X, S8Y, 5, 0, cw=CW_P)
place_R("Rpd", x, y, "b07_vg", "gnd", "500k")
x, y = grid(S8X, S8Y, 5, 1)
place_fet("XMclamp", "nh", x, y, "pvdd", "b07_vg", "gnd", "gnd", 100, 0.5, m=4)

# Fast diode stack (column 2-3): XMf1..XMf7
for i, (name, d, g, s, b) in enumerate([
    ("XMf1", "pvdd", "pvdd", "b07_nf6", "gnd"),
    ("XMf2", "b07_nf6", "b07_nf6", "b07_nf5", "gnd"),
    ("XMf3", "b07_nf5", "b07_nf5", "b07_nf4", "gnd"),
    ("XMf4", "b07_nf4", "b07_nf4", "b07_nf3", "gnd"),
    ("XMf5", "b07_nf3", "b07_nf3", "b07_nf2", "gnd"),
    ("XMf6", "b07_nf2", "b07_nf2", "b07_nf1", "gnd"),
    ("XMf7", "b07_nf1", "b07_nf1", "gnd", "gnd"),
]):
    r, c = divmod(i, 2)
    x, y = grid(S8X + 600, S8Y, r, c)
    place_fet(name, "nh", x, y, d, g, s, b, 10, 0.5)
out.append("")

# ================================================================
# SECTION 9: MODE CONTROL (Block 08) — 62 FETs + 5 resistors
# ================================================================
S9X, S9Y = -3700, -1300
S9W, S9H = 8400, 5500
section("Section 9: Mode Control (Block 08)", "BVDD ladder + 4 Schmitt comparators + combinational logic — 62 FETs + 5 resistors",
        S9X, S9Y, S9X + S9W, S9Y + S9H, layer=4)

# --- Resistor Ladder (top-left of section) ---
T("Resistor Ladder (~400k)", S9X + 30, S9Y + 80, xm=0.28, ym=0.28, attrs="layer=4")
for i, (name, p, m, w, l) in enumerate([
    ("XRtop", "bvdd", "b08_tap1", 1, 37),
    ("XR12", "b08_tap1", "b08_tap2", 1, 62),
    ("XR23", "b08_tap2", "b08_tap3", 1, 6),
    ("XR34", "b08_tap3", "b08_tap4", 1, 17),
    ("XRbot", "b08_tap4", "gnd", 1, 69),
]):
    x, y = grid(S9X, S9Y, 0, i, cw=CW_P)
    place_rxh(name, x, y, p, m, "gnd", w, l)

# --- Comparators (rows 1-3) ---
T("Comparators (Schmitt trigger)", S9X + 30, S9Y + 380, xm=0.28, ym=0.28, attrs="layer=4")
COMP_Y0 = S9Y + 350
for ci, (tap, cinv, comp, hf_w) in enumerate([
    ("b08_tap1", "b08_c1inv", "b08_comp1", 1.6),
    ("b08_tap2", "b08_c2inv", "b08_comp2", 1.05),
    ("b08_tap3", "b08_c3inv", "b08_comp3", 0.9),
    ("b08_tap4", "b08_c4inv", "b08_comp4", 0.73),
]):
    cx0 = S9X + ci * 1200
    # INV1 PFET + NFET
    x, y = grid(cx0, COMP_Y0, 0, 0)
    place_fet(f"XMc{ci+1}ivp", "ph", x, y, cinv, tap, "pvdd", "pvdd", 2, 2)
    x, y = grid(cx0, COMP_Y0, 0, 1)
    place_fet(f"XMc{ci+1}ivn", "nh", x, y, cinv, tap, "gnd", "gnd", 2, 2)
    # INV2 PFET + NFET
    x, y = grid(cx0, COMP_Y0, 1, 0)
    place_fet(f"XMc{ci+1}iv2p", "ph", x, y, comp, cinv, "pvdd", "pvdd", 4, 2)
    x, y = grid(cx0, COMP_Y0, 1, 1)
    place_fet(f"XMc{ci+1}iv2n", "nh", x, y, comp, cinv, "gnd", "gnd", 2, 2)
    # Feedback NFET (Schmitt)
    x, y = grid(cx0, COMP_Y0, 1, 2)
    place_fet(f"XMhf{ci+1}", "nh", x, y, cinv, comp, "gnd", "gnd", hf_w, 100)
    # Comp label
    T(f"COMP{ci+1} (tap{ci+1})", cx0 + 30, COMP_Y0 + 15, xm=0.22, ym=0.22, attrs="layer=4")

# --- Logic section ---
LOGIC_Y0 = S9Y + 1450
T("Combinational Logic", S9X + 30, LOGIC_Y0, xm=0.28, ym=0.28, attrs="layer=4")

# Comp inverters (row 0)
T("comp1b..comp4b inverters", S9X + 30, LOGIC_Y0 + 30, xm=0.2, ym=0.2, attrs="layer=13")
for ci in range(4):
    cx0 = S9X + ci * 550
    comp_in = f"b08_comp{ci+1}"
    comp_out = f"b08_comp{ci+1}b"
    x, y = grid(cx0, LOGIC_Y0 + 20, 0, 0)
    place_fet(f"XMinv{ci+1}p", "ph", x, y, comp_out, comp_in, "pvdd", "pvdd", 4, 2)
    x, y = grid(cx0, LOGIC_Y0 + 20, 0, 1)
    place_fet(f"XMinv{ci+1}n", "nh", x, y, comp_out, comp_in, "gnd", "gnd", 2, 2)

# pass_off buffer (row 1, col 0)
T("pass_off = BUF(comp1b)", S9X + 30, LOGIC_Y0 + 310, xm=0.2, ym=0.2, attrs="layer=13")
x, y = grid(S9X, LOGIC_Y0 + 300, 0, 0)
place_fet("XMpo_bufp", "ph", x, y, "pass_off", "b08_comp1b", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, LOGIC_Y0 + 300, 0, 1)
place_fet("XMpo_bufn", "nh", x, y, "pass_off", "b08_comp1b", "gnd", "gnd", 2, 2)

# bypass_en logic (row 2)
T("bypass_en = (comp1 AND NOT comp2b) OR (comp3 AND NOT comp4b)", S9X + 30, LOGIC_Y0 + 570, xm=0.18, ym=0.18, attrs="layer=13")
BY_Y = LOGIC_Y0 + 560
# NMOS pull-down stack 1
x, y = grid(S9X, BY_Y, 0, 0)
place_fet("XMby_n1a", "nh", x, y, "b08_by_s1", "b08_comp1", "gnd", "gnd", 2, 2)
x, y = grid(S9X, BY_Y, 0, 1)
place_fet("XMby_n1b", "nh", x, y, "b08_bypass_enb", "b08_comp2b", "b08_by_s1", "b08_by_s1", 2, 2)
# NMOS pull-down stack 2
x, y = grid(S9X, BY_Y, 0, 2)
place_fet("XMby_n2a", "nh", x, y, "b08_by_s2", "b08_comp3", "gnd", "gnd", 2, 2)
x, y = grid(S9X, BY_Y, 0, 3)
place_fet("XMby_n2b", "nh", x, y, "b08_bypass_enb", "b08_comp4b", "b08_by_s2", "b08_by_s2", 2, 2)
# PMOS pull-up
x, y = grid(S9X, BY_Y, 1, 0)
place_fet("XMby_p1a", "ph", x, y, "b08_by_pmid", "b08_comp1", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, BY_Y, 1, 1)
place_fet("XMby_p1b", "ph", x, y, "b08_by_pmid", "b08_comp2b", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, BY_Y, 1, 2)
place_fet("XMby_p2a", "ph", x, y, "b08_bypass_enb", "b08_comp3", "b08_by_pmid", "b08_by_pmid", 4, 2)
x, y = grid(S9X, BY_Y, 1, 3)
place_fet("XMby_p2b", "ph", x, y, "b08_bypass_enb", "b08_comp4b", "b08_by_pmid", "b08_by_pmid", 4, 2)
# Output buffer
x, y = grid(S9X, BY_Y, 1, 4)
place_fet("XMby_outp", "ph", x, y, "bypass_en", "b08_bypass_enb", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, BY_Y, 1, 5)
place_fet("XMby_outn", "nh", x, y, "bypass_en", "b08_bypass_enb", "gnd", "gnd", 2, 2)

# ea_en logic (row 3)
EA_Y = LOGIC_Y0 + 1100
T("mc_ea_en = (comp2 AND NOT comp3b) OR comp4", S9X + 30, EA_Y, xm=0.18, ym=0.18, attrs="layer=13")
x, y = grid(S9X, EA_Y, 0, 0)
place_fet("XMea_n1a", "nh", x, y, "b08_ea_s1", "b08_comp2", "gnd", "gnd", 2, 2)
x, y = grid(S9X, EA_Y, 0, 1)
place_fet("XMea_n1b", "nh", x, y, "b08_ea_enb", "b08_comp3b", "b08_ea_s1", "b08_ea_s1", 2, 2)
x, y = grid(S9X, EA_Y, 0, 2)
place_fet("XMea_n2", "nh", x, y, "b08_ea_enb", "b08_comp4", "gnd", "gnd", 2, 2)
x, y = grid(S9X, EA_Y, 1, 0)
place_fet("XMea_p1a", "ph", x, y, "b08_ea_pmid", "b08_comp2", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, EA_Y, 1, 1)
place_fet("XMea_p1b", "ph", x, y, "b08_ea_pmid", "b08_comp3b", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, EA_Y, 1, 2)
place_fet("XMea_p2", "ph", x, y, "b08_ea_enb", "b08_comp4", "b08_ea_pmid", "b08_ea_pmid", 4, 2)
x, y = grid(S9X, EA_Y, 1, 3)
place_fet("XMea_outp", "ph", x, y, "mc_ea_en", "b08_ea_enb", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, EA_Y, 1, 4)
place_fet("XMea_outn", "nh", x, y, "mc_ea_en", "b08_ea_enb", "gnd", "gnd", 2, 2)

# ref_sel logic (row 4)
RS_Y = LOGIC_Y0 + 1640
T("ref_sel = comp1 AND NOT comp3b", S9X + 30, RS_Y, xm=0.18, ym=0.18, attrs="layer=13")
x, y = grid(S9X, RS_Y, 0, 0)
place_fet("XMrs_n1", "nh", x, y, "b08_rs_s1", "b08_comp1", "gnd", "gnd", 2, 2)
x, y = grid(S9X, RS_Y, 0, 1)
place_fet("XMrs_n2", "nh", x, y, "b08_ref_selb", "b08_comp3b", "b08_rs_s1", "b08_rs_s1", 2, 2)
x, y = grid(S9X, RS_Y, 0, 2)
place_fet("XMrs_p1", "ph", x, y, "b08_ref_selb", "b08_comp1", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, RS_Y, 0, 3)
place_fet("XMrs_p2", "ph", x, y, "b08_ref_selb", "b08_comp3b", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, RS_Y, 1, 0)
place_fet("XMrs_outp", "ph", x, y, "ref_sel", "b08_ref_selb", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X, RS_Y, 1, 1)
place_fet("XMrs_outn", "nh", x, y, "ref_sel", "b08_ref_selb", "gnd", "gnd", 2, 2)

# uvov_en logic (double inverter from comp4)
UV_EN_Y = LOGIC_Y0 + 2180
T("uvov_en = BUF(comp4)", S9X + 2500, UV_EN_Y, xm=0.18, ym=0.18, attrs="layer=13")
x, y = grid(S9X + 2500, UV_EN_Y, 0, 0)
place_fet("XMuv_p1", "ph", x, y, "b08_uvov_enb", "b08_comp4", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X + 2500, UV_EN_Y, 0, 1)
place_fet("XMuv_n1", "nh", x, y, "b08_uvov_enb", "b08_comp4", "gnd", "gnd", 2, 2)
x, y = grid(S9X + 2500, UV_EN_Y, 0, 2)
place_fet("XMuv_p2", "ph", x, y, "uvov_en", "b08_uvov_enb", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X + 2500, UV_EN_Y, 0, 3)
place_fet("XMuv_n2", "nh", x, y, "uvov_en", "b08_uvov_enb", "gnd", "gnd", 2, 2)

# ilim_en logic (double inverter from comp4)
T("ilim_en = BUF(comp4)", S9X + 2500, UV_EN_Y + 280, xm=0.18, ym=0.18, attrs="layer=13")
x, y = grid(S9X + 2500, UV_EN_Y + 270, 1, 0)
place_fet("XMil_p1", "ph", x, y, "b08_ilim_enb", "b08_comp4", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X + 2500, UV_EN_Y + 270, 1, 1)
place_fet("XMil_n1", "nh", x, y, "b08_ilim_enb", "b08_comp4", "gnd", "gnd", 2, 2)
x, y = grid(S9X + 2500, UV_EN_Y + 270, 1, 2)
place_fet("XMil_p2", "ph", x, y, "ilim_en", "b08_ilim_enb", "pvdd", "pvdd", 4, 2)
x, y = grid(S9X + 2500, UV_EN_Y + 270, 1, 3)
place_fet("XMil_n2", "nh", x, y, "ilim_en", "b08_ilim_enb", "gnd", "gnd", 2, 2)
out.append("")

# ================================================================
# SECTION 10: STARTUP CIRCUIT (Block 09) — 4 FETs + 7 resistors
# ================================================================
S10X, S10Y = 500, -3100
S10W, S10H = 2600, 1400
section("Section 10: Startup Circuit (Block 09)", "CG NFET level shifter + bootstrap + threshold detector",
        S10X, S10Y, S10X + S10W, S10Y + S10H, layer=4)

# Row 0: Bias divider + CG FET + Rload
x, y = grid(S10X, S10Y, 0, 0, cw=CW_P)
place_R("Rlb1", x, y, "bvdd", "b09_ls_bias", "200k")
x, y = grid(S10X, S10Y, 0, 1, cw=CW_P)
place_R("Rlb2", x, y, "b09_ls_bias", "gnd", "500k")
x, y = grid(S10X, S10Y, 0, 2)
place_fet("XMN_cg", "nh", x, y, "ea_out", "b09_ls_bias", "gate", "gnd", 1.2, 4)
x, y = grid(S10X, S10Y, 0, 3, cw=CW_P)
place_rxh("XR_load", x, y, "bvdd", "gate", "gnd", 1, 19)
x, y = grid(S10X, S10Y, 0, 4, cw=CW_P)
place_R("Ren", x, y, "bvdd", "ea_en", "100")

# Row 1: Threshold detector for startup_done
T("startup_done detector", S10X + 30, S10Y + 380, xm=0.2, ym=0.2, attrs="layer=13")
x, y = grid(S10X, S10Y, 1, 0, cw=CW_P)
place_rxh("XR_top_sd", x, y, "pvdd", "b09_sense_mid", "gnd", 2, 788)
x, y = grid(S10X, S10Y, 1, 1, cw=CW_P)
place_rxh("XR_bot_sd", x, y, "b09_sense_mid", "gnd", "gnd", 2, 212)
x, y = grid(S10X, S10Y, 1, 2)
place_fet("XMN_det", "nh", x, y, "b09_det_n", "b09_sense_mid", "gnd", "gnd", 4, 1)
x, y = grid(S10X, S10Y, 1, 3, cw=CW_P)
place_rxh("XR_pu", x, y, "bvdd", "b09_det_n", "gnd", 1, 2000)
x, y = grid(S10X, S10Y, 2, 0)
place_fet("XMP_inv1", "ph", x, y, "startup_done", "b09_det_n", "bvdd", "bvdd", 4, 1)
x, y = grid(S10X, S10Y, 2, 1)
place_fet("XMN_inv1", "nh", x, y, "startup_done", "b09_det_n", "gnd", "gnd", 2, 1)
out.append("")

# ================================================================
# TOP-LEVEL PASSIVES (Soft-start RC + Cload)
# ================================================================
comment("=" * 60)
comment("TOP-LEVEL PASSIVES")
comment("=" * 60)
TL_X, TL_Y = -3700, -1300
# Already inside section 9 area, put them separately
TL_X, TL_Y = 3500, -3200
rect_dashed(TL_X, TL_Y, TL_X + 800, TL_Y + 700, 13)
T("Top-Level Passives", TL_X + 15, TL_Y + 15, xm=0.3, ym=0.3, attrs="layer=13")
T("Soft-start + Output cap", TL_X + 15, TL_Y + 45, xm=0.2, ym=0.2, attrs="layer=13")

x, y = grid(TL_X, TL_Y, 0, 0, cw=CW_P)
place_R("Rss", x, y, "avbg", "vref_ss", "200k")
x, y = grid(TL_X, TL_Y, 0, 1, cw=CW_P)
place_C("Css", x, y, "vref_ss", "gnd", "30n")
x, y = grid(TL_X, TL_Y, 0, 2, cw=CW_P)
place_C("Cload", x, y, "pvdd", "gnd", "200p")
out.append("")

# ================================================================
# INTER-BLOCK NET ANNOTATIONS
# ================================================================
comment("INTER-BLOCK NET ANNOTATIONS")
anno_x, anno_y = -3700, 4400
T("Key Inter-Block Nets:", anno_x, anno_y, xm=0.35, ym=0.35, attrs="layer=4")
nets_info = [
    "bvdd — Battery supply input (5.4-10.5V) — to Pass Device, Current Limiter, Mode Control, Startup",
    "pvdd — Regulated 5.0V output — from Pass Device drain, to Feedback, Compensation, UV/OV, Zener",
    "gnd — Ground — shared by all blocks",
    "gate — Pass device gate (BVDD domain) — driven by Startup CG LS, sensed by Current Limiter",
    "ea_out — Error amp output (PVDD domain) — to Startup CG LS input, and Compensation",
    "vfb — Feedback voltage (~1.226V) — from Feedback divider to Error Amp (-) input",
    "vref_ss — Soft-started reference — avbg through RC filter to Error Amp (+) input",
    "ea_en — Error amp enable — from Startup (always BVDD) to Error Amp en pin",
    "uvov_en — UV/OV enable — from Mode Control to UV and OV comparators",
    "avbg — Bandgap reference (1.226V) — to UV/OV refs, Startup, Soft-start",
    "ibias — 1uA bias current — to Error Amp bias mirror",
]
for i, info in enumerate(nets_info):
    T(info, anno_x, anno_y + 35 + i * 25, xm=0.2, ym=0.2, attrs="layer=13")

# ================================================================
# WRITE OUTPUT
# ================================================================
outpath = "/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration/pvdd_regulator_full.sch"
with open(outpath, "w") as f:
    f.write("\n".join(out) + "\n")

print(f"Generated {outpath}")
print(f"Total xschem elements: {len(out)}")
print(f"Total components placed: {PIN_C // 4} (approx, based on pin count / 4)")
