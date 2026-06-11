# Learned Rules — the interpreter's curriculum

**The list.** Every rule the golden plans have taught (or still need to
teach) the automatic .cir → schematic interpreter. Regenerate the live
gap anytime with:

```
python -m glass diff-plan <golden.plan>
```

Goldens live next to their netlists:
`vibrosense/00_bias/design.bias_generator.plan`,
`vibrosense/00_bias/bias_distribution/design_full.bias_generator_full.plan`,
`vibrosense/04_envelope/design.envelope_det.plan`,
`vibrosense/05_rms_crest/design.{ota5,rms_squarer,lpf_rc,peak_detector,rms_crest_top}.plan`.

---

## A. Implemented (2026-06-11, commit 07523a8)

| # | Rule | Taught by | Where |
|---|------|-----------|-------|
| R1 | A section that is just one lone capacitor merges into the **preceding** region (comp caps belong with the block they compensate). | bias_generator: `XC_comp` → OTA region | `place.py` cap-merge pass |
| R2 | A mirror-bank candidate whose drain feeds an unclaimed **resistor** chain leaves the bank for its divider column. Caps explicitly do **not** count — first version included them and silently dissolved the OTA load mirror (caught by `test_plan`). | bias_generator_full: `XMvbp_sink`/`XMbcp_sink` under their dividers; false bank `XM1+sinks` gone | `recognize.py` `_drain_feeds_rc` |
| R3 | A lateral (R90) device slots **immediately after the column of its same-section channel partner**, not at the sheet's end. | rms_squarer: `Riso_s` beside its branch — auto now reproduces the golden interleave exactly | `place.py` key_override |
| R4 | Section titles with no word characters are rejected; section-less objects sort at their **natural netlist position**, not last. | bias_generator_full: junk `"="` region; leading mirror bank | `parser.py` + `place.py` `sec_idx` |

## B. Backlog (the residual gap, by evidence)

Structural devices-differing per sheet (renames excluded):
**envelope 0 · bias 4 · peak 5 · squarer 6 · bias_full 13**

| # | Rule to encode | Evidence (from diff-plan) |
|---|----------------|---------------------------|
| B1 | **Merge protection one-offs into the adjacent startup region** (or generally: 1-device regions whose device shares a net with a neighbor region merge into it). | bias & bias_full: `XM6` leaker → "Startup & protection"; accounts for the whole bias gap (4) |
| B2 | **Narrative order: a core comes before the mirror bank it drives** (bias-first reading: core → mirror → regulation). | bias & bias_full FLOW ORDER lines |
| B3 | **A diode-connected cascode-bias FET belongs with its mirror bank**, not wherever its netlist position fell. | bias_full: `XMbcn` → "PMOS mirror + cascode bias" |
| B4 | **Sibling generator regions merge** when they form one bias chain (vbp + vbcp generation = one region), and the chain's series resistor (`XRbcp`) stays lateral between the sink columns rather than stacking into one. | bias_full: vbp/vbcp REGION + COLUMN + ORIENT lines |
| B5 | **Sheets without section comments get synthesized regions** — at minimum one region per symmetric branch pair (signal/reference) or per recognized functional cluster. | squarer (6) and peak_detector (5) gaps are purely "golden named regions where auto had none" |
| B6 | Port-flag stubs should not overlap subckt-box edges (renderer polish, from rms_crest_top review). | visual note, not in diff |

## C. How the loop runs

1. Design (or fix) a sheet in the live plan editor → save → it's a golden.
2. `glass diff-plan golden.plan` → categorized semantic gap.
3. Encode recurring lines as interpreter rules (section A grows, B shrinks).
4. `python -m unittest discover -s tests` guards against regressions —
   the auto-plan identity test and the goldens keep old lessons learned.
