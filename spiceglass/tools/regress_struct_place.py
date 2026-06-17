"""Structure-aware placement gate (N2).

The optimizer now rewards keeping a recognized structure's objects
contiguous. It's verify-gated, so it can only change WHICH verifying order
wins — never correctness.

  SP1 cost term works: a contiguous structure scores better than a split
      one (struct_breaks 0 vs 1), with crossings unchanged.
  SP2 no regression: a sample of recognized topologies still verifies
      100% via the product path (the structure hint is live).
  SP3 quality not worse: optimized crossings <= seed crossings.

    python tools/regress_struct_place.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

import tools.gen_realistic as gen                          # noqa: E402
from glass.engine.db import Device                         # noqa: E402
from glass.engine.parser import parse_text                 # noqa: E402
from glass.engine.classify import classify_design           # noqa: E402
from glass.engine.place import place                       # noqa: E402
from glass.engine.route import route                       # noqa: E402
from glass.engine.verify import verify                     # noqa: E402
from glass.engine.score import score                       # noqa: E402
from glass.web.server import _best_placement                # noqa: E402
from glass.engine import optimize as opt                   # noqa: E402


def main() -> int:
    fails = []

    # SP1: cost term — contiguous structure beats split (same crossings)
    def dev(nm, nets):
        return Device(name=nm, kind="nmos", model="", nets=nets,
                      roles=[], params={})
    oA1 = ("chain", [dev("MA1", ["a", "x"])])
    oA2 = ("chain", [dev("MA2", ["a", "y"])])
    oB = ("chain", [dev("MB", ["b", "z"])])
    objs = [oA1, oA2, oB]
    dev_struct = {"MA1": "pair#0", "MA2": "pair#0"}     # MB unlabeled
    onets = {id(o): opt._nets(o, {}, set()) for o in objs}
    osec = {id(o): "" for o in objs}
    ostruct = opt._ostruct(objs, dev_struct)
    contig = opt.cost([oA1, oA2, oB], onets, osec, None, ostruct)
    split = opt.cost([oA1, oB, oA2], onets, osec, None, ostruct)
    if not (contig["struct_breaks"] == 0 and split["struct_breaks"] == 1):
        fails.append(("SP1", f"struct_breaks contig={contig['struct_breaks']} "
                             f"split={split['struct_breaks']}"))
    if not (opt._scalar(contig) < opt._scalar(split)):
        fails.append(("SP1", "contiguous order not preferred"))

    # SP2 + SP3: real topologies still verify, crossings not worse
    by = {fn.__name__: fn for fn in gen.TEMPLATES}
    names = ["ota_5t", "ota_telescopic", "ota_folded_cascode",
             "cascode_mirror", "mirror_bank", "comparator", "ota_two_stage",
             "current_mirror_ota", "inverter_chain"]
    checked = bad = 0
    for nm in names:
        fn = by.get(nm)
        if not fn:
            continue
        for seed in range(6):
            r = random.Random(seed)
            base, ports, lines = fn(r)
            text = f".subckt {base} {ports}\n" + "\n".join(lines) + "\n.ends\n"
            d = parse_text(text)
            classify_design(d)
            sub = d.subckts[base]
            seed_sh = place(sub)
            seed_sc = score(seed_sh, route(seed_sh))
            sh, rt, _ = _best_placement(sub)
            checked += 1
            if not verify(rt).ok:
                bad += 1
                fails.append(("SP2", f"{base} seed {seed} did not verify"))
            if score(sh, rt).crossings > seed_sc.crossings:
                fails.append(("SP3", f"{base} seed {seed} crossings worse"))

    print(f"struct-place gate: {checked} placements checked, {bad} unverified")
    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails[:20]:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — SP1 structure term rewards contiguity, SP2 recognized "
          "topologies verify 100%, SP3 crossings never worse than seed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
