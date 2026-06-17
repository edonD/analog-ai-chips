"""CDL dialect conformance gate (improvement: one more dialect).

A foundry CDL deck (with *.PININFO / *.BIPOLAR directives, '$' layout
properties, '//' inline comments, '+' continuations) must parse to the
EXACT SAME circuit as its plain-SPICE twin — same ports, same devices,
same per-device nets and W/L — and both must convert + round-trip verify.

    python tools/regress_cdl.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_file                # noqa: E402
from glass.engine.classify import classify_design          # noqa: E402
from glass.engine.place import place                       # noqa: E402
from glass.engine.route import route                       # noqa: E402
from glass.engine.verify import verify                     # noqa: E402

CDL = """*.BIPOLAR
*.RESI = 2000
*.PININFO inp:I inn:I out:O vdd:B vss:B vbias:I
.SUBCKT ota5t inp inn out vdd vss vbias
MP3 d1  d1  vdd vdd pfet W=10u L=0.5u $X=0 $Y=0
MP4 out d1  vdd vdd pfet W=10u L=0.5u $X=1 $Y=0
MN1 d1  inp tail vss nfet W=10u L=0.5u $SUB=vss
MN2 out inn tail vss nfet W=10u L=0.5u // input pair
MN5 tail vbias vss vss nfet
+ W=20u L=0.5u $extra=1
.ENDS
"""

SPICE = """.subckt ota5t inp inn out vdd vss vbias
MP3 d1  d1  vdd vdd pfet W=10u L=0.5u
MP4 out d1  vdd vdd pfet W=10u L=0.5u
MN1 d1  inp tail vss nfet W=10u L=0.5u
MN2 out inn tail vss nfet W=10u L=0.5u
MN5 tail vbias vss vss nfet W=20u L=0.5u
.ends
"""


def _structure(path):
    d = parse_file(path)
    classify_design(d)
    out = {}
    for name, sub in d.subckts.items():
        out[name] = {
            "ports": list(sub.ports),
            "devs": {dv.name: (dv.kind, list(dv.nets),
                               dv.params.get("w"), dv.params.get("l"))
                     for dv in sub.devices},
        }
    return d, out


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    fails = []
    fc = os.path.join(here, "_cdl.cdl")
    fs = os.path.join(here, "_spice.cir")
    open(fc, "w", encoding="utf-8", newline="\n").write(CDL)
    open(fs, "w", encoding="utf-8", newline="\n").write(SPICE)
    try:
        dc, sc = _structure(fc)
        ds, ss = _structure(fs)

        # C1: identical structure CDL vs SPICE twin
        if sc != ss:
            fails.append(("C1", f"CDL structure != SPICE twin\n"
                                f"  CDL:   {sc}\n  SPICE: {ss}"))

        # C2: no '$' property leaked into nets or params
        for name, info in sc.items():
            for dn, (kind, nets, w, l) in info["devs"].items():
                if any("$" in n for n in nets):
                    fails.append(("C2", f"{dn}: '$' leaked into nets {nets}"))
            sub = dc.subckts[name]
            for dv in sub.devices:
                if any(k.startswith("$") for k in dv.params):
                    fails.append(("C2", f"{dv.name}: '$' param "
                                        f"{list(dv.params)}"))

        # C3: both convert + round-trip verify
        for tag, des in (("CDL", dc), ("SPICE", ds)):
            sub = des.subckts["ota5t"]
            v = verify(route(place(sub)))
            if not v.ok:
                fails.append(("C3", f"{tag} did not verify: {v.errors[:1]}"))
    finally:
        os.unlink(fc)
        os.unlink(fs)

    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails[:20]:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — C1 CDL == SPICE twin (ports/devices/nets/W/L), "
          "C2 no '$' leakage, C3 both convert + verify")
    return 0


if __name__ == "__main__":
    sys.exit(main())
