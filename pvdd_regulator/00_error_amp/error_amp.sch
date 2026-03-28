v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}
T {Block 00: Error Amplifier} 2400 1400 0 0 0.6 0.6 {}
T {PVDD 5V LDO — SkyWater SKY130A} 2400 1450 0 0 0.4 0.4 {}
T {2026-03-28} 2400 1490 0 0 0.35 0.35 {}
T {BIAS SECTION} 0 -200 0 0 0.4 0.4 {}
T {DIFF PAIR + MIRROR LOAD} 800 -200 0 0 0.4 0.4 {}
T {STAGE 2} 1600 -200 0 0 0.4 0.4 {}
T {MILLER COMP} 1200 -200 0 0 0.4 0.4 {}
T {ENABLE} -400 -200 0 0 0.4 0.4 {}

C {devices/title.sym} 2200 1520 0 0 {name=l1 author="Analog AI Chips"}

C {devices/ipin.sym} -700 400 0 0 {name=p1 lab=vref}
C {devices/ipin.sym} -700 600 0 0 {name=p2 lab=vfb}
C {devices/ipin.sym} -700 900 0 0 {name=p3 lab=ibias}
C {devices/ipin.sym} -700 1100 0 0 {name=p4 lab=en}
C {devices/opin.sym} 2100 600 0 0 {name=p5 lab=vout_gate}
C {devices/iopin.sym} -700 -100 0 0 {name=p6 lab=pvdd}
C {devices/iopin.sym} -700 1300 0 0 {name=p7 lab=gnd}

C {devices/lab_pin.sym} -500 -100 0 0 {name=l_pvdd lab=pvdd}
C {devices/lab_pin.sym} -500 1300 0 0 {name=l_gnd lab=gnd}

C {devices/lab_pin.sym} -300 900 0 0 {name=l_ibias lab=ibias}
C {devices/lab_pin.sym} -300 1100 0 0 {name=l_en lab=en}

C {devices/lab_pin.sym} -500 400 0 0 {name=l_vref lab=vref}
C {devices/lab_pin.sym} -500 600 0 0 {name=l_vfb lab=vfb}

C {devices/lab_pin.sym} 2000 600 0 0 {name=l_vout_gate lab=vout_gate}

C {devices/lab_pin.sym} -200 800 2 0 {name=l_ibias_en lab=ibias_en}
C {devices/lab_pin.sym} 400 0 2 0 {name=l_pb_tail lab=pb_tail}
C {devices/lab_pin.sym} 800 200 2 0 {name=l_tail_s lab=tail_s}
C {devices/lab_pin.sym} 900 700 0 0 {name=l_d1 lab=d1}
C {devices/lab_pin.sym} 1100 700 0 0 {name=l_d2 lab=d2}
C {devices/lab_pin.sym} 1400 700 0 0 {name=l_comp_mid lab=comp_mid}

C {sky130_fd_pr/nfet_g5v0d10v5.sym} -380 1100 0 0 {name=XMen
L=1
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}

N -360 1130 -360 1300 {lab=gnd}
N -360 1070 -360 900 {lab=ibias_en}
N -400 1100 -500 1100 {lab=en}
N -360 900 -200 900 {lab=ibias_en}

C {sky130_fd_pr/pfet_g5v0d10v5.sym} -380 -50 0 0 {name=XMpu
L=1
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}

N -360 -80 -360 -100 {lab=pvdd}
N -360 -20 -360 100 {lab=vout_gate}
N -400 -50 -500 -50 {lab=en}

C {devices/lab_pin.sym} -500 -50 0 0 {name=l_en2 lab=en}
C {devices/lab_pin.sym} -360 -100 2 0 {name=l_pvdd2 lab=pvdd}
C {devices/lab_pin.sym} -360 100 0 0 {name=l_vout_gate2 lab=vout_gate}

C {sky130_fd_pr/nfet_g5v0d10v5.sym} -20 900 0 0 {name=XMbn0
L=8
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}

N 0 930 0 1050 {lab=gnd}
N 0 870 0 800 {lab=ibias_en}
N -40 900 -200 900 {lab=ibias_en}
N 0 800 -200 800 {lab=ibias_en}

C {devices/lab_pin.sym} 0 1050 0 0 {name=l_gnd2 lab=gnd}
C {devices/lab_pin.sym} 0 800 2 0 {name=l_ibias_en2 lab=ibias_en}

C {sky130_fd_pr/nfet_g5v0d10v5.sym} 180 900 0 0 {name=XMbn_pb
L=8
W=20
nf=1
mult=20
model=nfet_g5v0d10v5
spiceprefix=X
}

N 200 930 200 1050 {lab=gnd}
N 200 870 200 700 {lab=pb_tail}
N 160 900 0 900 {lab=ibias_en}

C {devices/lab_pin.sym} 200 1050 0 0 {name=l_gnd3 lab=gnd}
C {devices/lab_pin.sym} 200 700 2 0 {name=l_pb_tail2 lab=pb_tail}

C {devices/lab_pin.sym} 0 900 2 0 {name=l_ibias_en3 lab=ibias_en}

C {sky130_fd_pr/pfet_g5v0d10v5.sym} 380 100 0 0 {name=XMbp0
L=4
W=20
nf=1
mult=4
model=pfet_g5v0d10v5
spiceprefix=X
}

N 400 70 400 -100 {lab=pvdd}
N 400 130 400 300 {lab=pb_tail}
N 360 100 200 100 {lab=pb_tail}
N 200 100 200 700 {lab=pb_tail}
N 400 300 400 700 {lab=pb_tail}

C {devices/lab_pin.sym} 400 -100 2 0 {name=l_pvdd3 lab=pvdd}
C {devices/lab_pin.sym} 400 300 0 0 {name=l_pb_tail3 lab=pb_tail}

C {sky130_fd_pr/pfet_g5v0d10v5.sym} 780 100 0 0 {name=XMtail
L=4
W=20
nf=1
mult=4
model=pfet_g5v0d10v5
spiceprefix=X
}

N 800 70 800 -100 {lab=pvdd}
N 800 130 800 250 {lab=tail_s}
N 760 100 600 100 {lab=pb_tail}

C {devices/lab_pin.sym} 800 -100 2 0 {name=l_pvdd4 lab=pvdd}
C {devices/lab_pin.sym} 800 250 0 0 {name=l_tail_s2 lab=tail_s}
C {devices/lab_pin.sym} 600 100 0 0 {name=l_pb_tail4 lab=pb_tail}

C {sky130_fd_pr/pfet_g5v0d10v5.sym} 680 400 0 0 {name=XM1
L=4
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}

N 700 370 700 250 {lab=tail_s}
N 700 250 800 250 {lab=tail_s}
N 700 430 700 600 {lab=d1}
N 660 400 500 400 {lab=vref}

C {devices/lab_pin.sym} 500 400 0 0 {name=l_vref2 lab=vref}
C {devices/lab_pin.sym} 700 600 0 0 {name=l_d12 lab=d1}

C {sky130_fd_pr/pfet_g5v0d10v5.sym} 920 400 0 1 {name=XM2
L=4
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}

N 900 370 900 250 {lab=tail_s}
N 900 250 800 250 {lab=tail_s}
N 900 430 900 600 {lab=d2}
N 940 400 1100 400 {lab=vfb}

C {devices/lab_pin.sym} 1100 400 2 0 {name=l_vfb2 lab=vfb}
C {devices/lab_pin.sym} 900 600 0 0 {name=l_d22 lab=d2}

C {sky130_fd_pr/nfet_g5v0d10v5.sym} 680 800 0 0 {name=XMn_l
L=8
W=20
nf=1
mult=2
model=nfet_g5v0d10v5
spiceprefix=X
}

N 700 830 700 1050 {lab=gnd}
N 700 770 700 600 {lab=d1}
N 660 800 600 800 {lab=d1}
N 600 800 600 600 {lab=d1}
N 600 600 700 600 {lab=d1}

C {devices/lab_pin.sym} 700 1050 0 0 {name=l_gnd4 lab=gnd}

C {sky130_fd_pr/nfet_g5v0d10v5.sym} 920 800 0 1 {name=XMn_r
L=8
W=20
nf=1
mult=2
model=nfet_g5v0d10v5
spiceprefix=X
}

N 900 830 900 1050 {lab=gnd}
N 900 770 900 600 {lab=d2}
N 940 800 1000 800 {lab=d1}
N 1000 800 1000 600 {lab=d1}
N 1000 600 700 600 {lab=d1}

C {devices/lab_pin.sym} 900 1050 0 0 {name=l_gnd5 lab=gnd}
C {devices/lab_pin.sym} 1000 800 2 0 {name=l_d13 lab=d1}

C {sky130_fd_pr/nfet_g5v0d10v5.sym} 1580 800 0 0 {name=XMcs
L=1
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}

N 1600 830 1600 1050 {lab=gnd}
N 1600 770 1600 600 {lab=vout_gate}
N 1560 800 1400 800 {lab=d2}

C {devices/lab_pin.sym} 1600 1050 0 0 {name=l_gnd6 lab=gnd}
C {devices/lab_pin.sym} 1600 600 2 0 {name=l_vout_gate3 lab=vout_gate}
C {devices/lab_pin.sym} 1400 800 0 0 {name=l_d23 lab=d2}

C {sky130_fd_pr/pfet_g5v0d10v5.sym} 1580 200 0 0 {name=XMp_ld
L=4
W=20
nf=1
mult=8
model=pfet_g5v0d10v5
spiceprefix=X
}

N 1600 170 1600 -100 {lab=pvdd}
N 1600 230 1600 600 {lab=vout_gate}
N 1560 200 1400 200 {lab=pb_tail}

C {devices/lab_pin.sym} 1600 -100 2 0 {name=l_pvdd5 lab=pvdd}
C {devices/lab_pin.sym} 1400 200 0 0 {name=l_pb_tail5 lab=pb_tail}

N 1600 600 2000 600 {lab=vout_gate}

C {devices/capa.sym} 1200 600 1 0 {name=Cc
m=1
value=1300p
}

N 1170 600 900 600 {lab=d2}
N 1230 600 1400 600 {lab=comp_mid}

C {devices/lab_pin.sym} 900 600 0 0 {name=l_d24 lab=d2}
C {devices/lab_pin.sym} 1400 600 2 0 {name=l_comp_mid2 lab=comp_mid}

C {devices/res.sym} 1500 600 1 0 {name=Rc
value=11.38k
}

N 1470 600 1400 600 {lab=comp_mid}
N 1530 600 1600 600 {lab=vout_gate}

C {devices/lab_pin.sym} -500 900 0 0 {name=l_ibias2 lab=ibias}
N -500 900 -300 900 {lab=ibias}
N -300 900 -200 900 {lab=ibias}
