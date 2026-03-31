v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {ERROR AMPLIFIER — Two-Stage Miller OTA} -300 -1200 0 0 0.85 0.85 {layer=4}
T {Block 00 — 12 MOSFETs + Cc + Rc} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {vref(+), vfb(-), vout_gate(out), pvdd, gnd, ibias, en  |  design.cir .subckt error_amp} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="Claude / analog-ai-chips"}

* ============================================================
* PORT PINS
* ============================================================
T {PORT PINS} -600 -940 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -900 0 0 {name=p1 lab=vref}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -860 0 0 {name=p2 lab=vfb}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -820 0 0 {name=p3 lab=ibias}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -780 0 0 {name=p4 lab=en}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -740 0 0 {name=p5 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -700 0 0 {name=p6 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -400 -900 0 0 {name=p7 lab=vout_gate}
* ============================================================
* ENABLE LOGIC
* ============================================================
T {ENABLE LOGIC} -300 -680 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -100 -600 0 0 {name=XMen L=1 W=20 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMen} -125 -650 0 0 0.22 0.22 {layer=13}
T {N: W=20 L=1} -125 -635 0 0 0.18 0.18 {layer=5}
N -120 -600 -160 -600 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -160 -600 0 0 {name=lb1 sig_type=std_logic lab=en}
N -80 -600 -50 -600 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -50 -600 2 0 {name=lb2 sig_type=std_logic lab=gnd}
N -80 -630 -80 -670 {lab=ibias_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -80 -670 2 0 {name=lb3 sig_type=std_logic lab=ibias_en}
N -80 -570 -80 -530 {lab=ibias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -80 -530 2 0 {name=lb4 sig_type=std_logic lab=ibias}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 350 -600 0 0 {name=XMpu L=1 W=20 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMpu} 325 -650 0 0 0.22 0.22 {layer=13}
T {P: W=20 L=1} 325 -635 0 0 0.18 0.18 {layer=5}
N 330 -600 290 -600 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 290 -600 0 0 {name=lb5 sig_type=std_logic lab=en}
N 370 -600 400 -600 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -600 2 0 {name=lb6 sig_type=std_logic lab=pvdd}
N 370 -630 370 -670 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 370 -670 2 0 {name=lb7 sig_type=std_logic lab=pvdd}
N 370 -570 370 -530 {lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 370 -530 2 0 {name=lb8 sig_type=std_logic lab=vout_gate}
* ============================================================
* BIAS CHAIN
* ============================================================
T {BIAS CHAIN} -500 -350 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -400 -200 0 0 {name=XMbn0 L=8 W=20 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMbn0} -425 -250 0 0 0.22 0.22 {layer=13}
T {N: W=20 L=8} -425 -235 0 0 0.18 0.18 {layer=5}
N -420 -200 -460 -200 {lab=ibias_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -460 -200 0 0 {name=lb9 sig_type=std_logic lab=ibias_en}
N -380 -200 -350 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -350 -200 2 0 {name=lb10 sig_type=std_logic lab=gnd}
N -380 -230 -380 -270 {lab=ibias_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -380 -270 2 0 {name=lb11 sig_type=std_logic lab=ibias_en}
N -380 -170 -380 -130 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -380 -130 2 0 {name=lb12 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -400 200 0 0 {name=XMbn_pb L=8 W=20 nf=1 mult=200 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMbn_pb} -425 150 0 0 0.22 0.22 {layer=13}
T {N: W=20 L=8 m=200} -425 165 0 0 0.18 0.18 {layer=5}
N -420 200 -460 200 {lab=ibias_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -460 200 0 0 {name=lb13 sig_type=std_logic lab=ibias_en}
N -380 200 -350 200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -350 200 2 0 {name=lb14 sig_type=std_logic lab=gnd}
N -380 170 -380 130 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -380 130 2 0 {name=lb15 sig_type=std_logic lab=pb_tail}
N -380 230 -380 270 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -380 270 2 0 {name=lb16 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 0 -200 0 0 {name=XMbp0 L=4 W=20 nf=1 mult=4 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMbp0} -25 -250 0 0 0.22 0.22 {layer=13}
T {P: W=20 L=4 m=4} -25 -235 0 0 0.18 0.18 {layer=5}
N -20 -200 -60 -200 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -60 -200 0 0 {name=lb17 sig_type=std_logic lab=pb_tail}
N 20 -200 50 -200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 50 -200 2 0 {name=lb18 sig_type=std_logic lab=pvdd}
N 20 -230 20 -270 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -270 2 0 {name=lb19 sig_type=std_logic lab=pvdd}
N 20 -170 20 -130 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -130 2 0 {name=lb20 sig_type=std_logic lab=pb_tail}
* ============================================================
* STAGE 1 — DIFF PAIR
* ============================================================
T {STAGE 1 — DIFF PAIR} 200 -380 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 400 -250 0 0 {name=XMtail L=4 W=20 nf=1 mult=4 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMtail} 375 -300 0 0 0.22 0.22 {layer=13}
T {P: W=20 L=4 m=4} 375 -285 0 0 0.18 0.18 {layer=5}
N 380 -250 340 -250 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -250 0 0 {name=lb21 sig_type=std_logic lab=pb_tail}
N 420 -250 450 -250 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 450 -250 2 0 {name=lb22 sig_type=std_logic lab=pvdd}
N 420 -280 420 -320 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -320 2 0 {name=lb23 sig_type=std_logic lab=pvdd}
N 420 -220 420 -180 {lab=tail_s}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -180 2 0 {name=lb24 sig_type=std_logic lab=tail_s}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 200 100 0 0 {name=XM1 L=4 W=80 nf=1 mult=2 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM1} 175 50 0 0 0.22 0.22 {layer=13}
T {P: W=80 L=4 m=2} 175 65 0 0 0.18 0.18 {layer=5}
N 180 100 140 100 {lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 100 0 0 {name=lb25 sig_type=std_logic lab=vref}
N 220 100 250 100 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 100 2 0 {name=lb26 sig_type=std_logic lab=pvdd}
N 220 70 220 30 {lab=tail_s}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 30 2 0 {name=lb27 sig_type=std_logic lab=tail_s}
N 220 130 220 170 {lab=d1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 170 2 0 {name=lb28 sig_type=std_logic lab=d1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 600 100 0 0 {name=XM2 L=4 W=80 nf=1 mult=2 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM2} 575 50 0 0 0.22 0.22 {layer=13}
T {P: W=80 L=4 m=2} 575 65 0 0 0.18 0.18 {layer=5}
N 580 100 540 100 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 100 0 0 {name=lb29 sig_type=std_logic lab=vfb}
N 620 100 650 100 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 100 2 0 {name=lb30 sig_type=std_logic lab=pvdd}
N 620 70 620 30 {lab=tail_s}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 30 2 0 {name=lb31 sig_type=std_logic lab=tail_s}
N 620 130 620 170 {lab=d2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 170 2 0 {name=lb32 sig_type=std_logic lab=d2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 200 450 0 0 {name=XMn_l L=8 W=20 nf=1 mult=2 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMn_l} 175 400 0 0 0.22 0.22 {layer=13}
T {N: W=20 L=8 m=2} 175 415 0 0 0.18 0.18 {layer=5}
N 180 450 140 450 {lab=d1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 450 0 0 {name=lb33 sig_type=std_logic lab=d1}
N 220 450 250 450 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 450 2 0 {name=lb34 sig_type=std_logic lab=gnd}
N 220 420 220 380 {lab=d1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 380 2 0 {name=lb35 sig_type=std_logic lab=d1}
N 220 480 220 520 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 520 2 0 {name=lb36 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 600 450 0 0 {name=XMn_r L=8 W=20 nf=1 mult=2 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMn_r} 575 400 0 0 0.22 0.22 {layer=13}
T {N: W=20 L=8 m=2} 575 415 0 0 0.18 0.18 {layer=5}
N 580 450 540 450 {lab=d1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 450 0 0 {name=lb37 sig_type=std_logic lab=d1}
N 620 450 650 450 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 450 2 0 {name=lb38 sig_type=std_logic lab=gnd}
N 620 420 620 380 {lab=d2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 380 2 0 {name=lb39 sig_type=std_logic lab=d2}
N 620 480 620 520 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 520 2 0 {name=lb40 sig_type=std_logic lab=gnd}
N 220 170 220 380 {lab=d1}
T {d1} 230 275 0 0 0.28 0.28 {layer=8}
N 620 170 620 380 {lab=d2}
T {d2} 630 275 0 0 0.28 0.28 {layer=8}
* ============================================================
* STAGE 2 — CS GAIN
* ============================================================
T {STAGE 2 — CS GAIN} 900 -380 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1050 -200 0 0 {name=XMp_ld L=4 W=20 nf=1 mult=8 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMp_ld} 1025 -250 0 0 0.22 0.22 {layer=13}
T {P: W=20 L=4 m=8} 1025 -235 0 0 0.18 0.18 {layer=5}
N 1030 -200 990 -200 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 990 -200 0 0 {name=lb41 sig_type=std_logic lab=pb_tail}
N 1070 -200 1100 -200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -200 2 0 {name=lb42 sig_type=std_logic lab=pvdd}
N 1070 -230 1070 -270 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 -270 2 0 {name=lb43 sig_type=std_logic lab=pvdd}
N 1070 -170 1070 -130 {lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 -130 2 0 {name=lb44 sig_type=std_logic lab=vout_gate}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1050 200 0 0 {name=XMcs L=1 W=20 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMcs} 1025 150 0 0 0.22 0.22 {layer=13}
T {N: W=20 L=1} 1025 165 0 0 0.18 0.18 {layer=5}
N 1030 200 990 200 {lab=d2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 990 200 0 0 {name=lb45 sig_type=std_logic lab=d2}
N 1070 200 1100 200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 200 2 0 {name=lb46 sig_type=std_logic lab=gnd}
N 1070 170 1070 130 {lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 130 2 0 {name=lb47 sig_type=std_logic lab=vout_gate}
N 1070 230 1070 270 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 270 2 0 {name=lb48 sig_type=std_logic lab=gnd}
N 1070 -130 1070 130 {lab=vout_gate}
T {vout_gate} 1080 0 0 0 0.28 0.28 {layer=8}
* ============================================================
* MILLER COMP
* ============================================================
T {MILLER COMP} 1350 -380 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 1450 -100 0 0 {name=Cc value=30p}
T {Cc} 1470 -120 0 0 0.2 0.2 {layer=13}
T {30p} 1470 -92 0 0 0.18 0.18 {layer=5}
N 1450 -130 1450 -165 {lab=d2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1450 -165 2 0 {name=lb49 sig_type=std_logic lab=d2}
N 1450 -70 1450 -35 {lab=comp_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1450 -35 2 0 {name=lb50 sig_type=std_logic lab=comp_mid}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1450 200 0 0 {name=Rc value=25k}
T {Rc} 1470 180 0 0 0.2 0.2 {layer=13}
T {25k} 1470 208 0 0 0.18 0.18 {layer=5}
N 1450 170 1450 135 {lab=comp_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1450 135 2 0 {name=lb51 sig_type=std_logic lab=comp_mid}
N 1450 230 1450 265 {lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1450 265 2 0 {name=lb52 sig_type=std_logic lab=vout_gate}
N 1450 -35 1450 135 {lab=comp_mid}
T {comp_mid} 1465 50 0 0 0.28 0.28 {layer=8}
L 8 -350 -720 600 -720 {dash=5}
L 8 600 -720 600 -480 {dash=5}
L 8 600 -480 -350 -480 {dash=5}
L 8 -350 -480 -350 -720 {dash=5}
L 8 -550 -350 150 -350 {dash=5}
L 8 150 -350 150 350 {dash=5}
L 8 150 350 -550 350 {dash=5}
L 8 -550 350 -550 -350 {dash=5}
L 8 50 -380 850 -380 {dash=5}
L 8 850 -380 850 600 {dash=5}
L 8 850 600 50 600 {dash=5}
L 8 50 600 50 -380 {dash=5}
L 8 850 -380 1250 -380 {dash=5}
L 8 1250 -380 1250 350 {dash=5}
L 8 1250 350 850 350 {dash=5}
L 8 850 350 850 -380 {dash=5}
L 8 1330 -380 1570 -380 {dash=5}
L 8 1570 -380 1570 350 {dash=5}
L 8 1570 350 1330 350 {dash=5}
L 8 1330 350 1330 -380 {dash=5}
