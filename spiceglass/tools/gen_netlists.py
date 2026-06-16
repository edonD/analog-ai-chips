"""Procedural analog/mixed-signal netlist generator for the conversion
benchmark — broad coverage to find what the converter can't yet handle.

Synthesizes valid ngspice .subckt netlists by composing randomized blocks
across the device/topology space: MOS/BJT/JFET stages, mirrors & cascodes,
diff pairs, bandgap/ references, logic gates & latches, level shifters,
diode rectifiers/clamps, LC/RC/RL passives, controlled sources (E/F/G/H),
behavioral B-sources, voltage switches, charge pumps. Correct-by-
construction; seeded for reproducibility.

    python tools/gen_netlists.py --count 10000 --out benchmark/gen10k --seed 1
    python tools/benchmark.py    --dir benchmark/gen10k
"""
import argparse
import os
import random


class Builder:
    def __init__(self, rng):
        self.rng = rng
        self.lines = []
        self.n = 0
        self.sig = 0
        self.nets = ["gnd", "vdd"]
        self.dual = rng.random() < 0.25     # some have a 2nd supply domain
        if self.dual:
            self.nets.append("svdd")

    def _w(self):
        return f"{self.rng.choice([1, 2, 4, 8, 10, 20, 40])}u"

    def _l(self):
        return self.rng.choice(["0.18u", "0.5u", "1u", "2u"])

    def _val(self):
        return self.rng.choice(["1k", "10k", "100k", "1meg", "100", "1p",
                               "10p", "1n", "100f", "1u", "10u"])

    def net(self, fresh=False):
        sigs = [x for x in self.nets if x not in ("gnd", "vdd", "svdd")]
        if fresh or self.rng.random() < 0.45 or len(sigs) < 2:
            self.sig += 1
            nm = f"n{self.sig}"
            self.nets.append(nm)
            return nm
        return self.rng.choice(sigs)

    def vrail(self):
        return self.rng.choice(["vdd", "svdd"]) if self.dual else "vdd"

    # ----- device primitives (all valid ngspice) -----
    def mos(self, kind, d, g, s):
        self.n += 1
        b = self.vrail() if kind == "pmos" else "gnd"
        self.lines.append(f"M{self.n} {d} {g} {s} {b} {kind} "
                          f"W={self._w()} L={self._l()}")

    def bjt(self, kind, c, b, e):
        self.n += 1
        self.lines.append(f"Q{self.n} {c} {b} {e} {kind}")

    def jfet(self, kind, d, g, s):
        self.n += 1
        self.lines.append(f"J{self.n} {d} {g} {s} {kind}")

    def dio(self, a, c, model="diode"):
        self.n += 1
        self.lines.append(f"D{self.n} {a} {c} {model}")

    def pas(self, ch, a, b):
        self.n += 1
        self.lines.append(f"{ch}{self.n} {a} {b} {self._val()}")

    def ctrl(self, letter, op, on):
        self.n += 1
        if letter in ("E", "G"):       # voltage-controlled (4 nodes)
            self.lines.append(f"{letter}{self.n} {op} {on} "
                              f"{self.net()} {self.net()} 2")
        else:                          # F/H current-controlled (sense V src)
            self.n += 1
            self.lines.append(f"Vs{self.n} {self.net()} {self.net()} 0")
            self.lines.append(f"{letter}{self.n} {op} {on} Vs{self.n} 2")

    def bsrc(self, p, n):
        self.n += 1
        self.lines.append(f"B{self.n} {p} {n} V=v({self.net()})*1.5")

    def vsw(self, a, b):
        self.n += 1
        self.lines.append(f"S{self.n} {a} {b} {self.net()} gnd sw")

    # ----- blocks -----
    def mirror(self):
        self.lines.append("** ===== Current Mirror =====")
        bias = self.net(True); self.mos("nmos", bias, bias, "gnd")
        for _ in range(self.rng.randint(1, 5)):
            self.mos("nmos", self.net(), bias, "gnd")

    def cascode_mirror(self):
        self.lines.append("** ===== Cascode Mirror =====")
        b1, b2 = self.net(True), self.net(True)
        self.mos("nmos", b1, b1, "gnd"); self.mos("nmos", b2, b2, b1)
        for _ in range(self.rng.randint(1, 3)):
            m = self.net(); self.mos("nmos", m, b1, "gnd")
            self.mos("nmos", self.net(), b2, m)

    def diffpair(self):
        self.lines.append("** ===== Differential Pair =====")
        tail = self.net(True); k = self.rng.choice(["nmos", "pmos"])
        op, on = self.net(True), self.net(True)
        self.mos(k, op, self.net(True), tail); self.mos(k, on, self.net(True), tail)
        self.mos("nmos", tail, self.net(), "gnd")
        ld = "pmos" if k == "nmos" else "nmos"; r = self.vrail() if ld == "pmos" else "gnd"
        g = self.net(True); self.mos(ld, op, g, r); self.mos(ld, on, g, r)

    def bjt_pair(self):
        self.lines.append("** ===== BJT Diff Pair =====")
        k = self.rng.choice(["npn", "pnp"]); tail = self.net(True)
        self.bjt(k, self.net(True), self.net(True), tail)
        self.bjt(k, self.net(True), self.net(True), tail)
        self.pas("R", tail, "gnd")

    def bandgap(self):
        self.lines.append("** ===== Bandgap Core =====")
        self.bjt("npn", "vdd", self.net(True), self.net(True))
        self.bjt("npn", "vdd", self.net(True), self.net(True))
        self.pas("R", self.net(), "gnd"); self.pas("R", self.net(), "gnd")

    def jfet_stage(self):
        self.lines.append("** ===== JFET Stage =====")
        k = self.rng.choice(["njf", "pjf"]); o = self.net(True)
        self.jfet(k, o, self.net(), "gnd"); self.pas("R", "vdd", o)

    def cs_stage(self):
        self.lines.append("** ===== Gain Stage =====")
        o = self.net(True); self.mos("nmos", o, self.net(), "gnd")
        self.mos("pmos", o, self.net(), self.vrail())

    def cascode(self):
        self.lines.append("** ===== Cascode =====")
        mid = self.net(True); self.mos("nmos", mid, self.net(), "gnd")
        self.mos("nmos", self.net(True), self.net(), mid)

    def inverter(self):
        self.lines.append("** ===== Inverter =====")
        i, o = self.net(), self.net(True)
        self.mos("pmos", o, i, self.vrail()); self.mos("nmos", o, i, "gnd")

    def nand(self):
        self.lines.append("** ===== NAND =====")
        a, b, o = self.net(), self.net(), self.net(True); mid = self.net(True)
        self.mos("pmos", o, a, "vdd"); self.mos("pmos", o, b, "vdd")
        self.mos("nmos", o, a, mid); self.mos("nmos", mid, b, "gnd")

    def latch(self):
        self.lines.append("** ===== Latch =====")
        q, qb = self.net(True), self.net(True)
        self.mos("nmos", q, qb, "gnd"); self.mos("nmos", qb, q, "gnd")
        self.mos("pmos", q, qb, "vdd"); self.mos("pmos", qb, q, "vdd")

    def level_shifter(self):
        self.lines.append("** ===== Level Shifter =====")
        self.dual = True
        if "svdd" not in self.nets:
            self.nets.append("svdd")
        a, b = self.net(True), self.net(True)
        self.mos("nmos", a, self.net(), "gnd"); self.mos("nmos", b, self.net(), "gnd")
        self.mos("pmos", a, b, "svdd"); self.mos("pmos", b, a, "svdd")

    def rectifier(self):
        self.lines.append("** ===== Rectifier =====")
        ac, o = self.net(True), self.net(True)
        self.dio(ac, o); self.dio("gnd", ac); self.dio(ac, o, "schottky")
        self.pas("C", o, "gnd")

    def zener(self):
        self.lines.append("** ===== Zener Clamp =====")
        o = self.net(); self.dio("gnd", o, "zener"); self.pas("R", "vdd", o)

    def rc(self):
        self.lines.append("** ===== RC =====")
        a, b = self.net(), self.net(True); self.pas("R", a, b); self.pas("C", b, "gnd")

    def lc(self):
        self.lines.append("** ===== LC Tank =====")
        a = self.net(True); self.pas("L", "vdd", a); self.pas("C", a, "gnd")

    def follower(self):
        self.lines.append("** ===== Source Follower =====")
        o = self.net(True); self.mos("nmos", "vdd", self.net(), o)
        self.mos("nmos", o, self.net(), "gnd")

    def ctrl_block(self):
        L = self.rng.choice(["E", "G", "F", "H"])
        self.lines.append(f"** ===== Controlled Source {L} =====")
        self.ctrl(L, self.net(True), "gnd")

    def b_block(self):
        self.lines.append("** ===== Behavioral Source =====")
        self.bsrc(self.net(True), "gnd")

    def switch_block(self):
        self.lines.append("** ===== Switch =====")
        self.vsw(self.net(True), self.net())

    def charge_pump(self):
        self.lines.append("** ===== Charge Pump =====")
        a, b = self.net(True), self.net(True)
        self.dio("vdd", a); self.pas("C", a, self.net()); self.dio(a, b)
        self.pas("C", b, "gnd")

    def build(self):
        blocks = [self.mirror, self.cascode_mirror, self.diffpair,
                  self.bjt_pair, self.bandgap, self.jfet_stage, self.cs_stage,
                  self.cascode, self.inverter, self.nand, self.latch,
                  self.level_shifter, self.rectifier, self.zener, self.rc,
                  self.lc, self.follower, self.ctrl_block, self.b_block,
                  self.switch_block, self.charge_pump]
        for _ in range(self.rng.randint(1, 6)):
            self.rng.choice(blocks)()
        sigs = [x for x in self.nets if x not in ("vdd", "gnd", "svdd")]
        ports = ["vdd", "gnd"] + (["svdd"] if self.dual else []) + \
            self.rng.sample(sigs, min(3, len(sigs)))
        return ports


def gen_one(name, rng):
    b = Builder(rng)
    ports = b.build()
    return "\n".join([f".subckt {name} " + " ".join(ports)] + b.lines
                     + [".ends"]) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=10000)
    ap.add_argument("--out", default="benchmark/gen10k")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rng = random.Random(args.seed)
    for i in range(args.count):
        with open(os.path.join(args.out, f"gen_{i:05d}.cir"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(gen_one(f"gen_{i:05d}", random.Random(rng.random())))
    print(f"wrote {args.count} netlists to {args.out}")


if __name__ == "__main__":
    main()
