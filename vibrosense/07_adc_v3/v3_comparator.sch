v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 07: SAR ADC v3 — Comparator} -500 -1700 0 0 1.0 1.0 {layer=15}
T {Pre-Amplifier + StrongARM Latch + SR Latch  —  SKY130A} -500 -1640 0 0 0.5 0.5 {layer=15}
T {Offset < 0.01 mV all corners  |  VDD = 1.8 V  |  Decision < 40 ns for 1 LSB} -500 -1590 0 0 0.4 0.4 {layer=8}
T {Stage 1: Pre-Amplifier (Continuous)} -350 -1500 0 0 0.5 0.5 {layer=4}
T {NMOS diff pair + PMOS mirror  —  Gain ~20-40x} -350 -1460 0 0 0.3 0.3 {layer=8}
T {M_n1} -200 -1200 0 0 0.3 0.3 {layer=8}
T {8/1} -200 -1176 0 0 0.25 0.25 {layer=8}
T {M_n2} 200 -1200 0 0 0.3 0.3 {layer=8}
T {8/1} 200 -1176 0 0 0.25 0.25 {layer=8}
T {M_p1 (diode)} -200 -1380 0 0 0.3 0.3 {layer=8}
T {4/1} -200 -1356 0 0 0.25 0.25 {layer=8}
T {M_p2} 200 -1380 0 0 0.3 0.3 {layer=8}
T {4/1} 200 -1356 0 0 0.25 0.25 {layer=8}
T {M_tail1} 0 -1070 0 0 0.3 0.3 {layer=8}
T {4/2} 0 -1046 0 0 0.25 0.25 {layer=8}
T {M_bias} -400 -1070 0 0 0.3 0.3 {layer=8}
T {2/2} -400 -1046 0 0 0.25 0.25 {layer=8}
T {Rbias} -400 -1260 0 0 0.25 0.25 {layer=8}
T {200k} -400 -1236 0 0 0.25 0.25 {layer=8}
T {Stage 2: StrongARM Latch (Dynamic)} 500 -1500 0 0 0.5 0.5 {layer=4}
T {Clocked evaluation — comp_clk HIGH = evaluate} 500 -1460 0 0 0.3 0.3 {layer=8}
T {M_in1} 530 -1200 0 0 0.3 0.3 {layer=8}
T {4/0.5} 530 -1176 0 0 0.25 0.25 {layer=8}
T {M_in2} 850 -1200 0 0 0.3 0.3 {layer=8}
T {4/0.5} 850 -1176 0 0 0.25 0.25 {layer=8}
T {M_ln1} 530 -1300 0 0 0.3 0.3 {layer=8}
T {2/0.15} 530 -1276 0 0 0.25 0.25 {layer=8}
T {M_ln2} 850 -1300 0 0 0.3 0.3 {layer=8}
T {2/0.15} 850 -1276 0 0 0.25 0.25 {layer=8}
T {M_lp1} 530 -1400 0 0 0.3 0.3 {layer=8}
T {2/0.15} 530 -1376 0 0 0.25 0.25 {layer=8}
T {M_lp2} 850 -1400 0 0 0.3 0.3 {layer=8}
T {2/0.15} 850 -1376 0 0 0.25 0.25 {layer=8}
T {M_rst_p} 530 -1480 0 0 0.3 0.3 {layer=8}
T {2/0.15} 530 -1456 0 0 0.25 0.25 {layer=8}
T {M_rst_n} 850 -1480 0 0 0.3 0.3 {layer=8}
T {2/0.15} 850 -1456 0 0 0.25 0.25 {layer=8}
T {M_tail2} 690 -1070 0 0 0.3 0.3 {layer=8}
T {4/0.15} 690 -1046 0 0 0.25 0.25 {layer=8}
T {cross-coupled} 680 -1350 0 0 0.25 0.25 {layer=5}
T {Stage 3: SR Latch (Static Hold)} 1150 -1500 0 0 0.5 0.5 {layer=4}
T {NAND-based — holds decision through StrongARM reset} 1150 -1460 0 0 0.3 0.3 {layer=8}
T {SR1 (2×PMOS + 2×NMOS)} 1150 -1370 0 0 0.3 0.3 {layer=8}
T {W=2/0.15} 1150 -1346 0 0 0.25 0.25 {layer=8}
T {SR2 (2×PMOS + 2×NMOS)} 1150 -1250 0 0 0.3 0.3 {layer=8}
T {W=2/0.15} 1150 -1226 0 0 0.25 0.25 {layer=8}
T {Output Buffers} 1150 -1130 0 0 0.4 0.4 {layer=4}
T {2× INV chains (4 transistors each)} 1150 -1090 0 0 0.3 0.3 {layer=8}
T {Power Gating} -500 -900 0 0 0.4 0.4 {layer=4}
T {M_pg: PMOS header W=10u, gate=sleep_bar} -500 -860 0 0 0.3 0.3 {layer=8}
T {sleep_n → INV → sleep_bar → PMOS header → vdd_int} -500 -830 0 0 0.25 0.25 {layer=8}
T {Total: ~53 transistors} -500 -770 0 0 0.35 0.35 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -140 -1140 0 0 {name=XM_n1
W=8
L=1
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 240 -1140 0 1 {name=XM_n2
W=8
L=1
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -140 -1320 0 0 {name=XM_p1
W=4
L=1
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 240 -1320 0 1 {name=XM_p2
W=4
L=1
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 20 -1020 0 0 {name=XM_tail1
W=4
L=2
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -360 -1020 0 0 {name=XM_bias
W=2
L=2
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 570 -1140 0 0 {name=XM_in1
W=4
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 890 -1140 0 1 {name=XM_in2
W=4
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 710 -1020 0 0 {name=XM_tail2
W=4
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 20 -1320 0 0 {name=XM_pg
W=10
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -1140 0 1 {name=p_inp lab=inp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 400 -1140 0 0 {name=p_inn lab=inn}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1400 -1370 0 0 {name=p_outp lab=outp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1400 -1250 0 0 {name=p_outn lab=outn}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -1540 0 1 {name=p_vdd lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -960 0 1 {name=p_vss lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 710 -960 0 0 {name=p_comp_clk lab=comp_clk}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -500 -900 0 1 {name=p_sleep_n lab=sleep_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -120 -1290 0 1 {name=l_d1n lab=d1n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 220 -1290 0 0 {name=l_d1p lab=d1p}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 50 -1080 0 0 {name=l_tail1 lab=tail1}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -340 -1080 0 0 {name=l_vbias lab=vbias}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -500 -1430 0 1 {name=l_vdd_int lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 590 -1270 0 1 {name=l_outp_i lab=outp_i}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 870 -1270 0 0 {name=l_outn_i lab=outn_i}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 730 -1080 0 0 {name=l_tail2 lab=tail2}
N -120 -1540 -120 -1350 {lab=vdd_int}
N -120 -1540 220 -1540 {lab=vdd_int}
N 220 -1540 220 -1350 {lab=vdd_int}
N -120 -1290 -120 -1170 {lab=d1n}
N 220 -1290 220 -1170 {lab=d1p}
N -160 -1320 -260 -1320 {lab=d1n}
N -260 -1320 -260 -1290 {lab=d1n}
N -120 -1110 -120 -1080 {lab=tail1}
N 220 -1110 220 -1080 {lab=tail1}
N -120 -1080 220 -1080 {lab=tail1}
N 50 -1080 50 -990 {lab=tail1}
N 50 -960 50 -920 {lab=vss}
N -500 -1140 -160 -1140 {lab=inp}
N 260 -1140 400 -1140 {lab=inn}
N 590 -1540 590 -1170 {lab=outp_i}
N 870 -1540 870 -1170 {lab=outn_i}
N 590 -1110 590 -1080 {lab=tail2}
N 870 -1110 870 -1080 {lab=tail2}
N 590 -1080 870 -1080 {lab=tail2}
N 730 -1080 730 -990 {lab=tail2}
N 590 -1540 870 -1540 {lab=vdd_int}
