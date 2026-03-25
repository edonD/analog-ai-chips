v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 07: SAR ADC v3 — Comparator} -600 -2200 0 0 1.0 1.0 {layer=15}
T {Pre-Amplifier + StrongARM Latch + SR Latch + Output Buffers  —  SKY130A} -600 -2140 0 0 0.5 0.5 {layer=15}
T {Offset < 0.01 mV all corners  |  VDD = 1.8 V  |  Decision < 40 ns for 1 LSB} -600 -2090 0 0 0.4 0.4 {layer=8}
T {Power Gating} -600 -1920 0 0 0.5 0.5 {layer=4}
T {sleep_n -> INV -> sleep_bar -> PMOS header -> vdd_int} -600 -1880 0 0 0.3 0.3 {layer=8}
T {M_slp_n} -580 -1720 0 0 0.3 0.3 {layer=8}
T {1/0.15} -580 -1696 0 0 0.25 0.25 {layer=8}
T {M_slp_p} -580 -1560 0 0 0.3 0.3 {layer=8}
T {2/0.15} -580 -1536 0 0 0.25 0.25 {layer=8}
T {M_pg} -400 -1560 0 0 0.3 0.3 {layer=8}
T {10/0.15} -400 -1536 0 0 0.25 0.25 {layer=8}
T {Bias Generation} -600 -1400 0 0 0.5 0.5 {layer=4}
T {M_bias} -580 -1230 0 0 0.3 0.3 {layer=8}
T {2/2} -580 -1206 0 0 0.25 0.25 {layer=8}
T {Rbias} -420 -1360 0 0 0.25 0.25 {layer=8}
T {200k} -420 -1336 0 0 0.25 0.25 {layer=8}
T {Stage 1: Pre-Amplifier (Continuous)} 0 -2080 0 0 0.5 0.5 {layer=4}
T {NMOS diff pair + PMOS mirror load — Gain ~20-40x} 0 -2040 0 0 0.3 0.3 {layer=8}
T {M_p1 (diode)} -30 -1880 0 0 0.3 0.3 {layer=8}
T {4/1} -30 -1856 0 0 0.25 0.25 {layer=8}
T {M_p2} 360 -1880 0 0 0.3 0.3 {layer=8}
T {4/1} 360 -1856 0 0 0.25 0.25 {layer=8}
T {M_n1} -30 -1580 0 0 0.3 0.3 {layer=8}
T {8/1} -30 -1556 0 0 0.25 0.25 {layer=8}
T {M_n2} 360 -1580 0 0 0.3 0.3 {layer=8}
T {8/1} 360 -1556 0 0 0.25 0.25 {layer=8}
T {M_tail1} 140 -1360 0 0 0.3 0.3 {layer=8}
T {4/2} 140 -1336 0 0 0.25 0.25 {layer=8}
T {Stage 2: StrongARM Latch (Dynamic)} 700 -2080 0 0 0.5 0.5 {layer=4}
T {Clocked by comp_clk: LOW=reset, HIGH=evaluate} 700 -2040 0 0 0.3 0.3 {layer=8}
T {M_rst_p} 720 -1920 0 0 0.3 0.3 {layer=8}
T {2/0.15} 720 -1896 0 0 0.25 0.25 {layer=8}
T {M_rst_n} 1060 -1920 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1060 -1896 0 0 0.25 0.25 {layer=8}
T {M_lp1} 720 -1800 0 0 0.3 0.3 {layer=8}
T {2/0.15} 720 -1776 0 0 0.25 0.25 {layer=8}
T {M_lp2} 1060 -1800 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1060 -1776 0 0 0.25 0.25 {layer=8}
T {M_ln1} 720 -1640 0 0 0.3 0.3 {layer=8}
T {2/0.15} 720 -1616 0 0 0.25 0.25 {layer=8}
T {M_ln2} 1060 -1640 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1060 -1616 0 0 0.25 0.25 {layer=8}
T {M_in1} 720 -1500 0 0 0.3 0.3 {layer=8}
T {4/0.5} 720 -1476 0 0 0.25 0.25 {layer=8}
T {M_in2} 1060 -1500 0 0 0.3 0.3 {layer=8}
T {4/0.5} 1060 -1476 0 0 0.25 0.25 {layer=8}
T {M_tail2} 880 -1280 0 0 0.3 0.3 {layer=8}
T {4/0.15} 880 -1256 0 0 0.25 0.25 {layer=8}
T {cross-coupled} 870 -1720 0 0 0.25 0.25 {layer=5}
T {Stage 3: SR Latch} 1500 -2080 0 0 0.5 0.5 {layer=4}
T {NAND-based — holds decision through StrongARM reset} 1500 -2040 0 0 0.3 0.3 {layer=8}
T {M_sr1_p1} 1480 -1920 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1480 -1896 0 0 0.25 0.25 {layer=8}
T {M_sr1_p2} 1620 -1920 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1620 -1896 0 0 0.25 0.25 {layer=8}
T {M_sr1_n1} 1480 -1720 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1480 -1696 0 0 0.25 0.25 {layer=8}
T {M_sr1_n2} 1620 -1580 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1620 -1556 0 0 0.25 0.25 {layer=8}
T {M_sr2_p1} 1780 -1920 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1780 -1896 0 0 0.25 0.25 {layer=8}
T {M_sr2_p2} 1920 -1920 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1920 -1896 0 0 0.25 0.25 {layer=8}
T {M_sr2_n1} 1780 -1720 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1780 -1696 0 0 0.25 0.25 {layer=8}
T {M_sr2_n2} 1920 -1580 0 0 0.3 0.3 {layer=8}
T {2/0.15} 1920 -1556 0 0 0.25 0.25 {layer=8}
T {Output Buffers} 2100 -2080 0 0 0.5 0.5 {layer=4}
T {2x inverter chains — non-inverting from SR latch} 2100 -2040 0 0 0.3 0.3 {layer=8}
T {M_inv1_p} 2120 -1920 0 0 0.3 0.3 {layer=8}
T {4/0.15} 2120 -1896 0 0 0.25 0.25 {layer=8}
T {M_inv1_n} 2120 -1720 0 0 0.3 0.3 {layer=8}
T {2/0.15} 2120 -1696 0 0 0.25 0.25 {layer=8}
T {M_inv2_p} 2300 -1920 0 0 0.3 0.3 {layer=8}
T {4/0.15} 2300 -1896 0 0 0.25 0.25 {layer=8}
T {M_inv2_n} 2300 -1720 0 0 0.3 0.3 {layer=8}
T {2/0.15} 2300 -1696 0 0 0.25 0.25 {layer=8}
T {M_inv3_p} 2120 -1440 0 0 0.3 0.3 {layer=8}
T {4/0.15} 2120 -1416 0 0 0.25 0.25 {layer=8}
T {M_inv3_n} 2120 -1240 0 0 0.3 0.3 {layer=8}
T {2/0.15} 2120 -1216 0 0 0.25 0.25 {layer=8}
T {M_inv4_p} 2300 -1440 0 0 0.3 0.3 {layer=8}
T {4/0.15} 2300 -1416 0 0 0.25 0.25 {layer=8}
T {M_inv4_n} 2300 -1240 0 0 0.3 0.3 {layer=8}
T {2/0.15} 2300 -1216 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -520 -1680 0 0 {name=XM_slp_n
W=1
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -520 -1520 0 0 {name=XM_slp_p
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -320 -1520 0 0 {name=XM_pg
W=10
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -520 -1190 0 0 {name=XM_bias
W=2
L=2
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -400 -1300 0 0 {name=XRbias
W=0.35
L=200
mult=1
model=res_xhigh_po
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 40 -1820 0 0 {name=XM_p1
W=4
L=1
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 380 -1820 0 1 {name=XM_p2
W=4
L=1
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 40 -1520 0 0 {name=XM_n1
W=8
L=1
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 380 -1520 0 1 {name=XM_n2
W=8
L=1
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 190 -1310 0 0 {name=XM_tail1
W=4
L=2
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 780 -1860 0 0 {name=XM_rst_p
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1100 -1860 0 1 {name=XM_rst_n
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 780 -1740 0 0 {name=XM_lp1
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1100 -1740 0 1 {name=XM_lp2
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 780 -1600 0 0 {name=XM_ln1
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1100 -1600 0 1 {name=XM_ln2
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 780 -1460 0 0 {name=XM_in1
W=4
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1100 -1460 0 1 {name=XM_in2
W=4
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 920 -1240 0 0 {name=XM_tail2
W=4
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1540 -1860 0 0 {name=XM_sr1_p1
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1680 -1860 0 0 {name=XM_sr1_p2
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1600 -1680 0 0 {name=XM_sr1_n1
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1600 -1540 0 0 {name=XM_sr1_n2
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1820 -1860 0 0 {name=XM_sr2_p1
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1960 -1860 0 0 {name=XM_sr2_p2
W=2
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1880 -1680 0 0 {name=XM_sr2_n1
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1880 -1540 0 0 {name=XM_sr2_n2
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2160 -1860 0 0 {name=XM_inv1_p
W=4
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2160 -1680 0 0 {name=XM_inv1_n
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2340 -1860 0 0 {name=XM_inv2_p
W=4
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2340 -1680 0 0 {name=XM_inv2_n
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2160 -1380 0 0 {name=XM_inv3_p
W=4
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2160 -1200 0 0 {name=XM_inv3_n
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 2340 -1380 0 0 {name=XM_inv4_p
W=4
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2340 -1200 0 0 {name=XM_inv4_n
W=2
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -700 -2000 0 1 {name=p_vdd lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -700 -1100 0 1 {name=p_vss lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -200 -1520 0 1 {name=p_inp lab=inp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 500 -1520 0 0 {name=p_inn lab=inn}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 2500 -1770 0 0 {name=p_outp lab=outp}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 2500 -1290 0 0 {name=p_outn lab=outn}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -700 -1680 0 1 {name=p_comp_clk lab=comp_clk}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -700 -1620 0 1 {name=p_sleep_n lab=sleep_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -500 -1620 0 1 {name=l_vbias lab=vbias}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 170 -1310 0 1 {name=l_vbias2 lab=vbias}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -500 -1460 0 0 {name=l_sleep_bar lab=sleep_bar}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -340 -1520 0 1 {name=l_sleep_bar2 lab=sleep_bar}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} -300 -1490 0 0 {name=l_vdd_int lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 60 -1960 0 1 {name=l_vdd_int2 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 360 -1960 0 0 {name=l_vdd_int3 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 60 -1700 0 0 {name=l_d1n lab=d1n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 360 -1700 0 1 {name=l_d1p lab=d1p}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 210 -1380 0 0 {name=l_tail1 lab=tail1}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 800 -1960 0 1 {name=l_vdd_int4 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1080 -1960 0 0 {name=l_vdd_int5 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 800 -1670 0 0 {name=l_outp_i lab=outp_i}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1080 -1670 0 1 {name=l_outn_i lab=outn_i}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1300 0 0 {name=l_tail2 lab=tail2}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 760 -1460 0 1 {name=l_d1p2 lab=d1p}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1120 -1460 0 0 {name=l_d1n2 lab=d1n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 760 -1860 0 1 {name=l_comp_clk2 lab=comp_clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1120 -1860 0 0 {name=l_comp_clk3 lab=comp_clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 900 -1240 0 1 {name=l_comp_clk4 lab=comp_clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1520 -1860 0 1 {name=l_outn_i2 lab=outn_i}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -1860 0 1 {name=l_qbar_sr lab=qbar_sr}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1580 -1680 0 1 {name=l_outn_i3 lab=outn_i}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1580 -1540 0 1 {name=l_qbar_sr2 lab=qbar_sr}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1620 -1790 0 0 {name=l_q_sr lab=q_sr}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1800 -1860 0 1 {name=l_outp_i2 lab=outp_i}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -1860 0 1 {name=l_q_sr2 lab=q_sr}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1860 -1680 0 1 {name=l_outp_i3 lab=outp_i}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1860 -1540 0 1 {name=l_q_sr3 lab=q_sr}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1900 -1790 0 0 {name=l_qbar_sr3 lab=qbar_sr}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1560 -1960 0 1 {name=l_vdd_int6 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1700 -1960 0 0 {name=l_vdd_int7 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1840 -1960 0 1 {name=l_vdd_int8 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1980 -1960 0 0 {name=l_vdd_int9 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 2140 -1860 0 1 {name=l_q_sr4 lab=q_sr}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 2320 -1860 0 1 {name=l_mid_p lab=mid_p}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 2140 -1380 0 1 {name=l_qbar_sr4 lab=qbar_sr}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 2320 -1380 0 1 {name=l_mid_n lab=mid_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 2180 -1960 0 0 {name=l_vdd_int10 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 2360 -1960 0 0 {name=l_vdd_int11 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 2180 -1480 0 0 {name=l_vdd_int12 lab=vdd_int}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 2360 -1480 0 0 {name=l_vdd_int13 lab=vdd_int}
N -700 -2000 -500 -2000 {lab=vdd}
N -500 -2000 -300 -2000 {lab=vdd}
N -300 -2000 -300 -1550 {lab=vdd}
N -500 -2000 -500 -1550 {lab=vdd}
N -700 -1620 -540 -1620 {lab=sleep_n}
N -540 -1520 -540 -1620 {lab=sleep_n}
N -540 -1680 -540 -1620 {lab=sleep_n}
N -500 -1710 -500 -2000 {lab=vdd}
N -500 -1650 -500 -1620 {lab=sleep_bar}
N -500 -1620 -500 -1550 {lab=sleep_bar}
N -500 -1490 -500 -1460 {lab=sleep_bar}
N -500 -1460 -340 -1460 {lab=sleep_bar}
N -340 -1520 -340 -1460 {lab=sleep_bar}
N -300 -1490 -300 -1460 {lab=vdd_int}
N -700 -1100 -500 -1100 {lab=vss}
N -500 -1100 -500 -1160 {lab=vss}
N -400 -1332 -400 -1460 {lab=vdd_int}
N -400 -1460 -300 -1460 {lab=vdd_int}
N -400 -1268 -400 -1220 {lab=vbias}
N -500 -1220 -400 -1220 {lab=vbias}
N -500 -1220 -500 -1190 {lab=vbias}
N -540 -1190 -540 -1220 {lab=vbias}
N -540 -1220 -500 -1220 {lab=vbias}
N -200 -1520 20 -1520 {lab=inp}
N 400 -1520 500 -1520 {lab=inn}
N 60 -1960 60 -1850 {lab=vdd_int}
N 360 -1960 360 -1850 {lab=vdd_int}
N 60 -1790 60 -1700 {lab=d1n}
N 360 -1790 360 -1700 {lab=d1p}
N 20 -1820 -80 -1820 {lab=d1n}
N -80 -1820 -80 -1700 {lab=d1n}
N -80 -1700 60 -1700 {lab=d1n}
N 400 -1820 480 -1820 {lab=d1n}
N 480 -1820 480 -1700 {lab=d1n}
N 60 -1700 480 -1700 {lab=d1n}
N 60 -1550 60 -1490 {lab=d1n}
N 60 -1490 60 -1700 {lab=d1n}
N 360 -1550 360 -1490 {lab=d1p}
N 60 -1490 60 -1420 {lab=d1n}
N 360 -1490 360 -1420 {lab=d1p}
N 60 -1420 210 -1420 {lab=tail1}
N 210 -1420 360 -1420 {lab=tail1}
N 210 -1420 210 -1340 {lab=tail1}
N 210 -1280 210 -1100 {lab=vss}
N -500 -1100 210 -1100 {lab=vss}
N 800 -1960 800 -1890 {lab=vdd_int}
N 1080 -1960 1080 -1890 {lab=vdd_int}
N 800 -1830 800 -1770 {lab=outp_i}
N 1080 -1830 1080 -1770 {lab=outn_i}
N 800 -1710 800 -1670 {lab=outp_i}
N 1080 -1710 1080 -1670 {lab=outn_i}
N 800 -1630 800 -1570 {lab=outp_i}
N 1080 -1630 1080 -1570 {lab=outn_i}
N 800 -1570 800 -1490 {lab=sn1}
N 1080 -1570 1080 -1490 {lab=sn2}
N 800 -1430 800 -1380 {lab=tail2}
N 1080 -1430 1080 -1380 {lab=tail2}
N 800 -1380 1080 -1380 {lab=tail2}
N 940 -1380 940 -1270 {lab=tail2}
N 940 -1210 940 -1100 {lab=vss}
N 210 -1100 940 -1100 {lab=vss}
N 760 -1740 700 -1740 {lab=outn_i}
N 700 -1740 700 -1600 {lab=outn_i}
N 760 -1600 700 -1600 {lab=outn_i}
N 700 -1600 700 -1500 {lab=outn_i}
N 700 -1500 1080 -1500 {lab=outn_i}
N 1080 -1500 1080 -1670 {lab=outn_i}
N 1120 -1740 1180 -1740 {lab=outp_i}
N 1180 -1740 1180 -1600 {lab=outp_i}
N 1120 -1600 1180 -1600 {lab=outp_i}
N 1180 -1600 1180 -1500 {lab=outp_i}
N 800 -1500 1180 -1500 {lab=outp_i}
N 800 -1670 800 -1500 {lab=outp_i}
N 1560 -1960 1560 -1890 {lab=vdd_int}
N 1700 -1960 1700 -1890 {lab=vdd_int}
N 1560 -1830 1560 -1790 {lab=q_sr}
N 1700 -1830 1700 -1790 {lab=q_sr}
N 1560 -1790 1700 -1790 {lab=q_sr}
N 1620 -1790 1620 -1710 {lab=q_sr}
N 1620 -1650 1620 -1610 {lab=mid_sr1}
N 1620 -1570 1620 -1510 {lab=mid_sr1}
N 1620 -1610 1620 -1570 {lab=mid_sr1}
N 1620 -1510 1620 -1100 {lab=vss}
N 1840 -1960 1840 -1890 {lab=vdd_int}
N 1980 -1960 1980 -1890 {lab=vdd_int}
N 1840 -1830 1840 -1790 {lab=qbar_sr}
N 1980 -1830 1980 -1790 {lab=qbar_sr}
N 1840 -1790 1980 -1790 {lab=qbar_sr}
N 1900 -1790 1900 -1710 {lab=qbar_sr}
N 1900 -1650 1900 -1610 {lab=mid_sr2}
N 1900 -1570 1900 -1510 {lab=mid_sr2}
N 1900 -1610 1900 -1570 {lab=mid_sr2}
N 1900 -1510 1900 -1100 {lab=vss}
N 940 -1100 1620 -1100 {lab=vss}
N 1620 -1100 1900 -1100 {lab=vss}
N 2180 -1960 2180 -1890 {lab=vdd_int}
N 2180 -1830 2180 -1770 {lab=mid_p}
N 2180 -1770 2180 -1710 {lab=mid_p}
N 2180 -1650 2180 -1100 {lab=vss}
N 2360 -1960 2360 -1890 {lab=vdd_int}
N 2360 -1830 2360 -1770 {lab=outp}
N 2360 -1770 2500 -1770 {lab=outp}
N 2360 -1650 2360 -1100 {lab=vss}
N 2180 -1480 2180 -1410 {lab=vdd_int}
N 2180 -1350 2180 -1290 {lab=mid_n}
N 2180 -1290 2180 -1230 {lab=mid_n}
N 2180 -1170 2180 -1100 {lab=vss}
N 2360 -1480 2360 -1410 {lab=vdd_int}
N 2360 -1350 2360 -1290 {lab=outn}
N 2360 -1290 2500 -1290 {lab=outn}
N 2360 -1170 2360 -1100 {lab=vss}
N 1900 -1100 2180 -1100 {lab=vss}
N 2180 -1100 2360 -1100 {lab=vss}
N 2140 -1860 2140 -1680 {lab=q_sr}
N 2140 -1680 2140 -1770 {lab=q_sr}
N 2180 -1770 2320 -1770 {lab=mid_p}
N 2320 -1770 2320 -1860 {lab=mid_p}
N 2320 -1680 2320 -1770 {lab=mid_p}
N 2140 -1380 2140 -1200 {lab=qbar_sr}
N 2180 -1290 2320 -1290 {lab=mid_n}
N 2320 -1290 2320 -1380 {lab=mid_n}
N 2320 -1200 2320 -1290 {lab=mid_n}
N -700 -1680 -700 -1620 {lab=comp_clk}
