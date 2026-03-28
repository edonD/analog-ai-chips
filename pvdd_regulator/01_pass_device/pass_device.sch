v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {BLOCK 01: PASS DEVICE} -500 -900 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator} -500 -830 0 0 0.5 0.5 {layer=8}
T {SkyWater SKY130A Process} -500 -790 0 0 0.4 0.4 {}
T {Device: sky130_fd_pr__pfet_g5v0d10v5  (HV PMOS, Vds max = 10.5V)} -500 -730 0 0 0.35 0.35 {}
T {W = 100 um / instance,  L = 0.5 um,  10 parallel instances} -500 -690 0 0 0.35 0.35 {}
T {Total W = 1.0 mm} -500 -650 0 0 0.4 0.4 {layer=7}
T {Date: 2026-03-28} -500 -600 0 0 0.3 0.3 {}
T {.subckt pass_device  gate  bvdd  pvdd} -500 -560 0 0 0.3 0.3 {layer=13}
T {BVDD} 400 -700 0 0 0.7 0.7 {layer=7}
T {5.4 V  to  10.5 V} 400 -650 0 0 0.3 0.3 {}
T {(Battery Supply)} 400 -620 0 0 0.25 0.25 {}
T {Source / Bulk} 400 -480 0 0 0.25 0.25 {layer=8}
T {GATE} -350 -400 0 0 0.7 0.7 {layer=4}
T {From Error Amplifier} -350 -350 0 0 0.3 0.3 {}
T {0 V = fully ON} -350 -310 0 0 0.25 0.25 {layer=5}
T {BVDD = fully OFF} -350 -280 0 0 0.25 0.25 {layer=5}
T {PVDD} 560 -160 0 0 0.7 0.7 {layer=7}
T {5.0 V regulated output} 560 -110 0 0 0.3 0.3 {}
T {Drain} 400 -260 0 0 0.25 0.25 {layer=8}
T {XM1 .. XM10} 230 -460 0 0 0.4 0.4 {}
T {sky130_fd_pr__pfet_g5v0d10v5} 150 -490 0 0 0.3 0.3 {layer=13}
T {W = 100u   L = 0.5u   x 10} 230 -430 0 0 0.3 0.3 {layer=5}
T {CHARACTERIZATION} -500 70 0 0 0.5 0.5 {layer=4}
T {Id at dropout (TT 27C)   =  84.2 mA      spec >= 50 mA       PASS} -500 130 0 0 0.3 0.3 {layer=7}
T {Id at dropout (SS 150C)  =  56.8 mA      spec >= 50 mA       PASS} -500 170 0 0 0.3 0.3 {layer=7}
T {Rds_on                   =  4.75 ohm     spec <= 20 ohm      PASS} -500 210 0 0 0.3 0.3 {layer=7}
T {Cgs                      =  1.04 pF      (measured)} -500 250 0 0 0.3 0.3 {layer=7}
T {gm at 10 mA              =  5.4 mA/V     (measured)} -500 290 0 0 0.3 0.3 {layer=7}
T {Leakage (off)            =  0.00002 uA   spec <= 1 uA        PASS} -500 330 0 0 0.3 0.3 {layer=7}
T {Total Width              =  1.0 mm       spec <= 20 mm       PASS} -500 370 0 0 0.3 0.3 {layer=7}
T {All 7/7 specs PASS} -500 430 0 0 0.45 0.45 {layer=4}
C {devices/pmos4.sym} 340 -380 0 0 {name=XM1
W=100e-6
L=0.5e-6
model=sky130_fd_pr__pfet_g5v0d10v5
spiceprefix=X
}
N -150 -380 320 -380 {lab=gate}
N 360 -410 360 -560 {lab=bvdd}
N 360 -560 360 -580 {lab=bvdd}
N 360 -380 360 -410 {lab=bvdd}
N 360 -350 360 -200 {lab=pvdd}
N 360 -200 530 -200 {lab=pvdd}
C {devices/iopin.sym} -150 -380 0 1 {name=p1 lab=gate}
C {devices/iopin.sym} 360 -580 3 0 {name=p2 lab=bvdd}
C {devices/iopin.sym} 530 -200 0 0 {name=p3 lab=pvdd}
C {devices/title.sym} -560 560 0 0 {name=l1 author="Block 01: Pass Device -- Analog AI Chips PVDD LDO Regulator"}
