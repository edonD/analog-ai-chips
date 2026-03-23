v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 00: Bias Generator} -400 -1300 0 0 1.0 1.0 {layer=15}
T {Beta-Multiplier Self-Biased Current Reference  —  SKY130A} -400 -1240 0 0 0.5 0.5 {layer=15}
T {Iref = 500 nA  |  TC < 150 ppm/C  |  VDD = 1.8 V} -400 -1190 0 0 0.4 0.4 {layer=8}
T {PMOS Current Mirror} -50 -1100 0 0 0.4 0.4 {layer=4}
T {M3} -100 -1020 0 0 0.3 0.3 {layer=8}
T {4/4} -100 -996 0 0 0.25 0.25 {layer=8}
T {M4} 230 -1020 0 0 0.3 0.3 {layer=8}
T {4/4} 230 -996 0 0 0.25 0.25 {layer=8}
T {NMOS Pair (K=4)} -50 -760 0 0 0.4 0.4 {layer=4}
T {M1} -100 -680 0 0 0.3 0.3 {layer=8}
T {2/4} -100 -656 0 0 0.25 0.25 {layer=8}
T {M2} 230 -680 0 0 0.3 0.3 {layer=8}
T {8/4} 230 -656 0 0 0.25 0.25 {layer=8}
T {Regulation OTA} 540 -1100 0 0 0.4 0.4 {layer=4}
T {Mo3} 540 -1020 0 0 0.3 0.3 {layer=8}
T {2/4} 540 -996 0 0 0.25 0.25 {layer=8}
T {Mo4} 740 -1020 0 0 0.3 0.3 {layer=8}
T {2/4} 740 -996 0 0 0.25 0.25 {layer=8}
T {Mo1} 540 -810 0 0 0.3 0.3 {layer=8}
T {1/4} 540 -786 0 0 0.25 0.25 {layer=8}
T {Mo2} 740 -810 0 0 0.3 0.3 {layer=8}
T {1/4} 740 -786 0 0 0.25 0.25 {layer=8}
T {Mo5} 650 -660 0 0 0.3 0.3 {layer=8}
T {1/4} 650 -636 0 0 0.25 0.25 {layer=8}
T {Output Mirror} 960 -1100 0 0 0.4 0.4 {layer=4}
T {M7} 980 -1020 0 0 0.3 0.3 {layer=8}
T {4/4} 980 -996 0 0 0.25 0.25 {layer=8}
T {TC-Compensated R1} 30 -510 0 0 0.35 0.35 {layer=4}
T {R1a: xhigh_po} 30 -455 0 0 0.25 0.25 {layer=8}
T {0.35/7.1} 30 -435 0 0 0.25 0.25 {layer=8}
T {R1b: iso_pw} 30 -355 0 0 0.25 0.25 {layer=8}
T {0.35/6.55} 30 -335 0 0 0.25 0.25 {layer=8}
T {Comp Cap} 400 -510 0 0 0.35 0.35 {layer=4}
T {C_comp} 400 -455 0 0 0.25 0.25 {layer=8}
T {5 pF MIM} 400 -435 0 0 0.25 0.25 {layer=8}
T {Anti-Deadlock} 940 -760 0 0 0.35 0.35 {layer=4}
T {M6} 980 -680 0 0 0.3 0.3 {layer=8}
T {0.5/0.5} 970 -656 0 0 0.25 0.25 {layer=8}
T {RC Startup} 1200 -1100 0 0 0.4 0.4 {layer=4}
T {C_gs} 1220 -1020 0 0 0.25 0.25 {layer=8}
T {MIM 25x50} 1210 -996 0 0 0.25 0.25 {layer=8}
T {R_gs} 1400 -680 0 0 0.25 0.25 {layer=8}
T {0.35/1360} 1390 -656 0 0 0.25 0.25 {layer=8}
T {Msw} 1240 -810 0 0 0.3 0.3 {layer=8}
T {4/0.5} 1240 -786 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -40 -940 0 0 {name=XM3
W=4
L=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 260 -940 0 1 {name=XM4
W=4
L=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -40 -600 0 0 {name=XM1
W=2
L=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 260 -600 0 1 {name=XM2
W=8
L=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 110 -430 0 0 {name=XR1a
W=0.35
L=7.1
mult=1
model=res_xhigh_po
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_iso_pw.sym} 110 -330 0 0 {name=XR1b
W=0.35
L=6.55
mult=1
model=res_iso_pw
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 560 -940 0 0 {name=XMo3
W=2
L=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 760 -940 0 1 {name=XMo4
W=2
L=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 560 -840 0 0 {name=XMo1
W=1
L=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 760 -840 0 1 {name=XMo2
W=1
L=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 640 -720 0 0 {name=XMo5
W=1
L=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 440 -390 0 0 {name=XC_comp
W=50
L=50
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1020 -940 0 0 {name=XM7
W=4
L=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1020 -600 0 0 {name=XM6
W=0.5
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 1300 -960 0 0 {name=XC_gs
W=25
L=50
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 1420 -600 0 0 {name=XR_gs
W=0.35
L=1360
mult=1
model=res_xhigh_po
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1300 -840 0 0 {name=XMsw
W=4
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -400 -1140 0 1 {name=p_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -400 -260 0 1 {name=p_gnd lab=gnd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1140 -910 0 0 {name=p_iref lab=iref_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 110 -860 0 0 {name=l_vbias lab=vbias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -20 -770 0 1 {name=l_nbias lab=nbias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 240 -770 0 0 {name=l_outn lab=out_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 110 -500 0 1 {name=l_srcm2 lab=src_m2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 110 -380 0 1 {name=l_midr lab=mid_r}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -880 0 1 {name=l_od1 lab=od1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 660 -750 0 0 {name=l_otail lab=otail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1360 -872 0 0 {name=l_gs lab=gs}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 -840 0 1 {name=l_outn2 lab=out_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -840 0 0 {name=l_nbias2 lab=nbias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -720 0 1 {name=l_nbias3 lab=nbias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -940 0 1 {name=l_vbias2 lab=vbias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1040 -630 0 0 {name=l_vbias3 lab=vbias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1280 -840 0 1 {name=l_vbias4 lab=vbias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1320 -810 0 0 {name=l_nbias4 lab=nbias}
N -20 -970 -20 -1140 {lab=vdd}
N 240 -970 240 -1140 {lab=vdd}
N -20 -1140 240 -1140 {lab=vdd}
N 240 -1140 580 -1140 {lab=vdd}
N 580 -970 580 -1140 {lab=vdd}
N 580 -1140 740 -1140 {lab=vdd}
N 740 -970 740 -1140 {lab=vdd}
N 740 -1140 1040 -1140 {lab=vdd}
N 1040 -970 1040 -1140 {lab=vdd}
N 1040 -1140 1300 -1140 {lab=vdd}
N 1300 -1140 1300 -990 {lab=vdd}
N -400 -1140 -20 -1140 {lab=vdd}
N -20 -910 -20 -600 {lab=nbias}
N 240 -910 240 -600 {lab=out_n}
N -60 -940 -180 -940 {lab=vbias}
N -180 -940 -180 -860 {lab=vbias}
N 280 -940 380 -940 {lab=vbias}
N 380 -940 380 -860 {lab=vbias}
N -180 -860 380 -860 {lab=vbias}
N -20 -570 -20 -260 {lab=gnd}
N 240 -570 240 -540 {lab=src_m2}
N 240 -540 110 -540 {lab=src_m2}
N 110 -540 110 -462 {lab=src_m2}
N 110 -398 110 -362 {lab=mid_r}
N 110 -298 110 -260 {lab=gnd}
N 580 -910 580 -870 {lab=od1}
N 580 -870 740 -870 {lab=od1}
N 740 -940 740 -870 {lab=od1}
N 440 -870 580 -870 {lab=od1}
N 440 -870 440 -422 {lab=od1}
N 740 -910 740 -860 {lab=vbias}
N 740 -860 380 -860 {lab=vbias}
N 580 -810 580 -750 {lab=otail}
N 580 -750 660 -750 {lab=otail}
N 660 -750 740 -750 {lab=otail}
N 740 -750 740 -810 {lab=otail}
N 660 -750 660 -690 {lab=otail}
N 660 -690 660 -260 {lab=gnd}
N 440 -358 440 -260 {lab=gnd}
N 1040 -910 1040 -870 {lab=iref_out}
N 1040 -870 1140 -870 {lab=iref_out}
N 1140 -870 1140 -910 {lab=iref_out}
N 1040 -570 1040 -260 {lab=gnd}
N 1300 -928 1300 -872 {lab=gs}
N 1300 -872 1420 -872 {lab=gs}
N 1420 -872 1420 -568 {lab=gs}
N 1320 -810 1320 -260 {lab=nbias}
N 1420 -568 1420 -260 {lab=gnd}
N -400 -260 -20 -260 {lab=gnd}
N -20 -260 110 -260 {lab=gnd}
N 110 -260 440 -260 {lab=gnd}
N 440 -260 660 -260 {lab=gnd}
N 660 -260 1040 -260 {lab=gnd}
N 1040 -260 1320 -260 {lab=gnd}
N 1320 -260 1420 -260 {lab=gnd}
