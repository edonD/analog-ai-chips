"""Search/find gate (improvement #3, loop S1-S2).

  S1 find correctness — for every instance name and every net label on a
     sheet, find_in returns EXACTLY the occurrences (count matches the
     .asc), no misses, no false hits.
  S2 negative — a non-existent name returns nothing (no crash).

    python tools/regress_find.py
"""
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.web.server import convert_to_asc, find_in       # noqa: E402
from glass.asc.parse import parse_asc, _read_text           # noqa: E402


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(here, ".."))
    srcs = (sorted(glob.glob("examples/leaf_*.cir"))[:6] +
            sorted(glob.glob("examples/hier_*.cir"))[:4] +
            ["examples/op_demo_ota5t.cir"])
    queries, fails = 0, []
    for s in srcs:
        if not os.path.exists(s):
            continue
        asc = convert_to_asc(s)
        text = _read_text(asc)
        sheet = parse_asc(asc)
        inst_names = [i.attrs.get("InstName", "") for i in sheet.insts
                      if i.attrs.get("InstName")]
        flag_names = [n for (_, _, n) in sheet.flags]

        # S1: instance names -> exact instance occurrence count
        for nm in set(inst_names):
            truth = sum(1 for x in inst_names if x.lower() == nm.lower())
            got = len(find_in(text, nm)["instances"])
            queries += 1
            if got != truth:
                fails.append((s, nm, f"inst {got} != {truth}"))
        # S1: net labels -> exact flag occurrence count
        for nm in set(flag_names):
            truth = sum(1 for x in flag_names if x.lower() == nm.lower())
            got = len(find_in(text, nm)["flags"])
            queries += 1
            if got != truth:
                fails.append((s, nm, f"flag {got} != {truth}"))
        # S2: bogus query -> nothing
        r = find_in(text, "no_such_name_xyz_123")
        if r["instances"] or r["flags"]:
            fails.append((s, "<bogus>", "matched nonexistent name"))

    print(f"find gate: {queries} queries across {len(srcs)} sheets")
    if fails:
        print(f"FAIL ({len(fails)}):")
        for s, nm, m in fails[:30]:
            print(f"  {os.path.basename(s)} '{nm}': {m}")
        return 1
    print("PASS — S1 exact match counts (instances + nets), S2 bogus -> none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
