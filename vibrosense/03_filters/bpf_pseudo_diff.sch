v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}

T {VibroSense Block 03: Pseudo-Differential BPF Channel} -200 -1200 0 0 0.65 0.65 {layer=15}
T {Tow-Thomas Biquad  --  Ch2: f0=1000 Hz, Q=0.67, C1=118 pF, C2=260 pF} -200 -1150 0 0 0.3 0.3 {layer=15}
T {6x ota_foldcasc + 4 Caps + 4 Pseudo-Resistors  |  Iref = 200 nA  |  Power = 4.7 uW} -200 -1115 0 0 0.25 0.25 {layer=8}
T {POSITIVE PATH} -150 -1060 0 0 0.35 0.35 {layer=4}
T {NEGATIVE PATH} -150 -500 0 0 0.35 0.35 {layer=4}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -350 -1000 0 1 {name=p_vinp lab=vinp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} -350 -440 0 1 {name=p_vinn lab=vinn}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1000 -1050 0 0 {name=p_bp_outp lab=bp_outp}
C {/usr/share/xschem/xschem_library/devices/iopin.sym} 1000 -490 0 0 {name=p_bp_outn lab=bp_outn}
C {ota_foldcasc.sym} 0 -1000 0 0 {name=Xota1p model=ota_foldcasc spiceprefix=X}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -1080 1 0 {name=l_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -920 3 0 {name=l_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -40 -920 3 0 {name=l_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -920 3 0 {name=l_vbcn lab=vbcn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -40 -1080 1 0 {name=l_vbp lab=vbp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -1080 1 0 {name=l_vbcp lab=vbcp}
T {OTA1p} -30 -910 0 0 0.25 0.25 {layer=8}
N -350 -1030 -100 -1030 {lab=vinp}
N 100 -1000 250 -1000 {lab=int1p}
N 700 -1000 700 -1100 {lab=int2p}
N 700 -1100 -140 -1100 {lab=int2p}
N -140 -1100 -140 -970 {lab=int2p}
N -140 -970 -100 -970 {lab=int2p}
C {ota_foldcasc.sym} 500 -1000 0 0 {name=Xota2p model=ota_foldcasc spiceprefix=X}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -1080 1 0 {name=l_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -920 3 0 {name=l_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 460 -920 3 0 {name=l_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 -920 3 0 {name=l_vbcn lab=vbcn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 460 -1080 1 0 {name=l_vbp lab=vbp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 -1080 1 0 {name=l_vbcp lab=vbcp}
T {OTA2p} 470 -910 0 0 0.25 0.25 {layer=8}
N 250 -1000 250 -1030 {lab=int1p}
N 250 -1030 400 -1030 {lab=int1p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -970 0 1 {name=l_vcm lab=vcm}
N 600 -1000 700 -1000 {lab=int2p}
C {ota_foldcasc.sym} 250 -780 0 0 {name=Xota3p model=ota_foldcasc spiceprefix=X}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -860 1 0 {name=l_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -700 3 0 {name=l_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -700 3 0 {name=l_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 290 -700 3 0 {name=l_vbcn lab=vbcn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -860 1 0 {name=l_vbp lab=vbp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 290 -860 1 0 {name=l_vbcp lab=vbcp}
T {OTA3p} 220 -690 0 0 0.25 0.25 {layer=8}
T {(damping)} 220 -670 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -810 0 1 {name=l_vcm lab=vcm}
N 250 -1000 250 -750 {lab=int1p}
N 250 -750 150 -750 {lab=int1p}
N 350 -780 400 -780 {lab=int1p}
N 400 -780 400 -1000 {lab=int1p}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 170 -780 0 0 {name=C1p m=1 value=118p footprint=1206 device="ceramic capacitor"}
T {C1p} 185 -790 0 0 0.22 0.22 {layer=8}
T {118p} 185 -772 0 0 0.18 0.18 {layer=8}
N 170 -1000 170 -800 {lab=int1p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 170 -760 3 0 {name=l_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 700 -780 0 0 {name=C2p m=1 value=260p footprint=1206 device="ceramic capacitor"}
T {C2p} 715 -790 0 0 0.22 0.22 {layer=8}
T {260p} 715 -772 0 0 0.18 0.18 {layer=8}
N 700 -1000 700 -800 {lab=int2p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -760 3 0 {name=l_vss lab=vss}
C {pseudo_res.sym} 100 -860 1 0 {name=Xpr1p model=pseudo_res spiceprefix=X}
N 100 -1000 100 -910 {lab=int1p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -810 3 0 {name=l_vcm lab=vcm}
C {pseudo_res.sym} 780 -860 1 0 {name=Xpr2p model=pseudo_res spiceprefix=X}
N 780 -1000 780 -910 {lab=int2p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -810 3 0 {name=l_vcm lab=vcm}
N 250 -1000 250 -1050 {lab=int1p}
N 250 -1050 1000 -1050 {lab=bp_outp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 260 -1015 0 0 {name=l_int1p lab=int1p}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 710 -1015 0 0 {name=l_int2p lab=int2p}
C {ota_foldcasc.sym} 0 -440 0 0 {name=Xota1n model=ota_foldcasc spiceprefix=X}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -520 1 0 {name=l_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 0 -360 3 0 {name=l_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -40 -360 3 0 {name=l_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -360 3 0 {name=l_vbcn lab=vbcn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} -40 -520 1 0 {name=l_vbp lab=vbp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 40 -520 1 0 {name=l_vbcp lab=vbcp}
T {OTA1n} -30 -350 0 0 0.25 0.25 {layer=8}
N -350 -470 -100 -470 {lab=vinn}
N 100 -440 250 -440 {lab=int1n}
N 700 -440 700 -540 {lab=int2n}
N 700 -540 -140 -540 {lab=int2n}
N -140 -540 -140 -410 {lab=int2n}
N -140 -410 -100 -410 {lab=int2n}
C {ota_foldcasc.sym} 500 -440 0 0 {name=Xota2n model=ota_foldcasc spiceprefix=X}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -520 1 0 {name=l_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 500 -360 3 0 {name=l_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 460 -360 3 0 {name=l_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 -360 3 0 {name=l_vbcn lab=vbcn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 460 -520 1 0 {name=l_vbp lab=vbp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 540 -520 1 0 {name=l_vbcp lab=vbcp}
T {OTA2n} 470 -350 0 0 0.25 0.25 {layer=8}
N 250 -440 250 -470 {lab=int1n}
N 250 -470 400 -470 {lab=int1n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 400 -410 0 1 {name=l_vcm lab=vcm}
N 600 -440 700 -440 {lab=int2n}
C {ota_foldcasc.sym} 250 -220 0 0 {name=Xota3n model=ota_foldcasc spiceprefix=X}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -300 1 0 {name=l_vdd lab=vdd}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 250 -140 3 0 {name=l_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -140 3 0 {name=l_vbn lab=vbn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 290 -140 3 0 {name=l_vbcn lab=vbcn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 210 -300 1 0 {name=l_vbp lab=vbp}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 290 -300 1 0 {name=l_vbcp lab=vbcp}
T {OTA3n} 220 -130 0 0 0.25 0.25 {layer=8}
T {(damping)} 220 -110 0 0 0.2 0.2 {layer=5}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 150 -250 0 1 {name=l_vcm lab=vcm}
N 250 -440 250 -190 {lab=int1n}
N 250 -190 150 -190 {lab=int1n}
N 350 -220 400 -220 {lab=int1n}
N 400 -220 400 -440 {lab=int1n}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 170 -220 0 0 {name=C1n m=1 value=118p footprint=1206 device="ceramic capacitor"}
T {C1n} 185 -230 0 0 0.22 0.22 {layer=8}
T {118p} 185 -212 0 0 0.18 0.18 {layer=8}
N 170 -440 170 -240 {lab=int1n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 170 -200 3 0 {name=l_vss lab=vss}
C {/usr/share/xschem/xschem_library/devices/capa.sym} 700 -220 0 0 {name=C2n m=1 value=260p footprint=1206 device="ceramic capacitor"}
T {C2n} 715 -230 0 0 0.22 0.22 {layer=8}
T {260p} 715 -212 0 0 0.18 0.18 {layer=8}
N 700 -440 700 -240 {lab=int2n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 700 -200 3 0 {name=l_vss lab=vss}
C {pseudo_res.sym} 100 -300 1 0 {name=Xpr1n model=pseudo_res spiceprefix=X}
N 100 -440 100 -350 {lab=int1n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 100 -250 3 0 {name=l_vcm lab=vcm}
C {pseudo_res.sym} 780 -300 1 0 {name=Xpr2n model=pseudo_res spiceprefix=X}
N 780 -440 780 -350 {lab=int2n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 780 -250 3 0 {name=l_vcm lab=vcm}
N 250 -440 250 -490 {lab=int1n}
N 250 -490 1000 -490 {lab=bp_outn}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 260 -455 0 0 {name=l_int1n lab=int1n}
C {/usr/share/xschem/xschem_library/devices/lab_pin.sym} 710 -455 0 0 {name=l_int2n lab=int2n}
T {Vout_diff = bp_outp - bp_outn} 800 -1080 0 0 0.22 0.22 {layer=4}
T {(HD2 cancelled by pseudo-diff topology)} 800 -1060 0 0 0.18 0.18 {layer=5}
T {Shared bias: VBN, VBCN, VBP, VBCP from ota_bias_dist} -150 -130 0 0 0.22 0.22 {layer=4}
T {PR = back-to-back PMOS W=0.42u L=10u (>100 GOhm DC bias)} -150 -105 0 0 0.18 0.18 {layer=5}
