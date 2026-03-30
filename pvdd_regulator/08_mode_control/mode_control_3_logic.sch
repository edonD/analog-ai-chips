v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {LOGIC — Mode Decode & Output Drivers} -300 -1400 0 0 0.85 0.85 {layer=4}
T {Block 08 — Mode Control — Sub-block 3 of 3} -300 -1330 0 0 0.45 0.45 {layer=8}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -300 -1295 0 0 0.3 0.3 {}
T {42 MOSFETs: 4 inverters + pass_off buffer + AOI22 + AOI21 + NAND2 + 2x double-buffer} -300 -1265 0 0 0.28 0.28 {layer=13}
T {All logic at L=2um, PFET W=4um, NFET W=2um (5V thick-oxide gate)} -300 -1235 0 0 0.28 0.28 {layer=5}

C {/usr/share/xschem/xschem_library/devices/title.sym} -300 1800 0 0 {name=l1 author="Block 08 Sub-3: Logic -- Analog AI Chips PVDD LDO Regulator"}

* PORT PINS (signals crossing between sub-schematics)
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -1120 0 0 {name=p1 lab=comp1}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -1090 0 0 {name=p2 lab=comp2}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -1060 0 0 {name=p3 lab=comp3}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -1030 0 0 {name=p4 lab=comp4}
C {/usr/share/xschem/xschem_library/devices/ipin.sym} -300 -1000 0 0 {name=p5 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -1120 0 0 {name=p6 lab=bypass_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -1090 0 0 {name=p7 lab=ea_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -1060 0 0 {name=p8 lab=ref_sel}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -1030 0 0 {name=p9 lab=uvov_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -1000 0 0 {name=p10 lab=ilim_en}
C {/usr/share/xschem/xschem_library/devices/opin.sym} -180 -970 0 0 {name=p11 lab=pass_off}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -180 -940 0 0 {name=p12 lab=gnd}

* ================================================================
* SECTION 1: Comparator Inverters comp1b..comp4b + pass_off buffer
* 4 inverters (8 FETs) + 1 buffer (2 FETs) = 10 FETs
* ================================================================

T {COMPARATOR INVERTERS + PASS_OFF BUFFER} -100 -950 0 0 0.5 0.5 {layer=4}
T {comp_b = !comp  |  pass_off = !!comp1b = !comp1} -100 -910 0 0 0.28 0.28 {layer=5}

T {XMinv1p} -80 -850 0 0 0.22 0.22 {layer=13}
T {P:4/2} -80 -833 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -20 -800 0 0 {name=XMinv1p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 0 -830 0 -880 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -880 2 0 {name=l1a sig_type=std_logic lab=pvdd}
N 0 -770 0 -730 {lab=comp1b}
N -40 -800 -120 -800 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -120 -800 0 0 {name=l1c sig_type=std_logic lab=comp1}
N 0 -800 20 -800 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -800 2 0 {name=l1d sig_type=std_logic lab=pvdd}
T {XMinv1n} -80 -670 0 0 0.22 0.22 {layer=13}
T {N:2/2} -80 -653 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -20 -700 0 0 {name=XMinv1n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 0 -730 0 -730 {lab=comp1b}
N 0 -670 0 -620 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 -620 0 0 {name=lg3 lab=GND}
N -40 -700 -120 -700 {lab=comp1}
N -120 -700 -120 -800 {lab=comp1}
N 0 -700 20 -700 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -700 2 0 {name=l2d sig_type=std_logic lab=gnd}
T {comp1b} 10 -740 0 0 0.28 0.28 {layer=8}

T {XMinv2p} 220 -850 0 0 0.22 0.22 {layer=13}
T {P:4/2} 220 -833 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 280 -800 0 0 {name=XMinv2p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 300 -830 300 -880 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -880 2 0 {name=l4a sig_type=std_logic lab=pvdd}
N 300 -770 300 -730 {lab=comp2b}
N 260 -800 180 -800 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 180 -800 0 0 {name=l4c sig_type=std_logic lab=comp2}
N 300 -800 320 -800 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 320 -800 2 0 {name=l4d sig_type=std_logic lab=pvdd}
T {XMinv2n} 220 -670 0 0 0.22 0.22 {layer=13}
T {N:2/2} 220 -653 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 280 -700 0 0 {name=XMinv2n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 300 -730 300 -730 {lab=comp2b}
N 300 -670 300 -620 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 300 -620 0 0 {name=lg6 lab=GND}
N 260 -700 180 -700 {lab=comp2}
N 180 -700 180 -800 {lab=comp2}
N 300 -700 320 -700 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 320 -700 2 0 {name=l5d sig_type=std_logic lab=gnd}
T {comp2b} 310 -740 0 0 0.28 0.28 {layer=8}

T {XMinv3p} 520 -850 0 0 0.22 0.22 {layer=13}
T {P:4/2} 520 -833 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 580 -800 0 0 {name=XMinv3p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 600 -830 600 -880 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 -880 2 0 {name=l7a sig_type=std_logic lab=pvdd}
N 600 -770 600 -730 {lab=comp3b}
N 560 -800 480 -800 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 480 -800 0 0 {name=l7c sig_type=std_logic lab=comp3}
N 600 -800 620 -800 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -800 2 0 {name=l7d sig_type=std_logic lab=pvdd}
T {XMinv3n} 520 -670 0 0 0.22 0.22 {layer=13}
T {N:2/2} 520 -653 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 580 -700 0 0 {name=XMinv3n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 600 -730 600 -730 {lab=comp3b}
N 600 -670 600 -620 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 600 -620 0 0 {name=lg9 lab=GND}
N 560 -700 480 -700 {lab=comp3}
N 480 -700 480 -800 {lab=comp3}
N 600 -700 620 -700 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 -700 2 0 {name=l8d sig_type=std_logic lab=gnd}
T {comp3b} 610 -740 0 0 0.28 0.28 {layer=8}

T {XMinv4p} 820 -850 0 0 0.22 0.22 {layer=13}
T {P:4/2} 820 -833 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 880 -800 0 0 {name=XMinv4p L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 900 -830 900 -880 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 900 -880 2 0 {name=l10a sig_type=std_logic lab=pvdd}
N 900 -770 900 -730 {lab=comp4b}
N 860 -800 780 -800 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -800 0 0 {name=l10c sig_type=std_logic lab=comp4}
N 900 -800 920 -800 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -800 2 0 {name=l10d sig_type=std_logic lab=pvdd}
T {XMinv4n} 820 -670 0 0 0.22 0.22 {layer=13}
T {N:2/2} 820 -653 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 880 -700 0 0 {name=XMinv4n L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 900 -730 900 -730 {lab=comp4b}
N 900 -670 900 -620 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 900 -620 0 0 {name=lg12 lab=GND}
N 860 -700 780 -700 {lab=comp4}
N 780 -700 780 -800 {lab=comp4}
N 900 -700 920 -700 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 -700 2 0 {name=l11d sig_type=std_logic lab=gnd}
T {comp4b} 910 -740 0 0 0.28 0.28 {layer=8}

T {PASS_OFF} 1150 -950 0 0 0.4 0.4 {layer=4}
T {pass_off = !comp1b = comp1  (HIGH when BVDD<TH1)} 1150 -915 0 0 0.22 0.22 {layer=7}
T {XMpo_bufp} 1140 -850 0 0 0.22 0.22 {layer=13}
T {P:4/2} 1140 -833 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1200 -800 0 0 {name=XMpo_bufp L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 1220 -830 1220 -880 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1220 -880 2 0 {name=l13a sig_type=std_logic lab=pvdd}
N 1220 -770 1220 -730 {lab=pass_off}
N 1180 -800 1100 -800 {lab=comp1b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1100 -800 0 0 {name=l13c sig_type=std_logic lab=comp1b}
N 1220 -800 1240 -800 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1240 -800 2 0 {name=l13d sig_type=std_logic lab=pvdd}
T {XMpo_bufn} 1140 -670 0 0 0.22 0.22 {layer=13}
T {N:2/2} 1140 -653 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1200 -700 0 0 {name=XMpo_bufn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 1220 -730 1220 -730 {lab=pass_off}
N 1220 -670 1220 -620 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1220 -620 0 0 {name=lg15 lab=GND}
N 1180 -700 1100 -700 {lab=comp1b}
N 1100 -700 1100 -800 {lab=comp1b}
N 1220 -700 1240 -700 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1240 -700 2 0 {name=l14d sig_type=std_logic lab=gnd}
T {pass_off} 1230 -740 0 0 0.28 0.28 {layer=8}

* ================================================================
* SECTION 2: bypass_en — AOI22 + output INV (10 FETs)
* bypass_enb = !((comp1·!comp2) + (comp3·!comp4))
* bypass_en = (comp1·!comp2) + (comp3·!comp4)  [AOI22 + INV]
* PMOS: 2 series pairs in parallel  |  NMOS: 2 series stacks in parallel
* ================================================================

T {BYPASS_EN — AOI22 + INV} -100 -530 0 0 0.5 0.5 {layer=4}
T {bypass_en = (comp1 · comp2b) + (comp3 · comp4b) = (comp1·!comp2)+(comp3·!comp4)} -100 -495 0 0 0.28 0.28 {layer=5}

T {PMOS pull-up (series pairs)} -80 -440 0 0 0.25 0.25 {layer=7}
T {XMby_p1a} -80 -430 0 0 0.22 0.22 {layer=13}
T {P:4/2} -80 -413 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -20 -380 0 0 {name=XMby_p1a L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 0 -410 0 -460 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -460 2 0 {name=l16a sig_type=std_logic lab=pvdd}
N 0 -350 0 -300 {lab=by_pmid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -300 2 0 {name=l16b sig_type=std_logic lab=by_pmid}
N -40 -380 -100 -380 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -380 0 0 {name=l16c sig_type=std_logic lab=comp1}
N 0 -380 20 -380 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -380 2 0 {name=l16d sig_type=std_logic lab=pvdd}

T {XMby_p1b} 170 -430 0 0 0.22 0.22 {layer=13}
T {P:4/2} 170 -413 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 230 -380 0 0 {name=XMby_p1b L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 250 -410 250 -460 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -460 2 0 {name=l17a sig_type=std_logic lab=pvdd}
N 250 -350 250 -300 {lab=by_pmid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -300 2 0 {name=l17b sig_type=std_logic lab=by_pmid}
N 210 -380 150 -380 {lab=comp2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -380 0 0 {name=l17c sig_type=std_logic lab=comp2b}
N 250 -380 270 -380 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 -380 2 0 {name=l17d sig_type=std_logic lab=pvdd}

T {XMby_p2a} 420 -430 0 0 0.22 0.22 {layer=13}
T {P:4/2} 420 -413 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 480 -380 0 0 {name=XMby_p2a L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 500 -410 500 -460 {lab=by_pmid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -460 2 0 {name=l18a sig_type=std_logic lab=by_pmid}
N 500 -350 500 -300 {lab=bypass_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -300 2 0 {name=l18b sig_type=std_logic lab=bypass_enb}
N 460 -380 400 -380 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -380 0 0 {name=l18c sig_type=std_logic lab=comp3}
N 500 -380 520 -380 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 -380 2 0 {name=l18d sig_type=std_logic lab=pvdd}

T {XMby_p2b} 670 -430 0 0 0.22 0.22 {layer=13}
T {P:4/2} 670 -413 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 730 -380 0 0 {name=XMby_p2b L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 750 -410 750 -460 {lab=by_pmid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 -460 2 0 {name=l19a sig_type=std_logic lab=by_pmid}
N 750 -350 750 -300 {lab=bypass_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 -300 2 0 {name=l19b sig_type=std_logic lab=bypass_enb}
N 710 -380 650 -380 {lab=comp4b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 -380 0 0 {name=l19c sig_type=std_logic lab=comp4b}
N 750 -380 770 -380 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 770 -380 2 0 {name=l19d sig_type=std_logic lab=pvdd}

T {NMOS pull-down (series stacks)} -80 -200 0 0 0.25 0.25 {layer=7}
T {XMby_n1a} -80 -90 0 0 0.22 0.22 {layer=13}
T {N:2/2} -80 -73 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -20 -140 0 0 {name=XMby_n1a L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 0 -170 0 -220 {lab=by_s1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -220 2 0 {name=l20a sig_type=std_logic lab=by_s1}
N 0 -110 0 -60 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 -60 0 0 {name=lg21 lab=GND}
N -40 -140 -100 -140 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 -140 0 0 {name=l20c sig_type=std_logic lab=comp1}
N 0 -140 20 -140 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 -140 2 0 {name=l20d sig_type=std_logic lab=gnd}

T {XMby_n1b} 170 -90 0 0 0.22 0.22 {layer=13}
T {N:2/2} 170 -73 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 230 -140 0 0 {name=XMby_n1b L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 250 -170 250 -220 {lab=bypass_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -220 2 0 {name=l22a sig_type=std_logic lab=bypass_enb}
N 250 -110 250 -60 {lab=by_s1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -60 2 0 {name=l22b sig_type=std_logic lab=by_s1}
N 210 -140 150 -140 {lab=comp2b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -140 0 0 {name=l22c sig_type=std_logic lab=comp2b}
N 250 -140 270 -140 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 -140 2 0 {name=l22d sig_type=std_logic lab=gnd}

T {XMby_n2a} 420 -90 0 0 0.22 0.22 {layer=13}
T {N:2/2} 420 -73 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 480 -140 0 0 {name=XMby_n2a L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 500 -170 500 -220 {lab=by_s2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -220 2 0 {name=l23a sig_type=std_logic lab=by_s2}
N 500 -110 500 -60 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 500 -60 0 0 {name=lg24 lab=GND}
N 460 -140 400 -140 {lab=comp3}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -140 0 0 {name=l23c sig_type=std_logic lab=comp3}
N 500 -140 520 -140 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 -140 2 0 {name=l23d sig_type=std_logic lab=gnd}

T {XMby_n2b} 670 -90 0 0 0.22 0.22 {layer=13}
T {N:2/2} 670 -73 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 730 -140 0 0 {name=XMby_n2b L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 750 -170 750 -220 {lab=bypass_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 -220 2 0 {name=l25a sig_type=std_logic lab=bypass_enb}
N 750 -110 750 -60 {lab=by_s2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 750 -60 2 0 {name=l25b sig_type=std_logic lab=by_s2}
N 710 -140 650 -140 {lab=comp4b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 650 -140 0 0 {name=l25c sig_type=std_logic lab=comp4b}
N 750 -140 770 -140 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 770 -140 2 0 {name=l25d sig_type=std_logic lab=gnd}

T {Output INV} 1000 -440 0 0 0.25 0.25 {layer=7}
T {XMby_outp} 990 -430 0 0 0.22 0.22 {layer=13}
T {P:4/2} 990 -413 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1050 -380 0 0 {name=XMby_outp L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 1070 -410 1070 -460 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1070 -460 2 0 {name=l26a sig_type=std_logic lab=pvdd}
N 1070 -350 1070 -310 {lab=bypass_en}
N 1030 -380 950 -380 {lab=bypass_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 950 -380 0 0 {name=l26c sig_type=std_logic lab=bypass_enb}
N 1070 -380 1090 -380 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1090 -380 2 0 {name=l26d sig_type=std_logic lab=pvdd}
T {XMby_outn} 990 -250 0 0 0.22 0.22 {layer=13}
T {N:2/2} 990 -233 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1050 -280 0 0 {name=XMby_outn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 1070 -310 1070 -310 {lab=bypass_en}
N 1070 -250 1070 -200 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1070 -200 0 0 {name=lg28 lab=GND}
N 1030 -280 950 -280 {lab=bypass_enb}
N 950 -280 950 -380 {lab=bypass_enb}
N 1070 -280 1090 -280 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1090 -280 2 0 {name=l27d sig_type=std_logic lab=gnd}
T {bypass_en} 1080 -320 0 0 0.28 0.28 {layer=8}

* ================================================================
* SECTION 3: ea_en — AOI21 + output INV (8 FETs)
* ea_enb = !((comp2·!comp3) + comp4)
* ea_en = (comp2·!comp3) + comp4  [AOI21 + INV]
* ================================================================

T {EA_EN — AOI21 + INV} -100 50 0 0 0.5 0.5 {layer=4}
T {ea_en = (comp2 · comp3b) + comp4 = (comp2·!comp3)+comp4} -100 85 0 0 0.28 0.28 {layer=5}

T {PMOS pull-up} -80 140 0 0 0.25 0.25 {layer=7}
T {XMea_p1a} -80 150 0 0 0.22 0.22 {layer=13}
T {P:4/2} -80 167 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -20 200 0 0 {name=XMea_p1a L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 0 170 0 120 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 120 2 0 {name=l29a sig_type=std_logic lab=pvdd}
N 0 230 0 280 {lab=ea_pmid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 280 2 0 {name=l29b sig_type=std_logic lab=ea_pmid}
N -40 200 -100 200 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 200 0 0 {name=l29c sig_type=std_logic lab=comp2}
N 0 200 20 200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 200 2 0 {name=l29d sig_type=std_logic lab=pvdd}

T {XMea_p1b} 170 150 0 0 0.22 0.22 {layer=13}
T {P:4/2} 170 167 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 230 200 0 0 {name=XMea_p1b L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 250 170 250 120 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 120 2 0 {name=l30a sig_type=std_logic lab=pvdd}
N 250 230 250 280 {lab=ea_pmid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 280 2 0 {name=l30b sig_type=std_logic lab=ea_pmid}
N 210 200 150 200 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 200 0 0 {name=l30c sig_type=std_logic lab=comp3b}
N 250 200 270 200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 200 2 0 {name=l30d sig_type=std_logic lab=pvdd}

T {XMea_p2} 420 150 0 0 0.22 0.22 {layer=13}
T {P:4/2} 420 167 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 480 200 0 0 {name=XMea_p2 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 500 170 500 120 {lab=ea_pmid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 120 2 0 {name=l31a sig_type=std_logic lab=ea_pmid}
N 500 230 500 280 {lab=ea_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 280 2 0 {name=l31b sig_type=std_logic lab=ea_enb}
N 460 200 400 200 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 200 0 0 {name=l31c sig_type=std_logic lab=comp4}
N 500 200 520 200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 200 2 0 {name=l31d sig_type=std_logic lab=pvdd}

T {NMOS pull-down} -80 380 0 0 0.25 0.25 {layer=7}
T {XMea_n1a} -80 490 0 0 0.22 0.22 {layer=13}
T {N:2/2} -80 507 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -20 440 0 0 {name=XMea_n1a L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 0 410 0 360 {lab=ea_s1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 360 2 0 {name=l32a sig_type=std_logic lab=ea_s1}
N 0 470 0 520 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 520 0 0 {name=lg33 lab=GND}
N -40 440 -100 440 {lab=comp2}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 440 0 0 {name=l32c sig_type=std_logic lab=comp2}
N 0 440 20 440 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 440 2 0 {name=l32d sig_type=std_logic lab=gnd}

T {XMea_n1b} 170 490 0 0 0.22 0.22 {layer=13}
T {N:2/2} 170 507 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 230 440 0 0 {name=XMea_n1b L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 250 410 250 360 {lab=ea_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 360 2 0 {name=l34a sig_type=std_logic lab=ea_enb}
N 250 470 250 520 {lab=ea_s1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 520 2 0 {name=l34b sig_type=std_logic lab=ea_s1}
N 210 440 150 440 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 440 0 0 {name=l34c sig_type=std_logic lab=comp3b}
N 250 440 270 440 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 440 2 0 {name=l34d sig_type=std_logic lab=gnd}

T {XMea_n2} 420 490 0 0 0.22 0.22 {layer=13}
T {N:2/2} 420 507 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 480 440 0 0 {name=XMea_n2 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 500 410 500 360 {lab=ea_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 360 2 0 {name=l35a sig_type=std_logic lab=ea_enb}
N 500 470 500 520 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 500 520 0 0 {name=lg36 lab=GND}
N 460 440 400 440 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 440 0 0 {name=l35c sig_type=std_logic lab=comp4}
N 500 440 520 440 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 520 440 2 0 {name=l35d sig_type=std_logic lab=gnd}

T {Output INV} 730 140 0 0 0.25 0.25 {layer=7}
T {XMea_outp} 720 150 0 0 0.22 0.22 {layer=13}
T {P:4/2} 720 167 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 780 200 0 0 {name=XMea_outp L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 800 170 800 120 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 800 120 2 0 {name=l37a sig_type=std_logic lab=pvdd}
N 800 230 800 270 {lab=ea_en}
N 760 200 680 200 {lab=ea_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 680 200 0 0 {name=l37c sig_type=std_logic lab=ea_enb}
N 800 200 820 200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 200 2 0 {name=l37d sig_type=std_logic lab=pvdd}
T {XMea_outn} 720 330 0 0 0.22 0.22 {layer=13}
T {N:2/2} 720 347 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 780 300 0 0 {name=XMea_outn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 800 270 800 270 {lab=ea_en}
N 800 330 800 380 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 800 380 0 0 {name=lg39 lab=GND}
N 760 300 680 300 {lab=ea_enb}
N 680 300 680 200 {lab=ea_enb}
N 800 300 820 300 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 820 300 2 0 {name=l38d sig_type=std_logic lab=gnd}
T {ea_en} 810 260 0 0 0.28 0.28 {layer=8}

* ================================================================
* SECTION 4: ref_sel — NAND2 + output INV (6 FETs)
* ref_selb = !(comp1 · !comp3) = NAND2(comp1, comp3b)
* ref_sel = comp1 · !comp3  [NAND2 + INV]
* ================================================================

T {REF_SEL — NAND2 + INV} -100 620 0 0 0.5 0.5 {layer=4}
T {ref_sel = comp1 · comp3b = comp1 · !comp3} -100 655 0 0 0.28 0.28 {layer=5}

T {PMOS pull-up (parallel)} -80 710 0 0 0.25 0.25 {layer=7}
T {XMrs_p1} -80 720 0 0 0.22 0.22 {layer=13}
T {P:4/2} -80 737 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -20 770 0 0 {name=XMrs_p1 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 0 740 0 690 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 690 2 0 {name=l40a sig_type=std_logic lab=pvdd}
N 0 800 0 850 {lab=ref_selb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 850 2 0 {name=l40b sig_type=std_logic lab=ref_selb}
N -40 770 -100 770 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 770 0 0 {name=l40c sig_type=std_logic lab=comp1}
N 0 770 20 770 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 770 2 0 {name=l40d sig_type=std_logic lab=pvdd}

T {XMrs_p2} 170 720 0 0 0.22 0.22 {layer=13}
T {P:4/2} 170 737 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 230 770 0 0 {name=XMrs_p2 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 250 740 250 690 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 690 2 0 {name=l41a sig_type=std_logic lab=pvdd}
N 250 800 250 850 {lab=ref_selb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 850 2 0 {name=l41b sig_type=std_logic lab=ref_selb}
N 210 770 150 770 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 770 0 0 {name=l41c sig_type=std_logic lab=comp3b}
N 250 770 270 770 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 770 2 0 {name=l41d sig_type=std_logic lab=pvdd}

T {NMOS pull-down (series)} -80 930 0 0 0.25 0.25 {layer=7}
T {XMrs_n1} -80 1040 0 0 0.22 0.22 {layer=13}
T {N:2/2} -80 1057 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -20 990 0 0 {name=XMrs_n1 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 0 960 0 910 {lab=rs_s1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 910 2 0 {name=l42a sig_type=std_logic lab=rs_s1}
N 0 1020 0 1070 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 1070 0 0 {name=lg43 lab=GND}
N -40 990 -100 990 {lab=comp1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -100 990 0 0 {name=l42c sig_type=std_logic lab=comp1}
N 0 990 20 990 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 990 2 0 {name=l42d sig_type=std_logic lab=gnd}

T {XMrs_n2} 170 1040 0 0 0.22 0.22 {layer=13}
T {N:2/2} 170 1057 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 230 990 0 0 {name=XMrs_n2 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 250 960 250 910 {lab=ref_selb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 910 2 0 {name=l44a sig_type=std_logic lab=ref_selb}
N 250 1020 250 1070 {lab=rs_s1}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 1070 2 0 {name=l44b sig_type=std_logic lab=rs_s1}
N 210 990 150 990 {lab=comp3b}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 990 0 0 {name=l44c sig_type=std_logic lab=comp3b}
N 250 990 270 990 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 270 990 2 0 {name=l44d sig_type=std_logic lab=gnd}

T {Output INV} 530 710 0 0 0.25 0.25 {layer=7}
T {XMrs_outp} 520 720 0 0 0.22 0.22 {layer=13}
T {P:4/2} 520 737 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 580 770 0 0 {name=XMrs_outp L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 600 740 600 690 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 690 2 0 {name=l45a sig_type=std_logic lab=pvdd}
N 600 800 600 840 {lab=ref_sel}
N 560 770 480 770 {lab=ref_selb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 480 770 0 0 {name=l45c sig_type=std_logic lab=ref_selb}
N 600 770 620 770 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 770 2 0 {name=l45d sig_type=std_logic lab=pvdd}
T {XMrs_outn} 520 900 0 0 0.22 0.22 {layer=13}
T {N:2/2} 520 917 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 580 870 0 0 {name=XMrs_outn L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 600 840 600 840 {lab=ref_sel}
N 600 900 600 950 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 600 950 0 0 {name=lg47 lab=GND}
N 560 870 480 870 {lab=ref_selb}
N 480 870 480 770 {lab=ref_selb}
N 600 870 620 870 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 620 870 2 0 {name=l46d sig_type=std_logic lab=gnd}
T {ref_sel} 610 830 0 0 0.28 0.28 {layer=8}

* ================================================================
* SECTION 5: uvov_en — double buffer (4 FETs)
* uvov_enb = !comp4, uvov_en = !!comp4 = comp4
* ================================================================

T {UVOV_EN — Double Buffer} -100 1180 0 0 0.5 0.5 {layer=4}
T {uvov_en = comp4 (buffered)} -100 1215 0 0 0.28 0.28 {layer=5}

T {XMuv_p1} -80 1230 0 0 0.22 0.22 {layer=13}
T {P:4/2} -80 1247 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} -20 1280 0 0 {name=XMuv_p1 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 0 1250 0 1200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 1200 2 0 {name=l48a sig_type=std_logic lab=pvdd}
N 0 1310 0 1350 {lab=uvov_enb}
N -40 1280 -120 1280 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -120 1280 0 0 {name=l48c sig_type=std_logic lab=comp4}
N 0 1280 20 1280 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 1280 2 0 {name=l48d sig_type=std_logic lab=pvdd}
T {XMuv_n1} -80 1410 0 0 0.22 0.22 {layer=13}
T {N:2/2} -80 1427 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} -20 1380 0 0 {name=XMuv_n1 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 0 1350 0 1350 {lab=uvov_enb}
N 0 1410 0 1460 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 0 1460 0 0 {name=lg50 lab=GND}
N -40 1380 -120 1380 {lab=comp4}
N -120 1380 -120 1280 {lab=comp4}
N 0 1380 20 1380 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 20 1380 2 0 {name=l49d sig_type=std_logic lab=gnd}
T {uvov_enb} 10 1340 0 0 0.28 0.28 {layer=8}

T {XMuv_p2} 240 1230 0 0 0.22 0.22 {layer=13}
T {P:4/2} 240 1247 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 300 1280 0 0 {name=XMuv_p2 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 320 1250 320 1200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 320 1200 2 0 {name=l51a sig_type=std_logic lab=pvdd}
N 320 1310 320 1350 {lab=uvov_en}
N 280 1280 200 1280 {lab=uvov_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 200 1280 0 0 {name=l51c sig_type=std_logic lab=uvov_enb}
N 320 1280 340 1280 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 1280 2 0 {name=l51d sig_type=std_logic lab=pvdd}
T {XMuv_n2} 240 1410 0 0 0.22 0.22 {layer=13}
T {N:2/2} 240 1427 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 300 1380 0 0 {name=XMuv_n2 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 320 1350 320 1350 {lab=uvov_en}
N 320 1410 320 1460 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 320 1460 0 0 {name=lg53 lab=GND}
N 280 1380 200 1380 {lab=uvov_enb}
N 200 1380 200 1280 {lab=uvov_enb}
N 320 1380 340 1380 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 340 1380 2 0 {name=l52d sig_type=std_logic lab=gnd}
T {uvov_en} 330 1340 0 0 0.28 0.28 {layer=8}

* ================================================================
* SECTION 6: ilim_en — double buffer (4 FETs)
* ilim_enb = !comp4, ilim_en = !!comp4 = comp4
* ================================================================

T {ILIM_EN — Double Buffer} 650 1180 0 0 0.5 0.5 {layer=4}
T {ilim_en = comp4 (buffered)} 650 1215 0 0 0.28 0.28 {layer=5}

T {XMil_p1} 640 1230 0 0 0.22 0.22 {layer=13}
T {P:4/2} 640 1247 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 700 1280 0 0 {name=XMil_p1 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 720 1250 720 1200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 720 1200 2 0 {name=l54a sig_type=std_logic lab=pvdd}
N 720 1310 720 1350 {lab=ilim_enb}
N 680 1280 600 1280 {lab=comp4}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 600 1280 0 0 {name=l54c sig_type=std_logic lab=comp4}
N 720 1280 740 1280 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 740 1280 2 0 {name=l54d sig_type=std_logic lab=pvdd}
T {XMil_n1} 640 1410 0 0 0.22 0.22 {layer=13}
T {N:2/2} 640 1427 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 700 1380 0 0 {name=XMil_n1 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 720 1350 720 1350 {lab=ilim_enb}
N 720 1410 720 1460 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 720 1460 0 0 {name=lg56 lab=GND}
N 680 1380 600 1380 {lab=comp4}
N 600 1380 600 1280 {lab=comp4}
N 720 1380 740 1380 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 740 1380 2 0 {name=l55d sig_type=std_logic lab=gnd}
T {ilim_enb} 730 1340 0 0 0.28 0.28 {layer=8}

T {XMil_p2} 960 1230 0 0 0.22 0.22 {layer=13}
T {P:4/2} 960 1247 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_g5v0d10v5.sym} 1020 1280 0 0 {name=XMil_p2 L=2 W=4 nf=1 mult=1 model=pfet_g5v0d10v5 spiceprefix=X}
N 1040 1250 1040 1200 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1040 1200 2 0 {name=l57a sig_type=std_logic lab=pvdd}
N 1040 1310 1040 1350 {lab=ilim_en}
N 1000 1280 920 1280 {lab=ilim_enb}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 920 1280 0 0 {name=l57c sig_type=std_logic lab=ilim_enb}
N 1040 1280 1060 1280 {lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1060 1280 2 0 {name=l57d sig_type=std_logic lab=pvdd}
T {XMil_n2} 960 1410 0 0 0.22 0.22 {layer=13}
T {N:2/2} 960 1427 0 0 0.18 0.18 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_g5v0d10v5.sym} 1020 1380 0 0 {name=XMil_n2 L=2 W=2 nf=1 mult=1 model=nfet_g5v0d10v5 spiceprefix=X}
N 1040 1350 1040 1350 {lab=ilim_en}
N 1040 1410 1040 1460 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/gnd.sym} 1040 1460 0 0 {name=lg59 lab=GND}
N 1000 1380 920 1380 {lab=ilim_enb}
N 920 1380 920 1280 {lab=ilim_enb}
N 1040 1380 1060 1380 {lab=gnd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 1060 1380 2 0 {name=l58d sig_type=std_logic lab=gnd}
T {ilim_en} 1050 1340 0 0 0.28 0.28 {layer=8}

* ================================================================
* TRUTH TABLE & BOOLEAN EQUATIONS
* ================================================================

T {BOOLEAN EQUATIONS:} -300 1530 0 0 0.4 0.4 {layer=4}
T {pass_off  = !comp1                                     (INV buffer)} -300 1570 0 0 0.28 0.28 {layer=5}
T {bypass_en = (comp1·!comp2) + (comp3·!comp4)            (AOI22 + INV)} -300 1600 0 0 0.28 0.28 {layer=5}
T {ea_en     = (comp2·!comp3) + comp4                     (AOI21 + INV)} -300 1630 0 0 0.28 0.28 {layer=5}
T {ref_sel   = comp1 · !comp3                             (NAND2 + INV)} -300 1660 0 0 0.28 0.28 {layer=5}
T {uvov_en   = comp4                                      (double buffer)} -300 1690 0 0 0.28 0.28 {layer=5}
T {ilim_en   = comp4                                      (double buffer)} -300 1720 0 0 0.28 0.28 {layer=5}

T {TRUTH TABLE:} -300 1770 0 0 0.4 0.4 {layer=4}
T {Mode       | c1 c2 c3 c4 | pass_off bypass_en ea_en ref_sel uvov_en ilim_en} -300 1810 0 0 0.28 0.28 {layer=8}
T {-----------|-------------|----------------------------------------------------} -300 1835 0 0 0.28 0.28 {layer=8}
T {Shutdown   |  0  0  0  0 |    1        0        0      0       0       0} -300 1860 0 0 0.28 0.28 {layer=5}
T {Startup    |  1  0  0  0 |    0        1        0      1       0       0} -300 1885 0 0 0.28 0.28 {layer=5}
T {Regulating |  1  1  0  0 |    0        0        1      1       0       0} -300 1910 0 0 0.28 0.28 {layer=5}
T {Regulated  |  1  1  1  0 |    0        1        0      0       0       0} -300 1935 0 0 0.28 0.28 {layer=5}
T {Overvoltage|  1  1  1  1 |    0        0        1      0       1       1} -300 1960 0 0 0.28 0.28 {layer=5}

T {42 MOSFETs total: 21 PFET (W=4 L=2) + 21 NFET (W=2 L=2)  |  All sky130 5V thick-oxide} -300 2010 0 0 0.3 0.3 {layer=7}
