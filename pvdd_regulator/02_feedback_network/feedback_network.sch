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
T {BLOCK 02: FEEDBACK NETWORK} -800 -1100 0 0 1.2 1.2 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Resistive Voltage Divider} -800 -1000 0 0 0.5 0.5 {layer=8}
T {Device: sky130_fd_pr__res_xhigh_po   (P- polysilicon, ~2000 ohm/sq, low TC)} -800 -955 0 0 0.35 0.35 {}
T {.subckt feedback_network  pvdd  vfb  gnd} -800 -915 0 0 0.32 0.32 {layer=13}

* ================================================================
* PORT LIST
* ================================================================
T {PORTS} -800 -820 0 0 0.5 0.5 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -800 -760 0 0 {name=p1 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -680 -760 0 0 {name=p2 lab=vfb}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -680 -720 0 0 {name=p3 lab=gnd}

* ================================================================
* CIRCUIT: centered vertical divider
* PVDD at top -> XR_TOP -> VFB -> XR_BOT -> GND at bottom
* Uses PDK sky130_fd_pr__res_xhigh_po symbols
* ================================================================

* --- PVDD supply rail (top of divider) ---
T {PVDD} -130 -820 0 0 0.55 0.55 {layer=4}
T {5.0V regulated output} -130 -780 0 0 0.28 0.28 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -740 0 1 {name=l_pvdd sig_type=std_logic lab=pvdd}
N 0 -740 0 -640 {lab=pvdd}

* --- XR_TOP: top resistor of divider (pvdd to vfb) ---
T {XR_TOP} -280 -510 0 0 0.5 0.5 {layer=4}
T {sky130_fd_pr__res_xhigh_po} 100 -540 0 0 0.28 0.28 {layer=5}
T {W = 3.0 um   L = 536 um} 100 -505 0 0 0.28 0.28 {layer=5}
T {R ~ 365 kohm} 100 -470 0 0 0.35 0.35 {layer=7}
T {body = gnd} 100 -440 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 0 -500 0 0 {name=XR_TOP
W=3.0
L=536
model=res_xhigh_po
spiceprefix=X
mult=1
}
N 0 -640 0 -530 {lab=pvdd}
N 0 -470 0 -330 {lab=vfb}
N 20 -500 60 -500 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -500 2 0 {name=l_rb1 sig_type=std_logic lab=gnd}

* --- VFB node: feedback tap point (center of divider) ---
T {VFB = 1.226V} -280 -280 0 0 0.6 0.6 {layer=4}
T {ratio = R_BOT / (R_TOP + R_BOT) = 0.2452} -280 -235 0 0 0.28 0.28 {}
T {connects to error amp inverting input} -280 -205 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -280 2 0 {name=l_vfb sig_type=std_logic lab=vfb}
N 0 -330 0 -280 {lab=vfb}
N 0 -280 200 -280 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 200 -280 2 0 {name=l_vfb_out sig_type=std_logic lab=vfb}
T {vfb} 55 -295 0 0 0.35 0.35 {layer=8}

* --- XR_BOT: bottom resistor of divider (vfb to gnd) ---
T {XR_BOT} -280 -120 0 0 0.5 0.5 {layer=4}
T {sky130_fd_pr__res_xhigh_po} 100 -150 0 0 0.28 0.28 {layer=5}
T {W = 3.0 um   L = 174.30 um} 100 -115 0 0 0.28 0.28 {layer=5}
T {R ~ 118 kohm} 100 -80 0 0 0.35 0.35 {layer=7}
T {body = gnd} 100 -50 0 0 0.22 0.22 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 0 -110 0 0 {name=XR_BOT
W=3.0
L=174.30
model=res_xhigh_po
spiceprefix=X
mult=1
}
N 0 -280 0 -140 {lab=vfb}
N 0 -80 0 20 {lab=gnd}
N 20 -110 60 -110 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -110 2 0 {name=l_rb2 sig_type=std_logic lab=gnd}

* --- GND rail (bottom of divider) ---
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 20 0 0 {name=lg1 lab=GND}

* --- Current annotation ---
T {I_div = 10.35 uA} -200 -505 0 0 0.3 0.3 {layer=7}
T {|} -155 -460 0 0 0.35 0.35 {layer=7}
T {v} -155 -415 0 0 0.35 0.35 {layer=7}

* ================================================================
* DESIGN SUMMARY
* ================================================================

T {DESIGN SUMMARY} 500 -820 0 0 0.55 0.55 {layer=4}

T {Topology} 500 -750 0 0 0.4 0.4 {layer=8}
T {Two-resistor matched voltage divider} 500 -710 0 0 0.3 0.3 {}
T {Both R_TOP and R_BOT use sky130_fd_pr__res_xhigh_po} 500 -680 0 0 0.3 0.3 {}
T {Same width W=3.0 um for Pelgrom matching} 500 -650 0 0 0.3 0.3 {}

T {Resistance Values} 500 -580 0 0 0.4 0.4 {layer=8}
T {R_TOP      =  365 kohm    (L = 536 um)} 500 -540 0 0 0.3 0.3 {layer=7}
T {R_BOT      =  118 kohm    (L = 174.30 um)} 500 -510 0 0 0.3 0.3 {layer=7}
T {R_total    =  483 kohm} 500 -480 0 0 0.3 0.3 {}

T {Operating Point} 500 -410 0 0 0.4 0.4 {layer=8}
T {Ratio       =  0.24520} 500 -370 0 0 0.3 0.3 {layer=7}
T {VFB         =  5.0 x 0.24520  =  1.226V} 500 -340 0 0 0.3 0.3 {layer=7}
T {I_divider   =  10.35 uA} 500 -310 0 0 0.3 0.3 {layer=7}

* ================================================================
* TITLE FRAME
* ================================================================
C {/usr/share/xschem/xschem_library/devices/title.sym} -800 630 0 0 {name=l1 author="Block 02: Feedback Network -- Analog AI Chips PVDD LDO Regulator"}
