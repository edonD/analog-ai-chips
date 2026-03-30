v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

* ================================================================
* TITLE BLOCK
* ================================================================
T {BLOCK 09: STARTUP CIRCUIT} -1100 -1250 0 0 1.2 1.2 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Switched Source Follower + Level Shifter} -1100 -1170 0 0 0.5 0.5 {layer=8}
T {All HV: sky130_fd_pr__pfet_g5v0d10v5 / nfet_g5v0d10v5  (Vds max 10.5V)} -1100 -1130 0 0 0.35 0.35 {}
T {.subckt startup  bvdd  pvdd  gate  gnd  vref  startup_done  ea_en  ea_out} -1100 -1095 0 0 0.32 0.32 {layer=13}

* ================================================================
* PORT LIST
* ================================================================
T {PORTS} -1100 -1010 0 0 0.5 0.5 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1100 -960 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -1100 -930 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -980 -960 0 0 {name=p3 lab=gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -980 -930 0 0 {name=p4 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1100 -900 0 0 {name=p5 lab=vref}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -980 -900 0 0 {name=p6 lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -980 -870 0 0 {name=p7 lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -1100 -870 0 0 {name=p8 lab=ea_out}

* ================================================================
* SECTION 1: PVDD THRESHOLD DETECTOR (left)
* ================================================================
T {PVDD THRESHOLD DETECTOR} -1100 -800 0 0 0.5 0.5 {layer=4}
T {Trips at PVDD ~ 4V (sense_mid = PVDD x 0.2125)} -1100 -760 0 0 0.28 0.28 {}

C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -900 -720 0 1 {name=l_pv1 sig_type=std_logic lab=pvdd}
N -900 -720 -900 -660 {lab=pvdd}

T {XR_top} -990 -570 0 0 0.25 0.25 {layer=13}
T {xhigh_po  W=2  L=788} -990 -545 0 0 0.2 0.2 {layer=5}
T {R ~ 788 kohm} -990 -520 0 0 0.25 0.25 {layer=7}
C {/usr/share/xschem/xschem_library/devices/res.sym} -900 -570 0 0 {name=XR_top
value="sky130_fd_pr__res_xhigh_po w=2 l=788"
}
N -900 -660 -900 -600 {lab=pvdd}
N -900 -540 -900 -440 {lab=sense_mid}
T {sense_mid} -895 -450 0 0 0.25 0.25 {layer=8}

T {XR_bot} -990 -350 0 0 0.25 0.25 {layer=13}
T {xhigh_po  W=2  L=212} -990 -325 0 0 0.2 0.2 {layer=5}
T {R ~ 212 kohm} -990 -300 0 0 0.25 0.25 {layer=7}
C {/usr/share/xschem/xschem_library/devices/res.sym} -900 -350 0 0 {name=XR_bot
value="sky130_fd_pr__res_xhigh_po w=2 l=212"
}
N -900 -440 -900 -380 {lab=sense_mid}
N -900 -320 -900 -250 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -900 -250 0 0 {name=lg1 lab=GND}

T {XMN_det} -750 -350 0 0 0.25 0.25 {layer=13}
T {W=4 L=1} -750 -328 0 0 0.2 0.2 {layer=5}
T {B=GND} -650 -395 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -700 -430 0 0 {name=XMN_det
L=1
W=4
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N -680 -400 -680 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -680 -280 0 0 {name=lg2 lab=GND}
N -680 -460 -680 -530 {lab=det_n}
N -720 -430 -900 -430 {lab=sense_mid}
N -900 -440 -900 -430 {lab=sense_mid}
T {det_n} -675 -540 0 0 0.25 0.25 {layer=8}

T {XR_pu} -750 -620 0 0 0.25 0.25 {layer=13}
T {xhigh_po  W=1  L=2000} -750 -595 0 0 0.2 0.2 {layer=5}
T {R ~ 4 Mohm} -750 -570 0 0 0.25 0.25 {layer=7}
C {/usr/share/xschem/xschem_library/devices/res.sym} -680 -620 0 0 {name=XR_pu
value="sky130_fd_pr__res_xhigh_po w=1 l=2000"
}
N -680 -650 -680 -700 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -680 -700 0 1 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -680 -590 -680 -530 {lab=det_n}

* ================================================================
* SECTION 2: INVERTER CHAIN (det_n -> det_out -> inv_det)
* ================================================================
T {LOGIC: INVERTER CHAIN} -500 -800 0 0 0.5 0.5 {layer=4}

T {INV1: det_n -> det_out} -500 -660 0 0 0.25 0.25 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -430 -570 0 0 {name=XMP_inv1
L=1 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X
}
N -410 -600 -410 -640 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -410 -640 0 1 {name=l_bv2 sig_type=std_logic lab=bvdd}
N -410 -540 -410 -500 {lab=det_out}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -430 -460 0 0 {name=XMN_inv1
L=1 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N -410 -430 -410 -370 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -410 -370 0 0 {name=lg3 lab=GND}
N -450 -570 -520 -570 {lab=det_n}
N -520 -570 -520 -460 {lab=det_n}
N -520 -460 -450 -460 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -520 -530 0 0 {name=l_dn sig_type=std_logic lab=det_n}
T {det_out} -405 -510 0 0 0.25 0.25 {layer=8}

T {INV2: det_out -> inv_det} -310 -660 0 0 0.25 0.25 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -240 -570 0 0 {name=XMP_inv2
L=1 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X
}
N -220 -600 -220 -640 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -220 -640 0 1 {name=l_bv3 sig_type=std_logic lab=bvdd}
N -220 -540 -220 -500 {lab=inv_det}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -240 -460 0 0 {name=XMN_inv2
L=1 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N -220 -430 -220 -370 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -220 -370 0 0 {name=lg4 lab=GND}
N -260 -570 -330 -570 {lab=det_out}
N -330 -570 -330 -460 {lab=det_out}
N -330 -460 -260 -460 {lab=det_out}
N -330 -500 -410 -500 {lab=det_out}
T {inv_det} -215 -510 0 0 0.25 0.25 {layer=8}
T {HIGH during startup} -215 -485 0 0 0.18 0.18 {}

* ================================================================
* SECTION 3: SWITCHED SOURCE FOLLOWERS
* ================================================================
T {SWITCHED SOURCE FOLLOWERS} 50 -800 0 0 0.5 0.5 {layer=4}
T {Active during startup (inv_det=BVDD), OFF after (inv_det=0V)} 50 -760 0 0 0.28 0.28 {}
T {Body effect: gate ~ BVDD - 1.5V, Vsg ~ 1.5V} 50 -735 0 0 0.25 0.25 {}

T {XMN_sf1  W=20 L=1} 60 -550 0 0 0.2 0.2 {layer=5}
T {B=GND} 160 -595 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 120 -610 0 0 {name=XMN_sf1
L=1 W=20 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 140 -640 140 -680 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 -680 0 1 {name=l_bv4 sig_type=std_logic lab=bvdd}
N 140 -580 140 -510 {lab=gate}
N 100 -610 30 -610 {lab=inv_det}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 30 -610 0 0 {name=l_id1 sig_type=std_logic lab=inv_det}

T {XMN_sf2  W=20 L=1} 260 -550 0 0 0.2 0.2 {layer=5}
T {B=GND} 360 -595 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 320 -610 0 0 {name=XMN_sf2
L=1 W=20 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 340 -640 340 -680 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -680 0 1 {name=l_bv5 sig_type=std_logic lab=bvdd}
N 340 -580 340 -510 {lab=gate}
N 300 -610 230 -610 {lab=inv_det}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 230 -610 0 0 {name=l_id2 sig_type=std_logic lab=inv_det}

N 140 -510 340 -510 {lab=gate}
N 240 -510 240 -470 {lab=gate}
T {gate} 245 -475 0 0 0.35 0.35 {layer=4}
T {-> pass device gate} 245 -450 0 0 0.2 0.2 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 240 -510 0 0 {name=l_gate1 sig_type=std_logic lab=gate}

* ================================================================
* SECTION 4: LEVEL SHIFTER
* ================================================================
T {NON-INVERTING LEVEL SHIFTER} 50 -390 0 0 0.5 0.5 {layer=4}
T {NMOS common-gate + R_load from BVDD + 4-diode clamped bias} 50 -355 0 0 0.28 0.28 {}

T {XR_load  W=1 L=50} 360 -345 0 0 0.2 0.2 {layer=5}
T {R ~ 100 kohm} 360 -320 0 0 0.25 0.25 {layer=7}
C {/usr/share/xschem/xschem_library/devices/res.sym} 430 -300 0 0 {name=XR_load
value="sky130_fd_pr__res_xhigh_po w=1 l=50"
}
N 430 -330 430 -420 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 -420 0 1 {name=l_bv6 sig_type=std_logic lab=bvdd}
N 430 -270 430 -200 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 -200 0 0 {name=l_gate2 sig_type=std_logic lab=gate}

T {XMN_cg  W=2 L=4} 60 -195 0 0 0.2 0.2 {layer=5}
T {common-gate} 60 -170 0 0 0.18 0.18 {}
T {B=GND} 200 -240 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 160 -250 0 0 {name=XMN_cg
L=4 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 180 -280 180 -340 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -340 0 1 {name=l_gate3 sig_type=std_logic lab=gate}
N 180 -220 180 -160 {lab=ea_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -160 0 0 {name=l_ea1 sig_type=std_logic lab=ea_out}
T {ea_out (from error amp)} 185 -170 0 0 0.25 0.25 {layer=8}
N 140 -250 70 -250 {lab=ls_bias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 70 -250 0 0 {name=l_lsb sig_type=std_logic lab=ls_bias}

* ================================================================
* SECTION 5: BIAS + DIODE CLAMP
* ================================================================
T {LEVEL SHIFTER BIAS + CLAMP} 600 -800 0 0 0.5 0.5 {layer=4}
T {R divider from BVDD, clamped by 4x diode NMOS (W=18um)} 600 -760 0 0 0.28 0.28 {}

C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -720 0 1 {name=l_bv7 sig_type=std_logic lab=bvdd}
N 700 -720 700 -650 {lab=bvdd}
T {XR_lb1  W=2 L=1000  R~1M} 720 -610 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} 700 -610 0 0 {name=XR_lb1
value="sky130_fd_pr__res_xhigh_po w=2 l=1000"
}
N 700 -650 700 -640 {lab=bvdd}
N 700 -580 700 -530 {lab=ls_bias}
T {ls_bias ~ 4.2V} 705 -540 0 0 0.3 0.3 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -530 2 0 {name=l_lsb2 sig_type=std_logic lab=ls_bias}

T {4x diode-connected NMOS  W=18 L=1} 720 -480 0 0 0.22 0.22 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 680 -470 0 0 {name=XMD1
L=1 W=18 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 700 -500 700 -530 {lab=ls_bias}
N 660 -470 620 -470 {lab=ls_bias}
N 620 -470 620 -530 {lab=ls_bias}
N 620 -530 700 -530 {lab=ls_bias}
N 700 -440 700 -420 {lab=d1}

C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 680 -390 0 0 {name=XMD2
L=1 W=18 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 660 -390 620 -390 {lab=d1}
N 620 -390 620 -420 {lab=d1}
N 620 -420 700 -420 {lab=d1}
N 700 -360 700 -340 {lab=d2}

C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 680 -310 0 0 {name=XMD3
L=1 W=18 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 660 -310 620 -310 {lab=d2}
N 620 -310 620 -340 {lab=d2}
N 620 -340 700 -340 {lab=d2}
N 700 -280 700 -260 {lab=d3}

C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 680 -230 0 0 {name=XMD4
L=1 W=18 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 660 -230 620 -230 {lab=d3}
N 620 -230 620 -260 {lab=d3}
N 620 -260 700 -260 {lab=d3}
N 700 -200 700 -150 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 700 -150 0 0 {name=lg5 lab=GND}

T {XR_lb2  W=2 L=6000  R~6M} 820 -420 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} 850 -350 0 0 {name=XR_lb2
value="sky130_fd_pr__res_xhigh_po w=2 l=6000"
}
N 850 -380 850 -530 {lab=ls_bias}
N 850 -530 700 -530 {lab=ls_bias}
N 850 -320 850 -150 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 850 -150 0 0 {name=lg6 lab=GND}

* ================================================================
* SECTION 6: STARTUP ea_out PULLUP
* ================================================================
T {STARTUP ea_out PULLUP} -500 -195 0 0 0.4 0.4 {layer=4}
T {ON during startup (det_out=LOW), OFF after} -500 -165 0 0 0.22 0.22 {}

T {XMP_pu_ea  W=1 L=1  B=PVDD} -500 -120 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -430 -40 0 0 {name=XMP_pu_ea
L=1 W=1 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X
}
N -410 -70 -410 -100 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -410 -100 0 1 {name=l_pv2 sig_type=std_logic lab=pvdd}
N -410 -10 -410 30 {lab=ea_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -410 30 0 0 {name=l_ea2 sig_type=std_logic lab=ea_out}
N -450 -40 -520 -40 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -520 -40 0 0 {name=l_do1 sig_type=std_logic lab=det_out}

* ================================================================
* SECTION 7: ea_en RC DELAY
* ================================================================
T {ea_en: RC DELAYED HANDOFF} -1100 -100 0 0 0.5 0.5 {layer=4}
T {Inverter + RC for soft handoff (tau = 2.4ms)} -1100 -65 0 0 0.28 0.28 {}

T {INV(ea_en) P:W=2 L=1 N:W=4 L=1} -1070 -10 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1030 -10 0 0 {name=XMP_ea
L=1 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X
}
N -1010 -40 -1010 -60 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1010 -60 0 1 {name=l_bv8 sig_type=std_logic lab=bvdd}
N -1010 20 -1010 60 {lab=ea_en_fast}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -1030 100 0 0 {name=XMN_ea
L=1 W=4 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N -1010 130 -1010 170 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -1010 170 0 0 {name=lg7 lab=GND}
N -1050 -10 -1120 -10 {lab=inv_det}
N -1120 -10 -1120 100 {lab=inv_det}
N -1120 100 -1050 100 {lab=inv_det}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1120 50 0 0 {name=l_id3 sig_type=std_logic lab=inv_det}
T {ea_en_fast} -1005 55 0 0 0.22 0.22 {layer=8}

T {XR_delay  W=1 L=10000  R=20M} -870 30 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} -870 60 1 0 {name=XR_delay
value="sky130_fd_pr__res_xhigh_po w=1 l=10000"
}
N -900 60 -1010 60 {lab=ea_en_fast}
N -840 60 -750 60 {lab=ea_en}
T {ea_en} -745 50 0 0 0.3 0.3 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -750 60 2 0 {name=l_ea_en sig_type=std_logic lab=ea_en}

T {C_delay = 120 pF} -810 100 0 0 0.25 0.25 {layer=7}
C {/usr/share/xschem/xschem_library/devices/capa.sym} -750 120 0 0 {name=C_delay
m=1
value=120p
}
N -750 90 -750 60 {lab=ea_en}
N -750 150 -750 190 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -750 190 0 0 {name=lg8 lab=GND}

* ================================================================
* SECTION 8: startup_done BUFFER
* ================================================================
T {startup_done: DOUBLE-INVERSION BUFFER} 50 -50 0 0 0.4 0.4 {layer=4}
T {det_out -> sd_inv -> startup_done} 50 -20 0 0 0.22 0.22 {}

T {INV3 P:W=4 L=1 N:W=2 L=1} 85 30 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 120 50 0 0 {name=XMP_sd1
L=1 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 120 160 0 0 {name=XMN_sd1
L=1 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 140 20 140 -20 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 140 -20 0 1 {name=l_bv9 sig_type=std_logic lab=bvdd}
N 140 80 140 130 {lab=sd_inv}
N 140 190 140 230 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 140 230 0 0 {name=lg9 lab=GND}
N 100 50 50 50 {lab=det_out}
N 50 50 50 160 {lab=det_out}
N 50 160 100 160 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 50 105 0 0 {name=l_do2 sig_type=std_logic lab=det_out}

T {INV4 P:W=4 L=1 N:W=2 L=1} 265 30 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 300 50 0 0 {name=XMP_sd2
L=1 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 300 160 0 0 {name=XMN_sd2
L=1 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X
}
N 320 20 320 -20 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 320 -20 0 1 {name=l_bv10 sig_type=std_logic lab=bvdd}
N 320 80 320 130 {lab=startup_done}
N 320 190 320 230 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 320 230 0 0 {name=lg10 lab=GND}
N 280 50 230 50 {lab=sd_inv}
N 230 50 230 160 {lab=sd_inv}
N 230 160 280 160 {lab=sd_inv}
N 230 105 140 105 {lab=sd_inv}
T {startup_done} 325 100 0 0 0.3 0.3 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 320 105 2 0 {name=l_sd sig_type=std_logic lab=startup_done}

* ================================================================
* CHARACTERIZATION
* ================================================================
T {CHARACTERIZATION  (TT 27C, BVDD = 7V, Cout = 10nF)} -1100 380 0 0 0.55 0.55 {layer=4}

T {PVDD overshoot (basic, 7V)   =  168 mV          spec <= 200 mV        PASS} -1100 440 0 0 0.28 0.28 {layer=7}
T {PVDD final (basic)           =  4.978 V         spec [4.9, 5.2] V     PASS} -1100 470 0 0 0.28 0.28 {layer=7}
T {PVDD monotonic               =  YES             spec = yes             PASS} -1100 500 0 0 0.28 0.28 {layer=7}
T {Handoff glitch               =  0 mV            spec <= 100 mV        PASS} -1100 530 0 0 0.28 0.28 {layer=7}
T {50mA load: PVDD final        =  4.977 V         spec [4.9, 5.2] V     PASS} -1100 560 0 0 0.28 0.28 {layer=7}
T {Peak inrush                  =  22 mA           spec <= 150 mA        PASS} -1100 590 0 0 0.28 0.28 {layer=7}
T {SS 150C: PVDD final          =  4.942 V         spec [4.9, 5.2] V     PASS} -1100 620 0 0 0.28 0.28 {layer=7}
T {Post-startup leakage         < 1 uA             spec <= 1 uA          PASS} -1100 650 0 0 0.28 0.28 {layer=7}
T {Fast ramp overshoot (10.5V)  =  257 mV          spec <= 200 mV        FAIL (Cgd coupling)} -1100 700 0 0 0.28 0.28 {layer=7}
T {FF -40C overshoot (10.5V)    =  296 mV          spec <= 200 mV        FAIL (Cgd coupling)} -1100 730 0 0 0.28 0.28 {layer=7}

T {8/12 specs PASS  |  Remaining: fast/slow ramp overshoot at BVDD=10.5V (Cgd coupling limited)} -1100 780 0 0 0.45 0.45 {layer=4}

* ================================================================
* TITLE FRAME
* ================================================================
C {/usr/share/xschem/xschem_library/devices/title.sym} -1100 880 0 0 {name=l1 author="Block 09: Startup Circuit -- Analog AI Chips PVDD LDO Regulator"}
