v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Level Shifter DOWN (PVDD -> SVDD)} 300 100 0 0 0.8 0.8 {layer=15}
T {Block 06 -- Cross-Coupled PMOS Level Shifter} 300 140 0 0 0.5 0.5 {layer=15}
T {PVDD 5V to SVDD 2.2V} 300 175 0 0 0.4 0.4 {layer=8}
T {Input Inverter} 340 230 0 0 0.4 0.4 {layer=4}
T {(PVDD domain)} 340 260 0 0 0.3 0.3 {layer=8}
T {Cross-Coupled PMOS Pair} 700 230 0 0 0.4 0.4 {layer=4}
T {(SVDD domain)} 700 260 0 0 0.3 0.3 {layer=8}
T {NMOS Pull-Downs} 740 530 0 0 0.35 0.35 {layer=4}
T {B=PVDD} 425 320 0 0 0.3 0.3 {layer=7}
T {B=GND} 425 460 0 0 0.3 0.3 {layer=7}
T {B=SVDD} 725 340 0 0 0.3 0.3 {layer=7}
T {B=SVDD} 925 340 0 0 0.3 0.3 {layer=7}
T {B=GND} 725 550 0 0 0.3 0.3 {layer=7}
T {B=GND} 925 550 0 0 0.3 0.3 {layer=7}
C {/usr/share/xschem/xschem_library/devices/title.sym} 300 800 0 0 {name=l1 author="Claude AI -- Block 06 -- Level Shifter DOWN (PVDD->SVDD) -- 2026-03-28"}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 400 330 0 0 {name=XMP_INV
W=4
L=0.5
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 400 470 0 0 {name=XMN_INV
W=2
L=0.5
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 700 350 0 0 {name=XMP1
W=4
L=0.5
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 900 350 0 0 {name=XMP2
W=4
L=0.5
nf=1
mult=1
model=pfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 700 560 0 0 {name=XMN1
W=2
L=1
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 900 560 0 0 {name=XMN2
W=2
L=1
nf=1
mult=1
model=nfet_g5v0d10v5
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} 300 400 0 0 {name=p1 lab=in}
C {/usr/share/xschem/xschem_library/devices/opin.sym} 1000 440 0 0 {name=p2 lab=out}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 300 290 0 1 {name=p3 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 720 280 0 0 {name=p4 lab=svdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 720 660 0 0 {name=p5 lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 330 0 0 {name=l_inv_gin sig_type=std_logic lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 470 0 0 {name=l_inv_gin2 sig_type=std_logic lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 300 0 1 {name=l_inv_pvdd sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 330 0 1 {name=l_inv_pbody sig_type=std_logic lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 500 0 1 {name=l_inv_gnd sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 420 470 0 1 {name=l_inv_nbody sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 480 400 0 1 {name=l_inv_out sig_type=std_logic lab=in_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 320 0 1 {name=l_mp1_s sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 350 0 1 {name=l_mp1_b sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 320 0 1 {name=l_mp2_s sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 350 0 1 {name=l_mp2_b sig_type=std_logic lab=svdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 680 350 0 0 {name=l_mp1_g sig_type=std_logic lab=out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 350 0 0 {name=l_mp2_g sig_type=std_logic lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 440 0 0 {name=l_n1 sig_type=std_logic lab=n1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 440 0 1 {name=l_out sig_type=std_logic lab=out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 680 560 0 0 {name=l_mn1_g sig_type=std_logic lab=in}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 880 560 0 0 {name=l_mn2_g sig_type=std_logic lab=in_b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 590 0 1 {name=l_mn1_gnd sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 560 0 1 {name=l_mn1_body sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 590 0 1 {name=l_mn2_gnd sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 560 0 1 {name=l_mn2_body sig_type=std_logic lab=gnd}
N 420 360 420 400 {lab=in_b}
N 420 400 420 440 {lab=in_b}
N 420 400 480 400 {lab=in_b}
N 300 400 380 400 {lab=in}
N 380 330 380 400 {}
N 380 400 380 470 {}
N 720 380 720 440 {lab=n1}
N 720 440 720 530 {lab=n1}
N 920 380 920 440 {lab=out}
N 920 440 920 530 {lab=out}
N 920 440 1000 440 {lab=out}
N 300 290 420 290 {lab=pvdd}
N 420 290 420 300 {lab=pvdd}
N 720 280 720 320 {lab=svdd}
N 720 280 920 280 {lab=svdd}
N 920 280 920 320 {lab=svdd}
N 720 590 720 660 {lab=gnd}
N 720 660 920 660 {lab=gnd}
N 920 590 920 660 {lab=gnd}
N 420 330 420 300 {lab=pvdd}
N 420 470 420 500 {lab=gnd}
N 720 350 720 320 {lab=svdd}
N 920 350 920 320 {lab=svdd}
N 720 560 720 590 {lab=gnd}
N 920 560 920 590 {lab=gnd}
