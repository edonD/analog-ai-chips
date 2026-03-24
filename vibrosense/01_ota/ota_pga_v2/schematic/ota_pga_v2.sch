v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense PGA OTA v2.1 (Two-Stage Miller)} -400 -1580 0 0 0.6 0.6 {}
T {SKY130A} -400 -1540 0 0 0.35 0.35 {layer=8}
T {STAGE 1: Diff Pair + Mirror} -280 -1370 0 0 0.3 0.3 {layer=8}
T {STAGE 2: CS + Sink} 480 -1370 0 0 0.3 0.3 {layer=8}
T {COMPENSATION} 210 -1100 0 0 0.25 0.25 {layer=8}
T {Rz = 40k} 250 -1040 0 0 0.2 0.2 {layer=5}
T {Cc = 3.8pF} 250 -900 0 0 0.2 0.2 {layer=5}
T {M3 diode} -300 -1180 0 0 0.2 0.2 {layer=5}
T {gate = drain} -300 -1160 0 0 0.18 0.18 {layer=5}
T {M1: 5u/14u} -310 -680 0 0 0.18 0.18 {layer=5}
T {M2: 5u/14u} 120 -680 0 0 0.18 0.18 {layer=5}
T {M3: 2u/2u} -310 -1210 0 0 0.18 0.18 {layer=5}
T {M4: 2u/2u} 120 -1210 0 0 0.18 0.18 {layer=5}
T {M5: 10u/2u} 560 -1210 0 0 0.18 0.18 {layer=5}
T {M7: 5.5u/2u} 560 -340 0 0 0.18 0.18 {layer=5}
T {M11: 15u/18u} -120 -340 0 0 0.18 0.18 {layer=5}
T {(unused)} -480 -280 0 0 0.18 0.18 {layer=8}
T {(unused)} -480 -230 0 0 0.18 0.18 {layer=8}
T {(unused)} -480 -180 0 0 0.18 0.18 {layer=8}
T {v_mir} -215 -960 0 0 0.18 0.18 {layer=4}
T {v_s1} 105 -960 0 0 0.18 0.18 {layer=4}
T {otail} -60 -610 0 0 0.18 0.18 {layer=4}
T {rz_mid} 240 -960 0 0 0.18 0.18 {layer=4}
N -400 -1450 660 -1450 {lab=vdd}
N -400 -130 660 -130 {lab=gnd}
N -200 -1340 -200 -1450 {lab=vdd}
N 100 -1340 100 -1450 {lab=vdd}
N 540 -1340 540 -1450 {lab=vdd}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -220 -1310 0 0 {name=M3 L=2u W=2u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 80 -1310 0 0 {name=M4 L=2u W=2u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 520 -1310 0 0 {name=M5 L=2u W=10u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -220 -750 0 0 {name=M1 L=14u W=5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 120 -750 0 1 {name=M2 L=14u W=5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -70 -400 0 0 {name=M11 L=18u W=15u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 520 -400 0 0 {name=M7 L=2u W=5.5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/res.sym} 230 -1020 0 0 {name=Rz value=40k}
C {devices/capa.sym} 230 -880 0 0 {name=Cc value=3.8p}
N -200 -1310 -180 -1310 {lab=vdd}
N 100 -1310 120 -1310 {lab=vdd}
N 540 -1310 560 -1310 {lab=vdd}
N -200 -1280 -200 -1230 {lab=v_mir}
N -240 -1310 -330 -1310 {lab=v_mir}
N -330 -1310 -330 -1230 {lab=v_mir}
N -330 -1230 -200 -1230 {lab=v_mir}
N 60 -1310 -30 -1310 {lab=v_mir}
C {devices/lab_pin.sym} -30 -1310 0 1 {name=lmir1 lab=v_mir}
N 100 -1280 100 -1230 {lab=v_s1}
C {devices/lab_pin.sym} 100 -1230 3 0 {name=ls1a lab=v_s1}
N -200 -780 -200 -940 {lab=v_mir}
C {devices/lab_pin.sym} -200 -940 1 0 {name=lmir2 lab=v_mir}
N -240 -750 -360 -750 {lab=inp}
N -200 -750 -180 -750 {lab=gnd}
C {devices/lab_pin.sym} -180 -750 0 0 {name=lb1 lab=gnd}
N -200 -720 -200 -630 {lab=otail}
N 100 -780 100 -940 {lab=v_s1}
C {devices/lab_pin.sym} 100 -940 1 0 {name=ls1b lab=v_s1}
N 140 -750 260 -750 {lab=inn}
N 100 -750 80 -750 {lab=gnd}
C {devices/lab_pin.sym} 80 -750 0 1 {name=lb2 lab=gnd}
N 100 -720 100 -630 {lab=otail}
N -200 -630 100 -630 {lab=otail}
N -50 -630 -50 -430 {lab=otail}
N -50 -370 -50 -130 {lab=gnd}
N -90 -400 -180 -400 {lab=vbn}
C {devices/lab_pin.sym} -180 -400 0 1 {name=lvbn1 lab=vbn}
N -50 -400 -30 -400 {lab=gnd}
C {devices/lab_pin.sym} -30 -400 0 0 {name=lb3 lab=gnd}
N 500 -1310 440 -1310 {lab=v_s1}
C {devices/lab_pin.sym} 440 -1310 0 1 {name=ls1c lab=v_s1}
N 540 -1280 540 -1230 {lab=out}
C {devices/lab_pin.sym} 540 -1230 3 0 {name=lout1 lab=out}
N 540 -370 540 -130 {lab=gnd}
N 500 -400 430 -400 {lab=vbn}
C {devices/lab_pin.sym} 430 -400 0 1 {name=lvbn2 lab=vbn}
N 540 -400 560 -400 {lab=gnd}
C {devices/lab_pin.sym} 560 -400 0 0 {name=lb4 lab=gnd}
N 540 -430 540 -480 {lab=out}
C {devices/lab_pin.sym} 540 -480 1 0 {name=lout2 lab=out}
N 540 -480 660 -480 {lab=out}
N 230 -1050 230 -1090 {lab=v_s1}
C {devices/lab_pin.sym} 230 -1090 1 0 {name=ls1d lab=v_s1}
N 230 -990 230 -910 {lab=rz_mid}
N 230 -850 230 -820 {lab=out}
C {devices/lab_pin.sym} 230 -820 3 0 {name=lout3 lab=out}
C {devices/iopin.sym} -360 -750 2 0 {name=p30 lab=inp}
C {devices/iopin.sym} 260 -750 0 0 {name=p31 lab=inn}
C {devices/iopin.sym} 660 -480 0 0 {name=p32 lab=out}
C {devices/iopin.sym} 100 -1490 3 0 {name=p33 lab=vdd}
C {devices/iopin.sym} 100 -90 1 0 {name=p34 lab=gnd}
C {devices/iopin.sym} -400 -400 2 0 {name=p35 lab=vbn}
C {devices/iopin.sym} -420 -260 2 0 {name=p36 lab=vbp}
C {devices/iopin.sym} -420 -210 2 0 {name=p37 lab=vbcp}
C {devices/iopin.sym} -420 -160 2 0 {name=p38 lab=vbcn}
N 100 -1490 100 -1450 {lab=vdd}
N 100 -130 100 -90 {lab=gnd}
N -400 -400 -180 -400 {lab=vbn}
