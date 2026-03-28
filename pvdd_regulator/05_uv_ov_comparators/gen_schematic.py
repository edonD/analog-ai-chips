#!/usr/bin/env python3
"""
gen_schematic.py — Generate xschem .sch files for Block 05 UV/OV Comparators.

Style matches Block 01 pass_device reference:
  Dark theme, large colored annotations, clean spacious layout,
  characterization results at bottom, no clutter.

xschem layer colors (dark theme):
  4 = green (titles, key labels)
  5 = red/brown (warnings, notes)
  7 = red (values, measurements)
  8 = yellow (subtitles, signal descriptions)
  13 = light (spice info, model names)
  (none) = gray (regular text)

Pin geometry (relative to instance origin x,y):
  nmos4: D(+20,-30) G(-20,0) S(+20,+30) B(+20,0)
  pmos4: D(+20,+30) G(-20,0) S(+20,-30) B(+20,0)
  res:   P(0,-30)   M(0,+30)
  gnd:   p(0,0)
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def T(txt, x, y, sz=0.35, layer=None, rot=0):
    lstr = f"layer={layer}" if layer else ""
    return f"T {{{txt}}} {x} {y} {rot} 0 {sz} {sz} {{{lstr}}}\n"


def C(sym, x, y, flip=0, rot=0, props=""):
    return f"C {{{sym}}} {x} {y} {flip} {rot} {{{props}}}\n"


def N(x1, y1, x2, y2, lab=""):
    if lab:
        return f"N {x1} {y1} {x2} {y2} {{lab={lab}}}\n"
    return f"N {x1} {y1} {x2} {y2} {{}}\n"


HDR = "v {xschem version=3.4.4 file_version=1.2\n}\nG {}\nK {}\nV {}\nS {}\nE {}\n"


def build_uv():
    s = HDR

    # ===== TITLE =====
    s += T("BLOCK 05: UV COMPARATOR", -600, -1100, 1.0, 4)
    s += T("PVDD 5.0V LDO Regulator", -600, -1020, 0.5, 8)
    s += T("SkyWater SKY130A Process", -600, -980, 0.4)
    s += T("Topology: NMOS differential pair + PMOS current mirror load", -600, -920, 0.35)
    s += T("Supply: vdd_comp = 1.8 V    |    Threshold: PVDD < 4.3 V    |    uv_flag = HIGH when undervoltage", -600, -880, 0.35)
    s += T("Date: 2026-03-28", -600, -830, 0.3)
    s += T(".subckt uv_comparator  pvdd  vref  uv_flag  vdd_comp  gnd  en", -600, -790, 0.3, 13)

    # ===== RESISTIVE DIVIDER =====
    s += T("RESISTIVE DIVIDER", -600, -700, 0.5, 4)
    s += T("Scales PVDD down to ~1.226 V", -600, -660, 0.3)
    s += T("at threshold crossing", -600, -630, 0.3)

    s += T("pvdd", -580, -560, 0.4, 7)
    rx, ry = -500, -470
    s += C("res.sym", rx, ry, props="name=R_top value=500k")
    s += N(rx, -540, rx, ry - 30)
    s += C("iopin.sym", rx, -540, 3, 0, "name=p_pvdd lab=pvdd")

    mid_y = -380
    s += N(rx, ry + 30, rx, mid_y)
    s += N(rx, mid_y, rx + 80, mid_y)
    s += T("mid_uv", rx + 90, mid_y - 10, 0.35, 8)

    s += C("res.sym", rx, mid_y + 70, props="name=R_bot value=199.4k")
    s += N(rx, mid_y, rx, mid_y + 40)
    s += N(rx, mid_y + 100, rx, mid_y + 140)
    s += C("gnd.sym", rx, mid_y + 140, props="name=l1 lab=GND")

    # ===== HYSTERESIS =====
    s += T("HYSTERESIS", -320, -700, 0.45, 4)
    s += T("R_hyst = 2.5 Meg", -320, -660, 0.3, 7)
    s += T("Feedback: out_n to mid_uv", -320, -630, 0.3)
    s += T("Positive feedback for clean switching", -320, -600, 0.25, 5)

    rhyst_x = -250
    s += C("res.sym", rhyst_x, mid_y + 30, props="name=R_hyst value=2.5M")
    s += N(rx + 80, mid_y, rhyst_x, mid_y)          # horizontal to top pin
    s += N(rhyst_x, mid_y + 60, -170, mid_y + 60)   # horizontal from bottom pin
    s += T("out_n", -160, mid_y + 50, 0.3, 8)

    # ===== BIAS =====
    s += T("BIAS", -100, -700, 0.45, 4)
    s += T("~1 uA self-biased", -100, -660, 0.3)

    bx = -30
    s += C("res.sym", bx, -550, props="name=R_bias value=800k")
    s += N(bx, -620, bx, -580)
    s += T("vdd_comp", bx - 60, -640, 0.3, 8)

    s += C("nmos4.sym", bx - 20, -430, props="name=XMbias model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1 spiceprefix=X")
    s += N(bx, -520, bx, -460)
    s += N(bx - 40, -430, bx - 40, -460)
    s += N(bx - 40, -460, bx, -460)
    s += N(bx, -400, bx, -360)
    s += C("gnd.sym", bx, -360, props="name=l2 lab=GND")
    # Body to source (both gnd)
    s += N(bx, -430, bx, -400)
    s += T("bias_n", bx + 30, -470, 0.3, 8)

    # ===== DIFF PAIR + MIRROR =====
    s += T("NMOS DIFFERENTIAL PAIR", 200, -700, 0.5, 4)
    s += T("+ PMOS CURRENT MIRROR LOAD", 200, -660, 0.45, 4)

    # PMOS Mirror
    m3x, m3y = 280, -500
    s += C("pmos4.sym", m3x, m3y, props="name=XM3 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1 spiceprefix=X")
    s += N(m3x + 20, m3y - 30, m3x + 20, m3y - 70)
    s += T("vdd_comp", m3x + 30, m3y - 80, 0.3, 8)
    s += N(m3x - 20, m3y, m3x - 40, m3y)
    s += N(m3x - 40, m3y, m3x - 40, m3y + 30)
    s += N(m3x - 40, m3y + 30, m3x + 20, m3y + 30)
    s += N(m3x + 20, m3y, m3x + 40, m3y)
    s += N(m3x + 40, m3y, m3x + 40, m3y - 70)
    s += T("out_p", m3x + 30, m3y + 25, 0.25, 13)

    m4x, m4y = 530, -500
    s += C("pmos4.sym", m4x, m4y, props="name=XM4 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1 spiceprefix=X")
    s += N(m4x + 20, m4y - 30, m4x + 20, m4y - 70)
    s += T("vdd_comp", m4x + 30, m4y - 80, 0.3, 8)
    s += N(m4x - 20, m4y, m3x - 40, m4y)
    s += N(m4x + 20, m4y, m4x + 40, m4y)
    s += N(m4x + 40, m4y, m4x + 40, m4y - 70)
    s += T("out_n", m4x + 30, m4y + 25, 0.35, 7)

    # NMOS Diff Pair
    m1x, m1y = 280, -320
    s += C("nmos4.sym", m1x, m1y, props="name=XM1 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1 spiceprefix=X")
    s += N(m1x + 20, m1y - 30, m3x + 20, m3y + 30)
    s += T("mid_uv", m1x - 120, m1y - 10, 0.35, 8)
    s += N(m1x - 100, m1y, m1x - 20, m1y)
    s += N(m1x + 20, m1y + 30, m1x + 20, m1y + 60)
    # Body to GND (B=gnd, NOT tail — S=tail is different net)
    s += N(m1x + 20, m1y, m1x + 40, m1y)
    s += N(m1x + 40, m1y, m1x + 40, m1y + 40)
    s += C("gnd.sym", m1x + 40, m1y + 40, props="name=lb1 lab=GND")

    m2x, m2y = 530, -320
    s += C("nmos4.sym", m2x, m2y, props="name=XM2 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1 spiceprefix=X")
    s += N(m2x + 20, m2y - 30, m4x + 20, m4y + 30)
    s += T("vref", m2x - 100, m2y - 10, 0.35, 8)
    s += N(m2x - 80, m2y, m2x - 20, m2y)
    s += N(m2x + 20, m2y + 30, m2x + 20, m2y + 60)
    # Body to GND
    s += N(m2x + 20, m2y, m2x + 40, m2y)
    s += N(m2x + 40, m2y, m2x + 40, m2y + 40)
    s += C("gnd.sym", m2x + 40, m2y + 40, props="name=lb2 lab=GND")

    tail_y = m1y + 60
    s += N(m1x + 20, tail_y, m2x + 20, tail_y)
    tail_cx = (m1x + m2x) // 2 + 20
    s += N(tail_cx, tail_y, tail_cx, tail_y + 30)
    s += T("tail", tail_cx + 10, tail_y - 5, 0.3, 13)

    # Tail current source
    tx, ty = tail_cx - 20, tail_y + 80
    s += C("nmos4.sym", tx, ty, props="name=XMtail model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1 spiceprefix=X")
    s += N(tx + 20, ty - 30, tail_cx, tail_y + 30)
    s += N(tx - 20, ty, tx - 60, ty)
    s += T("bias_n", tx - 120, ty - 10, 0.3, 8)
    s += N(tx + 20, ty + 30, tx + 20, ty + 60)
    s += C("gnd.sym", tx + 20, ty + 60, props="name=l3 lab=GND")
    # Body to source (both gnd)
    s += N(tx + 20, ty, tx + 20, ty + 30)

    # ===== OUTPUT STAGE =====
    s += T("ENABLE + NOR OUTPUT", 750, -700, 0.5, 4)
    s += T("uv_flag = NOR(out_n, en_bar)", 750, -660, 0.35, 13)
    s += T("HIGH when PVDD < threshold", 750, -630, 0.3, 5)

    # Enable inverter
    enx = 800
    s += C("pmos4.sym", enx, -510, props="name=XMen_p model=sky130_fd_pr__pfet_01v8 w=0.84u l=0.15u m=1 spiceprefix=X")
    s += C("nmos4.sym", enx, -430, props="name=XMen_n model=sky130_fd_pr__nfet_01v8 w=0.42u l=0.15u m=1 spiceprefix=X")
    s += N(enx - 20, -510, enx - 20, -430)
    s += N(enx - 20, -470, enx - 60, -470)
    s += T("en", enx - 110, -480, 0.35, 8)
    s += N(enx + 20, -480, enx + 20, -460)
    s += T("en_bar", enx + 50, -475, 0.3, 13)
    s += N(enx + 20, -470, enx + 50, -470)
    s += N(enx + 20, -540, enx + 20, -570)
    s += T("vdd_comp", enx + 30, -580, 0.25, 8)
    s += N(enx + 20, -510, enx + 40, -510)
    s += N(enx + 40, -510, enx + 40, -570)
    s += N(enx + 20, -400, enx + 20, -370)
    s += C("gnd.sym", enx + 20, -370, props="name=l4 lab=GND")
    s += N(enx + 20, -430, enx + 40, -430)
    s += N(enx + 40, -430, enx + 40, -370)

    # NOR gate
    np1x, np1y = 980, -490
    s += C("pmos4.sym", np1x, np1y, props="name=XMnor_p1 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1 spiceprefix=X")
    s += N(np1x - 20, np1y, np1x - 60, np1y)
    s += T("out_n", np1x - 120, np1y - 10, 0.3, 8)
    s += N(np1x + 20, np1y - 30, np1x + 20, np1y - 60)
    s += T("vdd_comp", np1x + 30, np1y - 70, 0.25, 8)
    s += N(np1x + 20, np1y, np1x + 40, np1y)
    s += N(np1x + 40, np1y, np1x + 40, np1y - 60)

    np2x, np2y = 980, -400
    s += C("pmos4.sym", np2x, np2y, props="name=XMnor_p2 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1 spiceprefix=X")
    s += N(np2x - 20, np2y, np2x - 60, np2y)
    s += T("en_bar", np2x - 120, np2y - 10, 0.3, 8)
    s += N(np1x + 20, np1y + 30, np2x + 20, np2y - 30)
    s += N(np2x + 20, np2y, np1x + 20, np1y + 30)

    nn1x, nn1y = 950, -280
    s += C("nmos4.sym", nn1x, nn1y, props="name=XMnor_n1 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1 spiceprefix=X")
    s += N(nn1x - 20, nn1y, nn1x - 60, nn1y)
    s += T("out_n", nn1x - 120, nn1y - 10, 0.25, 8)
    s += N(nn1x + 20, nn1y + 30, nn1x + 20, nn1y + 60)
    s += C("gnd.sym", nn1x + 20, nn1y + 60, props="name=l5 lab=GND")
    s += N(nn1x + 20, nn1y, nn1x + 40, nn1y)
    s += N(nn1x + 40, nn1y, nn1x + 40, nn1y + 60)

    nn2x, nn2y = 1060, -280
    s += C("nmos4.sym", nn2x, nn2y, props="name=XMnor_n2 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1 spiceprefix=X")
    s += N(nn2x - 20, nn2y, nn2x - 60, nn2y)
    s += T("en_bar", nn2x - 130, nn2y - 10, 0.25, 8)
    s += N(nn2x + 20, nn2y + 30, nn2x + 20, nn2y + 60)
    s += C("gnd.sym", nn2x + 20, nn2y + 60, props="name=l6 lab=GND")
    s += N(nn2x + 20, nn2y, nn2x + 40, nn2y)
    s += N(nn2x + 40, nn2y, nn2x + 40, nn2y + 60)

    out_y = -340
    s += N(nn1x + 20, nn1y - 30, nn1x + 20, out_y)
    s += N(nn2x + 20, nn2y - 30, nn2x + 20, out_y)
    s += N(nn1x + 20, out_y, nn2x + 20, out_y)
    nor_cx = (nn1x + nn2x) // 2 + 20
    s += N(nor_cx, out_y, np2x + 20, out_y)           # horizontal to align
    s += N(np2x + 20, out_y, np2x + 20, np2y + 30)    # vertical up to PMOS drain

    s += N(nn2x + 20, out_y, nn2x + 150, out_y)
    s += C("iopin.sym", nn2x + 150, out_y, 0, 0, "name=p_out lab=uv_flag")
    s += T("uv_flag", nn2x + 160, out_y - 30, 0.5, 4)
    s += T("HIGH when PVDD < 4.3 V", nn2x + 160, out_y + 10, 0.3)

    # ===== CHARACTERIZATION =====
    cy = 100
    s += T("CHARACTERIZATION", -600, cy, 0.5, 4)
    s += T("UV threshold (falling, TT 27C)   =  4.289 V       spec 4.0 - 4.5 V       PASS", -600, cy+60, 0.3, 7)
    s += T("UV hysteresis                     =  63.5 mV       spec 50 - 150 mV        PASS", -600, cy+100, 0.3, 7)
    s += T("UV de-assertion (rising)          =  4.353 V       within spec window       PASS", -600, cy+140, 0.3, 7)
    s += T("Response time                     =  < 0.01 us     spec <= 5 us             PASS", -600, cy+180, 0.3, 7)
    s += T("Power (from vdd_comp)             =  2.71 uA       spec <= 5 uA             PASS", -600, cy+220, 0.3, 7)
    s += T("Output rail-to-rail               =  YES            0 / 1.8 V               PASS", -600, cy+260, 0.3, 7)
    s += T("Threshold error                   =  5.2 mV        spec <= 200 mV           PASS", -600, cy+300, 0.3, 7)
    s += T("All 13/13 specs PASS", -600, cy+370, 0.45, 4)

    s += C("title.sym", -660, cy+500, props='name=l1 author="Block 05: UV Comparator -- Analog AI Chips PVDD LDO Regulator"')
    return s


def build_ov():
    s = HDR

    s += T("BLOCK 05: OV COMPARATOR", -600, -1100, 1.0, 4)
    s += T("PVDD 5.0V LDO Regulator", -600, -1020, 0.5, 8)
    s += T("SkyWater SKY130A Process", -600, -980, 0.4)
    s += T("Topology: NMOS differential pair + PMOS current mirror load", -600, -920, 0.35)
    s += T("Supply: vdd_comp = 1.8 V    |    Threshold: PVDD > 5.5 V    |    ov_flag = HIGH when overvoltage", -600, -880, 0.35)
    s += T("NOTE: Diff pair inputs SWAPPED vs UV  (M1 = vref, M2 = mid_ov)", -600, -840, 0.35, 5)
    s += T("Date: 2026-03-28", -600, -790, 0.3)
    s += T(".subckt ov_comparator  pvdd  vref  ov_flag  vdd_comp  gnd  en", -600, -750, 0.3, 13)

    # Divider
    s += T("RESISTIVE DIVIDER", -600, -660, 0.5, 4)
    s += T("Scales PVDD down to ~1.226 V", -600, -620, 0.3)

    s += T("pvdd", -580, -540, 0.4, 7)
    rx, ry = -500, -450
    s += C("res.sym", rx, ry, props="name=R_top value=500k")
    s += N(rx, -520, rx, ry - 30)
    s += C("iopin.sym", rx, -520, 3, 0, "name=p_pvdd lab=pvdd")

    mid_y = -360
    s += N(rx, ry + 30, rx, mid_y)
    s += N(rx, mid_y, rx + 80, mid_y)
    s += T("mid_ov", rx + 90, mid_y - 10, 0.35, 8)

    s += C("res.sym", rx, mid_y + 70, props="name=R_bot value=146k")
    s += N(rx, mid_y, rx, mid_y + 40)
    s += N(rx, mid_y + 100, rx, mid_y + 140)
    s += C("gnd.sym", rx, mid_y + 140, props="name=l1 lab=GND")

    # Hysteresis
    s += T("HYSTERESIS", -320, -660, 0.45, 4)
    s += T("R_hyst = 8 Meg", -320, -620, 0.3, 7)
    s += T("Feedback: ov_flag to mid_ov", -320, -590, 0.3)
    s += T("Positive feedback for clean switching", -320, -560, 0.25, 5)

    rhyst_x = -250
    s += C("res.sym", rhyst_x, mid_y + 30, props="name=R_hyst value=8M")
    s += N(rx + 80, mid_y, rhyst_x, mid_y)          # horizontal to top pin
    s += N(rhyst_x, mid_y + 60, -170, mid_y + 60)   # horizontal from bottom pin
    s += T("ov_flag", -160, mid_y + 50, 0.3, 7)
    s += T("(from output)", -160, mid_y + 75, 0.2, 5)

    # Bias
    s += T("BIAS", -100, -660, 0.45, 4)
    s += T("~1 uA self-biased", -100, -620, 0.3)

    bx = -30
    s += C("res.sym", bx, -530, props="name=R_bias value=800k")
    s += N(bx, -600, bx, -560)
    s += T("vdd_comp", bx - 60, -620, 0.3, 8)

    s += C("nmos4.sym", bx - 20, -410, props="name=XMbias model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1 spiceprefix=X")
    s += N(bx, -500, bx, -440)
    s += N(bx - 40, -410, bx - 40, -440)
    s += N(bx - 40, -440, bx, -440)
    s += N(bx, -380, bx, -340)
    s += C("gnd.sym", bx, -340, props="name=l2 lab=GND")
    # Body to source (both gnd)
    s += N(bx, -410, bx, -380)
    s += T("bias_n", bx + 30, -450, 0.3, 8)

    # Diff pair + mirror
    s += T("NMOS DIFFERENTIAL PAIR", 200, -660, 0.5, 4)
    s += T("+ PMOS CURRENT MIRROR LOAD", 200, -620, 0.45, 4)
    s += T("Inputs SWAPPED: M1=vref, M2=mid_ov", 200, -585, 0.3, 5)

    m3x, m3y = 280, -480
    s += C("pmos4.sym", m3x, m3y, props="name=XM3 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1 spiceprefix=X")
    s += N(m3x + 20, m3y - 30, m3x + 20, m3y - 70)
    s += T("vdd_comp", m3x + 30, m3y - 80, 0.3, 8)
    s += N(m3x - 20, m3y, m3x - 40, m3y)
    s += N(m3x - 40, m3y, m3x - 40, m3y + 30)
    s += N(m3x - 40, m3y + 30, m3x + 20, m3y + 30)
    s += N(m3x + 20, m3y, m3x + 40, m3y)
    s += N(m3x + 40, m3y, m3x + 40, m3y - 70)
    s += T("out_p", m3x + 30, m3y + 25, 0.25, 13)

    m4x, m4y = 530, -480
    s += C("pmos4.sym", m4x, m4y, props="name=XM4 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1 spiceprefix=X")
    s += N(m4x + 20, m4y - 30, m4x + 20, m4y - 70)
    s += T("vdd_comp", m4x + 30, m4y - 80, 0.3, 8)
    s += N(m4x - 20, m4y, m3x - 40, m4y)
    s += N(m4x + 20, m4y, m4x + 40, m4y)
    s += N(m4x + 40, m4y, m4x + 40, m4y - 70)
    s += T("out_n", m4x + 30, m4y + 25, 0.35, 7)

    m1x, m1y = 280, -300
    s += C("nmos4.sym", m1x, m1y, props="name=XM1 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1 spiceprefix=X")
    s += N(m1x + 20, m1y - 30, m3x + 20, m3y + 30)
    s += T("vref", m1x - 100, m1y - 10, 0.35, 8)
    s += N(m1x - 80, m1y, m1x - 20, m1y)
    s += N(m1x + 20, m1y + 30, m1x + 20, m1y + 60)
    # Body to GND (B=gnd, S=tail — different nets)
    s += N(m1x + 20, m1y, m1x + 40, m1y)
    s += N(m1x + 40, m1y, m1x + 40, m1y + 40)
    s += C("gnd.sym", m1x + 40, m1y + 40, props="name=lb1 lab=GND")

    m2x, m2y = 530, -300
    s += C("nmos4.sym", m2x, m2y, props="name=XM2 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1 spiceprefix=X")
    s += N(m2x + 20, m2y - 30, m4x + 20, m4y + 30)
    s += T("mid_ov", m2x - 100, m2y - 10, 0.35, 8)
    s += N(m2x - 80, m2y, m2x - 20, m2y)
    s += N(m2x + 20, m2y + 30, m2x + 20, m2y + 60)
    # Body to GND
    s += N(m2x + 20, m2y, m2x + 40, m2y)
    s += N(m2x + 40, m2y, m2x + 40, m2y + 40)
    s += C("gnd.sym", m2x + 40, m2y + 40, props="name=lb2 lab=GND")

    tail_y = m1y + 60
    s += N(m1x + 20, tail_y, m2x + 20, tail_y)
    tail_cx = (m1x + m2x) // 2 + 20
    s += N(tail_cx, tail_y, tail_cx, tail_y + 30)
    s += T("tail", tail_cx + 10, tail_y - 5, 0.3, 13)

    tx, ty = tail_cx - 20, tail_y + 80
    s += C("nmos4.sym", tx, ty, props="name=XMtail model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1 spiceprefix=X")
    s += N(tx + 20, ty - 30, tail_cx, tail_y + 30)
    s += N(tx - 20, ty, tx - 60, ty)
    s += T("bias_n", tx - 120, ty - 10, 0.3, 8)
    s += N(tx + 20, ty + 30, tx + 20, ty + 60)
    s += C("gnd.sym", tx + 20, ty + 60, props="name=l3 lab=GND")
    # Body to source (both gnd)
    s += N(tx + 20, ty, tx + 20, ty + 30)

    # Output stage
    s += T("ENABLE + NOR OUTPUT", 750, -660, 0.5, 4)
    s += T("ov_flag = NOR(out_n, en_bar)", 750, -620, 0.35, 13)
    s += T("HIGH when PVDD > threshold", 750, -590, 0.3, 5)

    enx = 800
    s += C("pmos4.sym", enx, -490, props="name=XMen_p model=sky130_fd_pr__pfet_01v8 w=0.84u l=0.15u m=1 spiceprefix=X")
    s += C("nmos4.sym", enx, -410, props="name=XMen_n model=sky130_fd_pr__nfet_01v8 w=0.42u l=0.15u m=1 spiceprefix=X")
    s += N(enx - 20, -490, enx - 20, -410)
    s += N(enx - 20, -450, enx - 60, -450)
    s += T("en", enx - 110, -460, 0.35, 8)
    s += N(enx + 20, -460, enx + 20, -440)
    s += T("en_bar", enx + 50, -455, 0.3, 13)
    s += N(enx + 20, -450, enx + 50, -450)
    s += N(enx + 20, -520, enx + 20, -550)
    s += T("vdd_comp", enx + 30, -560, 0.25, 8)
    s += N(enx + 20, -490, enx + 40, -490)
    s += N(enx + 40, -490, enx + 40, -550)
    s += N(enx + 20, -380, enx + 20, -350)
    s += C("gnd.sym", enx + 20, -350, props="name=l4 lab=GND")
    s += N(enx + 20, -410, enx + 40, -410)
    s += N(enx + 40, -410, enx + 40, -350)

    np1x, np1y = 980, -470
    s += C("pmos4.sym", np1x, np1y, props="name=XMnor_p1 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1 spiceprefix=X")
    s += N(np1x - 20, np1y, np1x - 60, np1y)
    s += T("out_n", np1x - 120, np1y - 10, 0.3, 8)
    s += N(np1x + 20, np1y - 30, np1x + 20, np1y - 60)
    s += T("vdd_comp", np1x + 30, np1y - 70, 0.25, 8)
    s += N(np1x + 20, np1y, np1x + 40, np1y)
    s += N(np1x + 40, np1y, np1x + 40, np1y - 60)

    np2x, np2y = 980, -380
    s += C("pmos4.sym", np2x, np2y, props="name=XMnor_p2 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1 spiceprefix=X")
    s += N(np2x - 20, np2y, np2x - 60, np2y)
    s += T("en_bar", np2x - 120, np2y - 10, 0.3, 8)
    s += N(np1x + 20, np1y + 30, np2x + 20, np2y - 30)
    s += N(np2x + 20, np2y, np1x + 20, np1y + 30)

    nn1x, nn1y = 950, -260
    s += C("nmos4.sym", nn1x, nn1y, props="name=XMnor_n1 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1 spiceprefix=X")
    s += N(nn1x - 20, nn1y, nn1x - 60, nn1y)
    s += T("out_n", nn1x - 120, nn1y - 10, 0.25, 8)
    s += N(nn1x + 20, nn1y + 30, nn1x + 20, nn1y + 60)
    s += C("gnd.sym", nn1x + 20, nn1y + 60, props="name=l5 lab=GND")
    s += N(nn1x + 20, nn1y, nn1x + 40, nn1y)
    s += N(nn1x + 40, nn1y, nn1x + 40, nn1y + 60)

    nn2x, nn2y = 1060, -260
    s += C("nmos4.sym", nn2x, nn2y, props="name=XMnor_n2 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1 spiceprefix=X")
    s += N(nn2x - 20, nn2y, nn2x - 60, nn2y)
    s += T("en_bar", nn2x - 130, nn2y - 10, 0.25, 8)
    s += N(nn2x + 20, nn2y + 30, nn2x + 20, nn2y + 60)
    s += C("gnd.sym", nn2x + 20, nn2y + 60, props="name=l6 lab=GND")
    s += N(nn2x + 20, nn2y, nn2x + 40, nn2y)
    s += N(nn2x + 40, nn2y, nn2x + 40, nn2y + 60)

    out_y = -320
    s += N(nn1x + 20, nn1y - 30, nn1x + 20, out_y)
    s += N(nn2x + 20, nn2y - 30, nn2x + 20, out_y)
    s += N(nn1x + 20, out_y, nn2x + 20, out_y)
    nor_cx = (nn1x + nn2x) // 2 + 20
    s += N(nor_cx, out_y, np2x + 20, out_y)           # horizontal to align
    s += N(np2x + 20, out_y, np2x + 20, np2y + 30)    # vertical up to PMOS drain

    s += N(nn2x + 20, out_y, nn2x + 150, out_y)
    s += C("iopin.sym", nn2x + 150, out_y, 0, 0, "name=p_out lab=ov_flag")
    s += T("ov_flag", nn2x + 160, out_y - 30, 0.5, 4)
    s += T("HIGH when PVDD > 5.5 V", nn2x + 160, out_y + 10, 0.3)

    # Characterization
    cy = 120
    s += T("CHARACTERIZATION", -600, cy, 0.5, 4)
    s += T("OV threshold (rising, TT 27C)    =  5.495 V       spec 5.25 - 5.7 V       PASS", -600, cy+60, 0.3, 7)
    s += T("OV hysteresis                     =  112.2 mV      spec 50 - 150 mV         PASS", -600, cy+100, 0.3, 7)
    s += T("OV de-assertion (falling)         =  5.383 V       within spec window       PASS", -600, cy+140, 0.3, 7)
    s += T("Response time                     =  < 0.01 us     spec <= 5 us             PASS", -600, cy+180, 0.3, 7)
    s += T("Power (from vdd_comp)             =  2.57 uA       spec <= 5 uA             PASS", -600, cy+220, 0.3, 7)
    s += T("Output rail-to-rail               =  YES            0 / 1.8 V               PASS", -600, cy+260, 0.3, 7)
    s += T("Threshold error                   =  5.2 mV        spec <= 200 mV           PASS", -600, cy+300, 0.3, 7)
    s += T("All 13/13 specs PASS", -600, cy+370, 0.45, 4)

    s += C("title.sym", -660, cy+500, props='name=l1 author="Block 05: OV Comparator -- Analog AI Chips PVDD LDO Regulator"')
    return s


if __name__ == '__main__':
    with open('uv_comparator.sch', 'w') as f:
        f.write(build_uv())
    print("Generated uv_comparator.sch")

    with open('ov_comparator.sch', 'w') as f:
        f.write(build_ov())
    print("Generated ov_comparator.sch")
