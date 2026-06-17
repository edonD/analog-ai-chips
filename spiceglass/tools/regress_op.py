"""OP back-annotation gate test (IMPROVEMENT_LOOP improvement 3).

Strict gates, each against ground truth:
  O1  node voltages exact — resistor divider has an ANALYTIC answer
      (0.750 V); run_op must match within 1 mV.
  O3  region truth table — three MOSFETs placed in KNOWN regions
      (diode-connected ⇒ saturation; tiny Vds ⇒ triode; Vgs<Vth ⇒ off);
      run_op must classify all three correctly.
  O2  no silent omission — every net in the deck appears in nodes.
  O4  graceful failure — an unresolved model ⇒ ok=False with a reason,
      no crash.
  O5  determinism — two runs give identical node voltages.

Needs ngspice (bundled Spice64 or on PATH). If absent, SKIPs (cannot
verify) rather than passing silently.

    python tools/regress_op.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.op import run_op, ngspice_bin            # noqa: E402

DIVIDER = """* divider
Vdd in 0 1.0
R1 in mid 1k
R2 mid 0 3k
"""

REGIONS = """* mos region truth table
.model nm nmos (level=1 vto=0.5 kp=120u lambda=0.02)
Vsat ds 0 1.0
Vgsat g1 0 1.0
Msat ds g1 0 0 nm W=10u L=1u
Vtri dt 0 0.1
Vgtri g2 0 1.0
Mtri dt g2 0 0 nm W=10u L=1u
Voff do 0 1.0
Vgoff g3 0 0.2
Moff do g3 0 0 nm W=10u L=1u
"""

BADMODEL = """* missing model
Vdd d 0 1.0
M1 d g 0 0 doesnotexist W=1u L=1u
Vg g 0 1.0
"""


def main() -> int:
    if not ngspice_bin():
        print("SKIP — ngspice not found; cannot verify OP back-annotation")
        return 0
    fails = []

    # O1: analytic node voltage
    r = run_op(DIVIDER)
    if not r.ok:
        fails.append(("O1", f"divider failed: {r.error}"))
    elif abs(r.nodes.get("mid", -9) - 0.75) > 1e-3:
        fails.append(("O1", f"v(mid)={r.nodes.get('mid')} != 0.750 (±1mV)"))

    # O2: every net present (in, mid)
    if r.ok and not {"in", "mid"} <= set(r.nodes):
        fails.append(("O2", f"missing nets; got {sorted(r.nodes)}"))

    # O3: region truth table
    r3 = run_op(REGIONS)
    if not r3.ok:
        fails.append(("O3", f"regions deck failed: {r3.error}"))
    else:
        want = {"msat": "sat", "mtri": "triode", "moff": "off"}  # lowercase keys
        for name, exp in want.items():
            got = r3.mos.get(name, {}).get("region")
            if got != exp:
                fails.append(("O3", f"{name}: got {got}, want {exp} "
                                    f"(vds={r3.mos.get(name,{}).get('vds')}, "
                                    f"vdsat={r3.mos.get(name,{}).get('vdsat')}, "
                                    f"id={r3.mos.get(name,{}).get('id')})"))

    # O4: graceful failure on unresolved model
    rb = run_op(BADMODEL)
    if rb.ok or not rb.error:
        fails.append(("O4", "bad-model deck did not fail gracefully"))

    # O5: determinism
    ra, rc = run_op(DIVIDER), run_op(DIVIDER)
    if ra.nodes != rc.nodes:
        fails.append(("O5", "two runs differ"))

    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — O1 nodes exact (±1mV), O2 full coverage, O3 region truth "
          "table (sat/triode/off), O4 graceful failure, O5 deterministic")
    print(f"  divider v(mid)={r.nodes['mid']:.4f}  regions: " +
          ", ".join(f"{k}={v['region']}" for k, v in r3.mos.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
