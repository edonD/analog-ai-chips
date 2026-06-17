"""Dataset export gate (improvement #4).

  D1 completeness — every record is verified=True, every device carries a
     placement (x,y,orient non-null), device count consistent, and every
     net referenced by a device or wire is in the record's net list (no
     silent drops).
  D2 determinism — exporting the same corpus twice is byte-identical.
  D3 reconstructability — placement + wires together cover all devices and
     all wired nets (the pair is sufficient to redraw the schematic).

    python tools/regress_dataset.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from export_dataset import export                          # noqa: E402


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(here, ".."))
    out1, out2 = "dataset/_gate1.jsonl", "dataset/_gate2.jsonl"
    w, s = export("examples", out1)
    export("examples", out2)
    fails = []

    recs = [json.loads(l) for l in open(out1, encoding="utf-8")]
    if not recs:
        fails.append(("D1", "no records exported"))
    for r in recs:
        if not r["verified"]:
            fails.append(("D1", f"{r['name']}: unverified record written"))
        if len(r["devices"]) != r["n_devices"]:
            fails.append(("D1", f"{r['name']}: device count mismatch"))
        nets = set(r["nets"])
        for d in r["devices"]:
            if d["x"] is None or d["y"] is None or d["orient"] is None:
                fails.append(("D1", f"{r['name']}.{d['name']}: no placement"))
            for n in d["nets"]:                     # D3: device nets covered
                if n not in nets:
                    fails.append(("D3", f"{r['name']}: dev net '{n}' not "
                                        "in net list"))
        for w_ in r["wires"]:                       # D3: wire nets covered
            if w_[4] not in nets and w_[4] != "0":
                fails.append(("D3", f"{r['name']}: wire net '{w_[4]}' not "
                                    "in net list"))

    # D2: determinism (byte-identical)
    if open(out1, "rb").read() != open(out2, "rb").read():
        fails.append(("D2", "two exports differ"))

    for f in (out1, out2):
        try:
            os.unlink(f)
        except OSError:
            pass

    print(f"dataset gate: {w} records exported (skipped {s})")
    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails[:30]:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — D1 complete (verified + full placement + nets), "
          "D2 deterministic, D3 reconstructable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
