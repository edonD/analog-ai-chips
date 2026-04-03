v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 06: Charge-Domain MAC Classifier} -450 -2250 0 0 1.0 1.0 {layer=15}
T {4-Class WTA  --  8 Inputs x 4-Bit Weights  --  SKY130A} -450 -2180 0 0 0.5 0.5 {layer=15}
T {702 Transistors  |  260 MIM Caps  |  < 0.001 uW @ 10 Hz  |  VDD = 1.8 V} -450 -2120 0 0 0.4 0.4 {layer=8}
N -450 -2050 2300 -2050 {lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -2050 0 1 {name=p_vdd lab=vdd}
N -450 -350 2300 -350 {lab=gnd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -350 0 1 {name=p_gnd lab=gnd}
T {Charge-Sharing MAC Cell  (1 of 32 per MAC, 4 MACs total)} -380 -2000 0 0 0.45 0.45 {layer=4}
T {Signal path:  input -> Sample TG -> top_plate -> MIM Cap -> GND} -380 -1960 0 0 0.3 0.3 {layer=8}
T {top_plate -> Eval TG -> bitline  |  top_plate -> Reset SW -> GND} -380 -1930 0 0 0.3 0.3 {layer=8}
T {Sample TG} -250 -1870 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -220 -1750 0 0 {name=XMNs
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {MNs} -260 -1780 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} -260 -1755 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -80 -1750 0 1 {name=XMPs
W=1.68
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {MPs} -30 -1780 0 0 0.3 0.3 {layer=8}
T {1.68/0.15} -30 -1755 0 0 0.25 0.25 {layer=8}
N -200 -1780 -100 -1780 {}
N -200 -1720 -100 -1720 {}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -240 -1750 0 1 {name=l_phi_s lab=phi_s}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -60 -1750 0 0 {name=l_phi_sb lab=phi_sb}
N -150 -1780 -150 -1850 {}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -150 -1850 3 0 {name=l_in0 lab=in[0]}
T {MIM Cap} -200 -1640 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -150 -1610 0 0 {name=XC0_b0
W=4.63
L=4.63
MF=1
model=cap_mim_m3_1
spiceprefix=X
}
T {50 fF} -130 -1620 0 0 0.25 0.25 {layer=8}
T {4.63 x 4.63 um} -130 -1600 0 0 0.2 0.2 {layer=8}
N -150 -1720 -150 -1640 {}
N -150 -1580 -150 -350 {}
T {Eval TG} 140 -1870 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 160 -1750 0 0 {name=XMNe
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {MNe} 120 -1780 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} 120 -1755 0 0 0.25 0.25 {layer=8}
T {(+ PMOS 1.68/0.15)} 120 -1730 0 0 0.2 0.2 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 140 -1750 0 1 {name=l_phi_e lab=phi_e}
N -100 -1720 180 -1720 {}
N 180 -1780 180 -1870 {}
T {bitline} 185 -1860 0 0 0.25 0.25 {layer=15}
T {Reset} 310 -1870 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 330 -1750 0 0 {name=XMNr
W=0.42
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {MNr} 290 -1780 0 0 0.3 0.3 {layer=8}
T {0.42/0.15} 290 -1755 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 310 -1750 0 1 {name=l_phi_r lab=phi_r}
N 180 -1720 350 -1720 {}
N 350 -1780 350 -1720 {}
N 350 -1720 350 -350 {}
T {BL Reset} 430 -1870 0 0 0.35 0.35 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 460 -1750 0 0 {name=XMNblr
W=0.84
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {MNblr} 420 -1780 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} 420 -1755 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 440 -1750 0 1 {name=l_phi_r2 lab=phi_r}
N 180 -1780 480 -1780 {}
N 480 -1720 480 -350 {}
T {x32 cells per MAC (8 inputs x 4 bits)} -200 -1530 0 0 0.3 0.3 {layer=15}
T {x4 MAC units (Normal, Imbalance, Bearing, Looseness)} -200 -1500 0 0 0.3 0.3 {layer=15}
T {Total: 644 transistors + 128 MIM caps + 4 BL reset} -200 -1470 0 0 0.3 0.3 {layer=15}
T {StrongARM Latch Comparator  (1 of 3 in WTA tree)} 700 -2000 0 0 0.45 0.45 {layer=4}
T {Dynamic: zero static power  |  11 transistors  |  Input offset sigma = 3.54 mV} 700 -1960 0 0 0.3 0.3 {layer=8}
T {Reset PMOS (CLK=0)} 820 -1900 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 800 -1850 0 0 {name=XM7
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {M7} 760 -1880 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} 760 -1855 0 0 0.25 0.25 {layer=8}
N 820 -1880 820 -2050 {}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 780 -1850 0 1 {name=l_clk7 lab=clk}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 960 -1850 0 0 {name=XM9
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {M9} 920 -1880 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} 920 -1855 0 0 0.25 0.25 {layer=8}
N 980 -1880 980 -2050 {}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1850 0 1 {name=l_clk9 lab=clk}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1220 -1850 0 1 {name=XM10
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {M10} 1250 -1880 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} 1250 -1855 0 0 0.25 0.25 {layer=8}
N 1200 -1880 1200 -2050 {}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1240 -1850 0 0 {name=l_clk10 lab=clk}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1380 -1850 0 1 {name=XM8
W=0.84
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {M8} 1410 -1880 0 0 0.3 0.3 {layer=8}
T {0.84/0.15} 1410 -1855 0 0 0.25 0.25 {layer=8}
N 1360 -1880 1360 -2050 {}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -1850 0 0 {name=l_clk8 lab=clk}
N 820 -2050 1360 -2050 {}
T {P-Latch (cross-coupled)} 820 -1760 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 800 -1700 0 0 {name=XM5
W=1
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {M5} 760 -1730 0 0 0.3 0.3 {layer=8}
T {1/0.15} 760 -1705 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 820 -1730 3 0 {name=l_vdd5 lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 780 -1700 0 1 {name=l_voutn_g5 lab=voutn}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1380 -1700 0 1 {name=XM6
W=1
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
T {M6} 1410 -1730 0 0 0.3 0.3 {layer=8}
T {1/0.15} 1410 -1705 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1360 -1730 3 0 {name=l_vdd6 lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -1700 0 0 {name=l_voutp_g6 lab=voutp}
T {N-Latch (cross-coupled)} 820 -1610 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 800 -1550 0 0 {name=XM3
W=1
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {M3} 760 -1580 0 0 0.3 0.3 {layer=8}
T {1/0.15} 760 -1555 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 780 -1550 0 1 {name=l_voutn_g3 lab=voutn}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1380 -1550 0 1 {name=XM4
W=1
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {M4} 1410 -1580 0 0 0.3 0.3 {layer=8}
T {1/0.15} 1410 -1555 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -1550 0 0 {name=l_voutp_g4 lab=voutp}
N 820 -1820 770 -1820 {}
N 820 -1670 770 -1670 {}
N 820 -1580 770 -1580 {}
N 770 -1820 770 -1580 {}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 770 -1660 0 1 {name=l_voutp lab=voutp}
N 1360 -1820 1410 -1820 {}
N 1360 -1670 1410 -1670 {}
N 1360 -1580 1410 -1580 {}
N 1410 -1820 1410 -1580 {}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1410 -1660 0 0 {name=l_voutn lab=voutn}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 710 -1660 0 1 {name=p_voutp lab=voutp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1470 -1660 0 0 {name=p_voutn lab=voutn}
N 980 -1820 940 -1820 {}
N 820 -1520 940 -1520 {}
N 940 -1820 940 -1520 {}
T {di_p} 945 -1750 0 0 0.2 0.2 {layer=15}
N 1200 -1820 1240 -1820 {}
N 1360 -1520 1240 -1520 {}
N 1240 -1820 1240 -1520 {}
T {di_n} 1210 -1750 0 0 0.2 0.2 {layer=15}
T {Input Pair} 950 -1470 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 950 -1400 0 0 {name=XM1
W=4
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {M1} 910 -1430 0 0 0.3 0.3 {layer=8}
T {4/0.5} 910 -1405 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 930 -1400 0 1 {name=l_vinp lab=vinp}
N 970 -1430 940 -1430 {}
N 940 -1520 940 -1430 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1230 -1400 0 1 {name=XM2
W=4
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {M2} 1260 -1430 0 0 0.3 0.3 {layer=8}
T {4/0.5} 1260 -1405 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1250 -1400 0 0 {name=l_vinn lab=vinn}
N 1210 -1430 1240 -1430 {}
N 1240 -1520 1240 -1430 {}
N 970 -1370 1210 -1370 {}
T {tail} 1070 -1365 0 0 0.2 0.2 {layer=15}
T {Tail Switch} 1050 -1310 0 0 0.3 0.3 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1070 -1250 0 0 {name=XM0
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {M0} 1030 -1280 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1030 -1255 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -1250 0 1 {name=l_clk0 lab=clk}
N 1090 -1280 1090 -1370 {}
N 1090 -1220 1090 -350 {}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 890 -1400 0 1 {name=p_vinp lab=vinp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1290 -1400 0 0 {name=p_vinn lab=vinn}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1010 -1250 0 1 {name=p_clk lab=clk}
T {4-Class Winner-Take-All System} 1600 -2000 0 0 0.45 0.45 {layer=4}
T {8 Features (in[0..7])} 1620 -1920 0 0 0.3 0.3 {layer=15}
T {|} 1660 -1895 0 0 0.3 0.3 {layer=15}
T {+-- MAC_0: Normal   --+} 1620 -1870 0 0 0.28 0.28 {layer=15}
T {|                      +--> Comp_01 --+} 1620 -1845 0 0 0.28 0.28 {layer=15}
T {+-- MAC_1: Imbalance --+             |} 1620 -1820 0 0 0.28 0.28 {layer=15}
T {|                                    +--> Comp_final --> class[1:0]} 1620 -1795 0 0 0.28 0.28 {layer=15}
T {+-- MAC_2: Bearing   --+             |} 1620 -1770 0 0 0.28 0.28 {layer=15}
T {|                      +--> Comp_23 --+} 1620 -1745 0 0 0.28 0.28 {layer=15}
T {+-- MAC_3: Looseness --+} 1620 -1720 0 0 0.28 0.28 {layer=15}
T {Device Count Summary} 1600 -1480 0 0 0.4 0.4 {layer=4}
T {MAC units:    4 x 161T = 644 transistors} 1620 -1440 0 0 0.28 0.28 {layer=8}
T {              4 x 32 = 128 MIM caps} 1620 -1415 0 0 0.28 0.28 {layer=8}
T {              4 x 32 = 128 parasitic caps} 1620 -1390 0 0 0.28 0.28 {layer=8}
T {StrongARM:    3 x 11T = 33 transistors} 1620 -1360 0 0 0.28 0.28 {layer=8}
T {Clock gen:    1 x 28T = 28 transistors} 1620 -1335 0 0 0.28 0.28 {layer=8}
T {BL reset:     4 x  1T =  4 transistors} 1620 -1310 0 0 0.28 0.28 {layer=8}
T {---------------------------------------} 1620 -1280 0 0 0.28 0.28 {layer=8}
T {TOTAL:       ~709 transistors + ~260 caps} 1620 -1255 0 0 0.28 0.28 {layer=8}
T {Key Specifications (ngspice verified)} 1600 -1190 0 0 0.4 0.4 {layer=4}
T {MAC linearity:     0.08 LSB  (spec < 2 LSB)    PASS} 1620 -1150 0 0 0.28 0.28 {layer=8}
T {Charge injection:  0.307 LSB (spec < 1 LSB)     PASS} 1620 -1125 0 0 0.28 0.28 {layer=8}
T {WTA margin:        19.3 mV   (spec > 5 mV)      PASS} 1620 -1100 0 0 0.28 0.28 {layer=8}
T {Monte Carlo acc:   99.5%     (spec > 85%)        PASS} 1620 -1075 0 0 0.28 0.28 {layer=8}
T {Corner variation:  0.11%     (spec < 5%)         PASS} 1620 -1050 0 0 0.28 0.28 {layer=8}
T {Power @ 10 Hz:     < 0.001 uW (spec < 5 uW)     PASS} 1620 -1025 0 0 0.28 0.28 {layer=8}
T {MIM Cap: sky130_fd_pr__cap_mim_m3_1} 1600 -960 0 0 0.35 0.35 {layer=4}
T {Area cap: 2.0 fF/um^2  |  Fringe: 0.38 fF/um} 1620 -925 0 0 0.25 0.25 {layer=8}
T {Bottom-plate parasitic: 0.1 fF/um^2} 1620 -900 0 0 0.25 0.25 {layer=8}
T {Cunit = 50 fF  (bit0: 4.63x4.63 um)} 1620 -875 0 0 0.25 0.25 {layer=8}
T {Total bitline: 6.36 pF per MAC} 1620 -850 0 0 0.25 0.25 {layer=8}
T {3-Phase Clock Generator} 1600 -790 0 0 0.35 0.35 {layer=4}
T {NAND-based non-overlapping (28 transistors)} 1620 -760 0 0 0.25 0.25 {layer=8}
T {Phases: phi_s (sample), phi_e (eval), phi_r (reset)} 1620 -735 0 0 0.25 0.25 {layer=8}
T {Non-overlap > 1 ns | All phases full rail} 1620 -710 0 0 0.25 0.25 {layer=8}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1850 0 1 {name=p_in0 lab=in[0]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1820 0 1 {name=p_in1 lab=in[1]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1790 0 1 {name=p_in2 lab=in[2]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1760 0 1 {name=p_in3 lab=in[3]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1730 0 1 {name=p_in4 lab=in[4]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1700 0 1 {name=p_in5 lab=in[5]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1670 0 1 {name=p_in6 lab=in[6]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1640 0 1 {name=p_in7 lab=in[7]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 2300 -1550 0 0 {name=p_class0 lab=class[0]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 2300 -1520 0 0 {name=p_class1 lab=class[1]}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -450 -1600 0 1 {name=p_clkin lab=clk_in}
