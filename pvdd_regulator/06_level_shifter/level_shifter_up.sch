v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Level Shifter UP (SVDD -> BVDD)} 160 -1080 0 0 0.8 0.8 {layer=15}
T {Block 06 | Cross-Coupled PMOS Level Shifter | SKY130A} 160 -1030 0 0 0.4 0.4 {layer=15}
T {SVDD (2.2V) -> BVDD (5.4-10.5V) | All g5v0d10v5} 160 -990 0 0 0.35 0.35 {layer=8}
T {Input Inverter (SVDD domain)} 260 -800 0 0 0.4 0.4 {layer=4}
T {NMOS Pull-Downs (L=1u)} 540 -480 0 0 0.4 0.4 {layer=4}
T {Cross-Coupled PMOS (BVDD domain)} 540 -800 0 0 0.4 0.4 {layer=4}
C {devices/title.sym} 160 -30 0 0 {name=l1 author="PVDD LDO"}
C {devices/ipin.sym} 160 -620 0 0 {name=p1 lab=in}
C {devices/opin.sym} 880 -560 0 0 {name=p2 lab=out}
C {devices/iopin.sym} 160 -920 0 1 {name=p3 lab=bvdd}
C {devices/iopin.sym} 160 -880 0 1 {name=p4 lab=svdd}
C {devices/iopin.sym} 160 -200 0 1 {name=p5 lab=gnd}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 300 -680 0 0 {name=XMP_INV
L=0.5
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 300 -560 0 0 {name=XMN_INV
L=0.5
W=2
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 560 -400 0 0 {name=XMN1
L=1
W=15
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {sky130_fd_pr/nfet_g5v0d10v5.sym} 760 -400 0 0 {name=XMN2
L=1
W=15
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 560 -660 0 0 {name=XMP1
L=0.5
W=4
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {sky130_fd_pr/pfet_g5v0d10v5.sym} 760 -660 0 0 {name=XMP2
L=0.5
W=5
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {devices/lab_pin.sym} 280 -680 0 0 {name=l1a sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 280 -560 0 0 {name=l1b sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 540 -400 0 0 {name=l2a sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 740 -400 0 0 {name=l2b sig_type=std_logic lab=in_b}
C {devices/lab_pin.sym} 360 -620 0 0 {name=l3a sig_type=std_logic lab=in_b}
C {devices/lab_pin.sym} 880 -560 0 0 {name=l4a sig_type=std_logic lab=out}
N 160 -920 240 -920 {lab=bvdd}
N 160 -880 240 -880 {lab=svdd}
N 160 -200 240 -200 {lab=gnd}
N 160 -620 280 -620 {lab=in}
N 280 -620 280 -680 {lab=in}
N 280 -620 280 -560 {lab=in}
N 320 -650 320 -620 {lab=in_b}
N 320 -620 320 -590 {lab=in_b}
N 320 -620 360 -620 {lab=in_b}
N 320 -710 320 -880 {lab=svdd}
N 320 -680 320 -710 {lab=svdd}
N 320 -530 320 -200 {lab=gnd}
N 320 -560 320 -530 {lab=gnd}
N 580 -690 580 -920 {lab=bvdd}
N 580 -660 580 -690 {lab=bvdd}
N 780 -690 780 -920 {lab=bvdd}
N 780 -660 780 -690 {lab=bvdd}
N 240 -920 580 -920 {lab=bvdd}
N 580 -920 780 -920 {lab=bvdd}
N 580 -630 580 -560 {lab=n1}
N 580 -560 580 -430 {lab=n1}
N 780 -630 780 -560 {lab=out}
N 780 -560 780 -430 {lab=out}
N 780 -560 880 -560 {lab=out}
N 580 -370 580 -200 {lab=gnd}
N 580 -400 580 -370 {lab=gnd}
N 780 -370 780 -200 {lab=gnd}
N 780 -400 780 -370 {lab=gnd}
N 240 -200 580 -200 {lab=gnd}
N 580 -200 780 -200 {lab=gnd}
N 540 -660 500 -660 {lab=out}
N 500 -660 500 -500 {lab=out}
N 500 -500 820 -500 {lab=out}
N 820 -500 820 -560 {lab=out}
N 820 -560 780 -560 {lab=out}
N 740 -660 700 -660 {lab=n1}
N 700 -660 700 -520 {lab=n1}
N 700 -520 560 -520 {lab=n1}
N 560 -520 560 -560 {lab=n1}
N 560 -560 580 -560 {lab=n1}
C {devices/lab_pin.sym} 240 -920 0 0 {name=l5a sig_type=std_logic lab=bvdd}
C {devices/lab_pin.sym} 240 -880 0 0 {name=l5b sig_type=std_logic lab=svdd}
C {devices/lab_pin.sym} 240 -200 0 0 {name=l5c sig_type=std_logic lab=gnd}
C {devices/lab_pin.sym} 580 -560 0 1 {name=l6a sig_type=std_logic lab=n1}
T {B=SVDD} 325 -690 0 0 0.3 0.3 {layer=7}
T {B=GND} 325 -550 0 0 0.3 0.3 {layer=7}
T {B=GND} 585 -410 0 0 0.3 0.3 {layer=7}
T {B=GND} 785 -410 0 0 0.3 0.3 {layer=7}
T {B=BVDD} 585 -670 0 0 0.3 0.3 {layer=7}
T {B=BVDD} 785 -670 0 0 0.3 0.3 {layer=7}
