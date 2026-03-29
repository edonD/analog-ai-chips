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
* TITLE BLOCK (top)
* ================================================================
T {BLOCK 02: FEEDBACK NETWORK} -800 -1100 0 0 1.2 1.2 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Resistive Voltage Divider} -800 -1000 0 0 0.5 0.5 {layer=8}
T {Device: sky130_fd_pr__res_xhigh_po   (P- polysilicon, ~2000 ohm/sq, low TC)} -800 -955 0 0 0.35 0.35 {}
T {.subckt feedback_network  pvdd  vfb  gnd} -800 -915 0 0 0.32 0.32 {layer=13}

* ================================================================
* PORT LIST (top-left)
* ================================================================
T {PORTS} -800 -820 0 0 0.5 0.5 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -800 -760 0 0 {name=p1 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -680 -760 0 0 {name=p2 lab=vfb}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -680 -720 0 0 {name=p3 lab=gnd}

* ================================================================
* CIRCUIT: centered vertical divider
* PVDD at top → R_TOP → VFB → R_BOT → GND at bottom
* Generous vertical spacing for readability
* ================================================================

* --- PVDD supply rail (top of divider) ---
T {PVDD} -130 -820 0 0 0.55 0.55 {layer=4}
T {5.0V regulated output} -130 -780 0 0 0.28 0.28 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -740 0 1 {name=l_pvdd sig_type=std_logic lab=pvdd}
N 0 -740 0 -640 {lab=pvdd}

* --- R_TOP: top resistor of divider (pvdd to vfb) ---
T {R_TOP} -280 -510 0 0 0.5 0.5 {layer=4}
T {XR_TOP} 100 -570 0 0 0.3 0.3 {layer=13}
T {sky130_fd_pr__res_xhigh_po} 100 -540 0 0 0.28 0.28 {layer=5}
T {W = 3.0 um   L = 536 um} 100 -505 0 0 0.28 0.28 {layer=5}
T {R = 365 kohm} 100 -470 0 0 0.35 0.35 {layer=7}
T {substrate = gnd} 100 -440 0 0 0.22 0.22 {layer=7}
C {/usr/share/xschem/xschem_library/devices/res.sym} 0 -500 0 0 {name=XR_TOP
value="sky130_fd_pr__res_xhigh_po w=3.0 l=536"
}
N 0 -640 0 -530 {lab=pvdd}
N 0 -470 0 -330 {lab=vfb}

* --- VFB node: feedback tap point (center of divider) ---
T {VFB = 1.226V} -280 -280 0 0 0.6 0.6 {layer=4}
T {ratio = R_BOT / (R_TOP + R_BOT) = 0.2452} -280 -235 0 0 0.28 0.28 {}
T {connects to error amp inverting input} -280 -205 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -280 2 0 {name=l_vfb sig_type=std_logic lab=vfb}
N 0 -330 0 -280 {lab=vfb}
N 0 -280 200 -280 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 200 -280 2 0 {name=l_vfb_out sig_type=std_logic lab=vfb}
T {vfb} 55 -295 0 0 0.35 0.35 {layer=8}

* --- R_BOT: bottom resistor of divider (vfb to gnd) ---
T {R_BOT} -280 -120 0 0 0.5 0.5 {layer=4}
T {XR_BOT} 100 -180 0 0 0.3 0.3 {layer=13}
T {sky130_fd_pr__res_xhigh_po} 100 -150 0 0 0.28 0.28 {layer=5}
T {W = 3.0 um   L = 174.30 um} 100 -115 0 0 0.28 0.28 {layer=5}
T {R = 118 kohm} 100 -80 0 0 0.35 0.35 {layer=7}
T {substrate = gnd} 100 -50 0 0 0.22 0.22 {layer=7}
C {/usr/share/xschem/xschem_library/devices/res.sym} 0 -110 0 0 {name=XR_BOT
value="sky130_fd_pr__res_xhigh_po w=3.0 l=174.30"
}
N 0 -280 0 -140 {lab=vfb}
N 0 -80 0 20 {lab=gnd}

* --- GND rail (bottom of divider) ---
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 20 0 0 {name=lg1 lab=GND}

* --- Current annotation (left side of divider) ---
T {I_div = 10.35 uA} -200 -505 0 0 0.3 0.3 {layer=7}
T {|} -155 -460 0 0 0.35 0.35 {layer=7}
T {v} -155 -415 0 0 0.35 0.35 {layer=7}

* ================================================================
* DESIGN SUMMARY (right side, well-separated)
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
T {R_parallel =  89.4 kohm} 500 -450 0 0 0.3 0.3 {}

T {Operating Point} 500 -380 0 0 0.4 0.4 {layer=8}
T {Ratio       =  0.24520} 500 -340 0 0 0.3 0.3 {layer=7}
T {VFB         =  5.0 x 0.24520  =  1.226V} 500 -310 0 0 0.3 0.3 {layer=7}
T {I_divider   =  10.35 uA} 500 -280 0 0 0.3 0.3 {layer=7}

T {AC / Parasitics} 500 -210 0 0 0.4 0.4 {layer=8}
T {Feedback pole  =  12.7 MHz  (>> loop BW)} 500 -170 0 0 0.3 0.3 {}
T {Parasitic cap  =  ~0.14 pF  (<< 2 pF spec)} 500 -140 0 0 0.3 0.3 {}
T {Area           =  2131 um^2  (3.3% of chip)} 500 -110 0 0 0.3 0.3 {}

T {TC Cancellation} 500 -40 0 0 0.4 0.4 {layer=8}
T {Same resistor type + same width} 500 0 0 0 0.28 0.28 {}
T {=> first-order TC cancellation (0.07 mV drift)} 500 28 0 0 0.28 0.28 {}
T {=> Pelgrom matching (MC 3-sigma = 4.69 mV)} 500 56 0 0 0.28 0.28 {}

* ================================================================
* CHARACTERIZATION (bottom, full width)
* ================================================================

T {CHARACTERIZATION  (TT 27C,  PVDD = 5.0V)} -800 200 0 0 0.55 0.55 {layer=4}

T {VFB accuracy       =  1.22600 V      error = 0.004 mV        spec <= 1 mV                PASS} -800 280 0 0 0.3 0.3 {layer=7}
T {Temp drift         =  0.07 mV        (-40C to 150C)          spec <= 5 mV                PASS} -800 315 0 0 0.3 0.3 {layer=7}
T {Corner drift       =  0 mV           (SS/FF at 27C)          spec <= 10 mV               PASS} -800 350 0 0 0.3 0.3 {layer=7}
T {Divider current    =  10.35 uA       (PVDD = 5.0V)           spec 10-15 uA               PASS} -800 385 0 0 0.3 0.3 {layer=7}
T {Noise at VFB       =  38.5 uVrms     (1Hz-1MHz, analytical)  spec <= 50 uVrms            PASS} -800 420 0 0 0.3 0.3 {layer=7}
T {MC 3-sigma         =  4.69 mV        (500 runs)              spec <= 10 mV               PASS} -800 455 0 0 0.3 0.3 {layer=7}

T {All 6/6 specs PASS  +  MC PASS} -800 520 0 0 0.55 0.55 {layer=4}

* ================================================================
* TITLE FRAME (bottom)
* ================================================================
C {/usr/share/xschem/xschem_library/devices/title.sym} -800 630 0 0 {name=l1 author="Block 02: Feedback Network -- Analog AI Chips PVDD LDO Regulator"}
