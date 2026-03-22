# Process Node Comparison for Analog AI Chip Design

*Research date: 2026-03-22. Written from the perspective of an analog IC process engineer evaluating fabrication options for VibroSense-1 commercialization beyond the sky130 prototype.*

---

## Executive Summary

VibroSense-1 is prototyped on SkyWater SKY130 (130nm) for cost and accessibility reasons. But 130nm is not where this chip should ship in volume. The production migration path depends on balancing power reduction, NRE cost, foundry access, and time-to-market.

**Recommendation: GF 22FDX (22nm FD-SOI) for production.**

Rationale: FD-SOI body biasing delivers 2-4x power reduction over bulk 130nm without redesigning the analog core from scratch. BrainChip taped out AKD1500 on 22FDX for ~$2.3M. Aspinity moved AML200 to 22nm. The node is purpose-built for low-power analog/mixed-signal IoT. VibroSense-1's target market (always-on industrial sensors) is exactly what 22FDX was designed for.

**Fallback: TSMC 65nm or UMC 55nm BCD** if 22FDX access proves difficult for a startup with limited volume commitments.

---

## 1. What Process Nodes Do Commercial Analog AI Chips Actually Use?

| Company | Chip | Process Node | Foundry | Year | Why This Node |
|---------|------|-------------|---------|------|---------------|
| Aspinity | AML100 | Not disclosed (~130-180nm est.) | Unknown | 2024 | First silicon, low risk |
| Aspinity | AML200 | 22nm | Unknown | 2025 | 10x capacity increase, TOPS-level perf at <100uW |
| POLYN | NASP VAD | 40-90nm | Unknown | 2025 | Process-agnostic design, asynchronous analog |
| Mythic | M1076 | 40nm | TSMC | 2021 | Mature embedded NOR flash available at 40nm |
| EnCharge | EN100 | 16nm | TSMC | 2025 | Proven SRAM libraries, capacitor CIM density |
| BrainChip | AKD1000 | 28nm | TSMC | 2022 | Cost, simplicity for first neuromorphic SoC |
| BrainChip | AKD1500 | 22nm FD-SOI | GlobalFoundries | 2026 | Ultra-low power, body biasing for edge AI |
| IBM | HERMES | 14nm | IBM/Samsung | 2023 | PCM backend integration proven at 14nm |
| Axelera | Metis | 12nm | Unknown | 2024 | Digital IMC, benefits from density |
| Syntiant | NDP120 | 40nm | Unknown | 2023 | Mature node, digital accelerator |
| Innatera | T1 SNN | 28nm (est.) | Unknown | 2025 | Mixed analog-digital neuromorphic |

**Pattern:** Pure analog chips (Aspinity, POLYN) cluster at 22-90nm. Mixed-signal CIM chips (Mythic, EnCharge) use 16-40nm. Digital-heavy chips (Axelera) push to 12nm. Nobody doing analog AI inference uses nodes below 12nm. The physics advantage of analog is greatest at mature nodes.

---

## 2. Open Source PDK Comparison: sky130 vs GF180 vs IHP SG13G2

### Head-to-Head

| Feature | SkyWater SKY130 | GF180MCU | IHP SG13G2 |
|---------|----------------|----------|------------|
| **Node** | 130nm CMOS | 180nm CMOS | 130nm SiGe BiCMOS |
| **Supply voltage** | 1.8V core, 3.3V I/O | 3.3V / 5V / 6V | 1.2V (thin ox), 3.3V (thick ox) |
| **Metal layers** | 5 + 1 local interconnect | 3-5 (variants A-D) | 5 thin + 2 thick + MIM |
| **MIM capacitors** | Yes (2 fF/um^2) | Yes | Yes |
| **High-res poly resistors** | Yes (300, 2000 ohm/sq) | Yes | Yes |
| **Bipolar devices** | No | No | **Yes (SiGe:C HBT, fT=350 GHz)** |
| **SRAM** | 6T available | 6T available | 6T available |
| **Fabrication access** | Efabless chipIgnite (paused Q1 2025) | Wafer.space (~$200/slot, quarterly 2026) | Tiny Tapeout IHP shuttle; Europractice MPW |
| **Tapeout cost (prototype)** | ~$10K (chipIgnite shuttle) | ~$200-7K (wafer.space) | ~EUR 5-15K (Europractice MPW) |
| **Production wafer cost** | High (boutique fab, US) | Low (GF Singapore, cost-optimized) | Medium (IHP Germany) |
| **PDK maturity** | Most mature, largest community | Growing, fewer analog designs | Newest open PDK, rapidly developing |
| **Analog model quality** | Known PMOS subthreshold issues | Less community validation | SiGe models well-characterized for RF |
| **Community ecosystem** | Largest (hundreds of tapeouts) | Growing (wafer.space driving) | Smallest but active |
| **Best for** | Digital/mixed-signal prototyping | Cost-sensitive prototyping, 5V analog | RF, mmWave, high-speed analog |
| **License** | Apache 2.0 | Apache 2.0 | Apache 2.0 |

### Pros and Cons for Analog AI

**SKY130 (current VibroSense-1 target):**
- Pros: Largest ecosystem, most tapeout experience, MIM caps for charge-domain CIM, 1.8V supply reasonable for low power.
- Cons: PMOS subthreshold models broken (confirmed in program.md), 130nm means larger devices for same gm, higher power than scaled nodes, SkyWater is a small US fab with higher production costs, chipIgnite shuttle currently paused.
- Verdict: Good for prototype validation. Not viable for volume production.

**GF180MCU:**
- Pros: Cheapest fabrication path (~$200 per slot on wafer.space), GF Singapore fab means lowest production wafer cost of the three, 5V/6V options useful for direct MEMS interface, 1000 parts per slot for initial production runs.
- Cons: 180nm is a step backward from 130nm in density and speed, higher power consumption than sky130 at equivalent functionality, fewer analog designs validated, 3.3V minimum supply is higher power.
- Verdict: Cheapest path to silicon but wrong direction for low-power analog AI. Only use if budget is the sole constraint.

**IHP SG13G2:**
- Pros: SiGe BiCMOS with 350 GHz HBTs is exceptional for RF and high-speed analog, dual gate oxide (1.2V/3.3V) gives low-power digital with high-voltage analog I/O, thick metal layers (2-3 um) reduce interconnect resistance, 130nm CMOS comparable to sky130 for digital.
- Cons: Open-source PDK explicitly "not intended for production at this moment," smallest community, IHP is a research fab (higher cost than commercial foundries), overkill for VibroSense-1 (no RF needed).
- Verdict: Best open PDK for RF analog. Overkill for VibroSense-1. Would be ideal for a chip that needs to process wireless signals before analog ML.

### Recommendation for Prototype Phase

**Use sky130 for the initial prototype** (design is already targeting it). If chipIgnite remains paused, fall back to **GF180MCU via wafer.space** for a rapid proof-of-concept, accepting the power penalty. IHP SG13G2 only if RF integration is added to the VibroSense roadmap.

---

## 3. What Would VibroSense-1 Gain by Moving to Smaller Nodes?

### Power Scaling Analysis

VibroSense-1 power budget on sky130 (130nm): **300 uW typical, 600 uW hard limit** (from program.md).

| Parameter | 130nm (sky130) | 65nm (TSMC/UMC) | 40nm (TSMC) | 28nm (TSMC/Samsung) | 22nm FD-SOI (GF) |
|-----------|---------------|-----------------|-------------|--------------------|--------------------|
| **Vdd (core)** | 1.8V | 1.2V | 1.1V | 0.9V | 0.8V (with body bias) |
| **Dynamic power scaling** | 1x (baseline) | ~0.44x | ~0.37x | ~0.25x | ~0.20x |
| **Leakage** | Low | Moderate | Higher | Higher (bulk) | **Very low (FD-SOI)** |
| **gm/Id efficiency** | Good | Good | Good | Reduced (short-channel) | **Excellent (steep SS)** |
| **Analog area** | 1x | ~0.6x | ~0.5x | ~0.4x | ~0.5x |
| **Capacitor density** | 2 fF/um^2 (MIM) | 3-5 fF/um^2 (MOM) | 5-8 fF/um^2 | 8-12 fF/um^2 | 5-8 fF/um^2 |
| **Transistor matching (Avt)** | Best | Good | Moderate | Worse (RDF) | **Good (no RDF in thin body)** |

**Key insight:** Dynamic power scales roughly as CV^2f. Reducing Vdd from 1.8V to 0.8V alone gives a 5x power reduction. But analog circuits care about signal swing, noise, and matching -- not just switching power. The real gains are:

### At 65nm (TSMC CLN65LP / UMC 55nm)

- **Power reduction: ~2x** (Vdd drops to 1.2V, but analog circuits need headroom, so effective Vdd for signal chain is ~1.0V vs ~1.5V at 130nm).
- **Benefit:** Enough to hit the 100-150 uW range that POLYN claims for its VibroSense chip. Competitive with Aspinity AML100.
- **Cost:** Moderate NRE ($500K-1M for MPW, $2-5M for full mask set). Accessible via Europractice or Muse/GSME shuttles.
- **Design effort:** Moderate. Analog topologies port well from 130nm to 65nm. Main work is resizing for lower Vdd headroom and updated device models.
- **Risk:** Low. 65nm is extremely mature, abundant foundry capacity, well-understood for analog.

### At 40nm (TSMC CLN40LP)

- **Power reduction: ~2.5-3x** over 130nm.
- **Benefit:** Potentially sub-100 uW. Matches or beats POLYN's claimed specs.
- **Cost:** Higher NRE ($1-3M for MPW + iterations). Mythic chose 40nm for M1076 -- it's proven for analog AI.
- **Design effort:** Moderate-high. 40nm has thinner gate oxide, lower headroom. Cascode stacking becomes tighter. Analog designers start fighting for voltage headroom.
- **Risk:** Low-moderate. 40nm is mature but fewer analog-specific IP blocks available through shuttles compared to 65nm.

### At 28nm (TSMC CLN28HPC / Samsung 28nm)

- **Power reduction: ~3-4x** over 130nm.
- **Benefit:** Sub-100 uW achievable. Best digital integration (larger on-chip FSM/MCU possible). BrainChip AKD1000 proved complex neuromorphic SoC works at 28nm.
- **Cost:** Significant NRE ($2-5M full mask set, ~$70-130K for MPW shuttle slot). Wafer cost ~$1,500-3,000.
- **Design effort:** High. Analog design at 28nm bulk requires careful attention to short-channel effects, increased random dopant fluctuation (RDF), reduced intrinsic gain (gm*ro drops). PMOS in particular suffers from degraded analog performance.
- **Risk:** Moderate. The analog portion of the chip does not inherently benefit from 28nm scaling. You are paying for digital density you may not need. 28nm bulk CMOS is the wrong node for a primarily analog chip.

### At 22nm FD-SOI (GF 22FDX)

- **Power reduction: 3-5x** over 130nm (with body biasing).
- **Benefit:** This is the sweet spot. FD-SOI eliminates the RDF problem of bulk 28nm. Body biasing gives a free knob to tune Vth post-fabrication -- invaluable for analog process compensation. Subthreshold slope is steeper (better gm/Id). Leakage is dramatically lower than bulk at any node.
- **Cost:** NRE ~$2-3M (BrainChip's AKD1500 tapeout was ~$2.3M). Mask set ~$1-2M.
- **Design effort:** Moderate. FD-SOI is actually *easier* for analog than bulk 28nm because device behavior is more ideal (fewer short-channel effects, no pocket implant variability). Body biasing can compensate for process corners -- replacing the 4-bit tuning DAC in the VibroSense filter bank.
- **Risk:** Low-moderate. GF 22FDX is in volume production, Aspinity and BrainChip have validated it for analog AI. Main risk is GF's smaller foundry ecosystem vs TSMC.

---

## 4. FD-SOI: Why It Is Ideal for Low-Power Analog

### The Physics Advantage

FD-SOI (Fully Depleted Silicon-on-Insulator) places the transistor channel on a thin (~7nm) silicon film on top of a buried oxide (BOX). This architecture gives four critical advantages for analog:

**1. No Random Dopant Fluctuation (RDF)**
In bulk CMOS below 40nm, random placement of dopant atoms causes threshold voltage (Vth) mismatch between adjacent transistors. This is the dominant source of analog mismatch at advanced nodes. In FD-SOI, the channel is undoped -- Vth is set by the gate workfunction, not dopants. Result: **better matching at 22nm FD-SOI than at 65nm bulk**.

**2. Steeper Subthreshold Slope**
FD-SOI achieves subthreshold slopes of 65-70 mV/decade vs 80-90 mV/decade for bulk CMOS. This means:
- Transistors turn off more completely (lower leakage).
- Higher gm/Id at the same bias current (more transconductance per microamp).
- More efficient analog circuits at ultra-low current.

This directly addresses the VibroSense-1 problem: on sky130, we cannot trust PMOS in weak inversion. On 22FDX, subthreshold operation is well-modeled and reliable for both NMOS and PMOS.

**3. Back-Gate (Body) Biasing**
FD-SOI allows forward body bias (FBB) of up to +2V and reverse body bias (RBB) of -2V through the substrate beneath the BOX. This shifts Vth by ~100-150 mV, enabling:
- **Post-fabrication tuning:** Compensate for process variation without redesign.
- **Dynamic power management:** Lower Vth (higher speed, higher leakage) when active; raise Vth (lower leakage) when sleeping.
- **Analog frequency tuning:** Replace or supplement the programmable bias current DAC in Gm-C filters. Apply body bias to OTA transistors to tune gm directly.

GF's Adaptive Body Biasing (ABB) delivers **up to 60% lower power at same frequency or 30% higher performance at same power**.

**4. Lower Parasitic Capacitance**
The BOX layer eliminates source/drain-to-substrate junction capacitance. Less parasitic C means:
- Faster circuits at the same power.
- Lower power at the same speed.
- Better noise performance (less capacitive loading on high-impedance nodes).

### FD-SOI for VibroSense-1 Specifically

| VibroSense-1 Block | Benefit from FD-SOI |
|--------------------|---------------------|
| Bias generator | Body bias replaces or supplements resistor-based PTAT reference. Better Vth matching improves current mirror accuracy. |
| OTA | Can safely use PMOS in subthreshold (models are reliable). gm/Id efficiency improvement means lower bias current for same gain. Estimated 2-3x power reduction per OTA. |
| Gm-C filters | Body bias provides a free frequency tuning knob. Could replace 4-bit tuning DAC. Less process variation means less tuning range needed. |
| Envelope detectors | Lower leakage means hold capacitors hold charge longer. Better precision at small signals. |
| Charge-domain MAC | Better capacitor matching (no junction capacitance interfering). Cleaner charge transfer. |
| Digital control | SRAM leakage down to 0.35 pA/cell (22FDX+ with source bias). Digital block can be nearly free in power. |

### Available FD-SOI Nodes

| Node | Foundry | Status | Key Features |
|------|---------|--------|-------------- |
| **22FDX** | GlobalFoundries | Volume production | Body biasing, ULL SRAM, eNVM (RRAM), automotive qualified |
| **22FDX+** | GlobalFoundries | Volume production (2025) | Enhanced ULL SRAM (0.35 pA/cell), embedded RRAM for NVM weights |
| **28FDS** | Samsung | Production | FD-SOI, body biasing, less ecosystem than GF |
| **18FDS** | Samsung | Production | Next-gen FD-SOI, higher density |
| **28nm FD-SOI** | STMicroelectronics | Internal (not open foundry) | Used in ST's own products |

---

## 5. NRE and Fabrication Costs by Node

### Full Mask Set Tapeout (Production Intent)

| Node | Mask Set Cost | Design NRE (labor + tools) | Total First Tapeout | Wafer Cost (production) | Min Viable Volume |
|------|-------------|--------------------------|--------------------|-----------------------|-------------------|
| **180nm (GF180)** | $100-300K | $200-500K | **$300K-800K** | $800-1,200/wafer | 100 wafers/year |
| **130nm (sky130)** | $200-500K | $300-800K | **$500K-1.3M** | $1,000-1,500/wafer | 100 wafers/year |
| **65nm (TSMC/UMC)** | $500K-1M | $500K-2M | **$1-3M** | $1,500-2,500/wafer | 200 wafers/year |
| **40nm (TSMC)** | $1-2M | $1-3M | **$2-5M** | $2,000-3,000/wafer | 500 wafers/year |
| **28nm bulk (TSMC/Samsung)** | $1-2M | $2-5M | **$3-7M** | $1,500-3,000/wafer | 500 wafers/year |
| **22nm FD-SOI (GF)** | $1-2M | $1-3M | **$2-4M** | $2,000-3,500/wafer | 200 wafers/year |
| **16/14nm (TSMC/Samsung)** | $3-5M | $5-15M | **$10-30M** | $4,000-6,000/wafer | 1,000 wafers/year |
| **7nm (TSMC)** | $10-20M | $20-50M | **$50-100M** | $10,000-16,000/wafer | 5,000 wafers/year |
| **5/3nm (TSMC)** | $20-40M | $50-200M | **$100-400M** | $16,000-20,000+/wafer | 10,000+ wafers/year |

### Prototype/Shuttle Costs (MPW)

| Node | Shuttle Option | Cost per Slot | Parts Received | Turnaround |
|------|---------------|--------------|----------------|-----------|
| **180nm (GF180)** | Wafer.space | ~$200-7,000 | 100-1,000 | ~6 months |
| **130nm (sky130)** | Efabless chipIgnite (paused) | ~$10,000 | 100-300 | ~6-9 months |
| **130nm (IHP SG13G2)** | Tiny Tapeout / Europractice | ~EUR 5-15K | 20-50 | ~6-9 months |
| **65nm (TSMC)** | Europractice / Muse-GSME | ~$45-70K | 20-40 | ~4-6 months |
| **40nm (TSMC)** | Europractice / Muse-GSME | ~$60-100K | 20-40 | ~4-6 months |
| **28nm (TSMC/Samsung)** | Europractice / Muse-GSME | ~$70-130K | 20-40 | ~4-6 months |
| **22nm FD-SOI (GF)** | GF MPW / CMC Microsystems | ~$50-100K (est.) | 20-40 | ~4-6 months |

### Cost Perspective for VibroSense-1

At VibroSense-1's target ASP of $5-15 and initial volumes of 10K-100K units:

| Node | Die size (est.) | Dies/wafer (300mm) | Cost/die (at 10K wafers/yr) | Cost/die (at 100 wafers/yr) | Viable? |
|------|----------------|-------------------|-----------------------------|-----------------------------|---------|
| 130nm | ~9 mm^2 | ~6,500 | $0.20 | $0.50 | Yes (if production fab available) |
| 65nm | ~4 mm^2 | ~14,000 | $0.15 | $0.40 | Yes |
| 28nm | ~2.5 mm^2 | ~22,000 | $0.10 | $0.35 | Yes (but NRE is high) |
| 22nm FD-SOI | ~3 mm^2 | ~18,000 | $0.15 | $0.40 | Yes |

At low volumes (100 wafers/year), die cost is dominated by NRE amortization, not wafer cost. The $2-4M NRE for 22FDX spread over 100K units = $20-40/die in NRE alone -- which exceeds the ASP target. **You need 500K+ cumulative units to amortize 22FDX NRE at the $5-15 ASP.**

This means the prototype-to-production path must be staged:
1. Prototype on sky130/GF180 ($10-50K)
2. Validate with customers using prototype silicon
3. Commit to production node only with $2-5M in committed purchase orders or funding

---

## 6. Foundry Access for Startups

### Tier 1: Open Source / Ultra-Low Cost (Prototype Only)

| Foundry | Process | Access Method | Min Cost | Best For |
|---------|---------|--------------|----------|----------|
| SkyWater | 130nm | Efabless chipIgnite (paused) | ~$10K | Digital/mixed-signal prototypes |
| GlobalFoundries | 180nm | Wafer.space | ~$200 | Cheapest possible silicon |
| IHP | 130nm SiGe BiCMOS | Tiny Tapeout / Europractice | ~$5-15K | RF/analog prototypes |

**Status (March 2026):** Sky130 chipIgnite shuttles are paused while exploring options. Wafer.space GF180 is delivering first run (March 2026), with quarterly runs planned for 2026. IHP shuttles available through Tiny Tapeout.

### Tier 2: Academic/Research Shuttles (Prototype + Small Volume)

| Broker | Foundries Available | Typical Nodes | Access Requirements |
|--------|--------------------|--------------|--------------------|
| **Europractice** | TSMC, GF, IHP, X-FAB, UMC, ON Semi | 180nm to 28nm | European academic/research (some industry) |
| **CMC Microsystems** | TSMC, GF 22FDX, X-FAB | 180nm to 22nm | Canadian academic/industry |
| **MOSIS** (now part of Europractice ecosystem) | Various | 180nm to 65nm | US academic |
| **Muse Semi / GSME** | TSMC | 180nm to 28nm | Commercial (startup-friendly) |

### Tier 3: Commercial Foundry Direct (Production)

| Foundry | Analog-Relevant Nodes | Startup-Friendly? | Min Volume | Notes |
|---------|----------------------|-------------------|------------|-------|
| **TSMC** | 180nm, 65nm, 40nm, 28nm, 16nm | Moderate (through brokers) | ~1,000 wafers/year for direct | Industry standard. Best IP ecosystem. Access through Muse/GSME for small volume. |
| **GlobalFoundries** | 180nm, 130nm, 65nm, 40nm, 22FDX | **Yes** (MPW program) | ~200 wafers/year | Best for FD-SOI. Strong MPW program. BrainChip validates startup access. |
| **Samsung** | 28FDS, 14nm, 8nm | Moderate | ~500 wafers/year | FD-SOI option. Less accessible than GF for startups. |
| **UMC** | 180nm, 110nm, 65nm, 55nm, 40nm, 28nm | **Yes** | ~200 wafers/year | Cost-competitive. New 55nm BCD (Oct 2025) excellent for mixed-signal. |
| **Tower Semiconductor** | 1um to 65nm (BCD, RF SOI, SiGe) | **Yes** (specialty analog focus) | ~100 wafers/year | Best pure-play analog foundry. MEMS+CMOS integration. Expanding 300mm 65nm BCD at Intel Fab 11X. |
| **X-FAB** | 1um to 110nm (CMOS, SOI, BCD) | **Yes** (analog specialty) | ~50 wafers/year | Monolithic MEMS+CMOS integration at 180nm. Best for sensor chips. Six fabs. |

### Best Path for VibroSense-1 Startup

**Phase 1 (Now, $10-50K):** Prototype on sky130 (if chipIgnite resumes) or GF180 (wafer.space). Validate analog chain functionality.

**Phase 2 ($50-100K):** If 65nm chosen for production, do an MPW shuttle at TSMC 65nm via Muse/GSME or Europractice. If 22FDX chosen, apply for GF MPW program or CMC Microsystems access.

**Phase 3 ($2-4M):** Full mask tapeout on production node. Requires Series A funding or strategic customer commitment.

---

## 7. The Production Migration Path

### sky130 Prototype to Production: Recommended Path

```
sky130 (130nm) prototype          GF 22FDX (22nm FD-SOI) production
    $10-50K                              $2-4M NRE
    6-9 months                           12-18 months
    300 uW power                         60-100 uW power
    Functional validation                Volume production
         │                                      │
         │    ┌──────────────────────┐          │
         └───►│  Intermediate step:  │──────────┘
              │  65nm MPW shuttle    │
              │  ($50-70K)           │
              │  Validate analog     │
              │  scaling assumptions │
              └──────────────────────┘
```

### Migration Considerations

**What changes between 130nm and 22nm FD-SOI:**

| Aspect | 130nm sky130 | 22nm FD-SOI | Redesign Effort |
|--------|-------------|-------------|-----------------|
| Supply voltage | 1.8V | 0.8V (with body bias) | Full voltage domain redesign |
| OTA topology | Folded cascode | Folded cascode (same) | Resize all transistors, rebias |
| Gm-C filters | Bias current tuning DAC | Body bias tuning (simpler!) | Simplified tuning circuit |
| Capacitors | MIM (2 fF/um^2) | MOM/MIM (5-8 fF/um^2) | Smaller caps, recalculate C values |
| Digital control | Standard cells | SRAM + logic (much smaller) | Port and resynthesize |
| PMOS subthreshold | Broken models, avoid | Well-characterized, usable | Can redesign for lower power |
| ESD | 3.3V I/O pads | 1.8V/3.3V I/O options | Redesign pad ring |
| Total redesign | -- | -- | **~6-9 months for experienced team** |

**What stays the same:**
- System architecture (filter bank + envelope + MAC classifier)
- Algorithm (charge-domain CIM, same weight precision)
- Digital control (SPI registers, FSM)
- Testbench methodology

### Alternative Production Paths

**Path A: Stay at 130nm (Tower or X-FAB)**
- Pros: Minimal redesign, fastest time to market, lowest NRE ($500K-1M).
- Cons: 300 uW power is 3-10x worse than competitors (POLYN claims 100 uW, Aspinity claims 36 uW). Not competitive.
- When: Only if you cannot raise >$2M for production tapeout.

**Path B: Move to 65nm (TSMC via Muse/GSME or Tower 65nm BCD)**
- Pros: Moderate redesign, 2x power reduction to ~150 uW, mature ecosystem, Tower expanding 65nm BCD at Intel Fab 11X.
- Cons: Still not matching FD-SOI power efficiency. Bulk CMOS at 65nm has no body biasing advantage.
- When: If GF 22FDX access is difficult or if you need integrated BCD (high-voltage MEMS drive + analog + digital on one die).

**Path C: Move to 22nm FD-SOI (GF 22FDX) -- RECOMMENDED**
- Pros: 3-5x power reduction to 60-100 uW, body biasing simplifies calibration, BrainChip validated path at ~$2.3M NRE, competitive with Aspinity/POLYN.
- Cons: Requires $2-4M NRE, 12-18 month redesign, smaller foundry ecosystem than TSMC.
- When: With Series A funding ($5-10M) and validated customer demand.

**Path D: Move to 28nm bulk (TSMC or Samsung)**
- Pros: Lowest die cost at high volume, best digital integration.
- Cons: Analog performance worse than 22FDX due to RDF. Higher NRE than 22FDX. No body biasing.
- When: Only if chip evolves to have significant digital content (on-chip MCU, BLE, etc.).

---

## 8. MEMS + CMOS Integration Options

VibroSense-1 connects to an external MEMS accelerometer. Future versions may integrate the MEMS sensor on the same die or package.

### Three Approaches

**A. Separate Chips (Current VibroSense-1 Approach)**
```
[MEMS Accel] ──analog wire──> [VibroSense-1 ASIC] ──SPI──> [MCU]
  (e.g. ADXL356)               (sky130 / 22FDX)           (nRF52)
```
- Pros: Best performance per component. Each optimized on its own process. Simplest design. Fastest to market.
- Cons: Board area for multiple chips. Parasitic capacitance on analog interconnect. Higher system cost.
- Best for: Prototype and first 2-3 production years.

**B. System-in-Package (SiP)**
```
┌─────────────────────────────┐
│    Package (QFN or LGA)     │
│  ┌──────┐     ┌──────────┐  │
│  │ MEMS │────►│ VibroSense│  │
│  │ die  │     │ ASIC die  │  │
│  └──────┘     └──────────┘  │
│       wire bonds / RDL      │
└─────────────────────────────┘
```
- Pros: Single package reduces board area. Shorter interconnects (lower parasitics). Each die on optimal process node. Customer sees one component.
- Cons: Multi-die packaging adds $0.50-2.00 per unit. Requires OSAT partnership. Thermal coupling between MEMS and ASIC.
- Best for: Volume production (>100K units/year) where board space matters.
- Available from: ASE, Amkor, JCET. X-FAB also offers SiP services.

**C. Monolithic MEMS-on-CMOS**
```
┌──────────────────────────────┐
│  Single Die                  │
│  ┌────────────────────────┐  │
│  │ MEMS accelerometer     │  │
│  │ (surface micromachined) │  │
│  ├────────────────────────┤  │
│  │ CMOS readout + analog  │  │
│  │ ML + digital control   │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```
- Pros: Minimum package size. Zero parasitic interconnect. Lowest system cost at very high volume. Single-chip solution is most attractive to customers.
- Cons: MEMS process constrains CMOS node (typically 180nm or 130nm). Higher NRE ($5-10M). Longer development (18-24 months). MEMS and CMOS process steps must be compatible. Very few foundries can do this.
- Foundries: **X-FAB** (180nm MEMS+CMOS, in production), **Tower** (limited), **STMicroelectronics** (internal only), **Bosch** (internal only).
- Best for: High-volume consumer applications (>1M units/year). Not recommended for VibroSense-1 at current stage.

### Recommendation

**Years 1-3:** Separate chips (MEMS + ASIC). Focus engineering on the analog ML, not on MEMS integration.

**Years 3-5:** System-in-Package. Once VibroSense-1 is validated with customers, partner with an OSAT to create a single-package solution. This reduces customer board area and creates a stickier product.

**Years 5+:** Evaluate monolithic integration only if volume exceeds 1M units/year and you can afford the $5-10M NRE. By then, the optimal CMOS node for monolithic may be X-FAB 130nm or 110nm (which supports MEMS).

---

## 9. Process Node Decision Matrix for VibroSense-1

| Criterion | Weight | 130nm (sky130) | 65nm (TSMC) | 28nm bulk | 22nm FD-SOI (GF) |
|-----------|--------|---------------|-------------|-----------|-------------------|
| Power efficiency | 30% | 2/10 | 5/10 | 6/10 | **9/10** |
| NRE cost | 20% | **10/10** | 7/10 | 4/10 | 6/10 |
| Analog performance | 20% | 5/10 | 7/10 | 5/10 | **9/10** |
| Startup access | 15% | **9/10** | 7/10 | 5/10 | 7/10 |
| Production scalability | 10% | 3/10 | 8/10 | **9/10** | 7/10 |
| Time to market | 5% | **9/10** | 7/10 | 5/10 | 6/10 |
| **Weighted score** | | **5.45** | **6.50** | **5.30** | **7.85** |

**Winner: GF 22FDX (22nm FD-SOI)** for production, with sky130 for prototype validation.

---

## 10. Key Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| GF 22FDX access denied to small startup | Cannot fabricate on recommended node | Use Europractice or CMC Microsystems for MPW access. BrainChip (small company) got access, so precedent exists. |
| $2-4M NRE exceeds available funding | Cannot tape out production chip | Stage the investment: $50-70K for 65nm MPW first to validate scaling assumptions. Only commit full NRE with customer LOIs in hand. |
| Analog redesign for 0.8V takes longer than expected | Schedule slip, burn rate | Hire analog designer with FD-SOI experience. Budget 12 months, plan for 18. |
| Sky130 chipIgnite remains paused | Prototype delay | Fall back to GF180 via wafer.space ($200-7K) or IHP SG13G2 via Tiny Tapeout. |
| PMOS subthreshold issue on sky130 does not exist on 22FDX | Prototype may not accurately predict production behavior | This is actually a benefit -- the production chip will be *better* than the prototype. Design prototype conservatively (no subthreshold PMOS), then optimize on 22FDX. |
| Competitor (POLYN, Aspinity) ships before VibroSense-1 production | Market share loss | Differentiate on 4-class fault identification (competitors only do binary anomaly detection). Use prototype silicon for customer demos while production is in development. |

---

## 11. Summary: The Commercialization Roadmap

```
2026 Q1-Q3: Prototype on sky130/GF180
            ├── Validate analog chain (OTA, filters, envelope, MAC)
            ├── Demonstrate to potential customers
            └── Cost: $10-50K

2026 Q3-Q4: 65nm MPW shuttle (optional intermediate step)
            ├── Validate analog scaling to lower Vdd
            ├── Confirm power reduction estimates
            └── Cost: $50-70K

2027 Q1:    Raise Series A ($5-10M)
            ├── Customer LOIs from prototype demos
            └── Production tapeout funding secured

2027 Q1-Q3: Full 22FDX design and tapeout
            ├── Analog redesign for 0.8V FD-SOI
            ├── Add body bias tuning (replace DAC-based tuning)
            ├── Leverage PMOS subthreshold (now reliable)
            └── Cost: $2-4M NRE

2027 Q4:    First 22FDX silicon back
            ├── Characterization and qualification
            └── Target: <100 uW always-on

2028 Q1-Q2: Production ramp
            ├── GF 22FDX volume production
            ├── ASP: $5-15
            └── Target: 50K-100K units Year 1

2029+:      System-in-Package (MEMS + ASIC)
            └── Single-package solution for customer convenience
```

---

## Sources

Key data points compiled from web research and cross-referenced with existing project research files. Specific sources:

- [Efabless chipIgnite program](https://efabless.com/chipignite/2110C) -- sky130 shuttle pricing and status
- [IHP Open Source PDK](https://github.com/IHP-GmbH/IHP-Open-PDK) -- SG13G2 technology details
- [GlobalFoundries FDX platform](https://gf.com/technology-platforms/fdx-fd-soi/) -- 22FDX body biasing and specifications
- [GF 22FDX+ announcement](https://gf.com/gf-press-release/globalfoundries-unveils-power-efficient-advancements-to-22fdx-platform-at-annual-tech-summit/) -- ULL SRAM, embedded RRAM
- [BrainChip AKD1500 tapeout](https://brainchip.com/brainchip-tapes-out-akd1500-chip-in-globalfoundries-22nm-fd-soi-process/) -- $2.3M tapeout cost on 22FDX
- [Aspinity AML200](https://www.aspinity.com/aml200/) -- 22nm analog ML chip
- [Wafer.space GF180MCU](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1) -- low-cost GF180 fabrication
- [Semiconductor Engineering: Legacy Nodes](https://semiengineering.com/legacy-process-nodes-going-strong/) -- mature node economics
- [Semiconductor Engineering: Analog's Unfair Disadvantage](https://semiengineering.com/analogs-unfair-disadvantage/) -- analog scaling challenges
- [SemiAnalysis: Photomask Cost Trends](https://newsletter.semianalysis.com/p/the-dark-side-of-the-semiconductor) -- mask set cost escalation
- [What Will That Chip Cost (Semiconductor Engineering)](https://semiengineering.com/what-will-that-chip-cost/) -- NRE cost by node
- [X-FAB Technology Portfolio](https://www.xfab.com/technology) -- MEMS+CMOS integration capabilities
- [Tower Semiconductor](https://towersemi.com/) -- 65nm BCD expansion at Intel Fab 11X
- [UMC 55nm BCD announcement](https://www.umc.com/en/News/press_release/Content/technology_related/20251022) -- new analog mixed-signal platform
- [Muse Semiconductor / GSME](https://www.musesemi.com/) -- TSMC shuttle access for startups
- [Europractice IC Service](https://europractice-ic.com/schedules-prices-2025/) -- MPW shuttle schedules and pricing
- [CMC Microsystems GF 22FDX access](https://www.cmc.ca/globalfoundries-22fdx-fdsoi-22-nm/) -- Canadian academic/industry access
- [EE Times: FD-SOI vs Bulk CMOS](https://semiengineering.com/bulk-cmos-versus-fd-soi/) -- FD-SOI analog advantages
- [AnySilicon: FDSOI Guide](https://anysilicon.com/fdsoi/) -- comprehensive FD-SOI overview
- [IIC-OSIC-TOOLS Docker](https://github.com/iic-jku/IIC-OSIC-TOOLS) -- open source EDA for all three PDKs
