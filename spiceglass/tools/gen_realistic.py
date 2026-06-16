"""Realistic analog netlist generator — parameterized REAL topologies.

Unlike gen_netlists.py (a random-wiring robustness fuzzer that produces
electrically-meaningless nets), every template here is an actual analog
circuit with correct internal wiring: real input/bias/signal paths, no
floating gates, matched pairs matched. Variation comes from randomized
device sizes, mirror ratios, stage counts and structural options — so the
output is realistic AND diverse, suitable as a benchmark and as training
data (netlist <-> known-correct topology).

    python tools/gen_realistic.py --count 3000 --out benchmark/real --seed 1
    python tools/benchmark.py     --dir benchmark/real
"""
import argparse
import os
import random


def W(rng, lo=2, hi=40):
    return f"{rng.choice([1, 2, 4, 6, 8, 10, 16, 20, 32, 40])}u"


def L(rng):
    return rng.choice(["0.18u", "0.35u", "0.5u", "1u", "2u"])


def Rv(rng):
    return rng.choice(["1k", "2k", "5k", "10k", "20k", "50k", "100k"])


def Cv(rng):
    return rng.choice(["100f", "250f", "500f", "1p", "2p", "5p", "10p"])


# Each template returns (name, ports, lines). Wiring is fixed & correct;
# only sizes/ratios/counts vary.

def ota_5t(r):
    w1, w2, w3, l = W(r), W(r), W(r), L(r)
    return ("ota_5t", "inp inn out vdd gnd vbias", [
        "** ===== Input Pair =====",
        f"M1 d1  inp tail gnd nmos W={w1} L={l}",
        f"M2 out inn tail gnd nmos W={w1} L={l}",
        "** ===== Mirror Load =====",
        f"M3 d1  d1 vdd vdd pmos W={w2} L={l}",
        f"M4 out d1 vdd vdd pmos W={w2} L={l}",
        "** ===== Tail =====",
        f"M5 tail vbias gnd gnd nmos W={w3} L={l}"])


def ota_two_stage(r):
    w1, w2, w3, w4, w5, l = (W(r), W(r), W(r), W(r), W(r), L(r))
    lines = [
        "** ===== Stage 1 (5T) =====",
        f"M1 n1 inp tail gnd nmos W={w1} L={l}",
        f"M2 n2 inn tail gnd nmos W={w1} L={l}",
        f"M3 n1 n1 vdd vdd pmos W={w2} L={l}",
        f"M4 n2 n1 vdd vdd pmos W={w2} L={l}",
        f"M5 tail vbias gnd gnd nmos W={w3} L={l}",
        "** ===== Stage 2 (CS + Miller) =====",
        f"M6 out n2 vdd vdd pmos W={w4} L={l}",
        f"M7 out vbias gnd gnd nmos W={w5} L={l}",
        f"Cc out n2 {Cv(r)}"]
    if r.random() < 0.5:                       # nulling resistor variant
        lines[-1] = f"Rz out nz {Rv(r)}"
        lines.append(f"Cc nz n2 {Cv(r)}")
    return ("ota_two_stage_miller", "inp inn out vdd gnd vbias", lines)


def ota_telescopic(r):
    w, l = W(r), L(r)
    return ("ota_telescopic", "inp inn out vdd gnd vbn vbc vbp vbpc", [
        "** ===== Input Pair =====",
        f"M1 a inp tail gnd nmos W={w} L={l}",
        f"M2 b inn tail gnd nmos W={w} L={l}",
        f"M9 tail vbn gnd gnd nmos W={W(r)} L={l}",
        "** ===== NMOS Cascodes =====",
        f"M3 c vbc a gnd nmos W={w} L={l}",
        f"M4 out vbc b gnd nmos W={w} L={l}",
        "** ===== PMOS Cascode Load =====",
        f"M5 c vbpc d vdd pmos W={w} L={l}",
        f"M6 out vbpc e vdd pmos W={w} L={l}",
        f"M7 d vbp vdd vdd pmos W={w} L={l}",
        f"M8 e vbp vdd vdd pmos W={w} L={l}"])


def ota_folded_cascode(r):
    w, l = W(r), L(r)
    return ("ota_folded_cascode",
            "inp inn out vdd gnd vbp vbpc vbnc", [
        "** ===== Input Pair (PMOS) =====",
        f"M1 fa inp tail vdd pmos W={w} L={l}",
        f"M2 fb inn tail vdd pmos W={w} L={l}",
        f"M3 tail vbp vdd vdd pmos W={W(r)} L={l}",
        "** ===== Folding Current Sources =====",
        f"M4 fa vbp vdd vdd pmos W={w} L={l}",
        f"M5 fb vbp vdd vdd pmos W={w} L={l}",
        "** ===== PMOS Cascodes =====",
        f"M6 c   vbpc fa vdd pmos W={w} L={l}",
        f"M7 out vbpc fb vdd pmos W={w} L={l}",
        "** ===== NMOS Cascode Mirror =====",
        f"M8 c   vbnc na gnd nmos W={w} L={l}",
        f"M9 out vbnc nb gnd nmos W={w} L={l}",
        f"M10 na c gnd gnd nmos W={w} L={l}",
        f"M11 nb c gnd gnd nmos W={w} L={l}"])


def mirror_bank(r):
    k = r.randint(2, 5)
    base = r.choice([1, 2, 4]); l = L(r)
    lines = ["** ===== Reference (diode) =====",
             f"M0 iref iref gnd gnd nmos W={base*4}u L={l}"]
    ports = ["vdd", "gnd", "iref"]
    lines.append("** ===== Mirror Outputs =====")
    for i in range(1, k + 1):
        ports.append(f"io{i}")
        lines.append(f"M{i} io{i} iref gnd gnd nmos W={base*r.choice([1,2,4])}u L={l}")
    return ("current_mirror_bank", " ".join(ports), lines)


def cascode_mirror(r):
    l = W(r), L(r)
    w, l = l
    return ("cascode_mirror", "vdd gnd iref io1 io2", [
        "** ===== Diode Stack =====",
        f"M0 vc vc iref gnd nmos W={w} L={l}",
        f"M1 iref vb gnd gnd nmos W={w} L={l}",
        f"M2 vb vb gnd gnd nmos W={w} L={l}",
        "** ===== Outputs =====",
        f"M3 a vb gnd gnd nmos W={w} L={l}",
        f"M4 io1 vc a gnd nmos W={w} L={l}",
        f"M5 b vb gnd gnd nmos W={w} L={l}",
        f"M6 io2 vc b gnd nmos W={w} L={l}"])


def wilson_mirror(r):
    w, l = W(r), L(r)
    return ("wilson_mirror", "vdd gnd iref iout", [
        f"M1 iref iref n1 gnd nmos W={w} L={l}",
        f"M2 n1 n1 gnd gnd nmos W={w} L={l}",
        f"M3 iout iref n2 gnd nmos W={w} L={l}",
        f"M4 n2 n1 gnd gnd nmos W={w} L={l}"])


def beta_multiplier(r):
    w, l = W(r), L(r)
    return ("beta_multiplier_bias", "vdd gnd vbiasn vbiasp", [
        "** ===== PMOS Mirror =====",
        f"M1 nl vbiasp vdd vdd pmos W={w} L={l}",
        f"M2 nr vbiasp vdd vdd pmos W={w} L={l}",
        "** ===== NMOS + Degeneration =====",
        f"M3 nl nr gnd gnd nmos W={w} L={l}",
        f"M4 nr nr ns gnd nmos W={4*4}u L={l}",
        f"Rs ns gnd {Rv(r)}",
        f"M5 vbiasp nl vdd vdd pmos W={w} L={l}",
        f"M6 vbiasn nl gnd gnd nmos W={w} L={l}"])


def comparator(r):
    w, l = W(r), L(r)
    return ("comparator", "inp inn out vdd gnd vbias", [
        "** ===== Input Pair =====",
        f"M1 d1 inp tail gnd nmos W={w} L={l}",
        f"M2 d2 inn tail gnd nmos W={w} L={l}",
        f"M5 tail vbias gnd gnd nmos W={w} L={l}",
        "** ===== Mirror Load =====",
        f"M3 d1 d1 vdd vdd pmos W={w} L={l}",
        f"M4 d2 d1 vdd vdd pmos W={w} L={l}",
        "** ===== Output Inverter =====",
        f"M6 out d2 vdd vdd pmos W={W(r)} L={l}",
        f"M7 out d2 gnd gnd nmos W={W(r)} L={l}"])


def inverter_chain(r):
    n = r.randint(2, 5); l = L(r); lines = []; w = r.choice([1, 2])
    ports = ["vdd", "gnd", "in", "out"]
    prev = "in"
    for i in range(n):
        nxt = "out" if i == n - 1 else f"n{i}"
        lines += [f"** ===== Inverter {i+1} =====",
                  f"Mp{i} {nxt} {prev} vdd vdd pmos W={w*2}u L={l}",
                  f"Mn{i} {nxt} {prev} gnd gnd nmos W={w}u L={l}"]
        prev = nxt; w *= 3
    lines.append(f"CL out gnd {Cv(r)}")
    return ("inverter_chain", " ".join(ports), lines)


def level_shifter(r):
    w, l = W(r), L(r)
    return ("level_shifter", "in vdd svdd gnd out", [
        "** ===== LV Input =====",
        f"Mi1 inb in vdd vdd pmos W={w} L={l}",
        f"Mi2 inb in gnd gnd nmos W={w} L={l}",
        "** ===== Pull-down Drivers =====",
        f"M1 a in gnd gnd nmos W={w} L={l}",
        f"M2 b inb gnd gnd nmos W={w} L={l}",
        "** ===== Cross-coupled PMOS (HV) =====",
        f"M3 a b svdd svdd pmos W={w} L={l}",
        f"M4 b a svdd svdd pmos W={w} L={l}",
        "** ===== HV Output =====",
        f"Mo1 out b svdd svdd pmos W={w} L={l}",
        f"Mo2 out b gnd gnd nmos W={w} L={l}"])


def nand2(r):
    w, l = W(r), L(r)
    return ("cmos_nand2", "a b out vdd gnd", [
        f"M1 out a vdd vdd pmos W={w} L={l}",
        f"M2 out b vdd vdd pmos W={w} L={l}",
        f"M3 out a mid gnd nmos W={w} L={l}",
        f"M4 mid b gnd gnd nmos W={w} L={l}"])


def common_source(r):
    w, l = W(r), L(r)
    return ("common_source", "in out vdd gnd vbias", [
        "** ===== Gain Device =====",
        f"M1 out in gnd gnd nmos W={w} L={l}",
        "** ===== Current-source Load =====",
        f"M2 out vbias vdd vdd pmos W={W(r)} L={l}"])


def rc_filter(r):
    n = r.randint(2, 4); lines = []; prev = "in"
    ports = ["in", "out", "gnd"]
    for i in range(n):
        nxt = "out" if i == n - 1 else f"m{i}"
        lines += [f"** ===== Stage {i+1} =====",
                  f"R{i} {prev} {nxt} {Rv(r)}",
                  f"C{i} {nxt} gnd {Cv(r)}"]
        prev = nxt
    return ("rc_filter", " ".join(ports), lines)


def bandgap_core(r):
    return ("bandgap_core", "vdd gnd vbg", [
        "** ===== PTAT BJT Branches =====",
        "Q1 vc1 vc1 gnd npn",
        "Q2 vc2 vc2 ne npn",
        f"R1 ne gnd {Rv(r)}",
        "** ===== Amp + Mirror =====",
        f"M1 vc1 vc1 vdd vdd pmos W={W(r)} L={L(r)}",
        f"M2 vc2 vc1 vdd vdd pmos W={W(r)} L={L(r)}",
        f"M3 vbg vc1 vdd vdd pmos W={W(r)} L={L(r)}",
        f"R2 vbg vbg2 {Rv(r)}",
        "Q3 vbg2 vbg2 gnd npn"])


def class_ab_output(r):
    w, l = W(r), L(r)
    return ("class_ab_output", "in out vdd gnd vbn vbp", [
        "** ===== Bias =====",
        f"M1 gp vbp vdd vdd pmos W={w} L={l}",
        f"M2 gn vbn gnd gnd nmos W={w} L={l}",
        "** ===== Driver =====",
        f"M3 gp in vdd vdd pmos W={w} L={l}",
        f"M4 gn in gnd gnd nmos W={w} L={l}",
        "** ===== Output =====",
        f"M5 out gp vdd vdd pmos W={4*8}u L={l}",
        f"M6 out gn gnd gnd nmos W={4*8}u L={l}"])


def ota_fulldiff_cmfb(r):
    w, l = W(r), L(r)
    return ("ota_fulldiff_cmfb", "inp inn outp outn vdd gnd vbn", [
        "** ===== Input Pair =====",
        f"M1 outp inp tail gnd nmos W={w} L={l}",
        f"M2 outn inn tail gnd nmos W={w} L={l}",
        f"M5 tail vbn gnd gnd nmos W={W(r)} L={l}",
        "** ===== PMOS Loads (CMFB) =====",
        f"M3 outp vcmfb vdd vdd pmos W={w} L={l}",
        f"M4 outn vcmfb vdd vdd pmos W={w} L={l}",
        "** ===== CMFB Sense =====",
        f"R1 outp vcm {Rv(r)}", f"R2 outn vcm {Rv(r)}",
        f"M6 vcmfb vcm gnd gnd nmos W={w} L={l}"])


def cascode_amp(r):
    w, l = W(r), L(r)
    return ("cascode_amp", "in out vdd gnd vbc vbp", [
        f"M1 mid in gnd gnd nmos W={w} L={l}",
        f"M2 out vbc mid gnd nmos W={w} L={l}",
        f"M3 out vbp vdd vdd pmos W={W(r)} L={l}"])


def diff_pair_res_load(r):
    w, l = W(r), L(r)
    return ("diff_pair_res_load", "inp inn outp outn vdd gnd vbn", [
        f"M1 outp inp tail gnd nmos W={w} L={l}",
        f"M2 outn inn tail gnd nmos W={w} L={l}",
        f"M3 tail vbn gnd gnd nmos W={W(r)} L={l}",
        f"R1 vdd outp {Rv(r)}", f"R2 vdd outn {Rv(r)}"])


def widlar_mirror(r):
    w, l = W(r), L(r)
    return ("widlar_mirror", "vdd gnd iref iout", [
        f"M1 iref iref gnd gnd nmos W={w} L={l}",
        f"M2 iout iref ns gnd nmos W={w} L={l}",
        f"Rs ns gnd {Rv(r)}"])


def peaking_current_source(r):
    w, l = W(r), L(r)
    return ("peaking_current_source", "vdd gnd iref iout", [
        f"M1 iref iref gnd gnd nmos W={w} L={l}",
        f"R1 iref g {Rv(r)}",
        f"M2 iout g gnd gnd nmos W={w} L={l}"])


def lv_cascode_mirror(r):
    w, l = W(r), L(r)
    return ("lv_cascode_mirror", "vdd gnd iref iout vbc", [
        f"M1 a iref gnd gnd nmos W={w} L={l}",
        f"M2 iref vbc a gnd nmos W={w} L={l}",
        f"M3 b iref gnd gnd nmos W={w} L={l}",
        f"M4 iout vbc b gnd nmos W={w} L={l}"])


def brokaw_bandgap(r):
    return ("brokaw_bandgap", "vdd gnd vbg", [
        "Q1 c1 vbg gnd npn", "Q2 c2 vbg ne npn",
        f"R1 ne gnd {Rv(r)}", f"R2 vbg gnd {Rv(r)}",
        f"M1 c1 c2 vdd vdd pmos W={W(r)} L={L(r)}",
        f"M2 c2 c2 vdd vdd pmos W={W(r)} L={L(r)}",
        f"M3 vbg c1 vdd vdd pmos W={W(r)} L={L(r)}"])


def vbe_multiplier(r):
    return ("vbe_multiplier", "top bot", [
        "Q1 top mid bot npn",
        f"R1 top mid {Rv(r)}",
        f"R2 mid bot {Rv(r)}"])


def strongarm_latch(r):
    w, l = W(r), L(r)
    return ("strongarm_latch", "inp inn outp outn clk vdd gnd", [
        f"M0 tail clk gnd gnd nmos W={W(r)} L={l}",
        "** ===== Input Pair =====",
        f"M1 dp inp tail gnd nmos W={w} L={l}",
        f"M2 dn inn tail gnd nmos W={w} L={l}",
        "** ===== Cross-coupled =====",
        f"M3 outp outn dp gnd nmos W={w} L={l}",
        f"M4 outn outp dn gnd nmos W={w} L={l}",
        f"M5 outp outn vdd vdd pmos W={w} L={l}",
        f"M6 outn outp vdd vdd pmos W={w} L={l}",
        "** ===== Precharge =====",
        f"M7 outp clk vdd vdd pmos W={w} L={l}",
        f"M8 outn clk vdd vdd pmos W={w} L={l}"])


def double_tail_comparator(r):
    w, l = W(r), L(r)
    return ("double_tail_comparator", "inp inn outp outn clk vdd gnd", [
        f"M0 t1 clk gnd gnd nmos W={W(r)} L={l}",
        f"M1 dp inp t1 gnd nmos W={w} L={l}",
        f"M2 dn inn t1 gnd nmos W={w} L={l}",
        f"M3 dp clk vdd vdd pmos W={w} L={l}",
        f"M4 dn clk vdd vdd pmos W={w} L={l}",
        "** ===== Latch Stage =====",
        f"M5 outp dn vdd vdd pmos W={w} L={l}",
        f"M6 outn dp vdd vdd pmos W={w} L={l}",
        f"M7 outp outn gnd gnd nmos W={w} L={l}",
        f"M8 outn outp gnd gnd nmos W={w} L={l}"])


def hysteresis_comparator(r):
    w, l = W(r), L(r)
    return ("hysteresis_comparator", "inp inn out vdd gnd vbn", [
        f"M1 dp inp tail gnd nmos W={w} L={l}",
        f"M2 dn inn tail gnd nmos W={w} L={l}",
        f"M5 tail vbn gnd gnd nmos W={w} L={l}",
        "** ===== Cross-coupled Load (hysteresis) =====",
        f"M3 dp dn vdd vdd pmos W={w} L={l}",
        f"M4 dn dp vdd vdd pmos W={w} L={l}",
        f"M6 out dn vdd vdd pmos W={W(r)} L={l}",
        f"M7 out dn gnd gnd nmos W={W(r)} L={l}"])


def ring_oscillator(r):
    n = r.choice([3, 5, 7]); l = L(r)
    nodes = ["out"] + [f"r{i}" for i in range(1, n)]
    lines = [f"** {n}-stage ring"]
    for i in range(n):
        a, b = nodes[i], nodes[(i + 1) % n]
        lines += [f"Mp{i} {b} {a} vdd vdd pmos W=2u L={l}",
                  f"Mn{i} {b} {a} gnd gnd nmos W=1u L={l}"]
    return ("ring_oscillator", "out vdd gnd", lines)


def gilbert_cell(r):
    w, l = W(r), L(r)
    return ("gilbert_cell", "lop lon rfp rfn outp outn vdd gnd vbn", [
        f"M0 tail vbn gnd gnd nmos W={W(r)} L={l}",
        "** ===== RF Pair =====",
        f"M1 a rfp tail gnd nmos W={w} L={l}",
        f"M2 b rfn tail gnd nmos W={w} L={l}",
        "** ===== LO Quad =====",
        f"M3 outp lop a gnd nmos W={w} L={l}",
        f"M4 outn lon a gnd nmos W={w} L={l}",
        f"M5 outp lon b gnd nmos W={w} L={l}",
        f"M6 outn lop b gnd nmos W={w} L={l}",
        f"R1 vdd outp {Rv(r)}", f"R2 vdd outn {Rv(r)}"])


def lc_vco(r):
    w, l = W(r), L(r)
    return ("lc_vco", "outp outn vdd gnd vbn", [
        "** ===== LC Tank =====",
        f"L1 vdd outp {Cv(r)}", f"L2 vdd outn {Cv(r)}",
        f"C1 outp outn {Cv(r)}",
        "** ===== Cross-coupled Pair =====",
        f"M1 outp outn t gnd nmos W={w} L={l}",
        f"M2 outn outp t gnd nmos W={w} L={l}",
        f"M3 t vbn gnd gnd nmos W={W(r)} L={l}"])


def gate_driver(r):
    w, l = W(r), L(r)
    return ("gate_driver", "in out vdd gnd", [
        f"M1 a in vdd vdd pmos W={2*r.choice([2,4])}u L={l}",
        f"M2 a in gnd gnd nmos W={r.choice([2,4])}u L={l}",
        f"M3 out a vdd vdd pmos W={4*8}u L={l}",
        f"M4 out a gnd gnd nmos W={4*8}u L={l}"])


def hbridge_leg(r):
    w, l = W(r), L(r)
    return ("hbridge_leg", "hin lin sw vdd gnd", [
        f"M1 sw hin vdd vdd pmos W={4*8}u L={l}",
        f"M2 sw lin gnd gnd nmos W={4*8}u L={l}"])


def charge_pump(r):
    return ("charge_pump", "clk vin vout gnd", [
        "** ===== Dickson Stages =====",
        "D1 vin a diode", f"C1 a clk {Cv(r)}",
        "D2 a b diode", f"C2 b gnd {Cv(r)}",
        "D3 b vout diode", f"C3 vout gnd {Cv(r)}"])


def nor2(r):
    w, l = W(r), L(r)
    return ("cmos_nor2", "a b out vdd gnd", [
        f"M1 mid a vdd vdd pmos W={w} L={l}",
        f"M2 out b mid vdd pmos W={w} L={l}",
        f"M3 out a gnd gnd nmos W={w} L={l}",
        f"M4 out b gnd gnd nmos W={w} L={l}"])


def transmission_gate(r):
    w, l = W(r), L(r)
    return ("transmission_gate", "in out en enb vdd gnd", [
        f"M1 in en out gnd nmos W={w} L={l}",
        f"M2 in enb out vdd pmos W={w} L={l}"])


def schmitt(r):
    w, l = W(r), L(r)
    return ("schmitt_trigger", "in out vdd gnd", [
        f"M1 a in vdd vdd pmos W={w} L={l}",
        f"M2 out in a vdd pmos W={w} L={l}",
        f"M3 b in gnd gnd nmos W={w} L={l}",
        f"M4 out in b gnd nmos W={w} L={l}",
        f"M5 a out vdd vdd pmos W={w} L={l}",
        f"M6 b out gnd gnd nmos W={w} L={l}"])


def esd_clamp(r):
    return ("esd_clamp", "pad vdd gnd", [
        "D1 pad vdd diode", "D2 gnd pad diode",
        f"R1 pad n1 {Rv(r)}",
        f"M1 vdd n1 gnd gnd nmos W={4*16}u L={L(r)}",
        f"C1 n1 gnd {Cv(r)}"])


def peak_detector(r):
    w, l = W(r), L(r)
    return ("peak_detector", "in out vdd gnd vbn", [
        f"M1 d1 in tail gnd nmos W={w} L={l}",
        f"M2 d2 out tail gnd nmos W={w} L={l}",
        f"M5 tail vbn gnd gnd nmos W={w} L={l}",
        f"M3 d1 d1 vdd vdd pmos W={w} L={l}",
        f"M4 d2 d1 vdd vdd pmos W={w} L={l}",
        "D1 d2 out diode", f"Ch out gnd {Cv(r)}"])


def sample_hold(r):
    w, l = W(r), L(r)
    return ("sample_hold", "in out clk clkb vdd gnd", [
        f"M1 in clk hold gnd nmos W={w} L={l}",
        f"M2 in clkb hold vdd pmos W={w} L={l}",
        f"Ch hold gnd {Cv(r)}",
        "** ===== Buffer =====",
        f"M3 out hold vdd vdd pmos W={w} L={l}",
        f"M4 out hold gnd gnd nmos W={w} L={l}"])


def voltage_doubler(r):
    return ("voltage_doubler", "clk vin vout gnd", [
        "D1 vin a diode", f"C1 a clk {Cv(r)}",
        "D2 a vout diode", f"C2 vout gnd {Cv(r)}"])


def rc_ladder3(r):
    lines, prev = [], "in"
    for i in range(r.randint(3, 5)):
        nxt = "out" if i == 2 else f"m{i}"
        lines += [f"R{i} {prev} {nxt} {Rv(r)}", f"C{i} {nxt} gnd {Cv(r)}"]
        prev = nxt
    return ("rc_ladder", "in out gnd", lines)


def r2r_dac(r):
    n = r.choice([3, 4, 5]); lines = ["** R-2R ladder"]
    for i in range(n):
        lines += [f"Rs{i} node{i} node{i+1} 2k",
                  f"Rr{i} node{i} bit{i} 1k"]
    bits = " ".join(f"bit{i}" for i in range(n))
    return ("r2r_dac", f"out gnd {bits}",
            lines + [f"Rt node{n} out 2k"])


TEMPLATES = [ota_5t, ota_two_stage, ota_telescopic, ota_folded_cascode,
             mirror_bank, cascode_mirror, wilson_mirror, beta_multiplier,
             comparator, inverter_chain, level_shifter, nand2,
             common_source, rc_filter, bandgap_core, class_ab_output,
             ota_fulldiff_cmfb, cascode_amp, diff_pair_res_load,
             widlar_mirror, peaking_current_source, lv_cascode_mirror,
             brokaw_bandgap, vbe_multiplier, strongarm_latch,
             double_tail_comparator,
             hysteresis_comparator, ring_oscillator, gilbert_cell, lc_vco,
             gate_driver, hbridge_leg, charge_pump, nor2, transmission_gate,
             schmitt, esd_clamp, peak_detector, sample_hold, voltage_doubler,
             rc_ladder3, r2r_dac]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=3000)
    ap.add_argument("--out", default="benchmark/real")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rng = random.Random(args.seed)
    counts = {}
    for i in range(args.count):
        tmpl = rng.choice(TEMPLATES)
        base, ports, lines = tmpl(random.Random(rng.random()))
        counts[base] = counts.get(base, 0) + 1
        nm = f"{base}_{counts[base]:04d}"
        text = "\n".join([f"** {base} (realistic template variant)",
                          f".subckt {nm} {ports}"] + lines
                         + [f".ends {nm}"]) + "\n"
        with open(os.path.join(args.out, nm + ".cir"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    print(f"wrote {args.count} realistic netlists to {args.out}")
    for k in sorted(counts):
        print(f"  {k:24} {counts[k]}")


if __name__ == "__main__":
    main()
