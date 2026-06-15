# Faithful symbol rendering — engines surveyed & decisions

*Date: 2026-06-15. How SpiceGlass renders real, correct symbols instead of
approximations.*

## The problem
Our first symbol set was hand-drawn glyphs with pins reverse-engineered
from a corpus — fine to look at, but pins were guesses, so wires didn't
always land and connectivity/DRC could be wrong. To be genuinely useful
we need **correct pins** (the electrical contract) and faithful artwork,
learning from the engines that do this well.

## Engines surveyed
- **xschem** (Stefan Schippers) — the de-facto open-source *analog IC*
  schematic tool (SKY130/IHP PDKs use it). `.sym` format: line-oriented,
  pins are boxes on layer 5 with `name/dir/pinnumber`; pin order = file
  order = SPICE order. Base `devices/` library is **GPL-2.0**; the
  **SKY130/IHP PDK symbol libs are Apache-2.0** (reusable). No native
  `.asy` export exists.
- **KiCad / KiCanvas** — largest symbol ecosystem. `.kicad_sym` S-expr,
  mm grid, rich pin electrical types, multi-unit + DeMorgan body styles,
  3-point arcs. Libraries are **CC-BY-SA-4.0 + a "libraries exception"**
  (the exception frees *your designs*, NOT redistribution of converted
  symbols — converting their geometry is copyleft Adapted Material).
  **KiCanvas itself is MIT** and its parser/pin-placement code is the best
  reference. KiCad documents the exact LTspice scale: 16 LTspice units =
  50 mil = 1.27 mm.
- **LTspice `.asy`** — our hub format. Full grammar recovered (LINE/
  RECTANGLE/CIRCLE/ARC/TEXT/WINDOW/PIN/PINATTR/SYMATTR; Normal/Wide width;
  style 0–4; pin orientation as a justification keyword; SpiceOrder is the
  netlist node order). **ADI's EULA forbids redistributing the `.asy`
  files** — so we cannot ship them.

## Decisions
1. **Clean-room library on real pins.** Pins are functional interop facts
   (uncopyrightable); the drawing is ours. We ship `glass/asc/symlib.py`:
   original artwork anchored to LTspice's *published* pin coordinates
   (cross-checked against open mirrors and our corpus). This is what KiCad
   and every community converter do — match coordinates so wires land,
   draw your own glyphs. **No vendor `.asy` is committed to the repo.**
2. **Real `.asy` still wins when present.** If an LTspice install or a
   sheet's local `sg_sym/` provides a `.asy`, that is used; `symlib` is the
   offline fallback. So the tool is faithful both ways.
3. **Full `.asy` rendering**: implemented ARC (bbox-ellipse + angle
   markers, CCW in y-down screen space) in both the server SVG path and
   the canvas client, so real LTspice symbols with arcs render.

## Verified pin coordinates (the contract)
Ground-truthed for: res/res2, cap/polcap, ind/ind2, diode (zener/
schottky/led), voltage (0,16)/(0,96), current (0,0)/(0,80), bv (0,16)/
(0,96), bi (0,0)/(0,80), e/g (4-pin VCVS/VCCS — g has +/− flipped),
f/h (2-pin), sw (terminals (0,16)/(0,96) + control (−48,32)/(−48,80)),
npn/pnp (C 64,0 · B 0,48 · E 64,96), nmos/pmos (D 48,0 · G 0,80 · S
48,96), nmos4/pmos4 (+ bulk 48,48), njf/pjf (D 48,0 · G 0,64 · S 48,96),
opamp (inverting input is SpiceOrder 1), opamp2/LT100x (5-pin),
UniversalOpamp2 (centred frame, negative-Y inputs).

## Result
Corpus dashed-box instances: **84 → 27**. The remaining 27 are
specialized parts (Gain block, NE555, SR flip-flop, transmission line,
optocoupler) left as honest dashed boxes rather than drawn with guessed
pins.

## Importer — built (`glass/asc/import_sym.py`)
A `.kicad_sym` (S-expr) and xschem `.sym` (line-oriented) parser converts
real libraries to our AsySymbol and writes faithful `.asy` into an import
dir the resolver searches. Verified against the real KiCad `Device`
library (571 symbols: R/C/L-with-arc-coils, diodes, BJT/MOSFET with
envelopes) and xschem `devices/`. Coordinate maps: KiCad mm × 16/1.27,
Y negated; xschem × 1.6; pins land on our 16-unit grid. 3-point KiCad
arcs → bbox+markers (CCW-passes-mid). The user imports their own files
(never bundled); `uploads/imported_sym/` is gitignored. The UI exposes it
as **Import lib…** + the imported symbols in the **+ Component** palette.

## Future (when wanted)
- Multi-unit explode (e.g. dual op-amps → unit 1 / unit 2 as separate
  symbols) and KiCad alternate body styles; carry pin electrical type.
- Carry pin names + SpiceOrder through to netlisting and name-aware DRC.
