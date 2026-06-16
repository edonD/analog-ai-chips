"""Converter regression harness — run the .cir -> .asc engine over a
corpus and flag anything that crashes or fails the round-trip verifier.

Two tiers:
  CORE  the in-house AI-generated blocks (vibrosense/, pvdd_regulator/).
        These MUST all verify — a CORE failure exits non-zero so a bad
        converter change can't land silently.
  WILD  third-party ngspice example decks (Spice64/), a different netlist
        class. Informational: prints the mismatch list as a to-do for
        broadening parser / placement / symbol coverage.

Usage (from the spiceglass/ dir):
    python tools/regress.py            # core + wild summary
    python tools/regress.py --wild     # also list every wild mismatch
    python tools/regress.py --core-only
Uses plain seed placement (fast); add --optimize to exercise the
verify-gated optimizer (slower).
"""
import argparse
import glob
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_file          # noqa: E402
from glass.engine.classify import classify_design    # noqa: E402
from glass.engine.place import place                 # noqa: E402
from glass.engine.route import route                 # noqa: E402
from glass.engine.verify import verify               # noqa: E402
from glass.web.server import _register_top, _best_placement  # noqa: E402

CORE = ["../vibrosense", "../pvdd_regulator"]
WILD = ["Spice64"]


def _cirs(roots):
    out = []
    for r in roots:
        out += glob.glob(os.path.join(r, "**", "*.cir"), recursive=True)
    return sorted(set(out))


def _run_sheet(sub, optimize):
    if optimize:
        sh, r, _ = _best_placement(sub)
    else:
        sh = place(sub); r = route(sh)
    return verify(r)


def scan(roots, optimize):
    out = Counter()
    crashes, mismatches = [], []
    for f in _cirs(roots):
        rel = os.path.relpath(f)
        try:
            d = parse_file(f); classify_design(d); _register_top(d)
        except Exception as e:
            out["parse_fail"] += 1
            crashes.append((rel, f"parse: {type(e).__name__}: {e}"))
            continue
        names = [n for n in d.order if d.subckts[n].devices]
        if not names:
            out["empty"] += 1
            continue
        for name in names:
            sub = d.subckts[name]
            tag = name if len(names) > 1 else ""
            try:
                v = _run_sheet(sub, optimize)
            except Exception as e:
                out["crash"] += 1
                crashes.append((f"{rel}:{name}", f"{type(e).__name__}: {e}"))
                continue
            if v.ok:
                out["verified"] += 1
            else:
                out["mismatch"] += 1
                mismatches.append((f"{rel}:{name}", v.errors[0]))
    return out, crashes, mismatches


def report(title, out, crashes, mismatches, show_mismatches):
    n = sum(out.values())
    print(f"\n=== {title}: {out['verified']} verified / "
          f"{out['mismatch']} mismatch / {out['crash']} crash / "
          f"{out['parse_fail']} parse-fail / {out['empty']} empty "
          f"({n} sheets) ===")
    for who, err in crashes:
        print(f"  CRASH    {who}  {err}")
    if show_mismatches:
        for who, err in mismatches[:60]:
            print(f"  mismatch {who}  | {err}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wild", action="store_true",
                    help="list every wild (ngspice) mismatch")
    ap.add_argument("--core-only", action="store_true")
    ap.add_argument("--optimize", action="store_true",
                    help="use the verify-gated optimizer (slower)")
    args = ap.parse_args()

    t0 = time.time()
    co, cc, cm = scan(CORE, args.optimize)
    report("CORE (must verify)", co, cc, cm, show_mismatches=True)
    wild_bad = 0
    if not args.core_only:
        wo, wc, wm = scan(WILD, args.optimize)
        report("WILD (ngspice examples — informational)", wo, wc, wm,
               show_mismatches=args.wild)
        wild_bad = len(wc)
    print(f"\nfinished in {time.time() - t0:.1f}s")

    core_bad = co["mismatch"] + co["crash"] + co["parse_fail"]
    if core_bad:
        print(f"FAIL: {core_bad} CORE sheet(s) regressed")
        return 1
    if wild_bad:
        print(f"note: {wild_bad} wild crash(es) — parser robustness gap")
    print("CORE clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
