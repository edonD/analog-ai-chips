v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {Block 06: Level Shifter Up} -300 -1200 0 0 0.85 0.85 {layer=4}
T {1.8V to 5V level shift  |  HV g5v0d10v5 FETs} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {.subckt level_shifter_up in out bvdd svdd gnd} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="PVDD LDO — Level Shifter"}

* ============================================================
* Ports
* ============================================================
T {Ports} -250 -900 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -250 -850 0 0 {name=p1 lab=in}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -800 0 0 {name=p2 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -750 0 0 {name=p3 lab=svdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -700 0 0 {name=p4 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -250 -650 0 0 {name=p5 lab=out}
L 8 -100 -620 1150 -620 {dash=5}
L 8 1150 -620 1150 350 {dash=5}
L 8 1150 350 -100 350 {dash=5}
L 8 -100 350 -100 -620 {dash=5}
* ============================================================
* Input Inverter
* ============================================================
T {Input Inverter} 20 -500 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 100 100 0 0 {name=XMN_INV L=0.5 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN_INV} 75 50 0 0 0.22 0.22 {layer=13}
T {N: W=2 L=0.5} 75 65 0 0 0.18 0.18 {layer=5}
N 80 100 40 100 {lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 100 0 0 {name=lb1 sig_type=std_logic lab=in}
N 120 100 150 100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 100 2 0 {name=lb2 sig_type=std_logic lab=gnd}
N 120 70 120 30 {lab=in_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 30 2 0 {name=lb3 sig_type=std_logic lab=in_b}
N 120 130 120 170 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 170 2 0 {name=lb4 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 100 -250 0 0 {name=XMP_INV L=0.5 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMP_INV} 75 -300 0 0 0.22 0.22 {layer=13}
T {P: W=4 L=0.5} 75 -285 0 0 0.18 0.18 {layer=5}
N 80 -250 40 -250 {lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -250 0 0 {name=lb5 sig_type=std_logic lab=in}
N 120 -250 150 -250 {lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -250 2 0 {name=lb6 sig_type=std_logic lab=svdd}
N 120 -280 120 -320 {lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 -320 2 0 {name=lb7 sig_type=std_logic lab=svdd}
N 120 -220 120 -180 {lab=in_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 -180 2 0 {name=lb8 sig_type=std_logic lab=in_b}
* ============================================================
* NMOS Pull-downs
* ============================================================
T {NMOS Pull-downs} 370 -500 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 450 100 0 0 {name=XMN1 L=1 W=15 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN1} 425 50 0 0 0.22 0.22 {layer=13}
T {N: W=15 L=1} 425 65 0 0 0.18 0.18 {layer=5}
N 430 100 390 100 {lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 390 100 0 0 {name=lb9 sig_type=std_logic lab=in}
N 470 100 500 100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 100 2 0 {name=lb10 sig_type=std_logic lab=gnd}
N 470 70 470 30 {lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 30 2 0 {name=lb11 sig_type=std_logic lab=n1}
N 470 130 470 170 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 170 2 0 {name=lb12 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 730 100 0 0 {name=XMN2 L=1 W=15 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN2} 705 50 0 0 0.22 0.22 {layer=13}
T {N: W=15 L=1} 705 65 0 0 0.18 0.18 {layer=5}
N 710 100 670 100 {lab=in_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 100 0 0 {name=lb13 sig_type=std_logic lab=in_b}
N 750 100 780 100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 100 2 0 {name=lb14 sig_type=std_logic lab=gnd}
N 750 70 750 30 {lab=out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 30 2 0 {name=lb15 sig_type=std_logic lab=out}
N 750 130 750 170 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 170 2 0 {name=lb16 sig_type=std_logic lab=gnd}
* ============================================================
* Cross-coupled PMOS
* ============================================================
T {Cross-coupled PMOS} 370 -500 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 450 -300 0 0 {name=XMP1 L=0.5 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMP1} 425 -350 0 0 0.22 0.22 {layer=13}
T {P: W=4 L=0.5} 425 -335 0 0 0.18 0.18 {layer=5}
N 430 -300 390 -300 {lab=out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 390 -300 0 0 {name=lb17 sig_type=std_logic lab=out}
N 470 -300 500 -300 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -300 2 0 {name=lb18 sig_type=std_logic lab=bvdd}
N 470 -330 470 -370 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 -370 2 0 {name=lb19 sig_type=std_logic lab=bvdd}
N 470 -270 470 -230 {lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 -230 2 0 {name=lb20 sig_type=std_logic lab=n1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 730 -300 0 0 {name=XMP2 L=0.5 W=5 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMP2} 705 -350 0 0 0.22 0.22 {layer=13}
T {P: W=5 L=0.5} 705 -335 0 0 0.18 0.18 {layer=5}
N 710 -300 670 -300 {lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -300 0 0 {name=lb21 sig_type=std_logic lab=n1}
N 750 -300 780 -300 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -300 2 0 {name=lb22 sig_type=std_logic lab=bvdd}
N 750 -330 750 -370 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 -370 2 0 {name=lb23 sig_type=std_logic lab=bvdd}
N 750 -270 750 -230 {lab=out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 -230 2 0 {name=lb24 sig_type=std_logic lab=out}
T {Cross-coupled latch: XMP1.G=out, XMP2.G=n1} 400 -220 0 0 0.22 0.22 {layer=13}
T {Level Shifter: svdd(1.8V) -> bvdd(5V)} -50 300 0 0 0.3 0.3 {layer=8}
