"""Hierarchical OP back-annotation gate (improvement #2).

run_op must read node voltages AND MOSFET regions THROUGH subckt
instances, using ngspice's hierarchical addressing.

  HO1 internal node voltage exact — x1.mid is an analytic divider
      (2.0 * 3k/4k = 1.5 V); must match within 1 mV, under its instance
      prefix (x1.mid, not bare mid).
  HO2 device regions at depth: a diode-connected FET inside X1 -> sat,
      a Vgs=0 FET inside X1 -> off (keyed m.x1.msat / m.x1.moff).
  HO3 top-level + hierarchical coexist (mtop present alongside m.x1.*).

    python tools/regress_op_hier.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.op import run_op, ngspice_bin           # noqa: E402

DECK = """* hierarchical op gate
.model nm nmos (level=1 vto=0.5 kp=120u)
.subckt blk vdd vss
R1 vdd mid 1k
R2 mid vss 3k
MSAT ds ds vss vss nm W=4u L=0.5u
RS vdd ds 5k
MOFF od vss vss vss nm W=4u L=0.5u
RO vdd od 5k
.ends
Vdd vdd 0 2.0
X1 vdd 0 blk
MTOP dt dt 0 0 nm W=4u L=0.5u
RT vdd dt 5k
"""


def main() -> int:
    if not ngspice_bin():
        print("SKIP — ngspice not found")
        return 0
    r = run_op(DECK)
    fails = []
    if not r.ok:
        print(f"FAIL — run_op error: {r.error}")
        return 1

    # HO1 internal node, prefixed, analytic
    v = r.nodes.get("x1.mid")
    if v is None:
        fails.append(("HO1", f"x1.mid missing; nodes={sorted(r.nodes)}"))
    elif abs(v - 1.5) > 1e-3:
        fails.append(("HO1", f"x1.mid={v} != 1.500 (±1mV)"))

    # HO2 regions at depth
    want = {"m.x1.msat": "sat", "m.x1.moff": "off"}
    for key, exp in want.items():
        got = r.mos.get(key, {}).get("region")
        if got != exp:
            fails.append(("HO2", f"{key}: {got} != {exp} "
                                 f"(have {sorted(r.mos)})"))

    # HO3 top-level coexists
    if r.mos.get("mtop", {}).get("region") != "sat":
        fails.append(("HO3", f"mtop region "
                             f"{r.mos.get('mtop', {}).get('region')} != sat"))

    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — HO1 internal node x1.mid=1.500V exact, HO2 depth regions "
          "(msat=sat, moff=off), HO3 top+hier coexist")
    regions = ", ".join(f"{k}={v['region']}" for k, v in r.mos.items())
    print(f"  mos: {regions}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
