"""Dense-routing gate (E5).

Circuits that crowd many nets onto few tracks — parallel devices between
two nodes, 3-net junctions, ring oscillators — used to leave shorts the
local nudge couldn't fix. The iterated terminal-jog must now route them
to a clean (verified) schematic via the product path.

  DR1 parallel R||C||R between two nodes verifies
  DR2 three parallel devices sharing both terminals (3-net crowd) verifies
  DR3 5-stage ring oscillator verifies
  DR4 RC ladder with parallel taps (ac-test shape) verifies

    python tools/regress_dense.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_text                 # noqa: E402
from glass.engine.classify import classify_design           # noqa: E402
from glass.engine.verify import verify                      # noqa: E402
from glass.web.server import _best_placement                # noqa: E402

CASES = {
    "DR1_parallel": """.subckt par a b vdd gnd
R1 a b 1k
C1 a b 1p
R2 a b 2k
Rt1 vdd a 1k
Rt2 b gnd 1k
.ends""",
    "DR2_triplecrowd": """.subckt crowd a b vdd gnd
M1 a g b gnd nmos w=2u l=1u
M2 a g b gnd nmos w=2u l=1u
M3 a g b gnd nmos w=2u l=1u
Rg vdd g 10k
Rt vdd a 1k
Rb b gnd 1k
.ends""",
    "DR3_ring": """.subckt ring out vdd gnd
Mp0 n1 out vdd vdd pmos w=2u l=0.5u
Mn0 n1 out gnd gnd nmos w=1u l=0.5u
Mp1 n2 n1 vdd vdd pmos w=2u l=0.5u
Mn1 n2 n1 gnd gnd nmos w=1u l=0.5u
Mp2 out n2 vdd vdd pmos w=2u l=0.5u
Mn2 out n2 gnd gnd nmos w=1u l=0.5u
.ends""",
    "DR4_rcladder": """.subckt rcl in out vdd gnd
R1 in n2 1k
R2 n2 n3 1k
R3 n3 out 1k
C2 n2 n3 1u
C3 n3 out 1u
Rt vdd in 1k
Rb out gnd 1k
.ends""",
}


def main() -> int:
    fails = []
    for name, deck in CASES.items():
        d = parse_text(deck)
        classify_design(d)
        sub = d.subckts[next(iter(d.subckts))]
        try:
            _, r, _ = _best_placement(sub)
            ok = verify(r).ok
            err = "" if ok else verify(r).errors[0]
        except Exception as e:
            ok, err = False, f"crash {e}"
        print(f"  {name:18} {'OK' if ok else 'FAIL: ' + err[:48]}")
        if not ok:
            fails.append((name, err))
    if fails:
        print(f"FAIL ({len(fails)})")
        return 1
    print("PASS — DR1-DR4 dense circuits route to a verified schematic")
    return 0


if __name__ == "__main__":
    sys.exit(main())
