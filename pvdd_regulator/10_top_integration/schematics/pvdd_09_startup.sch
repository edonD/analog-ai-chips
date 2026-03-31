v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {STARTUP — Level-Shift + Detect + Inverter} -300 -1200 0 0 0.85 0.85 {layer=4}
T {Block 09 — 3 MOSFETs + 3 res_xhigh_po + 2 bare R + 1 bare R(Ren)} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {bvdd, pvdd, gate, gnd, vref, startup_done, ea_en, ea_out  |  design.cir .subckt startup} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="Claude / analog-ai-chips"}

* ============================================================
* PORT PINS
* ============================================================
T {PORT PINS} -700 -940 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -700 -900 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -700 -860 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -700 -820 0 0 {name=p3 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -700 -780 0 0 {name=p4 lab=ea_out}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -700 -740 0 0 {name=p5 lab=vref}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -450 -900 0 0 {name=p6 lab=gate}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -450 -860 0 0 {name=p7 lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -450 -820 0 0 {name=p8 lab=ea_en}
* ============================================================
* BIAS DIVIDER
* ============================================================
T {BIAS DIVIDER} -450 -650 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/res.sym} -350 -500 0 0 {name=Rlb1 value=200k}
T {Rlb1} -330 -520 0 0 0.2 0.2 {layer=13}
T {200k} -330 -492 0 0 0.18 0.18 {layer=5}
N -350 -530 -350 -565 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -350 -565 2 0 {name=lb1 sig_type=std_logic lab=bvdd}
N -350 -470 -350 -435 {lab=ls_bias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -350 -435 2 0 {name=lb2 sig_type=std_logic lab=ls_bias}
C {/usr/share/xschem/xschem_library/devices/res.sym} -350 -300 0 0 {name=Rlb2 value=500k}
T {Rlb2} -330 -320 0 0 0.2 0.2 {layer=13}
T {500k} -330 -292 0 0 0.18 0.18 {layer=5}
N -350 -330 -350 -365 {lab=ls_bias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -350 -365 2 0 {name=lb3 sig_type=std_logic lab=ls_bias}
N -350 -270 -350 -235 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -350 -235 2 0 {name=lb4 sig_type=std_logic lab=gnd}
* ============================================================
* CG LEVEL SHIFTER
* ============================================================
T {CG LEVEL SHIFTER} -20 -650 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 100 -300 0 0 {name=XMN_cg L=4e-06 W=1.2e-06 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN_cg} 75 -350 0 0 0.22 0.22 {layer=13}
T {N: W=1.2e-06 L=4e-06} 75 -335 0 0 0.18 0.18 {layer=5}
N 80 -300 40 -300 {lab=ls_bias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -300 0 0 {name=lb5 sig_type=std_logic lab=ls_bias}
N 120 -300 150 -300 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -300 2 0 {name=lb6 sig_type=std_logic lab=gnd}
N 120 -330 120 -370 {lab=ea_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 -370 2 0 {name=lb7 sig_type=std_logic lab=ea_out}
N 120 -270 120 -230 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 -230 2 0 {name=lb8 sig_type=std_logic lab=gate}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 250 -400 0 0 {name=XR_load W=1 L=19 model=res_xhigh_po spiceprefix=X}
T {XR_load} 270 -425 0 0 0.2 0.2 {layer=13}
T {W=1 L=19} 270 -390 0 0 0.17 0.17 {layer=5}
N 250 -430 250 -465 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -465 2 0 {name=lb9 sig_type=std_logic lab=bvdd}
N 250 -370 250 -335 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -335 2 0 {name=lb10 sig_type=std_logic lab=gate}
N 230 -400 205 -400 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 205 -400 0 0 {name=lb11 sig_type=std_logic lab=gnd}
* ============================================================
* EA ENABLE
* ============================================================
T {EA ENABLE} 20 -100 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/res.sym} 100 -10 0 0 {name=Ren value=100}
T {Ren} 120 -30 0 0 0.2 0.2 {layer=13}
T {100} 120 -2 0 0 0.18 0.18 {layer=5}
N 100 -40 100 -75 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -75 2 0 {name=lb12 sig_type=std_logic lab=bvdd}
N 100 20 100 55 {lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 55 2 0 {name=lb13 sig_type=std_logic lab=ea_en}
* ============================================================
* STARTUP-DONE DETECTOR
* ============================================================
T {STARTUP-DONE DETECTOR} 380 -650 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 500 -500 0 0 {name=XR_top W=2 L=788 model=res_xhigh_po spiceprefix=X}
T {XR_top} 520 -525 0 0 0.2 0.2 {layer=13}
T {W=2 L=788} 520 -490 0 0 0.17 0.17 {layer=5}
N 500 -530 500 -565 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -565 2 0 {name=lb14 sig_type=std_logic lab=pvdd}
N 500 -470 500 -435 {lab=sense_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -435 2 0 {name=lb15 sig_type=std_logic lab=sense_mid}
N 480 -500 455 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 455 -500 0 0 {name=lb16 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 500 -300 0 0 {name=XR_bot W=2 L=212 model=res_xhigh_po spiceprefix=X}
T {XR_bot} 520 -325 0 0 0.2 0.2 {layer=13}
T {W=2 L=212} 520 -290 0 0 0.17 0.17 {layer=5}
N 500 -330 500 -365 {lab=sense_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -365 2 0 {name=lb17 sig_type=std_logic lab=sense_mid}
N 500 -270 500 -235 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -235 2 0 {name=lb18 sig_type=std_logic lab=gnd}
N 480 -300 455 -300 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 455 -300 0 0 {name=lb19 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 700 -300 0 0 {name=XMN_det L=1e-06 W=4e-06 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN_det} 675 -350 0 0 0.22 0.22 {layer=13}
T {N: W=4e-06 L=1e-06} 675 -335 0 0 0.18 0.18 {layer=5}
N 680 -300 640 -300 {lab=sense_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 640 -300 0 0 {name=lb20 sig_type=std_logic lab=sense_mid}
N 720 -300 750 -300 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 -300 2 0 {name=lb21 sig_type=std_logic lab=gnd}
N 720 -330 720 -370 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 -370 2 0 {name=lb22 sig_type=std_logic lab=det_n}
N 720 -270 720 -230 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 -230 2 0 {name=lb23 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 700 -500 0 0 {name=XR_pu W=1 L=2000 model=res_xhigh_po spiceprefix=X}
T {XR_pu} 720 -525 0 0 0.2 0.2 {layer=13}
T {W=1 L=2000} 720 -490 0 0 0.17 0.17 {layer=5}
N 700 -530 700 -565 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -565 2 0 {name=lb24 sig_type=std_logic lab=bvdd}
N 700 -470 700 -435 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -435 2 0 {name=lb25 sig_type=std_logic lab=det_n}
N 680 -500 655 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 655 -500 0 0 {name=lb26 sig_type=std_logic lab=gnd}
* ============================================================
* INV
* ============================================================
T {INV} 890 -480 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 950 -400 0 0 {name=XMP_inv1 L=1e-06 W=4e-06 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMP_inv1} 925 -450 0 0 0.22 0.22 {layer=13}
T {P: W=4e-06 L=1e-06} 925 -435 0 0 0.18 0.18 {layer=5}
N 930 -400 890 -400 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 890 -400 0 0 {name=lb27 sig_type=std_logic lab=det_n}
N 970 -400 1000 -400 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -400 2 0 {name=lb28 sig_type=std_logic lab=bvdd}
N 970 -430 970 -470 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -470 2 0 {name=lb29 sig_type=std_logic lab=bvdd}
N 970 -370 970 -330 {lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -330 2 0 {name=lb30 sig_type=std_logic lab=startup_done}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 950 -200 0 0 {name=XMN_inv1 L=1e-06 W=2e-06 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN_inv1} 925 -250 0 0 0.22 0.22 {layer=13}
T {N: W=2e-06 L=1e-06} 925 -235 0 0 0.18 0.18 {layer=5}
N 930 -200 890 -200 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 890 -200 0 0 {name=lb31 sig_type=std_logic lab=det_n}
N 970 -200 1000 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -200 2 0 {name=lb32 sig_type=std_logic lab=gnd}
N 970 -230 970 -270 {lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -270 2 0 {name=lb33 sig_type=std_logic lab=startup_done}
N 970 -170 970 -130 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -130 2 0 {name=lb34 sig_type=std_logic lab=gnd}
L 4 -500 -620 -200 -620 {dash=5}
L 4 -200 -620 -200 -200 {dash=5}
L 4 -200 -200 -500 -200 {dash=5}
L 4 -500 -200 -500 -620 {dash=5}
L 5 -50 -550 350 -550 {dash=5}
L 5 350 -550 350 -100 {dash=5}
L 5 350 -100 -50 -100 {dash=5}
L 5 -50 -100 -50 -550 {dash=5}
L 7 350 -620 1100 -620 {dash=5}
L 7 1100 -620 1100 -100 {dash=5}
L 7 1100 -100 350 -100 {dash=5}
L 7 350 -100 350 -620 {dash=5}
