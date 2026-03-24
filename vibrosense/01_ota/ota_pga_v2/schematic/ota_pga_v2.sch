v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense PGA OTA v2.1 (Two-Stage Miller)} -250 -1140 0 0 0.5 0.5 {}
T {SKY130A — 7 Transistors + Rz + Cc} -250 -1115 0 0 0.28 0.28 {layer=8}
T {STAGE 1} -50 -1050 0 0 0.3 0.3 {layer=8}
T {Diff Pair + Mirror} -100 -1025 0 0 0.2 0.2 {layer=8}
T {STAGE 2} 430 -1050 0 0 0.3 0.3 {layer=8}
T {CS + Sink} 430 -1025 0 0 0.2 0.2 {layer=8}
T {COMPENSATION} 250 -935 0 0 0.22 0.22 {layer=8}
T {M3 diode} -240 -855 0 0 0.18 0.18 {layer=5}
T {gate = drain} -240 -838 0 0 0.15 0.15 {layer=5}
T {Rz = 40k} 300 -870 0 0 0.2 0.2 {layer=5}
T {Cc = 3.8pF} 300 -770 0 0 0.2 0.2 {layer=5}
T {v_mir} -118 -835 0 0 0.18 0.18 {layer=4}
T {v_s1} 112 -835 0 0 0.18 0.18 {layer=4}
T {otail} -15 -645 0 0 0.18 0.18 {layer=4}
T {rz_mid} 290 -812 0 0 0.15 0.15 {layer=4}
T {(unused)} -200 -310 0 0 0.15 0.15 {layer=8}
T {(unused)} -200 -340 0 0 0.15 0.15 {layer=8}
T {(unused)} -200 -370 0 0 0.15 0.15 {layer=8}

N -250 -1100 600 -1100 {lab=vdd}
N -250 -250 600 -250 {lab=gnd}

N -130 -980 -130 -1100 {lab=vdd}
N 100 -980 100 -1100 {lab=vdd}
N 470 -980 470 -1100 {lab=vdd}

N -130 -950 -110 -950 {lab=vdd}
N 100 -950 120 -950 {lab=vdd}
N 470 -950 490 -950 {lab=vdd}

N -25 -420 -25 -250 {lab=gnd}
N 470 -420 470 -250 {lab=gnd}

N -130 -700 -110 -700 {lab=gnd}
N 100 -700 80 -700 {lab=gnd}
N -25 -450 -5 -450 {lab=gnd}
N 470 -450 490 -450 {lab=gnd}

N -130 -920 -130 -730 {lab=v_mir}
N -170 -950 -220 -950 {lab=v_mir}
N -220 -950 -220 -900 {lab=v_mir}
N -220 -900 60 -900 {lab=v_mir}
N 60 -900 60 -950 {lab=v_mir}

N 100 -920 100 -730 {lab=v_s1}
N 100 -890 430 -890 {lab=v_s1}
N 430 -890 430 -950 {lab=v_s1}

N 280 -830 280 -790 {lab=rz_mid}

N 470 -920 470 -480 {lab=out}
N 280 -730 470 -730 {lab=out}
N 470 -600 550 -600 {lab=out}

N -130 -670 100 -670 {lab=otail}
N -25 -670 -25 -480 {lab=otail}

N -200 -450 -65 -450 {lab=vbn}
N 430 -450 380 -450 {lab=vbn}

N -170 -700 -260 -700 {lab=inp}
N 140 -700 230 -700 {lab=inn}

N 130 -1150 130 -1100 {lab=vdd}
N 130 -250 130 -200 {lab=gnd}

C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -150 -950 0 0 {name=M3 L=2u W=2u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 80 -950 0 0 {name=M4 L=2u W=2u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 450 -950 0 0 {name=M5 L=2u W=10u nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -150 -700 0 0 {name=M1 L=14u W=5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 120 -700 0 1 {name=M2 L=14u W=5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -45 -450 0 0 {name=M11 L=18u W=15u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 450 -450 0 0 {name=M7 L=2u W=5.5u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/res.sym} 280 -860 0 0 {name=Rz value=40k}
C {devices/capa.sym} 280 -760 0 0 {name=Cc value=3.8p}

C {devices/lab_pin.sym} -110 -950 0 0 {name=l1 lab=vdd}
C {devices/lab_pin.sym} 120 -950 0 0 {name=l2 lab=vdd}
C {devices/lab_pin.sym} 490 -950 0 0 {name=l3 lab=vdd}
C {devices/lab_pin.sym} -110 -700 0 0 {name=l4 lab=gnd}
C {devices/lab_pin.sym} 80 -700 0 1 {name=l5 lab=gnd}
C {devices/lab_pin.sym} -5 -450 0 0 {name=l6 lab=gnd}
C {devices/lab_pin.sym} 490 -450 0 0 {name=l7 lab=gnd}
C {devices/lab_pin.sym} 380 -450 0 1 {name=l8 lab=vbn}

C {devices/iopin.sym} -260 -700 2 0 {name=p_inp lab=inp}
C {devices/iopin.sym} 230 -700 0 0 {name=p_inn lab=inn}
C {devices/iopin.sym} 550 -600 0 0 {name=p_out lab=out}
C {devices/iopin.sym} 130 -1150 3 0 {name=p_vdd lab=vdd}
C {devices/iopin.sym} 130 -200 1 0 {name=p_gnd lab=gnd}
C {devices/iopin.sym} -200 -450 2 0 {name=p_vbn lab=vbn}
C {devices/iopin.sym} -220 -310 2 0 {name=p_vbp lab=vbp}
C {devices/iopin.sym} -220 -340 2 0 {name=p_vbcp lab=vbcp}
C {devices/iopin.sym} -220 -370 2 0 {name=p_vbcn lab=vbcn}
