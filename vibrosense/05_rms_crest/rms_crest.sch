v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 05: True RMS + Peak + Crest Factor} -380 -1520 0 0 1.0 1.0 {layer=15}
T {Single-Pair MOSFET Square-Law Squarer -- SKY130A} -380 -1460 0 0 0.5 0.5 {layer=15}
T {10 MOSFETs  |  8 Resistors  |  3 Capacitors  |  8.0 uW  |  All PVT PASS} -380 -1410 0 0 0.4 0.4 {layer=8}
T {MOSFET Square-Law Squarer} -80 -1300 0 0 0.5 0.5 {layer=4}
T {Rsig} -25 -1100 0 0 0.3 0.3 {layer=8}
T {100k} -25 -1078 0 0 0.25 0.25 {layer=8}
C {/usr/share/xschem/xschem_library/devices/res.sym} 20 -1100 0 0 {name=R_sig
value=100k}
N 20 -1340 20 -1130 {lab=vdd}
N 20 -1070 20 -860 {lab=sig_d}
T {XMs} -35 -700 0 0 0.3 0.3 {layer=8}
T {0.84/6} -35 -678 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 0 -720 0 0 {name=XMs
W=0.84
L=6
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
N 20 -860 20 -750 {lab=sig_d}
N 20 -690 20 -260 {lab=gnd}
T {Riso_s} 105 -905 0 0 0.25 0.25 {layer=8}
T {1k} 125 -885 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/res.sym} 140 -860 3 0 {name=R_iso_s
value=1k}
N 20 -860 110 -860 {lab=sig_d}
T {Rref} 255 -1100 0 0 0.3 0.3 {layer=8}
T {100k} 255 -1078 0 0 0.25 0.25 {layer=8}
C {/usr/share/xschem/xschem_library/devices/res.sym} 300 -1100 0 0 {name=R_ref
value=100k}
N 300 -1340 300 -1130 {lab=vdd}
N 300 -1070 300 -860 {lab=ref_d}
T {XMr} 245 -700 0 0 0.3 0.3 {layer=8}
T {0.84/6} 245 -678 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 280 -720 0 0 {name=XMr
W=0.84
L=6
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
N 300 -860 300 -750 {lab=ref_d}
N 300 -690 300 -260 {lab=gnd}
T {Riso_r} 385 -905 0 0 0.25 0.25 {layer=8}
T {1k} 405 -885 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/res.sym} 420 -860 3 0 {name=R_iso_r
value=1k}
N 300 -860 390 -860 {lab=ref_d}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -20 -720 0 1 {name=l_inp1 lab=inp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 260 -720 0 1 {name=l_vcm1 lab=vcm}
T {Low-Pass Filters} 490 -1300 0 0 0.45 0.45 {layer=4}
T {fc = 50 Hz} 490 -1265 0 0 0.3 0.3 {layer=8}
T {Rlpf} 540 -905 0 0 0.25 0.25 {layer=8}
T {3.18M} 540 -885 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/res.sym} 570 -860 3 0 {name=R_lpf_sig
value=3.18Meg}
N 170 -860 540 -860 {lab=sq_sig}
T {Clpf} 615 -735 0 0 0.25 0.25 {layer=8}
T {1nF} 615 -715 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 600 -720 0 0 {name=C_lpf_sig
value=1n}
N 600 -860 600 -750 {lab=rms_out}
N 600 -690 600 -260 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 680 -860 0 0 {name=p_rms_out lab=rms_out}
N 600 -860 680 -860 {lab=rms_out}
T {Rlpf} 540 -605 0 0 0.25 0.25 {layer=8}
T {3.18M} 540 -585 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/res.sym} 570 -560 3 0 {name=R_lpf_ref
value=3.18Meg}
N 450 -860 450 -560 {lab=sq_ref}
N 450 -560 540 -560 {lab=sq_ref}
T {Clpf} 615 -435 0 0 0.25 0.25 {layer=8}
T {1nF} 615 -415 0 0 0.2 0.2 {layer=8}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 600 -420 0 0 {name=C_lpf_ref
value=1n}
N 600 -560 600 -450 {lab=rms_ref}
N 600 -390 600 -260 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 680 -560 0 0 {name=p_rms_ref lab=rms_ref}
N 600 -560 680 -560 {lab=rms_ref}
T {Active Peak Detector} 820 -1300 0 0 0.45 0.45 {layer=4}
T {5-Transistor OTA + Hold} 820 -1265 0 0 0.3 0.3 {layer=8}
T {M3} 870 -1130 0 0 0.3 0.3 {layer=8}
T {2/2} 870 -1108 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 890 -1060 0 0 {name=XM3
W=2
L=2
nf=1
mult=1
model=pfet_01v8
spiceprefix=X}
T {M4} 1110 -1130 0 0 0.3 0.3 {layer=8}
T {2/2} 1110 -1108 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1090 -1060 0 1 {name=XM4
W=2
L=2
nf=1
mult=1
model=pfet_01v8
spiceprefix=X}
N 910 -1090 910 -1340 {lab=vdd}
N 1070 -1090 1070 -1340 {lab=vdd}
N 910 -1030 870 -1030 {lab=d1_pk}
N 870 -1030 870 -1060 {lab=d1_pk}
N 870 -1060 870 -1160 {lab=pbias_pk}
N 870 -1160 1110 -1160 {lab=pbias_pk}
N 1110 -1160 1110 -1060 {lab=pbias_pk}
T {M1} 870 -900 0 0 0.3 0.3 {layer=8}
T {4/2} 870 -878 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 890 -830 0 0 {name=XM1
W=4
L=2
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
T {M2} 1110 -900 0 0 0.3 0.3 {layer=8}
T {4/2} 1110 -878 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1090 -830 0 1 {name=XM2
W=4
L=2
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
N 910 -1030 910 -860 {lab=d1_pk}
N 1070 -1030 1070 -860 {lab=pk_ota_out}
N 910 -800 910 -770 {lab=tail_pk}
N 1070 -800 1070 -770 {lab=tail_pk}
N 910 -770 1070 -770 {lab=tail_pk}
T {Mt} 960 -710 0 0 0.3 0.3 {layer=8}
T {2/4} 960 -688 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 970 -650 0 0 {name=XMt
W=2
L=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
N 990 -770 990 -680 {lab=tail_pk}
N 990 -620 990 -260 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 -650 0 1 {name=l_vbn_mt lab=vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 870 -830 0 1 {name=l_inp_pk lab=inp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1110 -830 0 0 {name=l_pk_fb lab=peak_out}
T {Charge NFET} 1220 -1130 0 0 0.35 0.35 {layer=4}
T {XMchrg} 1220 -1070 0 0 0.3 0.3 {layer=8}
T {4/0.5} 1220 -1048 0 0 0.25 0.25 {layer=8}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1230 -980 0 0 {name=XMchrg
W=4
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
N 1250 -1010 1250 -1340 {lab=vdd}
N 1070 -980 1210 -980 {lab=pk_ota_out}
N 1250 -950 1250 -820 {lab=peak_out}
T {Chold} 1290 -735 0 0 0.3 0.3 {layer=8}
T {500pF} 1290 -713 0 0 0.25 0.25 {layer=8}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 1250 -720 0 0 {name=C_hold
value=500p}
N 1250 -820 1250 -750 {lab=peak_out}
N 1250 -690 1250 -260 {lab=gnd}
T {XMdis} 1365 -575 0 0 0.3 0.3 {layer=8}
T {0.42/20} 1365 -553 0 0 0.25 0.25 {layer=8}
T {Discharge} 1345 -620 0 0 0.25 0.25 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1360 -500 0 0 {name=XMdis
W=0.42
L=20
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
N 1380 -530 1380 -820 {lab=peak_out}
N 1250 -820 1380 -820 {lab=peak_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1340 -500 0 1 {name=l_vcm_dis lab=vcm}
N 1380 -470 1380 -400 {lab=vcm}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1380 -400 0 0 {name=l_vcm_dis_s lab=vcm}
T {XMrst} 1495 -575 0 0 0.3 0.3 {layer=8}
T {1/0.5} 1495 -553 0 0 0.25 0.25 {layer=8}
T {Reset} 1490 -620 0 0 0.25 0.25 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1490 -500 0 0 {name=XMrst
W=1
L=0.5
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
N 1510 -530 1510 -820 {lab=peak_out}
N 1380 -820 1510 -820 {lab=peak_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1470 -500 0 1 {name=l_reset_g lab=reset}
N 1510 -470 1510 -400 {lab=vcm}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1510 -400 0 0 {name=l_vcm_rst_s lab=vcm}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1580 -820 0 0 {name=p_peak_out lab=peak_out}
N 1510 -820 1580 -820 {lab=peak_out}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -380 -1340 0 1 {name=p_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -380 -260 0 1 {name=p_gnd lab=gnd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -80 -720 0 1 {name=p_inp lab=inp}
N -80 -720 -20 -720 {lab=inp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -80 -400 0 1 {name=p_vcm lab=vcm}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -80 -500 0 1 {name=p_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -80 -350 0 1 {name=p_reset lab=reset}
N -380 -1340 20 -1340 {lab=vdd}
N 20 -1340 300 -1340 {lab=vdd}
N 300 -1340 910 -1340 {lab=vdd}
N 910 -1340 1070 -1340 {lab=vdd}
N 1070 -1340 1250 -1340 {lab=vdd}
N -380 -260 20 -260 {lab=gnd}
N 20 -260 300 -260 {lab=gnd}
N 300 -260 600 -260 {lab=gnd}
N 600 -260 990 -260 {lab=gnd}
N 990 -260 1250 -260 {lab=gnd}
N 1250 -260 1510 -260 {lab=gnd}
