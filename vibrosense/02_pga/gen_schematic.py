#!/usr/bin/env python3
"""Generate a clean, professional xschem schematic for the PGA block.

Same circuit, same components, same connections — just laid out with
more spacing, cleaner wire routing, and readable labels.
"""

import os, subprocess, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── Paths ────────────────────────────────────────────────────────────
SKY = ("/home/ubuntu/.volare/volare/sky130/versions/"
       "6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/"
       "sky130A/libs.tech/xschem/sky130_fd_pr")
DEV = "/usr/share/xschem/xschem_library/devices"

NFET  = f"{SKY}/nfet_01v8.sym"
PFET  = f"{SKY}/pfet_01v8.sym"
MIM   = f"{SKY}/cap_mim_m3_1.sym"
IOPIN = f"{DEV}/iopin.sym"
LABPIN = f"{DEV}/lab_pin.sym"

lines = []

# ── Helpers ──────────────────────────────────────────────────────────
def T(text, x, y, rot=0, mir=0, sx=0.3, sy=0.3, layer=8):
    lines.append(f'T {{{text}}} {x} {y} {rot} {mir} {sx} {sy} {{layer={layer}}}')

def N(x1, y1, x2, y2, lab=""):
    lines.append(f'N {x1} {y1} {x2} {y2} {{lab={lab}}}' if lab
                 else f'N {x1} {y1} {x2} {y2} {{}}')

def nmos(name, x, y, w, l, mir=0):
    lines.append(
        f'C {{{NFET}}} {x} {y} 0 {mir} {{name=X{name}\n'
        f'W={w}\nL={l}\nnf=1\nmult=1\nmodel=nfet_01v8\nspiceprefix=X\n}}')

def pmos(name, x, y, w, l, mir=0):
    lines.append(
        f'C {{{PFET}}} {x} {y} 0 {mir} {{name=X{name}\n'
        f'W={w}\nL={l}\nnf=1\nmult=1\nmodel=pfet_01v8\nspiceprefix=X\n}}')

def mim(name, x, y, w, l):
    lines.append(
        f'C {{{MIM}}} {x} {y} 0 0 {{name=X{name}\n'
        f'W={w}\nL={l}\nMF=1\nmodel=cap_mim_m3_1\nspiceprefix=X\n}}')

def iopin(name, x, y, rot=0, mir=0, lab=""):
    lines.append(f'C {{{IOPIN}}} {x} {y} {rot} {mir} {{name={name} lab={lab}}}')

def labpin(name, x, y, rot=0, mir=0, lab=""):
    lines.append(f'C {{{LABPIN}}} {x} {y} {rot} {mir} {{name={name} lab={lab}}}')

def box(x1, y1, x2, y2, layer=3):
    """Dashed rectangle (layer 3 = background grey)."""
    lines.append(f'L {layer} {x1} {y1} {x2} {y1} {{dash=4}}')
    lines.append(f'L {layer} {x2} {y1} {x2} {y2} {{dash=4}}')
    lines.append(f'L {layer} {x2} {y2} {x1} {y2} {{dash=4}}')
    lines.append(f'L {layer} {x1} {y2} {x1} {y1} {{dash=4}}')

def solidbox(x1, y1, x2, y2, layer=7):
    """Solid rectangle."""
    lines.append(f'L {layer} {x1} {y1} {x2} {y1} {{}}')
    lines.append(f'L {layer} {x2} {y1} {x2} {y2} {{}}')
    lines.append(f'L {layer} {x2} {y2} {x1} {y2} {{}}')
    lines.append(f'L {layer} {x1} {y2} {x1} {y1} {{}}')

def triangle(cx, cy, size=60, layer=7):
    """OTA triangle symbol pointing right."""
    s = size
    # Left vertical edge, top-right diagonal, bottom-right diagonal
    lines.append(f'L {layer} {cx - s} {cy - s} {cx - s} {cy + s} {{}}')
    lines.append(f'L {layer} {cx - s} {cy - s} {cx + s} {cy} {{}}')
    lines.append(f'L {layer} {cx - s} {cy + s} {cx + s} {cy} {{}}')


# ══════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════
lines.append('v {xschem version=3.4.4 file_version=1.2}')
for sec in 'GKVSE':
    lines.append(f'{sec} {{}}')

# ══════════════════════════════════════════════════════════════════════
#  LAYOUT GRID — generous spacing
#
#  X layout:
#    -900..-300  Decoder
#    -100..500   Input caps + switches
#     600..1100  OTA + feedback
#
#  Y layout:
#    -2400       Title
#    -2200       VDD rail
#    -2100..-800 Main circuit
#    -700        VSS rail
# ══════════════════════════════════════════════════════════════════════

VDD_Y = -2200
VSS_Y = -700
VCM_Y = -950    # common-mode reference line

# ── Title block ──────────────────────────────────────────────────────
T("VibroSense Block 02 — Programmable Gain Amplifier (PGA)",
  -900, -2450, sx=0.9, sy=0.9, layer=15)
T("Capacitive-Feedback  |  4-Gain (1x / 4x / 16x / 64x)  |  SKY130A",
  -900, -2390, sx=0.45, sy=0.45, layer=15)
T("Gain err < 0.15 dB  |  BW = 27 kHz @ 16x  |  THD = 0.19 %  |  P = 9.94 uW  |  49 transistors",
  -900, -2340, sx=0.35, sy=0.35, layer=8)

# ── Supply rails (horizontal) ───────────────────────────────────────
N(-900, VDD_Y, 1200, VDD_Y, "VDD")
N(-900, VSS_Y, 1200, VSS_Y, "VSS")
iopin("p_vdd", -900, VDD_Y, rot=0, mir=1, lab="VDD")
iopin("p_vss", -900, VSS_Y, rot=0, mir=1, lab="VSS")
T("VDD = 1.8 V", -850, VDD_Y - 30, sx=0.3, sy=0.3, layer=4)
T("VSS = 0 V", -850, VSS_Y + 15, sx=0.3, sy=0.3, layer=4)

# ══════════════════════════════════════════════════════════════════════
#  SECTION 1: 2-to-4 CMOS DECODER  (left side)
# ══════════════════════════════════════════════════════════════════════
DEC_X = -600   # center of decoder area

box(-920, -2170, -280, -830, layer=3)
T("2-to-4 CMOS Decoder", -900, -2150, sx=0.45, sy=0.45, layer=4)
T("28 transistors  |  Static CMOS  |  < 40 nW", -900, -2110, sx=0.3, sy=0.3, layer=8)

# ── Input pins g1, g0 ───────────────────────────────────────────────
iopin("p_g1", -920, -2060, rot=0, mir=1, lab="g1")
iopin("p_g0", -920, -2020, rot=0, mir=1, lab="g0")
N(-920, -2060, -750, -2060, "g1")
N(-920, -2020, -500, -2020, "g0")

# ── Inverter 0: g0 → g0b ────────────────────────────────────────────
INV0_X = -500
INV0_Y_P = -1960   # PMOS
INV0_Y_N = -1880   # NMOS

T("INV0: g0 → g0b", INV0_X - 60, -2020 + 25, sx=0.22, sy=0.22, layer=8)
pmos("P_inv0", INV0_X, INV0_Y_P, 0.84, 0.15)
nmos("N_inv0", INV0_X, INV0_Y_N, 0.42, 0.15)
# Gate connections
N(INV0_X - 20, INV0_Y_P, INV0_X - 40, INV0_Y_P, "g0")
N(INV0_X - 40, INV0_Y_P, INV0_X - 40, INV0_Y_N, "g0")
N(INV0_X - 20, INV0_Y_N, INV0_X - 40, INV0_Y_N, "g0")
# Connect to g0 input wire
N(INV0_X - 40, -2020, INV0_X - 40, INV0_Y_P, "g0")
# VDD/VSS
N(INV0_X + 20, INV0_Y_P - 30, INV0_X + 20, VDD_Y, "VDD")
N(INV0_X + 20, INV0_Y_N + 30, INV0_X + 20, VSS_Y, "VSS")
# Drain-drain = output g0b
N(INV0_X + 20, INV0_Y_P + 30, INV0_X + 20, INV0_Y_N - 30, "g0b")
labpin("l_g0b", INV0_X + 50, -1920, rot=0, mir=0, lab="g0b")
N(INV0_X + 20, -1920, INV0_X + 50, -1920, "g0b")
# Bulk connections
T("0.84/0.15", INV0_X + 30, INV0_Y_P - 10, sx=0.2, sy=0.2, layer=8)
T("0.42/0.15", INV0_X + 30, INV0_Y_N - 10, sx=0.2, sy=0.2, layer=8)

# ── Inverter 1: g1 → g1b ────────────────────────────────────────────
INV1_X = -750
INV1_Y_P = -1960
INV1_Y_N = -1880

T("INV1: g1 → g1b", INV1_X - 60, -2060 + 25, sx=0.22, sy=0.22, layer=8)
pmos("P_inv1", INV1_X, INV1_Y_P, 0.84, 0.15)
nmos("N_inv1", INV1_X, INV1_Y_N, 0.42, 0.15)
N(INV1_X - 20, INV1_Y_P, INV1_X - 40, INV1_Y_P, "g1")
N(INV1_X - 40, INV1_Y_P, INV1_X - 40, INV1_Y_N, "g1")
N(INV1_X - 20, INV1_Y_N, INV1_X - 40, INV1_Y_N, "g1")
N(INV1_X - 40, -2060, INV1_X - 40, INV1_Y_P, "g1")
N(INV1_X + 20, INV1_Y_P - 30, INV1_X + 20, VDD_Y, "VDD")
N(INV1_X + 20, INV1_Y_N + 30, INV1_X + 20, VSS_Y, "VSS")
N(INV1_X + 20, INV1_Y_P + 30, INV1_X + 20, INV1_Y_N - 30, "g1b")
labpin("l_g1b", INV1_X + 50, -1920, rot=0, mir=0, lab="g1b")
N(INV1_X + 20, -1920, INV1_X + 50, -1920, "g1b")
T("0.84/0.15", INV1_X + 30, INV1_Y_P - 10, sx=0.2, sy=0.2, layer=8)
T("0.42/0.15", INV1_X + 30, INV1_Y_N - 10, sx=0.2, sy=0.2, layer=8)

# ── NAND2 + Output INV gates (x4) ───────────────────────────────────
# Each NAND2: 2 PMOS parallel + 2 NMOS stacked → inverted through output INV
# Arranged in a 2x2 grid for compactness

NAND_LABELS = [
    ("nand0", "g1b", "g0b", "sel0", "1x"),
    ("nand1", "g1b", "g0",  "sel1", "4x"),
    ("nand2", "g1",  "g0b", "sel2", "16x"),
    ("nand3", "g1",  "g0",  "sel3", "64x"),
]

NAND_X_START = -900
NAND_Y_START = -1780
NAND_DY = 200  # vertical spacing between NAND rows

for i, (nname, inA, inB, sel, gain) in enumerate(NAND_LABELS):
    nx = NAND_X_START + 30
    ny = NAND_Y_START + i * NAND_DY

    # Compact NAND representation as labeled box
    solidbox(nx, ny, nx + 120, ny + 60, layer=7)
    T(f"NAND2", nx + 10, ny + 8, sx=0.25, sy=0.25, layer=8)
    T(f"({inA},{inB})", nx + 10, ny + 30, sx=0.2, sy=0.2, layer=8)

    # Input labels
    labpin(f"l_{nname}_a", nx - 20, ny + 15, rot=0, mir=1, lab=inA)
    labpin(f"l_{nname}_b", nx - 20, ny + 40, rot=0, mir=1, lab=inB)
    N(nx - 20, ny + 15, nx, ny + 15, inA)
    N(nx - 20, ny + 40, nx, ny + 40, inB)

    # Output inverter box
    oinv_x = nx + 160
    solidbox(oinv_x, ny + 5, oinv_x + 60, ny + 55, layer=7)
    T("INV", oinv_x + 10, ny + 15, sx=0.22, sy=0.22, layer=8)

    # Wire NAND out → INV in
    N(nx + 120, ny + 30, oinv_x, ny + 30, f"{nname}_out")

    # INV output = sel line
    N(oinv_x + 60, ny + 30, oinv_x + 120, ny + 30, sel)
    labpin(f"l_{sel}", oinv_x + 120, ny + 30, rot=0, mir=0, lab=sel)
    T(f"→ {sel} ({gain})", oinv_x + 65, ny + 18, sx=0.22, sy=0.22, layer=4)

    # NAND transistor detail (tiny annotation)
    T(f"P: 0.84/0.15  N: 0.84/0.15", nx + 10, ny + 48, sx=0.15, sy=0.15, layer=8)

# Output inverter sizing annotation
T("Output INVs: P 0.84/0.15, N 0.42/0.15", NAND_X_START + 30, NAND_Y_START + 4 * NAND_DY + 15,
  sx=0.22, sy=0.22, layer=8)

# NOTE: Transistor-level NAND/INV detail is in pga_real.spice.
# The .sch shows the architectural block diagram with real inverters for g0/g1
# and symbolic NAND+INV boxes for the decoder outputs.


# ══════════════════════════════════════════════════════════════════════
#  SECTION 2: SWITCHED INPUT CAPACITOR NETWORK (center)
# ══════════════════════════════════════════════════════════════════════
CAP_X = 0       # left edge of cap symbols
SW_X = 250      # switch transistor x
INN_X = 400     # virtual ground bus x

box(-120, -2170, 570, -830, layer=3)
T("Switched Capacitor Network", -100, -2150, sx=0.45, sy=0.45, layer=4)

# Input pin
iopin("p_vin", -120, -1500, rot=0, mir=1, lab="vin")
N(-120, -1500, -60, -1500, "vin")
# Vertical vin bus
N(-60, -2060, -60, -900, "vin")

# Virtual ground bus (inn) — vertical line
N(INN_X, -2060, INN_X, -900, "inn")
labpin("l_inn", INN_X + 30, -1500, rot=0, mir=0, lab="inn")
T("inn (virtual ground)", INN_X + 40, -1510, sx=0.22, sy=0.22, layer=8)

# 4 gain paths, evenly spaced
CAP_DATA = [
    ("Cin1", 22.4, 22.4, "S1", 0.42, "sel0", "mid1", "1x: 1 pF",  -2050),
    ("Cin2", 44.7, 44.7, "S2", 0.42, "sel1", "mid2", "4x: 4 pF",  -1750),
    ("Cin3", 89.4, 89.4, "S3", 1,    "sel2", "mid3", "16x: 16 pF", -1450),
    ("Cin4", 178.9, 178.9, "S4", 5,   "sel3", "mid4", "64x: 64 pF", -1150),
]

for cname, cw, cl, sname, sw, sellab, midlab, label, cy in CAP_DATA:
    # MIM capacitor: vin → mid
    mim(cname, CAP_X, cy, cw, cl)
    # Wire from vin bus to cap top
    N(-60, cy - 30, CAP_X, cy - 30, "vin")
    # Wire from cap bottom to mid node
    N(CAP_X, cy + 32, CAP_X + 40, cy + 32, midlab)

    # Mid node label
    labpin(f"l_{midlab}", CAP_X + 40, cy + 32, rot=0, mir=0, lab=midlab)

    # NMOS switch: mid → inn, gate = sel
    nmos(sname, SW_X, cy + 32, sw, 0.15)
    # Switch drain = mid
    N(CAP_X + 40, cy + 32, SW_X - 20, cy + 32, midlab)
    # Switch source = inn bus
    N(SW_X + 20, cy + 62, INN_X, cy + 62, "inn")
    N(INN_X, cy + 62, INN_X, cy + 32, "inn")
    # Switch gate = sel (label)
    labpin(f"l_{sellab}_sw", SW_X - 40, cy + 32, rot=0, mir=1, lab=sellab)
    N(SW_X - 40, cy + 32, SW_X - 20, cy + 32, sellab)
    # Switch bulk = VSS
    N(SW_X + 20, cy + 2, SW_X + 20, cy - 20, "VSS")

    # Annotations
    T(label, CAP_X - 80, cy - 50, sx=0.25, sy=0.25, layer=4)
    sw_txt = f"W={sw}/L=0.15" if isinstance(sw, (int, float)) else f"W={sw}/L=0.15"
    T(sw_txt, SW_X + 30, cy + 20, sx=0.18, sy=0.18, layer=8)

# ── Mid-node pseudo-resistors (annotation only — transistors in pga_real.spice)
T("Mid-node pseudo-R (×4 pairs)", -100, -870, sx=0.25, sy=0.25, layer=4)
T("Back-to-back PMOS W=0.42/L=10, bulk=VDD", -100, -850, sx=0.2, sy=0.2, layer=8)
T("~100 GΩ from each mid node to Vcm", -100, -835, sx=0.2, sy=0.2, layer=8)
T("8 transistors total", -100, -820, sx=0.2, sy=0.2, layer=8)


# ══════════════════════════════════════════════════════════════════════
#  SECTION 3: OTA + FEEDBACK NETWORK  (right side)
# ══════════════════════════════════════════════════════════════════════
OTA_X = 750     # OTA triangle center
OTA_Y = -1500   # OTA center y

box(580, -2170, 1200, -830, layer=3)
T("OTA + Feedback Network", 600, -2150, sx=0.45, sy=0.45, layer=4)

# ── OTA triangle symbol ─────────────────────────────────────────────
triangle(OTA_X, OTA_Y, size=80, layer=7)
T("OTA", OTA_X - 30, OTA_Y - 12, sx=0.35, sy=0.35, layer=8)
T("ota_pga_v2", OTA_X - 45, OTA_Y + 12, sx=0.22, sy=0.22, layer=8)
T("2-stage Miller", OTA_X - 100, OTA_Y + 90, sx=0.22, sy=0.22, layer=8)
T("UGB = 422 kHz", OTA_X - 100, OTA_Y + 110, sx=0.22, sy=0.22, layer=8)
T("Av = 60 dB", OTA_X - 100, OTA_Y + 130, sx=0.22, sy=0.22, layer=8)
T("7 MOSFETs", OTA_X - 100, OTA_Y + 150, sx=0.22, sy=0.22, layer=8)

# OTA input pins:  (−) = inn, (+) = vcm
# (−) on top input of triangle
OTA_INP_Y = OTA_Y - 40   # inverting input (inn)
OTA_INN_Y = OTA_Y + 40   # non-inverting input (vcm)
OTA_OUT_X = OTA_X + 80    # output

T("−", OTA_X - 70, OTA_INP_Y - 12, sx=0.4, sy=0.4, layer=4)
T("+", OTA_X - 70, OTA_INN_Y - 12, sx=0.4, sy=0.4, layer=4)

# inn → OTA (−)
N(INN_X, -1500, 620, -1500, "inn")
N(620, -1500, 620, OTA_INP_Y, "inn")
N(620, OTA_INP_Y, OTA_X - 80, OTA_INP_Y, "inn")

# vcm → OTA (+)
iopin("p_vcm", 600, OTA_INN_Y, rot=0, mir=1, lab="vcm")
N(600, OTA_INN_Y, OTA_X - 80, OTA_INN_Y, "vcm")

# OTA output → vout
VOUT_X = 1100
N(OTA_OUT_X, OTA_Y, VOUT_X, OTA_Y, "vout")
iopin("p_vout", VOUT_X, OTA_Y, rot=0, mir=0, lab="vout")
labpin("l_vout", VOUT_X - 10, OTA_Y - 30, rot=0, mir=0, lab="vout")

# OTA supply connections
N(OTA_X, OTA_Y - 80, OTA_X, VDD_Y, "VDD")
N(OTA_X, OTA_Y + 80, OTA_X, VSS_Y, "VSS")

# ── Feedback capacitor Cf ────────────────────────────────────────────
CF_X = 850
CF_Y = -1800

mim("Cf", CF_X, CF_Y, 22.4, 22.4)
T("Cf = 1 pF", CF_X - 60, CF_Y - 55, sx=0.28, sy=0.28, layer=4)
T("22.4 × 22.4 MIM", CF_X - 60, CF_Y - 35, sx=0.2, sy=0.2, layer=8)

# Cf top → inn (wire up from inn bus to cap)
N(620, OTA_INP_Y, 620, CF_Y - 30, "inn")
N(620, CF_Y - 30, CF_X, CF_Y - 30, "inn")

# Cf bottom → vout (wire to output node)
N(CF_X, CF_Y + 32, CF_X, OTA_Y, "vout")

# ── Feedback pseudo-resistor (parallel to Cf) ───────────────────────
FPR_X = 1000
FPR_Y_A = -1870
FPR_Y_B = -1740

pmos("Mpr1", FPR_X, FPR_Y_A, 0.42, 10)
pmos("Mpr2", FPR_X, FPR_Y_B, 0.42, 10)

T("Feedback pseudo-R", FPR_X - 70, FPR_Y_A - 55, sx=0.25, sy=0.25, layer=4)
T("Back-to-back PMOS", FPR_X - 70, FPR_Y_A - 35, sx=0.2, sy=0.2, layer=8)
T("W=0.42/L=10, bulk=VDD", FPR_X - 70, FPR_Y_A - 20, sx=0.2, sy=0.2, layer=8)

# Mpr1 top (drain) → inn node
N(FPR_X + 20, FPR_Y_A - 30, FPR_X + 20, CF_Y - 60, "inn")
N(FPR_X + 20, CF_Y - 60, 660, CF_Y - 60, "inn")
N(660, CF_Y - 60, 660, CF_Y - 30, "inn")
# Mpr1 gate = inn (diode-connected)
N(FPR_X - 20, FPR_Y_A, FPR_X - 40, FPR_Y_A, "inn")
N(FPR_X - 40, FPR_Y_A, FPR_X - 40, CF_Y - 60, "inn")
# Mpr1 source → Mpr2 drain (internal node)
N(FPR_X + 20, FPR_Y_A + 30, FPR_X + 20, FPR_Y_B - 30, "")
# Mpr2 source (bottom) → vout
N(FPR_X + 20, FPR_Y_B + 30, FPR_X + 20, OTA_Y, "vout")
N(FPR_X + 20, OTA_Y, VOUT_X, OTA_Y, "vout")
# Mpr2 gate = vout (diode-connected)
N(FPR_X - 20, FPR_Y_B, FPR_X - 40, FPR_Y_B, "vout")
N(FPR_X - 40, FPR_Y_B, FPR_X - 40, OTA_Y, "vout")

# ── Load capacitor (external) ───────────────────────────────────────
T("CL = 10 pF", VOUT_X - 30, OTA_Y + 40, sx=0.25, sy=0.25, layer=8)
T("(external load)", VOUT_X - 30, OTA_Y + 60, sx=0.2, sy=0.2, layer=8)

# ── OTA bias pins ────────────────────────────────────────────────────
BIAS_X = 620
BIAS_Y = -900
iopin("p_vbn",  BIAS_X, BIAS_Y,      rot=0, mir=1, lab="vbn")
iopin("p_vbcn", BIAS_X, BIAS_Y + 30, rot=0, mir=1, lab="vbcn")
iopin("p_vbp",  BIAS_X, BIAS_Y + 60, rot=0, mir=1, lab="vbp")
iopin("p_vbcp", BIAS_X, BIAS_Y + 90, rot=0, mir=1, lab="vbcp")
T("OTA bias:", BIAS_X + 30, BIAS_Y - 20, sx=0.22, sy=0.22, layer=4)
T("vbn = 0.65 V", BIAS_X + 30, BIAS_Y,       sx=0.2, sy=0.2, layer=8)
T("vbcn = 0.88 V", BIAS_X + 30, BIAS_Y + 30, sx=0.2, sy=0.2, layer=8)
T("vbp = 0.73 V", BIAS_X + 30, BIAS_Y + 60,  sx=0.2, sy=0.2, layer=8)
T("vbcp = 0.475 V", BIAS_X + 30, BIAS_Y + 90, sx=0.2, sy=0.2, layer=8)


# ══════════════════════════════════════════════════════════════════════
#  WRITE .sch FILE
# ══════════════════════════════════════════════════════════════════════
sch_path = "pga.sch"
with open(sch_path, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f"Written: {sch_path}  ({len(lines)} lines)")

# ══════════════════════════════════════════════════════════════════════
#  RENDER TO SVG AND PNG
# ══════════════════════════════════════════════════════════════════════
# Use xschem in batch mode to export SVG
svg_path = "pga.svg"
png_path = "pga.png"

# Try xschem SVG export via xvfb-run (needs a display)
try:
    result = subprocess.run(
        ["xvfb-run", "-a", "xschem", "--svg", "--quit", sch_path],
        capture_output=True, text=True, timeout=30)
    if os.path.exists(svg_path):
        print(f"SVG exported: {svg_path}")
    else:
        print(f"xschem output: {result.stdout[:300]}")
        print(f"xschem stderr: {result.stderr[:300]}")
        raise RuntimeError("xschem did not produce SVG")
except Exception as e:
    print(f"xschem SVG export failed: {e}")
    print("Generating SVG manually...")

    # ── Manual SVG — professional schematic rendering ──────────────
    W, H = 1600, 1000  # canvas size
    s = []  # SVG lines
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" style="background:#0d1117">')
    s.append('''<style>
  text { font-family: "Cascadia Code", "JetBrains Mono", "Fira Code", monospace; }
  .wire { stroke: #58a6ff; stroke-width: 1.5; fill: none; }
  .wireh { stroke: #58a6ff; stroke-width: 2; fill: none; }
  .comp { stroke: #7ee787; stroke-width: 1.8; fill: none; }
  .box  { stroke: #484f58; stroke-width: 1; fill: none; stroke-dasharray: 8,4; }
  .sbox { stroke: #7ee787; stroke-width: 1.5; fill: rgba(126,231,135,0.06); }
  .title { fill: #f0f6fc; }
  .sub  { fill: #8b949e; }
  .lbl  { fill: #7ee787; }
  .note { fill: #e3b341; }
  .pin  { fill: #ff7b72; font-weight: bold; }
  .dim  { fill: #6e7681; }
</style>''')

    # ── Title ──
    s.append(f'<text x="30" y="32" class="title" font-size="20" font-weight="bold">'
             f'VibroSense Block 02 — Programmable Gain Amplifier (PGA)</text>')
    s.append(f'<text x="30" y="52" class="sub" font-size="12">'
             f'Capacitive-Feedback  |  4-Gain (1x / 4x / 16x / 64x)  |  SKY130A  |  49 Transistors</text>')
    s.append(f'<text x="30" y="70" class="note" font-size="11">'
             f'Gain err &lt;0.15 dB  |  BW = 27 kHz @ 16x  |  THD = 0.19%  |  P = 9.94 \u00b5W</text>')

    # ── Supply rails ──
    RAIL_Y1, RAIL_Y2 = 90, 950
    s.append(f'<line x1="20" y1="{RAIL_Y1}" x2="{W-20}" y2="{RAIL_Y1}" class="wireh"/>')
    s.append(f'<line x1="20" y1="{RAIL_Y2}" x2="{W-20}" y2="{RAIL_Y2}" class="wireh"/>')
    s.append(f'<text x="25" y="{RAIL_Y1-4}" class="lbl" font-size="11">VDD = 1.8 V</text>')
    s.append(f'<text x="25" y="{RAIL_Y2+14}" class="lbl" font-size="11">VSS = 0 V</text>')

    # ── Section boxes ──
    # Decoder: x 20..420, Caps: 440..960, OTA: 980..1580
    DEC = (25, 105, 415, 935)
    CAP = (435, 105, 955, 935)
    OTA_BOX = (975, 105, 1575, 935)
    for bx1, by1, bx2, by2 in [DEC, CAP, OTA_BOX]:
        s.append(f'<rect x="{bx1}" y="{by1}" width="{bx2-bx1}" height="{by2-by1}" class="box"/>')

    s.append(f'<text x="35" y="125" class="lbl" font-size="14" font-weight="bold">2-to-4 CMOS Decoder</text>')
    s.append(f'<text x="35" y="142" class="dim" font-size="10">28 transistors | Static CMOS | &lt;40 nW</text>')
    s.append(f'<text x="445" y="125" class="lbl" font-size="14" font-weight="bold">Switched Capacitor Network</text>')
    s.append(f'<text x="985" y="125" class="lbl" font-size="14" font-weight="bold">OTA + Feedback</text>')

    # ── Decoder ──
    # g1, g0 input pins
    s.append(f'<text x="32" y="175" class="pin" font-size="13">g1</text>')
    s.append(f'<text x="32" y="205" class="pin" font-size="13">g0</text>')
    s.append(f'<line x1="55" y1="170" x2="100" y2="170" class="wire"/>')
    s.append(f'<line x1="55" y1="200" x2="100" y2="200" class="wire"/>')

    # Inverters
    for i, (pin, out, px) in enumerate([("g1", "g1b", 110), ("g0", "g0b", 250)]):
        s.append(f'<rect x="{px}" y="155" width="80" height="55" class="sbox" rx="4"/>')
        s.append(f'<text x="{px+8}" y="175" class="note" font-size="11">INV</text>')
        s.append(f'<text x="{px+8}" y="195" class="dim" font-size="9">{pin} \u2192 {out}</text>')
        # output wire
        s.append(f'<line x1="{px+80}" y1="182" x2="{px+105}" y2="182" class="wire"/>')
        s.append(f'<text x="{px+82}" y="175" class="lbl" font-size="9">{out}</text>')
    # Wire g1 to INV1
    s.append(f'<line x1="100" y1="170" x2="100" y2="182" class="wire"/>')
    s.append(f'<line x1="100" y1="182" x2="110" y2="182" class="wire"/>')
    # Wire g0 to INV2
    s.append(f'<line x1="100" y1="200" x2="240" y2="200" class="wire"/>')
    s.append(f'<line x1="240" y1="200" x2="240" y2="182" class="wire"/>')
    s.append(f'<line x1="240" y1="182" x2="250" y2="182" class="wire"/>')

    # NAND2 + INV gates (4 rows)
    nand_data = [
        ("g1b", "g0b", "sel0", "1x",  260),
        ("g1b", "g0",  "sel1", "4x",  410),
        ("g1",  "g0b", "sel2", "16x", 560),
        ("g1",  "g0",  "sel3", "64x", 710),
    ]
    for inA, inB, sel, gain, ny in nand_data:
        # NAND box
        s.append(f'<rect x="55" y="{ny}" width="115" height="50" class="sbox" rx="4"/>')
        s.append(f'<text x="63" y="{ny+20}" class="note" font-size="11">NAND2</text>')
        s.append(f'<text x="63" y="{ny+38}" class="dim" font-size="9">({inA}, {inB})</text>')
        # INV box
        s.append(f'<rect x="200" y="{ny+5}" width="55" height="40" class="sbox" rx="4"/>')
        s.append(f'<text x="210" y="{ny+30}" class="note" font-size="11">INV</text>')
        # Wires
        s.append(f'<line x1="170" y1="{ny+25}" x2="200" y2="{ny+25}" class="wire"/>')
        s.append(f'<line x1="255" y1="{ny+25}" x2="400" y2="{ny+25}" class="wire"/>')
        # sel label
        s.append(f'<text x="270" y="{ny+20}" class="lbl" font-size="12" font-weight="bold">{sel}</text>')
        s.append(f'<text x="310" y="{ny+20}" class="dim" font-size="10">({gain})</text>')
        # Input labels
        s.append(f'<text x="35" y="{ny+18}" class="dim" font-size="8">{inA}</text>')
        s.append(f'<text x="35" y="{ny+38}" class="dim" font-size="8">{inB}</text>')

    # Decoder detail note
    s.append(f'<text x="40" y="870" class="dim" font-size="9">'
             f'NAND: P 0.84/0.15, N 0.84/0.15</text>')
    s.append(f'<text x="40" y="885" class="dim" font-size="9">'
             f'Out INV: P 0.84/0.15, N 0.42/0.15</text>')
    s.append(f'<text x="40" y="900" class="dim" font-size="9">'
             f'Transistor-level: pga_real.spice</text>')

    # ── Switched Cap Network ──
    # vin input pin
    s.append(f'<text x="448" y="175" class="pin" font-size="13">vin</text>')
    VIN_X = 500
    s.append(f'<line x1="{VIN_X}" y1="170" x2="{VIN_X}" y2="860" class="wire"/>')  # vin bus

    INN_BUS = 870  # inn vertical bus x
    s.append(f'<line x1="{INN_BUS}" y1="170" x2="{INN_BUS}" y2="860" class="wire"/>')
    s.append(f'<text x="{INN_BUS+5}" y="530" class="note" font-size="10" '
             f'transform="rotate(-90,{INN_BUS+5},530)">inn (virtual ground)</text>')

    # 4 cap+switch channels
    cap_rows = [
        ("Cin1", "1 pF",  "22.4\u00d722.4", "XS1", "W=0.42", "sel0", "mid1", 210),
        ("Cin2", "4 pF",  "44.7\u00d744.7", "XS2", "W=0.42", "sel1", "mid2", 380),
        ("Cin3", "16 pF", "89.4\u00d789.4", "XS3", "W=1",    "sel2", "mid3", 550),
        ("Cin4", "64 pF", "178.9\u00d7178.9","XS4", "W=5",   "sel3", "mid4", 720),
    ]
    for cname, cval, cdim, sname, sw, sellab, midlab, cy in cap_rows:
        # Horizontal wire from vin bus
        s.append(f'<line x1="{VIN_X}" y1="{cy}" x2="580" y2="{cy}" class="wire"/>')
        # Cap symbol (two parallel plates)
        s.append(f'<line x1="580" y1="{cy-12}" x2="580" y2="{cy+12}" class="comp" stroke-width="2.5"/>')
        s.append(f'<line x1="590" y1="{cy-12}" x2="590" y2="{cy+12}" class="comp" stroke-width="2.5"/>')
        # Cap label
        s.append(f'<text x="555" y="{cy-18}" class="lbl" font-size="11">{cname}</text>')
        s.append(f'<text x="555" y="{cy+30}" class="dim" font-size="8">{cval} ({cdim})</text>')
        # Wire from cap to mid node
        s.append(f'<line x1="590" y1="{cy}" x2="660" y2="{cy}" class="wire"/>')
        # Mid node dot
        s.append(f'<circle cx="660" cy="{cy}" r="3" fill="#58a6ff"/>')
        s.append(f'<text x="650" y="{cy-8}" class="dim" font-size="8">{midlab}</text>')
        # NMOS switch symbol
        s.append(f'<rect x="680" y="{cy-15}" width="50" height="30" class="sbox" rx="3"/>')
        s.append(f'<text x="688" y="{cy+5}" class="note" font-size="10">{sname}</text>')
        s.append(f'<text x="685" y="{cy+22}" class="dim" font-size="7">{sw}/L=0.15</text>')
        # Gate label
        s.append(f'<text x="690" y="{cy-20}" class="lbl" font-size="8">{sellab}</text>')
        # Wire from switch to inn bus
        s.append(f'<line x1="730" y1="{cy}" x2="{INN_BUS}" y2="{cy}" class="wire"/>')
        # sel wire from decoder (dashed to show connection)
        s.append(f'<line x1="400" y1="{cy}" x2="440" y2="{cy}" class="wire" '
                 f'stroke-dasharray="4,3" stroke="#7ee787" stroke-width="1"/>')

    # Mid-node pseudo-R annotation
    s.append(f'<text x="450" y="870" class="dim" font-size="9">'
             f'Mid-node pseudo-R: 4\u00d7 back-to-back PMOS 0.42/10</text>')
    s.append(f'<text x="450" y="885" class="dim" font-size="9">'
             f'~100 G\u2126 to Vcm  |  bulk=VDD  |  8 transistors</text>')

    # ── OTA + Feedback ──
    # OTA triangle
    OTA_CX, OTA_CY = 1250, 530
    TS = 80  # triangle half-size
    s.append(f'<polygon points="{OTA_CX-TS},{OTA_CY-TS} {OTA_CX-TS},{OTA_CY+TS} '
             f'{OTA_CX+TS},{OTA_CY}" class="comp" fill="rgba(126,231,135,0.04)"/>')
    s.append(f'<text x="{OTA_CX-35}" y="{OTA_CY+6}" class="note" font-size="16" font-weight="bold">OTA</text>')
    s.append(f'<text x="{OTA_CX-TS+10}" y="{OTA_CY-30}" class="lbl" font-size="16">\u2212</text>')
    s.append(f'<text x="{OTA_CX-TS+10}" y="{OTA_CY+40}" class="lbl" font-size="16">+</text>')

    # OTA detail
    s.append(f'<text x="{OTA_CX-70}" y="{OTA_CY+TS+25}" class="note" font-size="10">ota_pga_v2</text>')
    s.append(f'<text x="{OTA_CX-70}" y="{OTA_CY+TS+42}" class="dim" font-size="9">'
             f'2-stage Miller compensated</text>')
    s.append(f'<text x="{OTA_CX-70}" y="{OTA_CY+TS+57}" class="dim" font-size="9">'
             f'UGB = 422 kHz  |  Av = 60 dB</text>')
    s.append(f'<text x="{OTA_CX-70}" y="{OTA_CY+TS+72}" class="dim" font-size="9">'
             f'7 MOSFETs (subcircuit)</text>')

    # inn → OTA (−)
    INN_OTA_Y = OTA_CY - 40
    s.append(f'<line x1="{INN_BUS}" y1="500" x2="990" y2="500" class="wire"/>')
    s.append(f'<line x1="990" y1="500" x2="990" y2="{INN_OTA_Y}" class="wire"/>')
    s.append(f'<line x1="990" y1="{INN_OTA_Y}" x2="{OTA_CX-TS}" y2="{INN_OTA_Y}" class="wire"/>')

    # vcm → OTA (+)
    VCM_OTA_Y = OTA_CY + 40
    s.append(f'<text x="990" y="{VCM_OTA_Y+4}" class="pin" font-size="11">vcm</text>')
    s.append(f'<line x1="1030" y1="{VCM_OTA_Y}" x2="{OTA_CX-TS}" y2="{VCM_OTA_Y}" class="wire"/>')

    # OTA → vout
    VOUT_X_SVG = 1530
    s.append(f'<line x1="{OTA_CX+TS}" y1="{OTA_CY}" x2="{VOUT_X_SVG}" y2="{OTA_CY}" class="wire"/>')
    s.append(f'<text x="{VOUT_X_SVG-30}" y="{OTA_CY-10}" class="pin" font-size="13">vout</text>')
    # vout dot
    s.append(f'<circle cx="{VOUT_X_SVG-50}" cy="{OTA_CY}" r="3" fill="#58a6ff"/>')

    # VDD/VSS connections
    s.append(f'<line x1="{OTA_CX}" y1="{OTA_CY-TS}" x2="{OTA_CX}" y2="{RAIL_Y1}" class="wire" '
             f'stroke-dasharray="4,3"/>')
    s.append(f'<line x1="{OTA_CX}" y1="{OTA_CY+TS}" x2="{OTA_CX}" y2="{RAIL_Y2}" class="wire" '
             f'stroke-dasharray="4,3"/>')

    # ── Feedback cap Cf ──
    CF_X_SVG = 1100
    CF_TOP_Y = 250
    CF_BOT_Y = OTA_CY
    # Cf from inn to vout (above the OTA)
    # Top wire from inn node up
    s.append(f'<line x1="990" y1="{INN_OTA_Y}" x2="990" y2="{CF_TOP_Y}" class="wire"/>')
    s.append(f'<line x1="990" y1="{CF_TOP_Y}" x2="{CF_X_SVG-5}" y2="{CF_TOP_Y}" class="wire"/>')
    # Cap symbol
    s.append(f'<line x1="{CF_X_SVG-5}" y1="{CF_TOP_Y-12}" x2="{CF_X_SVG-5}" y2="{CF_TOP_Y+12}" '
             f'class="comp" stroke-width="2.5"/>')
    s.append(f'<line x1="{CF_X_SVG+5}" y1="{CF_TOP_Y-12}" x2="{CF_X_SVG+5}" y2="{CF_TOP_Y+12}" '
             f'class="comp" stroke-width="2.5"/>')
    s.append(f'<text x="{CF_X_SVG-20}" y="{CF_TOP_Y-18}" class="lbl" font-size="12" font-weight="bold">'
             f'Cf = 1 pF</text>')
    s.append(f'<text x="{CF_X_SVG-20}" y="{CF_TOP_Y+30}" class="dim" font-size="8">22.4\u00d722.4 MIM</text>')
    # Right wire from Cf to vout
    s.append(f'<line x1="{CF_X_SVG+5}" y1="{CF_TOP_Y}" x2="{VOUT_X_SVG-50}" y2="{CF_TOP_Y}" class="wire"/>')
    s.append(f'<line x1="{VOUT_X_SVG-50}" y1="{CF_TOP_Y}" x2="{VOUT_X_SVG-50}" y2="{OTA_CY}" class="wire"/>')

    # ── Feedback pseudo-R (in parallel with Cf) ──
    PR_X_SVG = 1250
    s.append(f'<rect x="{PR_X_SVG-30}" y="{CF_TOP_Y-15}" width="70" height="30" class="sbox" rx="4"/>')
    s.append(f'<text x="{PR_X_SVG-22}" y="{CF_TOP_Y+5}" class="note" font-size="10">Pseudo-R</text>')
    s.append(f'<text x="{PR_X_SVG-15}" y="{CF_TOP_Y+25}" class="dim" font-size="8">'
             f'PMOS 0.42/10 \u00d72</text>')

    # CL annotation
    s.append(f'<text x="{VOUT_X_SVG-55}" y="{OTA_CY+30}" class="dim" font-size="9">'
             f'CL = 10 pF (ext)</text>')

    # ── Bias pins ──
    s.append(f'<text x="990" y="820" class="lbl" font-size="10">OTA bias:</text>')
    for j, (bn, bv) in enumerate([("vbn","0.65V"),("vbcn","0.88V"),("vbp","0.73V"),("vbcp","0.475V")]):
        s.append(f'<text x="990" y="{838+j*16}" class="pin" font-size="9">{bn}</text>')
        s.append(f'<text x="1045" y="{838+j*16}" class="dim" font-size="9">= {bv}</text>')

    # ── Gain formula ──
    s.append(f'<text x="990" y="185" class="note" font-size="11">'
             f'Gain = Cin(sel) / Cf</text>')
    s.append(f'<text x="990" y="205" class="dim" font-size="9">'
             f'1x: 1/1  |  4x: 4/1  |  16x: 16/1  |  64x: 64/1</text>')

    s.append('</svg>')

    with open(svg_path, 'w') as f:
        f.write('\n'.join(s))
    print(f"Written: {svg_path}")

# Convert SVG to PNG
if os.path.exists(svg_path):
    try:
        subprocess.run(
            ["rsvg-convert", "-w", "1600", "-h", "1200",
             "-o", png_path, svg_path],
            check=True, capture_output=True, timeout=15)
        print(f"Converted: {png_path}")
    except Exception as e:
        print(f"PNG conversion failed: {e}")

print("\nDone.")
