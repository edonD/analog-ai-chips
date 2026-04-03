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
T {BLOCK 09: STARTUP CIRCUIT} -600 -900 0 0 1.2 1.2 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  v41: Direct Gate Drive} -600 -830 0 0 0.5 0.5 {layer=8}
T {Gate drive: ea_out -> Rgate(1k) -> gate  |  ea_en: BVDD pullup via Ren(100R)} -600 -795 0 0 0.35 0.35 {}
T {.subckt startup bvdd pvdd gate gnd vref startup_done ea_en ea_out} -600 -760 0 0 0.32 0.32 {layer=13}

* ================================================================
* PORT LIST
* ================================================================
T {PORTS} -600 -680 0 0 0.5 0.5 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -640 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -610 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -480 -640 0 0 {name=p3 lab=gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -480 -610 0 0 {name=p4 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -600 -580 0 0 {name=p5 lab=vref}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -480 -580 0 0 {name=p6 lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -480 -550 0 0 {name=p7 lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -550 0 0 {name=p8 lab=ea_out}

* ================================================================
* SECTION 1: Rgate — gate drive isolation (1k)
* ea_out (BVDD domain) drives pass gate directly through Rgate
* FIX-27: damps startup gate oscillation
* ================================================================
T {GATE DRIVE ISOLATION} -600 -470 0 0 0.5 0.5 {layer=4}
T {Rgate = 1k: ea_out -> gate} -600 -435 0 0 0.28 0.28 {}
T {EA slew rate (0.575 V/us from Cc=40pF) is bottleneck, not Rgate} -600 -410 0 0 0.22 0.22 {}

C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -500 -350 0 0 {name=l_ea1 sig_type=std_logic lab=ea_out}
N -500 -350 -440 -350 {lab=ea_out}
T {Rgate} -420 -390 0 0 0.25 0.25 {layer=13}
T {1 kohm} -420 -370 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} -350 -350 1 0 {name=Rgate
value=1k
}
N -440 -350 -380 -350 {lab=ea_out}
N -320 -350 -230 -350 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -230 -350 2 0 {name=l_gate1 sig_type=std_logic lab=gate}
T {gate} -270 -340 0 0 0.3 0.3 {layer=8}

* ================================================================
* SECTION 2: Ren — ea_en BVDD pullup (100 ohm)
* ea_en ALWAYS HIGH (tied to BVDD through low-R)
* ================================================================
T {ea_en PULLUP} -600 -260 0 0 0.5 0.5 {layer=4}
T {Ren = 100R: BVDD -> ea_en (always HIGH)} -600 -225 0 0 0.28 0.28 {}

C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -500 -170 0 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -500 -170 -440 -170 {lab=bvdd}
T {Ren} -420 -210 0 0 0.25 0.25 {layer=13}
T {100 ohm} -420 -190 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} -350 -170 1 0 {name=Ren
value=100
}
N -440 -170 -380 -170 {lab=bvdd}
N -320 -170 -230 -170 {lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -230 -170 2 0 {name=l_ea_en sig_type=std_logic lab=ea_en}
T {ea_en} -270 -160 0 0 0.3 0.3 {layer=8}

* ================================================================
* SECTION 3: startup_done DETECTOR
* HIGH when PVDD > ~4V
* Resistive divider: sense_mid = pvdd x 212/(788+212) = pvdd x 0.212
* Trips when sense_mid > Vth ~ 0.7V -> pvdd > 3.3V
* ================================================================
T {STARTUP_DONE DETECTOR} 100 -470 0 0 0.5 0.5 {layer=4}
T {Resistive divider + NFET comparator + inverter buffer} 100 -435 0 0 0.28 0.28 {}
T {Trips at PVDD ~ 3.3V (sense_mid = PVDD x 0.212)} 100 -410 0 0 0.25 0.25 {}

* --- XR_top: pvdd to sense_mid, xhigh_po W=2 L=788 ---
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 200 -370 0 1 {name=l_pv1 sig_type=std_logic lab=pvdd}
N 200 -370 200 -330 {lab=pvdd}

T {XR_top} 110 -260 0 0 0.25 0.25 {layer=13}
T {xhigh_po W=2 L=788} 110 -240 0 0 0.2 0.2 {layer=5}
T {R ~ 788 kohm} 110 -215 0 0 0.25 0.25 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 200 -260 0 0 {name=XR_top
W=2
L=788
model=res_xhigh_po
spiceprefix=X
mult=1}
N 200 -290 200 -330 {lab=pvdd}
N 200 -230 200 -180 {lab=sense_mid}
N 220 -260 250 -260 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -260 2 0 {name=l_grt sig_type=std_logic lab=gnd}

T {sense_mid} 210 -185 0 0 0.25 0.25 {layer=8}

* --- XR_bot: sense_mid to gnd, xhigh_po W=2 L=212 ---
T {XR_bot} 110 -120 0 0 0.25 0.25 {layer=13}
T {xhigh_po W=2 L=212} 110 -100 0 0 0.2 0.2 {layer=5}
T {R ~ 212 kohm} 110 -75 0 0 0.25 0.25 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 200 -120 0 0 {name=XR_bot
W=2
L=212
model=res_xhigh_po
spiceprefix=X
mult=1}
N 200 -150 200 -180 {lab=sense_mid}
N 200 -90 200 -40 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 200 -40 0 0 {name=lg1 lab=GND}
N 220 -120 250 -120 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -120 2 0 {name=l_grb sig_type=std_logic lab=gnd}

* --- XMN_det: NFET detector, sense_mid on gate, det_n on drain ---
T {XMN_det} 350 -160 0 0 0.25 0.25 {layer=13}
T {W=4 L=1} 350 -140 0 0 0.2 0.2 {layer=5}
T {B=GND} 430 -205 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 390 -240 0 0 {name=XMN_det
L=1
W=4
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 370 -240 300 -240 {lab=sense_mid}
N 300 -240 300 -180 {lab=sense_mid}
N 300 -180 200 -180 {lab=sense_mid}
N 410 -210 410 -100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 410 -100 0 0 {name=lg2 lab=GND}
N 410 -270 410 -340 {lab=det_n}
T {det_n} 415 -345 0 0 0.25 0.25 {layer=8}

* --- XR_pu: pullup resistor, bvdd to det_n, xhigh_po W=1 L=2000 ---
T {XR_pu} 470 -370 0 0 0.25 0.25 {layer=13}
T {xhigh_po W=1 L=2000} 470 -350 0 0 0.2 0.2 {layer=5}
T {R ~ 4 Mohm} 470 -325 0 0 0.25 0.25 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 540 -370 0 0 {name=XR_pu
W=1
L=2000
model=res_xhigh_po
spiceprefix=X
mult=1}
N 540 -400 540 -440 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 -440 0 1 {name=l_bv2 sig_type=std_logic lab=bvdd}
N 540 -340 540 -310 {lab=det_n}
N 540 -310 410 -310 {lab=det_n}
N 410 -340 410 -310 {lab=det_n}
N 560 -370 590 -370 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -370 2 0 {name=l_grpu sig_type=std_logic lab=gnd}

* --- XMP_inv1 + XMN_inv1: inverter buffer, det_n -> startup_done ---
T {INVERTER: det_n -> startup_done} 630 -470 0 0 0.4 0.4 {layer=4}
T {XMP_inv1  W=4 L=1  B=BVDD} 640 -370 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 700 -330 0 0 {name=XMP_inv1
L=1
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
N 720 -360 720 -400 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 -400 0 1 {name=l_bv3 sig_type=std_logic lab=bvdd}
N 720 -300 720 -270 {lab=startup_done}

T {XMN_inv1  W=2 L=1  B=GND} 640 -190 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 700 -220 0 0 {name=XMN_inv1
L=1
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
N 720 -190 720 -140 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 720 -140 0 0 {name=lg3 lab=GND}
N 720 -250 720 -270 {lab=startup_done}

* Gate connections for inverter
N 680 -330 650 -330 {lab=det_n}
N 650 -330 650 -220 {lab=det_n}
N 650 -220 680 -220 {lab=det_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 -280 0 0 {name=l_dn sig_type=std_logic lab=det_n}

T {startup_done} 725 -275 0 0 0.3 0.3 {layer=8}
N 720 -270 800 -270 {lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -270 2 0 {name=l_sd sig_type=std_logic lab=startup_done}

* ================================================================
* NOTES
* ================================================================
T {DESIGN NOTES (v41)} -600 50 0 0 0.5 0.5 {layer=4}
T {1. Rgate (1k) series resistance for gate drive isolation (FIX-27)} -600 100 0 0 0.28 0.28 {}
T {2. ea_en always HIGH via Ren(100R) to BVDD} -600 130 0 0 0.28 0.28 {}
T {3. startup_done = HIGH when PVDD > ~3.3V (resistor divider + comparator)} -600 160 0 0 0.28 0.28 {}
T {4. Active startup gate pulldown (XMsu_pd) DISABLED — caused PVDD overshoot} -600 190 0 0 0.28 0.28 {}
T {5. EA + soft-start handle startup correctly without active pulldown} -600 220 0 0 0.28 0.28 {}
T {6. No level shifter needed — ea_out drives gate directly via Rgate} -600 250 0 0 0.28 0.28 {}

* ================================================================
* TITLE FRAME
* ================================================================
C {/usr/share/xschem/xschem_library/devices/title.sym} -600 400 0 0 {name=l1 author="Block 09: Startup Circuit v41 -- Analog AI Chips PVDD LDO Regulator"}
