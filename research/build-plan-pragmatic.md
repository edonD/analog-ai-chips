# Pragmatic Analog CIM Chip Build Plan

**Goal:** Design and tape out a real analog compute-in-memory chip using open-source PDKs and tools. Not a paper exercise — real silicon.

---

## Architecture Decision: Capacitor-Based SRAM CIM on SKY130

### Why This Topology

After 23 research files covering every analog CIM approach, **charge-domain CIM using SRAM + MIM capacitors** is the best architecture to build first:

| Factor | Capacitor/SRAM CIM | RRAM CIM | Flash CIM | Digital CIM |
|--------|-------------------|----------|-----------|-------------|
| Available in sky130? | Yes (MIM caps + 6T SRAM) | Yes (sky130_fd_pr_reram) but yield uncertain | No (SONOS not in open PDK) | Yes but defeats purpose |
| Precision | 6-8 effective bits | 3-4 bits (variability) | 5-6 bits | 8+ bits |
| Drift | None | Some | Some | None |
| Temperature stability | Excellent (geometry-based) | Poor | Moderate | Excellent |
| Reproducibility | High | Low (stochastic filaments) | N/A | High |
| Design complexity | Moderate | High (forming, programming) | N/A | Low |
| Novelty | High (no open-source exists) | Medium | N/A | Low |

**The EnCharge-inspired capacitor CIM approach uses Q=CV physics:**
- Weights stored in SRAM cells that gate switches to MIM capacitors
- Input applied as voltage; multiplication via Q=CV
- Accumulation via charge sharing on a common wire
- Output is already a voltage — feed directly to SAR ADC

This is the architecture our research identified as #1 recommended (see `design-tradeoffs-synthesis.md`).

---

## The Chip: "AnalogML-1"

### Specifications

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Process | SkyWater SKY130 (130nm) | Open PDK, tapeout available |
| CIM Array | 32x32 (1,024 weights) | Fits in chipIgnite area, large enough to run a real tiny model |
| Weight precision | 4-bit (16 levels) | Realistic for first silicon; maps to 4 SRAM cells per weight |
| Input precision | 4-bit (16 voltage levels) | DAC generates 16 voltage steps |
| Output precision | 8-bit (SAR ADC) | Use JKU's open-source 12-bit SAR ADC, truncate to 8 |
| MAC operation | Charge-domain (Q=CV) | MIM caps (2 fF/um²), voltage-mode input |
| Activation | Digital ReLU | Simple comparator + pass gate |
| Digital control | RISC-V or FSM on Caravel | Caravel harness provides management SoC |
| Clock | 10-50 MHz | Conservative for first silicon |
| Supply | 1.8V core, 3.3V I/O | Standard sky130 |
| Target area | <2 mm² (CIM core) | Fits in 10 mm² chipIgnite die with ADCs + digital |
| Target TOPS/W | >1 TOPS/W | Modest goal; prove the concept works |

### What It Can Run

A 32x32 array with 4-bit weights can run:
- **MNIST digit classification** (784→32→10 = 2 layers, tiled across time)
- **Keyword spotting** (small feature vector → classification)
- **Anomaly detection** (sensor data → threshold)

These are toy models, but they prove the analog MAC works on real silicon.

---

## Circuit Architecture (Block Diagram)

```
                    ┌──────────────────────────────┐
                    │        DIGITAL CONTROL        │
                    │    (FSM / Caravel RISC-V)     │
                    └──────────┬───────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
         ┌────▼────┐    ┌─────▼─────┐    ┌─────▼─────┐
         │  4-bit  │    │  32x32    │    │   8-bit   │
         │  DAC    │    │  SRAM     │    │  SAR ADC  │
         │  Array  │    │  Weight   │    │  (per col │
         │ (32 ch) │    │  Storage  │    │  or muxed)│
         └────┬────┘    └─────┬─────┘    └─────▲─────┘
              │               │                │
              │          ┌────▼────┐           │
              └─────────►│ CIM MAC │───────────┘
                         │  Array  │
                         │ 32x32   │
                         │ MIM Cap │
                         └─────────┘

CIM MAC Array Detail (one cell):
    ┌─────────────────────────────────┐
    │                                 │
    │  SRAM cell ──► Switch ──► MIM Cap ──► Column bitline
    │  (weight)      (NMOS)     (2fF/um²)   (charge accumulation)
    │                  ▲
    │                  │
    │            Input voltage
    │            (from DAC)
    │                                 │
    └─────────────────────────────────┘

    V_in × C_weight = Q (charge on bitline)
    Sum of Q across rows = MAC result
    SAR ADC converts accumulated voltage to digital
```

---

## Circuit-Level Design Details

### 1. CIM Cell (The Core)

Each cell implements one multiply:

```
         WL (row select)
            │
        ┌───┴───┐
        │ 6T    │
        │ SRAM  │──── stores 4 bits (4 cells per weight)
        │ cell  │     or 1-bit per cell with binary encoding
        └───┬───┘
            │ weight bit
            │
        ┌───┴───┐
   Vin ─┤ NMOS  ├─── to column bitline (charge accumulation)
        │switch │
        └───┬───┘
            │
         ┌──┴──┐
         │ MIM │ C = sized proportional to weight bit significance
         │ Cap │ (C, 2C, 4C, 8C for 4-bit weight)
         └──┬──┘
            │
           GND
```

**How it works:**
1. SRAM stores weight bit (0 or 1)
2. If weight=1, NMOS switch connects MIM cap to column bitline
3. Input voltage V_in drives the top plate
4. Charge transferred: Q = C_weight × V_in (multiplication!)
5. All rows share the column bitline — charges add (accumulation!)
6. Bitline voltage = (1/C_total) × Σ(C_i × V_in_i) = MAC result

**For 4-bit weights:** Use binary-weighted capacitors (C, 2C, 4C, 8C) per weight, each gated by one SRAM bit. Total weight = sum of connected capacitors.

**Sky130 MIM cap sizing:**
- Unit cap C = 10 fF (≈ 5 um² at 2 fF/um²)
- 8C = 80 fF (≈ 40 um²)
- Total per 4-bit weight: C+2C+4C+8C = 15C = 150 fF (≈ 75 um²)
- 32x32 array: 32 × 32 × 150 fF = 153.6 pF total cap area ≈ 76,800 um² ≈ 0.077 mm²

### 2. Input DAC (4-bit, 32 channels)

Simple resistor-string DAC per row:
- P+ poly resistor string (300 ohm/sq)
- 16 taps for 4-bit resolution
- Decoder selects tap via NMOS switches
- Output range: 0 to 1.8V in 16 steps (112.5 mV/step)
- 32 independent DACs, one per row

**Alternative:** Single DAC + sample-and-hold per row (saves area, slower)

### 3. Output ADC (8-bit SAR)

Use the **JKU 12-bit SAR ADC** (Apache 2.0, designed for sky130):
- 12-bit, 1.44 MS/s, 703 uW at 1.8V
- Area: 0.175 mm²
- Truncate to 8-bit output (or use full 12 bits for characterization)
- Need one per column or multiplex across columns

**For 32 columns:**
- Option A: 32 ADCs (5.6 mm² — too much area)
- Option B: 4 ADCs + 8:1 column mux (0.7 mm² — practical)
- Option C: 1 ADC + 32:1 column mux (0.175 mm² — cheapest, slowest)

**Recommendation:** Option B (4 ADCs) balances throughput and area.

### 4. Digital Control

Use the Caravel harness management SoC (RISC-V) for:
- Programming SRAM weights via Wishbone bus
- Sequencing DAC inputs
- Reading ADC outputs
- Implementing activation functions (ReLU = max(0, x))
- Multi-layer inference by feeding outputs back as inputs

### 5. Sense Amplifier / Column Precharge

Before each MAC:
1. Precharge all column bitlines to V_ref (0.9V)
2. Apply input voltages to rows
3. Charge redistribution shifts bitline voltage
4. Sense amplifier detects voltage change
5. SAR ADC converts result

**Key design challenge:** Parasitic capacitance on bitlines dilutes the signal. Need careful extraction and simulation.

---

## Tool Flow

### Setup (5 minutes)

```bash
# Install Docker, then:
docker pull hpretl/iic-osic-tools:latest
docker run -it -p 8888:8888 -v $(pwd):/foss/designs hpretl/iic-osic-tools:latest

# Inside container, all tools available:
# xschem, ngspice, magic, klayout, netgen, openroad, yosys, etc.
```

### Design Flow

```
Step 1: Schematic Design (Xschem)
   └─► Draw CIM cell, DAC, sense amp, digital control
   └─► Generate SPICE netlist

Step 2: SPICE Simulation (ngspice)
   └─► Single cell characterization (V_in vs Q_out)
   └─► 8x8 array simulation (verify MAC accuracy)
   └─► Monte Carlo (mismatch, process variation)
   └─► Temperature sweep (-40C to 125C)
   └─► Corner analysis (TT, SS, FF, SF, FS)

Step 3: Layout (Magic + KLayout)
   └─► CIM cell layout (manual, for matching)
   └─► Array placement (regular grid)
   └─► ADC layout (from JKU IP)
   └─► Digital control (OpenLane auto-P&R)
   └─► Top-level integration

Step 4: Verification
   └─► DRC (Magic built-in)
   └─► LVS (Netgen)
   └─► PEX (Magic parasitic extraction)
   └─► Post-layout simulation (ngspice with parasitics)

Step 5: Tapeout
   └─► GDS generation
   └─► Submit to ChipFoundry chipIgnite or Tiny Tapeout
```

---

## Cost and Timeline

### Option A: Tiny Tapeout Proof-of-Concept (Fastest, Cheapest)

| Item | Cost | Timeline |
|------|------|----------|
| Tiny Tapeout TTSKY26a (2 analog tiles) | ~$400 | Submit by mid-2026 |
| Analog pins (4-6) | ~$300 | |
| Test equipment (oscilloscope, SMU) | Existing or ~$2K used | |
| **Total** | **~$700-2,700** | **Chips by Dec 2026** |

What fits: 8x8 CIM array + 1 ADC. Enough to prove Q=CV MAC works.

### Option B: chipIgnite Full Design (Recommended)

| Item | Cost | Timeline |
|------|------|----------|
| chipIgnite shuttle | $14,950 | ~5 months |
| Test board / evaluation | ~$500 | |
| Test equipment | Existing or ~$5K | |
| **Total** | **~$15,500-20,000** | **Chips ~5 months after submit** |

What fits: 32x32 CIM array + 4 SAR ADCs + digital control + test structures. Full proof-of-concept.

### Option C: wafer.space GF180 (Cheapest Full Design)

| Item | Cost | Timeline |
|------|------|----------|
| wafer.space 1000 chips | $7,000 | TBD (shuttles running) |
| **Total** | **~$7,500-12,000** | |

Advantage: 1000 chips for testing. Disadvantage: 180nm, no MIM caps in open PDK (use MOS caps or MoM).

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| MIM cap matching limits precision | Include test structures to measure cap matching; design for 4-bit initially |
| Parasitic bitline capacitance kills signal | Pre-layout extraction; keep bitlines short; add gain stage before ADC |
| PMOS model issues (known sky130 problem) | Use NMOS-heavy design; avoid PMOS in signal path where possible |
| SRAM write disturb during CIM operation | Separate read/compute phases; add isolation switches |
| ADC bottleneck | Start with muxed single ADC; upgrade to parallel if area allows |
| First tapeout doesn't work | Include extensive test points, bypass modes, and standalone ADC test |

---

## What Makes This Novel

1. **First open-source analog CIM chip** — no one has done this on sky130
2. **Capacitor-based CIM** on an open PDK — validates the EnCharge physics with freely available tools
3. **Fully reproducible** — anyone can rebuild it from the open-source design files
4. **Real tapeout path** — chipIgnite or Tiny Tapeout, not just simulation
5. **Published comparison** — measure actual TOPS/W and compare to our 23 research files' predictions

---

## Design Phases

### Phase 1: Single Cell Characterization (1-2 weeks)
- Design one CIM cell in Xschem
- Simulate in ngspice: linearity, noise, mismatch (Monte Carlo)
- Establish precision floor for sky130 MIM caps
- **Deliverable:** Cell-level performance numbers

### Phase 2: Small Array (2-3 weeks)
- 8x8 CIM array + simple resistor-string DAC + comparator
- Simulate full MAC operation
- Run MNIST inference in simulation (software golden model → analog)
- **Deliverable:** Array-level accuracy and power estimates

### Phase 3: Full Design (4-6 weeks)
- 32x32 array + 4 SAR ADCs + digital FSM + Caravel integration
- Layout, DRC, LVS, PEX, post-layout sim
- **Deliverable:** GDS ready for tapeout

### Phase 4: Tapeout + Test (3-6 months)
- Submit to chipIgnite or Tiny Tapeout
- Design test PCB
- Measure real silicon: MAC accuracy, TOPS/W, temperature sweep
- **Deliverable:** Silicon-verified analog CIM chip

---

## Key Files and Tools

| What | Where |
|------|-------|
| PDK | `google/skywater-pdk` (GitHub) |
| MIM cap models | `sky130_fd_pr` library |
| RRAM option | `sky130_fd_pr_reram` (backup approach) |
| SRAM cells | OpenRAM `sky130_sram_macros` |
| 12-bit SAR ADC | `iic-jku/SKY130_SAR-ADC1` (GitHub) |
| EDA Docker | `hpretl/iic-osic-tools` (Docker Hub) |
| Caravel harness | `efabless/caravel_user_project` (GitHub) |
| Analog template | `TinyTapeout/ttsky-analog-template` (GitHub) |
| Tapeout | chipfoundry.io ($14,950) or tinytapeout.com (~$700) |

---

## References

- EnCharge AI architecture: `research/encharge-ai.md`
- ADC/DAC design tradeoffs: `research/adc-dac-bottleneck.md`
- Precision limits: `research/precision-noise-challenges.md`
- Design tradeoffs: `research/design-tradeoffs-synthesis.md`
- JKU SAR ADC paper: Austrochip 2023
- SkyWater PDK docs: skywater-pdk.readthedocs.io
- ChipFoundry chipIgnite: chipfoundry.io
