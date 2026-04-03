v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 07: 8-bit SAR ADC v3 — Top Level} -200 -1800 0 0 1.0 1.0 {layer=15}
T {Charge-Redistribution SAR ADC  —  SKY130A  —  Full Redesign} -200 -1740 0 0 0.5 0.5 {layer=15}
T {8 bits | 10 kSPS | 28 uW | Vref=1.2V | VDD=1.8V | Cunit=200fF} -200 -1690 0 0 0.4 0.4 {layer=8}
T {Signal Flow:  Vin -> [CMOS TG] -> Vtop <-> [Cap DAC] <-> [SAR Logic]   |   Vtop -> [Comparator] -> comp_out -> [SAR Logic]} -200 -1640 0 0 0.3 0.3 {layer=5}
T {Sample Switch (CMOS Transmission Gate)} -100 -1560 0 0 0.5 0.5 {layer=4}
T {Ron ~50 ohm  |  tau = 50 x 51.2p = 2.6 ns} -100 -1520 0 0 0.3 0.3 {layer=8}
T {sample=HIGH: TG ON, Vin charges vtop to Vin} -100 -1490 0 0 0.25 0.25 {layer=8}
T {M_sw_n} 85 -1420 0 0 0.3 0.3 {layer=8}
T {NMOS 5/0.15} 75 -1396 0 0 0.25 0.25 {layer=8}
T {M_sw_p} 85 -1280 0 0 0.3 0.3 {layer=8}
T {PMOS 10/0.15} 75 -1256 0 0 0.25 0.25 {layer=8}
T {8-bit Binary-Weighted Capacitor DAC} 470 -1560 0 0 0.5 0.5 {layer=4}
T {v3_cap_dac subcircuit} 470 -1520 0 0 0.3 0.3 {layer=8}
T {Cunit = 200 fF  |  Total = 256 x Cunit = 51.2 pF} 470 -1490 0 0 0.25 0.25 {layer=8}
T {Binary weights: 128C 64C 32C 16C 8C 4C 2C 1C + 1C dummy} 470 -1460 0 0 0.25 0.25 {layer=8}
T {Bottom-plate switches: CMOS TG (NMOS 4u + PMOS 8u per bit)} 470 -1430 0 0 0.25 0.25 {layer=8}
T {ctrl=HIGH -> bottom plate to Vref} 470 -1400 0 0 0.25 0.25 {layer=8}
T {ctrl=LOW  -> bottom plate to GND} 470 -1370 0 0 0.25 0.25 {layer=8}
T {DAC reset: d[7:0] AND NOT(sample) gates outputs during sampling} 470 -1340 0 0 0.25 0.25 {layer=5}
T {Comparator (Pre-amp + StrongARM + SR Latch)} 470 -1240 0 0 0.5 0.5 {layer=4}
T {v3_comparator subcircuit  —  ~53 transistors} 470 -1200 0 0 0.3 0.3 {layer=8}
T {inp = vtop  |  inn = vref} 470 -1170 0 0 0.25 0.25 {layer=8}
T {Pre-amp gain ~20-40x  |  StrongARM dynamic latch} 470 -1140 0 0 0.25 0.25 {layer=8}
T {Decision < 40 ns for 1 LSB overdrive} 470 -1110 0 0 0.25 0.25 {layer=8}
T {Offset < 0.01 mV all corners} 470 -1080 0 0 0.25 0.25 {layer=8}
T {comp_out: HIGH = keep bit, LOW = clear bit} 470 -1050 0 0 0.25 0.25 {layer=5}
T {SAR Logic (One-Hot State Machine)} 1070 -1560 0 0 0.5 0.5 {layer=4}
T {v3_sar_logic subcircuit} 1070 -1520 0 0 0.3 0.3 {layer=8}
T {States: IDLE -> S1(sample) -> S2(bit7) -> ... -> S9(bit0) -> IDLE} 1070 -1490 0 0 0.25 0.25 {layer=8}
T {10 DFFs (XSPICE)  |  8 bit registers  |  DAC mux logic} 1070 -1460 0 0 0.25 0.25 {layer=8}
T {comp_clk = NOT(clk) AND eval_active} 1070 -1430 0 0 0.25 0.25 {layer=8}
T {DAC outputs: d[7:0] = (bit_q OR tentative) AND NOT(sample)} 1070 -1400 0 0 0.25 0.25 {layer=8}
T {Generates: sample, sample_b, valid, comp_clk} 1070 -1370 0 0 0.25 0.25 {layer=8}
T {Valid delayed 10 ns for d0 settling} 1070 -1340 0 0 0.25 0.25 {layer=5}
T {Conversion Cycle} -200 -940 0 0 0.5 0.5 {layer=4}
T {1. IDLE: wait for convert=HIGH} -200 -900 0 0 0.3 0.3 {layer=8}
T {2. S1 (Sample): close TG, all DAC->GND, vtop=Vin} -200 -870 0 0 0.3 0.3 {layer=8}
T {3. S2-S9 (Bit trials): MSB->LSB, compare vtop vs Vref} -200 -840 0 0 0.3 0.3 {layer=8}
T {4. Output valid on d[7:0], valid pulse asserted} -200 -810 0 0 0.3 0.3 {layer=8}
T {Code = round((Vref - Vin) / Vref x 256)  [complement code]} -200 -770 0 0 0.3 0.3 {layer=5}
T {Performance Summary} 600 -940 0 0 0.5 0.5 {layer=4}
T {TB2: 13 codes +/-1 LSB, monotonic, even+odd codes} 600 -900 0 0 0.3 0.3 {layer=8}
T {TB8: 5/5 corners pass (TT/SS/FF/SF/FS)} 600 -870 0 0 0.3 0.3 {layer=8}
T {Power: 28.2 uW active, 34.5 nW sleep} 600 -840 0 0 0.3 0.3 {layer=8}
T {Wakeup: 95.1 us (includes 10-cycle conversion)} 600 -810 0 0 0.3 0.3 {layer=8}
T {v3 Fixes: DAC reset, bit register clear, comp redesign} 600 -770 0 0 0.3 0.3 {layer=5}
L 4 440 -1590 950 -1590 {}
L 4 950 -1590 950 -1290 {}
L 4 950 -1290 440 -1290 {}
L 4 440 -1290 440 -1590 {}
L 4 440 -1260 950 -1260 {}
L 4 950 -1260 950 -1010 {}
L 4 950 -1010 440 -1010 {}
L 4 440 -1010 440 -1260 {}
L 4 1040 -1590 1700 -1590 {}
L 4 1700 -1590 1700 -1290 {}
L 4 1700 -1290 1040 -1290 {}
L 4 1040 -1290 1040 -1590 {}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 140 -1370 0 0 {name=XM_sw_n
W=5
L=0.15
nf=1
mult=1
model=nfet_01v8
spiceprefix=X
}
C {/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 140 -1230 0 0 {name=XM_sw_p
W=10
L=0.15
nf=1
mult=1
model=pfet_01v8
spiceprefix=X
}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -300 -1340 0 1 {name=p_vin lab=vin}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -300 -1600 0 1 {name=p_vdd lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -300 -700 0 1 {name=p_vss lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -300 -1200 0 1 {name=p_vref lab=vref}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -300 -1060 0 1 {name=p_clk lab=clk}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -300 -1020 0 1 {name=p_convert lab=convert}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -300 -980 0 1 {name=p_sleep_n lab=sleep_n}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1530 0 0 {name=p_d7 lab=d7}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1500 0 0 {name=p_d6 lab=d6}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1470 0 0 {name=p_d5 lab=d5}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1440 0 0 {name=p_d4 lab=d4}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1410 0 0 {name=p_d3 lab=d3}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1380 0 0 {name=p_d2 lab=d2}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1350 0 0 {name=p_d1 lab=d1}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1320 0 0 {name=p_d0 lab=d0}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1800 -1260 0 0 {name=p_valid lab=valid}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 120 -1370 0 1 {name=l_sample_n lab=sample}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 120 -1230 0 1 {name=l_sample_b_p lab=sample_b}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 300 -1600 0 0 {name=l_vtop_sw lab=vtop}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 450 -1580 0 1 {name=l_vtop_dac lab=vtop}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 450 -1180 0 1 {name=l_vtop_comp lab=vtop}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 450 -1140 0 1 {name=l_vref_comp lab=vref}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 450 -1300 0 1 {name=l_vref_dac lab=vref}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 450 -1030 0 1 {name=l_sleep_n_comp lab=sleep_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1180 0 0 {name=l_comp_out lab=comp_out}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1140 0 0 {name=l_comp_out_n lab=comp_out_n}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1100 0 0 {name=l_comp_clk_out lab=comp_clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1480 0 0 {name=l_d_dac lab=d7,d6,d5,d4,d3,d2,d1,d0}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1440 0 0 {name=l_db_dac lab=d7_b,d6_b,d5_b,d4_b,d3_b,d2_b,d1_b,d0_b}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 450 -1400 0 1 {name=l_vss_dac lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1400 0 0 {name=l_vdd_dac lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1360 0 0 {name=l_vss_dac2 lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 450 -1020 0 1 {name=l_vdd_comp lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 940 -1020 0 0 {name=l_vss_comp lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -1540 0 1 {name=l_comp_out_sar lab=comp_out}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -1500 0 1 {name=l_clk_sar lab=clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -1460 0 1 {name=l_convert_sar lab=convert}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -1420 0 1 {name=l_vdd_sar lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1050 -1380 0 1 {name=l_vss_sar lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -1570 0 0 {name=l_d_sar lab=d7,d6,d5,d4,d3,d2,d1,d0}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -1550 0 0 {name=l_db_sar lab=d7_b,d6_b,d5_b,d4_b,d3_b,d2_b,d1_b,d0_b}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -1530 0 0 {name=l_sample_sar lab=sample}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -1510 0 0 {name=l_sample_b_sar lab=sample_b}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -1490 0 0 {name=l_comp_clk_sar lab=comp_clk}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1690 -1470 0 0 {name=l_valid_sar lab=valid}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1530 0 1 {name=l_d7_io lab=d7}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1500 0 1 {name=l_d6_io lab=d6}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1470 0 1 {name=l_d5_io lab=d5}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1440 0 1 {name=l_d4_io lab=d4}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1410 0 1 {name=l_d3_io lab=d3}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1380 0 1 {name=l_d2_io lab=d2}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1350 0 1 {name=l_d1_io lab=d1}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1320 0 1 {name=l_d0_io lab=d0}
C {/usr/local/share/xschem/xschem_library/devices/lab_pin.sym} 1770 -1260 0 1 {name=l_valid_io lab=valid}
N -300 -1340 60 -1340 {lab=vin}
N 60 -1340 160 -1340 {lab=vin}
N 60 -1260 160 -1260 {lab=vin}
N 60 -1340 60 -1260 {lab=vin}
N 160 -1400 300 -1400 {lab=vtop}
N 160 -1200 300 -1200 {lab=vtop}
N 300 -1400 300 -1200 {lab=vtop}
N 300 -1600 300 -1400 {lab=vtop}
N 160 -1370 220 -1370 {lab=vss}
N 220 -1370 220 -700 {lab=vss}
N -300 -700 220 -700 {lab=vss}
N 160 -1230 250 -1230 {lab=vdd}
N 250 -1600 250 -1230 {lab=vdd}
N -300 -1600 250 -1600 {lab=vdd}
