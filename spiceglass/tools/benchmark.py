"""Generative conversion benchmark + diagnostic.

Scores the .cir -> .asc engine over a corpus and breaks the results down
by what's IN each circuit (device-card type) and by size, so the report
tells us WHAT to improve, not just an overall percentage.

    python tools/benchmark.py --dir benchmark/gen10k
    python tools/benchmark.py --dir benchmark/gen10k --optimize
"""
import argparse
import glob
import os
import sys
import time
from collections import Counter, defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, ".."))

from glass.asc.parse import _read_text                    # noqa: E402
from glass.engine.parser import parse_file                # noqa: E402
from glass.engine.classify import classify_design         # noqa: E402
from glass.engine.place import place                      # noqa: E402
from glass.engine.route import route                      # noqa: E402
from glass.engine.verify import verify                    # noqa: E402
from glass.web.server import _register_top, _best_placement  # noqa: E402

LETTER = {"M": "MOSFET", "Q": "BJT", "J": "JFET", "D": "diode",
          "R": "resistor", "C": "capacitor", "L": "inductor",
          "E": "VCVS(E)", "G": "VCCS(G)", "F": "CCCS(F)", "H": "CCVS(H)",
          "B": "behavioral(B)", "S": "switch(S)", "X": "subckt-inst(X)",
          "V": "Vsource", "I": "Isource"}


def card_letters(path):
    out = set()
    for ln in _read_text(path).splitlines():
        s = ln.strip()
        if not s or s[0] in "*." :
            continue
        c = s[0].upper()
        if c in LETTER:
            out.add(c)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="benchmark/gen")
    ap.add_argument("--optimize", action="store_true")
    args = ap.parse_args()
    files = sorted(glob.glob(os.path.join(args.dir, "**", "*.cir"),
                             recursive=True))
    if not files:
        print(f"no .cir under {args.dir}"); return 1

    t0 = time.time()
    out = Counter()
    ftype = Counter()                       # failure-type histogram
    by_dev = defaultdict(lambda: [0, 0])    # letter -> [verified, total]
    by_size = defaultdict(lambda: [0, 0])
    for f in files:
        letters = card_letters(f)
        try:
            d = parse_file(f); classify_design(d); _register_top(d)
        except Exception as e:
            out["parse_fail"] += 1
            ftype["parse:" + type(e).__name__] += 1
            continue
        names = [n for n in d.order if d.subckts[n].devices]
        if not names:
            out["empty"] += 1
            continue
        sub = d.subckts[names[0]]
        nd = len(sub.devices)
        bucket = "1-8" if nd <= 8 else ("9-16" if nd <= 16 else
                                        ("17-32" if nd <= 32 else "33+"))
        try:
            if args.optimize:
                sh, r, _ = _best_placement(sub)
            else:
                sh = place(sub); r = route(sh)
            ok = verify(r).ok
            if ok:
                out["verified"] += 1
            else:
                out["mismatch"] += 1
                e0 = verify(r).errors[0]
                ftype["OPEN" if e0.startswith("OPEN") else
                      ("SHORT" if "SHORT" in e0 else "other")] += 1
        except Exception as e:
            out["crash"] += 1
            ftype["crash:" + type(e).__name__] += 1
            ok = False
        by_size[bucket][0] += ok; by_size[bucket][1] += 1
        for c in letters:
            by_dev[c][0] += ok; by_dev[c][1] += 1

    valid = out["verified"] + out["mismatch"] + out["crash"]
    rate = 100 * out["verified"] / valid if valid else 0
    bar = "=" * 64
    print(bar)
    print(f"SpiceGlass conversion benchmark — {len(files)} netlists  "
          f"(optimizer {'on' if args.optimize else 'off'})")
    print(bar)
    print(f"  invalid-format {out['parse_fail']}   no-devices {out['empty']}"
          f"   crashes {out['crash']}")
    print(f"  VERIFIED {out['verified']}/{valid}  ({rate:.1f}%)   "
          f"mismatch {out['mismatch']}")
    print(f"  time {time.time() - t0:.0f}s")

    def table(title, d, order=None):
        print(f"\n  {title}")
        keys = order or sorted(d, key=lambda k: -d[k][1])
        for k in keys:
            ok, tot = d[k]
            if tot:
                name = LETTER.get(k, k)
                print(f"    {name:16} {ok:5}/{tot:<5} {100*ok//tot:3d}%")

    table("verify rate by device type present:", by_dev)
    table("verify rate by size (devices):", by_size,
          order=["1-8", "9-16", "17-32", "33+"])
    print("\n  failure types:")
    for k, v in ftype.most_common():
        print(f"    {k:22} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
