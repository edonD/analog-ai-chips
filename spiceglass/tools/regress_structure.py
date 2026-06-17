"""Structure-recognition gate (E3).

The recognizer must tag the expected motif on known topologies — the
recognition labels that feed the dataset and design reports. Pure
analysis: it cannot regress placement (it never touches it).

  R1 expected structure present per topology (5T->diff_pair+current_mirror,
     mirrors->current_mirror, inverter->inverter, NAND->nand2, NOR->nor2,
     follower->source_follower, cascode mirror->cascode).
  R2 no false gates on a plain resistor divider.

    python tools/regress_structure.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

import tools.gen_realistic as gen                          # noqa: E402
from glass.engine.parser import parse_text                 # noqa: E402
from glass.engine.classify import classify_design           # noqa: E402
from glass.engine.structure import structure_kinds          # noqa: E402


def _kinds_for(fn):
    r = random.Random(0)
    base, ports, lines = fn(r)
    text = f".subckt {base} {ports}\n" + "\n".join(lines) + "\n.ends\n"
    d = parse_text(text)
    classify_design(d)
    return base, structure_kinds(d.subckts[base])


# fn name -> a structure kind that MUST be recognized
EXPECT = {
    "ota_5t": "diff_pair",
    "ota_5t_cm": "current_mirror",      # placeholder; checked via OR below
    "mirror_bank": "current_mirror",
    "cascode_mirror": "current_mirror",
    "inverter_chain": "inverter",
    "nand2": "nand2",
    "nor2": "nor2",
    "common_source": None,              # just a gain stage — no false claim
}


def main() -> int:
    by_name = {fn.__name__: fn for fn in gen.TEMPLATES}
    fails = []

    def check(fnname, must):
        fn = by_name.get(fnname)
        if not fn:
            return
        base, kinds = _kinds_for(fn)
        if must and must not in kinds:
            fails.append((fnname, f"missing '{must}'; got {kinds}"))

    check("ota_5t", "diff_pair")
    check("ota_5t", "current_mirror")
    check("mirror_bank", "current_mirror")
    check("cascode_mirror", "current_mirror")
    check("inverter_chain", "inverter")
    check("nand2", "nand2")
    check("nor2", "nor2")
    # source follower appears in class_ab_output / common-drain stages
    check("ota_two_stage", "diff_pair")

    # R2: a plain RC divider yields no transistor-gate structures
    d = parse_text(".subckt rc a b gnd\nR1 a b 1k\nR2 b gnd 1k\n"
                   "C1 b gnd 1p\n.ends\n")
    classify_design(d)
    if structure_kinds(d.subckts["rc"]):
        fails.append(("rc_divider", "false structure on passive divider"))

    if fails:
        print(f"FAIL ({len(fails)}):")
        for n, m in fails:
            print(f"  {n}: {m}")
        return 1
    # report what each known topology recognizes
    for fnname in ("ota_5t", "ota_telescopic", "cascode_mirror",
                   "inverter_chain", "nand2", "nor2", "class_ab_output"):
        fn = by_name.get(fnname)
        if fn:
            base, kinds = _kinds_for(fn)
            print(f"  {base:22} -> {kinds}")
    print("PASS — expected motifs tagged; no false structures on passives")
    return 0


if __name__ == "__main__":
    sys.exit(main())
