v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 07: SAR ADC v3 — 8-bit Cap DAC} -500 -1500 0 0 1.0 1.0 {layer=15}
T {Binary-Weighted Charge-Redistribution DAC  —  SKY130A} -500 -1440 0 0 0.5 0.5 {layer=15}
T {Cunit = 200 fF  |  Total = 256 x Cunit = 51.2 pF  |  1 dummy cap} -500 -1390 0 0 0.4 0.4 {layer=8}
T {Top Plate} -500 -1310 0 0 0.5 0.5 {layer=4}
T {Common node "top" — connects to comparator inp and sample switch} -500 -1270 0 0 0.3 0.3 {layer=8}
T {top (vtop)} -520 -1215 0 0 0.35 0.35 {layer=4}
T {Binary Capacitors} -500 -1060 0 0 0.5 0.5 {layer=4}
T {C128} -380 -1145 0 0 0.3 0.3 {layer=8}
T {128x200fF} -400 -1120 0 0 0.2 0.2 {layer=8}
T {= 25.6pF} -400 -1100 0 0 0.2 0.2 {layer=8}
T {C64} -200 -1145 0 0 0.3 0.3 {layer=8}
T {64x200fF} -220 -1120 0 0 0.2 0.2 {layer=8}
T {= 12.8pF} -220 -1100 0 0 0.2 0.2 {layer=8}
T {C32} -20 -1145 0 0 0.3 0.3 {layer=8}
T {32x200fF} -40 -1120 0 0 0.2 0.2 {layer=8}
T {= 6.4pF} -40 -1100 0 0 0.2 0.2 {layer=8}
T {C16} 160 -1145 0 0 0.3 0.3 {layer=8}
T {16x200fF} 140 -1120 0 0 0.2 0.2 {layer=8}
T {= 3.2pF} 140 -1100 0 0 0.2 0.2 {layer=8}
T {C8} 340 -1145 0 0 0.3 0.3 {layer=8}
T {8x200fF} 320 -1120 0 0 0.2 0.2 {layer=8}
T {= 1.6pF} 320 -1100 0 0 0.2 0.2 {layer=8}
T {C4} 520 -1145 0 0 0.3 0.3 {layer=8}
T {4x200fF} 500 -1120 0 0 0.2 0.2 {layer=8}
T {= 800fF} 500 -1100 0 0 0.2 0.2 {layer=8}
T {C2} 700 -1145 0 0 0.3 0.3 {layer=8}
T {2x200fF} 680 -1120 0 0 0.2 0.2 {layer=8}
T {= 400fF} 680 -1100 0 0 0.2 0.2 {layer=8}
T {C1} 880 -1145 0 0 0.3 0.3 {layer=8}
T {1x200fF} 860 -1120 0 0 0.2 0.2 {layer=8}
T {(LSB)} 860 -1100 0 0 0.2 0.2 {layer=8}
T {Cdummy} 1050 -1145 0 0 0.3 0.3 {layer=5}
T {1x200fF} 1030 -1120 0 0 0.2 0.2 {layer=5}
T {-> GND} 1030 -1100 0 0 0.2 0.2 {layer=5}
T {Bottom-Plate Switches} -500 -920 0 0 0.5 0.5 {layer=4}
T {Each bit: bit_sw subcircuit = 2 NMOS W=4u + 2 PMOS W=8u (CMOS TG pair)} -500 -880 0 0 0.3 0.3 {layer=8}
T {ctrl=HIGH -> bottom plate to Vref  |  ctrl=LOW -> bottom plate to GND} -500 -850 0 0 0.3 0.3 {layer=8}
T {Settling: MSB tau = Ron x Ceq ~ 400 x 12.8p = 5.1 ns  |  5tau << 100 ns (5 MHz)} -500 -820 0 0 0.25 0.25 {layer=5}
T {MSB Switch Detail (Xsw7 — bit_sw subcircuit)} -500 -760 0 0 0.4 0.4 {layer=4}
T {TG to Vref} -480 -700 0 0 0.3 0.3 {layer=8}
T {ON when sw7=HIGH, sw7_b=LOW} -480 -675 0 0 0.2 0.2 {layer=8}
T {M_vr_n} -410 -545 0 0 0.25 0.25 {layer=8}
T {NMOS 4/0.15} -415 -525 0 0 0.2 0.2 {layer=8}
T {M_vr_p} -240 -545 0 0 0.25 0.25 {layer=8}
T {PMOS 8/0.15} -245 -525 0 0 0.2 0.2 {layer=8}
T {TG to GND} 120 -700 0 0 0.3 0.3 {layer=8}
T {ON when sw7=LOW, sw7_b=HIGH} 120 -675 0 0 0.2 0.2 {layer=8}
T {M_gn_n} 190 -545 0 0 0.25 0.25 {layer=8}
T {NMOS 4/0.15} 185 -525 0 0 0.2 0.2 {layer=8}
T {M_gn_p} 360 -545 0 0 0.25 0.25 {layer=8}
T {PMOS 8/0.15} 355 -525 0 0 0.2 0.2 {layer=8}
T {Switches sw6..sw0: identical bit_sw subcircuits (not drawn)} -500 -400 0 0 0.3 0.3 {layer=8}
T {4 transistors per bit x 8 bits = 32 switch transistors total} -500 -370 0 0 0.25 0.25 {layer=5}
T {DC Convergence Aids} 600 -760 0 0 0.4 0.4 {layer=4}
T {Rleak per bottom node: 10 Gohm to GND} 600 -720 0 0 0.3 0.3 {layer=8}
T {Rleak_top: 100 Gohm to GND (top plate)} 600 -690 0 0 0.3 0.3 {layer=8}
T {At 100G: leakage = 12pA -> 0.05 LSB/conversion} 600 -660 0 0 0.25 0.25 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -360 -1170 0 0 {name=XC128
W=50
L=51.2
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -180 -1170 0 0 {name=XC64
W=50
L=25.6
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 0 -1170 0 0 {name=XC32
W=40
L=16
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 180 -1170 0 0 {name=XC16
W=28.28
L=11.32
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 360 -1170 0 0 {name=XC8
W=20
L=8
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 540 -1170 0 0 {name=XC4
W=14.14
L=5.66
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 720 -1170 0 0 {name=XC2
W=10
L=4
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 900 -1170 0 0 {name=XC1
W=7.07
L=2.83
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 1080 -1170 0 0 {name=XCdummy
W=7.07
L=2.83
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -400 -600 0 0 {name=XM_vr_n
W=4
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -200 -600 0 1 {name=XM_vr_p
W=8
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 200 -600 0 0 {name=XM_gn_n
W=4
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 400 -600 0 1 {name=XM_gn_p
W=8
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -1200 0 1 {name=p_top lab=top}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -960 0 1 {name=p_vref lab=vref}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -300 0 1 {name=p_gnd lab=gnd_node}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -260 0 1 {name=p_vdd lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -220 0 1 {name=p_vss lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -960 0 0 {name=p_sw7 lab=sw7}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -930 0 0 {name=p_sw7b lab=sw7_b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -900 0 0 {name=p_sw6 lab=sw6}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -870 0 0 {name=p_sw6b lab=sw6_b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -840 0 0 {name=p_sw5 lab=sw5}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -810 0 0 {name=p_sw5b lab=sw5_b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -780 0 0 {name=p_sw4 lab=sw4}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -750 0 0 {name=p_sw4b lab=sw4_b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -720 0 0 {name=p_sw3 lab=sw3}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -690 0 0 {name=p_sw3b lab=sw3_b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -660 0 0 {name=p_sw2 lab=sw2}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -630 0 0 {name=p_sw2b lab=sw2_b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -600 0 0 {name=p_sw1 lab=sw1}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -570 0 0 {name=p_sw1b lab=sw1_b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -540 0 0 {name=p_sw0 lab=sw0}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1200 -510 0 0 {name=p_sw0b lab=sw0_b}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -360 -1140 0 1 {name=l_bn7 lab=bn7}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -180 -1140 0 1 {name=l_bn6 lab=bn6}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 0 -1140 0 1 {name=l_bn5 lab=bn5}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 180 -1140 0 1 {name=l_bn4 lab=bn4}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 360 -1140 0 1 {name=l_bn3 lab=bn3}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 540 -1140 0 1 {name=l_bn2 lab=bn2}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 720 -1140 0 1 {name=l_bn1 lab=bn1}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 900 -1140 0 1 {name=l_bn0 lab=bn0}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1080 -1140 0 1 {name=l_gnd_dummy lab=gnd_node}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -420 -600 0 1 {name=l_gate_vrn lab=sw7}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -180 -600 0 0 {name=l_gate_vrp lab=sw7_b}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 180 -600 0 1 {name=l_gate_gnn lab=sw7_b}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 420 -600 0 0 {name=l_gate_gnp lab=sw7}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -380 -600 0 0 {name=l_bulk_vrn lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -220 -600 0 1 {name=l_bulk_vrp lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 220 -600 0 0 {name=l_bulk_gnn lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 380 -600 0 1 {name=l_bulk_gnp lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -300 -460 0 1 {name=l_bn7_sw lab=bn7}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 300 -460 0 1 {name=l_bn7_sw2 lab=bn7}
N -500 -1200 1120 -1200 {lab=top}
N -380 -630 -380 -660 {lab=vref}
N -380 -660 -220 -660 {lab=vref}
N -220 -660 -220 -630 {lab=vref}
N -380 -570 -380 -460 {lab=bn7}
N -380 -460 -220 -460 {lab=bn7}
N -220 -460 -220 -570 {lab=bn7}
N 220 -630 220 -660 {lab=gnd_node}
N 220 -660 380 -660 {lab=gnd_node}
N 380 -660 380 -630 {lab=gnd_node}
N 220 -570 220 -460 {lab=bn7}
N 220 -460 380 -460 {lab=bn7}
N 380 -460 380 -570 {lab=bn7}
N -300 -660 -300 -700 {lab=vref}
N 300 -660 300 -700 {lab=gnd_node}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -300 -700 0 0 {name=l_vref_sw lab=vref}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 300 -700 0 0 {name=l_gnd_sw lab=gnd_node}
