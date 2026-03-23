v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -700 -1400 700 -1400 {lab=vdd}
N -700 200 700 200 {lab=gnd}
N -400 -1400 -400 -1350 {lab=vdd}
N -400 -1350 -400 -1300 {lab=vdd_int}
N -400 -1300 -200 -1300 {lab=vdd_int}
N -200 -1300 -200 -1230 {lab=vdd_int}
N -200 -1200 -180 -1200 {lab=vdd_int}
N 200 -1300 200 -1230 {lab=vdd_int}
N 200 -1200 220 -1200 {lab=vdd_int}
N -200 -1170 -200 -1100 {lab=v_mir}
N 200 -1170 200 -1100 {lab=v_s1}
N -200 -1100 200 -1100 {lab=v_mir}
N -200 -1100 -200 -1050 {lab=v_mir}
N -240 -1200 -280 -1200 {lab=v_mir}
N 160 -1200 -280 -1200 {lab=v_mir}
N -280 -1200 -280 -1100 {lab=v_mir}
N -200 -800 -200 -830 {lab=v_mir}
N 200 -800 200 -830 {lab=v_s1}
N -160 -770 -100 -770 {lab=inp}
N 160 -770 100 -770 {lab=inn}
N -200 -770 -220 -770 {lab=gnd}
N 200 -770 220 -770 {lab=gnd}
N -200 -740 -200 -680 {lab=otail}
N 200 -740 200 -680 {lab=otail}
N -200 -680 200 -680 {lab=otail}
N 0 -680 0 -620 {lab=otail}
N 0 -590 0 -560 {lab=otail}
N -40 -560 -80 -560 {lab=vbn}
N 0 -530 0 200 {lab=gnd}
N 0 -560 20 -560 {lab=gnd}
N 200 -1100 200 -1050 {lab=v_s1}
N 200 -1050 350 -1050 {lab=v_s1}
N 350 -1050 500 -1050 {lab=v_s1}
N 500 -1050 500 -1000 {lab=rz_mid}
N 500 -1000 500 -800 {lab=rz_mid}
N 500 -800 500 -700 {lab=out}
N 600 -1230 600 -1300 {lab=vdd_int}
N -200 -1300 600 -1300 {lab=vdd_int}
N 600 -1200 620 -1200 {lab=vdd_int}
N 600 -1170 600 -1100 {lab=out}
N 600 -1100 600 -700 {lab=out}
N 500 -700 600 -700 {lab=out}
N 600 -700 700 -700 {lab=out}
N 600 -400 600 -430 {lab=out}
N 600 -370 600 200 {lab=gnd}
N 560 -400 520 -400 {lab=vbn}
N 600 -400 620 -400 {lab=gnd}
N 560 -1200 350 -1200 {lab=v_s1}
N 350 -1200 350 -1050 {lab=v_s1}
N -100 -770 -100 -770 {lab=inp}
N 100 -770 100 -770 {lab=inn}
N -400 -1300 -400 -1250 {lab=vdd_int}
N -400 -1220 -400 -1200 {lab=vdd_int}
N -400 -1200 -200 -1200 {lab=vdd_int}
T {VibroSense PGA OTA v2 (Two-Stage Miller)} -700 -1600 0 0 0.6 0.6 {}
T {SKY130A — 7 Transistors + Rz + Cc} -700 -1550 0 0 0.35 0.35 {layer=8}
T {STAGE 1: Diff Pair + Mirror} -300 -900 0 0 0.3 0.3 {layer=8}
T {STAGE 2: PMOS CS} 520 -1080 0 0 0.3 0.3 {layer=8}
T {Miller Compensation} 380 -950 0 0 0.3 0.3 {layer=8}
T {Rz} 480 -1030 0 0 0.25 0.25 {layer=4}
T {Cc} 480 -840 0 0 0.25 0.25 {layer=4}
T {Rvdd} -420 -1310 0 0 0.25 0.25 {layer=4}
T {Cvdd} -420 -1240 0 0 0.25 0.25 {layer=4}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -220 -1200 0 0 {name=M3 L=2u W=2u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -200 -1170 3 0 {name=p1 lab=v_mir}
C {devices/lab_pin.sym} -280 -1200 0 1 {name=p2 lab=v_mir}
C {devices/lab_pin.sym} -200 -1230 1 0 {name=p3 lab=vdd_int}
C {devices/lab_pin.sym} -180 -1200 0 0 {name=p4 lab=vdd_int}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 180 -1200 0 0 {name=M4 L=2u W=2u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 200 -1170 3 0 {name=p5 lab=v_s1}
C {devices/lab_pin.sym} 160 -1200 0 1 {name=p6 lab=v_mir}
C {devices/lab_pin.sym} 200 -1230 1 0 {name=p7 lab=vdd_int}
C {devices/lab_pin.sym} 220 -1200 0 0 {name=p8 lab=vdd_int}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -180 -770 0 1 {name=M1 L=14u W=5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -200 -830 1 0 {name=p9 lab=v_mir}
C {devices/lab_pin.sym} -100 -770 0 0 {name=p10 lab=inp}
C {devices/lab_pin.sym} -200 -740 3 0 {name=p11 lab=otail}
C {devices/lab_pin.sym} -220 -770 0 1 {name=p12 lab=gnd}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -20 -560 0 0 {name=M11 L=14u W=11.4u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 0 -620 1 0 {name=p13 lab=otail}
C {devices/lab_pin.sym} -80 -560 0 1 {name=p14 lab=vbn}
C {devices/lab_pin.sym} 0 -530 3 0 {name=p15 lab=gnd}
C {devices/lab_pin.sym} 20 -560 0 0 {name=p16 lab=gnd}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 160 -770 0 0 {name=M2 L=14u W=5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 200 -830 1 0 {name=p17 lab=v_s1}
C {devices/lab_pin.sym} 100 -770 0 1 {name=p18 lab=inn}
C {devices/lab_pin.sym} 200 -740 3 0 {name=p19 lab=otail}
C {devices/lab_pin.sym} 220 -770 0 0 {name=p20 lab=gnd}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 580 -1200 0 0 {name=M5 L=1u W=5u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 600 -1170 3 0 {name=p21 lab=out}
C {devices/lab_pin.sym} 350 -1200 0 1 {name=p22 lab=v_s1}
C {devices/lab_pin.sym} 600 -1230 1 0 {name=p23 lab=vdd_int}
C {devices/lab_pin.sym} 620 -1200 0 0 {name=p24 lab=vdd_int}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 580 -400 0 0 {name=M7 L=2u W=5.5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 600 -430 1 0 {name=p25 lab=out}
C {devices/lab_pin.sym} 520 -400 0 1 {name=p26 lab=vbn}
C {devices/lab_pin.sym} 600 -370 3 0 {name=p27 lab=gnd}
C {devices/lab_pin.sym} 620 -400 0 0 {name=p28 lab=gnd}
C {devices/lab_pin.sym} 700 -700 0 0 {name=p29 lab=out}
C {devices/iopin.sym} -100 -770 2 0 {name=p30 lab=inp}
C {devices/iopin.sym} 100 -770 2 0 {name=p31 lab=inn}
C {devices/iopin.sym} 750 -700 0 0 {name=p32 lab=out}
C {devices/iopin.sym} 0 -1450 3 0 {name=p33 lab=vdd}
C {devices/iopin.sym} 0 250 1 0 {name=p34 lab=gnd}
C {devices/iopin.sym} -800 -560 2 0 {name=p35 lab=vbn}
C {devices/iopin.sym} -800 -300 2 0 {name=p36 lab=vbcn}
C {devices/iopin.sym} -800 -1200 2 0 {name=p37 lab=vbp}
C {devices/iopin.sym} -800 -1000 2 0 {name=p38 lab=vbcp}
N -800 -560 -80 -560 {lab=vbn}
N 520 -400 -80 -400 {lab=vbn}
N -80 -400 -80 -560 {lab=vbn}
N 0 -1450 0 -1400 {lab=vdd}
N 0 200 0 250 {lab=gnd}
