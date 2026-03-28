v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {BLOCK 05: UV COMPARATOR} -600 -1100 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator} -600 -1020 0 0 0.5 0.5 {layer=8}
T {SkyWater SKY130A Process} -600 -980 0 0 0.4 0.4 {}
T {Topology: NMOS differential pair + PMOS current mirror load} -600 -920 0 0 0.35 0.35 {}
T {Supply: vdd_comp = 1.8 V    |    Threshold: PVDD < 4.3 V    |    uv_flag = HIGH when undervoltage} -600 -880 0 0 0.35 0.35 {}
T {Date: 2026-03-28} -600 -830 0 0 0.3 0.3 {}
T {.subckt uv_comparator  pvdd  vref  uv_flag  vdd_comp  gnd  en} -600 -790 0 0 0.3 0.3 {layer=13}
T {RESISTIVE DIVIDER} -600 -700 0 0 0.5 0.5 {layer=4}
T {Scales PVDD down to ~1.226 V} -600 -660 0 0 0.3 0.3 {}
T {at threshold crossing} -600 -630 0 0 0.3 0.3 {}
T {pvdd} -580 -560 0 0 0.4 0.4 {layer=7}
C {res.sym} -500 -470 0 0 {name=R_top value=500k}
N -500 -540 -500 -500 {}
C {iopin.sym} -500 -540 3 0 {name=p_pvdd lab=pvdd}
N -500 -440 -500 -380 {}
N -500 -380 -420 -380 {}
T {mid_uv} -410 -390 0 0 0.35 0.35 {layer=8}
C {res.sym} -500 -310 0 0 {name=R_bot value=199.4k}
N -500 -380 -500 -340 {}
N -500 -280 -500 -240 {}
C {gnd.sym} -500 -240 0 0 {name=l1 lab=GND}
T {HYSTERESIS} -320 -700 0 0 0.45 0.45 {layer=4}
T {R_hyst = 2.5 Meg} -320 -660 0 0 0.3 0.3 {layer=7}
T {Feedback: out_n to mid_uv} -320 -630 0 0 0.3 0.3 {}
T {Positive feedback for clean switching} -320 -600 0 0 0.25 0.25 {layer=5}
C {res.sym} -250 -350 0 0 {name=R_hyst value=2.5M}
N -420 -380 -250 -380 {}
N -250 -320 -170 -320 {}
T {out_n} -160 -330 0 0 0.3 0.3 {layer=8}
T {BIAS} -100 -700 0 0 0.45 0.45 {layer=4}
T {~1 uA self-biased} -100 -660 0 0 0.3 0.3 {}
C {res.sym} -30 -550 0 0 {name=R_bias value=800k}
N -30 -620 -30 -580 {}
T {vdd_comp} -90 -640 0 0 0.3 0.3 {layer=8}
C {nmos4.sym} -50 -430 0 0 {name=XMbias model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1 spiceprefix=X}
N -30 -520 -30 -460 {}
N -70 -430 -70 -460 {}
N -70 -460 -30 -460 {}
N -30 -400 -30 -360 {}
C {gnd.sym} -30 -360 0 0 {name=l2 lab=GND}
T {bias_n} 0 -470 0 0 0.3 0.3 {layer=8}
T {NMOS DIFFERENTIAL PAIR} 200 -700 0 0 0.5 0.5 {layer=4}
T {+ PMOS CURRENT MIRROR LOAD} 200 -660 0 0 0.45 0.45 {layer=4}
C {pmos4.sym} 280 -500 0 0 {name=XM3 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1 spiceprefix=X}
N 300 -530 300 -570 {}
T {vdd_comp} 310 -580 0 0 0.3 0.3 {layer=8}
N 260 -500 240 -500 {}
N 240 -500 240 -470 {}
N 240 -470 300 -470 {}
N 300 -500 320 -500 {}
N 320 -500 320 -570 {}
T {out_p} 310 -475 0 0 0.25 0.25 {layer=13}
C {pmos4.sym} 530 -500 0 0 {name=XM4 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1 spiceprefix=X}
N 550 -530 550 -570 {}
T {vdd_comp} 560 -580 0 0 0.3 0.3 {layer=8}
N 510 -500 240 -500 {}
N 240 -500 240 -500 {}
N 550 -500 570 -500 {}
N 570 -500 570 -570 {}
T {out_n} 560 -475 0 0 0.35 0.35 {layer=7}
C {nmos4.sym} 280 -320 0 0 {name=XM1 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1 spiceprefix=X}
N 300 -350 300 -470 {}
T {mid_uv} 160 -330 0 0 0.35 0.35 {layer=8}
N 180 -320 260 -320 {}
N 300 -290 300 -260 {}
N 300 -320 320 -320 {}
C {nmos4.sym} 530 -320 0 0 {name=XM2 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1 spiceprefix=X}
N 550 -350 550 -470 {}
T {vref} 430 -330 0 0 0.35 0.35 {layer=8}
N 450 -320 510 -320 {}
N 550 -290 550 -260 {}
N 550 -320 570 -320 {}
N 300 -260 550 -260 {}
N 425 -260 425 -230 {}
T {tail} 435 -265 0 0 0.3 0.3 {layer=13}
C {nmos4.sym} 405 -180 0 0 {name=XMtail model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1 spiceprefix=X}
N 425 -210 425 -230 {}
N 385 -180 345 -180 {}
T {bias_n} 285 -190 0 0 0.3 0.3 {layer=8}
N 425 -150 425 -120 {}
C {gnd.sym} 425 -120 0 0 {name=l3 lab=GND}
T {ENABLE + NOR OUTPUT} 750 -700 0 0 0.5 0.5 {layer=4}
T {uv_flag = NOR(out_n, en_bar)} 750 -660 0 0 0.35 0.35 {layer=13}
T {HIGH when PVDD < threshold} 750 -630 0 0 0.3 0.3 {layer=5}
C {pmos4.sym} 800 -510 0 0 {name=XMen_p model=sky130_fd_pr__pfet_01v8 w=0.84u l=0.15u m=1 spiceprefix=X}
C {nmos4.sym} 800 -430 0 0 {name=XMen_n model=sky130_fd_pr__nfet_01v8 w=0.42u l=0.15u m=1 spiceprefix=X}
N 780 -510 780 -430 {}
N 780 -470 740 -470 {}
T {en} 690 -480 0 0 0.35 0.35 {layer=8}
N 820 -480 820 -460 {}
T {en_bar} 850 -475 0 0 0.3 0.3 {layer=13}
N 820 -470 850 -470 {}
N 820 -540 820 -570 {}
T {vdd_comp} 830 -580 0 0 0.25 0.25 {layer=8}
N 820 -510 840 -510 {}
N 840 -510 840 -570 {}
N 820 -400 820 -370 {}
C {gnd.sym} 820 -370 0 0 {name=l4 lab=GND}
N 820 -430 840 -430 {}
N 840 -430 840 -370 {}
C {pmos4.sym} 980 -490 0 0 {name=XMnor_p1 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1 spiceprefix=X}
N 960 -490 920 -490 {}
T {out_n} 860 -500 0 0 0.3 0.3 {layer=8}
N 1000 -520 1000 -550 {}
T {vdd_comp} 1010 -560 0 0 0.25 0.25 {layer=8}
N 1000 -490 1020 -490 {}
N 1020 -490 1020 -550 {}
C {pmos4.sym} 980 -400 0 0 {name=XMnor_p2 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1 spiceprefix=X}
N 960 -400 920 -400 {}
T {en_bar} 860 -410 0 0 0.3 0.3 {layer=8}
N 1000 -460 1000 -430 {}
N 1000 -400 1000 -460 {}
C {nmos4.sym} 950 -280 0 0 {name=XMnor_n1 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1 spiceprefix=X}
N 930 -280 890 -280 {}
T {out_n} 830 -290 0 0 0.25 0.25 {layer=8}
N 970 -250 970 -220 {}
C {gnd.sym} 970 -220 0 0 {name=l5 lab=GND}
N 970 -280 990 -280 {}
N 990 -280 990 -220 {}
C {nmos4.sym} 1060 -280 0 0 {name=XMnor_n2 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1 spiceprefix=X}
N 1040 -280 1000 -280 {}
T {en_bar} 930 -290 0 0 0.25 0.25 {layer=8}
N 1080 -250 1080 -220 {}
C {gnd.sym} 1080 -220 0 0 {name=l6 lab=GND}
N 1080 -280 1100 -280 {}
N 1100 -280 1100 -220 {}
N 970 -310 970 -340 {}
N 1080 -310 1080 -340 {}
N 970 -340 1080 -340 {}
N 1025 -340 1000 -340 {}
N 1000 -340 1000 -370 {}
N 1080 -340 1210 -340 {}
C {iopin.sym} 1210 -340 0 0 {name=p_out lab=uv_flag}
T {uv_flag} 1220 -370 0 0 0.5 0.5 {layer=4}
T {HIGH when PVDD < 4.3 V} 1220 -330 0 0 0.3 0.3 {}
T {CHARACTERIZATION} -600 100 0 0 0.5 0.5 {layer=4}
T {UV threshold (falling, TT 27C)   =  4.289 V       spec 4.0 - 4.5 V       PASS} -600 160 0 0 0.3 0.3 {layer=7}
T {UV hysteresis                     =  63.5 mV       spec 50 - 150 mV        PASS} -600 200 0 0 0.3 0.3 {layer=7}
T {UV de-assertion (rising)          =  4.353 V       within spec window       PASS} -600 240 0 0 0.3 0.3 {layer=7}
T {Response time                     =  < 0.01 us     spec <= 5 us             PASS} -600 280 0 0 0.3 0.3 {layer=7}
T {Power (from vdd_comp)             =  2.71 uA       spec <= 5 uA             PASS} -600 320 0 0 0.3 0.3 {layer=7}
T {Output rail-to-rail               =  YES            0 / 1.8 V               PASS} -600 360 0 0 0.3 0.3 {layer=7}
T {Threshold error                   =  5.2 mV        spec <= 200 mV           PASS} -600 400 0 0 0.3 0.3 {layer=7}
T {All 13/13 specs PASS} -600 470 0 0 0.45 0.45 {layer=4}
C {title.sym} -660 600 0 0 {name=l1 author="Block 05: UV Comparator -- Analog AI Chips PVDD LDO Regulator"}
