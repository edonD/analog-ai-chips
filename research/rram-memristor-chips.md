# RRAM/Memristor-Based AI Chips: Deep Dive

## Summary

Resistive RAM (RRAM/ReRAM) is the most actively researched non-volatile memory technology for analog compute-in-memory (CIM) AI accelerators. Based on metal-oxide resistive switching — most commonly hafnium oxide (HfO2) — RRAM offers the highest density among CIM candidates (3-4x SRAM), true non-volatility, CMOS compatibility, and sub-10nm scaling potential. As of early 2026, RRAM CIM has produced more published silicon than any other analog CIM approach, with landmark chips from UCSD/Stanford (NeuRRAM), Tsinghua University (STELLAR, 28nm macro), Peking University (24-bit precision solver), and a Huawei-ByteDance-Tsinghua collaboration unveiled at ISSCC 2026. Yet no RRAM CIM chip is in volume production for AI inference. The gap between research demonstrations and commercial products remains defined by device variability, limited endurance, stuck-at faults, and the programming overhead that analog non-idealities impose.

---

## 1. How RRAM Works: Physics of the Filament

### Switching Mechanism

RRAM devices store information as resistance states. In the dominant filamentary type (used in virtually all CIM chips), a conductive filament forms and dissolves within a thin metal-oxide layer:

- **SET (Low Resistance State, LRS):** Applying a voltage across the oxide drives oxygen vacancies to form a conductive filament bridging the two electrodes. Current flows through this nanoscale metallic path.
- **RESET (High Resistance State, HRS):** Reversing or applying a different voltage partially ruptures the filament (typically at its narrowest point near one electrode), creating a tunnel barrier.
- **FORMING:** The first SET operation requires a higher voltage to create the initial filament. This is an annoyance for manufacturing — it adds a test step and can damage weak devices.

### HfO2: The Dominant Material

Hafnium oxide is the workhorse RRAM material for CIM because:

1. **CMOS compatibility:** HfO2 is already used as a high-k gate dielectric in advanced CMOS (since Intel's 45nm in 2007). Foundries know how to deposit it.
2. **Well-characterized:** Thousands of papers on HfO2 RRAM switching.
3. **Good on/off ratio:** Typically 10-100x between LRS and HRS.
4. **Scalable:** Demonstrated down to sub-10nm feature sizes.

The conductive filament in HfO2 devices has been directly imaged via atomic-scale TEM, revealing a quasi-core-shell structure: a crystalline hexagonal-Hf6O metallic core (essentially metallic Hf with one interstitial oxygen) surrounded by monoclinic or tetragonal HfOx. The filament diameter is typically 2-10 nm.

**Common device stacks for CIM:**
- TiN/HfOx/TaOy/TiN (Tsinghua STELLAR chip)
- Ti/HfO2/TiN (many academic demos)
- TaOx-based (Peking University 40nm chip)
- Proprietary stacks (TetraMem, Crossbar Inc.)

### The 1T1R Cell

Nearly all CIM-grade RRAM uses a 1-Transistor-1-Resistor (1T1R) structure. The access transistor:
- Acts as a selector, eliminating sneak-path currents in the crossbar
- Controls compliance current during SET (preventing filament overgrowth)
- Enables precise analog programming via gate voltage modulation
- Costs area (the transistor dominates the cell footprint at mature nodes)

Alternative structures — 1S1R (one selector), 1D1R (one diode), self-rectifying RRAM — trade area savings for less precise analog control and are less common in CIM.

---

## 2. RRAM Crossbar Arrays for MAC Operations

### How Analog MAC Works

The crossbar array is the computational primitive of RRAM CIM:

1. **Weights stored as conductances:** Each RRAM cell at intersection (i,j) is programmed to conductance G_ij representing a neural network weight.
2. **Input as voltage:** Input vector elements are applied as voltages V_i to the wordlines (rows).
3. **Ohm's law multiplication:** Current through cell (i,j) = V_i × G_ij.
4. **Kirchhoff's law accumulation:** Column (bitline) current = Σ(V_i × G_ij) — the dot product.
5. **ADC conversion:** The analog column current is digitized for downstream processing.

This performs a full matrix-vector multiplication (MVM) in a single step — O(1) time complexity vs. O(n²) for digital. For an N×N crossbar, that's N² multiply-accumulate operations simultaneously.

### Differential Weight Encoding

RRAM conductance is always positive, but neural network weights are signed. The standard solution is **differential encoding**: each weight uses two RRAM cells (G+ and G-), with the effective weight W = G+ - G-. This doubles cell count but enables bipolar weights. NeuRRAM uses this approach, encoding each weight with just two cells while achieving 4-bit effective precision.

### Critical Non-Idealities

**Sneak-path currents:** In passive crossbar arrays (without per-cell transistors), current can flow through unintended paths. For a read of cell (i,j), current sneaks through adjacent low-resistance cells, corrupting the measurement. The 1T1R structure eliminates this but at area cost. Impact worsens with array size — a key reason why practical RRAM crossbars are limited to 256×256 or 512×512 rather than the theoretically possible millions of cells.

**IR drop (wire resistance):** Metal interconnects in the crossbar have finite resistance. As array size grows, voltage drops along wordlines and bitlines cause cells far from the drivers to see reduced voltages, leading to systematic computation errors. For a 256×256 array with typical wire resistance, the worst-case cell can see 10-20% voltage reduction. Solutions:
- Limit array size (128×128 or 256×256 typical)
- IR-drop-aware training/compensation in software
- Double-sided driving of wordlines/bitlines

**Device variability (D2D and C2C):**
- Device-to-Device (D2D): Cells programmed to the same target show different conductances due to manufacturing variation in oxide thickness, composition, and filament formation sites. Typical σ/μ = 5-20%.
- Cycle-to-Cycle (C2C): The same cell programmed repeatedly to the same target gives slightly different conductances each time, because filament formation/rupture is inherently stochastic. Typical σ/μ = 3-10%.

**Random Telegraph Noise (RTN):** Traps in the oxide cause discrete conductance fluctuations during read, particularly severe in HRS where fewer conduction paths exist. This is a fundamental property of nanoscale filaments — the capture/emission of a single electron by a trap can measurably change the current.

**Read disturb:** Applying read voltages can gradually shift the conductance state, particularly for devices in intermediate analog levels. This is especially problematic for CIM where cells are read continuously during inference.

**Temperature sensitivity:** RRAM conductance has a temperature coefficient. Joule heating during read/write creates local temperature gradients. Automotive temperature ranges (-40°C to 150°C) have not been demonstrated for analog CIM operation (though Weebit's digital RRAM has achieved AEC-Q100 150°C qualification for binary storage).

---

## 3. State-of-the-Art RRAM CIM Chips: Who Has Real Silicon?

### 3.1 NeuRRAM (UCSD/Stanford/Tsinghua, 2022)

**Publication:** Nature, August 2022 — "A compute-in-memory chip based on resistive random-access memory"

**The landmark RRAM CIM chip.** First fully integrated, large-scale demonstration of RRAM CIM executing diverse real AI tasks.

**Architecture:**
- 48 neurosynaptic cores
- Each core: 256×256 RRAM crossbar (65,536 cells) + 256 CMOS neuron circuits
- Total: 3 million RRAM synapses, 12,000 neurons
- **Transposable Neurosynaptic Array (TNSA):** The key innovation. CMOS neurons are physically interleaved within the RRAM array (not just on the periphery). Each neuron's connections to the array can be configured as either input or output, enabling the same hardware to support different dataflow directions. This allows reconfiguration for diverse NN architectures without rewiring.
- Differential 2-cell encoding per weight (G+ and G-), achieving 4-bit effective weight precision
- **Process:** 130nm CMOS with RRAM integrated in back-end-of-line (BEOL)
- Energy-efficient voltage-sensing neuron circuits perform analog-to-digital conversion in-situ

**Results:**
| Task | Accuracy | Notes |
|------|----------|-------|
| MNIST (7-layer CNN) | 99.0% | Comparable to 4-bit quantized software |
| CIFAR-10 (ResNet-20) | 85.7% | 14.3% error rate |
| Google Speech Commands | 84.7% | — |
| Image denoising (Bayesian) | 70% error reduction | vs. noisy input |

**Energy Efficiency:**
- 2x better energy-delay product (EDP) than prior RRAM CIM chips
- 7-13x higher computational density than prior state-of-the-art
- Specific TOPS/W numbers not published in the same format as commercial chips (academic metrics focused on EDP)

**Significance:** NeuRRAM proved that RRAM CIM can achieve software-comparable accuracy on real tasks, not just synthetic benchmarks. The TNSA architecture solved the reconfigurability problem that plagued earlier fixed-function CIM chips.

**Limitations:**
- 130nm process — enormous by modern standards (7-10x the feature size of current edge AI chips)
- 3 million synapses supports only small models (think MNIST/CIFAR, not ImageNet or LLMs)
- No published system-level power or throughput numbers comparable to commercial chips
- Research prototype, not a product

**Team:** Weier Wan (Stanford/UCSD), co-advised by Gert Cauwenberghs (UCSD bioengineering) and H.-S. Philip Wong (Stanford). Tsinghua's Huaqiang Wu contributed RRAM device expertise.

**Post-2022 development:** In December 2025, researchers at UCSD's IEEE IEDM presentation demonstrated a new "bulk RRAM" variant (see Section 7) with 6-bit per cell and 3D stacking, representing a potential next-generation path.

---

### 3.2 Tsinghua STELLAR Chip (2023)

**Publication:** Science, September 2023 — "Edge learning using a fully integrated neuro-inspired memristor chip"

**The first RRAM chip to demonstrate on-chip learning** (not just inference).

**Architecture:**
- Full-system integrated chip: multiple RRAM crossbar arrays + all CMOS peripheral circuits for complete on-chip learning
- **Monolithic 3D integration:** RRAM arrays fabricated directly above CMOS logic (not side-by-side)
- 2T2R cell configuration to handle signed weights and mitigate IR drop
- TiN/HfOx/TaOy/TiN memristor stack
- STELLAR (Sign- and Threshold-based Learning) algorithm: specifically designed for memristor hardware — avoids the precise weight updates that analog devices struggle with, using only sign and threshold operations

**Results:**
- Motion control, image classification, speech recognition — all with on-chip learning
- Software-comparable accuracy achieved
- Energy consumption: **3% of equivalent ASIC** for on-chip learning tasks

**Key Innovation:** On-chip learning is extremely challenging for RRAM because:
1. Each weight update requires a program-verify cycle (slow, energy-intensive)
2. RRAM endurance is limited (10^6 - 10^8 cycles typical)
3. Programming noise makes precise gradient updates nearly impossible

STELLAR sidesteps these by using a binarized learning rule that only requires coarse weight updates (sign flips), dramatically reducing the number and precision of write operations needed.

**Team:** Wu Huaqiang, Gao Bin — Tsinghua University School of Integrated Circuits, LEMON Lab.

---

### 3.3 Tsinghua 28nm 576K RRAM CIM Macro (2025)

**Publication:** Journal of Semiconductors, January 2025

**The most process-advanced RRAM CIM macro from Chinese academia.**

**Specifications:**
- **Process:** 28nm — the most advanced node for a published RRAM CIM chip
- **Array:** 576K RRAM cells
- **Area efficiency:** 2.82 TOPS/mm²
- **Energy efficiency:** 35.6 TOPS/W
- **Hybrid programming scheme:** 4.67x faster programming, 0.15x power saving, 4.31x more compact weight distribution vs. conventional P&V
- Novel direct-current ADC design shared between programming and inference stages

**Significance:** This demonstrates that RRAM CIM can be fabricated at foundry-relevant nodes (28nm is where most IoT/edge chips are made today). The hybrid programming scheme addresses one of RRAM CIM's biggest practical pain points — the hours of program-verify time needed to set up weights.

---

### 3.4 Peking University 24-Bit Precision RRAM Solver (2025)

**Publication:** Nature Electronics, October 2025 — "Precise and scalable analogue matrix equation solving using resistive random-access memory chips"

**The most precise analog computation ever demonstrated on RRAM.**

**Architecture:**
- TaOx-based RRAM on commercial **40nm CMOS** foundry process
- 1T1R cells programmed to 8 discrete conductance levels (3-bit per cell)
- Conductance range: 0.5-35 μS, with write-verify achieving 100% programming success across 400 tested cells
- Two-circuit approach:
  1. **Fast approximation circuit:** Low-precision matrix inversion (~120 ns per operation)
  2. **Refinement circuit:** High-precision matrix-vector multiplication using bit slicing across multiple RRAM arrays
- Iterative algorithm combines both circuits

**Results:**
- **24-bit fixed-point precision** for 16×16 matrix inversion (comparable to FP32)
- Relative errors below 10^-7 after 10 iterations
- 100-1000x higher throughput and energy efficiency than GPUs for MIMO signal detection
- Atomic operational latency: ~120 ns for LP-INV operation

**The Catch:** This is not a general-purpose AI inference chip. It solves matrix equations — a specific mathematical operation that happens to map perfectly onto analog crossbar arrays. The 1000x-faster-than-GPU claim is for this specific workload (large-scale MIMO signal detection), not for general neural network inference. The 24-bit precision comes from the iterative algorithm (running the analog hardware multiple times), not from 24-bit analog resolution per device (which remains 3-bit). It is an excellent demonstration of how low-precision analog can be composed into high-precision computation, but the throughput advantage shrinks as more iterations are needed.

**Team:** Sun Zhong, Institute for Artificial Intelligence, Peking University; Beijing Advanced Innovation Center for Integrated Circuits.

---

### 3.5 Huawei-ByteDance-Tsinghua RRAM Chip (ISSCC 2026)

**Announced:** March 2026 at ISSCC 2026

An unusual alliance between Huawei, ByteDance, Tsinghua University, and other Beijing research institutions unveiled an RRAM-based AI acceleration chip. Key claims:

- **66x faster than conventional CPUs** for targeted AI workloads
- Developed in the context of US semiconductor sanctions, as China pushes for domestic alternatives

**Details are sparse** — the full ISSCC paper requires subscription access and detailed specifications have not been publicly released as of March 2026. The involvement of both Huawei (hardware) and ByteDance (AI workloads/software) suggests this is more than a pure research exercise — it targets real deployment scenarios.

**Significance for the RRAM field:** This is the first time major Chinese tech companies (not just universities) have publicly backed RRAM CIM for AI, suggesting the technology is approaching commercial relevance in China's domestic semiconductor ecosystem.

---

## 4. TetraMem: The 11-Bit-Per-Device Claim

### Background

TetraMem Inc., founded 2018, spun out of research by J. Joshua Yang (USC), Qiangfei Xia (UMass Amherst), and collaborators. The company develops analog in-memory computing chips using multi-level RRAM (memristors).

### The Science Paper (February 2024)

"Programming memristor arrays with arbitrarily high precision for analog computing" — published in *Science*, vol. 383(6685):903-910.

**Claim:** Achieving 2,048 conductance levels (11 bits) per device — the highest device precision among all known memory technologies.

**How it works:**
The key insight is that you don't need each individual device to be precise — you need the *weighted combination* of devices to be precise. The method:

1. Program the first device to approximate the target value
2. Measure the programming error
3. Program a second device to compensate for that error
4. Measure the residual error
5. Program a third device to compensate for the residual
6. Continue until the desired precision is reached

Each subsequent device compensates for the errors of the previous ones, achieving arbitrarily high precision from low-precision components. This is essentially a hardware implementation of iterative refinement / successive approximation.

**Results:** Solving partial differential equations with <10^-15 error, with higher energy efficiency than digital computing.

**The catch:** The 11-bit figure refers to the effective precision of a *multi-device composite*, not a single RRAM cell achieving 2,048 distinguishable levels independently. A single device still has ~6-8 bits of raw resolution at best (and more like 3-4 bits in typical crossbar operation). The multi-device approach trades area and programming time for precision — each effective "weight" requires multiple RRAM cells and multiple program-verify cycles. This is a legitimate and clever approach, but it should not be compared directly to a single SRAM cell or flash cell storing 11 bits.

### TetraMem Products

- **MX100:** First evaluation SoC, fabricated in a commercial process, demonstrated in March 2024 with applications in AR/VR face tracking and autonomous vehicle monitoring
- **MX200:** Next-generation chip on 22nm, designed for edge inference (low-power, low-latency)
- **Partnership with Andes Technology:** Licensed the NX27V RISC-V vector CPU, combined with TetraMem's analog CIM via the Andes Custom Extension (ACE) interface
- **Investors:** SK hynix, SK Square, LIG Nex1, Shinhan Financial Group, Foothill Ventures
- **SK hynix research partnership:** Announced November 2024

**Status as of early 2026:** TetraMem has demonstrated functional SoCs but has not announced volume production or published independent benchmark results. The company appears to be in the late-prototype / early-sampling stage, targeting 2026-2027 for commercial availability.

---

## 5. Chinese RRAM Efforts: An Emerging Lead

China has the most active RRAM CIM research ecosystem in the world, driven by:

1. **Strategic imperative:** US semiconductor sanctions make advanced digital chips (TSMC 5nm, 3nm) unavailable. Analog CIM on mature nodes (28nm, 40nm) offers a potential architectural end-run.
2. **Strong academic base:** Tsinghua and Peking University have world-leading RRAM device and circuit groups.
3. **Government funding:** RRAM CIM aligns with China's "new productive forces" and semiconductor self-sufficiency goals.
4. **Industry adoption:** The Huawei-ByteDance ISSCC 2026 collaboration signals commercial interest.

### Key Chinese Groups

| Institution | Key Researchers | Notable Chips | Focus |
|-------------|----------------|---------------|-------|
| Tsinghua Univ. (LEMON Lab) | Wu Huaqiang, Gao Bin | STELLAR (Science 2023), 28nm 576K macro, NeuRRAM co-author | On-chip learning, 3D integration, programming optimization |
| Peking University | Sun Zhong | 40nm 24-bit precision solver (Nature Electronics 2025) | High-precision analog computing, iterative algorithms |
| Tsinghua + Huawei + ByteDance | Multiple | ISSCC 2026 RRAM chip | Commercial AI acceleration |

### The 28nm Advantage

China's domestic foundries (SMIC, Hua Hong) can fabricate 28nm chips without US-controlled EUV lithography. RRAM CIM at 28nm is therefore entirely within China's manufacturing capability — unlike cutting-edge digital AI chips that require TSMC's advanced nodes. This makes RRAM CIM strategically significant for China's AI hardware ambitions.

---

## 6. RRAM Reliability Challenges: The Hard Problems

### 6.1 Endurance

RRAM endurance — the number of SET/RESET cycles before failure — varies dramatically:

| Application | Required Endurance | Typical HfO2 RRAM | Status |
|-------------|-------------------|-------------------|--------|
| Digital NVM (code storage) | 10^5 - 10^6 | 10^6 - 10^8 | Adequate |
| CIM inference (write-once) | 10^3 - 10^4 | Easily met | OK |
| CIM with model updates | 10^5 - 10^6 | 10^6 - 10^8 | Marginal |
| CIM with on-chip training | 10^8 - 10^12 | 10^6 - 10^8 | **Insufficient** |

The endurance bottleneck is critical for on-chip learning. STELLAR's approach (coarse binary updates instead of precise gradient updates) partially addresses this by reducing the number and magnitude of write operations, but fundamentally, RRAM devices degrade with cycling. ITRI has demonstrated 10^10 endurance in optimized devices, but this is not yet standard in foundry processes.

**Failure modes at end-of-life:**
- Stuck-at-LRS (stuck-on): Filament becomes permanently formed, cell always conducts
- Stuck-at-HRS (stuck-off): Oxide damage prevents filament reformation
- Increased variability: Resistance distributions widen, reducing effective bit precision

### 6.2 Variability

This is the single most important challenge for RRAM CIM.

**Device-to-Device (D2D) variability** arises from:
- Oxide thickness variations across the wafer
- Composition non-uniformity in deposited films
- Stochastic filament formation (random nucleation sites)
- Transistor threshold voltage mismatch in the access device

**Cycle-to-Cycle (C2C) variability** arises from:
- Stochastic oxygen vacancy dynamics (each SET/RESET creates a slightly different filament)
- Random trap states in the oxide
- Thermal fluctuations during switching

**Quantified impact:** In a typical 256×256 RRAM array programmed for CIM, the effective precision is 3-4 bits per cell, even though individual cells can be programmed to 6+ distinguishable levels under careful lab conditions. Array-scale operation with parallel sensing, IR drop, and readout noise reduces the usable precision.

### 6.3 Stuck-At Faults (SAF)

Manufacturing defects cause some cells to be permanently stuck in LRS (stuck-at-1) or HRS (stuck-at-0). These are hard faults that cannot be fixed by reprogramming.

**Typical SAF rates:** 0.1% - 5% depending on process maturity and oxide quality.

**Impact on neural networks:**
- At <1% SAF rate: Accuracy degradation is negligible for most DNNs (neural networks are naturally fault-tolerant)
- At 1-7.5% SAF rate: Differential mapping methods can recover original inference accuracy
- At 7.5-30% SAF rate: Fault-aware training (DropConnect-style) can limit accuracy loss to <1%
- At >30% SAF rate: Accuracy degrades significantly regardless of mitigation

**Mitigation strategies:**
1. **Fault-aware training:** Include fault models during training so the network learns around defects
2. **DropConnect emulation:** Randomly zero weights during training to build robustness to stuck-at faults
3. **Redundancy:** Map critical weights to multiple cells
4. **Post-manufacturing calibration:** Detect faulty cells and remap weights to avoid them

### 6.4 Programming Overhead

Programming RRAM for CIM is fundamentally different from digital RRAM writing:

- **Digital:** Program to binary LRS or HRS — fast (5-10 ns per pulse), low energy (~350 fJ/bit)
- **Analog CIM:** Program to precise intermediate conductance levels — requires iterative program-verify (P&V) cycles

**Typical P&V sequence:**
1. Apply a programming pulse (SET or RESET, 10-100 ns)
2. Read the resulting conductance
3. Compare to target
4. If not within tolerance, apply adjusted pulse
5. Repeat until target is met

For 3-bit precision (8 levels): Average 3-4 P&V cycles per cell
For 4-bit precision (16 levels): Average 5-10 P&V cycles per cell
For 6-bit precision: May require 20+ cycles

**Time to program a full chip:** For a NeuRRAM-scale chip (3M cells at 4-bit precision), programming takes minutes to hours. Tsinghua's hybrid programming scheme (4.67x speedup) helps but doesn't eliminate the fundamental issue.

### 6.5 Retention and Drift

RRAM has better retention than PCM (which suffers from crystallization drift) but is not immune:
- Intermediate conductance states can drift over time (weeks to months)
- Temperature accelerates drift
- HRS states are more stable than intermediate states
- Drift direction is generally toward lower conductance (filament relaxation)

Compared to PCM (where drift coefficient v = 0.1-0.15 is a major problem), RRAM drift is smaller but non-zero and poorly characterized for long-duration analog CIM operation.

---

## 7. RRAM vs. Flash CIM vs. PCM CIM vs. Capacitor CIM

### Head-to-Head Comparison

| Property | RRAM | Flash (Mythic) | PCM (IBM) | Capacitor (EnCharge) | SRAM CIM |
|----------|------|----------------|-----------|---------------------|----------|
| **Cell size** | 1T1R (~50-100 F²) | 1T (~25 F²) | 1T1R (~50-100 F²) | SRAM-based (~100-150 F²) | 6T (~150 F²) |
| **Density advantage** | 3-4x vs SRAM | 6-8x vs SRAM | 3-4x vs SRAM | ~1x SRAM | Baseline |
| **Non-volatile** | Yes | Yes | Yes | **No** (volatile) | **No** |
| **Effective bits (CIM)** | 3-4 | 4-6 | 3-4 | 6-8 | N/A (digital) |
| **Write energy** | ~pJ/cell | ~10-100 pJ/cell | ~10 pJ/cell | ~fJ/cell (capacitor charge) | ~fJ/cell |
| **Write speed** | 10-100 ns | ~10 μs (FN tunneling) | 50-100 ns | <1 ns | <1 ns |
| **Endurance** | 10^6-10^8 | 10^4-10^5 | 10^8-10^9 | Unlimited (SRAM) | Unlimited |
| **On/Off ratio** | 10-100x | 100-1000x | 10-100x | N/A | N/A |
| **Drift** | Low | Very low | **High** (v=0.1-0.15) | None | None |
| **Variability** | **High** (filament stochasticity) | Moderate | Moderate-High | **Low** (capacitor matching) | Very Low |
| **DC sneak paths** | Yes (need 1T1R) | No (gated) | Yes (need 1T1R) | **No** (charge-domain) | No |
| **Process maturity** | Emerging (22-40nm in fabs) | Mature (40nm+) | Emerging (14nm IBM) | Uses standard SRAM | Mature |
| **Best TOPS/W published** | 35.6 (Tsinghua 28nm) | ~8 (Mythic Gen1, 120 claimed Gen2) | 12.4 (IBM HERMES) | ~24 claimed (EnCharge EN100) | 192.3 (ISSCC 2025 digital) |
| **Best TOPS/mm²** | 2.82 (Tsinghua 28nm) | ~1 (Mythic est.) | ~1 (IBM est.) | 30 claimed (EnCharge) | varies |

### Key Takeaways

**RRAM's advantages over Flash CIM:**
- Much faster write speed (10-100 ns vs. 10 μs) — enabling model updates in the field
- Lower write voltage — Flash requires high voltages (8-15V) for Fowler-Nordheim tunneling
- Better scaling potential — Flash struggles below 28nm; RRAM demonstrated at sub-10nm
- Comparable or better density

**RRAM's advantages over PCM:**
- Much lower drift — PCM's resistance drift is its Achilles' heel
- Lower write current/energy — PCM requires melting/recrystallizing, which is power-hungry
- Simpler integration — PCM requires specialized materials (GeSbTe or similar)

**RRAM's disadvantages vs. Capacitor CIM (EnCharge):**
- Worse variability — RRAM filament stochasticity is fundamentally harder to control than capacitor charge
- DC sneak paths — capacitor CIM operates in charge/time domain, inherently sneak-path-free
- Lower effective precision — capacitor CIM achieves 6-8 effective bits vs. RRAM's 3-4
- Higher write energy for programming — capacitor CIM uses standard SRAM writes
- But: RRAM is non-volatile (no weight reloading from DRAM at power-on)

**RRAM's disadvantages vs. SRAM CIM:**
- Variability and noise reduce effective precision
- Programming is slow and complex
- Endurance limits model updates
- But: RRAM is 3-4x denser and non-volatile

---

## 8. Circuit Innovations for RRAM Non-Idealities

### 8.1 Bit Slicing

Since a single RRAM cell achieves only 3-4 effective bits, higher-precision weights are split across multiple cells:

- **Weight bit slicing:** An 8-bit weight is stored across two 4-bit cells (or three 3-bit cells). The column currents from each slice are digitally combined with appropriate shifting.
- **Input bit slicing:** Multi-bit inputs are applied one bit at a time as successive voltage pulses, with accumulation in the digital domain.

Peking University's 24-bit precision achievement uses extensive bit slicing across multiple arrays — combining 3-bit-per-cell arrays through a bit-sliced matrix-vector multiplication to achieve high composite precision.

**Cost:** Bit slicing multiplies the required array area and number of ADC conversions proportionally. A 4-bit weight in 2-bit slices requires 2x the cells and 2x the ADC reads, plus digital shift-and-add logic.

### 8.2 Differential Mapping

The 2T2R (or 2-cell differential) approach:
- Each weight W = G+ - G-
- Subtracts common-mode noise (thermal, supply noise)
- Cancels first-order offset errors
- Enables bipolar weights without negative conductances

NeuRRAM's differential encoding achieves 4-bit effective precision from cells with higher raw variability, proving the approach works at scale.

### 8.3 ADC Sharing and In-Memory ADC

ADCs dominate RRAM CIM area and power (40-85% of system total). Key innovations:

- **Shared ADCs:** One ADC serves multiple columns via time-multiplexing. Tsinghua's 28nm macro uses a shared direct-current ADC for both programming and inference, saving area.
- **CCO-based ADC:** Current-controlled oscillators convert analog column current to a frequency, counted by a digital counter. Avoids voltage-domain ADC noise. Used in NeuRRAM's neuron circuits.
- **In-memory ADC:** The RRAM array itself participates in the conversion — e.g., reference currents generated by known RRAM states are compared against compute currents. Published results show 0.01x energy of conventional ADCs.
- **TNSA approach (NeuRRAM):** Physically interleaving CMOS neurons within the RRAM array minimizes the wire distance between analog computation and digitization, reducing noise pickup and enabling voltage-sensing (vs. current-sensing) for better energy efficiency.

### 8.4 Programming Optimization

Tsinghua's hybrid programming scheme (28nm macro):
- Combines coarse fast programming with fine iterative verification
- 4.67x programming speedup
- 0.15x power reduction during programming
- Achieves 4.31x more compact weight distributions

The Compliance-free Ultra-short Smart Pulse Programming (CUSPP) technique uses sub-nanosecond pulses to minimize energy per programming step, enabling faster and more reliable multi-level programming.

### 8.5 Variation-Aware Training

The most impactful mitigation is not in hardware but in software:
- Inject device noise models (D2D variance, C2C variance, stuck-at faults) into the training loop
- The network learns to be robust to hardware imperfections
- NeuRRAM's software-comparable accuracy was achieved specifically through noise-aware training
- Results: NeuRRAM achieved 85.7% on CIFAR-10 (vs. ~86% software baseline for 4-bit quantized models)

**The coupling problem:** Noise-aware training creates tight hardware-software coupling — a model trained for one chip's noise profile may not work on another. This is antithetical to the software portability that makes GPUs dominant.

---

## 9. UCSD Bulk RRAM: A Potential Game-Changer (2025)

Presented at IEEE IEDM 2025 (December 2025), UCSD researchers introduced **bulk RRAM** — a fundamentally different switching mechanism:

### How It Differs

- **Conventional RRAM:** Switching occurs via a nanoscale filament (2-10 nm diameter) — inherently stochastic
- **Bulk RRAM:** The entire oxide layer switches from high to low resistance — no filament formation

### Advantages

1. **No forming step required** — eliminates a major manufacturing headache
2. **No selector transistor needed** — the bulk switching mechanism is inherently non-linear enough to suppress sneak paths
3. **6-bit per cell** (64 resistance levels) with a single voltage pulse — vs. iterative P&V for filamentary RRAM
4. **3D stackable:** Demonstrated 8-layer 3D stack with 40nm cell size
5. **Scalable:** Individual cells at 40nm, with a path to smaller

### Implications

If bulk RRAM's advantages hold up at scale, it would address several of RRAM CIM's biggest problems simultaneously:
- Eliminates forming (manufacturing simplification)
- Removes the selector transistor (area reduction)
- Higher per-cell precision (fewer bit slices needed)
- 3D stacking for massive density

**Caution:** This is a device demonstration, not a CIM chip. The path from IEDM device paper to integrated CIM chip is typically 3-5 years. Variability, endurance, and noise characteristics at array scale are unknown. But this represents the most promising RRAM device innovation in years.

---

## 10. The Path to Production

### Where RRAM CIM Stands in 2026

**Foundry availability:**
- **GlobalFoundries:** 22FDX+ with embedded RRAM (OxRAM) announced August 2025. PDK available. Volume production targeted for 2026. Focused on digital NVM (code storage, wireless MCU), not analog CIM specifically.
- **TSMC:** Offers RRAM (OxRAM) technology. Used by academic groups and startups.
- **UMC + eMemory:** 22nm RRAM qualified. Focused on embedded NVM for IoT.
- **Chinese foundries:** SMIC and others can support RRAM at 28nm+.

**Companies with RRAM CIM silicon:**
- TetraMem (MX100 SoC, MX200 in development)
- Crossbar Inc. (XPU accelerator with RRAM — 30x speedup, 500x power reduction vs. ARM+DDR4)
- Weebit Nano (RRAM IP licensing to onsemi, TI — focused on NVM, not CIM yet, though they won a Korean government ACiM project in March 2026)

**Companies with CIM silicon using other NVM:**
- Mythic AI (Flash CIM, Gen 2 shipping)
- IBM (PCM CIM, HERMES research)
- EnCharge AI (Capacitor CIM, EN100)

### What Needs to Happen

1. **Yield improvement:** SAF rates need to drop below 0.1% for production-grade CIM. Current rates of 0.1-5% are acceptable for research but not for high-volume manufacturing.

2. **Programming time reduction:** Hours to program a chip is unacceptable for production. Need to reach minutes or seconds. Tsinghua's hybrid programming helps but more innovation is needed.

3. **Endurance for model updates:** If CIM chips need OTA model updates (increasingly required for edge AI), 10^6 cycles may not be enough. Bulk RRAM's potential for higher endurance is encouraging.

4. **Temperature qualification:** No RRAM CIM chip has demonstrated operation across automotive or industrial temperature ranges in analog mode. Weebit's AEC-Q100 qualification is for digital RRAM, not analog CIM.

5. **Software ecosystem:** No mature compiler/SDK exists for RRAM CIM. Each chip requires custom model-to-hardware mapping. This is arguably the biggest barrier to adoption — without a software ecosystem, even perfect hardware won't get deployed.

6. **Standard benchmarks:** MLPerf-style benchmarks for CIM hardware are needed to enable fair comparison. Current published results use different models, datasets, and measurement methodologies, making comparison nearly impossible.

### Timeline Estimate

| Milestone | Estimated Date |
|-----------|---------------|
| First RRAM CIM product sampling (TetraMem MX200 or similar) | 2026-2027 |
| GlobalFoundries 22FDX+ RRAM volume production | 2026 |
| First independent RRAM CIM benchmark results | 2027 |
| RRAM CIM in commercial edge AI product | 2027-2028 |
| RRAM CIM competitive with digital for mainstream AI workloads | 2030+ (if ever) |

---

## 11. Honest Assessment

### What RRAM CIM Does Well

1. **Density:** 3-4x over SRAM means more weights on chip, less data movement
2. **Non-volatility:** Instant-on, no weight reloading — critical for always-on edge AI
3. **Energy for MVM:** The physics is fundamentally favorable — Ohm's law multiply is nearly free
4. **Proven in silicon:** Multiple chips demonstrate real AI tasks at software-comparable accuracy
5. **Scalable process:** Can be manufactured at 28nm and below, in existing fabs

### What RRAM CIM Does Poorly

1. **Variability:** The stochastic filament is both RRAM's feature and its curse. 3-4 effective bits per cell means every approach requires bit slicing, differential encoding, or multi-device composites — all of which eat into the density advantage.
2. **Programming:** Slow, power-hungry, and itself limited by endurance. This makes model updates costly and limits the field-upgradeability that modern edge AI demands.
3. **System-level efficiency:** The 2-10x advantage over digital at system level (after ADCs, DACs, programming overhead, calibration) is real but modest — and digital CIM keeps improving (192.3 TFLOPS/W at ISSCC 2025 for SRAM CIM).
4. **Software:** No ecosystem. Every deployment is a custom project.
5. **Precision ceiling:** For workloads requiring INT8 or better, RRAM CIM requires extensive bit slicing that erodes its throughput and area advantages.

### The Fundamental Question

RRAM CIM's value proposition rests on density × non-volatility × energy. If you need to store millions of weights on-chip without external DRAM, and inference energy is your binding constraint, RRAM CIM is compelling. But:

- If you can tolerate SRAM volatility (weight reload from flash at power-on), capacitor/SRAM CIM may offer better precision and simpler programming
- If you need 8+ bit precision, digital CIM or conventional digital accelerators may be more practical
- If your model fits in SRAM, digital CIM's improving efficiency (192 TFLOPS/W) may close the gap before RRAM CIM reaches production maturity

The strongest near-term case for RRAM CIM is **always-on edge AI** at extreme power budgets (<1 mW), where non-volatility eliminates standby power and the small model sizes (sub-1M parameters) keep within RRAM's effective precision range. The weakest case is competing head-to-head with NVIDIA or even Mythic/EnCharge on mainstream inference workloads.

China's strategic investment may change the equation — if Huawei and ByteDance push RRAM CIM into production for domestic AI deployment, the technology could reach commercial maturity faster than purely market-driven development would allow.

---

## Sources

- [NeuRRAM: UCSD/Stanford Announcement](https://today.ucsd.edu/story/Nature_bioengineering_2022)
- [NeuRRAM Nature 2022 Paper](https://www.nature.com/articles/s41586-022-04992-8)
- [NeuRRAM IEEE Brain Article](https://brain.ieee.org/newsletter/2022-issue-2/neurram-rram-compute-in-memory-chip-for-efficient-versatile-and-accurate-ai-inference/)
- [STELLAR: Edge learning memristor chip - Science 2023](https://www.science.org/doi/10.1126/science.ade3483)
- [Tsinghua STELLAR Breakthrough - CGTN](https://news.cgtn.com/news/2023-10-11/China-makes-major-breakthrough-in-memristor-computing-in-memory-chips-1nOqlLtvMgE/index.html)
- [Tsinghua 28nm 576K RRAM CIM Macro](https://www.jos.ac.cn/en/article/doi/10.1088/1674-4926/24100017)
- [Peking University RRAM 24-bit Precision - Nature Electronics 2025](https://www.nature.com/articles/s41928-025-01477-0)
- [Peking University RRAM - TechXplore](https://techxplore.com/news/2025-10-rram-based-analog-rapidly-matrix.html)
- [Huawei-ByteDance RRAM Chip ISSCC 2026 - DigiTimes](https://www.digitimes.com/news/a20260302PD215/huawei-bytedance-rram-isscc-2026.html)
- [TetraMem Science Paper: Arbitrarily High Precision](https://www.science.org/doi/10.1126/science.adi9405)
- [TetraMem + Andes RISC-V SoC](https://semiwiki.com/ip/349000-tetramem-integrates-energy-efficient-in-memory-computing-with-andes-risc-v-vector-processor/)
- [TetraMem TechInsights DLA Overview](https://www.techinsights.com/blog/tetramem-touts-memory-dla)
- [Bulk RRAM: Scaling the AI Memory Wall - IEEE Spectrum](https://spectrum.ieee.org/ai-and-memory-wall)
- [GlobalFoundries 22FDX+ RRAM Announcement](https://gf.com/gf-press-release/globalfoundries-announces-availability-of-22fdx-rram-technology-for-wireless-connectivity-and-ai-applications/)
- [Weebit Nano 2025 Targets](https://www.weebit-nano.com/news/press-releases/weebit-nano-reports-on-2025-targets-achievement/)
- [Weebit ReRAM for Edge AI](https://www.weebit-nano.com/reram-powered-edge-aia-game-changer-for-energy-efficiency-cost-and-security/)
- [Crossbar Inc. RRAM AI Accelerator](https://www.rram-info.com/crossbar-announces-rram-based-ai-accelerator-chip)
- [HfO2 Filament Atomic-Scale Imaging - Nature Communications](https://www.nature.com/articles/s41467-021-27575-z)
- [RRAM Endurance and Retention Challenges](https://ieeexplore.ieee.org/iel7/8955687/8964633/08964707.pdf)
- [Sneak Path Solutions - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9418872/)
- [Drop-Connect Fault Tolerance for RRAM](https://arxiv.org/html/2404.15498v1)
- [RRAM vs NVM Comparison in CIM](https://pubs.aip.org/aip/adv/article/15/3/035317/3339501)
- [Bit Slicing for Variability-Aware RRAM CIM](https://www.degruyterbrill.com/document/doi/10.1515/itit-2023-0018/html)
- [RRAM CIM Trends and Challenges](https://www.sciencedirect.com/science/article/pii/S2709472322000028)
- [Current Opinions on Memristor ML Hardware 2025](https://www.sciencedirect.com/science/article/pii/S1359028625000130)
- [Neuromorphic Computing at Scale - Nature 2025 Review](https://gwern.net/doc/ai/scaling/hardware/2025-kudithipudi.pdf)
