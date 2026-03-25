v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 02 — Programmable Gain Amplifier (PGA)} -900 -2450 0 0 0.9 0.9 {layer=15}
T {Capacitive-Feedback  |  4-Gain (1x / 4x / 16x / 64x)  |  SKY130A} -900 -2390 0 0 0.45 0.45 {layer=15}
T {Gain err < 0.15 dB  |  BW = 27 kHz @ 16x  |  THD = 0.19 %  |  P = 9.94 uW  |  49 transistors} -900 -2340 0 0 0.35 0.35 {layer=8}
N -900 -2200 1200 -2200 {lab=VDD}
N -900 -700 1200 -700 {lab=VSS}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -900 -2200 0 1 {name=p_vdd lab=VDD}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -900 -700 0 1 {name=p_vss lab=VSS}
T {VDD = 1.8 V} -850 -2230 0 0 0.3 0.3 {layer=4}
T {VSS = 0 V} -850 -685 0 0 0.3 0.3 {layer=4}
L 3 -920 -2170 -280 -2170 {dash=4}
L 3 -280 -2170 -280 -830 {dash=4}
L 3 -280 -830 -920 -830 {dash=4}
L 3 -920 -830 -920 -2170 {dash=4}
T {2-to-4 CMOS Decoder} -900 -2150 0 0 0.45 0.45 {layer=4}
T {28 transistors  |  Static CMOS  |  < 40 nW} -900 -2110 0 0 0.3 0.3 {layer=8}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -920 -2060 0 1 {name=p_g1 lab=g1}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -920 -2020 0 1 {name=p_g0 lab=g0}
N -920 -2060 -750 -2060 {lab=g1}
N -920 -2020 -500 -2020 {lab=g0}
T {INV0: g0 → g0b} -560 -1995 0 0 0.22 0.22 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -500 -1960 0 0 {name=XP_inv0
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -500 -1880 0 0 {name=XN_inv0
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N -520 -1960 -540 -1960 {lab=g0}
N -540 -1960 -540 -1880 {lab=g0}
N -520 -1880 -540 -1880 {lab=g0}
N -540 -2020 -540 -1960 {lab=g0}
N -480 -1990 -480 -2200 {lab=VDD}
N -480 -1850 -480 -700 {lab=VSS}
N -480 -1930 -480 -1910 {lab=g0b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -450 -1920 0 0 {name=l_g0b lab=g0b}
N -480 -1920 -450 -1920 {lab=g0b}
T {0.84/0.15} -470 -1970 0 0 0.2 0.2 {layer=8}
T {0.42/0.15} -470 -1890 0 0 0.2 0.2 {layer=8}
T {INV1: g1 → g1b} -810 -2035 0 0 0.22 0.22 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -750 -1960 0 0 {name=XP_inv1
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -750 -1880 0 0 {name=XN_inv1
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N -770 -1960 -790 -1960 {lab=g1}
N -790 -1960 -790 -1880 {lab=g1}
N -770 -1880 -790 -1880 {lab=g1}
N -790 -2060 -790 -1960 {lab=g1}
N -730 -1990 -730 -2200 {lab=VDD}
N -730 -1850 -730 -700 {lab=VSS}
N -730 -1930 -730 -1910 {lab=g1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -700 -1920 0 0 {name=l_g1b lab=g1b}
N -730 -1920 -700 -1920 {lab=g1b}
T {0.84/0.15} -720 -1970 0 0 0.2 0.2 {layer=8}
T {0.42/0.15} -720 -1890 0 0 0.2 0.2 {layer=8}
L 7 -870 -1780 -750 -1780 {}
L 7 -750 -1780 -750 -1720 {}
L 7 -750 -1720 -870 -1720 {}
L 7 -870 -1720 -870 -1780 {}
T {NAND2} -860 -1772 0 0 0.25 0.25 {layer=8}
T {(g1b,g0b)} -860 -1750 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -890 -1765 0 1 {name=l_nand0_a lab=g1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -890 -1740 0 1 {name=l_nand0_b lab=g0b}
N -890 -1765 -870 -1765 {lab=g1b}
N -890 -1740 -870 -1740 {lab=g0b}
L 7 -710 -1775 -650 -1775 {}
L 7 -650 -1775 -650 -1725 {}
L 7 -650 -1725 -710 -1725 {}
L 7 -710 -1725 -710 -1775 {}
T {INV} -700 -1765 0 0 0.22 0.22 {layer=8}
N -750 -1750 -710 -1750 {lab=nand0_out}
N -650 -1750 -590 -1750 {lab=sel0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -590 -1750 0 0 {name=l_sel0 lab=sel0}
T {→ sel0 (1x)} -645 -1762 0 0 0.22 0.22 {layer=4}
T {P: 0.84/0.15  N: 0.84/0.15} -860 -1732 0 0 0.15 0.15 {layer=8}
L 7 -870 -1580 -750 -1580 {}
L 7 -750 -1580 -750 -1520 {}
L 7 -750 -1520 -870 -1520 {}
L 7 -870 -1520 -870 -1580 {}
T {NAND2} -860 -1572 0 0 0.25 0.25 {layer=8}
T {(g1b,g0)} -860 -1550 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -890 -1565 0 1 {name=l_nand1_a lab=g1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -890 -1540 0 1 {name=l_nand1_b lab=g0}
N -890 -1565 -870 -1565 {lab=g1b}
N -890 -1540 -870 -1540 {lab=g0}
L 7 -710 -1575 -650 -1575 {}
L 7 -650 -1575 -650 -1525 {}
L 7 -650 -1525 -710 -1525 {}
L 7 -710 -1525 -710 -1575 {}
T {INV} -700 -1565 0 0 0.22 0.22 {layer=8}
N -750 -1550 -710 -1550 {lab=nand1_out}
N -650 -1550 -590 -1550 {lab=sel1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -590 -1550 0 0 {name=l_sel1 lab=sel1}
T {→ sel1 (4x)} -645 -1562 0 0 0.22 0.22 {layer=4}
T {P: 0.84/0.15  N: 0.84/0.15} -860 -1532 0 0 0.15 0.15 {layer=8}
L 7 -870 -1380 -750 -1380 {}
L 7 -750 -1380 -750 -1320 {}
L 7 -750 -1320 -870 -1320 {}
L 7 -870 -1320 -870 -1380 {}
T {NAND2} -860 -1372 0 0 0.25 0.25 {layer=8}
T {(g1,g0b)} -860 -1350 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -890 -1365 0 1 {name=l_nand2_a lab=g1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -890 -1340 0 1 {name=l_nand2_b lab=g0b}
N -890 -1365 -870 -1365 {lab=g1}
N -890 -1340 -870 -1340 {lab=g0b}
L 7 -710 -1375 -650 -1375 {}
L 7 -650 -1375 -650 -1325 {}
L 7 -650 -1325 -710 -1325 {}
L 7 -710 -1325 -710 -1375 {}
T {INV} -700 -1365 0 0 0.22 0.22 {layer=8}
N -750 -1350 -710 -1350 {lab=nand2_out}
N -650 -1350 -590 -1350 {lab=sel2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -590 -1350 0 0 {name=l_sel2 lab=sel2}
T {→ sel2 (16x)} -645 -1362 0 0 0.22 0.22 {layer=4}
T {P: 0.84/0.15  N: 0.84/0.15} -860 -1332 0 0 0.15 0.15 {layer=8}
L 7 -870 -1180 -750 -1180 {}
L 7 -750 -1180 -750 -1120 {}
L 7 -750 -1120 -870 -1120 {}
L 7 -870 -1120 -870 -1180 {}
T {NAND2} -860 -1172 0 0 0.25 0.25 {layer=8}
T {(g1,g0)} -860 -1150 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -890 -1165 0 1 {name=l_nand3_a lab=g1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -890 -1140 0 1 {name=l_nand3_b lab=g0}
N -890 -1165 -870 -1165 {lab=g1}
N -890 -1140 -870 -1140 {lab=g0}
L 7 -710 -1175 -650 -1175 {}
L 7 -650 -1175 -650 -1125 {}
L 7 -650 -1125 -710 -1125 {}
L 7 -710 -1125 -710 -1175 {}
T {INV} -700 -1165 0 0 0.22 0.22 {layer=8}
N -750 -1150 -710 -1150 {lab=nand3_out}
N -650 -1150 -590 -1150 {lab=sel3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -590 -1150 0 0 {name=l_sel3 lab=sel3}
T {→ sel3 (64x)} -645 -1162 0 0 0.22 0.22 {layer=4}
T {P: 0.84/0.15  N: 0.84/0.15} -860 -1132 0 0 0.15 0.15 {layer=8}
T {Output INVs: P 0.84/0.15, N 0.42/0.15} -870 -965 0 0 0.22 0.22 {layer=8}
L 3 -120 -2170 570 -2170 {dash=4}
L 3 570 -2170 570 -830 {dash=4}
L 3 570 -830 -120 -830 {dash=4}
L 3 -120 -830 -120 -2170 {dash=4}
T {Switched Capacitor Network} -100 -2150 0 0 0.45 0.45 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -120 -1500 0 1 {name=p_vin lab=vin}
N -120 -1500 -60 -1500 {lab=vin}
N -60 -2060 -60 -900 {lab=vin}
N 400 -2060 400 -900 {lab=inn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 430 -1500 0 0 {name=l_inn lab=inn}
T {inn (virtual ground)} 440 -1510 0 0 0.22 0.22 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 0 -2050 0 0 {name=XCin1
W=22.4
L=22.4
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
N -60 -2080 0 -2080 {lab=vin}
N 0 -2018 40 -2018 {lab=mid1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -2018 0 0 {name=l_mid1 lab=mid1}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 250 -2018 0 0 {name=XS1
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 40 -2018 230 -2018 {lab=mid1}
N 270 -1988 400 -1988 {lab=inn}
N 400 -1988 400 -2018 {lab=inn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -2018 0 1 {name=l_sel0_sw lab=sel0}
N 210 -2018 230 -2018 {lab=sel0}
N 270 -2048 270 -2070 {lab=VSS}
T {1x: 1 pF} -80 -2100 0 0 0.25 0.25 {layer=4}
T {W=0.42/L=0.15} 280 -2030 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 0 -1750 0 0 {name=XCin2
W=44.7
L=44.7
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
N -60 -1780 0 -1780 {lab=vin}
N 0 -1718 40 -1718 {lab=mid2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -1718 0 0 {name=l_mid2 lab=mid2}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 250 -1718 0 0 {name=XS2
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 40 -1718 230 -1718 {lab=mid2}
N 270 -1688 400 -1688 {lab=inn}
N 400 -1688 400 -1718 {lab=inn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -1718 0 1 {name=l_sel1_sw lab=sel1}
N 210 -1718 230 -1718 {lab=sel1}
N 270 -1748 270 -1770 {lab=VSS}
T {4x: 4 pF} -80 -1800 0 0 0.25 0.25 {layer=4}
T {W=0.42/L=0.15} 280 -1730 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 0 -1450 0 0 {name=XCin3
W=89.4
L=89.4
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
N -60 -1480 0 -1480 {lab=vin}
N 0 -1418 40 -1418 {lab=mid3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -1418 0 0 {name=l_mid3 lab=mid3}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 250 -1418 0 0 {name=XS3
W=1
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 40 -1418 230 -1418 {lab=mid3}
N 270 -1388 400 -1388 {lab=inn}
N 400 -1388 400 -1418 {lab=inn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -1418 0 1 {name=l_sel2_sw lab=sel2}
N 210 -1418 230 -1418 {lab=sel2}
N 270 -1448 270 -1470 {lab=VSS}
T {16x: 16 pF} -80 -1500 0 0 0.25 0.25 {layer=4}
T {W=1/L=0.15} 280 -1430 0 0 0.18 0.18 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 0 -1150 0 0 {name=XCin4
W=178.9
L=178.9
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
N -60 -1180 0 -1180 {lab=vin}
N 0 -1118 40 -1118 {lab=mid4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -1118 0 0 {name=l_mid4 lab=mid4}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 250 -1118 0 0 {name=XS4
W=5
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 40 -1118 230 -1118 {lab=mid4}
N 270 -1088 400 -1088 {lab=inn}
N 400 -1088 400 -1118 {lab=inn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -1118 0 1 {name=l_sel3_sw lab=sel3}
N 210 -1118 230 -1118 {lab=sel3}
N 270 -1148 270 -1170 {lab=VSS}
T {64x: 64 pF} -80 -1200 0 0 0.25 0.25 {layer=4}
T {W=5/L=0.15} 280 -1130 0 0 0.18 0.18 {layer=8}
T {Mid-node pseudo-R (×4 pairs)} -100 -870 0 0 0.25 0.25 {layer=4}
T {Back-to-back PMOS W=0.42/L=10, bulk=VDD} -100 -850 0 0 0.2 0.2 {layer=8}
T {~100 GΩ from each mid node to Vcm} -100 -835 0 0 0.2 0.2 {layer=8}
T {8 transistors total} -100 -820 0 0 0.2 0.2 {layer=8}
L 3 580 -2170 1200 -2170 {dash=4}
L 3 1200 -2170 1200 -830 {dash=4}
L 3 1200 -830 580 -830 {dash=4}
L 3 580 -830 580 -2170 {dash=4}
T {OTA + Feedback Network} 600 -2150 0 0 0.45 0.45 {layer=4}
L 7 670 -1580 670 -1420 {}
L 7 670 -1580 830 -1500 {}
L 7 670 -1420 830 -1500 {}
T {OTA} 720 -1512 0 0 0.35 0.35 {layer=8}
T {ota_pga_v2} 705 -1488 0 0 0.22 0.22 {layer=8}
T {2-stage Miller} 650 -1410 0 0 0.22 0.22 {layer=8}
T {UGB = 422 kHz} 650 -1390 0 0 0.22 0.22 {layer=8}
T {Av = 60 dB} 650 -1370 0 0 0.22 0.22 {layer=8}
T {7 MOSFETs} 650 -1350 0 0 0.22 0.22 {layer=8}
T {−} 680 -1552 0 0 0.4 0.4 {layer=4}
T {+} 680 -1472 0 0 0.4 0.4 {layer=4}
N 400 -1500 620 -1500 {lab=inn}
N 620 -1500 620 -1540 {lab=inn}
N 620 -1540 670 -1540 {lab=inn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 600 -1460 0 1 {name=p_vcm lab=vcm}
N 600 -1460 670 -1460 {lab=vcm}
N 830 -1500 1100 -1500 {lab=vout}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1100 -1500 0 0 {name=p_vout lab=vout}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1090 -1530 0 0 {name=l_vout lab=vout}
N 750 -1580 750 -2200 {lab=VDD}
N 750 -1420 750 -700 {lab=VSS}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 850 -1800 0 0 {name=XCf
W=22.4
L=22.4
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
T {Cf = 1 pF} 790 -1855 0 0 0.28 0.28 {layer=4}
T {22.4 × 22.4 MIM} 790 -1835 0 0 0.2 0.2 {layer=8}
N 620 -1540 620 -1830 {lab=inn}
N 620 -1830 850 -1830 {lab=inn}
N 850 -1768 850 -1500 {lab=vout}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1000 -1870 0 0 {name=XMpr1
W=0.42
L=10
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1000 -1740 0 0 {name=XMpr2
W=0.42
L=10
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {Feedback pseudo-R} 930 -1925 0 0 0.25 0.25 {layer=4}
T {Back-to-back PMOS} 930 -1905 0 0 0.2 0.2 {layer=8}
T {W=0.42/L=10, bulk=VDD} 930 -1890 0 0 0.2 0.2 {layer=8}
N 1020 -1900 1020 -1860 {lab=inn}
N 1020 -1860 660 -1860 {lab=inn}
N 660 -1860 660 -1830 {lab=inn}
N 980 -1870 960 -1870 {lab=inn}
N 960 -1870 960 -1860 {lab=inn}
N 1020 -1840 1020 -1770 {}
N 1020 -1710 1020 -1500 {lab=vout}
N 1020 -1500 1100 -1500 {lab=vout}
N 980 -1740 960 -1740 {lab=vout}
N 960 -1740 960 -1500 {lab=vout}
T {CL = 10 pF} 1070 -1460 0 0 0.25 0.25 {layer=8}
T {(external load)} 1070 -1440 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 620 -900 0 1 {name=p_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 620 -870 0 1 {name=p_vbcn lab=vbcn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 620 -840 0 1 {name=p_vbp lab=vbp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 620 -810 0 1 {name=p_vbcp lab=vbcp}
T {OTA bias:} 650 -920 0 0 0.22 0.22 {layer=4}
T {vbn = 0.65 V} 650 -900 0 0 0.2 0.2 {layer=8}
T {vbcn = 0.88 V} 650 -870 0 0 0.2 0.2 {layer=8}
T {vbp = 0.73 V} 650 -840 0 0 0.2 0.2 {layer=8}
T {vbcp = 0.475 V} 650 -810 0 0 0.2 0.2 {layer=8}
