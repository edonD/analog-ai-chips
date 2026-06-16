"""Generative conversion benchmark — score the .cir -> .asc engine on a
corpus of AI-generated analog netlists.

The intended product workflow is: an AI writes a SPICE netlist, and the
engine converts it to an editable, PROVABLY-CORRECT schematic. This
benchmark measures exactly that: over a directory of generated .cir
files it reports how many are valid-format, how many convert AND pass the
round-trip verifier, and lists every failure as a coverage to-do.

Generate a corpus with the benchmark generator agents (writes to
benchmark/gen/), then:

    python tools/benchmark.py                 # score benchmark/gen
    python tools/benchmark.py --optimize      # with the layout optimizer
    python tools/benchmark.py --dir other/dir
"""
import argparse
import glob
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)               # for regress
sys.path.insert(0, os.path.join(_HERE, ".."))

from regress import scan                 # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="benchmark/gen")
    ap.add_argument("--optimize", action="store_true")
    args = ap.parse_args()

    files = glob.glob(os.path.join(args.dir, "**", "*.cir"), recursive=True)
    if not files:
        print(f"no .cir found under {args.dir} — generate a corpus first.")
        return 1
    t0 = time.time()
    out, crashes, mismatches = scan([args.dir], args.optimize)
    valid = out["verified"] + out["mismatch"] + out["crash"]
    rate = (100 * out["verified"] / valid) if valid else 0.0

    bar = "=" * 60
    print(bar)
    print(f"SpiceGlass conversion benchmark — {args.dir}")
    print(bar)
    print(f"  generated netlists    : {len(files)}")
    print(f"  invalid format        : {out['parse_fail']}")
    print(f"  no drawable devices   : {out['empty']}")
    print(f"  --- of {valid} valid, device-bearing netlists ---")
    print(f"  VERIFIED (correct)    : {out['verified']}   <-- {rate:.0f}%")
    print(f"  mismatch (wrong/ugly) : {out['mismatch']}")
    print(f"  crash                 : {out['crash']}")
    print(f"  optimizer             : {'on' if args.optimize else 'off'}")
    print(f"  time                  : {time.time() - t0:.1f}s")
    if crashes:
        print("\n  CRASHES:")
        for who, err in crashes:
            print(f"    {who}  {err}")
    if mismatches:
        print("\n  MISMATCHES (coverage to-do):")
        for who, err in mismatches:
            print(f"    {who}  | {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
