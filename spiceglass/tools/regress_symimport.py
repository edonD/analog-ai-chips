"""PDK / hand-drawn symbol-import gate (E6).

Validates that SpiceGlass ingests real foundry/hand-drawn symbols end to
end — the foundation of PDK symbol fidelity. Uses the repo's actual xschem
.sym files.

  SI1 a real xschem .sym parses to a symbol with named pins + body lines
      (scaled onto our grid).
  SI2 it round-trips to .asy and back with the same pin names (so it
      resolves + renders in the editor).
  SI3 once imported into a dir on the resolve path, resolve_asy finds it.

Note: auto-substituting an imported symbol's PINS into routing (so a block
instance is laid out on the real symbol's pins) is the remaining
integration; this locks the ingest/render/resolve foundation it builds on.

    python tools/regress_symimport.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.asc import parse as ascparse                    # noqa: E402
from glass.asc.parse import parse_asy, resolve_asy          # noqa: E402
from glass.asc.import_sym import import_text, asy_text       # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SYMS = [
    "vibrosense/04_envelope/ota_pga_v2.sym",
    "vibrosense/03_filters/ota_foldcasc.sym",
    "vibrosense/03_filters/pseudo_res.sym",
]


def main() -> int:
    fails = []
    found = 0
    for rel in SYMS:
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            continue
        found += 1
        name = os.path.basename(rel)[:-4]
        content = open(p, encoding="utf-8", errors="replace").read()

        # SI1 parse
        got = import_text(content, "xschem")
        sym = got.get("imported")
        if not sym or not sym.pins or not sym.lines:
            fails.append((name, "SI1: no pins/lines parsed"))
            continue
        pin_names = {pn[2] for pn in sym.pins}
        if not all(isinstance(n, str) and n for n in pin_names):
            fails.append((name, "SI1: unnamed pins"))

        # SI2 round-trip to .asy and back
        with tempfile.TemporaryDirectory() as d:
            ap = os.path.join(d, name + ".asy")
            with open(ap, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(asy_text(sym, name))
            back = parse_asy(ap)
            if len(back.pins) != len(sym.pins):
                fails.append((name, f"SI2: pin count {len(back.pins)} != "
                                    f"{len(sym.pins)}"))
            if {q[2] for q in back.pins} != pin_names:
                fails.append((name, "SI2: pin names not preserved"))

            # SI3 resolve once on the path
            ascparse.EXTRA_SYM_DIRS.append(d)
            try:
                if resolve_asy(name, REPO) is None:
                    fails.append((name, "SI3: not resolved after import"))
            finally:
                ascparse.EXTRA_SYM_DIRS.remove(d)

        print(f"  {name:18} pins={len(sym.pins)} "
              f"({', '.join(sorted(pin_names))[:46]}) lines={len(sym.lines)}")

    if not found:
        print("SKIP — no repo .sym files present")
        return 0
    if fails:
        print(f"FAIL ({len(fails)}):")
        for n, m in fails:
            print(f"  {n}: {m}")
        return 1
    print("PASS — SI1 parse (named pins+body), SI2 .asy round-trip, "
          "SI3 resolves on the import path")
    return 0


if __name__ == "__main__":
    sys.exit(main())
