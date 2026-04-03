v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 01: PASS DEVICE} -500 -900 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -500 -830 0 0 0.5 0.5 {layer=8}
T {Device: sky130_fd_pr__pfet_g5v0d10v5  (HV PMOS, Vds max = 10.5V)} -500 -790 0 0 0.35 0.35 {}
T {W = 50 um per finger,  m=2 per instance (100 um effective),  L = 0.5 um} -500 -750 0 0 0.35 0.35 {}
T {10 parallel instances -> Total W = 1.0 mm} -500 -710 0 0 0.4 0.4 {layer=7}
T {.subckt pass_device  gate  bvdd  pvdd} -500 -670 0 0 0.3 0.3 {layer=13}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -500 -600 0 0 {name=p1 lab=gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -500 -570 0 0 {name=p2 lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -500 -540 0 0 {name=p3 lab=pvdd}

C {/usr/share/xschem/xschem_library/devices/title.sym} -560 560 0 0 {name=l1 author="Block 01: Pass Device -- Analog AI Chips PVDD LDO Regulator"}

T {BVDD (Source/Bulk)} -50 -500 0 0 0.5 0.5 {layer=7}
T {GATE (from EA)} -450 -300 0 0 0.4 0.4 {layer=4}
T {PVDD (Drain, regulated output)} -50 100 0 0 0.5 0.5 {layer=7}

* ================================================================
* ROW 1: XM1 .. XM5 (left to right)
* All: sky130_fd_pr__pfet_g5v0d10v5  W=50  L=0.5  m=2
* Source=bvdd, Drain=pvdd, Gate=gate, Bulk=bvdd
* ================================================================

T {Row 1: XM1-XM5} -350 -400 0 0 0.35 0.35 {layer=13}

* --- XM1 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -200 -300 0 0 {name=XM1
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -220 -300 0 0 {name=l_g1 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -330 2 0 {name=l_s1 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -270 0 0 {name=l_d1 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -300 2 0 {name=l_b1 sig_type=std_logic lab=bvdd}

* --- XM2 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 0 -300 0 0 {name=XM2
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -20 -300 0 0 {name=l_g2 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -330 2 0 {name=l_s2 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -270 0 0 {name=l_d2 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -300 2 0 {name=l_b2 sig_type=std_logic lab=bvdd}

* --- XM3 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 200 -300 0 0 {name=XM3
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -300 0 0 {name=l_g3 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 -330 2 0 {name=l_s3 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 -270 0 0 {name=l_d3 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 -300 2 0 {name=l_b3 sig_type=std_logic lab=bvdd}

* --- XM4 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 400 -300 0 0 {name=XM4
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 -300 0 0 {name=l_g4 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -330 2 0 {name=l_s4 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -270 0 0 {name=l_d4 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -300 2 0 {name=l_b4 sig_type=std_logic lab=bvdd}

* --- XM5 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 600 -300 0 0 {name=XM5
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -300 0 0 {name=l_g5 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -330 2 0 {name=l_s5 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -270 0 0 {name=l_d5 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -300 2 0 {name=l_b5 sig_type=std_logic lab=bvdd}

* ================================================================
* ROW 2: XM6 .. XM10 (left to right)
* ================================================================

T {Row 2: XM6-XM10} -350 -100 0 0 0.35 0.35 {layer=13}

* --- XM6 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -200 0 0 0 {name=XM6
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -220 0 0 0 {name=l_g6 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 -30 2 0 {name=l_s6 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 30 0 0 {name=l_d6 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -180 0 2 0 {name=l_b6 sig_type=std_logic lab=bvdd}

* --- XM7 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 0 0 0 0 {name=XM7
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -20 0 0 0 {name=l_g7 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -30 2 0 {name=l_s7 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 30 0 0 {name=l_d7 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 0 2 0 {name=l_b7 sig_type=std_logic lab=bvdd}

* --- XM8 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 200 0 0 0 {name=XM8
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 0 0 0 {name=l_g8 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 -30 2 0 {name=l_s8 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 30 0 0 {name=l_d8 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 220 0 2 0 {name=l_b8 sig_type=std_logic lab=bvdd}

* --- XM9 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 400 0 0 0 {name=XM9
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 0 0 0 {name=l_g9 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 -30 2 0 {name=l_s9 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 30 0 0 {name=l_d9 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 0 2 0 {name=l_b9 sig_type=std_logic lab=bvdd}

* --- XM10 ---
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 600 0 0 0 {name=XM10
L=0.5
W=50
nf=1
mult=2
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 0 0 0 {name=l_g10 sig_type=std_logic lab=gate}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -30 2 0 {name=l_s10 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 30 0 0 {name=l_d10 sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 0 2 0 {name=l_b10 sig_type=std_logic lab=bvdd}

T {All 10 instances: W=50u L=0.5u m=2 (100um eff. each)} -350 150 0 0 0.3 0.3 {layer=5}
T {Total effective width = 1.0 mm} -350 180 0 0 0.35 0.35 {layer=7}
