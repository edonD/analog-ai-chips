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
T {10/11 specs pass | Leakage 0.66uA | Peak inrush 5.9mA} -650 -875 0 0 0.25 0.25 {layer=5}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -760 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -730 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -700 0 0 {name=p3 lab=vref}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -760 0 0 {name=p4 lab=gate}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -730 0 0 {name=p5 lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -560 -700 0 0 {name=p6 lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -670 0 0 {name=p7 lab=gnd}

T {PVDD THRESHOLD} -450 -550 0 0 0.5 0.5 {layer=4}
T {DETECTOR} -450 -520 0 0 0.5 0.5 {layer=4}
T {GATE PULLDOWN} 100 -550 0 0 0.5 0.5 {layer=4}
T {OUTPUT FLAGS} 500 -550 0 0 0.5 0.5 {layer=4}

C {/usr/share/xschem/xschem_library/devices/title.sym} -650 830 0 0 {name=l1 author="Block 09: Startup Circuit -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* PVDD Threshold Detector
* ================================================================

* XR_top: 4.1M resistor from PVDD to sense_mid
T {XR_top} -430 -400 0 0 0.25 0.25 {layer=13}
T {4.1M (W=2 L=4100)} -430 -380 0 0 0.2 0.2 {layer=5}

* XR_bot: 900k resistor from sense_mid to GND
T {XR_bot} -430 -250 0 0 0.25 0.25 {layer=13}
T {900k (W=2 L=900)} -430 -230 0 0 0.2 0.2 {layer=5}

* MN_det: detection NMOS
T {MN_det} -290 -250 0 0 0.25 0.25 {layer=13}
T {W=10 L=1} -290 -230 0 0 0.2 0.2 {layer=5}

* XR_pu: 10M pull-up resistor
T {XR_pu} -130 -400 0 0 0.25 0.25 {layer=13}
T {10M (W=1 L=5001)} -130 -380 0 0 0.2 0.2 {layer=5}

* Connection labels
N -400 -450 -400 -420 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -400 -450 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}
N -400 -360 -400 -270 {lab=sense_mid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -350 -310 0 0 {name=l_sm sig_type=std_logic lab=sense_mid}
N -400 -210 -400 -170 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -400 -170 2 1 {name=l_g1 sig_type=std_logic lab=gnd}

N -260 -310 -260 -270 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -260 -310 2 0 {name=l_do sig_type=std_logic lab=det_out}
N -260 -210 -260 -170 {lab=gnd}

N -100 -450 -100 -420 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -450 2 0 {name=l_bv1 sig_type=std_logic lab=bvdd}
N -100 -360 -100 -310 {lab=det_out}

* ================================================================
* Gate Pulldown
* ================================================================

T {XR_gate} 120 -400 0 0 0.25 0.25 {layer=13}
T {102k (W=1 L=51)} 120 -380 0 0 0.2 0.2 {layer=5}

T {MN_gate} 120 -250 0 0 0.25 0.25 {layer=13}
T {W=5 L=1} 120 -230 0 0 0.2 0.2 {layer=5}

N 150 -450 150 -420 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -450 2 0 {name=l_gate sig_type=std_logic lab=gate}
N 150 -360 150 -270 {lab=pull_mid}
N 150 -210 150 -170 {lab=gnd}
N 80 -240 80 -240 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 80 -240 0 1 {name=l_do2 sig_type=std_logic lab=det_out}

* ================================================================
* MN_pu: Regulation assist
* ================================================================

T {MN_pu} 320 -400 0 0 0.25 0.25 {layer=13}
T {W=0.42 L=8} 320 -380 0 0 0.2 0.2 {layer=5}
T {Source follower} 320 -360 0 0 0.18 0.18 {layer=8}
T {bvdd-domain} 320 -345 0 0 0.18 0.18 {layer=8}
T {regulation assist} 320 -330 0 0 0.18 0.18 {layer=8}

N 350 -450 350 -420 {lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 350 -450 2 0 {name=l_bv3 sig_type=std_logic lab=bvdd}
N 350 -280 350 -250 {lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 350 -250 2 1 {name=l_gate2 sig_type=std_logic lab=gate}

* ================================================================
* Output Inverters
* ================================================================

T {INV: startup_done} 530 -450 0 0 0.25 0.25 {layer=13}
T {MP W=4 L=1} 530 -430 0 0 0.18 0.18 {layer=5}
T {MN W=2 L=1} 530 -415 0 0 0.18 0.18 {layer=5}

T {INV: ea_en} 530 -320 0 0 0.25 0.25 {layer=13}
T {MP W=4 L=1} 530 -300 0 0 0.18 0.18 {layer=5}
T {MN W=2 L=1} 530 -285 0 0 0.18 0.18 {layer=5}

N 500 -400 500 -400 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -400 0 1 {name=l_do3 sig_type=std_logic lab=det_out}
N 600 -400 650 -400 {lab=startup_done}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 -400 0 0 {name=l_sd sig_type=std_logic lab=startup_done}

N 500 -270 500 -270 {lab=det_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -270 0 1 {name=l_do4 sig_type=std_logic lab=det_out}
N 600 -270 650 -270 {lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 -270 0 0 {name=l_ea sig_type=std_logic lab=ea_en}
