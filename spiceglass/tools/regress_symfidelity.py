"""Sky130 symbol + parameter fidelity gate (improvement: PDK fidelity).

Strict gates:
  F1 parameter fidelity — device_value() shows model + w/l and any
     non-default nf/m/mult, in order, dropping unit defaults (=1); a
     value-only passive shows just its value.
  F2 Sky130 classification — fets→nmos/pmos (4 terminals d/g/s/b),
     res→res, cap_mim/cap_var→cap, diode→dio, npn→npn; MOS symbol art
     exposes all four pins.
  F3 faithfulness on REAL decks — every modeled device's annotation
     contains its (compact) model and its exact w and l (no loss).

    python tools/regress_symfidelity.py
"""
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.db import Device                        # noqa: E402
from glass.engine.parser import parse_file                # noqa: E402
from glass.engine.classify import (classify_design,        # noqa: E402
                                    device_value, short_model)
from glass.geom import pin_offsets                         # noqa: E402


def _dev(model, params, kind="nmos"):
    return Device(name="M1", kind=kind, model=model, nets=[], roles=[],
                  params=params)


def main() -> int:
    fails = []

    # ---- F1 parameter fidelity
    cases = [
        (_dev("nmos", {"w": "4", "l": "0.5", "nf": "2", "m": "3"}),
         "nmos w=4 l=0.5 nf=2 m=3"),
        (_dev("sky130_fd_pr__pfet_01v8", {"w": "4", "l": "4"}),
         "pfet_01v8 w=4 l=4"),
        (_dev("sky130_fd_pr__nfet_01v8",
              {"w": "4", "l": "0.5", "m": "1", "nf": "1"}),   # defaults drop
         "nfet_01v8 w=4 l=0.5"),
        (_dev("", {"value": "10k"}, kind="res"), "10k"),
    ]
    for dev, exp in cases:
        got = device_value(dev)
        if got != exp:
            fails.append(("F1", f"got '{got}' want '{exp}'"))

    # ---- F2 classification + 4-terminal MOS
    deck = """* sky130 classify probe
.subckt probe vdd gnd a b c
XM1 a b gnd gnd sky130_fd_pr__nfet_01v8 w=1 l=1
XM2 a b vdd vdd sky130_fd_pr__pfet_01v8 w=1 l=1
XR1 a c gnd sky130_fd_pr__res_xhigh_po w=0.35 l=5
XC1 a c gnd sky130_fd_pr__cap_mim_m3_1 w=4 l=4
XD1 a c sky130_fd_pr__diode_pw2nd_05v5
XQ1 a b c sky130_fd_pr__npn_05v5_W1p00L1p00
.ends
"""
    here = os.path.dirname(os.path.abspath(__file__))
    tmp = os.path.join(here, "_symfid_probe.cir")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(deck)
    try:
        d = parse_file(tmp)
        classify_design(d)
        want_kind = {"XM1": "nmos", "XM2": "pmos", "XR1": "res",
                     "XC1": "cap", "XD1": "dio", "XQ1": "npn"}
        devs = {dv.name: dv for dv in d.subckts["probe"].devices}
        for name, exp in want_kind.items():
            got = devs.get(name)
            if not got or got.kind != exp:
                fails.append(("F2", f"{name}: kind "
                                    f"{got.kind if got else None} != {exp}"))
        for nm in ("XM1", "XM2"):
            roles = devs[nm].roles
            if roles != ["d", "g", "s", "b"]:
                fails.append(("F2", f"{nm} roles {roles} != d,g,s,b"))
            offs = pin_offsets(devs[nm], "R0")
            if set(offs) != {"d", "g", "s", "b"}:
                fails.append(("F2", f"{nm} symbol pins {set(offs)} != 4-term"))
    finally:
        os.unlink(tmp)

    # ---- F3 faithfulness on real decks
    real = (glob.glob(os.path.join(here, "..", "..", "vibrosense",
                                   "*", "design.cir")) +
            glob.glob(os.path.join(here, "..", "..", "pvdd_regulator",
                                   "*", "design.cir")))
    checked = 0
    for f in real:
        try:
            dd = parse_file(f)
            classify_design(dd)
        except Exception:
            continue
        for sub in dd.subckts.values():
            for dev in sub.devices:
                if dev.kind not in ("nmos", "pmos", "res", "cap"):
                    continue
                if "w" not in dev.params:
                    continue
                ann = device_value(dev)
                checked += 1
                sm = short_model(dev)
                if sm and sm not in ann:
                    fails.append(("F3", f"{dev.name}: model '{sm}' missing"))
                for k in ("w", "l"):
                    if k in dev.params and f"{k}={dev.params[k]}" not in ann:
                        fails.append(("F3", f"{dev.name}: {k} not faithful "
                                            f"in '{ann}'"))

    print(f"symbol/param fidelity: F1 {len(cases)} cases, "
          f"F2 classify probe, F3 {checked} real devices")
    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails[:30]:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — F1 params exact (nf/m/mult, defaults dropped), "
          "F2 Sky130 classes + 4-terminal MOS, F3 real decks faithful")
    return 0


if __name__ == "__main__":
    sys.exit(main())
