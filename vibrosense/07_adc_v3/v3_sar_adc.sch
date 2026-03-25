v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 07: 8-bit SAR ADC v3 — Top Level} -600 -1800 0 0 1.0 1.0 {layer=15}
T {Charge-Redistribution SAR ADC  —  SKY130A  —  Full Redesign} -600 -1740 0 0 0.5 0.5 {layer=15}
T {8 bits | 10 kSPS | 28 µW | Vref=1.2V | VDD=1.8V | Cunit=200fF} -600 -1690 0 0 0.4 0.4 {layer=8}
T {Sample Switch (CMOS TG)} -500 -1580 0 0 0.5 0.5 {layer=4}
T {Ron ~50Ω  |  τ = 50×51.2p = 2.6 ns} -500 -1540 0 0 0.3 0.3 {layer=8}
T {M_sw_n} -400 -1440 0 0 0.3 0.3 {layer=8}
T {5/0.15} -400 -1416 0 0 0.25 0.25 {layer=8}
T {M_sw_p} -400 -1340 0 0 0.3 0.3 {layer=8}
T {10/0.15} -400 -1316 0 0 0.25 0.25 {layer=8}
T {8-bit Cap DAC} 0 -1580 0 0 0.5 0.5 {layer=4}
T {Binary-weighted  |  256×Cunit  |  Cunit=200fF  |  Total=51.2pF} 0 -1540 0 0 0.3 0.3 {layer=8}
T {128C} 30 -1460 0 0 0.3 0.3 {layer=8}
T {64C} 120 -1460 0 0 0.3 0.3 {layer=8}
T {32C} 200 -1460 0 0 0.3 0.3 {layer=8}
T {16C} 275 -1460 0 0 0.3 0.3 {layer=8}
T {8C} 345 -1460 0 0 0.3 0.3 {layer=8}
T {4C} 405 -1460 0 0 0.3 0.3 {layer=8}
T {2C} 460 -1460 0 0 0.3 0.3 {layer=8}
T {1C} 510 -1460 0 0 0.3 0.3 {layer=8}
T {1C} 560 -1460 0 0 0.3 0.3 {layer=5}
T {dummy} 555 -1436 0 0 0.2 0.2 {layer=5}
T {Bottom-plate switches: CMOS TG W=4u/8u per bit} 0 -1380 0 0 0.25 0.25 {layer=8}
T {vtop} -200 -1480 0 0 0.35 0.35 {layer=5}
T {Comparator} 0 -1260 0 0 0.5 0.5 {layer=4}
T {Pre-amp + StrongARM + SR latch  |  Offset < 0.01 mV} 0 -1220 0 0 0.3 0.3 {layer=8}
T {inp = vtop} 30 -1160 0 0 0.25 0.25 {layer=8}
T {inn = vref} 30 -1130 0 0 0.25 0.25 {layer=8}
T {comp_out: HIGH=keep bit, LOW=clear} 30 -1100 0 0 0.25 0.25 {layer=8}
T {~53 transistors} 30 -1070 0 0 0.25 0.25 {layer=5}
T {SAR Logic} 500 -1260 0 0 0.5 0.5 {layer=4}
T {One-hot state machine  |  XSPICE DFF + CMOS gates} 500 -1220 0 0 0.3 0.3 {layer=8}
T {States: IDLE → S1(sample) → S2(bit7) → ... → S9(bit0) → IDLE} 500 -1180 0 0 0.25 0.25 {layer=8}
T {10 DFFs (XSPICE)  |  8 bit registers  |  DAC mux logic} 500 -1150 0 0 0.25 0.25 {layer=8}
T {comp_clk = NOT(clk) AND eval_active} 500 -1120 0 0 0.25 0.25 {layer=8}
T {DAC outputs: d[7:0] = (bit_q OR tentative) AND NOT(sample)} 500 -1090 0 0 0.25 0.25 {layer=8}
T {Valid delayed 10ns for d0 settling} 500 -1060 0 0 0.25 0.25 {layer=8}
T {Conversion Cycle} -600 -920 0 0 0.5 0.5 {layer=4}
T {1. IDLE: wait for convert=HIGH} -600 -880 0 0 0.3 0.3 {layer=8}
T {2. S1 (Sample): close TG, all DAC→GND, vtop=Vin} -600 -850 0 0 0.3 0.3 {layer=8}
T {3. S2-S9 (Bit trials): MSB→LSB, compare vtop vs Vref} -600 -820 0 0 0.3 0.3 {layer=8}
T {4. Output valid on d[7:0], valid pulse asserted} -600 -790 0 0 0.3 0.3 {layer=8}
T {Code = round((Vref − Vin) / Vref × 256)  [complement]} -600 -750 0 0 0.3 0.3 {layer=5}
T {Performance Summary} 200 -920 0 0 0.5 0.5 {layer=4}
T {TB2: 13 codes ±1 LSB, monotonic, even+odd codes} 200 -880 0 0 0.3 0.3 {layer=8}
T {TB8: 5/5 corners pass (TT/SS/FF/SF/FS)} 200 -850 0 0 0.3 0.3 {layer=8}
T {Power: 28.2 µW active, 34.5 nW sleep} 200 -820 0 0 0.3 0.3 {layer=8}
T {Wakeup: 95.1 µs (includes 10-cycle conversion)} 200 -790 0 0 0.3 0.3 {layer=8}
T {v3 Fixes: DAC reset, bit register clear, comp redesign} 200 -750 0 0 0.3 0.3 {layer=5}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -360 -1400 0 0 {name=XM_sw_n
W=5
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -360 -1300 0 0 {name=XM_sw_p
W=10
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -1400 0 1 {name=p_vin lab=vin}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -1140 0 1 {name=p_vref lab=vref}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -1030 0 1 {name=p_clk lab=clk}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -990 0 1 {name=p_convert lab=convert}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -950 0 1 {name=p_sleep_n lab=sleep_n}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -1620 0 1 {name=p_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -600 -680 0 1 {name=p_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1400 0 0 {name=p_d7 lab=d7}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1370 0 0 {name=p_d6 lab=d6}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1340 0 0 {name=p_d5 lab=d5}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1310 0 0 {name=p_d4 lab=d4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1280 0 0 {name=p_d3 lab=d3}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1250 0 0 {name=p_d2 lab=d2}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1220 0 0 {name=p_d1 lab=d1}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1190 0 0 {name=p_d0 lab=d0}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 900 -1140 0 0 {name=p_valid lab=valid}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -200 -1480 0 1 {name=l_vtop lab=vtop}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 300 -1140 0 0 {name=l_comp_out lab=comp_out}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -340 -1460 0 0 {name=l_sample lab=sample}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -1030 0 0 {name=l_comp_clk lab=comp_clk}
N -600 -1400 -380 -1400 {lab=vin}
N -340 -1370 -340 -1330 {lab=vtop}
N -340 -1480 -340 -1430 {lab=vtop}
N -340 -1480 0 -1480 {lab=vtop}
N -340 -1270 -340 -1200 {lab=vss}
