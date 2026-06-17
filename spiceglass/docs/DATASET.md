# SpiceGlass Dataset — (netlist → verified placed schematic)

The endgame is learned placement/recognition. SpiceGlass already produces
the one thing such models need and that is otherwise expensive: **ground-
truth pairs** — a netlist graph in, device coordinates out, with
**correctness guaranteed by the round-trip verifier**. Every generated
netlist the converter places *and* the verifier accepts is a labelled
example.

## Build it

```bash
cd spiceglass
# 1. generate a corpus (seeded, reproducible) — flat and/or hierarchical
python tools/gen_realistic.py --count 5000 --out benchmark/real --seed 1
python tools/gen_hier.py      --count 1500 --out benchmark/hier --seed 1
# 2. export verified (netlist -> placement) records
python tools/export_dataset.py --dir benchmark/real --out dataset/real.jsonl
python tools/export_dataset.py --dir benchmark/hier --out dataset/hier.jsonl
```

Only **verified** records are written — the corpus is the moat. The export
is deterministic for a fixed corpus. Generators and bulk corpora are
seed-reproducible; `dataset/` is gitignored (regenerate any size).

## Record schema (JSONL, one object per line)

| field | type | meaning |
|-------|------|---------|
| `name` | str | unique sample id (filename stem) |
| `topology` | str | family (e.g. `ota_folded_cascode`, `bandgap_ldo`) — a label |
| `ports` | [str] | subckt ports |
| `nets` | [str] | every net (the connectivity vocabulary) |
| `devices` | [obj] | one per device (below) |
| `wires` | [[x1,y1,x2,y2,net]] | routed geometry (the drawn nets) |
| `verified` | bool | always true in an export (round-trip verifier label) |
| `n_devices`, `n_nets` | int | sizes |

Each **device**:

| field | type | meaning |
|-------|------|---------|
| `name` | str | instance name |
| `kind` | str | nmos/pmos/res/cap/dio/npn/pnp/sub/… |
| `model` | str | model / subckt name |
| `nets` | [str] | connected nets, in pin order |
| `roles` | [str] | pin roles aligned to `nets` (d/g/s/b, p/n, …) |
| `params` | obj | w/l/m/nf/value/… |
| **`x`, `y`, `orient`** | int,int,str | **the placement label** (grid units, LTspice orient) |

So the supervised target is straightforward: given `(devices without
x/y/orient, nets, ports)` predict `(x, y, orient)` per device; `wires`
gives the routed result for routing models; `topology` is a recognition
label.

## Why this is unusual
- **Correctness, not just plausibility.** Public schematic datasets are
  scraped/heuristic; here every pair passes a connectivity proof
  (`verify.py`), so labels are clean.
- **Unlimited, balanced, parameterized.** 75 flat topologies + 25
  hierarchical systems, any count, any seed; the family is a free label.
- **Reconstructable.** placement + wires redraw the exact schematic (gate
  D3), so records are self-contained.

## Gate
`tools/regress_dataset.py` — D1 completeness (verified, full placement, no
dropped nets), D2 determinism (byte-identical re-export), D3
reconstructability (placement + wires cover all devices/nets).
