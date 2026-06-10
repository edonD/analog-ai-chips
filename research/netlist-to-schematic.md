# Netlist → Schematic: Visualizing AI-Generated SPICE Circuits

**Research date:** 2026-06-10
**Question:** AI flows (VibroSense, PVDD) generate ngspice `.cir` netlists. Nothing turns them back into readable schematics. What exists, what's the catch, and what should we adopt / build / train?
**Method:** Deep-research harness — 104 agents, 22 sources fetched, 110 claims extracted, 25 verified by 3-vote adversarial verification (25 confirmed, 0 refuted), plus targeted follow-up fetches for the dataset/2025-26 gaps.

---

## TL;DR

1. **No maintained open-source tool converts SPICE netlists to readable analog schematics.** The open-source field is two abandoned/caretaker projects and a digital-only renderer.
2. **One mature commercial tool exists:** SpiceVision PRO (Concept Engineering / Altair). It does exactly this, in seconds, from any SPICE dialect — and can export editable schematics into Cadence Virtuoso (paid add-on). User-reported aesthetics: "generally mediocre."
3. **Research woke up to this exact pain in 2024–2025.** Sony AI's **Schemato** (MLCAD 2025) fine-tuned Llama-3.1-8B for netlist→schematic — its stated motivation is verbatim our problem ("ML-generated netlists lack human interpretability"). Edinburgh's **EEschematic** (Oct 2025, MIT-licensed, active) is a multimodal-LLM agent doing SPICE→editable schematic with visual chain-of-thought refinement.
4. **The catch everywhere:** LLM converters fail to compile ~25% of the time and *never guarantee the schematic matches the netlist*. Generic graph layout (ELK/dot) produces analog spaghetti. Readability — rails folded, PMOS up / NMOS down, differential symmetry — is the hard 20% that nobody open-source has built.
5. **Recommendation: build a small deterministic converter** (~1–2k lines Python → SVG + xschem `.sch`) exploiting three properties of *our* AI-generated netlists that make the general problem easy here: small blocks (15–55 devices), PDK-primitive-only instances, and LLM section comments that pre-cluster the circuit. Add a **round-trip verification** (re-extract netlist from drawn schematic, graph-isomorphism check vs. input) so every schematic is provably correct — the one feature no LLM approach can offer.

---

## Why this is hard (and why it stayed unsolved)

Schematic capture is a one-way street by design: drawing → netlist loses *positions*; going back requires re-inventing them. A netlist is a hypergraph (devices = nodes, nets = hyperedges); any graph-layout engine can place it. What it can't do is make it *read like a schematic*, because analog readability is a set of unwritten conventions:

- **Power rails are not wires.** VDD on top, VSS/GND on bottom, drawn as stubs/labels per device. Routing them as ordinary nets is the #1 cause of spaghetti.
- **Current branches are columns.** Every VDD→VSS source-drain stack is drawn vertically: PMOS up top, cascodes mid, NMOS at bottom. Horizontal position = signal flow, left (inputs/bias) to right (outputs).
- **Symmetry is meaning.** Differential pairs mirror about an axis; current-mirror gates align horizontally. Breaking symmetry hides the topology even when connectivity is right.
- **High-fanout bias nets become labels,** not drawn wires.

Generic Sugiyama/layered layout (graphviz `dot`, ELK) knows none of this. Commercial EDA solved it decades ago and charges for it; open-source never needed it because the *forward* direction (draw, then netlist) was the only workflow — until LLMs started writing netlists directly. That is why the gap is real, newly painful, and newly studied.

---

## Verified landscape

### Commercial — the only turn-key answer

**SpiceVision PRO** (Concept Engineering GmbH, acquired by Altair 2022; current release "SpiceVision PRO 2025") — verified 3-0 on all claims:

- "Takes any SPICE netlist, SPICE model and extracted parasitic netlist and generates clean, easy-to-read transistor-level schematics" — "on the fly (within seconds)". Input dialects: SPICE, HSPICE, Spectre, Calibre, CDL, Eldo, PSPICE (Altair docs add spice2/spice3/ltspice), plus DSPF/SPEF/RSPF parasitics. ngspice is not named explicitly — generic spice3 should cover our netlists, but `.control` blocks / B-sources are unverified.
- Analog-readability feature that survived verification: automatic display-level **merge of parallel/serial devices** (e.g., the 20 parallel PMOS fingers in our OTA fold would collapse to one symbol). No verified claim about rail folding or differential-pair symmetry.
- **Virtuoso Schematic Export** (separately licensed, SKILL-based, mature since 2005): netlist → editable Virtuoso schematic. comp.cad.cadence users: "works great," symbols auto-inserted from analogLib, aesthetics "generally mediocre."
- Pricing unverified; eval licenses exist per vendor site.

**Nlview** (same vendor) — the schematic-rendering engine OEM'd into many EDA tools — is **digital-first**: transistor-level rendering is a paid T-engine add-on, and Nlview does **not** parse SPICE itself (front-ends like SpiceVision do). Embedding Nlview alone solves neither parsing nor analog layout.

*Unverified this round (verification-pipeline gap, not absence of capability):* Cadence Virtuoso's native CDL import, Synopsys Custom Compiler generation. Both reportedly exist in some form; at a Cadence site the practical route is SpiceVision's exporter or asking CAD support.

### Open source — effectively dead for analog

| Tool | What it is | Status (verified 2026-06-10) |
|---|---|---|
| **asg** (aidangoettsch/asg, MIT, PyPI) | The only SPICE→xschem generator found. Built for qflow *digital* output; also emits KiCad EESchema. Layout = column placement + greedy constraints (left-to-right by distance-to-inputs, untangle-by-mirroring) — not Sugiyama. | Abandoned: 20 commits, Jun–Oct 2020, 0 PRs. Open issue: "Support for analog components in schematic output." WOSET 2020 slides list analog as future work. |
| **f18m/netlist-viewer** (MIT, C++/wxWidgets) | Standalone GUI: "loading SPICE netlists and convert them in a schematic (i.e. graphical) format." | Caretaker mode — author hasn't used it since ~2010, seeking maintainers; v0.4 binaries Mar 2025, last push Apr 2026. Analog layout quality unestablished. |
| **netlistsvg** (nturley/netlistsvg, MIT) | SVG schematics via elkjs (layered/Sugiyama, "similar to dot"). Ships an **analog symbol skin** (`lib/analog.svg`: resistors, BJTs, vcc/gnd) and a worked analog example. | **Cannot read SPICE at all** — input is Yosys JSON only (closed issue #58: "How to generate from an NGSPICE netlist?" — no path). Stale since Dec 2020. Usable as a *renderer* if we write the SPICE→JSON front-end, but placement stays digital-generic. |

*Unverified by the harness:* xschem itself (no netlist-import/auto-placement exists to my knowledge — the flow is strictly schematic→netlist), Qucs-S SPICE import (imports for *simulation*, not placed schematics), lcapy (draws from netlists but needs manual position hints per component), schemdraw/SKiDL (programmatic drawing, manual placement), tscircuit, Falstad CircuitJS. None of these is known to auto-place a SPICE netlist.

### LLM-based converters — the 2024–2026 wave

**Schemato** — *"Schemato: An LLM for Netlist-to-Schematic Conversion"*, arXiv:2411.13899 (v1 Nov 2024, v2 Jun 2025), published MLCAD 2025. 8 of 10 authors Sony-affiliated (Sony AI Switzerland, Sony Semiconductor Solutions; EPFL/TUM co-affiliations). Verified 3-0:

- Motivation is verbatim our pain: ML models "typically generate netlists that lack human interpretability… it is crucial to translate ML-generated netlists into interpretable schematics quickly and accurately."
- Fine-tuned **Llama-3.1-8B**; **76% compilation success** vs 63% for the best general baseline (GPT-4o); graph-edit-distance and structural-similarity scores 1.8×/4.3× higher than best baseline LLMs.
- **I/O doesn't fit our flow** (verified 2-1): input is LTspice-derived `.net`, output is exclusively **LTspice `.asc`** — not xschem, not SVG. The v1 CircuiTikZ output task was dropped in v2. Weights/code public availability not established.
- Honest read: proof that fine-tuning works + a recipe, not a tool. A quarter of outputs don't compile, and "compiles" ≠ "matches the input netlist."

**EEschematic** — *"EEschematic: Multimodal-LLM Based AI Agent for Schematic Generation of Analog Circuit"*, arXiv:2510.17002 (Oct 2025), Chang Liu & Danial Chitnis, University of Edinburgh. GitHub `eelab-dev/EEschematic`, **MIT, active** (release Oct 2025, 28 stars):

- SPICE netlist → "schematic diagrams in a human-editable JSON-like format"; few-shot with six analog substructure examples; **Visual Chain-of-Thought** — the MLLM iteratively *looks at* the rendered schematic and refines placement/wiring for clarity and symmetry.
- Demonstrated on CMOS inverter, 5T-OTA, telescopic cascode — exactly our block class.
- This is the closest existing open project to our need, and independent validation of the "agentic render-and-refine" approach. Unknowns: robustness on Sky130 `X`-prefixed PDK instances, behavior at 50+ devices.

**CircuitLM** — arXiv:2601.04505 (Jan 2026, accepted LAD'26): natural-language → CircuitJSON schematics with force-directed visualization, component knowledge base to fight hallucination. Adjacent (NL input, breadboard-level, force-directed ≠ analog conventions) but confirms the space is accelerating.

### Structure recognition — the missing analog ingredient, already solved

**Kunal et al., "GNN-based Hierarchical Annotation for Analog Circuits," IEEE TCAD 42(9), Sept 2023** (UMN + TAMU + Intel Labs; the ALIGN project, DARPA IDEA). Verified 3-0:

- Input deliberately SPICE ("the most natural and universal mode in which an analog designer… may use the software"); output is a hierarchy: elements → primitives (**differential pairs, current mirrors** — found by exact VF2 subgraph isomorphism against 21 templates) → sub-blocks (**OTA, LNA, mixer, oscillator** — GraphSAGE+ node classification, F1 ≈ 90–92%).
- Auto-derives **symmetry / matching / common-centroid constraints**. The paper feeds them to layout generation, not schematic drawing — but this is precisely the recognition layer a readable schematic generator needs, and ALIGN is open source (`ALIGN-analoglayout/ALIGN-public`).

### Datasets — the train-a-model leg (follow-up fetches, not adversarially verified)

| Dataset | Contents | Notes |
|---|---|---|
| **AMSNet** (arXiv:2405.09045, UCLA/Ningbo/Tsinghua et al.) | Transistor-level schematics + SPICE netlists | Initial set public |
| **AMSNet 2.0** (arXiv:2505.09155, LAD25) | **2,686 circuits**: schematic images + Spectre netlists + OpenAccess digital schematics + **component/net positions** | Positions = placement ground truth — the key asset for training a placer |
| **Masala-CHAI** (arXiv:2411.14299, NYU Karri group) | **7,500** textbook schematics with GPT-4-extracted SPICE netlists | Open-sourced, CC-BY 4.0 badge |
| Open xschem libraries (Sky130 etc.) | Every `.sch` + extracted netlist is a free (netlist → placed schematic-as-text) pair | Schematic-as-text makes LLM fine-tuning natural |

---

## The catch (per repo rule)

1. **"Compiles" is not "correct."** Schemato's headline is 76% *compilation* success — i.e., a quarter of outputs are broken files, and nothing reported guarantees the other 75% are *the same circuit* as the input. For design work, a beautiful wrong schematic is worse than no schematic. Any converter we adopt must prove netlist ≡ schematic.
2. **The only tool that "just works" is commercial,** and even its aesthetics draw a "generally mediocre" from practitioners — after ~25 years of engineering. Calibrate expectations: auto-generated schematics aid *reading*, they don't replace a designer's drawing.
3. **Open-source attempts died precisely at the analog step** (asg's open issue; netlistsvg's digital-only placement). The parsing and drawing are easy; the conventions are the moat.
4. **LLM placement quality degrades with size.** EEschematic demos top out around telescopic-cascode scale (~10–15 devices); our blocks reach 50+ (OTA: 53 instances) and the full chain ~2,300. Hierarchy (one schematic per `.subckt`, symbols for sub-blocks) is mandatory, not optional.

---

## Recommendation: adopt / build / train

**Adopt (day job, Cadence environment):** Ask CAD support about a SpiceVision PRO eval — for reading legacy/extracted HVCM netlists it is the industrial answer, and the Virtuoso SKILL export turns netlists into editable schematics.

**Build (this repo's flow — the main recommendation):** A deterministic `cir2sch` converter. Our AI-generated netlists are a *much easier* problem than general SPICE:

- Blocks are 15–55 devices, one `.subckt` per file — human-schematic scale.
- Every device is an `X` instance of a known PDK primitive (`sky130_fd_pr__nfet_01v8`, `__pfet_01v8`, `__res_xhigh_po`, `__cap_mim_m3_1`, …) — classification is a prefix table, no model-card ambiguity.
- The LLM writes `** ===== Section =====` comments that already partition the netlist into functional clusters (mirror / diff pair / OTA / startup) — free grouping hints unique to AI-generated netlists; no published tool exploits them.

Pipeline (pure Python + SVG, no external deps required on this machine — ngspice/Python/Node present, no xschem/graphviz):

1. **Parse** ngspice subset: `.subckt`/`.ends`, `X`/`M`/`R`/`C`/`V`/`I`/`D` cards, `+` continuations, `w= l=` params; comment-section capture.
2. **Classify** devices via PDK prefix map → symbol + terminal roles (D/G/S/B; res p/n/body; cap p/n/body).
3. **Recognize structure** (ALIGN-style VF2 motif matching, trivial at this scale): diff pairs (shared source, gates ≠), current mirrors (shared gate, one diode-connected), cascode stacks, diode loads, startup/leaker one-offs.
4. **Fold rails:** nets named/at VDD/VSS/GND (plus any net tied to a supply source) become per-device stubs. Bias nets with fanout > 4 become labels.
5. **Place by convention:** decompose into VDD→VSS current branches (source-drain chains); each branch = a column (PMOS top, NMOS bottom, cascodes stacked); order columns by signal flow (BFS from input pins, bias left, outputs right); mirror recognized pairs about a local axis; keep comment-section clusters adjacent.
6. **Route** orthogonally (gate taps enter from the side; short elbows; labels for anything ugly).
7. **Emit** SVG (browser viewing, drop into block READMEs) and optionally xschem `.sch` (text format, Sky130 symbol libs) for hand-tidying — replacing today's manual redraw step.
8. **Verify (the differentiator):** re-extract a netlist from the placed schematic and check graph isomorphism against the input (canonical labeling with device type/W/L as node attributes, terminal roles on edges). Stamp **VERIFIED ✓ / MISMATCH ✗** onto the SVG. This converts "pretty picture" into "proof."

Effort estimate: v0.1 (parse → classify → rails → columns → SVG + verify) ≈ 1–2k lines; the bias generator (17 devices, 7 branches) is the natural first target, with `bias_generator.png` (hand-drawn xschem) as ground truth for comparison.

**Hybrid (cheap accelerant):** Try **EEschematic** as-is (MIT) on `00_bias/design.cir`; and/or use a Claude agentic loop (generate placement JSON → render with our SVG backend → look → refine), which is EEschematic's method with a stronger model. Always gate any LLM-placed schematic with step 8's isomorphism check — that combination (LLM aesthetics + deterministic proof) doesn't exist anywhere yet.

**Train (later, only if rule-based placement disappoints at scale):** AMSNet 2.0's position data + Masala-CHAI + harvested xschem `.sch`/netlist pairs make a Schemato-style fine-tune targeting xschem-`.sch`-as-text feasible. This is a research project (months), and the deterministic tool both reduces its necessity and would generate its training data.

---

## Open questions

- SpiceVision PRO pricing / eval terms; behavior on ngspice-specific constructs (`.control`, B-sources).
- EEschematic robustness on Sky130 `X`-instance netlists and >30-device blocks.
- Schemato weights/code: never located publicly.
- Whether Qucs-S / xschem grew any import capability recently (unverified by the harness; believed absent).

## Sources

Verified by 3-vote adversarial verification unless noted:

- SpiceVision PRO: https://www.concept.de/SpiceVision.html · https://www.concept.de/datasheet_spicevisionpro.pdf · https://help.altair.com/silicon_debug_tools/spice/manual.html · Virtuoso export: https://help.altair.com/2026/silicon_debug_tools/spice/tutorial/skillexport.html
- Nlview / T-engine: https://www.concept.de/nlview.html · https://www.concept.de/tengine.html
- asg: https://github.com/aidangoettsch/asg · https://pypi.org/project/asg/ · WOSET'20: https://woset-workshop.github.io/PDFs/2020/a13.pdf
- netlist-viewer: https://github.com/f18m/netlist-viewer
- netlistsvg: https://github.com/nturley/netlistsvg (issue #58)
- Schemato: https://arxiv.org/abs/2411.13899 · https://doi.org/10.1109/MLCAD65511.2025.11189059
- EEschematic: https://arxiv.org/abs/2510.17002 · https://github.com/eelab-dev/EEschematic *(follow-up fetch)*
- ALIGN GNN annotation: http://people.ece.umn.edu/~sachin/jnl/tcad23kk.pdf · https://doi.org/10.1109/TCAD.2023.3236269 · https://github.com/ALIGN-analoglayout/ALIGN-public
- Datasets *(follow-up fetches)*: AMSNet https://arxiv.org/abs/2405.09045 · AMSNet 2.0 https://arxiv.org/abs/2505.09155 · Masala-CHAI https://arxiv.org/abs/2411.14299
- CircuitLM *(follow-up fetch)*: https://arxiv.org/abs/2601.04505

**Verification stats:** 5 search angles, 22 sources fetched, 110 claims extracted, top 25 adversarially verified: 25 confirmed (24 unanimous 3-0, 1 split 2-1), 0 refuted. Coverage caveat: Virtuoso/Custom Compiler native import, xschem/Qucs-S import status, and the dataset details rest on follow-up single-fetches or practitioner knowledge, not the adversarial pipeline.
