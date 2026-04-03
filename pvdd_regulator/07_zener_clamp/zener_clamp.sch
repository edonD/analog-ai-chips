v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {BLOCK 07: MOS Voltage Clamp (v19)} -200 -1320 0 0 0.8 0.8 {layer=15}
T {PVDD 5V LDO | SkyWater SKY130A | Hybrid Clamp: Precision 4-FET Stack + Fast 7-NFET Stack} -200 -1270 0 0 0.4 0.4 {layer=8}
T {.subckt zener_clamp pvdd gnd ibias} -200 -1230 0 0 0.35 0.35 {layer=13}
T {PRECISION STACK: N-P-N-P (4 devices, L=4u)} -200 -1100 0 0 0.5 0.5 {layer=4}
T {+ Series Rstack for process-stable offset} -200 -1070 0 0 0.3 0.3 {}
T {GATE PULLDOWN + PTAT COMPENSATION} -200 -280 0 0 0.5 0.5 {layer=4}
T {FAST PARALLEL STACK: 7x NFET L=0.5u W=10u} 500 -1100 0 0 0.5 0.5 {layer=4}
T {CLAMP NMOS: W=50u m=4 (200um total)} 900 -1100 0 0 0.5 0.5 {layer=4}
C {devices/title.sym} -200 200 0 0 {name=l1 author="PVDD LDO"}
C {devices/iopin.sym} -200 -1180 0 1 {name=p1 lab=pvdd}
C {devices/iopin.sym} -200 -1150 0 1 {name=p2 lab=gnd}
C {devices/ipin.sym} -200 -1120 0 0 {name=p3 lab=ibias}
N -200 -1180 -100 -1180 {lab=pvdd}
N -200 -1150 -100 -1150 {lab=gnd}
C {devices/lab_pin.sym} -100 -1180 0 0 {name=lp1 sig_type=std_logic lab=pvdd}
C {devices/lab_pin.sym} -100 -1150 0 0 {name=lp2 sig_type=std_logic lab=gnd}
C {devices/lab_pin.sym} -100 -1120 0 0 {name=lp3 sig_type=std_logic lab=ibias}
N -200 -1120 -100 -1120 {lab=ibias}
T {XMd1 (NFET diode)} -180 -1000 0 0 0.25 0.25 {layer=13}
T {W=2.2 L=4} -180 -978 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} -80 -960 0 0 {name=XMd1
L=4
W=2.2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -60 -990 -60 -1040 {lab=pvdd}
C {devices/lab_pin.sym} -60 -1040 2 0 {name=ld1d sig_type=std_logic lab=pvdd}
N -100 -960 -160 -960 {lab=pvdd}
N -160 -960 -160 -1040 {lab=pvdd}
C {devices/lab_pin.sym} -160 -1040 2 0 {name=ld1g sig_type=std_logic lab=pvdd}
N -60 -930 -60 -890 {lab=n3}
T {B=n3} -50 -945 0 0 0.2 0.2 {layer=7}
T {n3} -55 -895 0 0 0.25 0.25 {layer=8}
T {XMd2 (PFET diode)} -180 -830 0 0 0.25 0.25 {layer=13}
T {W=20 L=4} -180 -808 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} -80 -790 0 0 {name=XMd2
L=4
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -60 -820 -60 -890 {lab=n3}
N -60 -760 -60 -720 {lab=n2}
N -100 -790 -160 -790 {lab=n2}
N -160 -790 -160 -720 {lab=n2}
N -160 -720 -60 -720 {lab=n2}
T {B=n3} -50 -805 0 0 0.2 0.2 {layer=7}
T {n2} -55 -725 0 0 0.25 0.25 {layer=8}
T {XMd3 (NFET diode)} -180 -660 0 0 0.25 0.25 {layer=13}
T {W=2.2 L=4} -180 -638 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} -80 -620 0 0 {name=XMd3
L=4
W=2.2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -60 -650 -60 -720 {lab=n2}
N -60 -590 -60 -550 {lab=n1}
N -100 -620 -160 -620 {lab=n2}
N -160 -620 -160 -720 {lab=n2}
T {B=n1} -50 -635 0 0 0.2 0.2 {layer=7}
T {n1} -55 -555 0 0 0.25 0.25 {layer=8}
T {XMd4 (PFET diode)} -180 -490 0 0 0.25 0.25 {layer=13}
T {W=20 L=4} -180 -468 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} -80 -450 0 0 {name=XMd4
L=4
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -60 -480 -60 -550 {lab=n1}
N -60 -420 -60 -380 {lab=ns}
N -100 -450 -160 -450 {lab=n1}
N -160 -450 -160 -550 {lab=n1}
N -160 -550 -60 -550 {lab=n1}
T {B=ns} -50 -465 0 0 0.2 0.2 {layer=7}
T {ns} -55 -385 0 0 0.25 0.25 {layer=8}
T {XRstack: xhigh_po W=2 L=190} -180 -340 0 0 0.25 0.25 {layer=13}
T {R ~ 190k (process-stable offset)} -180 -318 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/res_xhigh_po.sym} -60 -300 0 0 {name=XRstack
W=3.0
L=190
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -60 -380 -60 -330 {lab=ns}
N -60 -270 -60 -220 {lab=vg}
T {vg} -55 -225 0 0 0.35 0.35 {layer=4}
T {XRpd: xhigh_po W=2 L=500} -180 -190 0 0 0.25 0.25 {layer=13}
T {Rpd ~ 500k (gate pulldown)} -180 -168 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/res_xhigh_po.sym} -60 -140 0 0 {name=XRpd
W=3.0
L=500
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -60 -220 -60 -170 {lab=vg}
N -60 -110 -60 -60 {lab=gnd}
C {devices/lab_pin.sym} -60 -60 0 0 {name=lrpd_gnd sig_type=std_logic lab=gnd}
T {PTAT COMPENSATION} 120 -280 0 0 0.4 0.4 {layer=4}
T {Mirror ibias to sink current from vg} 120 -255 0 0 0.25 0.25 {}
T {XMptat_d (diode)} 120 -200 0 0 0.25 0.25 {layer=13}
T {W=2 L=8} 120 -178 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 200 -140 0 0 {name=XMptat_d
L=8
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 220 -170 220 -220 {lab=ibias}
C {devices/lab_pin.sym} 220 -220 2 0 {name=lptd_d sig_type=std_logic lab=ibias}
N 180 -140 140 -140 {lab=ibias}
N 140 -140 140 -220 {lab=ibias}
C {devices/lab_pin.sym} 140 -220 2 0 {name=lptd_g sig_type=std_logic lab=ibias}
N 220 -110 220 -60 {lab=gnd}
C {devices/lab_pin.sym} 220 -60 0 0 {name=lptd_s sig_type=std_logic lab=gnd}
T {B=GND} 225 -155 0 0 0.2 0.2 {layer=7}
T {XMptat_m (mirror)} 320 -200 0 0 0.25 0.25 {layer=13}
T {W=5 L=8} 320 -178 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 400 -140 0 0 {name=XMptat_m
L=8
W=5
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 420 -170 420 -220 {lab=vg}
C {devices/lab_pin.sym} 420 -220 2 0 {name=lptm_d sig_type=std_logic lab=vg}
N 380 -140 340 -140 {lab=ibias}
C {devices/lab_pin.sym} 340 -140 0 0 {name=lptm_g sig_type=std_logic lab=ibias}
N 420 -110 420 -60 {lab=gnd}
C {devices/lab_pin.sym} 420 -60 0 0 {name=lptm_s sig_type=std_logic lab=gnd}
T {B=GND} 425 -155 0 0 0.2 0.2 {layer=7}
T {XMf1} 480 -1000 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 480 -978 0 0 0.15 0.15 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -960 0 0 {name=XMf1
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -990 580 -1040 {lab=pvdd}
C {devices/lab_pin.sym} 580 -1040 2 0 {name=lf1d sig_type=std_logic lab=pvdd}
N 540 -960 500 -960 {lab=pvdd}
N 500 -960 500 -1040 {lab=pvdd}
C {devices/lab_pin.sym} 500 -1040 2 0 {name=lf1g sig_type=std_logic lab=pvdd}
N 580 -930 580 -890 {lab=nf6}
T {B=GND} 585 -975 0 0 0.2 0.2 {layer=7}
T {nf6} 585 -895 0 0 0.2 0.2 {layer=8}
T {XMf2} 480 -850 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 480 -828 0 0 0.15 0.15 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -810 0 0 {name=XMf2
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -840 580 -890 {lab=nf6}
N 540 -810 500 -810 {lab=nf6}
N 500 -810 500 -890 {lab=nf6}
N 500 -890 580 -890 {lab=nf6}
N 580 -780 580 -740 {lab=nf5}
T {B=GND} 585 -825 0 0 0.2 0.2 {layer=7}
T {nf5} 585 -745 0 0 0.2 0.2 {layer=8}
T {XMf3} 480 -700 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 480 -678 0 0 0.15 0.15 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -660 0 0 {name=XMf3
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -690 580 -740 {lab=nf5}
N 540 -660 500 -660 {lab=nf5}
N 500 -660 500 -740 {lab=nf5}
N 500 -740 580 -740 {lab=nf5}
N 580 -630 580 -590 {lab=nf4}
T {B=GND} 585 -675 0 0 0.2 0.2 {layer=7}
T {nf4} 585 -595 0 0 0.2 0.2 {layer=8}
T {XMf4} 480 -550 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 480 -528 0 0 0.15 0.15 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -510 0 0 {name=XMf4
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -540 580 -590 {lab=nf4}
N 540 -510 500 -510 {lab=nf4}
N 500 -510 500 -590 {lab=nf4}
N 500 -590 580 -590 {lab=nf4}
N 580 -480 580 -440 {lab=nf3}
T {B=GND} 585 -525 0 0 0.2 0.2 {layer=7}
T {nf3} 585 -445 0 0 0.2 0.2 {layer=8}
T {XMf5} 480 -400 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 480 -378 0 0 0.15 0.15 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -360 0 0 {name=XMf5
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -390 580 -440 {lab=nf3}
N 540 -360 500 -360 {lab=nf3}
N 500 -360 500 -440 {lab=nf3}
N 500 -440 580 -440 {lab=nf3}
N 580 -330 580 -290 {lab=nf2}
T {B=GND} 585 -375 0 0 0.2 0.2 {layer=7}
T {nf2} 585 -295 0 0 0.2 0.2 {layer=8}
T {XMf6} 480 -250 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 480 -228 0 0 0.15 0.15 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -210 0 0 {name=XMf6
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -240 580 -290 {lab=nf2}
N 540 -210 500 -210 {lab=nf2}
N 500 -210 500 -290 {lab=nf2}
N 500 -290 580 -290 {lab=nf2}
N 580 -180 580 -140 {lab=nf1}
T {B=GND} 585 -225 0 0 0.2 0.2 {layer=7}
T {nf1} 585 -145 0 0 0.2 0.2 {layer=8}
T {XMf7} 480 -100 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 480 -78 0 0 0.15 0.15 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -60 0 0 {name=XMf7
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -90 580 -140 {lab=nf1}
N 540 -60 500 -60 {lab=nf1}
N 500 -60 500 -140 {lab=nf1}
N 500 -140 580 -140 {lab=nf1}
N 580 -30 580 20 {lab=gnd}
C {devices/lab_pin.sym} 580 20 0 0 {name=lf7s sig_type=std_logic lab=gnd}
T {B=GND} 585 -75 0 0 0.2 0.2 {layer=7}
T {XMclamp} 880 -1000 0 0 0.25 0.25 {layer=13}
T {W=50 L=0.5 m=4 (200um total)} 880 -978 0 0 0.2 0.2 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 960 -940 0 0 {name=XMclamp
L=0.5
W=50
nf=1
mult=4
model=nfet_g5v0d10v5
spiceprefix=X
}
N 980 -970 980 -1040 {lab=pvdd}
C {devices/lab_pin.sym} 980 -1040 2 0 {name=lcl_d sig_type=std_logic lab=pvdd}
N 940 -940 880 -940 {lab=vg}
C {devices/lab_pin.sym} 880 -940 0 0 {name=lcl_g sig_type=std_logic lab=vg}
N 980 -910 980 -860 {lab=gnd}
C {devices/lab_pin.sym} 980 -860 0 0 {name=lcl_s sig_type=std_logic lab=gnd}
T {B=GND} 985 -955 0 0 0.2 0.2 {layer=7}
