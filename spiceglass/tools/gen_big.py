"""Stress-test generator: tile bias_generator.asc into an NxM array to
measure parse + render performance at complex-circuit scale."""
import re
import sys
import time

sys.path.insert(0, ".")

src = open(r"examples\bias_generator.asc", encoding="utf-8").read()
lines = src.splitlines()

NX, NY = int(sys.argv[1]), int(sys.argv[2])
DX, DY = 1800, 700
out = ["Version 4", f"SHEET 1 {NX * DX} {NY * DY}"]
for ty in range(NY):
    for tx in range(NX):
        ox, oy = tx * DX, ty * DY
        tag = f"_{tx}_{ty}"
        for ln in lines:
            t = ln.split()
            if not t:
                continue
            h = t[0].upper()
            if h == "WIRE":
                out.append(f"WIRE {int(t[1])+ox} {int(t[2])+oy} "
                           f"{int(t[3])+ox} {int(t[4])+oy}")
            elif h == "FLAG":
                out.append(f"FLAG {int(t[1])+ox} {int(t[2])+oy} {t[3]}{tag}")
            elif h == "SYMBOL":
                out.append(f"SYMBOL {t[1]} {int(t[2])+ox} {int(t[3])+oy} "
                           f"{t[4]}")
            elif h == "SYMATTR" and t[1] == "InstName":
                out.append(f"SYMATTR InstName {t[2]}{tag}")
            elif h == "SYMATTR":
                out.append(ln)
open("big.asc", "w", encoding="utf-8").write("\n".join(out))

from glass.asc.parse import asc_to_svg, parse_asc

t0 = time.perf_counter()
sheet = parse_asc("big.asc")
t1 = time.perf_counter()
svg = asc_to_svg(sheet, ".")
t2 = time.perf_counter()
open("big.svg", "w", encoding="utf-8").write(svg)
elems = svg.count("<line") + svg.count("<circle") + svg.count("<text") \
    + svg.count("<path") + svg.count("<ellipse") + svg.count("<rect")
print(f"{NX}x{NY}: {len(sheet.insts)} symbols, {len(sheet.wires)} wires")
print(f"parse {1000*(t1-t0):.0f} ms, render {1000*(t2-t1):.0f} ms, "
      f"svg {len(svg)//1024} KB, ~{elems} svg elements")
