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
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Sense-Mirror Current Limiter} -650 -970 0 0 0.45 0.45 {layer=8}
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  (Vds max 10.5V)} -650 -935 0 0 0.3 0.3 {}
T {.subckt current_limiter  gate  bvdd  pvdd  gnd  ilim_flag  ibias} -650 -905 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -760 0 0 {name=p1 lab=gate}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -730 0 0 {name=p2 lab=ibias}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -760 0 0 {name=p3 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -730 0 0 {name=p4 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -700 0 0 {name=p5 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -470 -760 0 0 {name=p6 lab=ilim_flag}

T {CASCODE BIAS} -520 -830 0 0 0.5 0.5 {layer=4}
T {SENSE + CASCODE} -120 -830 0 0 0.5 0.5 {layer=4}
T {CURRENT COMPARATOR} 300 -830 0 0 0.5 0.5 {layer=4}
T {INVERTER + PULLUP} 650 -830 0 0 0.5 0.5 {layer=4}
T {GATE CLAMP} 1050 -830 0 0 0.5 0.5 {layer=4}
T {FLAG OUTPUT} 1450 -830 0 0 0.5 0.5 {layer=4}

C {/usr/share/xschem/xschem_library/devices/title.sym} -650 830 0 0 {name=l1 author="Block 04: Current Limiter -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* CASCODE BIAS: XRcas_top (bvdd → cas_bias) + XRcas_bot (cas_bias → gnd)
* Resistive divider from BVDD: cas_bias = BVDD × 400/(300+400)
* ================================================================

* --- XRcas_top: Top bias resistor (W=1 L=300) ---
T {XRcas_top} -580 -660 0 0 0.25 0.25 {layer=13}
T {W=1 L=300} -580 -638 0 0 0.2 0.2 {layer=5}
T {~600k} -580 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -490 -640 0 0 {name=XRcas_top
W=1
L=300
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -490 -670 -490 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -490 -760 2 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -490 -610 -490 -530 {lab=cas_bias}
N -510 -640 -560 -640 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -560 -640 0 0 {name=l_gn1 sig_type=std_logic lab=gnd}
T {cas_bias} -485 -535 0 0 0.3 0.3 {layer=8}

* --- XRcas_bot: Bottom bias resistor (W=1 L=400) ---
T {XRcas_bot} -580 -370 0 0 0.25 0.25 {layer=13}
T {W=1 L=400} -580 -348 0 0 0.2 0.2 {layer=5}
T {~800k} -580 -326 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -490 -430 0 0 {name=XRcas_bot
W=1
L=400
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -490 -460 -490 -530 {lab=cas_bias}
N -490 -400 -490 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -490 -280 0 0 {name=lg1 lab=GND}
N -510 -430 -560 -430 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -560 -430 0 0 {name=l_gn2 sig_type=std_logic lab=gnd}

* ================================================================
* SENSE + CASCODE: XMs (sense PFET) → cas_mid → XMcas (cascode) → sense_out
* ================================================================

* --- XMs: PMOS sense transistor (W=1u L=0.5u, 1/1000 of pass device) ---
T {XMs} -200 -660 0 0 0.25 0.25 {layer=13}
T {W=1u L=0.5u} -200 -638 0 0 0.2 0.2 {layer=5}
T {sense 1/1000} -200 -616 0 0 0.18 0.18 {}
T {B=BVDD} -80 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -120 -680 0 0 {name=XMs
L=0.5e-6
W=1e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -100 -710 -100 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -760 2 0 {name=l_bv2 sig_type=std_logic lab=bvdd}
N -100 -650 -100 -560 {lab=cas_mid}
N -140 -680 -250 -680 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -250 -680 0 0 {name=l_g1 sig_type=std_logic lab=gate}
T {gate} -245 -695 0 0 0.3 0.3 {layer=8}
T {cas_mid} -95 -565 0 0 0.3 0.3 {layer=8}

* --- XMcas: Cascode PMOS (W=10u L=0.5u) for Vds matching ---
T {XMcas} -200 -420 0 0 0.25 0.25 {layer=13}
T {W=10u L=0.5u} -200 -398 0 0 0.2 0.2 {layer=5}
T {cascode} -200 -376 0 0 0.18 0.18 {}
T {B=cas_mid} -80 -470 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -120 -440 0 0 {name=XMcas
L=0.5e-6
W=10e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N -100 -470 -100 -560 {lab=cas_mid}
N -100 -410 -100 -310 {lab=sense_out}
N -140 -440 -250 -440 {lab=cas_bias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -250 -440 0 0 {name=l_cb1 sig_type=std_logic lab=cas_bias}
T {cas_bias} -245 -455 0 0 0.3 0.3 {layer=8}
T {sense_out} -95 -315 0 0 0.3 0.3 {layer=8}

* ================================================================
* CURRENT COMPARATOR: XMref_d (diode, ibias) + XMref_m (mirror, 50:1)
* ================================================================

* --- XMref_d: NMOS diode-connected reference (W=2u L=8u) ---
T {XMref_d} 260 -340 0 0 0.25 0.25 {layer=13}
T {W=2u L=8u} 260 -318 0 0 0.2 0.2 {layer=5}
T {ibias diode} 260 -296 0 0 0.18 0.18 {}
T {B=GND} 390 -385 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 350 -420 0 0 {name=XMref_d
L=8e-6
W=2e-6
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 370 -450 370 -530 {lab=ibias}
N 370 -390 370 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 370 -280 0 0 {name=lg2 lab=GND}
N 330 -420 270 -420 {lab=ibias}
N 270 -420 270 -530 {lab=ibias}
N 270 -530 370 -530 {lab=ibias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 320 -530 0 0 {name=l_ib1 sig_type=std_logic lab=ibias}
T {ibias} 280 -540 0 0 0.3 0.3 {layer=8}

* --- XMref_m: NMOS mirror (W=100u L=8u, 50:1 ratio) ---
T {XMref_m} 460 -340 0 0 0.25 0.25 {layer=13}
T {W=100u L=8u} 460 -318 0 0 0.2 0.2 {layer=5}
T {50:1 mirror} 460 -296 0 0 0.18 0.18 {}
T {B=GND} 590 -385 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 550 -420 0 0 {name=XMref_m
L=8e-6
W=100e-6
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 570 -450 570 -530 {lab=sense_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 570 -530 2 0 {name=l_so1 sig_type=std_logic lab=sense_out}
N 570 -390 570 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 570 -280 0 0 {name=lg3 lab=GND}
N 530 -420 470 -420 {lab=ibias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 470 -420 0 0 {name=l_ib2 sig_type=std_logic lab=ibias}
T {sense_out} 575 -535 0 0 0.3 0.3 {layer=8}

* ================================================================
* INVERTER + PULLUP: XMinv_n/XMinv_p + XRpu
* Converts sense_out → det_n
* ================================================================

* --- XMinv_p: Inverter PMOS (W=20u L=1u) ---
T {XMinv_p} 600 -660 0 0 0.25 0.25 {layer=13}
T {W=20u L=1u} 600 -638 0 0 0.2 0.2 {layer=5}
T {B=BVDD} 720 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 680 -680 0 0 {name=XMinv_p
L=1e-6
W=20e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 700 -710 700 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -760 2 0 {name=l_bv3 sig_type=std_logic lab=bvdd}
N 700 -650 700 -560 {lab=det_n}
N 660 -680 590 -680 {lab=sense_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -680 0 0 {name=l_so2 sig_type=std_logic lab=sense_out}

* --- XMinv_n: Inverter NMOS (W=10u L=1u) ---
T {XMinv_n} 600 -340 0 0 0.25 0.25 {layer=13}
T {W=10u L=1u} 600 -318 0 0 0.2 0.2 {layer=5}
T {B=GND} 720 -385 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 680 -420 0 0 {name=XMinv_n
L=1e-6
W=10e-6
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 700 -450 700 -560 {lab=det_n}
N 700 -390 700 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 700 -280 0 0 {name=lg4 lab=GND}
N 660 -420 590 -420 {lab=sense_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -420 0 0 {name=l_so3 sig_type=std_logic lab=sense_out}
T {det_n} 705 -565 0 0 0.3 0.3 {layer=8}

* --- XRpu: Pull-up resistor on det_n (W=1 L=500) ---
T {XRpu} 800 -660 0 0 0.25 0.25 {layer=13}
T {W=1 L=500} 800 -638 0 0 0.2 0.2 {layer=5}
T {~1M pullup} 800 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 850 -640 0 0 {name=XRpu
W=1
L=500
model=res_xhigh_po
spiceprefix=X
mult=1
}
N 850 -670 850 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 850 -760 2 0 {name=l_bv4 sig_type=std_logic lab=bvdd}
N 850 -610 850 -560 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 850 -560 0 0 {name=l_dn0 sig_type=std_logic lab=det_n}
N 830 -640 780 -640 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -640 0 0 {name=l_gn3 sig_type=std_logic lab=gnd}

* ================================================================
* GATE CLAMP: XMclamp1-4 (4x PMOS W=50u L=0.5u, pulls gate toward BVDD)
* ================================================================

* --- XMclamp1: Clamp PMOS #1 (W=50u L=0.5u) ---
T {XMclamp1} 1000 -660 0 0 0.25 0.25 {layer=13}
T {W=50u L=0.5u} 1000 -638 0 0 0.2 0.2 {layer=5}
T {B=BVDD} 1120 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1080 -680 0 0 {name=XMclamp1
L=0.5e-6
W=50e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1100 -710 1100 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -760 2 0 {name=l_bv5 sig_type=std_logic lab=bvdd}
N 1100 -650 1100 -560 {lab=gate}
N 1060 -680 990 -680 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 990 -680 0 0 {name=l_dn1 sig_type=std_logic lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -560 0 0 {name=l_g2 sig_type=std_logic lab=gate}

* --- XMclamp2: Clamp PMOS #2 (W=50u L=0.5u) ---
T {XMclamp2} 1200 -660 0 0 0.25 0.25 {layer=13}
T {W=50u L=0.5u} 1200 -638 0 0 0.2 0.2 {layer=5}
T {B=BVDD} 1320 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1280 -680 0 0 {name=XMclamp2
L=0.5e-6
W=50e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1300 -710 1300 -760 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1300 -760 2 0 {name=l_bv6 sig_type=std_logic lab=bvdd}
N 1300 -650 1300 -560 {lab=gate}
N 1260 -680 1190 -680 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1190 -680 0 0 {name=l_dn2 sig_type=std_logic lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1300 -560 0 0 {name=l_g3 sig_type=std_logic lab=gate}

* --- XMclamp3: Clamp PMOS #3 (W=50u L=0.5u) ---
T {XMclamp3} 1000 -420 0 0 0.25 0.25 {layer=13}
T {W=50u L=0.5u} 1000 -398 0 0 0.2 0.2 {layer=5}
T {B=BVDD} 1120 -470 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1080 -440 0 0 {name=XMclamp3
L=0.5e-6
W=50e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1100 -470 1100 -520 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -520 2 0 {name=l_bv7 sig_type=std_logic lab=bvdd}
N 1100 -410 1100 -340 {lab=gate}
N 1060 -440 990 -440 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 990 -440 0 0 {name=l_dn3 sig_type=std_logic lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -340 0 0 {name=l_g4 sig_type=std_logic lab=gate}

* --- XMclamp4: Clamp PMOS #4 (W=50u L=0.5u) ---
T {XMclamp4} 1200 -420 0 0 0.25 0.25 {layer=13}
T {W=50u L=0.5u} 1200 -398 0 0 0.2 0.2 {layer=5}
T {B=BVDD} 1320 -470 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1280 -440 0 0 {name=XMclamp4
L=0.5e-6
W=50e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1300 -470 1300 -520 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1300 -520 2 0 {name=l_bv8 sig_type=std_logic lab=bvdd}
N 1300 -410 1300 -340 {lab=gate}
N 1260 -440 1190 -440 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1190 -440 0 0 {name=l_dn4 sig_type=std_logic lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1300 -340 0 0 {name=l_g5 sig_type=std_logic lab=gate}

T {4x clamp PFETs pull gate toward BVDD when det_n LOW} 990 -260 0 0 0.22 0.22 {layer=7}

* ================================================================
* FLAG OUTPUT: XMfp (PMOS) + XMfn (NMOS) inverter
* ilim_flag output
* ================================================================

* --- XMfp: Flag PMOS (W=2u L=1u) ---
T {XMfp} 1400 -660 0 0 0.25 0.25 {layer=13}
T {W=2u L=1u} 1400 -638 0 0 0.2 0.2 {layer=5}
T {B=PVDD} 1520 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1480 -680 0 0 {name=XMfp
L=1e-6
W=2e-6
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 1500 -710 1500 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -760 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}
N 1500 -650 1500 -560 {lab=ilim_flag}
N 1460 -680 1390 -680 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1390 -680 0 0 {name=l_dn5 sig_type=std_logic lab=det_n}

* --- XMfn: Flag NMOS (W=2u L=1u) ---
T {XMfn} 1400 -340 0 0 0.25 0.25 {layer=13}
T {W=2u L=1u} 1400 -318 0 0 0.2 0.2 {layer=5}
T {B=GND} 1520 -385 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1480 -420 0 0 {name=XMfn
L=1e-6
W=2e-6
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 1500 -450 1500 -560 {lab=ilim_flag}
N 1500 -390 1500 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1500 -280 0 0 {name=lg5 lab=GND}
N 1460 -420 1390 -420 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1390 -420 0 0 {name=l_dn6 sig_type=std_logic lab=det_n}

* ilim_flag output
T {ilim_flag} 1535 -565 0 0 0.35 0.35 {layer=4}
N 1500 -560 1620 -560 {lab=ilim_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1620 -560 2 0 {name=l_fl sig_type=std_logic lab=ilim_flag}

* ================================================================
* SIGNAL FLOW ANNOTATIONS
* ================================================================
T {gate (from pass device) → XMs gate} -250 -780 0 0 0.22 0.22 {layer=5}
T {XMs mirrors 1/1000 of pass device current through cascode XMcas} -250 -200 0 0 0.22 0.22 {layer=5}
T {XMref_d: ibias (1uA) diode | XMref_m: 50:1 mirror sinks 50uA from sense_out} 260 -200 0 0 0.22 0.22 {layer=5}
T {When Isense > 50uA: sense_out HIGH → det_n LOW → clamp ON → gate to BVDD} 260 -170 0 0 0.22 0.22 {layer=5}
T {Trip point: 50uA × 1000 = 50mA load current} 260 -140 0 0 0.22 0.22 {layer=5}
