v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {Block 01: Pass Device} -300 -1200 0 0 0.85 0.85 {layer=4}
T {10x PMOS pfet_g5v0d10v5  W=100u L=0.5u  |  Total W = 1 mm} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {.subckt pass_device gate bvdd pvdd} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="PVDD LDO — Pass Device Array"}

* ============================================================
* Ports
* ============================================================
T {Ports} -250 -900 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -250 -850 0 0 {name=p1 lab=gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -800 0 0 {name=p2 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -250 -750 0 0 {name=p3 lab=pvdd}
* ============================================================
* Row 1: XM1 – XM5
* ============================================================
T {Row 1: XM1 – XM5} -50 -600 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 0 -400 0 0 {name=XM1 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM1} -25 -450 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} -25 -435 0 0 0.18 0.18 {layer=5}
N -20 -400 -60 -400 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -60 -400 0 0 {name=lb1 sig_type=std_logic lab=gate}
N 20 -400 50 -400 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 50 -400 2 0 {name=lb2 sig_type=std_logic lab=bvdd}
N 20 -430 20 -470 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -470 2 0 {name=lb3 sig_type=std_logic lab=bvdd}
N 20 -370 20 -330 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -330 2 0 {name=lb4 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 400 -400 0 0 {name=XM2 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM2} 375 -450 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} 375 -435 0 0 0.18 0.18 {layer=5}
N 380 -400 340 -400 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -400 0 0 {name=lb5 sig_type=std_logic lab=gate}
N 420 -400 450 -400 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 450 -400 2 0 {name=lb6 sig_type=std_logic lab=bvdd}
N 420 -430 420 -470 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -470 2 0 {name=lb7 sig_type=std_logic lab=bvdd}
N 420 -370 420 -330 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -330 2 0 {name=lb8 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 800 -400 0 0 {name=XM3 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM3} 775 -450 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} 775 -435 0 0 0.18 0.18 {layer=5}
N 780 -400 740 -400 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 740 -400 0 0 {name=lb9 sig_type=std_logic lab=gate}
N 820 -400 850 -400 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 850 -400 2 0 {name=lb10 sig_type=std_logic lab=bvdd}
N 820 -430 820 -470 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 -470 2 0 {name=lb11 sig_type=std_logic lab=bvdd}
N 820 -370 820 -330 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 -330 2 0 {name=lb12 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1200 -400 0 0 {name=XM4 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM4} 1175 -450 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} 1175 -435 0 0 0.18 0.18 {layer=5}
N 1180 -400 1140 -400 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1140 -400 0 0 {name=lb13 sig_type=std_logic lab=gate}
N 1220 -400 1250 -400 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 -400 2 0 {name=lb14 sig_type=std_logic lab=bvdd}
N 1220 -430 1220 -470 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -470 2 0 {name=lb15 sig_type=std_logic lab=bvdd}
N 1220 -370 1220 -330 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -330 2 0 {name=lb16 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1600 -400 0 0 {name=XM5 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM5} 1575 -450 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} 1575 -435 0 0 0.18 0.18 {layer=5}
N 1580 -400 1540 -400 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1540 -400 0 0 {name=lb17 sig_type=std_logic lab=gate}
N 1620 -400 1650 -400 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1650 -400 2 0 {name=lb18 sig_type=std_logic lab=bvdd}
N 1620 -430 1620 -470 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 -470 2 0 {name=lb19 sig_type=std_logic lab=bvdd}
N 1620 -370 1620 -330 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 -330 2 0 {name=lb20 sig_type=std_logic lab=pvdd}
* ============================================================
* Row 2: XM6 – XM10
* ============================================================
T {Row 2: XM6 – XM10} -50 -100 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 0 100 0 0 {name=XM6 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM6} -25 50 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} -25 65 0 0 0.18 0.18 {layer=5}
N -20 100 -60 100 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -60 100 0 0 {name=lb21 sig_type=std_logic lab=gate}
N 20 100 50 100 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 50 100 2 0 {name=lb22 sig_type=std_logic lab=bvdd}
N 20 70 20 30 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 30 2 0 {name=lb23 sig_type=std_logic lab=bvdd}
N 20 130 20 170 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 170 2 0 {name=lb24 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 400 100 0 0 {name=XM7 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM7} 375 50 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} 375 65 0 0 0.18 0.18 {layer=5}
N 380 100 340 100 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 100 0 0 {name=lb25 sig_type=std_logic lab=gate}
N 420 100 450 100 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 450 100 2 0 {name=lb26 sig_type=std_logic lab=bvdd}
N 420 70 420 30 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 30 2 0 {name=lb27 sig_type=std_logic lab=bvdd}
N 420 130 420 170 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 170 2 0 {name=lb28 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 800 100 0 0 {name=XM8 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM8} 775 50 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} 775 65 0 0 0.18 0.18 {layer=5}
N 780 100 740 100 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 740 100 0 0 {name=lb29 sig_type=std_logic lab=gate}
N 820 100 850 100 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 850 100 2 0 {name=lb30 sig_type=std_logic lab=bvdd}
N 820 70 820 30 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 30 2 0 {name=lb31 sig_type=std_logic lab=bvdd}
N 820 130 820 170 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 170 2 0 {name=lb32 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1200 100 0 0 {name=XM9 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM9} 1175 50 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} 1175 65 0 0 0.18 0.18 {layer=5}
N 1180 100 1140 100 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1140 100 0 0 {name=lb33 sig_type=std_logic lab=gate}
N 1220 100 1250 100 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 100 2 0 {name=lb34 sig_type=std_logic lab=bvdd}
N 1220 70 1220 30 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 30 2 0 {name=lb35 sig_type=std_logic lab=bvdd}
N 1220 130 1220 170 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 170 2 0 {name=lb36 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1600 100 0 0 {name=XM10 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM10} 1575 50 0 0 0.22 0.22 {layer=13}
T {P: W=100 L=0.5} 1575 65 0 0 0.18 0.18 {layer=5}
N 1580 100 1540 100 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1540 100 0 0 {name=lb37 sig_type=std_logic lab=gate}
N 1620 100 1650 100 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1650 100 2 0 {name=lb38 sig_type=std_logic lab=bvdd}
N 1620 70 1620 30 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 30 2 0 {name=lb39 sig_type=std_logic lab=bvdd}
N 1620 130 1620 170 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 170 2 0 {name=lb40 sig_type=std_logic lab=pvdd}

* ============================================================
* Supply Rails
* ============================================================
T {Supply Rails} -100 -650 0 0 0.35 0.35 {layer=4}
N -30 -470 1670 -470 {lab=bvdd}
N -30 30 1670 30 {lab=bvdd}
N -30 -330 1670 -330 {lab=pvdd}
N -30 170 1670 170 {lab=pvdd}
N -90 -400 1570 -400 {lab=gate}
N -90 100 1570 100 {lab=gate}
N -90 -400 -90 100 {lab=gate}
T {10x PMOS  W=100u  L=0.5u} 0 300 0 0 0.4 0.4 {layer=4}
T {Total W = 1 mm  —  Pass Device for PVDD 5V LDO} 0 350 0 0 0.3 0.3 {layer=8}
L 8 -150 -680 1720 -680 {dash=5}
L 8 1720 -680 1720 270 {dash=5}
L 8 1720 270 -150 270 {dash=5}
L 8 -150 270 -150 -680 {dash=5}
