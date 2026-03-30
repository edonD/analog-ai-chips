v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {RESISTOR LADDER} -200 -1200 0 0 1.0 1.0 {layer=4}
T {Block 08 — Mode Control — Sub-block 1 of 3} -200 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Resistor Divider} -200 -1095 0 0 0.3 0.3 {}
T {5 resistors: res_xhigh_po  |  Total ~400kOhm  |  Iq ~17.5uA @ 7V} -200 -1065 0 0 0.28 0.28 {layer=13}

* ================================================================
* PORT PINS
* ================================================================
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -200 -950 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -80 -950 0 0 {name=p2 lab=tap1}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -80 -920 0 0 {name=p3 lab=tap2}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -80 -890 0 0 {name=p4 lab=tap3}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -80 -860 0 0 {name=p5 lab=tap4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -80 -830 0 0 {name=p6 lab=gnd}

C {/usr/share/xschem/xschem_library/devices/title.sym} -200 600 0 0 {name=l1 author="Block 08 Sub-1: Resistor Ladder -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* CHARACTERIZATION
* ================================================================
T {Resistance Values (res_xhigh_po, ~2.08 kOhm/sq):} 200 -1200 0 0 0.35 0.35 {layer=4}
T {XRtop:  w=1 l=37  ~77 kOhm} 200 -1160 0 0 0.3 0.3 {layer=7}
T {XR12:   w=1 l=62  ~129 kOhm} 200 -1130 0 0 0.3 0.3 {layer=7}
T {XR23:   w=1 l=6   ~12.5 kOhm} 200 -1100 0 0 0.3 0.3 {layer=7}
T {XR34:   w=1 l=17  ~35 kOhm} 200 -1070 0 0 0.3 0.3 {layer=7}
T {XRbot:  w=1 l=69  ~143 kOhm} 200 -1040 0 0 0.3 0.3 {layer=7}
T {Total: ~397 kOhm  |  Iq = BVDD/Rtotal} 200 -1000 0 0 0.3 0.3 {layer=7}
T {Thresholds (BVDD):} 200 -960 0 0 0.35 0.35 {layer=4}
T {tap1: TH1 = 2.51V  (comp1 trips -> pass_off)} 200 -920 0 0 0.3 0.3 {layer=7}
T {tap2: TH2 = 4.16V  (comp2 trips -> ea_en, bypass_en)} 200 -890 0 0 0.3 0.3 {layer=7}
T {tap3: TH3 = 4.47V  (comp3 trips -> ref_sel, ea_en, bypass_en)} 200 -860 0 0 0.3 0.3 {layer=7}
T {tap4: TH4 = 5.60V  (comp4 trips -> uvov_en, ilim_en, bypass_en, ea_en)} 200 -830 0 0 0.3 0.3 {layer=7}

* ================================================================
* RESISTOR CHAIN — Vertical: BVDD (top) to GND (bottom)
* ================================================================

* --- BVDD supply at top ---
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -800 2 0 {name=l_bvdd sig_type=std_logic lab=bvdd}
N 0 -800 0 -770 {lab=bvdd}
T {BVDD (battery)} 10 -795 0 0 0.35 0.35 {layer=8}

* --- XRtop: bvdd to tap1, l=37 (~77k) ---
T {XRtop} -80 -730 0 0 0.3 0.3 {layer=13}
T {w=1 l=37  (~77 kOhm)} -80 -705 0 0 0.22 0.22 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 0 -700 0 0 {name=XRtop
W=1
L=37
model=res_xhigh_po
spiceprefix=X
mult=1}
N 0 -730 0 -770 {lab=bvdd}
N 0 -670 0 -600 {lab=tap1}
N 20 -700 40 -700 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -700 2 0 {name=l_grt sig_type=std_logic lab=gnd}

* --- tap1 node ---
T {tap1  (TH1=2.51V)} 10 -605 0 0 0.35 0.35 {layer=8}
N 0 -600 100 -600 {lab=tap1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -600 2 0 {name=l_tap1 sig_type=std_logic lab=tap1}

* --- XR12: tap1 to tap2, l=62 (~129k) ---
T {XR12} -80 -530 0 0 0.3 0.3 {layer=13}
T {w=1 l=62  (~129 kOhm)} -80 -505 0 0 0.22 0.22 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 0 -500 0 0 {name=XR12
W=1
L=62
model=res_xhigh_po
spiceprefix=X
mult=1}
N 0 -530 0 -600 {lab=tap1}
N 0 -470 0 -400 {lab=tap2}
N 20 -500 40 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -500 2 0 {name=l_gr12 sig_type=std_logic lab=gnd}

* --- tap2 node ---
T {tap2  (TH2=4.16V)} 10 -405 0 0 0.35 0.35 {layer=8}
N 0 -400 100 -400 {lab=tap2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -400 2 0 {name=l_tap2 sig_type=std_logic lab=tap2}

* --- XR23: tap2 to tap3, l=6 (~12.5k) ---
T {XR23} -80 -330 0 0 0.3 0.3 {layer=13}
T {w=1 l=6  (~12.5 kOhm)} -80 -305 0 0 0.22 0.22 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 0 -300 0 0 {name=XR23
W=1
L=6
model=res_xhigh_po
spiceprefix=X
mult=1}
N 0 -330 0 -400 {lab=tap2}
N 0 -270 0 -200 {lab=tap3}
N 20 -300 40 -300 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -300 2 0 {name=l_gr23 sig_type=std_logic lab=gnd}

* --- tap3 node ---
T {tap3  (TH3=4.47V)} 10 -205 0 0 0.35 0.35 {layer=8}
N 0 -200 100 -200 {lab=tap3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -200 2 0 {name=l_tap3 sig_type=std_logic lab=tap3}

* --- XR34: tap3 to tap4, l=17 (~35k) ---
T {XR34} -80 -130 0 0 0.3 0.3 {layer=13}
T {w=1 l=17  (~35 kOhm)} -80 -105 0 0 0.22 0.22 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 0 -100 0 0 {name=XR34
W=1
L=17
model=res_xhigh_po
spiceprefix=X
mult=1}
N 0 -130 0 -200 {lab=tap3}
N 0 -70 0 0 {lab=tap4}
N 20 -100 40 -100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -100 2 0 {name=l_gr34 sig_type=std_logic lab=gnd}

* --- tap4 node ---
T {tap4  (TH4=5.60V)} 10 -5 0 0 0.35 0.35 {layer=8}
N 0 0 100 0 {lab=tap4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 0 2 0 {name=l_tap4 sig_type=std_logic lab=tap4}

* --- XRbot: tap4 to gnd, l=69 (~143k) ---
T {XRbot} -80 70 0 0 0.3 0.3 {layer=13}
T {w=1 l=69  (~143 kOhm)} -80 95 0 0 0.22 0.22 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 0 100 0 0 {name=XRbot
W=1
L=69
model=res_xhigh_po
spiceprefix=X
mult=1}
N 0 70 0 0 {lab=tap4}
N 0 130 0 180 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 180 0 0 {name=lg_bot lab=GND}
N 20 100 40 100 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 100 2 0 {name=l_grbot sig_type=std_logic lab=gnd}
