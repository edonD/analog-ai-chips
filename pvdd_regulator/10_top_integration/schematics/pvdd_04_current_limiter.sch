v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {Block 04: Current Limiter} -300 -1200 0 0 0.85 0.85 {layer=4}
T {Sense PMOS + Rs  |  Detect NFET + Rpu  |  Gate Clamp  |  Flag Inverter} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {.subckt current_limiter gate bvdd pvdd gnd ilim_flag} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="PVDD LDO — Over-Current Protection"}

* ============================================================
* Ports
* ============================================================
T {Ports} -300 -950 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -900 0 0 {name=p1 lab=gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -300 -850 0 0 {name=p2 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -300 -800 0 0 {name=p3 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -300 -750 0 0 {name=p4 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -300 -700 0 0 {name=p5 lab=ilim_flag}
* ============================================================
* Sense: XMs + XRs
* ============================================================
T {Sense: XMs + XRs} 0 -600 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 100 -350 0 0 {name=XMs L=0.5 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMs} 75 -400 0 0 0.22 0.22 {layer=13}
T {P: W=2 L=0.5} 75 -385 0 0 0.18 0.18 {layer=5}
N 80 -350 40 -350 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -350 0 0 {name=lb1 sig_type=std_logic lab=gate}
N 120 -350 150 -350 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -350 2 0 {name=lb2 sig_type=std_logic lab=bvdd}
N 120 -380 120 -420 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 -420 2 0 {name=lb3 sig_type=std_logic lab=bvdd}
N 120 -320 120 -280 {lab=sense_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 -280 2 0 {name=lb4 sig_type=std_logic lab=sense_n}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 120 200 0 0 {name=XRs W=1 L=3.12 model=res_xhigh_po spiceprefix=X}
T {XRs} 140 175 0 0 0.2 0.2 {layer=13}
T {W=1 L=3.12} 140 210 0 0 0.17 0.17 {layer=5}
N 120 170 120 135 {lab=sense_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 135 2 0 {name=lb5 sig_type=std_logic lab=sense_n}
N 120 230 120 265 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 265 2 0 {name=lb6 sig_type=std_logic lab=gnd}
N 100 200 75 200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 75 200 0 0 {name=lb7 sig_type=std_logic lab=gnd}
T {Rs (sense)} 150 190 0 0 0.22 0.22 {layer=4}
N 120 -280 120 135 {lab=sense_n}
* ============================================================
* Detect: XMdet + XRpu
* ============================================================
T {Detect: XMdet + XRpu} 450 -600 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 550 -350 0 0 {name=XMdet L=1 W=5 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMdet} 525 -400 0 0 0.22 0.22 {layer=13}
T {N: W=5 L=1} 525 -385 0 0 0.18 0.18 {layer=5}
N 530 -350 490 -350 {lab=sense_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 490 -350 0 0 {name=lb8 sig_type=std_logic lab=sense_n}
N 570 -350 600 -350 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -350 2 0 {name=lb9 sig_type=std_logic lab=gnd}
N 570 -380 570 -420 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 -420 2 0 {name=lb10 sig_type=std_logic lab=det_n}
N 570 -320 570 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 -280 2 0 {name=lb11 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 570 -600 0 0 {name=XRpu W=1 L=5 model=res_xhigh_po spiceprefix=X}
T {XRpu} 590 -625 0 0 0.2 0.2 {layer=13}
T {W=1 L=5} 590 -590 0 0 0.17 0.17 {layer=5}
N 570 -630 570 -665 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 -665 2 0 {name=lb12 sig_type=std_logic lab=bvdd}
N 570 -570 570 -535 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 -535 2 0 {name=lb13 sig_type=std_logic lab=det_n}
N 550 -600 525 -600 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 525 -600 0 0 {name=lb14 sig_type=std_logic lab=gnd}
T {Rpu (pull-up)} 600 -610 0 0 0.22 0.22 {layer=4}
* ============================================================
* Clamp: XMclamp
* ============================================================
T {Clamp: XMclamp} 900 -600 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1000 -350 0 0 {name=XMclamp L=1 W=20 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMclamp} 975 -400 0 0 0.22 0.22 {layer=13}
T {P: W=20 L=1} 975 -385 0 0 0.18 0.18 {layer=5}
N 980 -350 940 -350 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -350 0 0 {name=lb15 sig_type=std_logic lab=det_n}
N 1020 -350 1050 -350 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -350 2 0 {name=lb16 sig_type=std_logic lab=bvdd}
N 1020 -380 1020 -420 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1020 -420 2 0 {name=lb17 sig_type=std_logic lab=bvdd}
N 1020 -320 1020 -280 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1020 -280 2 0 {name=lb18 sig_type=std_logic lab=gate}
T {Gate clamp} 970 -250 0 0 0.25 0.25 {layer=4}
T {Pulls gate toward bvdd} 950 -215 0 0 0.2 0.2 {layer=8}
T {when Ilim tripped} 950 -185 0 0 0.2 0.2 {layer=8}
* ============================================================
* Flag Inverter: XMfp / XMfn
* ============================================================
T {Flag Inverter: XMfp / XMfn} 1350 -600 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1450 -400 0 0 {name=XMfp L=1 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMfp} 1425 -450 0 0 0.22 0.22 {layer=13}
T {P: W=2 L=1} 1425 -435 0 0 0.18 0.18 {layer=5}
N 1430 -400 1390 -400 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1390 -400 0 0 {name=lb19 sig_type=std_logic lab=det_n}
N 1470 -400 1500 -400 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -400 2 0 {name=lb20 sig_type=std_logic lab=pvdd}
N 1470 -430 1470 -470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1470 -470 2 0 {name=lb21 sig_type=std_logic lab=pvdd}
N 1470 -370 1470 -330 {lab=ilim_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1470 -330 2 0 {name=lb22 sig_type=std_logic lab=ilim_flag}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1450 50 0 0 {name=XMfn L=1 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMfn} 1425 0 0 0 0.22 0.22 {layer=13}
T {N: W=2 L=1} 1425 15 0 0 0.18 0.18 {layer=5}
N 1430 50 1390 50 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1390 50 0 0 {name=lb23 sig_type=std_logic lab=det_n}
N 1470 50 1500 50 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 50 2 0 {name=lb24 sig_type=std_logic lab=gnd}
N 1470 20 1470 -20 {lab=ilim_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1470 -20 2 0 {name=lb25 sig_type=std_logic lab=ilim_flag}
N 1470 80 1470 120 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1470 120 2 0 {name=lb26 sig_type=std_logic lab=gnd}
N 1470 -330 1470 -20 {lab=ilim_flag}
T {ilim_flag} 1500 -175 0 0 0.28 0.28 {layer=4}
T {HIGH = current limit active} 1430 180 0 0 0.22 0.22 {layer=8}
L 8 -30 -500 260 -500 {dash=5}
L 8 260 -500 260 320 {dash=5}
L 8 260 320 -30 320 {dash=5}
L 8 -30 320 -30 -500 {dash=5}
L 8 420 -730 710 -730 {dash=5}
L 8 710 -730 710 -230 {dash=5}
L 8 710 -230 420 -230 {dash=5}
L 8 420 -230 420 -730 {dash=5}
L 8 870 -500 1160 -500 {dash=5}
L 8 1160 -500 1160 -230 {dash=5}
L 8 1160 -230 870 -230 {dash=5}
L 8 870 -230 870 -500 {dash=5}
L 8 1320 -550 1610 -550 {dash=5}
L 8 1610 -550 1610 170 {dash=5}
L 8 1610 170 1320 170 {dash=5}
L 8 1320 170 1320 -550 {dash=5}
T {OCP: If load current causes Vs(sense_n) > Vth(XMdet), det_n goes LOW,} 0 450 0 0 0.25 0.25 {layer=8}
T {XMclamp turns ON pulling gate toward bvdd (limiting Ids), flag goes HIGH.} 0 490 0 0 0.25 0.25 {layer=8}
