v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}

T {VibroSense Block 03: 4-Bit Binary-Weighted Cascode Current Mirror DAC} -300 -1200 0 0 0.55 0.55 {layer=15}
T {SKY130A  |  Iout = Iunit x (8*b3 + 4*b2 + 2*b1 + b0)  |  DNL = 0.0006 LSB} -300 -1150 0 0 0.3 0.3 {layer=8}
N -300 -1100 1300 -1100 {lab=vdd}
N -300 -200 1300 -200 {lab=vss}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -300 -1100 0 1 {name=p_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -300 -200 0 1 {name=p_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -200 -1100 3 0 {name=p_iref lab=iref}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1300 -580 0 0 {name=p_iout lab=iout}
T {REF} -150 -1050 0 0 0.35 0.35 {layer=4}
T {BIT 0 (1x)} 100 -1050 0 0 0.35 0.35 {layer=4}
T {BIT 1 (2x)} 370 -1050 0 0 0.35 0.35 {layer=4}
T {BIT 2 (4x)} 650 -1050 0 0 0.35 0.35 {layer=4}
T {BIT 3 (8x)} 950 -1050 0 0 0.35 0.35 {layer=4}
N -200 -1100 -100 -1100 {lab=iref}
N -100 -1100 -100 -950 {lab=iref}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -120 -900 0 0 {name=XMref_cas
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {Mcas_ref} -190 -920 0 0 0.22 0.22 {layer=8}
T {2/4} -190 -900 0 0 0.18 0.18 {layer=8}
N -100 -930 -100 -950 {lab=iref}
N -140 -900 -180 -900 {lab=gate_c}
N -180 -900 -180 -930 {lab=gate_c}
N -180 -930 -100 -930 {lab=gate_c}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -120 -700 0 0 {name=XMref_bot
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {Mmir_ref} -190 -720 0 0 0.22 0.22 {layer=8}
T {2/4} -190 -700 0 0 0.18 0.18 {layer=8}
N -100 -870 -100 -730 {lab=mid_ref}
N -140 -700 -180 -700 {lab=gate_n}
N -180 -700 -180 -730 {lab=gate_n}
N -180 -730 -100 -730 {lab=gate_n}
N -100 -670 -100 -200 {lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 -900 0 1 {name=l_gate_c lab=gate_c}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 -700 0 1 {name=l_gate_n lab=gate_n}
N -160 -900 1100 -900 {lab=gate_c}
N -160 -700 1100 -700 {lab=gate_n}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 160 -900 0 0 {name=XM0_cas
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {1x} 185 -925 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 160 -700 0 0 {name=XM0_bot
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 180 -670 180 -200 {lab=vss}
N 180 -870 180 -730 {lab=mid0}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 160 -500 0 0 {name=XM0_sw
W=1u
L=0.15u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {sw} 185 -520 0 0 0.18 0.18 {layer=5}
T {1/0.15} 185 -498 0 0 0.16 0.16 {layer=8}
N 180 -930 180 -560 {lab=sw0d}
N 180 -470 180 -560 {lab=sw0d}
N 180 -530 180 -400 {lab=iout}
N 140 -500 110 -500 {lab=b0}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 110 -500 0 1 {name=l_b0 lab=b0}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 430 -900 0 0 {name=XM1_cas
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {2x} 455 -925 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 430 -700 0 0 {name=XM1_bot
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 450 -670 450 -200 {lab=vss}
N 450 -870 450 -730 {lab=mid1}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 430 -500 0 0 {name=XM1_sw
W=1u
L=0.15u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {sw} 455 -520 0 0 0.18 0.18 {layer=5}
T {1/0.15} 455 -498 0 0 0.16 0.16 {layer=8}
N 450 -930 450 -560 {lab=sw1d}
N 450 -470 450 -560 {lab=sw1d}
N 450 -530 450 -400 {lab=iout}
N 410 -500 380 -500 {lab=b1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 380 -500 0 1 {name=l_b1 lab=b1}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 710 -900 0 0 {name=XM2_cas
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {4x} 735 -925 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 710 -700 0 0 {name=XM2_bot
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 730 -670 730 -200 {lab=vss}
N 730 -870 730 -730 {lab=mid2}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 710 -500 0 0 {name=XM2_sw
W=1u
L=0.15u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {sw} 735 -520 0 0 0.18 0.18 {layer=5}
T {1/0.15} 735 -498 0 0 0.16 0.16 {layer=8}
N 730 -930 730 -560 {lab=sw2d}
N 730 -470 730 -560 {lab=sw2d}
N 730 -530 730 -400 {lab=iout}
N 690 -500 660 -500 {lab=b2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 660 -500 0 1 {name=l_b2 lab=b2}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1010 -900 0 0 {name=XM3_cas
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {8x} 1035 -925 0 0 0.2 0.2 {layer=5}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1010 -700 0 0 {name=XM3_bot
W=2u
L=4u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
N 1030 -670 1030 -200 {lab=vss}
N 1030 -870 1030 -730 {lab=mid3}
C {/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1010 -500 0 0 {name=XM3_sw
W=1u
L=0.15u
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
T {sw} 1035 -520 0 0 0.18 0.18 {layer=5}
T {1/0.15} 1035 -498 0 0 0.16 0.16 {layer=8}
N 1030 -930 1030 -560 {lab=sw3d}
N 1030 -470 1030 -560 {lab=sw3d}
N 1030 -530 1030 -400 {lab=iout}
N 990 -500 960 -500 {lab=b3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 960 -500 0 1 {name=l_b3 lab=b3}
N 180 -400 1300 -400 {lab=iout}
N 1300 -400 1300 -580 {lab=iout}
T {100G bleed resistors on each switch node (not shown)} 100 -260 0 0 0.2 0.2 {layer=5}
