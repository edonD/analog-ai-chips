# SpiceGlass Improvement Loop

A hard-gated process for the editor improvements (xschem-parity gaps).
**One improvement at a time. No improvement is "done" — and the next one
does not start — until every gate below is green with pasted, reproducible
evidence.** Manual "looks fine" is not evidence.

Priority order (do not reorder without sign-off):
**1. Hierarchy navigation → 2. Net highlighting → 3. OP/bias back-annotation → 4. Search/find.**

---

## The loop (per improvement)

```
1. BUILD the smallest version that could pass all gates.
2. SELF-VERIFY: run every gate. Paste the command + its output as evidence.
3. ADVERSARIAL PASS: actively try to break it (edge cases below). Log what
   you tried and the result. A gate with no attempted break is not passed.
4. GATE: if ANY gate is red, fix and return to step 2. No partial credit,
   no "TODO later", no skipping a gate as "not applicable" without writing
   one sentence of justification.
5. COMMIT only when 100% green. The commit body must contain the evidence
   block (below).
6. STOP. Report the evidence and wait for explicit sign-off before the
   next improvement. Do not start the next one preemptively.
```

**Toughness rules**
- Every functional claim needs an **automated check against ground truth**
  (the round-trip verifier `verify.py` is the oracle), not a screenshot.
- **No silent drops.** Every device/net/block is either handled correctly
  or explicitly listed as unhandled. A feature that works on 95% and
  silently mis-handles 5% is RED.
- **No regressions, ever** (global invariants below run after every change).
- Reproducible: every number comes from a committed command + a fixed seed.

---

## Global invariants — must ALL stay green after EVERY improvement

Run these before every commit. Any red = the improvement is not done.

| # | Gate | Command | Pass condition |
|---|------|---------|----------------|
| G1 | Engine regression | `python tools/regress.py --core-only` | prints `CORE clean.`, exit 0 |
| G2 | Golden unit tests | `python -m unittest discover -s tests` | `OK`, exit 0 |
| G3 | Realistic benchmark | `python tools/gen_realistic.py --count 7500 --out benchmark/real --seed 21 && python tools/benchmark.py --dir benchmark/real --optimize` | `VERIFIED 100.0%`, 0 crashes, 0 invalid |
| G4 | Hierarchical benchmark | `python tools/gen_hier.py --count 2500 --out benchmark/hier --seed 3` + all-subckt verify | every TOP + every leaf verifies, 0 crashes |
| G5 | Server boots & serves | `python -m glass edit examples/hier_full_afe.cir --no-browser` → curl `/` and `/api/asc` | both HTTP 200 |
| G6 | No secret/work-doc leak | `git status` review | no TDK PDF/PPTX, no `pepties/`, no bulk corpora committed |
| G7 | Reproducible | re-run G3/G4 from seed | byte-identical netlists, identical pass counts |

---

## Improvement 1 — Hierarchy navigation (push/pop)

**Goal:** double-click a block instance opens that subckt's sheet; a
breadcrumb shows the path; `Esc`/back returns to the parent at the prior
view; works to arbitrary depth.

Gates (all required):
- [ ] **N1 — Open correctness.** Double-clicking any block box opens the
      child sheet, and that sheet is **byte-identical** to converting that
      subckt directly. Automated: for all 25 hierarchical systems,
      enumerate every `sub` instance, open it, assert the served `.asc`
      equals `convert_to_asc` of that subckt. **100% match.**
- [ ] **N2 — Every block is reachable.** For all 25 systems, every block
      instance is openable and its child **round-trip VERIFIES**. Count of
      unopenable or non-verifying blocks = **0**.
- [ ] **N3 — No false blocks.** Primitive devices (mos/res/cap/…) are NOT
      treated as openable blocks. Automated: asserting double-click on a
      leaf primitive does nothing. 0 false positives over all leaf examples.
- [ ] **N4 — Up/back integrity.** Down-then-up returns to the exact parent
      sheet with pan/zoom restored; unsaved parent edits are preserved (or
      an explicit warning is shown — silent loss is RED).
- [ ] **N5 — Depth.** Works to depth ≥ 3 (build a 3-level test netlist:
      system → sub-system → leaf). Breadcrumb shows full path.
- [ ] **N6 — Adversarial.** Recursive/cyclic subckt reference → no infinite
      loop, clear message. Missing child definition → clear message, no
      crash. Block with 0 devices → handled.
- [ ] **N7 — Perf.** Opening a child (≤16-device block) renders in < 500 ms
      measured; no full-page reload (single-page transition).
- [ ] **N8 — Test committed.** A headless test (`tools/` or `tests/`)
      encodes N1–N3 and runs in CI/regress; reproducible command pasted.
- [ ] **N9 — Global invariants G1–G7 green.**

---

## Improvement 2 — Net highlighting

**Goal:** click a wire/pin/label and the entire electrical net lights up
(every segment + every pin), nothing from other nets.

Gates (all required):
- [ ] **H1 — Exactness vs oracle.** The highlighted set must equal the
      net's membership as computed by `verify.py`'s connectivity extraction
      — **exact set equality** (no extra, no missing). Automated over
      ≥ 200 nets sampled across all examples: **100% exact**, including
      multi-segment nets, corner junctions, and T-junctions.
- [ ] **H2 — Rails & labels.** Highlighting a rail (vdd/gnd) or a labelled
      net lights up *all* of its stubs/labels across the sheet. The
      gnd-class (`0`) net is handled.
- [ ] **H3 — Isolation.** Zero geometry from any other net is highlighted
      (false-positive pixels = 0). Verified on the densest example
      (gilbert_cell / full_afe).
- [ ] **H4 — Interaction safety.** Highlight does not break select/drag/
      wire/place modes; a clear/toggle exists; ESC clears.
- [ ] **H5 — Perf.** Highlighting a 100+-segment net completes in < 50 ms;
      no visible jank; works at all zoom levels.
- [ ] **H6 — Adversarial.** Click on empty space → nothing highlights.
      Click on a junction shared by ≤1 net → correct net only. Overlapping
      collinear wires of different nets → only the clicked net.
- [ ] **H7 — Test committed** encoding H1 (set-equality vs `verify.py`).
- [ ] **H8 — Global invariants G1–G7 green.**

---

## Improvement 3 — Operating-point / bias back-annotation

**Goal:** run ngspice `.op`, overlay DC node voltages on nets and color
each MOS by operating region (off / subthreshold / triode / saturation).
This is the "intelligent magnifying glass."

Gates (all required):
- [ ] **O1 — Value correctness.** Every annotated node voltage matches the
      ngspice raw output within **1 mV** (or 0.1%). Automated diff against
      the raw file. Mismatches = 0.
- [ ] **O2 — No silent omission.** Every net in the netlist is either
      annotated with a value or **listed** as un-annotated with a reason.
      Coverage report printed; unexplained omissions = 0.
- [ ] **O3 — Region correctness.** MOS region classification matches a
      hand-checked truth table on a known circuit (5T OTA with a
      deliberately starved tail): the starved device shows **off/
      subthreshold (red)**; saturated devices show saturation. 100% match
      on the truth table.
- [ ] **O4 — Graceful failure.** ngspice missing / sim diverges / no `.op`
      → clear message, **schematic still renders**, no crash, exit handled.
- [ ] **O5 — Determinism.** Same netlist → identical annotation across runs.
- [ ] **O6 — Coverage.** Runs end-to-end on ≥ 10 representative leaf
      circuits and ≥ 3 hierarchical tops; report pass/fail per circuit.
- [ ] **O7 — Test committed** (O1 value-diff + O3 region truth table).
- [ ] **O8 — Global invariants G1–G7 green.**

---

## Improvement 4 — Search / find (net or instance)

Gates (all required):
- [ ] **S1 — Find correctness.** Searching a net/instance name selects and
      centers **every** matching element; count matches the netlist's
      occurrence count exactly. 0 misses, 0 false hits, over ≥ 100 queries.
- [ ] **S2 — Negative case.** A non-existent name yields a clear "no match",
      no crash, no spurious selection.
- [ ] **S3 — Scale.** Works on the largest example with no perceptible lag
      (< 100 ms to first result).
- [ ] **S4 — Test committed**; **S5 — Global invariants G1–G7 green.**

---

## Evidence block (paste into each commit body)

```
IMPROVEMENT: <name>
GATES: <n>/<n> green
  G1 CORE clean ........ <pasted line>
  G2 tests OK .......... <pasted line>
  G3 realistic 100% .... VERIFIED <n>/<n>
  G4 hier verifies ..... TOP <n>/<n>, subckts <n>/<n>
  G5 server ............ GET / 200, /api/asc 200
  <feature gates> ...... <command + result per gate>
ADVERSARIAL: <what was attempted to break it, and the outcome>
```

---

## Scoreboard

| Improvement | Status | Gates green | Evidence commit |
|-------------|--------|-------------|-----------------|
| 1. Hierarchy navigation | ⬜ not started | 0/9 | — |
| 2. Net highlighting | ⬜ not started | 0/8 | — |
| 3. OP back-annotation | ⬜ not started | 0/8 | — |
| 4. Search / find | ⬜ not started | 0/5 | — |

Legend: ⬜ not started · 🟡 in progress · ✅ done (all gates green, signed off).
