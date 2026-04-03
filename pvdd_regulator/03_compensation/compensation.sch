v {xschem version=3.4.6 file_version=1.2}
G {}
K {type=subcircuit
format="@name @pinlist @symname"
template="name=x1"
}
V {}
S {}
E {}

T {BLOCK 03: COMPENSATION NETWORK} -500 -700 0 0 1.0 1.0 {layer=4}
T {PVDD 5.0V LDO Regulator  |  SkyWater SKY130A} -500 -620 0 0 0.45 0.45 {layer=8}
T {.subckt compensation  vout_gate  pvdd  gnd} -500 -555 0 0 0.28 0.28 {layer=13}

C {/usr/share/xschem/xschem_library/devices/ipin.sym} -500 -460 0 0 {name=p1 lab=vout_gate}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -410 -460 0 0 {name=p2 lab=pvdd}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -410 -430 0 0 {name=p3 lab=gnd}

C {/usr/share/xschem/xschem_library/devices/title.sym} -500 600 0 0 {name=l1 author="Block 03: Compensation -- Analog AI Chips PVDD LDO Regulator"}

* ================================================================
* STATUS: EMPTY PLACEHOLDER
* All external compensation has been removed.
* ================================================================

T {STATUS: EMPTY -- All external compensation removed} -500 -380 0 0 0.55 0.55 {layer=4}

T {Actual compensation is handled by:} -500 -300 0 0 0.4 0.4 {layer=8}
T {- Inner EA Miller: Cc=40pF + Rc=5k (in Block 00, FIX-21)} -500 -260 0 0 0.35 0.35 {}
T {- External bypass: Cout_ext=1uF (in Block 10)} -500 -225 0 0 0.35 0.35 {}
T {- System UGB ~ 1-2.4kHz, PM ~ 80-160 deg (stable, 1uF cap dominates)} -500 -190 0 0 0.35 0.35 {}

T {This subcircuit is kept as a placeholder with no devices.} -500 -120 0 0 0.4 0.4 {layer=5}
T {Miller comp REMOVED -- inner EA Cc/Rc (40pF/5k) handles pole-splitting} -500 -80 0 0 0.3 0.3 {}
T {Outer Cc+Rz was redundant, killing bandwidth (UGB=170Hz with it)} -500 -50 0 0 0.3 0.3 {}
T {Output Cout REMOVED -- 1uF external cap dominates} -500 -20 0 0 0.3 0.3 {}
