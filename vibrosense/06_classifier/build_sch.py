#!/usr/bin/env python3
"""One-shot script to build classifier.sch — run once then delete."""
SKY = "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr"
DEV = "/usr/local/share/xschem/xschem_library/devices"
L = []  # output lines
def T(txt, x, y, sz, layer): L.append(f'T {{{txt}}} {x} {y} 0 0 {sz} {sz} {{layer={layer}}}')
def W(x1,y1,x2,y2,net): L.append(f'N {x1} {y1} {x2} {y2} {{lab={net}}}')
def IO(name,lab,x,y,m=0): L.append(f'C {{{DEV}/iopin.sym}} {x} {y} 0 {m} {{name={name} lab={lab}}}')
def LP(name,lab,x,y,m=0): L.append(f'C {{{DEV}/lab_pin.sym}} {x} {y} 0 {m} {{name={name} lab={lab}}}')

def NF(name,x,y,w,l,m=0):
    """NFET: g(x-20*s,y) d(x+20*s,y-30) s(x+20*s,y+30) where s=1 if m=0, s=-1 if m=1"""
    L.append(f'C {{{SKY}/nfet_01v8.sym}} {x} {y} 0 {m} {{name={name}\nW={w}\nL={l}\nnf=1\nmult=1\nmodel=nfet_01v8\nspiceprefix=X\n}}')
    s = 1 if m==0 else -1
    return {'g':(x-20*s,y),'d':(x+20*s,y-30),'s':(x+20*s,y+30),'b':(x+20*s,y)}

def PF(name,x,y,w,l,m=0):
    """PFET: g(x-20*s,y) s(x+20*s,y-30)[VDD] d(x+20*s,y+30)[circuit]"""
    L.append(f'C {{{SKY}/pfet_01v8.sym}} {x} {y} 0 {m} {{name={name}\nW={w}\nL={l}\nnf=1\nmult=1\nmodel=pfet_01v8\nspiceprefix=X\n}}')
    s = 1 if m==0 else -1
    return {'g':(x-20*s,y),'s':(x+20*s,y-30),'d':(x+20*s,y+30),'b':(x+20*s,y)}

def CAP(name,x,y,w,l):
    """MIM cap: c0(x,y-30)[top] c1(x,y+30)[bottom]"""
    L.append(f'C {{{SKY}/cap_mim_m3_1.sym}} {x} {y} 0 0 {{name={name}\nW={w}\nL={l}\nMF=1\nmodel=cap_mim_m3_1\nspiceprefix=X\n}}')
    return {'c0':(x,y-30),'c1':(x,y+30)}


VDD = -1430
VSS = -480

# ==================== HEADER ====================
L.append('v {xschem version=3.4.4 file_version=1.2}')
for h in 'GKVSE': L.append(f'{h} {{}}')

# ==================== TITLE ====================
T('VibroSense Block 06: Charge-Domain MAC Classifier', -200, -1550, 1.0, 15)
T('8-Input x 4-Bit Weight MAC  |  StrongARM Comparator  |  3-Phase Clock  \\u2014  SKY130A  |  1.8 V', -200, -1500, 0.4, 15)
T('~702 transistors  |  ~260 MIM caps  |  10/10 specs PASS in ngspice-42  |  0.08 LSB linearity  |  99.5% MC accuracy  |  < 1 nW @ 10 Hz', -200, -1465, 0.3, 8)

# ==================== SECTION 1: MAC BIT-CELL ====================
T('MAC Bit-Cell (Input 0, Bit 0 \\u2014 representative)', -550, -1410, 0.45, 4)
T('x32 cells/MAC  x4 MACs  =  128 cells, ~702 transistors total', -550, -1380, 0.25, 8)

# --- Sample TG ---
T('Sample TG', -540, -1340, 0.3, 4)
T('en = AND(phi_s, weight_bit)', -540, -1320, 0.2, 8)

sn = NF('XNt0b0', -430, -1270, 0.84, 0.15)
T('XNt0b0', -475, -1285, 0.2, 8); T('0.84/0.15', -475, -1268, 0.18, 8)
sp = PF('XPt0b0', -260, -1270, 1.68, 0.15, m=1)
T('XPt0b0', -215, -1285, 0.2, 8); T('1.68/0.15', -215, -1268, 0.18, 8)

# TG wires: in0 side (NFET drain + PFET source) and top0b0 side (NFET source + PFET drain)
W(-410,-1300, -280,-1300, 'in0')       # in0 bus
W(-410,-1240, -280,-1240, 'top0b0')    # top_plate bus
W(-345,-1300, -345,-1370, 'in0')       # in0 up to input

LP('l_en0b0','en0b0',-460,-1270, 1); W(-460,-1270,-450,-1270,'en0b0')
LP('l_en0b0b','en0b0b',-230,-1270, 0); W(-240,-1270,-230,-1270,'en0b0b')
IO('p_in0','in0',-345,-1380, 0)

# --- Caps ---
T('Weight Cap', -420, -1200, 0.3, 4)
c1 = CAP('XC0b0', -380, -1155, 5, 10)
T('C0b0', -415, -1160, 0.2, 8); T('50 fF', -415, -1143, 0.18, 8)
c2 = CAP('XCbp0b0', -250, -1155, 2.24, 2.24)
T('Cbp0b0', -215, -1160, 0.2, 8); T('5 fF par.', -215, -1143, 0.18, 8)

# top0b0 from TG down to caps
W(-345,-1240, -345,-1185, 'top0b0')
W(-380,-1185, -250,-1185, 'top0b0')   # horizontal connecting cap tops
# cap bottoms to vss
W(-380,-1125, -380,-1105, 'vss'); LP('l_vss_c1','vss',-380,-1105,0)
W(-250,-1125, -250,-1105, 'vss'); LP('l_vss_c2','vss',-250,-1105,0)

# --- Eval TG ---
T('Eval TG', -540, -1080, 0.3, 4)

en = NF('XNe0b0', -430, -1030, 0.84, 0.15)
T('XNe0b0', -475, -1045, 0.2, 8); T('0.84/0.15', -475, -1028, 0.18, 8)
ep = PF('XPe0b0', -260, -1030, 1.68, 0.15, m=1)
T('XPe0b0', -215, -1045, 0.2, 8); T('1.68/0.15', -215, -1028, 0.18, 8)

W(-410,-1060, -280,-1060, 'top0b0')   # top_plate side
W(-410,-1000, -280,-1000, 'bl')       # bitline side
W(-345,-1185, -345,-1060, 'top0b0')   # vertical from caps to eval TG

LP('l_phi_e','phi_e',-460,-1030, 1); W(-460,-1030,-450,-1030,'phi_e')
LP('l_phi_eb','phi_eb',-230,-1030, 0); W(-240,-1030,-230,-1030,'phi_eb')

# --- Reset NMOS ---
T('Reset', -140, -1145, 0.3, 4)
T('XNr0b0', -140, -1125, 0.2, 8); T('0.42/0.15', -140, -1108, 0.18, 8)
rn = NF('XNr0b0', -120, -1080, 0.42, 0.15)
LP('l_phi_r_r','phi_r',-155,-1080,1); W(-155,-1080,-140,-1080,'phi_r')
LP('l_top0b0_r','top0b0',-100,-1120,0); W(-100,-1110,-100,-1120,'top0b0')
LP('l_vss_r','vss',-100,-1060,0); W(-100,-1050,-100,-1060,'vss')

# --- BL Reset + Cpar ---
T('Bitline Reset', -540, -920, 0.3, 4)
T('XNblrst', -475, -900, 0.2, 8); T('0.84/0.15', -475, -883, 0.18, 8)
br = NF('XNblrst', -430, -870, 0.84, 0.15)
LP('l_phi_r_bl','phi_r',-470,-870,1); W(-470,-870,-450,-870,'phi_r')

T('Cpar', -270, -920, 0.3, 4); T('80 fF routing', -270, -900, 0.2, 8)
cp = CAP('XCpar', -260, -870, 8, 10)

# bl from eval TG to bitline reset area
W(-345,-1000, -345,-900, 'bl')
W(-410,-900, -260,-900, 'bl')    # horizontal: BL reset drain to Cpar top
# VSS connections
W(-410,-840, -410, VSS, 'vss')
W(-260,-840, -260, VSS, 'vss')
LP('l_bl','bl',-345,-950,1)

# Section 1 rails
W(-550, VDD, -80, VDD, 'vdd')
W(-550, VSS, -80, VSS, 'vss')
IO('p_vdd1','vdd',-560, VDD, 1)
IO('p_vss1','vss',-560, VSS, 1)


# ==================== SECTION 2: STRONGARM COMPARATOR ====================
T('StrongARM Latch Comparator (10T)', 200, -1410, 0.45, 4)
T('CLK=0: Reset  |  CLK=1: Evaluate + Regenerate', 200, -1385, 0.25, 8)

# VDD rail
W(200, VDD, 900, VDD, 'vdd')

# --- Reset PMOS row (y=-1300) ---
T('Reset', 230, -1345, 0.3, 4)

XM9  = PF('XM9',  265,-1300, 0.84, 0.15)
T('XM9',  228,-1308, 0.18, 8); T('0.84/0.15', 223,-1293, 0.15, 8)
XM7  = PF('XM7',  395,-1300, 0.84, 0.15)
T('XM7',  358,-1308, 0.18, 8); T('0.84/0.15', 353,-1293, 0.15, 8)

T('P-Latch', 475, -1345, 0.3, 4)
XM5  = PF('XM5',  500,-1300, 1.0, 0.15)
T('XM5',  463,-1308, 0.18, 8); T('1/0.15', 463,-1293, 0.15, 8)

XM6  = PF('XM6',  620,-1300, 1.0, 0.15, m=1)
T('XM6',  643,-1308, 0.18, 8); T('1/0.15', 643,-1293, 0.15, 8)
XM8  = PF('XM8',  725,-1300, 0.84, 0.15, m=1)
T('XM8',  748,-1308, 0.18, 8); T('0.84/0.15', 748,-1293, 0.15, 8)
XM10 = PF('XM10', 855,-1300, 0.84, 0.15, m=1)
T('XM10', 878,-1308, 0.18, 8); T('0.84/0.15', 878,-1293, 0.15, 8)


# VDD from each source
for sx in [285, 415, 520, 600, 705, 835]:
    W(sx, -1330, sx, VDD, 'vdd')

# CLK gates
for gx in [245, 375]:           # XM9, XM7 (mirror=0, gate at x-20)
    LP(f'l_clk_{gx}','clk', gx-15, -1300, 1); W(gx-15,-1300, gx,-1300,'clk')
for gx in [745, 875]:           # XM8, XM10 (mirror=1, gate at x+20)
    LP(f'l_clk_{gx}','clk', gx+15, -1300, 0); W(gx,-1300, gx+15,-1300,'clk')

# voutp: XM7.d(415,-1270) to XM5.d(520,-1270)
W(415,-1270, 520,-1270, 'voutp')
# voutn: XM6.d(600,-1270) to XM8.d(705,-1270)
W(600,-1270, 705,-1270, 'voutn')
# di_p: XM9.d(285,-1270)
LP('l_dip_m9','di_p', 285,-1258, 0); W(285,-1270, 285,-1258, 'di_p')
# di_n: XM10.d(835,-1270)
LP('l_din_m10','di_n', 835,-1258, 0); W(835,-1270, 835,-1258, 'di_n')

# Cross-couple gates
LP('l_voutn_g5','voutn', 465,-1300, 1); W(465,-1300, 480,-1300,'voutn')   # XM5.g
LP('l_voutp_g6','voutp', 655,-1300, 0); W(640,-1300, 655,-1300,'voutp')   # XM6.g

# --- Cross-coupled NMOS (y=-1170) ---
T('N-Latch', 395, -1220, 0.3, 4)

XM3 = NF('XM3', 440,-1170, 1.0, 0.15)
T('XM3', 398,-1178, 0.18, 8); T('1/0.15', 398,-1163, 0.15, 8)
XM4 = NF('XM4', 680,-1170, 1.0, 0.15, m=1)
T('XM4', 700,-1178, 0.18, 8); T('1/0.15', 700,-1163, 0.15, 8)

# XM3.d(460,-1200) to voutp, XM4.d(660,-1200) to voutn
W(460,-1200, 460,-1270, 'voutp')   # up to voutp wire (460 is between 415-520) ✓
W(660,-1200, 660,-1270, 'voutn')   # up to voutn wire (660 is between 600-705) ✓

# Cross-couple gates
LP('l_voutn_g3','voutn', 405,-1170, 1); W(405,-1170, 420,-1170,'voutn')
LP('l_voutp_g4','voutp', 715,-1170, 0); W(700,-1170, 715,-1170,'voutp')

# di_p: XM3.s(460,-1140)   di_n: XM4.s(660,-1140)

# Output pins
IO('p_voutp','voutp', 468, -1253, 0)
IO('p_voutn','voutn', 652, -1253, 0)

# --- Input Diff Pair (y=-1060) ---
T('Input Pair', 420, -1110, 0.3, 4)

XM1 = NF('XM1', 440,-1060, 4.0, 0.5)
T('XM1', 398,-1068, 0.18, 8); T('4/0.5', 398,-1053, 0.15, 8)
XM2 = NF('XM2', 680,-1060, 4.0, 0.5, m=1)
T('XM2', 700,-1068, 0.18, 8); T('4/0.5', 700,-1053, 0.15, 8)

# di_p: XM1.d(460,-1090) up to XM3.s(460,-1140)
W(460,-1090, 460,-1140, 'di_p')
# di_n: XM2.d(660,-1090) up to XM4.s(660,-1140)
W(660,-1090, 660,-1140, 'di_n')

# Input gates
IO('p_vinp','vinp', 400,-1060, 1); W(400,-1060, 420,-1060,'vinp')
IO('p_vinn','vinn', 720,-1060, 0); W(700,-1060, 720,-1060,'vinn')

# tail: XM1.s(460,-1030) to XM2.s(660,-1030)
W(460,-1030, 660,-1030, 'tail')

# --- Tail Switch (y=-950) ---
T('Tail', 528, -985, 0.3, 4)

XM0 = NF('XM0', 540,-950, 2.0, 0.15)
T('XM0', 498,-958, 0.18, 8); T('2/0.15', 498,-943, 0.15, 8)

# XM0.d(560,-980) to tail
W(560,-980, 560,-1030, 'tail')
# XM0.s(560,-920) to VSS
W(560,-920, 560, VSS, 'vss')
# gate = clk
IO('p_clk','clk', 500,-950, 1); W(500,-950, 520,-950,'clk')

# VSS rail for section 2
W(200, VSS, 900, VSS, 'vss')


# ==================== SECTION 3: CLOCK GENERATOR ====================
T('Non-Overlapping 3-Phase Clock Generator (30T)', 1000, -1410, 0.45, 4)
T('NAND-based  |  clk_in \\u2192 phi_s, phi_e, phi_r with dead time', 1000, -1385, 0.25, 8)

# VDD/VSS for clock gen use local lab_pin stubs on each inverter

# Inverter helper: place PFET at yc-35, NFET at yc+35
# Connect gate wire, output wire, VDD and VSS
def inv(pn, nn, x, yc, pw, nw, input_net, output_net, pl=0.15, nl=0.15):
    PF(pn, x, yc-35, pw, pl)
    NF(nn, x, yc+35, nw, nl)
    W(x-20, yc-35, x-20, yc+35, input_net)     # gate
    W(x+20, yc-5, x+20, yc+5, output_net)       # output (drain-drain)
    W(x+20, yc-65, x+20, yc-80, 'vdd')          # short VDD stub
    LP(f'l_vdd_{pn}','vdd', x+20, yc-80, 0)
    W(x+20, yc+65, x+20, yc+80, 'vss')          # short VSS stub
    LP(f'l_vss_{nn}','vss', x+20, yc+80, 0)
    return (x-20, yc), (x+20, yc)  # input point, output point

# --- Row 1: Buffer + phi_s (y_c = -1280) ---
T('Buffer', 1085, -1355, 0.3, 4)
_, ob1 = inv('XP_buf1','XN_buf1', 1080, -1280, 1.68, 0.84, 'clk_in','clk_buf1')
T('buf1', 1105, -1283, 0.18, 8)
_, ob2 = inv('XP_buf2','XN_buf2', 1200, -1280, 1.68, 0.84, 'clk_buf1','clk_buf')
T('buf2', 1225, -1283, 0.18, 8)
W(ob1[0], ob1[1], 1180, -1280, 'clk_buf1')  # buf1.out to buf2.in

IO('p_clk_in','clk_in', 1040, -1280, 1)
W(1040,-1280, 1060,-1280,'clk_in')

T('phi_s', 1325, -1355, 0.3, 4)
_, os1 = inv('XP_s1','XN_s1', 1350, -1280, 1.68, 0.84, 'clk_buf','phi_sb')
T('s1', 1375, -1283, 0.18, 8)
_, os2 = inv('XP_s2','XN_s2', 1470, -1280, 1.68, 0.84, 'phi_sb','phi_s')
T('s2', 1495, -1283, 0.18, 8)
W(ob2[0], ob2[1], 1330, -1280, 'clk_buf')  # buf2.out to s1.in
W(os1[0], os1[1], 1450, -1280, 'phi_sb')   # s1.out to s2.in

IO('p_phi_s','phi_s', 1510, -1280, 0)
W(1490,-1280, 1510,-1280, 'phi_s')

# --- Row 2: Delay chain (y_c = -1120) ---
T('Delay Chain (4 slow inverters \\u2248 1.2 ns)', 1050, -1195, 0.3, 4)

dnets = ['phi_sb','d1','d2','d3','d4']
dxs = [1080, 1200, 1320, 1440]
for i, dx in enumerate(dxs):
    _, od = inv(f'XP_d{i+1}', f'XN_d{i+1}', dx, -1120, 0.84, 0.42, dnets[i], dnets[i+1])
    T(f'd{i+1}', dx+25, -1123, 0.18, 8)
    if i > 0:
        W(prev_o[0], prev_o[1], dx-20, -1120, dnets[i])
    prev_o = od

# d1 input from phi_sb (use lab_pin)
LP('l_phisb_d','phi_sb', 1045, -1120, 1); W(1045,-1120, 1060,-1120,'phi_sb')
# d4 output label
LP('l_d4_out','d4', 1475, -1120, 0); W(1460,-1120, 1475,-1120,'d4')

# --- Row 3: NAND gate (y ≈ -940) ---
T('NAND', 1050, -1010, 0.3, 4)
T('AND(phi_sb, d4)', 1050, -990, 0.2, 8)

# PMOS parallel: sources to VDD, drains to nand_e1
pa1 = PF('XP_na1', 1070, -960, 0.84, 0.15)
T('pa1', 1033,-963, 0.15, 8)
pa2 = PF('XP_na2', 1160, -960, 0.84, 0.15)
T('pa2', 1185,-963, 0.15, 8)

W(1090,-990, 1090,-1005, 'vdd'); LP('l_vdd_pa1','vdd',1090,-1005,0)
W(1180,-990, 1180,-1005, 'vdd'); LP('l_vdd_pa2','vdd',1180,-1005,0)
W(1090,-930, 1180,-930, 'nand_e1')  # pa1.d to pa2.d

# NMOS series: na1 drain=nand_e1, na1.s=n_na1, na2.d=n_na1, na2.s=vss
na1 = NF('XN_na1', 1115, -890, 0.84, 0.15)
T('na1', 1140,-893, 0.15, 8)
na2 = NF('XN_na2', 1115, -830, 0.84, 0.15)
T('na2', 1140,-833, 0.15, 8)

# na1.d(1135,-920) to nand_e1 wire
W(1135,-920, 1135,-930, 'nand_e1')  # T-junction onto pa drain wire
# na1.s(1135,-860) to na2.d(1135,-860): auto-connect (same point!)
# na2.s(1135,-800) to VSS
W(1135,-800, 1135,-790, 'vss'); LP('l_vss_na2','vss',1135,-790,0)

# Gate connections
LP('l_phisb_pa1','phi_sb', 1035,-960, 1); W(1035,-960, 1050,-960,'phi_sb')
LP('l_d4_pa2','d4', 1125,-960, 1); W(1125,-960, 1140,-960,'d4')
LP('l_phisb_na1','phi_sb', 1080,-890, 1); W(1080,-890, 1095,-890,'phi_sb')
LP('l_d4_na2','d4', 1080,-830, 1); W(1080,-830, 1095,-830,'d4')

# --- phi_e output inverter ---
T('phi_e', 1250, -1010, 0.3, 4)
_, oe1 = inv('XP_e1','XN_e1', 1280, -940, 1.68, 0.84, 'nand_e1','phi_e')
T('e1', 1305, -943, 0.18, 8)

# Connect NAND output to phi_e inverter input
LP('l_nand_e1','nand_e1', 1245, -940, 1); W(1245,-940, 1260,-940,'nand_e1')

# phi_eb complement
_, oeb = inv('XP_eb','XN_eb', 1400, -940, 1.68, 0.84, 'phi_e','phi_eb')
T('eb', 1425, -943, 0.18, 8)
W(oe1[0], oe1[1], 1380, -940, 'phi_e')

IO('p_phi_e','phi_e', 1310, -960, 0)
IO('p_phi_eb','phi_eb', 1440, -940, 0)
W(1420,-940, 1440,-940, 'phi_eb')

# --- NOR gate (y ≈ -940) ---
T('NOR', 1520, -1010, 0.3, 4)
T('NOR(phi_s, phi_e)', 1520, -990, 0.2, 8)

# Parallel NMOS: both drain=phi_r_b, both source=vss
nr1 = NF('XN_nr1', 1540, -890, 0.84, 0.15)
T('nr1', 1565,-893, 0.15, 8)
nr2 = NF('XN_nr2', 1630, -890, 0.84, 0.15)
T('nr2', 1655,-893, 0.15, 8)

W(1560,-920, 1650,-920, 'phi_r_b')  # drain wire
W(1560,-860, 1560,-845, 'vss'); LP('l_vss_nr1','vss',1560,-845,0)
W(1650,-860, 1650,-845, 'vss'); LP('l_vss_nr2','vss',1650,-845,0)

# Series PMOS: pr1 source=VDD, pr1 drain=n_nr=pr2 source, pr2 drain=phi_r_b
pr1 = PF('XP_nr1', 1585, -980, 1.68, 0.15)
T('pr1', 1610,-983, 0.15, 8)
pr2 = PF('XP_nr2', 1585, -930, 1.68, 0.15)
T('pr2', 1610,-933, 0.15, 8)

W(1605,-1010, 1605,-1025, 'vdd'); LP('l_vdd_pr1','vdd',1605,-1025,0)  # pr1 source
W(1605,-950, 1605,-960, 'n_nr')     # pr1.d to pr2.s (series connection)
W(1605,-900, 1605,-920, 'phi_r_b')  # pr2.d to phi_r_b wire

# Gate connections
LP('l_phis_nr1','phi_s', 1505,-890, 1); W(1505,-890, 1520,-890,'phi_s')
LP('l_phie_nr2','phi_e', 1615,-890, 1); W(1615,-890, 1610,-890,'phi_e')
LP('l_phis_pr1','phi_s', 1550,-980, 1); W(1550,-980, 1565,-980,'phi_s')
LP('l_phie_pr2','phi_e', 1550,-930, 1); W(1550,-930, 1565,-930,'phi_e')

# --- phi_r output inverter ---
T('phi_r', 1700, -1010, 0.3, 4)
_, ori = inv('XP_ri','XN_ri', 1730, -940, 1.68, 0.84, 'phi_r_b','phi_r')
T('ri', 1755, -943, 0.18, 8)

LP('l_phirb_ri','phi_r_b', 1695,-940, 1); W(1695,-940, 1710,-940,'phi_r_b')

IO('p_phi_r','phi_r', 1770, -940, 0)
W(1750,-940, 1770,-940, 'phi_r')


# ==================== GLOBAL ====================
IO('p_vdd','vdd', 200, VDD, 1)
IO('p_vss','vss', 200, VSS, 1)

# ==================== WRITE ====================
with open('/home/ubuntu/analog-ai-chips/vibrosense/06_classifier/classifier.sch','w') as f:
    f.write('\n'.join(L) + '\n')
print(f"OK: {len(L)} lines")
