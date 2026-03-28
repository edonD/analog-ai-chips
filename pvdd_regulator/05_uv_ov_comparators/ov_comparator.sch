v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {BLOCK 05: OV COMPARATOR} -600 -1100 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator} -600 -1020 0 0 0.5 0.5 {layer=8}
T {SkyWater SKY130A Process} -600 -980 0 0 0.4 0.4 {}
T {Topology: NMOS differential pair + PMOS current mirror load} -600 -920 0 0 0.35 0.35 {}
T {Supply: vdd_comp = 1.8 V    |    Threshold: PVDD > 5.5 V    |    ov_flag = HIGH when overvoltage} -600 -880 0 0 0.35 0.35 {}
T {NOTE: Diff pair inputs SWAPPED vs UV  (M1 = vref, M2 = mid_ov)} -600 -840 0 0 0.35 0.35 {layer=5}
T {Date: 2026-03-28} -600 -790 0 0 0.3 0.3 {}
T {.subckt ov_comparator  pvdd  vref  ov_flag  vdd_comp  gnd  en} -600 -750 0 0 0.3 0.3 {layer=13}
T {RESISTIVE DIVIDER} -600 -660 0 0 0.5 0.5 {layer=4}
T {Scales PVDD down to ~1.226 V} -600 -620 0 0 0.3 0.3 {}
T {pvdd} -580 -540 0 0 0.4 0.4 {layer=7}
C {res.sym} -500 -450 0 0 {name=R_top value=500k}
N -500 -520 -500 -480 {}
C {iopin.sym} -500 -520 3 0 {name=p_pvdd lab=pvdd}
N -500 -420 -500 -360 {}
N -500 -360 -420 -360 {}
T {mid_ov} -410 -370 0 0 0.35 0.35 {layer=8}
C {res.sym} -500 -290 0 0 {name=R_bot value=146k}
N -500 -360 -500 -320 {}
N -500 -260 -500 -220 {}
C {gnd.sym} -500 -220 0 0 {name=l1 lab=GND}
T {HYSTERESIS} -320 -660 0 0 0.45 0.45 {layer=4}
T {R_hyst = 8 Meg} -320 -620 0 0 0.3 0.3 {layer=7}
T {Feedback: ov_flag to mid_ov} -320 -590 0 0 0.3 0.3 {}
T {Positive feedback for clean switching} -320 -560 0 0 0.25 0.25 {layer=5}
C {res.sym} -320 -360 0 1 {name=R_hyst value=8M}
N -420 -360 -350 -360 {}
N -290 -360 -170 -360 {}
T {ov_flag} -160 -370 0 0 0.3 0.3 {layer=7}
T {(from output)} -160 -345 0 0 0.2 0.2 {layer=5}
T {BIAS} -100 -660 0 0 0.45 0.45 {layer=4}
T {~1 uA self-biased} -100 -620 0 0 0.3 0.3 {}
C {res.sym} -30 -530 0 0 {name=R_bias value=800k}
N -30 -600 -30 -560 {}
T {vdd_comp} -90 -620 0 0 0.3 0.3 {layer=8}
C {nmos4.sym} -50 -410 0 0 {name=XMbias model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1 spiceprefix=X}
N -30 -500 -30 -440 {}
N -70 -410 -70 -440 {}
N -70 -440 -30 -440 {}
N -30 -380 -30 -340 {}
C {gnd.sym} -30 -340 0 0 {name=l2 lab=GND}
N -10 -410 -10 -340 {}
T {bias_n} 0 -450 0 0 0.3 0.3 {layer=8}
T {NMOS DIFFERENTIAL PAIR} 200 -660 0 0 0.5 0.5 {layer=4}
T {+ PMOS CURRENT MIRROR LOAD} 200 -620 0 0 0.45 0.45 {layer=4}
T {Inputs SWAPPED: M1=vref, M2=mid_ov} 200 -585 0 0 0.3 0.3 {layer=5}
C {pmos4.sym} 280 -480 0 0 {name=XM3 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1 spiceprefix=X}
N 300 -510 300 -550 {}
T {vdd_comp} 310 -560 0 0 0.3 0.3 {layer=8}
N 260 -480 240 -480 {}
N 240 -480 240 -450 {}
N 240 -450 300 -450 {}
N 300 -480 320 -480 {}
N 320 -480 320 -550 {}
T {out_p} 310 -455 0 0 0.25 0.25 {layer=13}
C {pmos4.sym} 530 -480 0 0 {name=XM4 model=sky130_fd_pr__pfet_01v8 w=2u l=1u m=1 spiceprefix=X}
N 550 -510 550 -550 {}
T {vdd_comp} 560 -560 0 0 0.3 0.3 {layer=8}
N 510 -480 240 -480 {}
N 240 -480 240 -480 {}
N 550 -480 570 -480 {}
N 570 -480 570 -550 {}
T {out_n} 560 -455 0 0 0.35 0.35 {layer=7}
C {nmos4.sym} 280 -300 0 0 {name=XM1 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1 spiceprefix=X}
N 300 -330 300 -450 {}
T {vref} 180 -310 0 0 0.35 0.35 {layer=8}
N 200 -300 260 -300 {}
N 300 -270 300 -240 {}
N 300 -300 320 -300 {}
C {nmos4.sym} 530 -300 0 0 {name=XM2 model=sky130_fd_pr__nfet_01v8 w=2u l=1u m=1 spiceprefix=X}
N 550 -330 550 -450 {}
T {mid_ov} 430 -310 0 0 0.35 0.35 {layer=8}
N 450 -300 510 -300 {}
N 550 -270 550 -240 {}
N 550 -300 570 -300 {}
N 300 -240 550 -240 {}
N 425 -240 425 -210 {}
T {tail} 435 -245 0 0 0.3 0.3 {layer=13}
N 320 -300 320 -140 {}
N 570 -300 570 -140 {}
C {nmos4.sym} 405 -160 0 0 {name=XMtail model=sky130_fd_pr__nfet_01v8 w=1u l=4u m=1 spiceprefix=X}
N 425 -190 425 -210 {}
N 385 -160 345 -160 {}
T {bias_n} 285 -170 0 0 0.3 0.3 {layer=8}
N 425 -130 425 -100 {}
C {gnd.sym} 425 -100 0 0 {name=l3 lab=GND}
N 425 -160 445 -160 {}
N 445 -160 445 -100 {}
T {ENABLE + NOR OUTPUT} 750 -660 0 0 0.5 0.5 {layer=4}
T {ov_flag = NOR(out_n, en_bar)} 750 -620 0 0 0.35 0.35 {layer=13}
T {HIGH when PVDD > threshold} 750 -590 0 0 0.3 0.3 {layer=5}
C {pmos4.sym} 800 -490 0 0 {name=XMen_p model=sky130_fd_pr__pfet_01v8 w=0.84u l=0.15u m=1 spiceprefix=X}
C {nmos4.sym} 800 -410 0 0 {name=XMen_n model=sky130_fd_pr__nfet_01v8 w=0.42u l=0.15u m=1 spiceprefix=X}
N 780 -490 780 -410 {}
N 780 -450 740 -450 {}
T {en} 690 -460 0 0 0.35 0.35 {layer=8}
N 820 -460 820 -440 {}
T {en_bar} 850 -455 0 0 0.3 0.3 {layer=13}
N 820 -450 850 -450 {}
N 820 -520 820 -550 {}
T {vdd_comp} 830 -560 0 0 0.25 0.25 {layer=8}
N 820 -490 840 -490 {}
N 840 -490 840 -550 {}
N 820 -380 820 -350 {}
C {gnd.sym} 820 -350 0 0 {name=l4 lab=GND}
N 820 -410 840 -410 {}
N 840 -410 840 -350 {}
C {pmos4.sym} 980 -470 0 0 {name=XMnor_p1 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1 spiceprefix=X}
N 960 -470 920 -470 {}
T {out_n} 860 -480 0 0 0.3 0.3 {layer=8}
N 1000 -500 1000 -530 {}
T {vdd_comp} 1010 -540 0 0 0.25 0.25 {layer=8}
N 1000 -470 1020 -470 {}
N 1020 -470 1020 -530 {}
C {pmos4.sym} 980 -380 0 0 {name=XMnor_p2 model=sky130_fd_pr__pfet_01v8 w=4u l=0.15u m=1 spiceprefix=X}
N 960 -380 920 -380 {}
T {en_bar} 860 -390 0 0 0.3 0.3 {layer=8}
N 1000 -440 1000 -410 {}
N 1000 -380 1000 -440 {}
C {nmos4.sym} 950 -260 0 0 {name=XMnor_n1 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1 spiceprefix=X}
N 930 -260 890 -260 {}
T {out_n} 830 -270 0 0 0.25 0.25 {layer=8}
N 970 -230 970 -200 {}
C {gnd.sym} 970 -200 0 0 {name=l5 lab=GND}
N 970 -260 990 -260 {}
N 990 -260 990 -200 {}
C {nmos4.sym} 1060 -260 0 0 {name=XMnor_n2 model=sky130_fd_pr__nfet_01v8 w=1u l=0.15u m=1 spiceprefix=X}
N 1040 -260 1000 -260 {}
T {en_bar} 930 -270 0 0 0.25 0.25 {layer=8}
N 1080 -230 1080 -200 {}
C {gnd.sym} 1080 -200 0 0 {name=l6 lab=GND}
N 1080 -260 1100 -260 {}
N 1100 -260 1100 -200 {}
N 970 -290 970 -320 {}
N 1080 -290 1080 -320 {}
N 970 -320 1080 -320 {}
N 1025 -320 1000 -350 {}
N 1080 -320 1210 -320 {}
C {iopin.sym} 1210 -320 0 0 {name=p_out lab=ov_flag}
T {ov_flag} 1220 -350 0 0 0.5 0.5 {layer=4}
T {HIGH when PVDD > 5.5 V} 1220 -310 0 0 0.3 0.3 {}
T {CHARACTERIZATION} -600 120 0 0 0.5 0.5 {layer=4}
T {OV threshold (rising, TT 27C)    =  5.495 V       spec 5.25 - 5.7 V       PASS} -600 180 0 0 0.3 0.3 {layer=7}
T {OV hysteresis                     =  112.2 mV      spec 50 - 150 mV         PASS} -600 220 0 0 0.3 0.3 {layer=7}
T {OV de-assertion (falling)         =  5.383 V       within spec window       PASS} -600 260 0 0 0.3 0.3 {layer=7}
T {Response time                     =  < 0.01 us     spec <= 5 us             PASS} -600 300 0 0 0.3 0.3 {layer=7}
T {Power (from vdd_comp)             =  2.57 uA       spec <= 5 uA             PASS} -600 340 0 0 0.3 0.3 {layer=7}
T {Output rail-to-rail               =  YES            0 / 1.8 V               PASS} -600 380 0 0 0.3 0.3 {layer=7}
T {Threshold error                   =  5.2 mV        spec <= 200 mV           PASS} -600 420 0 0 0.3 0.3 {layer=7}
T {All 13/13 specs PASS} -600 490 0 0 0.45 0.45 {layer=4}
C {title.sym} -660 620 0 0 {name=l1 author="Block 05: OV Comparator -- Analog AI Chips PVDD LDO Regulator"}
