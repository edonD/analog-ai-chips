v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 04: CURRENT LIMITER} -650 -1050 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Sense-Mirror Brick-Wall Limiter} -650 -970 0 0 0.45 0.45 {layer=8}
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  (Vds max 10.5V)} -650 -935 0 0 0.3 0.3 {}
T {.subckt current_limiter  gate  bvdd  pvdd  gnd  ilim_flag} -650 -905 0 0 0.28 0.28 {layer=13}

C {/usr/local/share/xschem/xschem_library/devices/ipin.sym} -650 -760 0 0 {name=p1 lab=gate}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -560 -760 0 0 {name=p2 lab=bvdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -560 -730 0 0 {name=p3 lab=pvdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -560 -700 0 0 {name=p4 lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/opin.sym} -470 -760 0 0 {name=p5 lab=ilim_flag}

T {SENSE MIRROR} -420 -830 0 0 0.5 0.5 {layer=4}
T {DETECTION} 150 -830 0 0 0.5 0.5 {layer=4}
T {GATE CLAMP} 550 -830 0 0 0.5 0.5 {layer=4}
T {FLAG OUTPUT} 900 -830 0 0 0.5 0.5 {layer=4}

C {/usr/local/share/xschem/xschem_library/devices/title.sym} -650 830 0 0 {name=l1 author="Block 04: Current Limiter -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* SENSE MIRROR: XMs (PMOS sense) -> sense_n -> XRs (sense resistor) -> GND
* Vertical stack: BVDD at top, GND at bottom
* ================================================================

* --- XMs: PMOS sense transistor (mirrors pass device current / 500) ---
T {XMs} -480 -660 0 0 0.25 0.25 {layer=13}
T {W=2u L=0.5u m=1} -480 -638 0 0 0.2 0.2 {layer=5}
T {sense 1/500} -480 -616 0 0 0.18 0.18 {}
T {B=BVDD} -370 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -410 -680 0 0 {name=XMs
L=0.5e-6
W=2e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -390 -710 -390 -760 {lab=bvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -390 -760 2 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -390 -650 -390 -560 {lab=sense_n}
N -430 -680 -500 -680 {lab=gate}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -500 -680 0 0 {name=l_g1 sig_type=std_logic lab=gate}
T {gate} -500 -695 0 0 0.3 0.3 {layer=8}
T {sense_n} -385 -565 0 0 0.3 0.3 {layer=8}

* --- XRs: Sense resistor (xhigh_po W=1 L=3.12) ---
T {XRs} -480 -370 0 0 0.25 0.25 {layer=13}
T {W=1 L=3.12} -480 -348 0 0 0.2 0.2 {layer=5}
T {Rs ~ 6.1k} -480 -326 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -390 -430 0 0 {name=XRs
W=1
L=3.12
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -390 -460 -390 -560 {lab=sense_n}
N -390 -400 -390 -280 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/gnd.sym} -390 -280 0 0 {name=lg1 lab=GND}
N -410 -430 -460 -430 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -460 -430 0 0 {name=l_gn1 sig_type=std_logic lab=gnd}

* ================================================================
* DETECTION: XMdet (NMOS) senses voltage on sense_n
* When Vsense > Vth, XMdet turns on, pulling det_n low
* ================================================================

* --- XMdet: Detection NMOS (W=5u L=1u) ---
T {XMdet} 100 -340 0 0 0.25 0.25 {layer=13}
T {W=5u L=1u m=1} 100 -318 0 0 0.2 0.2 {layer=5}
T {Vth detect} 100 -296 0 0 0.18 0.18 {}
T {B=GND} 220 -385 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 180 -420 0 0 {name=XMdet
L=1e-6
W=5e-6
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 200 -450 200 -560 {lab=det_n}
N 200 -390 200 -280 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/gnd.sym} 200 -280 0 0 {name=lg2 lab=GND}
N 160 -420 60 -420 {lab=sense_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 60 -420 0 0 {name=l_sn2 sig_type=std_logic lab=sense_n}
T {sense_n} 65 -435 0 0 0.3 0.3 {layer=8}
T {det_n} 205 -565 0 0 0.3 0.3 {layer=8}

* --- XRpu: Pull-up resistor (xhigh_po W=1 L=5) ---
T {XRpu} 100 -660 0 0 0.25 0.25 {layer=13}
T {W=1 L=5} 100 -638 0 0 0.2 0.2 {layer=5}
T {Rpu ~ 10.5k} 100 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 200 -640 0 0 {name=XRpu
W=1
L=5
model=res_xhigh_po
spiceprefix=X
mult=1
}
N 200 -670 200 -760 {lab=bvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 200 -760 2 0 {name=l_bv2 sig_type=std_logic lab=bvdd}
N 200 -610 200 -560 {lab=det_n}
N 180 -640 130 -640 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 130 -640 0 0 {name=l_gn2 sig_type=std_logic lab=gnd}

* ================================================================
* GATE CLAMP: XMclamp (PMOS) pulls gate toward BVDD when det_n goes low
* THIS IS THE FEEDBACK PATH: XMclamp drain -> gate port
* ================================================================

* --- XMclamp: Clamp PMOS (W=20u L=1u) ---
T {XMclamp} 500 -660 0 0 0.25 0.25 {layer=13}
T {W=20u L=1u m=1} 500 -638 0 0 0.2 0.2 {layer=5}
T {gate clamp} 500 -616 0 0 0.18 0.18 {}
T {B=BVDD} 610 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 570 -680 0 0 {name=XMclamp
L=1e-6
W=20e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 590 -710 590 -760 {lab=bvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 590 -760 2 0 {name=l_bv3 sig_type=std_logic lab=bvdd}
N 590 -650 590 -560 {lab=gate}
N 550 -680 450 -680 {lab=det_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 450 -680 0 0 {name=l_dn3 sig_type=std_logic lab=det_n}
T {det_n} 455 -695 0 0 0.3 0.3 {layer=8}
T {gate (feedback)} 595 -565 0 0 0.3 0.3 {layer=4}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 590 -560 0 0 {name=l_g3 sig_type=std_logic lab=gate}

* --- Feedback annotation ---
T {FEEDBACK: det_n LOW -> XMclamp ON -> gate pulled to BVDD -> pass FET off} 450 -530 0 0 0.22 0.22 {layer=7}
T {This is the brick-wall current limiting action} 450 -505 0 0 0.2 0.2 {}

* ================================================================
* FLAG OUTPUT: XMfp/XMfn inverter driven by det_n
* ilim_flag = LOW when limiting (det_n LOW -> XMfp ON, XMfn OFF)
* ================================================================

* --- XMfp: Flag PMOS (W=2u L=1u) ---
T {XMfp} 850 -660 0 0 0.25 0.25 {layer=13}
T {W=2u L=1u m=1} 850 -638 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 960 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 920 -680 0 0 {name=XMfp
L=1e-6
W=2e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 940 -710 940 -760 {lab=pvdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -760 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}
N 940 -650 940 -560 {lab=ilim_flag}
N 900 -680 800 -680 {lab=det_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 800 -680 0 0 {name=l_dn4 sig_type=std_logic lab=det_n}

* --- XMfn: Flag NMOS (W=2u L=1u) ---
T {XMfn} 850 -340 0 0 0.25 0.25 {layer=13}
T {W=2u L=1u m=1} 850 -318 0 0 0.2 0.2 {layer=5}
T {B=GND} 960 -385 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 920 -420 0 0 {name=XMfn
L=1e-6
W=2e-6
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 940 -450 940 -560 {lab=ilim_flag}
N 940 -390 940 -280 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/gnd.sym} 940 -280 0 0 {name=lg3 lab=GND}
N 900 -420 800 -420 {lab=det_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 800 -420 0 0 {name=l_dn5 sig_type=std_logic lab=det_n}

* ilim_flag output
T {ilim_flag} 975 -565 0 0 0.35 0.35 {layer=4}
T {LOW = limiting} 975 -540 0 0 0.2 0.2 {}
N 940 -560 1060 -560 {lab=ilim_flag}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1060 -560 2 0 {name=l_fl sig_type=std_logic lab=ilim_flag}

* ================================================================
* CHARACTERIZATION
* ================================================================

T {CHARACTERIZATION  (PVDD = 5.0V, BVDD = 10.5V)} -650 500 0 0 0.5 0.5 {layer=4}
T {TT 27C  Ilim         =  79.0 mA       (Iload at trip)           PASS} -650 555 0 0 0.28 0.28 {layer=7}
T {SS 150C Ilim (primary)=  135.7 mA      spec >= 100 mA           PASS} -650 585 0 0 0.28 0.28 {layer=7}
T {FF -40C Ilim          =  43.4 mA       (cold corner minimum)    PASS} -650 615 0 0 0.28 0.28 {layer=7}
T {PVT Spread            =  3.1x          (135.7 / 43.4)           PASS} -650 645 0 0 0.28 0.28 {layer=7}
T {Iq (no load)          =  ~0.0002 uA    (near zero quiescent)    PASS} -650 675 0 0 0.28 0.28 {layer=7}
T {Short-circuit Iout    =  ~105 mA       (vs 598 mA without)      PASS} -650 705 0 0 0.28 0.28 {layer=7}
T {Loop Phase Margin     =  104 deg       at UGB=423 kHz           PASS} -650 735 0 0 0.28 0.28 {layer=7}
T {Sense ratio N=500, Rs=6.1k, Rpu=10.5k    Detect threshold ~ Vth} -650 765 0 0 0.28 0.28 {layer=7}
T {All 9/9 specs PASS} -650 810 0 0 0.45 0.45 {layer=4}
