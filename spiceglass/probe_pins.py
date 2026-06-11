"""Derive LTspice native-symbol pin offsets empirically: across the
corpus, wire endpoints near an instance, inverse-transformed into
symbol-local coordinates, cluster at the true pin positions."""
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, ".")
from glass.parse_asc import parse_asc

INV = {
    "R0": lambda x, y: (x, y), "R90": lambda x, y: (-y, x),
    "R180": lambda x, y: (-x, -y), "R270": lambda x, y: (y, -x),
    "M0": lambda x, y: (-x, y), "M180": lambda x, y: (x, -y),
    "M90": lambda x, y: (y, x), "M270": lambda x, y: (-y, -x),
}

corpus = os.path.expandvars(r"%TEMP%\asc_corpus")
hits: dict[str, Counter] = defaultdict(Counter)
ninst: Counter = Counter()

for root, _dirs, files in os.walk(corpus):
    for f in files:
        if not f.lower().endswith(".asc"):
            continue
        try:
            sheet = parse_asc(os.path.join(root, f))
        except Exception:
            continue
        pts = set()
        for (x1, y1, x2, y2) in sheet.wires:
            pts.add((x1, y1))
            pts.add((x2, y2))
        for (x, y, _n) in sheet.flags:
            pts.add((x, y))
        for inst in sheet.insts:
            name = inst.sym.split("\\")[-1].lower()
            inv = INV.get(inst.rot)
            if inv is None:
                continue
            ninst[name] += 1
            for (px, py) in pts:
                dx, dy = px - inst.x, py - inst.y
                if abs(dx) <= 160 and abs(dy) <= 160:
                    hits[name][inv(dx, dy)] += 1

for name, n in ninst.most_common(14):
    common = [(pt, c) for pt, c in hits[name].most_common(8)
              if c >= max(2, 0.4 * n)]
    print(f"{name:12s} n={n:4d}  pins~ " +
          "  ".join(f"{pt}x{c}" for pt, c in common))
