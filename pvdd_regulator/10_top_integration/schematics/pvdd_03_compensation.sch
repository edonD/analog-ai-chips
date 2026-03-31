v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {Block 03: Compensation Network} -300 -1200 0 0 0.85 0.85 {layer=4}
T {Miller Cc ~ 30 pF  |  Rz ~ 5 kOhm  |  Cout ~ 70 pF} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {.subckt compensation vout_gate pvdd gnd} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="PVDD LDO — Compensation"}

* ============================================================
* Ports
* ============================================================
T {Ports} -250 -900 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -250 -850 0 0 {name=p1 lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -800 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -750 0 0 {name=p3 lab=gnd}
* ============================================================
* Miller Compensation: Cc + Rz
* ============================================================
T {Miller Compensation: Cc + Rz} 20 -450 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 100 -200 0 0 {name=XCc W=122 L=122 MF=1 model=cap_mim_m3_1 spiceprefix=X}
T {XCc} 120 -225 0 0 0.2 0.2 {layer=13}
T {122x122} 120 -190 0 0 0.17 0.17 {layer=5}
N 100 -230 100 -265 {lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -265 2 0 {name=lb1 sig_type=std_logic lab=vout_gate}
N 100 -170 100 -135 {lab=cc_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -135 2 0 {name=lb2 sig_type=std_logic lab=cc_mid}
T {Cc ~ 30 pF} 70 -110 0 0 0.28 0.28 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 550 -200 0 0 {name=XRz W=4 L=10 model=res_xhigh_po spiceprefix=X}
T {XRz} 570 -225 0 0 0.2 0.2 {layer=13}
T {W=4 L=10} 570 -190 0 0 0.17 0.17 {layer=5}
N 550 -230 550 -265 {lab=cc_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 -265 2 0 {name=lb3 sig_type=std_logic lab=cc_mid}
N 550 -170 550 -135 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 -135 2 0 {name=lb4 sig_type=std_logic lab=pvdd}
N 530 -200 505 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 505 -200 0 0 {name=lb5 sig_type=std_logic lab=gnd}
T {Rz ~ 5 kOhm} 530 -110 0 0 0.28 0.28 {layer=4}
N 100 -135 100 -80 {lab=cc_mid}
N 100 -80 550 -80 {lab=cc_mid}
N 550 -80 550 -135 {lab=cc_mid}
* ============================================================
* Output Capacitor: Cout
* ============================================================
T {Output Capacitor: Cout} 970 -450 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 1050 -200 0 0 {name=XCout W=187 L=187 MF=1 model=cap_mim_m3_1 spiceprefix=X}
T {XCout} 1070 -225 0 0 0.2 0.2 {layer=13}
T {187x187} 1070 -190 0 0 0.17 0.17 {layer=5}
N 1050 -230 1050 -265 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -265 2 0 {name=lb6 sig_type=std_logic lab=pvdd}
N 1050 -170 1050 -135 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -135 2 0 {name=lb7 sig_type=std_logic lab=gnd}
T {Cout ~ 70 pF} 1020 -110 0 0 0.28 0.28 {layer=4}
T {vout_gate (ea_out)} 60 -330 0 0 0.25 0.25 {layer=8}
T {Cc  ──►  Rz  ──►  pvdd} 275 -20 0 0 0.3 0.3 {layer=8}
T {Miller compensation with zero-nulling resistor} 245 20 0 0 0.25 0.25 {layer=8}
L 8 20 -400 650 -400 {dash=5}
L 8 650 -400 650 -50 {dash=5}
L 8 650 -50 20 -50 {dash=5}
L 8 20 -50 20 -400 {dash=5}
L 8 970 -400 1150 -400 {dash=5}
L 8 1150 -400 1150 -50 {dash=5}
L 8 1150 -50 970 -50 {dash=5}
L 8 970 -50 970 -400 {dash=5}
