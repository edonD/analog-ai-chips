v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 04: Envelope Detector} -900 -2050 0 0 0.7 0.7 {layer=15}
T {Dual ota_pga_v2 Precision Half-Wave Rectifier + 5T Gm-C LPF  —  SKY130A} -900 -1980 0 0 0.35 0.35 {layer=15}
T {Power: 21 uW  |  VDD = 1.8 V  |  LPF fc ~ 9 Hz} -900 -1940 0 0 0.3 0.3 {layer=8}
T {PRECISION RECTIFIER} -700 -1870 0 0 0.4 0.4 {layer=4}
T {(dual OTA feedback)} -680 -1840 0 0 0.25 0.25 {layer=8}
T {Gm-C LOW-PASS FILTER} 520 -1870 0 0 0.4 0.4 {layer=4}
T {(5T OTA follower + 50nF)} 520 -1840 0 0 0.25 0.25 {layer=8}
T {|} 350 -1500 0 0 0.3 0.3 {layer=8}
T {|} 350 -1300 0 0 0.3 0.3 {layer=8}
T {|} 350 -1100 0 0 0.3 0.3 {layer=8}
T {|} 350 -900 0 0 0.3 0.3 {layer=8}
T {|} 350 -700 0 0 0.3 0.3 {layer=8}
T {|} 350 -500 0 0 0.3 0.3 {layer=8}
T {|} 350 -300 0 0 0.3 0.3 {layer=8}
T {Mph1} -260 -1620 0 0 0.3 0.3 {layer=8}
T {PMOS 2/1} -270 -1595 0 0 0.22 0.22 {layer=8}
T {Mph2} 40 -1620 0 0 0.3 0.3 {layer=8}
T {PMOS 2/1} 30 -1595 0 0 0.22 0.22 {layer=8}
T {Msink} -110 -520 0 0 0.3 0.3 {layer=8}
T {NMOS 0.42/100} -140 -495 0 0 0.22 0.22 {layer=8}
T {(triode discharge)} -150 -470 0 0 0.2 0.2 {layer=5}
T {Mp3} 490 -1620 0 0 0.3 0.3 {layer=8}
T {PMOS 4/4} 480 -1595 0 0 0.22 0.22 {layer=8}
T {(diode)} 490 -1575 0 0 0.2 0.2 {layer=5}
T {Mp4} 740 -1620 0 0 0.3 0.3 {layer=8}
T {PMOS 4/4} 730 -1595 0 0 0.22 0.22 {layer=8}
T {(mirror)} 740 -1575 0 0 0.2 0.2 {layer=5}
T {M1} 490 -1120 0 0 0.3 0.3 {layer=8}
T {NMOS 2/4} 480 -1095 0 0 0.22 0.22 {layer=8}
T {M2} 740 -1120 0 0 0.3 0.3 {layer=8}
T {NMOS 2/4} 730 -1095 0 0 0.22 0.22 {layer=8}
T {(follower)} 730 -1075 0 0 0.2 0.2 {layer=5}
T {Mtail} 615 -720 0 0 0.3 0.3 {layer=8}
T {NMOS 1/8} 605 -695 0 0 0.22 0.22 {layer=8}
T {Clpf = 50 nF} 1010 -960 0 0 0.3 0.3 {layer=8}
T {rect} 200 -1300 0 0 0.3 0.3 {layer=4}
T {oa1} -120 -1250 0 0 0.25 0.25 {layer=4}
T {oa2} -120 -950 0 0 0.25 0.25 {layer=4}
T {d1} 580 -1370 0 0 0.25 0.25 {layer=4}
T {tail} 680 -870 0 0 0.25 0.25 {layer=4}
N -900 -1800 1200 -1800 {lab=vdd}
N -900 -200 1200 -200 {lab=gnd}
N -650 -1180 -750 -1180 {lab=vin}
N -650 -1120 -750 -1120 {lab=rect}
N -450 -1150 -350 -1150 {lab=oa1}
N -550 -1230 -550 -1280 {lab=vdd}
N -550 -1070 -550 -1020 {lab=gnd}
N -590 -1070 -590 -1020 {lab=vbn}
N -510 -1070 -510 -1020 {lab=gnd}
N -590 -1230 -590 -1280 {lab=vdd}
N -510 -1230 -510 -1280 {lab=vdd}
N -650 -880 -750 -880 {lab=vcm}
N -650 -820 -750 -820 {lab=rect}
N -450 -850 -350 -850 {lab=oa2}
N -550 -930 -550 -980 {lab=vdd}
N -550 -770 -550 -720 {lab=gnd}
N -590 -770 -590 -720 {lab=vbn}
N -510 -770 -510 -720 {lab=gnd}
N -590 -930 -590 -980 {lab=vdd}
N -510 -930 -510 -980 {lab=vdd}
N -180 -1580 -180 -1800 {lab=vdd}
N -180 -1550 -160 -1550 {lab=vdd}
N -350 -1150 -350 -1550 {lab=oa1}
N -350 -1550 -220 -1550 {lab=oa1}
N -180 -1520 -180 -1350 {lab=rect}
N 120 -1580 120 -1800 {lab=vdd}
N 120 -1550 140 -1550 {lab=vdd}
N -350 -850 -250 -850 {lab=oa2}
N -250 -850 -250 -1550 {lab=oa2}
N -250 -1550 80 -1550 {lab=oa2}
N 120 -1520 120 -1350 {lab=rect}
N -180 -1350 120 -1350 {lab=rect}
N -30 -480 -30 -1350 {lab=rect}
N -70 -450 -110 -450 {lab=vdd}
N -30 -420 -30 -370 {lab=vcm}
N -30 -450 -10 -450 {lab=gnd}
N 120 -1350 450 -1350 {lab=rect}
N 450 -1350 450 -1050 {lab=rect}
N 450 -1050 510 -1050 {lab=rect}
N 570 -1580 570 -1800 {lab=vdd}
N 570 -1550 590 -1550 {lab=vdd}
N 570 -1520 570 -1400 {lab=d1}
N 530 -1550 530 -1400 {lab=d1}
N 530 -1400 570 -1400 {lab=d1}
N 820 -1580 820 -1800 {lab=vdd}
N 820 -1550 840 -1550 {lab=vdd}
N 820 -1520 820 -1400 {lab=vout}
N 780 -1550 530 -1550 {lab=d1}
N 530 -1550 530 -1400 {lab=d1}
N 570 -1080 570 -1400 {lab=d1}
N 530 -1050 510 -1050 {lab=rect}
N 570 -1020 570 -950 {lab=tail}
N 570 -1050 590 -1050 {lab=gnd}
N 820 -1080 820 -1400 {lab=vout}
N 780 -1050 780 -1020 {lab=vout}
N 780 -1020 820 -1020 {lab=vout}
N 820 -1020 820 -950 {lab=tail}
N 820 -1050 840 -1050 {lab=gnd}
N 570 -950 820 -950 {lab=tail}
N 675 -950 675 -680 {lab=tail}
N 655 -650 595 -650 {lab=vbn_lpf}
N 695 -620 695 -200 {lab=gnd}
N 695 -650 715 -650 {lab=gnd}
N 1050 -1130 1050 -1400 {lab=vout}
N 1050 -1400 820 -1400 {lab=vout}
N 1050 -1070 1050 -200 {lab=gnd}
N -900 -1180 -750 -1180 {lab=vin}
N -900 -880 -750 -880 {lab=vcm}
N 1050 -1400 1200 -1400 {lab=vout}
N -100 -1850 -100 -1800 {lab=vdd}
N -100 -100 -100 -200 {lab=gnd}
N -900 -1020 -590 -1020 {lab=vbn}
C {/home/ubuntu/analog-ai-chips/vibrosense/04_envelope/ota_pga_v2.sym} -550 -1150 0 0 {name=Xota1}
C {devices/lab_pin.sym} -750 -1180 0 1 {name=l1 lab=vin}
C {devices/lab_pin.sym} -750 -1120 0 1 {name=l2 lab=rect}
C {devices/lab_pin.sym} -550 -1280 1 0 {name=l3 lab=vdd}
C {devices/lab_pin.sym} -550 -1020 3 0 {name=l4 lab=gnd}
C {devices/lab_pin.sym} -590 -1020 3 0 {name=l5 lab=vbn}
C {devices/lab_pin.sym} -510 -1020 3 0 {name=l6 lab=gnd}
C {devices/lab_pin.sym} -590 -1280 1 0 {name=l7 lab=vdd}
C {devices/lab_pin.sym} -510 -1280 1 0 {name=l8 lab=vdd}
C {/home/ubuntu/analog-ai-chips/vibrosense/04_envelope/ota_pga_v2.sym} -550 -850 0 0 {name=Xota2}
C {devices/lab_pin.sym} -750 -880 0 1 {name=l9 lab=vcm}
C {devices/lab_pin.sym} -750 -820 0 1 {name=l10 lab=rect}
C {devices/lab_pin.sym} -550 -980 1 0 {name=l11 lab=vdd}
C {devices/lab_pin.sym} -550 -720 3 0 {name=l12 lab=gnd}
C {devices/lab_pin.sym} -590 -720 3 0 {name=l13 lab=vbn}
C {devices/lab_pin.sym} -510 -720 3 0 {name=l14 lab=gnd}
C {devices/lab_pin.sym} -590 -980 1 0 {name=l15 lab=vdd}
C {devices/lab_pin.sym} -510 -980 1 0 {name=l16 lab=vdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -200 -1550 0 0 {name=XMph1
W=2
L=1
nf=1
mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} -160 -1550 0 0 {name=l17 lab=vdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 100 -1550 0 0 {name=XMph2
W=2
L=1
nf=1
mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 140 -1550 0 0 {name=l18 lab=vdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -50 -450 0 0 {name=XMsink
W=0.42
L=100
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} -110 -450 0 1 {name=l19 lab=vdd}
C {devices/lab_pin.sym} -30 -370 3 0 {name=l20 lab=vcm}
C {devices/lab_pin.sym} -10 -450 0 0 {name=l21 lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 550 -1550 0 0 {name=XMp3
W=4
L=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 590 -1550 0 0 {name=l22 lab=vdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 800 -1550 0 0 {name=XMp4
W=4
L=4
nf=1
mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 840 -1550 0 0 {name=l23 lab=vdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 550 -1050 0 0 {name=XM1
W=2
L=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 590 -1050 0 0 {name=l24 lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 800 -1050 0 0 {name=XM2
W=2
L=4
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 840 -1050 0 0 {name=l25 lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 675 -650 0 0 {name=XMtail
W=1
L=8
nf=1
mult=1
model=nfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 595 -650 0 1 {name=l26 lab=vbn_lpf}
C {devices/lab_pin.sym} 715 -650 0 0 {name=l27 lab=gnd}
C {devices/capa.sym} 1050 -1100 0 0 {name=Clpf value=50n}
C {devices/iopin.sym} -900 -1180 2 0 {name=p28 lab=vin}
C {devices/iopin.sym} -900 -880 2 0 {name=p29 lab=vcm}
C {devices/iopin.sym} 1200 -1400 0 0 {name=p30 lab=vout}
C {devices/iopin.sym} -100 -1850 3 0 {name=p31 lab=vdd}
C {devices/iopin.sym} -100 -100 1 0 {name=p32 lab=gnd}
C {devices/iopin.sym} -900 -1020 2 0 {name=p33 lab=vbn}
C {devices/iopin.sym} 555 -650 2 0 {name=p34 lab=vbn_lpf}
