# EnCharge AI: Capacitor-Based Compute-in-Memory for AI Inference

## Executive Summary

EnCharge AI is the most technically credible analog compute-in-memory (CIM) startup as of mid-2026. Founded from Naveen Verma's Princeton lab, the company uses **capacitor-based charge-domain computation** inside SRAM arrays — a fundamentally different approach from the RRAM/Flash/PCM methods that have historically plagued analog CIM with drift, noise, and variability. Their EN100 chip (announced May 2025) claims 200+ TOPS at 8.25W in an M.2 form factor, with ~30 TOPS/mm² compute density — roughly 10x the area efficiency of conventional digital NPUs. The company has raised $144M+ (Series B led by Tiger Global, Feb 2025) and has DARPA backing through the OPTIMA program.

**The key claim**: 20x better performance-per-watt than leading digital AI accelerators, with no accuracy loss from analog noise.

**The key catch**: No independent benchmarks exist. No chips have shipped to customers yet. The EN100 "Early Access Program" is still in progress. The 150 TOPS/W figure from early interviews and the 40+ TOPS/W product spec have not been independently verified. SRAM-based weights are volatile, requiring reload from DRAM — a power cost that may erode the analog advantage.

---

## 1. How Capacitor-Based CIM Works

### 1.1 The Core Idea: Q = C × V

EnCharge's approach exploits the fundamental relationship between charge, capacitance, and voltage:

**Q = C × V** (charge = capacitance × voltage)

In a neural network MAC (multiply-accumulate) operation:
- **Weights** are stored as binary values in standard 6T SRAM cells
- **Metal-oxide-metal (MOM) capacitors** are fabricated in the metal interconnect layers *above* the SRAM cells, consuming no additional silicon area
- **Inputs** are applied as voltages to the capacitors
- **Multiplication** happens via Q = C × V: the input voltage (V) multiplied by the capacitance (C, controlled by the SRAM-stored weight) produces a charge (Q)
- **Accumulation** happens via charge conservation: charges from multiple multiplications share onto a common wire, and the resulting voltage represents the sum — the MAC result

### 1.2 Step-by-Step Circuit Operation

1. **Weight loading**: Binary weight bits are written into standard SRAM cells. Each SRAM cell controls a switch connected to a MOM capacitor.
2. **Charge phase**: All capacitors are pre-charged to a reference voltage.
3. **Multiplication**: Input data (up to 5-bit in the academic macro, 8-bit INT8 in the product) is applied as a voltage via a digital-switch DAC. The SRAM cell's stored weight bit gates the switch — if the weight is '1', the capacitor charges to a voltage proportional to the input; if '0', it doesn't.
4. **Accumulation**: The array switches into accumulation mode. All capacitors in a column share charge onto a common plate. By the law of charge conservation, the resulting voltage is proportional to the sum of all individual multiplications — this is the dot product.
5. **Digitization**: The accumulated voltage is read by a successive approximation register (SAR) ADC. Because the output is already a voltage (not a current), no transimpedance amplifier is needed — saving 3-4x the energy of the ADC itself.

### 1.3 Why This Is Different From Current-Domain CIM

Most analog CIM approaches (RRAM, Flash, PCM) work in the **current domain**:
- Weights are stored as conductance values in resistive memory elements
- Inputs are applied as voltages
- Ohm's law (I = G × V) produces current
- Currents from multiple cells sum on a shared wire (Kirchhoff's current law)
- The summed current must be converted to voltage via a transimpedance amplifier, then digitized

EnCharge's **charge-domain** approach avoids:
- The need for transimpedance amplifiers (major power/area savings)
- Current-mode noise (shot noise, thermal noise from resistive elements)
- Device-to-device variability (conductance in RRAM/PCM varies with filament formation, grain boundaries)

---

## 2. Why Capacitors Instead of RRAM/Flash/PCM?

This is the central architectural question, and EnCharge's answer is compelling at the physics level:

### 2.1 Capacitor Advantages

| Property | Capacitors (MOM) | RRAM | PCM | Flash |
|----------|------------------|------|-----|-------|
| **Temperature dependence** | Extremely low | High | High | Moderate |
| **Linearity** | Perfectly linear | Non-linear | Non-linear | Non-linear |
| **Variability** | Geometry-only (lithographic) | Filament-dependent (atomic-scale randomness) | Grain-dependent (random) | Threshold voltage drift |
| **Endurance** | Infinite (no wear) | Limited write cycles | Limited write cycles | Limited write cycles |
| **Precision control** | Determined by geometry (metal patterning) | Stochastic | Stochastic | Reasonable but drifts |
| **Output domain** | Voltage (direct ADC) | Current (needs TIA) | Current (needs TIA) | Current (needs TIA) |

As Verma puts it: "Capacitors don't vary with temperature, they don't have any material parameter dependencies, they are perfectly linear, and they only depend on geometry" — and geometry is what semiconductor manufacturing controls best.

### 2.2 Capacitor Disadvantages

| Issue | Impact |
|-------|--------|
| **Volatile storage** | Weights in SRAM must be reloaded from DRAM when the chip powers off or when switching model layers. RRAM/PCM/Flash store weights non-volatilely. |
| **SRAM cell size** | 6T SRAM cells are large (roughly 0.05-0.1 µm² at 16nm). This limits on-chip weight capacity vs. dense NVM like RRAM or Flash. |
| **Weight reloading overhead** | Because the SRAM array cannot hold an entire large model, weights must be tiled/virtualized from external DRAM. This data movement costs energy. |
| **Leakage power** | SRAM has static leakage current, especially at advanced nodes. NVM approaches can power-gate unused arrays. |
| **Multi-bit weights** | Each SRAM cell stores 1 bit. Multi-bit weights (e.g., INT8) require either multiple cells per weight or temporal accumulation across bit positions. |

### 2.3 The Fundamental Tradeoff

EnCharge trades **non-volatility and density** for **precision, reliability, and manufacturability**. This is a reasonable tradeoff for edge/client inference where:
- Power is available (laptop, workstation) — so SRAM leakage is tolerable
- Models change frequently — so volatile storage is acceptable
- Accuracy matters — so analog precision is critical
- Standard CMOS fabrication is needed — so no exotic materials required

It is a *worse* tradeoff for:
- Ultra-low-power always-on sensing (SRAM leakage dominates)
- Embedded devices with no DRAM (need NVM for weight storage)
- Very large models that exceed on-chip SRAM capacity by orders of magnitude

---

## 3. EN100 Chip Specifications

### 3.1 Product Specs (Announced May 29, 2025)

| Parameter | M.2 (Laptop) | PCIe (Workstation) |
|-----------|---------------|---------------------|
| **Peak compute** | 200+ TOPS (INT8) | ~1 POPS (INT8) |
| **Power envelope** | 8.25 W | ~40 W |
| **NPUs per card** | 1 | 4 |
| **Memory** | 32 GB LPDDR5 | 128 GB LPDDR5 |
| **Bandwidth** | Not disclosed | 272 GB/s |
| **Form factor** | M.2 2280 | PCIe add-in card |
| **Process node** | 16nm (TSMC) | 16nm (TSMC) |
| **Compute density** | ~30 TOPS/mm² | ~30 TOPS/mm² |
| **Precision** | INT8 primary | INT8 primary |

### 3.2 Key Performance Claims

- **~24 TOPS/W** (derived: 200 TOPS / 8.25W) for the M.2 form factor
- **~25 TOPS/W** (derived: 1000 TOPS / 40W) for the PCIe form factor
- **~20x better performance/watt** vs. "leading AI chips" (baseline not specified)
- **~30 TOPS/mm²** vs. ~3 TOPS/mm² for conventional digital NPUs (10x area advantage)
- **150 TOPS/W** claimed by Verma in early 2025 interview at 1W operating point (likely a single-macro peak efficiency, not system-level)

### 3.3 Supported Workloads

- Transformer/LLM inference (on-device chatbots)
- Computer vision (real-time object detection, classification)
- Image generation (diffusion models)
- Claims support for CNNs, transformers, and diffusion architectures
- Software stack supports PyTorch and TensorFlow through compiler toolchain

### 3.4 Availability

- Early Access Program Round 1: fully subscribed (as of May 2025)
- Early Access Program Round 2: opening for signups
- Production tapeout: scheduled for late 2025
- No confirmed volume shipping date as of March 2026

---

## 4. Academic Foundations

### 4.1 Key Papers from Verma Lab (Princeton)

**VLSI 2021**: "Fully Row/Column-Parallel In-memory Computing SRAM Macro employing Capacitor-based Mixed-signal Computation with 5-b Inputs"
- Authors: Lee, Valavi, Tang, Verma
- Process: 28nm
- Macro size: 1152 rows × 256 columns
- Energy efficiency: **5,796 TOPS/W** (normalized to 1-bit operations)
- Compute density: **12 TOPS/mm²** (normalized to 1-bit operations)
- Multi-level input via digital-switch DAC, preserving accuracy beyond 8-bit ADC resolution
- Dynamic-range doubling (DRD) technique halves ADC area
- CIFAR-10 accuracy: **91%** (equal to ideal software implementation)
- DOI: 10.23919/VLSICircuits52068.2021.9492444

**ISSCC 2021**: Additional CIM processor paper by Jia, Ozatay, Tang, Valavi, Pathak, Lee, Verma (details in Princeton publication archive).

**Earlier work (2017-2018)**: Zhang, Wang, Verma — foundational papers on in-memory computation of ML classifiers using charge-domain processing in SRAM.

### 4.2 Five Generations of Silicon

EnCharge claims "5 generations of designs across multiple process nodes and scaled-up architectures." The progression:
1. Early academic prototypes at Princeton (28nm process)
2. Scaled-up macros with multi-bit input support
3. Test chips with full system integration
4. Pre-production validation chips at TSMC 16nm
5. EN100 production design (16nm)

### 4.3 DARPA OPTIMA Program

- **$18.6M** awarded to Princeton + EnCharge AI (March 2024)
- Part of DARPA's $78M OPTIMA (Optimum Processing Technology Inside Memory Arrays) program
- Goal: develop next-generation switched-capacitor analog CIM chips
- Focus on end-to-end workload execution, not just macro-level demos

---

## 5. Company Profile

### 5.1 Founding and History

- **Founded**: 2022 (emerged from stealth December 2022)
- **Origin**: Naveen Verma's lab at Princeton University
- **~8 years of R&D** before product announcement (research since ~2017)

### 5.2 Founding Team

| Name | Role | Background |
|------|------|------------|
| **Naveen Verma, PhD** | CEO & Co-Founder | Princeton ECE professor since 2009; pioneered capacitor-based CIM |
| **Kailash Gopalakrishnan, PhD** | CTO & Co-Founder | Former IBM Fellow; 20+ years in AI hardware, led IBM's advanced AI HW/SW co-design |
| **Echere Iroaga, PhD** | COO & Co-Founder | 25+ years in semiconductor design; former VP/GM at MACOM; founded Renovus Inc. |

### 5.3 Key Technical Staff

- **Hossein Valavi** — Princeton lecturer; co-inventor of the core capacitor CIM technology (co-author on foundational papers)
- **Shwetank Kumar** — Chief Scientist
- **Yu-Hsin Chen** — Director, NPU Architecture
- **Sunil Shukla** — Senior Director, Chip Architectures & Platforms
- **Mayank Daga** — VP, Software Engineering

### 5.4 Advisory Board

Anantha Chandrakasan (MIT, dean of engineering), Andrea Goldsmith (Princeton, former IEEE president), Jim Plummer (Stanford, former dean of engineering), Sam Heidari, Donald Rosenberg, Richard Hegberg.

### 5.5 Funding

| Round | Date | Amount | Lead | Key Investors |
|-------|------|--------|------|---------------|
| Series A | Dec 2022 | $21.7M | AlleyCorp | Anzu Partners, Scout Ventures, Silicon Catalyst Angels |
| Series B | Feb 2025 | $100M+ | Tiger Global | In-Q-Tel (IQT), RTX Ventures, Samsung Ventures, HH-CTBC (Foxconn/CTBC), Maverick Silicon, Constellation Technology Ventures, Capital Ten, Vanderbilt University, Morgan Creek Digital |
| **DARPA OPTIMA** | Mar 2024 | $18.6M | Government | Princeton University collaboration |
| **Total raised** | — | **$144M+** | — | — |

Notable: In-Q-Tel (CIA venture arm), RTX Ventures (Raytheon), and Constellation Technology (defense) suggest DoD/intelligence interest. Samsung Ventures and Foxconn (via HH-CTBC) signal manufacturing ecosystem support.

---

## 6. Honest Assessment: The Catches

### 6.1 No Independent Benchmarks

The single biggest red flag. As of March 2026:
- No MLPerf results
- No third-party reviews of actual silicon
- No published inference benchmarks on standard models (ResNet, BERT, Llama, Stable Diffusion)
- The "20x better performance/watt" claim has no disclosed baseline or methodology
- The "150 TOPS/W" figure from early interviews is likely a macro-level peak number, not system-level

### 6.2 The TOPS/W Math Doesn't Add Up Cleanly

- **Macro-level claim**: 5,796 TOPS/W (1-bit normalized, academic paper)
- **Early interview claim**: 150 TOPS/W at 1W (presumably INT8, chip-level)
- **Product-level reality**: 200 TOPS / 8.25W = **~24 TOPS/W** (M.2 system)

The gap between 5,796 and 24 is the gap between a single macro doing 1-bit operations and a full system doing INT8 with DRAM, controllers, ADCs, I/O, and voltage regulators. This is a ~240x gap, which is large but not unreasonable — it includes:
- 8-bit vs 1-bit normalization (~64x)
- System overhead (DRAM, controllers, I/O, thermal): ~4x

Still, 24 TOPS/W at INT8 system-level would be genuinely excellent for a 16nm chip if real. For comparison:
- Apple M4 Neural Engine: ~18 TOPS at ~5W system = ~3.6 TOPS/W
- Qualcomm Hexagon NPU (Snapdragon 8 Gen 3): ~45 TOPS at ~15W = ~3 TOPS/W
- Intel Lunar Lake NPU: ~48 TOPS at unclear power
- NVIDIA Jetson Orin: 275 TOPS at 60W = ~4.6 TOPS/W

If EnCharge achieves 24 TOPS/W system-level at INT8, that would indeed be roughly 5-7x better than existing NPUs — not 20x, but still highly significant.

### 6.3 SRAM Volatility and Weight Reloading

This is the most fundamental architectural limitation:

- SRAM arrays cannot hold entire modern models (even a 7B parameter INT8 model = 7 GB of weights)
- The EN100 M.2 has 32 GB LPDDR5, so the model fits in DRAM but not in the SRAM compute array
- Weights must be **tiled**: loaded into SRAM, computed, then the next tile loaded
- This "virtual memory" approach for weights means DRAM bandwidth and energy become critical
- Every weight reload from DRAM costs energy that the analog CIM savings may not fully offset
- Verma acknowledges this: "weights cannot be stored permanently in the memory" due to utilization constraints

The key question: **does the energy saved by analog MAC inside SRAM exceed the energy cost of constantly shuffling weights from DRAM?** The answer likely depends on the model architecture:
- For models with high compute-to-parameter ratio (convolutions): yes, analog wins
- For models dominated by activation movement (attention layers): the advantage shrinks

### 6.4 Process Node Limitations

The EN100 is on **TSMC 16nm** — a 2016-era node. This has implications:
- SRAM cell size is larger than at 7nm or 5nm, limiting on-chip weight capacity
- SRAM leakage is higher than at more advanced nodes with better transistors
- The 30 TOPS/mm² claim at 16nm is impressive, but competitors on 5nm/4nm have more room for digital logic optimization
- Moving to advanced nodes should improve density, but SRAM scaling has slowed at sub-7nm

The choice of 16nm is likely pragmatic: lower NRE costs, proven SRAM libraries, faster time-to-market. It may also reflect the fact that the analog capacitor advantage is less node-dependent than digital scaling.

### 6.5 Software Ecosystem

- Claims PyTorch and TensorFlow support via compiler toolchain
- No public SDK, documentation, or developer tools visible as of March 2026
- No open-source compiler or model zoo
- The "purpose-built optimization tools" described in marketing materials have no public technical documentation
- Model quantization and mapping to the analog array is a non-trivial software challenge

### 6.6 Competitive Timing

The EN100 was announced May 2025 but has not shipped in volume. Meanwhile:
- Qualcomm, Intel, AMD, and Apple all ship NPUs in billions of devices
- NVIDIA Jetson dominates edge AI with proven software ecosystem (CUDA, TensorRT)
- The window for a new inference accelerator in the laptop/workstation market is narrowing as integrated NPUs improve

### 6.7 The "Analog Beats GPU" Claim Pattern

From the press: "the PCIe variant... delivering GPU-level compute capacity at a fraction of the cost and power consumption" and "at 4.5 watts, could match desktop GPUs with 1/100th the power draw."

This follows the familiar analog AI hype pattern:
- Compare peak TOPS of analog chip vs. total system power of GPU
- Ignore that the GPU runs FP16/FP32 while the analog chip runs INT8
- Ignore software ecosystem maturity
- Ignore that GPUs handle training + inference while analog is inference-only

### 6.8 Industry Skepticism

From SemiEngineering's 2025 CIM survey:
- Cadence's Frank Ferro: "I feel like we're not quite out of the research phase"
- Quadric's Nigel Drego: "We don't see it at our customers' sites"
- General consensus: "It's power, speed or accuracy with analog — pick two"

---

## 7. What Makes EnCharge Different (The Bull Case)

Despite the catches, EnCharge has several genuine advantages over prior analog CIM attempts:

### 7.1 Physics Advantage
Capacitors are genuinely better-behaved than resistive memory elements. The temperature independence, linearity, and geometry-only dependence are real physics — not marketing. This is the single strongest argument for EnCharge.

### 7.2 Standard CMOS Fabrication
MOM capacitors are formed in the metal interconnect layers already present in standard CMOS. No exotic materials (HfOx for RRAM, Ge-Sb-Te for PCM) or special process modules needed. Any foundry that makes SRAM can make this chip.

### 7.3 No Transimpedance Amplifier
The voltage-domain output eliminates a major source of power and area overhead in current-domain CIM. SAR ADCs are well-understood, low-power, and compact.

### 7.4 Reprogrammability
SRAM weights can be rewritten in nanoseconds (vs. microseconds-to-milliseconds for NVM). This enables rapid model switching and virtual-memory-style weight tiling that would be impractical with Flash or RRAM programming times.

### 7.5 Team Quality
Naveen Verma is a genuine expert (Princeton professor, published extensively, co-invented the technology). CTO Kailash Gopalakrishnan was an IBM Fellow — not a junior hire. The advisory board (Chandrakasan, Goldsmith, Plummer) is exceptional. This is not a team that will make elementary mistakes.

### 7.6 DARPA Validation
The $18.6M OPTIMA award is not trivial — DARPA technical program managers reviewed the technology. This is not proof of commercial viability, but it is evidence of technical credibility.

### 7.7 Demonstrated Silicon
Five generations of test chips, academic papers with real measured results (91% CIFAR-10 matching software, 5,796 TOPS/W at macro level). This is not PowerPoint engineering.

---

## 8. Competitive Positioning

### 8.1 vs. Other Analog CIM (Mythic, Sagence, TetraMem)

| | EnCharge | Mythic | Sagence | TetraMem |
|---|---------|--------|---------|----------|
| **Memory technology** | SRAM + capacitors | Flash | Flash (subthreshold) | RRAM (memristor) |
| **Compute domain** | Charge (voltage out) | Current | Current | Current |
| **Weight storage** | Volatile (SRAM) | Non-volatile (Flash) | Non-volatile (Flash) | Non-volatile (RRAM) |
| **Precision control** | Geometry-based (high) | Threshold voltage (moderate) | Logarithmic (novel) | Conductance (low) |
| **Temperature sensitivity** | Very low | Moderate | Low (subthreshold trick) | High |
| **Endurance** | Unlimited writes | Limited Flash cycles | Limited Flash cycles | Limited RRAM cycles |
| **Reprogramming speed** | Nanoseconds | Milliseconds | Milliseconds | Microseconds |
| **Process compatibility** | Standard CMOS | Standard Flash | Standard Flash | Requires RRAM module |
| **Peak claim** | 200 TOPS / 8.25W | 25 TOPS / ~3W (Gen1) | Research stage | Research stage |
| **Funding** | $144M+ | $300M+ | Undisclosed | $7.5M |
| **Status (Mar 2026)** | Early access program | Gen2 unverified | Pre-product | Pre-product |

### 8.2 vs. Digital NPUs

EnCharge's real competition is not other analog CIM startups — it's the NPUs already shipping in every laptop (Apple Neural Engine, Qualcomm Hexagon, Intel NPU). The EN100 must be:
- Dramatically more efficient (claimed 5-20x)
- Compatible with the same models (claimed PyTorch/TF support)
- Available in volume at competitive cost (unproven)
- Supported by a software ecosystem engineers will adopt (unproven)

The form factor strategy (M.2/PCIe add-in card) is smart — it avoids the impossible task of replacing integrated SoC NPUs and instead positions as a *supplemental* accelerator for workloads that exceed built-in NPU capability.

---

## 9. Key Technical Questions Still Unanswered

1. **How is multi-bit weight precision achieved?** Each SRAM cell stores 1 bit. For INT8 weights, how are 8 cells combined? Temporal accumulation across bit positions? Spatial: 8 SRAM cells per weight? This fundamentally affects density claims.

2. **What is the actual effective precision?** The macro achieves 8-bit ADC output, but what is the effective number of bits (ENOB) after analog noise? Does the system achieve true INT8 accuracy or something closer to INT6?

3. **What is the weight reload energy budget?** How much of the 8.25W goes to LPDDR5 access vs. compute? If DRAM dominates, the analog CIM advantage is eroded.

4. **How does attention work?** Transformer attention involves softmax, layer norm, and activation-to-activation matrix multiplies — not just weight-activation products. How does the analog array handle these?

5. **What happens with sparsity?** Modern models are increasingly sparse. Can the analog array exploit sparsity, or does it always compute dense MAC?

6. **What is the actual die area?** No die shot or area breakdown has been published.

7. **Floating-point support?** Verma has hinted at floating-point capability but disclosed no details. FP compute in an analog array would be a significant innovation if real.

---

## 10. Verdict

EnCharge AI is the most promising analog CIM startup for one reason: **they solved the right problem**. By choosing capacitors over resistive memory, they eliminated the noise, drift, and variability that have killed every previous analog CIM attempt. The physics is genuinely on their side.

But "most promising" is not "proven." The EN100 needs to:
1. Ship to customers (not just early access)
2. Publish independent benchmarks on real models (LLMs, vision transformers, diffusion)
3. Demonstrate the claimed 20x efficiency advantage at the system level, not just macro level
4. Build a usable software ecosystem

The 24 TOPS/W system-level efficiency (if real) at 16nm would be genuinely disruptive. The 30 TOPS/mm² compute density claim would make it the most area-efficient AI accelerator available. But until independent validation exists, these remain claims.

**Watch for**: First customer deployments, MLPerf submissions, independent teardowns, and the transition from early access to volume production. If EnCharge ships a working product in 2026 that delivers even 10x (not 20x) better TOPS/W than integrated NPUs, it would be the first commercially successful analog CIM chip — and a landmark moment for the field.

---

## Sources

- [EnCharge AI Technology Page](https://www.enchargeai.com/technology)
- [EnCharge AI About Us](https://www.enchargeai.com/about-us)
- [EN100 Product Page](https://en100.enchargeai.com)
- [EN100 Announcement — BusinessWire, May 2025](https://www.businesswire.com/news/home/20250529108055/en/EnCharge-AI-Announces-EN100-First-of-its-Kind-AI-Accelerator-for-On-Device-Computing)
- [EnCharge Picks The PC For Its First Analog AI Chip — EE Times](https://www.eetimes.com/encharge-picks-the-pc-for-its-first-analog-ai-chip/)
- [EnCharge's Analog AI Chip Promises Low-Power and Precision — IEEE Spectrum, June 2025](https://spectrum.ieee.org/analog-ai-chip-architecture)
- [EN100 Sets Stage for On-Device Inference — SiliconANGLE, May 2025](https://siliconangle.com/2025/05/29/encharges-en100-accelerator-chip-sets-stage-powerful-device-ai-inference/)
- [EnCharge raises $100M — TechCrunch, Feb 2025](https://techcrunch.com/2025/02/13/encharge-raises-100m-to-accelerate-ai-using-analog-chips/)
- [Startup gets $100M for low-power analog AI chips — The Register, Feb 2025](https://www.theregister.com/2025/02/17/encharge_ai_compute/)
- [EnCharge Series B announcement](https://www.enchargeai.com/news-and-publications/series-b)
- [DARPA-backed startup banks $100M — Fast Company](https://www.fastcompany.com/91278505/encharge-ai-banks-100-million-for-its-energy-slashing-analog-chips)
- [CEO Interview: Charge-based in-memory compute — EE News Europe](https://www.eenewseurope.com/en/ceo-interview-charge-based-in-memory-compute-at-encharge-ai/)
- [EnCharge AI reimagines computing — Princeton Engineering, Jan 2023](https://engineering.princeton.edu/news/2023/01/27/encharge-ai-reimagines-computing-meet-needs-cutting-edge-ai)
- [DARPA awards $18.6M to EnCharge/Princeton — HPCwire, Mar 2024](https://www.hpcwire.com/off-the-wire/darpa-awards-encharge-ai-and-princeton-18-6m-to-pioneer-next-gen-in-memory-ai-processors/)
- [Princeton news on DARPA-funded chip, Mar 2024](https://www.princeton.edu/news/2024/03/06/new-chip-built-ai-workloads-attracts-18m-government-funding-revolutionary-tech)
- [Is In-Memory Compute Still Alive? — SemiEngineering](https://semiengineering.com/is-in-memory-compute-still-alive/)
- [VLSI 2021 Paper: Lee, Valavi, Tang, Verma — Princeton](https://collaborate.princeton.edu/en/publications/fully-rowcolumn-parallel-in-memory-computing-sram-macro-employing-2)
- [ISSCC 2021: Jia, Ozatay, Tang, Valavi, Pathak, Lee, Verma](https://www.princeton.edu/~nverma/VermaLabSite/Publications/2021/JiaOzatayTangValaviPathakLeeVerma_ISSCC2021Proof.pdf)
- [Verma Lab Publications — Princeton](https://nverma.princeton.edu/group-publications)
- [EnCharge AI emerges from stealth — TechCrunch, Dec 2022](https://techcrunch.com/2022/12/14/encharge-ai-emerges-from-stealth-with-21-7m-to-develop-ai-accelerator-hardware/)
- [PCIe cards tap analog in-memory compute — EE News Europe](https://www.eenewseurope.com/en/pcie-cards-tap-analog-in-memory-compute-for-low-power-ai-inference/)
- [EnCharge AI — DataCenterDynamics](https://www.datacenterdynamics.com/en/news/encharge-ai-launches-its-analog-in-memory-en100-ai-accelerator/)
- [EnCharge AI — Anzu Partners](https://www.anzupartners.com/2025/05/29/encharge-ai-announces-en100-first-of-its-kind-ai-accelerator-for-on-device-computing/)
- [CAP-RAM: Charge-Domain CIM 6T-SRAM — arXiv 2107.02388](https://arxiv.org/pdf/2107.02388)
- [Princeton team wins Edison Patent Award](https://ece.princeton.edu/news/princeton-team-invented-advanced-ai-chip-wins-edison-patent-award)
