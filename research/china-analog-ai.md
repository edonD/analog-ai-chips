# China's Analog AI Chip Ecosystem: A Strategic Deep Dive

## Summary

China has the most active analog compute-in-memory (CIM) research ecosystem in the world, driven by a unique convergence of strategic imperatives (US export controls), strong academic institutions (Tsinghua, Peking University, Nanjing University, Zhejiang University), government funding ($47.5B Big Fund III, $8.2B National AI Fund), and emerging industry-academia alliances (Huawei-ByteDance-Tsinghua). As of early 2026, Chinese groups have published more RRAM CIM silicon than any other country, hold the precision record for analog vector-matrix multiplication (Nanjing University, 0.101% RMSE), demonstrated the first on-chip learning memristor chip (Tsinghua STELLAR), and built the world's largest neuromorphic computer (Zhejiang University Darwin Monkey, 2.1 billion neurons). However, **no Chinese analog CIM chip is in commercial production**, and the gap between research demonstrations and deployable products remains wide. The strategic question -- whether analog CIM on mature nodes (28nm) can bypass GPU export restrictions -- is real but overstated: analog CIM addresses edge inference, not the datacenter training workloads that export controls target.

---

## 1. The Strategic Context: Why China Bets on Analog CIM

### The Export Control Catalyst

US semiconductor export controls (October 2022, updated October 2023, December 2024) restrict China's access to:
- Advanced digital AI chips (NVIDIA A100/H100/H200, AMD MI300)
- EUV lithography equipment (ASML)
- Advanced foundry services (TSMC 7nm and below)

This creates a structural incentive for China to pursue **architectural end-runs** -- computing paradigms that deliver competitive AI performance on mature process nodes (28nm, 40nm) that Chinese foundries (SMIC, Hua Hong) can manufacture without restricted equipment.

Analog CIM fits this requirement:
- **28nm is sufficient.** RRAM CIM, flash CIM, and SRAM CIM all work at 28nm -- the node where SMIC and Hua Hong have stable production capacity.
- **No EUV needed.** 28nm uses 193nm immersion lithography, which China has domestically.
- **Efficiency from architecture, not process.** Analog CIM gains come from eliminating data movement (compute-in-memory), not from transistor scaling.

### The Reality Check

Analog CIM is **not** a replacement for datacenter GPUs. It addresses edge inference (1-10W power budgets, small-to-medium models), not the large-scale training and LLM inference that export controls primarily target. Chinese tech companies (Huawei, ByteDance, Baidu) still need digital AI accelerators for their core AI workloads, which is why Huawei's Ascend series and Cambricon's Siyuan chips receive far more investment than analog alternatives. ByteDance reportedly plans to purchase $5.7 billion worth of Huawei Ascend chips in 2026 alone.

That said, analog CIM has genuine niche value for:
- **6G base station signal processing** (Peking University's RRAM chip targets MIMO detection)
- **Always-on IoT/edge AI** (autonomous driving perception, voice processing)
- **Military/defense applications** (low-power, radiation-tolerant edge inference)
- **Brain-computer interfaces** (HKU-Tsinghua memristor BCI decoder)

---

## 2. The Major Players: Chinese Universities with Analog CIM Silicon

### 2.1 Tsinghua University -- LEMON Lab (Wu Huaqiang, Gao Bin)

**The dominant force in Chinese analog CIM research.** The Laboratory of Emerging Memory and Novel Computing (LEMON), led by Professors He Qian, Wu Huaqiang, and Associate Professor Gao Bin at Tsinghua's School of Integrated Circuits, has produced more memristor CIM silicon than any other group worldwide.

#### STELLAR Chip (Science, September 2023)

The world's first fully system-integrated memristor chip with on-chip learning.

| Specification | Detail |
|---------------|--------|
| Architecture | Monolithic 3D: RRAM arrays fabricated above CMOS logic |
| Cell structure | 2T2R (differential, for signed weights and IR-drop mitigation) |
| Memristor stack | TiN/HfOx/TaOy/TiN |
| Algorithm | STELLAR (Sign- and Threshold-based Learning) -- binarized updates |
| Tasks demonstrated | Motion control, image classification, speech recognition |
| Energy vs. ASIC | **3% of equivalent ASIC** for on-chip learning |
| On-chip learning | Yes -- the key innovation |

**Why STELLAR matters:** On-chip learning is extremely hard for RRAM because programming is slow, energy-intensive, and limited by endurance. STELLAR's clever workaround uses binarized updates (sign flips only) instead of precise gradient updates, dramatically reducing write operations. This sidesteps RRAM's fundamental endurance limitation.

**The catch:** STELLAR's learning algorithm is specialized -- it doesn't support standard backpropagation. Models must be designed for the STELLAR framework. The chip demonstrated only small tasks (MNIST-class), not production workloads.

#### 28nm 576K RRAM CIM Macro (Journal of Semiconductors, January 2025)

The most process-advanced RRAM CIM macro from Chinese academia.

| Specification | Detail |
|---------------|--------|
| Process node | **28nm** -- foundry-relevant, SMIC-compatible |
| Array size | 576K RRAM cells |
| Area efficiency | 2.82 TOPS/mm² |
| Energy efficiency | 35.6 TOPS/W |
| Programming speedup | 4.67x (hybrid programming scheme) |
| Programming power | 0.15x (vs. conventional program-verify) |
| Weight distribution | 4.31x more compact |
| RMSE | 1.14% (32 input parallelism), 2.03% (128 input parallelism) |
| ADC design | Novel direct-current ADC shared between programming and inference |

**Significance:** This proves that RRAM CIM can be manufactured at the 28nm node -- entirely within China's domestic foundry capability. The hybrid programming scheme is a practical innovation addressing one of RRAM CIM's worst bottlenecks (programming time).

**Team:** Siqi Liu, Songtao Wei, Peng Yao, and others from Tsinghua's School of Integrated Circuits.

#### memCS -- Compressed Sensing Accelerator (National Science Review, January 2026)

| Specification | Detail |
|---------------|--------|
| Architecture | 128Kb 1T1R memristor array (1024 columns x 128 rows) |
| Application | Compressed sensing for edge computing |
| Speedup | **11.22x** over state-of-the-art CMOS hardware |
| Energy savings | **30.46x** over state-of-the-art CMOS hardware |
| Image classification | 94.2% accuracy on ImageNet |
| Image reconstruction | 31.11 dB PSNR (near-software peak) |
| Innovation | Hardware-software co-optimization: measurement matrix modification (MMM) and sparsity enhancement (SE) strategies |

**Team:** Jianshi Tang (Associate Professor), Huaqiang Wu (Professor), Tsinghua University.

#### NeuRRAM Contribution

Tsinghua's Wu Huaqiang contributed RRAM device expertise to the landmark NeuRRAM chip (UCSD/Stanford, Nature 2022). The 48-core, 3 million synapse chip at 130nm remains the largest-scale RRAM CIM demonstration.

#### Memristor Brain-Computer Interface (Nature Electronics, February 2025)

Collaboration with HKU and Tianjin University. A 128K-cell memristor chip as an adaptive neuromorphic decoder for BCIs:
- **85.17% decoding accuracy** (equivalent to software methods)
- **1,643x less energy** than CPU-based systems
- **216x higher speed** (normalized)
- First demonstration of co-evolution between biological brain and neuromorphic hardware

---

### 2.2 Peking University -- Sun Zhong's Group

#### 24-Bit Precision RRAM Solver (Nature Electronics, October 2025)

The most precise analog computation ever demonstrated on RRAM -- and one of the most-hyped Chinese chip results of 2025.

| Specification | Detail |
|---------------|--------|
| Process node | **40nm** commercial CMOS foundry |
| Memory type | TaOx-based RRAM, 1T1R cells |
| Per-cell precision | 3-bit (8 conductance levels) |
| Effective precision | **24-bit fixed-point** (via iterative refinement) |
| Programming success | 100% across 400 tested cells |
| Conductance range | 0.5-35 uS |
| Architecture | Two-circuit: fast LP-INV approximation (~120 ns) + refinement MVM circuit |
| Benchmark | MIMO signal detection |
| vs. NVIDIA H100 | **1,000x throughput**, **100x energy efficiency** |
| vs. AMD Vega 20 | Similar speedup claims |
| Relative errors | Below 10^-7 after 10 iterations |

**The headline claim: "1,000x faster than NVIDIA GPUs."**

**The critical catch:** This is for **matrix equation solving** (specifically Ax=b), not general neural network inference. The 1,000x speedup is for large-scale MIMO signal detection -- a specific linear algebra workload that maps perfectly onto analog crossbar arrays. The 24-bit precision comes from iterative algorithmic refinement (running the analog hardware ~10 times), not from 24-bit analog resolution per device. Each iteration uses 3-bit hardware. The throughput advantage diminishes as more iterations are needed for higher precision.

**Honest assessment:** This is excellent science -- it proves that low-precision analog hardware can be composed into high-precision computation via algorithms. The MIMO/6G application is real and commercially relevant. But comparing it to GPUs running general neural network workloads is misleading. A GPU doing matrix inversion for MIMO is using <1% of its capability; a specialized analog chip for this workload should win.

**Applications:** 6G base stations, massive MIMO signal processing, radar signal processing.

**Team:** Sun Zhong, Institute for Artificial Intelligence, Peking University; Beijing Advanced Innovation Center for Integrated Circuits.

#### ISSCC 2025 Presence

Peking University had 15 papers accepted at ISSCC 2025 -- the most first-authored papers of any institution. Relevant CIM/AI papers:
- "A 22nm 60.81 TFLOPS/W Diffusion Accelerator with Bandwidth-Aware Memory Partition and BL-Segmented Compute-in-Memory" (Jing Yiqi)
- "A 28nm 109.8 TOPS/W 3D PNN Accelerator" (Zhou Changchun)
- "SKADI: A 28nm Complete K-SAT Solver Featuring Dual-path SRAM-based Macro" (Wu Zihan)

Note: These are digital SRAM CIM, not analog RRAM CIM -- reflecting the broader trend where digital CIM dominates at ISSCC.

---

### 2.3 Nanjing University -- Miao Feng, Liang Shijun

#### Geometry-Ratio CIM Chip (Science Advances, October 2025)

A fundamentally different approach to analog CIM precision that sidesteps the device variability problem.

| Specification | Detail |
|---------------|--------|
| Process | Standard CMOS (no exotic memory required) |
| Weight encoding | **Device geometry ratios** (not resistance) |
| Precision record | **0.101% RMSE** -- highest ever for analog vector-matrix multiplication |
| Temperature range | -78.5C to 180C (stable operation) |
| RMSE at extremes | 0.155% (-78.5C), 0.130% (180C) |
| Magnetic resilience | <0.21% output variation under strong magnetic fields |

**Why this matters:** Every other analog CIM approach encodes weights as device conductance/resistance -- which is inherently noisy, temperature-sensitive, and drifts over time. Nanjing University's innovation encodes weights using geometric ratios of device structures (e.g., transistor width/length ratios), which are set by lithography and are as stable as the silicon itself. This is a fundamental rethinking of how analog weights work.

**The catch:** The approach requires custom transistor sizing for each weight, which means:
1. Weight values are fixed at fabrication time (no reprogramming)
2. Each different model requires a different chip layout
3. Density may be limited by the geometric encoding constraints

This is more like a fixed-function ASIC than a reconfigurable accelerator. Extremely precise, but inflexible.

**Implications:** If combined with techniques for partial reconfigurability, geometry-ratio encoding could provide a stable, high-precision backbone for hybrid analog-digital CIM systems. The temperature and magnetic-field stability is exceptional and could be valuable for automotive, aerospace, and military applications.

---

### 2.4 Zhejiang University -- Darwin Neuromorphic Series

Not analog CIM per se, but the most ambitious brain-inspired computing effort in China.

#### Darwin-III Chip (National Science Review, 2023)

| Specification | Detail |
|---------------|--------|
| Process | 28nm |
| Neurons per chip | 2.35 million (spiking) |
| Synapses per chip | 100+ million |
| Features | Custom ISA for brain-inspired computing, real-time online learning |

#### Darwin Monkey ("Wukong") System (August 2025)

**The world's largest neuromorphic computer.**

| Specification | Detail |
|---------------|--------|
| Scale | **2.1 billion neurons**, **100+ billion synapses** |
| Hardware | 15 blade servers, each with 64 Darwin-III chips (960 chips total) |
| Power | ~2,000W total system |
| Neural equivalent | Approaching macaque brain complexity |
| Innovation | **Darwin Wafer** -- System-on-Wafer design, single 12-inch wafer integrating 64 Darwin-III dies |

**Comparison to Intel Hala Point (Loihi 2):**

| | Darwin Monkey | Intel Hala Point |
|---|---|---|
| Neurons | 2.1 billion | 1.15 billion |
| Chips | 960 (Darwin-III) | 1,152 (Loihi 2) |
| Process | 28nm | Intel 4 (PNP) |
| Power | ~2,000W | ~2,600W (estimated) |
| Status | Research system | Research system |

Darwin Monkey has nearly 2x the neuron count of Intel's Hala Point, the previous record holder. Both are research systems with no commercial applications. The use of 28nm (vs Intel's leading-edge process) is notable -- Darwin achieves scale through wafer-level integration rather than transistor density.

---

### 2.5 Tsinghua University -- Shi Luping (CBICR Lab, Tianjic)

Separate from Wu Huaqiang's LEMON lab, this group focuses on neuromorphic architectures.

#### Tianjic Chip (Nature, 2019; Science Robotics, 2022)

| Specification | Detail |
|---------------|--------|
| Process | 28nm |
| Type | Digital neuromorphic (not analog CIM) |
| Neurons | ~40,000 |
| Synapses | ~10 million |
| Cores | 156 computational function cores |
| Power | ~1W |
| Memory bandwidth | >610 GB/s internal |
| Key innovation | **Unified SNN+ANN architecture** -- supports both spiking and conventional neural networks on same hardware |

**TianjicX (2022):** Extended architecture supporting concurrent multi-paradigm execution. Demonstrated on Tianjicat robot performing multi-task perception and control.

**Significance:** Tianjic was a landmark for demonstrating that brain-inspired and conventional deep learning don't need separate chips. However, at ~40,000 neurons, it is tiny compared to Darwin-III (2.35M) or Intel Loihi 2 (1M per chip). The main contribution is architectural, not scale.

---

### 2.6 Tsinghua + Partners -- ACCEL (All-Analog Photoelectronic Chip)

#### ACCEL Chip (Nature, November 2023)

A hybrid optical-electronic analog chip for vision tasks.

| Specification | Detail |
|---------------|--------|
| Architecture | Optical Analog Computing (OAC) + Electronic Analog Computing (EAC) |
| OAC | Diffractive optical computing, 500x500 optical neurons |
| EAC | 32x32 photodiode array, capacitance compensation, SRAM peripherals |
| Process (EAC) | 180nm CMOS |
| Computing speed | 4.6 peta-operations/second (99%+ from optics) |
| Energy efficiency | 74.8 POPS/W (claimed) |
| vs. NVIDIA A100 | **3.7x faster** for image classification |
| vs. GPU (vision) | 3,000x faster, 4,000,000x less energy (claimed) |

**The catch:** ACCEL operates on fixed pre-trained optical layers -- the diffractive elements are physically fabricated for a specific task. It can classify images in the optical domain, but cannot be reprogrammed for different models without physically replacing the optical elements. The "4 million times less energy" claim compares against a full GPU running the same vision task, which is the most favorable possible comparison for a fixed-function optical chip. ACCEL cannot do anything a GPU can do beyond its specific trained task.

#### LightGen (Science, December 2025)

From Shanghai Jiao Tong University and Tsinghua University. An evolution of the optical computing approach:
- First all-optical chip for large-scale semantic generative models
- Millions of optical neurons on-chip
- All-optical dimensional transformation
- 100x faster and more energy-efficient than leading NVIDIA GPUs (for supported tasks)
- Capabilities: 512x512 image generation, 3D generation (NeRF), video generation, semantic control

---

## 3. The Huawei-ByteDance-Tsinghua Alliance (ISSCC 2026)

### What Was Announced

At ISSCC 2026 (February 2026), Huawei, ByteDance, Tsinghua University, and other Beijing research institutions jointly unveiled an RRAM-based AI acceleration chip.

### Key Claims
- **66x faster than conventional CPUs** for targeted AI workloads
- RRAM-based compute-in-memory architecture

### What We Don't Know (as of March 2026)
- Process node (likely 28nm, given Tsinghua's 28nm RRAM CIM capability)
- Specific architecture details
- What "targeted AI workloads" means
- System-level power and efficiency
- Whether this is a research prototype or product prototype

### Why It Matters

This is the first time major Chinese tech companies have publicly backed RRAM CIM for AI. The combination is significant:
- **Huawei:** Has semiconductor design (HiSilicon) and manufacturing relationships (SMIC)
- **ByteDance:** Has massive AI workloads (TikTok recommendation, content understanding) and knows what models need to run
- **Tsinghua:** Has the RRAM CIM device and circuit expertise

The collaboration signals that RRAM CIM is moving from pure academic research toward potential commercial deployment in China's domestic AI ecosystem.

### The Skeptic's View

"66x faster than CPUs" is a low bar. Modern GPUs are 100-1000x faster than CPUs for AI workloads. The relevant comparison would be against GPUs or dedicated NPUs, not CPUs. Until architecture details and independent benchmarks are published, this should be treated as a strategic announcement rather than a technical breakthrough.

---

## 4. Chinese Government Funding and Strategy

### The Big Fund III ($47.5 Billion)

The National Integrated Circuit Industry Investment Fund III, established May 2024, is the largest semiconductor investment vehicle in history:
- **Capital:** RMB 344 billion ($47.5B)
- **Duration:** 15 years (2024-2039)
- **Focus:** Manufacturing equipment, materials, HBM, advanced packaging
- **Operations began:** December 31, 2024

### The National AI Fund ($8.2 Billion)

Launched January 2025, RMB 60 billion ($8.2B) for AI ecosystem development.

### Relevance to Analog CIM

Neither fund has publicly announced dedicated analog CIM programs. The Big Fund III targets:
1. Wafer fab capacity (especially 28nm -- directly supports CIM manufacturing)
2. Semiconductor equipment and materials
3. HBM and advanced packaging

Analog CIM benefits **indirectly** from:
- Massive 28nm capacity expansion at SMIC and Hua Hong (makes RRAM CIM fabrication accessible)
- RRAM/NVM technology development for embedded applications
- General university research funding through Ministry of Science and Technology programs

### The "New Productive Forces" Doctrine

Xi Jinping's 2024-2025 emphasis on "new productive forces" (xinzhi shengchanli) includes AI hardware as a priority area. While not specifically targeting analog CIM, this umbrella policy provides political cover and funding justification for advanced computing research at Chinese universities.

---

## 5. Chinese Startups and Industry

### The Startup Gap

Unlike the US (which has EnCharge, Mythic/Softbank, d-Matrix, Axelera, Sagence, TetraMem), China has **no well-funded analog CIM startups** with visible profiles as of early 2026. Chinese analog CIM innovation is overwhelmingly academic.

### Notable Industry Players

| Company | Activity | Relevance |
|---------|----------|-----------|
| **Zbit Semiconductor** (Hefei, listed on STAR Market) | CiNOR -- NOR Flash CIM technology for on-device AI inference | Only Chinese company with public CIM chip plans. Main business is NOR Flash and MCUs. |
| **Cambricon Technologies** | Digital AI accelerator (Siyuan series). Targeting 500K chips in 2026. | Competing digital paradigm, not analog. |
| **Huawei HiSilicon** | Ascend digital AI chips. RRAM CIM via ISSCC 2026 collaboration. | Digital chips are main business; RRAM is research. |
| **SMIC** | Foundry at 28nm+. Can fabricate RRAM CIM chips. | Enabler, not a CIM chip designer. Capacity is rationed for digital AI priority customers (Huawei). |
| **Hua Hong Semiconductor** | Foundry at 28nm+. Specialty processes. | Similar enabler role as SMIC. |

### Why the Startup Gap Exists

1. **Venture capital climate:** Chinese VC in 2024-2025 favors proven digital AI chip companies (Cambricon, Biren, Enflame) over speculative analog approaches
2. **Talent concentration in universities:** Top RRAM CIM researchers (Wu Huaqiang, Sun Zhong, Miao Feng) remain in academia
3. **Government labs vs. startups:** Chinese R&D culture favors university/government lab-based development over startup formation for pre-commercial technology
4. **RRAM maturity:** The technology isn't yet reliable enough for VC-backed product development

---

## 6. China vs. US/Europe: Comparative Assessment

### Research Output

| Metric | China | US | Europe |
|--------|-------|-----|--------|
| RRAM CIM silicon demos | 5+ (Tsinghua STELLAR, 28nm macro, memCS, PKU solver, NeuRRAM co-author) | 3-4 (NeuRRAM, TetraMem MX100, Crossbar) | 1-2 (IBM HERMES is Zurich) |
| Publications (CIM, 2023-2026) | Dominant in quantity | Strong in quality | Moderate |
| ISSCC 2025 CIM papers | Multiple (mostly digital SRAM CIM) | Multiple | Multiple |
| Precision record | Nanjing U (0.101% RMSE) | TetraMem (11-bit composite) | IBM (12.4 TOPS/W PCM) |
| On-chip learning demo | Tsinghua STELLAR | None published | None published |
| Neuromorphic scale | ZJU Darwin Monkey (2.1B neurons) | Intel Hala Point (1.15B) | SpiNNaker2 (Manchester) |

### Commercial Readiness

| Metric | China | US | Europe |
|--------|-------|-----|--------|
| Funded startups | ~0 (dedicated analog CIM) | 5+ (EnCharge $144M, Mythic/SoftBank $600M+, d-Matrix $2B, Axelera $450M) | 1-2 (Axelera is Netherlands) |
| Products shipping | None | Mythic Gen 2, d-Matrix (digital CIM) | Axelera Metis (digital CIM) |
| Industry-academia link | Huawei-ByteDance-Tsinghua (ISSCC 2026) | DARPA OPTIMA ($78M), EnCharge-Princeton | ARM-IBM Zurich collaboration |

### Where China Leads

1. **RRAM device research:** Tsinghua's LEMON lab is arguably the world's best at memristor device optimization, programming schemes, and 3D integration
2. **On-chip learning:** STELLAR is the only published system-integrated chip with on-chip learning
3. **Neuromorphic scale:** Darwin Monkey (2.1B neurons) exceeds Intel Hala Point
4. **Precision innovation:** Nanjing's geometry-ratio encoding is a genuinely novel approach
5. **Strategic urgency:** Export controls create a level of national commitment that the US analog CIM community lacks
6. **Optical analog computing:** ACCEL and LightGen are world-leading hybrid photonic-electronic demonstrations

### Where China Lags

1. **Commercialization:** No analog CIM startup ecosystem. US has 5+ funded companies.
2. **Software ecosystem:** No Chinese analog CIM compiler or SDK. (US doesn't have a good one either, but at least Mythic and EnCharge are building them.)
3. **Digital CIM:** At ISSCC 2025, Chinese groups contributed digital SRAM CIM papers, but the best results (192.3 TFLOPS/W) came from international collaboration. Digital CIM companies (d-Matrix, Axelera) are Western.
4. **System-level validation:** Chinese demos are at the macro or small-chip level. No system-level benchmarks (MLPerf or equivalent) from any Chinese analog CIM chip.
5. **Foundry process integration:** While SMIC and Hua Hong can do 28nm CMOS, they have not publicly announced RRAM CIM-specific process options (unlike GlobalFoundries' 22FDX+ with RRAM).

---

## 7. Export Control Implications

### Can Chinese Analog CIM Bypass GPU Restrictions?

**Short answer: Not for the workloads that matter.**

US export controls target:
- **Training:** Requires FP16/BF16 precision, massive parallelism, huge memory bandwidth (HBM). Analog CIM cannot do this -- 3-8 bit effective precision is fundamentally insufficient.
- **LLM inference:** Requires billions of parameters, KV cache management, token-level latency. No analog CIM chip has run a real LLM. The capacity gap (4M weights on-chip vs. billions needed) is 250-1000x.
- **Datacenter-scale compute:** Requires reliability, deterministic behavior, standard software stacks. Analog CIM has none of these.

**Where analog CIM could matter strategically:**
- **Edge military AI:** Low-power, always-on inference for drone perception, battlefield sensor fusion, signal intelligence. Analog CIM at 28nm is ideal and entirely within Chinese manufacturing capability.
- **6G infrastructure:** Peking University's RRAM chip for MIMO signal processing is directly relevant to China's 6G deployment.
- **Autonomous vehicles:** Edge inference for perception at low power. Chinese EV industry (BYD, NIO, Xpeng) could be a deployment vehicle.
- **Surveillance/IoT:** Always-on image classification and anomaly detection at extreme power budgets.

### The Mature-Node Strategy

China's 28nm foundry capacity is projected to reach 39% of global mature-node production by 2027 (from 31% in 2023). This capacity is **not** restricted by export controls. Analog CIM chips on 28nm can be:
- Designed domestically (Tsinghua, Peking University expertise)
- Manufactured domestically (SMIC, Hua Hong)
- Deployed domestically (no export restrictions on domestic use)

This makes analog CIM one of the few AI hardware categories where China has a fully domestic supply chain.

### What US Policymakers Should Watch

Current export controls focus on:
- Logic chip performance (TOPS threshold)
- Memory bandwidth (HBM specifications)
- Lithography equipment (EUV)

Analog CIM chips fall below the performance thresholds that trigger export controls, because they are measured in different metrics (analog TOPS/W, not digital FLOPS). A high-performance analog CIM chip at 28nm would likely not be controlled under current regulations, even if it provides militarily useful capabilities for edge AI.

---

## 8. Key Technical Innovations from China

### Innovation 1: Geometry-Ratio Weight Encoding (Nanjing University)

**Problem solved:** Device variability -- the #1 challenge for all analog CIM.

**How:** Instead of using variable resistance (RRAM, PCM, flash) to encode weights, use the physical dimensions of transistors. Transistor width/length ratios are set by lithography and are as stable as the silicon substrate.

**Result:** 0.101% RMSE -- 10-100x better than any resistance-based approach.

**Trade-off:** Fixed at fabrication. No reprogramming.

### Innovation 2: STELLAR On-Chip Learning Algorithm (Tsinghua)

**Problem solved:** RRAM endurance limits on-chip training.

**How:** Replace precise gradient updates with binarized sign-and-threshold updates that require only coarse weight changes.

**Result:** On-chip learning at 3% of ASIC energy. Demonstrated on motion control, classification, speech recognition.

**Trade-off:** Not compatible with standard backpropagation. Specialized algorithm.

### Innovation 3: Iterative Precision Amplification (Peking University)

**Problem solved:** Low per-device precision (3-bit) limits analog computing accuracy.

**How:** Two-circuit architecture: fast approximate circuit + refinement circuit. Iterate to amplify 3-bit device precision to 24-bit system precision.

**Result:** 24-bit fixed-point precision for matrix equations. 10^-7 relative errors.

**Trade-off:** Each iteration consumes time and energy. Throughput advantage shrinks with iterations.

### Innovation 4: Wafer-Level Neuromorphic Integration (Zhejiang University)

**Problem solved:** Chip-to-chip interconnect limits neuromorphic system scale.

**How:** Darwin Wafer -- integrate 64 Darwin-III dies on a single 12-inch wafer, bypassing PCB interconnect bottlenecks.

**Result:** 2.1 billion neurons in a 2,000W system.

**Trade-off:** Wafer-level integration has yield challenges; a single die failure affects the whole wafer.

### Innovation 5: Hardware-Software Co-Optimization for CIM (Tsinghua memCS)

**Problem solved:** Non-ideal device behavior degrades CIM accuracy.

**How:** Systematically analyze device non-idealities, then modify the algorithm (measurement matrix modification, sparsity enhancement) to compensate.

**Result:** Near-software accuracy (94.2% on ImageNet) with 11.22x speedup and 30.46x energy savings.

**Lesson:** The most practical Chinese CIM results come from aggressive hardware-software co-design, not from trying to make hardware perfect.

---

## 9. The Chinese CIM Publication Machine

Chinese groups dominate CIM publication volume:

| Venue | Chinese CIM Papers (2023-2025) | Notable |
|-------|-------------------------------|---------|
| **Nature / Science / Nature Electronics** | STELLAR (Science 2023), NeuRRAM co-author (Nature 2022), PKU solver (Nat. Elec. 2025), BCI decoder (Nat. Elec. 2025), LightGen (Science 2025) | China leads in high-impact CIM publications |
| **Science Advances** | Nanjing U geometry-ratio chip, Tsinghua analog iteration | Novel architectures |
| **National Science Review** | memCS accelerator (2026) | Chinese-journal showcase |
| **Journal of Semiconductors** | Tsinghua 28nm macro (2025) | Practical circuit-level work |
| **ISSCC 2025** | 49 papers from China total (15 PKU, 13 Tsinghua); several digital SRAM CIM | Massive presence, but CIM papers are mostly digital, not analog |
| **ISSCC 2026** | Huawei-ByteDance-Tsinghua RRAM chip | First industry-backed analog CIM |

Despite this dominance in publications, **zero Chinese analog CIM chips are in commercial production.** The publication-to-product pipeline is broken, primarily due to the startup gap identified in Section 5.

---

## 10. Honest Assessment: China's Analog CIM Position

### Strengths

1. **World-class RRAM device research** -- Tsinghua's LEMON lab is genuinely the global leader in memristor CIM device optimization
2. **Novel architectural ideas** -- Geometry-ratio encoding, STELLAR on-chip learning, iterative precision amplification are all original contributions
3. **Strategic alignment** -- Export controls create national urgency that funds and motivates research
4. **Manufacturing capability** -- 28nm foundry capacity is domestic and expanding
5. **Academic depth** -- Multiple top-tier universities (Tsinghua, PKU, Nanjing, ZJU) with complementary expertise
6. **Publication volume** -- Dominant in high-impact journals

### Weaknesses

1. **No commercial ecosystem** -- Zero funded startups, zero products, zero revenue from analog CIM
2. **System-level gap** -- All demonstrations are at macro/chip level, not system level. No MLPerf benchmarks.
3. **Software vacuum** -- No compiler, SDK, or toolchain for Chinese analog CIM hardware
4. **Hype cycle risk** -- "1,000x faster than GPU" headlines create unrealistic expectations that will lead to disappointment
5. **Still not solving the big problem** -- Chinese analog CIM research is excellent for niche tasks (MIMO, compressed sensing, BCI) but doesn't address the core AI compute bottleneck (training, LLM inference)
6. **Foundry RRAM process maturity** -- SMIC/Hua Hong don't have announced RRAM CIM PDKs, unlike GlobalFoundries (22FDX+ RRAM)

### The Core Tension

China's analog CIM research is world-leading in publications and innovation. But the commercial infrastructure -- startups, venture funding, product engineering, software ecosystem -- is 3-5 years behind the US. The irony: China has better RRAM CIM science than the US, but the US is closer to analog CIM products (via EnCharge, Mythic/SoftBank, TetraMem).

The Huawei-ByteDance-Tsinghua collaboration at ISSCC 2026 could be the inflection point -- if it leads to a real product program backed by industry resources, China could close the commercialization gap quickly. If it remains a one-off research demo, the gap will persist.

### What to Watch

1. **Huawei RRAM chip follow-up:** Does the ISSCC 2026 demo lead to a product program?
2. **Tsinghua spinouts:** Does Wu Huaqiang's group form a startup? (This would be the Chinese analog of EnCharge.)
3. **SMIC RRAM process:** Does SMIC announce a CIM-specific RRAM PDK?
4. **Big Fund III allocation:** Does analog CIM receive dedicated government funding?
5. **Military adoption:** Does PLA adopt analog CIM for edge AI? (This would be the highest-impact deployment path.)

---

## Sources

- [STELLAR: Edge learning memristor chip -- Science 2023](https://www.science.org/doi/10.1126/science.ade3483)
- [Tsinghua STELLAR Breakthrough -- CGTN](https://news.cgtn.com/news/2023-10-11/China-makes-major-breakthrough-in-memristor-computing-in-memory-chips-1nOqlLtvMgE/index.html)
- [Tsinghua STELLAR -- School of Integrated Circuits](https://www.sic.tsinghua.edu.cn/en/info/1009/1542.htm)
- [Tsinghua 28nm 576K RRAM CIM Macro -- Journal of Semiconductors 2025](https://www.jos.ac.cn/en/article/doi/10.1088/1674-4926/24100017)
- [memCS Compressed Sensing Accelerator -- National Science Review 2026](https://academic.oup.com/nsr/article/13/1/nwaf499/8322430)
- [Memristor chip accelerates compressed sensing -- EurekAlert](https://www.eurekalert.org/news-releases/1109311)
- [Peking University RRAM Solver -- Nature Electronics 2025](https://www.nature.com/articles/s41928-025-01477-0)
- [Peking University RRAM -- TechXplore](https://techxplore.com/news/2025-10-rram-based-analog-rapidly-matrix.html)
- [PKU Analog Chip 1000x Faster -- PKU News](https://newsen.pku.edu.cn/PKUmedia/15269.html)
- [PKU ISSCC 2025 Papers](https://newsen.pku.edu.cn/news_events/news/focus/14752.html)
- [Nanjing University Precision Record -- TrendForce](https://www.trendforce.com/news/2025/10/17/news-chinese-research-team-breaks-precision-record-with-new-analog-in-memory-computing-chip/)
- [Nanjing University CIM Chip -- Global Times](https://www.globaltimes.cn/page/202510/1345832.shtml)
- [Nanjing University Analog CIM -- Science Advances](https://www.science.org/doi/10.1126/sciadv.adv7555)
- [Huawei-ByteDance RRAM Chip ISSCC 2026 -- DigiTimes](https://www.digitimes.com/news/a20260302PD215/huawei-bytedance-rram-isscc-2026.html)
- [Darwin Monkey / Wukong -- Zhejiang University](https://www.zju.edu.cn/english/2025/0910/c19573a3079424/page.htm)
- [Darwin-III Chip -- National Science Review 2023](https://academic.oup.com/nsr/article/11/5/nwae102/7631347)
- [Tianjic Chip -- Open Neuromorphic](https://open-neuromorphic.org/neuromorphic-computing/hardware/tianjic-tsinghua-university/)
- [ACCEL Photonic Chip -- Nature 2023](https://www.nature.com/articles/s41586-023-06558-8)
- [ACCEL -- Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/chinas-accel-analog-chip-promises-to-outpace-industry-best-in-ai-acceleration-for-vision-tasks)
- [LightGen Optical Chip -- Science 2025](https://singularityhub.com/2025/12/22/this-light-powered-ai-chip-is-100x-faster-than-a-top-nvidia-gpu/)
- [Memristor BCI Decoder -- Nature Electronics 2025](https://www.nature.com/articles/s41928-025-01340-2)
- [HKU Memristor BCI](https://www.eee.hku.hk/20250218-1/)
- [China Big Fund III -- Wikipedia](https://en.wikipedia.org/wiki/China_Integrated_Circuit_Industry_Investment_Fund)
- [Big Fund III Analysis -- Eurasia Review](https://www.eurasiareview.com/10122025-big-fund-iii-chinas-long-game-to-control-the-chips-that-make-the-world-work-analysis/)
- [China's 28nm Foundry Expansion -- DigiTimes](https://www.digitimes.com/news/a20250505PD209/28nm-wafer-fab-nexchip-smic-2027-capacity.html)
- [China Mature-Node Push -- DigiTimes March 2026](https://www.digitimes.com/news/a20260318VL209/12-inch-china-28nm-mature-process-hua-hong-semiconductor-nexchip-silan.html)
- [Zbit Semiconductor -- Official Site](https://zbitsemi.com/en/)
- [US Export Controls and China -- Congress.gov](https://www.congress.gov/crs-product/R48642)
- [Limits of Chip Export Controls -- CSIS](https://www.csis.org/analysis/limits-chip-export-controls-meeting-china-challenge)
- [China Semiconductor Self-Sufficiency -- Turing Institute](https://cetas.turing.ac.uk/publications/chinas-quest-semiconductor-self-sufficiency)
- [ByteDance $5.7B Huawei Chip Order -- Huawei Central](https://www.huaweicentral.com/bytedance-to-order-5-7-billion-huawei-ai-chips-over-nvidia-in-2026/)
- [Cambricon 500K Chips Target -- Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/cambricon-targets-500000-ai-chips-in-2026-as-china-accelerates-domestic-hardware-push)
- [DARPA OPTIMA / EnCharge $18.6M -- HPCwire](https://www.hpcwire.com/off-the-wire/darpa-awards-encharge-ai-and-princeton-18-6m-to-pioneer-next-gen-in-memory-ai-processors/)
- [NeuRRAM -- Nature 2022](https://www.nature.com/articles/s41586-022-04992-8)
