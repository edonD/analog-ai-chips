v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {ZENER CLAMP — Precision N-P-N-P-N Stack + Fast Diode Clamp} -300 -1200 0 0 0.85 0.85 {layer=4}
T {Block 07 — 12 MOSFETs + 1 Resistor} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {pvdd, gnd  |  design.cir .subckt zener_clamp} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="Claude / analog-ai-chips"}

* ============================================================
* PORT PINS
* ============================================================
T {PORT PINS} -600 -940 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -900 0 0 {name=p1 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -860 0 0 {name=p2 lab=gnd}
* ============================================================
* PRECISION N-P-N-P-N STACK
* ============================================================
T {PRECISION N-P-N-P-N STACK} -320 -750 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -200 -600 0 0 {name=XMd1 L=4e-06 W=2.2e-06 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMd1} -225 -650 0 0 0.22 0.22 {layer=13}
T {N: W=2.2e-06 L=4e-06} -225 -635 0 0 0.18 0.18 {layer=5}
N -220 -600 -260 -600 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -260 -600 0 0 {name=lb1 sig_type=std_logic lab=pvdd}
N -180 -600 -150 -600 {lab=n4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 -600 2 0 {name=lb2 sig_type=std_logic lab=n4}
N -180 -630 -180 -670 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -670 2 0 {name=lb3 sig_type=std_logic lab=pvdd}
N -180 -570 -180 -550 {lab=n4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -550 2 0 {name=lb4 sig_type=std_logic lab=n4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -200 -440 0 0 {name=XMd2 L=4e-06 W=2e-05 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMd2} -225 -490 0 0 0.22 0.22 {layer=13}
T {P: W=2e-05 L=4e-06} -225 -475 0 0 0.18 0.18 {layer=5}
N -220 -440 -260 -440 {lab=n3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -260 -440 0 0 {name=lb5 sig_type=std_logic lab=n3}
N -180 -440 -150 -440 {lab=n4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 -440 2 0 {name=lb6 sig_type=std_logic lab=n4}
N -180 -470 -180 -490 {lab=n4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -490 2 0 {name=lb7 sig_type=std_logic lab=n4}
N -180 -410 -180 -390 {lab=n3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -390 2 0 {name=lb8 sig_type=std_logic lab=n3}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -200 -280 0 0 {name=XMd3 L=4e-06 W=2.2e-06 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMd3} -225 -330 0 0 0.22 0.22 {layer=13}
T {N: W=2.2e-06 L=4e-06} -225 -315 0 0 0.18 0.18 {layer=5}
N -220 -280 -260 -280 {lab=n3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -260 -280 0 0 {name=lb9 sig_type=std_logic lab=n3}
N -180 -280 -150 -280 {lab=n2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 -280 2 0 {name=lb10 sig_type=std_logic lab=n2}
N -180 -310 -180 -330 {lab=n3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -330 2 0 {name=lb11 sig_type=std_logic lab=n3}
N -180 -250 -180 -230 {lab=n2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -230 2 0 {name=lb12 sig_type=std_logic lab=n2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -200 -120 0 0 {name=XMd4 L=4e-06 W=2e-05 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMd4} -225 -170 0 0 0.22 0.22 {layer=13}
T {P: W=2e-05 L=4e-06} -225 -155 0 0 0.18 0.18 {layer=5}
N -220 -120 -260 -120 {lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -260 -120 0 0 {name=lb13 sig_type=std_logic lab=n1}
N -180 -120 -150 -120 {lab=n2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 -120 2 0 {name=lb14 sig_type=std_logic lab=n2}
N -180 -150 -180 -170 {lab=n2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -170 2 0 {name=lb15 sig_type=std_logic lab=n2}
N -180 -90 -180 -70 {lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -70 2 0 {name=lb16 sig_type=std_logic lab=n1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -200 40 0 0 {name=XMd5 L=4e-06 W=2.2e-06 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMd5} -225 -10 0 0 0.22 0.22 {layer=13}
T {N: W=2.2e-06 L=4e-06} -225 5 0 0 0.18 0.18 {layer=5}
N -220 40 -260 40 {lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -260 40 0 0 {name=lb17 sig_type=std_logic lab=n1}
N -180 40 -150 40 {lab=vg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 40 2 0 {name=lb18 sig_type=std_logic lab=vg}
N -180 10 -180 -10 {lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -10 2 0 {name=lb19 sig_type=std_logic lab=n1}
N -180 70 -180 90 {lab=vg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 90 2 0 {name=lb20 sig_type=std_logic lab=vg}
C {/usr/share/xschem/xschem_library/devices/res.sym} -200 230 0 0 {name=Rpd value=500k}
T {Rpd} -180 210 0 0 0.2 0.2 {layer=13}
T {500k} -180 238 0 0 0.18 0.18 {layer=5}
N -200 200 -200 165 {lab=vg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 165 2 0 {name=lb21 sig_type=std_logic lab=vg}
N -200 260 -200 295 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 295 2 0 {name=lb22 sig_type=std_logic lab=gnd}
* ============================================================
* CLAMP NFET
* ============================================================
T {CLAMP NFET} 170 -750 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 250 -200 0 0 {name=XMclamp L=5e-07 W=0.0001 nf=1 mult=4 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMclamp} 225 -250 0 0 0.22 0.22 {layer=13}
T {N: W=0.0001 L=5e-07 m=4} 225 -235 0 0 0.18 0.18 {layer=5}
N 230 -200 190 -200 {lab=vg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 190 -200 0 0 {name=lb23 sig_type=std_logic lab=vg}
N 270 -200 300 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -200 2 0 {name=lb24 sig_type=std_logic lab=gnd}
N 270 -230 270 -270 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 -270 2 0 {name=lb25 sig_type=std_logic lab=pvdd}
N 270 -170 270 -130 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 -130 2 0 {name=lb26 sig_type=std_logic lab=gnd}
* ============================================================
* FAST DIODE STACK (7x)
* ============================================================
T {FAST DIODE STACK (7x)} 530 -750 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 650 -600 0 0 {name=XMf1 L=5e-07 W=1e-05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf1} 625 -650 0 0 0.22 0.22 {layer=13}
T {N: W=1e-05 L=5e-07} 625 -635 0 0 0.18 0.18 {layer=5}
N 630 -600 590 -600 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -600 0 0 {name=lb27 sig_type=std_logic lab=pvdd}
N 670 -600 700 -600 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -600 2 0 {name=lb28 sig_type=std_logic lab=gnd}
N 670 -630 670 -650 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -650 2 0 {name=lb29 sig_type=std_logic lab=pvdd}
N 670 -570 670 -550 {lab=nf6}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -550 2 0 {name=lb30 sig_type=std_logic lab=nf6}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 650 -460 0 0 {name=XMf2 L=5e-07 W=1e-05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf2} 625 -510 0 0 0.22 0.22 {layer=13}
T {N: W=1e-05 L=5e-07} 625 -495 0 0 0.18 0.18 {layer=5}
N 630 -460 590 -460 {lab=nf6}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -460 0 0 {name=lb31 sig_type=std_logic lab=nf6}
N 670 -460 700 -460 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -460 2 0 {name=lb32 sig_type=std_logic lab=gnd}
N 670 -490 670 -510 {lab=nf6}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -510 2 0 {name=lb33 sig_type=std_logic lab=nf6}
N 670 -430 670 -410 {lab=nf5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -410 2 0 {name=lb34 sig_type=std_logic lab=nf5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 650 -320 0 0 {name=XMf3 L=5e-07 W=1e-05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf3} 625 -370 0 0 0.22 0.22 {layer=13}
T {N: W=1e-05 L=5e-07} 625 -355 0 0 0.18 0.18 {layer=5}
N 630 -320 590 -320 {lab=nf5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -320 0 0 {name=lb35 sig_type=std_logic lab=nf5}
N 670 -320 700 -320 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -320 2 0 {name=lb36 sig_type=std_logic lab=gnd}
N 670 -350 670 -370 {lab=nf5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -370 2 0 {name=lb37 sig_type=std_logic lab=nf5}
N 670 -290 670 -270 {lab=nf4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -270 2 0 {name=lb38 sig_type=std_logic lab=nf4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 650 -180 0 0 {name=XMf4 L=5e-07 W=1e-05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf4} 625 -230 0 0 0.22 0.22 {layer=13}
T {N: W=1e-05 L=5e-07} 625 -215 0 0 0.18 0.18 {layer=5}
N 630 -180 590 -180 {lab=nf4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -180 0 0 {name=lb39 sig_type=std_logic lab=nf4}
N 670 -180 700 -180 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -180 2 0 {name=lb40 sig_type=std_logic lab=gnd}
N 670 -210 670 -230 {lab=nf4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -230 2 0 {name=lb41 sig_type=std_logic lab=nf4}
N 670 -150 670 -130 {lab=nf3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -130 2 0 {name=lb42 sig_type=std_logic lab=nf3}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 650 -40 0 0 {name=XMf5 L=5e-07 W=1e-05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf5} 625 -90 0 0 0.22 0.22 {layer=13}
T {N: W=1e-05 L=5e-07} 625 -75 0 0 0.18 0.18 {layer=5}
N 630 -40 590 -40 {lab=nf3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -40 0 0 {name=lb43 sig_type=std_logic lab=nf3}
N 670 -40 700 -40 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -40 2 0 {name=lb44 sig_type=std_logic lab=gnd}
N 670 -70 670 -90 {lab=nf3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -90 2 0 {name=lb45 sig_type=std_logic lab=nf3}
N 670 -10 670 10 {lab=nf2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 10 2 0 {name=lb46 sig_type=std_logic lab=nf2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 650 100 0 0 {name=XMf6 L=5e-07 W=1e-05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf6} 625 50 0 0 0.22 0.22 {layer=13}
T {N: W=1e-05 L=5e-07} 625 65 0 0 0.18 0.18 {layer=5}
N 630 100 590 100 {lab=nf2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 100 0 0 {name=lb47 sig_type=std_logic lab=nf2}
N 670 100 700 100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 100 2 0 {name=lb48 sig_type=std_logic lab=gnd}
N 670 70 670 50 {lab=nf2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 50 2 0 {name=lb49 sig_type=std_logic lab=nf2}
N 670 130 670 150 {lab=nf1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 150 2 0 {name=lb50 sig_type=std_logic lab=nf1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 650 240 0 0 {name=XMf7 L=5e-07 W=1e-05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf7} 625 190 0 0 0.22 0.22 {layer=13}
T {N: W=1e-05 L=5e-07} 625 205 0 0 0.18 0.18 {layer=5}
N 630 240 590 240 {lab=nf1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 240 0 0 {name=lb51 sig_type=std_logic lab=nf1}
N 670 240 700 240 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 240 2 0 {name=lb52 sig_type=std_logic lab=gnd}
N 670 210 670 190 {lab=nf1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 190 2 0 {name=lb53 sig_type=std_logic lab=nf1}
N 670 270 670 290 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 290 2 0 {name=lb54 sig_type=std_logic lab=gnd}
L 5 -350 -700 0 -700 {dash=5}
L 5 0 -700 0 350 {dash=5}
L 5 0 350 -350 350 {dash=5}
L 5 -350 350 -350 -700 {dash=5}
L 4 100 -350 420 -350 {dash=5}
L 4 420 -350 420 -50 {dash=5}
L 4 420 -50 100 -50 {dash=5}
L 4 100 -50 100 -350 {dash=5}
L 7 500 -700 850 -700 {dash=5}
L 7 850 -700 850 410 {dash=5}
L 7 850 410 500 410 {dash=5}
L 7 500 410 500 -700 {dash=5}
