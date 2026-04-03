v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 00: ERROR AMPLIFIER} -650 -1050 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Two-Stage Miller OTA} -650 -970 0 0 0.45 0.45 {layer=8}
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  (Vds max 10.5V)} -650 -935 0 0 0.3 0.3 {}
T {.subckt error_amp  vref  vfb  vout_gate  gnd  ibias  en  bvdd} -650 -905 0 0 0.28 0.28 {layer=13}
T {NOTE: EA is entirely BVDD-powered (pvdd port removed per FIX-10)} -650 -875 0 0 0.25 0.25 {layer=5}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -760 0 0 {name=p1 lab=vref}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -730 0 0 {name=p2 lab=vfb}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -700 0 0 {name=p3 lab=ibias}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -670 0 0 {name=p4 lab=en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -760 0 0 {name=p5 lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -730 0 0 {name=p6 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -700 0 0 {name=p7 lab=gnd}

T {BIAS} -420 -830 0 0 0.5 0.5 {layer=4}
T {STAGE 1: DIFF PAIR + MIRROR LOAD} 100 -830 0 0 0.5 0.5 {layer=4}
T {STAGE 2} 700 -830 0 0 0.5 0.5 {layer=4}

C {/usr/share/xschem/xschem_library/devices/title.sym} -650 830 0 0 {name=l1 author="Block 00: Error Amplifier -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* BIAS: XMbp0 (top, PMOS) -> pb_tail -> XMbn_pb (bottom, NMOS m=4) <- XMbn0 (1uA diode)
* Vertical stack: BVDD at top, GND at bottom, pb_tail in middle
* ================================================================

* --- XMbp0: PMOS bias diode, generates pb_tail (W=20 L=4 m=4) ---
T {XMbp0} -480 -660 0 0 0.25 0.25 {layer=13}
T {W=20 L=4 m=4} -480 -638 0 0 0.2 0.2 {layer=5}
T {B=BVDD} -370 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -410 -680 0 0 {name=XMbp0
L=4
W=20
nf=1
mult=4
model=pfet_g5v0d10v5
spiceprefix=X
}
N -390 -710 -390 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -390 -760 2 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -390 -650 -390 -560 {lab=pb_tail}
N -430 -680 -500 -680 {lab=pb_tail}
N -500 -680 -500 -560 {lab=pb_tail}
N -500 -560 -390 -560 {lab=pb_tail}
T {pb_tail} -385 -565 0 0 0.3 0.3 {layer=8}

* --- XMbn_pb: NMOS mirror m=4, feeds pb_tail via XMbp0 (W=20 L=8 m=4) ---
T {XMbn_pb} -280 -340 0 0 0.25 0.25 {layer=13}
T {W=20 L=8 m=4} -280 -318 0 0 0.2 0.2 {layer=5}
T {4x mirror} -280 -296 0 0 0.18 0.18 {}
T {B=GND} -330 -265 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -410 -400 0 0 {name=XMbn_pb
L=8
W=20
nf=1
mult=4
model=nfet_g5v0d10v5
spiceprefix=X
}
N -390 -370 -390 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -390 -280 0 0 {name=lg1 lab=GND}
N -390 -430 -390 -560 {lab=pb_tail}
N -430 -400 -530 -400 {lab=ibias_en}
T {ibias_en} -535 -410 2 0 0.25 0.25 {layer=8}

* --- XMbn0: NMOS 1uA diode-connected reference (W=2 L=8 m=1) ---
T {XMbn0} -600 -340 0 0 0.25 0.25 {layer=13}
T {W=2 L=8 m=1} -600 -318 0 0 0.2 0.2 {layer=5}
T {1 uA ref} -600 -296 0 0 0.18 0.18 {}
T {B=GND} -490 -265 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -570 -400 0 0 {name=XMbn0
L=8
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -550 -370 -550 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -550 -280 0 0 {name=lg2 lab=GND}
N -550 -430 -550 -470 {lab=ibias_en}
N -590 -400 -640 -400 {lab=ibias_en}
N -640 -400 -640 -470 {lab=ibias_en}
N -640 -470 -550 -470 {lab=ibias_en}
N -530 -400 -430 -400 {lab=ibias_en}

* ibias input
N -550 -470 -550 -560 {lab=ibias_en}
T {ibias} -605 -580 0 0 0.3 0.3 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -550 -600 2 0 {name=l_ib sig_type=std_logic lab=ibias}
N -550 -600 -550 -560 {lab=ibias}

* ================================================================
* STAGE 1: PMOS diff pair + NMOS current mirror load
* XMtail at top -> tail_s -> XM1/XM2 -> d1/d2 -> XMn_l/XMn_r at bottom
* ================================================================

* --- XMtail: tail current source (W=20 L=4 m=4) ---
T {XMtail} 100 -660 0 0 0.25 0.25 {layer=13}
T {W=20 L=4 m=4} 100 -638 0 0 0.2 0.2 {layer=5}
T {~40 uA tail} 100 -616 0 0 0.18 0.18 {}
T {B=BVDD} 200 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 160 -680 0 0 {name=XMtail
L=4
W=20
nf=1
mult=4
model=pfet_g5v0d10v5
spiceprefix=X
}
N 180 -710 180 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -760 2 0 {name=l_bv2 sig_type=std_logic lab=bvdd}
N 180 -650 180 -580 {lab=tail_s}
N 140 -680 60 -680 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -680 0 0 {name=l_pb3 sig_type=std_logic lab=pb_tail}
T {tail_s} 185 -590 0 0 0.25 0.25 {layer=8}

* --- XM1: diff pair + (vref) (W=80 L=4 m=2) ---
T {XM1 (+)} 55 -470 0 0 0.28 0.28 {layer=13}
T {W=80 L=4 m=2} 55 -448 0 0 0.2 0.2 {layer=5}
T {B=BVDD} 140 -545 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 110 -510 0 0 {name=XM1
L=4
W=80
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
N 130 -540 130 -580 {lab=tail_s}
N 130 -580 180 -580 {lab=tail_s}
N 130 -480 130 -350 {lab=d1}
N 90 -510 -10 -510 {lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -10 -510 0 0 {name=l_vr sig_type=std_logic lab=vref}
T {vref} -5 -525 0 0 0.3 0.3 {layer=8}

* --- XM2: diff pair - (vfb) (W=80 L=4 m=2) ---
T {XM2 (-)} 275 -470 0 0 0.28 0.28 {layer=13}
T {W=80 L=4 m=2} 275 -448 0 0 0.2 0.2 {layer=5}
T {B=BVDD} 240 -545 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 250 -510 0 1 {name=XM2
L=4
W=80
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
N 230 -540 230 -580 {lab=tail_s}
N 230 -580 180 -580 {lab=tail_s}
N 230 -480 230 -350 {lab=d2}
N 270 -510 380 -510 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 -510 2 0 {name=l_vf sig_type=std_logic lab=vfb}
T {vfb} 370 -525 2 0 0.3 0.3 {layer=8}

* --- XMn_l: NMOS mirror load (diode-connected) (W=20 L=8 m=2) ---
T {XMn_l} 55 -170 0 0 0.25 0.25 {layer=13}
T {W=20 L=8 m=2} 55 -148 0 0 0.2 0.2 {layer=5}
T {diode} 55 -128 0 0 0.18 0.18 {}
T {B=GND} 140 -215 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 110 -250 0 0 {name=XMn_l
L=8
W=20
nf=1
mult=2
model=nfet_g5v0d10v5
spiceprefix=X
}
N 130 -220 130 -100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 130 -100 0 0 {name=lg3 lab=GND}
N 130 -280 130 -350 {lab=d1}
N 90 -250 40 -250 {lab=d1}
N 40 -250 40 -350 {lab=d1}
N 40 -350 130 -350 {lab=d1}
T {d1} 135 -360 0 0 0.3 0.3 {layer=8}

* --- XMn_r: NMOS mirror load (output) (W=20 L=8 m=2) ---
T {XMn_r} 275 -170 0 0 0.25 0.25 {layer=13}
T {W=20 L=8 m=2} 275 -148 0 0 0.2 0.2 {layer=5}
T {mirror} 275 -128 0 0 0.18 0.18 {}
T {B=GND} 240 -215 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 250 -250 0 1 {name=XMn_r
L=8
W=20
nf=1
mult=2
model=nfet_g5v0d10v5
spiceprefix=X
}
N 230 -220 230 -100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 230 -100 0 0 {name=lg4 lab=GND}
N 230 -280 230 -350 {lab=d2}
N 270 -250 320 -250 {lab=d1}
N 320 -250 320 -350 {lab=d1}
N 320 -350 130 -350 {lab=d1}
T {d2} 235 -360 0 0 0.3 0.3 {layer=8}

* ================================================================
* MILLER COMPENSATION: Cc (40pF) in series with Rc (5k)
* From d2 to vout_gate (across Stage 2)
* FIX-21: was 20pF+8k, retuned after FIX-19 restored 71dB loop gain
* ================================================================

T {Cc = 40 pF} 430 -420 0 0 0.35 0.35 {layer=7}
T {FIX-21} 430 -395 0 0 0.18 0.18 {}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 480 -350 1 0 {name=Cc
m=1
value=40p
}
N 450 -350 230 -350 {lab=d2}
N 510 -350 570 -350 {lab=comp_mid}
T {comp_mid} 540 -365 0 0 0.2 0.2 {layer=8}

T {Rc = 5k} 580 -420 0 0 0.35 0.35 {layer=7}
T {> 1/gm2} 580 -395 0 0 0.18 0.18 {}
T {LHP zero} 580 -375 0 0 0.18 0.18 {}
C {/usr/share/xschem/xschem_library/devices/res.sym} 630 -350 1 0 {name=Rc
value=5k
}
N 600 -350 570 -350 {lab=comp_mid}
N 660 -350 750 -350 {lab=vout_gate}

* ================================================================
* STAGE 2: XMcs_p (PMOS load) on top, XMcs_n (NMOS CS) on bottom
* Connected at vout_gate node
* ================================================================

* --- XMcs_p: PMOS active load (W=20 L=4 m=2) ---
T {XMcs_p} 700 -660 0 0 0.25 0.25 {layer=13}
T {W=20 L=4 m=2} 700 -638 0 0 0.2 0.2 {layer=5}
T {~23 uA} 700 -616 0 0 0.18 0.18 {}
T {B=BVDD} 810 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 770 -680 0 0 {name=XMcs_p
L=4
W=20
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
N 790 -710 790 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 790 -760 2 0 {name=l_bv3 sig_type=std_logic lab=bvdd}
N 790 -650 790 -350 {lab=vout_gate}
N 750 -680 650 -680 {lab=pb_tail}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 -680 0 0 {name=l_pb4 sig_type=std_logic lab=pb_tail}

* --- XMcs_n: NMOS common-source amplifier (W=20 L=2 m=1) ---
T {XMcs_n} 700 -170 0 0 0.25 0.25 {layer=13}
T {W=20 L=2 m=1} 700 -148 0 0 0.2 0.2 {layer=5}
T {CS amp} 700 -128 0 0 0.18 0.18 {}
T {B=GND} 800 -215 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 770 -250 0 0 {name=XMcs_n
L=2
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 790 -220 790 -100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 790 -100 0 0 {name=lg5 lab=GND}
N 790 -280 790 -350 {lab=vout_gate}
N 750 -250 670 -250 {lab=d2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 670 -250 0 0 {name=l_d2g sig_type=std_logic lab=d2}

* vout_gate label and output
T {vout_gate} 830 -370 0 0 0.35 0.35 {layer=4}
T {-> pass FET gate} 830 -345 0 0 0.2 0.2 {}
N 790 -350 920 -350 {lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -350 2 0 {name=l_vg sig_type=std_logic lab=vout_gate}

* ================================================================
* ENABLE: small group, bottom-left
* XMen: NMOS switch gates ibias to ibias_en (W=20 L=1 m=1)
* XMpu: PMOS pullup drives vout_gate to BVDD when en=LOW (W=4 L=2 m=1)
* ================================================================

T {ENABLE} -650 10 0 0 0.45 0.45 {layer=4}

T {en} -670 120 0 0 0.35 0.35 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -640 130 0 0 {name=l_en_main sig_type=std_logic lab=en}
N -640 130 -600 130 {lab=en}

* --- XMpu: PMOS pullup (en=LOW -> vout_gate pulled to BVDD) (W=4 L=2 m=1) ---
T {XMpu} -530 30 0 0 0.25 0.25 {layer=13}
T {W=4 L=2 m=1} -530 52 0 0 0.2 0.2 {layer=5}
T {B=BVDD} -470 85 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -510 100 0 0 {name=XMpu
L=2
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -490 70 -490 40 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -490 40 2 0 {name=l_bv4 sig_type=std_logic lab=bvdd}
N -490 130 -490 170 {lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -490 170 0 0 {name=l_vg2 sig_type=std_logic lab=vout_gate}
N -530 100 -600 100 {lab=en}
N -600 100 -600 130 {lab=en}
T {en=LOW: pulls} -430 120 0 0 0.18 0.18 {}
T {vout_gate to BVDD} -430 140 0 0 0.18 0.18 {}

* --- XMen: NMOS bias switch (en=HIGH -> ibias flows to ibias_en) (W=20 L=1 m=1) ---
T {XMen} -530 195 0 0 0.25 0.25 {layer=13}
T {W=20 L=1 m=1} -530 217 0 0 0.2 0.2 {layer=5}
T {B=GND} -470 255 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -510 260 0 0 {name=XMen
L=1
W=20
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -490 290 -490 340 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -490 340 0 0 {name=lg6 lab=GND}
N -490 230 -490 200 {lab=ibias_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -490 200 2 0 {name=l_ibe sig_type=std_logic lab=ibias_en}
N -530 260 -600 260 {lab=en}
N -600 130 -600 260 {lab=en}
T {en=HIGH: passes} -430 250 0 0 0.18 0.18 {}
T {ibias to bias chain} -430 270 0 0 0.18 0.18 {}

* ================================================================
* DESIGN NOTES
* ================================================================

T {DESIGN NOTES} -650 500 0 0 0.5 0.5 {layer=4}
T {Supply: BVDD only (pvdd removed per FIX-10)} -650 555 0 0 0.28 0.28 {}
T {Cc=40pF, Rc=5k (FIX-21: retuned after FIX-19 restored 71dB loop gain)} -650 585 0 0 0.28 0.28 {layer=7}
T {Stage 2 load: XMcs_p m=2 (reduced from m=4 to save ~23uA Iq)} -650 615 0 0 0.28 0.28 {}
T {XMbn0: W=2u (1uA reference), XMbn_pb: m=4 (mirrors ~40uA)} -650 645 0 0 0.28 0.28 {}
