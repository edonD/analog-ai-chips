# SpiceGlass

**SPICE netlist → readable, *verified* analog schematic.** An open
SpiceVision for the AI design era — when the netlist is written by an AI,
the schematic is how the human stays in the loop.

Status: **M0 complete** (program.md has the full M0–M5 roadmap).

![bias generator](examples/bias_generator.png)

## What works today (M0)

- **Integer grid core**: the whole pipeline thinks in grid units (1 unit =
  10 px only at the render boundary). Every symbol is a fixed-size tile
  with pins on grid crossings (MOSFET 6×8: G(−3,0), D/S(+2,∓4), B(+3,0);
  2-terminal devices 4×8; subckt boxes sized by port count) — any `.cir`
  device maps to *some* tile, which is what keeps the converter general.
  Columns sit every 18 units, rows every 14, leaving 6 integer wiring
  tracks per row band and whole-unit vertical lanes. Placement, routing,
  and verification are exact integer math — no epsilons anywhere.
- **ngspice-subset parser**: `.subckt` hierarchy, Sky130 PDK `X`-instances,
  plain R/C/L, B/G behavioral sources with expressions, `+` continuations
- **Analog-aware placement** (deterministic, no LLM anywhere):
  rails folded to stubs, every VDD→GND source-drain path drawn as a vertical
  column (PMOS up, NMOS down), columns ordered by the netlist's own section
  comments, rows anchored by rail distance so differential pairs and mirrors
  align automatically, lateral switches rejected from stacks by
  monotonic-rail-progress chaining
- **Orthogonal routing** with per-lane collision avoidance, junction dots,
  net labels for high-fanout bias nets, port flags
- **Round-trip verification**: connectivity is re-extracted from the drawn
  geometry and checked against the input netlist (opens, shorts, collinear
  track overlaps). Every sheet carries a `VERIFIED ✓` / `MISMATCH ✗` stamp —
  during M0 bring-up this caught a real router short (stacked subckt-box
  pins) that was invisible to the eye.

## Interactive editor

`python -m glass edit design.cir` — browser editor with: device dragging
(R rotate / M mirror), **draggable wire segments** (grab any middle
segment; double-click a wire to add a jog; hand-edited nets are pinned,
drawn blue, persisted in the sidecar and respected by the router), grid
dots, live re-route + re-verify on every drop, an `/algo` page that
visualizes the routing pipeline (visibility graph, A* replay, nudging),
and a `/symbols` page — a pixel-style half-unit-grid symbol designer
(pins fixed by the grid contract, artwork yours; saved to symbols.json
and used by every renderer).

## Usage

```
cd spiceglass
python -m glass render ..\vibrosense\00_bias\design.cir -o out.svg
python -m glass render design.cir --all            # every subckt in the file
python -m glass render design.cir --subckt ota5 --png   # PNG via headless Edge
python -m glass json design.cir                    # circuit DB as JSON
python -m unittest discover -s tests               # golden regression
```

Zero dependencies — Python 3.10+ stdlib only.

## Examples (all auto-generated, all verified)

| Sheet | Source |
|---|---|
| ![ota5](examples/ota5.png) | `05_rms_crest` — 5T OTA |
| ![rms top](examples/rms_crest_top.png) | `05_rms_crest` — hierarchical top |

## Next (per program.md)

M1: parallel-device merge (×20 OTA fingers), diff-pair/mirror motif
recognition with mirrored placement, diode-connection wires.
M2: cone extraction + cookie-cutting. M3: ngspice OP overlay, doc
generation, xschem export. M4: interactive viewer. M5: logic recognition,
agent API.
