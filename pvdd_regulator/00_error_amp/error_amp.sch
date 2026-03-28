v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 00: ERROR AMPLIFIER} -580 -1060 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator} -580 -980 0 0 0.5 0.5 {layer=8}
T {SkyWater SKY130A Process  |  Two-Stage Miller-Compensated OTA} -580 -940 0 0 0.4 0.4 {}
T {All devices: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  (HV, Vds max = 10.5V)} -580 -900 0 0 0.35 0.35 {}
T {Date: 2026-03-28} -580 -860 0 0 0.3 0.3 {}
T {.subckt error_amp  vref  vfb  vout_gate  pvdd  gnd  ibias  en} -580 -820 0 0 0.3 0.3 {layer=13}

T {ENABLE} -560 -720 0 0 0.5 0.5 {layer=4}
T {BIAS} -200 -720 0 0 0.5 0.5 {layer=4}
T {STAGE 1: DIFF PAIR + MIRROR} 270 -720 0 0 0.5 0.5 {layer=4}
T {MILLER COMP} 700 -720 0 0 0.5 0.5 {layer=4}
T {STAGE 2} 920 -720 0 0 0.5 0.5 {layer=4}

C {/usr/share/xschem/xschem_library/devices/title.sym} -580 780 0 0 {name=l1 author="Block 00: Error Amplifier -- Analog AI Chips PVDD LDO Regulator"}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -580 -300 0 0 {name=p1 lab=vref}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -580 -260 0 0 {name=p2 lab=vfb}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -580 -220 0 0 {name=p3 lab=ibias}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -580 -180 0 0 {name=p4 lab=en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 1160 -200 0 0 {name=p5 lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -580 -380 0 0 {name=p6 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -580 -140 0 0 {name=p7 lab=gnd}

C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -530 -380 0 0 {name=l_pvdd sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -530 -140 0 0 {name=l_gnd sig_type=std_logic lab=gnd}

T {XMen  (enable switch)} -530 220 0 0 0.25 0.25 {layer=13}
T {W=20 L=1 m=1} -530 245 0 0 0.22 0.22 {layer=5}
T {B=GND} -470 195 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -480 160 0 0 {name=XMen
L=1
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -460 190 -460 270 {lab=gnd}
N -460 130 -460 60 {lab=ibias_en}
N -500 160 -560 160 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -560 160 0 0 {name=l_en1 sig_type=std_logic lab=en}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -460 270 0 0 {name=l_gnd_en lab=GND}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -460 60 2 0 {name=l_ibias_en1 sig_type=std_logic lab=ibias_en}

T {XMpu  (pullup when disabled)} -530 -580 0 0 0.25 0.25 {layer=13}
T {W=20 L=1 m=1} -530 -555 0 0 0.22 0.22 {layer=5}
T {B=PVDD} -470 -640 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -480 -610 0 0 {name=XMpu
L=1
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -460 -640 -460 -680 {lab=pvdd}
N -460 -580 -460 -510 {lab=vout_gate}
N -500 -610 -560 -610 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -560 -610 0 0 {name=l_en2 sig_type=std_logic lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -460 -680 2 0 {name=l_pvdd2 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -460 -510 0 0 {name=l_vout_gate_pu sig_type=std_logic lab=vout_gate}

T {XMbn0  (1 uA diode)} -200 220 0 0 0.25 0.25 {layer=13}
T {W=20 L=8 m=1} -200 245 0 0 0.22 0.22 {layer=5}
T {B=GND} -130 195 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -140 160 0 0 {name=XMbn0
L=8
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -120 190 -120 270 {lab=gnd}
N -120 130 -120 60 {lab=ibias_en}
N -160 160 -220 160 {lab=ibias_en}
N -220 160 -220 60 {lab=ibias_en}
N -220 60 -120 60 {lab=ibias_en}
N -460 60 -220 60 {lab=ibias_en}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -120 270 0 0 {name=l_gnd2 lab=GND}

T {XMbn_pb  (20 uA mirror)} -10 220 0 0 0.25 0.25 {layer=13}
T {W=20 L=8 m=20} -10 245 0 0 0.22 0.22 {layer=5}
T {B=GND} 80 195 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 50 160 0 0 {name=XMbn_pb
L=8
W=20
nf=1
mult=20
model=nfet_g5v0d10v5
spiceprefix=X
}
N 70 190 70 270 {lab=gnd}
N 70 130 70 -30 {lab=pb_tail}
N 30 160 -120 160 {lab=ibias_en}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 70 270 0 0 {name=l_gnd3 lab=GND}

T {XMbp0  (PMOS mirror)} -10 -580 0 0 0.25 0.25 {layer=13}
T {W=20 L=4 m=4} -10 -555 0 0 0.22 0.22 {layer=5}
T {B=PVDD} 80 -640 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 50 -610 0 0 {name=XMbp0
L=4
W=20
nf=1
mult=4
model=pfet_g5v0d10v5
spiceprefix=X
}
N 70 -640 70 -680 {lab=pvdd}
N 70 -580 70 -460 {lab=pb_tail}
N 30 -610 -30 -610 {lab=pb_tail}
N -30 -610 -30 -30 {lab=pb_tail}
N -30 -30 70 -30 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 70 -680 2 0 {name=l_pvdd3 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 70 -460 0 0 {name=l_pb_tail1 sig_type=std_logic lab=pb_tail}

T {XMtail  (20 uA tail)} 270 -580 0 0 0.25 0.25 {layer=13}
T {W=20 L=4 m=4} 270 -555 0 0 0.22 0.22 {layer=5}
T {B=PVDD} 350 -640 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 320 -610 0 0 {name=XMtail
L=4
W=20
nf=1
mult=4
model=pfet_g5v0d10v5
spiceprefix=X
}
N 340 -640 340 -680 {lab=pvdd}
N 340 -580 340 -480 {lab=tail_s}
N 300 -610 200 -610 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -680 2 0 {name=l_pvdd4 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 200 -610 0 0 {name=l_pb_tail2 sig_type=std_logic lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -480 0 0 {name=l_tail_s1 sig_type=std_logic lab=tail_s}

T {XM1  (+) vref} 220 -380 0 0 0.25 0.25 {layer=13}
T {W=80 L=4 m=2} 220 -355 0 0 0.22 0.22 {layer=5}
T {B=PVDD} 310 -450 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 280 -420 0 0 {name=XM1
L=4
W=80
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
N 300 -450 300 -480 {lab=tail_s}
N 300 -480 340 -480 {lab=tail_s}
N 300 -390 300 -280 {lab=d1}
N 260 -420 180 -420 {lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -420 0 0 {name=l_vref2 sig_type=std_logic lab=vref}

T {XM2  (-) vfb} 500 -380 0 0 0.25 0.25 {layer=13}
T {W=80 L=4 m=2} 500 -355 0 0 0.22 0.22 {layer=5}
T {B=PVDD} 590 -450 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 540 -420 0 1 {name=XM2
L=4
W=80
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
N 520 -450 520 -480 {lab=tail_s}
N 520 -480 340 -480 {lab=tail_s}
N 520 -390 520 -280 {lab=d2}
N 560 -420 640 -420 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 640 -420 2 0 {name=l_vfb2 sig_type=std_logic lab=vfb}

T {XMn_l  (mirror diode)} 220 -120 0 0 0.25 0.25 {layer=13}
T {W=20 L=8 m=2} 220 -95 0 0 0.22 0.22 {layer=5}
T {B=GND} 310 -200 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 280 -170 0 0 {name=XMn_l
L=8
W=20
nf=1
mult=2
model=nfet_g5v0d10v5
spiceprefix=X
}
N 300 -140 300 -60 {lab=gnd}
N 300 -200 300 -280 {lab=d1}
N 260 -170 200 -170 {lab=d1}
N 200 -170 200 -280 {lab=d1}
N 200 -280 300 -280 {lab=d1}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 300 -60 0 0 {name=l_gnd4 lab=GND}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -280 2 0 {name=l_d1 sig_type=std_logic lab=d1}

T {XMn_r  (mirror output)} 500 -120 0 0 0.25 0.25 {layer=13}
T {W=20 L=8 m=2} 500 -95 0 0 0.22 0.22 {layer=5}
T {B=GND} 590 -200 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 540 -170 0 1 {name=XMn_r
L=8
W=20
nf=1
mult=2
model=nfet_g5v0d10v5
spiceprefix=X
}
N 520 -140 520 -60 {lab=gnd}
N 520 -200 520 -280 {lab=d2}
N 560 -170 620 -170 {lab=d1}
N 620 -170 620 -280 {lab=d1}
N 620 -280 300 -280 {lab=d1}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 520 -60 0 0 {name=l_gnd5 lab=GND}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 -280 0 0 {name=l_d2 sig_type=std_logic lab=d2}

T {Cc = 36 pF} 700 -340 0 0 0.35 0.35 {layer=7}
T {(Miller cap)} 700 -310 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 740 -280 1 0 {name=Cc
m=1
value=36p
}
N 710 -280 520 -280 {lab=d2}
N 770 -280 840 -280 {lab=comp_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 840 -280 2 0 {name=l_comp_mid1 sig_type=std_logic lab=comp_mid}

T {Rc = 5 kohm} 860 -340 0 0 0.35 0.35 {layer=7}
T {(nulling R, LHP zero)} 860 -310 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/res.sym} 900 -280 1 0 {name=Rc
value=5k
}
N 870 -280 840 -280 {lab=comp_mid}
N 930 -280 1000 -280 {lab=vout_gate}

T {XMcs  (CS amp)} 930 -120 0 0 0.25 0.25 {layer=13}
T {W=20 L=1 m=1} 930 -95 0 0 0.22 0.22 {layer=5}
T {B=GND} 1020 -200 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 980 -170 0 0 {name=XMcs
L=1
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 1000 -140 1000 -60 {lab=gnd}
N 1000 -200 1000 -280 {lab=vout_gate}
N 960 -170 880 -170 {lab=d2}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1000 -60 0 0 {name=l_gnd6 lab=GND}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 -170 0 0 {name=l_d2_cs sig_type=std_logic lab=d2}

T {XMp_ld  (~40 uA load)} 930 -580 0 0 0.25 0.25 {layer=13}
T {W=20 L=4 m=8} 930 -555 0 0 0.22 0.22 {layer=5}
T {B=PVDD} 1020 -640 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 980 -610 0 0 {name=XMp_ld
L=4
W=20
nf=1
mult=8
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1000 -640 1000 -680 {lab=pvdd}
N 1000 -580 1000 -280 {lab=vout_gate}
N 960 -610 880 -610 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -680 2 0 {name=l_pvdd5 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 -610 0 0 {name=l_pb_tail3 sig_type=std_logic lab=pb_tail}

N 1000 -280 1160 -280 {lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1160 -280 2 0 {name=l_vout_gate_out sig_type=std_logic lab=vout_gate}

T {CHARACTERIZATION  (TT 27C, PVDD = 5.0V)} -580 400 0 0 0.5 0.5 {layer=4}
T {DC Gain              =  78.4 dB       spec >= 60 dB         PASS} -580 460 0 0 0.3 0.3 {layer=7}
T {UGB                  =  513 kHz       spec >= 500 kHz       PASS} -580 495 0 0 0.3 0.3 {layer=7}
T {Phase Margin         =  67.5 deg      spec [60, 80] deg     PASS} -580 530 0 0 0.3 0.3 {layer=7}
T {Gain Slope at UGB    =  -25.7 dB/dec  (proper -20 dB/dec)   PASS} -580 565 0 0 0.3 0.3 {layer=7}
T {Cc                   =  36 pF         spec <= 50 pF         PASS} -580 600 0 0 0.3 0.3 {layer=7}
T {Quiescent Current    =  86.3 uA       spec <= 100 uA        PASS} -580 635 0 0 0.3 0.3 {layer=7}
T {Input Offset         =  0.03 mV       spec <= 5 mV          PASS} -580 670 0 0 0.3 0.3 {layer=7}
T {Output Swing         =  9.7 mV to 5.0 V                     PASS} -580 705 0 0 0.3 0.3 {layer=7}
T {CMRR                 =  108.2 dB      spec >= 50 dB         PASS} -580 740 0 0 0.3 0.3 {layer=7}
T {PSRR                 =  108.3 dB      spec >= 40 dB         PASS} -580 775 0 0 0.3 0.3 {layer=7}
T {Input Noise          =  33.7 uVrms    spec <= 40 uVrms      PASS} -580 810 0 0 0.3 0.3 {layer=7}
T {PVT: 15/15 corners pass (5 process x 3 temp)} -580 845 0 0 0.3 0.3 {layer=7}
T {All 16/16 specs PASS} -580 900 0 0 0.45 0.45 {layer=4}
