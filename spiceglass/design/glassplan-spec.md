# GlassPlan Language Specification — v1

**Status:** normative for `glassplan 1` files (2026-06-11).
**Prior art studied:** LTspice `.asc` (line-based, absolute coords on a
16-unit grid, 8 orientations, explicit WIRE segments, Version header);
xschem `.sch` (instances + net segments, rot/flip); Cadence
Virtuoso/OpenAccess (instance transforms with the 8-element orientation
group R0/R90/R180/R270/MX/MY/MX90/MY90; connectivity derived from
geometry — same philosophy as our verifier); EDIF (hierarchical
cell/view/instance). HSPICE has no schematic representation (simulator
only). All of them are COORDINATE-level formats; GlassPlan deliberately
sits one level above (placement *intent*), with a complete escape hatch
down to coordinates so anything expressible in `.asc` is expressible
here.

## 1. Lexical rules

- Encoding UTF-8; a leading BOM is tolerated and ignored.
- Line-based. `#` starts a comment anywhere on a line (outside quotes).
- A trailing `\` continues the logical line onto the next physical line.
- Tokens: bare words, `"quoted strings"` (no escapes; no inner quotes),
  bracketed columns `[A B C]`, parenthesized lists `kw(A B)`.
- Keywords are lowercase and reserved at line-head position only:
  `glassplan plan mirror core5t pair diode-link lateral flow region
  orient shift place wire via path grid from`.
- Device and group names are case-sensitive and must match
  `[A-Za-z_][A-Za-z0-9_.\-]*`; they may not collide with keywords at
  line-head.

## 2. File structure

```
glassplan 1                      # version token, line 1 (required in v1;
                                 # absent -> treated as v0 with a warning)
plan NAME from NETLIST grid 1mm  # sheet header

<structure lines>                # any order
flow
  <region lines>                 # order = left-to-right narrative
<exception lines>                # any order
```

## 3. Structure lines (what the circuit IS)

```
mirror NAME = DEV DEV ...            # gate-tied bank, members left->right
core5t NAME = pair(A B) tail(T) loads(L1 L2) diode(D)
pair   NAME = pair(A B) [tail(T)]
diode-link = DEV ...                 # drawn gate-drain links
lateral    = DEV ...                 # default orientation R90
```
Semantics: structure lines declare tiles. `diode` must be a member of
the same group. Group names must be unique per plan.

## 4. Flow (how it READS)

```
region "Title" ITEM ITEM ...
ITEM := GROUPNAME | [DEV DEV ...]
```
- Regions are ordered left→right; items within a region likewise.
- `[A B C]` is a column, top (VDD side) to bottom (GND side).
- Region identity is POSITIONAL; titles need not be unique (duplicate
  titles share one shading box — discouraged but legal). Empty title
  `""` = unshaded region.
- TOTALITY (hard error otherwise): every netlist device appears exactly
  once across flow items (group members count via their group).

## 5. Exceptions (escape hatches, in increasing strength)

```
orient DEV O          # O in {R0 R90 R180 R270 MX MY MX90 MY90}
shift  DEV dx dy      # whole grid units, relative to realized slot
place  DEV x y        # ABSOLUTE grid coordinates (overrides slot)
wire   NET path x,y x,y x,y ...   # full pinned polyline (orthogonal,
                                  # integer grid); repeatable per net
wire   NET via x,y                # v0 compatibility; treated as a hint,
                                  # currently ignored with a warning
```
- The orientation set is the 8-element symmetry group of the square,
  matching LTspice/OpenAccess. Pin transforms: R90 (x,y)->(y,-x) and
  composition; MX mirrors horizontally, MY vertically.
- `wire ... path` polylines are routed verbatim IF they still touch
  every drawn pin of the net; otherwise dropped with a warning and the
  net auto-routes (same self-healing rule as editor-pinned wires).
- Realization remains deterministic: plan + netlist fully determine the
  schematic; the verifier still proves netlist ≡ drawing.

## 6. Diagnostics

Parsers MUST report the line number with every error/warning.
Realization errors name the offending devices ("does not place: X",
"places twice: Y").

## 7. Versioning & compatibility

- `glassplan 1` is this spec. Files without the token parse as v0
  (current emitter output) with a warning; the emitter now writes v1.
- Unknown line-head keywords are warnings, not errors (forward compat).

## 8. Deferred (v1.1 candidates, by demonstrated need)

- 2-D region composition (`row`/`stack` so a mirror bank can sit ABOVE
  its core columns — the classic beta-multiplier drawing; needs realizer
  support for vertical object stacking).
- `align A B ...` row-alignment hints across columns.
- Hierarchical sheet instances (plan-per-subckt references; today each
  subckt simply has its own plan).
- Pattern-library references (P4) once motifs are external data.
