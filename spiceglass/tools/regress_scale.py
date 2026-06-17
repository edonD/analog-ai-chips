"""Scale / performance-budget gate (E4).

The PRODUCT path (_best_placement) must stay responsive on large blocks.
The verify-gated optimizer's ordering search is super-linear, so it is
size-capped; above the cap a single plain placement is used (sub-second
and it verifies for structured blocks).

  SC1 a 60-device block converts+verifies in < 2 s
  SC2 a 200-device block in < 5 s
  SC3 a 600-device block in < 8 s   (was ~130 s before the cap)
  SC4 all of the above round-trip VERIFY (no correctness traded)

    python tools/regress_scale.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_text                 # noqa: E402
from glass.engine.classify import classify_design           # noqa: E402
from glass.engine.verify import verify                      # noqa: E402
from glass.web.server import _best_placement                # noqa: E402


def bank(n):
    L = [f".subckt bank{n} vdd gnd g", "M0 g g gnd gnd nmos w=2u l=1u"]
    for i in range(n):
        L += [f"M{i+1} o{i} g gnd gnd nmos w=2u l=1u",
              f"R{i} vdd o{i} 1k"]
    L.append(".ends")
    return "\n".join(L) + "\n"


def main() -> int:
    budgets = [(30, 2.0), (100, 5.0), (300, 8.0)]   # (n outputs, seconds)
    fails = []
    for n, budget in budgets:
        d = parse_text(bank(n))
        classify_design(d)
        sub = d.subckts[f"bank{n}"]
        nd = len(sub.devices)
        t = time.time()
        sh, r, note = _best_placement(sub)
        dt = time.time() - t
        ok = verify(r).ok
        tag = "OK" if ok else "MISMATCH"
        print(f"  {nd:4} devices: {dt:6.2f}s (budget {budget}s)  {tag}")
        if dt > budget:
            fails.append((nd, f"{dt:.2f}s > {budget}s budget"))
        if not ok:
            fails.append((nd, "did not verify"))

    if fails:
        print(f"FAIL ({len(fails)}):")
        for n, m in fails:
            print(f"  {n} dev: {m}")
        return 1
    print("PASS — SC1-SC4 large blocks convert + verify within budget")
    return 0


if __name__ == "__main__":
    sys.exit(main())
