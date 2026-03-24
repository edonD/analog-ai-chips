v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 02: Programmable Gain Amplifier (PGA)} -600 -2200 0 0 1.0 1.0 {layer=15}
T {Capacitive-Feedback, 4-Gain (1x/4x/16x/64x) — SKY130A} -600 -2140 0 0 0.5 0.5 {layer=15}
T {Gain<0.15dB err | BW=27kHz@16x | THD=0.19% | P=9.94uW} -600 -2090 0 0 0.4 0.4 {layer=8}
T {2-to-4 CMOS Decoder} -600 -2000 0 0 0.5 0.5 {layer=4}
T {INV g0 -> g0b} -550 -1930 0 0 0.25 0.25 {layer=8}
T {XP_inv0} -580 -1860 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} -580 -1836 0 0 0.25 0.25 {layer=8}
T {XN_inv0} -580 -1720 0 0 0.3 0.3 {layer=8}
T {0.42/0.15} -580 -1696 0 0 0.25 0.25 {layer=8}
T {INV g1 -> g1b} -300 -1930 0 0 0.25 0.25 {layer=8}
T {XP_inv1} -330 -1860 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} -330 -1836 0 0 0.25 0.25 {layer=8}
T {XN_inv1} -330 -1720 0 0 0.3 0.3 {layer=8}
T {0.42/0.15} -330 -1696 0 0 0.25 0.25 {layer=8}
T {NAND2 gates (x4)} -600 -1580 0 0 0.35 0.35 {layer=4}
T {NAND0: g1b,g0b} -580 -1530 0 0 0.25 0.25 {layer=8}
T {XP_nand0a/b} -580 -1500 0 0 0.25 0.25 {layer=8}
T {P: 0.84/0.15} -580 -1476 0 0 0.25 0.25 {layer=8}
T {XN_nand0a/b} -580 -1450 0 0 0.25 0.25 {layer=8}
T {N: 0.84/0.15} -580 -1426 0 0 0.25 0.25 {layer=8}
T {NAND1: g1b,g0} -350 -1530 0 0 0.25 0.25 {layer=8}
T {XP_nand1a/b} -350 -1500 0 0 0.25 0.25 {layer=8}
T {P: 0.84/0.15} -350 -1476 0 0 0.25 0.25 {layer=8}
T {XN_nand1a/b} -350 -1450 0 0 0.25 0.25 {layer=8}
T {N: 0.84/0.15} -350 -1426 0 0 0.25 0.25 {layer=8}
T {NAND2: g1,g0b} -580 -1380 0 0 0.25 0.25 {layer=8}
T {XP_nand2a/b} -580 -1350 0 0 0.25 0.25 {layer=8}
T {P: 0.84/0.15} -580 -1326 0 0 0.25 0.25 {layer=8}
T {XN_nand2a/b} -580 -1300 0 0 0.25 0.25 {layer=8}
T {N: 0.84/0.15} -580 -1276 0 0 0.25 0.25 {layer=8}
T {NAND3: g1,g0} -350 -1380 0 0 0.25 0.25 {layer=8}
T {XP_nand3a/b} -350 -1350 0 0 0.25 0.25 {layer=8}
T {P: 0.84/0.15} -350 -1326 0 0 0.25 0.25 {layer=8}
T {XN_nand3a/b} -350 -1300 0 0 0.25 0.25 {layer=8}
T {N: 0.84/0.15} -350 -1276 0 0 0.25 0.25 {layer=8}
T {Output INVs (x4)} -600 -1220 0 0 0.35 0.35 {layer=4}
T {XP_oinv0/XN_oinv0 -> sel0} -580 -1180 0 0 0.25 0.25 {layer=8}
T {XP_oinv1/XN_oinv1 -> sel1} -580 -1156 0 0 0.25 0.25 {layer=8}
T {XP_oinv2/XN_oinv2 -> sel2} -580 -1132 0 0 0.25 0.25 {layer=8}
T {XP_oinv3/XN_oinv3 -> sel3} -580 -1108 0 0 0.25 0.25 {layer=8}
T {P: 0.84/0.15, N: 0.42/0.15} -580 -1070 0 0 0.25 0.25 {layer=8}
T {20 transistors total} -580 -1040 0 0 0.25 0.25 {layer=8}
T {Switched Capacitor Network} 100 -2000 0 0 0.5 0.5 {layer=4}
T {Gain=1x: Cin1=1pF (22.4x22.4 MIM)} 100 -1930 0 0 0.3 0.3 {layer=8}
T {Gain=4x: Cin2=4pF (44.7x44.7 MIM)} 100 -1730 0 0 0.3 0.3 {layer=8}
T {Gain=16x: Cin3=16pF (89.4x89.4 MIM)} 100 -1530 0 0 0.3 0.3 {layer=8}
T {Gain=64x: Cin4=64pF (178.9x178.9 MIM)} 100 -1330 0 0 0.3 0.3 {layer=8}
T {XS1} 370 -1860 0 0 0.3 0.3 {layer=8}
T {W=0.42/L=0.15} 370 -1836 0 0 0.25 0.25 {layer=8}
T {XS2} 370 -1660 0 0 0.3 0.3 {layer=8}
T {W=0.42/L=0.15} 370 -1636 0 0 0.25 0.25 {layer=8}
T {XS3} 370 -1460 0 0 0.3 0.3 {layer=8}
T {W=1/L=0.15} 370 -1436 0 0 0.25 0.25 {layer=8}
T {XS4} 370 -1260 0 0 0.3 0.3 {layer=8}
T {W=5/L=0.15} 370 -1236 0 0 0.25 0.25 {layer=8}
T {Mid-node pseudo-R (x4 pairs)} 100 -1130 0 0 0.35 0.35 {layer=4}
T {XMmid1a/b..XMmid4a/b} 100 -1090 0 0 0.25 0.25 {layer=8}
T {PMOS W=0.42/L=10, bulk=VDD} 100 -1066 0 0 0.25 0.25 {layer=8}
T {8 transistors, ~100 GOhm to Vcm} 100 -1042 0 0 0.25 0.25 {layer=8}
T {OTA + Feedback} 700 -2000 0 0 0.5 0.5 {layer=4}
T {Cf = 1pF (22.4x22.4 MIM)} 700 -1930 0 0 0.3 0.3 {layer=8}
T {Pseudo-R: XMpr1/XMpr2} 700 -1900 0 0 0.25 0.25 {layer=8}
T {PMOS W=0.42/L=10, bulk=VDD} 700 -1876 0 0 0.25 0.25 {layer=8}
T {OTA (ota_pga_v2)} 780 -1700 0 0 0.45 0.45 {layer=4}
T {2-stage Miller compensated} 780 -1660 0 0 0.3 0.3 {layer=8}
T {UGB=422kHz, Av=60dB} 780 -1636 0 0 0.25 0.25 {layer=8}
T {7 transistors (subcircuit)} 780 -1612 0 0 0.25 0.25 {layer=8}
T {CL = 10pF (external load)} 700 -1420 0 0 0.3 0.3 {layer=8}
T {Supply Rails} -600 -960 0 0 0.4 0.4 {layer=4}
T {VDD = 1.8V} -580 -920 0 0 0.3 0.3 {layer=8}
T {VSS = 0V (GND)} -580 -896 0 0 0.3 0.3 {layer=8}
T {Bias: vbn=0.65V, vbcn=0.88V, vbp=0.73V, vbcp=0.475V} -580 -872 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -500 -1780 0 0 {name=XP_inv0
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -500 -1660 0 0 {name=XN_inv0
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -250 -1780 0 0 {name=XP_inv1
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -250 -1660 0 0 {name=XN_inv1
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 200 -1860 0 0 {name=XCin1
W=22.4
L=22.4
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 400 -1800 0 0 {name=XS1
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 200 -1660 0 0 {name=XCin2
W=44.7
L=44.7
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 400 -1600 0 0 {name=XS2
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 200 -1460 0 0 {name=XCin3
W=89.4
L=89.4
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 400 -1400 0 0 {name=XS3
W=1
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 200 -1260 0 0 {name=XCin4
W=178.9
L=178.9
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 400 -1200 0 0 {name=XS4
W=5
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 540 -1800 0 0 {name=XMmid1a
W=0.42
L=10
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 540 -1740 0 0 {name=XMmid1b
W=0.42
L=10
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 540 -1600 0 0 {name=XMmid2a
W=0.42
L=10
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 540 -1540 0 0 {name=XMmid2b
W=0.42
L=10
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} 800 -1850 0 0 {name=XCf
W=22.4
L=22.4
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 900 -1850 0 0 {name=XMpr1
W=0.42
L=10
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 900 -1790 0 0 {name=XMpr2
W=0.42
L=10
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -2040 0 1 {name=p_vdd lab=VDD}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -830 0 1 {name=p_vss lab=VSS}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 100 -2040 0 1 {name=p_vin lab=vin}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1050 -1550 0 0 {name=p_vout lab=vout}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 700 -1550 0 1 {name=p_vcm lab=vcm}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -1950 0 1 {name=p_g0 lab=g0}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -1970 0 1 {name=p_g1 lab=g1}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 700 -1480 0 1 {name=p_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 700 -1460 0 1 {name=p_vbcn lab=vbcn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 700 -1440 0 1 {name=p_vbp lab=vbp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 700 -1420 0 1 {name=p_vbcp lab=vbcp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -480 -1900 0 0 {name=l_g0 lab=g0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -230 -1900 0 0 {name=l_g1 lab=g1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -480 -1750 0 0 {name=l_g0b lab=g0b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -230 -1750 0 0 {name=l_g1b lab=g1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -1900 0 1 {name=l_vin lab=vin}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 350 -1900 0 0 {name=l_mid1 lab=mid1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 350 -1700 0 0 {name=l_mid2 lab=mid2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 350 -1500 0 0 {name=l_mid3 lab=mid3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 350 -1300 0 0 {name=l_mid4 lab=mid4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -1800 0 0 {name=l_inn lab=inn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 -1860 0 1 {name=l_sel0 lab=sel0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 -1660 0 1 {name=l_sel1 lab=sel1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 -1460 0 1 {name=l_sel2 lab=sel2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 -1260 0 1 {name=l_sel3 lab=sel3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -1600 0 0 {name=l_vout lab=vout}
N -480 -1810 -480 -1900 {lab=g0}
N -480 -1750 -480 -1660 {lab=g0b}
N -230 -1810 -230 -1900 {lab=g1}
N -230 -1750 -230 -1660 {lab=g1b}
N -480 -1900 -480 -1970 {lab=VDD}
N -480 -1630 -480 -1600 {lab=VSS}
N -230 -1900 -230 -1970 {lab=VDD}
N -230 -1630 -230 -1600 {lab=VSS}
N 150 -1900 200 -1900 {lab=vin}
N 200 -1828 350 -1828 {lab=mid1}
N 350 -1828 350 -1900 {lab=mid1}
N 150 -1700 200 -1700 {lab=vin}
N 200 -1628 350 -1628 {lab=mid2}
N 350 -1628 350 -1700 {lab=mid2}
N 150 -1500 200 -1500 {lab=vin}
N 200 -1428 350 -1428 {lab=mid3}
N 350 -1428 350 -1500 {lab=mid3}
N 150 -1300 200 -1300 {lab=vin}
N 200 -1228 350 -1228 {lab=mid4}
N 350 -1228 350 -1300 {lab=mid4}
N 420 -1770 420 -1600 {lab=inn}
N 420 -1600 500 -1600 {lab=inn}
N 420 -1570 420 -1400 {lab=inn}
N 420 -1370 420 -1200 {lab=inn}
N 500 -1600 500 -1800 {lab=inn}
N 500 -1800 700 -1800 {lab=inn}
N 700 -1800 800 -1850 {lab=inn}
N 800 -1818 1050 -1818 {lab=vout}
N 1050 -1818 1050 -1600 {lab=vout}
N 700 -1550 780 -1550 {lab=vcm}
N 1050 -1550 980 -1550 {lab=vout}
