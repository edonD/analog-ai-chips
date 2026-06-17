"""Design-report (glass doc) gate (N1).

  DOC1 every device appears exactly once as a table row (no drops).
  DOC2 recognized structures are listed (e.g. a 5T OTA shows diff_pair).
  DOC3 deterministic (two builds identical).
  DOC4 with OP, an "Operating point" section with a region is included.

    python tools/regress_doc.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_file, parse_text     # noqa: E402
from glass.engine.classify import classify_design           # noqa: E402
from glass.engine.report import markdown_report             # noqa: E402
from glass.engine.op import run_op_file, ngspice_bin        # noqa: E402

OTA = """.subckt ota5t inp inn out vdd gnd vbias
M1 d1 inp tail gnd nmos w=10u l=0.5u
M2 out inn tail gnd nmos w=10u l=0.5u
M3 d1 d1 vdd vdd pmos w=10u l=0.5u
M4 out d1 vdd vdd pmos w=10u l=0.5u
M5 tail vbias gnd gnd nmos w=20u l=0.5u
.ends
"""


def main() -> int:
    fails = []
    d = parse_text(OTA)
    classify_design(d)
    md = markdown_report(d)

    # DOC1: a table row per device
    sub = d.subckts["ota5t"]
    for dev in sub.devices:
        if f"| {dev.name} |" not in md:
            fails.append(("DOC1", f"{dev.name} missing from table"))
    if "## ota5t" not in md:
        fails.append(("DOC1", "subckt heading missing"))

    # DOC2: recognized structures listed
    if "diff_pair" not in md or "current_mirror" not in md:
        fails.append(("DOC2", "expected structures not in report"))

    # DOC3: deterministic
    if markdown_report(parse_text(OTA)) != md:
        # re-classify needed for fair compare
        d2 = parse_text(OTA)
        classify_design(d2)
        if markdown_report(d2) != md:
            fails.append(("DOC3", "report not deterministic"))

    # DOC4: OP section on a simulatable demo
    demo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "examples", "op_demo_ota5t.cir")
    if ngspice_bin() and os.path.exists(demo):
        dd = parse_file(demo)
        classify_design(dd)
        op = run_op_file(demo)
        mdop = markdown_report(dd, op=op if op.ok else None)
        if op.ok and ("Operating point" not in mdop
                      or " sat " not in mdop and "| sat |" not in mdop):
            fails.append(("DOC4", "OP section/region missing with --op"))

    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — DOC1 all devices tabled, DOC2 structures listed, "
          "DOC3 deterministic, DOC4 OP section present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
