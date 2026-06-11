"""GlassPlan P1 acceptance: an untouched auto-generated plan must
realize to EXACTLY the coordinates the automatic placer produces, for
every sheet, and stay VERIFIED. Run: python -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from glass import load                                  # noqa: E402
from glass.place import place                           # noqa: E402
from glass.plan import parse_plan, plan_for, realize_plan  # noqa: E402
from glass.route import route                           # noqa: E402
from glass.verify import verify                         # noqa: E402

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
NETLISTS = [
    r"vibrosense\00_bias\design.cir",
    r"vibrosense\00_bias\bias_distribution\design_full.cir",
    r"vibrosense\04_envelope\design.cir",
    r"vibrosense\05_rms_crest\design.cir",
]


def coords(sheet):
    return {n: (p.x, p.y, p.orient) for n, p in sheet.placed.items()}


class PlanRoundTrip(unittest.TestCase):
    def test_auto_plan_identity(self):
        for rel in NETLISTS:
            path = os.path.join(REPO, rel)
            for name in load(path).order:
                # fresh parses: place() mutates Device.section
                ref = place(load(path).subckts[name])
                design = load(path)
                text = plan_for(design, name)
                plan = parse_plan(text)
                fresh = load(path)
                sheet = realize_plan(fresh.subckts[name], plan)
                self.assertEqual(coords(ref), coords(sheet),
                                 f"{rel}:{name} plan round-trip drifted")
                verdict = verify(route(sheet))
                self.assertTrue(verdict.ok,
                                f"{rel}:{name} plan render not verified: "
                                f"{verdict.errors}")

    def test_plan_validation(self):
        path = os.path.join(REPO, NETLISTS[0])
        design = load(path)
        name = design.root().name
        text = plan_for(design, name)
        # remove one device from its column -> must be reported missing
        broken = text.replace("XM6 ", "").replace("[XM6]", "[]")
        with self.assertRaises(ValueError):
            realize_plan(load(path).subckts[name], parse_plan(broken))


if __name__ == "__main__":
    unittest.main()
