"""Parser-robustness gate (improvement: harden on real netlists).

Real foundry/HSPICE decks write parameters with spaces around '=' and
split across continuations (e.g. a line ending `W=` with the value on the
next `+` line). The value must become the PARAM, never a node.

  P1  'W= v', 'W = v', 'W =v' all parse v as the param, nodes intact
  P2  a value split onto a '+' continuation is captured, not leaked as a net
  P3  normal 'k=v' still works (no regression)

    python tools/regress_parser.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_text                # noqa: E402


def _dev(text, name):
    d = parse_text(text)
    sub = d.subckts["t"]
    return next(x for x in sub.devices if x.name == name)


def main() -> int:
    fails = []

    deck = """.subckt t d g s b
M1 d g s b nm W= 1u L =2u AD =3p
M2 d g s b nm W = 4u L= 5u
M3 d g s b nm W=6u L=7u
MC d g s b nm L=8u W=
+ 9u AD=1p
.ends
"""
    want = {"M1": ("1u", "2u"), "M2": ("4u", "5u"),
            "M3": ("6u", "7u"), "MC": ("9u", "8u")}
    for name, (w, l) in want.items():
        dv = _dev(deck, name)
        # P1/P2/P3: params captured
        if dv.params.get("w") != w or dv.params.get("l") != l:
            fails.append((name, f"w/l = {dv.params.get('w')}/"
                                f"{dv.params.get('l')}, want {w}/{l}"))
        # nodes must be exactly the four terminals — no value leaked in
        if dv.nets != ["d", "g", "s", "b"]:
            fails.append((name, f"nets leaked: {dv.nets}"))

    if fails:
        print(f"FAIL ({len(fails)}):")
        for n, m in fails:
            print(f"  {n}: {m}")
        return 1
    print("PASS — P1 spaces-around-'=', P2 value on continuation, "
          "P3 normal k=v; nodes never polluted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
