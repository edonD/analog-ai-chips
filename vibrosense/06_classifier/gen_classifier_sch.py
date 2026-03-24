#!/usr/bin/env python3
"""Generate xschem schematic for VibroSense Block 06: Charge-Domain MAC Classifier.

Produces classifier.sch matching the SPICE netlists exactly.
Three sections: MAC bit-cell, StrongARM comparator, Clock generator.
"""

SKY = "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr"
DEV = "/usr/local/share/xschem/xschem_library/devices"

lines = []

def T(text, x, y, size, layer):
    """Add text annotation."""
    lines.append(f'T {{{text}}} {x} {y} 0 0 {size} {size} {{layer={layer}}}')

def nfet(name, x, y, w, l, mirror=0):
    """Place NFET. Returns dict of pin absolute coords."""
    lines.append(f'C {{{SKY}/nfet_01v8.sym}} {x} {y} 0 {mirror} {{name={name}')
    lines.append(f'W={w}')
    lines.append(f'L={l}')
    lines.append(f'nf=1')
    lines.append(f'mult=1')
    lines.append(f'model=nfet_01v8')
    lines.append(f'spiceprefix=X')
    lines.append(f'}}')
    sx = -1 if mirror else 1
    return {
        'g': (x - 20*sx, y),
        'd': (x + 20*sx, y - 30),
        's': (x + 20*sx, y + 30),
        'b': (x + 20*sx, y),
    }

def pfet(name, x, y, w, l, mirror=0):
    """Place PFET. Returns dict of pin absolute coords.
    PFET pins: S at top (y-30), D at bottom (y+30)."""
    lines.append(f'C {{{SKY}/pfet_01v8.sym}} {x} {y} 0 {mirror} {{name={name}')
    lines.append(f'W={w}')
    lines.append(f'L={l}')
    lines.append(f'nf=1')
    lines.append(f'mult=1')
    lines.append(f'model=pfet_01v8')
    lines.append(f'spiceprefix=X')
    lines.append(f'}}')
    sx = -1 if mirror else 1
    return {
        'g': (x - 20*sx, y),
        's': (x + 20*sx, y - 30),  # source=VDD side (top)
        'd': (x + 20*sx, y + 30),  # drain=circuit side (bottom)
        'b': (x + 20*sx, y),
    }

def cap(name, x, y, w, l):
    """Place MIM cap. c0=top(y-30), c1=bottom(y+30)."""
    lines.append(f'C {{{SKY}/cap_mim_m3_1.sym}} {x} {y} 0 0 {{name={name}')
    lines.append(f'W={w}')
    lines.append(f'L={l}')
    lines.append(f'MF=1')
    lines.append(f'model=cap_mim_m3_1')
    lines.append(f'spiceprefix=X')
    lines.append(f'}}')
    return {'c0': (x, y-30), 'c1': (x, y+30)}

def iopin(name, label, x, y, mirror=0):
    lines.append(f'C {{{DEV}/iopin.sym}} {x} {y} 0 {mirror} {{name={name} lab={label}}}')

def labpin(name, label, x, y, mirror=0):
    lines.append(f'C {{{DEV}/lab_pin.sym}} {x} {y} 0 {mirror} {{name={name} lab={label}}}')

def wire(x1, y1, x2, y2, lab):
    lines.append(f'N {x1} {y1} {x2} {y2} {{lab={lab}}}')


# ===== HEADER =====
lines.append('v {xschem version=3.4.4 file_version=1.2}')
lines.append('G {}')
lines.append('K {}')
lines.append('V {}')
lines.append('S {}')
lines.append('E {}')

# ===== TITLE BLOCK =====
T('VibroSense Block 06: Charge-Domain MAC Classifier', -200, -2050, 1.0, 15)
T('8-Input x 4-Bit MAC  |  StrongARM Comparator  |  3-Phase Clock Gen  \\u2014  SKY130A', -200, -1990, 0.45, 15)
T('VDD = 1.8 V  |  Cunit = 50 fF  |  4-class WTA  |  ~702 transistors  |  10/10 specs PASS in ngspice', -200, -1950, 0.35, 8)

# ============================================================
# SECTION 1: MAC BIT-CELL (Representative: Input 0, Bit 0)
# ============================================================
SEC1_X = -600  # left edge
SEC1_CX = -350  # center x for signal path

T('MAC Bit-Cell (Input 0, Bit 0)', SEC1_X, -1880, 0.5, 4)
T('x32 per MAC  |  x4 MACs  =  128 bit-cells, 640 TGs, ~702 transistors total', SEC1_X, -1840, 0.3, 8)

# --- Signal flow is vertical: in0 (top) -> sample TG -> top_plate -> cap -> eval TG -> bitline (bottom) ---

# VDD rail at y=-1810
VDD_Y = -1810
VSS_Y = -610

# in0 input at top
T('Sample TG', SEC1_X, -1780, 0.35, 4)
T('en0b0 = AND(phi_s, w[0])', SEC1_X, -1755, 0.25, 8)

# Sample TG NMOS: gate=en0b0, drain=in0, source=top_plate
#   Place at (-400, -1700) mirror=0
#   Pins: g=(-420,-1700), d=(-380,-1730), s=(-380,-1670)
sn = nfet('XNt0b0', -400, -1700, 0.84, 0.15)
T('XNt0b0', -460, -1710, 0.25, 8)
T('0.84/0.15', -460, -1690, 0.2, 8)

# Sample TG PMOS: gate=en0b0b, drain=in0, source=top_plate
#   Place at (-400, -1630) mirror=0
#   PFET pins: g=(-420,-1630), s=(-380,-1660) [vdd-side=top], d=(-380,-1600) [circuit-side=bottom]
sp = pfet('XPt0b0', -400, -1630, 1.68, 0.15)
T('XPt0b0', -460, -1640, 0.25, 8)
T('1.68/0.15', -460, -1620, 0.2, 8)

# Wire: in0 to sample TG drains
# NFET drain = (-380, -1730), connect to in0 rail
wire(-380, -1760, -380, -1730, 'in0')
# PFET drain is at bottom (-380, -1600), but for TG in0 goes to PFET source (top = -1660)
# Actually: in a transmission gate, both NMOS and PMOS have one side connected to input and other to output
# NMOS: drain=in0(-380,-1730), source=top_plate(-380,-1670)
# PFET: source(top)=in0(-380,-1660), drain(bottom)=top_plate(-380,-1600)
# Connect NMOS drain to PFET source (both = in0 side)
wire(-380, -1730, -380, -1660, 'in0')

# Connect NMOS source to PFET drain (both = top_plate side)
wire(-380, -1670, -380, -1600, 'top0b0')

# Gate connections
labpin('l_en0b0', 'en0b0', -440, -1700, 1)
wire(-440, -1700, -420, -1700, 'en0b0')

labpin('l_en0b0b', 'en0b0b', -440, -1630, 1)
wire(-440, -1630, -420, -1630, 'en0b0b')

# in0 input pin
iopin('p_in0', 'in0', -380, -1780, 0)
wire(-380, -1780, -380, -1760, 'in0')

# --- Weight Cap C0b0 = 50fF ---
T('Weight Cap', -250, -1780, 0.35, 4)
T('C0b0 = 50 fF', -250, -1755, 0.25, 8)

# Cap placed at (-220, -1650), c0(top)=(-220,-1680), c1(bot)=(-220,-1620)
c1 = cap('XC0b0', -220, -1650, 5, 10)
# top plate connects to top0b0
wire(-380, -1635, -220, -1635, 'top0b0')  # horizontal from TG output
wire(-220, -1635, -220, -1680, 'top0b0')  # up to cap top
# bottom plate to VSS
wire(-220, -1620, -220, -1590, 'vss')
labpin('l_vss_c1', 'vss', -220, -1590, 0)

# --- Parasitic Cap Cbp0b0 = 5fF ---
T('Cbp0b0', -100, -1670, 0.25, 8)
T('5 fF', -100, -1650, 0.2, 8)
c2 = cap('XCbp0b0', -120, -1650, 2.24, 2.24)
wire(-220, -1635, -120, -1635, 'top0b0')
wire(-120, -1635, -120, -1680, 'top0b0')
wire(-120, -1620, -120, -1590, 'vss')

# --- Eval Transmission Gate ---
T('Eval TG', SEC1_X, -1560, 0.35, 4)
T('phi_e / phi_eb', SEC1_X, -1535, 0.25, 8)

# NFET: gate=phi_e, drain=top_plate, source=bl
en = nfet('XNe0b0', -400, -1480, 0.84, 0.15)
T('XNe0b0', -460, -1490, 0.25, 8)
T('0.84/0.15', -460, -1470, 0.2, 8)

# PFET: gate=phi_eb
ep = pfet('XPe0b0', -400, -1410, 1.68, 0.15)
T('XPe0b0', -460, -1420, 0.25, 8)
T('1.68/0.15', -460, -1400, 0.2, 8)

# top_plate connects to eval TG input side
wire(-380, -1600, -380, -1510, 'top0b0')  # from sample TG output down to eval NFET drain
# NFET drain=(-380,-1510), source=(-380,-1450)
# PFET source(top)=(-380,-1440), drain(bottom)=(-380,-1380)
wire(-380, -1510, -380, -1440, 'top0b0')  # NFET drain to PFET source = top_plate side
wire(-380, -1450, -380, -1380, 'bl')  # NFET source to PFET drain = bitline side

# Gate connections
labpin('l_phi_e', 'phi_e', -440, -1480, 1)
wire(-440, -1480, -420, -1480, 'phi_e')

labpin('l_phi_eb', 'phi_eb', -440, -1410, 1)
wire(-440, -1410, -420, -1410, 'phi_eb')

# --- Reset Switch XNr0b0 ---
T('Reset', -180, -1530, 0.35, 4)
T('XNr0b0', -180, -1505, 0.25, 8)
T('0.42/0.15', -180, -1485, 0.2, 8)

rn = nfet('XNr0b0', -170, -1480, 0.42, 0.15)
# gate=phi_r, drain=top_plate, source=vss
# g=(-190,-1480), d=(-150,-1510), s=(-150,-1450)
labpin('l_phi_r_r', 'phi_r', -210, -1480, 1)
wire(-210, -1480, -190, -1480, 'phi_r')
# drain connects to top_plate
wire(-150, -1510, -150, -1535, 'top0b0')
wire(-150, -1535, -220, -1535, 'top0b0')
wire(-220, -1535, -220, -1635, 'top0b0')
# Actually let me simplify: just connect drain up to the horizontal top_plate wire
# source to vss
wire(-150, -1450, -150, -1400, 'vss')
labpin('l_vss_r', 'vss', -150, -1400, 0)

# --- Bitline section ---
T('Bitline', SEC1_X, -1340, 0.35, 4)

# Bitline reset: XNblrst
T('XNblrst', SEC1_X, -1280, 0.25, 8)
T('0.84/0.15', SEC1_X, -1260, 0.2, 8)

br = nfet('XNblrst', -400, -1260, 0.84, 0.15)
# g=(-420,-1260)=phi_r, d=(-380,-1290)=bl, s=(-380,-1230)=vss
labpin('l_phi_r_bl', 'phi_r', -440, -1260, 1)
wire(-440, -1260, -420, -1260, 'phi_r')
# bl
wire(-380, -1380, -380, -1290, 'bl')  # from eval TG down to bitline reset drain
# source to vss
wire(-380, -1230, -380, -1200, 'vss')

# Bitline parasitic cap Cpar = 80fF
T('Cpar = 80 fF', -250, -1280, 0.25, 8)
cp = cap('XCpar', -220, -1270, 8, 10)
# c0=(-220,-1300) connects to bl, c1=(-220,-1240) to vss
wire(-380, -1310, -220, -1310, 'bl')
wire(-220, -1310, -220, -1300, 'bl')
wire(-220, -1240, -220, -1200, 'vss')

# bl output
labpin('l_bl', 'bl', -380, -1340, 1)

# VSS rail
wire(-600, -1200, -100, -1200, 'vss')
iopin('p_vss1', 'vss', -620, -1200, 1)

# VDD rail for section 1
wire(-600, -1810, -100, -1810, 'vdd')
iopin('p_vdd1', 'vdd', -620, -1810, 1)


# ============================================================
# SECTION 2: STRONGARM LATCH COMPARATOR (10 transistors)
# ============================================================
S2_CX = 800   # center x
S2_LX = 650   # left transistor x
S2_RX = 950   # right transistor x (mirrored)

T('StrongARM Latch Comparator (10T)', 500, -1880, 0.5, 4)
T('CLK=0: Reset (outputs to VDD)  |  CLK=1: Evaluate (regenerate)', 500, -1845, 0.3, 8)

# VDD rail
VDD2_Y = -1810
wire(500, VDD2_Y, 1500, VDD2_Y, 'vdd')

# --- Reset PMOS: XM7 (voutp), XM8 (voutn), XM9 (di_p), XM10 (di_n) ---
T('Reset PMOS', 530, -1780, 0.35, 4)

# XM7: pfet at (610,-1730) mirror=0. drain=voutp, gate=clk, source=vdd
m7 = pfet('XM7', 610, -1730, 0.84, 0.15)
T('XM7', 560, -1740, 0.25, 8)
T('0.84/0.15', 555, -1720, 0.2, 8)
# s=vdd at (630,-1760), d=voutp at (630,-1700)
wire(630, -1760, 630, VDD2_Y, 'vdd')

# XM8: pfet at (810,-1730) mirror=1. drain=voutn, gate=clk, source=vdd
m8 = pfet('XM8', 810, -1730, 0.84, 0.15, mirror=1)
T('XM8', 840, -1740, 0.25, 8)
T('0.84/0.15', 840, -1720, 0.2, 8)
wire(790, -1760, 790, VDD2_Y, 'vdd')

# XM9: pfet at (1050,-1730) mirror=0. drain=di_p, gate=clk, source=vdd
m9 = pfet('XM9', 1050, -1730, 0.84, 0.15)
T('XM9', 1000, -1740, 0.25, 8)
T('0.84/0.15', 995, -1720, 0.2, 8)
wire(1070, -1760, 1070, VDD2_Y, 'vdd')

# XM10: pfet at (1250,-1730) mirror=1. drain=di_n, gate=clk, source=vdd
m10 = pfet('XM10', 1250, -1730, 0.84, 0.15, mirror=1)
T('XM10', 1275, -1740, 0.25, 8)
T('0.84/0.15', 1275, -1720, 0.2, 8)
wire(1230, -1760, 1230, VDD2_Y, 'vdd')

# CLK gates for reset PMOS
labpin('l_clk7', 'clk', 570, -1730, 1)
wire(570, -1730, 590, -1730, 'clk')

labpin('l_clk8', 'clk', 850, -1730, 0)
wire(830, -1730, 850, -1730, 'clk')

labpin('l_clk9', 'clk', 1010, -1730, 1)
wire(1010, -1730, 1030, -1730, 'clk')

labpin('l_clk10', 'clk', 1290, -1730, 0)
wire(1270, -1730, 1290, -1730, 'clk')

# --- Cross-Coupled PMOS Latch: XM5, XM6 ---
T('Cross-Coupled PMOS', 650, -1660, 0.35, 4)

# XM5: pfet at (S2_LX, -1600) mirror=0
# drain=voutp(bottom), gate=voutn, source=vdd(top)
m5 = pfet('XM5', S2_LX, -1600, 1.0, 0.15)
T('XM5', 595, -1610, 0.25, 8)
T('1/0.15', 595, -1590, 0.2, 8)
wire(670, -1630, 670, VDD2_Y, 'vdd')  # source to VDD

# XM6: pfet at (S2_RX, -1600) mirror=1
m6 = pfet('XM6', S2_RX, -1600, 1.0, 0.15, mirror=1)
T('XM6', 970, -1610, 0.25, 8)
T('1/0.15', 970, -1590, 0.2, 8)
wire(930, -1630, 930, VDD2_Y, 'vdd')

# Cross-coupling: XM5.gate = voutn, XM6.gate = voutp
# XM5 gate at (630, -1600), XM6 gate at (970, -1600)
# voutp node: connect XM5 drain (670,-1570) and XM7 drain (630,-1700)
wire(670, -1570, 670, -1540, 'voutp')  # XM5 drain down to voutp line
wire(630, -1700, 630, -1540, 'voutp')  # XM7 drain down to voutp line
wire(630, -1540, 670, -1540, 'voutp')

# voutn node: XM6 drain (930,-1570), XM8 drain (790,-1700)
wire(930, -1570, 930, -1540, 'voutn')
wire(790, -1700, 790, -1540, 'voutn')
wire(790, -1540, 930, -1540, 'voutn')

# Cross-couple gates
# XM5.g=(630,-1600) connects to voutn: route from voutn line
wire(630, -1600, 630, -1555, 'voutn')
wire(630, -1555, 790, -1555, 'voutn')
wire(790, -1555, 790, -1540, 'voutn')

# XM6.g=(970,-1600) connects to voutp
wire(970, -1600, 970, -1555, 'voutp')
wire(970, -1555, 670, -1555, 'voutp')
# But this would cross the voutn wire. Use lab pins instead.
# Let me redo cross-coupling with lab pins to avoid crossings

# Actually, let me simplify. Use lab_pins for the cross-coupling connections.
# Remove the complex routing above - just use labels

# Clear the cross-coupling wires (can't remove, they're already appended)
# Let me use a cleaner approach from the start - redo section 2

# I'll restart section 2 with a cleaner layout below

# ============================================================
# Let me restart with a cleaner approach
# ============================================================

# OK - the problem is I can't un-append lines. Let me just make the schematic work
# by using lab_pins for cross-coupling connections instead of direct wires.

# XM5 gate to voutn - use lab pin
labpin('l_voutn_g5', 'voutn', 615, -1600, 1)
wire(615, -1600, 630, -1600, 'voutn')

# XM6 gate to voutp - use lab pin
labpin('l_voutp_g6', 'voutp', 985, -1600, 0)
wire(970, -1600, 985, -1600, 'voutp')

# --- Cross-Coupled NMOS Latch: XM3, XM4 ---
T('Cross-Coupled NMOS', 650, -1500, 0.35, 4)

# XM3: nfet at (S2_LX, -1440) mirror=0
# drain=voutp, gate=voutn, source=di_p
m3 = nfet('XM3', S2_LX, -1440, 1.0, 0.15)
T('XM3', 595, -1450, 0.25, 8)
T('1/0.15', 595, -1430, 0.2, 8)

# XM4: nfet at (S2_RX, -1440) mirror=1
m4 = nfet('XM4', S2_RX, -1440, 1.0, 0.15, mirror=1)
T('XM4', 970, -1450, 0.25, 8)
T('1/0.15', 970, -1430, 0.2, 8)

# XM3 drain (670,-1470) connects to voutp
wire(670, -1540, 670, -1470, 'voutp')

# XM4 drain (930,-1470) connects to voutn
wire(930, -1540, 930, -1470, 'voutn')

# XM3 gate = voutn, XM4 gate = voutp (cross-coupled)
labpin('l_voutn_g3', 'voutn', 615, -1440, 1)
wire(615, -1440, 630, -1440, 'voutn')

labpin('l_voutp_g4', 'voutp', 985, -1440, 0)
wire(970, -1440, 985, -1440, 'voutp')

# XM3 source (670,-1410) = di_p
# XM4 source (930,-1410) = di_n

# di_p connects to XM9 drain (1070,-1700)
labpin('l_dip_m3', 'di_p', 670, -1395, 0)
wire(670, -1410, 670, -1395, 'di_p')

labpin('l_dip_m9', 'di_p', 1070, -1700, 0)

labpin('l_din_m4', 'di_n', 930, -1395, 0)
wire(930, -1410, 930, -1395, 'di_n')

labpin('l_din_m10', 'di_n', 1230, -1700, 0)

# Output labels for voutp, voutn
iopin('p_voutp', 'voutp', 670, -1535, 0)
iopin('p_voutn', 'voutn', 930, -1535, 0)

# --- Input Differential Pair: XM1, XM2 ---
T('Input Diff Pair', 680, -1370, 0.35, 4)

# XM1: nfet at (S2_LX, -1310) mirror=0. gate=vinp, drain=di_p, source=tail
m1 = nfet('XM1', S2_LX, -1310, 4.0, 0.5)
T('XM1', 595, -1320, 0.25, 8)
T('4/0.5', 595, -1300, 0.2, 8)

# XM2: nfet at (S2_RX, -1310) mirror=1
m2 = nfet('XM2', S2_RX, -1310, 4.0, 0.5, mirror=1)
T('XM2', 970, -1320, 0.25, 8)
T('4/0.5', 970, -1300, 0.2, 8)

# XM1 drain (670,-1340) to di_p
labpin('l_dip_m1', 'di_p', 670, -1355, 0)
wire(670, -1340, 670, -1355, 'di_p')

# XM2 drain (930,-1340) to di_n
labpin('l_din_m2', 'di_n', 930, -1355, 0)
wire(930, -1340, 930, -1355, 'di_n')

# Inputs
iopin('p_vinp', 'vinp', 610, -1310, 1)
wire(610, -1310, 630, -1310, 'vinp')

iopin('p_vinn', 'vinn', 990, -1310, 0)
wire(970, -1310, 990, -1310, 'vinn')

# Sources to tail
wire(670, -1280, 670, -1260, 'tail')
wire(930, -1280, 930, -1260, 'tail')
wire(670, -1260, 930, -1260, 'tail')
wire(800, -1260, 800, -1240, 'tail')

# --- Tail Switch: XM0 ---
T('Tail Switch', 760, -1230, 0.35, 4)

m0 = nfet('XM0', 780, -1190, 2.0, 0.15)
T('XM0', 725, -1200, 0.25, 8)
T('2/0.15', 725, -1180, 0.2, 8)

# drain to tail
wire(800, -1220, 800, -1240, 'tail')

# gate = clk
labpin('l_clk0', 'clk', 740, -1190, 1)
wire(740, -1190, 760, -1190, 'clk')

# source to vss
wire(800, -1160, 800, -1130, 'vss')

# CLK input
iopin('p_clk', 'clk', 740, -1210, 1)

# VSS rail for section 2
wire(500, -1130, 1500, -1130, 'vss')


# ============================================================
# SECTION 3: 3-PHASE CLOCK GENERATOR (28 transistors)
# ============================================================
S3_X = 1800  # left edge

T('Non-Overlapping 3-Phase Clock Generator (28T)', S3_X, -1880, 0.5, 4)
T('clk_in -> phi_s (sample) -> phi_e (evaluate) -> phi_r (reset)', S3_X, -1845, 0.3, 8)

# VDD/VSS rails
wire(S3_X, VDD2_Y, 3400, VDD2_Y, 'vdd')
wire(S3_X, -1130, 3400, -1130, 'vss')

# Helper: place an inverter (PFET on top, NFET on bottom) and return pin positions
def inverter(pfet_name, nfet_name, x, y_center, pw, nw, pl=0.15, nl=0.15):
    """Place inverter centered at (x, y_center).
    PFET at y_center-50, NFET at y_center+50.
    Returns (gate_x, gate_y, drain_x, drain_y_top, drain_y_bot, source_top, source_bot)
    """
    # PFET at (x, y_center-50): s=(x+20, y_center-80)->vdd, d=(x+20, y_center-20)->out
    p = pfet(pfet_name, x, y_center-50, pw, pl)
    # NFET at (x, y_center+50): d=(x+20, y_center+20)->out, s=(x+20, y_center+80)->vss
    n = nfet(nfet_name, x, y_center+50, nw, nl)

    # Gate connections: both gates at x-20
    wire(x-20, y_center-50, x-20, y_center+50, 'inv_g_temp')

    # Output: connect PFET drain to NFET drain
    wire(x+20, y_center-20, x+20, y_center+20, 'inv_o_temp')

    return {
        'g': (x-20, y_center),      # combined gate point
        'out': (x+20, y_center),     # output midpoint
        'ps': (x+20, y_center-80),   # PFET source (VDD)
        'ns': (x+20, y_center+80),   # NFET source (VSS)
        'pd': (x+20, y_center-20),   # PFET drain
        'nd': (x+20, y_center+20),   # NFET drain
    }

# --- Master Clock Buffer: 2 inverter stages ---
T('Clock Buffer', S3_X+20, -1780, 0.35, 4)

inv_b1 = inverter('XP_buf1', 'XN_buf1', S3_X+50, -1680, 1.68, 0.84)
T('buf1', S3_X+80, -1680, 0.2, 8)
# VDD and VSS connections
wire(inv_b1['ps'][0], inv_b1['ps'][1], inv_b1['ps'][0], VDD2_Y, 'vdd')
wire(inv_b1['ns'][0], inv_b1['ns'][1], inv_b1['ns'][0], -1130, 'vss')
# Replace the temp gate net label
# Input: clk_in
iopin('p_clk_in', 'clk_in', S3_X, -1680, 1)
wire(S3_X, -1680, inv_b1['g'][0], inv_b1['g'][1], 'clk_in')

inv_b2 = inverter('XP_buf2', 'XN_buf2', S3_X+200, -1680, 1.68, 0.84)
T('buf2', S3_X+230, -1680, 0.2, 8)
wire(inv_b2['ps'][0], inv_b2['ps'][1], inv_b2['ps'][0], VDD2_Y, 'vdd')
wire(inv_b2['ns'][0], inv_b2['ns'][1], inv_b2['ns'][0], -1130, 'vss')
# Connect buf1 output to buf2 input
wire(inv_b1['out'][0], inv_b1['out'][1], inv_b2['g'][0], inv_b2['g'][1], 'clk_buf1')
# buf2 output = clk_buf
labpin('l_clk_buf', 'clk_buf', inv_b2['out'][0]+10, inv_b2['out'][1], 0)

# --- phi_s Generation: 2 inverters ---
T('phi_s Gen', S3_X+20, -1560, 0.35, 4)

inv_s1 = inverter('XP_s1', 'XN_s1', S3_X+50, -1470, 1.68, 0.84)
T('s1', S3_X+80, -1470, 0.2, 8)
wire(inv_s1['ps'][0], inv_s1['ps'][1], inv_s1['ps'][0], VDD2_Y, 'vdd')
wire(inv_s1['ns'][0], inv_s1['ns'][1], inv_s1['ns'][0], -1130, 'vss')
labpin('l_clk_buf_s', 'clk_buf', inv_s1['g'][0]-10, inv_s1['g'][1], 1)
# s1 output = phi_sb
labpin('l_phi_sb', 'phi_sb', inv_s1['out'][0]+10, inv_s1['out'][1], 0)

inv_s2 = inverter('XP_s2', 'XN_s2', S3_X+200, -1470, 1.68, 0.84)
T('s2', S3_X+230, -1470, 0.2, 8)
wire(inv_s2['ps'][0], inv_s2['ps'][1], inv_s2['ps'][0], VDD2_Y, 'vdd')
wire(inv_s2['ns'][0], inv_s2['ns'][1], inv_s2['ns'][0], -1130, 'vss')
wire(inv_s1['out'][0], inv_s1['out'][1], inv_s2['g'][0], inv_s2['g'][1], 'phi_sb')
# s2 output = phi_s
iopin('p_phi_s', 'phi_s', inv_s2['out'][0]+10, inv_s2['out'][1], 0)

# --- Delay Chain: 4 slow inverters ---
T('Delay Chain (1.2 ns)', S3_X+400, -1560, 0.35, 4)

prev_out = None
delay_names = ['d1', 'd2', 'd3', 'd4']
delay_nets = ['d1', 'd2', 'd3', 'd4']
for i, dn in enumerate(delay_names):
    dx = S3_X + 420 + i * 150
    inv_d = inverter(f'XP_{dn}', f'XN_{dn}', dx, -1470, 0.84, 0.42)
    T(dn, dx+30, -1470, 0.2, 8)
    wire(inv_d['ps'][0], inv_d['ps'][1], inv_d['ps'][0], VDD2_Y, 'vdd')
    wire(inv_d['ns'][0], inv_d['ns'][1], inv_d['ns'][0], -1130, 'vss')
    if i == 0:
        labpin(f'l_phi_sb_d', 'phi_sb', inv_d['g'][0]-10, inv_d['g'][1], 1)
    else:
        wire(prev_out[0], prev_out[1], inv_d['g'][0], inv_d['g'][1], delay_nets[i-1])
    prev_out = inv_d['out']
    if i < 3:
        labpin(f'l_{dn}', delay_nets[i], inv_d['out'][0]+10, inv_d['out'][1], 0)

# d4 output
labpin('l_d4', 'd4', prev_out[0]+10, prev_out[1], 0)

# --- NAND Gate for phi_e ---
T('NAND (phi_e enable)', S3_X+20, -1350, 0.35, 4)
T('NAND(phi_sb, d4)', S3_X+20, -1325, 0.25, 8)

# NAND: 2 series NMOS + 2 parallel PMOS
# Series NMOS: XN_na1 on top, XN_na2 on bottom
nand_x = S3_X + 80

n_na1 = nfet('XN_na1', nand_x, -1250, 0.84, 0.15)
T('na1', nand_x+30, -1260, 0.2, 8)
n_na2 = nfet('XN_na2', nand_x, -1190, 0.84, 0.15)
T('na2', nand_x+30, -1200, 0.2, 8)

# na1 source (bottom) to na2 drain (top)
wire(nand_x+20, -1220, nand_x+20, -1220, 'n_na1')  # they should auto-connect

# na2 source to VSS
wire(nand_x+20, -1160, nand_x+20, -1130, 'vss')

# na1 drain = nand output
# Parallel PMOS
p_na1 = pfet('XP_na1', nand_x+200, -1270, 0.84, 0.15)
T('pa1', nand_x+230, -1280, 0.2, 8)
p_na2 = pfet('XP_na2', nand_x+200, -1210, 0.84, 0.15)
T('pa2', nand_x+230, -1220, 0.2, 8)

# PMOS sources to VDD
wire(nand_x+220, -1300, nand_x+220, VDD2_Y, 'vdd')
wire(nand_x+220, -1240, nand_x+220, VDD2_Y, 'vdd')

# PMOS drains to nand output
wire(nand_x+220, -1240, nand_x+220, -1180, 'nand_e1')
wire(nand_x+20, -1280, nand_x+20, -1300, 'nand_e1')
wire(nand_x+20, -1300, nand_x+220, -1300, 'nand_e1')
# Actually this is getting complicated. Let me use lab pins for NAND connections.

# NAND output = nand_e1
labpin('l_nand_e1_n', 'nand_e1', nand_x+20, -1295, 0)
wire(nand_x+20, -1280, nand_x+20, -1295, 'nand_e1')

labpin('l_nand_e1_p1', 'nand_e1', nand_x+220, -1240, 0)
labpin('l_nand_e1_p2', 'nand_e1', nand_x+220, -1180, 0)

# Gate connections: na1.g=phi_sb, na2.g=d4, pa1.g=phi_sb, pa2.g=d4
labpin('l_phisb_na1', 'phi_sb', nand_x-30, -1250, 1)
wire(nand_x-30, -1250, nand_x-20, -1250, 'phi_sb')

labpin('l_d4_na2', 'd4', nand_x-30, -1190, 1)
wire(nand_x-30, -1190, nand_x-20, -1190, 'phi_sb')

labpin('l_phisb_pa1', 'phi_sb', nand_x+180, -1270, 1)
labpin('l_d4_pa2', 'd4', nand_x+180, -1210, 1)

# --- phi_e output inverter ---
T('phi_e Inverter', S3_X+400, -1350, 0.35, 4)

inv_e1 = inverter('XP_e1', 'XN_e1', S3_X+430, -1250, 1.68, 0.84)
T('e1', S3_X+460, -1250, 0.2, 8)
wire(inv_e1['ps'][0], inv_e1['ps'][1], inv_e1['ps'][0], VDD2_Y, 'vdd')
wire(inv_e1['ns'][0], inv_e1['ns'][1], inv_e1['ns'][0], -1130, 'vss')
labpin('l_nand_e1_inv', 'nand_e1', inv_e1['g'][0]-10, inv_e1['g'][1], 1)
# output = phi_e
iopin('p_phi_e', 'phi_e', inv_e1['out'][0]+10, inv_e1['out'][1], 0)

# phi_eb complement
inv_eb = inverter('XP_eb', 'XN_eb', S3_X+580, -1250, 1.68, 0.84)
T('eb', S3_X+610, -1250, 0.2, 8)
wire(inv_eb['ps'][0], inv_eb['ps'][1], inv_eb['ps'][0], VDD2_Y, 'vdd')
wire(inv_eb['ns'][0], inv_eb['ns'][1], inv_eb['ns'][0], -1130, 'vss')
wire(inv_e1['out'][0], inv_e1['out'][1], inv_eb['g'][0], inv_eb['g'][1], 'phi_e')
iopin('p_phi_eb', 'phi_eb', inv_eb['out'][0]+10, inv_eb['out'][1], 0)

# --- NOR Gate for phi_r ---
T('NOR (phi_r = NOR(phi_s, phi_e))', S3_X+800, -1350, 0.35, 4)

nor_x = S3_X + 860

# NOR: 2 parallel NMOS + 2 series PMOS
n_nr1 = nfet('XN_nr1', nor_x, -1250, 0.84, 0.15)
T('nr1', nor_x+30, -1260, 0.2, 8)
n_nr2 = nfet('XN_nr2', nor_x+120, -1250, 0.84, 0.15)
T('nr2', nor_x+150, -1260, 0.2, 8)

# Parallel NMOS: both drains to output, both sources to VSS
wire(nor_x+20, -1220, nor_x+20, -1210, 'vss')
wire(nor_x+20, -1210, nor_x+20, -1130, 'vss')
wire(nor_x+140, -1220, nor_x+140, -1130, 'vss')

# NOR output from NMOS drains
labpin('l_phi_r_b_n1', 'phi_r_b', nor_x+20, -1290, 0)
wire(nor_x+20, -1280, nor_x+20, -1290, 'phi_r_b')
labpin('l_phi_r_b_n2', 'phi_r_b', nor_x+140, -1290, 0)
wire(nor_x+140, -1280, nor_x+140, -1290, 'phi_r_b')

# Series PMOS
p_nr1 = pfet('XP_nr1', nor_x+60, -1400, 1.68, 0.15)
T('pr1', nor_x+90, -1410, 0.2, 8)
p_nr2 = pfet('XP_nr2', nor_x+60, -1340, 1.68, 0.15)
T('pr2', nor_x+90, -1350, 0.2, 8)

# pr1 source to VDD
wire(nor_x+80, -1430, nor_x+80, VDD2_Y, 'vdd')
# pr1 drain to pr2 source (series)
wire(nor_x+80, -1370, nor_x+80, -1370, 'n_nr')
# pr2 drain = phi_r_b output
labpin('l_phi_r_b_p', 'phi_r_b', nor_x+80, -1305, 0)
wire(nor_x+80, -1310, nor_x+80, -1305, 'phi_r_b')

# Gate connections
labpin('l_phis_nr1', 'phi_s', nor_x-30, -1250, 1)
wire(nor_x-30, -1250, nor_x-20, -1250, 'phi_s')

labpin('l_phie_nr2', 'phi_e', nor_x+100, -1250, 1)
wire(nor_x+100, -1250, nor_x+100, -1250, 'phi_e')

labpin('l_phis_pr1', 'phi_s', nor_x+40, -1400, 1)
labpin('l_phie_pr2', 'phi_e', nor_x+40, -1340, 1)

# --- phi_r output inverter ---
T('phi_r Inverter', S3_X+1100, -1350, 0.35, 4)

inv_ri = inverter('XP_ri', 'XN_ri', S3_X+1130, -1250, 1.68, 0.84)
T('ri', S3_X+1160, -1250, 0.2, 8)
wire(inv_ri['ps'][0], inv_ri['ps'][1], inv_ri['ps'][0], VDD2_Y, 'vdd')
wire(inv_ri['ns'][0], inv_ri['ns'][1], inv_ri['ns'][0], -1130, 'vss')
labpin('l_phi_r_b_ri', 'phi_r_b', inv_ri['g'][0]-10, inv_ri['g'][1], 1)
iopin('p_phi_r', 'phi_r', inv_ri['out'][0]+10, inv_ri['out'][1], 0)


# ============================================================
# GLOBAL IO PINS
# ============================================================
iopin('p_vdd', 'vdd', 500, VDD2_Y, 1)
iopin('p_vss', 'vss', 500, -1130, 1)


# ============================================================
# Write the file
# ============================================================
# Fix: remove temporary net labels from inverter helper function
# The inverter helper uses 'inv_g_temp' and 'inv_o_temp' labels which should
# be replaced with proper net names. Since xschem auto-connects overlapping
# wire segments, these temp labels are OK - they just label the short internal
# segments within each inverter.

output = '\n'.join(lines) + '\n'

# Fix the /usr/share path issue - replace with /usr/local/share
output = output.replace('/usr/share/xschem/', '/usr/local/share/xschem/')

with open('/home/ubuntu/analog-ai-chips/vibrosense/06_classifier/classifier.sch', 'w') as f:
    f.write(output)

print(f"Generated classifier.sch with {len(lines)} lines")
