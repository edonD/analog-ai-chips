"""Multi-file resolution gate (E1).

  I1 .include splices a subckt definition so an X-instance resolves to a
     block ('sub'), not an unknown box.
  I2 .lib "file" section pulls in that section's definitions.
  I3 a missing include is a warning, not a crash; the rest still parses.
  I4 an include cycle terminates (no hang), with a warning.

    python tools/regress_include.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_file                 # noqa: E402
from glass.engine.classify import classify_design           # noqa: E402


def _w(d, name, txt):
    with open(os.path.join(d, name), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(txt)
    return os.path.join(d, name)


def _kind(design, devname):
    for sub in design.subckts.values():
        for dv in sub.devices:
            if dv.name == devname:
                return dv.kind
    for dv in design.top_devices:
        if dv.name == devname:
            return dv.kind
    return None


def main() -> int:
    fails = []
    with tempfile.TemporaryDirectory() as d:
        # I1 .include
        _w(d, "leaf.inc",
           ".subckt blk a b vdd gnd\nM1 a b gnd gnd nmos w=1u l=1u\n.ends\n")
        m1 = _w(d, "main.cir",
                "* main\nXB n1 n2 vdd 0 blk\nR1 n1 0 1k\n"
                '.include "leaf.inc"\n')
        des = parse_file(m1)
        classify_design(des)
        if "blk" not in des.subckts:
            fails.append(("I1", "included subckt 'blk' not resolved"))
        if _kind(des, "XB") != "sub":
            fails.append(("I1", f"XB kind {_kind(des, 'XB')} != sub"))

        # I2 .lib section
        _w(d, "corner.lib",
           ".lib tt\n.subckt rblk p n\nR1 p n 1k\n.ends\n.endl\n"
           ".lib ff\n.subckt other p n\nR2 p n 2k\n.ends\n.endl\n")
        m2 = _w(d, "mainlib.cir",
                '* m\nXR a b rblk\n.lib "corner.lib" tt\n')
        des2 = parse_file(m2)
        classify_design(des2)
        if "rblk" not in des2.subckts:
            fails.append(("I2", "lib-section subckt 'rblk' not resolved"))
        if "other" in des2.subckts:
            fails.append(("I2", "wrong lib section pulled in ('other')"))

        # I3 missing include
        m3 = _w(d, "miss.cir",
                '* m\nR1 a 0 1k\n.include "nope.inc"\n')
        des3 = parse_file(m3)
        if _kind(des3, "R1") != "res":
            fails.append(("I3", "deck broke on missing include"))
        if not any("not found" in w for w in des3.warnings):
            fails.append(("I3", "no warning for missing include"))

        # I4 cycle
        _w(d, "a.cir", '* a\nRA x 0 1k\n.include "b.cir"\n')
        _w(d, "b.cir", '* b\nRB y 0 1k\n.include "a.cir"\n')
        des4 = parse_file(os.path.join(d, "a.cir"))
        if _kind(des4, "RA") != "res" or _kind(des4, "RB") != "res":
            fails.append(("I4", "cycle broke parsing"))
        if not any("cycle" in w for w in des4.warnings):
            fails.append(("I4", "no cycle warning"))

    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — I1 .include subckt resolves, I2 .lib section, "
          "I3 missing-include warned not crashed, I4 cycle terminates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
