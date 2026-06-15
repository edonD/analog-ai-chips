"""Golden regression: every real vibrosense netlist must place, route,
and round-trip VERIFY on every sheet. Run:  python -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from glass import load                      # noqa: E402
from glass.engine.place import place               # noqa: E402
from glass.engine.route import route               # noqa: E402
from glass.engine.verify import verify             # noqa: E402

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
NETLISTS = [
    r"vibrosense\00_bias\design.cir",
    r"vibrosense\00_bias\bias_distribution\design_full.cir",
    r"vibrosense\04_envelope\design.cir",
    r"vibrosense\05_rms_crest\design.cir",
]


class GoldenVerify(unittest.TestCase):
    def test_all_sheets_verify(self):
        total_sheets = 0
        for rel in NETLISTS:
            path = os.path.join(REPO, rel)
            design = load(path)
            self.assertTrue(design.order, f"{rel}: no subckts parsed")
            for name in design.order:
                sub = design.subckts[name]
                sheet = place(sub)
                routing = route(sheet)
                verdict = verify(routing)
                self.assertTrue(
                    verdict.ok,
                    f"{rel}:{name} failed verification: {verdict.errors}")
                placed = {d.name for d in sub.devices} - set(sheet.placed)
                self.assertFalse(placed, f"{rel}:{name} unplaced: {placed}")
                total_sheets += 1
        self.assertGreaterEqual(total_sheets, 8)

    def test_terminal_accounting(self):
        """No silent drops: every netlist terminal appears in the routing."""
        path = os.path.join(REPO, NETLISTS[0])
        design = load(path)
        sub = design.root()
        sheet = place(sub)
        routing = route(sheet)
        want = sum(len(d.nets) for d in sub.devices)
        self.assertEqual(len(routing.terminals), want)


if __name__ == "__main__":
    unittest.main()
