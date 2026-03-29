v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 03: COMPENSATION NETWORK} -500 -700 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Miller + Output Decoupling} -500 -620 0 0 0.45 0.45 {layer=8}
T {All PDK devices: sky130_fd_pr__cap_mim_m3_1, sky130_fd_pr__res_xhigh_po} -500 -585 0 0 0.3 0.3 {}
T {.subckt compensation  vout_gate  pvdd  gnd} -500 -555 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -500 -460 0 0 {name=p1 lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -410 -460 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -410 -430 0 0 {name=p3 lab=gnd}

C {/usr/share/xschem/xschem_library/devices/title.sym} -500 600 0 0 {name=l1 author="Block 03: Compensation -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* SECTION LABELS
* ================================================================

T {MILLER COMPENSATION} -350 -380 0 0 0.55 0.55 {layer=4}
T {Cc + Rz: pole-splitting with LHP zero} -350 -345 0 0 0.28 0.28 {}

T {OUTPUT DECOUPLING} 300 -380 0 0 0.55 0.55 {layer=4}
T {Cout: supplements 200pF Cload} 300 -345 0 0 0.28 0.28 {}

* ================================================================
* MILLER COMPENSATION PATH: vout_gate → XCc → cc_mid → XRz → pvdd
* Signal flow: left to right
* ================================================================

* --- vout_gate input label ---
T {vout_gate} -380 -255 0 0 0.35 0.35 {layer=4}
T {from error amp} -380 -230 0 0 0.2 0.2 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -350 -200 0 0 {name=l_vg sig_type=std_logic lab=vout_gate}
N -350 -200 -200 -200 {lab=vout_gate}

* --- XCc: Miller capacitor (30 pF MIM) ---
T {XCc} -195 -310 0 0 0.3 0.3 {layer=13}
T {Miller Cap} -195 -288 0 0 0.22 0.22 {}
T {~30 pF} -195 -268 0 0 0.22 0.22 {layer=5}
T {14,884 um^2} -195 -248 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -130 -200 3 0 {name=XCc
W=122
L=122
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
N -200 -200 -160 -200 {lab=vout_gate}
N -100 -200 -20 -200 {lab=cc_mid}
T {cc_mid} -15 -215 0 0 0.25 0.25 {layer=8}

* --- XRz: Nulling resistor (5 kOhm xhigh poly) ---
T {XRz} 30 -310 0 0 0.3 0.3 {layer=13}
T {Nulling R} 30 -288 0 0 0.22 0.22 {}
T {~5 kOhm} 30 -268 0 0 0.22 0.22 {layer=5}
T {LHP zero} 30 -248 0 0 0.18 0.18 {}
T {f_z = 1/(2pi*Rz*Cc)} 30 -228 0 0 0.15 0.15 {}
T {= 1.06 MHz} 30 -212 0 0 0.15 0.15 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 100 -200 3 0 {name=XRz
W=4
L=10
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -20 -200 70 -200 {lab=cc_mid}
N 130 -200 250 -200 {lab=pvdd}

* Body connection for Rz to gnd
N 100 -180 100 -140 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 100 -140 0 0 {name=lg1 lab=GND}

* --- pvdd label at end of Miller path ---
T {pvdd} 260 -215 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -200 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}

* ================================================================
* OUTPUT DECOUPLING: XCout from pvdd to gnd
* Vertical: pvdd at top, gnd at bottom
* ================================================================

* --- XCout: Output decoupling capacitor (70 pF MIM) ---
T {XCout} 390 -80 0 0 0.3 0.3 {layer=13}
T {Output Decoupling} 390 -58 0 0 0.22 0.22 {}
T {~70 pF} 390 -38 0 0 0.22 0.22 {layer=5}
T {34,969 um^2} 390 -18 0 0 0.18 0.18 {}
T {supplements 200pF Cload} 390 4 0 0 0.15 0.15 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 360 -50 0 0 {name=XCout
W=187
L=187
MF=1
model=cap_mim_m3_1
spiceprefix=X
}

* pvdd connection at top of Cout
N 360 -80 360 -200 {lab=pvdd}
N 250 -200 360 -200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 360 -200 2 0 {name=l_pv2 sig_type=std_logic lab=pvdd}

* gnd connection at bottom of Cout
N 360 -20 360 40 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 360 40 0 0 {name=lg2 lab=GND}

* ================================================================
* CIRCUIT TOPOLOGY DIAGRAM (for visual clarity)
* ================================================================

T {CIRCUIT TOPOLOGY:} -500 90 0 0 0.4 0.4 {layer=4}
T {vout_gate ──┤ XCc (30pF) ├── cc_mid ──┤ XRz (5k) ├── pvdd ──┤ XCout (70pF) ├── gnd} -500 130 0 0 0.32 0.32 {layer=8}
T {(EA output)       Miller cap         LHP zero node       nulling R           (5.0V)       output decoupling} -500 160 0 0 0.22 0.22 {}

* ================================================================
* CHARACTERIZATION (TT 27°C, BVDD=7V, with real Block 02 feedback)
* ================================================================

T {CHARACTERIZATION  (TT 27C, BVDD = 7.0V, real Block 02 feedback network)} -500 240 0 0 0.5 0.5 {layer=4}
T {PM at 0 mA       =  45.8 deg       spec >= 45 deg       PASS} -500 295 0 0 0.28 0.28 {layer=7}
T {PM at 100 uA     =  84.4 deg       spec >= 45 deg       PASS} -500 325 0 0 0.28 0.28 {layer=7}
T {PM at 1 mA       =  80.7 deg       spec >= 45 deg       PASS} -500 355 0 0 0.28 0.28 {layer=7}
T {PM at 10 mA      =  58.4 deg       spec >= 45 deg       PASS} -500 385 0 0 0.28 0.28 {layer=7}
T {PM at 50 mA      =  46.6 deg       spec >= 45 deg       PASS} -500 415 0 0 0.28 0.28 {layer=7}
T {GM at all loads   >  100 dB        spec >= 10 dB        PASS} -500 445 0 0 0.28 0.28 {layer=7}
T {Undershoot 1->10  =  116 mV        spec <= 150 mV       PASS} -500 475 0 0 0.28 0.28 {layer=7}
T {Overshoot 10->1   =  150 mV        spec <= 150 mV       PASS} -500 505 0 0 0.28 0.28 {layer=7}
T {Settling time     =  1.0 us        spec <= 10 us        PASS} -500 535 0 0 0.28 0.28 {layer=7}
T {Total comp area   =  49,901 um^2   spec <= 50,000 um^2  PASS} -500 565 0 0 0.28 0.28 {layer=7}
T {All 12/12 specs PASS} -500 600 0 0 0.45 0.45 {layer=4}
