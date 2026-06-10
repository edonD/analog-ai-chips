# SpiceGlass — An Open SpiceVision for the AI Design Era

**Program written:** 2026-06-10
**Mission:** Build what SpiceVision PRO is — *"takes any SPICE netlist, SPICE model and extracted parasitic netlist and generates clean, easy-to-read transistor-level schematics, and design documentation to speed up circuit design, circuit debugging, and circuit optimization at the transistor-level"* — open-source, ngspice-native, and designed for a world where the netlists are written by AI.
**Name:** working title `SpiceGlass` (a looking glass for SPICE). Alternatives: NetScope, OpenVision, cir2sch. Rename freely; nothing below depends on it.

---

## Part 0 — Why this can succeed where every open attempt died

Every prior open-source attempt (asg 2020, netlist-viewer 2010) died at the same step: making *arbitrary* netlists *readable*. We change the problem in three ways:

1. **Scope discipline.** First-class input is what our AI flows emit: ngspice netlists built from PDK primitives (`sky130_fd_pr__*` X-instances), one `.subckt` per block, 15–60 devices per sheet. Not 50M-device tape-out CDL. SpiceVision's "64-bit database for today's largest SoCs" is explicitly **out of scope** — hierarchy + cone views replace brute capacity.
2. **2023–2026 ingredients that didn't exist when asg died.** ALIGN's verified structure recognition (VF2 templates + GraphSAGE+, F1 ≈ 90–92%, IEEE TCAD 2023, open source), EEschematic's visual chain-of-thought LLM refinement (Edinburgh, Oct 2025, MIT), Schemato's fine-tuning recipe (Sony, MLCAD 2025), AMSNet 2.0's placement ground truth (2,686 circuits with component/net positions), and frontier LLMs as on-demand layout critics.
3. **A captive test suite with ground truth.** VibroSense's blocks ship hand-drawn xschem schematics (`bias_generator.png`, `ota_foldcasc.png`, …) next to their netlists — golden references for judging auto-layout quality, block by block.

And one structural advantage: SpiceVision sells to humans debugging foreign netlists. We are building for a **human + AI team designing new circuits** — which adds features SpiceVision doesn't have (operating-point overlay, provable netlist↔schematic equivalence, an agent API) and deletes features we don't need (SoC capacity, Eldo dialect, SAML-gated documentation).

---

## Part 1 — SpiceVision PRO feature teardown → SpiceGlass plan

Verbatim feature inventory from concept.de (live page + datasheet v2.19, fetched 2026-06-10), mapped to our plan:

| # | SpiceVision PRO feature (verbatim) | What it actually is | SpiceGlass |
|---|---|---|---|
| 1 | "Schematics from SPICE netlists … SPICE, HSPICE, Spectre, Calibre, CDL, Eldo, PSPICE" | Multi-dialect parser → circuit DB → placer → renderer | **M0.** ngspice dialect first; dialect plugins later (CDL second — it's near-SPICE and covers work use) |
| 2 | "Ultra fast SPICE-reader — SPICE to schematics on the fly (within seconds)" | Performance budget | **M0.** Budget: < 2 s for a 60-device block, < 10 s for ~2k devices hierarchical |
| 3 | "Simplification — merging components in parallel, such as transistors, or creating a non-parasitic view" | Display-level folding: N parallel fingers → one symbol ×N; hide parasitic R/C | **M1.** Our OTA's 20-finger PMOS is the test case. `m=`/identical-card detection + `--functional` view |
| 4 | "Automatic Logic Recognition — creates digital logic schematics from pure CMOS SPICE-level netlists" | Transistor→gate motif matching (inverter, NAND, TG, latch…) | **M5.** We have real targets: classifier's 128 TGs, SAR logic, PGA decoder (28 T) |
| 5 | "Cone display / Cone Window — an 'intelligent magnifying glass' … incremental schematic navigation … critical paths" | k-hop / path subgraph extraction around a seed net/device, rendered incrementally | **M2.** CLI first (`glass cone --net vbias --hops 2`), interactive in M4 |
| 6 | "Cookie-cutting — circuit fragments can be isolated and saved as SPICE netlists … for partial simulation, often running 10 to 100 times faster" | Fragment → standalone valid `.subckt` with boundary ports | **M2.** Direct synergy with our AI loop's testbench-per-block style |
| 7 | "Powerful GUI Cockpit — tree, schematic, cone and source file … drag-and-drop … search engine" | Multi-view UI with cross-probing | **M4.** Local web app (the machine has Node, no Qt/Tcl). Click net in source ↔ highlight in schematic |
| 8 | "64-bit database … today's largest SoCs and ASICs" | Capacity engineering | **Skip.** Bound: ~10k devices flat; beyond that, hierarchy + cones |
| 9 | "Tcl based UserWare API — custom design reports and ERC … 100+ examples … plugin mechanism" | Scriptable access to the circuit DB | **Surpass (M3/M5).** Python API from day one; **MCP server** so design agents can query connectivity, extract cones, run checks — UserWare for the agent era |
| 10 | "Cadence Interface / Netlist to Schematic — SKILL export into Virtuoso" (paid option) | Editable schematic in the designer's editor | **Analog equivalent (M3): xschem `.sch` export** (our ecosystem's editor, Sky130 symbols). SKILL export only if the day job ever needs it |
| 11 | "Post-Layout Debugging — SPEF/DSPF parasitic visualization, critical path extraction" (paid option) | RC network views + pruned export | **Defer (v2).** Pre-layout flow doesn't need it; revisit at tapeout |
| 12 | "Analog Waveform Viewer and Signal Tracing" (paid option) | Wave window + schematic cross-probe | **Replace.** Instead of a wave viewer: **operating-point overlay** (Part 3) — better fit for design-loop debugging |
| 13 | "design documentation" | Auto-reports | **Surpass (M3).** README-grade markdown: schematic + device table + pin table + recognized-structure narrative — automating what we currently hand-write per block |

**License/cost reality check:** SpiceVision is commercial (pricing unpublished, options sold separately, Linux/Windows). SpiceGlass is MIT from commit one.

---

## Part 2 — Research foundations (what we stand on)

Each subsystem builds on the strongest verified work found in the 2026-06-10 deep-research sweep (`research/netlist-to-schematic.md` has full citations):

| Subsystem | Foundation | What we take |
|---|---|---|
| Structure recognition | **Kunal et al., IEEE TCAD 42(9) 2023** (ALIGN, open source) | VF2 exact subgraph isomorphism against primitive templates (diff pair, simple/cascode mirror, …) — deterministic, no training. Their 21-template library is liftable. GNN tier (GraphSAGE+) only if/when we outgrow templates |
| Placement conventions | Classic analog drafting practice + ALIGN's symmetry constraints | Current-branch columns (every VDD→VSS source-drain stack is a column), PMOS top / NMOS bottom, signal flow left→right, mirror symmetric primitives, fold rails to stubs, label high-fanout nets |
| Generic layout fallback | **ELK layered (Sugiyama)** via elkjs — what netlistsvg uses | For glue/digital portions and as M0 fallback while the analog placer matures |
| LLM refinement | **EEschematic (arXiv:2510.17002, MIT)** — visual chain-of-thought: render → look → refine; few-shot on 6 analog substructures | Optional polish pass with a frontier model, strictly gated by our verifier |
| Fine-tuned conversion (later) | **Schemato (arXiv:2411.13899, MLCAD 2025)** — Llama-3.1-8B, 76% compile success | The recipe + the cautionary metric: "compiles" ≠ "correct" — which is why verification is core, not optional |
| Training data (later) | **AMSNet 2.0 (arXiv:2505.09155)** — 2,686 circuits *with positions*; **Masala-CHAI (arXiv:2411.14299)** — 7,500 pairs; harvested open xschem libs | Only if rule-based placement disappoints at scale |
| Correctness | Graph isomorphism (VF2 with device-type/size attributes) — LVS-lite | The round-trip verifier: schematic → re-extracted netlist ≡ input netlist, stamped on every output |

Patent note: netlist-to-schematic patents exist (e.g., US7917877 on transistor-level schematic generation; Concept Engineering's own 1990s-era work has expired). Re-implementing published algorithms (Sugiyama 1981, VF2) and product *functionality* in open source is standard practice; specific claims should be checked before any commercial use. Not legal advice.

---

## Part 3 — Where SpiceGlass beats SpiceVision (the AI-native features)

1. **Provable correctness.** Every emitted schematic carries a `VERIFIED ✓` / `MISMATCH ✗` stamp from graph-isomorphism re-extraction. SpiceVision doesn't advertise this; LLM converters can't offer it. For AI-generated circuits this is the difference between a picture and an instrument.
2. **Operating-point overlay.** We own the simulator (ngspice is on this machine; the AI loop already runs it). Parse `.op`/raw output → color devices by region (saturation / triode / subthreshold / off), annotate Vgs, Vds, Id, gm/Id on hover or print. The schematic becomes a bias-debug dashboard — directly attacking the #1 failure mode of AI-designed analog (mis-biased devices that "look" fine in the netlist).
3. **Agent API (MCP).** SpiceVision's Tcl UserWare, reimagined: expose the circuit database to design agents — `get_neighbors(net)`, `extract_cone(...)`, `cookie_cut(...)`, `check_erc(...)`, `render_fragment(...)`. The AI that wrote the netlist can finally *see and interrogate* its own circuit mid-design-loop.
4. **Comment-cluster hints.** Our AI netlists carry `** ===== Section =====` partitions (mirror / diff pair / startup …). The placer uses them as grouping constraints — information no general tool exploits because only LLM-written netlists have it.
5. **README-grade documentation.** `glass doc design.cir` emits the schematic SVG + device-sizing table + pin table + recognized-structures narrative in exactly the style of this repo's block READMEs — automating the most tedious hand-maintained artifact we produce today.
6. **Free, hackable, ours.**

---

## Part 4 — Architecture

Pure Python core (only `networkx` + stdlib; VF2 is `networkx.isomorphism`), SVG out, Node/elkjs optional, local web viewer later. Runs on this Windows box today.

```
spiceglass/
  program.md            # this file
  glass/
    parser.py           # ngspice subset: .subckt/.ends, X/M/R/C/L/V/I/D/Q cards,
                        #   + continuations, params (w= l= m=), .include/.lib refs,
                        #   comment-section capture. Dialect plugin interface (CDL next)
    db.py               # hierarchical circuit DB: Design ▸ Subckt ▸ Device/Net/Pin,
                        #   attributes, indices; JSON (de)serialization — the contract
                        #   between all other modules and the future viewer/MCP server
    classify.py         # PDK prefix maps (sky130 first): model → symbol + terminal
                        #   roles (D/G/S/B …); supply/ground/bias net detection
    recognize.py        # VF2 motif matching: diff pair, current mirrors, cascodes,
                        #   diode loads, TG, inverter/NAND (logic recognition, M5)
    simplify.py         # parallel/serial merge (×N badges), functional view
    place.py            # THE MOAT: branch-column analog placer
                        #   1. decompose into VDD→VSS current branches
                        #   2. branches → columns; x-order by signal-flow BFS
                        #   3. y-stack within column (PMOS top, NMOS bottom)
                        #   4. mirror recognized symmetric primitives
                        #   5. comment-cluster adjacency constraints
                        #   fallback: layered (Sugiyama) for unrecognized glue
    route.py            # orthogonal routing, rail stubs, net labels (fanout > 4)
    render_svg.py       # symbol library (IEEE-style MOS/R/C/D), wires, labels,
                        #   W/L annotations, verify stamp, cluster shading
    emit_xschem.py      # .sch writer with Sky130 symbol refs (M3)
    verify.py           # schematic → netlist re-extraction → attributed VF2
                        #   isomorphism vs input → report + stamp
    cone.py             # k-hop / path extraction; cookie-cut: fragment → valid
                        #   standalone .subckt with boundary ports (M2)
    annotate_op.py      # ngspice .op/raw parser → region coloring + bias labels (M3)
    doc.py              # markdown generator (M3)
    cli.py              # glass render | cone | cut | doc | verify | op
  viewer/               # M4: static HTML/JS, reads db.py JSON; tree + schematic +
                        #   cone + source panes, cross-probe, search
  tests/
    golden/             # vibrosense blocks as fixtures; hand-drawn PNGs as visual refs
```

**Design rules:**
- The circuit DB JSON is the stable interface — placer, renderer, viewer, MCP server, and any future learned model all speak it.
- Every transformation (merge, cone, cut) yields a netlist the verifier can check. **No silent drops:** every device and net is either drawn or listed in the report.
- Determinism: same input → same schematic (sorted iteration, no RNG). Diffs of generated SVGs are reviewable in git.

---

## Part 5 — Milestones

**M0 — First Light** *(the 20% that proves it)*
Parse → classify → rail folding → branch-column placement → routed SVG → verify stamp, CLI: `glass render vibrosense/00_bias/design.cir`.
**Accept:** 00_bias (17 devices, 7 branches) side-by-side comparable to hand-drawn `bias_generator.png`; isomorphism PASS; < 2 s; zero unplaced devices.

**M1 — Analog conventions**
Motif recognition (pair/mirror/cascode) + symmetry placement + parallel-merge (×20 OTA fingers → one symbol "×20") + net labels.
**Accept:** 01_ota (53 instances → ~13 symbols) readable; all 4 real vibrosense blocks render + verify; a cold reader can trace the folded-cascode signal path unaided.

**M2 — Fragments (the debug workflow)**
Cone extraction + cookie-cutting to standalone re-simulatable `.cir`.
**Accept:** extract the OTA out of a full-chain netlist; ngspice runs the fragment; cone of `vbias` at 2 hops shows exactly the mirror tree.

**M3 — Docs, OP overlay, xschem**
`glass doc` (README-grade markdown), `glass op` (region coloring from ngspice), xschem `.sch` export.
**Accept:** auto-regenerate 00_bias's README schematic+table section; a deliberately starved tail transistor shows red (off/subthreshold) in the overlay; exported `.sch` opens in xschem.

**M4 — Interactive viewer**
Local web app: hierarchy tree, schematic pane, cone-on-click, source↔schematic cross-probe, search.
**Accept:** load full-chain netlist (~2.3k devices) hierarchically; click any net in source → highlighted in schematic; cone expansion < 200 ms.

**M5 — Intelligence (research track)**
Logic recognition (TG/INV/NAND for classifier + SAR), LLM polish loop (EEschematic recipe, verification-gated), optional learned placer fine-tuned on AMSNet 2.0 + harvested xschem pairs, MCP server for design agents.
**Accept:** classifier's 128 TGs render as TG symbols; LLM-polished layouts never ship unverified; agent can answer "what loads node od1?" via MCP.

Order of value: M0–M1 remove the daily pain (READMEs, reviewing AI output). M2–M3 change the design loop (partial sims, bias debugging). M4–M5 make it a product.

---

## Part 6 — Risks and catches (found before they find us)

1. **Layout aesthetics is the whole game — and it's subjective.** SpiceVision, after ~25 years, still earns "generally mediocre" from practitioners. Mitigations: judge against our own hand-drawn ground truth per block; xschem export keeps a human-tidy escape hatch; LLM polish as taste pass; conventions encode the objective part of taste.
2. **Parser rabbit hole.** "Any SPICE" is a decade of edge cases. Mitigation: ngspice subset first, fail loudly on unsupported constructs (`.control`, B-sources → listed, not drawn), dialect plugins only on demand.
3. **Scale cliff.** Branch-column placement is O(small); the full chain (~2.3k devices + 645 cells) must stay hierarchical — never flatten. Cones are the answer to "show me everything."
4. **Verification gap:** isomorphism proves connectivity, not geometry — a verified schematic can still be ugly. That's why M0's acceptance is human side-by-side judgment, not just the stamp.
5. **Scope creep toward SpiceVision parity.** Waveforms, SPEF, Eldo, SoCs: explicitly deferred. The moat is analog readability + AI-loop integration, not feature count.

---

## Part 7 — Success metrics

- **Quality:** all real vibrosense blocks readable without manual edits (designer judgment vs hand-drawn refs).
- **Correctness:** 100% isomorphism PASS on every rendered block; zero silent drops, ever.
- **Speed:** `.cir` → README-ready SVG < 2 s (block), < 10 s (chip, hierarchical).
- **Adoption test:** the next vibrosense/pvdd block README ships an auto-generated schematic instead of a hand-drawn one.

## Next action

`M0` — implement `parser.py → db.py → classify.py → place.py (columns+rails) → render_svg.py → verify.py` against `vibrosense/00_bias/design.cir`, with the hand-drawn schematic as the visual reference.

## Sources

Feature inventory: https://www.concept.de/SpiceVision.html and datasheet v2.19 (https://www.concept.de/datasheet_spicevisionpro.pdf), fetched 2026-06-10. Research foundations: see `research/netlist-to-schematic.md` (verified landscape, full citations).
