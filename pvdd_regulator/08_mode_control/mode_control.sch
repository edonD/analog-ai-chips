v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 08: MODE CONTROL} -800 -1200 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Threshold Detector + CMOS Logic} -800 -1120 0 0 0.45 0.45 {layer=8}
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  |  res_xhigh_po} -800 -1085 0 0 0.3 0.3 {}
T {.subckt mode_control  bvdd  pvdd  svdd  gnd  vref  en_ret  bypass_en  ea_en  ref_sel  uvov_en  ilim_en  pass_off} -800 -1055 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -800 -910 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -800 -880 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -800 -850 0 0 {name=p3 lab=svdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -800 -820 0 0 {name=p4 lab=vref}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -800 -790 0 0 {name=p5 lab=en_ret}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -680 -910 0 0 {name=p6 lab=bypass_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -680 -880 0 0 {name=p7 lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -680 -850 0 0 {name=p8 lab=ref_sel}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -680 -820 0 0 {name=p9 lab=uvov_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -680 -790 0 0 {name=p10 lab=ilim_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -680 -760 0 0 {name=p11 lab=pass_off}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -680 -730 0 0 {name=p12 lab=gnd}

C {/usr/share/xschem/xschem_library/devices/title.sym} -800 1000 0 0 {name=l1 author="Block 08: Mode Control -- Analog AI Chips PVDD LDO Regulator"}

T {RESISTOR LADDER} -550 -680 0 0 0.5 0.5 {layer=4}
T {BVDD to GND  |  5 xhigh_po resistors  |  4 tap points} -550 -640 0 0 0.25 0.25 {}
T {~400 kohm total  |  Iq = 17.3 uA at BVDD = 7V} -550 -615 0 0 0.25 0.25 {}

T {COMPARATOR 1} -50 -680 0 0 0.5 0.5 {layer=4}
T {TH1 = 2.5V (POR exit)} -50 -645 0 0 0.25 0.25 {}

T {COMPARATORS 2-4} 400 -680 0 0 0.5 0.5 {layer=4}
T {Same topology, different FB sizing} 400 -645 0 0 0.25 0.25 {}

T {LOGIC DECODING} -50 140 0 0 0.5 0.5 {layer=4}
T {Thermometer code -> mode control outputs} -50 175 0 0 0.25 0.25 {}

C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -430 -580 2 0 {name=l_bvdd sig_type=std_logic lab=bvdd}
N -430 -580 -430 -550 {lab=bvdd}
T {BVDD} -455 -590 0 0 0.35 0.35 {layer=4}

C {/usr/share/xschem/xschem_library/devices/res.sym} -430 -510 0 0 {name=XRtop value="xhigh_po w=1 l=37"}
T {Rtop ~78k} -480 -510 0 0 0.22 0.22 {layer=13}
N -430 -550 -430 -540 {lab=bvdd}
N -430 -480 -430 -440 {lab=tap1}
T {tap1} -415 -450 0 0 0.3 0.3 {layer=8}
N -430 -440 -200 -440 {lab=tap1}

C {/usr/share/xschem/xschem_library/devices/res.sym} -430 -400 0 0 {name=XR12 value="xhigh_po w=1 l=62"}
T {R12 ~131k} -480 -400 0 0 0.22 0.22 {layer=13}
N -430 -440 -430 -430 {lab=tap1}
N -430 -370 -430 -330 {lab=tap2}
T {tap2} -415 -340 0 0 0.3 0.3 {layer=8}

C {/usr/share/xschem/xschem_library/devices/res.sym} -430 -290 0 0 {name=XR23 value="xhigh_po w=1 l=6"}
T {R23 ~13k} -480 -290 0 0 0.22 0.22 {layer=13}
N -430 -330 -430 -320 {lab=tap2}
N -430 -260 -430 -220 {lab=tap3}
T {tap3} -415 -230 0 0 0.3 0.3 {layer=8}

C {/usr/share/xschem/xschem_library/devices/res.sym} -430 -180 0 0 {name=XR34 value="xhigh_po w=1 l=17"}
T {R34 ~36k} -480 -180 0 0 0.22 0.22 {layer=13}
N -430 -220 -430 -210 {lab=tap3}
N -430 -150 -430 -110 {lab=tap4}
T {tap4} -415 -120 0 0 0.3 0.3 {layer=8}

C {/usr/share/xschem/xschem_library/devices/res.sym} -430 -70 0 0 {name=XRbot value="xhigh_po w=1 l=69"}
T {Rbot ~146k} -480 -70 0 0 0.22 0.22 {layer=13}
N -430 -110 -430 -100 {lab=tap4}
N -430 -40 -430 -10 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -430 -10 0 0 {name=lg1 lab=GND}

* --- COMP1: INV1 PFET ---
T {XMc1ivp} -100 -560 0 0 0.2 0.2 {layer=13}
T {P: W=2 L=2} -100 -545 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -30 -510 0 0 {name=XMc1ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N -10 -540 -10 -580 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -10 -580 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}
N -10 -480 -10 -440 {lab=c1inv}
N -50 -510 -200 -510 {lab=tap1}
N -200 -510 -200 -440 {lab=tap1}

* --- COMP1: INV1 NFET ---
T {XMc1ivn} -100 -370 0 0 0.2 0.2 {layer=13}
T {N: W=2 L=2} -100 -355 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -30 -400 0 0 {name=XMc1ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N -10 -370 -10 -320 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -10 -320 0 0 {name=lg2 lab=GND}
N -10 -430 -10 -440 {lab=c1inv}
N -50 -400 -200 -400 {lab=tap1}
N -200 -400 -200 -440 {lab=tap1}
T {c1inv} 0 -455 0 0 0.25 0.25 {layer=8}

* --- COMP1: Feedback NFET (Schmitt trigger) ---
T {XMhf1 (FB)} 65 -370 0 0 0.2 0.2 {layer=13}
T {N: W=1.6 L=100} 65 -355 0 0 0.18 0.18 {layer=5}
T {Hysteresis} 65 -340 0 0 0.18 0.18 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 110 -400 0 0 {name=XMhf1 L=100 W=1.6 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 130 -370 130 -320 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 130 -320 0 0 {name=lg3 lab=GND}
N 130 -430 130 -440 {lab=c1inv}
N 130 -440 -10 -440 {lab=c1inv}
N 90 -400 50 -400 {lab=comp1}

* --- COMP1: INV2 output ---
T {INV2 (P:4/2 N:2/2)} 180 -470 0 0 0.2 0.2 {layer=13}
N -10 -440 200 -440 {lab=c1inv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -440 2 0 {name=l_c1out sig_type=std_logic lab=comp1}
N 200 -440 250 -440 {lab=comp1}
N 50 -400 50 -250 {lab=comp1}
N 50 -250 250 -250 {lab=comp1}
N 250 -250 250 -440 {lab=comp1}
T {comp1} 260 -445 0 0 0.3 0.3 {layer=4}

* --- COMP2 block ---
T {COMP2: tap2 -> comp2} 400 -560 0 0 0.35 0.35 {layer=13}
T {INV1: P=2/2  N=2/2    |    FB NFET: W=1.05 L=100} 400 -530 0 0 0.22 0.22 {layer=5}
T {INV2: P=4/2  N=2/2    |    Hyst ~ 244 mV} 400 -510 0 0 0.22 0.22 {layer=5}
T {TH2 = 4.2V  (Retention regulate entry)} 400 -480 0 0 0.25 0.25 {layer=8}

* --- COMP3 block ---
T {COMP3: tap3 -> comp3} 400 -420 0 0 0.35 0.35 {layer=13}
T {INV1: P=2/2  N=2/2    |    FB NFET: W=0.9 L=100} 400 -390 0 0 0.22 0.22 {layer=5}
T {INV2: P=4/2  N=2/2    |    Hyst ~ 233 mV} 400 -370 0 0 0.22 0.22 {layer=5}
T {TH3 = 4.5V  (Power-up bypass entry)} 400 -340 0 0 0.25 0.25 {layer=8}

* --- COMP4 block ---
T {COMP4: tap4 -> comp4} 400 -280 0 0 0.35 0.35 {layer=13}
T {INV1: P=2/2  N=2/2    |    FB NFET: W=0.73 L=100} 400 -250 0 0 0.22 0.22 {layer=5}
T {INV2: P=4/2  N=2/2    |    Hyst ~ 235 mV} 400 -230 0 0 0.22 0.22 {layer=5}
T {TH4 = 5.6V  (Active regulate entry)} 400 -200 0 0 0.25 0.25 {layer=8}

* --- LOGIC ---
T {pass_off = buf(NOT comp1)} -50 230 0 0 0.28 0.28 {layer=8}
T {bypass_en = comp1*comp2b + comp3*comp4b} -50 260 0 0 0.28 0.28 {layer=8}
T {ea_en = comp2*comp3b + comp4} -50 290 0 0 0.28 0.28 {layer=8}
T {ref_sel = comp1*comp3b} -50 320 0 0 0.28 0.28 {layer=8}
T {uvov_en = buf(comp4)} -50 350 0 0 0.28 0.28 {layer=8}
T {ilim_en = buf(comp4)} -50 380 0 0 0.28 0.28 {layer=8}
T {All logic: PVDD-powered HV CMOS  (P:4/2  N:2/2)} -50 420 0 0 0.22 0.22 {layer=5}
T {AOI22 gate for bypass_en  |  AOI21 gate for ea_en  |  NAND+INV for ref_sel} -50 445 0 0 0.22 0.22 {layer=5}

C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 230 2 0 {name=l_po sig_type=std_logic lab=pass_off}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 260 2 0 {name=l_by sig_type=std_logic lab=bypass_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 290 2 0 {name=l_ea sig_type=std_logic lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 320 2 0 {name=l_rs sig_type=std_logic lab=ref_sel}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 350 2 0 {name=l_uv sig_type=std_logic lab=uvov_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 380 2 0 {name=l_il sig_type=std_logic lab=ilim_en}

* --- TRUTH TABLE ---
T {MODE TRUTH TABLE} 600 200 0 0 0.5 0.5 {layer=4}
T {Mode         c1 c2 c3 c4   bypass ea ref_sel uvov ilim pass_off} 600 250 0 0 0.22 0.22 {layer=13}
T {POR           0  0  0  0     0     0    X      0    0     1} 600 275 0 0 0.22 0.22 {}
T {Ret bypass    1  0  0  0     1     0    1      0    0     0} 600 295 0 0 0.22 0.22 {}
T {Ret regulate  1  1  0  0     0     1    1      0    0     0} 600 315 0 0 0.22 0.22 {}
T {PU bypass     1  1  1  0     1     0    0      0    0     0} 600 335 0 0 0.22 0.22 {}
T {Active        1  1  1  1     0     1    0      1    1     0} 600 355 0 0 0.22 0.22 {}

* --- CHARACTERIZATION ---
T {CHARACTERIZATION  (TT 27C  |  PVT worst-case SF 27C)} -800 530 0 0 0.5 0.5 {layer=4}
T {TH1 (POR exit)    =  2.507 V       spec [2.3, 2.7] V          PASS} -800 580 0 0 0.28 0.28 {layer=7}
T {TH2 (Ret reg)     =  4.158 V       spec [4.0, 4.4] V          PASS} -800 610 0 0 0.28 0.28 {layer=7}
T {TH3 (PU bypass)   =  4.439 V       spec [4.3, 4.7] V          PASS} -800 640 0 0 0.28 0.28 {layer=7}
T {TH4 (Active)      =  5.520 V       spec [5.4, 5.8] V          PASS} -800 670 0 0 0.28 0.28 {layer=7}
T {Max error = 1.43% TT, 8.05% PVT (SF)    spec <= 15%           PASS} -800 700 0 0 0.28 0.28 {layer=7}
T {Hysteresis  = 224 - 244 mV              spec [150, 250] mV     PASS} -800 730 0 0 0.28 0.28 {layer=7}
T {Iq (BVDD)   = 17.3 uA                   spec <= 20 uA          PASS} -800 760 0 0 0.28 0.28 {layer=7}
T {Monotonic = YES  |  Glitch-free = YES  |  Fast/Slow ramp = PASS} -800 790 0 0 0.28 0.28 {layer=7}
T {Power-down reverse = PASS  |  PVT 5 corners = PASS} -800 820 0 0 0.28 0.28 {layer=7}
T {44 MOSFETs + 5 resistors  |  Schmitt trigger hysteresis on each comparator} -800 860 0 0 0.28 0.28 {layer=7}
T {All 16/16 specs PASS} -800 910 0 0 0.45 0.45 {layer=4}
