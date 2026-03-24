#!/usr/bin/env python3
"""Generate xschem schematic for Block 05: True RMS + Peak + Crest Factor.
Iterate until aesthetically clean."""

PDK = "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr"
DEV = "/usr/share/xschem/xschem_library/devices"

lines = []

def T(text, x, y, scale=0.4, layer=4, rot=0, flip=0):
    lines.append(f'T {{{text}}} {x} {y} {rot} {flip} {scale} {scale} {{layer={layer}}}')

def C(sym, x, y, rot=0, flip=0, props=""):
    lines.append(f'C {{{sym}}} {x} {y} {rot} {flip} {{{props}}}')

def N(x1, y1, x2, y2, lab=""):
    lines.append(f'N {x1} {y1} {x2} {y2} {{lab={lab}}}')

def nfet(name, x, y, W, L, rot=0, flip=0):
    C(f"{PDK}/nfet_01v8.sym", x, y, rot, flip,
      f"name={name}\nW={W}\nL={L}\nnf=1\nmult=1\nmodel=nfet_01v8\nspiceprefix=X")

def pfet(name, x, y, W, L, rot=0, flip=0):
    C(f"{PDK}/pfet_01v8.sym", x, y, rot, flip,
      f"name={name}\nW={W}\nL={L}\nnf=1\nmult=1\nmodel=pfet_01v8\nspiceprefix=X")

def res(name, x, y, value, rot=0, flip=0):
    C(f"{DEV}/res.sym", x, y, rot, flip, f"name={name}\nvalue={value}")

def cap(name, x, y, value, rot=0, flip=0):
    C(f"{DEV}/capa.sym", x, y, rot, flip, f"name={name}\nvalue={value}")

def iopin(name, x, y, rot=0, flip=0, lab=""):
    C(f"{DEV}/iopin.sym", x, y, rot, flip, f"name={name} lab={lab}")

def labpin(name, x, y, rot=0, flip=0, lab=""):
    C(f"{DEV}/lab_pin.sym", x, y, rot, flip, f"name={name} lab={lab}")

# ====================================================================
# PIN POSITIONS (relative to component origin)
# ====================================================================
# NFET at (cx,cy,rot=0,flip=0): G(cx-20,cy) D(cx+20,cy-30) S(cx+20,cy+30) B(cx+20,cy)
# NFET at (cx,cy,rot=0,flip=1): G(cx+20,cy) D(cx-20,cy-30) S(cx-20,cy+30) B(cx-20,cy)
# PFET at (cx,cy,rot=0,flip=0): G(cx-20,cy) S(cx+20,cy-30) D(cx+20,cy+30) B(cx+20,cy)
# PFET at (cx,cy,rot=0,flip=1): G(cx+20,cy) S(cx-20,cy-30) D(cx-20,cy+30) B(cx-20,cy)
# res at (cx,cy,rot=0): P(cx,cy-30) M(cx,cy+30)
# res at (cx,cy,rot=3): P(cx-30,cy) M(cx+30,cy)
# capa at (cx,cy,rot=0): p(cx,cy-30) m(cx,cy+30)

# ====================================================================
lines.append('v {xschem version=3.4.4 file_version=1.2}')
for s in ['G', 'K', 'V', 'S', 'E']:
    lines.append(f'{s} {{}}')

# ====================================================================
# LAYOUT
# ====================================================================
VDD = -1340
GND = -260

# ====================================================================
# TITLE
# ====================================================================
T("VibroSense Block 05: True RMS + Peak + Crest Factor", -380, -1520, 1.0, 15)
T("Single-Pair MOSFET Square-Law Squarer -- SKY130A", -380, -1460, 0.5, 15)
T("10 MOSFETs  |  8 Resistors  |  3 Capacitors  |  8.0 uW  |  All PVT PASS", -380, -1410, 0.4, 8)

# ====================================================================
# SECTION 1: MOSFET SQUARE-LAW SQUARER
# ====================================================================
T("MOSFET Square-Law Squarer", -80, -1300, 0.5, 4)

# ---- Signal Branch (x=20) ----
# Rsig: 100k load from VDD to sig_d
T("Rsig", -25, -1100, 0.3, 8)
T("100k", -25, -1078, 0.25, 8)
res("R_sig", 20, -1100, "100k")
# P(20,-1130) M(20,-1070)

N(20, VDD, 20, -1130, "vdd")       # VDD to Rsig top
N(20, -1070, 20, -860, "sig_d")     # Rsig bottom to sig_d

# XMs: signal NFET
T("XMs", -35, -700, 0.3, 8)
T("0.84/6", -35, -678, 0.25, 8)
nfet("XMs", 0, -720, 0.84, 6)
# G(-20,-720) D(20,-750) S(20,-690) B(20,-720)

N(20, -860, 20, -750, "sig_d")      # sig_d to XMs drain
N(20, -690, 20, GND, "gnd")         # XMs source to GND

# Riso_s: 1k isolation horizontal
T("Riso_s", 105, -905, 0.25, 8)
T("1k", 125, -885, 0.2, 8)
res("R_iso_s", 140, -860, "1k", rot=3)
# P(110,-860) M(170,-860)
N(20, -860, 110, -860, "sig_d")     # sig_d to Riso_s

# ---- Reference Branch (x=300) ----
# Rref: 100k load from VDD to ref_d
T("Rref", 255, -1100, 0.3, 8)
T("100k", 255, -1078, 0.25, 8)
res("R_ref", 300, -1100, "100k")
# P(300,-1130) M(300,-1070)

N(300, VDD, 300, -1130, "vdd")       # VDD to Rref top
N(300, -1070, 300, -860, "ref_d")    # Rref bottom to ref_d

# XMr: reference NFET
T("XMr", 245, -700, 0.3, 8)
T("0.84/6", 245, -678, 0.25, 8)
nfet("XMr", 280, -720, 0.84, 6)
# G(260,-720) D(300,-750) S(300,-690) B(300,-720)

N(300, -860, 300, -750, "ref_d")     # ref_d to XMr drain
N(300, -690, 300, GND, "gnd")        # XMr source to GND

# Riso_r: 1k isolation horizontal
T("Riso_r", 385, -905, 0.25, 8)
T("1k", 405, -885, 0.2, 8)
res("R_iso_r", 420, -860, "1k", rot=3)
# P(390,-860) M(450,-860)
N(300, -860, 390, -860, "ref_d")     # ref_d to Riso_r

# Gate labels
labpin("l_inp1", -20, -720, 0, 1, "inp")    # XMs gate = inp
labpin("l_vcm1", 260, -720, 0, 1, "vcm")    # XMr gate = vcm

# ====================================================================
# SECTION 2: LOW-PASS FILTERS (fc = 50 Hz)
# ====================================================================
T("Low-Pass Filters", 490, -1300, 0.45, 4)
T("fc = 50 Hz", 490, -1265, 0.3, 8)

# ---- Signal LPF ----
T("Rlpf", 540, -905, 0.25, 8)
T("3.18M", 540, -885, 0.2, 8)
res("R_lpf_sig", 570, -860, "3.18Meg", rot=3)
# P(540,-860) M(600,-860)

N(170, -860, 540, -860, "sq_sig")   # Riso_s output to Rlpf_sig

T("Clpf", 615, -735, 0.25, 8)
T("1nF", 615, -715, 0.2, 8)
cap("C_lpf_sig", 600, -720, "1n")
# p(600,-750) m(600,-690)

N(600, -860, 600, -750, "rms_out")   # Rlpf output to cap top
N(600, -690, 600, GND, "gnd")        # cap bottom to GND

# rms_out output
iopin("p_rms_out", 680, -860, 0, 0, "rms_out")
N(600, -860, 680, -860, "rms_out")

# ---- Reference LPF ----
# Route sq_ref down then right, or keep at same y with offset

# sq_ref exits at (450, -860), route down to y=-560, then to LPF
T("Rlpf", 540, -605, 0.25, 8)
T("3.18M", 540, -585, 0.2, 8)
res("R_lpf_ref", 570, -560, "3.18Meg", rot=3)
# P(540,-560) M(600,-560)

N(450, -860, 450, -560, "sq_ref")    # sq_ref routes down
N(450, -560, 540, -560, "sq_ref")    # then right to Rlpf_ref

T("Clpf", 615, -435, 0.25, 8)
T("1nF", 615, -415, 0.2, 8)
cap("C_lpf_ref", 600, -420, "1n")
# p(600,-450) m(600,-390)

N(600, -560, 600, -450, "rms_ref")   # Rlpf output to cap top
N(600, -390, 600, GND, "gnd")        # cap bottom to GND

# rms_ref output
iopin("p_rms_ref", 680, -560, 0, 0, "rms_ref")
N(600, -560, 680, -560, "rms_ref")

# ====================================================================
# SECTION 3: ACTIVE PEAK DETECTOR
# ====================================================================
T("Active Peak Detector", 820, -1300, 0.45, 4)
T("5-Transistor OTA + Hold", 820, -1265, 0.3, 8)

# ---- PMOS Current Mirror (M3 diode-connected, M4 mirror) ----
T("M3", 870, -1130, 0.3, 8)
T("2/2", 870, -1108, 0.25, 8)
pfet("XM3", 890, -1060, 2, 2)
# G(870,-1060) S(910,-1090) D(910,-1030) B(910,-1060)

T("M4", 1110, -1130, 0.3, 8)
T("2/2", 1110, -1108, 0.25, 8)
pfet("XM4", 1090, -1060, 2, 2, flip=1)
# flip=1: G(1110,-1060) S(1070,-1090) D(1070,-1030) B(1070,-1060)

# M3 source to VDD
N(910, -1090, 910, VDD, "vdd")
# M4 source to VDD
N(1070, -1090, 1070, VDD, "vdd")

# M3 diode-connected: gate to drain
# M3 gate at (870,-1060), M3 drain at (910,-1030)
# Route: drain (910,-1030) left to (870,-1030) up to gate (870,-1060)
N(910, -1030, 870, -1030, "d1_pk")
N(870, -1030, 870, -1060, "d1_pk")

# M4 gate connects to M3 gate (mirror)
# M3 gate at (870,-1060), M4 gate at (1110,-1060)
# Route via a horizontal wire just above the transistors
N(870, -1060, 870, -1160, "pbias_pk")
N(870, -1160, 1110, -1160, "pbias_pk")
N(1110, -1160, 1110, -1060, "pbias_pk")

# ---- NMOS Differential Pair (M1, M2) ----
T("M1", 870, -900, 0.3, 8)
T("4/2", 870, -878, 0.25, 8)
nfet("XM1", 890, -830, 4, 2)
# G(870,-830) D(910,-860) S(910,-800) B(910,-830)

T("M2", 1110, -900, 0.3, 8)
T("4/2", 1110, -878, 0.25, 8)
nfet("XM2", 1090, -830, 4, 2, flip=1)
# flip=1: G(1110,-830) D(1070,-860) S(1070,-800) B(1070,-830)

# M3 drain to M1 drain (d1 node)
N(910, -1030, 910, -860, "d1_pk")

# M4 drain to M2 drain (pk_ota_out)
N(1070, -1030, 1070, -860, "pk_ota_out")

# M1, M2 sources tied → tail
N(910, -800, 910, -770, "tail_pk")
N(1070, -800, 1070, -770, "tail_pk")
N(910, -770, 1070, -770, "tail_pk")

# ---- Tail Transistor (Mt) ----
T("Mt", 960, -710, 0.3, 8)
T("2/4", 960, -688, 0.25, 8)
nfet("XMt", 970, -650, 2, 4)
# G(950,-650) D(990,-680) S(990,-620) B(990,-650)

N(990, -770, 990, -680, "tail_pk")   # tail to Mt drain
N(990, -620, 990, GND, "gnd")        # Mt source to GND

# Mt gate → vbn
labpin("l_vbn_mt", 950, -650, 0, 1, "vbn")

# OTA inputs
labpin("l_inp_pk", 870, -830, 0, 1, "inp")         # M1+ = inp
labpin("l_pk_fb", 1110, -830, 0, 0, "peak_out")     # M2- = peak_out

# ---- Output Stage ----
T("Charge NFET", 1220, -1130, 0.35, 4)
T("XMchrg", 1220, -1070, 0.3, 8)
T("4/0.5", 1220, -1048, 0.25, 8)

# XMchrg: gate=pk_ota_out, drain=VDD, source=peak_out
nfet("XMchrg", 1230, -980, 4, 0.5)
# G(1210,-980) D(1250,-1010) S(1250,-950) B(1250,-980)

N(1250, -1010, 1250, VDD, "vdd")     # XMchrg drain to VDD

# Gate from pk_ota_out
# pk_ota_out is on wire from M4 drain (1070,-1030) down to M2 drain (1070,-860)
# T-branch at (1070,-980) going right to XMchrg gate (1210,-980)
N(1070, -980, 1210, -980, "pk_ota_out")

# XMchrg source → peak_out
N(1250, -950, 1250, -820, "peak_out")

# Hold capacitor
T("Chold", 1290, -735, 0.3, 8)
T("500pF", 1290, -713, 0.25, 8)
cap("C_hold", 1250, -720, "500p")
# p(1250,-750) m(1250,-690)

N(1250, -820, 1250, -750, "peak_out") # peak_out to Chold top
N(1250, -690, 1250, GND, "gnd")       # Chold bottom to GND

# Discharge transistor
T("XMdis", 1365, -575, 0.3, 8)
T("0.42/20", 1365, -553, 0.25, 8)
T("Discharge", 1345, -620, 0.25, 4)
nfet("XMdis", 1360, -500, 0.42, 20)
# G(1340,-500) D(1380,-530) S(1380,-470) B(1380,-500)

N(1380, -530, 1380, -820, "peak_out") # XMdis drain to peak_out
N(1250, -820, 1380, -820, "peak_out") # horizontal link

labpin("l_vcm_dis", 1340, -500, 0, 1, "vcm")   # gate = vcm
N(1380, -470, 1380, -400, "vcm")                 # source to vcm
labpin("l_vcm_dis_s", 1380, -400, 0, 0, "vcm")

# Reset transistor
T("XMrst", 1495, -575, 0.3, 8)
T("1/0.5", 1495, -553, 0.25, 8)
T("Reset", 1490, -620, 0.25, 4)
nfet("XMrst", 1490, -500, 1, 0.5)
# G(1470,-500) D(1510,-530) S(1510,-470) B(1510,-500)

N(1510, -530, 1510, -820, "peak_out") # XMrst drain to peak_out
N(1380, -820, 1510, -820, "peak_out") # horizontal link

labpin("l_reset_g", 1470, -500, 0, 1, "reset")  # gate = reset
N(1510, -470, 1510, -400, "vcm")                  # source to vcm
labpin("l_vcm_rst_s", 1510, -400, 0, 0, "vcm")

# peak_out output
iopin("p_peak_out", 1580, -820, 0, 0, "peak_out")
N(1510, -820, 1580, -820, "peak_out")

# ====================================================================
# I/O PINS
# ====================================================================
iopin("p_vdd", -380, VDD, 0, 1, "vdd")
iopin("p_gnd", -380, GND, 0, 1, "gnd")
iopin("p_inp", -80, -720, 0, 1, "inp")
N(-80, -720, -20, -720, "inp")

iopin("p_vcm", -80, -400, 0, 1, "vcm")
iopin("p_vbn", -80, -500, 0, 1, "vbn")
iopin("p_reset", -80, -350, 0, 1, "reset")

# ====================================================================
# VDD RAIL
# ====================================================================
N(-380, VDD, 20, VDD, "vdd")
N(20, VDD, 300, VDD, "vdd")
N(300, VDD, 910, VDD, "vdd")
N(910, VDD, 1070, VDD, "vdd")
N(1070, VDD, 1250, VDD, "vdd")

# ====================================================================
# GND RAIL
# ====================================================================
N(-380, GND, 20, GND, "gnd")
N(20, GND, 300, GND, "gnd")
N(300, GND, 600, GND, "gnd")
N(600, GND, 990, GND, "gnd")
N(990, GND, 1250, GND, "gnd")
N(1250, GND, 1510, GND, "gnd")

# ====================================================================
# WRITE
# ====================================================================
with open('/home/ubuntu/analog-ai-chips/vibrosense/05_rms_crest/rms_crest.sch', 'w') as f:
    f.write('\n'.join(lines) + '\n')
print("Generated rms_crest.sch")
