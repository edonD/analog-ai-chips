#!/usr/bin/env python3
"""
gen_schematic.py — Generate xschem .sch files for Block 05 UV/OV Comparators.

Pin geometry (all relative to instance origin x,y):
  nmos4: D(+20,-30) G(-20,0) S(+20,+30) B(+20,0)
  pmos4: D(+20,+30) G(-20,0) S(+20,-30) B(+20,0)
  res:   P(0,-30)   M(0,+30)       (P=top, M=bottom)
  gnd:   p(0,0)                     (connect at top)
  lab_pin: pin at (0,0)             (wire connects here)
"""

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def sch_header():
    return (
        "v {xschem version=3.4.4 file_version=1.2\n}\n"
        "G {}\nK {}\nV {}\nS {}\nE {}\n"
    )


def inst(sym, x, y, flip=0, rot=0, props=""):
    return f"C {{{sym}}} {x} {y} {flip} {rot} {{{props}}}\n"


def wire(x1, y1, x2, y2, lab=""):
    if lab:
        return f"N {x1} {y1} {x2} {y2} {{lab={lab}}}\n"
    return f"N {x1} {y1} {x2} {y2} {{}}\n"


def text(x, y, txt, size=0.4, color=4, rot=0):
    return f"T {{{txt}}} {x} {y} {rot} {color} {size} {size} {{}}\n"


def rect(x1, y1, x2, y2, layer=2, dash=5):
    """layer 2 = gray outline, no fill. dash=5 = dashed."""
    return f"B {layer} {x1} {y1} {x2} {y2} {{dash={dash}}}\n"


def nmos(x, y, name, w="2u", l="1u", model="sky130_fd_pr__nfet_01v8"):
    """Returns (instance_str, pin_dict)."""
    s = inst("nmos4.sym", x, y, props=f"name={name} model={model} w={w} l={l} m=1")
    pins = {"d": (x+20, y-30), "g": (x-20, y), "s": (x+20, y+30), "b": (x+20, y)}
    return s, pins


def pmos(x, y, name, w="2u", l="1u", model="sky130_fd_pr__pfet_01v8"):
    s = inst("pmos4.sym", x, y, props=f"name={name} model={model} w={w} l={l} m=1")
    pins = {"d": (x+20, y+30), "g": (x-20, y), "s": (x+20, y-30), "b": (x+20, y)}
    return s, pins


def res(x, y, name, value, rot=0):
    s = inst("res.sym", x, y, rot=rot, props=f"name={name} value={value}")
    if rot == 0:
        pins = {"p": (x, y-30), "m": (x, y+30)}
    elif rot == 1:  # 90° CW
        pins = {"p": (x+30, y), "m": (x-30, y)}
    elif rot == 3:  # 90° CCW
        pins = {"p": (x-30, y), "m": (x+30, y)}
    else:
        pins = {"p": (x, y+30), "m": (x, y-30)}
    return s, pins


def gnd(x, y):
    return inst("gnd.sym", x, y, props="name=l1 lab=GND")


def lab(x, y, name, rot=0):
    """rot=0: label points right, rot=2: label points left."""
    return inst("lab_pin.sym", x, y, rot=rot, props=f"name=p1 sig_type=std_logic lab={name}")


def title_block(x, y):
    return inst("title.sym", x, y, props='name=l1 author="Block 05 UV/OV Comparators"')


# ============================================================
# UV Comparator
# ============================================================
def build_uv():
    out = sch_header()

    # Title
    out += text(100, -750, "UV COMPARATOR", size=0.7, color=4)
    out += text(100, -700, "Block 05 — PVDD Undervoltage Detector", size=0.4, color=8)
    out += text(100, -660, "NMOS diff pair + PMOS mirror | 1.8V supply | Threshold ~4.3V", size=0.35, color=8)

    # ========== SECTION: Resistive Divider ==========
    out += rect(60, -620, 380, 100, layer=2, dash=5)
    out += text(80, -610, "RESISTIVE DIVIDER", size=0.35, color=7)

    # R_top: pvdd → mid_uv
    s, rp = res(200, -450, "R_top", "500k")
    out += s
    # Wire from pvdd (above) to R_top.P
    out += wire(200, -560, 200, rp["p"][1])
    out += lab(120, -560, "pvdd", rot=0)
    out += wire(120, -560, 200, -560)

    # mid_uv node between R_top.M and R_bot.P
    mid_y = -370
    out += wire(rp["m"][0], rp["m"][1], 200, mid_y)

    # R_bot: mid_uv → gnd
    s, rb = res(200, -280, "R_bot", "199.4k")
    out += s
    out += wire(200, mid_y, 200, rb["p"][1])

    # Ground under R_bot
    out += wire(rb["m"][0], rb["m"][1], 200, -210)
    out += gnd(200, -210)

    # mid_uv label
    out += wire(200, mid_y, 350, mid_y)
    out += lab(350, mid_y, "mid_uv", rot=2)

    # ========== SECTION: Hysteresis Feedback ==========
    out += rect(360, -430, 650, -310, layer=2, dash=3)
    out += text(375, -425, "HYSTERESIS FEEDBACK", size=0.25, color=5)
    out += text(375, -400, "R_hyst from out_n", size=0.2, color=5)

    s, rh = res(500, mid_y, "R_hyst", "2.5M", rot=1)
    out += s
    # R_hyst.m (left) connects to mid_uv
    out += wire(rh["m"][0], rh["m"][1], 350, mid_y)
    # R_hyst.p (right) gets label out_n
    out += wire(rh["p"][0], rh["p"][1], 620, mid_y)
    out += lab(620, mid_y, "out_n", rot=2)

    # ========== SECTION: Bias Current ==========
    out += rect(650, -620, 870, 100, layer=2, dash=5)
    out += text(665, -610, "BIAS (~1uA)", size=0.35, color=8)

    # R_bias: vdd_comp → bias_n
    s, rbias = res(750, -480, "R_bias", "800k")
    out += s
    out += wire(750, -560, 750, rbias["p"][1])
    out += lab(680, -560, "vdd_comp", rot=0)
    out += wire(680, -560, 750, -560)

    # XMbias: diode NMOS (D=G=bias_n, S=gnd)
    bias_x, bias_y = 730, -360
    s, mb = nmos(bias_x, bias_y, "XMbias", w="1u", l="4u")
    out += s
    # R_bias.M to drain
    out += wire(rbias["m"][0], rbias["m"][1], mb["d"][0], mb["d"][1])
    # Diode: gate to drain
    out += wire(mb["g"][0], mb["g"][1], mb["g"][0], mb["d"][1])
    out += wire(mb["g"][0], mb["d"][1], mb["d"][0], mb["d"][1])
    # Source to gnd
    out += wire(mb["s"][0], mb["s"][1], mb["s"][0], mb["s"][1]+40)
    out += gnd(mb["s"][0], mb["s"][1]+40)
    # Body to gnd (source)
    out += wire(mb["b"][0], mb["b"][1], mb["b"][0]+20, mb["b"][1])
    out += wire(mb["b"][0]+20, mb["b"][1], mb["b"][0]+20, mb["s"][1]+40)
    # bias_n label
    out += lab(mb["d"][0]+30, mb["d"][1], "bias_n", rot=2)
    out += wire(mb["d"][0], mb["d"][1], mb["d"][0]+30, mb["d"][1])

    # ========== SECTION: Diff Pair + Mirror ==========
    out += rect(880, -620, 1350, 250, layer=2, dash=5)
    out += text(900, -610, "NMOS DIFF PAIR + PMOS MIRROR", size=0.35, color=4)

    # === PMOS Mirror Load (top) ===
    out += text(920, -590, "PMOS current mirror load", size=0.25, color=8)

    # XM3: diode PMOS left (D=out_p, S=vdd_comp)
    m3x, m3y = 980, -470
    s, m3 = pmos(m3x, m3y, "XM3", w="2u", l="1u")
    out += s
    # Source to vdd_comp
    out += wire(m3["s"][0], m3["s"][1], m3["s"][0], m3["s"][1]-30)
    out += lab(m3["s"][0]+10, m3["s"][1]-30, "vdd_comp", rot=2)
    # Body to vdd (same as source)
    out += wire(m3["b"][0], m3["b"][1], m3["b"][0]+20, m3["b"][1])
    out += wire(m3["b"][0]+20, m3["b"][1], m3["s"][0], m3["s"][1]-30)
    # Diode: gate to drain
    out += wire(m3["g"][0], m3["g"][1], m3["g"][0]-20, m3["g"][1])
    out += wire(m3["g"][0]-20, m3["g"][1], m3["g"][0]-20, m3["d"][1])
    out += wire(m3["g"][0]-20, m3["d"][1], m3["d"][0], m3["d"][1])
    # out_p label at drain
    out += lab(m3["d"][0]+10, m3["d"][1], "out_p", rot=2)

    # XM4: mirror PMOS right (D=out_n, S=vdd_comp)
    m4x, m4y = 1200, -470
    s, m4 = pmos(m4x, m4y, "XM4", w="2u", l="1u")
    out += s
    out += wire(m4["s"][0], m4["s"][1], m4["s"][0], m4["s"][1]-30)
    out += lab(m4["s"][0]+10, m4["s"][1]-30, "vdd_comp", rot=2)
    out += wire(m4["b"][0], m4["b"][1], m4["b"][0]+20, m4["b"][1])
    out += wire(m4["b"][0]+20, m4["b"][1], m4["s"][0], m4["s"][1]-30)
    # Gate from M3 gate (mirror connection)
    out += wire(m4["g"][0], m4["g"][1], m3["g"][0]-20, m4["g"][1])
    out += wire(m3["g"][0]-20, m4["g"][1], m3["g"][0]-20, m3["g"][1])
    # out_n at drain
    out += lab(m4["d"][0]+10, m4["d"][1], "out_n", rot=2)

    # === NMOS Diff Pair (middle) ===
    out += text(920, -380, "NMOS differential pair", size=0.25, color=8)

    # XM1: left (D=out_p, G=mid_uv, S=tail)
    m1x, m1y = 980, -290
    s, m1 = nmos(m1x, m1y, "XM1", w="2u", l="1u")
    out += s
    # Drain to out_p (up to M3 drain)
    out += wire(m1["d"][0], m1["d"][1], m3["d"][0], m3["d"][1])
    # Gate from mid_uv
    out += lab(m1["g"][0]-30, m1["g"][1], "mid_uv", rot=0)
    out += wire(m1["g"][0]-30, m1["g"][1], m1["g"][0], m1["g"][1])
    # Source down to tail
    out += wire(m1["s"][0], m1["s"][1], m1["s"][0], m1["s"][1]+30)
    # Body to gnd
    out += wire(m1["b"][0], m1["b"][1], m1["b"][0]+20, m1["b"][1])
    out += wire(m1["b"][0]+20, m1["b"][1], m1["b"][0]+20, m1["s"][1]+70)

    # XM2: right (D=out_n, G=vref, S=tail)
    m2x, m2y = 1200, -290
    s, m2 = nmos(m2x, m2y, "XM2", w="2u", l="1u")
    out += s
    # Drain to out_n (up to M4 drain)
    out += wire(m2["d"][0], m2["d"][1], m4["d"][0], m4["d"][1])
    # Gate from vref
    out += lab(m2["g"][0]-30, m2["g"][1], "vref", rot=0)
    out += wire(m2["g"][0]-30, m2["g"][1], m2["g"][0], m2["g"][1])
    # Source down to tail
    out += wire(m2["s"][0], m2["s"][1], m2["s"][0], m2["s"][1]+30)
    # Body to gnd
    out += wire(m2["b"][0], m2["b"][1], m2["b"][0]+20, m2["b"][1])
    out += wire(m2["b"][0]+20, m2["b"][1], m2["b"][0]+20, m2["s"][1]+70)

    # Connect sources (tail node)
    tail_y = m1["s"][1] + 30
    out += wire(m1["s"][0], tail_y, m2["s"][0], tail_y)
    tail_mid_x = (m1["s"][0] + m2["s"][0]) // 2
    out += wire(tail_mid_x, tail_y, tail_mid_x, tail_y + 30)
    out += lab(tail_mid_x, tail_y, "tail", rot=0)

    # === Tail Current Source ===
    out += text(1040, -160, "Tail current", size=0.25, color=8)
    tailx, taily = tail_mid_x - 20, -120
    s, mt = nmos(tailx, taily, "XMtail", w="1u", l="4u")
    out += s
    # Drain up to tail
    out += wire(mt["d"][0], mt["d"][1], tail_mid_x, tail_y + 30)
    # Gate from bias_n
    out += lab(mt["g"][0]-30, mt["g"][1], "bias_n", rot=0)
    out += wire(mt["g"][0]-30, mt["g"][1], mt["g"][0], mt["g"][1])
    # Source to gnd
    out += wire(mt["s"][0], mt["s"][1], mt["s"][0], mt["s"][1]+30)
    out += gnd(mt["s"][0], mt["s"][1]+30)
    # Body to gnd
    out += wire(mt["b"][0], mt["b"][1], mt["b"][0]+20, mt["b"][1])
    out += wire(mt["b"][0]+20, mt["b"][1], mt["s"][0], mt["s"][1]+30)

    # ========== SECTION: Enable + NOR Output ==========
    out += rect(1370, -620, 1780, 250, layer=2, dash=5)
    out += text(1390, -610, "ENABLE + NOR OUTPUT", size=0.35, color=6)

    # Enable inverter
    out += text(1390, -580, "en inverter", size=0.25, color=8)
    enx = 1450
    # NMOS
    s, en_n = nmos(enx, -450, "XMen_n", w="0.42u", l="0.15u")
    out += s
    # PMOS
    s, en_p = pmos(enx, -530, "XMen_p", w="0.84u", l="0.15u")
    out += s
    # Connect gates
    out += wire(en_n["g"][0], en_n["g"][1], en_n["g"][0]-30, en_n["g"][1])
    out += wire(en_p["g"][0], en_p["g"][1], en_p["g"][0]-30, en_p["g"][1])
    out += wire(en_n["g"][0]-30, en_n["g"][1], en_p["g"][0]-30, en_p["g"][1])
    out += lab(en_n["g"][0]-60, -490, "en", rot=0)
    out += wire(en_n["g"][0]-60, -490, en_n["g"][0]-30, -490)
    # Connect drains (output = en_bar)
    out += wire(en_n["d"][0], en_n["d"][1], en_p["d"][0], en_p["d"][1])
    enbar_y = (en_n["d"][1] + en_p["d"][1]) // 2
    out += lab(en_n["d"][0]+40, enbar_y, "en_bar", rot=2)
    out += wire(en_n["d"][0], enbar_y, en_n["d"][0]+40, enbar_y)
    # PMOS source to vdd
    out += wire(en_p["s"][0], en_p["s"][1], en_p["s"][0], en_p["s"][1]-20)
    out += lab(en_p["s"][0]+10, en_p["s"][1]-20, "vdd_comp", rot=2)
    # PMOS body to vdd
    out += wire(en_p["b"][0], en_p["b"][1], en_p["b"][0]+20, en_p["b"][1])
    out += wire(en_p["b"][0]+20, en_p["b"][1], en_p["s"][0], en_p["s"][1]-20)
    # NMOS source to gnd
    out += wire(en_n["s"][0], en_n["s"][1], en_n["s"][0], en_n["s"][1]+20)
    out += gnd(en_n["s"][0], en_n["s"][1]+20)
    # NMOS body to gnd
    out += wire(en_n["b"][0], en_n["b"][1], en_n["b"][0]+20, en_n["b"][1])
    out += wire(en_n["b"][0]+20, en_n["b"][1], en_n["s"][0], en_n["s"][1]+20)

    # NOR gate: uv_flag = NOR(out_n, en_bar)
    out += text(1550, -400, "NOR(out_n, en_bar)", size=0.25, color=6)

    # PMOS series stack
    s, np1 = pmos(1630, -340, "XMnor_p1", w="4u", l="0.15u")
    out += s
    out += wire(np1["g"][0], np1["g"][1], np1["g"][0]-30, np1["g"][1])
    out += lab(np1["g"][0]-30, np1["g"][1], "out_n", rot=0)
    out += wire(np1["s"][0], np1["s"][1], np1["s"][0], np1["s"][1]-20)
    out += lab(np1["s"][0]+10, np1["s"][1]-20, "vdd_comp", rot=2)
    out += wire(np1["b"][0], np1["b"][1], np1["b"][0]+20, np1["b"][1])
    out += wire(np1["b"][0]+20, np1["b"][1], np1["s"][0], np1["s"][1]-20)

    s, np2 = pmos(1630, -250, "XMnor_p2", w="4u", l="0.15u")
    out += s
    out += wire(np2["g"][0], np2["g"][1], np2["g"][0]-30, np2["g"][1])
    out += lab(np2["g"][0]-30, np2["g"][1], "en_bar", rot=0)
    # Connect np1.D to np2.S (series)
    out += wire(np1["d"][0], np1["d"][1], np2["s"][0], np2["s"][1])
    out += wire(np2["b"][0], np2["b"][1], np1["d"][0], np1["d"][1])

    # np2.D = output node
    out_nor_y = np2["d"][1]
    out += wire(np2["d"][0], np2["d"][1], np2["d"][0], np2["d"][1]+20)

    # NMOS parallel
    s, nn1 = nmos(1580, -120, "XMnor_n1", w="1u", l="0.15u")
    out += s
    out += wire(nn1["g"][0], nn1["g"][1], nn1["g"][0]-30, nn1["g"][1])
    out += lab(nn1["g"][0]-30, nn1["g"][1], "out_n", rot=0)
    out += wire(nn1["s"][0], nn1["s"][1], nn1["s"][0], nn1["s"][1]+20)
    out += gnd(nn1["s"][0], nn1["s"][1]+20)
    out += wire(nn1["b"][0], nn1["b"][1], nn1["b"][0]+20, nn1["b"][1])
    out += wire(nn1["b"][0]+20, nn1["b"][1], nn1["s"][0], nn1["s"][1]+20)

    s, nn2 = nmos(1700, -120, "XMnor_n2", w="1u", l="0.15u")
    out += s
    out += wire(nn2["g"][0], nn2["g"][1], nn2["g"][0]-30, nn2["g"][1])
    out += lab(nn2["g"][0]-30, nn2["g"][1], "en_bar", rot=0)
    out += wire(nn2["s"][0], nn2["s"][1], nn2["s"][0], nn2["s"][1]+20)
    out += gnd(nn2["s"][0], nn2["s"][1]+20)
    out += wire(nn2["b"][0], nn2["b"][1], nn2["b"][0]+20, nn2["b"][1])
    out += wire(nn2["b"][0]+20, nn2["b"][1], nn2["s"][0], nn2["s"][1]+20)

    # Connect NMOS drains and PMOS drain to output
    flag_y = -180
    out += wire(nn1["d"][0], nn1["d"][1], nn1["d"][0], flag_y)
    out += wire(nn2["d"][0], nn2["d"][1], nn2["d"][0], flag_y)
    out += wire(nn1["d"][0], flag_y, nn2["d"][0], flag_y)
    nor_out_x = (nn1["d"][0] + nn2["d"][0]) // 2
    out += wire(nor_out_x, flag_y, np2["d"][0], np2["d"][1]+20)

    # Output label
    out += wire(nn2["d"][0], flag_y, 1780, flag_y)
    out += lab(1780, flag_y, "uv_flag", rot=2)

    # Title block
    out += title_block(100, 400)

    return out


# ============================================================
# OV Comparator (same topology, different values + swapped inputs)
# ============================================================
def build_ov():
    out = sch_header()

    out += text(100, -750, "OV COMPARATOR", size=0.7, color=6)
    out += text(100, -700, "Block 05 — PVDD Overvoltage Detector", size=0.4, color=8)
    out += text(100, -660, "NMOS diff pair + PMOS mirror | 1.8V supply | Threshold ~5.5V", size=0.35, color=8)
    out += text(100, -630, "NOTE: Diff pair inputs SWAPPED vs UV (M1=vref, M2=mid_ov)", size=0.3, color=5)

    # Divider
    out += rect(60, -620, 380, 100, layer=2, dash=5)
    out += text(80, -610, "RESISTIVE DIVIDER", size=0.35, color=7)

    s, rp = res(200, -450, "R_top", "500k")
    out += s
    out += wire(200, -560, 200, rp["p"][1])
    out += lab(120, -560, "pvdd", rot=0)
    out += wire(120, -560, 200, -560)

    mid_y = -370
    out += wire(rp["m"][0], rp["m"][1], 200, mid_y)

    s, rb = res(200, -280, "R_bot", "146k")
    out += s
    out += wire(200, mid_y, 200, rb["p"][1])
    out += wire(rb["m"][0], rb["m"][1], 200, -210)
    out += gnd(200, -210)
    out += wire(200, mid_y, 350, mid_y)
    out += lab(350, mid_y, "mid_ov", rot=2)

    # Hysteresis: ov_flag → mid_ov
    out += rect(360, -430, 650, -310, layer=2, dash=3)
    out += text(375, -425, "HYSTERESIS FEEDBACK", size=0.25, color=5)
    out += text(375, -400, "R_hyst from ov_flag", size=0.2, color=5)

    s, rh = res(500, mid_y, "R_hyst", "8M", rot=1)
    out += s
    out += wire(rh["m"][0], rh["m"][1], 350, mid_y)
    out += wire(rh["p"][0], rh["p"][1], 620, mid_y)
    out += lab(620, mid_y, "ov_flag", rot=2)

    # Bias
    out += rect(650, -620, 870, 100, layer=2, dash=5)
    out += text(665, -610, "BIAS (~1uA)", size=0.35, color=8)

    s, rbias = res(750, -480, "R_bias", "800k")
    out += s
    out += wire(750, -560, 750, rbias["p"][1])
    out += lab(680, -560, "vdd_comp", rot=0)
    out += wire(680, -560, 750, -560)

    bias_x, bias_y = 730, -360
    s, mb = nmos(bias_x, bias_y, "XMbias", w="1u", l="4u")
    out += s
    out += wire(rbias["m"][0], rbias["m"][1], mb["d"][0], mb["d"][1])
    out += wire(mb["g"][0], mb["g"][1], mb["g"][0], mb["d"][1])
    out += wire(mb["g"][0], mb["d"][1], mb["d"][0], mb["d"][1])
    out += wire(mb["s"][0], mb["s"][1], mb["s"][0], mb["s"][1]+40)
    out += gnd(mb["s"][0], mb["s"][1]+40)
    out += wire(mb["b"][0], mb["b"][1], mb["b"][0]+20, mb["b"][1])
    out += wire(mb["b"][0]+20, mb["b"][1], mb["s"][0], mb["s"][1]+40)
    out += lab(mb["d"][0]+30, mb["d"][1], "bias_n", rot=2)
    out += wire(mb["d"][0], mb["d"][1], mb["d"][0]+30, mb["d"][1])

    # Diff pair + mirror
    out += rect(880, -620, 1350, 250, layer=2, dash=5)
    out += text(900, -610, "NMOS DIFF PAIR + PMOS MIRROR", size=0.35, color=4)

    # PMOS Mirror (same as UV)
    out += text(920, -590, "PMOS current mirror load", size=0.25, color=8)

    m3x, m3y = 980, -470
    s, m3 = pmos(m3x, m3y, "XM3", w="2u", l="1u")
    out += s
    out += wire(m3["s"][0], m3["s"][1], m3["s"][0], m3["s"][1]-30)
    out += lab(m3["s"][0]+10, m3["s"][1]-30, "vdd_comp", rot=2)
    out += wire(m3["b"][0], m3["b"][1], m3["b"][0]+20, m3["b"][1])
    out += wire(m3["b"][0]+20, m3["b"][1], m3["s"][0], m3["s"][1]-30)
    out += wire(m3["g"][0], m3["g"][1], m3["g"][0]-20, m3["g"][1])
    out += wire(m3["g"][0]-20, m3["g"][1], m3["g"][0]-20, m3["d"][1])
    out += wire(m3["g"][0]-20, m3["d"][1], m3["d"][0], m3["d"][1])
    out += lab(m3["d"][0]+10, m3["d"][1], "out_p", rot=2)

    m4x, m4y = 1200, -470
    s, m4 = pmos(m4x, m4y, "XM4", w="2u", l="1u")
    out += s
    out += wire(m4["s"][0], m4["s"][1], m4["s"][0], m4["s"][1]-30)
    out += lab(m4["s"][0]+10, m4["s"][1]-30, "vdd_comp", rot=2)
    out += wire(m4["b"][0], m4["b"][1], m4["b"][0]+20, m4["b"][1])
    out += wire(m4["b"][0]+20, m4["b"][1], m4["s"][0], m4["s"][1]-30)
    out += wire(m4["g"][0], m4["g"][1], m3["g"][0]-20, m4["g"][1])
    out += wire(m3["g"][0]-20, m4["g"][1], m3["g"][0]-20, m3["g"][1])
    out += lab(m4["d"][0]+10, m4["d"][1], "out_n", rot=2)

    # NMOS diff pair — INPUTS SWAPPED: M1=vref, M2=mid_ov
    out += text(920, -380, "NMOS diff pair (M1=vref, M2=mid_ov)", size=0.25, color=5)

    m1x, m1y = 980, -290
    s, m1 = nmos(m1x, m1y, "XM1", w="2u", l="1u")
    out += s
    out += wire(m1["d"][0], m1["d"][1], m3["d"][0], m3["d"][1])
    out += lab(m1["g"][0]-30, m1["g"][1], "vref", rot=0)  # SWAPPED
    out += wire(m1["g"][0]-30, m1["g"][1], m1["g"][0], m1["g"][1])
    out += wire(m1["s"][0], m1["s"][1], m1["s"][0], m1["s"][1]+30)
    out += wire(m1["b"][0], m1["b"][1], m1["b"][0]+20, m1["b"][1])
    out += wire(m1["b"][0]+20, m1["b"][1], m1["b"][0]+20, m1["s"][1]+70)

    m2x, m2y = 1200, -290
    s, m2 = nmos(m2x, m2y, "XM2", w="2u", l="1u")
    out += s
    out += wire(m2["d"][0], m2["d"][1], m4["d"][0], m4["d"][1])
    out += lab(m2["g"][0]-30, m2["g"][1], "mid_ov", rot=0)  # SWAPPED
    out += wire(m2["g"][0]-30, m2["g"][1], m2["g"][0], m2["g"][1])
    out += wire(m2["s"][0], m2["s"][1], m2["s"][0], m2["s"][1]+30)
    out += wire(m2["b"][0], m2["b"][1], m2["b"][0]+20, m2["b"][1])
    out += wire(m2["b"][0]+20, m2["b"][1], m2["b"][0]+20, m2["s"][1]+70)

    tail_y = m1["s"][1] + 30
    out += wire(m1["s"][0], tail_y, m2["s"][0], tail_y)
    tail_mid_x = (m1["s"][0] + m2["s"][0]) // 2
    out += wire(tail_mid_x, tail_y, tail_mid_x, tail_y + 30)
    out += lab(tail_mid_x, tail_y, "tail", rot=0)

    # Tail
    tailx, taily = tail_mid_x - 20, -120
    s, mt = nmos(tailx, taily, "XMtail", w="1u", l="4u")
    out += s
    out += wire(mt["d"][0], mt["d"][1], tail_mid_x, tail_y + 30)
    out += lab(mt["g"][0]-30, mt["g"][1], "bias_n", rot=0)
    out += wire(mt["g"][0]-30, mt["g"][1], mt["g"][0], mt["g"][1])
    out += wire(mt["s"][0], mt["s"][1], mt["s"][0], mt["s"][1]+30)
    out += gnd(mt["s"][0], mt["s"][1]+30)
    out += wire(mt["b"][0], mt["b"][1], mt["b"][0]+20, mt["b"][1])
    out += wire(mt["b"][0]+20, mt["b"][1], mt["s"][0], mt["s"][1]+30)

    # Enable + NOR (identical to UV)
    out += rect(1370, -620, 1780, 250, layer=2, dash=5)
    out += text(1390, -610, "ENABLE + NOR OUTPUT", size=0.35, color=6)

    enx = 1450
    s, en_n = nmos(enx, -450, "XMen_n", w="0.42u", l="0.15u")
    out += s
    s, en_p = pmos(enx, -530, "XMen_p", w="0.84u", l="0.15u")
    out += s
    out += wire(en_n["g"][0], en_n["g"][1], en_n["g"][0]-30, en_n["g"][1])
    out += wire(en_p["g"][0], en_p["g"][1], en_p["g"][0]-30, en_p["g"][1])
    out += wire(en_n["g"][0]-30, en_n["g"][1], en_p["g"][0]-30, en_p["g"][1])
    out += lab(en_n["g"][0]-60, -490, "en", rot=0)
    out += wire(en_n["g"][0]-60, -490, en_n["g"][0]-30, -490)
    out += wire(en_n["d"][0], en_n["d"][1], en_p["d"][0], en_p["d"][1])
    enbar_y = (en_n["d"][1] + en_p["d"][1]) // 2
    out += lab(en_n["d"][0]+40, enbar_y, "en_bar", rot=2)
    out += wire(en_n["d"][0], enbar_y, en_n["d"][0]+40, enbar_y)
    out += wire(en_p["s"][0], en_p["s"][1], en_p["s"][0], en_p["s"][1]-20)
    out += lab(en_p["s"][0]+10, en_p["s"][1]-20, "vdd_comp", rot=2)
    out += wire(en_p["b"][0], en_p["b"][1], en_p["b"][0]+20, en_p["b"][1])
    out += wire(en_p["b"][0]+20, en_p["b"][1], en_p["s"][0], en_p["s"][1]-20)
    out += wire(en_n["s"][0], en_n["s"][1], en_n["s"][0], en_n["s"][1]+20)
    out += gnd(en_n["s"][0], en_n["s"][1]+20)
    out += wire(en_n["b"][0], en_n["b"][1], en_n["b"][0]+20, en_n["b"][1])
    out += wire(en_n["b"][0]+20, en_n["b"][1], en_n["s"][0], en_n["s"][1]+20)

    # NOR
    out += text(1550, -400, "NOR(out_n, en_bar)", size=0.25, color=6)

    s, np1 = pmos(1630, -340, "XMnor_p1", w="4u", l="0.15u")
    out += s
    out += wire(np1["g"][0], np1["g"][1], np1["g"][0]-30, np1["g"][1])
    out += lab(np1["g"][0]-30, np1["g"][1], "out_n", rot=0)
    out += wire(np1["s"][0], np1["s"][1], np1["s"][0], np1["s"][1]-20)
    out += lab(np1["s"][0]+10, np1["s"][1]-20, "vdd_comp", rot=2)
    out += wire(np1["b"][0], np1["b"][1], np1["b"][0]+20, np1["b"][1])
    out += wire(np1["b"][0]+20, np1["b"][1], np1["s"][0], np1["s"][1]-20)

    s, np2 = pmos(1630, -250, "XMnor_p2", w="4u", l="0.15u")
    out += s
    out += wire(np2["g"][0], np2["g"][1], np2["g"][0]-30, np2["g"][1])
    out += lab(np2["g"][0]-30, np2["g"][1], "en_bar", rot=0)
    out += wire(np1["d"][0], np1["d"][1], np2["s"][0], np2["s"][1])
    out += wire(np2["b"][0], np2["b"][1], np1["d"][0], np1["d"][1])
    out += wire(np2["d"][0], np2["d"][1], np2["d"][0], np2["d"][1]+20)

    s, nn1 = nmos(1580, -120, "XMnor_n1", w="1u", l="0.15u")
    out += s
    out += wire(nn1["g"][0], nn1["g"][1], nn1["g"][0]-30, nn1["g"][1])
    out += lab(nn1["g"][0]-30, nn1["g"][1], "out_n", rot=0)
    out += wire(nn1["s"][0], nn1["s"][1], nn1["s"][0], nn1["s"][1]+20)
    out += gnd(nn1["s"][0], nn1["s"][1]+20)
    out += wire(nn1["b"][0], nn1["b"][1], nn1["b"][0]+20, nn1["b"][1])
    out += wire(nn1["b"][0]+20, nn1["b"][1], nn1["s"][0], nn1["s"][1]+20)

    s, nn2 = nmos(1700, -120, "XMnor_n2", w="1u", l="0.15u")
    out += s
    out += wire(nn2["g"][0], nn2["g"][1], nn2["g"][0]-30, nn2["g"][1])
    out += lab(nn2["g"][0]-30, nn2["g"][1], "en_bar", rot=0)
    out += wire(nn2["s"][0], nn2["s"][1], nn2["s"][0], nn2["s"][1]+20)
    out += gnd(nn2["s"][0], nn2["s"][1]+20)
    out += wire(nn2["b"][0], nn2["b"][1], nn2["b"][0]+20, nn2["b"][1])
    out += wire(nn2["b"][0]+20, nn2["b"][1], nn2["s"][0], nn2["s"][1]+20)

    flag_y = -180
    out += wire(nn1["d"][0], nn1["d"][1], nn1["d"][0], flag_y)
    out += wire(nn2["d"][0], nn2["d"][1], nn2["d"][0], flag_y)
    out += wire(nn1["d"][0], flag_y, nn2["d"][0], flag_y)
    nor_out_x = (nn1["d"][0] + nn2["d"][0]) // 2
    out += wire(nor_out_x, flag_y, np2["d"][0], np2["d"][1]+20)
    out += wire(nn2["d"][0], flag_y, 1780, flag_y)
    out += lab(1780, flag_y, "ov_flag", rot=2)

    out += title_block(100, 400)
    return out


if __name__ == '__main__':
    with open('uv_comparator.sch', 'w') as f:
        f.write(build_uv())
    print("Generated uv_comparator.sch")

    with open('ov_comparator.sch', 'w') as f:
        f.write(build_ov())
    print("Generated ov_comparator.sch")
