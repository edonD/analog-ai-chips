# IBM Analog AI Chip Research: Deep Dive

*Last updated: 2026-03-22*

IBM is arguably the most prolific research organization in analog in-memory computing for AI. Their work spans two distinct but related chip families -- the **HERMES analog AI chips** (true analog compute-in-memory using phase-change memory) and the **NorthPole digital near-memory chip** (purely digital but inspired by analog CIM principles). This document covers both, plus the software ecosystem and path forward.

---

## Table of Contents

1. [The HERMES Analog AI Chip Family](#1-the-hermes-analog-ai-chip-family)
2. [NorthPole: Digital Near-Memory (Not Analog)](#2-northpole-digital-near-memory-not-analog)
3. [Software Stack: aihwkit](#3-software-stack-aihwkit)
4. [Drift, Noise, and Variability -- The Core Engineering Challenges](#4-drift-noise-and-variability)
5. [Scaling to LLMs: Analog Foundation Models and MoE](#5-scaling-to-llms)
6. [Path to Production](#6-path-to-production)
7. [Comparison to Other Analog Approaches](#7-comparison-to-other-analog-approaches)
8. [Key Takeaways and Honest Assessment](#8-key-takeaways)
9. [Sources](#9-sources)

---

## 1. The HERMES Analog AI Chip Family

IBM's primary analog AI vehicle is the **HERMES project**, a series of mixed-signal in-memory computing chips based on phase-change memory (PCM). There are two major published silicon results.

### 1.1 First Generation: 34-Tile Chip (Nature, August 2023)

Published in *Nature* (vol. 620, pp. 768-775, 2023), this chip was the first to demonstrate that analog AI can handle real speech recognition tasks at near-software-equivalent accuracy.

**Specifications:**
- **Process:** 14nm CMOS with backend-integrated PCM
- **Tiles:** 34 analog in-memory computing tiles
- **PCM Devices:** 35 million phase-change memory devices total
- **Model Capacity:** Up to 17 million parameters (demonstrated), 45 million weights using 5-chip combination (140M PCM devices)
- **Peak Efficiency:** 12.4 TOPS/W chip-sustained performance
- **Memory:** Non-volatile -- weights retained when power is off

**Benchmark Results:**
| Task | Model | Accuracy | Comparison |
|------|-------|----------|------------|
| Keyword spotting | Google Speech Commands | Matched software baseline | 7x faster than best MLPerf submission in same category |
| Speech-to-text | RNNT (Librispeech) | 98.1% of digital baseline | 14x more energy efficient than digital |

The 14x energy efficiency claim is measured against MLPerf benchmarks on comparable digital hardware. IBM's own simulations have suggested 40-140x efficiency gains are theoretically possible for larger scale analog systems, but the 14x number is the measured silicon result.

**The catch:** The 17M parameter capacity is roughly two orders of magnitude smaller than GPT-3 (175B). The 14x efficiency gain is real but measured on relatively small models. Scaling to LLM-class workloads remains unproven in silicon.

### 1.2 Second Generation: 64-Core Chip (Nature Electronics, 2023)

Published in *Nature Electronics* (2023), this is the more architecturally complete HERMES chip.

**Specifications:**
- **Process:** 14nm CMOS with backend-integrated PCM
- **Cores:** 64 analog in-memory computing (AIMC) cores
- **Array per core:** 256 x 256 unit cells
- **Devices per unit cell:** 4 PCM devices (differential pair configuration)
- **Total PCM devices:** >16 million
- **Total weights:** ~4 million
- **On-chip communication:** Network-on-Chip (NoC) connecting all 64 tiles
- **Digital processing:** 8 Global Digital Processing Units (GDPUs) for activation functions, batch norm, pooling
- **MVM clock frequency:** Up to 1 GHz
- **ADC:** Time-based current-controlled oscillator (CCO) ADCs, 300ps/LSB linearized, flanking each array

**Performance:**

| Mode | Throughput | Energy Efficiency | MVM Precision |
|------|-----------|-------------------|---------------|
| 1-phase read (fast) | 63.1 TOPS | 9.76 TOPS/W | ~3 bits effective |
| 4-phase read (accurate) | 16.1 TOPS | 2.48 TOPS/W | ~4 bits effective |
| Throughput density | 400 GOPS/mm^2 | -- | 8-bit I/O |

**Key accuracy results:**
- CIFAR-10 (ResNet-9): **92.81%** -- highest reported for any analog chip using similar technology at time of publication
- ResNet-9 single inference: processed in **1.52 us** consuming **1.51 uJ**
- Also demonstrated LSTM networks with near-software accuracy

The 400 GOPS/mm^2 throughput density is **>15x higher** than previous multi-core resistive memory CIM chips.

### 1.3 How the Analog Compute Works

Each AIMC tile performs a matrix-vector multiplication (MVM) in the analog domain:

1. **Input encoding:** Digital input activations are converted to pulse-width modulated (PWM) voltage pulses applied to rows of the PCM crossbar array
2. **Analog MAC:** Current flows through PCM devices (whose conductance encodes weights). Kirchhoff's current law naturally sums the products at each column wire -- this IS the multiply-accumulate
3. **ADC conversion:** An array of 256 time-based CCO ADCs (128 on each side of the array) digitize the analog column currents
4. **Digital post-processing:** Results pass through on-tile digital units for shift, add, and scaling, then to GDPUs for activation functions

The key insight: the multiply-accumulate happens in physics (Ohm's law + Kirchhoff's law), in a single analog step, rather than through billions of digital multiply-add operations. This is where the energy savings come from -- no data movement, no digital multiplication circuits.

### 1.4 Phase-Change Memory: Why PCM?

IBM chose PCM over alternatives (ReRAM, MRAM, Flash) for several reasons:

- **Analog precision:** PCM provides a continuum of conductance states between amorphous (high resistance) and crystalline (low resistance), not just binary
- **Non-volatile:** Weights persist without power -- critical for edge deployment
- **Backend integration:** PCM can be fabricated in the BEOL (back-end-of-line) metal stack above CMOS logic, enabling tight integration
- **Mature at IBM:** IBM has decades of PCM research (originally for storage-class memory)
- **Programmability:** Electrical pulses control the amorphous/crystalline ratio, allowing weight programming

**Unit cell design:** Each weight uses 4 PCM devices in a differential configuration. This doubles the effective dynamic range and partially cancels common-mode noise/drift. A 256x256 array thus uses 256K PCM devices to store 64K weights.

---

## 2. NorthPole: Digital Near-Memory (Not Analog)

NorthPole is often discussed alongside IBM's analog work, but **it is a purely digital chip**. It is important to understand what it is and what it is not.

### 2.1 Architecture

- **Process:** 12nm
- **Transistors:** 22 billion
- **Die area:** 795 mm^2
- **Cores:** 256 digital, programmable cores
- **SRAM:** 224 MB distributed on-chip (192 MB in some reports, likely different accounting)
- **Per-core compute:** 2,048 8-bit ops/cycle (doubles at 4-bit, quadruples at 2-bit)
- **On-chip bandwidth:** 13 TB/s
- **Cooling:** Air-cooled (fans + heatsinks, no liquid cooling)

### 2.2 Key Design Principle

NorthPole eliminates ALL off-chip memory access during inference. The entire model must fit in on-chip SRAM. This is the same core idea as analog CIM (co-locate compute and memory) but executed entirely in digital logic. From outside the chip, NorthPole appears as an "active memory" -- you write a model in, and inference results come out.

### 2.3 Performance

**ResNet-50 (vs. 12nm GPU):**
- 25x higher FPS/watt (energy)
- 5x higher FPS/transistor (area)
- 22x lower latency
- Outperforms even 4nm GPUs on ResNet-50 in efficiency metrics

**vs. TrueNorth (predecessor):** ~4,000x faster

**LLM Inference (Granite 3B, September 2024):**
- Setup: 16 NorthPole cards in a 2U server, PCIe interconnect
- Model: IBM Granite-8B-Code-Base, quantized to a 3B-parameter variant with 4-bit weights and activations
- Latency: **<1 ms/token** -- 46.9x faster than next most energy-efficient GPU
- Throughput: **28,356 tokens/sec**
- Energy efficiency: **72.7x** more efficient than the next lowest-latency GPU
- Architecture: Pipelined parallelism, 14 transformer layers on 14 cards, output layer on 2 cards

### 2.4 NorthPole vs. HERMES: The Distinction

| Feature | NorthPole | HERMES (Analog) |
|---------|-----------|-----------------|
| Compute type | Digital | Analog (physics-based MAC) |
| Memory | SRAM (volatile) | PCM (non-volatile) |
| Precision | Configurable (2/4/8-bit) | ~3-4 bit effective MVM |
| Model capacity | 224 MB SRAM | ~4M weights (16M PCM devices) |
| Maturity | Demonstrated on LLMs | Research prototype |
| Off-chip memory | None | None |
| Weight persistence | Volatile (must reload) | Non-volatile (weights survive power-off) |

NorthPole proves the principle that near-memory/in-memory compute architectures deliver massive efficiency gains. But it does it digitally. The analog HERMES chips aim for even larger gains by eliminating the digital multiply circuits entirely, at the cost of noise, drift, and lower effective precision.

---

## 3. Software Stack: aihwkit

IBM's open-source **Analog Hardware Acceleration Kit (aihwkit)** is the primary software tool for the analog AI program.

### 3.1 Overview

- **Repository:** [github.com/IBM/aihwkit](https://github.com/IBM/aihwkit)
- **Language:** Python (with C++/CUDA backend)
- **Framework:** PyTorch integration
- **Latest version:** 0.9.2
- **Status:** Beta, under active development
- **License:** Apache 2.0

### 3.2 Key Features

- **Analog neural network layers:** Drop-in replacements for PyTorch Linear, Conv1d/2d/3d, LSTM
- **Device models:** Calibrated statistical models of PCM arrays (based on measurements from 1M-device chips), ReRAM, ECRAM
- **Hardware-aware training (HWA):** Injects realistic noise, drift, and quantization during training so models learn to be robust to analog non-idealities
- **Tiki-Taka training algorithm:** Specialized SGD variant designed for analog crossbar update rules
- **Inference simulation:** Models PCM drift over time, read noise, programming noise, ADC quantization
- **Global drift compensation:** Simulates the calibration procedure used on real hardware

### 3.3 Companion: aihwkit-lightning

- **Repository:** [github.com/IBM/aihwkit-lightning](https://github.com/IBM/aihwkit-lightning)
- Scalable hardware-aware training using PyTorch Lightning
- Designed for larger models and multi-GPU training

### 3.4 Maturity Assessment

The software is functional but clearly research-grade:
- Version numbering still below 1.0
- PyTorch compatibility can lag behind latest releases
- Documentation is decent but not production-polished
- Active development with regular releases through 2024-2025
- Used internally at IBM and by academic collaborators
- The PCM statistical models are the most valuable part -- calibrated on real silicon measurements, not toy models

---

## 4. Drift, Noise, and Variability -- The Core Engineering Challenges {#4-drift-noise-and-variability}

This is where analog AI either succeeds or fails. IBM has invested heavily in understanding and mitigating these issues.

### 4.1 PCM Conductance Drift

**The problem:** After programming, PCM devices in the amorphous state undergo structural relaxation, causing conductance to decrease over time following a power law: G(t) = G(t0) * (t/t0)^(-v), where v is the drift exponent (~0.05-0.1 for crystalline, much higher for amorphous states). This means stored weights change over time, degrading inference accuracy.

**IBM's solutions:**

1. **Global drift compensation:** Periodically read a subset of columns at a known input voltage. Compare the summed current to a reference measurement taken right after programming. Compute a single scaling factor to apply to all outputs. This is simple, cheap, and handles the dominant first-order drift effect.

2. **Projected PCM:** IBM's most important materials innovation. A thin "projection liner" of non-phase-change material is deposited in parallel with the PCM in the mushroom cell structure. During read operations, current partially bypasses the high-drift amorphous PCM through the lower-resistance liner. This:
   - Substantially reduces drift for RESET (amorphous) states
   - Reduces read noise across both SET and RESET states
   - Trade-off: reduced memory window (dynamic range)
   - Demonstrated on 300mm wafers at IBM AI Hardware Center in Albany
   - Published results show DNN accuracy improvement for both short-term and long-term after programming

3. **Hardware-aware training (HWA):** Train the neural network with simulated drift and noise injected during forward passes. The network learns weight configurations that are robust to drift, essentially finding "flat minima" in the loss landscape that tolerate weight perturbation.

### 4.2 Read Noise

**The problem:** Each analog read of a PCM device produces slightly different current due to 1/f noise and random telegraph noise. This adds stochastic error to every MAC operation.

**IBM's solutions:**
- Multi-phase reads (4-phase mode in HERMES averages out noise at cost of 4x throughput reduction)
- Differential cell design (4 PCM devices per weight partially cancel common-mode noise)
- Noise-aware training (inject read noise during training)

### 4.3 Device-to-Device Variability

**The problem:** No two PCM devices are identical. The conductance achieved for the same programming pulse varies across the array.

**IBM's solutions:**
- Closed-loop iterative programming: Apply pulse, read result, adjust, repeat until target conductance is reached. Achieves **<3% average weight error**
- Row-wise programming: Can tune up to 512 weights concurrently
- Statistical device models in aihwkit capture the variability distribution from real hardware

### 4.4 Limited Effective Precision

The HERMES chip achieves 3-4 bits effective MVM precision. This is the fundamental limitation of analog compute -- you cannot get 8-bit or 16-bit precision from a single analog read without multi-phase techniques that erode the throughput advantage. IBM's approach:
- Use analog for the heavy matrix multiplications (which dominate compute)
- Use digital logic for everything else (activations, normalization, attention)
- Accept the lower precision and train models to work with it (HWA training)

---

## 5. Scaling to LLMs: Analog Foundation Models and MoE {#5-scaling-to-llms}

The biggest question for analog AI: can it handle modern LLMs? IBM has been publishing actively on this.

### 5.1 Analog Foundation Models (NeurIPS 2025)

IBM and ETH Zurich published "Analog Foundation Models" at NeurIPS 2025, introducing a systematic method to adapt LLMs for analog hardware.

**The problem:** Off-the-shelf LLMs catastrophically fail when deployed on AIMC hardware due to noise and low-precision quantization. They cannot achieve even 4-bit digital quantization-equivalent performance.

**The solution -- a three-step pipeline:**
1. **Noise injection during training:** Simulate AIMC noise characteristics during fine-tuning
2. **Iterative weight clipping:** Stabilize weight distributions within the dynamic range of PCM devices
3. **Learned static quantization ranges:** Align input/output quantization with real hardware constraints

**Results:**
- Phi-3-mini-4k-instruct and Llama-3.2-1B-Instruct retain performance comparable to W4A8 (4-bit weight, 8-bit activation) digital baselines
- Outperforms both quantization-aware training (QAT) and post-training quantization (SpinQuant) on reasoning and factual benchmarks
- First systematic demonstration that large LLMs can be adapted to AIMC without catastrophic accuracy loss

### 5.2 3D Analog In-Memory Computing for MoE LLMs (Nature Computational Science, January 2025)

IBM proposed mapping Mixture-of-Experts (MoE) models onto 3D stacked non-volatile memory.

**Key idea:** Each expert in an MoE layer maps onto a physical layer in a 3D NVM stack. Since MoE only activates a subset of experts per token, only certain physical layers are active at any time -- natural sparsity alignment.

**Simulated results vs. GPUs:**
- Higher throughput
- Higher area efficiency
- Significantly higher energy efficiency (the advantage is largest for energy, because GPUs waste enormous energy on weight fetching -- a problem eliminated by CIM)

**Status:** Simulation only. No silicon demonstration of 3D analog CIM yet.

### 5.3 The Scaling Gap

Current HERMES silicon: ~4M weights (64 tiles x 256x256 / 4 devices per weight)

A 7B parameter LLM: ~7 billion weights

That is a gap of roughly **1,750x**. Closing this requires:
- More tiles per chip (hundreds to thousands)
- Larger arrays per tile
- Multi-chip systems (demonstrated with 5-chip 140M device system for speech)
- 3D stacking of PCM layers
- Advanced packaging (chiplets)

This is not a fundamental barrier, but it is a serious engineering challenge that puts production-scale analog LLM inference years away.

---

## 6. Path to Production {#6-path-to-production}

### 6.1 Current Status (as of early 2026)

- **HERMES chips:** Research prototypes fabricated at IBM's Albany NanoTech Complex. Active demonstrations at conferences (ISCAS 2025 included a live demo of automated DNN deployment on HERMES)
- **NorthPole:** More mature; demonstrated in server form factor (2U, 16 cards), LLM inference results published
- **AIU family:** IBM's broader AI chip family includes digital accelerators (Spyre for Power11, Telum II for z-series), analog AI, and NorthPole. Analog AI is explicitly described as the most experimental member

### 6.2 What IBM Has Said

- IBM describes HERMES as validating ideas "toward the development of a more self-contained, end-to-end chip that the company is already designing"
- They state "all the building blocks for analogue AI are in place" (Computer Weekly, 2023)
- Analog AI devices are "still very much in the research phase" but IBM is "looking to build a vibrant ecosystem and platform"
- The IBM AI Hardware Center in Albany has >100,000 sq ft of semiconductor fabrication space dedicated to next-generation AI chips

### 6.3 Realistic Timeline Assessment

- **2023-2024:** Proof-of-concept silicon (HERMES 34-tile, 64-core). Nature/Nature Electronics publications
- **2025-2026:** Algorithm and software maturation (Analog Foundation Models, MoE mapping). Next-generation chip design likely underway
- **2027-2028 (speculative):** Possible scaled-up analog chip with significantly more tiles, potentially targeting edge inference products
- **2029+ (speculative):** Production deployment in specific niches (edge AI, always-on inference, ultra-low-power devices)

IBM has NOT announced any commercial analog AI product or concrete productization timeline. The digital NorthPole and Spyre accelerators are much closer to deployment.

---

## 7. Comparison to Other Analog Approaches {#7-comparison-to-other-analog-approaches}

| Feature | IBM HERMES | Mythic M1076 | EnCharge EN100 | TetraMem |
|---------|-----------|--------------|----------------|----------|
| Memory tech | PCM | Flash | SRAM-based | ReRAM |
| Process | 14nm | 40nm | Not disclosed | Research |
| Compute type | Current-mode MAC | Current-mode MAC | Charge-domain MAC | Current-mode MAC |
| Key advantage | PCM non-volatility, IBM research depth | Shipping product (was) | Charge-domain noise reduction, 20x perf/W claim | Multi-level ReRAM |
| Key limitation | Research only, drift | Company pivoted/struggles | Startup, unproven at scale | Academic stage |
| Precision | 3-4 bit effective | ~8-bit claimed | Claims higher precision | Varies |
| Scale | 64 cores, 16M devices | Production chip | First chip | Lab demo |

**IBM's advantages over competitors:**
- Deepest understanding of device physics (decades of PCM research)
- Projected PCM for drift mitigation is a unique innovation
- Most comprehensive software ecosystem (aihwkit)
- Largest research team and fabrication capabilities
- Multiple Nature/Science publications establishing credibility

**IBM's disadvantages:**
- No commercial product or timeline
- PCM drift remains a fundamental challenge even with projected PCM
- 3-4 bit effective precision is low compared to digital 4-bit quantization
- Scaling to billions of parameters is undemonstrated in silicon

---

## 8. Key Takeaways and Honest Assessment {#8-key-takeaways}

### What IBM has proven:
1. **Analog CIM works for real neural networks.** The HERMES chips achieve near-software accuracy on CIFAR-10 and speech recognition -- not toy benchmarks
2. **Energy efficiency gains are real but modest at current scale.** 14x over digital for speech-to-text is significant but not the 100x sometimes claimed in press
3. **PCM drift can be managed** through a combination of projected PCM, global drift compensation, and hardware-aware training
4. **The software stack exists** and is usable for research (aihwkit)
5. **LLMs can be adapted for analog hardware** in simulation (Analog Foundation Models)

### What remains unproven:
1. **Scaling.** 4M weights to billions is a 1000x+ gap
2. **Production viability.** No commercial product, no announced timeline
3. **Long-term reliability.** PCM drift over months/years in deployment is not well-characterized
4. **Cost competitiveness.** PCM fabrication adds BEOL process steps; unclear cost vs. digital SRAM-based approaches
5. **LLM accuracy at scale on real silicon.** The NeurIPS 2025 results are simulated, not measured on chips
6. **Training on analog hardware.** Inference is demonstrated; on-chip training remains largely algorithmic/simulation work

### The verdict for analog AI at IBM:

IBM has the strongest research program in analog AI, period. They have real silicon, real measurements, and real publications in top venues. But the gap between their research prototypes and a production product is still enormous. The 64-core HERMES chip with 4M weights is impressive research but is orders of magnitude from competing with even a small GPU for real workloads.

The most likely path to impact is through NorthPole (digital near-memory) reaching production first, while analog continues to mature in the lab. If and when PCM manufacturing becomes cost-effective and the precision/drift challenges are fully solved, analog could deliver step-function improvements in inference efficiency for edge deployment. But that is a multi-year horizon, not 2026.

---

## 9. Sources {#9-sources}

### Key Papers
- "An analog-AI chip for energy-efficient speech recognition and transcription," *Nature* vol. 620, pp. 768-775, 2023. [Nature](https://www.nature.com/articles/s41586-023-06337-5)
- "A 64-core mixed-signal in-memory compute chip based on phase-change memory for deep neural network inference," *Nature Electronics*, 2023. [Nature Electronics](https://www.nature.com/articles/s41928-023-01010-1)
- "Neural inference at the frontier of energy, space, and time" (NorthPole), *Science*, 2023. [Science](https://www.science.org/doi/10.1126/science.adh1174)
- "Efficient scaling of large language models with mixture of experts and 3D analog in-memory computing," *Nature Computational Science*, January 2025. [Nat. Comput. Sci.](https://www.nature.com/articles/s43588-024-00753-x)
- "Analog Foundation Models," NeurIPS 2025. [OpenReview](https://openreview.net/forum?id=zo4zYTR8vn)
- "Optimization of Projected Phase Change Memory for Analog In-Memory Computing Inference," *Advanced Electronic Materials*, 2023. [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/aelm.202201190)
- "HERMES Core -- A 14nm CMOS and PCM-based In-Memory Compute Core using an array of 300ps/LSB Linearized CCO-based ADCs and local digital processing." [ResearchGate](https://www.researchgate.net/publication/353530571_HERMES_Core_-_A_14nm_CMOS_and_PCM-based_In-Memory_Compute_Core_using_an_array_of_300psLSB_Linearized_CCO-based_ADCs_and_local_digital_processing)
- "Using the IBM analog in-memory hardware acceleration kit for neural network training and inference," *APL Machine Learning*, 2023. [AIP](https://pubs.aip.org/aip/aml/article/1/4/041102/2923573/Using-the-IBM-analog-in-memory-hardware)

### IBM Research Blog Posts
- [An energy-efficient analog chip for AI inference](https://research.ibm.com/blog/analog-ai-chip-inference)
- [New analog AI chip design uses much less power for AI tasks](https://research.ibm.com/blog/analog-ai-chip-low-power)
- [IBM Research's new NorthPole AI chip](https://research.ibm.com/blog/northpole-ibm-ai-chip)
- [NorthPole achieves new speed and efficiency milestones (LLM results)](https://research.ibm.com/blog/northpole-llm-inference-results)
- [Why we need analog AI hardware](https://research.ibm.com/blog/why-we-need-analog-AI-hardware)
- [New algorithms may enable training AI models on analog chips](https://research.ibm.com/blog/analog-in-memory-training-algorithms)
- [IBM Research's AIU family of chips](https://research.ibm.com/blog/aiu-chip-family-ibm-research)
- [Analog in-memory computing could power tomorrow's AI models](https://research.ibm.com/blog/how-can-analog-in-memory-computing-power-transformer-models)
- [IBM's AI Hardware Center is building tomorrow's processors](https://research.ibm.com/blog/how-the-ibm-research-ai-hardware-center-is-building-tomorrow-s-processors)
- [IBM Analog AI project page](https://research.ibm.com/projects/analog-ai)

### Software
- [IBM aihwkit GitHub](https://github.com/IBM/aihwkit)
- [IBM aihwkit-lightning GitHub](https://github.com/IBM/aihwkit-lightning)
- [aihwkit documentation](https://aihwkit.readthedocs.io/en/latest/)
- [3D-CiM-LLM-Inference-Simulator GitHub](https://github.com/IBM/3D-CiM-LLM-Inference-Simulator)

### Press and Analysis
- [IBM's new analog chip should help mightily in power-hungry AI applications](https://spectrum.ieee.org/analog-ai-ibm) -- IEEE Spectrum
- [IBM Debuts Brain-Inspired Chip For Speedy, Efficient AI](https://spectrum.ieee.org/neuromorphic-computing-ibm-northpole) -- IEEE Spectrum
- [IBM describes analog AI chip that might displace GPUs](https://www.theregister.com/2023/08/14/ibm_describes_analog_ai_chip/) -- The Register
- [IBM says all the building blocks for analogue AI are in place](https://www.computerweekly.com/news/366548055/IBM-says-all-the-building-blocks-for-analogue-AI-are-in-place) -- Computer Weekly
- [Could IBM's AI Chip Reinvent Deep Learning Inference?](https://www.eetimes.com/could-ibms-ai-chip-reinvent-deep-learning-inference/) -- EE Times
- [IBM Touts Analog-Digital Hybrid Chip for AI Inferencing](https://www.tomshardware.com/news/ibm-touts-analog-digital-hybrid-chip-design-for-ai-inferencing-of-the-future) -- Tom's Hardware
- [NorthPole IBM Neuromorphic AI Hardware](https://open-neuromorphic.org/blog/northpole-ibm-neuromorphic-ai-hardware/) -- Open Neuromorphic
- [Optimizing Projected PCM for Analog Computing-In-Memory Inferencing](https://semiengineering.com/optimizing-projected-pcm-for-analog-computing-in-memory-inferencing-ibm/) -- Semiconductor Engineering
