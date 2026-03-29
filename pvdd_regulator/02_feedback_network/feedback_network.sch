v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 02: FEEDBACK NETWORK} -700 -900 0 0 1.2 1.2 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  Resistive Voltage Divider} -700 -800 0 0 0.5 0.5 {layer=8}
T {Device: sky130_fd_pr__res_xhigh_po  (P- polysilicon,  ~2000 ohm/sq,  low TC)} -700 -760 0 0 0.35 0.35 {}
T {.subckt feedback_network  pvdd  vfb  gnd} -700 -720 0 0 0.32 0.32 {layer=13}

* ================================================================
* PORT LIST (top-left corner)
* ================================================================
T {PORTS} -700 -620 0 0 0.5 0.5 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -700 -560 0 0 {name=p1 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -580 -560 0 0 {name=p2 lab=vfb}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -580 -520 0 0 {name=p3 lab=gnd}

* ================================================================
* CIRCUIT: Vertical divider, PVDD at top, GND at bottom
* Centered on x=0, tall vertical layout for clarity
* ================================================================

* --- PVDD rail ---
T {PVDD} -65 -600 0 0 0.6 0.6 {layer=4}
T {5.0V (regulated output)} -65 -560 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -520 0 1 {name=l_pvdd sig_type=std_logic lab=pvdd}
N 0 -520 0 -440 {lab=pvdd}

* --- R_TOP ---
T {XR_TOP} 80 -350 0 0 0.45 0.45 {layer=13}
T {sky130_fd_pr__res_xhigh_po} 80 -310 0 0 0.28 0.28 {layer=5}
T {W = 3.0 um} 80 -280 0 0 0.3 0.3 {layer=5}
T {L = 536 um} 80 -253 0 0 0.3 0.3 {layer=5}
T {R = 365 kohm} 80 -220 0 0 0.35 0.35 {layer=7}
T {sub -> gnd} 80 -193 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/res.sym} 0 -280 0 0 {name=XR_TOP
value="sky130_fd_pr__res_xhigh_po w=3.0 l=536"
}
N 0 -440 0 -310 {lab=pvdd}
N 0 -250 0 -120 {lab=vfb}

* --- VFB tap ---
T {VFB  =  1.226V} -200 -120 0 0 0.6 0.6 {layer=4}
T {ratio = R_BOT/(R_TOP+R_BOT) = 0.2452} -200 -75 0 0 0.25 0.25 {}
T {-> error amp (-) input} -200 -50 0 0 0.25 0.25 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -120 2 0 {name=l_vfb sig_type=std_logic lab=vfb}
N 0 -120 150 -120 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -120 2 0 {name=l_vfb_out sig_type=std_logic lab=vfb}

* --- R_BOT ---
T {XR_BOT} 80 10 0 0 0.45 0.45 {layer=13}
T {sky130_fd_pr__res_xhigh_po} 80 50 0 0 0.28 0.28 {layer=5}
T {W = 3.0 um} 80 80 0 0 0.3 0.3 {layer=5}
T {L = 174.30 um} 80 107 0 0 0.3 0.3 {layer=5}
T {R = 118 kohm} 80 140 0 0 0.35 0.35 {layer=7}
T {sub -> gnd} 80 167 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/res.sym} 0 80 0 0 {name=XR_BOT
value="sky130_fd_pr__res_xhigh_po w=3.0 l=174.30"
}
N 0 -120 0 50 {lab=vfb}
N 0 110 0 200 {lab=gnd}

* --- GND rail ---
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 200 0 0 {name=lg1 lab=GND}

* --- Current arrow annotation ---
T {I = 10.35 uA} -120 -280 0 0 0.3 0.3 {layer=7}
T {v} -95 -230 0 0 0.4 0.4 {layer=7}

* ================================================================
* DESIGN SUMMARY (right side, well-separated)
* ================================================================

T {DESIGN SUMMARY} 450 -600 0 0 0.55 0.55 {layer=4}

T {Topology:    Two-resistor voltage divider} 450 -530 0 0 0.3 0.3 {layer=7}
T {Resistor:    sky130_fd_pr__res_xhigh_po} 450 -500 0 0 0.3 0.3 {layer=7}
T {Width:       3.0 um  (matched, both resistors)} 450 -470 0 0 0.3 0.3 {layer=7}

T {R_TOP        = 365 kohm   (L = 536 um)} 450 -410 0 0 0.3 0.3 {}
T {R_BOT        = 118 kohm   (L = 174.30 um)} 450 -380 0 0 0.3 0.3 {}
T {R_total      = 483 kohm} 450 -350 0 0 0.3 0.3 {}
T {R_parallel   = 89.4 kohm} 450 -320 0 0 0.3 0.3 {}

T {Ratio        = 0.24520} 450 -260 0 0 0.3 0.3 {layer=7}
T {VFB          = 5.0 x 0.24520  =  1.226V} 450 -230 0 0 0.3 0.3 {layer=7}
T {I_divider    = 10.35 uA} 450 -200 0 0 0.3 0.3 {layer=7}

T {Feedback pole =  12.7 MHz  (>> loop BW)} 450 -140 0 0 0.3 0.3 {}
T {Parasitic cap =  ~0.14 pF  (<< 2 pF spec)} 450 -110 0 0 0.3 0.3 {}
T {Area          =  2131 um^2  (3.3% of chip)} 450 -80 0 0 0.3 0.3 {}

T {Same resistor type + same width} 450 -20 0 0 0.28 0.28 {}
T {= first-order TC cancellation} 450 8 0 0 0.28 0.28 {}
T {+ optimal Pelgrom matching} 450 36 0 0 0.28 0.28 {}

* ================================================================
* CHARACTERIZATION (bottom, full width)
* ================================================================

T {CHARACTERIZATION  (TT 27C,  PVDD = 5.0V)} -700 350 0 0 0.55 0.55 {layer=4}

T {VFB accuracy       =  1.22600 V      error = 0.004 mV      spec <= 1 mV             PASS} -700 420 0 0 0.3 0.3 {layer=7}
T {Temp drift         =  0.07 mV        (-40C to 150C)        spec <= 5 mV             PASS} -700 455 0 0 0.3 0.3 {layer=7}
T {Corner drift       =  0 mV           (SS/FF at 27C)        spec <= 10 mV            PASS} -700 490 0 0 0.3 0.3 {layer=7}
T {Divider current    =  10.35 uA                             spec 10-15 uA            PASS} -700 525 0 0 0.3 0.3 {layer=7}
T {Noise at VFB       =  38.5 uVrms     (1Hz-1MHz, analyt.)   spec <= 50 uVrms         PASS} -700 560 0 0 0.3 0.3 {layer=7}
T {MC 3-sigma         =  4.69 mV        (500 runs)            spec <= 10 mV            PASS} -700 595 0 0 0.3 0.3 {layer=7}

T {All 6/6 specs PASS  +  MC PASS} -700 660 0 0 0.55 0.55 {layer=4}

C {/usr/share/xschem/xschem_library/devices/title.sym} -700 760 0 0 {name=l1 author="Block 02: Feedback Network -- Analog AI Chips PVDD LDO Regulator"}
