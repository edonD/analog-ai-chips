v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {UV COMPARATOR} 100 -750 0 4 0.7 0.7 {}
T {Block 05 — PVDD Undervoltage Detector} 100 -700 0 8 0.4 0.4 {}
T {NMOS diff pair + PMOS mirror | 1.8V supply | Threshold ~4.3V} 100 -660 0 8 0.35 0.35 {}
B 2 60 -620 380 100 {dash=5}
T {RESISTIVE DIVIDER} 80 -610 0 7 0.35 0.35 {}
C {res.sym} 200 -450 0 0 {name=R_top value=500k}
N 200 -560 200 -480 {}
C {lab_pin.sym} 120 -560 0 0 {name=p1 sig_type=std_logic lab=pvdd}
N 120 -560 200 -560 {}
N 200 -420 200 -370 {}
C {res.sym} 200 -280 0 0 {name=R_bot value=199.4k}
N 200 -370 200 -310 {}
N 200 -250 200 -210 {}
C {gnd.sym} 200 -210 0 0 {name=l1 lab=GND}
N 200 -370 350 -370 {}
C {lab_pin.sym} 350 -370 0 2 {name=p1 sig_type=std_logic lab=mid_uv}
B 2 360 -430 650 -310 {dash=3}
T {HYSTERESIS FEEDBACK} 375 -425 0 5 0.25 0.25 {}
T {R_hyst from out_n} 375 -400 0 5 0.2 0.2 {}
C {res.sym} 500 -370 0 1 {name=R_hyst value=2.5M}
N 470 -370 350 -370 {}
N 530 -370 620 -370 {}
C {lab_pin.sym} 620 -370 0 2 {name=p1 sig_type=std_logic lab=out_n}
B 2 650 -620 870 100 {dash=5}
T {BIAS (~1uA)} 665 -610 0 8 0.35 0.35 {}
C {res.sym} 750 -480 0 0 {name=R_bias value=800k}
N 750 -560 750 -510 {}
C {lab_pin.sym} 680 -560 0 0 {name=p1 sig_type=std_logic lab=vdd_comp}
N 680 -560 750 -560 {}
C {nmos4.sym} 730 -360 0 0 {name=XMbias model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1}
N 750 -450 750 -390 {}
N 710 -360 710 -390 {}
N 710 -390 750 -390 {}
N 750 -330 750 -290 {}
C {gnd.sym} 750 -290 0 0 {name=l1 lab=GND}
N 750 -360 770 -360 {}
N 770 -360 770 -290 {}
C {lab_pin.sym} 780 -390 0 2 {name=p1 sig_type=std_logic lab=bias_n}
N 750 -390 780 -390 {}
B 2 880 -620 1350 250 {dash=5}
T {NMOS DIFF PAIR + PMOS MIRROR} 900 -610 0 4 0.35 0.35 {}
T {PMOS current mirror load} 920 -590 0 8 0.25 0.25 {}
C {pmos4.sym} 980 -470 0 0 {name=XM3 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1}
N 1000 -500 1000 -530 {}
C {lab_pin.sym} 1010 -530 0 2 {name=p1 sig_type=std_logic lab=vdd_comp}
N 1000 -470 1020 -470 {}
N 1020 -470 1000 -530 {}
N 960 -470 940 -470 {}
N 940 -470 940 -440 {}
N 940 -440 1000 -440 {}
C {lab_pin.sym} 1010 -440 0 2 {name=p1 sig_type=std_logic lab=out_p}
C {pmos4.sym} 1200 -470 0 0 {name=XM4 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1}
N 1220 -500 1220 -530 {}
C {lab_pin.sym} 1230 -530 0 2 {name=p1 sig_type=std_logic lab=vdd_comp}
N 1220 -470 1240 -470 {}
N 1240 -470 1220 -530 {}
N 1180 -470 940 -470 {}
N 940 -470 940 -470 {}
C {lab_pin.sym} 1230 -440 0 2 {name=p1 sig_type=std_logic lab=out_n}
T {NMOS differential pair} 920 -380 0 8 0.25 0.25 {}
C {nmos4.sym} 980 -290 0 0 {name=XM1 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1}
N 1000 -320 1000 -440 {}
C {lab_pin.sym} 930 -290 0 0 {name=p1 sig_type=std_logic lab=mid_uv}
N 930 -290 960 -290 {}
N 1000 -260 1000 -230 {}
N 1000 -290 1020 -290 {}
N 1020 -290 1020 -190 {}
C {nmos4.sym} 1200 -290 0 0 {name=XM2 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1}
N 1220 -320 1220 -440 {}
C {lab_pin.sym} 1150 -290 0 0 {name=p1 sig_type=std_logic lab=vref}
N 1150 -290 1180 -290 {}
N 1220 -260 1220 -230 {}
N 1220 -290 1240 -290 {}
N 1240 -290 1240 -190 {}
N 1000 -230 1220 -230 {}
N 1110 -230 1110 -200 {}
C {lab_pin.sym} 1110 -230 0 0 {name=p1 sig_type=std_logic lab=tail}
T {Tail current} 1040 -160 0 8 0.25 0.25 {}
C {nmos4.sym} 1090 -120 0 0 {name=XMtail model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1}
N 1110 -150 1110 -200 {}
C {lab_pin.sym} 1040 -120 0 0 {name=p1 sig_type=std_logic lab=bias_n}
N 1040 -120 1070 -120 {}
N 1110 -90 1110 -60 {}
C {gnd.sym} 1110 -60 0 0 {name=l1 lab=GND}
N 1110 -120 1130 -120 {}
N 1130 -120 1110 -60 {}
B 2 1370 -620 1780 250 {dash=5}
T {ENABLE + NOR OUTPUT} 1390 -610 0 6 0.35 0.35 {}
T {en inverter} 1390 -580 0 8 0.25 0.25 {}
C {nmos4.sym} 1450 -450 0 0 {name=XMen_n model=sky130_fd_pr__nfet_01v8 w=0.42u l=0.15u m=1}
C {pmos4.sym} 1450 -530 0 0 {name=XMen_p model=sky130_fd_pr__pfet_01v8 w=0.84u l=0.15u m=1}
N 1430 -450 1400 -450 {}
N 1430 -530 1400 -530 {}
N 1400 -450 1400 -530 {}
C {lab_pin.sym} 1370 -490 0 0 {name=p1 sig_type=std_logic lab=en}
N 1370 -490 1400 -490 {}
N 1470 -480 1470 -500 {}
C {lab_pin.sym} 1510 -490 0 2 {name=p1 sig_type=std_logic lab=en_bar}
N 1470 -490 1510 -490 {}
N 1470 -560 1470 -580 {}
C {lab_pin.sym} 1480 -580 0 2 {name=p1 sig_type=std_logic lab=vdd_comp}
N 1470 -530 1490 -530 {}
N 1490 -530 1470 -580 {}
N 1470 -420 1470 -400 {}
C {gnd.sym} 1470 -400 0 0 {name=l1 lab=GND}
N 1470 -450 1490 -450 {}
N 1490 -450 1470 -400 {}
T {NOR(out_n, en_bar)} 1550 -400 0 6 0.25 0.25 {}
C {pmos4.sym} 1630 -340 0 0 {name=XMnor_p1 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1}
N 1610 -340 1580 -340 {}
C {lab_pin.sym} 1580 -340 0 0 {name=p1 sig_type=std_logic lab=out_n}
N 1650 -370 1650 -390 {}
C {lab_pin.sym} 1660 -390 0 2 {name=p1 sig_type=std_logic lab=vdd_comp}
N 1650 -340 1670 -340 {}
N 1670 -340 1650 -390 {}
C {pmos4.sym} 1630 -250 0 0 {name=XMnor_p2 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1}
N 1610 -250 1580 -250 {}
C {lab_pin.sym} 1580 -250 0 0 {name=p1 sig_type=std_logic lab=en_bar}
N 1650 -310 1650 -280 {}
N 1650 -250 1650 -310 {}
N 1650 -220 1650 -200 {}
C {nmos4.sym} 1580 -120 0 0 {name=XMnor_n1 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1}
N 1560 -120 1530 -120 {}
C {lab_pin.sym} 1530 -120 0 0 {name=p1 sig_type=std_logic lab=out_n}
N 1600 -90 1600 -70 {}
C {gnd.sym} 1600 -70 0 0 {name=l1 lab=GND}
N 1600 -120 1620 -120 {}
N 1620 -120 1600 -70 {}
C {nmos4.sym} 1700 -120 0 0 {name=XMnor_n2 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1}
N 1680 -120 1650 -120 {}
C {lab_pin.sym} 1650 -120 0 0 {name=p1 sig_type=std_logic lab=en_bar}
N 1720 -90 1720 -70 {}
C {gnd.sym} 1720 -70 0 0 {name=l1 lab=GND}
N 1720 -120 1740 -120 {}
N 1740 -120 1720 -70 {}
N 1600 -150 1600 -180 {}
N 1720 -150 1720 -180 {}
N 1600 -180 1720 -180 {}
N 1660 -180 1650 -200 {}
N 1720 -180 1780 -180 {}
C {lab_pin.sym} 1780 -180 0 2 {name=p1 sig_type=std_logic lab=uv_flag}
C {title.sym} 100 400 0 0 {name=l1 author="Block 05 UV/OV Comparators"}
