#!/usr/bin/env python3
"""Generate xschem schematics for Block 03 filter bank — v2 clean layout."""

import os

PDK = "/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr"
PFET = f"{PDK}/pfet_01v8.sym"
NFET = f"{PDK}/nfet_01v8.sym"
DEV = "/usr/share/xschem/xschem_library/devices"


def header():
    return "v {xschem version=3.4.4 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n"


# ─── OTA symbol ─────────────────────────────────────────────────────

def gen_ota_sym():
    return """v {xschem version=3.4.4 file_version=1.2}
G {}
K {type=subcircuit
format="@spiceprefix@name @pinlist @symname"
template="name=X1"
}
V {}
S {}
E {}
L 7 -80 -60 80 60 {}
L 7 -80 60 80 60 {}
L 7 80 60 80 -60 {}
L 7 80 -60 -80 -60 {}
L 7 -80 -60 -80 60 {}
L 4 -100 -30 -80 -30 {}
L 4 -100 30 -80 30 {}
L 4 80 0 100 0 {}
L 4 0 -60 0 -80 {}
L 4 0 60 0 80 {}
L 4 -40 60 -40 80 {}
L 4 40 60 40 80 {}
L 4 -40 -60 -40 -80 {}
L 4 40 -60 40 -80 {}
T {+} -70 -40 0 0 0.3 0.3 {layer=4}
T {-} -70 20 0 0 0.3 0.3 {layer=4}
T {OTA} -25 -12 0 0 0.35 0.35 {layer=8}
T {@name} -25 65 0 0 0.25 0.25 {layer=15}
B 5 -100 -35 -80 -25 {name=vinp dir=in}
B 5 -100 25 -80 35 {name=vinn dir=in}
B 5 80 -5 100 5 {name=vout dir=out}
B 5 -5 -80 5 -60 {name=vdd dir=inout}
B 5 -5 60 5 80 {name=vss dir=inout}
B 5 -45 60 -35 80 {name=vbn dir=in}
B 5 35 60 45 80 {name=vbcn dir=in}
B 5 -45 -80 -35 -60 {name=vbp dir=in}
B 5 35 -80 45 -60 {name=vbcp dir=in}
"""


def gen_pr_sym():
    return """v {xschem version=3.4.4 file_version=1.2}
G {}
K {type=subcircuit
format="@spiceprefix@name @pinlist @symname"
template="name=X1"
}
V {}
S {}
E {}
L 7 -30 -15 30 -15 {}
L 7 -30 15 30 15 {}
L 7 30 15 30 -15 {}
L 7 -30 -15 -30 15 {}
L 4 -50 0 -30 0 {}
L 4 30 0 50 0 {}
T {PR} -15 -8 0 0 0.25 0.25 {layer=8}
T {@name} -15 20 0 0 0.2 0.2 {layer=15}
B 5 -50 -5 -30 5 {name=a dir=inout}
B 5 30 -5 50 5 {name=b dir=inout}
"""


# ─── Helpers ─────────────────────────────────────────────────────────

def T(s, x, y, sz=0.4, layer=15):
    return f'T {{{s}}} {x} {y} 0 0 {sz} {sz} {{layer={layer}}}'

def N(x1, y1, x2, y2, lab=""):
    return f'N {x1} {y1} {x2} {y2} {{lab={lab}}}'

def iopin(name, x, y, rot="0 0"):
    return f'C {{{DEV}/iopin.sym}} {x} {y} {rot} {{name=p_{name} lab={name}}}'

def labpin(name, x, y, rot="0 0"):
    return f'C {{{DEV}/lab_pin.sym}} {x} {y} {rot} {{name=l_{name} lab={name}}}'

def ota_inst(name, cx, cy, mirror=False):
    """Place OTA; return (component_line, pin_dict)."""
    o = "0 1" if mirror else "0 0"
    comp = f'C {{ota_foldcasc.sym}} {cx} {cy} {o} {{name={name} model=ota_foldcasc spiceprefix=X}}'
    if mirror:
        pins = {
            'inp': (cx+100, cy-30), 'inn': (cx+100, cy+30), 'out': (cx-100, cy),
            'vdd': (cx, cy-80), 'vss': (cx, cy+80),
            'vbn': (cx+40, cy+80), 'vbcn': (cx-40, cy+80),
            'vbp': (cx+40, cy-80), 'vbcp': (cx-40, cy-80),
        }
    else:
        pins = {
            'inp': (cx-100, cy-30), 'inn': (cx-100, cy+30), 'out': (cx+100, cy),
            'vdd': (cx, cy-80), 'vss': (cx, cy+80),
            'vbn': (cx-40, cy+80), 'vbcn': (cx+40, cy+80),
            'vbp': (cx-40, cy-80), 'vbcp': (cx+40, cy-80),
        }
    return comp, pins

def pr_inst(name, cx, cy, rot=0):
    """Place pseudo-resistor rotated 90 deg (vertical). Pins: a=top, b=bottom."""
    comp = f'C {{pseudo_res.sym}} {cx} {cy} 1 0 {{name={name} model=pseudo_res spiceprefix=X}}'
    return comp, {'a': (cx, cy-50), 'b': (cx, cy+50)}

def cap_inst(name, cx, cy, val="10p"):
    comp = f'C {{{DEV}/capa.sym}} {cx} {cy} 0 0 {{name={name} m=1 value={val} footprint=1206 device="ceramic capacitor"}}'
    return comp, {'p': (cx, cy-20), 'n': (cx, cy+20)}

def nfet_inst(name, cx, cy, w="2u", l="4u", mirror=False):
    o = "0 1" if mirror else "0 0"
    comp = f'C {{{NFET}}} {cx} {cy} {o} {{name={name}\nW={w}\nL={l}\nnf=1\nmult=1\nmodel=nfet_01v8\nspiceprefix=X\n}}'
    if mirror:
        return comp, {'g': (cx+20, cy), 'd': (cx-20, cy-30), 's': (cx-20, cy+30), 'b': (cx-20, cy)}
    return comp, {'g': (cx-20, cy), 'd': (cx+20, cy-30), 's': (cx+20, cy+30), 'b': (cx+20, cy)}


# ─── Bias pin labels for each OTA (avoids drawing long wires) ───────

def ota_bias_labels(pins):
    """Return lab_pin lines for vdd/vss/vbn/vbcn/vbp/vbcp."""
    lines = []
    lines.append(labpin("vdd", pins['vdd'][0], pins['vdd'][1], "1 0"))
    lines.append(labpin("vss", pins['vss'][0], pins['vss'][1], "3 0"))
    lines.append(labpin("vbn", pins['vbn'][0], pins['vbn'][1], "3 0"))
    lines.append(labpin("vbcn", pins['vbcn'][0], pins['vbcn'][1], "3 0"))
    lines.append(labpin("vbp", pins['vbp'][0], pins['vbp'][1], "1 0"))
    lines.append(labpin("vbcp", pins['vbcp'][0], pins['vbcp'][1], "1 0"))
    return lines


# ─── One half-path of the BPF (reusable for pos and neg) ────────────

def bpf_path(suffix, vin_name, bp_out_name, cx_start, cy,
             c1_val, c2_val, vin_x, bp_out_x):
    """
    Generate one path of pseudo-diff BPF.
    suffix: 'p' or 'n'
    cy: center y for OTA row
    Returns list of .sch lines.
    """
    L = []

    # OTA spacing
    ota1_cx = cx_start
    ota2_cx = cx_start + 500
    ota3_cx = cx_start + 250  # between OTA1 and OTA2, below

    # int1 node x (between OTA1 out and OTA2 in)
    int1_x = cx_start + 250
    int2_x = cx_start + 700

    int1_name = f"int1{suffix}"
    int2_name = f"int2{suffix}"

    # ── OTA1: vin(+), int2(-) → int1 ──
    c1, p1 = ota_inst(f"Xota1{suffix}", ota1_cx, cy)
    L.append(c1)
    L += ota_bias_labels(p1)
    L.append(T(f"OTA1{suffix}", ota1_cx-30, cy+90, 0.25, 8))

    # vin → OTA1(+)
    L.append(N(vin_x, p1['inp'][1], p1['inp'][0], p1['inp'][1], vin_name))

    # OTA1 out → int1 node
    L.append(N(p1['out'][0], p1['out'][1], int1_x, cy, int1_name))

    # int2 → OTA1(-) (feedback from right)
    # Route: int2_x at cy-100 (above), then left to OTA1(-)
    L.append(N(int2_x, cy, int2_x, cy-100, int2_name))
    L.append(N(int2_x, cy-100, p1['inn'][0]-40, cy-100, int2_name))
    L.append(N(p1['inn'][0]-40, cy-100, p1['inn'][0]-40, p1['inn'][1], int2_name))
    L.append(N(p1['inn'][0]-40, p1['inn'][1], p1['inn'][0], p1['inn'][1], int2_name))

    # ── OTA2: int1(+), vcm(-) → int2 ──
    c2, p2 = ota_inst(f"Xota2{suffix}", ota2_cx, cy)
    L.append(c2)
    L += ota_bias_labels(p2)
    L.append(T(f"OTA2{suffix}", ota2_cx-30, cy+90, 0.25, 8))

    # int1 → OTA2(+)
    L.append(N(int1_x, cy, int1_x, p2['inp'][1], int1_name))
    L.append(N(int1_x, p2['inp'][1], p2['inp'][0], p2['inp'][1], int1_name))

    # vcm → OTA2(-)
    L.append(labpin("vcm", p2['inn'][0], p2['inn'][1], "0 1"))

    # OTA2 out → int2 node
    L.append(N(p2['out'][0], p2['out'][1], int2_x, cy, int2_name))

    # ── OTA3: vcm(+), int1(-) → int1 (damping, output tied to - input) ──
    ota3_cy = cy + 220
    c3, p3 = ota_inst(f"Xota3{suffix}", ota3_cx, ota3_cy)
    L.append(c3)
    L += ota_bias_labels(p3)
    L.append(T(f"OTA3{suffix}", ota3_cx-30, ota3_cy+90, 0.25, 8))
    L.append(T("(damping)", ota3_cx-30, ota3_cy+110, 0.2, 5))

    # vcm → OTA3(+)
    L.append(labpin("vcm", p3['inp'][0], p3['inp'][1], "0 1"))

    # int1 → OTA3(-)
    L.append(N(int1_x, cy, int1_x, p3['inn'][1], int1_name))
    L.append(N(int1_x, p3['inn'][1], p3['inn'][0], p3['inn'][1], int1_name))

    # OTA3 out → int1 (self-connect)
    L.append(N(p3['out'][0], p3['out'][1], int1_x+150, ota3_cy, int1_name))
    L.append(N(int1_x+150, ota3_cy, int1_x+150, cy, int1_name))

    # ── C1: int1 to vss ──
    c1_cy = cy + 220
    c1_cx = int1_x - 80
    cc1, pc1 = cap_inst(f"C1{suffix}", c1_cx, c1_cy, c1_val)
    L.append(cc1)
    L.append(T(f"C1{suffix}", c1_cx+15, c1_cy-10, 0.22, 8))
    L.append(T(c1_val, c1_cx+15, c1_cy+8, 0.18, 8))
    L.append(N(c1_cx, cy, c1_cx, pc1['p'][1], int1_name))
    L.append(labpin("vss", c1_cx, pc1['n'][1], "3 0"))

    # ── C2: int2 to vss ──
    c2_cx = int2_x
    cc2, pc2 = cap_inst(f"C2{suffix}", c2_cx, c1_cy, c2_val)
    L.append(cc2)
    L.append(T(f"C2{suffix}", c2_cx+15, c1_cy-10, 0.22, 8))
    L.append(T(c2_val, c2_cx+15, c1_cy+8, 0.18, 8))
    L.append(N(c2_cx, cy, c2_cx, pc2['p'][1], int2_name))
    L.append(labpin("vss", c2_cx, pc2['n'][1], "3 0"))

    # ── PR1: int1 to vcm ──
    pr1_cx = int1_x - 150
    pr1_cy = cy + 140
    cp1, pp1 = pr_inst(f"Xpr1{suffix}", pr1_cx, pr1_cy)
    L.append(cp1)
    L.append(N(pr1_cx, cy, pr1_cx, pp1['a'][1], int1_name))
    L.append(labpin("vcm", pr1_cx, pp1['b'][1], "3 0"))

    # ── PR2: int2 to vcm ──
    pr2_cx = int2_x + 80
    cp2, pp2 = pr_inst(f"Xpr2{suffix}", pr2_cx, pr1_cy)
    L.append(cp2)
    L.append(N(pr2_cx, cy, pr2_cx, pp2['a'][1], int2_name))
    L.append(labpin("vcm", pr2_cx, pp2['b'][1], "3 0"))

    # ── BP output tap from int1 ──
    L.append(N(int1_x, cy, int1_x, cy-50, int1_name))
    L.append(N(int1_x, cy-50, bp_out_x, cy-50, bp_out_name))

    # Node labels
    L.append(labpin(int1_name, int1_x+10, cy-15, "0 0"))
    L.append(labpin(int2_name, int2_x+10, cy-15, "0 0"))

    return L


# ─── Page 1: BPF Pseudo-Differential Channel ────────────────────────

def gen_bpf_channel():
    L = [header()]

    # Title
    L.append(T("VibroSense Block 03: Pseudo-Differential BPF Channel", -200, -1200, 0.65, 15))
    L.append(T("Tow-Thomas Biquad  --  Ch2: f0=1000 Hz, Q=0.67, C1=118 pF, C2=260 pF", -200, -1150, 0.3, 15))
    L.append(T("6x ota_foldcasc + 4 Caps + 4 Pseudo-Resistors  |  Iref = 200 nA  |  Power = 4.7 uW", -200, -1115, 0.25, 8))

    # Section labels
    L.append(T("POSITIVE PATH", -150, -1060, 0.35, 4))
    L.append(T("NEGATIVE PATH", -150, -500, 0.35, 4))

    # IO pins
    L.append(iopin("vinp", -350, -1000, "0 1"))
    L.append(iopin("vinn", -350, -440, "0 1"))
    L.append(iopin("bp_outp", 1000, -1050, "0 0"))
    L.append(iopin("bp_outn", 1000, -490, "0 0"))

    # Positive path: OTAs at y=-1000
    L += bpf_path("p", "vinp", "bp_outp",
                   cx_start=0, cy=-1000,
                   c1_val="118p", c2_val="260p",
                   vin_x=-350, bp_out_x=1000)

    # Negative path: OTAs at y=-440
    L += bpf_path("n", "vinn", "bp_outn",
                   cx_start=0, cy=-440,
                   c1_val="118p", c2_val="260p",
                   vin_x=-350, bp_out_x=1000)

    # Differential output annotation
    L.append(T("Vout_diff = bp_outp - bp_outn", 800, -1080, 0.22, 4))
    L.append(T("(HD2 cancelled by pseudo-diff topology)", 800, -1060, 0.18, 5))

    # Notes
    L.append(T("Shared bias: VBN, VBCN, VBP, VBCP from ota_bias_dist", -150, -130, 0.22, 4))
    L.append(T("PR = back-to-back PMOS W=0.42u L=10u (>100 GOhm DC bias)", -150, -105, 0.18, 5))

    return '\n'.join(L) + '\n'


# ─── Page 2: 4-Bit Bias DAC ─────────────────────────────────────────

def gen_bias_dac():
    L = [header()]

    L.append(T("VibroSense Block 03: 4-Bit Binary-Weighted Cascode Current Mirror DAC", -300, -1200, 0.55, 15))
    L.append(T("SKY130A  |  Iout = Iunit x (8*b3 + 4*b2 + 2*b1 + b0)  |  DNL = 0.0006 LSB", -300, -1150, 0.3, 8))

    # Supply rails
    L.append(N(-300, -1100, 1300, -1100, "vdd"))
    L.append(N(-300, -200, 1300, -200, "vss"))
    L.append(iopin("vdd", -300, -1100, "0 1"))
    L.append(iopin("vss", -300, -200, "0 1"))
    L.append(iopin("iref", -200, -1100, "3 0"))
    L.append(iopin("iout", 1300, -580, "0 0"))

    # Section headers
    L.append(T("REF", -150, -1050, 0.35, 4))
    L.append(T("BIT 0 (1x)", 100, -1050, 0.35, 4))
    L.append(T("BIT 1 (2x)", 370, -1050, 0.35, 4))
    L.append(T("BIT 2 (4x)", 650, -1050, 0.35, 4))
    L.append(T("BIT 3 (8x)", 950, -1050, 0.35, 4))

    # Iref input
    L.append(N(-200, -1100, -100, -1100, "iref"))
    L.append(N(-100, -1100, -100, -950, "iref"))

    # Reference cascode (diode-connected)
    cr, pr_ = nfet_inst("XMref_cas", -120, -900, w="2u", l="4u")
    L.append(cr)
    L.append(T("Mcas_ref", -190, -920, 0.22, 8))
    L.append(T("2/4", -190, -900, 0.18, 8))
    # Diode: gate to drain
    L.append(N(pr_['d'][0], pr_['d'][1], pr_['d'][0], -950, "iref"))
    L.append(N(pr_['g'][0], pr_['g'][1], pr_['g'][0]-40, pr_['g'][1], "gate_c"))
    L.append(N(pr_['g'][0]-40, pr_['g'][1], pr_['g'][0]-40, -930, "gate_c"))
    L.append(N(pr_['g'][0]-40, -930, pr_['d'][0], -930, "gate_c"))

    # Reference mirror (diode-connected)
    cr2, pr2_ = nfet_inst("XMref_bot", -120, -700, w="2u", l="4u")
    L.append(cr2)
    L.append(T("Mmir_ref", -190, -720, 0.22, 8))
    L.append(T("2/4", -190, -700, 0.18, 8))
    L.append(N(pr_['s'][0], pr_['s'][1], pr2_['d'][0], pr2_['d'][1], "mid_ref"))
    L.append(N(pr2_['g'][0], pr2_['g'][1], pr2_['g'][0]-40, pr2_['g'][1], "gate_n"))
    L.append(N(pr2_['g'][0]-40, pr2_['g'][1], pr2_['g'][0]-40, -730, "gate_n"))
    L.append(N(pr2_['g'][0]-40, -730, pr2_['d'][0], -730, "gate_n"))
    L.append(N(pr2_['s'][0], pr2_['s'][1], pr2_['s'][0], -200, "vss"))

    # Gate bus labels
    L.append(labpin("gate_c", -200, -900, "0 1"))
    L.append(labpin("gate_n", -200, -700, "0 1"))

    # Gate bus wires across all cells
    L.append(N(-160, -900, 1100, -900, "gate_c"))
    L.append(N(-160, -700, 1100, -700, "gate_n"))

    # Bit cells
    bit_x = [180, 450, 730, 1030]
    bit_units = [1, 2, 4, 8]
    bit_names = ["b0", "b1", "b2", "b3"]

    for i, (bx, units, bname) in enumerate(zip(bit_x, bit_units, bit_names)):
        # Cascode transistor
        cc, pc = nfet_inst(f"XM{i}_cas", bx-20, -900, w="2u", l="4u")
        L.append(cc)
        L.append(T(f"{units}x", bx+5, -925, 0.2, 5))
        # Gate → gate_c bus (already connected via horizontal wire)

        # Mirror transistor
        cm, pm = nfet_inst(f"XM{i}_bot", bx-20, -700, w="2u", l="4u")
        L.append(cm)
        # Gate → gate_n bus (already connected via horizontal wire)
        L.append(N(pm['s'][0], pm['s'][1], pm['s'][0], -200, "vss"))
        # Cascode source → mirror drain
        L.append(N(pc['s'][0], pc['s'][1], pm['d'][0], pm['d'][1], f"mid{i}"))

        # Switch transistor
        cs, ps = nfet_inst(f"XM{i}_sw", bx-20, -500, w="1u", l="0.15u")
        L.append(cs)
        L.append(T(f"sw", bx+5, -520, 0.18, 5))
        L.append(T("1/0.15", bx+5, -498, 0.16, 8))

        # Cascode drain → switch source (above switch)
        L.append(N(pc['d'][0], pc['d'][1], pc['d'][0], -560, f"sw{i}d"))
        L.append(N(ps['s'][0], ps['s'][1], ps['s'][0], -560, f"sw{i}d"))
        # Wait, nfet drain is at (cx+20, cy-30), source at (cx+20, cy+30)
        # switch drain = ps['d'] is at top, connects to iout
        # switch source = ps['s'] is at bottom... no:
        # For the switch: drain goes to iout (up/left), source goes to cascode drain
        # Actually in the SPICE: XM0_sw iout b0 sw0d vss
        # This means: drain=iout, gate=b0, source=sw0d, body=vss
        # So switch source connects to cascode drain, switch drain to iout

        # switch drain → iout bus
        L.append(N(ps['d'][0], ps['d'][1], ps['d'][0], -400, "iout"))

        # switch gate → digital control
        L.append(N(ps['g'][0], ps['g'][1], ps['g'][0]-30, ps['g'][1], bname))
        L.append(labpin(bname, ps['g'][0]-30, ps['g'][1], "0 1"))

    # Iout bus
    L.append(N(bit_x[0], -400, 1300, -400, "iout"))
    L.append(N(1300, -400, 1300, -580, "iout"))

    # Note
    L.append(T("100G bleed resistors on each switch node (not shown)", 100, -260, 0.2, 5))

    return '\n'.join(L) + '\n'


# ─── Page 3: Filter Bank Top-Level ──────────────────────────────────

def gen_filter_bank_top():
    L = [header()]

    L.append(T("VibroSense Block 03: 5-Channel Filter Bank -- Top Level", -400, -1550, 0.65, 15))
    L.append(T("5x Bias DAC + Bias Distribution + Pseudo-Differential BPF -- SKY130A", -400, -1500, 0.3, 15))
    L.append(T("Total Power: 42.5 uW  |  VDD = 1.8 V  |  20-bit digital control (4 per channel)", -400, -1465, 0.25, 8))

    # IO pins on left
    L.append(iopin("vinp", -500, -750, "0 1"))
    L.append(iopin("vinn", -500, -700, "0 1"))
    L.append(iopin("vcm", -500, -650, "0 1"))
    L.append(iopin("iref", -500, -600, "0 1"))
    L.append(iopin("vdd", -500, -1400, "0 1"))
    L.append(iopin("vss", -500, -100, "0 1"))

    # Input bus lines
    L.append(N(-500, -750, -200, -750, "vinp"))
    L.append(N(-500, -700, -200, -700, "vinn"))
    L.append(N(-500, -650, -200, -650, "vcm"))
    L.append(N(-500, -600, -200, -600, "iref"))

    # Vertical bus from input to channels
    L.append(N(-200, -1350, -200, -200, ""))

    # Supply rails
    L.append(N(-500, -1400, 1500, -1400, "vdd"))
    L.append(N(-500, -100, 1500, -100, "vss"))

    channels = [
        ("Ch1", "f0=224 Hz, Q=0.75", "4.7 uW"),
        ("Ch2", "f0=1000 Hz, Q=0.67", "4.7 uW"),
        ("Ch3", "f0=3162 Hz, Q=1.05", "4.7 uW"),
        ("Ch4", "f0=7071 Hz, Q=1.41", "10.3 uW"),
        ("Ch5", "f0=14142 Hz, Q=1.41", "18.2 uW"),
    ]

    for i, (name, specs, pwr) in enumerate(channels):
        y = -1300 + i * 240
        box_l, box_r = -100, 1200
        box_t, box_b = y, y + 190

        # Box outline
        L.append(N(box_l, box_t, box_r, box_t, ""))
        L.append(N(box_l, box_b, box_r, box_b, ""))
        L.append(N(box_l, box_t, box_l, box_b, ""))
        L.append(N(box_r, box_t, box_r, box_b, ""))

        # Dividers
        L.append(N(250, box_t, 250, box_b, ""))
        L.append(N(550, box_t, 550, box_b, ""))

        # Channel label
        L.append(T(name, -80, y+15, 0.35, 4))
        L.append(T(specs, -80, y+45, 0.2, 8))
        L.append(T(pwr, -80, y+65, 0.2, 5))

        # Sub-block labels
        L.append(T("4-bit DAC", 50, y+90, 0.28, 4))
        L.append(T("Bias Dist", 330, y+90, 0.28, 4))
        L.append(T("Pseudo-Diff BPF", 700, y+90, 0.28, 4))
        L.append(T("6 OTAs + 4C + 4PR", 680, y+120, 0.18, 5))

        # Input connections from bus
        mid_y = y + 95
        L.append(N(-200, mid_y-20, box_l, mid_y-20, "vinp"))
        L.append(N(-200, mid_y+20, box_l, mid_y+20, "vinn"))

        # Iref
        L.append(N(-200, mid_y+50, box_l, mid_y+50, "iref"))

        # Digital control (bottom of box)
        for b in range(4):
            bx = 20 + b * 55
            L.append(labpin(f"ch{i+1}_b{b}", bx, box_b+10, "3 0"))

        # Differential outputs
        outp = f"ch{i+1}_outp"
        outn = f"ch{i+1}_outn"
        L.append(N(box_r, mid_y-20, 1500, mid_y-20, outp))
        L.append(N(box_r, mid_y+20, 1500, mid_y+20, outn))
        L.append(iopin(outp, 1500, mid_y-20, "0 0"))
        L.append(iopin(outn, 1500, mid_y+20, "0 0"))

    return '\n'.join(L) + '\n'


# ─── Main ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    d = "/home/ubuntu/analog-ai-chips/vibrosense/03_filters"

    for fname, content in [
        ("ota_foldcasc.sym", gen_ota_sym()),
        ("pseudo_res.sym", gen_pr_sym()),
        ("bpf_pseudo_diff.sch", gen_bpf_channel()),
        ("bias_dac_real.sch", gen_bias_dac()),
        ("filter_bank_top.sch", gen_filter_bank_top()),
    ]:
        with open(os.path.join(d, fname), 'w') as f:
            f.write(content)
        print(f"  {fname}")

    print("Done.")
