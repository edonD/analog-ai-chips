v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 06: Charge-Domain MAC Classifier} -200 -1550 0 0 1.0 1.0 {layer=15}
T {8-Input x 4-Bit Weight MAC  |  StrongARM Comparator  |  3-Phase Clock  \u2014  SKY130A  |  1.8 V} -200 -1500 0 0 0.4 0.4 {layer=15}
T {~702 transistors  |  ~260 MIM caps  |  10/10 specs PASS in ngspice-42  |  0.08 LSB linearity  |  99.5% MC accuracy  |  < 1 nW @ 10 Hz} -200 -1465 0 0 0.3 0.3 {layer=8}
T {MAC Bit-Cell (Input 0, Bit 0 \u2014 representative)} -550 -1410 0 0 0.45 0.45 {layer=4}
T {x32 cells/MAC  x4 MACs  =  128 cells, ~702 transistors total} -550 -1380 0 0 0.25 0.25 {layer=8}
T {Sample TG} -540 -1340 0 0 0.3 0.3 {layer=4}
T {en = AND(phi_s, weight_bit)} -540 -1320 0 0 0.2 0.2 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -430 -1270 0 0 {name=XNt0b0
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {XNt0b0} -475 -1285 0 0 0.2 0.2 {layer=8}
T {0.84/0.15} -475 -1268 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -260 -1270 0 1 {name=XPt0b0
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {XPt0b0} -215 -1285 0 0 0.2 0.2 {layer=8}
T {1.68/0.15} -215 -1268 0 0 0.18 0.18 {layer=8}
N -410 -1300 -280 -1300 {lab=in0}
N -410 -1240 -280 -1240 {lab=top0b0}
N -345 -1300 -345 -1370 {lab=in0}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -460 -1270 0 1 {name=l_en0b0 lab=en0b0}
N -460 -1270 -450 -1270 {lab=en0b0}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -230 -1270 0 0 {name=l_en0b0b lab=en0b0b}
N -240 -1270 -230 -1270 {lab=en0b0b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -345 -1380 0 0 {name=p_in0 lab=in0}
T {Weight Cap} -420 -1200 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -380 -1155 0 0 {name=XC0b0
W=5
L=10
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
T {C0b0} -415 -1160 0 0 0.2 0.2 {layer=8}
T {50 fF} -415 -1143 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -250 -1155 0 0 {name=XCbp0b0
W=2.24
L=2.24
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
T {Cbp0b0} -215 -1160 0 0 0.2 0.2 {layer=8}
T {5 fF par.} -215 -1143 0 0 0.18 0.18 {layer=8}
N -345 -1240 -345 -1185 {lab=top0b0}
N -380 -1185 -250 -1185 {lab=top0b0}
N -380 -1125 -380 -1105 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -380 -1105 0 0 {name=l_vss_c1 lab=vss}
N -250 -1125 -250 -1105 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -250 -1105 0 0 {name=l_vss_c2 lab=vss}
T {Eval TG} -540 -1080 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -430 -1030 0 0 {name=XNe0b0
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {XNe0b0} -475 -1045 0 0 0.2 0.2 {layer=8}
T {0.84/0.15} -475 -1028 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -260 -1030 0 1 {name=XPe0b0
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {XPe0b0} -215 -1045 0 0 0.2 0.2 {layer=8}
T {1.68/0.15} -215 -1028 0 0 0.18 0.18 {layer=8}
N -410 -1060 -280 -1060 {lab=top0b0}
N -410 -1000 -280 -1000 {lab=bl}
N -345 -1185 -345 -1060 {lab=top0b0}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -460 -1030 0 1 {name=l_phi_e lab=phi_e}
N -460 -1030 -450 -1030 {lab=phi_e}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -230 -1030 0 0 {name=l_phi_eb lab=phi_eb}
N -240 -1030 -230 -1030 {lab=phi_eb}
T {Reset} -140 -1145 0 0 0.3 0.3 {layer=4}
T {XNr0b0} -140 -1125 0 0 0.2 0.2 {layer=8}
T {0.42/0.15} -140 -1108 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -120 -1080 0 0 {name=XNr0b0
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -155 -1080 0 1 {name=l_phi_r_r lab=phi_r}
N -155 -1080 -140 -1080 {lab=phi_r}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -100 -1120 0 0 {name=l_top0b0_r lab=top0b0}
N -100 -1110 -100 -1120 {lab=top0b0}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -100 -1060 0 0 {name=l_vss_r lab=vss}
N -100 -1050 -100 -1060 {lab=vss}
T {Bitline Reset} -540 -920 0 0 0.3 0.3 {layer=4}
T {XNblrst} -475 -900 0 0 0.2 0.2 {layer=8}
T {0.84/0.15} -475 -883 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -430 -870 0 0 {name=XNblrst
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -470 -870 0 1 {name=l_phi_r_bl lab=phi_r}
N -470 -870 -450 -870 {lab=phi_r}
T {Cpar} -270 -920 0 0 0.3 0.3 {layer=4}
T {80 fF routing} -270 -900 0 0 0.2 0.2 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -260 -870 0 0 {name=XCpar
W=8
L=10
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
N -345 -1000 -345 -900 {lab=bl}
N -410 -900 -260 -900 {lab=bl}
N -410 -840 -410 -480 {lab=vss}
N -260 -840 -260 -480 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -345 -950 0 1 {name=l_bl lab=bl}
N -550 -1430 -80 -1430 {lab=vdd}
N -550 -480 -80 -480 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -560 -1430 0 1 {name=p_vdd1 lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -560 -480 0 1 {name=p_vss1 lab=vss}
T {StrongARM Latch Comparator (10T)} 200 -1410 0 0 0.45 0.45 {layer=4}
T {CLK=0: Reset  |  CLK=1: Evaluate + Regenerate} 200 -1385 0 0 0.25 0.25 {layer=8}
N 200 -1430 900 -1430 {lab=vdd}
T {Reset} 230 -1345 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 265 -1300 0 0 {name=XM9
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {XM9} 228 -1308 0 0 0.18 0.18 {layer=8}
T {0.84/0.15} 223 -1293 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 395 -1300 0 0 {name=XM7
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {XM7} 358 -1308 0 0 0.18 0.18 {layer=8}
T {0.84/0.15} 353 -1293 0 0 0.15 0.15 {layer=8}
T {P-Latch} 475 -1345 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 500 -1300 0 0 {name=XM5
W=1.0
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {XM5} 463 -1308 0 0 0.18 0.18 {layer=8}
T {1/0.15} 463 -1293 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 620 -1300 0 1 {name=XM6
W=1.0
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {XM6} 643 -1308 0 0 0.18 0.18 {layer=8}
T {1/0.15} 643 -1293 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 725 -1300 0 1 {name=XM8
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {XM8} 748 -1308 0 0 0.18 0.18 {layer=8}
T {0.84/0.15} 748 -1293 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 855 -1300 0 1 {name=XM10
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {XM10} 878 -1308 0 0 0.18 0.18 {layer=8}
T {0.84/0.15} 878 -1293 0 0 0.15 0.15 {layer=8}
N 285 -1330 285 -1430 {lab=vdd}
N 415 -1330 415 -1430 {lab=vdd}
N 520 -1330 520 -1430 {lab=vdd}
N 600 -1330 600 -1430 {lab=vdd}
N 705 -1330 705 -1430 {lab=vdd}
N 835 -1330 835 -1430 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 230 -1300 0 1 {name=l_clk_245 lab=clk}
N 230 -1300 245 -1300 {lab=clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 360 -1300 0 1 {name=l_clk_375 lab=clk}
N 360 -1300 375 -1300 {lab=clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 760 -1300 0 0 {name=l_clk_745 lab=clk}
N 745 -1300 760 -1300 {lab=clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 890 -1300 0 0 {name=l_clk_875 lab=clk}
N 875 -1300 890 -1300 {lab=clk}
N 415 -1270 520 -1270 {lab=voutp}
N 600 -1270 705 -1270 {lab=voutn}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 285 -1258 0 0 {name=l_dip_m9 lab=di_p}
N 285 -1270 285 -1258 {lab=di_p}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 835 -1258 0 0 {name=l_din_m10 lab=di_n}
N 835 -1270 835 -1258 {lab=di_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 465 -1300 0 1 {name=l_voutn_g5 lab=voutn}
N 465 -1300 480 -1300 {lab=voutn}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 655 -1300 0 0 {name=l_voutp_g6 lab=voutp}
N 640 -1300 655 -1300 {lab=voutp}
T {N-Latch} 395 -1220 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 440 -1170 0 0 {name=XM3
W=1.0
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {XM3} 398 -1178 0 0 0.18 0.18 {layer=8}
T {1/0.15} 398 -1163 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 680 -1170 0 1 {name=XM4
W=1.0
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {XM4} 700 -1178 0 0 0.18 0.18 {layer=8}
T {1/0.15} 700 -1163 0 0 0.15 0.15 {layer=8}
N 460 -1200 460 -1270 {lab=voutp}
N 660 -1200 660 -1270 {lab=voutn}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 405 -1170 0 1 {name=l_voutn_g3 lab=voutn}
N 405 -1170 420 -1170 {lab=voutn}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 715 -1170 0 0 {name=l_voutp_g4 lab=voutp}
N 700 -1170 715 -1170 {lab=voutp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 468 -1253 0 0 {name=p_voutp lab=voutp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 652 -1253 0 0 {name=p_voutn lab=voutn}
T {Input Pair} 420 -1110 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 440 -1060 0 0 {name=XM1
W=4.0
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {XM1} 398 -1068 0 0 0.18 0.18 {layer=8}
T {4/0.5} 398 -1053 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 680 -1060 0 1 {name=XM2
W=4.0
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {XM2} 700 -1068 0 0 0.18 0.18 {layer=8}
T {4/0.5} 700 -1053 0 0 0.15 0.15 {layer=8}
N 460 -1090 460 -1140 {lab=di_p}
N 660 -1090 660 -1140 {lab=di_n}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 400 -1060 0 1 {name=p_vinp lab=vinp}
N 400 -1060 420 -1060 {lab=vinp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 720 -1060 0 0 {name=p_vinn lab=vinn}
N 700 -1060 720 -1060 {lab=vinn}
N 460 -1030 660 -1030 {lab=tail}
T {Tail} 528 -985 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 540 -950 0 0 {name=XM0
W=2.0
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {XM0} 498 -958 0 0 0.18 0.18 {layer=8}
T {2/0.15} 498 -943 0 0 0.15 0.15 {layer=8}
N 560 -980 560 -1030 {lab=tail}
N 560 -920 560 -480 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 500 -950 0 1 {name=p_clk lab=clk}
N 500 -950 520 -950 {lab=clk}
N 200 -480 900 -480 {lab=vss}
T {Non-Overlapping 3-Phase Clock Generator (30T)} 1000 -1410 0 0 0.45 0.45 {layer=4}
T {NAND-based  |  clk_in \u2192 phi_s, phi_e, phi_r with dead time} 1000 -1385 0 0 0.25 0.25 {layer=8}
T {Buffer} 1085 -1355 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1080 -1315 0 0 {name=XP_buf1
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1080 -1245 0 0 {name=XN_buf1
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1060 -1315 1060 -1245 {lab=clk_in}
N 1100 -1285 1100 -1275 {lab=clk_buf1}
N 1100 -1345 1100 -1360 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -1360 0 0 {name=l_vdd_XP_buf1 lab=vdd}
N 1100 -1215 1100 -1200 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -1200 0 0 {name=l_vss_XN_buf1 lab=vss}
T {buf1} 1105 -1283 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1200 -1315 0 0 {name=XP_buf2
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1200 -1245 0 0 {name=XN_buf2
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1180 -1315 1180 -1245 {lab=clk_buf1}
N 1220 -1285 1220 -1275 {lab=clk_buf}
N 1220 -1345 1220 -1360 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -1360 0 0 {name=l_vdd_XP_buf2 lab=vdd}
N 1220 -1215 1220 -1200 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -1200 0 0 {name=l_vss_XN_buf2 lab=vss}
T {buf2} 1225 -1283 0 0 0.18 0.18 {layer=8}
N 1100 -1280 1180 -1280 {lab=clk_buf1}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1040 -1280 0 1 {name=p_clk_in lab=clk_in}
N 1040 -1280 1060 -1280 {lab=clk_in}
T {phi_s} 1325 -1355 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1350 -1315 0 0 {name=XP_s1
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1350 -1245 0 0 {name=XN_s1
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1330 -1315 1330 -1245 {lab=clk_buf}
N 1370 -1285 1370 -1275 {lab=phi_sb}
N 1370 -1345 1370 -1360 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1370 -1360 0 0 {name=l_vdd_XP_s1 lab=vdd}
N 1370 -1215 1370 -1200 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1370 -1200 0 0 {name=l_vss_XN_s1 lab=vss}
T {s1} 1375 -1283 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1470 -1315 0 0 {name=XP_s2
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1470 -1245 0 0 {name=XN_s2
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1450 -1315 1450 -1245 {lab=phi_sb}
N 1490 -1285 1490 -1275 {lab=phi_s}
N 1490 -1345 1490 -1360 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1490 -1360 0 0 {name=l_vdd_XP_s2 lab=vdd}
N 1490 -1215 1490 -1200 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1490 -1200 0 0 {name=l_vss_XN_s2 lab=vss}
T {s2} 1495 -1283 0 0 0.18 0.18 {layer=8}
N 1220 -1280 1330 -1280 {lab=clk_buf}
N 1370 -1280 1450 -1280 {lab=phi_sb}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1510 -1280 0 0 {name=p_phi_s lab=phi_s}
N 1490 -1280 1510 -1280 {lab=phi_s}
T {Delay Chain (4 slow inverters \u2248 1.2 ns)} 1050 -1195 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1080 -1155 0 0 {name=XP_d1
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1080 -1085 0 0 {name=XN_d1
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1060 -1155 1060 -1085 {lab=phi_sb}
N 1100 -1125 1100 -1115 {lab=d1}
N 1100 -1185 1100 -1200 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -1200 0 0 {name=l_vdd_XP_d1 lab=vdd}
N 1100 -1055 1100 -1040 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -1040 0 0 {name=l_vss_XN_d1 lab=vss}
T {d1} 1105 -1123 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1200 -1155 0 0 {name=XP_d2
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1200 -1085 0 0 {name=XN_d2
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1180 -1155 1180 -1085 {lab=d1}
N 1220 -1125 1220 -1115 {lab=d2}
N 1220 -1185 1220 -1200 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -1200 0 0 {name=l_vdd_XP_d2 lab=vdd}
N 1220 -1055 1220 -1040 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -1040 0 0 {name=l_vss_XN_d2 lab=vss}
T {d2} 1225 -1123 0 0 0.18 0.18 {layer=8}
N 1100 -1120 1180 -1120 {lab=d1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1320 -1155 0 0 {name=XP_d3
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1320 -1085 0 0 {name=XN_d3
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1300 -1155 1300 -1085 {lab=d2}
N 1340 -1125 1340 -1115 {lab=d3}
N 1340 -1185 1340 -1200 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1340 -1200 0 0 {name=l_vdd_XP_d3 lab=vdd}
N 1340 -1055 1340 -1040 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1340 -1040 0 0 {name=l_vss_XN_d3 lab=vss}
T {d3} 1345 -1123 0 0 0.18 0.18 {layer=8}
N 1220 -1120 1300 -1120 {lab=d2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1440 -1155 0 0 {name=XP_d4
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1440 -1085 0 0 {name=XN_d4
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1420 -1155 1420 -1085 {lab=d3}
N 1460 -1125 1460 -1115 {lab=d4}
N 1460 -1185 1460 -1200 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1460 -1200 0 0 {name=l_vdd_XP_d4 lab=vdd}
N 1460 -1055 1460 -1040 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1460 -1040 0 0 {name=l_vss_XN_d4 lab=vss}
T {d4} 1465 -1123 0 0 0.18 0.18 {layer=8}
N 1340 -1120 1420 -1120 {lab=d3}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1045 -1120 0 1 {name=l_phisb_d lab=phi_sb}
N 1045 -1120 1060 -1120 {lab=phi_sb}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1475 -1120 0 0 {name=l_d4_out lab=d4}
N 1460 -1120 1475 -1120 {lab=d4}
T {NAND} 1050 -1010 0 0 0.3 0.3 {layer=4}
T {AND(phi_sb, d4)} 1050 -990 0 0 0.2 0.2 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1070 -960 0 0 {name=XP_na1
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {pa1} 1033 -963 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1160 -960 0 0 {name=XP_na2
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {pa2} 1185 -963 0 0 0.15 0.15 {layer=8}
N 1090 -990 1090 -1005 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1090 -1005 0 0 {name=l_vdd_pa1 lab=vdd}
N 1180 -990 1180 -1005 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1180 -1005 0 0 {name=l_vdd_pa2 lab=vdd}
N 1090 -930 1180 -930 {lab=nand_e1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1115 -890 0 0 {name=XN_na1
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {na1} 1140 -893 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1115 -830 0 0 {name=XN_na2
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {na2} 1140 -833 0 0 0.15 0.15 {layer=8}
N 1135 -920 1135 -930 {lab=nand_e1}
N 1135 -800 1135 -790 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1135 -790 0 0 {name=l_vss_na2 lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1035 -960 0 1 {name=l_phisb_pa1 lab=phi_sb}
N 1035 -960 1050 -960 {lab=phi_sb}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1125 -960 0 1 {name=l_d4_pa2 lab=d4}
N 1125 -960 1140 -960 {lab=d4}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1080 -890 0 1 {name=l_phisb_na1 lab=phi_sb}
N 1080 -890 1095 -890 {lab=phi_sb}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1080 -830 0 1 {name=l_d4_na2 lab=d4}
N 1080 -830 1095 -830 {lab=d4}
T {phi_e} 1250 -1010 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1280 -975 0 0 {name=XP_e1
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1280 -905 0 0 {name=XN_e1
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1260 -975 1260 -905 {lab=nand_e1}
N 1300 -945 1300 -935 {lab=phi_e}
N 1300 -1005 1300 -1020 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1300 -1020 0 0 {name=l_vdd_XP_e1 lab=vdd}
N 1300 -875 1300 -860 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1300 -860 0 0 {name=l_vss_XN_e1 lab=vss}
T {e1} 1305 -943 0 0 0.18 0.18 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1245 -940 0 1 {name=l_nand_e1 lab=nand_e1}
N 1245 -940 1260 -940 {lab=nand_e1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1400 -975 0 0 {name=XP_eb
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1400 -905 0 0 {name=XN_eb
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1380 -975 1380 -905 {lab=phi_e}
N 1420 -945 1420 -935 {lab=phi_eb}
N 1420 -1005 1420 -1020 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1420 -1020 0 0 {name=l_vdd_XP_eb lab=vdd}
N 1420 -875 1420 -860 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1420 -860 0 0 {name=l_vss_XN_eb lab=vss}
T {eb} 1425 -943 0 0 0.18 0.18 {layer=8}
N 1300 -940 1380 -940 {lab=phi_e}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1310 -960 0 0 {name=p_phi_e lab=phi_e}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1440 -940 0 0 {name=p_phi_eb lab=phi_eb}
N 1420 -940 1440 -940 {lab=phi_eb}
T {NOR} 1520 -1010 0 0 0.3 0.3 {layer=4}
T {NOR(phi_s, phi_e)} 1520 -990 0 0 0.2 0.2 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1540 -890 0 0 {name=XN_nr1
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {nr1} 1565 -893 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1630 -890 0 0 {name=XN_nr2
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {nr2} 1655 -893 0 0 0.15 0.15 {layer=8}
N 1560 -920 1650 -920 {lab=phi_r_b}
N 1560 -860 1560 -845 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1560 -845 0 0 {name=l_vss_nr1 lab=vss}
N 1650 -860 1650 -845 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1650 -845 0 0 {name=l_vss_nr2 lab=vss}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1585 -980 0 0 {name=XP_nr1
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {pr1} 1610 -983 0 0 0.15 0.15 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1585 -930 0 0 {name=XP_nr2
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {pr2} 1610 -933 0 0 0.15 0.15 {layer=8}
N 1605 -1010 1605 -1025 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1605 -1025 0 0 {name=l_vdd_pr1 lab=vdd}
N 1605 -950 1605 -960 {lab=n_nr}
N 1605 -900 1605 -920 {lab=phi_r_b}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1505 -890 0 1 {name=l_phis_nr1 lab=phi_s}
N 1505 -890 1520 -890 {lab=phi_s}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1615 -890 0 1 {name=l_phie_nr2 lab=phi_e}
N 1615 -890 1610 -890 {lab=phi_e}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1550 -980 0 1 {name=l_phis_pr1 lab=phi_s}
N 1550 -980 1565 -980 {lab=phi_s}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1550 -930 0 1 {name=l_phie_pr2 lab=phi_e}
N 1550 -930 1565 -930 {lab=phi_e}
T {phi_r} 1700 -1010 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1730 -975 0 0 {name=XP_ri
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1730 -905 0 0 {name=XN_ri
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1710 -975 1710 -905 {lab=phi_r_b}
N 1750 -945 1750 -935 {lab=phi_r}
N 1750 -1005 1750 -1020 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1750 -1020 0 0 {name=l_vdd_XP_ri lab=vdd}
N 1750 -875 1750 -860 {lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1750 -860 0 0 {name=l_vss_XN_ri lab=vss}
T {ri} 1755 -943 0 0 0.18 0.18 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1695 -940 0 1 {name=l_phirb_ri lab=phi_r_b}
N 1695 -940 1710 -940 {lab=phi_r_b}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1770 -940 0 0 {name=p_phi_r lab=phi_r}
N 1750 -940 1770 -940 {lab=phi_r}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 200 -1430 0 1 {name=p_vdd lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 200 -480 0 1 {name=p_vss lab=vss}
