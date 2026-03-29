v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 07: ZENER CLAMP} -650 -1050 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Diode-Stack-Biased NMOS Clamp} -650 -970 0 0 0.45 0.45 {layer=8}
T {All HV: sky130_fd_pr__nfet_g5v0d10v5  (Vds max 10.5V)} -650 -935 0 0 0.3 0.3 {}
T {.subckt zener_clamp  pvdd  gnd} -650 -905 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/iopin.sym} -650 -760 0 0 {name=p1 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -650 -730 0 0 {name=p2 lab=gnd}

C {/usr/share/xschem/xschem_library/devices/title.sym} -650 830 0 0 {name=l1 author="Block 07: Zener Clamp -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* DIODE REFERENCE STACK: 5x diode-connected HV NFETs (L=4u, W=1.8u)
* Vertical stack: PVDD at top, vg at bottom
* Body = Source for all (no body effect)
* ================================================================

T {DIODE REFERENCE STACK} -200 -830 0 0 0.5 0.5 {layer=4}
T {5x diode-connected HV NFET} -200 -800 0 0 0.3 0.3 {}
T {L=4u W=1.8u body=source} -200 -775 0 0 0.25 0.25 {}

* --- XMd1: top diode (drain=gate=pvdd, source=n4) ---
T {XMd1} -80 -660 0 0 0.25 0.25 {layer=13}
T {W=1.8 L=4} -80 -638 0 0 0.2 0.2 {layer=5}
T {B=n4} 10 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -10 -680 0 0 {name=XMd1
L=4
W=1.8
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 10 -710 10 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 -760 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}
N 10 -650 10 -600 {lab=n4}
N -30 -680 -100 -680 {lab=pvdd}
N -100 -680 -100 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -760 2 0 {name=l_pv2 sig_type=std_logic lab=pvdd}
T {n4} 15 -605 0 0 0.25 0.25 {layer=8}

* --- XMd2 ---
T {XMd2} -80 -520 0 0 0.25 0.25 {layer=13}
T {W=1.8 L=4} -80 -498 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -10 -540 0 0 {name=XMd2
L=4
W=1.8
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 10 -570 10 -600 {lab=n4}
N 10 -510 10 -460 {lab=n3}
N -30 -540 -100 -540 {lab=n4}
N -100 -540 -100 -600 {lab=n4}
N -100 -600 10 -600 {lab=n4}
T {n3} 15 -465 0 0 0.25 0.25 {layer=8}

* --- XMd3 ---
T {XMd3} -80 -380 0 0 0.25 0.25 {layer=13}
T {W=1.8 L=4} -80 -358 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -10 -400 0 0 {name=XMd3
L=4
W=1.8
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 10 -430 10 -460 {lab=n3}
N 10 -370 10 -320 {lab=n2}
N -30 -400 -100 -400 {lab=n3}
N -100 -400 -100 -460 {lab=n3}
N -100 -460 10 -460 {lab=n3}
T {n2} 15 -325 0 0 0.25 0.25 {layer=8}

* --- XMd4 ---
T {XMd4} -80 -240 0 0 0.25 0.25 {layer=13}
T {W=1.8 L=4} -80 -218 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -10 -260 0 0 {name=XMd4
L=4
W=1.8
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 10 -290 10 -320 {lab=n2}
N 10 -230 10 -180 {lab=n1}
N -30 -260 -100 -260 {lab=n2}
N -100 -260 -100 -320 {lab=n2}
N -100 -320 10 -320 {lab=n2}
T {n1} 15 -185 0 0 0.25 0.25 {layer=8}

* --- XMd5: bottom diode (source=vg) ---
T {XMd5} -80 -100 0 0 0.25 0.25 {layer=13}
T {W=1.8 L=4} -80 -78 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -10 -120 0 0 {name=XMd5
L=4
W=1.8
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 10 -150 10 -180 {lab=n1}
N 10 -90 10 -30 {lab=vg}
N -30 -120 -100 -120 {lab=n1}
N -100 -120 -100 -180 {lab=n1}
N -100 -180 10 -180 {lab=n1}
T {vg} 15 -35 0 0 0.35 0.35 {layer=4}

* ================================================================
* GATE PULLDOWN: Rpd = 500 kOhm
* ================================================================

T {PULLDOWN} -200 30 0 0 0.5 0.5 {layer=4}
T {Rpd = 500 kOhm} -200 60 0 0 0.3 0.3 {layer=7}

C {/usr/share/xschem/xschem_library/devices/res.sym} 10 80 0 0 {name=Rpd
value=500k
}
N 10 -30 10 50 {lab=vg}
N 10 110 10 170 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 10 170 0 0 {name=lg1 lab=GND}

* ================================================================
* FEEDFORWARD CAP: Cff = 20 pF
* ================================================================

T {FEEDFORWARD} 250 -830 0 0 0.5 0.5 {layer=4}
T {Cff = 20 pF} 250 -800 0 0 0.35 0.35 {layer=7}
T {Fast transient} 250 -775 0 0 0.2 0.2 {}
T {response} 250 -755 0 0 0.2 0.2 {}

C {/usr/share/xschem/xschem_library/devices/capa.sym} 300 -400 0 0 {name=Cff
m=1
value=20p
}
N 300 -430 300 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -760 2 0 {name=l_pv3 sig_type=std_logic lab=pvdd}
N 300 -370 300 -30 {lab=vg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -30 0 0 {name=l_vg2 sig_type=std_logic lab=vg}

* ================================================================
* WIDE CLAMP NMOS: W=100u m=20 = 2000um, L=0.5u
* ================================================================

T {WIDE CLAMP NMOS} 500 -830 0 0 0.5 0.5 {layer=4}
T {XMclamp} 500 -660 0 0 0.25 0.25 {layer=13}
T {W=100 L=0.5 m=20} 500 -638 0 0 0.2 0.2 {layer=5}
T {2000 um total} 500 -616 0 0 0.18 0.18 {}
T {B=GND} 610 -710 0 0 0.2 0.2 {layer=7}

C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -680 0 0 {name=XMclamp
L=0.5
W=100
nf=1
mult=20
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -710 580 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -760 2 0 {name=l_pv4 sig_type=std_logic lab=pvdd}
N 580 -650 580 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 580 -500 0 0 {name=lg2 lab=GND}
N 540 -680 450 -680 {lab=vg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 450 -680 0 0 {name=l_vg3 sig_type=std_logic lab=vg}
T {vg} 455 -695 0 0 0.3 0.3 {layer=8}

* ================================================================
* CHARACTERIZATION
* ================================================================

T {CHARACTERIZATION  (TT 27C, PVDD = 5.0V)} -650 500 0 0 0.5 0.5 {layer=4}
T {Clamp onset (1mA) =  5.925 V     spec 5.5-6.2 V       PASS} -650 555 0 0 0.28 0.28 {layer=7}
T {Clamp at 10mA     =  6.18 V      spec <= 6.5 V        PASS} -650 585 0 0 0.28 0.28 {layer=7}
T {Leakage at 5.0V   =  898 nA      spec <= 1000 nA      PASS} -650 615 0 0 0.28 0.28 {layer=7}
T {Leakage at 5.17V  =  1946 nA     spec <= 5000 nA      PASS} -650 645 0 0 0.28 0.28 {layer=7}
T {Onset at 150C     =  5.115 V     spec >= 5.0 V        PASS} -650 675 0 0 0.28 0.28 {layer=7}
T {Onset at -40C     =  6.31 V      spec <= 7.0 V        PASS} -650 705 0 0 0.28 0.28 {layer=7}
T {Transient peak    =  6.44 V      spec <= 6.5 V        PASS} -650 735 0 0 0.28 0.28 {layer=7}
T {Peak current (7V) =  163 mA      spec >= 100 mA       PASS} -650 765 0 0 0.28 0.28 {layer=7}
T {All 9/9 specs PASS} -650 810 0 0 0.45 0.45 {layer=4}
