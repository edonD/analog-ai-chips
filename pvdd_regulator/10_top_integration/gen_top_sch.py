#!/usr/bin/env python3
"""Generate the PVDD 5V LDO Regulator top-level block diagram as xschem .sch.
Uses L (line) elements for rectangles to avoid filled/opaque boxes."""

lines = []

def L(layer, x1, y1, x2, y2, attrs=""):
    """Graphical line element."""
    lines.append(f"L {layer} {x1} {y1} {x2} {y2} {{{attrs}}}")

def T(text, x, y, rot=0, flip=0, xm=0.4, ym=0.4, attrs=""):
    lines.append(f'T {{{text}}} {x} {y} {rot} {flip} {xm} {ym} {{{attrs}}}')

def N(x1, y1, x2, y2, lab=""):
    if lab:
        lines.append(f'N {x1} {y1} {x2} {y2} {{lab={lab}}}')
    else:
        lines.append(f'N {x1} {y1} {x2} {y2} {{}}')

def C(sym, x, y, rot=0, flip=0, attrs=""):
    lines.append(f'C {{{sym}}} {x} {y} {rot} {flip} {{{attrs}}}')

def lab_pin(x, y, rot, name, pname):
    C("/usr/share/xschem/xschem_library/devices/lab_pin.sym",
      x, y, rot, 0, f"name={pname} sig_type=std_logic lab={name}")

def ipin(x, y, name, pname, rot=0):
    C("/usr/share/xschem/xschem_library/devices/ipin.sym",
      x, y, rot, 0, f"name={pname} lab={name}")

def opin(x, y, name, pname, rot=0):
    C("/usr/share/xschem/xschem_library/devices/opin.sym",
      x, y, rot, 0, f"name={pname} lab={name}")

def iopin(x, y, name, pname, rot=0):
    C("/usr/share/xschem/xschem_library/devices/iopin.sym",
      x, y, rot, 0, f"name={pname} lab={name}")

def comment(text):
    lines.append(f"* {text}")

def rect(x1, y1, x2, y2, layer=8):
    """Draw rectangle outline using 4 L lines."""
    L(layer, x1, y1, x2, y1)  # top
    L(layer, x2, y1, x2, y2)  # right
    L(layer, x2, y2, x1, y2)  # bottom
    L(layer, x1, y2, x1, y1)  # left

def block_box(name, desc, block_num, x1, y1, x2, y2, layer=8):
    """Draw a labeled block rectangle."""
    rect(x1, y1, x2, y2, layer)
    # Double outline for emphasis
    rect(x1-2, y1-2, x2+2, y2+2, layer)
    cx = (x1 + x2) // 2
    if block_num is not None:
        T(f"Block {block_num:02d}", cx - 60, y1 + 18, xm=0.22, ym=0.22, attrs=f"layer=13")
    T(name, cx - 80, y1 + 40, xm=0.4, ym=0.4, attrs=f"layer={layer}")
    if desc:
        T(desc, cx - 80, y1 + 68, xm=0.22, ym=0.22, attrs="layer=13")

# ================================================================
# HEADER
# ================================================================
lines.append("v {xschem version=3.4.6 file_version=1.2}")
lines.append("G {}")
lines.append('K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}')
lines.append("V {}")
lines.append("S {}")
lines.append("E {}")
lines.append("")

# ================================================================
# TITLE AND LEGEND
# ================================================================
T("PVDD 5V LDO Regulator", -1800, -2000, xm=1.1, ym=1.1, attrs="layer=4")
T("Top-Level Block Diagram", -1800, -1920, xm=0.6, ym=0.6, attrs="layer=8")
T("SkyWater SKY130A  |  10 Sub-blocks + Passives  |  Block 10: Top Integration",
  -1800, -1870, xm=0.32, ym=0.32, attrs="")
lines.append("")
T("Color Legend:", -1800, -1820, xm=0.3, ym=0.3, attrs="layer=13")
T("BVDD (5.4-10.5V)", -1590, -1820, xm=0.3, ym=0.3, attrs="layer=4")
T("PVDD (5.0V)", -1250, -1820, xm=0.3, ym=0.3, attrs="layer=5")
T("SVDD (2.2V)", -970, -1820, xm=0.3, ym=0.3, attrs="layer=7")
T("Internal", -710, -1820, xm=0.3, ym=0.3, attrs="layer=13")
lines.append("")

# Title block
C("/usr/share/xschem/xschem_library/devices/title.sym",
  -1800, 900, 0, 0,
  'name=l1 author="PVDD 5V LDO Regulator -- Top-Level Block Diagram -- Analog AI Chips"')
lines.append("")

# ================================================================
# EXTERNAL PORT PINS
# ================================================================
comment("EXTERNAL PORT PINS")

# Left side inputs
ipin(-1800, -1200, "bvdd", "p_bvdd")
T("BVDD (5.4-10.5V)", -1730, -1210, xm=0.32, ym=0.32, attrs="layer=4")

ipin(-1800, -1050, "avbg", "p_avbg")
T("AVBG (1.226V ref)", -1730, -1060, xm=0.32, ym=0.32, attrs="layer=13")

ipin(-1800, -950, "ibias", "p_ibias")
T("IBIAS (1uA)", -1730, -960, xm=0.32, ym=0.32, attrs="layer=13")

ipin(-1800, -500, "svdd", "p_svdd")
T("SVDD (2.2V)", -1730, -510, xm=0.32, ym=0.32, attrs="layer=7")

ipin(-1800, -400, "en", "p_en")
T("EN (active HIGH)", -1730, -410, xm=0.32, ym=0.32, attrs="layer=7")

ipin(-1800, -300, "en_ret", "p_en_ret")
T("EN_RET (retention)", -1730, -310, xm=0.32, ym=0.32, attrs="layer=7")

iopin(-1800, 650, "gnd", "p_gnd")
T("GND", -1740, 640, xm=0.35, ym=0.35, attrs="")

# Right side outputs
opin(3000, -1050, "pvdd", "p_pvdd")
T("PVDD (5.0V reg)", 2870, -1060, xm=0.35, ym=0.35, attrs="layer=5")

opin(3000, -1650, "uv_flag", "p_uv_flag")
T("UV_FLAG", 2880, -1660, xm=0.32, ym=0.32, attrs="layer=7")

opin(3000, -1450, "ov_flag", "p_ov_flag")
T("OV_FLAG", 2880, -1460, xm=0.32, ym=0.32, attrs="layer=7")
lines.append("")

# ================================================================
# BLOCK LAYOUT
# ================================================================
# Row 1 (protection): y ~ -1750 to -1450
# Row 2 (regulation): y ~ -1300 to -950
# Row 3 (support): y ~ -750 to -500
# Row 4 (control): y ~ -200 to 250

# ---------------------------------------------------------------
# BLOCK 01: PASS DEVICE
# ---------------------------------------------------------------
comment("BLOCK 01: PASS DEVICE")
b01 = (1600, -1300, 2150, -1000)
block_box("Pass Device", "PMOS 10x100u/0.5u", 1, *b01, layer=4)

T("gate", b01[0]+12, -1200, xm=0.25, ym=0.25, attrs="layer=4")
T("bvdd", 1780, b01[1]+12, xm=0.25, ym=0.25, attrs="layer=4")
T("pvdd", b01[2]-65, -1170, xm=0.25, ym=0.25, attrs="layer=5")

lab_pin(b01[0], -1180, 0, "gate", "lp01g")
lab_pin(1800, b01[1], 3, "bvdd", "lp01bv")
lab_pin(b01[2], -1150, 2, "pvdd", "lp01pv")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 00: ERROR AMPLIFIER
# ---------------------------------------------------------------
comment("BLOCK 00: ERROR AMPLIFIER")
b00 = (-200, -1350, 500, -1000)
block_box("Error Amplifier", "Two-stage Miller OTA", 0, *b00, layer=5)

T("vref_ss (+)", b00[0]+12, -1280, xm=0.23, ym=0.23, attrs="layer=13")
T("vfb (-)", b00[0]+12, -1210, xm=0.23, ym=0.23, attrs="layer=13")
T("ibias", b00[0]+12, -1140, xm=0.23, ym=0.23, attrs="layer=13")
T("ea_out", b00[2]-80, -1210, xm=0.23, ym=0.23, attrs="layer=13")
T("pvdd", 50, b00[1]+12, xm=0.22, ym=0.22, attrs="layer=5")
T("gnd", 50, b00[3]-20, xm=0.22, ym=0.22, attrs="")
T("ea_en", 250, b00[3]-20, xm=0.22, ym=0.22, attrs="layer=13")

lab_pin(b00[0], -1270, 0, "vref_ss", "lp00vr")
lab_pin(b00[0], -1200, 0, "vfb", "lp00vf")
lab_pin(b00[0], -1130, 0, "ibias", "lp00ib")
lab_pin(b00[2], -1200, 2, "ea_out", "lp00ea")
lab_pin(80, b00[1], 3, "pvdd", "lp00pv")
lab_pin(80, b00[3], 1, "gnd", "lp00gn")
lab_pin(280, b00[3], 1, "ea_en", "lp00en")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 09: STARTUP
# ---------------------------------------------------------------
comment("BLOCK 09: STARTUP")
b09 = (700, -1350, 1400, -1000)
block_box("Startup Circuit", "Bootstrap + CG Level Shifter", 9, *b09, layer=4)

T("ea_out", b09[0]+12, -1270, xm=0.23, ym=0.23, attrs="layer=13")
T("ea_en", b09[0]+12, -1200, xm=0.23, ym=0.23, attrs="layer=13")
T("avbg", b09[0]+12, -1130, xm=0.23, ym=0.23, attrs="layer=13")
T("gate", b09[2]-60, -1200, xm=0.23, ym=0.23, attrs="layer=4")
T("bvdd", 950, b09[1]+12, xm=0.22, ym=0.22, attrs="layer=4")
T("pvdd", 850, b09[3]-20, xm=0.22, ym=0.22, attrs="layer=5")
T("gnd", 1050, b09[3]-20, xm=0.22, ym=0.22, attrs="")
T("startup_done", 1150, b09[3]-20, xm=0.18, ym=0.18, attrs="layer=13")

lab_pin(b09[0], -1260, 0, "ea_out", "lp09ea")
lab_pin(b09[0], -1190, 0, "ea_en", "lp09en")
lab_pin(b09[0], -1120, 0, "avbg", "lp09av")
lab_pin(b09[2], -1190, 2, "gate", "lp09g")
lab_pin(980, b09[1], 3, "bvdd", "lp09bv")
lab_pin(880, b09[3], 1, "pvdd", "lp09pv")
lab_pin(1080, b09[3], 1, "gnd", "lp09gn")
lab_pin(1250, b09[3], 1, "startup_done", "lp09sd")
lines.append("")

# ---------------------------------------------------------------
# SOFT-START RC
# ---------------------------------------------------------------
comment("SOFT-START RC")
ss = (-900, -1300, -400, -1100)
rect(*ss, layer=13)
T("Soft-Start RC", -870, ss[1]+18, xm=0.32, ym=0.32, attrs="layer=13")
T("Rss=200k", -870, ss[1]+48, xm=0.22, ym=0.22, attrs="layer=13")
T("Css=30nF", -870, ss[1]+68, xm=0.22, ym=0.22, attrs="layer=13")
T("tau=6ms", -870, ss[1]+88, xm=0.22, ym=0.22, attrs="layer=13")

T("avbg", ss[0]+12, -1220, xm=0.22, ym=0.22, attrs="layer=13")
T("vref_ss", ss[2]-85, -1220, xm=0.22, ym=0.22, attrs="layer=13")
T("gnd", -680, ss[3]-18, xm=0.22, ym=0.22, attrs="")

lab_pin(ss[0], -1210, 0, "avbg", "lpss_av")
lab_pin(ss[2], -1210, 2, "vref_ss", "lpss_vr")
lab_pin(-650, ss[3], 1, "gnd", "lpss_gn")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 02: FEEDBACK NETWORK
# ---------------------------------------------------------------
comment("BLOCK 02: FEEDBACK NETWORK")
b02 = (700, -750, 1300, -500)
block_box("Feedback Network", "R_top=364k R_bot=118k", 2, *b02, layer=5)

T("pvdd", 900, b02[1]+12, xm=0.22, ym=0.22, attrs="layer=5")
T("vfb", b02[0]+12, -650, xm=0.23, ym=0.23, attrs="layer=13")
T("gnd", 950, b02[3]-18, xm=0.22, ym=0.22, attrs="")

lab_pin(930, b02[1], 3, "pvdd", "lp02pv")
lab_pin(b02[0], -640, 0, "vfb", "lp02vf")
lab_pin(980, b02[3], 1, "gnd", "lp02gn")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 03: COMPENSATION
# ---------------------------------------------------------------
comment("BLOCK 03: COMPENSATION")
b03 = (-200, -750, 450, -500)
block_box("Compensation", "Cc=30pF Rz=5k Cout=50pF", 3, *b03, layer=5)

T("ea_out", b03[0]+12, -660, xm=0.22, ym=0.22, attrs="layer=13")
T("pvdd", b03[2]-65, -660, xm=0.22, ym=0.22, attrs="layer=5")
T("gnd", 80, b03[3]-18, xm=0.22, ym=0.22, attrs="")

lab_pin(b03[0], -650, 0, "ea_out", "lp03ea")
lab_pin(b03[2], -650, 2, "pvdd", "lp03pv")
lab_pin(110, b03[3], 1, "gnd", "lp03gn")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 04: CURRENT LIMITER
# ---------------------------------------------------------------
comment("BLOCK 04: CURRENT LIMITER")
b04 = (300, -1750, 1000, -1500)
block_box("Current Limiter", "Sense mirror, Ilim~70mA", 4, *b04, layer=4)

T("gate", b04[0]+12, -1650, xm=0.22, ym=0.22, attrs="layer=4")
T("bvdd", 550, b04[1]+12, xm=0.22, ym=0.22, attrs="layer=4")
T("pvdd", b04[2]-65, -1660, xm=0.22, ym=0.22, attrs="layer=5")
T("gnd", 550, b04[3]-18, xm=0.22, ym=0.22, attrs="")
T("ilim_flag", b04[2]-100, -1600, xm=0.2, ym=0.2, attrs="layer=13")

lab_pin(b04[0], -1640, 0, "gate", "lp04g")
lab_pin(580, b04[1], 3, "bvdd", "lp04bv")
lab_pin(b04[2], -1650, 2, "pvdd", "lp04pv")
lab_pin(580, b04[3], 1, "gnd", "lp04gn")
lab_pin(b04[2], -1590, 2, "ilim_flag", "lp04fl")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 05: UV COMPARATOR
# ---------------------------------------------------------------
comment("BLOCK 05: UV COMPARATOR")
b5a = (1500, -1750, 2200, -1550)
block_box("UV Comparator", "Trip: PVDD < 4.3V", 5, *b5a, layer=7)

T("pvdd", b5a[0]+12, -1680, xm=0.22, ym=0.22, attrs="layer=5")
T("avbg", b5a[0]+12, -1640, xm=0.22, ym=0.22, attrs="layer=13")
T("uvov_en", b5a[0]+12, -1720, xm=0.2, ym=0.2, attrs="layer=13")
T("uv_flag", b5a[2]-90, -1670, xm=0.22, ym=0.22, attrs="layer=7")
T("svdd", 1750, b5a[1]+12, xm=0.2, ym=0.2, attrs="layer=7")
T("gnd", 1750, b5a[3]-16, xm=0.2, ym=0.2, attrs="")

lab_pin(b5a[0], -1670, 0, "pvdd", "lp5apv")
lab_pin(b5a[0], -1630, 0, "avbg", "lp5aav")
lab_pin(b5a[0], -1710, 0, "uvov_en", "lp5aen")
lab_pin(b5a[2], -1660, 2, "uv_flag", "lp5auf")
lab_pin(1780, b5a[1], 3, "svdd", "lp5asv")
lab_pin(1780, b5a[3], 1, "gnd", "lp5agn")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 05: OV COMPARATOR
# ---------------------------------------------------------------
comment("BLOCK 05: OV COMPARATOR")
b5b = (1500, -1500, 2200, -1300)
block_box("OV Comparator", "Trip: PVDD > 5.5V", 5, *b5b, layer=7)

T("pvdd", b5b[0]+12, -1430, xm=0.22, ym=0.22, attrs="layer=5")
T("avbg", b5b[0]+12, -1390, xm=0.22, ym=0.22, attrs="layer=13")
T("uvov_en", b5b[0]+12, -1470, xm=0.2, ym=0.2, attrs="layer=13")
T("ov_flag", b5b[2]-90, -1420, xm=0.22, ym=0.22, attrs="layer=7")
T("svdd", 1750, b5b[1]+12, xm=0.2, ym=0.2, attrs="layer=7")
T("gnd", 1750, b5b[3]-16, xm=0.2, ym=0.2, attrs="")

lab_pin(b5b[0], -1420, 0, "pvdd", "lp5bpv")
lab_pin(b5b[0], -1380, 0, "avbg", "lp5bav")
lab_pin(b5b[0], -1460, 0, "uvov_en", "lp5ben")
lab_pin(b5b[2], -1410, 2, "ov_flag", "lp5bof")
lab_pin(1780, b5b[1], 3, "svdd", "lp5bsv")
lab_pin(1780, b5b[3], 1, "gnd", "lp5bgn")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 07: ZENER CLAMP
# ---------------------------------------------------------------
comment("BLOCK 07: ZENER CLAMP")
b07 = (2350, -1300, 2800, -1050)
block_box("Zener Clamp", "Hybrid ~6V clamp", 7, *b07, layer=5)

T("pvdd", b07[0]+12, -1200, xm=0.22, ym=0.22, attrs="layer=5")
T("gnd", 2530, b07[3]-18, xm=0.22, ym=0.22, attrs="")

lab_pin(b07[0], -1190, 0, "pvdd", "lp07pv")
lab_pin(2560, b07[3], 1, "gnd", "lp07gn")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 08: MODE CONTROL
# ---------------------------------------------------------------
comment("BLOCK 08: MODE CONTROL")
b08 = (-100, -350, 1000, 200)
block_box("Mode Control", "BVDD ladder + Schmitt + logic", 8, *b08, layer=4)

# Left pins
left_pins = [
    ("bvdd", -270, 4), ("pvdd", -210, 5), ("svdd", -150, 7),
    ("avbg", -90, 13), ("en_ret", -30, 7)
]
for name, y, layer in left_pins:
    T(name, b08[0]+12, y, xm=0.22, ym=0.22, attrs=f"layer={layer}")
    lab_pin(b08[0], y+10, 0, name, f"lp08_{name}")

T("gnd", 400, b08[3]-18, xm=0.22, ym=0.22, attrs="")
lab_pin(430, b08[3], 1, "gnd", "lp08gn")

# Right pins (outputs)
right_pins = [
    ("bypass_en", -270, 13), ("mc_ea_en", -210, 13),
    ("ref_sel", -150, 13), ("uvov_en", -90, 13),
    ("ilim_en", -30, 13), ("pass_off", 30, 13)
]
for name, y, layer in right_pins:
    T(name, b08[2]-110, y, xm=0.22, ym=0.22, attrs=f"layer={layer}")
    lab_pin(b08[2], y+10, 2, name, f"lp08_{name}")
lines.append("")

# ---------------------------------------------------------------
# BLOCK 06: LEVEL SHIFTER
# ---------------------------------------------------------------
comment("BLOCK 06: LEVEL SHIFTER UP")
b06 = (-1200, -350, -550, -150)
block_box("Level Shifter", "SVDD -> BVDD", 6, *b06, layer=7)

T("en", b06[0]+12, -280, xm=0.22, ym=0.22, attrs="layer=7")
T("en_bvdd", b06[2]-95, -280, xm=0.22, ym=0.22, attrs="layer=4")
T("bvdd", -1000, b06[1]+12, xm=0.2, ym=0.2, attrs="layer=4")
T("svdd", -800, b06[1]+12, xm=0.2, ym=0.2, attrs="layer=7")
T("gnd", -900, b06[3]-16, xm=0.2, ym=0.2, attrs="")

lab_pin(b06[0], -270, 0, "en", "lp06en")
lab_pin(b06[2], -270, 2, "en_bvdd", "lp06eb")
lab_pin(-970, b06[1], 3, "bvdd", "lp06bv")
lab_pin(-770, b06[1], 3, "svdd", "lp06sv")
lab_pin(-870, b06[3], 1, "gnd", "lp06gn")
lines.append("")

# ---------------------------------------------------------------
# Cload
# ---------------------------------------------------------------
comment("Cload — 200 pF")
cl = (1650, -750, 2000, -550)
rect(*cl, layer=5)
T("Cload", 1680, cl[1]+18, xm=0.3, ym=0.3, attrs="layer=5")
T("200 pF", 1680, cl[1]+48, xm=0.25, ym=0.25, attrs="layer=5")

T("pvdd", 1770, cl[1]+12, xm=0.2, ym=0.2, attrs="layer=5")
T("gnd", 1770, cl[3]-16, xm=0.2, ym=0.2, attrs="")

lab_pin(1800, cl[1], 3, "pvdd", "lp_cl_pv")
lab_pin(1800, cl[3], 1, "gnd", "lp_cl_gn")
lines.append("")

# ================================================================
# MAIN SIGNAL-FLOW WIRES
# ================================================================
comment("MAIN SIGNAL FLOW WIRES")
lines.append("")

# === Main regulation loop ===

# avbg input → soft-start RC
N(-1800, -1050, -1400, -1050, "avbg")
N(-1400, -1050, -1400, -1210)
N(-1400, -1210, ss[0], -1210, "avbg")

# vref_ss: soft-start → EA
N(ss[2], -1210, -450, -1210)
N(-450, -1210, -450, -1270)
N(-450, -1270, b00[0], -1270, "vref_ss")

# ea_out: EA → startup
N(b00[2], -1200, 600, -1200)
N(600, -1200, 600, -1260)
N(600, -1260, b09[0], -1260, "ea_out")

# gate: startup → pass device
N(b09[2], -1190, b01[0], -1180, "gate")

# pvdd: pass device → output (right)
N(b01[2], -1150, 2700, -1150, "pvdd")
N(2700, -1150, 2700, -1050)
N(2700, -1050, 3000, -1050, "pvdd")

# bvdd: input → horizontal bus across top → pass device
N(-1800, -1200, -1550, -1200, "bvdd")
N(-1550, -1200, -1550, -1800)
N(-1550, -1800, 1800, -1800, "bvdd")
N(1800, -1800, 1800, b01[1], "bvdd")

# ibias: input → EA
N(-1800, -950, -1300, -950)
N(-1300, -950, -1300, -1130)
N(-1300, -1130, b00[0], -1130, "ibias")

# pvdd bus → feedback network (vertical drop from output bus)
N(2700, -1150, 2700, -800)
N(2700, -800, 930, -800)
N(930, -800, 930, b02[1], "pvdd")

# vfb: feedback → EA (loop return via bottom)
N(b02[0], -640, -350, -640)
N(-350, -640, -350, -1200)
N(-350, -1200, b00[0], -1200, "vfb")

# === Protection wires ===

# uv_flag: UV comp → output
N(b5a[2], -1660, 2600, -1660)
N(2600, -1660, 2600, -1650)
N(2600, -1650, 3000, -1650, "uv_flag")

# ov_flag: OV comp → output
N(b5b[2], -1410, 2600, -1410)
N(2600, -1410, 2600, -1450)
N(2600, -1450, 3000, -1450, "ov_flag")

# === Enable path ===

# en: input → level shifter
N(-1800, -400, -1400, -400)
N(-1400, -400, -1400, -270)
N(-1400, -270, b06[0], -270, "en")

# en_ret: input → mode control
N(-1800, -300, -1500, -300)
N(-1500, -300, -1500, -20)
N(-1500, -20, b08[0], -20, "en_ret")

# svdd: input → horizontal
N(-1800, -500, -1500, -500, "svdd")
lines.append("")

# ================================================================
# SIGNAL FLOW ANNOTATIONS
# ================================================================
comment("SIGNAL FLOW ANNOTATIONS")

# Flow arrows along main loop
T(">>>", -320, -1280, xm=0.4, ym=0.4, attrs="layer=13")
T(">>>", 530, -1270, xm=0.4, ym=0.4, attrs="layer=13")
T(">>>", 1430, -1195, xm=0.4, ym=0.4, attrs="layer=13")
T(">>>", 2200, -1160, xm=0.4, ym=0.4, attrs="layer=5")
T("<<<", -380, -655, xm=0.35, ym=0.35, attrs="layer=5")

# Numbered signal flow
T("1. avbg ramps via RC soft-start", -880, -1090, xm=0.22, ym=0.22, attrs="layer=13")
T("2. vref_ss drives EA non-inv input", -380, -1385, xm=0.22, ym=0.22, attrs="layer=13")
T("3. ea_out -> CG level shifter in startup block", 510, -1385, xm=0.22, ym=0.22, attrs="layer=13")
T("4. gate controls pass PMOS (BVDD domain)", 1420, -1385, xm=0.22, ym=0.22, attrs="layer=4")
T("5. PVDD regulated output", 2250, -1000, xm=0.22, ym=0.22, attrs="layer=5")
T("6. Feedback divider sets vfb = 1.226V at 5.0V", 600, -770, xm=0.22, ym=0.22, attrs="layer=5")
T("7. Compensation stabilizes loop (PM > 70 deg)", -180, -480, xm=0.22, ym=0.22, attrs="layer=5")

# Power flow
T("BVDD =========================> PVDD (power flow left to right)", -200, -1830, xm=0.25, ym=0.25, attrs="layer=4")

# Mode control annotations
T("Mode Control outputs:", 1050, -310, xm=0.23, ym=0.23, attrs="layer=13")
T("uvov_en -> UV/OV comparator enable", 1050, -280, xm=0.2, ym=0.2, attrs="layer=13")
T("ea_en -> Error amp enable (via startup)", 1050, -255, xm=0.2, ym=0.2, attrs="layer=13")
T("ilim_en -> Current limiter enable", 1050, -230, xm=0.2, ym=0.2, attrs="layer=13")
T("bypass_en, ref_sel, pass_off -> reserved", 1050, -205, xm=0.2, ym=0.2, attrs="layer=13")
lines.append("")

# ================================================================
# NET NAME ANNOTATIONS on wires
# ================================================================
comment("NET LABELS ON WIRES")

T("vref_ss", -430, -1240, xm=0.25, ym=0.25, attrs="layer=13")
T("ea_out", 540, -1230, xm=0.25, ym=0.25, attrs="layer=13")
T("gate", 1440, -1210, xm=0.28, ym=0.28, attrs="layer=4")
T("vfb (loop return)", -330, -680, xm=0.22, ym=0.22, attrs="layer=13")
T("pvdd bus", 2710, -1000, xm=0.22, ym=0.22, attrs="layer=5")
T("bvdd bus", 200, -1815, xm=0.25, ym=0.25, attrs="layer=4")
lines.append("")

# ================================================================
# DOMAIN BOUNDARY ANNOTATIONS (text-only, no filled boxes)
# ================================================================
comment("DOMAIN ANNOTATIONS")

# BVDD domain dashed boundary
L(4, -1560, -1810, 2160, -1810, "dash=5")
L(4, 2160, -1810, 2160, -960, "dash=5")
L(4, 2160, -960, -1560, -960, "dash=5")
L(4, -1560, -960, -1560, -1810, "dash=5")
T("BVDD DOMAIN", -1540, -1810, xm=0.2, ym=0.2, attrs="layer=4")

# PVDD domain
L(5, -250, -780, 2050, -780, "dash=5")
L(5, 2050, -780, 2050, -470, "dash=5")
L(5, 2050, -470, -250, -470, "dash=5")
L(5, -250, -470, -250, -780, "dash=5")
T("PVDD DOMAIN", -240, -780, xm=0.2, ym=0.2, attrs="layer=5")

# SVDD domain
L(7, 1470, -1780, 2250, -1780, "dash=5")
L(7, 2250, -1780, 2250, -1280, "dash=5")
L(7, 2250, -1280, 1470, -1280, "dash=5")
L(7, 1470, -1280, 1470, -1780, "dash=5")
T("SVDD DOMAIN", 1480, -1780, xm=0.2, ym=0.2, attrs="layer=7")

# Write file
outpath = "/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration/pvdd_regulator_top.sch"
with open(outpath, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Generated {outpath}")
print(f"Total lines: {len(lines)}")
