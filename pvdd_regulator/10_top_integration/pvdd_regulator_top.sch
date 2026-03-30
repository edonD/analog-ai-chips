v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {PVDD 5V LDO Regulator} -1800 -2000 0 0 1.1 1.1 {layer=4}
T {Top-Level Block Diagram} -1800 -1920 0 0 0.6 0.6 {layer=8}
T {SkyWater SKY130A  |  10 Sub-blocks + Passives  |  Block 10: Top Integration} -1800 -1870 0 0 0.32 0.32 {}

T {Color Legend:} -1800 -1820 0 0 0.3 0.3 {layer=13}
T {BVDD (5.4-10.5V)} -1590 -1820 0 0 0.3 0.3 {layer=4}
T {PVDD (5.0V)} -1250 -1820 0 0 0.3 0.3 {layer=5}
T {SVDD (2.2V)} -970 -1820 0 0 0.3 0.3 {layer=7}
T {Internal} -710 -1820 0 0 0.3 0.3 {layer=13}

C {/usr/share/xschem/xschem_library/devices/title.sym} -1800 900 0 0 {name=l1 author="PVDD 5V LDO Regulator -- Top-Level Block Diagram -- Analog AI Chips"}

* EXTERNAL PORT PINS
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1800 -1200 0 0 {name=p_bvdd lab=bvdd}
T {BVDD (5.4-10.5V)} -1730 -1210 0 0 0.32 0.32 {layer=4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1800 -1050 0 0 {name=p_avbg lab=avbg}
T {AVBG (1.226V ref)} -1730 -1060 0 0 0.32 0.32 {layer=13}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1800 -950 0 0 {name=p_ibias lab=ibias}
T {IBIAS (1uA)} -1730 -960 0 0 0.32 0.32 {layer=13}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1800 -500 0 0 {name=p_svdd lab=svdd}
T {SVDD (2.2V)} -1730 -510 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1800 -400 0 0 {name=p_en lab=en}
T {EN (active HIGH)} -1730 -410 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -1800 -300 0 0 {name=p_en_ret lab=en_ret}
T {EN_RET (retention)} -1730 -310 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -1800 650 0 0 {name=p_gnd lab=gnd}
T {GND} -1740 640 0 0 0.35 0.35 {}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 3000 -1050 0 0 {name=p_pvdd lab=pvdd}
T {PVDD (5.0V reg)} 2870 -1060 0 0 0.35 0.35 {layer=5}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 3000 -1650 0 0 {name=p_uv_flag lab=uv_flag}
T {UV_FLAG} 2880 -1660 0 0 0.32 0.32 {layer=7}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 3000 -1450 0 0 {name=p_ov_flag lab=ov_flag}
T {OV_FLAG} 2880 -1460 0 0 0.32 0.32 {layer=7}

* BLOCK 01: PASS DEVICE
L 4 1600 -1300 2150 -1300 {}
L 4 2150 -1300 2150 -1000 {}
L 4 2150 -1000 1600 -1000 {}
L 4 1600 -1000 1600 -1300 {}
L 4 1598 -1302 2152 -1302 {}
L 4 2152 -1302 2152 -998 {}
L 4 2152 -998 1598 -998 {}
L 4 1598 -998 1598 -1302 {}
T {Block 01} 1815 -1282 0 0 0.22 0.22 {layer=13}
T {Pass Device} 1795 -1260 0 0 0.4 0.4 {layer=4}
T {PMOS 10x100u/0.5u} 1795 -1232 0 0 0.22 0.22 {layer=13}
T {gate} 1612 -1200 0 0 0.25 0.25 {layer=4}
T {bvdd} 1780 -1288 0 0 0.25 0.25 {layer=4}
T {pvdd} 2085 -1170 0 0 0.25 0.25 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 -1180 0 0 {name=lp01g sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1800 -1300 3 0 {name=lp01bv sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2150 -1150 2 0 {name=lp01pv sig_type=std_logic lab=pvdd}

* BLOCK 00: ERROR AMPLIFIER
L 5 -200 -1350 500 -1350 {}
L 5 500 -1350 500 -1000 {}
L 5 500 -1000 -200 -1000 {}
L 5 -200 -1000 -200 -1350 {}
L 5 -202 -1352 502 -1352 {}
L 5 502 -1352 502 -998 {}
L 5 502 -998 -202 -998 {}
L 5 -202 -998 -202 -1352 {}
T {Block 00} 90 -1332 0 0 0.22 0.22 {layer=13}
T {Error Amplifier} 70 -1310 0 0 0.4 0.4 {layer=5}
T {Two-stage Miller OTA} 70 -1282 0 0 0.22 0.22 {layer=13}
T {vref_ss (+)} -188 -1280 0 0 0.23 0.23 {layer=13}
T {vfb (-)} -188 -1210 0 0 0.23 0.23 {layer=13}
T {ibias} -188 -1140 0 0 0.23 0.23 {layer=13}
T {ea_out} 420 -1210 0 0 0.23 0.23 {layer=13}
T {pvdd} 50 -1338 0 0 0.22 0.22 {layer=5}
T {gnd} 50 -1020 0 0 0.22 0.22 {}
T {ea_en} 250 -1020 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 -1270 0 0 {name=lp00vr sig_type=std_logic lab=vref_ss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 -1200 0 0 {name=lp00vf sig_type=std_logic lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 -1130 0 0 {name=lp00ib sig_type=std_logic lab=ibias}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -1200 2 0 {name=lp00ea sig_type=std_logic lab=ea_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 80 -1350 3 0 {name=lp00pv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 80 -1000 1 0 {name=lp00gn sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 280 -1000 1 0 {name=lp00en sig_type=std_logic lab=ea_en}

* BLOCK 09: STARTUP
L 4 700 -1350 1400 -1350 {}
L 4 1400 -1350 1400 -1000 {}
L 4 1400 -1000 700 -1000 {}
L 4 700 -1000 700 -1350 {}
L 4 698 -1352 1402 -1352 {}
L 4 1402 -1352 1402 -998 {}
L 4 1402 -998 698 -998 {}
L 4 698 -998 698 -1352 {}
T {Block 09} 990 -1332 0 0 0.22 0.22 {layer=13}
T {Startup Circuit} 970 -1310 0 0 0.4 0.4 {layer=4}
T {Bootstrap + CG Level Shifter} 970 -1282 0 0 0.22 0.22 {layer=13}
T {ea_out} 712 -1270 0 0 0.23 0.23 {layer=13}
T {ea_en} 712 -1200 0 0 0.23 0.23 {layer=13}
T {avbg} 712 -1130 0 0 0.23 0.23 {layer=13}
T {gate} 1340 -1200 0 0 0.23 0.23 {layer=4}
T {bvdd} 950 -1338 0 0 0.22 0.22 {layer=4}
T {pvdd} 850 -1020 0 0 0.22 0.22 {layer=5}
T {gnd} 1050 -1020 0 0 0.22 0.22 {}
T {startup_done} 1150 -1020 0 0 0.18 0.18 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -1260 0 0 {name=lp09ea sig_type=std_logic lab=ea_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -1190 0 0 {name=lp09en sig_type=std_logic lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -1120 0 0 {name=lp09av sig_type=std_logic lab=avbg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -1190 2 0 {name=lp09g sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 980 -1350 3 0 {name=lp09bv sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 -1000 1 0 {name=lp09pv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1080 -1000 1 0 {name=lp09gn sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 -1000 1 0 {name=lp09sd sig_type=std_logic lab=startup_done}

* SOFT-START RC
L 13 -900 -1300 -400 -1300 {}
L 13 -400 -1300 -400 -1100 {}
L 13 -400 -1100 -900 -1100 {}
L 13 -900 -1100 -900 -1300 {}
T {Soft-Start RC} -870 -1282 0 0 0.32 0.32 {layer=13}
T {Rss=200k} -870 -1252 0 0 0.22 0.22 {layer=13}
T {Css=30nF} -870 -1232 0 0 0.22 0.22 {layer=13}
T {tau=6ms} -870 -1212 0 0 0.22 0.22 {layer=13}
T {avbg} -888 -1220 0 0 0.22 0.22 {layer=13}
T {vref_ss} -485 -1220 0 0 0.22 0.22 {layer=13}
T {gnd} -680 -1118 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -900 -1210 0 0 {name=lpss_av sig_type=std_logic lab=avbg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -400 -1210 2 0 {name=lpss_vr sig_type=std_logic lab=vref_ss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -650 -1100 1 0 {name=lpss_gn sig_type=std_logic lab=gnd}

* BLOCK 02: FEEDBACK NETWORK
L 5 700 -750 1300 -750 {}
L 5 1300 -750 1300 -500 {}
L 5 1300 -500 700 -500 {}
L 5 700 -500 700 -750 {}
L 5 698 -752 1302 -752 {}
L 5 1302 -752 1302 -498 {}
L 5 1302 -498 698 -498 {}
L 5 698 -498 698 -752 {}
T {Block 02} 940 -732 0 0 0.22 0.22 {layer=13}
T {Feedback Network} 920 -710 0 0 0.4 0.4 {layer=5}
T {R_top=364k R_bot=118k} 920 -682 0 0 0.22 0.22 {layer=13}
T {pvdd} 900 -738 0 0 0.22 0.22 {layer=5}
T {vfb} 712 -650 0 0 0.23 0.23 {layer=13}
T {gnd} 950 -518 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 930 -750 3 0 {name=lp02pv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -640 0 0 {name=lp02vf sig_type=std_logic lab=vfb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 980 -500 1 0 {name=lp02gn sig_type=std_logic lab=gnd}

* BLOCK 03: COMPENSATION
L 5 -200 -750 450 -750 {}
L 5 450 -750 450 -500 {}
L 5 450 -500 -200 -500 {}
L 5 -200 -500 -200 -750 {}
L 5 -202 -752 452 -752 {}
L 5 452 -752 452 -498 {}
L 5 452 -498 -202 -498 {}
L 5 -202 -498 -202 -752 {}
T {Block 03} 65 -732 0 0 0.22 0.22 {layer=13}
T {Compensation} 45 -710 0 0 0.4 0.4 {layer=5}
T {Cc=30pF Rz=5k Cout=50pF} 45 -682 0 0 0.22 0.22 {layer=13}
T {ea_out} -188 -660 0 0 0.22 0.22 {layer=13}
T {pvdd} 385 -660 0 0 0.22 0.22 {layer=5}
T {gnd} 80 -518 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 -650 0 0 {name=lp03ea sig_type=std_logic lab=ea_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 450 -650 2 0 {name=lp03pv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 110 -500 1 0 {name=lp03gn sig_type=std_logic lab=gnd}

* BLOCK 04: CURRENT LIMITER
L 4 300 -1750 1000 -1750 {}
L 4 1000 -1750 1000 -1500 {}
L 4 1000 -1500 300 -1500 {}
L 4 300 -1500 300 -1750 {}
L 4 298 -1752 1002 -1752 {}
L 4 1002 -1752 1002 -1498 {}
L 4 1002 -1498 298 -1498 {}
L 4 298 -1498 298 -1752 {}
T {Block 04} 590 -1732 0 0 0.22 0.22 {layer=13}
T {Current Limiter} 570 -1710 0 0 0.4 0.4 {layer=4}
T {Sense mirror, Ilim~70mA} 570 -1682 0 0 0.22 0.22 {layer=13}
T {gate} 312 -1650 0 0 0.22 0.22 {layer=4}
T {bvdd} 550 -1738 0 0 0.22 0.22 {layer=4}
T {pvdd} 935 -1660 0 0 0.22 0.22 {layer=5}
T {gnd} 550 -1518 0 0 0.22 0.22 {}
T {ilim_flag} 900 -1600 0 0 0.2 0.2 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -1640 0 0 {name=lp04g sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -1750 3 0 {name=lp04bv sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -1650 2 0 {name=lp04pv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -1500 1 0 {name=lp04gn sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -1590 2 0 {name=lp04fl sig_type=std_logic lab=ilim_flag}

* BLOCK 05: UV COMPARATOR
L 7 1500 -1750 2200 -1750 {}
L 7 2200 -1750 2200 -1550 {}
L 7 2200 -1550 1500 -1550 {}
L 7 1500 -1550 1500 -1750 {}
L 7 1498 -1752 2202 -1752 {}
L 7 2202 -1752 2202 -1548 {}
L 7 2202 -1548 1498 -1548 {}
L 7 1498 -1548 1498 -1752 {}
T {Block 05} 1790 -1732 0 0 0.22 0.22 {layer=13}
T {UV Comparator} 1770 -1710 0 0 0.4 0.4 {layer=7}
T {Trip: PVDD < 4.3V} 1770 -1682 0 0 0.22 0.22 {layer=13}
T {pvdd} 1512 -1680 0 0 0.22 0.22 {layer=5}
T {avbg} 1512 -1640 0 0 0.22 0.22 {layer=13}
T {uvov_en} 1512 -1720 0 0 0.2 0.2 {layer=13}
T {uv_flag} 2110 -1670 0 0 0.22 0.22 {layer=7}
T {svdd} 1750 -1738 0 0 0.2 0.2 {layer=7}
T {gnd} 1750 -1566 0 0 0.2 0.2 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -1670 0 0 {name=lp5apv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -1630 0 0 {name=lp5aav sig_type=std_logic lab=avbg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -1710 0 0 {name=lp5aen sig_type=std_logic lab=uvov_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2200 -1660 2 0 {name=lp5auf sig_type=std_logic lab=uv_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1780 -1750 3 0 {name=lp5asv sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1780 -1550 1 0 {name=lp5agn sig_type=std_logic lab=gnd}

* BLOCK 05: OV COMPARATOR
L 7 1500 -1500 2200 -1500 {}
L 7 2200 -1500 2200 -1300 {}
L 7 2200 -1300 1500 -1300 {}
L 7 1500 -1300 1500 -1500 {}
L 7 1498 -1502 2202 -1502 {}
L 7 2202 -1502 2202 -1298 {}
L 7 2202 -1298 1498 -1298 {}
L 7 1498 -1298 1498 -1502 {}
T {Block 05} 1790 -1482 0 0 0.22 0.22 {layer=13}
T {OV Comparator} 1770 -1460 0 0 0.4 0.4 {layer=7}
T {Trip: PVDD > 5.5V} 1770 -1432 0 0 0.22 0.22 {layer=13}
T {pvdd} 1512 -1430 0 0 0.22 0.22 {layer=5}
T {avbg} 1512 -1390 0 0 0.22 0.22 {layer=13}
T {uvov_en} 1512 -1470 0 0 0.2 0.2 {layer=13}
T {ov_flag} 2110 -1420 0 0 0.22 0.22 {layer=7}
T {svdd} 1750 -1488 0 0 0.2 0.2 {layer=7}
T {gnd} 1750 -1316 0 0 0.2 0.2 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -1420 0 0 {name=lp5bpv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -1380 0 0 {name=lp5bav sig_type=std_logic lab=avbg}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -1460 0 0 {name=lp5ben sig_type=std_logic lab=uvov_en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2200 -1410 2 0 {name=lp5bof sig_type=std_logic lab=ov_flag}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1780 -1500 3 0 {name=lp5bsv sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1780 -1300 1 0 {name=lp5bgn sig_type=std_logic lab=gnd}

* BLOCK 07: ZENER CLAMP
L 5 2350 -1300 2800 -1300 {}
L 5 2800 -1300 2800 -1050 {}
L 5 2800 -1050 2350 -1050 {}
L 5 2350 -1050 2350 -1300 {}
L 5 2348 -1302 2802 -1302 {}
L 5 2802 -1302 2802 -1048 {}
L 5 2802 -1048 2348 -1048 {}
L 5 2348 -1048 2348 -1302 {}
T {Block 07} 2515 -1282 0 0 0.22 0.22 {layer=13}
T {Zener Clamp} 2495 -1260 0 0 0.4 0.4 {layer=5}
T {Hybrid ~6V clamp} 2495 -1232 0 0 0.22 0.22 {layer=13}
T {pvdd} 2362 -1200 0 0 0.22 0.22 {layer=5}
T {gnd} 2530 -1068 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2350 -1190 0 0 {name=lp07pv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2560 -1050 1 0 {name=lp07gn sig_type=std_logic lab=gnd}

* BLOCK 08: MODE CONTROL
L 4 -100 -350 1000 -350 {}
L 4 1000 -350 1000 200 {}
L 4 1000 200 -100 200 {}
L 4 -100 200 -100 -350 {}
L 4 -102 -352 1002 -352 {}
L 4 1002 -352 1002 202 {}
L 4 1002 202 -102 202 {}
L 4 -102 202 -102 -352 {}
T {Block 08} 390 -332 0 0 0.22 0.22 {layer=13}
T {Mode Control} 370 -310 0 0 0.4 0.4 {layer=4}
T {BVDD ladder + Schmitt + logic} 370 -282 0 0 0.22 0.22 {layer=13}
T {bvdd} -88 -270 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -260 0 0 {name=lp08_bvdd sig_type=std_logic lab=bvdd}
T {pvdd} -88 -210 0 0 0.22 0.22 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -200 0 0 {name=lp08_pvdd sig_type=std_logic lab=pvdd}
T {svdd} -88 -150 0 0 0.22 0.22 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -140 0 0 {name=lp08_svdd sig_type=std_logic lab=svdd}
T {avbg} -88 -90 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -80 0 0 {name=lp08_avbg sig_type=std_logic lab=avbg}
T {en_ret} -88 -30 0 0 0.22 0.22 {layer=7}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -20 0 0 {name=lp08_en_ret sig_type=std_logic lab=en_ret}
T {gnd} 400 182 0 0 0.22 0.22 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 200 1 0 {name=lp08gn sig_type=std_logic lab=gnd}
T {bypass_en} 890 -270 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -260 2 0 {name=lp08_bypass_en sig_type=std_logic lab=bypass_en}
T {mc_ea_en} 890 -210 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -200 2 0 {name=lp08_mc_ea_en sig_type=std_logic lab=mc_ea_en}
T {ref_sel} 890 -150 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -140 2 0 {name=lp08_ref_sel sig_type=std_logic lab=ref_sel}
T {uvov_en} 890 -90 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -80 2 0 {name=lp08_uvov_en sig_type=std_logic lab=uvov_en}
T {ilim_en} 890 -30 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 -20 2 0 {name=lp08_ilim_en sig_type=std_logic lab=ilim_en}
T {pass_off} 890 30 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1000 40 2 0 {name=lp08_pass_off sig_type=std_logic lab=pass_off}

* BLOCK 06: LEVEL SHIFTER UP
L 7 -1200 -350 -550 -350 {}
L 7 -550 -350 -550 -150 {}
L 7 -550 -150 -1200 -150 {}
L 7 -1200 -150 -1200 -350 {}
L 7 -1202 -352 -548 -352 {}
L 7 -548 -352 -548 -148 {}
L 7 -548 -148 -1202 -148 {}
L 7 -1202 -148 -1202 -352 {}
T {Block 06} -935 -332 0 0 0.22 0.22 {layer=13}
T {Level Shifter} -955 -310 0 0 0.4 0.4 {layer=7}
T {SVDD -> BVDD} -955 -282 0 0 0.22 0.22 {layer=13}
T {en} -1188 -280 0 0 0.22 0.22 {layer=7}
T {en_bvdd} -645 -280 0 0 0.22 0.22 {layer=4}
T {bvdd} -1000 -338 0 0 0.2 0.2 {layer=4}
T {svdd} -800 -338 0 0 0.2 0.2 {layer=7}
T {gnd} -900 -166 0 0 0.2 0.2 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1200 -270 0 0 {name=lp06en sig_type=std_logic lab=en}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -550 -270 2 0 {name=lp06eb sig_type=std_logic lab=en_bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -970 -350 3 0 {name=lp06bv sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -770 -350 3 0 {name=lp06sv sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -870 -150 1 0 {name=lp06gn sig_type=std_logic lab=gnd}

* Cload — 200 pF
L 5 1650 -750 2000 -750 {}
L 5 2000 -750 2000 -550 {}
L 5 2000 -550 1650 -550 {}
L 5 1650 -550 1650 -750 {}
T {Cload} 1680 -732 0 0 0.3 0.3 {layer=5}
T {200 pF} 1680 -702 0 0 0.25 0.25 {layer=5}
T {pvdd} 1770 -738 0 0 0.2 0.2 {layer=5}
T {gnd} 1770 -566 0 0 0.2 0.2 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1800 -750 3 0 {name=lp_cl_pv sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1800 -550 1 0 {name=lp_cl_gn sig_type=std_logic lab=gnd}

* MAIN SIGNAL FLOW WIRES

N -1800 -1050 -1400 -1050 {lab=avbg}
N -1400 -1050 -1400 -1210 {}
N -1400 -1210 -900 -1210 {lab=avbg}
N -400 -1210 -450 -1210 {}
N -450 -1210 -450 -1270 {}
N -450 -1270 -200 -1270 {lab=vref_ss}
N 500 -1200 600 -1200 {}
N 600 -1200 600 -1260 {}
N 600 -1260 700 -1260 {lab=ea_out}
N 1400 -1190 1600 -1180 {lab=gate}
N 2150 -1150 2700 -1150 {lab=pvdd}
N 2700 -1150 2700 -1050 {}
N 2700 -1050 3000 -1050 {lab=pvdd}
N -1800 -1200 -1550 -1200 {lab=bvdd}
N -1550 -1200 -1550 -1800 {}
N -1550 -1800 1800 -1800 {lab=bvdd}
N 1800 -1800 1800 -1300 {lab=bvdd}
N -1800 -950 -1300 -950 {}
N -1300 -950 -1300 -1130 {}
N -1300 -1130 -200 -1130 {lab=ibias}
N 2700 -1150 2700 -800 {}
N 2700 -800 930 -800 {}
N 930 -800 930 -750 {lab=pvdd}
N 700 -640 -350 -640 {}
N -350 -640 -350 -1200 {}
N -350 -1200 -200 -1200 {lab=vfb}
N 2200 -1660 2600 -1660 {}
N 2600 -1660 2600 -1650 {}
N 2600 -1650 3000 -1650 {lab=uv_flag}
N 2200 -1410 2600 -1410 {}
N 2600 -1410 2600 -1450 {}
N 2600 -1450 3000 -1450 {lab=ov_flag}
N -1800 -400 -1400 -400 {}
N -1400 -400 -1400 -270 {}
N -1400 -270 -1200 -270 {lab=en}
N -1800 -300 -1500 -300 {}
N -1500 -300 -1500 -20 {}
N -1500 -20 -100 -20 {lab=en_ret}
N -1800 -500 -1500 -500 {lab=svdd}

* SIGNAL FLOW ANNOTATIONS
T {>>>} -320 -1280 0 0 0.4 0.4 {layer=13}
T {>>>} 530 -1270 0 0 0.4 0.4 {layer=13}
T {>>>} 1430 -1195 0 0 0.4 0.4 {layer=13}
T {>>>} 2200 -1160 0 0 0.4 0.4 {layer=5}
T {<<<} -380 -655 0 0 0.35 0.35 {layer=5}
T {1. avbg ramps via RC soft-start} -880 -1090 0 0 0.22 0.22 {layer=13}
T {2. vref_ss drives EA non-inv input} -380 -1385 0 0 0.22 0.22 {layer=13}
T {3. ea_out -> CG level shifter in startup block} 510 -1385 0 0 0.22 0.22 {layer=13}
T {4. gate controls pass PMOS (BVDD domain)} 1420 -1385 0 0 0.22 0.22 {layer=4}
T {5. PVDD regulated output} 2250 -1000 0 0 0.22 0.22 {layer=5}
T {6. Feedback divider sets vfb = 1.226V at 5.0V} 600 -770 0 0 0.22 0.22 {layer=5}
T {7. Compensation stabilizes loop (PM > 70 deg)} -180 -480 0 0 0.22 0.22 {layer=5}
T {BVDD =========================> PVDD (power flow left to right)} -200 -1830 0 0 0.25 0.25 {layer=4}
T {Mode Control outputs:} 1050 -310 0 0 0.23 0.23 {layer=13}
T {uvov_en -> UV/OV comparator enable} 1050 -280 0 0 0.2 0.2 {layer=13}
T {ea_en -> Error amp enable (via startup)} 1050 -255 0 0 0.2 0.2 {layer=13}
T {ilim_en -> Current limiter enable} 1050 -230 0 0 0.2 0.2 {layer=13}
T {bypass_en, ref_sel, pass_off -> reserved} 1050 -205 0 0 0.2 0.2 {layer=13}

* NET LABELS ON WIRES
T {vref_ss} -430 -1240 0 0 0.25 0.25 {layer=13}
T {ea_out} 540 -1230 0 0 0.25 0.25 {layer=13}
T {gate} 1440 -1210 0 0 0.28 0.28 {layer=4}
T {vfb (loop return)} -330 -680 0 0 0.22 0.22 {layer=13}
T {pvdd bus} 2710 -1000 0 0 0.22 0.22 {layer=5}
T {bvdd bus} 200 -1815 0 0 0.25 0.25 {layer=4}

* DOMAIN ANNOTATIONS
L 4 -1560 -1810 2160 -1810 {dash=5}
L 4 2160 -1810 2160 -960 {dash=5}
L 4 2160 -960 -1560 -960 {dash=5}
L 4 -1560 -960 -1560 -1810 {dash=5}
T {BVDD DOMAIN} -1540 -1810 0 0 0.2 0.2 {layer=4}
L 5 -250 -780 2050 -780 {dash=5}
L 5 2050 -780 2050 -470 {dash=5}
L 5 2050 -470 -250 -470 {dash=5}
L 5 -250 -470 -250 -780 {dash=5}
T {PVDD DOMAIN} -240 -780 0 0 0.2 0.2 {layer=5}
L 7 1470 -1780 2250 -1780 {dash=5}
L 7 2250 -1780 2250 -1280 {dash=5}
L 7 2250 -1280 1470 -1280 {dash=5}
L 7 1470 -1280 1470 -1780 {dash=5}
T {SVDD DOMAIN} 1480 -1780 0 0 0.2 0.2 {layer=7}
