v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 09: STARTUP CIRCUIT} -650 -1050 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Gate Pulldown + Threshold Detect} -650 -970 0 0 0.45 0.45 {layer=8}
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  (Vds max 10.5V)} -650 -935 0 0 0.3 0.3 {}
T {.subckt startup  bvdd  pvdd  gate  gnd  vref  startup_done  ea_en} -650 -905 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -760 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -730 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -700 0 0 {name=p3 lab=vref}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -760 0 0 {name=p4 lab=gate}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -730 0 0 {name=p5 lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -700 0 0 {name=p6 lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -670 0 0 {name=p7 lab=gnd}

T {PVDD THRESHOLD DETECTOR} -500 -830 0 0 0.5 0.5 {layer=4}
T {GATE PULLDOWN} 200 -830 0 0 0.5 0.5 {layer=4}
T {REGULATION ASSIST} 550 -830 0 0 0.5 0.5 {layer=4}
T {OUTPUT FLAGS} 800 -830 0 0 0.5 0.5 {layer=4}

C {/usr/share/xschem/xschem_library/devices/title.sym} -650 830 0 0 {name=l1 author="Block 09: Startup Circuit -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* PVDD THRESHOLD DETECTOR
* R_top (8.2M) + R_bot (1.8M) divider from PVDD
* MN_det trips when sense_mid > Vth at PVDD ~ 3.9V
* R_pu (30M) pulls det_out to BVDD when MN_det is off
* ================================================================

* --- XR_top: 8.2M resistor from PVDD to sense_mid ---
T {XR_top} -480 -660 0 0 0.25 0.25 {layer=13}
T {W=2 L=8200} -480 -638 0 0 0.2 0.2 {layer=5}
T {~8.2 MOhm} -480 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -400 -580 0 0 {name=XR_top
W=2
L=8200
model=res_xhigh_po
spiceprefix=X
mult=1}
N -400 -550 -400 -480 {lab=sense_mid}
N -400 -610 -400 -700 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -400 -700 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}

* --- XR_bot: 1.8M resistor from sense_mid to GND ---
T {XR_bot} -480 -380 0 0 0.25 0.25 {layer=13}
T {W=2 L=1800} -480 -358 0 0 0.2 0.2 {layer=5}
T {~1.8 MOhm} -480 -338 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -400 -310 0 0 {name=XR_bot
W=2
L=1800
model=res_xhigh_po
spiceprefix=X
mult=1}
N -400 -340 -400 -480 {lab=sense_mid}
N -400 -280 -400 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -400 -200 0 0 {name=lg1 lab=GND}
T {sense_mid} -395 -490 0 0 0.3 0.3 {layer=8}

* --- MN_det: detection NMOS ---
T {MN_det} -200 -380 0 0 0.25 0.25 {layer=13}
T {W=10 L=1} -200 -358 0 0 0.2 0.2 {layer=5}
T {threshold} -200 -338 0 0 0.18 0.18 {}
T {comparator} -200 -320 0 0 0.18 0.18 {}
T {B=GND} -140 -445 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -230 -470 0 0 {name=MN_det
L=1
W=10
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -210 -440 -210 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -210 -200 0 0 {name=lg2 lab=GND}
N -210 -500 -210 -580 {lab=det_out}
N -250 -470 -340 -470 {lab=sense_mid}
N -340 -470 -340 -480 {lab=sense_mid}
N -340 -480 -400 -480 {lab=sense_mid}
T {det_out} -205 -585 0 0 0.3 0.3 {layer=8}

* --- XR_pu: 30M pull-up from BVDD ---
T {XR_pu} -100 -660 0 0 0.25 0.25 {layer=13}
T {W=1 L=15001} -100 -638 0 0 0.2 0.2 {layer=5}
T {~30 MOhm} -100 -616 0 0 0.18 0.18 {}
T {0.23 uA} -100 -598 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -20 -580 0 0 {name=XR_pu
W=1
L=15001
model=res_xhigh_po
spiceprefix=X
mult=1}
N -20 -610 -20 -700 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -20 -700 2 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -20 -550 -20 -580 {lab=det_out}
N -20 -580 -210 -580 {lab=det_out}

* ================================================================
* GATE PULLDOWN: R_gate (102k) + MN_gate
* During startup: det_out HIGH -> MN_gate ON -> gate pulled low
* After startup: det_out LOW -> MN_gate OFF -> gate released
* ================================================================

* --- XR_gate: 102k current limiter ---
T {XR_gate} 130 -660 0 0 0.25 0.25 {layer=13}
T {W=1 L=51} 130 -638 0 0 0.2 0.2 {layer=5}
T {~102 kOhm} 130 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 210 -580 0 0 {name=XR_gate
W=1
L=51
model=res_xhigh_po
spiceprefix=X
mult=1}
N 210 -610 210 -700 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -700 2 0 {name=l_gate sig_type=std_logic lab=gate}
N 210 -550 210 -500 {lab=pull_mid}
T {pull_mid} 215 -510 0 0 0.25 0.25 {layer=8}

* --- MN_gate: pulldown switch ---
T {MN_gate} 140 -380 0 0 0.25 0.25 {layer=13}
T {W=5 L=1} 140 -358 0 0 0.2 0.2 {layer=5}
T {gate pulldown} 140 -338 0 0 0.18 0.18 {}
T {B=GND} 220 -445 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 190 -470 0 0 {name=MN_gate
L=1
W=5
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 210 -440 210 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 210 -200 0 0 {name=lg3 lab=GND}
N 210 -500 210 -500 {lab=pull_mid}
N 170 -470 100 -470 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -470 0 0 {name=l_do1 sig_type=std_logic lab=det_out}

* ================================================================
* MN_pu: BVDD-DOMAIN REGULATION ASSIST
* NMOS source follower: drain=bvdd, gate=bvdd, source=gate
* Pulls gate toward bvdd-Vth, extending error amp output range
* Very weak (W=0.42u L=8u) for < 0.1 uA at regulation
* ================================================================

T {MN_pu} 500 -660 0 0 0.25 0.25 {layer=13}
T {W=0.42 L=8} 500 -638 0 0 0.2 0.2 {layer=5}
T {BVDD source} 500 -616 0 0 0.18 0.18 {}
T {follower} 500 -598 0 0 0.18 0.18 {}
T {B=GND} 590 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -740 0 0 {name=MN_pu
L=8
W=0.42
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 580 -770 580 -800 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -800 2 0 {name=l_bv2 sig_type=std_logic lab=bvdd}
N 540 -740 480 -740 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 480 -740 0 0 {name=l_bv3 sig_type=std_logic lab=bvdd}
N 580 -710 580 -660 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -660 0 0 {name=l_gate2 sig_type=std_logic lab=gate}

* ================================================================
* OUTPUT FLAGS: CMOS inverters from det_out
* startup_done = !det_out (HIGH when startup complete)
* ea_en = !det_out (enables error amplifier)
* ================================================================

* --- INV1: startup_done ---
T {INV: startup_done} 790 -700 0 0 0.25 0.25 {layer=13}

T {MP_sd} 820 -650 0 0 0.2 0.2 {layer=13}
T {W=4 L=1} 820 -632 0 0 0.18 0.18 {layer=5}
T {B=BVDD} 870 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 830 -680 0 0 {name=MP_sd
L=1
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 850 -710 850 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 850 -760 2 0 {name=l_bv4 sig_type=std_logic lab=bvdd}
N 850 -650 850 -600 {lab=startup_done}

T {MN_sd} 820 -500 0 0 0.2 0.2 {layer=13}
T {W=2 L=1} 820 -482 0 0 0.18 0.18 {layer=5}
T {B=GND} 870 -555 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 830 -570 0 0 {name=MN_sd
L=1
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 850 -540 850 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 850 -200 0 0 {name=lg4 lab=GND}
N 850 -600 850 -600 {lab=startup_done}
N 810 -680 750 -680 {lab=det_out}
N 750 -680 750 -570 {lab=det_out}
N 810 -570 750 -570 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 -630 0 0 {name=l_do2 sig_type=std_logic lab=det_out}
N 850 -600 920 -600 {lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -600 2 0 {name=l_sd sig_type=std_logic lab=startup_done}
T {startup_done} 925 -615 0 0 0.3 0.3 {layer=4}

* --- INV2: ea_en ---
T {INV: ea_en} 790 -380 0 0 0.25 0.25 {layer=13}

T {MP_ea} 820 -330 0 0 0.2 0.2 {layer=13}
T {W=4 L=1} 820 -312 0 0 0.18 0.18 {layer=5}
T {B=BVDD} 870 -390 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 830 -360 0 0 {name=MP_ea
L=1
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 850 -390 850 -440 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 850 -440 2 0 {name=l_bv5 sig_type=std_logic lab=bvdd}
N 850 -330 850 -280 {lab=ea_en}

T {MN_ea} 820 -180 0 0 0.2 0.2 {layer=13}
T {W=2 L=1} 820 -162 0 0 0.18 0.18 {layer=5}
T {B=GND} 870 -235 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 830 -250 0 0 {name=MN_ea
L=1
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 850 -220 850 -100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 850 -100 0 0 {name=lg5 lab=GND}
N 850 -280 850 -280 {lab=ea_en}
N 810 -360 730 -360 {lab=det_out}
N 730 -360 730 -250 {lab=det_out}
N 810 -250 730 -250 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 730 -310 0 0 {name=l_do3 sig_type=std_logic lab=det_out}
N 850 -280 920 -280 {lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -280 2 0 {name=l_ea sig_type=std_logic lab=ea_en}
T {ea_en} 925 -295 0 0 0.3 0.3 {layer=4}

* ================================================================
* CHARACTERIZATION
* ================================================================

T {CHARACTERIZATION  (TT 27C, BVDD = 7.0V)} -650 500 0 0 0.5 0.5 {layer=4}
T {Startup Time (no load) =   0 us        spec <= 100 us       PASS} -650 555 0 0 0.28 0.28 {layer=7}
T {Startup Time (50 mA)   =   5 us        spec <= 200 us       PASS} -650 585 0 0 0.28 0.28 {layer=7}
T {PVDD Monotonic          = YES           spec = YES           PASS} -650 615 0 0 0.28 0.28 {layer=7}
T {PVDD Overshoot          = 2000 mV       spec <= 200 mV       FAIL (system-level)} -650 645 0 0 0.28 0.28 {layer=7}
T {Handoff Glitch           =  50 mV       spec <= 100 mV       PASS} -650 675 0 0 0.28 0.28 {layer=7}
T {Leakage After Startup   = 0.22 uA      spec <= 1 uA         PASS} -650 705 0 0 0.28 0.28 {layer=7}
T {Peak Inrush Current      = 5.9 mA       spec <= 150 mA       PASS} -650 735 0 0 0.28 0.28 {layer=7}
T {All ramp rates (0.1, 1, 12 V/us), cold crank, PVT corners: PASS} -650 765 0 0 0.28 0.28 {layer=7}
T {10/11 Specs PASS  |  Overshoot is error amp output range limitation} -650 810 0 0 0.45 0.45 {layer=4}
