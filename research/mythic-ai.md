# Mythic AI: Analog Compute-in-Memory for AI Inference

*Research compiled: 2026-03-22*

---

## Executive Summary

Mythic is the most prominent startup attempting to commercialize analog compute-in-memory (CIM) for AI inference. Founded in 2012 as a University of Michigan spinout, Mythic nearly died in late 2022 when it ran out of cash before reaching revenue. It was rescued in 2023 with $13M, appointed an ex-NVIDIA executive as CEO in 2024, and in December 2025 raised $125M in an oversubscribed round backed by DCVC, SoftBank, Honda, and Lockheed Martin. The company claims 120 TOPS/W and 100x better energy efficiency than GPUs. Those claims deserve careful scrutiny.

---

## 1. Company History and Status

### Founding (2012)

- **Founded**: 2012 as **Isocline**, renamed to **Mythic** in 2017.
- **Founders**: Mike Henry (Virginia Tech) and Dave Fick (University of Michigan Integrated Circuits Lab).
- **Key early engineers**: Laura Fick (Ph.D. thesis was foundational technology for analog compute on flash arrays at high precision), Skylar Skrzyniarz (analog compute modeling), Malav Parikh (first industry-experienced chip engineer).
- **Core thesis**: The Von Neumann bottleneck (moving data between memory and compute) wastes 90%+ of energy in AI inference. If you store weights in flash and compute *in place* using Ohm's Law, you eliminate that bottleneck entirely.

### Funding History

| Round | Date | Amount | Lead / Key Investors |
|-------|------|--------|---------------------|
| Debt | Nov 2016 | $5.7M | - |
| Series A | Mar 2017 | $9M | DFJ |
| Series B | Mar 2018 | $40M | SoftBank Vision Fund, Lockheed Martin Ventures, Andy Bechtolsheim |
| Series B-1 | Jun 2019 | $30M | Valor Equity Partners |
| Series C | May 2021 | $70M | BlackRock, Hewlett Packard Enterprise |
| Rescue round | Mar 2023 | $13M | Atreides, DCVC, Lux Capital, Catapult Ventures |
| Latest | Dec 2025 | $125M | DCVC (lead), NEA, SoftBank KR, Honda, Lockheed Martin |

**Total raised**: ~$300M+ (PitchBook reports $302M).

### The 2022 Collapse

In November 2022, Mythic ran out of cash. VP of Engineering Ty Garibay stated publicly: *"We ran out of runway with the investors before we could get to revenue."* The company had burned through $165M+ over 10 years without achieving commercial revenue. Global VC for semiconductor startups declined 46% in 2022, and Mythic could not close its next round. CEO Mike Henry left. The company underwent radical restructuring and downsizing.

**What went wrong**:
- Spent a decade in development before shipping product.
- The M1108 (35 TOPS, 4W) was sampling in 2020 but never achieved volume commercial traction.
- Edge AI market was dominated by NVIDIA Jetson and Qualcomm, with established software ecosystems.
- Mythic's software stack (compiler, SDK) was immature relative to CUDA.
- The AI market shifted dramatically toward large language models and data center inference, not the edge vision workloads Mythic had designed for.

Sources: [The Register](https://www.theregister.com/2022/11/09/mythic_analog_ai_chips/), [TechCrunch](https://techcrunch.com/2023/03/09/ai-chip-startup-mythic-rises-from-the-ashes-with-13m-new-ceo/), [EE Times](https://www.eetimes.com/european-vcs-rescue-mythic-fick-becomes-ceo/)

### The Comeback (2023-2026)

- **Mar 2023**: $13M rescue funding. Dave Fick (co-founder, previously CTO) became CEO.
- **Jun 2024**: Dr. Taner Ozcelik named CEO. Ozcelik founded NVIDIA's automotive division, holds a Ph.D. from Northwestern and MBA from Wharton. Fick presumably returned to a technical role.
- **Dec 2025**: $125M oversubscribed round. Company pivoted messaging from "edge AI" to also encompassing data center LLM inference and automotive SoCs.
- **Feb 2026**: Joint development agreement with Honda for automotive-grade analog AI SoC for next-gen software-defined vehicles (target: late 2020s/early 2030s).
- **Mar 2026**: Partnership with Microchip/SST to use memBrain neuromorphic flash IP for next-gen APUs.

**Current status (March 2026)**: Operating, well-funded, actively hiring, with DoD and automotive OEM customers. Revenue reportedly ~$6.4M in 2025 with 58 employees (per Latka).

Sources: [Mythic PR Dec 2025](https://mythic.ai/whats-new/mythic-to-challenge-ais-gpu-pantheon-with-100x-energy-advantage-and-oversubscribed-125m-raise/), [Bloomberg](https://www.bloomberg.com/news/articles/2025-12-17/ai-chip-startup-mythic-raises-125-million-in-bid-to-take-on-nvidia), [Honda PR](https://mythic.ai/whats-new/honda-and-mythic-announce-joint-development-of-100x-energy-efficient-analog-ai-chip-for-next-generation-vehicles/)

---

## 2. Architecture: How Flash-Based Analog CIM Works

### The Core Idea

In a conventional digital accelerator, a multiply-accumulate (MAC) operation requires:
1. Reading weight from memory (SRAM or DRAM) -- this is the expensive part, ~10-100x more energy than the multiply itself.
2. Moving the weight to the ALU.
3. Performing the multiply in digital logic.
4. Accumulating the result.

Mythic's insight: if you store the weight as the *conductance* of a flash transistor, and apply the input as a *voltage*, then by Ohm's Law the resulting *current* is the product (I = V x G). Sum the currents on a column wire and you get a dot product -- for free, in physics, without ever "reading" the weight.

### Flash Cell as Analog Weight

- Each flash cell has a **floating gate** that traps electrons.
- The number of trapped electrons controls the cell's **threshold voltage**, which in turn controls its **conductance** (G = 1/R) when a gate voltage is applied.
- Mythic programs each cell to one of **256 conductance levels**, representing an **8-bit weight value**.
- This is the same basic NOR flash cell used in billions of shipped flash chips, but operated in the analog domain rather than as a binary 0/1 store.
- Non-volatile: weights are retained when power is removed (zero standby power for the weight memory).

### The Matrix Multiply Operation

1. **Input conversion**: Digital input activations are converted to analog voltages via **8-bit DACs** (one per row of the flash array).
2. **Analog multiply**: Each voltage is applied across its row. Each flash cell in that row produces a current proportional to V_input x G_weight.
3. **Analog accumulate**: Currents from all cells in a column sum on the bitline wire (Kirchhoff's Current Law). This is the dot product of the input vector with the weight column.
4. **Output conversion**: The summed currents are digitized back by **ADCs** (one per column) to produce digital partial sums.
5. **Digital post-processing**: Activation functions, batch normalization, pooling, and other non-linear operations are performed in a digital SIMD engine.

### Tile Architecture

Each Mythic chip is composed of multiple identical **tiles**. Each tile contains:

| Component | Function |
|-----------|----------|
| **Mythic ACE** (Analog Compute Engine) | Flash array + ADCs for analog matrix multiply |
| **SRAM** | Local storage for intermediate activations and program data |
| **SIMD vector engine** | Digital operations: MaxPool, ReLU, batch norm, etc. |
| **32-bit RISC-V nano-processor** | Per-tile control, sequencing, and dataflow management |
| **NoC router** | Network-on-Chip connects tiles for inter-tile data movement |

This is a **dataflow architecture**: each tile processes one or more layers (or partial layers) of the neural network, and data flows tile-to-tile across the NoC. The RISC-V core per tile provides flexible programmability.

### Product Specifications

**M1108 (First-gen flagship, Nov 2020)**:
- 108 tiles
- Up to 35 TOPS (INT8)
- ~4W typical power at peak throughput
- ~8.75 TOPS/W
- PCIe 2.0 interface
- 40nm process
- No external DRAM required

**M1076 (Smaller variant, 2021)**:
- 76 tiles
- Up to 25 TOPS (INT8)
- ~3W typical power
- ~8.3 TOPS/W
- 80M weight parameters on-chip
- 19mm x 15.5mm die
- 40nm process
- Supports INT4, INT8, INT16
- Available as bare die, M.2 card, or PCIe card (up to 16 AMPs per card = 400 TOPS)

**Demonstrated workloads on Gen 1**:
- YOLOv5 object detection at 60 fps on high-resolution video, consuming 3.5W
- ResNet-50, YOLOv3, OpenPose Body25

### Next-Generation Architecture (Gen 2)

- **Process**: 28nm (still mature node, now using SST/Microchip memBrain flash IP)
- **Chiplet-based**: Modular architecture scaling from 1 chiplet to 1,024 chiplets
- **Single chiplet**: ~120 TOPS (INT8), <1W
- **Claimed efficiency**: 120 TOPS/W
- **Target configurations**: 1 chiplet (edge vision), 4-16 chiplets (robotics/automotive), up to 1,024 chiplets (data center LLM inference)
- **Software**: CAMP SDK supporting ONNX, PyTorch, TensorFlow, NVIDIA TensorRT

Sources: [Mythic Technology Page](https://mythic.ai/technology/), [Mythic Products](https://mythic.ai/product/), [Next Platform](https://www.nextplatform.com/2018/08/23/a-mythic-approach-to-deep-learning-inference/), [EE Journal](https://www.eejournal.com/article/meet-mythic-ais-soon-to-be-legendary-analog-ai/), [SST memBrain PR](https://www.globenewswire.com/news-release/2026/03/17/3257057/0/en/Mythic-Selects-memBrain-Technology-from-Silicon-Storage-Technology-for-its-Next-Generation-of-Ultra-Low-Power-Analog-Processing-Units.html)

---

## 3. Performance Claims -- and the Catches

### Headline Claims (Dec 2025 press release)

| Claim | Number | Comparison Basis |
|-------|--------|-----------------|
| Energy efficiency | 120 TOPS/W | "100x better than top GPUs including memory transfers" |
| MAC energy | 17 femtojoules/MAC | "1,000x less than GPUs" |
| LLM throughput | 750x more tokens/s/W | "vs NVIDIA's highest-end GPUs for 1T parameter LLMs" |
| Cost per token | 80x lower | "as low as $0.005/M tokens for 100B LLMs" |

### Catch #1: TOPS/W Definition Games

The 120 TOPS/W number for the Gen 2 chiplet at <1W is extraordinary. For comparison:
- NVIDIA Jetson Orin (digital, 5nm): ~5-10 TOPS/W
- Qualcomm Hexagon NPU: ~10-15 TOPS/W
- Google TPU v5e: ~2-5 TOPS/W (at scale)

**But**: Mythic counts only the analog MAC operation energy (17 fJ/MAC). The total system power includes:
- DAC conversion on inputs
- ADC conversion on outputs
- Digital SIMD processing for non-MAC operations
- RISC-V control logic
- Network-on-Chip routing
- PCIe interface
- Board-level power delivery

In academic literature, **ADCs and DACs account for up to 85% of total power** in analog CIM systems. If the analog MAC itself is 17 fJ but the ADC/DAC overhead adds 10-50x, the system-level efficiency is very different from 120 TOPS/W.

**The Gen 1 chips tell the real story**: The M1108 delivered 35 TOPS at 4W = **8.75 TOPS/W system-level**. The M1076 delivered 25 TOPS at 3W = **8.3 TOPS/W system-level**. These are good numbers for 40nm edge chips, but they are not 100x better than GPUs. They are comparable to or slightly better than NVIDIA Jetson Xavier (built on a much more advanced 12nm process).

The Gen 2 claim of 120 TOPS at <1W for a single chiplet remains unverified by independent benchmarks. Moving from 40nm to 28nm and improving the analog array design could yield improvements, but a jump from ~8 TOPS/W to 120 TOPS/W (14x improvement) within one generation needs careful independent validation.

### Catch #2: The 750x LLM Claim

The claim of "750x more tokens per second per watt" for 1T parameter LLMs vs NVIDIA GPUs is described as from "internal benchmarks." Key questions:

- **What GPU baseline?** An A100? H100? B200? At what batch size? What precision?
- **Is this a projection or silicon measurement?** The Gen 2 chiplet is not yet shipping.
- **How are 1T parameters distributed across chiplets?** LLM inference requires not just MACs but attention computation, KV cache management, and high-bandwidth inter-chip communication. NVIDIA uses NVLink (900 GB/s on Blackwell). How do Mythic chiplets communicate?
- **What precision?** Analog at ~8-bit effective precision may or may not match the accuracy of FP8/INT8 on GPUs.

Without independent benchmarks (MLPerf or equivalent), the 750x claim should be treated as a marketing number from a pre-production architecture.

### Catch #3: Precision and Accuracy

Analog compute inherently operates with limited precision:

- **Noise**: Thermal noise, shot noise, and flicker noise in the flash cells and sense circuits corrupt analog signals.
- **Drift**: Flash cell conductance can drift over time as charge leaks from floating gates. Temperature changes alter cell behavior.
- **Variation**: Manufacturing process variation means nominally identical cells have different characteristics.
- **ADC quantization**: The ADC converting the analog sum back to digital introduces additional quantization error.

Mythic addresses these with:
- Internal calibration circuits (analog and digital) that periodically measure array outputs against expected values.
- Ability to "refresh" weights from off-chip digital values.
- Neural networks' inherent tolerance to noise (a key enabler -- NNs work even when individual weights deviate significantly from trained values).

**The real question**: What is the *effective* precision of the system after noise, drift, and calibration? Mythic claims 8-bit, but the effective number of bits (ENOB) under real operating conditions (temperature range, after months of deployment) may be closer to 5-6 bits. Research shows analog CIM chips operating between 10C and 60C can maintain classification accuracy within 2% of software baselines, but this is for simple CNNs, not for the nuanced accuracy requirements of LLMs.

### Catch #4: Software Ecosystem

Even if the hardware delivers, the software ecosystem is critical:
- Mythic's CAMP SDK supports ONNX, PyTorch, TensorFlow.
- The compiler must quantize floating-point models to INT8, simulate analog noise during quantization-aware training, and map layers efficiently across tiles.
- This is a proprietary, Mythic-only toolchain. No equivalent of CUDA's massive ecosystem.
- Developers must retrain or fine-tune models for analog noise characteristics.
- The number of validated, production-ready models on Mythic hardware is likely very small compared to what runs on NVIDIA or Qualcomm.

### Catch #5: Why 40nm/28nm?

Mythic uses mature process nodes (40nm for Gen 1, 28nm for Gen 2) because:
- Analog circuits do not benefit from transistor scaling the way digital logic does.
- Embedded flash (NOR) is not available on leading-edge nodes (7nm, 5nm, 3nm) -- the flash floating gate does not scale well.
- Mature nodes are cheaper per wafer.

**The downside**: Digital competitors on 5nm/3nm have vastly higher transistor density and clock speeds. NVIDIA's Blackwell on TSMC 4nm integrates orders of magnitude more digital logic per mm^2. Mythic's advantage has to come entirely from the architectural benefit of in-memory compute, because it cannot compete on raw transistor technology.

Sources: [Mythic Dec 2025 PR](https://mythic.ai/whats-new/mythic-to-challenge-ais-gpu-pantheon-with-100x-energy-advantage-and-oversubscribed-125m-raise/), [QuantumZeitgeist](https://quantumzeitgeist.com/mythic-ai-computing-ai-efficiency/), [SiliconANGLE](https://siliconangle.com/2025/12/17/compute-memory-chip-startup-mythic-raises-125m-round/)

---

## 4. Circuit-Level Innovations

### NOR Flash as Analog Synapse

Traditional NOR flash stores 1 bit: the cell is either programmed (electrons on floating gate, high threshold voltage, low/no current) or erased (no electrons, low threshold, current flows). Mythic instead programs the cell to an intermediate state -- a precise number of electrons that sets the conductance to one of 256 levels.

**Programming**: Uses incremental step pulse programming (ISPP) or similar techniques to iteratively add electrons until the target conductance is reached. This is slower than binary programming but achievable with standard flash programming circuits.

**Read (compute)**: Instead of sensing whether the cell conducts or not, Mythic biases the cell in its linear region and measures the *magnitude* of current. The cell acts as a voltage-controlled current source where the "control" is the stored weight.

### Matrix Multiply Without Reading Memory

This is the fundamental innovation. In a conventional system:
```
Energy_total = Energy_read_weight + Energy_multiply + Energy_accumulate
```
Where Energy_read_weight >> Energy_multiply.

In Mythic's system:
```
Energy_total = Energy_DAC + Energy_analog_MAC + Energy_ADC
```
There is no "read" step -- the weight participates directly in computation as a physical property (conductance) of the storage element.

### Power Management Innovation

Mythic published details on an evolution in power management for the M1076:
- Non-volatile flash means zero standby power for the weight memory.
- Power can be fully removed and restored; computation resumes instantly (no weight reloading from DRAM).
- Dynamic power gating of tiles not currently in use.
- This is a significant advantage for always-on edge deployment where average utilization is low.

### Calibration Architecture

Mythic incorporates both analog and digital calibration:
- **Periodic calibration**: Reference measurements against known values to detect and compensate for drift.
- **Temperature compensation**: Circuits to counteract temperature-dependent conductance changes.
- **Digital error correction**: Post-ADC digital correction to compensate for systematic analog errors.

The calibration overhead is a cost: it consumes silicon area, power, and time. But it is essential for maintaining accuracy over the chip's lifetime.

Sources: [Next Platform Hot Chips Analysis](https://www.nextplatform.com/2018/08/23/a-mythic-approach-to-deep-learning-inference/), [EE Journal](https://www.eejournal.com/article/meet-mythic-ais-soon-to-be-legendary-analog-ai/), [All About Circuits](https://www.allaboutcircuits.com/news/mythic-ai-redefines-edge-ai-by-combining-analog-processing-and-flash-memory/)

---

## 5. Comparison to Digital Alternatives

### Mythic M1076 (Gen 1) vs. NVIDIA Jetson Orin

| Metric | Mythic M1076 | Jetson Orin NX |
|--------|-------------|----------------|
| Process | 40nm | 5nm (Samsung) |
| TOPS (INT8) | 25 | 100 |
| Power | 3W | 10-25W |
| TOPS/W | ~8.3 | 4-10 |
| On-chip weights | 80M (no DRAM needed) | Requires LPDDR5 |
| Software ecosystem | Mythic CAMP SDK | CUDA, TensorRT, massive ecosystem |
| Supported models | CNNs, limited RNNs | Full range: CNNs, transformers, LLMs |
| Price | Not publicly listed | ~$400-600 |

**Verdict on Gen 1**: Mythic's TOPS/W advantage on Gen 1 hardware is modest (roughly 2x better than Jetson at system level), not the claimed 100x. The advantage is real but narrow, and the software ecosystem gap is enormous.

### Mythic Gen 2 (Projected) vs. Digital Edge Chips

If Mythic's Gen 2 truly delivers 120 TOPS at <1W per chiplet, that would be a paradigm shift. But this needs to be validated with:
1. Independent power measurement at the system level (not just the analog MAC).
2. Accuracy benchmarks on standardized models (MLPerf).
3. Real workload demonstrations (not just peak TOPS at synthetic throughput).

### The ADC/DAC Problem

This is the core challenge for all analog CIM. Academic research consistently finds:
- **ADC/DAC power = 40-85% of total CIM system power**, depending on resolution and speed.
- Higher precision ADCs (needed for accuracy) consume exponentially more power.
- This is why Mythic's per-MAC energy (17 fJ) and system-level energy (implied by 3W at 25 TOPS = 120 fJ/MAC for M1076) differ by ~7x.

The gap between "analog MAC energy" and "system energy" is the key number to watch. A 7x overhead is actually quite good for analog CIM -- some academic implementations see 20-50x overhead from peripherals. But it means the "1000x better than GPU" claim for the bare MAC operation does not translate to a 1000x system-level advantage.

---

## 6. What Engineers and Practitioners Say

### Positive Views

- The core physics argument is sound: computing in memory eliminates the dominant energy cost (data movement) of AI inference.
- Flash is a proven, reliable, high-endurance technology with decades of manufacturing experience.
- The non-volatile nature means zero standby power and instant resume -- genuinely valuable for edge/IoT.
- Neural networks' noise tolerance makes analog a uniquely good fit for AI, as opposed to general-purpose computing where analog failed.

### Critical Views

- **Bill Dally (NVIDIA Chief Scientist)** and others have argued that ADC/DAC conversion overhead will consume most of the power efficiency gains from analog compute.
- Hacker News commenters (including some who appear to have semiconductor industry experience) noted concerns about: wear and repeatability of flash cells, detection of degradation happening multiple layers deep, and whether production-quality models actually work well enough.
- The 2022 collapse demonstrated that technical innovation alone is insufficient without revenue, customers, and a software ecosystem.
- Multiple commenters expressed interest in seeing the technology prove itself in actual production deployments with transparent benchmarks, not press releases.

### The Honest Assessment

Mythic's technology addresses a real problem (memory wall / data movement energy dominance in AI). The physics works. The first-generation products were real, working silicon. But:

1. The efficiency advantage at the system level (Gen 1) was ~2-3x vs. digital, not 100x.
2. The software ecosystem remains a massive barrier to adoption.
3. Scaling to LLMs and data center workloads requires solving inter-chiplet communication, KV cache management, attention computation, and many other problems that are not addressed by analog MAC efficiency.
4. The Gen 2 claims (120 TOPS/W, 750x LLM throughput/W) are unverified projections.
5. The company has $300M+ of investor capital and ~$6M in revenue after 14 years.

Sources: [Hacker News discussion](https://news.ycombinator.com/item?id=35382513), [Hacker News M1000 thread](https://news.ycombinator.com/item?id=28368483), [The Register](https://www.theregister.com/2022/11/09/mythic_analog_ai_chips/)

---

## 7. Products and Partnerships (Current)

### Starlight

A new product category: sub-1W sensing devices containing multiple Mythic APUs. Designed to enhance image sensor performance by "extracting signals from noise using analog AI," claiming 50x improved lowlight sensor performance. Targeted at robotics and defense.

### Honda Partnership (Feb 2026)

Honda R&D will license Mythic's APU technology. The companies will co-develop an automotive-grade analog AI SoC for Honda's next-gen software-defined vehicles. Target: 100,000+ TOPS on-board AI compute within a strict low power envelope. Timeline: prototypes by late 2020s, production early 2030s.

### SST/Microchip memBrain Partnership (Mar 2026)

Mythic will use Silicon Storage Technology's memBrain neuromorphic flash IP for next-gen APUs. memBrain uses SST's SuperFlash eNVM bitcells. Available in 40nm and 28nm, with 22nm in development. This suggests Mythic is outsourcing the flash IP rather than designing it fully in-house, which could accelerate development.

### DoD Validation

Mythic states that its Gen 1 APUs have been "validated by the DoD" and "major defense partners." No specific programs or contracts have been publicly named.

### Data Center Ambitions

Mythic claims its APU-powered rack-scale servers can compete with NVIDIA Blackwell hardware, with "two orders of magnitude better TCO per token for 70B+ parameter models." This is the most aggressive and least-verified claim. No independent benchmarks have been published.

Sources: [Honda PR](https://global.honda/en/topics/2026/c_2026-02-04eng.html), [memBrain PR](https://ir.microchip.com/news-events/press-releases/detail/1375/mythic-selects-membrain-technology-from-silicon-storage-technology-for-its-next-generation-of-ultra-low-power-analog-processing-units), [Mythic website](https://mythic.ai/)

---

## 8. Key Open Questions

1. **Where are the independent benchmarks?** 14 years in, no MLPerf submission. No independent power measurement. All numbers are self-reported.

2. **What is the effective precision under real conditions?** The claimed 8-bit may degrade to 5-6 effective bits after noise, drift, and temperature variation. This matters enormously for LLM accuracy.

3. **How does inter-chiplet communication work at scale?** For 1T parameter LLMs across hundreds of chiplets, you need high-bandwidth, low-latency interconnect. Mythic has not disclosed its approach.

4. **What is the actual system-level TOPS/W for Gen 2?** The 120 TOPS/W may be the analog MAC only. System-level (including ADC/DAC, digital processing, I/O) could be 10-20x lower.

5. **Can the software ecosystem catch up?** CAMP SDK vs. CUDA is not a fair fight. Without broad developer adoption, even superior hardware cannot win.

6. **Revenue trajectory?** ~$6M in 2025 after $300M invested. The $125M round provides runway, but commercial traction remains the fundamental unsolved problem.

---

## 9. Verdict

Mythic is the best-funded, most technically mature company attempting flash-based analog CIM for AI. The physics is sound. The Gen 1 chips were real silicon that ran real workloads. The architecture genuinely eliminates the weight-read energy bottleneck that dominates digital AI inference.

But the efficiency claims have grown faster than the verified performance. Gen 1 delivered ~8 TOPS/W (good for 40nm, not revolutionary). Gen 2 claims 120 TOPS/W (extraordinary if true, but unverified). The 100x and 750x claims rely on internal benchmarks and favorable comparison methodology.

The biggest risk is not technical -- it is commercial. Mythic must convince customers to adopt a chip with a proprietary toolchain, limited model support, and unproven production track record, when NVIDIA offers CUDA compatibility, massive model libraries, and proven reliability. The Honda and Lockheed partnerships suggest some customers see enough value to commit R&D resources, but production revenue at scale remains years away.

**Bottom line**: Mythic is the most important test case for whether analog CIM can cross from "works in the lab" to "wins in the market." As of March 2026, the technology is promising but commercially unproven, and the headline efficiency claims need independent validation before they can be taken at face value.
