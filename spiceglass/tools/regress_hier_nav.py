"""Hierarchy-navigation gate test (IMPROVEMENT_LOOP improvement 1).

Encodes gates N1-N3 + N5 against the round-trip verifier (the oracle):

  N1  a descended child sheet == convert_subckt of that subckt (byte-exact,
      same reader) — what the editor opens is exactly the converter output.
  N2  every block instance, at every level, opens AND round-trip VERIFIES.
  N3  no false blocks: leaf circuits emit zero block symbols.
  N5  depth >= 3 works (examples/hier_three_level.cir).

Exit non-zero on any failure.  Run from spiceglass/:
    python tools/regress_hier_nav.py
"""
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_file            # noqa: E402
from glass.engine.classify import classify_design      # noqa: E402
from glass.engine.verify import verify                 # noqa: E402
from glass.asc.parse import _read_text                 # noqa: E402
from glass.web.server import (                          # noqa: E402
    AppState, convert_subckt, _best_placement, _register_top)


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(here, ".."))
    fails, n_blocks, n_leaf, max_depth = [], 0, 0, 0

    hier = sorted(glob.glob("examples/hier_*.cir"))
    for f in hier:
        design = parse_file(f)
        classify_design(design)
        _register_top(design)
        # every subckt that instantiates blocks — covers all hierarchy levels
        for name, sub in design.subckts.items():
            for d in sub.devices:
                if d.kind != "sub":
                    continue
                child = d.model
                n_blocks += 1
                # N2: descend opens + round-trip verifies
                try:
                    asc = convert_subckt(f, child)
                except Exception as e:
                    fails.append((f, child, f"open failed: "
                                            f"{type(e).__name__}: {e}"))
                    continue
                csub = design.subckts[child]
                _, routing, _ = _best_placement(csub)
                v = verify(routing)
                if not v.ok:
                    fails.append((f, child, f"verify: {v.errors[0]}"))
                # N1: served sheet == convert_subckt output (same reader)
                st = AppState(os.path.abspath(f))
                st.bootstrap()
                if st.descend(child)["text"] != _read_text(asc):
                    fails.append((f, child, "served != convert_subckt"))

    # N5: depth >= 3 for the three-level example
    f3 = "examples/hier_three_level.cir"
    if os.path.exists(f3):
        d3 = parse_file(f3)
        classify_design(d3)
        _register_top(d3)

        def depth(name, seen=()):
            if name in seen:
                return 0
            subs = [x.model for x in d3.subckts.get(name).devices
                    if x.kind == "sub" and x.model in d3.subckts]
            return 1 + max((depth(s, seen + (name,)) for s in subs),
                           default=0)
        root = d3.root().name
        max_depth = depth(root)
        if max_depth < 3:
            fails.append((f3, root, f"depth {max_depth} < 3"))

    # N3: leaf circuits emit no block symbols
    for f in sorted(glob.glob("examples/leaf_*.cir")):
        n_leaf += 1
        st = AppState(os.path.abspath(f))
        if "sg_blk_" in st.bootstrap()["text"]:
            fails.append((f, "-", "leaf emitted a block symbol (false block)"))

    print(f"hierarchy-nav gates: blocks tested {n_blocks}, leaves {n_leaf}, "
          f"max depth {max_depth}")
    if fails:
        print(f"FAIL ({len(fails)}):")
        for who, child, err in fails[:40]:
            print(f"  {who} :: {child}  {err}")
        return 1
    print("PASS — N1 (byte-exact), N2 (all blocks verify), "
          "N3 (no false blocks), N5 (depth>=3)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
