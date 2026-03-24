v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense PGA OTA v2 (Two-Stage Miller)} -900 -1850 0 0 0.6 0.6 {}
T {SKY130A — 7 Transistors + Rz + Cc} -900 -1800 0 0 0.35 0.35 {layer=8}
T {STAGE 1} -100 -1060 0 0 0.35 0.35 {layer=8}
T {Diff Pair + Mirror} -150 -1020 0 0 0.25 0.25 {layer=8}
T {STAGE 2} 700 -1060 0 0 0.35 0.35 {layer=8}
T {PMOS CS + NMOS Sink} 640 -1020 0 0 0.25 0.25 {layer=8}
T {(unused)} -750 -1100 0 0 0.2 0.2 {layer=8}
T {(unused)} -750 -1000 0 0 0.2 0.2 {layer=8}
T {(unused)} -750 -900 0 0 0.2 0.2 {layer=8}
T {M3 diode} -340 -1210 0 0 0.25 0.25 {layer=5}
T {gate = drain} -350 -1180 0 0 0.2 0.2 {layer=5}
T {COMPENSATION} 430 -1180 0 0 0.3 0.3 {layer=8}
T {Rz = 30k} 530 -1110 0 0 0.25 0.25 {layer=5}
T {Cc = 3.5pF} 530 -960 0 0 0.25 0.25 {layer=5}
T {rz_mid} 510 -1030 0 0 0.2 0.2 {layer=4}

N -850 -1700 800 -1700 {lab=vdd}
N -850 -200 800 -200 {lab=gnd}

N 0 -1760 0 -1700 {lab=vdd}
N 0 -200 0 -130 {lab=gnd}

N -180 -1380 -180 -1700 {lab=vdd}
N 220 -1380 220 -1700 {lab=vdd}
N 720 -1380 720 -1700 {lab=vdd}

N -180 -1350 -160 -1350 {lab=vdd}
N 220 -1350 240 -1350 {lab=vdd}
N 720 -1350 740 -1350 {lab=vdd}

N -180 -1320 -180 -1200 {lab=v_mir}
N -220 -1350 -350 -1350 {lab=v_mir}
N -350 -1350 -350 -1200 {lab=v_mir}
N -350 -1200 -180 -1200 {lab=v_mir}

N 180 -1350 120 -1350 {lab=v_mir}

N 220 -1320 220 -930 {lab=v_s1}
N 220 -1130 680 -1130 {lab=v_s1}
N 680 -1130 680 -1350 {lab=v_s1}

N -200 -930 -200 -970 {lab=v_mir}
N -200 -870 -200 -800 {lab=otail}
N -160 -900 -100 -900 {lab=inp}
N -200 -900 -230 -900 {lab=gnd}

N 220 -870 220 -800 {lab=otail}
N 180 -900 120 -900 {lab=inn}
N 220 -900 250 -900 {lab=gnd}

N -200 -800 220 -800 {lab=otail}
N 0 -800 0 -530 {lab=otail}

N 0 -470 0 -200 {lab=gnd}
N -800 -500 -40 -500 {lab=vbn}
N 0 -500 20 -500 {lab=gnd}

N 720 -1320 720 -530 {lab=out}

N 720 -470 720 -200 {lab=gnd}
N 680 -500 620 -500 {lab=vbn}
N 720 -500 740 -500 {lab=gnd}

N 500 -1070 500 -980 {lab=rz_mid}
N 500 -920 720 -920 {lab=out}

N 720 -800 790 -800 {lab=out}

C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -200 -1350 0 0 {name=M3 L=2u W=2u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 200 -1350 0 0 {name=M4 L=2u W=2u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 700 -1350 0 0 {name=M5 L=1u W=5u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -180 -900 0 1 {name=M1 L=14u W=5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 200 -900 0 0 {name=M2 L=14u W=5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -20 -500 0 0 {name=M11 L=14u W=11.4u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 700 -500 0 0 {name=M7 L=2u W=5.5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}

C {devices/res.sym} 500 -1100 0 0 {name=Rz value=30k}
C {devices/capa.sym} 500 -950 0 0 {name=Cc value=3.5p}

C {devices/lab_pin.sym} -160 -1350 0 0 {name=l1 lab=vdd}
C {devices/lab_pin.sym} 240 -1350 0 0 {name=l2 lab=vdd}
C {devices/lab_pin.sym} 740 -1350 0 0 {name=l3 lab=vdd}
C {devices/lab_pin.sym} -180 -1200 3 0 {name=l4 lab=v_mir}
C {devices/lab_pin.sym} 120 -1350 0 1 {name=l5 lab=v_mir}
C {devices/lab_pin.sym} -200 -970 1 0 {name=l6 lab=v_mir}
C {devices/lab_pin.sym} -230 -900 0 1 {name=l7 lab=gnd}
C {devices/lab_pin.sym} 250 -900 0 0 {name=l8 lab=gnd}
C {devices/lab_pin.sym} 20 -500 0 0 {name=l9 lab=gnd}
C {devices/lab_pin.sym} 740 -500 0 0 {name=l10 lab=gnd}
C {devices/lab_pin.sym} 620 -500 0 1 {name=l11 lab=vbn}
C {devices/lab_pin.sym} 790 -800 0 0 {name=l12 lab=out}

C {devices/iopin.sym} -100 -900 2 0 {name=p30 lab=inp}
C {devices/iopin.sym} 120 -900 2 0 {name=p31 lab=inn}
C {devices/iopin.sym} 800 -800 0 0 {name=p32 lab=out}
C {devices/iopin.sym} 0 -1760 3 0 {name=p33 lab=vdd}
C {devices/iopin.sym} 0 -130 1 0 {name=p34 lab=gnd}
C {devices/iopin.sym} -800 -500 2 0 {name=p35 lab=vbn}
C {devices/iopin.sym} -800 -1100 2 0 {name=p36 lab=vbp}
C {devices/iopin.sym} -800 -1000 2 0 {name=p37 lab=vbcp}
C {devices/iopin.sym} -800 -900 2 0 {name=p38 lab=vbcn}
