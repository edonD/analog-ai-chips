v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {COMPARATORS — Schmitt Trigger Threshold Detectors} -300 -1200 0 0 0.85 0.85 {layer=4}
T {Block 08 — Mode Control — Sub-block 2 of 3} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {4 comparators x (INV1_P + INV1_N + FB_NFET + INV2_P + INV2_N) = 20 MOSFETs} -300 -1065 0 0 0.28 0.28 {layer=13}
T {Each: tap -> INV1(Schmitt) -> INV2(buffer) -> comp    |    Hysteresis: 224-244 mV via feedback NFET} -300 -1035 0 0 0.28 0.28 {layer=5}

C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="Block 08 Sub-2: Comparators -- Analog AI Chips PVDD LDO Regulator"}

* PORT PINS (signals crossing between sub-schematics)
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -920 0 0 {name=p1 lab=tap1}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -890 0 0 {name=p2 lab=tap2}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -860 0 0 {name=p3 lab=tap3}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -830 0 0 {name=p4 lab=tap4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -800 0 0 {name=p5 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -920 0 0 {name=p6 lab=comp1}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -890 0 0 {name=p7 lab=comp2}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -860 0 0 {name=p8 lab=comp3}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -830 0 0 {name=p9 lab=comp4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -180 -800 0 0 {name=p10 lab=gnd}

* ================================================================
* COMP1 (TH1 = 2.51V) — tap1 input
* INV1: XMc1ivp (P:2/2) + XMc1ivn (N:2/2), FB: XMhf1 (N:1.6/100), INV2: XMc1iv2p (P:4/2) + XMc1iv2n (N:2/2)
* ================================================================

T {COMP1 (TH1=2.51V)} -100 -750 0 0 0.5 0.5 {layer=4}
T {Hysteresis: 224 mV} -100 -710 0 0 0.25 0.25 {layer=7}

* --- INV1 PFET: XMc1ivp ---
T {XMc1ivp} -80 -650 0 0 0.22 0.22 {layer=13}
T {P: W=2 L=2} -80 -633 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -20 -600 0 0 {name=XMc1ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 0 -600 20 -600 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -600 2 0 {name=lb501 sig_type=std_logic lab=pvdd}
N 0 -630 0 -680 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -680 2 0 {name=l_pv1a sig_type=std_logic lab=pvdd}
N 0 -570 0 -530 {lab=c1inv}
N -40 -600 -120 -600 {lab=tap1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -120 -600 0 0 {name=l_t1a sig_type=std_logic lab=tap1}

* --- INV1 NFET: XMc1ivn ---
T {XMc1ivn} -80 -470 0 0 0.22 0.22 {layer=13}
T {N: W=2 L=2} -80 -453 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -20 -500 0 0 {name=XMc1ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 0 -500 20 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -500 2 0 {name=lb502 sig_type=std_logic lab=gnd}
N 0 -470 0 -420 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 -420 0 0 {name=lg1a lab=GND}
N 0 -530 0 -530 {lab=c1inv}
N -40 -500 -120 -500 {lab=tap1}
N -120 -500 -120 -600 {lab=tap1}
T {c1inv} 10 -540 0 0 0.28 0.28 {layer=8}

* --- Feedback NFET: XMhf1 (Schmitt trigger) ---
T {XMhf1} 80 -470 0 0 0.22 0.22 {layer=13}
T {N: W=1.6 L=100} 80 -453 0 0 0.18 0.18 {layer=5}
T {FB (hyst)} 80 -436 0 0 0.18 0.18 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 120 -500 0 0 {name=XMhf1 L=100 W=1.6 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 140 -500 160 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 160 -500 2 0 {name=lb503 sig_type=std_logic lab=gnd}
N 140 -470 140 -420 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 140 -420 0 0 {name=lg1b lab=GND}
N 140 -530 0 -530 {lab=c1inv}
N 100 -500 60 -500 {lab=comp1}

* --- INV2 PFET: XMc1iv2p ---
T {XMc1iv2p} 210 -650 0 0 0.22 0.22 {layer=13}
T {P: W=4 L=2} 210 -633 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 270 -600 0 0 {name=XMc1iv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 290 -600 310 -600 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 -600 2 0 {name=lb504 sig_type=std_logic lab=pvdd}
N 290 -630 290 -680 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 290 -680 2 0 {name=l_pv1b sig_type=std_logic lab=pvdd}
N 290 -570 290 -530 {lab=comp1}
N 250 -600 170 -600 {lab=c1inv}
N 170 -600 170 -530 {lab=c1inv}
N 170 -530 0 -530 {lab=c1inv}

* --- INV2 NFET: XMc1iv2n ---
T {XMc1iv2n} 210 -470 0 0 0.22 0.22 {layer=13}
T {N: W=2 L=2} 210 -453 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 270 -500 0 0 {name=XMc1iv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 290 -500 310 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 -500 2 0 {name=lb505 sig_type=std_logic lab=gnd}
N 290 -470 290 -420 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 290 -420 0 0 {name=lg1c lab=GND}
N 290 -530 290 -530 {lab=comp1}
N 250 -500 170 -500 {lab=c1inv}
N 170 -500 170 -530 {lab=c1inv}

T {comp1} 300 -540 0 0 0.3 0.3 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -530 2 0 {name=l_c1 sig_type=std_logic lab=comp1}
N 290 -530 340 -530 {lab=comp1}
N 60 -500 60 -380 {lab=comp1}
N 60 -380 340 -380 {lab=comp1}
N 340 -380 340 -530 {lab=comp1}

* ================================================================
* COMP2 (TH2 = 4.16V) — tap2 input — same topology, FB W=1.05
* ================================================================

T {COMP2 (TH2=4.16V)} 500 -750 0 0 0.5 0.5 {layer=4}
T {Hysteresis: 244 mV   |   FB: W=1.05 L=100} 500 -710 0 0 0.25 0.25 {layer=7}

T {XMc2ivp} 520 -650 0 0 0.22 0.22 {layer=13}
T {P:2/2} 520 -633 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 580 -600 0 0 {name=XMc2ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 600 -600 620 -600 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -600 2 0 {name=lb506 sig_type=std_logic lab=pvdd}
N 600 -630 600 -680 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -680 2 0 {name=l_pv2a sig_type=std_logic lab=pvdd}
N 600 -570 600 -530 {lab=c2inv}
N 560 -600 480 -600 {lab=tap2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 480 -600 0 0 {name=l_t2a sig_type=std_logic lab=tap2}

T {XMc2ivn} 520 -470 0 0 0.22 0.22 {layer=13}
T {N:2/2} 520 -453 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 580 -500 0 0 {name=XMc2ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 600 -500 620 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -500 2 0 {name=lb507 sig_type=std_logic lab=gnd}
N 600 -470 600 -420 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 600 -420 0 0 {name=lg2a lab=GND}
N 600 -530 600 -530 {lab=c2inv}
N 560 -500 480 -500 {lab=tap2}
N 480 -500 480 -600 {lab=tap2}
T {c2inv} 610 -540 0 0 0.28 0.28 {layer=8}

T {XMhf2  N:1.05/100} 680 -470 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 720 -500 0 0 {name=XMhf2 L=100 W=1.05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 740 -500 760 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 760 -500 2 0 {name=lb508 sig_type=std_logic lab=gnd}
N 740 -470 740 -420 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 740 -420 0 0 {name=lg2b lab=GND}
N 740 -530 600 -530 {lab=c2inv}
N 700 -500 660 -500 {lab=comp2}

T {XMc2iv2p P:4/2} 810 -650 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 870 -600 0 0 {name=XMc2iv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 890 -600 910 -600 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 910 -600 2 0 {name=lb509 sig_type=std_logic lab=pvdd}
N 890 -630 890 -680 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 890 -680 2 0 {name=l_pv2b sig_type=std_logic lab=pvdd}
N 890 -570 890 -530 {lab=comp2}
N 850 -600 770 -600 {lab=c2inv}
N 770 -600 770 -530 {lab=c2inv}
N 770 -530 600 -530 {lab=c2inv}

T {XMc2iv2n N:2/2} 810 -470 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 870 -500 0 0 {name=XMc2iv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 890 -500 910 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 910 -500 2 0 {name=lb510 sig_type=std_logic lab=gnd}
N 890 -470 890 -420 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 890 -420 0 0 {name=lg2c lab=GND}
N 890 -530 890 -530 {lab=comp2}
N 850 -500 770 -500 {lab=c2inv}

T {comp2} 900 -540 0 0 0.3 0.3 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -530 2 0 {name=l_c2 sig_type=std_logic lab=comp2}
N 890 -530 940 -530 {lab=comp2}
N 660 -500 660 -380 {lab=comp2}
N 660 -380 940 -380 {lab=comp2}
N 940 -380 940 -530 {lab=comp2}

* ================================================================
* COMP3 (TH3 = 4.44V) — tap3 input — FB W=0.9
* ================================================================

T {COMP3 (TH3=4.44V)} -100 -250 0 0 0.5 0.5 {layer=4}
T {Hysteresis: 233 mV   |   FB: W=0.9 L=100} -100 -210 0 0 0.25 0.25 {layer=7}

T {XMc3ivp P:2/2} -80 -150 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -20 -100 0 0 {name=XMc3ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 0 -100 20 -100 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -100 2 0 {name=lb511 sig_type=std_logic lab=pvdd}
N 0 -130 0 -180 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -180 2 0 {name=l_pv3a sig_type=std_logic lab=pvdd}
N 0 -70 0 -30 {lab=c3inv}
N -40 -100 -120 -100 {lab=tap3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -120 -100 0 0 {name=l_t3a sig_type=std_logic lab=tap3}

T {XMc3ivn N:2/2} -80 30 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -20 0 0 0 {name=XMc3ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 0 0 20 0 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 0 2 0 {name=lb512 sig_type=std_logic lab=gnd}
N 0 30 0 80 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 80 0 0 {name=lg3a lab=GND}
N -40 0 -120 0 {lab=tap3}
N -120 0 -120 -100 {lab=tap3}
T {c3inv} 10 -40 0 0 0.28 0.28 {layer=8}

T {XMhf3 N:0.9/100} 80 30 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 120 0 0 0 {name=XMhf3 L=100 W=0.9 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 140 0 160 0 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 160 0 2 0 {name=lb513 sig_type=std_logic lab=gnd}
N 140 30 140 80 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 140 80 0 0 {name=lg3b lab=GND}
N 140 -30 0 -30 {lab=c3inv}
N 100 0 60 0 {lab=comp3}

T {XMc3iv2p P:4/2} 210 -150 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 270 -100 0 0 {name=XMc3iv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 290 -100 310 -100 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 -100 2 0 {name=lb514 sig_type=std_logic lab=pvdd}
N 290 -130 290 -180 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 290 -180 2 0 {name=l_pv3b sig_type=std_logic lab=pvdd}
N 290 -70 290 -30 {lab=comp3}
N 250 -100 170 -100 {lab=c3inv}
N 170 -100 170 -30 {lab=c3inv}
N 170 -30 0 -30 {lab=c3inv}

T {XMc3iv2n N:2/2} 210 30 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 270 0 0 0 {name=XMc3iv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 290 0 310 0 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 0 2 0 {name=lb515 sig_type=std_logic lab=gnd}
N 290 30 290 80 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 290 80 0 0 {name=lg3c lab=GND}
N 250 0 170 0 {lab=c3inv}

T {comp3} 300 -40 0 0 0.3 0.3 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -30 2 0 {name=l_c3 sig_type=std_logic lab=comp3}
N 290 -30 340 -30 {lab=comp3}
N 60 0 60 120 {lab=comp3}
N 60 120 340 120 {lab=comp3}
N 340 120 340 -30 {lab=comp3}

* ================================================================
* COMP4 (TH4 = 5.52V) — tap4 input — FB W=0.73
* ================================================================

T {COMP4 (TH4=5.52V)} 500 -250 0 0 0.5 0.5 {layer=4}
T {Hysteresis: 235 mV   |   FB: W=0.73 L=100} 500 -210 0 0 0.25 0.25 {layer=7}

T {XMc4ivp P:2/2} 520 -150 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 580 -100 0 0 {name=XMc4ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 600 -100 620 -100 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -100 2 0 {name=lb516 sig_type=std_logic lab=pvdd}
N 600 -130 600 -180 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -180 2 0 {name=l_pv4a sig_type=std_logic lab=pvdd}
N 600 -70 600 -30 {lab=c4inv}
N 560 -100 480 -100 {lab=tap4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 480 -100 0 0 {name=l_t4a sig_type=std_logic lab=tap4}

T {XMc4ivn N:2/2} 520 30 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 580 0 0 0 {name=XMc4ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 600 0 620 0 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 0 2 0 {name=lb517 sig_type=std_logic lab=gnd}
N 600 30 600 80 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 600 80 0 0 {name=lg4a lab=GND}
N 560 0 480 0 {lab=tap4}
N 480 0 480 -100 {lab=tap4}
T {c4inv} 610 -40 0 0 0.28 0.28 {layer=8}

T {XMhf4 N:0.73/100} 680 30 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 720 0 0 0 {name=XMhf4 L=100 W=0.73 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 740 0 760 0 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 760 0 2 0 {name=lb518 sig_type=std_logic lab=gnd}
N 740 30 740 80 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 740 80 0 0 {name=lg4b lab=GND}
N 740 -30 600 -30 {lab=c4inv}
N 700 0 660 0 {lab=comp4}

T {XMc4iv2p P:4/2} 810 -150 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 870 -100 0 0 {name=XMc4iv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 890 -100 910 -100 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 910 -100 2 0 {name=lb519 sig_type=std_logic lab=pvdd}
N 890 -130 890 -180 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 890 -180 2 0 {name=l_pv4b sig_type=std_logic lab=pvdd}
N 890 -70 890 -30 {lab=comp4}
N 850 -100 770 -100 {lab=c4inv}
N 770 -100 770 -30 {lab=c4inv}
N 770 -30 600 -30 {lab=c4inv}

T {XMc4iv2n N:2/2} 810 30 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 870 0 0 0 {name=XMc4iv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 890 0 910 0 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 910 0 2 0 {name=lb520 sig_type=std_logic lab=gnd}
N 890 30 890 80 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 890 80 0 0 {name=lg4c lab=GND}
N 850 0 770 0 {lab=c4inv}

T {comp4} 900 -40 0 0 0.3 0.3 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -30 2 0 {name=l_c4 sig_type=std_logic lab=comp4}
N 890 -30 940 -30 {lab=comp4}
N 660 0 660 120 {lab=comp4}
N 660 120 940 120 {lab=comp4}
N 940 120 940 -30 {lab=comp4}

* ================================================================
* CHARACTERIZATION
* ================================================================
T {All comparators use PVDD-powered CMOS inverters with Schmitt trigger feedback NFETs.} -300 350 0 0 0.28 0.28 {layer=5}
T {Feedback NFET (long L=100um) pulls c_inv LOW when comp=HIGH, raising effective falling trip -> hysteresis.} -300 380 0 0 0.28 0.28 {layer=5}
T {Measured: TH1=2.51V  TH2=4.16V  TH3=4.44V  TH4=5.52V  |  Hysteresis: 224-244 mV  |  16/16 PASS} -300 420 0 0 0.3 0.3 {layer=7}
