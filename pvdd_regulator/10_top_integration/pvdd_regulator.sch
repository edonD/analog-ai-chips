v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {PVDD 5V LDO Regulator — Top-Level Integration} -2200 -2600 0 0 1.0 1.0 {layer=4}
T {SkyWater SKY130A  |  Block 10  |  11 Sub-blocks + Top-Level Passives} -2200 -2530 0 0 0.4 0.4 {layer=8}
T {.subckt pvdd_regulator bvdd pvdd gnd avbg ibias svdd en en_ret uv_flag ov_flag startup_done} -2200 -2490 0 0 0.28 0.28 {layer=13}
T {v12: FIX-21 Miller comp Cc=40p Rc=5k | FIX-24 Cfb removed | FIX-25 Cff=22p | FIX-26 snubber removed | FIX-27 Rgate=1k} -2200 -2460 0 0 0.25 0.25 {}

C {/usr/share/xschem/xschem_library/devices/title.sym} -2200 2400 0 0 {name=l1 author="PVDD 5V LDO Regulator -- Top-Level Integration -- Analog AI Chips"}

* ============================================================
* EXTERNAL PORT PINS
* ============================================================
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -2200 -2200 0 0 {name=p_bvdd lab=bvdd}
T {BVDD (5.4-10.5V)} -2130 -2210 0 0 0.32 0.32 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -2200 -2100 0 0 {name=p_avbg lab=avbg}
T {AVBG (1.226V bandgap ref)} -2130 -2110 0 0 0.32 0.32 {layer=13}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -2200 -2000 0 0 {name=p_ibias lab=ibias}
T {IBIAS (1uA)} -2130 -2010 0 0 0.32 0.32 {layer=13}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -2200 -1900 0 0 {name=p_svdd lab=svdd}
T {SVDD (2.2V)} -2130 -1910 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -2200 -1800 0 0 {name=p_en lab=en}
T {EN (active HIGH, SVDD domain)} -2130 -1810 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -2200 -1700 0 0 {name=p_en_ret lab=en_ret}
T {EN_RET (retention mode)} -2130 -1710 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 3400 -2200 0 0 {name=p_pvdd lab=pvdd}
T {PVDD (5.0V regulated)} 3260 -2210 0 0 0.35 0.35 {layer=5}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 3400 -2100 0 0 {name=p_uv_flag lab=uv_flag}
T {UV_FLAG (SVDD domain)} 3260 -2110 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 3400 -2000 0 0 {name=p_ov_flag lab=ov_flag}
T {OV_FLAG (SVDD domain)} 3260 -2010 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 3400 -1900 0 0 {name=p_startup_done lab=startup_done}
T {STARTUP_DONE} 3260 -1910 0 0 0.32 0.32 {layer=5}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -2200 -1500 0 0 {name=p_gnd lab=gnd}
T {GND} -2140 -1510 0 0 0.35 0.35 {}

* ============================================================
* BLOCK 01: PASS DEVICE  (XM_pass)
* Source=BVDD, Drain=PVDD, Gate from error amp / startup
* ============================================================
L 4 1400 -2000 2100 -2000 {}
L 4 2100 -2000 2100 -1700 {}
L 4 2100 -1700 1400 -1700 {}
L 4 1400 -1700 1400 -2000 {}
L 4 1398 -2002 2102 -2002 {}
L 4 2102 -2002 2102 -1698 {}
L 4 2102 -1698 1398 -1698 {}
L 4 1398 -1698 1398 -2002 {}
T {Block 01} 1650 -1985 0 0 0.22 0.22 {layer=13}
T {Pass Device} 1630 -1960 0 0 0.45 0.45 {layer=4}
T {PMOS 10x100u/0.5u} 1630 -1930 0 0 0.22 0.22 {layer=13}
T {XM_pass} 1630 -1905 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -1870 0 0 {name=lp01g sig_type=std_logic lab=gate}
T {gate} 1412 -1880 0 0 0.25 0.25 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1750 -2000 3 0 {name=lp01s sig_type=std_logic lab=bvdd}
T {bvdd (S)} 1700 -1995 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2100 -1850 2 0 {name=lp01d sig_type=std_logic lab=pvdd}
T {pvdd (D)} 2020 -1860 0 0 0.25 0.25 {layer=5}

* ============================================================
* SOFT-START RC FILTER: avbg -> Rss -> vref_ss -> Css -> gnd
*   XRss: sky130_fd_pr__res_xhigh_po W=2u L=100u (100k on-chip)
*   Css:  22nF EXTERNAL capacitor
*   tau = 2.2ms
* ============================================================
L 13 -1600 -1300 -900 -1300 {}
L 13 -900 -1300 -900 -1050 {}
L 13 -900 -1050 -1600 -1050 {}
L 13 -1600 -1050 -1600 -1300 {}
T {Soft-Start RC} -1360 -1285 0 0 0.35 0.35 {layer=13}
T {XRss: xhigh_po W=2 L=100} -1588 -1260 0 0 0.22 0.22 {}
T {Css: 22nF (EXTERNAL)} -1588 -1240 0 0 0.22 0.22 {}
T {tau = Rss*Css = 2.2ms} -1588 -1220 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1600 -1180 0 0 {name=lp_ss1 sig_type=std_logic lab=avbg}
T {avbg} -1588 -1190 0 0 0.25 0.25 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -900 -1180 2 0 {name=lp_ss2 sig_type=std_logic lab=vref_ss}
T {vref_ss} -990 -1190 0 0 0.25 0.25 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1250 -1050 1 0 {name=lp_ss3 sig_type=std_logic lab=gnd}
T {gnd} -1260 -1060 0 0 0.22 0.22 {}

C {sky130_fd_pr/res_xhigh_po.sym} -1300 -1180 0 0 {name=XRss W=2 L=100 model=sky130_fd_pr__res_xhigh_po}
N -1400 -1180 -1600 -1180 {lab=avbg}
N -1200 -1180 -1050 -1180 {lab=vref_ss}

C {/usr/share/xschem/xschem_library/devices/capa.sym} -1050 -1100 0 0 {name=Css value=22n}
N -1050 -1180 -1050 -1130 {lab=vref_ss}
N -1050 -1070 -1050 -1050 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1050 -1050 1 0 {name=lp_css_g sig_type=std_logic lab=gnd}

* ============================================================
* BLOCK 00: ERROR AMPLIFIER  (XEA)
* Two-stage Miller OTA, BVDD-powered
* Ports: vref_ss vfb ea_out gnd ibias ea_en bvdd
* ============================================================
L 5 -600 -1700 300 -1700 {}
L 5 300 -1700 300 -1350 {}
L 5 300 -1350 -600 -1350 {}
L 5 -600 -1350 -600 -1700 {}
L 5 -602 -1702 302 -1702 {}
L 5 302 -1702 302 -1348 {}
L 5 302 -1348 -602 -1348 {}
L 5 -602 -1348 -602 -1702 {}
T {Block 00} -210 -1685 0 0 0.22 0.22 {layer=13}
T {Error Amplifier} -230 -1660 0 0 0.45 0.45 {layer=5}
T {Two-stage Miller OTA} -230 -1630 0 0 0.22 0.22 {layer=13}
T {BVDD-powered, Cc=40pF Rc=5k} -230 -1610 0 0 0.22 0.22 {layer=13}
T {XEA} -230 -1590 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -600 -1600 0 0 {name=lp00vr sig_type=std_logic lab=vref_ss}
T {vref_ss (+)} -588 -1610 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -600 -1540 0 0 {name=lp00vf sig_type=std_logic lab=vfb}
T {vfb (-)} -588 -1550 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -1540 2 0 {name=lp00eo sig_type=std_logic lab=ea_out}
T {ea_out} 230 -1550 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -600 -1470 0 0 {name=lp00gn sig_type=std_logic lab=gnd}
T {gnd} -588 -1480 0 0 0.23 0.23 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -600 -1410 0 0 {name=lp00ib sig_type=std_logic lab=ibias}
T {ibias} -588 -1420 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -1470 2 0 {name=lp00en sig_type=std_logic lab=ea_en}
T {ea_en} 230 -1480 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 -1700 3 0 {name=lp00bv sig_type=std_logic lab=bvdd}
T {bvdd} -170 -1698 0 0 0.22 0.22 {layer=4}

* ============================================================
* BLOCK 02: FEEDBACK NETWORK  (XFB)
* Resistive divider: pvdd -> vfb ~ 1.226V
* Ports: pvdd vfb gnd
* ============================================================
L 5 600 -1500 1200 -1500 {}
L 5 1200 -1500 1200 -1250 {}
L 5 1200 -1250 600 -1250 {}
L 5 600 -1250 600 -1500 {}
L 5 598 -1502 1202 -1502 {}
L 5 1202 -1502 1202 -1248 {}
L 5 1202 -1248 598 -1248 {}
L 5 598 -1248 598 -1502 {}
T {Block 02} 825 -1485 0 0 0.22 0.22 {layer=13}
T {Feedback Network} 800 -1460 0 0 0.4 0.4 {layer=5}
T {Resistive divider} 800 -1435 0 0 0.22 0.22 {layer=13}
T {XFB} 800 -1415 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -1400 0 0 {name=lp02pv sig_type=std_logic lab=pvdd}
T {pvdd} 612 -1410 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1200 -1400 2 0 {name=lp02vf sig_type=std_logic lab=vfb}
T {vfb} 1140 -1410 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 900 -1250 1 0 {name=lp02gn sig_type=std_logic lab=gnd}
T {gnd} 890 -1260 0 0 0.22 0.22 {}

* FIX-25: Feedforward cap Cff=22pF across R_TOP (pvdd to vfb)
* Zero at ~20kHz boosts phase margin by ~49 degrees
C {/usr/share/xschem/xschem_library/devices/capa.sym} 900 -1600 0 0 {name=Cff value=22p}
N 900 -1630 600 -1630 {lab=pvdd}
N 900 -1570 1200 -1570 {lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -1630 0 0 {name=lp_cff1 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1200 -1570 2 0 {name=lp_cff2 sig_type=std_logic lab=vfb}
T {Cff 22pF (FIX-25)} 920 -1610 0 0 0.22 0.22 {layer=13}

* ============================================================
* BLOCK 03: COMPENSATION  (XCOMP)
* Placeholder — all comp inside EA (Cc=40pF, Rc=5k from FIX-21)
* Ports: ea_out pvdd gnd
* ============================================================
L 8 600 -1100 1200 -1100 {}
L 8 1200 -1100 1200 -900 {}
L 8 1200 -900 600 -900 {}
L 8 600 -900 600 -1100 {}
T {Block 03} 825 -1085 0 0 0.22 0.22 {layer=13}
T {Compensation} 800 -1060 0 0 0.35 0.35 {layer=8}
T {(empty placeholder)} 800 -1035 0 0 0.22 0.22 {layer=13}
T {XCOMP} 800 -1015 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -1000 0 0 {name=lp03eo sig_type=std_logic lab=ea_out}
T {ea_out} 612 -1010 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1200 -1000 2 0 {name=lp03pv sig_type=std_logic lab=pvdd}
T {pvdd} 1140 -1010 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 900 -900 1 0 {name=lp03gn sig_type=std_logic lab=gnd}
T {gnd} 890 -910 0 0 0.22 0.22 {}

* ============================================================
* BLOCK 04: CURRENT LIMITER  (XILIM)
* Bandgap-referenced, always active
* Ports: gate bvdd pvdd gnd ilim_flag ibias_ilim
* ============================================================
L 4 1400 -1550 2100 -1550 {}
L 4 2100 -1550 2100 -1250 {}
L 4 2100 -1250 1400 -1250 {}
L 4 1400 -1250 1400 -1550 {}
L 4 1398 -1552 2102 -1552 {}
L 4 2102 -1552 2102 -1248 {}
L 4 2102 -1248 1398 -1248 {}
L 4 1398 -1248 1398 -1552 {}
T {Block 04} 1650 -1535 0 0 0.22 0.22 {layer=13}
T {Current Limiter} 1630 -1510 0 0 0.4 0.4 {layer=4}
T {Bandgap-ref, always active} 1630 -1480 0 0 0.22 0.22 {layer=13}
T {XILIM} 1630 -1460 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -1440 0 0 {name=lp04gt sig_type=std_logic lab=gate}
T {gate} 1412 -1450 0 0 0.23 0.23 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -1380 0 0 {name=lp04bv sig_type=std_logic lab=bvdd}
T {bvdd} 1412 -1390 0 0 0.23 0.23 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2100 -1440 2 0 {name=lp04pv sig_type=std_logic lab=pvdd}
T {pvdd} 2040 -1450 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1750 -1250 1 0 {name=lp04gn sig_type=std_logic lab=gnd}
T {gnd} 1740 -1260 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2100 -1380 2 0 {name=lp04if sig_type=std_logic lab=ilim_flag}
T {ilim_flag} 2010 -1390 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2100 -1320 2 0 {name=lp04ib sig_type=std_logic lab=ibias_ilim}
T {ibias_ilim} 2000 -1330 0 0 0.23 0.23 {layer=13}

* Dedicated bias for current limiter (FIX-15): 1uA
C {/usr/share/xschem/xschem_library/devices/isource.sym} 2400 -1400 0 0 {name=Iibias_ilim value=1u}
N 2400 -1430 2400 -1460 {lab=ibias_ilim}
N 2400 -1370 2400 -1340 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -1460 3 0 {name=lp_iilim1 sig_type=std_logic lab=ibias_ilim}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -1340 1 0 {name=lp_iilim2 sig_type=std_logic lab=gnd}
T {Iibias_ilim 1uA} 2420 -1420 0 0 0.22 0.22 {layer=13}
T {(FIX-15: dedicated)} 2420 -1400 0 0 0.18 0.18 {}

* ============================================================
* BLOCK 05: UV COMPARATOR  (XUV)
* Ports: pvdd avbg uv_flag svdd gnd uvov_en
* ============================================================
L 7 2400 -800 3100 -800 {}
L 7 3100 -800 3100 -500 {}
L 7 3100 -500 2400 -500 {}
L 7 2400 -500 2400 -800 {}
L 7 2398 -802 3102 -802 {}
L 7 3102 -802 3102 -498 {}
L 7 3102 -498 2398 -498 {}
L 7 2398 -498 2398 -802 {}
T {Block 05a} 2650 -785 0 0 0.22 0.22 {layer=13}
T {UV Comparator} 2630 -760 0 0 0.4 0.4 {layer=7}
T {XUV} 2630 -735 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -700 0 0 {name=lp05upv sig_type=std_logic lab=pvdd}
T {pvdd} 2412 -710 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -640 0 0 {name=lp05uav sig_type=std_logic lab=avbg}
T {avbg} 2412 -650 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 3100 -700 2 0 {name=lp05uuf sig_type=std_logic lab=uv_flag}
T {uv_flag} 3020 -710 0 0 0.23 0.23 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2750 -800 3 0 {name=lp05usv sig_type=std_logic lab=svdd}
T {svdd} 2740 -798 0 0 0.22 0.22 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2750 -500 1 0 {name=lp05ugn sig_type=std_logic lab=gnd}
T {gnd} 2740 -510 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -580 0 0 {name=lp05uen sig_type=std_logic lab=uvov_en}
T {uvov_en} 2412 -590 0 0 0.23 0.23 {layer=13}

* ============================================================
* BLOCK 05: OV COMPARATOR  (XOV)
* Ports: pvdd avbg ov_flag svdd gnd uvov_en
* ============================================================
L 7 2400 -400 3100 -400 {}
L 7 3100 -400 3100 -100 {}
L 7 3100 -100 2400 -100 {}
L 7 2400 -100 2400 -400 {}
L 7 2398 -402 3102 -402 {}
L 7 3102 -402 3102 -98 {}
L 7 3102 -98 2398 -98 {}
L 7 2398 -98 2398 -402 {}
T {Block 05b} 2650 -385 0 0 0.22 0.22 {layer=13}
T {OV Comparator} 2630 -360 0 0 0.4 0.4 {layer=7}
T {XOV} 2630 -335 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -300 0 0 {name=lp05opv sig_type=std_logic lab=pvdd}
T {pvdd} 2412 -310 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -240 0 0 {name=lp05oav sig_type=std_logic lab=avbg}
T {avbg} 2412 -250 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 3100 -300 2 0 {name=lp05oof sig_type=std_logic lab=ov_flag}
T {ov_flag} 3020 -310 0 0 0.23 0.23 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2750 -400 3 0 {name=lp05osv sig_type=std_logic lab=svdd}
T {svdd} 2740 -398 0 0 0.22 0.22 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2750 -100 1 0 {name=lp05ogn sig_type=std_logic lab=gnd}
T {gnd} 2740 -110 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -180 0 0 {name=lp05oen sig_type=std_logic lab=uvov_en}
T {uvov_en} 2412 -190 0 0 0.23 0.23 {layer=13}

* ============================================================
* BLOCK 07: MOS VOLTAGE CLAMP  (XZC)
* Overvoltage protection on PVDD
* Ports: pvdd gnd ibias
* ============================================================
L 5 2400 -1100 3100 -1100 {}
L 5 3100 -1100 3100 -900 {}
L 5 3100 -900 2400 -900 {}
L 5 2400 -900 2400 -1100 {}
L 5 2398 -1102 3102 -1102 {}
L 5 3102 -1102 3102 -898 {}
L 5 3102 -898 2398 -898 {}
L 5 2398 -898 2398 -1102 {}
T {Block 07} 2650 -1085 0 0 0.22 0.22 {layer=13}
T {MOS Voltage Clamp} 2620 -1060 0 0 0.35 0.35 {layer=5}
T {XZC} 2620 -1035 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -1020 0 0 {name=lp07pv sig_type=std_logic lab=pvdd}
T {pvdd} 2412 -1030 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2750 -900 1 0 {name=lp07gn sig_type=std_logic lab=gnd}
T {gnd} 2740 -910 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2400 -960 0 0 {name=lp07ib sig_type=std_logic lab=ibias}
T {ibias} 2412 -970 0 0 0.23 0.23 {layer=13}

* ============================================================
* BLOCK 08: MODE CONTROL  (XMC)
* BVDD ladder -> sequenced enables
* Ports: bvdd pvdd svdd gnd en_ret bypass_en mc_ea_en ref_sel uvov_en ilim_en pass_off
* ============================================================
L 4 -1800 -800 -800 -800 {}
L 4 -800 -800 -800 -300 {}
L 4 -800 -300 -1800 -300 {}
L 4 -1800 -300 -1800 -800 {}
L 4 -1802 -802 -798 -802 {}
L 4 -798 -802 -798 -298 {}
L 4 -798 -298 -1802 -298 {}
L 4 -1802 -298 -1802 -802 {}
T {Block 08} -1400 -785 0 0 0.22 0.22 {layer=13}
T {Mode Control} -1420 -760 0 0 0.45 0.45 {layer=4}
T {BVDD ladder + sequencing} -1420 -730 0 0 0.22 0.22 {layer=13}
T {XMC} -1420 -710 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1800 -680 0 0 {name=lp08bv sig_type=std_logic lab=bvdd}
T {bvdd} -1788 -690 0 0 0.23 0.23 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1800 -620 0 0 {name=lp08pv sig_type=std_logic lab=pvdd}
T {pvdd} -1788 -630 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1800 -560 0 0 {name=lp08sv sig_type=std_logic lab=svdd}
T {svdd} -1788 -570 0 0 0.23 0.23 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1300 -300 1 0 {name=lp08gn sig_type=std_logic lab=gnd}
T {gnd} -1310 -310 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1800 -500 0 0 {name=lp08er sig_type=std_logic lab=en_ret}
T {en_ret} -1788 -510 0 0 0.23 0.23 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -800 -680 2 0 {name=lp08by sig_type=std_logic lab=bypass_en}
T {bypass_en} -890 -690 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -800 -620 2 0 {name=lp08me sig_type=std_logic lab=mc_ea_en}
T {mc_ea_en} -890 -630 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -800 -560 2 0 {name=lp08rs sig_type=std_logic lab=ref_sel}
T {ref_sel} -890 -570 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -800 -500 2 0 {name=lp08ue sig_type=std_logic lab=uvov_en}
T {uvov_en} -890 -510 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -800 -440 2 0 {name=lp08ie sig_type=std_logic lab=ilim_en}
T {ilim_en} -890 -450 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -800 -380 2 0 {name=lp08po sig_type=std_logic lab=pass_off}
T {pass_off} -890 -390 0 0 0.23 0.23 {layer=4}

* ============================================================
* BLOCK 09: STARTUP CIRCUIT  (XSU)
* Direct gate drive, no common-gate level shifter
* Ports: bvdd pvdd gate gnd avbg startup_done su_ea_en ea_out
* ============================================================
L 4 -600 -1200 300 -1200 {}
L 4 300 -1200 300 -900 {}
L 4 300 -900 -600 -900 {}
L 4 -600 -900 -600 -1200 {}
L 4 -602 -1202 302 -1202 {}
L 4 302 -1202 302 -898 {}
L 4 302 -898 -602 -898 {}
L 4 -602 -898 -602 -1202 {}
T {Block 09} -210 -1185 0 0 0.22 0.22 {layer=13}
T {Startup Circuit} -230 -1160 0 0 0.4 0.4 {layer=4}
T {Rgate=1k (FIX-27)} -230 -1135 0 0 0.22 0.22 {layer=13}
T {XSU} -230 -1115 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -600 -1100 0 0 {name=lp09bv sig_type=std_logic lab=bvdd}
T {bvdd} -588 -1110 0 0 0.23 0.23 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -600 -1040 0 0 {name=lp09pv sig_type=std_logic lab=pvdd}
T {pvdd} -588 -1050 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -1100 2 0 {name=lp09gt sig_type=std_logic lab=gate}
T {gate} 240 -1110 0 0 0.23 0.23 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -150 -900 1 0 {name=lp09gn sig_type=std_logic lab=gnd}
T {gnd} -160 -910 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -600 -980 0 0 {name=lp09av sig_type=std_logic lab=avbg}
T {avbg} -588 -990 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -1040 2 0 {name=lp09sd sig_type=std_logic lab=startup_done}
T {startup_done} 200 -1050 0 0 0.23 0.23 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -980 2 0 {name=lp09se sig_type=std_logic lab=su_ea_en}
T {su_ea_en} 220 -990 0 0 0.23 0.23 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -600 -920 0 0 {name=lp09eo sig_type=std_logic lab=ea_out}
T {ea_out} -588 -930 0 0 0.23 0.23 {layer=13}

* ============================================================
* EA ENABLE: BVDD pullup resistor (always ON for startup robustness)
*   Ren_ea = 100 ohm, bvdd -> ea_en
*   mc_ea_en left floating (unused for ea_en)
* ============================================================
C {/usr/share/xschem/xschem_library/devices/res.sym} 500 -800 0 0 {name=Ren_ea value=100}
N 500 -830 500 -860 {lab=bvdd}
N 500 -770 500 -740 {lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -860 3 0 {name=lp_rea1 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -740 1 0 {name=lp_rea2 sig_type=std_logic lab=ea_en}
T {Ren_ea 100R} 520 -820 0 0 0.22 0.22 {layer=13}
T {ea_en always HIGH} 520 -800 0 0 0.18 0.18 {}

* ============================================================
* POR GATE PULLUP: pass_off -> inverter -> gate pullup PFET
*   During POR: pass_off=HIGH -> pass_off_b=LOW -> gate=BVDD -> pass OFF
*   After POR: pass_off=LOW -> pass_off_b=HIGH -> gate free for EA
*   XMpo_invp: PFET W=40u L=2u (FIX-14: widened from 4u)
*   XMpo_invn: NFET W=2u L=2u
*   XMgate_pu: PFET W=4u L=2u (FIX-14: weakened from W=10u L=1u)
* ============================================================
L 4 -400 -500 400 -500 {}
L 4 400 -500 400 -100 {}
L 4 400 -100 -400 -100 {}
L 4 -400 -100 -400 -500 {}
T {POR Gate Pullup Logic} -120 -485 0 0 0.35 0.35 {layer=4}
T {pass_off inverter + PFET pullup} -120 -460 0 0 0.22 0.22 {layer=13}

* Inverter PFET (XMpo_invp): D=pass_off_b G=pass_off S=bvdd B=bvdd
C {sky130_fd_pr/pfet_g5v0d10v5.sym} -200 -350 0 0 {name=XMpo_invp W=40e-6 L=2e-6 nf=1 mult=1
model=sky130_fd_pr__pfet_g5v0d10v5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -220 -350 0 0 {name=lp_invp_g sig_type=std_logic lab=pass_off}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -380 2 0 {name=lp_invp_d sig_type=std_logic lab=pass_off_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -320 2 0 {name=lp_invp_s sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -350 2 0 {name=lp_invp_b sig_type=std_logic lab=bvdd}
T {XMpo_invp} -280 -430 0 0 0.22 0.22 {layer=13}
T {PFET W=40u L=2u} -280 -410 0 0 0.18 0.18 {}

* Inverter NFET (XMpo_invn): D=pass_off_b G=pass_off S=gnd B=gnd
C {sky130_fd_pr/nfet_g5v0d10v5.sym} -200 -200 0 0 {name=XMpo_invn W=2e-6 L=2e-6 nf=1 mult=1
model=sky130_fd_pr__nfet_g5v0d10v5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -220 -200 0 0 {name=lp_invn_g sig_type=std_logic lab=pass_off}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -230 2 0 {name=lp_invn_d sig_type=std_logic lab=pass_off_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -170 2 0 {name=lp_invn_s sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -200 2 0 {name=lp_invn_b sig_type=std_logic lab=gnd}
T {XMpo_invn} -280 -280 0 0 0.22 0.22 {layer=13}
T {NFET W=2u L=2u} -280 -260 0 0 0.18 0.18 {}

* Gate pullup PFET (XMgate_pu): D=gate G=pass_off_b S=bvdd B=bvdd
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 200 -300 0 0 {name=XMgate_pu W=4e-6 L=2e-6 nf=1 mult=1
model=sky130_fd_pr__pfet_g5v0d10v5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -300 0 0 {name=lp_gpu_g sig_type=std_logic lab=pass_off_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 -330 2 0 {name=lp_gpu_d sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 -270 2 0 {name=lp_gpu_s sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 -300 2 0 {name=lp_gpu_b sig_type=std_logic lab=bvdd}
T {XMgate_pu} 120 -430 0 0 0.22 0.22 {layer=13}
T {PFET W=4u L=2u} 120 -410 0 0 0.18 0.18 {}
T {(FIX-14)} 120 -390 0 0 0.18 0.18 {}

* ============================================================
* BLOCK 06: LEVEL SHIFTER  (XLS_EN)
* Shifts EN from SVDD domain to BVDD domain
* Ports: en en_bvdd bvdd svdd gnd
* ============================================================
L 7 -1800 -1200 -1100 -1200 {}
L 7 -1100 -1200 -1100 -950 {}
L 7 -1100 -950 -1800 -950 {}
L 7 -1800 -950 -1800 -1200 {}
L 7 -1802 -1202 -1098 -1202 {}
L 7 -1098 -1202 -1098 -948 {}
L 7 -1098 -948 -1802 -948 {}
L 7 -1802 -948 -1802 -1202 {}
T {Block 06} -1540 -1185 0 0 0.22 0.22 {layer=13}
T {Level Shifter} -1560 -1160 0 0 0.4 0.4 {layer=7}
T {SVDD -> BVDD} -1560 -1135 0 0 0.22 0.22 {layer=13}
T {XLS_EN} -1560 -1115 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1800 -1100 0 0 {name=lp06en sig_type=std_logic lab=en}
T {en} -1788 -1110 0 0 0.23 0.23 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1100 -1100 2 0 {name=lp06eb sig_type=std_logic lab=en_bvdd}
T {en_bvdd} -1190 -1110 0 0 0.23 0.23 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1450 -1200 3 0 {name=lp06bv sig_type=std_logic lab=bvdd}
T {bvdd} -1460 -1198 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1800 -1040 0 0 {name=lp06sv sig_type=std_logic lab=svdd}
T {svdd} -1788 -1050 0 0 0.23 0.23 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1450 -950 1 0 {name=lp06gn sig_type=std_logic lab=gnd}
T {gnd} -1460 -960 0 0 0.22 0.22 {}

* ============================================================
* OUTPUT CAPACITORS
*   Cload: 200pF internal (on-chip MIM)
*   Cout_ext: 1uF external bypass capacitor
* ============================================================
L 5 2400 -1550 3100 -1550 {}
L 5 3100 -1550 3100 -1250 {}
L 5 3100 -1250 2400 -1250 {}
L 5 2400 -1250 2400 -1550 {}
T {Output Caps} 2640 -1535 0 0 0.35 0.35 {layer=5}
T {Cload=200pF (internal)} 2412 -1500 0 0 0.22 0.22 {}
T {Cout_ext=1uF (external)} 2412 -1480 0 0 0.22 0.22 {}

C {/usr/share/xschem/xschem_library/devices/capa.sym} 2600 -1400 0 0 {name=Cload value=200p}
N 2600 -1430 2600 -1460 {lab=pvdd}
N 2600 -1370 2600 -1340 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2600 -1460 3 0 {name=lp_cl1 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2600 -1340 1 0 {name=lp_cl2 sig_type=std_logic lab=gnd}
T {Cload 200pF} 2620 -1420 0 0 0.22 0.22 {layer=13}

C {/usr/share/xschem/xschem_library/devices/capa.sym} 2900 -1400 0 0 {name=Cout_ext value=1u}
N 2900 -1430 2900 -1460 {lab=pvdd}
N 2900 -1370 2900 -1340 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2900 -1460 3 0 {name=lp_ce1 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2900 -1340 1 0 {name=lp_ce2 sig_type=std_logic lab=gnd}
T {Cout_ext 1uF} 2920 -1420 0 0 0.22 0.22 {layer=13}

* ============================================================
* SPICE NETLIST (subcircuit instantiation code)
* This code block contains the actual SPICE subcircuit calls
* matching design.cir exactly, for netlist export.
* ============================================================
C {/usr/share/xschem/xschem_library/devices/code.sym} -2200 200 0 0 {name=SPICE_INSTANCES only_toplevel=false value="
* Block 01: Pass device
XM_pass gate bvdd pvdd pass_device

* Soft-start RC
XRss avbg vref_ss gnd sky130_fd_pr__res_xhigh_po w=2 l=100
Css vref_ss gnd 22n

* Block 00: Error amplifier
XEA vref_ss vfb ea_out gnd ibias ea_en bvdd error_amp

* Block 02: Feedback network
XFB pvdd vfb gnd feedback_network

* FIX-25: Feedforward cap
Cff pvdd vfb 22p

* Block 03: Compensation (placeholder)
XCOMP ea_out pvdd gnd compensation

* Block 04: Current limiter
Iibias_ilim 0 ibias_ilim 1u
XILIM gate bvdd pvdd gnd ilim_flag ibias_ilim current_limiter

* Block 05: UV/OV comparators
XUV pvdd avbg uv_flag svdd gnd uvov_en uv_comparator
XOV pvdd avbg ov_flag svdd gnd uvov_en ov_comparator

* Block 07: MOS voltage clamp
XZC pvdd gnd ibias zener_clamp

* Block 08: Mode control
XMC bvdd pvdd svdd gnd en_ret bypass_en mc_ea_en ref_sel uvov_en ilim_en pass_off mode_control

* Block 09: Startup circuit
XSU bvdd pvdd gate gnd avbg startup_done su_ea_en ea_out startup

* EA enable: BVDD pullup
Ren_ea bvdd ea_en 100

* POR gate pullup inverter + pullup PFET
XMpo_invp pass_off_b pass_off bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 w=40e-6 l=2e-6
XMpo_invn pass_off_b pass_off gnd gnd sky130_fd_pr__nfet_g5v0d10v5 w=2e-6 l=2e-6
XMgate_pu gate pass_off_b bvdd bvdd sky130_fd_pr__pfet_g5v0d10v5 w=4e-6 l=2e-6

* Block 06: Level shifter
XLS_EN en en_bvdd bvdd svdd gnd level_shifter_up

* Output capacitors
Cload pvdd gnd 200e-12
Cout_ext pvdd gnd 1u
"}

* ============================================================
* SIGNAL FLOW ANNOTATIONS
* ============================================================
T {Signal Flow:} -2200 -100 0 0 0.35 0.35 {layer=4}
T {1. BVDD ramps -> soft-start ramps vref_ss (tau=2.2ms)} -2200 -70 0 0 0.25 0.25 {}
T {2. Mode control sequences enables from BVDD ladder} -2200 -45 0 0 0.25 0.25 {}
T {3. EA compares vref_ss with vfb -> ea_out (BVDD domain)} -2200 -20 0 0 0.25 0.25 {}
T {4. ea_out -> Rgate=1k -> gate (direct drive, no CG)} -2200 5 0 0 0.25 0.25 {}
T {5. Pass PMOS regulates PVDD from BVDD} -2200 30 0 0 0.25 0.25 {}
T {6. Feedback divides PVDD -> vfb ~ 1.226V at regulation} -2200 55 0 0 0.25 0.25 {}
T {7. Cff=22pF feedforward zero boosts PM ~49 deg} -2200 80 0 0 0.25 0.25 {}
T {8. Current limiter clamps gate if Iload > ~50mA} -2200 105 0 0 0.25 0.25 {}
T {9. MOS clamp protects PVDD overvoltage} -2200 130 0 0 0.25 0.25 {}
T {10. UV/OV comparators monitor PVDD -> flags in SVDD domain} -2200 155 0 0 0.25 0.25 {}

* ============================================================
* NET LEGEND (internal nets)
* ============================================================
T {Internal Nets:} -2200 220 0 0 0.3 0.3 {layer=13}
T {gate — pass device gate node (driven by EA via startup Rgate)} -2200 245 0 0 0.22 0.22 {}
T {ea_out — error amp output (BVDD domain)} -2200 265 0 0 0.22 0.22 {}
T {vref_ss — soft-started reference (0 -> 1.226V over ~11ms)} -2200 285 0 0 0.22 0.22 {}
T {vfb — feedback voltage (~1.226V at regulation)} -2200 305 0 0 0.22 0.22 {}
T {ea_en — error amp enable (always HIGH via Ren_ea pullup)} -2200 325 0 0 0.22 0.22 {}
T {pass_off — POR signal from mode control} -2200 345 0 0 0.22 0.22 {}
T {pass_off_b — inverted pass_off (drives gate pullup)} -2200 365 0 0 0.22 0.22 {}
T {ibias_ilim — dedicated 1uA bias for current limiter} -2200 385 0 0 0.22 0.22 {}
T {ilim_flag — current limit active indicator} -2200 405 0 0 0.22 0.22 {}
T {uvov_en — UV/OV comparator enable from mode control} -2200 425 0 0 0.22 0.22 {}
T {mc_ea_en — mode control EA enable (unused, floating)} -2200 445 0 0 0.22 0.22 {}
T {en_bvdd — level-shifted enable in BVDD domain} -2200 465 0 0 0.22 0.22 {}
T {bypass_en, ref_sel, ilim_en, su_ea_en — mode control outputs} -2200 485 0 0 0.22 0.22 {}
