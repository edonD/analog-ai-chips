v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 05: UV COMPARATOR} -650 -1050 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A  |  NMOS Diff Pair + PMOS Mirror Load} -650 -970 0 0 0.45 0.45 {layer=8}
T {Core: 1.8V MOSFETs (nfet_01v8, pfet_01v8)  |  Supply: vdd_comp = 1.8V} -650 -935 0 0 0.3 0.3 {}
T {Threshold: PVDD < 4.3V → uv_flag = HIGH} -650 -905 0 0 0.3 0.3 {layer=5}
T {.subckt uv_comparator  pvdd  vref  uv_flag  vdd_comp  gnd  en} -650 -875 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -760 0 0 {name=p1 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -730 0 0 {name=p2 lab=vref}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -650 -700 0 0 {name=p3 lab=en}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -760 0 0 {name=p4 lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -560 -730 0 0 {name=p5 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -470 -760 0 0 {name=p6 lab=uv_flag}

T {RESISTIVE DIVIDER} -520 -830 0 0 0.5 0.5 {layer=4}
T {BIAS} -50 -830 0 0 0.5 0.5 {layer=4}
T {DIFF PAIR + MIRROR LOAD} 300 -830 0 0 0.5 0.5 {layer=4}
T {ENABLE + NOR OUTPUT} 850 -830 0 0 0.5 0.5 {layer=4}

C {/usr/share/xschem/xschem_library/devices/title.sym} -650 830 0 0 {name=l1 author="Block 05: UV Comparator -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* RESISTIVE DIVIDER: XR_top (pvdd → mid_uv) + XR_bot (mid_uv → gnd)
* ratio = 199.4/(500+199.4) = 0.28514 → trip at 4.299V
* ================================================================

* --- XR_top: Top divider resistor (W=2 L=500) ---
T {XR_top} -580 -660 0 0 0.25 0.25 {layer=13}
T {W=2 L=500} -580 -638 0 0 0.2 0.2 {layer=5}
T {~500k} -580 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -490 -640 0 0 {name=XR_top
W=2
L=500
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -490 -670 -490 -760 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -490 -760 2 0 {name=l_pv1 sig_type=std_logic lab=pvdd}
N -490 -610 -490 -530 {lab=mid_uv}
N -510 -640 -560 -640 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -560 -640 0 0 {name=l_gn1 sig_type=std_logic lab=gnd}
T {mid_uv} -485 -535 0 0 0.3 0.3 {layer=8}

* --- XR_bot: Bottom divider resistor (W=2 L=199.4) ---
T {XR_bot} -580 -370 0 0 0.25 0.25 {layer=13}
T {W=2 L=199.4} -580 -348 0 0 0.2 0.2 {layer=5}
T {~199.4k} -580 -326 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -490 -430 0 0 {name=XR_bot
W=2
L=199.4
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -490 -460 -490 -530 {lab=mid_uv}
N -490 -400 -490 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -490 -280 0 0 {name=lg1 lab=GND}
N -510 -430 -560 -430 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -560 -430 0 0 {name=l_gn2 sig_type=std_logic lab=gnd}

* --- XR_hyst: Hysteresis resistor (W=1 L=1250, out_n → mid_uv) ---
T {XR_hyst} -320 -660 0 0 0.25 0.25 {layer=13}
T {W=1 L=1250} -320 -638 0 0 0.2 0.2 {layer=5}
T {~2.5M hyst} -320 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -310 -540 0 0 {name=XR_hyst
W=1
L=1250
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -310 -570 -310 -600 {lab=out_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -310 -600 2 0 {name=l_on1 sig_type=std_logic lab=out_n}
N -310 -510 -310 -480 {lab=mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -310 -480 0 0 {name=l_mu1 sig_type=std_logic lab=mid_uv}
N -330 -540 -380 -540 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -380 -540 0 0 {name=l_gn3 sig_type=std_logic lab=gnd}

* ================================================================
* BIAS: XR_bias (vdd_comp → bias_n) + XMbias (diode NMOS)
* ================================================================

* --- XR_bias: Bias resistor (W=2 L=800) ---
T {XR_bias} -110 -660 0 0 0.25 0.25 {layer=13}
T {W=2 L=800} -110 -638 0 0 0.2 0.2 {layer=5}
T {~800k} -110 -616 0 0 0.18 0.18 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -20 -640 0 0 {name=XR_bias
W=2
L=800
model=res_xhigh_po
spiceprefix=X
mult=1
}
N -20 -670 -20 -760 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -20 -760 2 0 {name=l_vc1 sig_type=std_logic lab=vdd_comp}
N -20 -610 -20 -530 {lab=bias_n}
N -40 -640 -90 -640 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -90 -640 0 0 {name=l_gn4 sig_type=std_logic lab=gnd}
T {bias_n} -15 -535 0 0 0.3 0.3 {layer=8}

* --- XMbias: Diode-connected NMOS (W=1u L=4u) ---
T {XMbias} -110 -340 0 0 0.25 0.25 {layer=13}
T {W=1u L=4u} -110 -318 0 0 0.2 0.2 {layer=5}
T {~1uA diode} -110 -296 0 0 0.18 0.18 {}
T {B=GND} 0 -385 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -40 -420 0 0 {name=XMbias
L=4u
W=1u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N -20 -450 -20 -530 {lab=bias_n}
N -20 -390 -20 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} -20 -280 0 0 {name=lg2 lab=GND}
N -60 -420 -120 -420 {lab=bias_n}
N -120 -420 -120 -530 {lab=bias_n}
N -120 -530 -20 -530 {lab=bias_n}

* ================================================================
* TAIL CURRENT SOURCE: XMtail (mirrors bias)
* ================================================================

* --- XMtail: Tail NMOS (W=1u L=4u) ---
T {XMtail} 180 -160 0 0 0.25 0.25 {layer=13}
T {W=1u L=4u} 180 -138 0 0 0.2 0.2 {layer=5}
T {B=GND} 300 -205 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 260 -240 0 0 {name=XMtail
L=4u
W=1u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 280 -270 280 -330 {lab=tail}
N 280 -210 280 -120 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 280 -120 0 0 {name=lg3 lab=GND}
N 240 -240 170 -240 {lab=bias_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 170 -240 0 0 {name=l_bn1 sig_type=std_logic lab=bias_n}
T {tail} 285 -335 0 0 0.3 0.3 {layer=13}

* ================================================================
* NMOS DIFFERENTIAL PAIR: XM1 (mid_uv) + XM2 (vref)
* ================================================================

* --- XM1: Diff pair left (W=2u L=1u, gate=mid_uv) ---
T {XM1} 180 -360 0 0 0.25 0.25 {layer=13}
T {W=2u L=1u} 180 -338 0 0 0.2 0.2 {layer=5}
T {B=GND} 300 -405 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 260 -440 0 0 {name=XM1
L=1u
W=2u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 280 -470 280 -560 {lab=out_p}
N 280 -410 280 -330 {lab=tail}
N 240 -440 170 -440 {lab=mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 170 -440 0 0 {name=l_mu2 sig_type=std_logic lab=mid_uv}
T {out_p} 285 -565 0 0 0.3 0.3 {layer=8}

* --- XM2: Diff pair right (W=2u L=1u, gate=vref) ---
T {XM2} 450 -360 0 0 0.25 0.25 {layer=13}
T {W=2u L=1u} 450 -338 0 0 0.2 0.2 {layer=5}
T {B=GND} 570 -405 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 530 -440 0 0 {name=XM2
L=1u
W=2u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 550 -470 550 -560 {lab=out_n}
N 550 -410 550 -330 {lab=tail}
N 510 -440 440 -440 {lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 440 -440 0 0 {name=l_vr1 sig_type=std_logic lab=vref}
T {out_n} 555 -565 0 0 0.3 0.3 {layer=8}

* --- Tail connection ---
N 280 -330 550 -330 {lab=tail}

* ================================================================
* PMOS CURRENT MIRROR LOAD: XM3 (diode) + XM4 (mirror)
* ================================================================

* --- XM3: Mirror diode left (W=2u L=1u) ---
T {XM3} 180 -660 0 0 0.25 0.25 {layer=13}
T {W=2u L=1u} 180 -638 0 0 0.2 0.2 {layer=5}
T {B=vdd_comp} 300 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 260 -680 0 0 {name=XM3
L=1u
W=2u
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
N 280 -710 280 -760 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 280 -760 2 0 {name=l_vc2 sig_type=std_logic lab=vdd_comp}
N 280 -650 280 -560 {lab=out_p}
N 240 -680 200 -680 {lab=out_p}
N 200 -680 200 -560 {lab=out_p}
N 200 -560 280 -560 {lab=out_p}

* --- XM4: Mirror output right (W=2u L=1u) ---
T {XM4} 450 -660 0 0 0.25 0.25 {layer=13}
T {W=2u L=1u} 450 -638 0 0 0.2 0.2 {layer=5}
T {B=vdd_comp} 570 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 530 -680 0 0 {name=XM4
L=1u
W=2u
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
N 550 -710 550 -760 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 -760 2 0 {name=l_vc3 sig_type=std_logic lab=vdd_comp}
N 550 -650 550 -560 {lab=out_n}
N 510 -680 200 -680 {lab=out_p}

* ================================================================
* ENABLE INVERTER: XMen_n + XMen_p
* en → en_bar
* ================================================================

* --- XMen_p: Enable PMOS (W=0.84u L=0.15u) ---
T {XMen_p} 800 -660 0 0 0.25 0.25 {layer=13}
T {W=0.84u L=0.15u} 800 -638 0 0 0.2 0.2 {layer=5}
T {B=vdd_comp} 920 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 880 -680 0 0 {name=XMen_p
L=0.15u
W=0.84u
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
N 900 -710 900 -760 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 900 -760 2 0 {name=l_vc4 sig_type=std_logic lab=vdd_comp}
N 900 -650 900 -560 {lab=en_bar}
N 860 -680 790 -680 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 790 -680 0 0 {name=l_en1 sig_type=std_logic lab=en}

* --- XMen_n: Enable NMOS (W=0.42u L=0.15u) ---
T {XMen_n} 800 -340 0 0 0.25 0.25 {layer=13}
T {W=0.42u L=0.15u} 800 -318 0 0 0.2 0.2 {layer=5}
T {B=GND} 920 -385 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 880 -420 0 0 {name=XMen_n
L=0.15u
W=0.42u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 900 -450 900 -560 {lab=en_bar}
N 900 -390 900 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 900 -280 0 0 {name=lg4 lab=GND}
N 860 -420 790 -420 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 790 -420 0 0 {name=l_en2 sig_type=std_logic lab=en}
T {en_bar} 905 -565 0 0 0.3 0.3 {layer=13}

* ================================================================
* NOR OUTPUT GATE: uv_flag = NOR(out_n, en_bar)
* PMOS in series (both OFF for HIGH), NMOS in parallel (either ON for LOW)
* ================================================================

* --- XMnor_p1: NOR PMOS top (W=4u L=0.15u, gate=out_n) ---
T {XMnor_p1} 1050 -660 0 0 0.25 0.25 {layer=13}
T {W=4u L=0.15u} 1050 -638 0 0 0.2 0.2 {layer=5}
T {B=vdd_comp} 1170 -710 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1130 -680 0 0 {name=XMnor_p1
L=0.15u
W=4u
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
N 1150 -710 1150 -760 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -760 2 0 {name=l_vc5 sig_type=std_logic lab=vdd_comp}
N 1150 -650 1150 -600 {lab=nor_mid}
N 1110 -680 1040 -680 {lab=out_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1040 -680 0 0 {name=l_on2 sig_type=std_logic lab=out_n}
T {nor_mid} 1155 -605 0 0 0.25 0.25 {layer=13}

* --- XMnor_p2: NOR PMOS bottom (W=4u L=0.15u, gate=en_bar, B=nor_mid) ---
T {XMnor_p2} 1050 -480 0 0 0.25 0.25 {layer=13}
T {W=4u L=0.15u} 1050 -458 0 0 0.2 0.2 {layer=5}
T {B=nor_mid} 1170 -530 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1130 -500 0 0 {name=XMnor_p2
L=0.15u
W=4u
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
N 1150 -530 1150 -600 {lab=nor_mid}
N 1150 -470 1150 -410 {lab=uv_flag}
N 1110 -500 1040 -500 {lab=en_bar}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1040 -500 0 0 {name=l_eb1 sig_type=std_logic lab=en_bar}

* --- XMnor_n1: NOR NMOS left (W=1u L=0.15u, gate=out_n) ---
T {XMnor_n1} 1050 -240 0 0 0.25 0.25 {layer=13}
T {W=1u L=0.15u} 1050 -218 0 0 0.2 0.2 {layer=5}
T {B=GND} 1170 -285 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1130 -320 0 0 {name=XMnor_n1
L=0.15u
W=1u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1150 -350 1150 -410 {lab=uv_flag}
N 1150 -290 1150 -180 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1150 -180 0 0 {name=lg5 lab=GND}
N 1110 -320 1040 -320 {lab=out_n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1040 -320 0 0 {name=l_on3 sig_type=std_logic lab=out_n}

* --- XMnor_n2: NOR NMOS right (W=1u L=0.15u, gate=en_bar) ---
T {XMnor_n2} 1280 -240 0 0 0.25 0.25 {layer=13}
T {W=1u L=0.15u} 1280 -218 0 0 0.2 0.2 {layer=5}
T {B=GND} 1400 -285 0 0 0.2 0.2 {layer=7}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1360 -320 0 0 {name=XMnor_n2
L=0.15u
W=1u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1380 -350 1380 -410 {lab=uv_flag}
N 1380 -290 1380 -180 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1380 -180 0 0 {name=lg6 lab=GND}
N 1340 -320 1270 -320 {lab=en_bar}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1270 -320 0 0 {name=l_eb2 sig_type=std_logic lab=en_bar}

* --- uv_flag output connection ---
N 1150 -410 1380 -410 {lab=uv_flag}
N 1260 -410 1260 -390 {lab=uv_flag}
T {uv_flag} 1265 -395 0 0 0.35 0.35 {layer=4}
N 1380 -410 1500 -410 {lab=uv_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -410 2 0 {name=l_fl sig_type=std_logic lab=uv_flag}
T {HIGH when PVDD < 4.3V} 1265 -370 0 0 0.22 0.22 {}

* ================================================================
* SIGNAL FLOW ANNOTATIONS
* ================================================================
T {PVDD → R_top/R_bot divider → mid_uv (~1.226V at trip)} -520 -200 0 0 0.22 0.22 {layer=5}
T {Diff pair: XM1(mid_uv) vs XM2(vref) → out_n} 180 -200 0 0 0.22 0.22 {layer=5}
T {NOR(out_n, en_bar) → uv_flag HIGH when UV detected and enabled} 850 -200 0 0 0.22 0.22 {layer=5}
T {Hysteresis: XR_hyst feeds out_n back to mid_uv (positive feedback)} -320 -200 0 0 0.22 0.22 {layer=5}
