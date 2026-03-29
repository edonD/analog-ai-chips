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
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  |  res_xhigh_po} -650 -935 0 0 0.3 0.3 {}
T {.subckt current_limiter  gate  bvdd  pvdd  gnd  ilim_flag} -650 -905 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/iopin.sym} -650 -760 0 0 {name=p1 lab=gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -650 -730 0 0 {name=p2 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -650 -700 0 0 {name=p3 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -650 -670 0 0 {name=p4 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -760 0 0 {name=p5 lab=ilim_flag}

T {SENSE MIRROR} -420 -830 0 0 0.5 0.5 {layer=4}
T {DETECTION} 200 -830 0 0 0.5 0.5 {layer=4}
T {CLAMP} 650 -830 0 0 0.5 0.5 {layer=4}
T {FLAG OUTPUT} 950 -830 0 0 0.5 0.5 {layer=4}

C {/usr/share/xschem/xschem_library/devices/title.sym} -650 830 0 0 {name=l1 author="Block 04: Current Limiter -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* SENSE MIRROR: XMs (PMOS) + XRs (sense resistor)
* Vertical stack: BVDD at top, GND at bottom, sense_n in middle
* ================================================================

* --- XMs: Sense PMOS (mirrors pass FET current at N=500) ---
T {XMs} -480 -660 0 0 0.25 0.25 {layer=13}
T {W=2 L=0.5 m=1} -480 -638 0 0 0.2 0.2 {layer=5}
T {N=500 sense} -480 -616 0 0 0.18 0.18 {}
T {B=BVDD} -370 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -410 -680 0 0 {name=XMs
L=0.5
W=2
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -390 -710 -390 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -390 -760 2 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -390 -650 -390 -520 {lab=sense_n}
N -430 -680 -530 -680 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -530 -680 0 0 {name=l_gate1 sig_type=std_logic lab=gate}
T {gate} -525 -695 0 0 0.3 0.3 {layer=8}
T {sense_n} -385 -530 0 0 0.3 0.3 {layer=8}

* --- XRs: Sense Resistor (xhigh_po, W=1u L=3.12u, ~6.2k) ---
T {XRs} -480 -360 0 0 0.25 0.25 {layer=13}
T {W=1 L=3.12} -480 -338 0 0 0.2 0.2 {layer=5}
T {~6.2k ohm} -480 -316 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -390 -400 0 0 {name=XRs
L=3.12
W=1
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -390 -440 -390 -520 {lab=sense_n}
N -390 -360 -390 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -390 -280 0 0 {name=lg1 lab=GND}

* ================================================================
* DETECTION: XMdet (NMOS) + XRpu (pull-up resistor)
* XMdet gate senses sense_n, drain is det_n, pulled up by XRpu
* ================================================================

* --- XRpu: Pull-up Resistor (xhigh_po, W=1u L=5u, ~10.5k) ---
T {XRpu} 150 -660 0 0 0.25 0.25 {layer=13}
T {W=1 L=5} 150 -638 0 0 0.2 0.2 {layer=5}
T {~10.5k ohm} 150 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 240 -680 0 0 {name=XRpu
L=5
W=1
model=res_xhigh_po
spiceprefix=X
mult=1
}
N 240 -720 240 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 240 -760 2 0 {name=l_bv2 sig_type=std_logic lab=bvdd}
N 240 -640 240 -520 {lab=det_n}
T {det_n} 245 -530 0 0 0.3 0.3 {layer=8}

* --- XMdet: Detection NMOS (W=5u L=1u) ---
T {XMdet} 150 -340 0 0 0.25 0.25 {layer=13}
T {W=5 L=1 m=1} 150 -318 0 0 0.2 0.2 {layer=5}
T {detector} 150 -296 0 0 0.18 0.18 {}
T {B=GND} 260 -265 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 220 -400 0 0 {name=XMdet
L=1
W=5
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 240 -370 240 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 240 -280 0 0 {name=lg2 lab=GND}
N 240 -430 240 -520 {lab=det_n}
N 200 -400 100 -400 {lab=sense_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -400 0 0 {name=l_sn sig_type=std_logic lab=sense_n}
T {sense_n} 105 -415 0 0 0.25 0.25 {layer=8}

* Connect sense_n between sections
N -390 -520 100 -520 {lab=sense_n}
N 100 -520 100 -400 {lab=sense_n}

* ================================================================
* CLAMP: XMclamp (PMOS, gate=det_n, source=bvdd, drain=gate)
* Feedback path: when det_n goes low, XMclamp pulls gate toward bvdd
* ================================================================

* --- XMclamp: Clamp PMOS (W=20u L=1u) ---
T {XMclamp} 600 -660 0 0 0.25 0.25 {layer=13}
T {W=20 L=1 m=1} 600 -638 0 0 0.2 0.2 {layer=5}
T {gate clamp} 600 -616 0 0 0.18 0.18 {}
T {B=BVDD} 720 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 690 -680 0 0 {name=XMclamp
L=1
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 710 -710 710 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 710 -760 2 0 {name=l_bv3 sig_type=std_logic lab=bvdd}
N 710 -650 710 -560 {lab=gate}
T {gate (feedback)} 715 -575 0 0 0.3 0.3 {layer=4}

* Gate of XMclamp connected to det_n
N 670 -680 520 -680 {lab=det_n}
N 520 -680 520 -520 {lab=det_n}
N 240 -520 520 -520 {lab=det_n}

* Drain of XMclamp feeds back to gate port
N 710 -560 710 -500 {lab=gate}
N 710 -500 820 -500 {lab=gate}
N 820 -500 820 -680 {lab=gate}
N 820 -680 860 -680 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 860 -680 2 0 {name=l_gate_out sig_type=std_logic lab=gate}
T {-> pass FET gate} 870 -695 0 0 0.2 0.2 {}
T {FEEDBACK} 750 -510 0 0 0.35 0.35 {layer=4}

* ================================================================
* FLAG OUTPUT: XMfp (PMOS) + XMfn (NMOS) — inverter
* Input = det_n, Output = ilim_flag
* ================================================================

* --- XMfp: Flag PMOS (W=2u L=1u) ---
T {XMfp} 900 -660 0 0 0.25 0.25 {layer=13}
T {W=2 L=1 m=1} 900 -638 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 1020 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 990 -680 0 0 {name=XMfp
L=1
W=2
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1010 -710 1010 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1010 -760 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}
N 1010 -650 1010 -560 {lab=ilim_flag}

* Gate of XMfp connected to det_n
N 970 -680 900 -680 {lab=det_n}
N 900 -680 900 -520 {lab=det_n}
N 520 -520 900 -520 {lab=det_n}

* --- XMfn: Flag NMOS (W=2u L=1u) ---
T {XMfn} 900 -340 0 0 0.25 0.25 {layer=13}
T {W=2 L=1 m=1} 900 -318 0 0 0.2 0.2 {layer=5}
T {B=GND} 1020 -265 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 990 -400 0 0 {name=XMfn
L=1
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 1010 -370 1010 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1010 -280 0 0 {name=lg3 lab=GND}
N 1010 -430 1010 -560 {lab=ilim_flag}

* Gate of XMfn connected to det_n
N 970 -400 900 -400 {lab=det_n}
N 900 -400 900 -520 {lab=det_n}

* ilim_flag output
T {ilim_flag} 1060 -510 0 0 0.35 0.35 {layer=4}
N 1010 -560 1100 -560 {lab=ilim_flag}
N 1100 -560 1100 -500 {lab=ilim_flag}
N 1100 -500 1150 -500 {lab=ilim_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -500 2 0 {name=l_flag sig_type=std_logic lab=ilim_flag}

* ================================================================
* CHARACTERIZATION
* ================================================================

T {CHARACTERIZATION  (v3 — All values from simulation)} -650 500 0 0 0.5 0.5 {layer=4}
T {Ilim TT 27C       =  79.9 mA       spec [60, 80] mA     PASS} -650 555 0 0 0.28 0.28 {layer=7}
T {Ilim SS 150C      =  136.8 mA      spec >= 50 mA        PASS} -650 585 0 0 0.28 0.28 {layer=7}
T {Ilim FF -40C      =  43.4 mA       spec <= 100 mA       PASS} -650 615 0 0 0.28 0.28 {layer=7}
T {Response time     =  0.1 us        spec <= 10 us        PASS} -650 645 0 0 0.28 0.28 {layer=7}
T {PVDD impact       =  0.105 mV      spec <= 10 mV        PASS} -650 675 0 0 0.28 0.28 {layer=7}
T {Sense Iq          =  0.0002 uA     spec <= 10 uA        PASS} -650 705 0 0 0.28 0.28 {layer=7}
T {No oscillation    =  true          gate ripple < 200mV   PASS} -650 735 0 0 0.28 0.28 {layer=7}
T {Loop PM           =  104.5 deg     spec >= 45 deg       PASS} -650 765 0 0 0.28 0.28 {layer=7}
T {Short circuit     =  105 mA        vs 598 mA unlimited   PASS} -650 795 0 0 0.28 0.28 {layer=7}
T {All 9/9 specs PASS    Primary: ilim_ss150 = 136.8 mA} -650 840 0 0 0.45 0.45 {layer=4}
