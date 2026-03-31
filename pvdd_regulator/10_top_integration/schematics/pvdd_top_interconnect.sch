v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {PVDD 5V LDO REGULATOR — Top-Level Interconnect} -300 -1200 0 0 0.85 0.85 {layer=4}
T {All blocks shown as rectangles with inter-block wiring} -300 -1130 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1095 0 0 0.3 0.3 {}
T {bvdd, pvdd, gnd, avbg, ibias, svdd, en, en_ret, uv_flag, ov_flag  |  design.cir .subckt pvdd_regulator} -300 -1065 0 0 0.28 0.28 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -300 600 0 0 {name=l1 author="Claude / analog-ai-chips"}

* ============================================================
* PORT PINS
* ============================================================
T {PORT PINS} -1200 -1040 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1200 -1000 0 0 {name=p1 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1200 -960 0 0 {name=p2 lab=avbg}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1200 -920 0 0 {name=p3 lab=ibias}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1200 -880 0 0 {name=p4 lab=svdd}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1200 -840 0 0 {name=p5 lab=en}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1200 -800 0 0 {name=p6 lab=en_ret}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -900 -1000 0 0 {name=p7 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -900 -960 0 0 {name=p8 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -900 -920 0 0 {name=p9 lab=uv_flag}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -900 -880 0 0 {name=p10 lab=ov_flag}
L 8 -900 -600 -740 -600 {}
L 8 -740 -600 -740 -480 {}
L 8 -740 -480 -900 -480 {}
L 8 -900 -480 -900 -600 {}
T {LS_EN} -820 -555 0 0 0.35 0.35 {layer=8}
T {level_shifter_up} -820 -530 0 0 0.2 0.2 {layer=13}
T {en} -895 -570 0 0 0.18 0.18 {layer=7}
T {svdd} -895 -540 0 0 0.18 0.18 {layer=7}
T {gnd} -895 -510 0 0 0.18 0.18 {layer=8}
T {en_bvdd} -745 -540 0 0 0.18 0.18 {layer=4}
L 8 -650 -600 -470 -600 {}
L 8 -470 -600 -470 -480 {}
L 8 -470 -480 -650 -480 {}
L 8 -650 -480 -650 -600 {}
T {SOFT-START} -560 -555 0 0 0.35 0.35 {layer=8}
T {Rss=200k Css=30n} -560 -530 0 0 0.2 0.2 {layer=13}
T {avbg} -645 -560 0 0 0.18 0.18 {layer=8}
T {vref_ss} -475 -540 0 0 0.18 0.18 {layer=8}
T {gnd} -560 -485 0 0 0.18 0.18 {layer=8}
L 5 -380 -600 -180 -600 {}
L 5 -180 -600 -180 -480 {}
L 5 -180 -480 -380 -480 {}
L 5 -380 -480 -380 -600 {}
T {ERROR AMP} -280 -555 0 0 0.35 0.35 {layer=5}
T {error_amp} -280 -530 0 0 0.2 0.2 {layer=13}
T {vref_ss} -375 -570 0 0 0.18 0.18 {layer=8}
T {vfb} -375 -540 0 0 0.18 0.18 {layer=5}
T {ibias} -375 -510 0 0 0.18 0.18 {layer=8}
T {ea_out} -185 -560 0 0 0.18 0.18 {layer=8}
T {pvdd} -320 -595 0 0 0.18 0.18 {layer=5}
T {ea_en} -240 -595 0 0 0.18 0.18 {layer=8}
T {gnd} -280 -485 0 0 0.18 0.18 {layer=8}
L 5 -100 -600 80 -600 {}
L 5 80 -600 80 -480 {}
L 5 80 -480 -100 -480 {}
L 5 -100 -480 -100 -600 {}
T {COMP} -10 -555 0 0 0.35 0.35 {layer=5}
T {compensation} -10 -530 0 0 0.2 0.2 {layer=13}
T {ea_out} -95 -560 0 0 0.18 0.18 {layer=8}
T {pvdd} -40 -595 0 0 0.18 0.18 {layer=5}
T {gnd} -10 -485 0 0 0.18 0.18 {layer=8}
L 4 180 -600 380 -600 {}
L 4 380 -600 380 -480 {}
L 4 380 -480 180 -480 {}
L 4 180 -480 180 -600 {}
T {PASS DEV} 280 -555 0 0 0.35 0.35 {layer=4}
T {XM_pass} 280 -530 0 0 0.2 0.2 {layer=13}
T {gate} 185 -540 0 0 0.18 0.18 {layer=8}
T {bvdd} 240 -595 0 0 0.18 0.18 {layer=4}
T {pvdd} 280 -485 0 0 0.18 0.18 {layer=5}
L 5 480 -600 600 -600 {}
L 5 600 -600 600 -480 {}
L 5 600 -480 480 -480 {}
L 5 480 -480 480 -600 {}
T {Cload} 540 -555 0 0 0.35 0.35 {layer=5}
T {200pF} 540 -530 0 0 0.2 0.2 {layer=13}
T {pvdd} 485 -560 0 0 0.18 0.18 {layer=5}
T {gnd} 540 -485 0 0 0.18 0.18 {layer=8}
L 7 -700 -380 -500 -380 {}
L 7 -500 -380 -500 -260 {}
L 7 -500 -260 -700 -260 {}
L 7 -700 -260 -700 -380 {}
T {UV COMP} -600 -335 0 0 0.35 0.35 {layer=7}
T {uv_comparator} -600 -310 0 0 0.2 0.2 {layer=13}
T {pvdd} -695 -350 0 0 0.18 0.18 {layer=5}
T {avbg} -695 -320 0 0 0.18 0.18 {layer=8}
T {uv_flag} -505 -340 0 0 0.18 0.18 {layer=7}
T {svdd} -640 -375 0 0 0.18 0.18 {layer=7}
T {uvov_en} -560 -375 0 0 0.18 0.18 {layer=8}
T {gnd} -600 -265 0 0 0.18 0.18 {layer=8}
L 7 -400 -380 -200 -380 {}
L 7 -200 -380 -200 -260 {}
L 7 -200 -260 -400 -260 {}
L 7 -400 -260 -400 -380 {}
T {OV COMP} -300 -335 0 0 0.35 0.35 {layer=7}
T {ov_comparator} -300 -310 0 0 0.2 0.2 {layer=13}
T {pvdd} -395 -350 0 0 0.18 0.18 {layer=5}
T {avbg} -395 -320 0 0 0.18 0.18 {layer=8}
T {ov_flag} -205 -340 0 0 0.18 0.18 {layer=7}
T {svdd} -340 -375 0 0 0.18 0.18 {layer=7}
T {uvov_en} -260 -375 0 0 0.18 0.18 {layer=8}
T {gnd} -300 -265 0 0 0.18 0.18 {layer=8}
L 4 -100 -380 80 -380 {}
L 4 80 -380 80 -260 {}
L 4 80 -260 -100 -260 {}
L 4 -100 -260 -100 -380 {}
T {ZENER} -10 -335 0 0 0.35 0.35 {layer=4}
T {zener_clamp} -10 -310 0 0 0.2 0.2 {layer=13}
T {pvdd} -95 -340 0 0 0.18 0.18 {layer=5}
T {gnd} -10 -265 0 0 0.18 0.18 {layer=8}
L 4 180 -380 380 -380 {}
L 4 380 -380 380 -260 {}
L 4 380 -260 180 -260 {}
L 4 180 -260 180 -380 {}
T {ILIM} 280 -335 0 0 0.35 0.35 {layer=4}
T {current_limiter} 280 -310 0 0 0.2 0.2 {layer=13}
T {gate} 185 -350 0 0 0.18 0.18 {layer=8}
T {bvdd} 185 -320 0 0 0.18 0.18 {layer=4}
T {ilim_flag} 375 -340 0 0 0.18 0.18 {layer=8}
T {pvdd} 280 -375 0 0 0.18 0.18 {layer=5}
T {gnd} 280 -265 0 0 0.18 0.18 {layer=8}
L 8 -700 -160 -350 -160 {}
L 8 -350 -160 -350 -20 {}
L 8 -350 -20 -700 -20 {}
L 8 -700 -20 -700 -160 {}
T {MODE CONTROL} -525 -105 0 0 0.35 0.35 {layer=8}
T {mode_control} -525 -80 0 0 0.2 0.2 {layer=13}
T {bvdd} -695 -130 0 0 0.18 0.18 {layer=4}
T {pvdd} -695 -110 0 0 0.18 0.18 {layer=5}
T {svdd} -695 -90 0 0 0.18 0.18 {layer=7}
T {gnd} -695 -70 0 0 0.18 0.18 {layer=8}
T {avbg} -695 -50 0 0 0.18 0.18 {layer=8}
T {bypass_en} -355 -135 0 0 0.18 0.18 {layer=8}
T {mc_ea_en} -355 -115 0 0 0.18 0.18 {layer=8}
T {ref_sel} -355 -95 0 0 0.18 0.18 {layer=8}
T {uvov_en} -355 -75 0 0 0.18 0.18 {layer=8}
T {ilim_en} -355 -55 0 0 0.18 0.18 {layer=8}
T {pass_off} -355 -35 0 0 0.18 0.18 {layer=8}
T {en_ret} -600 -155 0 0 0.18 0.18 {layer=8}
L 4 -200 -160 20 -160 {}
L 4 20 -160 20 -20 {}
L 4 20 -20 -200 -20 {}
L 4 -200 -20 -200 -160 {}
T {STARTUP} -90 -105 0 0 0.35 0.35 {layer=4}
T {startup} -90 -80 0 0 0.2 0.2 {layer=13}
T {bvdd} -195 -130 0 0 0.18 0.18 {layer=4}
T {pvdd} -195 -110 0 0 0.18 0.18 {layer=5}
T {gnd} -195 -90 0 0 0.18 0.18 {layer=8}
T {ea_out} -195 -60 0 0 0.18 0.18 {layer=8}
T {gate} 15 -130 0 0 0.18 0.18 {layer=8}
T {startup_done} 15 -100 0 0 0.18 0.18 {layer=8}
T {ea_en} 15 -70 0 0 0.18 0.18 {layer=8}
T {vref} -140 -155 0 0 0.18 0.18 {layer=8}
L 5 180 -160 380 -160 {}
L 5 380 -160 380 -20 {}
L 5 380 -20 180 -20 {}
L 5 180 -20 180 -160 {}
T {FEEDBACK} 280 -105 0 0 0.35 0.35 {layer=5}
T {feedback_network} 280 -80 0 0 0.2 0.2 {layer=13}
T {pvdd} 185 -120 0 0 0.18 0.18 {layer=5}
T {vfb} 375 -100 0 0 0.18 0.18 {layer=5}
T {gnd} 280 -25 0 0 0.18 0.18 {layer=8}
* ============================================================
* INTER-BLOCK WIRING
* ============================================================
T {INTER-BLOCK WIRING} -1100 -850 0 0 0.35 0.35 {layer=4}
N -470 -540 -380 -570 {lab=vref_ss}
N -180 -560 -100 -560 {lab=ea_out}
N -180 -560 -180 -60 {lab=ea_out}
N -180 -60 -200 -60 {lab=ea_out}
N 20 -130 120 -130 {lab=gate}
N 120 -130 120 -540 {lab=gate}
N 120 -540 180 -540 {lab=gate}
N 120 -350 180 -350 {lab=gate}
N 380 -100 450 -100 {lab=vfb}
N 450 -100 450 -450 {lab=vfb}
N 450 -450 -420 -450 {lab=vfb}
N -420 -450 -420 -540 {lab=vfb}
N -420 -540 -380 -540 {lab=vfb}
N 280 -480 280 -450 {lab=pvdd}
N -700 -430 480 -430 {lab=pvdd}
T {pvdd} -200 -440 0 0 0.28 0.28 {layer=5}
N 180 -120 160 -120 {lab=pvdd}
N 160 -120 160 -430 {lab=pvdd}
N 480 -560 470 -560 {lab=pvdd}
N 470 -560 470 -430 {lab=pvdd}
N -700 -350 -720 -350 {lab=pvdd}
N -720 -350 -720 -430 {lab=pvdd}
N -400 -350 -420 -350 {lab=pvdd}
N -420 -350 -420 -430 {lab=pvdd}
N -100 -340 -120 -340 {lab=pvdd}
N -120 -340 -120 -430 {lab=pvdd}
N -900 -630 380 -630 {lab=bvdd}
T {bvdd} -600 -640 0 0 0.28 0.28 {layer=4}
N 280 -600 280 -630 {lab=bvdd}
N 240 -320 240 -630 {lab=bvdd}
N -200 -130 -230 -130 {lab=bvdd}
N -230 -130 -230 -630 {lab=bvdd}
N -700 -130 -720 -130 {lab=bvdd}
N -720 -130 -720 -630 {lab=bvdd}
N 20 -70 60 -70 {lab=ea_en}
N 60 -70 60 -660 {lab=ea_en}
N 60 -660 -240 -660 {lab=ea_en}
N -240 -660 -240 -600 {lab=ea_en}
N 20 -100 80 -100 {lab=startup_done}
N -900 40 600 40 {lab=gnd}
T {gnd} -200 30 0 0 0.28 0.28 {layer=8}
N -700 -410 -400 -410 {lab=svdd}
T {svdd} -550 -420 0 0 0.28 0.28 {layer=7}
N -640 -380 -640 -410 {lab=svdd}
N -340 -380 -340 -410 {lab=svdd}
N -350 -160 -350 -260 {lab=uvov_en}
N -350 -295 -560 -295 {lab=uvov_en}
N -560 -295 -560 -380 {lab=uvov_en}
N -350 -295 -260 -295 {lab=uvov_en}
N -260 -295 -260 -380 {lab=uvov_en}
N -650 -560 -670 -560 {lab=avbg}
N -670 -560 -670 -430 {lab=avbg}
N -700 -320 -740 -320 {lab=avbg}
N -400 -320 -440 -320 {lab=avbg}
N -380 -510 -420 -510 {lab=ibias}
N -500 -340 -480 -340 {lab=uv_flag}
N -200 -340 -180 -340 {lab=ov_flag}
N -740 -540 -720 -540 {lab=en_bvdd}
N -900 -570 -920 -570 {lab=en}
L 4 -950 -680 650 -680 {dash=5}
L 4 650 -680 650 80 {dash=5}
L 4 650 80 -950 80 {dash=5}
L 4 -950 80 -950 -680 {dash=5}
