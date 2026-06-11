# GlassPlan — the placement-intent language (design, v0)

**Status:** design for review (2026-06-11). Nothing implemented yet.
**Question answered:** what should be made *manually* to make the
algorithm's life easier, and is an intermediate "language" step the right
architecture for a SpiceVision-class automatic .cir → schematic drawer?

---

## 1. The diagnosis

Today's pipeline is:

```
design.cir ─parse→ CircuitDB ─[recognize+place+route, all in code]→ pixels
```

Every placement decision is **implicit inside the placer code**, and the
only persistent intermediate is the sidecar JSON of raw coordinates.
That has three structural problems:

1. **Corrections don't generalize.** When you drag XM6 two columns left,
   we record `XM6: x=152` — a fact about one instance of one sheet. The
   *reason* ("the leaker belongs with the startup group") is lost, so the
   algorithm can't learn it and the next netlist makes the same mistake.
2. **The hard part is entangled with the easy part.** "What is this
   circuit?" (mirrors, pairs, stacks, narrative order — *interpretation*)
   and "where exactly does everything sit?" (coordinates, tracks —
   *realization*) are different problems. Realization is deterministic
   and basically solved; interpretation is where quality lives. Mixing
   them in one pass means every interpretation fix risks the geometry.
3. **No good surface for a human (or an LLM) to intervene.** Pixels are
   too low-level; netlists carry no layout intent. There is no level at
   which you can say "this is a 3-output mirror bank; the OTA reads
   left-to-right after the core" — which is exactly how a designer thinks.

## 2. The proposal: a plan IR between netlist and geometry

```
design.cir ─parse→ CircuitDB
           ─interpret→  design.plan      ◄── the human/LLM-editable artifact
           ─realize→    coordinates      (deterministic, no heuristics)
           ─route→      wires            (OVG A* + nudging, as today)
           ─verify→     VERIFIED ✓       (unchanged, end-to-end)
```

**The plan is a text file** that states *structure* and *narrative*, not
coordinates:

```
plan bias_generator  from design.cir  grid 1mm

# ---- structure: what the circuit IS (recognizer output; correct freely)
mirror PMIR   = XM3 XM4 XM7              # gate=vbias, source=vdd
core5t OTA    = pair(XMo1 XMo2) tail(XMo5) loads(XMo3 XMo4) diode(XMo3)
diode-link    = XM1
lateral       = XMsw

# ---- narrative: how it READS, left to right; [..] = a column, top→bottom
flow
  region "Bias core"      PMIR  [XM1]
  region "Beta multiplier" [XM2 XR1a XR1b]
  region "Regulation OTA"  OTA  [XC_comp]
  region "Protection"      [XM6]
  region "Startup"         [XC_gs XR_gs]  [XMsw]

# ---- exceptions (escape hatches, all optional)
orient XMsw R90
shift  XC_comp +1 0          # one grid unit right of its slot
wire   out_n via 38,35       # pin a route through a point
```

Properties that make this the right contract:

- **Deterministic realization.** Same plan → same schematic, always.
  The realizer is the *existing* placer minus all guessing: stack columns
  by rail distance, mirror banks at tile pitch, anchor rows — pure
  mechanical geometry from declared relations.
- **Total and verifiable.** Every device appears exactly once (checked);
  realize→route→verify proves the drawing equals the netlist. A plan
  cannot produce a silently wrong schematic.
- **Three authors, one language.** The algorithm *generates* a plan; the
  human *edits* it (text, or via editor gestures that patch it); an LLM
  can *write or critique* one — and because realization+verification are
  deterministic, an LLM contributing at this level cannot break
  correctness. This is the sane version of Schemato: the model emits
  structure, never coordinates.
- **Corrections become teachable.** Plan diffs are semantic ("XM6 moved
  from region Protection to Startup", "C_comp ordered after OTA").
  Recurring diffs convert directly into interpreter rules — the
  adaptation loop we wanted, at the right abstraction level.

## 3. What gets made manually (ranked by leverage)

1. **Golden plans (~30 min each, do 3–5).** Hand-write the *ideal* plan
   for bias_generator, ota5, peak_detector, one testbench. These define
   "correct output" for the interpreter, become regression goldens
   (interpreter output diffed against them), and force the language to
   be expressive enough for real circuits. Highest leverage per minute
   of any manual work we can do.
2. **Pattern library (one-time, with me).** Today mirror/pair/5T/diode
   are hard-coded. Externalize each motif as a data entry:
   *match* (subgraph: device kinds + shared-net roles) +
   *draw* (relative tile slots + internal wires + exposed pins).
   ~15–20 entries cover most analog sheets: mirror bank, cascode mirror,
   wide-swing mirror, diff pair (+tail/+loads), cascode stack, source
   follower, level shifter, inverter, TG, RC compensation, divider
   string, beta-multiplier core, bandgap core. Each entry authored once
   fixes every future occurrence everywhere. (ALIGN validated exactly
   this: 21 templates + exact matching, TCAD 2023.)
3. **Style sheet (10 minutes, yours).** Your conventions as config, not
   code constants: supply-net regexes beyond vdd/gnd, bias-net naming
   (vbn/vbp/vbcn…), port-side rules (which names are inputs), label
   fanout threshold, region spacing, section-title style.
4. **Symbol artwork** (have the designer already; cosmetic, ongoing).
5. **Keep editing schematics** — after the editor starts saving plan
   patches instead of raw coordinates, every manual session produces
   generalizable training signal as a side effect.

## 4. Syntax candidates (decision needed)

A) **Netlist-flavored DSL** (shown above): line-oriented, comments with
   `#`, reads like the SPICE world you live in; needs a ~150-line parser.
B) **JSON**: zero parser work, machine-perfect, miserable to hand-edit
   (quoting, commas, no comments).
C) **TOML-ish sections**: middle ground; comments allowed; nesting
   awkward for ordered columns-within-regions.

Recommendation: **A**. The whole point is a file a designer edits as
naturally as a netlist; we control the parser (we already parse SPICE).
JSON remains the editor↔server wire format internally either way.

## 5. Migration plan (each step shippable, verified)

- **P1 — emit & consume.** `glass plan design.cir` writes `design.plan`
  (auto-generated from today's recognizer+heuristics). `glass render
  --plan design.plan` realizes it. Acceptance: untouched auto-plan
  renders byte-identical to today's output for all 8 sheets, VERIFIED.
- **P2 — goldens.** Hand-write golden plans for 3 blocks; tune the
  realizer until the goldens render the way you want; interpreter scored
  by diff-to-golden (new metric next to glass score).
- **P3 — editor speaks plan.** Save emits plan patches (region/order/
  orient/shift/wire) instead of raw coordinates; the sidecar JSON becomes
  derived state. Dragging across regions = `region` patch; reordering
  columns = order patch; small nudge = `shift`.
- **P4 — pattern library externalized.** Motif match+draw entries as
  data; recognizer = generic matcher over the library.
- **P5 — style sheet.**
- **P6 (optional, later) — LLM interpreter.** Claude reads netlist →
  emits plan → realize+verify+score, compared against the algorithmic
  plan. Best verified plan wins. Zero correctness risk by construction.

## 6. Honest risks

- **An IR can just relocate the pain** if the realizer is weak. Ours is
  the already-working placer stripped of guessing — the risky half stays
  behind the IR, which is the point.
- **Two sources of truth** (plan vs coordinate sidecar) would be worse
  than one. Resolution: the plan subsumes the sidecar; raw coordinates
  survive only as `shift` overrides *inside* the plan. One file.
- **Language scope creep.** v0 stays small: groups, flow/regions/columns,
  orient, shift, wire-via. No conditionals, no variables, no macros —
  it's a description, not a program.
