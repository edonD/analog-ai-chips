v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {PVDD 5V LDO Regulator — Full Transistor-Level Schematic} -3800 -5800 0 0 0.9 0.9 {layer=4}
T {SkyWater SKY130A  |  169 components  |  All 10 blocks flattened} -3800 -5740 0 0 0.35 0.35 {}
T {Every MOSFET, resistor, and capacitor drawn with real PDK symbols} -3800 -5710 0 0 0.3 0.3 {layer=13}
C {/usr/share/xschem/xschem_library/devices/title.sym} -3800 5800 0 0 {name=l1 author="PVDD 5V LDO Regulator -- Full Transistor-Level -- Analog AI Chips"}

* EXTERNAL PORT PINS
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -5500 0 0 {name=pp0 lab=bvdd}
T {bvdd} -3840 -5508 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -5400 0 0 {name=pp1 lab=pvdd}
T {pvdd} -3840 -5408 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -5300 0 0 {name=pp2 lab=gnd}
T {gnd} -3840 -5308 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -5200 0 0 {name=pp3 lab=avbg}
T {avbg} -3840 -5208 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -5100 0 0 {name=pp4 lab=ibias}
T {ibias} -3840 -5108 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -5000 0 0 {name=pp5 lab=svdd}
T {svdd} -3840 -5008 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4900 0 0 {name=pp6 lab=en}
T {en} -3840 -4908 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4800 0 0 {name=pp7 lab=en_ret}
T {en_ret} -3840 -4808 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4700 0 0 {name=pp8 lab=uv_flag}
T {uv_flag} -3840 -4708 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4600 0 0 {name=pp9 lab=ov_flag}
T {ov_flag} -3840 -4608 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4500 0 0 {name=pp10 lab=vref_ss}
T {vref_ss} -3840 -4508 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4400 0 0 {name=pp11 lab=ea_out}
T {ea_out} -3840 -4408 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4300 0 0 {name=pp12 lab=gate}
T {gate} -3840 -4308 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4200 0 0 {name=pp13 lab=ea_en}
T {ea_en} -3840 -4208 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4100 0 0 {name=pp14 lab=startup_done}
T {startup_done} -3840 -4108 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -4000 0 0 {name=pp15 lab=vfb}
T {vfb} -3840 -4008 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -3900 0 0 {name=pp16 lab=ilim_flag}
T {ilim_flag} -3840 -3908 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -3800 0 0 {name=pp17 lab=en_bvdd}
T {en_bvdd} -3840 -3808 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -3700 0 0 {name=pp18 lab=bypass_en}
T {bypass_en} -3840 -3708 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -3600 0 0 {name=pp19 lab=mc_ea_en}
T {mc_ea_en} -3840 -3608 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -3500 0 0 {name=pp20 lab=ref_sel}
T {ref_sel} -3840 -3508 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -3400 0 0 {name=pp21 lab=uvov_en}
T {uvov_en} -3840 -3408 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -3300 0 0 {name=pp22 lab=ilim_en}
T {ilim_en} -3840 -3308 0 0 0.22 0.22 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -3900 -3200 0 0 {name=pp23 lab=pass_off}
T {pass_off} -3840 -3208 0 0 0.22 0.22 {layer=4}

* ============================================================
* Section 1: Error Amplifier (Block 00)
* ============================================================
L 5 -3700 -5600 0 -5600 {dash=5}
L 5 0 -5600 0 -4000 {dash=5}
L 5 0 -4000 -3700 -4000 {dash=5}
L 5 -3700 -4000 -3700 -5600 {dash=5}
T {Section 1: Error Amplifier (Block 00)} -3685 -5585 0 0 0.4 0.4 {layer=5}
T {Two-stage Miller OTA — 12 FETs + Cc + Rc} -3685 -5555 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 -5410 0 0 {name=XMen L=1 W=20 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMen} -3585 -5455 0 0 0.18 0.18 {layer=13}
T {W=20 L=1} -3585 -5365 0 0 0.15 0.15 {layer=5}
N -3580 -5410 -3610 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -5410 0 0 {name=p1 sig_type=std_logic lab=ea_en}
N -3540 -5410 -3510 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -5410 2 0 {name=p2 sig_type=std_logic lab=gnd}
N -3540 -5440 -3540 -5465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -5465 3 0 {name=p3 sig_type=std_logic lab=b00_ibias_en}
N -3540 -5380 -3540 -5355 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -5355 1 0 {name=p4 sig_type=std_logic lab=ibias}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3300 -5410 0 0 {name=XMpu L=1 W=20 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMpu} -3305 -5455 0 0 0.18 0.18 {layer=13}
T {W=20 L=1} -3305 -5365 0 0 0.15 0.15 {layer=5}
N -3300 -5410 -3330 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -5410 0 0 {name=p5 sig_type=std_logic lab=ea_en}
N -3260 -5410 -3230 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -5410 2 0 {name=p6 sig_type=std_logic lab=pvdd}
N -3260 -5440 -3260 -5465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -5465 3 0 {name=p7 sig_type=std_logic lab=pvdd}
N -3260 -5380 -3260 -5355 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -5355 1 0 {name=p8 sig_type=std_logic lab=ea_out}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3020 -5410 0 0 {name=XMbn0 L=8 W=20 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMbn0} -3025 -5455 0 0 0.18 0.18 {layer=13}
T {W=20 L=8} -3025 -5365 0 0 0.15 0.15 {layer=5}
N -3020 -5410 -3050 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 -5410 0 0 {name=p9 sig_type=std_logic lab=b00_ibias_en}
N -2980 -5410 -2950 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 -5410 2 0 {name=p10 sig_type=std_logic lab=gnd}
N -2980 -5440 -2980 -5465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 -5465 3 0 {name=p11 sig_type=std_logic lab=b00_ibias_en}
N -2980 -5380 -2980 -5355 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 -5355 1 0 {name=p12 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 -5170 0 0 {name=XMbn_pb L=8 W=20 nf=1 mult=200 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMbn_pb} -3585 -5215 0 0 0.18 0.18 {layer=13}
T {W=20 L=8 m=200} -3585 -5125 0 0 0.15 0.15 {layer=5}
N -3580 -5170 -3610 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -5170 0 0 {name=p13 sig_type=std_logic lab=b00_ibias_en}
N -3540 -5170 -3510 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -5170 2 0 {name=p14 sig_type=std_logic lab=gnd}
N -3540 -5200 -3540 -5225 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -5225 3 0 {name=p15 sig_type=std_logic lab=b00_pb_tail}
N -3540 -5140 -3540 -5115 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -5115 1 0 {name=p16 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3300 -5170 0 0 {name=XMbp0 L=4 W=20 nf=1 mult=4 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMbp0} -3305 -5215 0 0 0.18 0.18 {layer=13}
T {W=20 L=4 m=4} -3305 -5125 0 0 0.15 0.15 {layer=5}
N -3300 -5170 -3330 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -5170 0 0 {name=p17 sig_type=std_logic lab=b00_pb_tail}
N -3260 -5170 -3230 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -5170 2 0 {name=p18 sig_type=std_logic lab=pvdd}
N -3260 -5200 -3260 -5225 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -5225 3 0 {name=p19 sig_type=std_logic lab=pvdd}
N -3260 -5140 -3260 -5115 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -5115 1 0 {name=p20 sig_type=std_logic lab=b00_pb_tail}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3580 -4930 0 0 {name=XMtail L=4 W=20 nf=1 mult=4 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMtail} -3585 -4975 0 0 0.18 0.18 {layer=13}
T {W=20 L=4 m=4} -3585 -4885 0 0 0.15 0.15 {layer=5}
N -3580 -4930 -3610 -4930 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -4930 0 0 {name=p21 sig_type=std_logic lab=b00_pb_tail}
N -3540 -4930 -3510 -4930 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -4930 2 0 {name=p22 sig_type=std_logic lab=pvdd}
N -3540 -4960 -3540 -4985 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -4985 3 0 {name=p23 sig_type=std_logic lab=pvdd}
N -3540 -4900 -3540 -4875 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -4875 1 0 {name=p24 sig_type=std_logic lab=b00_tail_s}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3300 -4930 0 0 {name=XM1 L=4 W=80 nf=1 mult=2 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM1} -3305 -4975 0 0 0.18 0.18 {layer=13}
T {W=80 L=4 m=2} -3305 -4885 0 0 0.15 0.15 {layer=5}
N -3300 -4930 -3330 -4930 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -4930 0 0 {name=p25 sig_type=std_logic lab=vref_ss}
N -3260 -4930 -3230 -4930 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -4930 2 0 {name=p26 sig_type=std_logic lab=pvdd}
N -3260 -4960 -3260 -4985 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -4985 3 0 {name=p27 sig_type=std_logic lab=b00_tail_s}
N -3260 -4900 -3260 -4875 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -4875 1 0 {name=p28 sig_type=std_logic lab=b00_d1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3020 -4930 0 0 {name=XM2 L=4 W=80 nf=1 mult=2 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM2} -3025 -4975 0 0 0.18 0.18 {layer=13}
T {W=80 L=4 m=2} -3025 -4885 0 0 0.15 0.15 {layer=5}
N -3020 -4930 -3050 -4930 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 -4930 0 0 {name=p29 sig_type=std_logic lab=vfb}
N -2980 -4930 -2950 -4930 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 -4930 2 0 {name=p30 sig_type=std_logic lab=pvdd}
N -2980 -4960 -2980 -4985 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 -4985 3 0 {name=p31 sig_type=std_logic lab=b00_tail_s}
N -2980 -4900 -2980 -4875 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 -4875 1 0 {name=p32 sig_type=std_logic lab=b00_d2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 -4690 0 0 {name=XMn_l L=8 W=20 nf=1 mult=2 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMn_l} -3585 -4735 0 0 0.18 0.18 {layer=13}
T {W=20 L=8 m=2} -3585 -4645 0 0 0.15 0.15 {layer=5}
N -3580 -4690 -3610 -4690 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -4690 0 0 {name=p33 sig_type=std_logic lab=b00_d1}
N -3540 -4690 -3510 -4690 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -4690 2 0 {name=p34 sig_type=std_logic lab=gnd}
N -3540 -4720 -3540 -4745 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -4745 3 0 {name=p35 sig_type=std_logic lab=b00_d1}
N -3540 -4660 -3540 -4635 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -4635 1 0 {name=p36 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 -4690 0 0 {name=XMn_r L=8 W=20 nf=1 mult=2 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMn_r} -3305 -4735 0 0 0.18 0.18 {layer=13}
T {W=20 L=8 m=2} -3305 -4645 0 0 0.15 0.15 {layer=5}
N -3300 -4690 -3330 -4690 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -4690 0 0 {name=p37 sig_type=std_logic lab=b00_d1}
N -3260 -4690 -3230 -4690 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -4690 2 0 {name=p38 sig_type=std_logic lab=gnd}
N -3260 -4720 -3260 -4745 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -4745 3 0 {name=p39 sig_type=std_logic lab=b00_d2}
N -3260 -4660 -3260 -4635 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -4635 1 0 {name=p40 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 -4450 0 0 {name=XMcs L=1 W=20 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMcs} -3585 -4495 0 0 0.18 0.18 {layer=13}
T {W=20 L=1} -3585 -4405 0 0 0.15 0.15 {layer=5}
N -3580 -4450 -3610 -4450 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -4450 0 0 {name=p41 sig_type=std_logic lab=b00_d2}
N -3540 -4450 -3510 -4450 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -4450 2 0 {name=p42 sig_type=std_logic lab=gnd}
N -3540 -4480 -3540 -4505 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -4505 3 0 {name=p43 sig_type=std_logic lab=ea_out}
N -3540 -4420 -3540 -4395 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -4395 1 0 {name=p44 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3300 -4450 0 0 {name=XMp_ld L=4 W=20 nf=1 mult=8 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMp_ld} -3305 -4495 0 0 0.18 0.18 {layer=13}
T {W=20 L=4 m=8} -3305 -4405 0 0 0.15 0.15 {layer=5}
N -3300 -4450 -3330 -4450 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -4450 0 0 {name=p45 sig_type=std_logic lab=b00_pb_tail}
N -3260 -4450 -3230 -4450 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -4450 2 0 {name=p46 sig_type=std_logic lab=pvdd}
N -3260 -4480 -3260 -4505 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -4505 3 0 {name=p47 sig_type=std_logic lab=pvdd}
N -3260 -4420 -3260 -4395 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -4395 1 0 {name=p48 sig_type=std_logic lab=ea_out}
C {/usr/share/xschem/xschem_library/devices/capa.sym} -2200 -4690 0 0 {name=Cc value=30p}
T {Cc} -2180 -4715 0 0 0.17 0.17 {layer=13}
T {30p} -2180 -4680 0 0 0.15 0.15 {layer=5}
N -2200 -4720 -2200 -4745 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2200 -4745 3 0 {name=p49 sig_type=std_logic lab=b00_d2}
N -2200 -4660 -2200 -4635 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2200 -4635 1 0 {name=p50 sig_type=std_logic lab=b00_comp_mid}
C {/usr/share/xschem/xschem_library/devices/res.sym} -2200 -4450 0 0 {name=Rc value=25k}
T {Rc} -2180 -4475 0 0 0.17 0.17 {layer=13}
T {25k} -2180 -4440 0 0 0.15 0.15 {layer=5}
N -2200 -4480 -2200 -4505 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2200 -4505 3 0 {name=p51 sig_type=std_logic lab=b00_comp_mid}
N -2200 -4420 -2200 -4395 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2200 -4395 1 0 {name=p52 sig_type=std_logic lab=ea_out}

* ============================================================
* Section 2: Pass Device (Block 01)
* ============================================================
L 4 500 -5600 3500 -5600 {dash=5}
L 4 3500 -5600 3500 -4800 {dash=5}
L 4 3500 -4800 500 -4800 {dash=5}
L 4 500 -4800 500 -5600 {dash=5}
T {Section 2: Pass Device (Block 01)} 515 -5585 0 0 0.4 0.4 {layer=4}
T {10x PMOS pfet_g5v0d10v5 W=100u L=0.5u — Total W=1mm} 515 -5555 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 620 -5410 0 0 {name=XM1 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM1} 615 -5455 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 615 -5365 0 0 0.15 0.15 {layer=5}
N 620 -5410 590 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -5410 0 0 {name=p53 sig_type=std_logic lab=gate}
N 660 -5410 690 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 690 -5410 2 0 {name=p54 sig_type=std_logic lab=bvdd}
N 660 -5440 660 -5465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 660 -5465 3 0 {name=p55 sig_type=std_logic lab=bvdd}
N 660 -5380 660 -5355 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 660 -5355 1 0 {name=p56 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 900 -5410 0 0 {name=XM2 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM2} 895 -5455 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 895 -5365 0 0 0.15 0.15 {layer=5}
N 900 -5410 870 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 870 -5410 0 0 {name=p57 sig_type=std_logic lab=gate}
N 940 -5410 970 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -5410 2 0 {name=p58 sig_type=std_logic lab=bvdd}
N 940 -5440 940 -5465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -5465 3 0 {name=p59 sig_type=std_logic lab=bvdd}
N 940 -5380 940 -5355 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -5355 1 0 {name=p60 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1180 -5410 0 0 {name=XM3 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM3} 1175 -5455 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 1175 -5365 0 0 0.15 0.15 {layer=5}
N 1180 -5410 1150 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -5410 0 0 {name=p61 sig_type=std_logic lab=gate}
N 1220 -5410 1250 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 -5410 2 0 {name=p62 sig_type=std_logic lab=bvdd}
N 1220 -5440 1220 -5465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -5465 3 0 {name=p63 sig_type=std_logic lab=bvdd}
N 1220 -5380 1220 -5355 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -5355 1 0 {name=p64 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1460 -5410 0 0 {name=XM4 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM4} 1455 -5455 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 1455 -5365 0 0 0.15 0.15 {layer=5}
N 1460 -5410 1430 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1430 -5410 0 0 {name=p65 sig_type=std_logic lab=gate}
N 1500 -5410 1530 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1530 -5410 2 0 {name=p66 sig_type=std_logic lab=bvdd}
N 1500 -5440 1500 -5465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -5465 3 0 {name=p67 sig_type=std_logic lab=bvdd}
N 1500 -5380 1500 -5355 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -5355 1 0 {name=p68 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1740 -5410 0 0 {name=XM5 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM5} 1735 -5455 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 1735 -5365 0 0 0.15 0.15 {layer=5}
N 1740 -5410 1710 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1710 -5410 0 0 {name=p69 sig_type=std_logic lab=gate}
N 1780 -5410 1810 -5410 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1810 -5410 2 0 {name=p70 sig_type=std_logic lab=bvdd}
N 1780 -5440 1780 -5465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1780 -5465 3 0 {name=p71 sig_type=std_logic lab=bvdd}
N 1780 -5380 1780 -5355 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1780 -5355 1 0 {name=p72 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 620 -5170 0 0 {name=XM6 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM6} 615 -5215 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 615 -5125 0 0 0.15 0.15 {layer=5}
N 620 -5170 590 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -5170 0 0 {name=p73 sig_type=std_logic lab=gate}
N 660 -5170 690 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 690 -5170 2 0 {name=p74 sig_type=std_logic lab=bvdd}
N 660 -5200 660 -5225 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 660 -5225 3 0 {name=p75 sig_type=std_logic lab=bvdd}
N 660 -5140 660 -5115 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 660 -5115 1 0 {name=p76 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 900 -5170 0 0 {name=XM7 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM7} 895 -5215 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 895 -5125 0 0 0.15 0.15 {layer=5}
N 900 -5170 870 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 870 -5170 0 0 {name=p77 sig_type=std_logic lab=gate}
N 940 -5170 970 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -5170 2 0 {name=p78 sig_type=std_logic lab=bvdd}
N 940 -5200 940 -5225 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -5225 3 0 {name=p79 sig_type=std_logic lab=bvdd}
N 940 -5140 940 -5115 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -5115 1 0 {name=p80 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1180 -5170 0 0 {name=XM8 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM8} 1175 -5215 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 1175 -5125 0 0 0.15 0.15 {layer=5}
N 1180 -5170 1150 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -5170 0 0 {name=p81 sig_type=std_logic lab=gate}
N 1220 -5170 1250 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 -5170 2 0 {name=p82 sig_type=std_logic lab=bvdd}
N 1220 -5200 1220 -5225 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -5225 3 0 {name=p83 sig_type=std_logic lab=bvdd}
N 1220 -5140 1220 -5115 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -5115 1 0 {name=p84 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1460 -5170 0 0 {name=XM9 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM9} 1455 -5215 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 1455 -5125 0 0 0.15 0.15 {layer=5}
N 1460 -5170 1430 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1430 -5170 0 0 {name=p85 sig_type=std_logic lab=gate}
N 1500 -5170 1530 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1530 -5170 2 0 {name=p86 sig_type=std_logic lab=bvdd}
N 1500 -5200 1500 -5225 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -5225 3 0 {name=p87 sig_type=std_logic lab=bvdd}
N 1500 -5140 1500 -5115 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1500 -5115 1 0 {name=p88 sig_type=std_logic lab=pvdd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1740 -5170 0 0 {name=XM10 L=0.5 W=100 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XM10} 1735 -5215 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5} 1735 -5125 0 0 0.15 0.15 {layer=5}
N 1740 -5170 1710 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1710 -5170 0 0 {name=p89 sig_type=std_logic lab=gate}
N 1780 -5170 1810 -5170 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1810 -5170 2 0 {name=p90 sig_type=std_logic lab=bvdd}
N 1780 -5200 1780 -5225 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1780 -5225 3 0 {name=p91 sig_type=std_logic lab=bvdd}
N 1780 -5140 1780 -5115 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1780 -5115 1 0 {name=p92 sig_type=std_logic lab=pvdd}

* ============================================================
* Section 3: Feedback Network (Block 02)
* ============================================================
L 5 500 -4700 1300 -4700 {dash=5}
L 5 1300 -4700 1300 -4000 {dash=5}
L 5 1300 -4000 500 -4000 {dash=5}
L 5 500 -4000 500 -4700 {dash=5}
T {Section 3: Feedback Network (Block 02)} 515 -4685 0 0 0.4 0.4 {layer=5}
T {Resistive divider — vfb = 1.226V at PVDD=5V} 515 -4655 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 600 -4510 0 0 {name=XR_TOP W=3.0 L=536 model=res_xhigh_po spiceprefix=X}
T {XR_TOP} 620 -4535 0 0 0.17 0.17 {layer=13}
T {W=3.0 L=536} 620 -4495 0 0 0.14 0.14 {layer=5}
N 600 -4540 600 -4565 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -4565 3 0 {name=p93 sig_type=std_logic lab=pvdd}
N 600 -4480 600 -4455 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -4455 1 0 {name=p94 sig_type=std_logic lab=vfb}
N 580 -4510 560 -4510 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 560 -4510 0 0 {name=p95 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 800 -4510 0 0 {name=XR_BOT W=3.0 L=174.3 model=res_xhigh_po spiceprefix=X}
T {XR_BOT} 820 -4535 0 0 0.17 0.17 {layer=13}
T {W=3.0 L=174.3} 820 -4495 0 0 0.14 0.14 {layer=5}
N 800 -4540 800 -4565 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -4565 3 0 {name=p96 sig_type=std_logic lab=vfb}
N 800 -4480 800 -4455 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -4455 1 0 {name=p97 sig_type=std_logic lab=gnd}
N 780 -4510 760 -4510 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 760 -4510 0 0 {name=p98 sig_type=std_logic lab=gnd}

* ============================================================
* Section 4: Compensation (Block 03)
* ============================================================
L 5 -3700 -3900 -2700 -3900 {dash=5}
L 5 -2700 -3900 -2700 -3300 {dash=5}
L 5 -2700 -3300 -3700 -3300 {dash=5}
L 5 -3700 -3300 -3700 -3900 {dash=5}
T {Section 4: Compensation (Block 03)} -3685 -3885 0 0 0.4 0.4 {layer=5}
T {Miller Cc + Rz + Cout} -3685 -3855 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -3600 -3710 0 0 {name=XCc W=122 L=122 MF=1 model=cap_mim_m3_1 spiceprefix=X}
T {XCc} -3580 -3735 0 0 0.17 0.17 {layer=13}
T {W=122 L=122} -3580 -3695 0 0 0.14 0.14 {layer=5}
N -3600 -3740 -3600 -3765 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3600 -3765 3 0 {name=p99 sig_type=std_logic lab=ea_out}
N -3600 -3680 -3600 -3655 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3600 -3655 1 0 {name=p100 sig_type=std_logic lab=b03_cc_mid}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -3400 -3710 0 0 {name=XRz W=4 L=10 model=res_xhigh_po spiceprefix=X}
T {XRz} -3380 -3735 0 0 0.17 0.17 {layer=13}
T {W=4 L=10} -3380 -3695 0 0 0.14 0.14 {layer=5}
N -3400 -3740 -3400 -3765 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3400 -3765 3 0 {name=p101 sig_type=std_logic lab=b03_cc_mid}
N -3400 -3680 -3400 -3655 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3400 -3655 1 0 {name=p102 sig_type=std_logic lab=pvdd}
N -3420 -3710 -3440 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3440 -3710 0 0 {name=p103 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/cap_mim_m3_1.sym} -3200 -3710 0 0 {name=XCout W=187 L=187 MF=1 model=cap_mim_m3_1 spiceprefix=X}
T {XCout} -3180 -3735 0 0 0.17 0.17 {layer=13}
T {W=187 L=187} -3180 -3695 0 0 0.14 0.14 {layer=5}
N -3200 -3740 -3200 -3765 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3200 -3765 3 0 {name=p104 sig_type=std_logic lab=pvdd}
N -3200 -3680 -3200 -3655 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3200 -3655 1 0 {name=p105 sig_type=std_logic lab=gnd}

* ============================================================
* Section 5: Current Limiter (Block 04)
* ============================================================
L 4 -2500 -3900 -300 -3900 {dash=5}
L 4 -300 -3900 -300 -3200 {dash=5}
L 4 -300 -3200 -2500 -3200 {dash=5}
L 4 -2500 -3200 -2500 -3900 {dash=5}
T {Section 5: Current Limiter (Block 04)} -2485 -3885 0 0 0.4 0.4 {layer=4}
T {Sense mirror + Vth detect + gate clamp — Ilim~70mA} -2485 -3855 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2380 -3710 0 0 {name=XMs L=0.5 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMs} -2385 -3755 0 0 0.18 0.18 {layer=13}
T {W=2 L=0.5} -2385 -3665 0 0 0.15 0.15 {layer=5}
N -2380 -3710 -2410 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2410 -3710 0 0 {name=p106 sig_type=std_logic lab=gate}
N -2340 -3710 -2310 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2310 -3710 2 0 {name=p107 sig_type=std_logic lab=bvdd}
N -2340 -3740 -2340 -3765 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2340 -3765 3 0 {name=p108 sig_type=std_logic lab=bvdd}
N -2340 -3680 -2340 -3655 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2340 -3655 1 0 {name=p109 sig_type=std_logic lab=b04_sense_n}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -2200 -3710 0 0 {name=XRs W=1 L=3.12 model=res_xhigh_po spiceprefix=X}
T {XRs} -2180 -3735 0 0 0.17 0.17 {layer=13}
T {W=1 L=3.12} -2180 -3695 0 0 0.14 0.14 {layer=5}
N -2200 -3740 -2200 -3765 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2200 -3765 3 0 {name=p110 sig_type=std_logic lab=b04_sense_n}
N -2200 -3680 -2200 -3655 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2200 -3655 1 0 {name=p111 sig_type=std_logic lab=gnd}
N -2220 -3710 -2240 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2240 -3710 0 0 {name=p112 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -1820 -3710 0 0 {name=XMdet L=1 W=5 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMdet} -1825 -3755 0 0 0.18 0.18 {layer=13}
T {W=5 L=1} -1825 -3665 0 0 0.15 0.15 {layer=5}
N -1820 -3710 -1850 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1850 -3710 0 0 {name=p113 sig_type=std_logic lab=b04_sense_n}
N -1780 -3710 -1750 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1750 -3710 2 0 {name=p114 sig_type=std_logic lab=gnd}
N -1780 -3740 -1780 -3765 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1780 -3765 3 0 {name=p115 sig_type=std_logic lab=b04_det_n}
N -1780 -3680 -1780 -3655 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1780 -3655 1 0 {name=p116 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -1800 -3710 0 0 {name=XRpu W=1 L=5 model=res_xhigh_po spiceprefix=X}
T {XRpu} -1780 -3735 0 0 0.17 0.17 {layer=13}
T {W=1 L=5} -1780 -3695 0 0 0.14 0.14 {layer=5}
N -1800 -3740 -1800 -3765 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1800 -3765 3 0 {name=p117 sig_type=std_logic lab=bvdd}
N -1800 -3680 -1800 -3655 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1800 -3655 1 0 {name=p118 sig_type=std_logic lab=b04_det_n}
N -1820 -3710 -1840 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1840 -3710 0 0 {name=p119 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1260 -3710 0 0 {name=XMclamp L=1 W=20 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMclamp} -1265 -3755 0 0 0.18 0.18 {layer=13}
T {W=20 L=1} -1265 -3665 0 0 0.15 0.15 {layer=5}
N -1260 -3710 -1290 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1290 -3710 0 0 {name=p120 sig_type=std_logic lab=b04_det_n}
N -1220 -3710 -1190 -3710 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1190 -3710 2 0 {name=p121 sig_type=std_logic lab=bvdd}
N -1220 -3740 -1220 -3765 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1220 -3765 3 0 {name=p122 sig_type=std_logic lab=bvdd}
N -1220 -3680 -1220 -3655 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1220 -3655 1 0 {name=p123 sig_type=std_logic lab=gate}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2380 -3470 0 0 {name=XMfp L=1 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMfp} -2385 -3515 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} -2385 -3425 0 0 0.15 0.15 {layer=5}
N -2380 -3470 -2410 -3470 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2410 -3470 0 0 {name=p124 sig_type=std_logic lab=b04_det_n}
N -2340 -3470 -2310 -3470 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2310 -3470 2 0 {name=p125 sig_type=std_logic lab=pvdd}
N -2340 -3500 -2340 -3525 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2340 -3525 3 0 {name=p126 sig_type=std_logic lab=pvdd}
N -2340 -3440 -2340 -3415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2340 -3415 1 0 {name=p127 sig_type=std_logic lab=ilim_flag}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -2100 -3470 0 0 {name=XMfn L=1 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMfn} -2105 -3515 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} -2105 -3425 0 0 0.15 0.15 {layer=5}
N -2100 -3470 -2130 -3470 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2130 -3470 0 0 {name=p128 sig_type=std_logic lab=b04_det_n}
N -2060 -3470 -2030 -3470 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2030 -3470 2 0 {name=p129 sig_type=std_logic lab=gnd}
N -2060 -3500 -2060 -3525 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2060 -3525 3 0 {name=p130 sig_type=std_logic lab=ilim_flag}
N -2060 -3440 -2060 -3415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2060 -3415 1 0 {name=p131 sig_type=std_logic lab=gnd}

* ============================================================
* Section 6: UV/OV Comparators (Block 05)
* ============================================================
L 7 1500 -4600 7100 -4600 {dash=5}
L 7 7100 -4600 7100 -2000 {dash=5}
L 7 7100 -2000 1500 -2000 {dash=5}
L 7 1500 -2000 1500 -4600 {dash=5}
T {Section 6: UV/OV Comparators (Block 05)} 1515 -4585 0 0 0.4 0.4 {layer=7}
T {NMOS diff pair + PMOS mirror + NOR output — SVDD domain} 1515 -4555 0 0 0.22 0.22 {layer=13}
T {UV Comparator — Trip PVDD < 4.3V} 1530 -4530 0 0 0.3 0.3 {layer=7}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1600 -4360 0 0 {name=uv_R_top value=500k}
T {uv_R_top} 1620 -4385 0 0 0.17 0.17 {layer=13}
T {500k} 1620 -4350 0 0 0.15 0.15 {layer=5}
N 1600 -4390 1600 -4415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 -4415 3 0 {name=p132 sig_type=std_logic lab=pvdd}
N 1600 -4330 1600 -4305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1600 -4305 1 0 {name=p133 sig_type=std_logic lab=b05uv_mid}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1800 -4360 0 0 {name=uv_R_bot value=199.4k}
T {uv_R_bot} 1820 -4385 0 0 0.17 0.17 {layer=13}
T {199.4k} 1820 -4350 0 0 0.15 0.15 {layer=5}
N 1800 -4390 1800 -4415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1800 -4415 3 0 {name=p134 sig_type=std_logic lab=b05uv_mid}
N 1800 -4330 1800 -4305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1800 -4305 1 0 {name=p135 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/res.sym} 2000 -4360 0 0 {name=uv_R_hyst value=2.5Meg}
T {uv_R_hyst} 2020 -4385 0 0 0.17 0.17 {layer=13}
T {2.5Meg} 2020 -4350 0 0 0.15 0.15 {layer=5}
N 2000 -4390 2000 -4415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2000 -4415 3 0 {name=p136 sig_type=std_logic lab=b05uv_out_n}
N 2000 -4330 2000 -4305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2000 -4305 1 0 {name=p137 sig_type=std_logic lab=b05uv_mid}
C {/usr/share/xschem/xschem_library/devices/res.sym} 2200 -4360 0 0 {name=uv_R_bias value=800k}
T {uv_R_bias} 2220 -4385 0 0 0.17 0.17 {layer=13}
T {800k} 2220 -4350 0 0 0.15 0.15 {layer=5}
N 2200 -4390 2200 -4415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2200 -4415 3 0 {name=p138 sig_type=std_logic lab=svdd}
N 2200 -4330 2200 -4305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2200 -4305 1 0 {name=p139 sig_type=std_logic lab=b05uv_bias_n}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1620 -4120 0 0 {name=uv_XMbias L=4 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {uv_XMbias} 1615 -4165 0 0 0.18 0.18 {layer=13}
T {W=1 L=4} 1615 -4075 0 0 0.15 0.15 {layer=5}
N 1620 -4120 1590 -4120 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1590 -4120 0 0 {name=p140 sig_type=std_logic lab=b05uv_bias_n}
N 1660 -4120 1690 -4120 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -4120 2 0 {name=p141 sig_type=std_logic lab=gnd}
N 1660 -4150 1660 -4175 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -4175 3 0 {name=p142 sig_type=std_logic lab=b05uv_bias_n}
N 1660 -4090 1660 -4065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -4065 1 0 {name=p143 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1900 -4120 0 0 {name=uv_XMtail L=4 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {uv_XMtail} 1895 -4165 0 0 0.18 0.18 {layer=13}
T {W=1 L=4} 1895 -4075 0 0 0.15 0.15 {layer=5}
N 1900 -4120 1870 -4120 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1870 -4120 0 0 {name=p144 sig_type=std_logic lab=b05uv_bias_n}
N 1940 -4120 1970 -4120 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1970 -4120 2 0 {name=p145 sig_type=std_logic lab=gnd}
N 1940 -4150 1940 -4175 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -4175 3 0 {name=p146 sig_type=std_logic lab=b05uv_tail}
N 1940 -4090 1940 -4065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -4065 1 0 {name=p147 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1620 -3880 0 0 {name=uv_XM1 L=1 W=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {uv_XM1} 1615 -3925 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 1615 -3835 0 0 0.15 0.15 {layer=5}
N 1620 -3880 1590 -3880 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1590 -3880 0 0 {name=p148 sig_type=std_logic lab=b05uv_mid}
N 1660 -3880 1690 -3880 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -3880 2 0 {name=p149 sig_type=std_logic lab=gnd}
N 1660 -3910 1660 -3935 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -3935 3 0 {name=p150 sig_type=std_logic lab=b05uv_out_p}
N 1660 -3850 1660 -3825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -3825 1 0 {name=p151 sig_type=std_logic lab=b05uv_tail}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1900 -3880 0 0 {name=uv_XM2 L=1 W=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {uv_XM2} 1895 -3925 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 1895 -3835 0 0 0.15 0.15 {layer=5}
N 1900 -3880 1870 -3880 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1870 -3880 0 0 {name=p152 sig_type=std_logic lab=avbg}
N 1940 -3880 1970 -3880 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1970 -3880 2 0 {name=p153 sig_type=std_logic lab=gnd}
N 1940 -3910 1940 -3935 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -3935 3 0 {name=p154 sig_type=std_logic lab=b05uv_out_n}
N 1940 -3850 1940 -3825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -3825 1 0 {name=p155 sig_type=std_logic lab=b05uv_tail}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1620 -3640 0 0 {name=uv_XM3 L=1 W=2 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {uv_XM3} 1615 -3685 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 1615 -3595 0 0 0.15 0.15 {layer=5}
N 1620 -3640 1590 -3640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1590 -3640 0 0 {name=p156 sig_type=std_logic lab=b05uv_out_p}
N 1660 -3640 1690 -3640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -3640 2 0 {name=p157 sig_type=std_logic lab=svdd}
N 1660 -3670 1660 -3695 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -3695 3 0 {name=p158 sig_type=std_logic lab=svdd}
N 1660 -3610 1660 -3585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -3585 1 0 {name=p159 sig_type=std_logic lab=b05uv_out_p}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1900 -3640 0 0 {name=uv_XM4 L=1 W=2 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {uv_XM4} 1895 -3685 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 1895 -3595 0 0 0.15 0.15 {layer=5}
N 1900 -3640 1870 -3640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1870 -3640 0 0 {name=p160 sig_type=std_logic lab=b05uv_out_p}
N 1940 -3640 1970 -3640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1970 -3640 2 0 {name=p161 sig_type=std_logic lab=svdd}
N 1940 -3670 1940 -3695 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -3695 3 0 {name=p162 sig_type=std_logic lab=svdd}
N 1940 -3610 1940 -3585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -3585 1 0 {name=p163 sig_type=std_logic lab=b05uv_out_n}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 1620 -3400 0 0 {name=uv_XMen_n L=0.15 W=0.42 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {uv_XMen_n} 1615 -3445 0 0 0.18 0.18 {layer=13}
T {W=0.42 L=0.15} 1615 -3355 0 0 0.15 0.15 {layer=5}
N 1620 -3400 1590 -3400 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1590 -3400 0 0 {name=p164 sig_type=std_logic lab=uvov_en}
N 1660 -3400 1690 -3400 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -3400 2 0 {name=p165 sig_type=std_logic lab=gnd}
N 1660 -3430 1660 -3455 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -3455 3 0 {name=p166 sig_type=std_logic lab=b05uv_en_bar}
N 1660 -3370 1660 -3345 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -3345 1 0 {name=p167 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1900 -3400 0 0 {name=uv_XMen_p L=0.15 W=0.84 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {uv_XMen_p} 1895 -3445 0 0 0.18 0.18 {layer=13}
T {W=0.84 L=0.15} 1895 -3355 0 0 0.15 0.15 {layer=5}
N 1900 -3400 1870 -3400 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1870 -3400 0 0 {name=p168 sig_type=std_logic lab=uvov_en}
N 1940 -3400 1970 -3400 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1970 -3400 2 0 {name=p169 sig_type=std_logic lab=svdd}
N 1940 -3430 1940 -3455 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -3455 3 0 {name=p170 sig_type=std_logic lab=svdd}
N 1940 -3370 1940 -3345 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -3345 1 0 {name=p171 sig_type=std_logic lab=b05uv_en_bar}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1620 -3160 0 0 {name=uv_XMnor_p1 L=0.15 W=4 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {uv_XMnor_p1} 1615 -3205 0 0 0.18 0.18 {layer=13}
T {W=4 L=0.15} 1615 -3115 0 0 0.15 0.15 {layer=5}
N 1620 -3160 1590 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1590 -3160 0 0 {name=p172 sig_type=std_logic lab=b05uv_out_n}
N 1660 -3160 1690 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -3160 2 0 {name=p173 sig_type=std_logic lab=svdd}
N 1660 -3190 1660 -3215 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -3215 3 0 {name=p174 sig_type=std_logic lab=svdd}
N 1660 -3130 1660 -3105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1660 -3105 1 0 {name=p175 sig_type=std_logic lab=b05uv_nor_mid}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1900 -3160 0 0 {name=uv_XMnor_p2 L=0.15 W=4 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {uv_XMnor_p2} 1895 -3205 0 0 0.18 0.18 {layer=13}
T {W=4 L=0.15} 1895 -3115 0 0 0.15 0.15 {layer=5}
N 1900 -3160 1870 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1870 -3160 0 0 {name=p176 sig_type=std_logic lab=b05uv_en_bar}
N 1940 -3160 1970 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1970 -3160 2 0 {name=p177 sig_type=std_logic lab=b05uv_nor_mid}
N 1940 -3190 1940 -3215 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -3215 3 0 {name=p178 sig_type=std_logic lab=b05uv_nor_mid}
N 1940 -3130 1940 -3105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1940 -3105 1 0 {name=p179 sig_type=std_logic lab=uv_flag}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2180 -3160 0 0 {name=uv_XMnor_n1 L=0.15 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {uv_XMnor_n1} 2175 -3205 0 0 0.18 0.18 {layer=13}
T {W=1 L=0.15} 2175 -3115 0 0 0.15 0.15 {layer=5}
N 2180 -3160 2150 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2150 -3160 0 0 {name=p180 sig_type=std_logic lab=b05uv_out_n}
N 2220 -3160 2250 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2250 -3160 2 0 {name=p181 sig_type=std_logic lab=gnd}
N 2220 -3190 2220 -3215 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2220 -3215 3 0 {name=p182 sig_type=std_logic lab=uv_flag}
N 2220 -3130 2220 -3105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2220 -3105 1 0 {name=p183 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 2460 -3160 0 0 {name=uv_XMnor_n2 L=0.15 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {uv_XMnor_n2} 2455 -3205 0 0 0.18 0.18 {layer=13}
T {W=1 L=0.15} 2455 -3115 0 0 0.15 0.15 {layer=5}
N 2460 -3160 2430 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2430 -3160 0 0 {name=p184 sig_type=std_logic lab=b05uv_en_bar}
N 2500 -3160 2530 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2530 -3160 2 0 {name=p185 sig_type=std_logic lab=gnd}
N 2500 -3190 2500 -3215 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2500 -3215 3 0 {name=p186 sig_type=std_logic lab=uv_flag}
N 2500 -3130 2500 -3105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 2500 -3105 1 0 {name=p187 sig_type=std_logic lab=gnd}
T {OV Comparator — Trip PVDD > 5.5V} 4330 -4530 0 0 0.3 0.3 {layer=7}
C {/usr/share/xschem/xschem_library/devices/res.sym} 4400 -4360 0 0 {name=ov_R_top value=500k}
T {ov_R_top} 4420 -4385 0 0 0.17 0.17 {layer=13}
T {500k} 4420 -4350 0 0 0.15 0.15 {layer=5}
N 4400 -4390 4400 -4415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4400 -4415 3 0 {name=p188 sig_type=std_logic lab=pvdd}
N 4400 -4330 4400 -4305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4400 -4305 1 0 {name=p189 sig_type=std_logic lab=b05ov_mid}
C {/usr/share/xschem/xschem_library/devices/res.sym} 4600 -4360 0 0 {name=ov_R_bot value=146k}
T {ov_R_bot} 4620 -4385 0 0 0.17 0.17 {layer=13}
T {146k} 4620 -4350 0 0 0.15 0.15 {layer=5}
N 4600 -4390 4600 -4415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4600 -4415 3 0 {name=p190 sig_type=std_logic lab=b05ov_mid}
N 4600 -4330 4600 -4305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4600 -4305 1 0 {name=p191 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/res.sym} 4800 -4360 0 0 {name=ov_R_hyst value=8Meg}
T {ov_R_hyst} 4820 -4385 0 0 0.17 0.17 {layer=13}
T {8Meg} 4820 -4350 0 0 0.15 0.15 {layer=5}
N 4800 -4390 4800 -4415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4800 -4415 3 0 {name=p192 sig_type=std_logic lab=ov_flag}
N 4800 -4330 4800 -4305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4800 -4305 1 0 {name=p193 sig_type=std_logic lab=b05ov_mid}
C {/usr/share/xschem/xschem_library/devices/res.sym} 5000 -4360 0 0 {name=ov_R_bias value=800k}
T {ov_R_bias} 5020 -4385 0 0 0.17 0.17 {layer=13}
T {800k} 5020 -4350 0 0 0.15 0.15 {layer=5}
N 5000 -4390 5000 -4415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5000 -4415 3 0 {name=p194 sig_type=std_logic lab=svdd}
N 5000 -4330 5000 -4305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5000 -4305 1 0 {name=p195 sig_type=std_logic lab=b05ov_bias_n}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 4420 -4120 0 0 {name=ov_XMbias L=4 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {ov_XMbias} 4415 -4165 0 0 0.18 0.18 {layer=13}
T {W=1 L=4} 4415 -4075 0 0 0.15 0.15 {layer=5}
N 4420 -4120 4390 -4120 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4390 -4120 0 0 {name=p196 sig_type=std_logic lab=b05ov_bias_n}
N 4460 -4120 4490 -4120 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4490 -4120 2 0 {name=p197 sig_type=std_logic lab=gnd}
N 4460 -4150 4460 -4175 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -4175 3 0 {name=p198 sig_type=std_logic lab=b05ov_bias_n}
N 4460 -4090 4460 -4065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -4065 1 0 {name=p199 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 4700 -4120 0 0 {name=ov_XMtail L=4 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {ov_XMtail} 4695 -4165 0 0 0.18 0.18 {layer=13}
T {W=1 L=4} 4695 -4075 0 0 0.15 0.15 {layer=5}
N 4700 -4120 4670 -4120 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4670 -4120 0 0 {name=p200 sig_type=std_logic lab=b05ov_bias_n}
N 4740 -4120 4770 -4120 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4770 -4120 2 0 {name=p201 sig_type=std_logic lab=gnd}
N 4740 -4150 4740 -4175 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -4175 3 0 {name=p202 sig_type=std_logic lab=b05ov_tail}
N 4740 -4090 4740 -4065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -4065 1 0 {name=p203 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 4420 -3880 0 0 {name=ov_XM1 L=1 W=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {ov_XM1} 4415 -3925 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 4415 -3835 0 0 0.15 0.15 {layer=5}
N 4420 -3880 4390 -3880 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4390 -3880 0 0 {name=p204 sig_type=std_logic lab=avbg}
N 4460 -3880 4490 -3880 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4490 -3880 2 0 {name=p205 sig_type=std_logic lab=gnd}
N 4460 -3910 4460 -3935 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -3935 3 0 {name=p206 sig_type=std_logic lab=b05ov_out_p}
N 4460 -3850 4460 -3825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -3825 1 0 {name=p207 sig_type=std_logic lab=b05ov_tail}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 4700 -3880 0 0 {name=ov_XM2 L=1 W=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {ov_XM2} 4695 -3925 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 4695 -3835 0 0 0.15 0.15 {layer=5}
N 4700 -3880 4670 -3880 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4670 -3880 0 0 {name=p208 sig_type=std_logic lab=b05ov_mid}
N 4740 -3880 4770 -3880 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4770 -3880 2 0 {name=p209 sig_type=std_logic lab=gnd}
N 4740 -3910 4740 -3935 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -3935 3 0 {name=p210 sig_type=std_logic lab=b05ov_out_n}
N 4740 -3850 4740 -3825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -3825 1 0 {name=p211 sig_type=std_logic lab=b05ov_tail}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 4420 -3640 0 0 {name=ov_XM3 L=1 W=2 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {ov_XM3} 4415 -3685 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 4415 -3595 0 0 0.15 0.15 {layer=5}
N 4420 -3640 4390 -3640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4390 -3640 0 0 {name=p212 sig_type=std_logic lab=b05ov_out_p}
N 4460 -3640 4490 -3640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4490 -3640 2 0 {name=p213 sig_type=std_logic lab=svdd}
N 4460 -3670 4460 -3695 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -3695 3 0 {name=p214 sig_type=std_logic lab=svdd}
N 4460 -3610 4460 -3585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -3585 1 0 {name=p215 sig_type=std_logic lab=b05ov_out_p}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 4700 -3640 0 0 {name=ov_XM4 L=1 W=2 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {ov_XM4} 4695 -3685 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 4695 -3595 0 0 0.15 0.15 {layer=5}
N 4700 -3640 4670 -3640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4670 -3640 0 0 {name=p216 sig_type=std_logic lab=b05ov_out_p}
N 4740 -3640 4770 -3640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4770 -3640 2 0 {name=p217 sig_type=std_logic lab=svdd}
N 4740 -3670 4740 -3695 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -3695 3 0 {name=p218 sig_type=std_logic lab=svdd}
N 4740 -3610 4740 -3585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -3585 1 0 {name=p219 sig_type=std_logic lab=b05ov_out_n}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 4420 -3400 0 0 {name=ov_XMen_n L=0.15 W=0.42 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {ov_XMen_n} 4415 -3445 0 0 0.18 0.18 {layer=13}
T {W=0.42 L=0.15} 4415 -3355 0 0 0.15 0.15 {layer=5}
N 4420 -3400 4390 -3400 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4390 -3400 0 0 {name=p220 sig_type=std_logic lab=uvov_en}
N 4460 -3400 4490 -3400 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4490 -3400 2 0 {name=p221 sig_type=std_logic lab=gnd}
N 4460 -3430 4460 -3455 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -3455 3 0 {name=p222 sig_type=std_logic lab=b05ov_en_bar}
N 4460 -3370 4460 -3345 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -3345 1 0 {name=p223 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 4700 -3400 0 0 {name=ov_XMen_p L=0.15 W=0.84 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {ov_XMen_p} 4695 -3445 0 0 0.18 0.18 {layer=13}
T {W=0.84 L=0.15} 4695 -3355 0 0 0.15 0.15 {layer=5}
N 4700 -3400 4670 -3400 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4670 -3400 0 0 {name=p224 sig_type=std_logic lab=uvov_en}
N 4740 -3400 4770 -3400 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4770 -3400 2 0 {name=p225 sig_type=std_logic lab=svdd}
N 4740 -3430 4740 -3455 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -3455 3 0 {name=p226 sig_type=std_logic lab=svdd}
N 4740 -3370 4740 -3345 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -3345 1 0 {name=p227 sig_type=std_logic lab=b05ov_en_bar}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 4420 -3160 0 0 {name=ov_XMnor_p1 L=0.15 W=4 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {ov_XMnor_p1} 4415 -3205 0 0 0.18 0.18 {layer=13}
T {W=4 L=0.15} 4415 -3115 0 0 0.15 0.15 {layer=5}
N 4420 -3160 4390 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4390 -3160 0 0 {name=p228 sig_type=std_logic lab=b05ov_out_n}
N 4460 -3160 4490 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4490 -3160 2 0 {name=p229 sig_type=std_logic lab=svdd}
N 4460 -3190 4460 -3215 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -3215 3 0 {name=p230 sig_type=std_logic lab=svdd}
N 4460 -3130 4460 -3105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4460 -3105 1 0 {name=p231 sig_type=std_logic lab=b05ov_nor_mid}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 4700 -3160 0 0 {name=ov_XMnor_p2 L=0.15 W=4 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
T {ov_XMnor_p2} 4695 -3205 0 0 0.18 0.18 {layer=13}
T {W=4 L=0.15} 4695 -3115 0 0 0.15 0.15 {layer=5}
N 4700 -3160 4670 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4670 -3160 0 0 {name=p232 sig_type=std_logic lab=b05ov_en_bar}
N 4740 -3160 4770 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4770 -3160 2 0 {name=p233 sig_type=std_logic lab=b05ov_nor_mid}
N 4740 -3190 4740 -3215 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -3215 3 0 {name=p234 sig_type=std_logic lab=b05ov_nor_mid}
N 4740 -3130 4740 -3105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4740 -3105 1 0 {name=p235 sig_type=std_logic lab=ov_flag}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 4980 -3160 0 0 {name=ov_XMnor_n1 L=0.15 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {ov_XMnor_n1} 4975 -3205 0 0 0.18 0.18 {layer=13}
T {W=1 L=0.15} 4975 -3115 0 0 0.15 0.15 {layer=5}
N 4980 -3160 4950 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4950 -3160 0 0 {name=p236 sig_type=std_logic lab=b05ov_out_n}
N 5020 -3160 5050 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5050 -3160 2 0 {name=p237 sig_type=std_logic lab=gnd}
N 5020 -3190 5020 -3215 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5020 -3215 3 0 {name=p238 sig_type=std_logic lab=ov_flag}
N 5020 -3130 5020 -3105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5020 -3105 1 0 {name=p239 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 5260 -3160 0 0 {name=ov_XMnor_n2 L=0.15 W=1 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
T {ov_XMnor_n2} 5255 -3205 0 0 0.18 0.18 {layer=13}
T {W=1 L=0.15} 5255 -3115 0 0 0.15 0.15 {layer=5}
N 5260 -3160 5230 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5230 -3160 0 0 {name=p240 sig_type=std_logic lab=b05ov_en_bar}
N 5300 -3160 5330 -3160 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5330 -3160 2 0 {name=p241 sig_type=std_logic lab=gnd}
N 5300 -3190 5300 -3215 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5300 -3215 3 0 {name=p242 sig_type=std_logic lab=ov_flag}
N 5300 -3130 5300 -3105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 5300 -3105 1 0 {name=p243 sig_type=std_logic lab=gnd}

* ============================================================
* Section 7: Level Shifter (Block 06)
* ============================================================
L 7 -3700 -3200 -1900 -3200 {dash=5}
L 7 -1900 -3200 -1900 -2500 {dash=5}
L 7 -1900 -2500 -3700 -2500 {dash=5}
L 7 -3700 -2500 -3700 -3200 {dash=5}
T {Section 7: Level Shifter (Block 06)} -3685 -3185 0 0 0.4 0.4 {layer=7}
T {SVDD->BVDD cross-coupled PMOS — 6 FETs} -3685 -3155 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 -3010 0 0 {name=XMN_INV L=0.5 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN_INV} -3585 -3055 0 0 0.18 0.18 {layer=13}
T {W=2 L=0.5} -3585 -2965 0 0 0.15 0.15 {layer=5}
N -3580 -3010 -3610 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -3010 0 0 {name=p244 sig_type=std_logic lab=en}
N -3540 -3010 -3510 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -3010 2 0 {name=p245 sig_type=std_logic lab=gnd}
N -3540 -3040 -3540 -3065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -3065 3 0 {name=p246 sig_type=std_logic lab=b06_in_b}
N -3540 -2980 -3540 -2955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -2955 1 0 {name=p247 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3300 -3010 0 0 {name=XMP_INV L=0.5 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMP_INV} -3305 -3055 0 0 0.18 0.18 {layer=13}
T {W=4 L=0.5} -3305 -2965 0 0 0.15 0.15 {layer=5}
N -3300 -3010 -3330 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -3010 0 0 {name=p248 sig_type=std_logic lab=en}
N -3260 -3010 -3230 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -3010 2 0 {name=p249 sig_type=std_logic lab=svdd}
N -3260 -3040 -3260 -3065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -3065 3 0 {name=p250 sig_type=std_logic lab=svdd}
N -3260 -2980 -3260 -2955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -2955 1 0 {name=p251 sig_type=std_logic lab=b06_in_b}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 -2770 0 0 {name=XMN1 L=1 W=15 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN1} -3585 -2815 0 0 0.18 0.18 {layer=13}
T {W=15 L=1} -3585 -2725 0 0 0.15 0.15 {layer=5}
N -3580 -2770 -3610 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -2770 0 0 {name=p252 sig_type=std_logic lab=en}
N -3540 -2770 -3510 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -2770 2 0 {name=p253 sig_type=std_logic lab=gnd}
N -3540 -2800 -3540 -2825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -2825 3 0 {name=p254 sig_type=std_logic lab=b06_n1}
N -3540 -2740 -3540 -2715 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -2715 1 0 {name=p255 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 -2770 0 0 {name=XMN2 L=1 W=15 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN2} -3305 -2815 0 0 0.18 0.18 {layer=13}
T {W=15 L=1} -3305 -2725 0 0 0.15 0.15 {layer=5}
N -3300 -2770 -3330 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -2770 0 0 {name=p256 sig_type=std_logic lab=b06_in_b}
N -3260 -2770 -3230 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -2770 2 0 {name=p257 sig_type=std_logic lab=gnd}
N -3260 -2800 -3260 -2825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -2825 3 0 {name=p258 sig_type=std_logic lab=en_bvdd}
N -3260 -2740 -3260 -2715 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -2715 1 0 {name=p259 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3020 -2770 0 0 {name=XMP1 L=0.5 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMP1} -3025 -2815 0 0 0.18 0.18 {layer=13}
T {W=4 L=0.5} -3025 -2725 0 0 0.15 0.15 {layer=5}
N -3020 -2770 -3050 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 -2770 0 0 {name=p260 sig_type=std_logic lab=en_bvdd}
N -2980 -2770 -2950 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 -2770 2 0 {name=p261 sig_type=std_logic lab=bvdd}
N -2980 -2800 -2980 -2825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 -2825 3 0 {name=p262 sig_type=std_logic lab=bvdd}
N -2980 -2740 -2980 -2715 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 -2715 1 0 {name=p263 sig_type=std_logic lab=b06_n1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2740 -2770 0 0 {name=XMP2 L=0.5 W=5 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMP2} -2745 -2815 0 0 0.18 0.18 {layer=13}
T {W=5 L=0.5} -2745 -2725 0 0 0.15 0.15 {layer=5}
N -2740 -2770 -2770 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2770 -2770 0 0 {name=p264 sig_type=std_logic lab=b06_n1}
N -2700 -2770 -2670 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2670 -2770 2 0 {name=p265 sig_type=std_logic lab=bvdd}
N -2700 -2800 -2700 -2825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 -2825 3 0 {name=p266 sig_type=std_logic lab=bvdd}
N -2700 -2740 -2700 -2715 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 -2715 1 0 {name=p267 sig_type=std_logic lab=en_bvdd}

* ============================================================
* Section 8: Zener Clamp (Block 07)
* ============================================================
L 5 -1700 -3200 300 -3200 {dash=5}
L 5 300 -3200 300 -1400 {dash=5}
L 5 300 -1400 -1700 -1400 {dash=5}
L 5 -1700 -1400 -1700 -3200 {dash=5}
T {Section 8: Zener Clamp (Block 07)} -1685 -3185 0 0 0.4 0.4 {layer=5}
T {Hybrid N-P-N-P-N stack + 7x fast diodes + clamp NFET} -1685 -3155 0 0 0.22 0.22 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -1580 -3010 0 0 {name=XMd1 L=4 W=2.2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMd1} -1585 -3055 0 0 0.18 0.18 {layer=13}
T {W=2.2 L=4} -1585 -2965 0 0 0.15 0.15 {layer=5}
N -1580 -3010 -1610 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1610 -3010 0 0 {name=p268 sig_type=std_logic lab=pvdd}
N -1540 -3010 -1510 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1510 -3010 2 0 {name=p269 sig_type=std_logic lab=b07_n4}
N -1540 -3040 -1540 -3065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -3065 3 0 {name=p270 sig_type=std_logic lab=pvdd}
N -1540 -2980 -1540 -2955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -2955 1 0 {name=p271 sig_type=std_logic lab=b07_n4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1580 -2770 0 0 {name=XMd2 L=4 W=20 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMd2} -1585 -2815 0 0 0.18 0.18 {layer=13}
T {W=20 L=4} -1585 -2725 0 0 0.15 0.15 {layer=5}
N -1580 -2770 -1610 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1610 -2770 0 0 {name=p272 sig_type=std_logic lab=b07_n3}
N -1540 -2770 -1510 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1510 -2770 2 0 {name=p273 sig_type=std_logic lab=b07_n4}
N -1540 -2800 -1540 -2825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -2825 3 0 {name=p274 sig_type=std_logic lab=b07_n4}
N -1540 -2740 -1540 -2715 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -2715 1 0 {name=p275 sig_type=std_logic lab=b07_n3}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -1580 -2530 0 0 {name=XMd3 L=4 W=2.2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMd3} -1585 -2575 0 0 0.18 0.18 {layer=13}
T {W=2.2 L=4} -1585 -2485 0 0 0.15 0.15 {layer=5}
N -1580 -2530 -1610 -2530 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1610 -2530 0 0 {name=p276 sig_type=std_logic lab=b07_n3}
N -1540 -2530 -1510 -2530 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1510 -2530 2 0 {name=p277 sig_type=std_logic lab=b07_n2}
N -1540 -2560 -1540 -2585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -2585 3 0 {name=p278 sig_type=std_logic lab=b07_n3}
N -1540 -2500 -1540 -2475 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -2475 1 0 {name=p279 sig_type=std_logic lab=b07_n2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1580 -2290 0 0 {name=XMd4 L=4 W=20 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMd4} -1585 -2335 0 0 0.18 0.18 {layer=13}
T {W=20 L=4} -1585 -2245 0 0 0.15 0.15 {layer=5}
N -1580 -2290 -1610 -2290 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1610 -2290 0 0 {name=p280 sig_type=std_logic lab=b07_n1}
N -1540 -2290 -1510 -2290 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1510 -2290 2 0 {name=p281 sig_type=std_logic lab=b07_n2}
N -1540 -2320 -1540 -2345 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -2345 3 0 {name=p282 sig_type=std_logic lab=b07_n2}
N -1540 -2260 -1540 -2235 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -2235 1 0 {name=p283 sig_type=std_logic lab=b07_n1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -1580 -2050 0 0 {name=XMd5 L=4 W=2.2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMd5} -1585 -2095 0 0 0.18 0.18 {layer=13}
T {W=2.2 L=4} -1585 -2005 0 0 0.15 0.15 {layer=5}
N -1580 -2050 -1610 -2050 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1610 -2050 0 0 {name=p284 sig_type=std_logic lab=b07_n1}
N -1540 -2050 -1510 -2050 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1510 -2050 2 0 {name=p285 sig_type=std_logic lab=b07_vg}
N -1540 -2080 -1540 -2105 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -2105 3 0 {name=p286 sig_type=std_logic lab=b07_n1}
N -1540 -2020 -1540 -1995 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1540 -1995 1 0 {name=p287 sig_type=std_logic lab=b07_vg}
C {/usr/share/xschem/xschem_library/devices/res.sym} -1600 -1810 0 0 {name=Rpd value=500k}
T {Rpd} -1580 -1835 0 0 0.17 0.17 {layer=13}
T {500k} -1580 -1800 0 0 0.15 0.15 {layer=5}
N -1600 -1840 -1600 -1865 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1600 -1865 3 0 {name=p288 sig_type=std_logic lab=b07_vg}
N -1600 -1780 -1600 -1755 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1600 -1755 1 0 {name=p289 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -1300 -1810 0 0 {name=XMclamp L=0.5 W=100 nf=1 mult=4 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMclamp} -1305 -1855 0 0 0.18 0.18 {layer=13}
T {W=100 L=0.5 m=4} -1305 -1765 0 0 0.15 0.15 {layer=5}
N -1300 -1810 -1330 -1810 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1330 -1810 0 0 {name=p290 sig_type=std_logic lab=b07_vg}
N -1260 -1810 -1230 -1810 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1230 -1810 2 0 {name=p291 sig_type=std_logic lab=gnd}
N -1260 -1840 -1260 -1865 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1260 -1865 3 0 {name=p292 sig_type=std_logic lab=pvdd}
N -1260 -1780 -1260 -1755 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1260 -1755 1 0 {name=p293 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -980 -3010 0 0 {name=XMf1 L=0.5 W=10 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf1} -985 -3055 0 0 0.18 0.18 {layer=13}
T {W=10 L=0.5} -985 -2965 0 0 0.15 0.15 {layer=5}
N -980 -3010 -1010 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1010 -3010 0 0 {name=p294 sig_type=std_logic lab=pvdd}
N -940 -3010 -910 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -910 -3010 2 0 {name=p295 sig_type=std_logic lab=gnd}
N -940 -3040 -940 -3065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -940 -3065 3 0 {name=p296 sig_type=std_logic lab=pvdd}
N -940 -2980 -940 -2955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -940 -2955 1 0 {name=p297 sig_type=std_logic lab=b07_nf6}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -700 -3010 0 0 {name=XMf2 L=0.5 W=10 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf2} -705 -3055 0 0 0.18 0.18 {layer=13}
T {W=10 L=0.5} -705 -2965 0 0 0.15 0.15 {layer=5}
N -700 -3010 -730 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -730 -3010 0 0 {name=p298 sig_type=std_logic lab=b07_nf6}
N -660 -3010 -630 -3010 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -630 -3010 2 0 {name=p299 sig_type=std_logic lab=gnd}
N -660 -3040 -660 -3065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -660 -3065 3 0 {name=p300 sig_type=std_logic lab=b07_nf6}
N -660 -2980 -660 -2955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -660 -2955 1 0 {name=p301 sig_type=std_logic lab=b07_nf5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -980 -2770 0 0 {name=XMf3 L=0.5 W=10 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf3} -985 -2815 0 0 0.18 0.18 {layer=13}
T {W=10 L=0.5} -985 -2725 0 0 0.15 0.15 {layer=5}
N -980 -2770 -1010 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1010 -2770 0 0 {name=p302 sig_type=std_logic lab=b07_nf5}
N -940 -2770 -910 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -910 -2770 2 0 {name=p303 sig_type=std_logic lab=gnd}
N -940 -2800 -940 -2825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -940 -2825 3 0 {name=p304 sig_type=std_logic lab=b07_nf5}
N -940 -2740 -940 -2715 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -940 -2715 1 0 {name=p305 sig_type=std_logic lab=b07_nf4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -700 -2770 0 0 {name=XMf4 L=0.5 W=10 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf4} -705 -2815 0 0 0.18 0.18 {layer=13}
T {W=10 L=0.5} -705 -2725 0 0 0.15 0.15 {layer=5}
N -700 -2770 -730 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -730 -2770 0 0 {name=p306 sig_type=std_logic lab=b07_nf4}
N -660 -2770 -630 -2770 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -630 -2770 2 0 {name=p307 sig_type=std_logic lab=gnd}
N -660 -2800 -660 -2825 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -660 -2825 3 0 {name=p308 sig_type=std_logic lab=b07_nf4}
N -660 -2740 -660 -2715 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -660 -2715 1 0 {name=p309 sig_type=std_logic lab=b07_nf3}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -980 -2530 0 0 {name=XMf5 L=0.5 W=10 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf5} -985 -2575 0 0 0.18 0.18 {layer=13}
T {W=10 L=0.5} -985 -2485 0 0 0.15 0.15 {layer=5}
N -980 -2530 -1010 -2530 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1010 -2530 0 0 {name=p310 sig_type=std_logic lab=b07_nf3}
N -940 -2530 -910 -2530 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -910 -2530 2 0 {name=p311 sig_type=std_logic lab=gnd}
N -940 -2560 -940 -2585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -940 -2585 3 0 {name=p312 sig_type=std_logic lab=b07_nf3}
N -940 -2500 -940 -2475 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -940 -2475 1 0 {name=p313 sig_type=std_logic lab=b07_nf2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -700 -2530 0 0 {name=XMf6 L=0.5 W=10 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf6} -705 -2575 0 0 0.18 0.18 {layer=13}
T {W=10 L=0.5} -705 -2485 0 0 0.15 0.15 {layer=5}
N -700 -2530 -730 -2530 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -730 -2530 0 0 {name=p314 sig_type=std_logic lab=b07_nf2}
N -660 -2530 -630 -2530 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -630 -2530 2 0 {name=p315 sig_type=std_logic lab=gnd}
N -660 -2560 -660 -2585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -660 -2585 3 0 {name=p316 sig_type=std_logic lab=b07_nf2}
N -660 -2500 -660 -2475 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -660 -2475 1 0 {name=p317 sig_type=std_logic lab=b07_nf1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -980 -2290 0 0 {name=XMf7 L=0.5 W=10 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMf7} -985 -2335 0 0 0.18 0.18 {layer=13}
T {W=10 L=0.5} -985 -2245 0 0 0.15 0.15 {layer=5}
N -980 -2290 -1010 -2290 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1010 -2290 0 0 {name=p318 sig_type=std_logic lab=b07_nf1}
N -940 -2290 -910 -2290 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -910 -2290 2 0 {name=p319 sig_type=std_logic lab=gnd}
N -940 -2320 -940 -2345 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -940 -2345 3 0 {name=p320 sig_type=std_logic lab=b07_nf1}
N -940 -2260 -940 -2235 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -940 -2235 1 0 {name=p321 sig_type=std_logic lab=gnd}

* ============================================================
* Section 9: Mode Control (Block 08)
* ============================================================
L 4 -3700 -1300 4700 -1300 {dash=5}
L 4 4700 -1300 4700 4200 {dash=5}
L 4 4700 4200 -3700 4200 {dash=5}
L 4 -3700 4200 -3700 -1300 {dash=5}
T {Section 9: Mode Control (Block 08)} -3685 -1285 0 0 0.4 0.4 {layer=4}
T {BVDD ladder + 4 Schmitt comparators + combinational logic — 62 FETs + 5 resistors} -3685 -1255 0 0 0.22 0.22 {layer=13}
T {Resistor Ladder (~400k)} -3670 -1220 0 0 0.28 0.28 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -3600 -1110 0 0 {name=XRtop W=1 L=37 model=res_xhigh_po spiceprefix=X}
T {XRtop} -3580 -1135 0 0 0.17 0.17 {layer=13}
T {W=1 L=37} -3580 -1095 0 0 0.14 0.14 {layer=5}
N -3600 -1140 -3600 -1165 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3600 -1165 3 0 {name=p322 sig_type=std_logic lab=bvdd}
N -3600 -1080 -3600 -1055 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3600 -1055 1 0 {name=p323 sig_type=std_logic lab=b08_tap1}
N -3620 -1110 -3640 -1110 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3640 -1110 0 0 {name=p324 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -3400 -1110 0 0 {name=XR12 W=1 L=62 model=res_xhigh_po spiceprefix=X}
T {XR12} -3380 -1135 0 0 0.17 0.17 {layer=13}
T {W=1 L=62} -3380 -1095 0 0 0.14 0.14 {layer=5}
N -3400 -1140 -3400 -1165 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3400 -1165 3 0 {name=p325 sig_type=std_logic lab=b08_tap1}
N -3400 -1080 -3400 -1055 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3400 -1055 1 0 {name=p326 sig_type=std_logic lab=b08_tap2}
N -3420 -1110 -3440 -1110 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3440 -1110 0 0 {name=p327 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -3200 -1110 0 0 {name=XR23 W=1 L=6 model=res_xhigh_po spiceprefix=X}
T {XR23} -3180 -1135 0 0 0.17 0.17 {layer=13}
T {W=1 L=6} -3180 -1095 0 0 0.14 0.14 {layer=5}
N -3200 -1140 -3200 -1165 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3200 -1165 3 0 {name=p328 sig_type=std_logic lab=b08_tap2}
N -3200 -1080 -3200 -1055 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3200 -1055 1 0 {name=p329 sig_type=std_logic lab=b08_tap3}
N -3220 -1110 -3240 -1110 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3240 -1110 0 0 {name=p330 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -3000 -1110 0 0 {name=XR34 W=1 L=17 model=res_xhigh_po spiceprefix=X}
T {XR34} -2980 -1135 0 0 0.17 0.17 {layer=13}
T {W=1 L=17} -2980 -1095 0 0 0.14 0.14 {layer=5}
N -3000 -1140 -3000 -1165 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3000 -1165 3 0 {name=p331 sig_type=std_logic lab=b08_tap3}
N -3000 -1080 -3000 -1055 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3000 -1055 1 0 {name=p332 sig_type=std_logic lab=b08_tap4}
N -3020 -1110 -3040 -1110 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3040 -1110 0 0 {name=p333 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} -2800 -1110 0 0 {name=XRbot W=1 L=69 model=res_xhigh_po spiceprefix=X}
T {XRbot} -2780 -1135 0 0 0.17 0.17 {layer=13}
T {W=1 L=69} -2780 -1095 0 0 0.14 0.14 {layer=5}
N -2800 -1140 -2800 -1165 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2800 -1165 3 0 {name=p334 sig_type=std_logic lab=b08_tap4}
N -2800 -1080 -2800 -1055 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2800 -1055 1 0 {name=p335 sig_type=std_logic lab=gnd}
N -2820 -1110 -2840 -1110 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2840 -1110 0 0 {name=p336 sig_type=std_logic lab=gnd}
T {Comparators (Schmitt trigger)} -3670 -920 0 0 0.28 0.28 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3580 -760 0 0 {name=XMc1ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMc1ivp} -3585 -805 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3585 -715 0 0 0.15 0.15 {layer=5}
N -3580 -760 -3610 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -760 0 0 {name=p337 sig_type=std_logic lab=b08_tap1}
N -3540 -760 -3510 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -760 2 0 {name=p338 sig_type=std_logic lab=pvdd}
N -3540 -790 -3540 -815 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -815 3 0 {name=p339 sig_type=std_logic lab=pvdd}
N -3540 -730 -3540 -705 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -705 1 0 {name=p340 sig_type=std_logic lab=b08_c1inv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 -760 0 0 {name=XMc1ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMc1ivn} -3305 -805 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3305 -715 0 0 0.15 0.15 {layer=5}
N -3300 -760 -3330 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -760 0 0 {name=p341 sig_type=std_logic lab=b08_tap1}
N -3260 -760 -3230 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -760 2 0 {name=p342 sig_type=std_logic lab=gnd}
N -3260 -790 -3260 -815 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -815 3 0 {name=p343 sig_type=std_logic lab=b08_c1inv}
N -3260 -730 -3260 -705 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -705 1 0 {name=p344 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3580 -520 0 0 {name=XMc1iv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMc1iv2p} -3585 -565 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3585 -475 0 0 0.15 0.15 {layer=5}
N -3580 -520 -3610 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 -520 0 0 {name=p345 sig_type=std_logic lab=b08_c1inv}
N -3540 -520 -3510 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 -520 2 0 {name=p346 sig_type=std_logic lab=pvdd}
N -3540 -550 -3540 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -575 3 0 {name=p347 sig_type=std_logic lab=pvdd}
N -3540 -490 -3540 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 -465 1 0 {name=p348 sig_type=std_logic lab=b08_comp1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 -520 0 0 {name=XMc1iv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMc1iv2n} -3305 -565 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3305 -475 0 0 0.15 0.15 {layer=5}
N -3300 -520 -3330 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 -520 0 0 {name=p349 sig_type=std_logic lab=b08_c1inv}
N -3260 -520 -3230 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 -520 2 0 {name=p350 sig_type=std_logic lab=gnd}
N -3260 -550 -3260 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -575 3 0 {name=p351 sig_type=std_logic lab=b08_comp1}
N -3260 -490 -3260 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 -465 1 0 {name=p352 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3020 -520 0 0 {name=XMhf1 L=100 W=1.6 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMhf1} -3025 -565 0 0 0.18 0.18 {layer=13}
T {W=1.6 L=100} -3025 -475 0 0 0.15 0.15 {layer=5}
N -3020 -520 -3050 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 -520 0 0 {name=p353 sig_type=std_logic lab=b08_comp1}
N -2980 -520 -2950 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 -520 2 0 {name=p354 sig_type=std_logic lab=gnd}
N -2980 -550 -2980 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 -575 3 0 {name=p355 sig_type=std_logic lab=b08_c1inv}
N -2980 -490 -2980 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 -465 1 0 {name=p356 sig_type=std_logic lab=gnd}
T {COMP1 (tap1)} -3670 -935 0 0 0.22 0.22 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2380 -760 0 0 {name=XMc2ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMc2ivp} -2385 -805 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -2385 -715 0 0 0.15 0.15 {layer=5}
N -2380 -760 -2410 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2410 -760 0 0 {name=p357 sig_type=std_logic lab=b08_tap2}
N -2340 -760 -2310 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2310 -760 2 0 {name=p358 sig_type=std_logic lab=pvdd}
N -2340 -790 -2340 -815 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2340 -815 3 0 {name=p359 sig_type=std_logic lab=pvdd}
N -2340 -730 -2340 -705 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2340 -705 1 0 {name=p360 sig_type=std_logic lab=b08_c2inv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -2100 -760 0 0 {name=XMc2ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMc2ivn} -2105 -805 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -2105 -715 0 0 0.15 0.15 {layer=5}
N -2100 -760 -2130 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2130 -760 0 0 {name=p361 sig_type=std_logic lab=b08_tap2}
N -2060 -760 -2030 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2030 -760 2 0 {name=p362 sig_type=std_logic lab=gnd}
N -2060 -790 -2060 -815 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2060 -815 3 0 {name=p363 sig_type=std_logic lab=b08_c2inv}
N -2060 -730 -2060 -705 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2060 -705 1 0 {name=p364 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2380 -520 0 0 {name=XMc2iv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMc2iv2p} -2385 -565 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -2385 -475 0 0 0.15 0.15 {layer=5}
N -2380 -520 -2410 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2410 -520 0 0 {name=p365 sig_type=std_logic lab=b08_c2inv}
N -2340 -520 -2310 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2310 -520 2 0 {name=p366 sig_type=std_logic lab=pvdd}
N -2340 -550 -2340 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2340 -575 3 0 {name=p367 sig_type=std_logic lab=pvdd}
N -2340 -490 -2340 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2340 -465 1 0 {name=p368 sig_type=std_logic lab=b08_comp2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -2100 -520 0 0 {name=XMc2iv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMc2iv2n} -2105 -565 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -2105 -475 0 0 0.15 0.15 {layer=5}
N -2100 -520 -2130 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2130 -520 0 0 {name=p369 sig_type=std_logic lab=b08_c2inv}
N -2060 -520 -2030 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2030 -520 2 0 {name=p370 sig_type=std_logic lab=gnd}
N -2060 -550 -2060 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2060 -575 3 0 {name=p371 sig_type=std_logic lab=b08_comp2}
N -2060 -490 -2060 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2060 -465 1 0 {name=p372 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -1820 -520 0 0 {name=XMhf2 L=100 W=1.05 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMhf2} -1825 -565 0 0 0.18 0.18 {layer=13}
T {W=1.05 L=100} -1825 -475 0 0 0.15 0.15 {layer=5}
N -1820 -520 -1850 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1850 -520 0 0 {name=p373 sig_type=std_logic lab=b08_comp2}
N -1780 -520 -1750 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1750 -520 2 0 {name=p374 sig_type=std_logic lab=gnd}
N -1780 -550 -1780 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1780 -575 3 0 {name=p375 sig_type=std_logic lab=b08_c2inv}
N -1780 -490 -1780 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1780 -465 1 0 {name=p376 sig_type=std_logic lab=gnd}
T {COMP2 (tap2)} -2470 -935 0 0 0.22 0.22 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1180 -760 0 0 {name=XMc3ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMc3ivp} -1185 -805 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -1185 -715 0 0 0.15 0.15 {layer=5}
N -1180 -760 -1210 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1210 -760 0 0 {name=p377 sig_type=std_logic lab=b08_tap3}
N -1140 -760 -1110 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1110 -760 2 0 {name=p378 sig_type=std_logic lab=pvdd}
N -1140 -790 -1140 -815 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1140 -815 3 0 {name=p379 sig_type=std_logic lab=pvdd}
N -1140 -730 -1140 -705 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1140 -705 1 0 {name=p380 sig_type=std_logic lab=b08_c3inv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -900 -760 0 0 {name=XMc3ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMc3ivn} -905 -805 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -905 -715 0 0 0.15 0.15 {layer=5}
N -900 -760 -930 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -930 -760 0 0 {name=p381 sig_type=std_logic lab=b08_tap3}
N -860 -760 -830 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -830 -760 2 0 {name=p382 sig_type=std_logic lab=gnd}
N -860 -790 -860 -815 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -860 -815 3 0 {name=p383 sig_type=std_logic lab=b08_c3inv}
N -860 -730 -860 -705 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -860 -705 1 0 {name=p384 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1180 -520 0 0 {name=XMc3iv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMc3iv2p} -1185 -565 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -1185 -475 0 0 0.15 0.15 {layer=5}
N -1180 -520 -1210 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1210 -520 0 0 {name=p385 sig_type=std_logic lab=b08_c3inv}
N -1140 -520 -1110 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1110 -520 2 0 {name=p386 sig_type=std_logic lab=pvdd}
N -1140 -550 -1140 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1140 -575 3 0 {name=p387 sig_type=std_logic lab=pvdd}
N -1140 -490 -1140 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1140 -465 1 0 {name=p388 sig_type=std_logic lab=b08_comp3}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -900 -520 0 0 {name=XMc3iv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMc3iv2n} -905 -565 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -905 -475 0 0 0.15 0.15 {layer=5}
N -900 -520 -930 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -930 -520 0 0 {name=p389 sig_type=std_logic lab=b08_c3inv}
N -860 -520 -830 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -830 -520 2 0 {name=p390 sig_type=std_logic lab=gnd}
N -860 -550 -860 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -860 -575 3 0 {name=p391 sig_type=std_logic lab=b08_comp3}
N -860 -490 -860 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -860 -465 1 0 {name=p392 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -620 -520 0 0 {name=XMhf3 L=100 W=0.9 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMhf3} -625 -565 0 0 0.18 0.18 {layer=13}
T {W=0.9 L=100} -625 -475 0 0 0.15 0.15 {layer=5}
N -620 -520 -650 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -650 -520 0 0 {name=p393 sig_type=std_logic lab=b08_comp3}
N -580 -520 -550 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -550 -520 2 0 {name=p394 sig_type=std_logic lab=gnd}
N -580 -550 -580 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -580 -575 3 0 {name=p395 sig_type=std_logic lab=b08_c3inv}
N -580 -490 -580 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -580 -465 1 0 {name=p396 sig_type=std_logic lab=gnd}
T {COMP3 (tap3)} -1270 -935 0 0 0.22 0.22 {layer=4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 20 -760 0 0 {name=XMc4ivp L=2 W=2 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMc4ivp} 15 -805 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} 15 -715 0 0 0.15 0.15 {layer=5}
N 20 -760 -10 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -10 -760 0 0 {name=p397 sig_type=std_logic lab=b08_tap4}
N 60 -760 90 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 90 -760 2 0 {name=p398 sig_type=std_logic lab=pvdd}
N 60 -790 60 -815 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -815 3 0 {name=p399 sig_type=std_logic lab=pvdd}
N 60 -730 60 -705 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -705 1 0 {name=p400 sig_type=std_logic lab=b08_c4inv}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 300 -760 0 0 {name=XMc4ivn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMc4ivn} 295 -805 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} 295 -715 0 0 0.15 0.15 {layer=5}
N 300 -760 270 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 -760 0 0 {name=p401 sig_type=std_logic lab=b08_tap4}
N 340 -760 370 -760 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 370 -760 2 0 {name=p402 sig_type=std_logic lab=gnd}
N 340 -790 340 -815 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -815 3 0 {name=p403 sig_type=std_logic lab=b08_c4inv}
N 340 -730 340 -705 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -705 1 0 {name=p404 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 20 -520 0 0 {name=XMc4iv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMc4iv2p} 15 -565 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} 15 -475 0 0 0.15 0.15 {layer=5}
N 20 -520 -10 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -10 -520 0 0 {name=p405 sig_type=std_logic lab=b08_c4inv}
N 60 -520 90 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 90 -520 2 0 {name=p406 sig_type=std_logic lab=pvdd}
N 60 -550 60 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -575 3 0 {name=p407 sig_type=std_logic lab=pvdd}
N 60 -490 60 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 60 -465 1 0 {name=p408 sig_type=std_logic lab=b08_comp4}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 300 -520 0 0 {name=XMc4iv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMc4iv2n} 295 -565 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} 295 -475 0 0 0.15 0.15 {layer=5}
N 300 -520 270 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 -520 0 0 {name=p409 sig_type=std_logic lab=b08_c4inv}
N 340 -520 370 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 370 -520 2 0 {name=p410 sig_type=std_logic lab=gnd}
N 340 -550 340 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -575 3 0 {name=p411 sig_type=std_logic lab=b08_comp4}
N 340 -490 340 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 -465 1 0 {name=p412 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 580 -520 0 0 {name=XMhf4 L=100 W=0.73 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMhf4} 575 -565 0 0 0.18 0.18 {layer=13}
T {W=0.73 L=100} 575 -475 0 0 0.15 0.15 {layer=5}
N 580 -520 550 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 550 -520 0 0 {name=p413 sig_type=std_logic lab=b08_comp4}
N 620 -520 650 -520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 -520 2 0 {name=p414 sig_type=std_logic lab=gnd}
N 620 -550 620 -575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -575 3 0 {name=p415 sig_type=std_logic lab=b08_c4inv}
N 620 -490 620 -465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -465 1 0 {name=p416 sig_type=std_logic lab=gnd}
T {COMP4 (tap4)} -70 -935 0 0 0.22 0.22 {layer=4}
T {Combinational Logic} -3670 150 0 0 0.28 0.28 {layer=4}
T {comp1b..comp4b inverters} -3670 180 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3580 360 0 0 {name=XMinv1p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMinv1p} -3585 315 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3585 405 0 0 0.15 0.15 {layer=5}
N -3580 360 -3610 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 360 0 0 {name=p417 sig_type=std_logic lab=b08_comp1}
N -3540 360 -3510 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 360 2 0 {name=p418 sig_type=std_logic lab=pvdd}
N -3540 330 -3540 305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 305 3 0 {name=p419 sig_type=std_logic lab=pvdd}
N -3540 390 -3540 415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 415 1 0 {name=p420 sig_type=std_logic lab=b08_comp1b}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 360 0 0 {name=XMinv1n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMinv1n} -3305 315 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3305 405 0 0 0.15 0.15 {layer=5}
N -3300 360 -3330 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 360 0 0 {name=p421 sig_type=std_logic lab=b08_comp1}
N -3260 360 -3230 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 360 2 0 {name=p422 sig_type=std_logic lab=gnd}
N -3260 330 -3260 305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 305 3 0 {name=p423 sig_type=std_logic lab=b08_comp1b}
N -3260 390 -3260 415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 415 1 0 {name=p424 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3030 360 0 0 {name=XMinv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMinv2p} -3035 315 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3035 405 0 0 0.15 0.15 {layer=5}
N -3030 360 -3060 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3060 360 0 0 {name=p425 sig_type=std_logic lab=b08_comp2}
N -2990 360 -2960 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2960 360 2 0 {name=p426 sig_type=std_logic lab=pvdd}
N -2990 330 -2990 305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2990 305 3 0 {name=p427 sig_type=std_logic lab=pvdd}
N -2990 390 -2990 415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2990 415 1 0 {name=p428 sig_type=std_logic lab=b08_comp2b}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -2750 360 0 0 {name=XMinv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMinv2n} -2755 315 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -2755 405 0 0 0.15 0.15 {layer=5}
N -2750 360 -2780 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2780 360 0 0 {name=p429 sig_type=std_logic lab=b08_comp2}
N -2710 360 -2680 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2680 360 2 0 {name=p430 sig_type=std_logic lab=gnd}
N -2710 330 -2710 305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2710 305 3 0 {name=p431 sig_type=std_logic lab=b08_comp2b}
N -2710 390 -2710 415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2710 415 1 0 {name=p432 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2480 360 0 0 {name=XMinv3p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMinv3p} -2485 315 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -2485 405 0 0 0.15 0.15 {layer=5}
N -2480 360 -2510 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2510 360 0 0 {name=p433 sig_type=std_logic lab=b08_comp3}
N -2440 360 -2410 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2410 360 2 0 {name=p434 sig_type=std_logic lab=pvdd}
N -2440 330 -2440 305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2440 305 3 0 {name=p435 sig_type=std_logic lab=pvdd}
N -2440 390 -2440 415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2440 415 1 0 {name=p436 sig_type=std_logic lab=b08_comp3b}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -2200 360 0 0 {name=XMinv3n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMinv3n} -2205 315 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -2205 405 0 0 0.15 0.15 {layer=5}
N -2200 360 -2230 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2230 360 0 0 {name=p437 sig_type=std_logic lab=b08_comp3}
N -2160 360 -2130 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2130 360 2 0 {name=p438 sig_type=std_logic lab=gnd}
N -2160 330 -2160 305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2160 305 3 0 {name=p439 sig_type=std_logic lab=b08_comp3b}
N -2160 390 -2160 415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2160 415 1 0 {name=p440 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1930 360 0 0 {name=XMinv4p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMinv4p} -1935 315 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -1935 405 0 0 0.15 0.15 {layer=5}
N -1930 360 -1960 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1960 360 0 0 {name=p441 sig_type=std_logic lab=b08_comp4}
N -1890 360 -1860 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1860 360 2 0 {name=p442 sig_type=std_logic lab=pvdd}
N -1890 330 -1890 305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1890 305 3 0 {name=p443 sig_type=std_logic lab=pvdd}
N -1890 390 -1890 415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1890 415 1 0 {name=p444 sig_type=std_logic lab=b08_comp4b}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -1650 360 0 0 {name=XMinv4n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMinv4n} -1655 315 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -1655 405 0 0 0.15 0.15 {layer=5}
N -1650 360 -1680 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1680 360 0 0 {name=p445 sig_type=std_logic lab=b08_comp4}
N -1610 360 -1580 360 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1580 360 2 0 {name=p446 sig_type=std_logic lab=gnd}
N -1610 330 -1610 305 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1610 305 3 0 {name=p447 sig_type=std_logic lab=b08_comp4b}
N -1610 390 -1610 415 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1610 415 1 0 {name=p448 sig_type=std_logic lab=gnd}
T {pass_off = BUF(comp1b)} -3670 460 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3580 640 0 0 {name=XMpo_bufp L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMpo_bufp} -3585 595 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3585 685 0 0 0.15 0.15 {layer=5}
N -3580 640 -3610 640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 640 0 0 {name=p449 sig_type=std_logic lab=b08_comp1b}
N -3540 640 -3510 640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 640 2 0 {name=p450 sig_type=std_logic lab=pvdd}
N -3540 610 -3540 585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 585 3 0 {name=p451 sig_type=std_logic lab=pvdd}
N -3540 670 -3540 695 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 695 1 0 {name=p452 sig_type=std_logic lab=pass_off}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 640 0 0 {name=XMpo_bufn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMpo_bufn} -3305 595 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3305 685 0 0 0.15 0.15 {layer=5}
N -3300 640 -3330 640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 640 0 0 {name=p453 sig_type=std_logic lab=b08_comp1b}
N -3260 640 -3230 640 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 640 2 0 {name=p454 sig_type=std_logic lab=gnd}
N -3260 610 -3260 585 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 585 3 0 {name=p455 sig_type=std_logic lab=pass_off}
N -3260 670 -3260 695 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 695 1 0 {name=p456 sig_type=std_logic lab=gnd}
T {bypass_en = (comp1 AND NOT comp2b) OR (comp3 AND NOT comp4b)} -3670 720 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 900 0 0 {name=XMby_n1a L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMby_n1a} -3585 855 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3585 945 0 0 0.15 0.15 {layer=5}
N -3580 900 -3610 900 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 900 0 0 {name=p457 sig_type=std_logic lab=b08_comp1}
N -3540 900 -3510 900 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 900 2 0 {name=p458 sig_type=std_logic lab=gnd}
N -3540 870 -3540 845 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 845 3 0 {name=p459 sig_type=std_logic lab=b08_by_s1}
N -3540 930 -3540 955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 955 1 0 {name=p460 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 900 0 0 {name=XMby_n1b L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMby_n1b} -3305 855 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3305 945 0 0 0.15 0.15 {layer=5}
N -3300 900 -3330 900 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 900 0 0 {name=p461 sig_type=std_logic lab=b08_comp2b}
N -3260 900 -3230 900 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 900 2 0 {name=p462 sig_type=std_logic lab=b08_by_s1}
N -3260 870 -3260 845 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 845 3 0 {name=p463 sig_type=std_logic lab=b08_bypass_enb}
N -3260 930 -3260 955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 955 1 0 {name=p464 sig_type=std_logic lab=b08_by_s1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3020 900 0 0 {name=XMby_n2a L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMby_n2a} -3025 855 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3025 945 0 0 0.15 0.15 {layer=5}
N -3020 900 -3050 900 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 900 0 0 {name=p465 sig_type=std_logic lab=b08_comp3}
N -2980 900 -2950 900 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 900 2 0 {name=p466 sig_type=std_logic lab=gnd}
N -2980 870 -2980 845 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 845 3 0 {name=p467 sig_type=std_logic lab=b08_by_s2}
N -2980 930 -2980 955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 955 1 0 {name=p468 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -2740 900 0 0 {name=XMby_n2b L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMby_n2b} -2745 855 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -2745 945 0 0 0.15 0.15 {layer=5}
N -2740 900 -2770 900 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2770 900 0 0 {name=p469 sig_type=std_logic lab=b08_comp4b}
N -2700 900 -2670 900 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2670 900 2 0 {name=p470 sig_type=std_logic lab=b08_by_s2}
N -2700 870 -2700 845 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 845 3 0 {name=p471 sig_type=std_logic lab=b08_bypass_enb}
N -2700 930 -2700 955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 955 1 0 {name=p472 sig_type=std_logic lab=b08_by_s2}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3580 1140 0 0 {name=XMby_p1a L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMby_p1a} -3585 1095 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3585 1185 0 0 0.15 0.15 {layer=5}
N -3580 1140 -3610 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 1140 0 0 {name=p473 sig_type=std_logic lab=b08_comp1}
N -3540 1140 -3510 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 1140 2 0 {name=p474 sig_type=std_logic lab=pvdd}
N -3540 1110 -3540 1085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 1085 3 0 {name=p475 sig_type=std_logic lab=pvdd}
N -3540 1170 -3540 1195 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 1195 1 0 {name=p476 sig_type=std_logic lab=b08_by_pmid}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3300 1140 0 0 {name=XMby_p1b L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMby_p1b} -3305 1095 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3305 1185 0 0 0.15 0.15 {layer=5}
N -3300 1140 -3330 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 1140 0 0 {name=p477 sig_type=std_logic lab=b08_comp2b}
N -3260 1140 -3230 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 1140 2 0 {name=p478 sig_type=std_logic lab=pvdd}
N -3260 1110 -3260 1085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 1085 3 0 {name=p479 sig_type=std_logic lab=pvdd}
N -3260 1170 -3260 1195 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 1195 1 0 {name=p480 sig_type=std_logic lab=b08_by_pmid}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3020 1140 0 0 {name=XMby_p2a L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMby_p2a} -3025 1095 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3025 1185 0 0 0.15 0.15 {layer=5}
N -3020 1140 -3050 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 1140 0 0 {name=p481 sig_type=std_logic lab=b08_comp3}
N -2980 1140 -2950 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 1140 2 0 {name=p482 sig_type=std_logic lab=b08_by_pmid}
N -2980 1110 -2980 1085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 1085 3 0 {name=p483 sig_type=std_logic lab=b08_by_pmid}
N -2980 1170 -2980 1195 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 1195 1 0 {name=p484 sig_type=std_logic lab=b08_bypass_enb}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2740 1140 0 0 {name=XMby_p2b L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMby_p2b} -2745 1095 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -2745 1185 0 0 0.15 0.15 {layer=5}
N -2740 1140 -2770 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2770 1140 0 0 {name=p485 sig_type=std_logic lab=b08_comp4b}
N -2700 1140 -2670 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2670 1140 2 0 {name=p486 sig_type=std_logic lab=b08_by_pmid}
N -2700 1110 -2700 1085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 1085 3 0 {name=p487 sig_type=std_logic lab=b08_by_pmid}
N -2700 1170 -2700 1195 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 1195 1 0 {name=p488 sig_type=std_logic lab=b08_bypass_enb}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2460 1140 0 0 {name=XMby_outp L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMby_outp} -2465 1095 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -2465 1185 0 0 0.15 0.15 {layer=5}
N -2460 1140 -2490 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2490 1140 0 0 {name=p489 sig_type=std_logic lab=b08_bypass_enb}
N -2420 1140 -2390 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2390 1140 2 0 {name=p490 sig_type=std_logic lab=pvdd}
N -2420 1110 -2420 1085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2420 1085 3 0 {name=p491 sig_type=std_logic lab=pvdd}
N -2420 1170 -2420 1195 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2420 1195 1 0 {name=p492 sig_type=std_logic lab=bypass_en}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -2180 1140 0 0 {name=XMby_outn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMby_outn} -2185 1095 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -2185 1185 0 0 0.15 0.15 {layer=5}
N -2180 1140 -2210 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2210 1140 0 0 {name=p493 sig_type=std_logic lab=b08_bypass_enb}
N -2140 1140 -2110 1140 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2110 1140 2 0 {name=p494 sig_type=std_logic lab=gnd}
N -2140 1110 -2140 1085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2140 1085 3 0 {name=p495 sig_type=std_logic lab=bypass_en}
N -2140 1170 -2140 1195 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2140 1195 1 0 {name=p496 sig_type=std_logic lab=gnd}
T {mc_ea_en = (comp2 AND NOT comp3b) OR comp4} -3670 1250 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 1440 0 0 {name=XMea_n1a L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMea_n1a} -3585 1395 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3585 1485 0 0 0.15 0.15 {layer=5}
N -3580 1440 -3610 1440 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 1440 0 0 {name=p497 sig_type=std_logic lab=b08_comp2}
N -3540 1440 -3510 1440 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 1440 2 0 {name=p498 sig_type=std_logic lab=gnd}
N -3540 1410 -3540 1385 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 1385 3 0 {name=p499 sig_type=std_logic lab=b08_ea_s1}
N -3540 1470 -3540 1495 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 1495 1 0 {name=p500 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 1440 0 0 {name=XMea_n1b L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMea_n1b} -3305 1395 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3305 1485 0 0 0.15 0.15 {layer=5}
N -3300 1440 -3330 1440 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 1440 0 0 {name=p501 sig_type=std_logic lab=b08_comp3b}
N -3260 1440 -3230 1440 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 1440 2 0 {name=p502 sig_type=std_logic lab=b08_ea_s1}
N -3260 1410 -3260 1385 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 1385 3 0 {name=p503 sig_type=std_logic lab=b08_ea_enb}
N -3260 1470 -3260 1495 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 1495 1 0 {name=p504 sig_type=std_logic lab=b08_ea_s1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3020 1440 0 0 {name=XMea_n2 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMea_n2} -3025 1395 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3025 1485 0 0 0.15 0.15 {layer=5}
N -3020 1440 -3050 1440 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 1440 0 0 {name=p505 sig_type=std_logic lab=b08_comp4}
N -2980 1440 -2950 1440 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 1440 2 0 {name=p506 sig_type=std_logic lab=gnd}
N -2980 1410 -2980 1385 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 1385 3 0 {name=p507 sig_type=std_logic lab=b08_ea_enb}
N -2980 1470 -2980 1495 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 1495 1 0 {name=p508 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3580 1680 0 0 {name=XMea_p1a L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMea_p1a} -3585 1635 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3585 1725 0 0 0.15 0.15 {layer=5}
N -3580 1680 -3610 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 1680 0 0 {name=p509 sig_type=std_logic lab=b08_comp2}
N -3540 1680 -3510 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 1680 2 0 {name=p510 sig_type=std_logic lab=pvdd}
N -3540 1650 -3540 1625 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 1625 3 0 {name=p511 sig_type=std_logic lab=pvdd}
N -3540 1710 -3540 1735 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 1735 1 0 {name=p512 sig_type=std_logic lab=b08_ea_pmid}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3300 1680 0 0 {name=XMea_p1b L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMea_p1b} -3305 1635 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3305 1725 0 0 0.15 0.15 {layer=5}
N -3300 1680 -3330 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 1680 0 0 {name=p513 sig_type=std_logic lab=b08_comp3b}
N -3260 1680 -3230 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 1680 2 0 {name=p514 sig_type=std_logic lab=pvdd}
N -3260 1650 -3260 1625 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 1625 3 0 {name=p515 sig_type=std_logic lab=pvdd}
N -3260 1710 -3260 1735 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 1735 1 0 {name=p516 sig_type=std_logic lab=b08_ea_pmid}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3020 1680 0 0 {name=XMea_p2 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMea_p2} -3025 1635 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3025 1725 0 0 0.15 0.15 {layer=5}
N -3020 1680 -3050 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 1680 0 0 {name=p517 sig_type=std_logic lab=b08_comp4}
N -2980 1680 -2950 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 1680 2 0 {name=p518 sig_type=std_logic lab=b08_ea_pmid}
N -2980 1650 -2980 1625 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 1625 3 0 {name=p519 sig_type=std_logic lab=b08_ea_pmid}
N -2980 1710 -2980 1735 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 1735 1 0 {name=p520 sig_type=std_logic lab=b08_ea_enb}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2740 1680 0 0 {name=XMea_outp L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMea_outp} -2745 1635 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -2745 1725 0 0 0.15 0.15 {layer=5}
N -2740 1680 -2770 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2770 1680 0 0 {name=p521 sig_type=std_logic lab=b08_ea_enb}
N -2700 1680 -2670 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2670 1680 2 0 {name=p522 sig_type=std_logic lab=pvdd}
N -2700 1650 -2700 1625 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 1625 3 0 {name=p523 sig_type=std_logic lab=pvdd}
N -2700 1710 -2700 1735 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 1735 1 0 {name=p524 sig_type=std_logic lab=mc_ea_en}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -2460 1680 0 0 {name=XMea_outn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMea_outn} -2465 1635 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -2465 1725 0 0 0.15 0.15 {layer=5}
N -2460 1680 -2490 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2490 1680 0 0 {name=p525 sig_type=std_logic lab=b08_ea_enb}
N -2420 1680 -2390 1680 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2390 1680 2 0 {name=p526 sig_type=std_logic lab=gnd}
N -2420 1650 -2420 1625 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2420 1625 3 0 {name=p527 sig_type=std_logic lab=mc_ea_en}
N -2420 1710 -2420 1735 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2420 1735 1 0 {name=p528 sig_type=std_logic lab=gnd}
T {ref_sel = comp1 AND NOT comp3b} -3670 1790 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3580 1980 0 0 {name=XMrs_n1 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMrs_n1} -3585 1935 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3585 2025 0 0 0.15 0.15 {layer=5}
N -3580 1980 -3610 1980 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 1980 0 0 {name=p529 sig_type=std_logic lab=b08_comp1}
N -3540 1980 -3510 1980 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 1980 2 0 {name=p530 sig_type=std_logic lab=gnd}
N -3540 1950 -3540 1925 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 1925 3 0 {name=p531 sig_type=std_logic lab=b08_rs_s1}
N -3540 2010 -3540 2035 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 2035 1 0 {name=p532 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 1980 0 0 {name=XMrs_n2 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMrs_n2} -3305 1935 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3305 2025 0 0 0.15 0.15 {layer=5}
N -3300 1980 -3330 1980 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 1980 0 0 {name=p533 sig_type=std_logic lab=b08_comp3b}
N -3260 1980 -3230 1980 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 1980 2 0 {name=p534 sig_type=std_logic lab=b08_rs_s1}
N -3260 1950 -3260 1925 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 1925 3 0 {name=p535 sig_type=std_logic lab=b08_ref_selb}
N -3260 2010 -3260 2035 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 2035 1 0 {name=p536 sig_type=std_logic lab=b08_rs_s1}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3020 1980 0 0 {name=XMrs_p1 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMrs_p1} -3025 1935 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3025 2025 0 0 0.15 0.15 {layer=5}
N -3020 1980 -3050 1980 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3050 1980 0 0 {name=p537 sig_type=std_logic lab=b08_comp1}
N -2980 1980 -2950 1980 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2950 1980 2 0 {name=p538 sig_type=std_logic lab=pvdd}
N -2980 1950 -2980 1925 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 1925 3 0 {name=p539 sig_type=std_logic lab=pvdd}
N -2980 2010 -2980 2035 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2980 2035 1 0 {name=p540 sig_type=std_logic lab=b08_ref_selb}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -2740 1980 0 0 {name=XMrs_p2 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMrs_p2} -2745 1935 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -2745 2025 0 0 0.15 0.15 {layer=5}
N -2740 1980 -2770 1980 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2770 1980 0 0 {name=p541 sig_type=std_logic lab=b08_comp3b}
N -2700 1980 -2670 1980 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2670 1980 2 0 {name=p542 sig_type=std_logic lab=pvdd}
N -2700 1950 -2700 1925 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 1925 3 0 {name=p543 sig_type=std_logic lab=pvdd}
N -2700 2010 -2700 2035 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -2700 2035 1 0 {name=p544 sig_type=std_logic lab=b08_ref_selb}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -3580 2220 0 0 {name=XMrs_outp L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMrs_outp} -3585 2175 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -3585 2265 0 0 0.15 0.15 {layer=5}
N -3580 2220 -3610 2220 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3610 2220 0 0 {name=p545 sig_type=std_logic lab=b08_ref_selb}
N -3540 2220 -3510 2220 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3510 2220 2 0 {name=p546 sig_type=std_logic lab=pvdd}
N -3540 2190 -3540 2165 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 2165 3 0 {name=p547 sig_type=std_logic lab=pvdd}
N -3540 2250 -3540 2275 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3540 2275 1 0 {name=p548 sig_type=std_logic lab=ref_sel}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -3300 2220 0 0 {name=XMrs_outn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMrs_outn} -3305 2175 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -3305 2265 0 0 0.15 0.15 {layer=5}
N -3300 2220 -3330 2220 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3330 2220 0 0 {name=p549 sig_type=std_logic lab=b08_ref_selb}
N -3260 2220 -3230 2220 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3230 2220 2 0 {name=p550 sig_type=std_logic lab=gnd}
N -3260 2190 -3260 2165 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 2165 3 0 {name=p551 sig_type=std_logic lab=ref_sel}
N -3260 2250 -3260 2275 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -3260 2275 1 0 {name=p552 sig_type=std_logic lab=gnd}
T {uvov_en = BUF(comp4)} -1200 2330 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1080 2520 0 0 {name=XMuv_p1 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMuv_p1} -1085 2475 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -1085 2565 0 0 0.15 0.15 {layer=5}
N -1080 2520 -1110 2520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1110 2520 0 0 {name=p553 sig_type=std_logic lab=b08_comp4}
N -1040 2520 -1010 2520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1010 2520 2 0 {name=p554 sig_type=std_logic lab=pvdd}
N -1040 2490 -1040 2465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1040 2465 3 0 {name=p555 sig_type=std_logic lab=pvdd}
N -1040 2550 -1040 2575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1040 2575 1 0 {name=p556 sig_type=std_logic lab=b08_uvov_enb}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -800 2520 0 0 {name=XMuv_n1 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMuv_n1} -805 2475 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -805 2565 0 0 0.15 0.15 {layer=5}
N -800 2520 -830 2520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -830 2520 0 0 {name=p557 sig_type=std_logic lab=b08_comp4}
N -760 2520 -730 2520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -730 2520 2 0 {name=p558 sig_type=std_logic lab=gnd}
N -760 2490 -760 2465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -760 2465 3 0 {name=p559 sig_type=std_logic lab=b08_uvov_enb}
N -760 2550 -760 2575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -760 2575 1 0 {name=p560 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -520 2520 0 0 {name=XMuv_p2 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMuv_p2} -525 2475 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -525 2565 0 0 0.15 0.15 {layer=5}
N -520 2520 -550 2520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -550 2520 0 0 {name=p561 sig_type=std_logic lab=b08_uvov_enb}
N -480 2520 -450 2520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -450 2520 2 0 {name=p562 sig_type=std_logic lab=pvdd}
N -480 2490 -480 2465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -480 2465 3 0 {name=p563 sig_type=std_logic lab=pvdd}
N -480 2550 -480 2575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -480 2575 1 0 {name=p564 sig_type=std_logic lab=uvov_en}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -240 2520 0 0 {name=XMuv_n2 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMuv_n2} -245 2475 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -245 2565 0 0 0.15 0.15 {layer=5}
N -240 2520 -270 2520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -270 2520 0 0 {name=p565 sig_type=std_logic lab=b08_uvov_enb}
N -200 2520 -170 2520 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -170 2520 2 0 {name=p566 sig_type=std_logic lab=gnd}
N -200 2490 -200 2465 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 2465 3 0 {name=p567 sig_type=std_logic lab=uvov_en}
N -200 2550 -200 2575 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 2575 1 0 {name=p568 sig_type=std_logic lab=gnd}
T {ilim_en = BUF(comp4)} -1200 2610 0 0 0.18 0.18 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -1080 3030 0 0 {name=XMil_p1 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMil_p1} -1085 2985 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -1085 3075 0 0 0.15 0.15 {layer=5}
N -1080 3030 -1110 3030 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1110 3030 0 0 {name=p569 sig_type=std_logic lab=b08_comp4}
N -1040 3030 -1010 3030 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1010 3030 2 0 {name=p570 sig_type=std_logic lab=pvdd}
N -1040 3000 -1040 2975 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1040 2975 3 0 {name=p571 sig_type=std_logic lab=pvdd}
N -1040 3060 -1040 3085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -1040 3085 1 0 {name=p572 sig_type=std_logic lab=b08_ilim_enb}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -800 3030 0 0 {name=XMil_n1 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMil_n1} -805 2985 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -805 3075 0 0 0.15 0.15 {layer=5}
N -800 3030 -830 3030 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -830 3030 0 0 {name=p573 sig_type=std_logic lab=b08_comp4}
N -760 3030 -730 3030 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -730 3030 2 0 {name=p574 sig_type=std_logic lab=gnd}
N -760 3000 -760 2975 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -760 2975 3 0 {name=p575 sig_type=std_logic lab=b08_ilim_enb}
N -760 3060 -760 3085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -760 3085 1 0 {name=p576 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -520 3030 0 0 {name=XMil_p2 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMil_p2} -525 2985 0 0 0.18 0.18 {layer=13}
T {W=4 L=2} -525 3075 0 0 0.15 0.15 {layer=5}
N -520 3030 -550 3030 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -550 3030 0 0 {name=p577 sig_type=std_logic lab=b08_ilim_enb}
N -480 3030 -450 3030 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -450 3030 2 0 {name=p578 sig_type=std_logic lab=pvdd}
N -480 3000 -480 2975 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -480 2975 3 0 {name=p579 sig_type=std_logic lab=pvdd}
N -480 3060 -480 3085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -480 3085 1 0 {name=p580 sig_type=std_logic lab=ilim_en}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -240 3030 0 0 {name=XMil_n2 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMil_n2} -245 2985 0 0 0.18 0.18 {layer=13}
T {W=2 L=2} -245 3075 0 0 0.15 0.15 {layer=5}
N -240 3030 -270 3030 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -270 3030 0 0 {name=p581 sig_type=std_logic lab=b08_ilim_enb}
N -200 3030 -170 3030 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -170 3030 2 0 {name=p582 sig_type=std_logic lab=gnd}
N -200 3000 -200 2975 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 2975 3 0 {name=p583 sig_type=std_logic lab=ilim_en}
N -200 3060 -200 3085 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 3085 1 0 {name=p584 sig_type=std_logic lab=gnd}

* ============================================================
* Section 10: Startup Circuit (Block 09)
* ============================================================
L 4 500 -3100 3100 -3100 {dash=5}
L 4 3100 -3100 3100 -1700 {dash=5}
L 4 3100 -1700 500 -1700 {dash=5}
L 4 500 -1700 500 -3100 {dash=5}
T {Section 10: Startup Circuit (Block 09)} 515 -3085 0 0 0.4 0.4 {layer=4}
T {CG NFET level shifter + bootstrap + threshold detector} 515 -3055 0 0 0.22 0.22 {layer=13}
C {/usr/share/xschem/xschem_library/devices/res.sym} 600 -2910 0 0 {name=Rlb1 value=200k}
T {Rlb1} 620 -2935 0 0 0.17 0.17 {layer=13}
T {200k} 620 -2900 0 0 0.15 0.15 {layer=5}
N 600 -2940 600 -2965 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -2965 3 0 {name=p585 sig_type=std_logic lab=bvdd}
N 600 -2880 600 -2855 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -2855 1 0 {name=p586 sig_type=std_logic lab=b09_ls_bias}
C {/usr/share/xschem/xschem_library/devices/res.sym} 800 -2910 0 0 {name=Rlb2 value=500k}
T {Rlb2} 820 -2935 0 0 0.17 0.17 {layer=13}
T {500k} 820 -2900 0 0 0.15 0.15 {layer=5}
N 800 -2940 800 -2965 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -2965 3 0 {name=p587 sig_type=std_logic lab=b09_ls_bias}
N 800 -2880 800 -2855 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -2855 1 0 {name=p588 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1180 -2910 0 0 {name=XMN_cg L=4 W=1.2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN_cg} 1175 -2955 0 0 0.18 0.18 {layer=13}
T {W=1.2 L=4} 1175 -2865 0 0 0.15 0.15 {layer=5}
N 1180 -2910 1150 -2910 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -2910 0 0 {name=p589 sig_type=std_logic lab=b09_ls_bias}
N 1220 -2910 1250 -2910 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 -2910 2 0 {name=p590 sig_type=std_logic lab=gnd}
N 1220 -2940 1220 -2965 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -2965 3 0 {name=p591 sig_type=std_logic lab=ea_out}
N 1220 -2880 1220 -2855 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -2855 1 0 {name=p592 sig_type=std_logic lab=gate}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 1200 -2910 0 0 {name=XR_load W=1 L=19 model=res_xhigh_po spiceprefix=X}
T {XR_load} 1220 -2935 0 0 0.17 0.17 {layer=13}
T {W=1 L=19} 1220 -2895 0 0 0.14 0.14 {layer=5}
N 1200 -2940 1200 -2965 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1200 -2965 3 0 {name=p593 sig_type=std_logic lab=bvdd}
N 1200 -2880 1200 -2855 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1200 -2855 1 0 {name=p594 sig_type=std_logic lab=gate}
N 1180 -2910 1160 -2910 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1160 -2910 0 0 {name=p595 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/res.sym} 1400 -2910 0 0 {name=Ren value=100}
T {Ren} 1420 -2935 0 0 0.17 0.17 {layer=13}
T {100} 1420 -2900 0 0 0.15 0.15 {layer=5}
N 1400 -2940 1400 -2965 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -2965 3 0 {name=p596 sig_type=std_logic lab=bvdd}
N 1400 -2880 1400 -2855 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1400 -2855 1 0 {name=p597 sig_type=std_logic lab=ea_en}
T {startup_done detector} 530 -2720 0 0 0.2 0.2 {layer=13}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 600 -2670 0 0 {name=XR_top_sd W=2 L=788 model=res_xhigh_po spiceprefix=X}
T {XR_top_sd} 620 -2695 0 0 0.17 0.17 {layer=13}
T {W=2 L=788} 620 -2655 0 0 0.14 0.14 {layer=5}
N 600 -2700 600 -2725 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -2725 3 0 {name=p598 sig_type=std_logic lab=pvdd}
N 600 -2640 600 -2615 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -2615 1 0 {name=p599 sig_type=std_logic lab=b09_sense_mid}
N 580 -2670 560 -2670 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 560 -2670 0 0 {name=p600 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 800 -2670 0 0 {name=XR_bot_sd W=2 L=212 model=res_xhigh_po spiceprefix=X}
T {XR_bot_sd} 820 -2695 0 0 0.17 0.17 {layer=13}
T {W=2 L=212} 820 -2655 0 0 0.14 0.14 {layer=5}
N 800 -2700 800 -2725 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -2725 3 0 {name=p601 sig_type=std_logic lab=b09_sense_mid}
N 800 -2640 800 -2615 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 -2615 1 0 {name=p602 sig_type=std_logic lab=gnd}
N 780 -2670 760 -2670 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 760 -2670 0 0 {name=p603 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1180 -2670 0 0 {name=XMN_det L=1 W=4 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN_det} 1175 -2715 0 0 0.18 0.18 {layer=13}
T {W=4 L=1} 1175 -2625 0 0 0.15 0.15 {layer=5}
N 1180 -2670 1150 -2670 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1150 -2670 0 0 {name=p604 sig_type=std_logic lab=b09_sense_mid}
N 1220 -2670 1250 -2670 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1250 -2670 2 0 {name=p605 sig_type=std_logic lab=gnd}
N 1220 -2700 1220 -2725 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -2725 3 0 {name=p606 sig_type=std_logic lab=b09_det_n}
N 1220 -2640 1220 -2615 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -2615 1 0 {name=p607 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/res_xhigh_po.sym} 1200 -2670 0 0 {name=XR_pu W=1 L=2000 model=res_xhigh_po spiceprefix=X}
T {XR_pu} 1220 -2695 0 0 0.17 0.17 {layer=13}
T {W=1 L=2000} 1220 -2655 0 0 0.14 0.14 {layer=5}
N 1200 -2700 1200 -2725 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1200 -2725 3 0 {name=p608 sig_type=std_logic lab=bvdd}
N 1200 -2640 1200 -2615 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1200 -2615 1 0 {name=p609 sig_type=std_logic lab=b09_det_n}
N 1180 -2670 1160 -2670 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1160 -2670 0 0 {name=p610 sig_type=std_logic lab=gnd}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 620 -2430 0 0 {name=XMP_inv1 L=1 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
T {XMP_inv1} 615 -2475 0 0 0.18 0.18 {layer=13}
T {W=4 L=1} 615 -2385 0 0 0.15 0.15 {layer=5}
N 620 -2430 590 -2430 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 590 -2430 0 0 {name=p611 sig_type=std_logic lab=b09_det_n}
N 660 -2430 690 -2430 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 690 -2430 2 0 {name=p612 sig_type=std_logic lab=bvdd}
N 660 -2460 660 -2485 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 660 -2485 3 0 {name=p613 sig_type=std_logic lab=bvdd}
N 660 -2400 660 -2375 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 660 -2375 1 0 {name=p614 sig_type=std_logic lab=startup_done}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 900 -2430 0 0 {name=XMN_inv1 L=1 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
T {XMN_inv1} 895 -2475 0 0 0.18 0.18 {layer=13}
T {W=2 L=1} 895 -2385 0 0 0.15 0.15 {layer=5}
N 900 -2430 870 -2430 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 870 -2430 0 0 {name=p615 sig_type=std_logic lab=b09_det_n}
N 940 -2430 970 -2430 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 970 -2430 2 0 {name=p616 sig_type=std_logic lab=gnd}
N 940 -2460 940 -2485 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -2485 3 0 {name=p617 sig_type=std_logic lab=startup_done}
N 940 -2400 940 -2375 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 940 -2375 1 0 {name=p618 sig_type=std_logic lab=gnd}

* ============================================================
* TOP-LEVEL PASSIVES
* ============================================================
L 13 3500 -3200 4300 -3200 {dash=5}
L 13 4300 -3200 4300 -2500 {dash=5}
L 13 4300 -2500 3500 -2500 {dash=5}
L 13 3500 -2500 3500 -3200 {dash=5}
T {Top-Level Passives} 3515 -3185 0 0 0.3 0.3 {layer=13}
T {Soft-start + Output cap} 3515 -3155 0 0 0.2 0.2 {layer=13}
C {/usr/share/xschem/xschem_library/devices/res.sym} 3600 -3010 0 0 {name=Rss value=200k}
T {Rss} 3620 -3035 0 0 0.17 0.17 {layer=13}
T {200k} 3620 -3000 0 0 0.15 0.15 {layer=5}
N 3600 -3040 3600 -3065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 3600 -3065 3 0 {name=p619 sig_type=std_logic lab=avbg}
N 3600 -2980 3600 -2955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 3600 -2955 1 0 {name=p620 sig_type=std_logic lab=vref_ss}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 3800 -3010 0 0 {name=Css value=30n}
T {Css} 3820 -3035 0 0 0.17 0.17 {layer=13}
T {30n} 3820 -3000 0 0 0.15 0.15 {layer=5}
N 3800 -3040 3800 -3065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 3800 -3065 3 0 {name=p621 sig_type=std_logic lab=vref_ss}
N 3800 -2980 3800 -2955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 3800 -2955 1 0 {name=p622 sig_type=std_logic lab=gnd}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 4000 -3010 0 0 {name=Cload value=200p}
T {Cload} 4020 -3035 0 0 0.17 0.17 {layer=13}
T {200p} 4020 -3000 0 0 0.15 0.15 {layer=5}
N 4000 -3040 4000 -3065 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4000 -3065 3 0 {name=p623 sig_type=std_logic lab=pvdd}
N 4000 -2980 4000 -2955 {}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 4000 -2955 1 0 {name=p624 sig_type=std_logic lab=gnd}

* INTER-BLOCK NET ANNOTATIONS
T {Key Inter-Block Nets:} -3700 4400 0 0 0.35 0.35 {layer=4}
T {bvdd — Battery supply input (5.4-10.5V) — to Pass Device, Current Limiter, Mode Control, Startup} -3700 4435 0 0 0.2 0.2 {layer=13}
T {pvdd — Regulated 5.0V output — from Pass Device drain, to Feedback, Compensation, UV/OV, Zener} -3700 4460 0 0 0.2 0.2 {layer=13}
T {gnd — Ground — shared by all blocks} -3700 4485 0 0 0.2 0.2 {layer=13}
T {gate — Pass device gate (BVDD domain) — driven by Startup CG LS, sensed by Current Limiter} -3700 4510 0 0 0.2 0.2 {layer=13}
T {ea_out — Error amp output (PVDD domain) — to Startup CG LS input, and Compensation} -3700 4535 0 0 0.2 0.2 {layer=13}
T {vfb — Feedback voltage (~1.226V) — from Feedback divider to Error Amp (-) input} -3700 4560 0 0 0.2 0.2 {layer=13}
T {vref_ss — Soft-started reference — avbg through RC filter to Error Amp (+) input} -3700 4585 0 0 0.2 0.2 {layer=13}
T {ea_en — Error amp enable — from Startup (always BVDD) to Error Amp en pin} -3700 4610 0 0 0.2 0.2 {layer=13}
T {uvov_en — UV/OV enable — from Mode Control to UV and OV comparators} -3700 4635 0 0 0.2 0.2 {layer=13}
T {avbg — Bandgap reference (1.226V) — to UV/OV refs, Startup, Soft-start} -3700 4660 0 0 0.2 0.2 {layer=13}
T {ibias — 1uA bias current — to Error Amp bias mirror} -3700 4685 0 0 0.2 0.2 {layer=13}
