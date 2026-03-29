v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 08: MODE CONTROL} -600 -1350 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Shared Ladder + Schmitt Trigger Comparators} -600 -1280 0 0 0.45 0.45 {layer=8}
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  |  Resistors: res_xhigh_po} -600 -1245 0 0 0.3 0.3 {}
T {.subckt mode_control bvdd pvdd svdd gnd vref en_ret bypass_en ea_en ref_sel uvov_en ilim_en pass_off} -600 -1215 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/title.sym} -600 1200 0 0 {name=l1 author="Block 08: Mode Control -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* PORT PINS
* ================================================================
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -1080 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -1050 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -1020 0 0 {name=p3 lab=svdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -990 0 0 {name=p4 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -960 0 0 {name=p5 lab=vref}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -930 0 0 {name=p6 lab=en_ret}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -500 -1080 0 0 {name=p7 lab=bypass_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -500 -1050 0 0 {name=p8 lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -500 -1020 0 0 {name=p9 lab=ref_sel}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -500 -990 0 0 {name=p10 lab=uvov_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -500 -960 0 0 {name=p11 lab=ilim_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -500 -930 0 0 {name=p12 lab=pass_off}

* ================================================================
* RESISTOR LADDER (~400k, Iq ~17.5uA at 7V)
* Vertical stack: BVDD at top, GND at bottom
* ================================================================

T {RESISTOR LADDER} -530 -830 0 0 0.5 0.5 {layer=4}
T {~400k total, Iq~17uA} -530 -805 0 0 0.25 0.25 {}

* --- XRtop: bvdd to tap1, l=37 ---
T {XRtop} -530 -740 0 0 0.25 0.25 {layer=13}
T {w=1 l=37} -530 -720 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -470 -710 0 0 {name=XRtop
W=1
L=37
model=res_xhigh_po
spiceprefix=X
mult=1}
N -470 -740 -470 -770 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -470 -770 2 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -470 -680 -470 -640 {lab=tap1}
N -450 -710 -430 -710 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -430 -710 2 0 {name=l_grt sig_type=std_logic lab=gnd}

* --- XR12: tap1 to tap2, l=62 ---
T {XR12} -530 -600 0 0 0.25 0.25 {layer=13}
T {w=1 l=62} -530 -580 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -470 -570 0 0 {name=XR12
W=1
L=62
model=res_xhigh_po
spiceprefix=X
mult=1}
N -470 -600 -470 -640 {lab=tap1}
T {tap1} -460 -645 0 0 0.3 0.3 {layer=8}
N -470 -540 -470 -500 {lab=tap2}
N -450 -570 -430 -570 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -430 -570 2 0 {name=l_gr12 sig_type=std_logic lab=gnd}

* --- XR23: tap2 to tap3, l=6 ---
T {XR23} -530 -460 0 0 0.25 0.25 {layer=13}
T {w=1 l=6} -530 -440 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -470 -430 0 0 {name=XR23
W=1
L=6
model=res_xhigh_po
spiceprefix=X
mult=1}
N -470 -460 -470 -500 {lab=tap2}
T {tap2} -460 -505 0 0 0.3 0.3 {layer=8}
N -470 -400 -470 -360 {lab=tap3}
N -450 -430 -430 -430 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -430 -430 2 0 {name=l_gr23 sig_type=std_logic lab=gnd}

* --- XR34: tap3 to tap4, l=17 ---
T {XR34} -530 -320 0 0 0.25 0.25 {layer=13}
T {w=1 l=17} -530 -300 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -470 -290 0 0 {name=XR34
W=1
L=17
model=res_xhigh_po
spiceprefix=X
mult=1}
N -470 -320 -470 -360 {lab=tap3}
T {tap3} -460 -365 0 0 0.3 0.3 {layer=8}
N -470 -260 -470 -220 {lab=tap4}
N -450 -290 -430 -290 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -430 -290 2 0 {name=l_gr34 sig_type=std_logic lab=gnd}

* --- XRbot: tap4 to gnd, l=69 ---
T {XRbot} -530 -180 0 0 0.25 0.25 {layer=13}
T {w=1 l=69} -530 -160 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -470 -150 0 0 {name=XRbot
W=1
L=69
model=res_xhigh_po
spiceprefix=X
mult=1}
N -470 -180 -470 -220 {lab=tap4}
T {tap4} -460 -225 0 0 0.3 0.3 {layer=8}
N -470 -120 -470 -80 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -470 -80 0 0 {name=lg_bot lab=GND}
N -450 -150 -430 -150 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -430 -150 2 0 {name=l_grbot sig_type=std_logic lab=gnd}

* Horizontal wires from taps to comparators
N -470 -640 -200 -640 {lab=tap1}
N -470 -500 -200 -500 {lab=tap2}
N -470 -360 -200 -360 {lab=tap3}
N -470 -220 -200 -220 {lab=tap4}

* ================================================================
* COMP1 (TH1=2.5V) — tap1 input
* INV1: XMc1ivp (P) + XMc1ivn (N), feedback: XMhf1, INV2: XMc1iv2p + XMc1iv2n
* ================================================================

T {COMP1 (TH1=2.51V)} -180 -830 0 0 0.45 0.45 {layer=4}

* --- XMc1ivp: PFET INV1 top ---
T {XMc1ivp} -160 -740 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} -160 -720 0 0 0.2 0.2 {layer=5}
T {B=PVDD} -50 -790 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -90 -760 0 0 {name=XMc1ivp
L=2
W=2
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -70 -790 -70 -830 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -70 -830 2 0 {name=l_pvc1a sig_type=std_logic lab=pvdd}
N -70 -730 -70 -690 {lab=c1inv}
N -110 -760 -200 -760 {lab=tap1}
N -200 -760 -200 -640 {lab=tap1}

* --- XMc1ivn: NFET INV1 bottom ---
T {XMc1ivn} -160 -580 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} -160 -560 0 0 0.2 0.2 {layer=5}
T {B=GND} -50 -620 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -90 -640 0 0 {name=XMc1ivn
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -70 -610 -70 -560 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -70 -560 0 0 {name=lgc1n lab=GND}
N -70 -670 -70 -690 {lab=c1inv}
N -110 -640 -200 -640 {lab=tap1}
T {c1inv} -65 -695 0 0 0.25 0.25 {layer=8}

* --- XMhf1: feedback NFET (Schmitt) ---
T {XMhf1} 30 -660 0 0 0.25 0.25 {layer=13}
T {W=1.6 L=100} 30 -640 0 0 0.2 0.2 {layer=5}
T {feedback} 30 -620 0 0 0.18 0.18 {}
T {B=GND} 110 -690 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 70 -720 0 0 {name=XMhf1
L=100
W=1.6
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 90 -690 90 -560 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 90 -560 0 0 {name=lgchf1 lab=GND}
N 90 -750 90 -690 {lab=c1inv}
N 90 -690 -70 -690 {lab=c1inv}
N 50 -720 -10 -720 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -10 -720 0 0 {name=l_hf1g sig_type=std_logic lab=comp1}

* --- XMc1iv2p: PFET INV2 top ---
T {XMc1iv2p} -160 -500 0 0 0.25 0.25 {layer=13}
T {W=4 L=2} -160 -480 0 0 0.2 0.2 {layer=5}
T {B=PVDD} -50 -550 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -90 -520 0 0 {name=XMc1iv2p
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -70 -550 -70 -580 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -70 -580 2 0 {name=l_pvc1b sig_type=std_logic lab=pvdd}
N -70 -490 -70 -450 {lab=comp1}
N -110 -520 -140 -520 {lab=c1inv}
N -140 -520 -140 -690 {lab=c1inv}
N -140 -690 -70 -690 {lab=c1inv}

* --- XMc1iv2n: NFET INV2 bottom ---
T {XMc1iv2n} -160 -360 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} -160 -340 0 0 0.2 0.2 {layer=5}
T {B=GND} -50 -390 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -90 -410 0 0 {name=XMc1iv2n
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -70 -380 -70 -330 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -70 -330 0 0 {name=lgc1iv2n lab=GND}
N -70 -440 -70 -450 {lab=comp1}
N -110 -410 -140 -410 {lab=c1inv}
N -140 -410 -140 -520 {lab=c1inv}
T {comp1} -65 -455 0 0 0.3 0.3 {layer=8}
N -70 -450 20 -450 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -450 2 0 {name=l_comp1 sig_type=std_logic lab=comp1}

* ================================================================
* COMP2 (TH2=4.16V) — tap2 input
* ================================================================

T {COMP2 (TH2=4.16V)} 200 -830 0 0 0.45 0.45 {layer=4}

* --- XMc2ivp: PFET INV1 top ---
T {XMc2ivp} 220 -740 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 220 -720 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 330 -790 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 290 -760 0 0 {name=XMc2ivp
L=2
W=2
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 310 -790 310 -830 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 -830 2 0 {name=l_pvc2a sig_type=std_logic lab=pvdd}
N 310 -730 310 -690 {lab=c2inv}
N 270 -760 190 -760 {lab=tap2}
N 190 -760 190 -500 {lab=tap2}

* --- XMc2ivn: NFET INV1 bottom ---
T {XMc2ivn} 220 -580 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 220 -560 0 0 0.2 0.2 {layer=5}
T {B=GND} 330 -620 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 290 -640 0 0 {name=XMc2ivn
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 310 -610 310 -560 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 310 -560 0 0 {name=lgc2n lab=GND}
N 310 -670 310 -690 {lab=c2inv}
N 270 -640 190 -640 {lab=tap2}
N 190 -640 190 -500 {lab=tap2}
T {c2inv} 315 -695 0 0 0.25 0.25 {layer=8}

* --- XMhf2: feedback NFET ---
T {XMhf2} 400 -660 0 0 0.25 0.25 {layer=13}
T {W=1.05 L=100} 400 -640 0 0 0.2 0.2 {layer=5}
T {B=GND} 480 -690 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 440 -720 0 0 {name=XMhf2
L=100
W=1.05
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 460 -690 460 -560 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 460 -560 0 0 {name=lgchf2 lab=GND}
N 460 -750 460 -690 {lab=c2inv}
N 460 -690 310 -690 {lab=c2inv}
N 420 -720 370 -720 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 370 -720 0 0 {name=l_hf2g sig_type=std_logic lab=comp2}

* --- XMc2iv2p: PFET INV2 ---
T {XMc2iv2p} 220 -500 0 0 0.25 0.25 {layer=13}
T {W=4 L=2} 220 -480 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 330 -550 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 290 -520 0 0 {name=XMc2iv2p
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 310 -550 310 -580 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 310 -580 2 0 {name=l_pvc2b sig_type=std_logic lab=pvdd}
N 310 -490 310 -450 {lab=comp2}
N 270 -520 240 -520 {lab=c2inv}
N 240 -520 240 -690 {lab=c2inv}
N 240 -690 310 -690 {lab=c2inv}

* --- XMc2iv2n: NFET INV2 ---
T {XMc2iv2n} 220 -360 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 220 -340 0 0 0.2 0.2 {layer=5}
T {B=GND} 330 -390 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 290 -410 0 0 {name=XMc2iv2n
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 310 -380 310 -330 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 310 -330 0 0 {name=lgc2iv2n lab=GND}
N 310 -440 310 -450 {lab=comp2}
N 270 -410 240 -410 {lab=c2inv}
N 240 -410 240 -520 {lab=c2inv}
T {comp2} 315 -455 0 0 0.3 0.3 {layer=8}
N 310 -450 400 -450 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -450 2 0 {name=l_comp2 sig_type=std_logic lab=comp2}

* ================================================================
* COMP3 (TH3=4.44V) — tap3 input
* ================================================================

T {COMP3 (TH3=4.44V)} 570 -830 0 0 0.45 0.45 {layer=4}

* --- XMc3ivp ---
T {XMc3ivp} 590 -740 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 590 -720 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 700 -790 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 660 -760 0 0 {name=XMc3ivp
L=2
W=2
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 680 -790 680 -830 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 680 -830 2 0 {name=l_pvc3a sig_type=std_logic lab=pvdd}
N 680 -730 680 -690 {lab=c3inv}
N 640 -760 560 -760 {lab=tap3}
N 560 -760 560 -360 {lab=tap3}

* --- XMc3ivn ---
T {XMc3ivn} 590 -580 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 590 -560 0 0 0.2 0.2 {layer=5}
T {B=GND} 700 -620 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 660 -640 0 0 {name=XMc3ivn
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 680 -610 680 -560 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 680 -560 0 0 {name=lgc3n lab=GND}
N 680 -670 680 -690 {lab=c3inv}
N 640 -640 560 -640 {lab=tap3}
N 560 -640 560 -360 {lab=tap3}
T {c3inv} 685 -695 0 0 0.25 0.25 {layer=8}

* --- XMhf3 ---
T {XMhf3} 770 -660 0 0 0.25 0.25 {layer=13}
T {W=0.9 L=100} 770 -640 0 0 0.2 0.2 {layer=5}
T {B=GND} 850 -690 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 810 -720 0 0 {name=XMhf3
L=100
W=0.9
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 830 -690 830 -560 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 830 -560 0 0 {name=lgchf3 lab=GND}
N 830 -750 830 -690 {lab=c3inv}
N 830 -690 680 -690 {lab=c3inv}
N 790 -720 740 -720 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 740 -720 0 0 {name=l_hf3g sig_type=std_logic lab=comp3}

* --- XMc3iv2p ---
T {XMc3iv2p} 590 -500 0 0 0.25 0.25 {layer=13}
T {W=4 L=2} 590 -480 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 700 -550 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 660 -520 0 0 {name=XMc3iv2p
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 680 -550 680 -580 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 680 -580 2 0 {name=l_pvc3b sig_type=std_logic lab=pvdd}
N 680 -490 680 -450 {lab=comp3}
N 640 -520 610 -520 {lab=c3inv}
N 610 -520 610 -690 {lab=c3inv}
N 610 -690 680 -690 {lab=c3inv}

* --- XMc3iv2n ---
T {XMc3iv2n} 590 -360 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 590 -340 0 0 0.2 0.2 {layer=5}
T {B=GND} 700 -390 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 660 -410 0 0 {name=XMc3iv2n
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 680 -380 680 -330 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 680 -330 0 0 {name=lgc3iv2n lab=GND}
N 680 -440 680 -450 {lab=comp3}
N 640 -410 610 -410 {lab=c3inv}
N 610 -410 610 -520 {lab=c3inv}
T {comp3} 685 -455 0 0 0.3 0.3 {layer=8}
N 680 -450 770 -450 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 770 -450 2 0 {name=l_comp3 sig_type=std_logic lab=comp3}

* ================================================================
* COMP4 (TH4=5.52V) — tap4 input
* ================================================================

T {COMP4 (TH4=5.52V)} 940 -830 0 0 0.45 0.45 {layer=4}

* --- XMc4ivp ---
T {XMc4ivp} 960 -740 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 960 -720 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 1070 -790 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1030 -760 0 0 {name=XMc4ivp
L=2
W=2
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1050 -790 1050 -830 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -830 2 0 {name=l_pvc4a sig_type=std_logic lab=pvdd}
N 1050 -730 1050 -690 {lab=c4inv}
N 1010 -760 930 -760 {lab=tap4}
N 930 -760 930 -220 {lab=tap4}

* --- XMc4ivn ---
T {XMc4ivn} 960 -580 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 960 -560 0 0 0.2 0.2 {layer=5}
T {B=GND} 1070 -620 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1030 -640 0 0 {name=XMc4ivn
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 1050 -610 1050 -560 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1050 -560 0 0 {name=lgc4n lab=GND}
N 1050 -670 1050 -690 {lab=c4inv}
N 1010 -640 930 -640 {lab=tap4}
N 930 -640 930 -220 {lab=tap4}
T {c4inv} 1055 -695 0 0 0.25 0.25 {layer=8}

* --- XMhf4 ---
T {XMhf4} 1140 -660 0 0 0.25 0.25 {layer=13}
T {W=0.73 L=100} 1140 -640 0 0 0.2 0.2 {layer=5}
T {B=GND} 1220 -690 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1180 -720 0 0 {name=XMhf4
L=100
W=0.73
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 1200 -690 1200 -560 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1200 -560 0 0 {name=lgchf4 lab=GND}
N 1200 -750 1200 -690 {lab=c4inv}
N 1200 -690 1050 -690 {lab=c4inv}
N 1160 -720 1110 -720 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1110 -720 0 0 {name=l_hf4g sig_type=std_logic lab=comp4}

* --- XMc4iv2p ---
T {XMc4iv2p} 960 -500 0 0 0.25 0.25 {layer=13}
T {W=4 L=2} 960 -480 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 1070 -550 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1030 -520 0 0 {name=XMc4iv2p
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1050 -550 1050 -580 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -580 2 0 {name=l_pvc4b sig_type=std_logic lab=pvdd}
N 1050 -490 1050 -450 {lab=comp4}
N 1010 -520 980 -520 {lab=c4inv}
N 980 -520 980 -690 {lab=c4inv}
N 980 -690 1050 -690 {lab=c4inv}

* --- XMc4iv2n ---
T {XMc4iv2n} 960 -360 0 0 0.25 0.25 {layer=13}
T {W=2 L=2} 960 -340 0 0 0.2 0.2 {layer=5}
T {B=GND} 1070 -390 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1030 -410 0 0 {name=XMc4iv2n
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 1050 -380 1050 -330 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1050 -330 0 0 {name=lgc4iv2n lab=GND}
N 1050 -440 1050 -450 {lab=comp4}
N 1010 -410 980 -410 {lab=c4inv}
N 980 -410 980 -520 {lab=c4inv}
T {comp4} 1055 -455 0 0 0.3 0.3 {layer=8}
N 1050 -450 1140 -450 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1140 -450 2 0 {name=l_comp4 sig_type=std_logic lab=comp4}

* ================================================================
* LOGIC SECTION — Inverters (comp1b..comp4b)
* ================================================================

T {LOGIC: INVERTERS} -180 -200 0 0 0.5 0.5 {layer=4}

* --- XMinv1p / XMinv1n: comp1 -> comp1b ---
T {XMinv1p} -160 -130 0 0 0.22 0.22 {layer=13}
T {W=4 L=2} -160 -115 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -90 -100 0 0 {name=XMinv1p
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -70 -130 -70 -160 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -70 -160 2 0 {name=l_pvlg1a sig_type=std_logic lab=pvdd}
N -70 -70 -70 -30 {lab=comp1b}
N -110 -100 -150 -100 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 -100 0 0 {name=l_c1lg sig_type=std_logic lab=comp1}

T {XMinv1n} -160 20 0 0 0.22 0.22 {layer=13}
T {W=2 L=2} -160 35 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -90 0 0 0 {name=XMinv1n
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -70 30 -70 60 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -70 60 0 0 {name=lginv1n lab=GND}
N -70 -30 -70 -30 {lab=comp1b}
N -110 0 -150 0 {lab=comp1}
N -150 0 -150 -100 {lab=comp1}
T {comp1b} -65 -35 0 0 0.25 0.25 {layer=8}
N -70 -30 10 -30 {lab=comp1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 -30 2 0 {name=l_c1b sig_type=std_logic lab=comp1b}

* --- XMinv2p / XMinv2n: comp2 -> comp2b ---
T {XMinv2p} 100 -130 0 0 0.22 0.22 {layer=13}
T {W=4 L=2} 100 -115 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 170 -100 0 0 {name=XMinv2p
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 190 -130 190 -160 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 190 -160 2 0 {name=l_pvlg2a sig_type=std_logic lab=pvdd}
N 190 -70 190 -30 {lab=comp2b}
N 150 -100 110 -100 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 110 -100 0 0 {name=l_c2lg sig_type=std_logic lab=comp2}

T {XMinv2n} 100 20 0 0 0.22 0.22 {layer=13}
T {W=2 L=2} 100 35 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 170 0 0 0 {name=XMinv2n
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 190 30 190 60 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 190 60 0 0 {name=lginv2n lab=GND}
N 190 -30 190 -30 {lab=comp2b}
N 150 0 110 0 {lab=comp2}
N 110 0 110 -100 {lab=comp2}
T {comp2b} 195 -35 0 0 0.25 0.25 {layer=8}
N 190 -30 270 -30 {lab=comp2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 -30 2 0 {name=l_c2b sig_type=std_logic lab=comp2b}

* --- XMinv3p / XMinv3n: comp3 -> comp3b ---
T {XMinv3p} 360 -130 0 0 0.22 0.22 {layer=13}
T {W=4 L=2} 360 -115 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 430 -100 0 0 {name=XMinv3p
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 450 -130 450 -160 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 450 -160 2 0 {name=l_pvlg3a sig_type=std_logic lab=pvdd}
N 450 -70 450 -30 {lab=comp3b}
N 410 -100 370 -100 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 370 -100 0 0 {name=l_c3lg sig_type=std_logic lab=comp3}

T {XMinv3n} 360 20 0 0 0.22 0.22 {layer=13}
T {W=2 L=2} 360 35 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 430 0 0 0 {name=XMinv3n
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 450 30 450 60 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 450 60 0 0 {name=lginv3n lab=GND}
N 450 -30 450 -30 {lab=comp3b}
N 410 0 370 0 {lab=comp3}
N 370 0 370 -100 {lab=comp3}
T {comp3b} 455 -35 0 0 0.25 0.25 {layer=8}
N 450 -30 530 -30 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 530 -30 2 0 {name=l_c3b sig_type=std_logic lab=comp3b}

* --- XMinv4p / XMinv4n: comp4 -> comp4b ---
T {XMinv4p} 620 -130 0 0 0.22 0.22 {layer=13}
T {W=4 L=2} 620 -115 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 690 -100 0 0 {name=XMinv4p
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 710 -130 710 -160 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 710 -160 2 0 {name=l_pvlg4a sig_type=std_logic lab=pvdd}
N 710 -70 710 -30 {lab=comp4b}
N 670 -100 630 -100 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 630 -100 0 0 {name=l_c4lg sig_type=std_logic lab=comp4}

T {XMinv4n} 620 20 0 0 0.22 0.22 {layer=13}
T {W=2 L=2} 620 35 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 690 0 0 0 {name=XMinv4n
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 710 30 710 60 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 710 60 0 0 {name=lginv4n lab=GND}
N 710 -30 710 -30 {lab=comp4b}
N 670 0 630 0 {lab=comp4}
N 630 0 630 -100 {lab=comp4}
T {comp4b} 715 -35 0 0 0.25 0.25 {layer=8}
N 710 -30 790 -30 {lab=comp4b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 790 -30 2 0 {name=l_c4b sig_type=std_logic lab=comp4b}

* ================================================================
* LOGIC: pass_off buffer (comp1b -> pass_off)
* ================================================================

T {PASS_OFF BUFFER} -180 120 0 0 0.4 0.4 {layer=4}

T {XMpo_bufp} -160 180 0 0 0.22 0.22 {layer=13}
T {W=4 L=2} -160 195 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -90 210 0 0 {name=XMpo_bufp
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -70 180 -70 150 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -70 150 2 0 {name=l_pvpo1 sig_type=std_logic lab=pvdd}
N -70 240 -70 280 {lab=pass_off}
N -110 210 -150 210 {lab=comp1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 210 0 0 {name=l_po_g1 sig_type=std_logic lab=comp1b}

T {XMpo_bufn} -160 330 0 0 0.22 0.22 {layer=13}
T {W=2 L=2} -160 345 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -90 310 0 0 {name=XMpo_bufn
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -70 340 -70 370 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -70 370 0 0 {name=lgpo_n lab=GND}
N -70 280 -70 280 {lab=pass_off}
N -110 310 -150 310 {lab=comp1b}
N -150 310 -150 210 {lab=comp1b}
T {pass_off} -65 275 0 0 0.3 0.3 {layer=8}
N -70 280 30 280 {lab=pass_off}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 30 280 2 0 {name=l_passoff sig_type=std_logic lab=pass_off}

* ================================================================
* LOGIC: bypass_en AOI22 + output inverter
* XMby_n1a, XMby_n1b, XMby_n2a, XMby_n2b (NFET stack)
* XMby_p1a, XMby_p1b, XMby_p2a, XMby_p2b (PFET stack)
* XMby_outp, XMby_outn (output inverter)
* ================================================================

T {BYPASS_EN: AOI22 + INV} 150 120 0 0 0.4 0.4 {layer=4}

* NFET pull-down path 1: comp1 (n1a) in series with comp2b (n1b)
T {XMby_n1a} 130 330 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 170 310 0 0 {name=XMby_n1a
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 190 340 190 370 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 190 370 0 0 {name=lgby1a lab=GND}
N 190 280 190 250 {lab=by_s1}
N 150 310 120 310 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 310 0 0 {name=l_by1a sig_type=std_logic lab=comp1}
T {by_s1} 195 255 0 0 0.2 0.2 {layer=8}

T {XMby_n1b} 130 210 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 170 200 0 0 {name=XMby_n1b
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 190 230 190 250 {lab=by_s1}
N 190 170 190 150 {lab=bypass_enb}
N 150 200 120 200 {lab=comp2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 200 0 0 {name=l_by1b sig_type=std_logic lab=comp2b}

* NFET pull-down path 2: comp3 (n2a) in series with comp4b (n2b)
T {XMby_n2a} 270 330 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 310 310 0 0 {name=XMby_n2a
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 330 340 330 370 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 330 370 0 0 {name=lgby2a lab=GND}
N 330 280 330 250 {lab=by_s2}
N 290 310 260 310 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 260 310 0 0 {name=l_by2a sig_type=std_logic lab=comp3}
T {by_s2} 335 255 0 0 0.2 0.2 {layer=8}

T {XMby_n2b} 270 210 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 310 200 0 0 {name=XMby_n2b
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 330 230 330 250 {lab=by_s2}
N 330 170 330 150 {lab=bypass_enb}
N 290 200 260 200 {lab=comp4b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 260 200 0 0 {name=l_by2b sig_type=std_logic lab=comp4b}
N 190 150 330 150 {lab=bypass_enb}
T {bypass_enb} 240 145 0 0 0.25 0.25 {layer=8}

* PFET pull-up: parallel paths
T {XMby_p1a} 130 500 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 170 530 0 0 {name=XMby_p1a
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 190 500 190 470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 190 470 2 0 {name=l_pvby1a sig_type=std_logic lab=pvdd}
N 190 560 190 590 {lab=by_pmid}
N 150 530 120 530 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 530 0 0 {name=l_byp1a sig_type=std_logic lab=comp1}

T {XMby_p1b} 270 500 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 310 530 0 0 {name=XMby_p1b
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 330 500 330 470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 330 470 2 0 {name=l_pvby1b sig_type=std_logic lab=pvdd}
N 330 560 330 590 {lab=by_pmid}
N 290 530 260 530 {lab=comp2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 260 530 0 0 {name=l_byp1b sig_type=std_logic lab=comp2b}
N 190 590 330 590 {lab=by_pmid}
T {by_pmid} 240 585 0 0 0.2 0.2 {layer=8}

T {XMby_p2a} 130 630 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 170 660 0 0 {name=XMby_p2a
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 190 630 190 590 {lab=by_pmid}
N 190 690 190 720 {lab=bypass_enb}
N 150 660 120 660 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 660 0 0 {name=l_byp2a sig_type=std_logic lab=comp3}

T {XMby_p2b} 270 630 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 310 660 0 0 {name=XMby_p2b
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 330 630 330 590 {lab=by_pmid}
N 330 690 330 720 {lab=bypass_enb}
N 290 660 260 660 {lab=comp4b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 260 660 0 0 {name=l_byp2b sig_type=std_logic lab=comp4b}
N 190 720 330 720 {lab=bypass_enb}
N 260 720 260 150 {lab=bypass_enb}

* Output inverter: bypass_enb -> bypass_en
T {XMby_outp} 400 500 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 440 530 0 0 {name=XMby_outp
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 460 500 460 470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 460 470 2 0 {name=l_pvbyout sig_type=std_logic lab=pvdd}
N 460 560 460 600 {lab=bypass_en}
N 420 530 380 530 {lab=bypass_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 530 0 0 {name=l_byoutg1 sig_type=std_logic lab=bypass_enb}

T {XMby_outn} 400 630 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 440 650 0 0 {name=XMby_outn
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 460 680 460 710 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 460 710 0 0 {name=lgbyout lab=GND}
N 460 620 460 600 {lab=bypass_en}
N 420 650 380 650 {lab=bypass_enb}
N 380 650 380 530 {lab=bypass_enb}
T {bypass_en} 465 595 0 0 0.3 0.3 {layer=8}
N 460 600 540 600 {lab=bypass_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 600 2 0 {name=l_bypass_en sig_type=std_logic lab=bypass_en}

* ================================================================
* LOGIC: ea_en AOI21 + output inverter
* XMea_n1a, XMea_n1b, XMea_n2 (NFET)
* XMea_p1a, XMea_p1b, XMea_p2 (PFET)
* XMea_outp, XMea_outn
* ================================================================

T {EA_EN: AOI21 + INV} 600 120 0 0 0.4 0.4 {layer=4}

* NFET path 1: comp2 (n1a) + comp3b (n1b) in series
T {XMea_n1a} 580 330 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 620 310 0 0 {name=XMea_n1a
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 640 340 640 370 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 640 370 0 0 {name=lgea1a lab=GND}
N 640 280 640 250 {lab=ea_s1}
N 600 310 570 310 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 310 0 0 {name=l_ea1a sig_type=std_logic lab=comp2}
T {ea_s1} 645 255 0 0 0.2 0.2 {layer=8}

T {XMea_n1b} 580 210 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 620 200 0 0 {name=XMea_n1b
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 640 230 640 250 {lab=ea_s1}
N 640 170 640 150 {lab=ea_enb}
N 600 200 570 200 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 200 0 0 {name=l_ea1b sig_type=std_logic lab=comp3b}

* NFET path 2: comp4 to GND (parallel)
T {XMea_n2} 730 330 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 770 310 0 0 {name=XMea_n2
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 790 340 790 370 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 790 370 0 0 {name=lgea2 lab=GND}
N 790 280 790 150 {lab=ea_enb}
N 750 310 720 310 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 310 0 0 {name=l_ea2 sig_type=std_logic lab=comp4}
N 640 150 790 150 {lab=ea_enb}
T {ea_enb} 700 145 0 0 0.25 0.25 {layer=8}

* PFET pull-up
T {XMea_p1a} 580 500 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 620 530 0 0 {name=XMea_p1a
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 640 500 640 470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 640 470 2 0 {name=l_pvea1a sig_type=std_logic lab=pvdd}
N 640 560 640 590 {lab=ea_pmid}
N 600 530 570 530 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 530 0 0 {name=l_eap1a sig_type=std_logic lab=comp2}

T {XMea_p1b} 730 500 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 770 530 0 0 {name=XMea_p1b
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 790 500 790 470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 790 470 2 0 {name=l_pvea1b sig_type=std_logic lab=pvdd}
N 790 560 790 590 {lab=ea_pmid}
N 750 530 720 530 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 530 0 0 {name=l_eap1b sig_type=std_logic lab=comp3b}
N 640 590 790 590 {lab=ea_pmid}
T {ea_pmid} 700 585 0 0 0.2 0.2 {layer=8}

T {XMea_p2} 650 630 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 700 660 0 0 {name=XMea_p2
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 720 630 720 590 {lab=ea_pmid}
N 720 690 720 720 {lab=ea_enb}
N 680 660 650 660 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 660 0 0 {name=l_eap2 sig_type=std_logic lab=comp4}
N 720 720 720 150 {lab=ea_enb}

* Output inverter
T {XMea_outp} 850 500 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 890 530 0 0 {name=XMea_outp
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 910 500 910 470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 910 470 2 0 {name=l_pveaout sig_type=std_logic lab=pvdd}
N 910 560 910 600 {lab=ea_en}
N 870 530 840 530 {lab=ea_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 840 530 0 0 {name=l_eaoutg1 sig_type=std_logic lab=ea_enb}

T {XMea_outn} 850 630 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 890 650 0 0 {name=XMea_outn
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 910 680 910 710 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 910 710 0 0 {name=lgeaout lab=GND}
N 910 620 910 600 {lab=ea_en}
N 870 650 840 650 {lab=ea_enb}
N 840 650 840 530 {lab=ea_enb}
T {ea_en} 915 595 0 0 0.3 0.3 {layer=8}
N 910 600 990 600 {lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 990 600 2 0 {name=l_ea_en sig_type=std_logic lab=ea_en}

* ================================================================
* LOGIC: ref_sel NAND2 + INV
* XMrs_n1, XMrs_n2 (NFET series)
* XMrs_p1, XMrs_p2 (PFET parallel)
* XMrs_outp, XMrs_outn
* ================================================================

T {REF_SEL: NAND2 + INV} -180 440 0 0 0.4 0.4 {layer=4}

T {XMrs_n1} -200 620 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -160 600 0 0 {name=XMrs_n1
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -140 630 -140 660 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -140 660 0 0 {name=lgrs1 lab=GND}
N -140 570 -140 540 {lab=rs_s1}
N -180 600 -210 600 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -210 600 0 0 {name=l_rs1 sig_type=std_logic lab=comp1}
T {rs_s1} -135 545 0 0 0.2 0.2 {layer=8}

T {XMrs_n2} -200 490 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -160 500 0 0 {name=XMrs_n2
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -140 530 -140 540 {lab=rs_s1}
N -140 470 -140 450 {lab=ref_selb}
N -180 500 -210 500 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -210 500 0 0 {name=l_rs2 sig_type=std_logic lab=comp3b}
T {ref_selb} -135 445 0 0 0.25 0.25 {layer=8}

T {XMrs_p1} -200 750 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -160 770 0 0 {name=XMrs_p1
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -140 740 -140 710 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -140 710 2 0 {name=l_pvrs1 sig_type=std_logic lab=pvdd}
N -140 800 -140 830 {lab=ref_selb}
N -180 770 -210 770 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -210 770 0 0 {name=l_rsp1 sig_type=std_logic lab=comp1}

T {XMrs_p2} -50 750 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -10 770 0 0 {name=XMrs_p2
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 10 740 10 710 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 10 710 2 0 {name=l_pvrs2 sig_type=std_logic lab=pvdd}
N 10 800 10 830 {lab=ref_selb}
N -30 770 -60 770 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -60 770 0 0 {name=l_rsp2 sig_type=std_logic lab=comp3b}
N -140 830 10 830 {lab=ref_selb}
N -60 830 -60 450 {lab=ref_selb}
N -60 450 -140 450 {lab=ref_selb}

* Output inverter
T {XMrs_outp} 80 750 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 120 770 0 0 {name=XMrs_outp
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 140 740 140 710 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 710 2 0 {name=l_pvrsout sig_type=std_logic lab=pvdd}
N 140 800 140 840 {lab=ref_sel}
N 100 770 60 770 {lab=ref_selb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 770 0 0 {name=l_rsoutg1 sig_type=std_logic lab=ref_selb}

T {XMrs_outn} 80 870 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 120 890 0 0 {name=XMrs_outn
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 140 920 140 950 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 140 950 0 0 {name=lgrsout lab=GND}
N 140 860 140 840 {lab=ref_sel}
N 100 890 60 890 {lab=ref_selb}
N 60 890 60 770 {lab=ref_selb}
T {ref_sel} 145 835 0 0 0.3 0.3 {layer=8}
N 140 840 220 840 {lab=ref_sel}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 840 2 0 {name=l_ref_sel sig_type=std_logic lab=ref_sel}

* ================================================================
* LOGIC: uvov_en double buffer (comp4 -> uvov_enb -> uvov_en)
* XMuv_p1, XMuv_n1, XMuv_p2, XMuv_n2
* ================================================================

T {UVOV_EN: BUF(comp4)} 350 440 0 0 0.4 0.4 {layer=4}

T {XMuv_p1} 340 510 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 380 530 0 0 {name=XMuv_p1
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 400 500 400 470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 470 2 0 {name=l_pvuv1 sig_type=std_logic lab=pvdd}
N 400 560 400 600 {lab=uvov_enb}
N 360 530 330 530 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 330 530 0 0 {name=l_uv1g sig_type=std_logic lab=comp4}

T {XMuv_n1} 340 630 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 380 650 0 0 {name=XMuv_n1
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 400 680 400 710 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 400 710 0 0 {name=lguv1 lab=GND}
N 400 620 400 600 {lab=uvov_enb}
N 360 650 330 650 {lab=comp4}
N 330 650 330 530 {lab=comp4}
T {uvov_enb} 405 595 0 0 0.25 0.25 {layer=8}

T {XMuv_p2} 480 510 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 520 530 0 0 {name=XMuv_p2
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 540 500 540 470 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 470 2 0 {name=l_pvuv2 sig_type=std_logic lab=pvdd}
N 540 560 540 600 {lab=uvov_en}
N 500 530 470 530 {lab=uvov_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 530 0 0 {name=l_uv2g1 sig_type=std_logic lab=uvov_enb}

T {XMuv_n2} 480 630 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 520 650 0 0 {name=XMuv_n2
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 540 680 540 710 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 540 710 0 0 {name=lguv2 lab=GND}
N 540 620 540 600 {lab=uvov_en}
N 500 650 470 650 {lab=uvov_enb}
N 470 650 470 530 {lab=uvov_enb}
T {uvov_en} 545 595 0 0 0.3 0.3 {layer=8}
N 540 600 620 600 {lab=uvov_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 600 2 0 {name=l_uvov_en sig_type=std_logic lab=uvov_en}

* ================================================================
* LOGIC: ilim_en double buffer (comp4 -> ilim_enb -> ilim_en)
* XMil_p1, XMil_n1, XMil_p2, XMil_n2
* ================================================================

T {ILIM_EN: BUF(comp4)} 350 770 0 0 0.4 0.4 {layer=4}

T {XMil_p1} 340 840 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 380 860 0 0 {name=XMil_p1
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 400 830 400 800 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 800 2 0 {name=l_pvil1 sig_type=std_logic lab=pvdd}
N 400 890 400 930 {lab=ilim_enb}
N 360 860 330 860 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 330 860 0 0 {name=l_il1g sig_type=std_logic lab=comp4}

T {XMil_n1} 340 960 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 380 980 0 0 {name=XMil_n1
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 400 1010 400 1040 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 400 1040 0 0 {name=lgil1 lab=GND}
N 400 950 400 930 {lab=ilim_enb}
N 360 980 330 980 {lab=comp4}
N 330 980 330 860 {lab=comp4}
T {ilim_enb} 405 925 0 0 0.25 0.25 {layer=8}

T {XMil_p2} 480 840 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 520 860 0 0 {name=XMil_p2
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 540 830 540 800 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 800 2 0 {name=l_pvil2 sig_type=std_logic lab=pvdd}
N 540 890 540 930 {lab=ilim_en}
N 500 860 470 860 {lab=ilim_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 860 0 0 {name=l_il2g1 sig_type=std_logic lab=ilim_enb}

T {XMil_n2} 480 960 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 520 980 0 0 {name=XMil_n2
L=2
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 540 1010 540 1040 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 540 1040 0 0 {name=lgil2 lab=GND}
N 540 950 540 930 {lab=ilim_en}
N 500 980 470 980 {lab=ilim_enb}
N 470 980 470 860 {lab=ilim_enb}
T {ilim_en} 545 925 0 0 0.3 0.3 {layer=8}
N 540 930 620 930 {lab=ilim_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 930 2 0 {name=l_ilim_en sig_type=std_logic lab=ilim_en}

* ================================================================
* CHARACTERIZATION
* ================================================================

T {CHARACTERIZATION  (TT 27C, PVDD = 5.0V, BVDD ramp 0-7V)} -600 1050 0 0 0.5 0.5 {layer=4}
T {TH1 (pass_off) = 2.51V     TH2 (bypass_en) = 4.16V     TH3 (ea_en) = 4.44V     TH4 (uvov/ilim) = 5.52V} -600 1090 0 0 0.28 0.28 {layer=7}
T {Hysteresis = 224-244 mV (Schmitt trigger)     |     Iq = 17.3 uA     |     thresh_max_error = 1.43% TT, 8.05% PVT} -600 1115 0 0 0.28 0.28 {layer=7}
T {PVT: 5 process corners (TT/SS/FF/SF/FS) verified     |     Monotonic + Glitch-free     |     16/16 specs PASS} -600 1140 0 0 0.28 0.28 {layer=7}
T {All 16/16 specs PASS} -600 1175 0 0 0.45 0.45 {layer=4}
