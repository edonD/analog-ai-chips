v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Level Shifter UP (SVDD -> BVDD)} 240 -1060 0 0 0.8 0.8 {layer=15}
T {Block 06  |  Cross-Coupled PMOS Level Shifter  |  SKY130A} 240 -1010 0 0 0.4 0.4 {layer=15}
T {SVDD = 2.2 V  ->  BVDD (higher voltage domain)} 240 -970 0 0 0.35 0.35 {layer=8}
T {Input Inverter} 280 -780 0 0 0.4 0.4 {layer=4}
T {Cross-Coupled PMOS Pair} 620 -780 0 0 0.4 0.4 {layer=4}
T {NMOS Pull-Downs} 620 -460 0 0 0.4 0.4 {layer=4}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 320 -660 0 0 {name=XMP_INV
W=4
L=0.5
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 320 -540 0 0 {name=XMN_INV
W=2
L=0.5
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -380 0 0 {name=XMN1
W=15
L=1
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 760 -380 0 0 {name=XMN2
W=15
L=1
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 560 -640 0 0 {name=XMP1
W=4
L=0.5
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 760 -640 0 0 {name=XMP2
W=5
L=0.5
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} 240 -600 0 0 {name=p_in lab=in}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 900 -530 0 0 {name=p_out lab=out}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 240 -900 0 1 {name=p_bvdd lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 240 -860 0 1 {name=p_svdd lab=svdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 240 -260 0 1 {name=p_gnd lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 240 -600 0 1 {name=l_in1 sig_type=std_logic lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -660 0 1 {name=l_in2 sig_type=std_logic lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -540 0 1 {name=l_in3 sig_type=std_logic lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 -380 0 1 {name=l_in4 sig_type=std_logic lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 740 -380 0 1 {name=l_inb1 sig_type=std_logic lab=in_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 -600 0 0 {name=l_inb2 sig_type=std_logic lab=in_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -530 0 1 {name=l_n1a sig_type=std_logic lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -530 0 0 {name=l_out1 sig_type=std_logic lab=out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 900 -530 0 0 {name=l_out2 sig_type=std_logic lab=out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -900 0 0 {name=l_bvdd1 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -860 0 0 {name=l_svdd1 sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -260 0 0 {name=l_gnd1 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -690 0 0 {name=l_svdd2 sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -660 0 0 {name=l_svdd_body sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -540 0 0 {name=l_gnd_body sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -380 0 0 {name=l_gnd_body2 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -380 0 0 {name=l_gnd_body3 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 580 -640 0 0 {name=l_bvdd_body1 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -640 0 0 {name=l_bvdd_body2 sig_type=std_logic lab=bvdd}
C {/usr/share/xschem/xschem_library/devices/title.sym} 240 -200 0 0 {name=l1 author="Claude AI"}
N 240 -900 340 -900 {lab=bvdd}
N 240 -860 340 -860 {lab=svdd}
N 240 -260 340 -260 {lab=gnd}
N 340 -690 340 -860 {lab=svdd}
N 340 -510 340 -260 {lab=gnd}
N 340 -630 340 -600 {lab=in_b}
N 340 -600 380 -600 {lab=in_b}
N 340 -570 340 -600 {lab=in_b}
N 580 -670 580 -900 {lab=bvdd}
N 780 -670 780 -900 {lab=bvdd}
N 580 -900 780 -900 {lab=bvdd}
N 340 -900 580 -900 {lab=bvdd}
N 580 -610 580 -530 {lab=n1}
N 580 -530 580 -410 {lab=n1}
N 780 -610 780 -530 {lab=out}
N 780 -530 780 -410 {lab=out}
N 780 -530 900 -530 {lab=out}
N 580 -350 580 -260 {lab=gnd}
N 780 -350 780 -260 {lab=gnd}
N 340 -260 580 -260 {lab=gnd}
N 580 -260 780 -260 {lab=gnd}
N 540 -640 500 -640 {lab=out}
N 500 -640 500 -470 {lab=out}
N 500 -470 810 -470 {lab=out}
N 810 -470 810 -530 {lab=out}
N 810 -530 780 -530 {lab=out}
N 740 -640 720 -640 {lab=n1}
N 720 -640 720 -490 {lab=n1}
N 720 -490 560 -490 {lab=n1}
N 560 -490 560 -530 {lab=n1}
N 560 -530 580 -530 {lab=n1}
