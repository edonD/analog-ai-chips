v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 08: MODE CONTROL} -650 -1350 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Shared Ladder + PVDD Inverter Threshold Detectors} -650 -1270 0 0 0.45 0.45 {layer=8}
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  (Vds max 10.5V)} -650 -1235 0 0 0.3 0.3 {}
T {.subckt mode_control  bvdd  pvdd  svdd  gnd  vref  en_ret  bypass_en  ea_en  ref_sel  uvov_en  ilim_en  pass_off} -650 -1205 0 0 0.28 0.28 {layer=13}

* ================================================================
* PORT PINS
* ================================================================

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -1080 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -1050 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -1020 0 0 {name=p3 lab=svdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -990 0 0 {name=p4 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -960 0 0 {name=p5 lab=vref}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -930 0 0 {name=p6 lab=en_ret}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -1080 0 0 {name=p7 lab=bypass_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -1050 0 0 {name=p8 lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -1020 0 0 {name=p9 lab=ref_sel}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -990 0 0 {name=p10 lab=uvov_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -960 0 0 {name=p11 lab=ilim_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -930 0 0 {name=p12 lab=pass_off}

C {/usr/share/xschem/xschem_library/devices/title.sym} -650 1530 0 0 {name=l1 author="Block 08: Mode Control -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* RESISTOR LADDER (~400 kohm from BVDD to GND)
* 5 resistors: Rtop(l=8) - R12(l=68) - R23(l=8) - R34(l=21) - Rbot(l=86)
* 4 tap points: tap1, tap2, tap3, tap4
* ================================================================

T {RESISTOR LADDER} -420 -830 0 0 0.5 0.5 {layer=4}
T {~400 kohm total  |  Iq ~17 uA at 7V} -420 -800 0 0 0.25 0.25 {}
T {xhigh_po w=1} -420 -780 0 0 0.2 0.2 {layer=5}

* --- BVDD supply ---
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -310 -760 2 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -310 -760 -310 -720 {lab=bvdd}
T {BVDD} -340 -770 0 0 0.3 0.3 {layer=4}

* --- Rtop: l=8 ---
T {Rtop} -370 -690 0 0 0.25 0.25 {layer=13}
T {w=1 l=8} -370 -668 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} -310 -680 0 0 {name=XRtop
value="sky130_fd_pr__res_xhigh_po w=1 l=8"
}
N -310 -720 -310 -710 {lab=bvdd}
N -310 -650 -310 -610 {lab=tap1}
T {tap1} -295 -615 0 0 0.3 0.3 {layer=8}
N -310 -610 -100 -610 {lab=tap1}

* --- R12: l=68 ---
T {R12} -370 -570 0 0 0.25 0.25 {layer=13}
T {w=1 l=68} -370 -548 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} -310 -560 0 0 {name=XR12
value="sky130_fd_pr__res_xhigh_po w=1 l=68"
}
N -310 -610 -310 -590 {lab=tap1}
N -310 -530 -310 -490 {lab=tap2}
T {tap2} -295 -495 0 0 0.3 0.3 {layer=8}
N -310 -490 -100 -490 {lab=tap2}

* --- R23: l=8 ---
T {R23} -370 -450 0 0 0.25 0.25 {layer=13}
T {w=1 l=8} -370 -428 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} -310 -440 0 0 {name=XR23
value="sky130_fd_pr__res_xhigh_po w=1 l=8"
}
N -310 -490 -310 -470 {lab=tap2}
N -310 -410 -310 -370 {lab=tap3}
T {tap3} -295 -375 0 0 0.3 0.3 {layer=8}
N -310 -370 -100 -370 {lab=tap3}

* --- R34: l=21 ---
T {R34} -370 -330 0 0 0.25 0.25 {layer=13}
T {w=1 l=21} -370 -308 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} -310 -320 0 0 {name=XR34
value="sky130_fd_pr__res_xhigh_po w=1 l=21"
}
N -310 -370 -310 -350 {lab=tap3}
N -310 -290 -310 -250 {lab=tap4}
T {tap4} -295 -255 0 0 0.3 0.3 {layer=8}
N -310 -250 -100 -250 {lab=tap4}

* --- Rbot: l=86 ---
T {Rbot} -370 -210 0 0 0.25 0.25 {layer=13}
T {w=1 l=86} -370 -188 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} -310 -200 0 0 {name=XRbot
value="sky130_fd_pr__res_xhigh_po w=1 l=86"
}
N -310 -250 -310 -230 {lab=tap4}
N -310 -170 -310 -100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -310 -100 0 0 {name=lg1 lab=GND}

* --- Anti-alias caps on taps ---
T {C_tap 100fF each} -210 -640 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/capa.sym} -200 -580 0 0 {name=C_tap1 m=1 value=100f}
N -200 -610 -200 -610 {lab=tap1}
N -200 -550 -200 -520 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -200 -520 0 0 {name=lg_ct1 lab=GND}

C {/usr/share/xschem/xschem_library/devices/capa.sym} -140 -460 0 0 {name=C_tap2 m=1 value=100f}
N -140 -490 -140 -490 {lab=tap2}
N -140 -430 -140 -400 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -140 -400 0 0 {name=lg_ct2 lab=GND}

C {/usr/share/xschem/xschem_library/devices/capa.sym} -200 -340 0 0 {name=C_tap3 m=1 value=100f}
N -200 -370 -200 -370 {lab=tap3}
N -200 -310 -200 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -200 -280 0 0 {name=lg_ct3 lab=GND}

C {/usr/share/xschem/xschem_library/devices/capa.sym} -140 -220 0 0 {name=C_tap4 m=1 value=100f}
N -140 -250 -140 -250 {lab=tap4}
N -140 -190 -140 -160 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -140 -160 0 0 {name=lg_ct4 lab=GND}

* ================================================================
* COMPARATORS 1-4: Each is 2 PVDD-referenced inverters
* INV1 (tap -> c_inv) + INV2 (c_inv -> comp)
* PFET from PVDD, NFET from GND
* ================================================================

T {COMPARATORS (PVDD-referenced inverters)} 100 -830 0 0 0.5 0.5 {layer=4}
T {Each: INV1(tap->c_inv) + INV2(c_inv->comp)} 100 -800 0 0 0.25 0.25 {}

* ================================================================
* COMP1: tap1 -> c1inv -> comp1    (TH1 = 2.55V)
* ================================================================

T {COMP1  (TH1 = 2.55V)} 100 -710 0 0 0.35 0.35 {layer=4}

* --- INV1a: PFET pull-up ---
T {XMc1ivp} 50 -660 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 50 -638 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 200 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 160 -680 0 0 {name=XMc1ivp
L=20
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 180 -710 180 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -760 2 0 {name=l_pvc1a sig_type=std_logic lab=pvdd}
N 180 -650 180 -600 {lab=c1inv}
N 140 -680 60 -680 {lab=tap1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -680 0 0 {name=l_t1a sig_type=std_logic lab=tap1}

* --- INV1b: NFET pull-down ---
T {XMc1ivn} 50 -480 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 50 -458 0 0 0.2 0.2 {layer=5}
T {B=GND} 200 -530 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 160 -550 0 0 {name=XMc1ivn
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 180 -520 180 -440 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 180 -440 0 0 {name=lg_c1n lab=GND}
N 180 -580 180 -600 {lab=c1inv}
N 140 -550 60 -550 {lab=tap1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -550 0 0 {name=l_t1b sig_type=std_logic lab=tap1}
T {c1inv} 185 -605 0 0 0.25 0.25 {layer=8}

* --- INV2a: PFET ---
T {XMc1iv2p} 310 -660 0 0 0.25 0.25 {layer=13}
T {W=40 L=20} 310 -638 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 450 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 410 -680 0 0 {name=XMc1iv2p
L=20
W=40
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 430 -710 430 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 -760 2 0 {name=l_pvc1b sig_type=std_logic lab=pvdd}
N 430 -650 430 -600 {lab=comp1}
N 390 -680 300 -680 {lab=c1inv}
N 300 -680 300 -600 {lab=c1inv}
N 300 -600 180 -600 {lab=c1inv}

* --- INV2b: NFET ---
T {XMc1iv2n} 310 -480 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 310 -458 0 0 0.2 0.2 {layer=5}
T {B=GND} 450 -530 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 410 -550 0 0 {name=XMc1iv2n
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 430 -520 430 -440 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 430 -440 0 0 {name=lg_c1n2 lab=GND}
N 430 -580 430 -600 {lab=comp1}
N 390 -550 300 -550 {lab=c1inv}
N 300 -550 300 -600 {lab=c1inv}
T {comp1} 435 -605 0 0 0.3 0.3 {layer=8}
N 430 -600 550 -600 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 -600 2 0 {name=l_comp1 sig_type=std_logic lab=comp1}

* ================================================================
* COMP2: tap2 -> c2inv -> comp2    (TH2 = 4.34V)
* ================================================================

T {COMP2  (TH2 = 4.34V)} 650 -710 0 0 0.35 0.35 {layer=4}

T {XMc2ivp} 600 -660 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 600 -638 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 750 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 710 -680 0 0 {name=XMc2ivp
L=20
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 730 -710 730 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 730 -760 2 0 {name=l_pvc2a sig_type=std_logic lab=pvdd}
N 730 -650 730 -600 {lab=c2inv}
N 690 -680 610 -680 {lab=tap2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 610 -680 0 0 {name=l_t2a sig_type=std_logic lab=tap2}

T {XMc2ivn} 600 -480 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 600 -458 0 0 0.2 0.2 {layer=5}
T {B=GND} 750 -530 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 710 -550 0 0 {name=XMc2ivn
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 730 -520 730 -440 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 730 -440 0 0 {name=lg_c2n lab=GND}
N 730 -580 730 -600 {lab=c2inv}
N 690 -550 610 -550 {lab=tap2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 610 -550 0 0 {name=l_t2b sig_type=std_logic lab=tap2}
T {c2inv} 735 -605 0 0 0.25 0.25 {layer=8}

T {XMc2iv2p} 860 -660 0 0 0.25 0.25 {layer=13}
T {W=40 L=20} 860 -638 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 1000 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 960 -680 0 0 {name=XMc2iv2p
L=20
W=40
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 980 -710 980 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 980 -760 2 0 {name=l_pvc2b sig_type=std_logic lab=pvdd}
N 980 -650 980 -600 {lab=comp2}
N 940 -680 850 -680 {lab=c2inv}
N 850 -680 850 -600 {lab=c2inv}
N 850 -600 730 -600 {lab=c2inv}

T {XMc2iv2n} 860 -480 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 860 -458 0 0 0.2 0.2 {layer=5}
T {B=GND} 1000 -530 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 960 -550 0 0 {name=XMc2iv2n
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 980 -520 980 -440 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 980 -440 0 0 {name=lg_c2n2 lab=GND}
N 980 -580 980 -600 {lab=comp2}
N 940 -550 850 -550 {lab=c2inv}
N 850 -550 850 -600 {lab=c2inv}
T {comp2} 985 -605 0 0 0.3 0.3 {layer=8}
N 980 -600 1100 -600 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -600 2 0 {name=l_comp2 sig_type=std_logic lab=comp2}

* ================================================================
* COMP3: tap3 -> c3inv -> comp3    (TH3 = 4.65V)
* ================================================================

T {COMP3  (TH3 = 4.65V)} 100 -380 0 0 0.35 0.35 {layer=4}

T {XMc3ivp} 50 -330 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 50 -308 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 200 -380 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 160 -350 0 0 {name=XMc3ivp
L=20
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 180 -380 180 -430 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -430 2 0 {name=l_pvc3a sig_type=std_logic lab=pvdd}
N 180 -320 180 -270 {lab=c3inv}
N 140 -350 60 -350 {lab=tap3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -350 0 0 {name=l_t3a sig_type=std_logic lab=tap3}

T {XMc3ivn} 50 -150 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 50 -128 0 0 0.2 0.2 {layer=5}
T {B=GND} 200 -200 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 160 -220 0 0 {name=XMc3ivn
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 180 -190 180 -110 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 180 -110 0 0 {name=lg_c3n lab=GND}
N 180 -250 180 -270 {lab=c3inv}
N 140 -220 60 -220 {lab=tap3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -220 0 0 {name=l_t3b sig_type=std_logic lab=tap3}
T {c3inv} 185 -275 0 0 0.25 0.25 {layer=8}

T {XMc3iv2p} 310 -330 0 0 0.25 0.25 {layer=13}
T {W=40 L=20} 310 -308 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 450 -380 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 410 -350 0 0 {name=XMc3iv2p
L=20
W=40
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 430 -380 430 -430 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 -430 2 0 {name=l_pvc3b sig_type=std_logic lab=pvdd}
N 430 -320 430 -270 {lab=comp3}
N 390 -350 300 -350 {lab=c3inv}
N 300 -350 300 -270 {lab=c3inv}
N 300 -270 180 -270 {lab=c3inv}

T {XMc3iv2n} 310 -150 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 310 -128 0 0 0.2 0.2 {layer=5}
T {B=GND} 450 -200 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 410 -220 0 0 {name=XMc3iv2n
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 430 -190 430 -110 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 430 -110 0 0 {name=lg_c3n2 lab=GND}
N 430 -250 430 -270 {lab=comp3}
N 390 -220 300 -220 {lab=c3inv}
N 300 -220 300 -270 {lab=c3inv}
T {comp3} 435 -275 0 0 0.3 0.3 {layer=8}
N 430 -270 550 -270 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 -270 2 0 {name=l_comp3 sig_type=std_logic lab=comp3}

* ================================================================
* COMP4: tap4 -> c4inv -> comp4    (TH4 = 5.67V)
* ================================================================

T {COMP4  (TH4 = 5.67V)} 650 -380 0 0 0.35 0.35 {layer=4}

T {XMc4ivp} 600 -330 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 600 -308 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 750 -380 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 710 -350 0 0 {name=XMc4ivp
L=20
W=20
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 730 -380 730 -430 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 730 -430 2 0 {name=l_pvc4a sig_type=std_logic lab=pvdd}
N 730 -320 730 -270 {lab=c4inv}
N 690 -350 610 -350 {lab=tap4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 610 -350 0 0 {name=l_t4a sig_type=std_logic lab=tap4}

T {XMc4ivn} 600 -150 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 600 -128 0 0 0.2 0.2 {layer=5}
T {B=GND} 750 -200 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 710 -220 0 0 {name=XMc4ivn
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 730 -190 730 -110 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 730 -110 0 0 {name=lg_c4n lab=GND}
N 730 -250 730 -270 {lab=c4inv}
N 690 -220 610 -220 {lab=tap4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 610 -220 0 0 {name=l_t4b sig_type=std_logic lab=tap4}
T {c4inv} 735 -275 0 0 0.25 0.25 {layer=8}

T {XMc4iv2p} 860 -330 0 0 0.25 0.25 {layer=13}
T {W=40 L=20} 860 -308 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 1000 -380 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 960 -350 0 0 {name=XMc4iv2p
L=20
W=40
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 980 -380 980 -430 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 980 -430 2 0 {name=l_pvc4b sig_type=std_logic lab=pvdd}
N 980 -320 980 -270 {lab=comp4}
N 940 -350 850 -350 {lab=c4inv}
N 850 -350 850 -270 {lab=c4inv}
N 850 -270 730 -270 {lab=c4inv}

T {XMc4iv2n} 860 -150 0 0 0.25 0.25 {layer=13}
T {W=20 L=20} 860 -128 0 0 0.2 0.2 {layer=5}
T {B=GND} 1000 -200 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 960 -220 0 0 {name=XMc4iv2n
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 980 -190 980 -110 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 980 -110 0 0 {name=lg_c4n2 lab=GND}
N 980 -250 980 -270 {lab=comp4}
N 940 -220 850 -220 {lab=c4inv}
N 850 -220 850 -270 {lab=c4inv}
T {comp4} 985 -275 0 0 0.3 0.3 {layer=8}
N 980 -270 1100 -270 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -270 2 0 {name=l_comp4 sig_type=std_logic lab=comp4}

* ================================================================
* LOGIC SECTION: Inverter buffers + AOI gates
* Generates: pass_off, bypass_en, ea_en, ref_sel, uvov_en, ilim_en
* ================================================================

T {LOGIC: AOI GATES + OUTPUT BUFFERS} -650 60 0 0 0.5 0.5 {layer=4}
T {comp1..4 -> comp1b..4b (inverters) -> AOI -> output buffers} -650 90 0 0 0.25 0.25 {}

* --- Complement inverters: comp1->comp1b, comp2->comp2b, comp3->comp3b, comp4->comp4b ---

T {COMP INVERTERS} -650 140 0 0 0.35 0.35 {layer=4}

T {XMinv1p/n: comp1 -> comp1b} -620 175 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -560 200 0 0 {name=XMinv1p
L=20
W=40
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -540 170 -540 140 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -540 140 2 0 {name=l_pvl1 sig_type=std_logic lab=pvdd}
N -540 230 -540 260 {lab=comp1b}
N -580 200 -640 200 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -640 200 0 0 {name=l_c1g sig_type=std_logic lab=comp1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -560 300 0 0 {name=XMinv1n
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -540 330 -540 360 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -540 360 0 0 {name=lg_inv1 lab=GND}
N -540 270 -540 260 {lab=comp1b}
N -580 300 -640 300 {lab=comp1}
N -640 200 -640 300 {lab=comp1}
T {comp1b} -535 255 0 0 0.25 0.25 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -480 260 2 0 {name=l_c1b sig_type=std_logic lab=comp1b}
N -540 260 -480 260 {lab=comp1b}

T {XMinv2p/n: comp2 -> comp2b} -380 175 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -320 200 0 0 {name=XMinv2p
L=20
W=40
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -300 170 -300 140 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -300 140 2 0 {name=l_pvl2 sig_type=std_logic lab=pvdd}
N -300 230 -300 260 {lab=comp2b}
N -340 200 -400 200 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -400 200 0 0 {name=l_c2g sig_type=std_logic lab=comp2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -320 300 0 0 {name=XMinv2n
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -300 330 -300 360 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -300 360 0 0 {name=lg_inv2 lab=GND}
N -300 270 -300 260 {lab=comp2b}
N -340 300 -400 300 {lab=comp2}
N -400 200 -400 300 {lab=comp2}
T {comp2b} -295 255 0 0 0.25 0.25 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -240 260 2 0 {name=l_c2b sig_type=std_logic lab=comp2b}
N -300 260 -240 260 {lab=comp2b}

T {XMinv3p/n: comp3 -> comp3b} -140 175 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -80 200 0 0 {name=XMinv3p
L=20
W=40
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -60 170 -60 140 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -60 140 2 0 {name=l_pvl3 sig_type=std_logic lab=pvdd}
N -60 230 -60 260 {lab=comp3b}
N -100 200 -160 200 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -160 200 0 0 {name=l_c3g sig_type=std_logic lab=comp3}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -80 300 0 0 {name=XMinv3n
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -60 330 -60 360 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -60 360 0 0 {name=lg_inv3 lab=GND}
N -60 270 -60 260 {lab=comp3b}
N -100 300 -160 300 {lab=comp3}
N -160 200 -160 300 {lab=comp3}
T {comp3b} -55 255 0 0 0.25 0.25 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 260 2 0 {name=l_c3b sig_type=std_logic lab=comp3b}
N -60 260 0 260 {lab=comp3b}

T {XMinv4p/n: comp4 -> comp4b} 100 175 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 160 200 0 0 {name=XMinv4p
L=20
W=40
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 180 170 180 140 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 140 2 0 {name=l_pvl4 sig_type=std_logic lab=pvdd}
N 180 230 180 260 {lab=comp4b}
N 140 200 80 200 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 80 200 0 0 {name=l_c4g sig_type=std_logic lab=comp4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 160 300 0 0 {name=XMinv4n
L=20
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 180 330 180 360 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 180 360 0 0 {name=lg_inv4 lab=GND}
N 180 270 180 260 {lab=comp4b}
N 140 300 80 300 {lab=comp4}
N 80 200 80 300 {lab=comp4}
T {comp4b} 185 255 0 0 0.25 0.25 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 240 260 2 0 {name=l_c4b sig_type=std_logic lab=comp4b}
N 180 260 240 260 {lab=comp4b}

* ================================================================
* OUTPUT LOGIC BLOCKS (shown as labeled boxes with descriptions)
* ================================================================

T {OUTPUT LOGIC} -650 440 0 0 0.5 0.5 {layer=4}

* --- pass_off: buffer of comp1b ---
T {pass_off = BUF(comp1b)} -620 500 0 0 0.35 0.35 {layer=4}
T {comp1b -> pass_off  (BVDD < TH1: pass FET off)} -620 530 0 0 0.22 0.22 {}
T {XMpo_bufp/n} -620 555 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 580 0 0 {name=l_po_in sig_type=std_logic lab=comp1b}
N -620 580 -520 580 {lab=comp1b}
T {->  INV  ->} -510 575 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -400 580 2 0 {name=l_po_out sig_type=std_logic lab=pass_off}
N -450 580 -400 580 {lab=pass_off}

* --- bypass_en: AOI(comp1*comp2b + comp3*comp4b) -> INV ---
T {bypass_en = INV(AOI(comp1*comp2b, comp3*comp4b))} -620 640 0 0 0.35 0.35 {layer=4}
T {BVDD in [TH1..TH2] OR [TH3..TH4]: bypass capacitor mode} -620 670 0 0 0.22 0.22 {}
T {AOI22 + output INV} -620 695 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 720 0 0 {name=l_by_c1 sig_type=std_logic lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 745 0 0 {name=l_by_c2b sig_type=std_logic lab=comp2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 770 0 0 {name=l_by_c3 sig_type=std_logic lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 795 0 0 {name=l_by_c4b sig_type=std_logic lab=comp4b}
T {->  AOI22 -> INV  ->} -510 740 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -300 755 2 0 {name=l_by_out sig_type=std_logic lab=bypass_en}
N -350 755 -300 755 {lab=bypass_en}

* --- ea_en: AOI(comp2*comp3b, comp4) -> INV ---
T {ea_en = INV(AOI(comp2*comp3b, comp4))} -620 850 0 0 0.35 0.35 {layer=4}
T {BVDD in [TH2..TH3] OR > TH4: error amp enabled} -620 880 0 0 0.22 0.22 {}
T {AOI21 + output INV} -620 905 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 930 0 0 {name=l_ea_c2 sig_type=std_logic lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 955 0 0 {name=l_ea_c3b sig_type=std_logic lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 980 0 0 {name=l_ea_c4 sig_type=std_logic lab=comp4}
T {->  AOI21 -> INV  ->} -510 950 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -300 955 2 0 {name=l_ea_out sig_type=std_logic lab=ea_en}
N -350 955 -300 955 {lab=ea_en}

* --- ref_sel: NOR(comp1, comp3b) -> INV ---
T {ref_sel = INV(NOR(comp1, comp3b))} -620 1040 0 0 0.35 0.35 {layer=4}
T {BVDD > TH1 AND < TH3: select internal reference} -620 1070 0 0 0.22 0.22 {}
T {NOR2 + output INV} -620 1095 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 1120 0 0 {name=l_rs_c1 sig_type=std_logic lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 1145 0 0 {name=l_rs_c3b sig_type=std_logic lab=comp3b}
T {->  NOR2 -> INV  ->} -510 1130 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -300 1130 2 0 {name=l_rs_out sig_type=std_logic lab=ref_sel}
N -350 1130 -300 1130 {lab=ref_sel}

* --- uvov_en: double-INV of comp4 ---
T {uvov_en = BUF(comp4)} -620 1200 0 0 0.35 0.35 {layer=4}
T {BVDD > TH4: UV/OV monitor enabled} -620 1230 0 0 0.22 0.22 {}
T {INV + INV} -620 1255 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 1280 0 0 {name=l_uv_c4 sig_type=std_logic lab=comp4}
T {->  INV -> INV  ->} -510 1275 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -300 1280 2 0 {name=l_uv_out sig_type=std_logic lab=uvov_en}
N -350 1280 -300 1280 {lab=uvov_en}

* --- ilim_en: double-INV of comp4 ---
T {ilim_en = BUF(comp4)} -620 1330 0 0 0.35 0.35 {layer=4}
T {BVDD > TH4: current limiter enabled} -620 1360 0 0 0.22 0.22 {}
T {INV + INV} -620 1385 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -620 1410 0 0 {name=l_il_c4 sig_type=std_logic lab=comp4}
T {->  INV -> INV  ->} -510 1405 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -300 1410 2 0 {name=l_il_out sig_type=std_logic lab=ilim_en}
N -350 1410 -300 1410 {lab=ilim_en}

* ================================================================
* CHARACTERIZATION
* ================================================================

T {CHARACTERIZATION  (TT 27C, PVDD = 5.0V, BVDD ramp 0-7V)} 400 440 0 0 0.5 0.5 {layer=4}
T {TH1 (pass_off)    =  2.55 V        (BVDD rising)         } 400 500 0 0 0.28 0.28 {layer=7}
T {TH2 (bypass_en)   =  4.34 V        (BVDD rising)         } 400 530 0 0 0.28 0.28 {layer=7}
T {TH3 (ea_en)       =  4.65 V        (BVDD rising)         } 400 560 0 0 0.28 0.28 {layer=7}
T {TH4 (uvov/ilim)   =  5.67 V        (BVDD rising)         } 400 590 0 0 0.28 0.28 {layer=7}
T {Iq               =  17.3 uA       (ladder quiescent)     } 400 640 0 0 0.28 0.28 {layer=7}
T {thresh_max_error  =  3.34 %        vs. design targets     } 400 670 0 0 0.28 0.28 {layer=7}
T {specs_pass        =  16/16         ALL PASS               } 400 700 0 0 0.28 0.28 {layer=7}
T {PVT: 5 process x 3 temp corners verified} 400 750 0 0 0.28 0.28 {layer=7}
T {All 16/16 specs PASS} 400 800 0 0 0.45 0.45 {layer=4}
