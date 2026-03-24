#!/usr/bin/env python3
"""Generate xschem schematic for VibroSense Block 04: Envelope Detector.

Circuit: dual ota_pga_v2 precision half-wave rectifier + 5T Gm-C LPF
Source netlist: envelope_det.spice (DO NOT MODIFY — schematic must match exactly)

Generates:
  - ota_pga_v2.sym   (OTA subcircuit symbol for hierarchical use)
  - envelope_det.sch  (full schematic)
"""

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PDK = "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A"
NFET_SYM = f"{PDK}/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym"
PFET_SYM = f"{PDK}/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym"
OTA_SYM  = os.path.abspath("ota_pga_v2.sym")

# ──────────────────────────────────────────────────────────
# Pin offset math (rot=0)
# NFET: D=(+20,-30) G=(-20,0) S=(+20,+30) B=(+20,0)
# PFET: D=(+20,+30) G=(-20,0) S=(+20,-30) B=(+20,0)
# flip=1 → negate x offsets
# ──────────────────────────────────────────────────────────

def nfet_pins(cx, cy, flip=0):
    s = -1 if flip else 1
    return {'D': (cx+s*20, cy-30), 'G': (cx-s*20, cy),
            'S': (cx+s*20, cy+30), 'B': (cx+s*20, cy)}

def pfet_pins(cx, cy, flip=0):
    s = -1 if flip else 1
    return {'D': (cx+s*20, cy+30), 'G': (cx-s*20, cy),
            'S': (cx+s*20, cy-30), 'B': (cx+s*20, cy)}


# ──────────────────────────────────────────────────────────
# STEP 1: Generate ota_pga_v2.sym
# ──────────────────────────────────────────────────────────

def gen_ota_sym():
    """Create a rectangular OTA symbol with 9 pins matching ota_pga_v2 subcircuit.
    Pin order: vdd gnd inp inn out vbn vbcn vbp vbcp
    """
    sym = r"""v {xschem version=3.4.4 file_version=1.2}
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
B 5 -100 -35 -80 -25 {name=inp dir=in}
B 5 -100 25 -80 35 {name=inn dir=in}
B 5 80 -5 100 5 {name=out dir=out}
B 5 -5 -80 5 -60 {name=vdd dir=inout}
B 5 -5 60 5 80 {name=gnd dir=inout}
B 5 -45 60 -35 80 {name=vbn dir=in}
B 5 35 60 45 80 {name=vbcn dir=in}
B 5 -45 -80 -35 -60 {name=vbp dir=in}
B 5 35 -80 45 -60 {name=vbcp dir=in}
"""
    with open("ota_pga_v2.sym", "w") as f:
        f.write(sym)
    print(f"Generated ota_pga_v2.sym ({len(sym)} bytes)")


# ──────────────────────────────────────────────────────────
# STEP 2: Generate envelope_det.sch
# ──────────────────────────────────────────────────────────

HEADER = """v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}"""

texts = []
components = []
wires = []
_pc = [0]

def _n():
    _pc[0] += 1
    return _pc[0]

def T(text, x, y, sz_h=0.4, sz_v=0.4, layer=8):
    texts.append(f'T {{{text}}} {x} {y} 0 0 {sz_h} {sz_v} {{layer={layer}}}')

def C(sym, cx, cy, rot, flip, attrs):
    components.append(f'C {{{sym}}} {cx} {cy} {rot} {flip} {{{attrs}}}')

def N(x1, y1, x2, y2, lab):
    wires.append(f'N {x1} {y1} {x2} {y2} {{lab={lab}}}')

def lab(x, y, rot, flip, name):
    n = _n()
    components.append(f'C {{devices/lab_pin.sym}} {x} {y} {rot} {flip} {{name=l{n} lab={name}}}')

def iopin(x, y, rot, flip, name):
    n = _n()
    components.append(f'C {{devices/iopin.sym}} {x} {y} {rot} {flip} {{name=p{n} lab={name}}}')

def build_sch():
    # ════════════════════════════════════════════════════════
    # LAYOUT COORDINATES
    # ════════════════════════════════════════════════════════
    #
    #  VDD rail:  y = -1800
    #  GND rail:  y =  100
    #
    #  LEFT: Rectifier (x: -900 .. 250)
    #    OTA1 center: (-550, -1150)
    #    OTA2 center: (-550, -850)
    #    Mph1 PMOS:   (-200, -1550)
    #    Mph2 PMOS:   ( 100, -1550)
    #    Msink NMOS:  (-50,  -450)
    #
    #  RIGHT: LPF (x: 450 .. 1200)
    #    Mp3 PMOS:    (550, -1550) diode
    #    Mp4 PMOS:    (800, -1550) mirror
    #    M1 NFET:     (550, -1050) G=rect
    #    M2 NFET:     (800, -1050) G=vout (follower)
    #    Mtail NFET:  (675, -650)
    #    Clpf:        (1050,-900)

    # ── Title ──
    T("VibroSense Block 04: Envelope Detector", -900, -2050, 0.7, 0.7, 15)
    T("Dual ota_pga_v2 Precision Half-Wave Rectifier + 5T Gm-C LPF  —  SKY130A",
      -900, -1980, 0.35, 0.35, 15)
    T("Power: 21 uW  |  VDD = 1.8 V  |  LPF fc ~ 9 Hz", -900, -1940, 0.3, 0.3, 8)

    # ── Section labels ──
    T("PRECISION RECTIFIER", -700, -1870, 0.4, 0.4, 4)
    T("(dual OTA feedback)", -680, -1840, 0.25, 0.25, 8)
    T("Gm-C LOW-PASS FILTER", 520, -1870, 0.4, 0.4, 4)
    T("(5T OTA follower + 50nF)", 520, -1840, 0.25, 0.25, 8)

    # ── Section divider ──
    T("|", 350, -1500, 0.3, 0.3, 8)
    T("|", 350, -1300, 0.3, 0.3, 8)
    T("|", 350, -1100, 0.3, 0.3, 8)
    T("|", 350, -900, 0.3, 0.3, 8)
    T("|", 350, -700, 0.3, 0.3, 8)
    T("|", 350, -500, 0.3, 0.3, 8)
    T("|", 350, -300, 0.3, 0.3, 8)

    # ── Device labels ──
    T("Mph1", -260, -1620, 0.3, 0.3, 8)
    T("PMOS 2/1", -270, -1595, 0.22, 0.22, 8)
    T("Mph2", 40, -1620, 0.3, 0.3, 8)
    T("PMOS 2/1", 30, -1595, 0.22, 0.22, 8)
    T("Msink", -110, -520, 0.3, 0.3, 8)
    T("NMOS 0.42/100", -140, -495, 0.22, 0.22, 8)
    T("(triode discharge)", -150, -470, 0.2, 0.2, 5)

    T("Mp3", 490, -1620, 0.3, 0.3, 8)
    T("PMOS 4/4", 480, -1595, 0.22, 0.22, 8)
    T("(diode)", 490, -1575, 0.2, 0.2, 5)
    T("Mp4", 740, -1620, 0.3, 0.3, 8)
    T("PMOS 4/4", 730, -1595, 0.22, 0.22, 8)
    T("(mirror)", 740, -1575, 0.2, 0.2, 5)
    T("M1", 490, -1120, 0.3, 0.3, 8)
    T("NMOS 2/4", 480, -1095, 0.22, 0.22, 8)
    T("M2", 740, -1120, 0.3, 0.3, 8)
    T("NMOS 2/4", 730, -1095, 0.22, 0.22, 8)
    T("(follower)", 730, -1075, 0.2, 0.2, 5)
    T("Mtail", 615, -720, 0.3, 0.3, 8)
    T("NMOS 1/8", 605, -695, 0.22, 0.22, 8)
    T("Clpf = 50 nF", 1010, -960, 0.3, 0.3, 8)

    # Net labels on key nodes
    T("rect", 200, -1300, 0.3, 0.3, 4)
    T("oa1", -120, -1250, 0.25, 0.25, 4)
    T("oa2", -120, -950, 0.25, 0.25, 4)
    T("d1", 580, -1370, 0.25, 0.25, 4)
    T("tail", 680, -870, 0.25, 0.25, 4)

    # ════════════════════════════════════════════════════════
    # SUPPLY RAILS
    # ════════════════════════════════════════════════════════
    N(-900, -1800, 1200, -1800, "vdd")
    N(-900, -200, 1200, -200, "gnd")

    # ════════════════════════════════════════════════════════
    # RECTIFIER SECTION
    # ════════════════════════════════════════════════════════

    # --- OTA1: positive-half follower ---
    # ota_pga_v2 pins: vdd gnd inp inn out vbn vbcn vbp vbcp
    # Instance: Xota1 vdd gnd vin rect oa1 vbn gnd vdd vdd
    # Symbol pins at offsets from center (-550, -1150):
    #   inp=(-100,-30), inn=(-100,+30), out=(+100,0)
    #   vdd=(0,-80), gnd=(0,+80), vbn=(-40,+80)
    #   vbcn=(+40,+80), vbp=(-40,-80), vbcp=(+40,-80)
    C(OTA_SYM, -550, -1150, 0, 0,
      "name=Xota1")
    # OTA1 wiring
    N(-650, -1180, -750, -1180, "vin")       # inp = vin
    lab(-750, -1180, 0, 1, "vin")
    N(-650, -1120, -750, -1120, "rect")      # inn = rect
    lab(-750, -1120, 0, 1, "rect")
    N(-450, -1150, -350, -1150, "oa1")       # out = oa1
    N(-550, -1230, -550, -1280, "vdd")       # vdd
    lab(-550, -1280, 1, 0, "vdd")
    N(-550, -1070, -550, -1020, "gnd")       # gnd
    lab(-550, -1020, 3, 0, "gnd")
    N(-590, -1070, -590, -1020, "vbn")       # vbn
    lab(-590, -1020, 3, 0, "vbn")
    N(-510, -1070, -510, -1020, "gnd")       # vbcn = gnd
    lab(-510, -1020, 3, 0, "gnd")
    N(-590, -1230, -590, -1280, "vdd")       # vbp = vdd
    lab(-590, -1280, 1, 0, "vdd")
    N(-510, -1230, -510, -1280, "vdd")       # vbcp = vdd
    lab(-510, -1280, 1, 0, "vdd")

    # --- OTA2: vcm clamp ---
    # Instance: Xota2 vdd gnd vcm rect oa2 vbn gnd vdd vdd
    C(OTA_SYM, -550, -850, 0, 0,
      "name=Xota2")
    N(-650, -880, -750, -880, "vcm")         # inp = vcm
    lab(-750, -880, 0, 1, "vcm")
    N(-650, -820, -750, -820, "rect")        # inn = rect
    lab(-750, -820, 0, 1, "rect")
    N(-450, -850, -350, -850, "oa2")         # out = oa2
    N(-550, -930, -550, -980, "vdd")         # vdd
    lab(-550, -980, 1, 0, "vdd")
    N(-550, -770, -550, -720, "gnd")         # gnd
    lab(-550, -720, 3, 0, "gnd")
    N(-590, -770, -590, -720, "vbn")         # vbn
    lab(-590, -720, 3, 0, "vbn")
    N(-510, -770, -510, -720, "gnd")         # vbcn = gnd
    lab(-510, -720, 3, 0, "gnd")
    N(-590, -930, -590, -980, "vdd")         # vbp = vdd
    lab(-590, -980, 1, 0, "vdd")
    N(-510, -930, -510, -980, "vdd")         # vbcp = vdd
    lab(-510, -980, 1, 0, "vdd")

    # --- Mph1 PMOS: rect oa1 vdd vdd ---
    # XMph1 rect oa1 vdd vdd sky130_fd_pr__pfet_01v8 w=2 l=1
    # PFET pin order in symbol: D G S B
    C(PFET_SYM, -200, -1550, 0, 0,
      "name=XMph1\nW=2\nL=1\nnf=1\nmult=1\nmodel=pfet_01v8\nspiceprefix=X")
    ph1 = pfet_pins(-200, -1550, 0)
    # S = vdd (top)
    N(ph1['S'][0], ph1['S'][1], ph1['S'][0], -1800, "vdd")
    # B = vdd
    N(ph1['B'][0], ph1['B'][1], ph1['B'][0]+20, ph1['B'][1], "vdd")
    lab(ph1['B'][0]+20, ph1['B'][1], 0, 0, "vdd")
    # G = oa1 (Manhattan route: OTA1 out → right → up → left to gate)
    # OTA1 out at (-350,-1150), Mph1 gate at (-220,-1550)
    N(-350, -1150, -350, -1550, "oa1")       # vertical up
    N(-350, -1550, ph1['G'][0], -1550, "oa1") # horizontal to gate
    # D = rect (bottom)
    N(ph1['D'][0], ph1['D'][1], ph1['D'][0], -1350, "rect")

    # --- Mph2 PMOS: rect oa2 vdd vdd ---
    C(PFET_SYM, 100, -1550, 0, 0,
      "name=XMph2\nW=2\nL=1\nnf=1\nmult=1\nmodel=pfet_01v8\nspiceprefix=X")
    ph2 = pfet_pins(100, -1550, 0)
    N(ph2['S'][0], ph2['S'][1], ph2['S'][0], -1800, "vdd")
    N(ph2['B'][0], ph2['B'][1], ph2['B'][0]+20, ph2['B'][1], "vdd")
    lab(ph2['B'][0]+20, ph2['B'][1], 0, 0, "vdd")
    # G = oa2 (Manhattan route at x=-250 to avoid oa1 at x=-350)
    # OTA2 out at (-350,-850), route up at x=-250, then right to Mph2 gate at (80,-1550)
    N(-350, -850, -250, -850, "oa2")         # horizontal right
    N(-250, -850, -250, -1550, "oa2")        # vertical up
    N(-250, -1550, ph2['G'][0], -1550, "oa2") # horizontal to gate
    # D = rect
    N(ph2['D'][0], ph2['D'][1], ph2['D'][0], -1350, "rect")

    # Connect the two Mph drain nodes (rect bus)
    N(ph1['D'][0], -1350, ph2['D'][0], -1350, "rect")

    # --- Msink NMOS: rect vdd vcm gnd ---
    # XMsink rect vdd vcm gnd sky130_fd_pr__nfet_01v8 w=0.42 l=100
    C(NFET_SYM, -50, -450, 0, 0,
      "name=XMsink\nW=0.42\nL=100\nnf=1\nmult=1\nmodel=nfet_01v8\nspiceprefix=X")
    ms = nfet_pins(-50, -450, 0)
    # D = rect (top)
    N(ms['D'][0], ms['D'][1], ms['D'][0], -1350, "rect")
    # G = vdd
    N(ms['G'][0], ms['G'][1], ms['G'][0]-40, ms['G'][1], "vdd")
    lab(ms['G'][0]-40, ms['G'][1], 0, 1, "vdd")
    # S = vcm (goes down to a vcm label, not to GND rail)
    N(ms['S'][0], ms['S'][1], ms['S'][0], ms['S'][1]+50, "vcm")
    lab(ms['S'][0], ms['S'][1]+50, 3, 0, "vcm")
    # B = gnd
    N(ms['B'][0], ms['B'][1], ms['B'][0]+20, ms['B'][1], "gnd")
    lab(ms['B'][0]+20, ms['B'][1], 0, 0, "gnd")

    # Route rect from rectifier to LPF
    N(ph2['D'][0], -1350, 450, -1350, "rect")
    # Down to M1 gate level
    N(450, -1350, 450, -1050, "rect")
    # Over to M1 gate
    N(450, -1050, 510, -1050, "rect")

    # ════════════════════════════════════════════════════════
    # LPF SECTION
    # ════════════════════════════════════════════════════════

    # --- Mp3 PMOS: d1 d1 vdd vdd (diode-connected) ---
    C(PFET_SYM, 550, -1550, 0, 0,
      "name=XMp3\nW=4\nL=4\nnf=1\nmult=1\nmodel=pfet_01v8\nspiceprefix=X")
    p3 = pfet_pins(550, -1550, 0)
    N(p3['S'][0], p3['S'][1], p3['S'][0], -1800, "vdd")
    N(p3['B'][0], p3['B'][1], p3['B'][0]+20, p3['B'][1], "vdd")
    lab(p3['B'][0]+20, p3['B'][1], 0, 0, "vdd")
    # D = d1
    N(p3['D'][0], p3['D'][1], p3['D'][0], -1400, "d1")
    # G = d1 (diode: connect gate to drain)
    N(p3['G'][0], p3['G'][1], p3['G'][0], -1400, "d1")
    N(p3['G'][0], -1400, p3['D'][0], -1400, "d1")

    # --- Mp4 PMOS: vout d1 vdd vdd ---
    C(PFET_SYM, 800, -1550, 0, 0,
      "name=XMp4\nW=4\nL=4\nnf=1\nmult=1\nmodel=pfet_01v8\nspiceprefix=X")
    p4 = pfet_pins(800, -1550, 0)
    N(p4['S'][0], p4['S'][1], p4['S'][0], -1800, "vdd")
    N(p4['B'][0], p4['B'][1], p4['B'][0]+20, p4['B'][1], "vdd")
    lab(p4['B'][0]+20, p4['B'][1], 0, 0, "vdd")
    # D = vout
    N(p4['D'][0], p4['D'][1], p4['D'][0], -1400, "vout")
    # G = d1 (mirror: connect to Mp3 gate/drain)
    N(p4['G'][0], p4['G'][1], p3['G'][0], p4['G'][1], "d1")
    N(p3['G'][0], p4['G'][1], p3['G'][0], -1400, "d1")

    # --- M1 NFET: d1 rect tail gnd ---
    # (rect is the LPF input = vin of lpf_10hz subcircuit)
    C(NFET_SYM, 550, -1050, 0, 0,
      "name=XM1\nW=2\nL=4\nnf=1\nmult=1\nmodel=nfet_01v8\nspiceprefix=X")
    m1 = nfet_pins(550, -1050, 0)
    # D = d1 (up to Mp3 drain)
    N(m1['D'][0], m1['D'][1], m1['D'][0], -1400, "d1")
    # G = rect (already connected via N above to 510, -1050)
    N(m1['G'][0], m1['G'][1], 510, -1050, "rect")
    # S = tail
    N(m1['S'][0], m1['S'][1], m1['S'][0], -950, "tail")
    # B = gnd
    N(m1['B'][0], m1['B'][1], m1['B'][0]+20, m1['B'][1], "gnd")
    lab(m1['B'][0]+20, m1['B'][1], 0, 0, "gnd")

    # --- M2 NFET: vout vout tail gnd (follower config) ---
    C(NFET_SYM, 800, -1050, 0, 0,
      "name=XM2\nW=2\nL=4\nnf=1\nmult=1\nmodel=nfet_01v8\nspiceprefix=X")
    m2 = nfet_pins(800, -1050, 0)
    # D = vout (up to Mp4 drain)
    N(m2['D'][0], m2['D'][1], m2['D'][0], -1400, "vout")
    # G = vout (follower: gate tied to drain)
    N(m2['G'][0], m2['G'][1], m2['G'][0], -1020, "vout")
    N(m2['G'][0], -1020, m2['D'][0], -1020, "vout")
    # S = tail
    N(m2['S'][0], m2['S'][1], m2['S'][0], -950, "tail")
    # B = gnd
    N(m2['B'][0], m2['B'][1], m2['B'][0]+20, m2['B'][1], "gnd")
    lab(m2['B'][0]+20, m2['B'][1], 0, 0, "gnd")

    # Connect M1 and M2 sources (tail bus)
    N(m1['S'][0], -950, m2['S'][0], -950, "tail")
    # Tail down to Mtail drain
    N(675, -950, 675, -680, "tail")

    # --- Mtail NFET: tail vbn_lpf gnd gnd ---
    C(NFET_SYM, 675, -650, 0, 0,
      "name=XMtail\nW=1\nL=8\nnf=1\nmult=1\nmodel=nfet_01v8\nspiceprefix=X")
    mt = nfet_pins(675, -650, 0)
    # D = tail (already connected above)
    # G = vbn_lpf
    N(mt['G'][0], mt['G'][1], mt['G'][0]-60, mt['G'][1], "vbn_lpf")
    lab(mt['G'][0]-60, mt['G'][1], 0, 1, "vbn_lpf")
    # S = gnd
    N(mt['S'][0], mt['S'][1], mt['S'][0], -200, "gnd")
    # B = gnd
    N(mt['B'][0], mt['B'][1], mt['B'][0]+20, mt['B'][1], "gnd")
    lab(mt['B'][0]+20, mt['B'][1], 0, 0, "gnd")

    # --- Clpf: 50nF from vout to gnd ---
    C("devices/capa.sym", 1050, -1100, 0, 0, "name=Clpf value=50n")
    # Cap top = vout
    N(1050, -1130, 1050, -1400, "vout")
    N(1050, -1400, p4['D'][0], -1400, "vout")
    # Cap bottom = gnd
    N(1050, -1070, 1050, -200, "gnd")

    # ════════════════════════════════════════════════════════
    # I/O PINS
    # ════════════════════════════════════════════════════════
    iopin(-900, -1180, 2, 0, "vin")
    N(-900, -1180, -750, -1180, "vin")

    iopin(-900, -880, 2, 0, "vcm")
    N(-900, -880, -750, -880, "vcm")

    iopin(1200, -1400, 0, 0, "vout")
    N(1050, -1400, 1200, -1400, "vout")

    iopin(-100, -1850, 3, 0, "vdd")
    N(-100, -1850, -100, -1800, "vdd")

    iopin(-100, -100, 1, 0, "gnd")
    N(-100, -100, -100, -200, "gnd")

    iopin(-900, -1020, 2, 0, "vbn")
    N(-900, -1020, -590, -1020, "vbn")

    iopin(555, -650, 2, 0, "vbn_lpf")

    # ════════════════════════════════════════════════════════
    # ASSEMBLE
    # ════════════════════════════════════════════════════════
    out = HEADER + "\n"
    for t in texts:
        out += t + "\n"
    for w in wires:
        out += w + "\n"
    for c in components:
        out += c + "\n"
    return out


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    gen_ota_sym()

    sch = build_sch()
    with open("envelope_det.sch", "w") as f:
        f.write(sch)
    print(f"Generated envelope_det.sch ({len(sch)} bytes, "
          f"{len(components)} components, {len(wires)} wires, {len(texts)} texts)")
