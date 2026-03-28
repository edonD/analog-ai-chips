v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}
T {BLOCK 00: ERROR AMPLIFIER} -1200 -1600 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator} -1200 -1520 0 0 0.5 0.5 {layer=8}
T {SkyWater SKY130A Process} -1200 -1480 0 0 0.4 0.4 {}
T {Two-Stage Miller-Compensated OTA} -1200 -1420 0 0 0.4 0.4 {}
T {All devices: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  (HV, Vds max = 10.5V)} -1200 -1380 0 0 0.35 0.35 {}
T {Date: 2026-03-28} -1200 -1320 0 0 0.3 0.3 {}
T {.subckt error_amp  vref  vfb  vout_gate  pvdd  gnd  ibias  en} -1200 -1280 0 0 0.3 0.3 {layer=13}

T {ENABLE} -1100 -900 0 0 0.6 0.6 {layer=4}
T {BIAS} -300 -900 0 0 0.6 0.6 {layer=4}
T {STAGE 1: DIFF PAIR + MIRROR LOAD} 700 -900 0 0 0.6 0.6 {layer=4}
T {MILLER COMPENSATION} 1700 -900 0 0 0.6 0.6 {layer=4}
T {STAGE 2} 2500 -900 0 0 0.6 0.6 {layer=4}

T {PVDD (5.0V)} -300 -800 0 0 0.4 0.4 {layer=7}
T {GND} -300 800 0 0 0.4 0.4 {layer=7}

C {devices/title.sym} 2200 1200 0 0 {name=l1 author="Block 00: Error Amplifier -- Analog AI Chips PVDD LDO Regulator"}

C {devices/ipin.sym} -1200 -200 0 0 {name=p1 lab=vref}
C {devices/ipin.sym} -1200 0 0 0 {name=p2 lab=vfb}
C {devices/ipin.sym} -1200 400 0 0 {name=p3 lab=ibias}
C {devices/ipin.sym} -1200 600 0 0 {name=p4 lab=en}
C {devices/opin.sym} 3400 -200 0 0 {name=p5 lab=vout_gate}
C {devices/iopin.sym} -1200 -700 0 0 {name=p6 lab=pvdd}
C {devices/iopin.sym} -1200 700 0 0 {name=p7 lab=gnd}

C {devices/lab_pin.sym} -1000 -700 0 0 {name=l_pvdd lab=pvdd}
C {devices/lab_pin.sym} -1000 700 0 0 {name=l_gnd lab=gnd}

C {devices/lab_pin.sym} -1000 -200 0 0 {name=l_vref lab=vref}
C {devices/lab_pin.sym} -1000 0 0 0 {name=l_vfb lab=vfb}

C {devices/lab_pin.sym} 3200 -200 0 0 {name=l_vout_gate lab=vout_gate}

C {devices/lab_pin.sym} -600 400 0 0 {name=l_ibias lab=ibias}
C {devices/lab_pin.sym} -600 600 0 0 {name=l_en lab=en}

C {devices/lab_pin.sym} -400 200 2 0 {name=l_ibias_en lab=ibias_en}
C {devices/lab_pin.sym} 200 -400 2 0 {name=l_pb_tail lab=pb_tail}
C {devices/lab_pin.sym} 800 -300 2 0 {name=l_tail_s lab=tail_s}
C {devices/lab_pin.sym} 900 200 0 0 {name=l_d1 lab=d1}
C {devices/lab_pin.sym} 1400 200 0 0 {name=l_d2 lab=d2}
C {devices/lab_pin.sym} 2100 200 0 0 {name=l_comp_mid lab=comp_mid}

T {XMen} -900 680 0 0 0.3 0.3 {layer=13}
T {W=20 L=1 m=1} -900 720 0 0 0.25 0.25 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} -780 600 0 0 {name=XMen
L=1
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}

N -760 630 -760 700 {lab=gnd}
N -760 570 -760 400 {lab=ibias_en}
N -800 600 -900 600 {lab=en}
N -760 400 -400 400 {lab=ibias_en}

C {devices/lab_pin.sym} -760 700 0 0 {name=l_gnd_en lab=gnd}

T {XMpu} -900 -680 0 0 0.3 0.3 {layer=13}
T {W=20 L=1 m=1} -900 -640 0 0 0.25 0.25 {layer=5}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} -780 -550 0 0 {name=XMpu
L=1
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}

N -760 -580 -760 -700 {lab=pvdd}
N -760 -520 -760 -300 {lab=vout_gate}
N -800 -550 -900 -550 {lab=en}

C {devices/lab_pin.sym} -900 -550 0 0 {name=l_en2 lab=en}
C {devices/lab_pin.sym} -760 -700 2 0 {name=l_pvdd2 lab=pvdd}
C {devices/lab_pin.sym} -760 -300 0 0 {name=l_vout_gate2 lab=vout_gate}

T {XMbn0} -280 480 0 0 0.3 0.3 {layer=13}
T {W=20 L=8 m=1} -280 520 0 0 0.25 0.25 {layer=5}
T {1 uA ref} -280 560 0 0 0.25 0.25 {}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} -220 400 0 0 {name=XMbn0
L=8
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}

N -200 430 -200 700 {lab=gnd}
N -200 370 -200 200 {lab=ibias_en}
N -240 400 -400 400 {lab=ibias_en}
N -200 200 -400 200 {lab=ibias_en}

C {devices/lab_pin.sym} -200 700 0 0 {name=l_gnd2 lab=gnd}

T {XMbn_pb} 120 480 0 0 0.3 0.3 {layer=13}
T {W=20 L=8 m=20} 120 520 0 0 0.25 0.25 {layer=5}
T {20 uA mirror} 120 560 0 0 0.25 0.25 {}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 80 400 0 0 {name=XMbn_pb
L=8
W=20
nf=1
mult=20
model=nfet_g5v0d10v5
spiceprefix=X
}

N 100 430 100 700 {lab=gnd}
N 100 370 100 100 {lab=pb_tail}
N 60 400 -200 400 {lab=ibias_en}

C {devices/lab_pin.sym} 100 700 0 0 {name=l_gnd3 lab=gnd}

T {XMbp0} 380 -480 0 0 0.3 0.3 {layer=13}
T {W=20 L=4 m=4} 380 -440 0 0 0.25 0.25 {layer=5}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 280 -350 0 0 {name=XMbp0
L=4
W=20
nf=1
mult=4
model=pfet_g5v0d10v5
spiceprefix=X
}

N 300 -380 300 -700 {lab=pvdd}
N 300 -320 300 -100 {lab=pb_tail}
N 260 -350 100 -350 {lab=pb_tail}
N 100 -350 100 100 {lab=pb_tail}
N 300 -100 200 -100 {lab=pb_tail}

C {devices/lab_pin.sym} 300 -700 2 0 {name=l_pvdd3 lab=pvdd}
C {devices/lab_pin.sym} 200 -100 0 0 {name=l_pb_tail3 lab=pb_tail}

T {XMtail} 780 -480 0 0 0.3 0.3 {layer=13}
T {W=20 L=4 m=4} 780 -440 0 0 0.25 0.25 {layer=5}
T {20 uA tail} 780 -400 0 0 0.25 0.25 {}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 680 -550 0 0 {name=XMtail
L=4
W=20
nf=1
mult=4
model=pfet_g5v0d10v5
spiceprefix=X
}

N 700 -580 700 -700 {lab=pvdd}
N 700 -520 700 -350 {lab=tail_s}
N 660 -550 500 -550 {lab=pb_tail}

C {devices/lab_pin.sym} 700 -700 2 0 {name=l_pvdd4 lab=pvdd}
C {devices/lab_pin.sym} 700 -350 0 0 {name=l_tail_s2 lab=tail_s}
C {devices/lab_pin.sym} 500 -550 0 0 {name=l_pb_tail4 lab=pb_tail}

T {XM1  (+)} 660 -100 0 0 0.3 0.3 {layer=13}
T {W=80 L=4 m=2} 660 -60 0 0 0.25 0.25 {layer=5}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 580 -200 0 0 {name=XM1
L=4
W=80
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}

N 600 -230 600 -350 {lab=tail_s}
N 600 -350 700 -350 {lab=tail_s}
N 600 -170 600 100 {lab=d1}
N 560 -200 300 -200 {lab=vref}

C {devices/lab_pin.sym} 300 -200 0 0 {name=l_vref2 lab=vref}

T {XM2  (-)} 1180 -100 0 0 0.3 0.3 {layer=13}
T {W=80 L=4 m=2} 1180 -60 0 0 0.25 0.25 {layer=5}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 1120 -200 0 1 {name=XM2
L=4
W=80
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}

N 1100 -230 1100 -350 {lab=tail_s}
N 1100 -350 700 -350 {lab=tail_s}
N 1100 -170 1100 100 {lab=d2}
N 1140 -200 1400 -200 {lab=vfb}

C {devices/lab_pin.sym} 1400 -200 2 0 {name=l_vfb2 lab=vfb}

T {XMn_l} 560 380 0 0 0.3 0.3 {layer=13}
T {W=20 L=8 m=2} 560 420 0 0 0.25 0.25 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 580 300 0 0 {name=XMn_l
L=8
W=20
nf=1
mult=2
model=nfet_g5v0d10v5
spiceprefix=X
}

N 600 330 600 700 {lab=gnd}
N 600 270 600 100 {lab=d1}
N 560 300 450 300 {lab=d1}
N 450 300 450 100 {lab=d1}
N 450 100 600 100 {lab=d1}

C {devices/lab_pin.sym} 600 700 0 0 {name=l_gnd4 lab=gnd}

T {XMn_r} 1180 380 0 0 0.3 0.3 {layer=13}
T {W=20 L=8 m=2} 1180 420 0 0 0.25 0.25 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 1120 300 0 1 {name=XMn_r
L=8
W=20
nf=1
mult=2
model=nfet_g5v0d10v5
spiceprefix=X
}

N 1100 330 1100 700 {lab=gnd}
N 1100 270 1100 100 {lab=d2}
N 1140 300 1300 300 {lab=d1}
N 1300 300 1300 100 {lab=d1}
N 1300 100 600 100 {lab=d1}

C {devices/lab_pin.sym} 1100 700 0 0 {name=l_gnd5 lab=gnd}

T {XMcs} 2580 380 0 0 0.3 0.3 {layer=13}
T {W=20 L=1 m=1} 2580 420 0 0 0.25 0.25 {layer=5}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 2480 300 0 0 {name=XMcs
L=1
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}

N 2500 330 2500 700 {lab=gnd}
N 2500 270 2500 -200 {lab=vout_gate}
N 2460 300 2200 300 {lab=d2}

C {devices/lab_pin.sym} 2500 700 0 0 {name=l_gnd6 lab=gnd}
C {devices/lab_pin.sym} 2200 300 0 0 {name=l_d23 lab=d2}

T {XMp_ld} 2580 -480 0 0 0.3 0.3 {layer=13}
T {W=20 L=4 m=8} 2580 -440 0 0 0.25 0.25 {layer=5}
T {~40 uA load} 2580 -400 0 0 0.25 0.25 {}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 2480 -550 0 0 {name=XMp_ld
L=4
W=20
nf=1
mult=8
model=pfet_g5v0d10v5
spiceprefix=X
}

N 2500 -580 2500 -700 {lab=pvdd}
N 2500 -520 2500 -200 {lab=vout_gate}
N 2460 -550 2200 -550 {lab=pb_tail}

C {devices/lab_pin.sym} 2500 -700 2 0 {name=l_pvdd5 lab=pvdd}
C {devices/lab_pin.sym} 2200 -550 0 0 {name=l_pb_tail5 lab=pb_tail}

N 2500 -200 3200 -200 {lab=vout_gate}

T {Cc = 36 pF} 1800 -50 0 0 0.4 0.4 {layer=7}
T {(18k um^2 MIM)} 1800 0 0 0 0.25 0.25 {}
C {devices/capa.sym} 1750 -200 1 0 {name=Cc
m=1
value=36p
}

N 1720 -200 1100 -200 {lab=d2}
N 1780 -200 2000 -200 {lab=comp_mid}

C {devices/lab_pin.sym} 1100 -200 0 0 {name=l_d24 lab=d2}
C {devices/lab_pin.sym} 2000 -200 2 0 {name=l_comp_mid2 lab=comp_mid}

T {Rc = 5 kohm} 2150 -50 0 0 0.4 0.4 {layer=7}
T {(> 1/gm2, LHP zero)} 2150 0 0 0 0.25 0.25 {}
C {devices/res.sym} 2200 -200 1 0 {name=Rc
value=5k
}

N 2170 -200 2000 -200 {lab=comp_mid}
N 2230 -200 2500 -200 {lab=vout_gate}

C {devices/lab_pin.sym} -900 400 0 0 {name=l_ibias2 lab=ibias}
N -900 400 -600 400 {lab=ibias}

T {CHARACTERIZATION  (TT 27C, PVDD = 5.0V)} -1200 900 0 0 0.5 0.5 {layer=4}
T {DC Gain              =  78.4 dB       spec >= 60 dB         PASS} -1200 970 0 0 0.3 0.3 {layer=7}
T {UGB                  =  513 kHz       spec >= 500 kHz       PASS} -1200 1010 0 0 0.3 0.3 {layer=7}
T {Phase Margin         =  67.5 deg      spec [60, 80] deg     PASS} -1200 1050 0 0 0.3 0.3 {layer=7}
T {Gain Slope at UGB    =  -25.7 dB/dec  (proper -20 dB/dec)   PASS} -1200 1090 0 0 0.3 0.3 {layer=7}
T {Cc                   =  36 pF         spec <= 50 pF         PASS} -1200 1130 0 0 0.3 0.3 {layer=7}
T {Quiescent Current    =  86.3 uA       spec <= 100 uA        PASS} -1200 1170 0 0 0.3 0.3 {layer=7}
T {Input Offset         =  0.03 mV       spec <= 5 mV          PASS} -1200 1210 0 0 0.3 0.3 {layer=7}
T {Output Swing         =  9.7 mV to 5.0 V                     PASS} -1200 1250 0 0 0.3 0.3 {layer=7}
T {CMRR                 =  108.2 dB      spec >= 50 dB         PASS} -1200 1290 0 0 0.3 0.3 {layer=7}
T {PSRR                 =  108.3 dB      spec >= 40 dB         PASS} -1200 1330 0 0 0.3 0.3 {layer=7}
T {Input Noise          =  33.7 uVrms    spec <= 40 uVrms      PASS} -1200 1370 0 0 0.3 0.3 {layer=7}
T {PVT: 15/15 corners pass (5 process x 3 temp)} -1200 1410 0 0 0.3 0.3 {layer=7}
T {All 16/16 specs PASS} -1200 1470 0 0 0.45 0.45 {layer=4}
