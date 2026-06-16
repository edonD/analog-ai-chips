"""Hierarchical multi-block system generator for the conversion benchmark.

Real chips nest blocks: a bandgap feeds an LDO, a TIA feeds a filter feeds
a comparator, an oscillator feeds a buffer. gen_realistic.py covers the
leaf blocks; this composes them into TOP subckts that instantiate the
leaves via X-instances (kind="sub" — drawn as wired block boxes), with
supplies/bias shared by name and signals chained stage-to-stage.

Each emitted file is self-contained: the TOP subckt first (so the default
benchmark, which converts the first non-empty subckt, exercises the
hierarchy), then the leaf .subckt definitions it uses.

    python tools/gen_hier.py --count 2000 --out benchmark/hier --seed 1
    python tools/gen_hier.py --list           # show the system catalog
"""
import argparse
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from gen_realistic import (                                   # noqa: E402
    Cv, ota_5t, ldo, bandgap_core, comparator, tia, sallen_key_lp,
    sample_hold, strongarm_latch, ring_oscillator, inverter_chain,
    class_ab_output, common_source, rc_filter, lna_cascode, gm_c_biquad,
    cascode_mirror, mirror_bank, gate_driver, buck_power_stage)


def block(fn, r, slot):
    base, ports, lines = fn(r)
    return {"name": f"{base}_{slot}", "ports": ports.split(), "lines": lines}


def nets_for(b, mapping):
    """Net list aligned to the block's port order. Unmapped ports default
    to themselves: vdd/gnd/svdd and named bias rails (vbn, vbias, ...) are
    thereby shared across blocks and exposed at the top."""
    return [mapping.get(p, p) for p in b["ports"]]


def emit(name, sysname, insts, top_ports, extra=None):
    out = [f"** {sysname} (hierarchical system)"]
    out.append(f".subckt {name} " + " ".join(top_ports))
    for inst, b, nets in insts:
        out.append(f"X{inst} " + " ".join(nets) + f" {b['name']}")
    out += extra or []
    out.append(".ends")
    seen = set()
    for _, b, _ in insts:
        if b["name"] in seen:
            continue
        seen.add(b["name"])
        out.append(f".subckt {b['name']} " + " ".join(b["ports"]))
        out += b["lines"]
        out.append(".ends")
    return "\n".join(out) + "\n"


# ---- system catalog: each composes real leaf blocks with correct wiring

def sys_bandgap_ldo(name, r):
    bg = block(bandgap_core, r, "bg"); reg = block(ldo, r, "reg")
    insts = [("bg", bg, nets_for(bg, {"vbg": "vref"})),
             ("reg", reg, nets_for(reg, {"vout": "vout"}))]
    return emit(name, "bandgap_ldo", insts, ["vdd", "gnd", "vout", "vbn"],
                [f"Cout vout gnd {Cv(r)}"])


def sys_sensor_chain(name, r):
    a = block(tia, r, "tia"); f = block(sallen_key_lp, r, "flt")
    c = block(comparator, r, "cmp")
    insts = [("tia", a, nets_for(a, {"in": "pin", "out": "s1"})),
             ("flt", f, nets_for(f, {"in": "s1", "out": "s2"})),
             ("cmp", c, nets_for(c, {"inp": "s2", "inn": "vref",
                                     "out": "dout"}))]
    return emit(name, "sensor_chain", insts,
                ["pin", "vref", "dout", "vdd", "gnd", "vbn", "vbias"])


def sys_amp_output(name, r):
    a = block(ota_5t, r, "ota"); o = block(class_ab_output, r, "out")
    insts = [("ota", a, nets_for(a, {"out": "s1"})),
             ("out", o, nets_for(o, {"in": "s1", "out": "aout"}))]
    return emit(name, "amp_output_stage", insts,
                ["inp", "inn", "aout", "vdd", "gnd", "vbias", "vbn", "vbp"])


def sys_two_stage_amp(name, r):
    a = block(ota_5t, r, "s1"); b = block(common_source, r, "s2")
    insts = [("s1", a, nets_for(a, {"out": "m"})),
             ("s2", b, nets_for(b, {"in": "m", "out": "aout"}))]
    return emit(name, "two_stage_amp", insts,
                ["inp", "inn", "aout", "vdd", "gnd", "vbias"])


def sys_adc_frontend(name, r):
    s = block(sample_hold, r, "sh"); c = block(comparator, r, "cmp")
    insts = [("sh", s, nets_for(s, {"in": "ain", "out": "s1"})),
             ("cmp", c, nets_for(c, {"inp": "s1", "inn": "vref",
                                     "out": "dout"}))]
    return emit(name, "adc_frontend", insts,
                ["ain", "vref", "dout", "clk", "clkb",
                 "vdd", "gnd", "vbias"])


def sys_comparator_buffer(name, r):
    c = block(strongarm_latch, r, "cmp"); b = block(inverter_chain, r, "buf")
    insts = [("cmp", c, nets_for(c, {"outp": "s1"})),
             ("buf", b, nets_for(b, {"in": "s1", "out": "dout"}))]
    return emit(name, "comparator_buffer", insts,
                ["inp", "inn", "outn", "dout", "clk", "vdd", "gnd"])


def sys_clock_gen(name, r):
    o = block(ring_oscillator, r, "osc"); b = block(inverter_chain, r, "buf")
    insts = [("osc", o, nets_for(o, {"out": "s1"})),
             ("buf", b, nets_for(b, {"in": "s1", "out": "clkout"}))]
    return emit(name, "clock_gen", insts, ["clkout", "vdd", "gnd"])


def sys_bias_distribution(name, r):
    a = block(cascode_mirror, r, "ref"); b = block(mirror_bank, r, "fan")
    insts = [("ref", a, nets_for(a, {"io1": "io1", "io2": "io2"})),
             ("fan", b, nets_for(b, {"io1": "m1", "io2": "m2",
                                     "io3": "m3", "io4": "m4"}))]
    return emit(name, "bias_distribution", insts,
                ["vdd", "gnd", "iref", "io1", "io2", "m1", "m2", "m3", "m4"])


def sys_rf_receiver(name, r):
    a = block(lna_cascode, r, "lna"); f = block(gm_c_biquad, r, "if")
    insts = [("lna", a, nets_for(a, {"out": "rf"})),
             ("if", f, nets_for(f, {"in": "rf", "out": "ifout"}))]
    return emit(name, "rf_receiver", insts,
                ["rfin", "ifout", "vdd", "gnd", "vbias", "vbc", "vbn"])


def sys_filter_cascade(name, r):
    a = block(rc_filter, r, "pre"); b = block(sallen_key_lp, r, "biq")
    insts = [("pre", a, nets_for(a, {"in": "fin", "out": "s1"})),
             ("biq", b, nets_for(b, {"in": "s1", "out": "fout"}))]
    return emit(name, "filter_cascade", insts,
                ["fin", "fout", "vdd", "gnd", "vbn"])


def sys_gate_drive(name, r):
    g = block(gate_driver, r, "drv"); p = block(buck_power_stage, r, "pwr")
    insts = [("drv", g, nets_for(g, {"in": "pwm", "out": "hg"})),
             ("pwr", p, nets_for(p, {"hin": "hg"}))]
    return emit(name, "gate_drive_stage", insts,
                ["pwm", "lin", "sw", "vdd", "gnd"])


def sys_afe_chain(name, r):
    a = block(tia, r, "tia"); f = block(gm_c_biquad, r, "flt")
    o = block(class_ab_output, r, "buf")
    insts = [("tia", a, nets_for(a, {"in": "pin", "out": "s1"})),
             ("flt", f, nets_for(f, {"in": "s1", "out": "s2"})),
             ("buf", o, nets_for(o, {"in": "s2", "out": "aout"}))]
    return emit(name, "analog_frontend", insts,
                ["pin", "aout", "vdd", "gnd", "vbn", "vbp"])


SYSTEMS = [sys_bandgap_ldo, sys_sensor_chain, sys_amp_output,
           sys_two_stage_amp, sys_adc_frontend, sys_comparator_buffer,
           sys_clock_gen, sys_bias_distribution, sys_rf_receiver,
           sys_filter_cascade, sys_gate_drive, sys_afe_chain]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=2000)
    ap.add_argument("--out", default="benchmark/hier")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        for s in SYSTEMS:
            print("  " + s.__name__[4:])
        print(f"\n{len(SYSTEMS)} systems")
        return
    os.makedirs(args.out, exist_ok=True)
    rng = random.Random(args.seed)
    for i in range(args.count):
        sysfn = SYSTEMS[i % len(SYSTEMS)]
        r = random.Random(rng.random())
        name = f"{sysfn.__name__[4:]}_{i:05d}"
        text = sysfn(name, r)
        with open(os.path.join(args.out, f"{name}.cir"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    print(f"wrote {args.count} hierarchical netlists to {args.out}")


if __name__ == "__main__":
    main()
