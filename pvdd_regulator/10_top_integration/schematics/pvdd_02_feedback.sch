v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {Block 02: Feedback Network} -300 -1200 0 0 0.85 0.85 {layer=4}
T {Resistive divider: R_TOP=364k, R_BOT=118k  |  vfb = 1.226 V} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {.subckt feedback_network pvdd vfb gnd} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="PVDD LDO — Feedback Divider"}

* ============================================================
* Ports
* ============================================================
T {Ports} -250 -900 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -850 0 0 {name=p1 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -250 -800 0 0 {name=p2 lab=vfb}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -750 0 0 {name=p3 lab=gnd}
* ============================================================
* R_TOP: 364 kOhm
* ============================================================
T {R_TOP: 364 kOhm} 250 -470 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 400 -350 0 0 {name=XR_TOP W=3.0 L=536 model=res_xhigh_po spiceprefix=X}
T {XR_TOP} 420 -375 0 0 0.2 0.2 {layer=13}
T {W=3.0 L=536} 420 -340 0 0 0.17 0.17 {layer=5}
N 400 -380 400 -415 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -415 2 0 {name=lb1 sig_type=std_logic lab=pvdd}
N 400 -320 400 -285 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -285 2 0 {name=lb2 sig_type=std_logic lab=vfb}
N 380 -350 355 -350 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 355 -350 0 0 {name=lb3 sig_type=std_logic lab=gnd}
T {R_TOP ~ 364 kOhm} 460 -360 0 0 0.28 0.28 {layer=4}
* ============================================================
* R_BOT: 118 kOhm
* ============================================================
T {R_BOT: 118 kOhm} 250 30 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 400 150 0 0 {name=XR_BOT W=3.0 L=174.3 model=res_xhigh_po spiceprefix=X}
T {XR_BOT} 420 125 0 0 0.2 0.2 {layer=13}
T {W=3.0 L=174.3} 420 160 0 0 0.17 0.17 {layer=5}
N 400 120 400 85 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 85 2 0 {name=lb4 sig_type=std_logic lab=vfb}
N 400 180 400 215 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 215 2 0 {name=lb5 sig_type=std_logic lab=gnd}
N 380 150 355 150 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 355 150 0 0 {name=lb6 sig_type=std_logic lab=gnd}
T {R_BOT ~ 118 kOhm} 460 140 0 0 0.28 0.28 {layer=4}
N 400 -285 400 85 {lab=vfb}
N 400 -415 400 -480 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -480 2 0 {name=lb7 sig_type=std_logic lab=pvdd}
N 400 215 400 280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 280 2 0 {name=lb8 sig_type=std_logic lab=gnd}
T {vfb} 425 -115 0 0 0.35 0.35 {layer=4}
T {vfb = pvdd x 118 / (364 + 118) = 1.226 V} 300 370 0 0 0.32 0.32 {layer=8}
T {(at pvdd = 5.0 V nominal)} 300 410 0 0 0.25 0.25 {layer=8}
L 8 280 -530 650 -530 {dash=5}
L 8 650 -530 650 330 {dash=5}
L 8 650 330 280 330 {dash=5}
L 8 280 330 280 -530 {dash=5}
