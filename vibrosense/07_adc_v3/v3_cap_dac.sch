v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VibroSense Block 07: SAR ADC v3 — 8-bit Cap DAC} -400 -1400 0 0 1.0 1.0 {layer=15}
T {Binary-Weighted Charge-Redistribution DAC  —  SKY130A} -400 -1340 0 0 0.5 0.5 {layer=15}
T {Cunit = 200 fF  |  Total = 256×Cunit = 51.2 pF  |  1 dummy cap} -400 -1290 0 0 0.4 0.4 {layer=8}
T {Top Plate (vtop)} -400 -1190 0 0 0.5 0.5 {layer=4}
T {Common node — connects to comparator inp and sample switch} -400 -1150 0 0 0.3 0.3 {layer=8}
T {Parasitic Cp ~42 fF (comparator gate + switch drain)} -400 -1120 0 0 0.25 0.25 {layer=5}
T {Binary-Weighted Capacitors} -400 -1050 0 0 0.5 0.5 {layer=4}
T {C128} -350 -980 0 0 0.35 0.35 {layer=8}
T {128×200fF} -370 -950 0 0 0.25 0.25 {layer=8}
T {= 25.6pF} -370 -925 0 0 0.25 0.25 {layer=8}
T {C64} -170 -980 0 0 0.35 0.35 {layer=8}
T {64×200fF} -190 -950 0 0 0.25 0.25 {layer=8}
T {= 12.8pF} -190 -925 0 0 0.25 0.25 {layer=8}
T {C32} 10 -980 0 0 0.35 0.35 {layer=8}
T {32×200fF} -10 -950 0 0 0.25 0.25 {layer=8}
T {= 6.4pF} -10 -925 0 0 0.25 0.25 {layer=8}
T {C16} 190 -980 0 0 0.35 0.35 {layer=8}
T {16×200fF} 170 -950 0 0 0.25 0.25 {layer=8}
T {= 3.2pF} 170 -925 0 0 0.25 0.25 {layer=8}
T {C8} 370 -980 0 0 0.35 0.35 {layer=8}
T {8×200fF} 350 -950 0 0 0.25 0.25 {layer=8}
T {= 1.6pF} 350 -925 0 0 0.25 0.25 {layer=8}
T {C4} 550 -980 0 0 0.35 0.35 {layer=8}
T {4×200fF} 530 -950 0 0 0.25 0.25 {layer=8}
T {= 800fF} 530 -925 0 0 0.25 0.25 {layer=8}
T {C2} 710 -980 0 0 0.35 0.35 {layer=8}
T {2×200fF} 690 -950 0 0 0.25 0.25 {layer=8}
T {= 400fF} 690 -925 0 0 0.25 0.25 {layer=8}
T {C1} 870 -980 0 0 0.35 0.35 {layer=8}
T {1×200fF} 850 -950 0 0 0.25 0.25 {layer=8}
T {(LSB)} 850 -925 0 0 0.25 0.25 {layer=8}
T {Cdummy} 1040 -980 0 0 0.35 0.35 {layer=5}
T {1×200fF} 1020 -950 0 0 0.25 0.25 {layer=5}
T {→ GND} 1020 -925 0 0 0.25 0.25 {layer=5}
T {Bottom-Plate Switches (CMOS TG)} -400 -850 0 0 0.5 0.5 {layer=4}
T {Each bit: NMOS W=4u + PMOS W=8u transmission gate (v3.1: 4× wider for settling)} -400 -810 0 0 0.3 0.3 {layer=8}
T {ctrl=HIGH → bottom plate to Vref  |  ctrl=LOW → bottom plate to GND} -400 -780 0 0 0.3 0.3 {layer=8}
T {Settling: MSB τ = Ron×Ceq ≈ 400×12.8p = 5.1 ns  |  5τ = 25.6 ns « 100 ns (5MHz half-cycle)} -400 -750 0 0 0.25 0.25 {layer=5}
T {Switch Detail} -400 -680 0 0 0.4 0.4 {layer=4}
T {M_vr_n: NMOS W=4u L=0.15u} -400 -640 0 0 0.3 0.3 {layer=8}
T {M_vr_p: PMOS W=8u L=0.15u} -400 -610 0 0 0.3 0.3 {layer=8}
T {M_gn_n: NMOS W=4u L=0.15u} -400 -580 0 0 0.3 0.3 {layer=8}
T {M_gn_p: PMOS W=8u L=0.15u} -400 -550 0 0 0.3 0.3 {layer=8}
T {4 transistors per bit × 8 bits = 32 switch transistors} -400 -510 0 0 0.25 0.25 {layer=5}
T {DC Convergence} 400 -680 0 0 0.4 0.4 {layer=4}
T {Rleak per bottom plate: 10 GΩ to GND} 400 -640 0 0 0.3 0.3 {layer=8}
T {Rleak_top: 100 GΩ to GND (top plate)} 400 -610 0 0 0.3 0.3 {layer=8}
T {At 100G: leakage = 12pA → 0.05 LSB/conversion} 400 -580 0 0 0.25 0.25 {layer=5}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -400 -1190 0 1 {name=p_top lab=top}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -400 -850 0 1 {name=p_vref lab=vref}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -400 -480 0 1 {name=p_gnd lab=gnd_node}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -400 -440 0 1 {name=p_vdd lab=vdd}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} -400 -400 0 1 {name=p_vss lab=vss}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1150 -850 0 0 {name=p_sw7 lab=sw7}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1150 -820 0 0 {name=p_sw6 lab=sw6}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1150 -790 0 0 {name=p_sw5 lab=sw5}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1150 -760 0 0 {name=p_sw4 lab=sw4}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1150 -730 0 0 {name=p_sw3 lab=sw3}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1150 -700 0 0 {name=p_sw2 lab=sw2}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1150 -670 0 0 {name=p_sw1 lab=sw1}
C {/usr/local/share/xschem/xschem_library/devices/iopin.sym} 1150 -640 0 0 {name=p_sw0 lab=sw0}
N -350 -1100 1050 -1100 {lab=top}
