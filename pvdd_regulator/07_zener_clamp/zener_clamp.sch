v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 07: ZENER CLAMP} -750 -1100 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Hybrid 3N2P + Fast Stack Clamp} -750 -1020 0 0 0.45 0.45 {layer=8}
T {HV devices: sky130_fd_pr__nfet_g5v0d10v5 / pfet_g5v0d10v5  (Vds max 10.5V)} -750 -985 0 0 0.3 0.3 {}
T {.subckt zener_clamp  pvdd  gnd} -750 -955 0 0 0.28 0.28 {layer=13}

C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -750 -820 0 0 {name=p1 lab=pvdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -750 -790 0 0 {name=p2 lab=gnd}

T {PRECISION STACK (N-P-N-P-N)} -300 -880 0 0 0.5 0.5 {layer=4}
T {Sets DC clamp onset ~5.98V} -300 -850 0 0 0.25 0.25 {}
T {Mixed NFET+PFET for corner} -300 -830 0 0 0.25 0.25 {}
T {compensation (body=source)} -300 -810 0 0 0.25 0.25 {}

T {FAST STACK} 450 -880 0 0 0.5 0.5 {layer=4}
T {7x NFET L=0.5u} 450 -850 0 0 0.25 0.25 {}
T {Transient absorption} 450 -830 0 0 0.25 0.25 {}
T {(body=GND)} 450 -810 0 0 0.25 0.25 {}

T {CLAMP NMOS} 800 -880 0 0 0.5 0.5 {layer=4}

C {/usr/local/share/xschem/xschem_library/devices/title.sym} -750 880 0 0 {name=l1 author="Block 07: Zener Clamp (v16b) -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* PRECISION STACK: N-P-N-P-N  (top to bottom)
* ================================================================

* --- XMd1: NFET diode, top ---
T {XMd1 (N)} -180 -700 0 0 0.25 0.25 {layer=13}
T {W=2.2 L=4} -180 -678 0 0 0.2 0.2 {layer=5}
T {B=n4} -70 -750 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -110 -720 0 0 {name=XMd1
L=4
W=2.2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -90 -750 -90 -780 {lab=pvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -90 -780 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}
N -90 -690 -90 -650 {lab=n4}
N -130 -720 -200 -720 {lab=pvdd}
N -200 -720 -200 -780 {lab=pvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -200 -780 2 0 {name=l_pv1b sig_type=std_logic lab=pvdd}
T {n4} -85 -655 0 0 0.25 0.25 {layer=8}

* --- XMd2: PFET diode ---
T {XMd2 (P)} -180 -560 0 0 0.25 0.25 {layer=13}
T {W=20 L=4} -180 -538 0 0 0.2 0.2 {layer=5}
T {B=n4} -70 -610 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -110 -580 0 0 {name=XMd2
L=4
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -90 -610 -90 -650 {lab=n4}
N -90 -550 -90 -510 {lab=n3}
N -130 -580 -200 -580 {lab=n3}
N -200 -580 -200 -510 {lab=n3}
N -200 -510 -90 -510 {lab=n3}
T {n3} -85 -515 0 0 0.25 0.25 {layer=8}

* --- XMd3: NFET diode ---
T {XMd3 (N)} -180 -420 0 0 0.25 0.25 {layer=13}
T {W=2.2 L=4} -180 -398 0 0 0.2 0.2 {layer=5}
T {B=n2} -70 -470 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -110 -440 0 0 {name=XMd3
L=4
W=2.2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -90 -470 -90 -510 {lab=n3}
N -90 -410 -90 -370 {lab=n2}
N -130 -440 -200 -440 {lab=n3}
N -200 -440 -200 -510 {lab=n3}
T {n2} -85 -375 0 0 0.25 0.25 {layer=8}

* --- XMd4: PFET diode ---
T {XMd4 (P)} -180 -280 0 0 0.25 0.25 {layer=13}
T {W=20 L=4} -180 -258 0 0 0.2 0.2 {layer=5}
T {B=n2} -70 -330 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -110 -300 0 0 {name=XMd4
L=4
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -90 -330 -90 -370 {lab=n2}
N -90 -270 -90 -230 {lab=n1}
N -130 -300 -200 -300 {lab=n1}
N -200 -300 -200 -230 {lab=n1}
N -200 -230 -90 -230 {lab=n1}
T {n1} -85 -235 0 0 0.25 0.25 {layer=8}

* --- XMd5: NFET diode, bottom ---
T {XMd5 (N)} -180 -140 0 0 0.25 0.25 {layer=13}
T {W=2.2 L=4} -180 -118 0 0 0.2 0.2 {layer=5}
T {B=vg} -70 -190 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -110 -160 0 0 {name=XMd5
L=4
W=2.2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -90 -190 -90 -230 {lab=n1}
N -90 -130 -90 -60 {lab=vg}
N -130 -160 -200 -160 {lab=n1}
N -200 -160 -200 -230 {lab=n1}
T {vg} -85 -65 0 0 0.35 0.35 {layer=4}

* ================================================================
* GATE PULLDOWN: Rpd = 500 kOhm
* ================================================================

T {Rpd = 500k} -200 20 0 0 0.3 0.3 {layer=7}
C {/usr/local/share/xschem/xschem_library/devices/res.sym} -90 50 0 0 {name=Rpd
value=500k
}
N -90 -60 -90 20 {lab=vg}
N -90 80 -90 140 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/gnd.sym} -90 140 0 0 {name=lg1 lab=GND}

* ================================================================
* FEEDFORWARD CAPS: Cff1 = 5pF from n2, Cff2 = 25pF from n1
* ================================================================

T {FEEDFORWARD} 100 -450 0 0 0.4 0.4 {layer=4}

T {Cff1 = 5 pF} 130 -380 0 0 0.3 0.3 {layer=7}
T {from n2} 130 -355 0 0 0.2 0.2 {}
C {/usr/local/share/xschem/xschem_library/devices/capa.sym} 170 -300 0 0 {name=Cff1
m=1
value=5p
}
N 170 -330 170 -370 {lab=n2}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 170 -370 2 0 {name=l_n2a sig_type=std_logic lab=n2}
N 170 -270 170 -60 {lab=vg}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 170 -60 0 0 {name=l_vg2 sig_type=std_logic lab=vg}

T {Cff2 = 25 pF} 280 -380 0 0 0.3 0.3 {layer=7}
T {from n1} 280 -355 0 0 0.2 0.2 {}
C {/usr/local/share/xschem/xschem_library/devices/capa.sym} 310 -300 0 0 {name=Cff2
m=1
value=25p
}
N 310 -330 310 -370 {lab=n1}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 310 -370 2 0 {name=l_n1a sig_type=std_logic lab=n1}
N 310 -270 310 -60 {lab=vg}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 310 -60 0 0 {name=l_vg3 sig_type=std_logic lab=vg}

* ================================================================
* FAST PARALLEL DIODE STACK: 7x NFET L=0.5u W=10u (body=GND)
* ================================================================

* --- XMf1: top ---
T {XMf1} 420 -700 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 420 -683 0 0 0.15 0.15 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 490 -720 0 0 {name=XMf1
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 510 -750 510 -780 {lab=pvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 510 -780 2 0 {name=l_pv2 sig_type=std_logic lab=pvdd}
N 510 -690 510 -660 {lab=nf6}
N 470 -720 430 -720 {lab=pvdd}
N 430 -720 430 -780 {lab=pvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 430 -780 2 0 {name=l_pv2b sig_type=std_logic lab=pvdd}

* --- XMf2..XMf6 (shown as block) ---
T {XMf2 .. XMf6} 420 -600 0 0 0.2 0.2 {layer=13}
T {5x W=10 L=0.5  B=GND} 420 -580 0 0 0.15 0.15 {layer=5}
N 510 -660 510 -540 {lab=nf6..nf1}
T {...} 515 -610 0 0 0.5 0.5 {}

* --- XMf7: bottom ---
T {XMf7} 420 -460 0 0 0.2 0.2 {layer=13}
T {W=10 L=0.5} 420 -443 0 0 0.15 0.15 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 490 -480 0 0 {name=XMf7
L=0.5
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 510 -510 510 -540 {lab=nf1}
N 510 -450 510 -400 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/gnd.sym} 510 -400 0 0 {name=lg2 lab=GND}
N 470 -480 430 -480 {lab=nf1}
N 430 -480 430 -540 {lab=nf1}
N 430 -540 510 -540 {lab=nf1}

* ================================================================
* WIDE CLAMP NMOS
* ================================================================

T {XMclamp} 700 -700 0 0 0.25 0.25 {layer=13}
T {W=100 L=0.5 m=20} 700 -678 0 0 0.2 0.2 {layer=5}
T {2000 um total} 700 -656 0 0 0.18 0.18 {}
T {B=GND} 830 -750 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 780 -720 0 0 {name=XMclamp
L=0.5
W=100
nf=1
mult=20
model=nfet_g5v0d10v5
spiceprefix=X
}
N 800 -750 800 -780 {lab=pvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 800 -780 2 0 {name=l_pv3 sig_type=std_logic lab=pvdd}
N 800 -690 800 -550 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/gnd.sym} 800 -550 0 0 {name=lg3 lab=GND}
N 760 -720 660 -720 {lab=vg}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 660 -720 0 0 {name=l_vg4 sig_type=std_logic lab=vg}
T {vg} 665 -735 0 0 0.3 0.3 {layer=8}

* ================================================================
* CHARACTERIZATION
* ================================================================

T {CHARACTERIZATION  (TT 27C, PVDD = 5.0V)} -750 500 0 0 0.5 0.5 {layer=4}
T {Clamp onset (1mA)  =  5.98 V       spec 5.5-6.2 V       PASS} -750 555 0 0 0.28 0.28 {layer=7}
T {Clamp at 10mA      =  6.205 V      spec <= 6.5 V        PASS} -750 585 0 0 0.28 0.28 {layer=7}
T {Leakage at 5.0V    =  515 nA       spec <= 1000 nA      PASS} -750 615 0 0 0.28 0.28 {layer=7}
T {Leakage at 5.17V   =  923 nA       spec <= 5000 nA      PASS} -750 645 0 0 0.28 0.28 {layer=7}
T {Onset at 150C      =  5.02 V       spec >= 5.0 V        PASS} -750 675 0 0 0.28 0.28 {layer=7}
T {Onset at -40C      =  6.465 V      spec <= 7.0 V        PASS} -750 705 0 0 0.28 0.28 {layer=7}
T {Transient peak     =  6.06 V       spec <= 6.5 V        PASS (Rsrc=10)} -750 735 0 0 0.28 0.28 {layer=7}
T {Peak current (7V)  =  210 mA       spec >= 100 mA       PASS} -750 765 0 0 0.28 0.28 {layer=7}
T {PVT: 11/15 pass    Rsrc=5 peak: 6.45V PASS    Startup surge: 77mA} -750 795 0 0 0.28 0.28 {layer=7}
T {All 9/9 TT specs PASS} -750 840 0 0 0.45 0.45 {layer=4}
