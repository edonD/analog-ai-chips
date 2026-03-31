v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {Block 05: UV/OV Comparators} -300 -1200 0 0 0.85 0.85 {layer=4}
T {Under-Voltage (trip=4.3V) + Over-Voltage (trip=5.5V)  |  1.8V FETs} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {.subckt uv_comparator / .subckt ov_comparator  —  pvdd vref flag vdd_comp gnd en} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="PVDD LDO — UV/OV Protection"}

* ============================================================
* Ports
* ============================================================
T {Ports} -250 -900 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -250 -850 0 0 {name=p1 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -250 -800 0 0 {name=p2 lab=vref}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -250 -750 0 0 {name=p3 lab=en}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -700 0 0 {name=p4 lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -250 -650 0 0 {name=p5 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -250 -600 0 0 {name=p6 lab=uv_flag}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -250 -550 0 0 {name=p7 lab=ov_flag}
* ============================================================
* UV Comparator (trip = 4.3V)
* ============================================================
T {UV Comparator (trip = 4.3V)} -50 -660 0 0 0.35 0.35 {layer=4}
L 8 -150 -720 1250 -720 {dash=5}
L 8 1250 -720 1250 280 {dash=5}
L 8 1250 280 -150 280 {dash=5}
L 8 -150 280 -150 -720 {dash=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} 0 -550 0 0 {name=R_top_uv value=500k}
T {R_top_uv} 20 -570 0 0 0.2 0.2 {layer=13}
T {500k} 20 -542 0 0 0.18 0.18 {layer=5}
N 0 -580 0 -615 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -615 2 0 {name=lb1 sig_type=std_logic lab=pvdd}
N 0 -520 0 -485 {lab=mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -485 2 0 {name=lb2 sig_type=std_logic lab=mid_uv}
C {/usr/share/xschem/xschem_library/devices/res.sym} 0 -390 0 0 {name=R_bot_uv value=199.4k}
T {R_bot_uv} 20 -410 0 0 0.2 0.2 {layer=13}
T {199.4k} 20 -382 0 0 0.18 0.18 {layer=5}
N 0 -420 0 -455 {lab=mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -455 2 0 {name=lb3 sig_type=std_logic lab=mid_uv}
N 0 -360 0 -325 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -325 2 0 {name=lb4 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/res.sym} 120 -470 0 0 {name=R_hyst_uv value=2.5Meg}
T {R_hyst_uv} 140 -490 0 0 0.2 0.2 {layer=13}
T {2.5Meg} 140 -462 0 0 0.18 0.18 {layer=5}
N 120 -500 120 -535 {lab=out_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 -535 2 0 {name=lb5 sig_type=std_logic lab=out_n_uv}
N 120 -440 120 -405 {lab=mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 120 -405 2 0 {name=lb6 sig_type=std_logic lab=mid_uv}
C {/usr/share/xschem/xschem_library/devices/res.sym} 240 -550 0 0 {name=R_bias_uv value=800k}
T {R_bias_uv} 260 -570 0 0 0.2 0.2 {layer=13}
T {800k} 260 -542 0 0 0.18 0.18 {layer=5}
N 240 -580 240 -615 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 240 -615 2 0 {name=lb7 sig_type=std_logic lab=vdd_comp}
N 240 -520 240 -485 {lab=bias_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 240 -485 2 0 {name=lb8 sig_type=std_logic lab=bias_n_uv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 400 -250 0 0 {name=XMbias_uv L=4 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMbias_uv} 375 -300 0 0 0.22 0.22 {layer=13}
T {N: W=1 L=4} 375 -285 0 0 0.18 0.18 {layer=5}
N 380 -250 340 -250 {lab=bias_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -250 0 0 {name=lb9 sig_type=std_logic lab=bias_n_uv}
N 420 -250 450 -250 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 450 -250 2 0 {name=lb10 sig_type=std_logic lab=gnd}
N 420 -280 420 -320 {lab=bias_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -320 2 0 {name=lb11 sig_type=std_logic lab=bias_n_uv}
N 420 -220 420 -180 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -180 2 0 {name=lb12 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 600 -250 0 0 {name=XMtail_uv L=4 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMtail_uv} 575 -300 0 0 0.22 0.22 {layer=13}
T {N: W=1 L=4} 575 -285 0 0 0.18 0.18 {layer=5}
N 580 -250 540 -250 {lab=bias_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 -250 0 0 {name=lb13 sig_type=std_logic lab=bias_n_uv}
N 620 -250 650 -250 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 -250 2 0 {name=lb14 sig_type=std_logic lab=gnd}
N 620 -280 620 -320 {lab=tail_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -320 2 0 {name=lb15 sig_type=std_logic lab=tail_uv}
N 620 -220 620 -180 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -180 2 0 {name=lb16 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 500 -400 0 0 {name=XM1_uv L=1 W=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XM1_uv} 475 -450 0 0 0.22 0.22 {layer=13}
T {N: W=2 L=1} 475 -435 0 0 0.18 0.18 {layer=5}
N 480 -400 440 -400 {lab=mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 440 -400 0 0 {name=lb17 sig_type=std_logic lab=mid_uv}
N 520 -400 550 -400 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 -400 2 0 {name=lb18 sig_type=std_logic lab=gnd}
N 520 -430 520 -470 {lab=out_p_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 -470 2 0 {name=lb19 sig_type=std_logic lab=out_p_uv}
N 520 -370 520 -330 {lab=tail_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 -330 2 0 {name=lb20 sig_type=std_logic lab=tail_uv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 750 -400 0 0 {name=XM2_uv L=1 W=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XM2_uv} 725 -450 0 0 0.22 0.22 {layer=13}
T {N: W=2 L=1} 725 -435 0 0 0.18 0.18 {layer=5}
N 730 -400 690 -400 {lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 690 -400 0 0 {name=lb21 sig_type=std_logic lab=vref}
N 770 -400 800 -400 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -400 2 0 {name=lb22 sig_type=std_logic lab=gnd}
N 770 -430 770 -470 {lab=out_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 770 -470 2 0 {name=lb23 sig_type=std_logic lab=out_n_uv}
N 770 -370 770 -330 {lab=tail_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 770 -330 2 0 {name=lb24 sig_type=std_logic lab=tail_uv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 500 -650 0 0 {name=XM3_uv L=1 W=2 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XM3_uv} 475 -700 0 0 0.22 0.22 {layer=13}
T {P: W=2 L=1} 475 -685 0 0 0.18 0.18 {layer=5}
N 480 -650 440 -650 {lab=out_p_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 440 -650 0 0 {name=lb25 sig_type=std_logic lab=out_p_uv}
N 520 -650 550 -650 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 -650 2 0 {name=lb26 sig_type=std_logic lab=vdd_comp}
N 520 -680 520 -720 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 -720 2 0 {name=lb27 sig_type=std_logic lab=vdd_comp}
N 520 -620 520 -580 {lab=out_p_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 -580 2 0 {name=lb28 sig_type=std_logic lab=out_p_uv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 750 -650 0 0 {name=XM4_uv L=1 W=2 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XM4_uv} 725 -700 0 0 0.22 0.22 {layer=13}
T {P: W=2 L=1} 725 -685 0 0 0.18 0.18 {layer=5}
N 730 -650 690 -650 {lab=out_p_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 690 -650 0 0 {name=lb29 sig_type=std_logic lab=out_p_uv}
N 770 -650 800 -650 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -650 2 0 {name=lb30 sig_type=std_logic lab=vdd_comp}
N 770 -680 770 -720 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 770 -720 2 0 {name=lb31 sig_type=std_logic lab=vdd_comp}
N 770 -620 770 -580 {lab=out_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 770 -580 2 0 {name=lb32 sig_type=std_logic lab=out_n_uv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 900 -300 0 0 {name=XMen_n_uv L=0.15 W=0.42 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMen_n_uv} 875 -350 0 0 0.22 0.22 {layer=13}
T {N: W=0.42 L=0.15} 875 -335 0 0 0.18 0.18 {layer=5}
N 880 -300 840 -300 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 840 -300 0 0 {name=lb33 sig_type=std_logic lab=en}
N 920 -300 950 -300 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 -300 2 0 {name=lb34 sig_type=std_logic lab=gnd}
N 920 -330 920 -370 {lab=en_bar_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -370 2 0 {name=lb35 sig_type=std_logic lab=en_bar_uv}
N 920 -270 920 -230 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -230 2 0 {name=lb36 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 900 -450 0 0 {name=XMen_p_uv L=0.15 W=0.84 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XMen_p_uv} 875 -500 0 0 0.22 0.22 {layer=13}
T {P: W=0.84 L=0.15} 875 -485 0 0 0.18 0.18 {layer=5}
N 880 -450 840 -450 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 840 -450 0 0 {name=lb37 sig_type=std_logic lab=en}
N 920 -450 950 -450 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 -450 2 0 {name=lb38 sig_type=std_logic lab=vdd_comp}
N 920 -480 920 -520 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -520 2 0 {name=lb39 sig_type=std_logic lab=vdd_comp}
N 920 -420 920 -380 {lab=en_bar_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -380 2 0 {name=lb40 sig_type=std_logic lab=en_bar_uv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1100 -550 0 0 {name=XMnor_p1_uv L=0.15 W=4 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XMnor_p1_uv} 1075 -600 0 0 0.22 0.22 {layer=13}
T {P: W=4 L=0.15} 1075 -585 0 0 0.18 0.18 {layer=5}
N 1080 -550 1040 -550 {lab=out_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1040 -550 0 0 {name=lb41 sig_type=std_logic lab=out_n_uv}
N 1120 -550 1150 -550 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -550 2 0 {name=lb42 sig_type=std_logic lab=vdd_comp}
N 1120 -580 1120 -620 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 -620 2 0 {name=lb43 sig_type=std_logic lab=vdd_comp}
N 1120 -520 1120 -480 {lab=nor_mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 -480 2 0 {name=lb44 sig_type=std_logic lab=nor_mid_uv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1100 -400 0 0 {name=XMnor_p2_uv L=0.15 W=4 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XMnor_p2_uv} 1075 -450 0 0 0.22 0.22 {layer=13}
T {P: W=4 L=0.15} 1075 -435 0 0 0.18 0.18 {layer=5}
N 1080 -400 1040 -400 {lab=en_bar_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1040 -400 0 0 {name=lb45 sig_type=std_logic lab=en_bar_uv}
N 1120 -400 1150 -400 {lab=nor_mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -400 2 0 {name=lb46 sig_type=std_logic lab=nor_mid_uv}
N 1120 -430 1120 -470 {lab=nor_mid_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 -470 2 0 {name=lb47 sig_type=std_logic lab=nor_mid_uv}
N 1120 -370 1120 -330 {lab=uv_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 -330 2 0 {name=lb48 sig_type=std_logic lab=uv_flag}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1100 -200 0 0 {name=XMnor_n1_uv L=0.15 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMnor_n1_uv} 1075 -250 0 0 0.22 0.22 {layer=13}
T {N: W=1 L=0.15} 1075 -235 0 0 0.18 0.18 {layer=5}
N 1080 -200 1040 -200 {lab=out_n_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1040 -200 0 0 {name=lb49 sig_type=std_logic lab=out_n_uv}
N 1120 -200 1150 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -200 2 0 {name=lb50 sig_type=std_logic lab=gnd}
N 1120 -230 1120 -270 {lab=uv_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 -270 2 0 {name=lb51 sig_type=std_logic lab=uv_flag}
N 1120 -170 1120 -130 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1120 -130 2 0 {name=lb52 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1300 -200 0 0 {name=XMnor_n2_uv L=0.15 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMnor_n2_uv} 1275 -250 0 0 0.22 0.22 {layer=13}
T {N: W=1 L=0.15} 1275 -235 0 0 0.18 0.18 {layer=5}
N 1280 -200 1240 -200 {lab=en_bar_uv}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1240 -200 0 0 {name=lb53 sig_type=std_logic lab=en_bar_uv}
N 1320 -200 1350 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1350 -200 2 0 {name=lb54 sig_type=std_logic lab=gnd}
N 1320 -230 1320 -270 {lab=uv_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1320 -270 2 0 {name=lb55 sig_type=std_logic lab=uv_flag}
N 1320 -170 1320 -130 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1320 -130 2 0 {name=lb56 sig_type=std_logic lab=gnd}
T {UV trip = 4.3V  |  R_top=500k / R_bot=199.4k  |  Vdiv = PVDD * 199.4/699.4} 0 150 0 0 0.25 0.25 {layer=8}
* ============================================================
* OV Comparator (trip = 5.5V)
* ============================================================
T {OV Comparator (trip = 5.5V)} 1550 -660 0 0 0.35 0.35 {layer=4}
L 8 1450 -720 2850 -720 {dash=5}
L 8 2850 -720 2850 280 {dash=5}
L 8 2850 280 1450 280 {dash=5}
L 8 1450 280 1450 -720 {dash=5}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1600 -550 0 0 {name=R_top_ov value=500k}
T {R_top_ov} 1620 -570 0 0 0.2 0.2 {layer=13}
T {500k} 1620 -542 0 0 0.18 0.18 {layer=5}
N 1600 -580 1600 -615 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 -615 2 0 {name=lb57 sig_type=std_logic lab=pvdd}
N 1600 -520 1600 -485 {lab=mid_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 -485 2 0 {name=lb58 sig_type=std_logic lab=mid_ov}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1600 -390 0 0 {name=R_bot_ov value=146k}
T {R_bot_ov} 1620 -410 0 0 0.2 0.2 {layer=13}
T {146k} 1620 -382 0 0 0.18 0.18 {layer=5}
N 1600 -420 1600 -455 {lab=mid_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 -455 2 0 {name=lb59 sig_type=std_logic lab=mid_ov}
N 1600 -360 1600 -325 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 -325 2 0 {name=lb60 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1720 -470 0 0 {name=R_hyst_ov value=8Meg}
T {R_hyst_ov} 1740 -490 0 0 0.2 0.2 {layer=13}
T {8Meg} 1740 -462 0 0 0.18 0.18 {layer=5}
N 1720 -500 1720 -535 {lab=ov_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1720 -535 2 0 {name=lb61 sig_type=std_logic lab=ov_flag}
N 1720 -440 1720 -405 {lab=mid_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1720 -405 2 0 {name=lb62 sig_type=std_logic lab=mid_ov}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1840 -550 0 0 {name=R_bias_ov value=800k}
T {R_bias_ov} 1860 -570 0 0 0.2 0.2 {layer=13}
T {800k} 1860 -542 0 0 0.18 0.18 {layer=5}
N 1840 -580 1840 -615 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1840 -615 2 0 {name=lb63 sig_type=std_logic lab=vdd_comp}
N 1840 -520 1840 -485 {lab=bias_n_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1840 -485 2 0 {name=lb64 sig_type=std_logic lab=bias_n_ov}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2000 -250 0 0 {name=XMbias_ov L=4 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMbias_ov} 1975 -300 0 0 0.22 0.22 {layer=13}
T {N: W=1 L=4} 1975 -285 0 0 0.18 0.18 {layer=5}
N 1980 -250 1940 -250 {lab=bias_n_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -250 0 0 {name=lb65 sig_type=std_logic lab=bias_n_ov}
N 2020 -250 2050 -250 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2050 -250 2 0 {name=lb66 sig_type=std_logic lab=gnd}
N 2020 -280 2020 -320 {lab=bias_n_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2020 -320 2 0 {name=lb67 sig_type=std_logic lab=bias_n_ov}
N 2020 -220 2020 -180 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2020 -180 2 0 {name=lb68 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2200 -250 0 0 {name=XMtail_ov L=4 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMtail_ov} 2175 -300 0 0 0.22 0.22 {layer=13}
T {N: W=1 L=4} 2175 -285 0 0 0.18 0.18 {layer=5}
N 2180 -250 2140 -250 {lab=bias_n_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2140 -250 0 0 {name=lb69 sig_type=std_logic lab=bias_n_ov}
N 2220 -250 2250 -250 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2250 -250 2 0 {name=lb70 sig_type=std_logic lab=gnd}
N 2220 -280 2220 -320 {lab=tail_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2220 -320 2 0 {name=lb71 sig_type=std_logic lab=tail_ov}
N 2220 -220 2220 -180 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2220 -180 2 0 {name=lb72 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2100 -400 0 0 {name=XM1_ov L=1 W=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XM1_ov} 2075 -450 0 0 0.22 0.22 {layer=13}
T {N: W=2 L=1} 2075 -435 0 0 0.18 0.18 {layer=5}
N 2080 -400 2040 -400 {lab=vref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2040 -400 0 0 {name=lb73 sig_type=std_logic lab=vref}
N 2120 -400 2150 -400 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2150 -400 2 0 {name=lb74 sig_type=std_logic lab=gnd}
N 2120 -430 2120 -470 {lab=out_p_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2120 -470 2 0 {name=lb75 sig_type=std_logic lab=out_p_ov}
N 2120 -370 2120 -330 {lab=tail_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2120 -330 2 0 {name=lb76 sig_type=std_logic lab=tail_ov}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2350 -400 0 0 {name=XM2_ov L=1 W=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XM2_ov} 2325 -450 0 0 0.22 0.22 {layer=13}
T {N: W=2 L=1} 2325 -435 0 0 0.18 0.18 {layer=5}
N 2330 -400 2290 -400 {lab=mid_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2290 -400 0 0 {name=lb77 sig_type=std_logic lab=mid_ov}
N 2370 -400 2400 -400 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -400 2 0 {name=lb78 sig_type=std_logic lab=gnd}
N 2370 -430 2370 -470 {lab=out_n_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2370 -470 2 0 {name=lb79 sig_type=std_logic lab=out_n_ov}
N 2370 -370 2370 -330 {lab=tail_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2370 -330 2 0 {name=lb80 sig_type=std_logic lab=tail_ov}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2100 -650 0 0 {name=XM3_ov L=1 W=2 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XM3_ov} 2075 -700 0 0 0.22 0.22 {layer=13}
T {P: W=2 L=1} 2075 -685 0 0 0.18 0.18 {layer=5}
N 2080 -650 2040 -650 {lab=out_p_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2040 -650 0 0 {name=lb81 sig_type=std_logic lab=out_p_ov}
N 2120 -650 2150 -650 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2150 -650 2 0 {name=lb82 sig_type=std_logic lab=vdd_comp}
N 2120 -680 2120 -720 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2120 -720 2 0 {name=lb83 sig_type=std_logic lab=vdd_comp}
N 2120 -620 2120 -580 {lab=out_p_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2120 -580 2 0 {name=lb84 sig_type=std_logic lab=out_p_ov}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2350 -650 0 0 {name=XM4_ov L=1 W=2 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XM4_ov} 2325 -700 0 0 0.22 0.22 {layer=13}
T {P: W=2 L=1} 2325 -685 0 0 0.18 0.18 {layer=5}
N 2330 -650 2290 -650 {lab=out_p_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2290 -650 0 0 {name=lb85 sig_type=std_logic lab=out_p_ov}
N 2370 -650 2400 -650 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -650 2 0 {name=lb86 sig_type=std_logic lab=vdd_comp}
N 2370 -680 2370 -720 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2370 -720 2 0 {name=lb87 sig_type=std_logic lab=vdd_comp}
N 2370 -620 2370 -580 {lab=out_n_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2370 -580 2 0 {name=lb88 sig_type=std_logic lab=out_n_ov}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2500 -300 0 0 {name=XMen_n_ov L=0.15 W=0.42 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMen_n_ov} 2475 -350 0 0 0.22 0.22 {layer=13}
T {N: W=0.42 L=0.15} 2475 -335 0 0 0.18 0.18 {layer=5}
N 2480 -300 2440 -300 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2440 -300 0 0 {name=lb89 sig_type=std_logic lab=en}
N 2520 -300 2550 -300 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2550 -300 2 0 {name=lb90 sig_type=std_logic lab=gnd}
N 2520 -330 2520 -370 {lab=en_bar_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2520 -370 2 0 {name=lb91 sig_type=std_logic lab=en_bar_ov}
N 2520 -270 2520 -230 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2520 -230 2 0 {name=lb92 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2500 -450 0 0 {name=XMen_p_ov L=0.15 W=0.84 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XMen_p_ov} 2475 -500 0 0 0.22 0.22 {layer=13}
T {P: W=0.84 L=0.15} 2475 -485 0 0 0.18 0.18 {layer=5}
N 2480 -450 2440 -450 {lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2440 -450 0 0 {name=lb93 sig_type=std_logic lab=en}
N 2520 -450 2550 -450 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2550 -450 2 0 {name=lb94 sig_type=std_logic lab=vdd_comp}
N 2520 -480 2520 -520 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2520 -520 2 0 {name=lb95 sig_type=std_logic lab=vdd_comp}
N 2520 -420 2520 -380 {lab=en_bar_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2520 -380 2 0 {name=lb96 sig_type=std_logic lab=en_bar_ov}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2700 -550 0 0 {name=XMnor_p1_ov L=0.15 W=4 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XMnor_p1_ov} 2675 -600 0 0 0.22 0.22 {layer=13}
T {P: W=4 L=0.15} 2675 -585 0 0 0.18 0.18 {layer=5}
N 2680 -550 2640 -550 {lab=out_n_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2640 -550 0 0 {name=lb97 sig_type=std_logic lab=out_n_ov}
N 2720 -550 2750 -550 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2750 -550 2 0 {name=lb98 sig_type=std_logic lab=vdd_comp}
N 2720 -580 2720 -620 {lab=vdd_comp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2720 -620 2 0 {name=lb99 sig_type=std_logic lab=vdd_comp}
N 2720 -520 2720 -480 {lab=nor_mid_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2720 -480 2 0 {name=lb100 sig_type=std_logic lab=nor_mid_ov}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2700 -400 0 0 {name=XMnor_p2_ov L=0.15 W=4 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {XMnor_p2_ov} 2675 -450 0 0 0.22 0.22 {layer=13}
T {P: W=4 L=0.15} 2675 -435 0 0 0.18 0.18 {layer=5}
N 2680 -400 2640 -400 {lab=en_bar_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2640 -400 0 0 {name=lb101 sig_type=std_logic lab=en_bar_ov}
N 2720 -400 2750 -400 {lab=nor_mid_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2750 -400 2 0 {name=lb102 sig_type=std_logic lab=nor_mid_ov}
N 2720 -430 2720 -470 {lab=nor_mid_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2720 -470 2 0 {name=lb103 sig_type=std_logic lab=nor_mid_ov}
N 2720 -370 2720 -330 {lab=ov_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2720 -330 2 0 {name=lb104 sig_type=std_logic lab=ov_flag}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2700 -200 0 0 {name=XMnor_n1_ov L=0.15 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMnor_n1_ov} 2675 -250 0 0 0.22 0.22 {layer=13}
T {N: W=1 L=0.15} 2675 -235 0 0 0.18 0.18 {layer=5}
N 2680 -200 2640 -200 {lab=out_n_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2640 -200 0 0 {name=lb105 sig_type=std_logic lab=out_n_ov}
N 2720 -200 2750 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2750 -200 2 0 {name=lb106 sig_type=std_logic lab=gnd}
N 2720 -230 2720 -270 {lab=ov_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2720 -270 2 0 {name=lb107 sig_type=std_logic lab=ov_flag}
N 2720 -170 2720 -130 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2720 -130 2 0 {name=lb108 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2900 -200 0 0 {name=XMnor_n2_ov L=0.15 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {XMnor_n2_ov} 2875 -250 0 0 0.22 0.22 {layer=13}
T {N: W=1 L=0.15} 2875 -235 0 0 0.18 0.18 {layer=5}
N 2880 -200 2840 -200 {lab=en_bar_ov}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2840 -200 0 0 {name=lb109 sig_type=std_logic lab=en_bar_ov}
N 2920 -200 2950 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2950 -200 2 0 {name=lb110 sig_type=std_logic lab=gnd}
N 2920 -230 2920 -270 {lab=ov_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2920 -270 2 0 {name=lb111 sig_type=std_logic lab=ov_flag}
N 2920 -170 2920 -130 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2920 -130 2 0 {name=lb112 sig_type=std_logic lab=gnd}
T {OV trip = 5.5V  |  R_top=500k / R_bot=146k  |  Vdiv = PVDD * 146/646} 1600 150 0 0 0.25 0.25 {layer=8}
T {NOTE: Diff pair inputs swapped vs UV — vref on M1, mid_ov on M2} 1600 190 0 0 0.22 0.22 {layer=13}
