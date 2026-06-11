"""Dev helper: render a plan (or netlist) to a width-capped PNG for
visual review.  usage: python shot.py <plan|cir> [out.png] [maxw]"""
import sys

sys.path.insert(0, ".")
from glass.classify import classify_design
from glass.parser import parse_file
from glass.place import place
from glass.plan import parse_plan, realize_plan
from glass.render_svg import render_sheet
from glass.route import route
from glass.snapshot import svg_to_png_bytes
from glass.verify import verify
import os

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "shot.png"
maxw = int(sys.argv[3]) if len(sys.argv) > 3 else 1900

if src.endswith(".plan"):
    with open(src, encoding="utf-8") as fh:
        plan = parse_plan(fh.read())
    net = os.path.join(os.path.dirname(os.path.abspath(src)), plan.source)
    design = parse_file(net)
    classify_design(design)
    sheet = realize_plan(design.subckts[plan.name], plan)
else:
    design = parse_file(src)
    classify_design(design)
    sheet = place(design.root())

routing = route(sheet)
verdict = verify(routing)
svg = render_sheet(sheet, routing, verdict, {"path": "", "date": ""})
png = svg_to_png_bytes(svg, max_w=maxw)
with open(out, "wb") as fh:
    fh.write(png)
print(f"{'VERIFIED' if verdict.ok else 'MISMATCH: ' + str(verdict.errors)}"
      f" -> {out}")
