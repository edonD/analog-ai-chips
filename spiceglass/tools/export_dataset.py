"""Export the (netlist -> verified placed schematic) dataset.

The endgame: learned placement/recognition needs ground-truth pairs. Every
generated netlist that the converter places AND the round-trip verifier
accepts is a labelled training example — netlist graph in, device
coordinates out, correctness guaranteed.

Each JSONL record (schema in docs/DATASET.md):
  name, topology, ports, nets,
  devices:[{name,kind,model,nets,roles,params, x,y,orient}],  # x/y = label
  wires:[[x1,y1,x2,y2,net]], verified, n_devices, n_nets

Only verified records are written (the corpus is the moat). Deterministic
for a fixed corpus.

    python tools/gen_realistic.py --count 2000 --out benchmark/real --seed 1
    python tools/export_dataset.py --dir benchmark/real --out dataset/real.jsonl
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_file                 # noqa: E402
from glass.engine.classify import classify_design           # noqa: E402
from glass.engine.verify import verify                      # noqa: E402
from glass.web.server import _best_placement, _register_top  # noqa: E402


def record(name, topology, sub, sheet, routing, ok) -> dict:
    devs = []
    for d in sub.devices:
        p = sheet.placed.get(d.name)
        devs.append({
            "name": d.name, "kind": d.kind, "model": d.model,
            "nets": list(d.nets), "roles": list(d.roles),
            "params": dict(d.params),
            "x": (p.x if p else None), "y": (p.y if p else None),
            "orient": (p.orient if p else None),
        })
    wires = [[int(s.x1), int(s.y1), int(s.x2), int(s.y2), s.net]
             for s in routing.segments]
    return {
        "name": name, "topology": topology,
        "ports": list(sub.ports), "nets": sorted(sub.nets()),
        "devices": devs, "wires": wires,
        "verified": bool(ok),
        "n_devices": len(sub.devices), "n_nets": len(sub.nets()),
    }


def export(dirpath, outpath) -> tuple[int, int]:
    files = sorted(glob.glob(os.path.join(dirpath, "**", "*.cir"),
                             recursive=True))
    os.makedirs(os.path.dirname(os.path.abspath(outpath)) or ".",
                exist_ok=True)
    written = skipped = 0
    with open(outpath, "w", encoding="utf-8", newline="\n") as out:
        for f in files:
            base = "_".join(os.path.basename(f)[:-4].split("_")[:-1]) \
                or os.path.basename(f)[:-4]
            try:
                d = parse_file(f)
                classify_design(d)
                _register_top(d)
                names = [n for n in d.order if d.subckts[n].devices]
                if not names:
                    skipped += 1
                    continue
                sub = d.subckts[names[0]]
                sheet, routing, _ = _best_placement(sub)
                ok = verify(routing).ok
            except Exception:
                skipped += 1
                continue
            if not ok:                       # only verified pairs are labels
                skipped += 1
                continue
            out.write(json.dumps(record(os.path.basename(f)[:-4], base,
                                         sub, sheet, routing, ok)) + "\n")
            written += 1
    return written, skipped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="benchmark/real")
    ap.add_argument("--out", default="dataset/spiceglass.jsonl")
    args = ap.parse_args()
    w, s = export(args.dir, args.out)
    print(f"wrote {w} verified (netlist -> placed schematic) records to "
          f"{args.out}  (skipped {s} unverified/empty)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
