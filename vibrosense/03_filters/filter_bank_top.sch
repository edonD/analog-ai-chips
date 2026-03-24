v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}

T {VibroSense Block 03: 5-Channel Filter Bank -- Top Level} -400 -1550 0 0 0.65 0.65 {layer=15}
T {5x Bias DAC + Bias Distribution + Pseudo-Differential BPF -- SKY130A} -400 -1500 0 0 0.3 0.3 {layer=15}
T {Total Power: 42.5 uW  |  VDD = 1.8 V  |  20-bit digital control (4 per channel)} -400 -1465 0 0 0.25 0.25 {layer=8}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -500 -750 0 1 {name=p_vinp lab=vinp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -500 -700 0 1 {name=p_vinn lab=vinn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -500 -650 0 1 {name=p_vcm lab=vcm}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -500 -600 0 1 {name=p_iref lab=iref}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -500 -1400 0 1 {name=p_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -500 -100 0 1 {name=p_vss lab=vss}
N -500 -750 -200 -750 {lab=vinp}
N -500 -700 -200 -700 {lab=vinn}
N -500 -650 -200 -650 {lab=vcm}
N -500 -600 -200 -600 {lab=iref}
N -200 -1350 -200 -200 {lab=}
N -500 -1400 1500 -1400 {lab=vdd}
N -500 -100 1500 -100 {lab=vss}
N -100 -1300 1200 -1300 {lab=}
N -100 -1110 1200 -1110 {lab=}
N -100 -1300 -100 -1110 {lab=}
N 1200 -1300 1200 -1110 {lab=}
N 250 -1300 250 -1110 {lab=}
N 550 -1300 550 -1110 {lab=}
T {Ch1} -80 -1285 0 0 0.35 0.35 {layer=4}
T {f0=224 Hz, Q=0.75} -80 -1255 0 0 0.2 0.2 {layer=8}
T {4.7 uW} -80 -1235 0 0 0.2 0.2 {layer=5}
T {4-bit DAC} 50 -1210 0 0 0.28 0.28 {layer=4}
T {Bias Dist} 330 -1210 0 0 0.28 0.28 {layer=4}
T {Pseudo-Diff BPF} 700 -1210 0 0 0.28 0.28 {layer=4}
T {6 OTAs + 4C + 4PR} 680 -1180 0 0 0.18 0.18 {layer=5}
N -200 -1225 -100 -1225 {lab=vinp}
N -200 -1185 -100 -1185 {lab=vinn}
N -200 -1155 -100 -1155 {lab=iref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -1100 3 0 {name=l_ch1_b0 lab=ch1_b0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 75 -1100 3 0 {name=l_ch1_b1 lab=ch1_b1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 130 -1100 3 0 {name=l_ch1_b2 lab=ch1_b2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 185 -1100 3 0 {name=l_ch1_b3 lab=ch1_b3}
N 1200 -1225 1500 -1225 {lab=ch1_outp}
N 1200 -1185 1500 -1185 {lab=ch1_outn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -1225 0 0 {name=p_ch1_outp lab=ch1_outp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -1185 0 0 {name=p_ch1_outn lab=ch1_outn}
N -100 -1060 1200 -1060 {lab=}
N -100 -870 1200 -870 {lab=}
N -100 -1060 -100 -870 {lab=}
N 1200 -1060 1200 -870 {lab=}
N 250 -1060 250 -870 {lab=}
N 550 -1060 550 -870 {lab=}
T {Ch2} -80 -1045 0 0 0.35 0.35 {layer=4}
T {f0=1000 Hz, Q=0.67} -80 -1015 0 0 0.2 0.2 {layer=8}
T {4.7 uW} -80 -995 0 0 0.2 0.2 {layer=5}
T {4-bit DAC} 50 -970 0 0 0.28 0.28 {layer=4}
T {Bias Dist} 330 -970 0 0 0.28 0.28 {layer=4}
T {Pseudo-Diff BPF} 700 -970 0 0 0.28 0.28 {layer=4}
T {6 OTAs + 4C + 4PR} 680 -940 0 0 0.18 0.18 {layer=5}
N -200 -985 -100 -985 {lab=vinp}
N -200 -945 -100 -945 {lab=vinn}
N -200 -915 -100 -915 {lab=iref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -860 3 0 {name=l_ch2_b0 lab=ch2_b0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 75 -860 3 0 {name=l_ch2_b1 lab=ch2_b1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 130 -860 3 0 {name=l_ch2_b2 lab=ch2_b2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 185 -860 3 0 {name=l_ch2_b3 lab=ch2_b3}
N 1200 -985 1500 -985 {lab=ch2_outp}
N 1200 -945 1500 -945 {lab=ch2_outn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -985 0 0 {name=p_ch2_outp lab=ch2_outp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -945 0 0 {name=p_ch2_outn lab=ch2_outn}
N -100 -820 1200 -820 {lab=}
N -100 -630 1200 -630 {lab=}
N -100 -820 -100 -630 {lab=}
N 1200 -820 1200 -630 {lab=}
N 250 -820 250 -630 {lab=}
N 550 -820 550 -630 {lab=}
T {Ch3} -80 -805 0 0 0.35 0.35 {layer=4}
T {f0=3162 Hz, Q=1.05} -80 -775 0 0 0.2 0.2 {layer=8}
T {4.7 uW} -80 -755 0 0 0.2 0.2 {layer=5}
T {4-bit DAC} 50 -730 0 0 0.28 0.28 {layer=4}
T {Bias Dist} 330 -730 0 0 0.28 0.28 {layer=4}
T {Pseudo-Diff BPF} 700 -730 0 0 0.28 0.28 {layer=4}
T {6 OTAs + 4C + 4PR} 680 -700 0 0 0.18 0.18 {layer=5}
N -200 -745 -100 -745 {lab=vinp}
N -200 -705 -100 -705 {lab=vinn}
N -200 -675 -100 -675 {lab=iref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -620 3 0 {name=l_ch3_b0 lab=ch3_b0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 75 -620 3 0 {name=l_ch3_b1 lab=ch3_b1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 130 -620 3 0 {name=l_ch3_b2 lab=ch3_b2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 185 -620 3 0 {name=l_ch3_b3 lab=ch3_b3}
N 1200 -745 1500 -745 {lab=ch3_outp}
N 1200 -705 1500 -705 {lab=ch3_outn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -745 0 0 {name=p_ch3_outp lab=ch3_outp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -705 0 0 {name=p_ch3_outn lab=ch3_outn}
N -100 -580 1200 -580 {lab=}
N -100 -390 1200 -390 {lab=}
N -100 -580 -100 -390 {lab=}
N 1200 -580 1200 -390 {lab=}
N 250 -580 250 -390 {lab=}
N 550 -580 550 -390 {lab=}
T {Ch4} -80 -565 0 0 0.35 0.35 {layer=4}
T {f0=7071 Hz, Q=1.41} -80 -535 0 0 0.2 0.2 {layer=8}
T {10.3 uW} -80 -515 0 0 0.2 0.2 {layer=5}
T {4-bit DAC} 50 -490 0 0 0.28 0.28 {layer=4}
T {Bias Dist} 330 -490 0 0 0.28 0.28 {layer=4}
T {Pseudo-Diff BPF} 700 -490 0 0 0.28 0.28 {layer=4}
T {6 OTAs + 4C + 4PR} 680 -460 0 0 0.18 0.18 {layer=5}
N -200 -505 -100 -505 {lab=vinp}
N -200 -465 -100 -465 {lab=vinn}
N -200 -435 -100 -435 {lab=iref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -380 3 0 {name=l_ch4_b0 lab=ch4_b0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 75 -380 3 0 {name=l_ch4_b1 lab=ch4_b1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 130 -380 3 0 {name=l_ch4_b2 lab=ch4_b2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 185 -380 3 0 {name=l_ch4_b3 lab=ch4_b3}
N 1200 -505 1500 -505 {lab=ch4_outp}
N 1200 -465 1500 -465 {lab=ch4_outn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -505 0 0 {name=p_ch4_outp lab=ch4_outp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -465 0 0 {name=p_ch4_outn lab=ch4_outn}
N -100 -340 1200 -340 {lab=}
N -100 -150 1200 -150 {lab=}
N -100 -340 -100 -150 {lab=}
N 1200 -340 1200 -150 {lab=}
N 250 -340 250 -150 {lab=}
N 550 -340 550 -150 {lab=}
T {Ch5} -80 -325 0 0 0.35 0.35 {layer=4}
T {f0=14142 Hz, Q=1.41} -80 -295 0 0 0.2 0.2 {layer=8}
T {18.2 uW} -80 -275 0 0 0.2 0.2 {layer=5}
T {4-bit DAC} 50 -250 0 0 0.28 0.28 {layer=4}
T {Bias Dist} 330 -250 0 0 0.28 0.28 {layer=4}
T {Pseudo-Diff BPF} 700 -250 0 0 0.28 0.28 {layer=4}
T {6 OTAs + 4C + 4PR} 680 -220 0 0 0.18 0.18 {layer=5}
N -200 -265 -100 -265 {lab=vinp}
N -200 -225 -100 -225 {lab=vinn}
N -200 -195 -100 -195 {lab=iref}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -140 3 0 {name=l_ch5_b0 lab=ch5_b0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 75 -140 3 0 {name=l_ch5_b1 lab=ch5_b1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 130 -140 3 0 {name=l_ch5_b2 lab=ch5_b2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 185 -140 3 0 {name=l_ch5_b3 lab=ch5_b3}
N 1200 -265 1500 -265 {lab=ch5_outp}
N 1200 -225 1500 -225 {lab=ch5_outn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -265 0 0 {name=p_ch5_outp lab=ch5_outp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1500 -225 0 0 {name=p_ch5_outn lab=ch5_outn}
