"""Procedural analog-netlist generator for the conversion benchmark.

AI-authored netlists (benchmark/gen/) give realistic topologies but don't
scale to thousands. This synthesizes large volumes of VALID, structurally
diverse ngspice .subckt netlists by composing randomized analog building
blocks (mirrors, diff pairs, cascodes, CS stages, inverters, RC nets,
sources). Correct-by-construction (only legal device cards, models
nmos/pmos/npn/pnp/diode, vdd/gnd rails), seeded for reproducibility.

    python tools/gen_netlists.py --count 1000 --out benchmark/gen1000 --seed 1
then score with:
    python tools/benchmark.py --dir benchmark/gen1000
"""
import argparse
import os
import random


class Builder:
    def __init__(self, rng):
        self.rng = rng
        self.lines = []
        self.n = 0          # device counter
        self.sig = 0        # signal-net counter
        self.nets = ["gnd", "vdd"]

    def _w(self):
        return f"{self.rng.choice([1, 2, 4, 8, 10, 20, 40])}u"

    def _l(self):
        return f"{self.rng.choice(['0.18u', '0.5u', '1u', '2u'])}"

    def net(self, fresh=False):
        if fresh or self.rng.random() < 0.5 or len(self.nets) < 4:
            self.sig += 1
            nm = f"n{self.sig}"
            self.nets.append(nm)
            return nm
        return self.rng.choice([x for x in self.nets if x not in ("gnd", "vdd")]
                               or ["gnd"])

    def mos(self, kind, d, g, s):
        self.n += 1
        b = "vdd" if kind == "pmos" else "gnd"
        self.lines.append(f"M{self.n} {d} {g} {s} {b} {kind} "
                          f"W={self._w()} L={self._l()}")

    def passive(self, c, a, b):
        self.n += 1
        v = self.rng.choice(["1k", "10k", "100k", "1meg", "100", "1p", "10p",
                             "1n", "100f"])
        self.lines.append(f"{c}{self.n} {a} {b} {v}")

    # -------- blocks (each emits valid devices on shared/fresh nets) -------
    def mirror(self):
        self.lines.append("** ===== Current Mirror =====")
        bias = self.net(fresh=True)
        self.mos("nmos", bias, bias, "gnd")              # diode-connected
        for _ in range(self.rng.randint(1, 4)):
            self.mos("nmos", self.net(), bias, "gnd")

    def diffpair(self):
        self.lines.append("** ===== Differential Pair =====")
        tail = self.net(fresh=True)
        inp, inn = self.net(fresh=True), self.net(fresh=True)
        op, on = self.net(fresh=True), self.net(fresh=True)
        k = self.rng.choice(["nmos", "pmos"])
        self.mos(k, op, inp, tail)
        self.mos(k, on, inn, tail)
        self.mos("nmos", tail, self.net(), "gnd")        # tail
        ld = "pmos" if k == "nmos" else "nmos"
        rail = "vdd" if ld == "pmos" else "gnd"
        g = self.net(fresh=True)
        self.mos(ld, op, g, rail)
        self.mos(ld, on, g, rail)

    def cs_stage(self):
        self.lines.append("** ===== Gain Stage =====")
        out = self.net(fresh=True)
        self.mos("nmos", out, self.net(), "gnd")
        self.mos("pmos", out, self.net(), "vdd")

    def cascode(self):
        self.lines.append("** ===== Cascode =====")
        mid, top = self.net(fresh=True), self.net(fresh=True)
        self.mos("nmos", mid, self.net(), "gnd")
        self.mos("nmos", top, self.net(), mid)

    def inverter(self):
        self.lines.append("** ===== Inverter =====")
        i, o = self.net(), self.net(fresh=True)
        self.mos("pmos", o, i, "vdd")
        self.mos("nmos", o, i, "gnd")

    def rc(self):
        self.lines.append("** ===== RC =====")
        a, b = self.net(), self.net(fresh=True)
        self.passive("R", a, b)
        self.passive("C", b, "gnd")

    def follower(self):
        self.lines.append("** ===== Source Follower =====")
        o = self.net(fresh=True)
        self.mos("nmos", "vdd", self.net(), o)
        self.mos("nmos", o, self.net(), "gnd")

    def build(self):
        blocks = [self.mirror, self.diffpair, self.cs_stage, self.cascode,
                  self.inverter, self.rc, self.follower]
        for _ in range(self.rng.randint(1, 4)):
            self.rng.choice(blocks)()
        ports = ["vdd", "gnd"] + self.rng.sample(
            [x for x in self.nets if x not in ("vdd", "gnd")],
            min(3, max(0, len(self.nets) - 2)))
        return ports


def gen_one(name, rng):
    b = Builder(rng)
    ports = b.build()
    head = [f".subckt {name} " + " ".join(ports)]
    return "\n".join(head + b.lines + [".ends"]) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1000)
    ap.add_argument("--out", default="benchmark/gen1000")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rng = random.Random(args.seed)
    for i in range(args.count):
        name = f"gen_{i:04d}"
        with open(os.path.join(args.out, name + ".cir"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(gen_one(name, rng))
    print(f"wrote {args.count} netlists to {args.out}")


if __name__ == "__main__":
    main()
