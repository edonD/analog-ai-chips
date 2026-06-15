"""Empirically determine LTspice's rotation/mirror point transforms:
for instances of symbols with KNOWN base pins, try candidate transforms
and count how many wire endpoints they hit across the corpus."""
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, ".")
from glass.asc.parse import parse_asc

BASE = {
    "res": [(16, 16), (16, 96)],
    "cap": [(16, 0), (16, 64)],
    "voltage": [(0, 16), (0, 96)],
    "diode": [(16, 0), (16, 64)],
    "npn": [(64, 0), (0, 48), (64, 96)],
    "ind": [(16, 16), (16, 96)],
}

CAND = {
    "A": lambda x, y: (y, -x),     # my current R90
    "B": lambda x, y: (-y, x),     # the opposite R90
    "C": lambda x, y: (-x, -y),    # 180
    "D": lambda x, y: (-x, y),     # mirror X
    "E": lambda x, y: (x, -y),     # mirror Y
    "F": lambda x, y: (y, x),
    "G": lambda x, y: (-y, -x),
    "I": lambda x, y: (x, y),
}

corpus = os.path.expandvars(r"%TEMP%\asc_corpus")
score: dict[str, Counter] = defaultdict(Counter)
n_inst: Counter = Counter()

for root, _d, files in os.walk(corpus):
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
            if name not in BASE or inst.rot == "R0":
                continue
            n_inst[inst.rot] += 1
            for key, t in CAND.items():
                hits = sum(1 for (px, py) in BASE[name]
                           if (inst.x + t(px, py)[0],
                               inst.y + t(px, py)[1]) in pts)
                score[inst.rot][key] += hits

for rot in sorted(score):
    top = score[rot].most_common(3)
    print(f"{rot}: n={n_inst[rot]:3d}  " +
          "  ".join(f"{k}={c}" for k, c in top))
