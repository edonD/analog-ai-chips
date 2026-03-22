# Analog Compute-in-Memory (CIM) Landscape: 2025-2026

*Comprehensive overview of who has silicon, what works, what does not, and where the field is heading.*

Last updated: 2026-03-22

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Memory Technologies for CIM](#memory-technologies-for-cim)
3. [Companies with Actual Silicon](#companies-with-actual-silicon)
4. [Startups to Watch](#startups-to-watch)
5. [Dead or Dying](#dead-or-dying)
6. [Key Academic Groups](#key-academic-groups)
7. [ISSCC 2025 CIM Papers](#isscc-2025-cim-papers)
8. [Performance Comparison Table](#performance-comparison-table)
9. [Fundamental Tradeoffs](#fundamental-tradeoffs)
10. [The Software Problem](#the-software-problem)
11. [CIM for LLMs and Transformers](#cim-for-llms-and-transformers)
12. [Government and Institutional Funding](#government-and-institutional-funding)
13. [Honest Assessment](#honest-assessment)
14. [Sources](#sources)

---

## Executive Summary

Analog compute-in-memory (CIM) promises 10-100x better energy efficiency than digital accelerators for AI inference by eliminating the memory-data movement bottleneck. As of early 2026, the landscape is:

- **Two credible analog CIM startups have launched commercial products**: EnCharge AI (capacitor/SRAM, EN100, 200 TOPS at 8.25W) and Mythic (flash-based, M1076, 25 TOPS at 3-4W). A third, Sagence AI, is expected to launch its first NOR-flash product imminently.
- **Digital in-memory computing is ahead in production**: Axelera AI (Metis, 214 TOPS in 12nm, digital IMC) is shipping and has announced its next-gen Europa chip (629 TOPS). MemryX ships the MX3 with a near-memory dataflow architecture.
- **IBM's HERMES chip** remains the most impressive academic/research CIM demonstration: 64 PCM-based analog cores, 16.1 TOPS, 14nm CMOS.
- **Peking University's RRAM chip** (Oct 2025, published in Nature Electronics) claimed 1000x speed advantage over GPUs for matrix equation solving --- but this is for a very specific workload, not general DNN inference.
- **The catch is always precision**: analog CIM typically achieves 4-bit effective precision. Going higher requires calibration, multi-phase reads, or hybrid digital correction, which eats into the efficiency advantage.
- **"Power, speed, or accuracy --- pick two"** remains the fundamental law of analog CIM (quote from Quadric co-founder, Semiconductor Engineering).
- **Most designers are not using CIM**: it "isn't even on the radar for most designers" per Semiconductor Engineering (2025).

The field is at an inflection point. EnCharge and Mythic's commercial launches in 2024-2025 will determine whether analog CIM achieves real market traction or returns to academia.

---

## Memory Technologies for CIM

Six memory technologies are being explored for CIM, each with distinct tradeoffs:

### SRAM-Based CIM
- **Maturity**: Highest. Uses existing foundry SRAM cells. TSMC, Samsung, and academic groups have demonstrated CIM macros.
- **Speed**: Fastest read/write (<1ns). Best throughput: 8.17 TOPS in benchmarks.
- **Weakness**: Volatile (loses weights on power-off), high leakage (5.65 mW), large cell size (6T cell). Not ideal for always-on edge.
- **Who uses it**: EnCharge AI (modified SRAM + capacitors), TSMC research macros, most ISSCC papers.
- **Key result**: TSMC/NTHU demonstrated 133.5 TFLOPS/W in 16nm with microscaling data format.

### Flash/NOR Flash-Based CIM
- **Maturity**: High. Flash is a mature manufacturing technology.
- **Advantage**: Non-volatile (weights persist without power), high density, low cost at scale.
- **Weakness**: Slow write/program times, limited endurance (~10K-100K cycles), aging/drift of stored analog values.
- **Who uses it**: Mythic (40nm embedded flash, M1076), Sagence AI (NOR flash in deep subthreshold), Anaflash (logic-compatible embedded flash).
- **Key result**: Mythic M1076 stores 80M weight parameters on-chip with zero external memory, achieving 25 TOPS at 3-4W.

### RRAM (ReRAM) / Memristor-Based CIM
- **Maturity**: Medium. TSMC, GlobalFoundries, and Samsung have fab processes, but consistency remains a challenge.
- **Advantage**: Non-volatile, very small cell (4F^2), multilevel capability (up to 11 bits demonstrated by TetraMem), low leakage (1.23 mW).
- **Weakness**: Read/write speed variability (1-100ns), device-to-device variation, endurance concerns, noise.
- **Who uses it**: TetraMem (RRAM-based SoC with RISC-V), Peking University (precision record), IBM (early research).
- **Key result**: Peking University's RRAM chip solved matrix equations 1000x faster than H100 GPU with 100x less energy --- but only for that specific workload. TetraMem claims 11-bit/device precision, highest among all memory types.

### Phase-Change Memory (PCM)
- **Maturity**: Medium. IBM is the primary driver, with 14nm CMOS + PCM integration demonstrated.
- **Advantage**: Non-volatile, multi-level storage, good density.
- **Weakness**: High write energy, resistance drift over time (analog values shift), thermal sensitivity.
- **Who uses it**: IBM (HERMES chip, 64 cores, 256x256 arrays, 16M+ devices).
- **Key result**: HERMES achieves 16.1-63.1 TOPS at 2.48-9.76 TOPS/W. MVM throughput per area (400 GOPS/mm^2) is 15x higher than prior multi-core AIMC chips. Effective precision: 3-4 bits per MVM.

### MRAM (STT-MRAM / SOT-MRAM)
- **Maturity**: Medium-high for standalone memory (Everspin mass-producing 64/128Mb in 2025), early for CIM.
- **Advantage**: Excellent endurance (>10^12 cycles), fast read/write, non-volatile, radiation-hard.
- **Weakness**: Binary storage (difficult for multilevel/analog), relatively large cell, high write current.
- **Who uses it**: Samsung (first MRAM-based in-memory computing demo), imec (SOT-MRAM research for CIM), Samsung foundry eMRAM at 14nm (mass production 2024, 8nm planned for 2026).
- **Key result**: Samsung demonstrated world's first MRAM-based in-memory computing. imec targets 10,000 TOPS/W with SOT-MRAM CIM.

### FeRAM / FeFET / Capacitive CIM
- **Maturity**: Early-to-medium. Emerging as a promising alternative.
- **Advantage**: Non-volatile, fast switching, low power, good endurance.
- **Weakness**: Scalability concerns, limited commercial availability.
- **Who uses it**: imec (FeFET research), academic groups. EnCharge AI's capacitor-based approach is related but uses standard CMOS capacitors rather than ferroelectric materials.
- **Key result**: Benchmarking shows FeCAP-based capacitive CIM crossbars deliver 31-48% lower total inference energy compared to RRAM and STT-MRAM arrays across VGG-8, ResNet-18, and ResNet-50.

---

## Companies with Actual Silicon

### EnCharge AI --- Capacitor-Based SRAM CIM
- **Founded**: 2022, spun out of Princeton University (Prof. Naveen Verma's lab)
- **Funding**: $144M+ total ($100M Series B in Feb 2025, oversubscribed). DARPA OPTIMA grant of $18.6M.
- **Product**: EN100 AI accelerator (announced May 2025)
  - M.2 form factor: >200 TOPS (INT8), 8.25W, 32GB LPDDR5 --- ~24 TOPS/W
  - PCIe form factor: ~1 PETAOPS (4 NPUs), 40W, 128GB LPDDR5, 272 Gbps bandwidth
  - Supports 4-bit and 8-bit analog precision; digital engines on-chip for higher precision / FP layers
  - Claimed 20x better perf/watt vs competing solutions; >40 TOPS/W efficiency
- **Technology insight**: Uses charge on capacitors (not current through resistors). SRAM cells control capacitors in metal layers. Output is a voltage signal, eliminating transimpedance amplifiers. Capacitors have very low temperature coefficients --- capacitance depends on geometry (wire spacing), which CMOS fabs control precisely. This is the key innovation that addresses the noise/drift problem of prior analog approaches.
- **Status**: First commercial product launched. Targeting laptops, workstations, edge devices.
- **The catch**: 4-8 bit precision. Needs digital fallback for FP layers. Real-world accuracy results on production models not yet independently verified.

### Mythic --- Flash-Based Analog Processing
- **Founded**: 2012 (originally Isee). Nearly died in Nov 2022 (ran out of cash).
- **Funding**: $125M Series B (Dec 2025, led by DCVC). Strategic investors include Honda and Lockheed Martin. New CEO Taner Ozcelik (ex-NVIDIA).
- **Product**: M1076 Analog Matrix Processor
  - 40nm embedded flash process
  - 76 AMP tiles, 80M weight parameters stored on-chip
  - 25 TOPS at 3-4W (best case ~8.33 TOPS/W)
  - No external memory required for model storage
- **Claimed efficiency**: 120 TOPS/W (current generation APUs) --- 100x more energy-efficient than GPUs.
- **Status**: Shipped first commercial products in late 2023 / early 2024. Targeting defense (primary), public safety, industrial, consumer. Dramatic comeback from near-death.
- **The catch**: The 120 TOPS/W claim likely refers to the raw MAC operation efficiency, not system-level. The 40nm process limits density. Flash endurance limits retraining. The near-death experience and pivot raises questions about long-term viability.

### Axelera AI --- Digital In-Memory Computing (Comparator)
- **Product**: Metis AIPU (12nm CMOS, digital IMC)
  - 214 TOPS (INT8), ~15 TOPS/W, quad-core
  - Available in M.2, PCIe, and 4-chip PCIe (856 TOPS) form factors
  - 1GB DRAM (M.2), up to 16GB (M.2 Max)
- **Next-gen**: Europa chip (2025 announcement, shipping H1 2026)
  - 629 TOPS (INT8), 8 AI cores, 2nd-gen D-IMC architecture
- **Why it matters**: Axelera chose *digital* IMC, avoiding analog precision issues. This is the clearest competitor showing that CIM benefits (reduced data movement) can be captured digitally.
- **The catch**: Digital IMC does not achieve the same raw MAC efficiency as analog. But it trades efficiency for deterministic accuracy and simpler programming model.

### MemryX --- Near-Memory Dataflow Architecture
- **Product**: MX3 AI Accelerator
  - Streaming, many-core, near-memory dataflow design
  - >20x better perf/watt than GPUs for targeted inference
  - 0.5-3W per chip, 9x9mm package
  - PCIe Gen3 + USB 3.1 interfaces
  - $149 for M.2 module (24 TOPS)
- **Next-gen**: MX4 announced (targeting data center scale, distributed asynchronous dataflow)
- **Status**: In production. Shipping MX3 silicon.

### IBM Research --- HERMES PCM Chip
- **Chip**: 64-core mixed-signal AIMC chip, 14nm CMOS + PCM back-end
  - 256x256 arrays per core, 4 PCM devices per unit cell, >16M devices total
  - 16.1-63.1 TOPS, 2.48-9.76 TOPS/W
  - 400 GOPS/mm^2 (15x better than prior AIMC chips)
  - 92.81% accuracy on CIFAR-10
  - Each core has a light digital processing unit for activations
- **Status**: Research chip, not commercial product. Published in Nature Electronics (2023). IBM continues PCM CIM research with LLM focus.
- **The catch**: 3-4 bit effective MVM precision. PCM resistance drift requires periodic re-calibration. Not on a path to commercial product as of 2026.

### Syntiant --- Mixed-Signal Edge AI (Production)
- **Products**:
  - NDP120/NDP200: Core 2 engine, <1mW, 6.4 GOPS. Production since ~2021.
  - NDP250: Core 3 engine, 30 GOPS, 5x improvement over previous gen. At-memory architecture.
  - Uses mix of analog and digital compute with embedded flash memory.
- **Status**: In production, shipping to customers. Used in earbuds, smart speakers, doorbells.
- **Next-gen**: On-device LLM chip planned for 2025 introduction.
- **The catch**: Very low-end of the performance spectrum (milliwatts, GOPS not TOPS). Targets always-on sensing, not serious DNN inference. Excellent in its niche but not competing with EnCharge/Mythic/Axelera.

### Aspinity --- Fully Analog ML
- **Product**: AML100 (analogML family)
  - Reconfigurable Analog Modular Processor (RAMP) platform
  - Operates entirely in the analog domain
  - Claims 95% reduction in always-on system power
- **Status**: In production for always-on wake/detect applications.
- **The catch**: Extremely limited model complexity. This is analog *signal processing* more than analog *compute*. Useful for wake-word detection and anomaly sensing, not DNN inference.

---

## Startups to Watch

### Sagence AI (formerly Analog Inference)
- **Technology**: NOR flash in deep subthreshold regime. Stores weights logarithmically to handle nonlinear math in subthreshold. Licensed standard flash cells.
- **Funding**: Backed by TDK Ventures and others.
- **Product**: First product (vision-focused) planned for 2025 launch.
- **Roadmap**: 3D-stacked analog chips linked via UCIe interposer. "Delphi" system claims 666K tokens/sec on Llama2-70B at 59kW (vs 624kW for H100 system) --- 10x power reduction at equivalent throughput.
- **The catch**: These are *simulation* numbers, not measured silicon. The 10x claim depends on successful 3D stacking, UCIe integration, and subthreshold analog precision holding up at scale. No silicon results published yet.

### TetraMem --- RRAM Analog CIM
- **Technology**: Multi-level RRAM with 11-bit/device precision (highest reported for any memory technology). RRAM memristors (Al2O3/HfO2 stack, Ta/Ti top electrode, Pt bottom).
- **Collaborations**: Andes Technology (RISC-V CPU integration), Synopsys (EDA/cloud), Samsung Foundry.
- **Product**: "Cullinan" analog-in-RRAM SoC. Initial designs at 22nm, roadmap to 7nm and below. Founding team demonstrated scalability to 2nm.
- **Status**: Development stage, working toward tape-out. CES 2025 showcase.
- **The catch**: RRAM device variability and endurance remain concerns. 11-bit precision is per-device; system-level effective precision after array parasitics and noise may be lower. No independently verified benchmark results.

### Anaflash --- Embedded Flash CIM
- **Technology**: Logic-compatible embedded flash (standard logic devices only). 4Mb of 4-bit/cell flash for weight storage. Zero-standby-power weight memory.
- **Process**: Samsung Foundry 28nm.
- **Product**: AI MCU for battery-powered edge devices. Sampling to partners/customers.
- **Collaboration**: Legato Logic (next-gen edge computing partnership, Feb 2025).
- **The catch**: Very small model capacity (4Mb). MCU-class, not accelerator-class.

### Blumind --- Analog Edge AI (Canada)
- **Focus**: Low-power analog AI for always-on wearables, smart home, industrial IoT.
- **Funding**: $14.1M raise for analog AI inference chips.
- **Product**: Keyword recognition chip scheduled for 2025 mass production.
- **The catch**: Very narrow application scope (keyword spotting). Similar niche to Syntiant/Aspinity.

### Rain AI / Rain Neuromorphics --- Memristor Training
- **Technology**: Analog memristor crossbar arrays. Claims orders of magnitude lower energy for DNN training (not just inference).
- **Achievement**: Demonstrated on-chip analog training --- a significant technical milestone.
- **Status**: Shipped initial chips Oct 2024 for IoT/wearable pilots.
- **CRITICAL**: $150M Series B round collapsed (Q1 2025). Company reportedly entering asset sale process (Q2 2025). Potential acquirers: OpenAI, NVIDIA, Microsoft circling for patents and talent.
- **The catch**: Financially dead or dying. Technology may survive via acquisition. Cautionary tale of how hard it is to commercialize analog AI.

---

## Dead or Dying

| Company | What Happened | Lesson |
|---------|---------------|--------|
| **Rain AI** | $150M round collapsed Q1 2025. Asset sale in progress. | Analog AI training is orders of magnitude harder than inference. Capital intensity kills. |
| **Mythic (2022)** | Ran out of cash Nov 2022. Revived with new CEO and $125M in Dec 2025. | Flash-based analog can work, but market timing and business execution matter as much as technology. |
| **Various unnamed** | Per Semiconductor Engineering: "some companies have pivoted to digital while others have outright abandoned the technology." | Analog CIM is a graveyard of good ideas that could not achieve manufacturing consistency. |

---

## Key Academic Groups

### Peking University (China)
- **Breakthrough**: RRAM chip solving matrix equations 1000x faster than Nvidia H100, 100x less energy. Published in Nature Electronics, Oct 2025.
- **Approach**: Two-circuit RRAM configuration --- one for fast approximate calculation, second for iterative refinement. Combines analog speed with digital-class accuracy.
- **Significance**: Manufactured on commercial production process (could be mass-produced). But the workload is matrix equation solving, not general DNN inference.

### Nanjing University (China)
- **Breakthrough**: Record-setting 0.101% RMSE for parallel vector-matrix multiplication --- highest precision ever for analog CIM. Published in Science Advances, 2025.
- **Approach**: Encodes weights through stable device geometry ratios rather than unstable physical parameters (resistance). Fabricated in standard CMOS.
- **Significance**: Addresses the fundamental precision problem of analog computing at the device physics level.

### Princeton University (USA)
- **Lab**: Prof. Naveen Verma's group.
- **Contribution**: Capacitor-based in-memory computing that became EnCharge AI. DARPA OPTIMA funding ($18.6M).
- **Approach**: Charge-domain computation using SRAM-controlled metal capacitors. Voltage-mode sensing eliminates TIA overhead.

### IBM Research + ETH Zurich
- **Contribution**: HERMES chip (64-core PCM), LLM-on-analog research, precision-optimized digital processing units for AIMC.
- **Recent work**: IBM/ETH demonstrated LLMs on analog hardware, MoE model attention acceleration, training algorithms for analog devices.

### imec + KU Leuven (Belgium)
- **Contribution**: Comprehensive benchmarking of analog vs digital SRAM CIM. IGZO-based DRAM for analog CIM research.
- **Key number**: imec's AnIA analog inference accelerator reached 2,900 TOPS/W for vector-matrix multiplications (2020). Research targeting 10,000 TOPS/W with SOT-MRAM and FeFET.
- **Significance**: Provides the most rigorous fair comparison between analog and digital CIM approaches.

### USC Viterbi (USA)
- **Contribution**: Chip design enabling arbitrarily high precision with analog memories. Related to TetraMem's founding team.

### Hokkaido University + TDK (Japan)
- **Contribution**: Analog reservoir AI chip for real-time learning. Won CEATEC 2025 Innovation Award.
- **Approach**: Reservoir computing mimicking cerebellum function. Short-term memory in analog circuits for time-series data.

### Northwestern University (USA)
- **Contribution**: Prof. Jie Gu received $3.8M DARPA ScAN program award (2025) for analog CIM research.

---

## ISSCC 2025 CIM Papers

Session 14: Compute-in-Memory was a dedicated session. Known papers:

| Paper | Title | Process | Key Metric |
|-------|-------|---------|------------|
| 14.4 | 51.6 TFLOPS/W Full-Datapath CIM Macro (sparsity-aware, compound AI) | - | 51.6 TFLOPS/W |
| 14.5 | 192.3 TFLOPS/W Accurate/Approximate Dual-Mode-Transpose Digital 6T-SRAM CIM Macro | 28nm | 192.3 TFLOPS/W, FP training+inference |
| 14.6 | 64kb Bit-Rotated Hybrid-CIM Macro with Sign-Bit-Processing | 28nm | Hybrid analog-digital |
| 14.7 | NeuroPilot: 69.4fJ/node, 0.22ns/node, 32x32 Mimetic-Path-Searching CIM Macro | 28nm | 69.4 fJ/node |

**Notable trend**: The top efficiency numbers (192.3 TFLOPS/W) are from *digital* SRAM CIM, not analog. This is significant --- digital CIM is catching up in efficiency while maintaining full precision. Papers increasingly focus on hybrid approaches.

**Also from TSMC research** (not ISSCC 2025 specifically):
- 16nm 216kb, 188.4 TOPS/W and 133.5 TFLOPS/W Microscaling Multi-Mode Gain-Cell CIM Macro
- 40nm RRAM CIM macro: 2.38 MCells/mm^2, 9.81-350 TOPS/W

---

## Performance Comparison Table

| Chip/Product | Type | Memory Tech | Process | TOPS | TOPS/W | Precision | Status |
|---|---|---|---|---|---|---|---|
| **EnCharge EN100** (M.2) | Analog CIM | SRAM+Capacitor | Undisclosed | 200 | ~24 | INT4/INT8 | Launched 2025 |
| **EnCharge EN100** (PCIe) | Analog CIM | SRAM+Capacitor | Undisclosed | ~1000 | ~25 | INT4/INT8 | Launched 2025 |
| **Mythic M1076** | Analog CIM | Embedded Flash | 40nm | 25 | ~8.3 | Analog ~4-8b | Shipping 2023-24 |
| **Sagence (sim)** | Analog CIM | NOR Flash | TBD | TBD | TBD (claims 10x H100) | TBD | Pre-silicon |
| **IBM HERMES** | Analog CIM | PCM | 14nm | 16-63 | 2.5-9.8 | 3-4b effective | Research |
| **Axelera Metis** | Digital IMC | SRAM (digital) | 12nm | 214 | ~15 | INT8 | Shipping |
| **Axelera Europa** | Digital IMC | SRAM (digital) | Undisclosed | 629 | TBD | INT8 | H1 2026 |
| **MemryX MX3** | Near-memory | SRAM | Undisclosed | 24 | >20x GPU | INT8 | Shipping |
| **Syntiant NDP250** | Mixed-signal | Flash | Undisclosed | 0.03 | Very high | INT8 | Shipping |
| **TetraMem Cullinan** | Analog CIM | RRAM | 22nm | TBD | TBD | Up to 11b/device | Development |
| **Anaflash MCU** | Analog CIM | Embedded Flash | 28nm | <1 | High | 4b weights | Sampling |
| **TDK Reservoir** | Analog | Magnetic analog | N/A | N/A | Ultra-low | Analog | Prototype |
| **imec AnIA** | Analog CIM | SRAM | Research | N/A | 2,900 TOPS/W (macro) | Research | Research |

*Note: TOPS/W numbers are not directly comparable across different precision levels, workloads, and measurement methodologies. Macro-level efficiency (imec) is always much higher than system-level (EnCharge, Mythic).*

---

## Fundamental Tradeoffs

### 1. Precision vs. Efficiency
- Analog CIM's core advantage is massively parallel multiply-accumulate (MAC) in the analog domain.
- Precision is limited by: device variation, noise, temperature drift, aging, ADC resolution.
- **Current wall: ~4 bits effective** for most analog approaches. EnCharge claims 8-bit with capacitor tech. TetraMem claims 11-bit per device (RRAM).
- Every additional bit of precision roughly doubles the ADC power and area.
- **The precision gap**: LLMs and transformers increasingly use INT4/INT8 quantization, which plays to analog's sweet spot. But some layers require FP16/FP32, forcing digital fallback.

### 2. Area vs. Performance
- SRAM CIM: Large cells (6T) but fast and compatible with standard fabs.
- RRAM CIM: Very dense (4F^2) but variable and less mature.
- Flash CIM: Mature fabs, high density, but slow writes and limited endurance.
- PCM CIM: Good density, but complex integration and drift issues.

### 3. Inference-Only vs. Training
- Nearly all commercial analog CIM is inference-only.
- On-chip analog training is an order of magnitude harder: requires bidirectional weight updates, precise gradients, and convergence under noise.
- Rain AI demonstrated analog training but is now financially collapsed.
- IBM and academic groups are exploring training, but it remains far from commercial viability.
- **Practical reality**: Models are trained digitally (GPU/TPU), then weights are loaded onto analog CIM for inference.

### 4. Analog vs. Digital CIM
Per imec/KU Leuven benchmarking:
- **Analog CIM**: Better energy efficiency for large macro sizes on convolutional and pointwise layers.
- **Digital CIM**: Better for depthwise layers with small macro sizes. Deterministic, no calibration needed.
- **Hybrid approaches are emerging**: Use analog for bulk MAC operations, digital for precision-critical paths.

### 5. Manufacturing Consistency
- "Manufacturing and environmental variations have proven extremely challenging and likely hurt past efforts" (Semiconductor Engineering).
- Flash: Analog value drift with aging and temperature cycling.
- RRAM: Device-to-device variation in switching characteristics.
- PCM: Resistance drift over time.
- SRAM+Capacitors (EnCharge approach): Capacitance depends on geometry only --- most resistant to variation. This is EnCharge's key differentiator.

---

## The Software Problem

The software stack is a critical and underappreciated challenge for analog CIM adoption:

- **No standard toolchain**: Each analog CIM chip requires its own compiler, mapper, and runtime. There is no CUDA equivalent for analog.
- **Weight mapping complexity**: Analog weights must account for device non-idealities, requiring hardware-aware quantization and calibration.
- **Noise-aware training**: Models may need to be re-trained or fine-tuned with hardware noise models to maintain accuracy on analog chips.
- **Hybrid execution**: When some layers run analog and others run digital, the compiler must handle partitioning, data format conversion (analog-to-digital boundaries), and scheduling.

**Company solutions**:
- **EnCharge**: Full software stack with compiler to map applications to hardware. SRAM-based weights can be reprogrammed quickly.
- **Mythic**: MAPP (Mythic AI Processing Platform) SDK supporting TensorFlow/PyTorch model porting. Includes compilers, optimizers, runtime.
- **Axelera** (digital): Voyager SDK with more conventional compilation flow.
- **IBM**: Open-sourced AIHWKIT (Analog AI Hardware Kit) for simulation and training with analog hardware models.

**The gap**: "Most compiler stacks are still optimized for NVIDIA's GPU dominance, making it hard to support emerging AI chips with equal depth." Full hardware democratization is not yet reality.

---

## CIM for LLMs and Transformers

This is the emerging frontier, driven by the massive energy cost of LLM inference:

### The Opportunity
- Attention mechanism's KV cache and softmax computations use ~70-80% of LLM inference energy in digital accelerators.
- Analog CIM could dramatically reduce this by computing dot products directly in memory.

### Recent Results
- **IBM/ETH Zurich**: Demonstrated AIMC for MoE (Mixture of Experts) LLMs. Noise-resilient rescaling for transformer attention layers. Published Jan 2025.
- **Research (Nature Computational Science, Sep 2025)**: Analog IMC attention mechanism using IGZO gain-cell crossbar arrays for KV cache. Claimed 70,000x energy reduction and 100x speedup vs GPUs for a 1.5B parameter model.
- **Sagence AI** (simulation): Claims Delphi system could run Llama2-70B at 666K tokens/sec at 59kW vs 624kW for H100 cluster.

### Reality Check
- These are prototype/simulation results, not production systems.
- LLMs require high precision for attention scores; analog noise directly degrades output quality.
- The analog advantage is strongest for the MAC-heavy linear projections, but softmax and layer norm still need digital computation.
- Commercial AIMC for LLMs remains in "prototype/trial stages, with no widespread adoption yet."

---

## Government and Institutional Funding

### DARPA OPTIMA Program
- "Optimum Processing Technology Inside Memory Arrays"
- Total: potentially $78M over 4.5 years
- Awards to: IBM, Infineon, Princeton ($18.5M), Georgia Tech ($9.1M), UCLA ($8M)
- EnCharge AI received $18.6M DARPA grant (linked to Princeton work)

### DARPA ScAN Program
- Northwestern University Prof. Jie Gu: $3.8M award (Nov 2025)

### Industry Investment
- Semiconductor startups raised $3B for AI chips in Q4 2025 alone (75 companies)
- Analog CIM market projected to grow from $251M (2025) to $2.45B by 2035 (25.6% CAGR)

---

## Honest Assessment

### Where Analog CIM Wins (Today)
1. **Ultra-low-power always-on sensing**: Syntiant, Aspinity dominate here. Milliwatt-scale keyword detection, anomaly sensing. This is real, shipping, profitable.
2. **Edge inference with constrained power**: EnCharge EN100 at 200 TOPS / 8.25W is competitive for on-device AI. If the precision holds up on real workloads, this is the strongest near-term case.
3. **Defense and specialized applications**: Mythic's pivot to defense makes sense --- defense tolerates higher unit costs and values power efficiency in field-deployed systems.

### Where Analog CIM Loses (Today)
1. **Data center inference**: Digital accelerators (NVIDIA, AMD, Google TPU, custom ASICs) are too far ahead in software ecosystem, scale, and proven reliability.
2. **Training**: Almost entirely a digital domain. Analog training remains academic.
3. **General-purpose flexibility**: Analog chips are optimized for specific operations (MAC). General-purpose workloads need digital.
4. **Complex models with mixed precision**: Any model requiring FP16+ precision for some layers forces hybrid execution, reducing analog's advantage.

### The Key Questions for 2026-2027
1. **Will EnCharge's EN100 achieve claimed accuracy on real customer workloads?** This is the single most important data point for the field.
2. **Can Sagence deliver on its simulation-based claims with actual silicon?**
3. **Will Axelera's digital IMC approach prove that you do not need analog to win the efficiency game?** If Europa (629 TOPS, digital) matches or exceeds analog efficiency in practice, it would undermine the analog thesis.
4. **Will any analog CIM chip run a full LLM with acceptable quality?** IBM's research points toward feasibility, but production is years away.
5. **Can the software ecosystem mature enough for analog CIM to be usable by mainstream developers?**

### The Verdict (as of March 2026)
Analog CIM has survived its "trough of disillusionment" and is entering a critical proof-of-concept phase. EnCharge AI and Mythic have real products. The technology works for inference at 4-8 bit precision. The energy efficiency advantage is real but narrower than marketing claims suggest when measured at the system level with realistic precision requirements.

The biggest threat to analog CIM is not that it does not work --- it does --- but that digital CIM and conventional digital accelerators are improving fast enough to close the efficiency gap while maintaining full precision and a mature software ecosystem. Axelera's Metis at 214 TOPS and 15 TOPS/W (digital, deterministic, INT8) vs EnCharge's EN100 at 200 TOPS and ~24 TOPS/W (analog, needs calibration, INT4/INT8) shows the gap is narrowing.

**The field will be decided by customers, not by papers.** The next 18 months of real-world deployment data from EnCharge, Mythic, and Sagence will determine whether analog CIM becomes a mainstream technology or remains a niche for ultra-low-power edge devices.

---

## Sources

### Industry Analysis
- [Is In-Memory Compute Still Alive? - Semiconductor Engineering](https://semiengineering.com/is-in-memory-compute-still-alive/)
- [Challenges For Compute-In-Memory Accelerators - Semiconductor Engineering](https://semiengineering.com/challenges-for-compute-in-memory-accelerators/)
- [Comparing Analog and Digital SRAM In-Memory Computing - KU Leuven/Semiconductor Engineering](https://semiengineering.com/comparing-analog-and-digital-sram-in-memory-computing-architectures-ku-leuven/)
- [Compute-In Memory Accelerators Up-End Network Design Tradeoffs - Semiconductor Engineering](https://semiengineering.com/more-data-less-movement/)

### Company Sources
- [EnCharge AI EN100 Announcement - BusinessWire](https://www.businesswire.com/news/home/20250529108055/en/EnCharge-AI-Announces-EN100-First-of-its-Kind-AI-Accelerator-for-On-Device-Computing)
- [EnCharge AI Technology Page](https://www.enchargeai.com/technology)
- [EnCharge Analog AI Chip - IEEE Spectrum](https://spectrum.ieee.org/analog-ai-chip-architecture)
- [EnCharge Picks The PC For Its First Analog AI Chip - EE Times](https://www.eetimes.com/encharge-picks-the-pc-for-its-first-analog-ai-chip/)
- [Mythic $125M Raise - Mythic](https://mythic.ai/whats-new/mythic-to-challenge-ais-gpu-pantheon-with-100x-energy-advantage-and-oversubscribed-125m-raise/)
- [Mythic M1076 Product Brief](https://mythic.ai/products/m1076-analog-matrix-processor/)
- [Mythic Revival - TechCrunch](https://techcrunch.com/2023/03/09/ai-chip-startup-mythic-rises-from-the-ashes-with-13m-new-ceo/)
- [Sagence AI - TechCrunch](https://techcrunch.com/2024/11/18/sagence-is-building-analog-chips-to-run-ai/)
- [Sagence AI - IEEE Spectrum](https://spectrum.ieee.org/analog-ai-2669898661)
- [TetraMem and Andes RISC-V Collaboration](https://tetramem.com/andes-technology-and-tetramem-collaborate-to-build-groundbreaking-ai-accelerator-chip-with-analog-in-memory-computing/)
- [TetraMem Cullinan SoC - EE News Europe](https://www.eenewseurope.com/en/tetramem-shows-off-cullinan-analog-in-reram-soc/)
- [Anaflash + Legato Logic - BusinessWire](https://www.businesswire.com/news/home/20250205794984/en/ANAFLASH-and-Legato-Logic-Unite-to-Drive-Next-Generation-Edge-Computing)
- [Anaflash Samsung Foundry Collaboration](https://finance.yahoo.com/news/anaflash-advances-embedded-flash-memory-180000104.html)
- [Axelera AI Metis Platform](https://axelera.ai/ai-accelerators/metis-m2-ai-acceleration-card)
- [MemryX MX3 Datasheet](https://developer.memryx.com/specs/mx3_datasheet.html)
- [Syntiant NDP250](https://www.syntiant.com/ndp250)
- [Aspinity AML100 - TechInsights](https://www.techinsights.com/blog/aspinity-tackles-analog-variability)

### Research Papers and Academic Sources
- [IBM HERMES 64-core PCM chip - Nature Electronics](https://www.nature.com/articles/s41928-023-01010-1)
- [Peking University RRAM chip - Nature Electronics (Oct 2025)](https://www.nature.com/articles/s41928-025-01477-0)
- [Nanjing University precision record - Science Advances (2025)](https://www.science.org/doi/10.1126/sciadv.ady4798)
- [Analog IMC Attention Mechanism for LLMs - Nature Computational Science (Sep 2025)](https://www.nature.com/articles/s43588-025-00854-1)
- [IBM MoE LLM on Analog - Nature Computational Science](https://www.nature.com/articles/s43588-024-00753-x)
- [Fast and Robust Analog In-Memory DNN Training - Nature Communications](https://www.nature.com/articles/s41467-024-51221-z)
- [Achieving High Precision in Analog IMC Systems - npj Unconventional Computing](https://www.nature.com/articles/s44335-025-00044-2)
- [Analog or Digital IMC? Benchmarking - arXiv/IEEE](https://arxiv.org/abs/2405.14978)
- [Review of SRAM-based CIM Circuits - arXiv](https://arxiv.org/html/2411.06079v2)
- [FeCAP Capacitive CIM Benchmarking - Wiley](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aidi.202500143)
- [Deep Learning Software Stacks for AIMC - Nature Reviews Electrical Engineering](https://www.nature.com/articles/s44287-025-00187-1)
- [Memory Is All You Need: CIM for LLMs - arXiv](https://arxiv.org/html/2406.08413v1)
- [Comparison of CIM with NVM Types - AIP Advances](https://pubs.aip.org/aip/adv/article/15/3/035317/3339501)

### Conference Sources
- [ISSCC 2025 Advance Program](https://submissions.mirasmart.com/ISSCC2025/PDF/ISSCC2025AdvanceProgram.pdf)
- [ISSCC 2025 Press Kit](https://static1.squarespace.com/static/6130ef779c7a2574bd4b8888/t/685ea4544cb9a51096997798/1751032932060/ISSCC_2025_Press_Kit_2_1_2025.pdf)
- [BUAA SRAM CIM Literature List - GitHub](https://github.com/BUAA-CI-LAB/Literatures-on-SRAM-based-CIM)

### Other Sources
- [TDK Analog Reservoir AI Chip](https://www.tdk.com/en/news_center/press/20251002_01.html)
- [Rain AI Status - EE Times](https://www.eetimes.com/rain-demonstrates-ai-training-on-analog-chip/)
- [DARPA OPTIMA - Breaking Defense](https://breakingdefense.com/2024/03/darpas-optima-program-seeks-ultra-efficient-ai-chips/)
- [DARPA Awards EnCharge/Princeton $18.6M - HPCwire](https://www.hpcwire.com/off-the-wire/darpa-awards-encharge-ai-and-princeton-18-6m-to-pioneer-next-gen-in-memory-ai-processors/)
- [Ceremorphic 5nm Tape-out](https://ceremorphic.com/ceremorphic-tapes-out-ai-supercomputing-chip-on-tsmc-5nm-node-featuring-circuit-technology-for-unrivaled-energy-efficiency-performance-and-reliability/)
- [Samsung MRAM-based In-Memory Computing Demo](https://news.samsung.com/global/samsung-demonstrates-the-worlds-first-mram-based-in-memory-computing)
- [GlobalFoundries RRAM Technology](https://marklapedus.substack.com/p/globalfoundries-rolls-out-rram-sige)
- [imec Machine Learning Accelerators](https://www.imec-int.com/en/expertise/cmos-advanced/compute/accelerators)
- [Chinese Research Team Breaks Precision Record - TrendForce](https://www.trendforce.com/news/2025/10/17/news-chinese-research-team-breaks-precision-record-with-new-analog-in-memory-computing-chip/)
- [Peking University RRAM 1000x claim - Live Science](https://www.livescience.com/technology/computing/china-solves-century-old-problem-with-new-analog-chip-that-is-1-000-times-faster-than-high-end-nvidia-gpus)
- [Neo Semiconductor 3D X-DRAM - TrendForce](https://www.trendforce.com/news/2025/05/09/news-new-generation-of-3d-x-dram-unveiled-aiming-to-boost-dram-bit-density-by-10x/)
- [Analog AI Chip Market Size - Precedence Research](https://www.precedenceresearch.com/analog-ai-chip-market)
