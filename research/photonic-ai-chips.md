# Photonic AI Chips: Optical Computing for Neural Networks (2025-2026)

**Date:** 2026-03-22
**Status:** Active research area with massive investment, but compute products remain pre-commercial. Interconnect products are shipping.

---

## Executive Summary

Photonic computing for AI uses light (photons) instead of electrons to perform the matrix multiplications at the heart of neural networks. The physics is compelling: light travels at c, does not generate resistive heat, and can encode information across multiple wavelengths simultaneously. In theory, this yields enormous speed and energy advantages.

In practice, photonic AI computing in 2025-2026 is splitting into two very different stories:

1. **Photonic interconnect** (moving data with light between electronic chips) is commercially real and shipping. NVIDIA, Lightmatter, Ayar Labs, and Celestial AI (acquired by Marvell for $5.5B) are deploying co-packaged optics. This is not speculative -- it is happening now.

2. **Photonic compute** (performing matrix multiplication with light) remains mostly in the lab or early prototype stage. Claims of 100-160 TOPS/W exist but come with enormous asterisks around precision, workload scope, and system-level accounting. No photonic compute chip is running production AI workloads at a hyperscaler as of early 2026.

The honest assessment: photonic interconnect is a 2025-2026 story. Photonic compute is a 2028-2032+ story, if it works at all for general AI.

---

## Table of Contents

1. [How Photonic Matrix Multiplication Works](#1-how-photonic-matrix-multiplication-works)
2. [The Two Architectures: MZI vs. Microring](#2-the-two-architectures-mzi-vs-microring)
3. [Company Landscape](#3-company-landscape)
4. [Performance Numbers: What Has Actually Been Measured](#4-performance-numbers-what-has-actually-been-measured)
5. [The Fundamental Challenges](#5-the-fundamental-challenges)
6. [Photonic vs. Electronic Analog](#6-photonic-vs-electronic-analog)
7. [The Interconnect Story (Where Photonics Actually Wins Today)](#7-the-interconnect-story)
8. [Honest Assessment: Timeline and Viability](#8-honest-assessment)
9. [Sources](#9-sources)

---

## 1. How Photonic Matrix Multiplication Works

Matrix-vector multiplication (MVM) is the dominant operation in neural network inference and training. In a photonic processor, this operation is performed using the physics of light interference and modulation rather than transistor switching.

### The Basic Principle

Light has amplitude and phase. When two beams of light interfere, the resulting amplitude depends on their relative phase -- this is the physical basis for optical multiplication. A beam's intensity can be modulated (multiplied by a weight), and multiple modulated beams can be combined (summed) on a photodetector. This gives you a multiply-accumulate (MAC) operation in the optical domain.

The key advantage: **the multiplication happens at the speed of light propagation through the chip (~picoseconds), consuming near-zero energy for the computation itself.** The energy cost comes from (a) encoding inputs onto light (modulation), (b) reading out results (photodetection + ADC), and (c) powering the laser source.

### Three Main Approaches

**Coherent (Mach-Zehnder Interferometer meshes):**
- Used by Lightmatter (Envise), MIT research
- MZI arrays implement unitary matrix transformations
- An N x N matrix requires N^2 MZIs
- Phase shifters on each MZI arm set the matrix weights
- Any matrix can be decomposed via SVD into two unitary matrices and a diagonal matrix, each implementable in MZIs

**Wavelength-Division Multiplexing (Microring Resonator weight banks):**
- Used by various academic groups, NVIDIA's CPO modulator technology
- Each microring resonator is tuned to a specific wavelength
- The resonance controls transmission (= weight) for that wavelength channel
- Multiple wavelengths carry different input values simultaneously
- A single waveguide with N microrings implements an N-element dot product
- Demonstrated: ~5.1 bits effective precision on 2 Gbps signals
- Compute density: ~4.67 TOPS/s/mm^2 demonstrated

**Diffractive / Free-space optics:**
- Used by Tsinghua (Taichi), Lumai, LightGen
- Light propagates through physical layers (diffractive optical elements or spatial light modulators)
- Each pixel/element modulates light passing through it
- Massive parallelism (millions of elements) but hard to integrate on-chip
- LightGen: 2M+ photonic "neurons" in a 3D stacked design

---

## 2. The Two Architectures: MZI vs. Microring

### Mach-Zehnder Interferometer (MZI) Mesh

**How it works:** An MZI splits a light beam into two paths, applies a relative phase shift, then recombines them. The output power depends on the phase difference. A mesh of MZIs can implement an arbitrary unitary matrix transformation.

**Strengths:**
- Mathematically elegant -- any matrix decomposable via SVD can be mapped
- Broadband operation (works across wavelengths)
- Well-studied, mature silicon photonics component
- Recent result: 16-channel coherent photonic processor achieving 1.28 TOPS

**Weaknesses:**
- N^2 scaling: a 256x256 matrix needs 65,536 MZIs
- Cascaded insertion losses accumulate -- each MZI adds ~0.1-0.5 dB loss
- Phase errors compound across the mesh
- Thermal sensitivity: each phase shifter must be actively stabilized
- Footprint: each MZI is ~100-500 um, so large matrices consume significant area

### Microring Resonator Weight Banks

**How it works:** Microring resonators are tiny (5-50 um radius) circular waveguides that couple to a bus waveguide. At resonance, light is absorbed or redirected; off-resonance, it passes through. By thermally or electrically tuning the resonance, you control the weight applied to each wavelength channel.

**Strengths:**
- Extremely compact (~10 um footprint per weight)
- Naturally supports WDM -- different weights on different wavelengths
- High compute density demonstrated (4.67 TOPS/s/mm^2)
- NVIDIA chose microring modulators for their CPO switches

**Weaknesses:**
- Very temperature sensitive (~80 pm/C resonance shift for silicon)
- Narrow bandwidth per ring -- limits to specific wavelength channels
- Crosstalk between adjacent rings
- Limited dynamic range for weight encoding
- Continuous active tuning required to maintain weight accuracy

---

## 3. Company Landscape

### Tier 1: Photonic Interconnect (Shipping or Near-Shipping)

#### Lightmatter -- Passage (Interconnect)
- **Valuation:** $4.4B (Oct 2024 Series D, $400M raised, $850M total)
- **Passage M1000:** 3D photonic superchip interposer
  - 114 Tbps total optical bandwidth
  - 4,000+ mm^2 multi-reticle active photonic interposer
  - 34 integrated chiplets, 1024 SerDes lanes, 256 optical fibers
  - 800 Gbps per fiber (16 bidirectional WDM wavelengths x 448 Gbps)
  - Built-in solid-state optical circuit switching
  - Fabricated on GlobalFoundries Fotonix silicon photonics platform
  - **Available:** Summer 2025
- **Passage L200:** 3D co-packaged optics for XPUs
  - 32 Tbps and 64 Tbps versions
  - 5-10x improvement over existing CPO solutions
  - 200+ Tbps total I/O bandwidth per chip package
  - **Available:** 2026
- Source: [Lightmatter M1000 Press Release](https://lightmatter.co/press-release/lightmatter-unveils-passage-m1000-photonic-superchip-worlds-fastest-ai-interconnect/)

#### Ayar Labs -- Optical I/O Chiplets
- **Funding:** $870M total ($500M Series E, March 2026, led by Neuberger Berman; investors include NVIDIA, AMD, MediaTek)
- **Valuation:** $3.75B
- **TeraPHY Optical I/O Chiplet:**
  - First UCIe (Universal Chiplet Interconnect Express) optical chiplet
  - 8 Tbps bandwidth per chiplet
  - 16-wavelength SuperNova light source
  - Compatible with standard multi-chip package architectures
- **Timeline:** Prototypes complete; production samples expected 2026; volume deployment 2026-2028
- Partnership with Alchip for co-packaged optics manufacturing at TSMC
- Source: [Ayar Labs UCIe Chiplet](https://ayarlabs.com/news/ayar-labs-unveils-worlds-first-ucie-optical-chiplet-for-ai-scale-up-architectures/)

#### Celestial AI -- Photonic Fabric (Acquired by Marvell)
- **Acquisition:** $5.5B by Marvell ($3.25B initial: $1B cash + 27.2M shares), closing by end of March 2026
- **Photonic Fabric Module (Aug 2025):**
  - World's first SoC with optical interconnect integrated in middle of silicon die
  - Optical Multi-Chip Interconnect Bridge (OMIB)
  - 16 Tbps bandwidth in a single chiplet
  - 10x capacity of state-of-the-art 1.6T ports
  - 2x power efficiency of copper interconnects
- Revenue expected late 2028, billion-dollar run-rate by end of 2029
- Source: [Celestial AI Hot Chips 2025](https://www.servethehome.com/celestial-ai-photonic-fabric-module-at-hot-chips-2025/)

#### NVIDIA -- Co-Packaged Optics Switches
- **Spectrum-X Photonics** (Ethernet) and **Quantum-X Photonics** (InfiniBand) switches
- Announced at GTC 2025
- Based on micro-ring modulator (MRM) technology
- Quantum-X Photonics: 144 ports of 800 Gb/s InfiniBand
  - 18 silicon photonics engines, 324 optical connections, 288 data links
  - 36 laser inputs, 4.8 Tb/s aggregate throughput
  - 4x fewer lasers, 3.5x more power efficient, 10x better network resiliency
- Partners: TSMC, Coherent, Corning, Lumentum
- **Timeline:** Quantum-X Photonics late 2025; Spectrum-X Photonics 2026
- Source: [NVIDIA Spectrum-X Photonics](https://nvidianews.nvidia.com/news/nvidia-spectrum-x-co-packaged-optics-networking-switches-ai-factories)

#### iPronics -- Software-Defined Photonic Switches
- Raised EUR 20M Series A (Jan 2025)
- ONE-32: world's first silicon photonics optical circuit switch (OCS)
- Real-time switching demonstrated at OFC 2025
- Manufacturing partnership with Fabrinet (March 2026)
- First 10 hyperscaler and AI-cluster OEM customers
- Source: [iPronics Series A](https://ipronics.com/ipronics-raises-20m-in-series-a-to-advance-optical-networking-for-next-gen-ai-data-centers/)

### Tier 2: Photonic Compute (Pre-Commercial / Prototype)

#### Lightmatter -- Envise (Compute)
- **Architecture:** 2D array of Mach-Zehnder interferometers in silicon photonics
- **Performance:** 65.5 TOPS (Adaptive Block Floating-Point 16-bit) at 78W electrical + 1.6W optical = ~820 TOPS/W (ABFP16)
- **Precision:** Adaptive Block Floating-Point (ABFP) -- groups numbers into blocks with shared exponent
  - Analog gain control amplifies signals before ADC to maximize precision capture
  - "Accuracies approaching 32-bit floating-point digital systems" claimed
- **System:** 50 billion transistors, 6 chips per package, ~1 million photonic components
- Envise 4S: 16 Envise Chips in 4U, 3kW, 1TB DDR4, 3TB SSD, 6.4 Tbps optical interconnect
- Demonstrated on ResNet, BERT, GPT-3, Atari RL, DLRM without quantization-aware training
- **Key limitation:** Thermal management -- "dedicated mixed-signal circuits" actively control ~1 million photonic elements
- **Status:** Customer samples; no public evidence of hyperscaler production deployment
- Source: [Lightmatter Blog](https://lightmatter.co/blog/a-new-kind-of-computer/)

#### Lightelligence (Shanghai)
- Raised $210M+ in Series C
- **LightSphere X:** Distributed optical interconnect GPU supernode (with Biren Technology, ZTE)
  - Won SAIL Award at World AI Conference 2025
- **Xizhi Tianshu:** Optoelectronic hybrid computing card with world's largest 128x128 photonic matrix
- Two business lines: photonic networking + photonic computing
- China's first xPU-CPO optoelectronic co-packaged prototype
- CEO prediction: photonic chips to account for 30% of computing power in data centers within 5 years
- Source: [Lightelligence 36kr](https://eu.36kr.com/en/p/3452345776231816)

#### Neurophos
- **Funding:** $110M Series A (Jan 2026), led by Gates Frontier, with Microsoft M12, Aramco Ventures, Bosch Ventures
- **Core innovation:** Micron-scale metamaterial optical modulators, claimed 10,000x smaller than previous photonic elements
- **Architecture:** OPU (Optical Processing Unit) with 1M+ optical processing elements per chip
  - Single photonic tensor core: 1,000 x 1,000 processing elements
  - Combined with compute-in-memory technology
- **Claimed performance:**
  - 470 petaFLOPS FP4/INT4 (~10x NVIDIA Rubin)
  - 234,000 TOPS at 300 TOPS/W
  - Clock speeds exceeding 100 GHz
- **Timeline:** Pilot with Terakraft data center 2027; first systems early 2028; production scaling late 2028
- **Red flag:** These numbers are extraordinary and unverified. No third-party benchmarks. Manufacturing at standard foundries claimed but not demonstrated at scale.
- Source: [SiliconANGLE](https://siliconangle.com/2026/01/22/chip-startup-neurophos-gets-110m-replace-electrons-photons-accelerate-ai-compute/)

#### Q.ANT (Germany)
- **Platform:** Thin-Film Lithium Niobate on Insulator (TFLNoI) -- not silicon photonics
- **NPU Gen 2:**
  - 8 parallel channels
  - Clock: 200 MHz -> 2 GHz (Gen 1 to Gen 2)
  - Current throughput: 8 GOPS (yes, GOPS, not TOPS)
  - Power: 150W
  - PCIe Gen4 x8 interface
  - Operating temp: 15-35C
- **Energy per operation:** 76 fJ for 8-bit TFLN vs. 2,300 fJ for 8-bit CMOS (claimed 30x advantage)
- **Roadmap:** 0.1 GOPS (2024) -> 8 GOPS (2025) -> 100,000 GOPS (2028) -- that is a million-fold increase claimed in 4 years
- **Key advantage:** Native nonlinear operations in lithium niobate -- one optical element does what 100-1000 CMOS transistors do
- **Honest read:** 8 GOPS at 150W is orders of magnitude behind GPUs today. The roadmap is extremely aggressive. Lithium niobate is a niche platform, not mainstream foundry-compatible.
- Rack-mountable server (NPS) with Linux, C/C++/Python APIs
- Shipping to customers H1 2026
- Source: [Q.ANT Photonic Computing](https://qant.com/photonic-computing/)

#### Lumai (Oxford, UK)
- **Approach:** Free-space optics (not integrated photonics)
- **How it works:** 1,024 laser sources encode input vector, light spreads through 3D space via lens, electronic display pixels modulate light (= matrix weights), photodetector array reads output
- **Funding:** $10M+ (April 2025)
- Claimed 4x faster inference than GPUs with "order of magnitude" cost reduction
- Very early stage. Free-space optics is inherently harder to manufacture and integrate than on-chip solutions.
- Source: [Lumai Optics.org](https://optics.org/news/16/4/7)

#### Luminous Computing
- Raised $105M Series A (2022)
- Developing hybrid systems: optical modules for linear operations, CMOS for nonlinearity and control
- **Status unclear as of 2025-2026.** No major product announcements found. May be pivoting or in stealth.
- Source: [The Register](https://www.theregister.com/2022/03/05/luminous-ai-supercomputer-photonics/)

### Tier 3: Academic / Research Prototypes

#### Tsinghua -- Taichi Photonic Chiplet
- Published in *Science* (April 2024)
- **Architecture:** Integrated diffractive-interference hybrid design
- Distributed computing: binary encoding protocol divides tasks into sub-problems deployable on photonic chiplets
- **Scale:** 13.96 million artificial neurons (vs. 1.47M in next-largest competing design)
- **Efficiency:** 160 TOPS/W claimed
- **Benchmark:** 1,000-category classification on 1,623-category Omniglot dataset at 91.89% accuracy; AIGC tasks demonstrated
- **Catch:** The 160 TOPS/W number likely excludes laser power, DAC/ADC power, and electronic control overhead. The chip performs specific demonstration tasks, not general neural network inference.
- Source: [Science paper](https://www.science.org/doi/10.1126/science.adl1203)

#### Shanghai Jiao Tong / Tsinghua -- LightGen
- Published in *Science* (Dec 2025)
- All-optical chip for generative AI
- 2M+ photonic "neurons" in 3D stacked layers
- Claimed 100x faster and 100x more energy efficient than NVIDIA A100 on generative tasks
- **Critical limitations:**
  - Still relies on bulky lasers and spatial light modulators for input
  - Metasurfaces made with specialized processes, not standard foundry
  - **"Only in tightly constrained domains"** -- specialized analog machines, not general-purpose
  - Prototype only
- Source: [TechXplore](https://techxplore.com/news/2025-12-optical-chip-boost-tier-nvidia.html)

#### MIT -- Integrated Photonic Processor
- Published in *Nature Photonics* (Dec 2024)
- Fully integrated optical deep neural network on-chip
- All key operations (linear + nonlinear) done optically
- Sub-nanosecond inference latency
- 96% training accuracy, 92% inference accuracy
- Nonlinear Optical Function Units (NOFUs): siphon small amount of light to photodiodes for nonlinear activation -- minimal energy
- Fabricated with commercial CMOS foundry techniques
- **Significance:** First fully integrated photonic processor with on-chip nonlinear activation -- eliminates the usual optical-to-electronic conversion bottleneck for nonlinearity
- Source: [MIT News](https://news.mit.edu/2024/photonic-processor-could-enable-ultrafast-ai-computations-1202)

---

## 4. Performance Numbers: What Has Actually Been Measured

### The Numbers Everyone Cites

| Chip/System | Claimed TOPS/W | Precision | What They Don't Tell You |
|-------------|---------------|-----------|--------------------------|
| Tsinghua Taichi | 160 TOPS/W | Low (analog) | Likely excludes laser, DAC/ADC, control electronics |
| Neurophos OPU | 300 TOPS/W | FP4/INT4 | No third-party verification; product not yet built |
| Lightmatter Envise | ~820 TOPS/W (ABFP16) | ABFP16 | 78W electrical + 1.6W optical for chip; system power higher |
| LightGen | 100x A100 | Analog | Prototype; narrow generative tasks only |
| Q.ANT NPU 2 | ~0.05 TOPS/W | 8-bit analog | 8 GOPS at 150W; orders of magnitude behind GPUs |
| MIT integrated | N/A (sub-ns latency) | ~4-6 bit effective | Small-scale demonstration |

### Actually Measured (Published, Peer-Reviewed)

- **1.28 TOPS** on a 16-channel coherent MZI photonic processor (Science Advances, 2025)
- **8.19 TOPS** throughput, 4.21 TOPS/W (excluding lasers) / 2.38 TOPS/W (including lasers) -- from a large-scale photonic accelerator (Nature, 2025)
- **8 GOPS** from Q.ANT NPU 2 at 150W (commercial product, 2025)
- **0.196 TOPS** from microring resonator crossbar at 9.83 GS/s (academic, 2025)

### For Context: NVIDIA H100

- 3,958 TOPS (INT8) at ~700W = **~5.7 TOPS/W (INT8)**
- 989 TFLOPS (FP16 Tensor) at ~700W = **~1.4 TFLOPS/W (FP16)**

### The Precision Problem in Benchmarking

Photonic chips typically operate at 4-8 bit effective precision. Comparing a 4-bit photonic TOPS number to an 8-bit or 16-bit GPU TOPS number is misleading. At equivalent precision:

- A "160 TOPS/W at 4-bit" is roughly equivalent to "40 TOPS/W at 8-bit" (halving bits roughly halves the effective operations)
- Even then, the photonic number often excludes system overhead

**The only fair comparison is: total system power for a complete inference task at equivalent output quality.** No photonic chip has published this comparison on a standard benchmark (MLPerf or equivalent).

---

## 5. The Fundamental Challenges

### 5.1 The DAC/ADC Bottleneck

This is the single biggest challenge for photonic compute. Every photonic processor must:

1. **Convert digital inputs to analog optical signals** (DAC -> electrical modulator -> optical)
2. **Perform optical computation** (the "free" part)
3. **Convert optical outputs back to digital** (photodetector -> ADC -> digital)

The DAC/ADC conversion dominates the energy budget. Research shows:
- With current technology, you cannot reliably exceed ~4-bit precision for all-optical ADCs
- DAC/ADC power consumption can exceed the power saved by optical computation
- Each layer of a neural network requires a full round-trip: digital -> optical -> compute -> optical -> electrical -> digital

**Emerging solutions:**
- PCM-based (phase-change material) DACs/ADCs enabling direct digital-optical conversion with ~40% DAC and 70-98% ADC power reduction
- Photonic ADC architectures that use optical sampling to overcome electronic timing jitter
- Compute-in-memory approaches that reduce the frequency of domain crossings

### 5.2 The Nonlinearity Problem

Neural networks require nonlinear activation functions (ReLU, GELU, etc.) between layers. Light is inherently linear -- that is what makes it good for matrix multiplication, but it also means:

- Most photonic neural networks use **opto-electronic conversion for nonlinearity**: optical signal -> photodetector -> electronic nonlinear function -> modulator -> back to optical
- This kills the speed and efficiency advantage because you leave the optical domain at every layer
- All-optical nonlinearity is extremely difficult to achieve efficiently

**Current approaches to optical nonlinearity:**
- MIT's NOFUs: siphon small light amount to photodiodes (hybrid, minimal energy, but still opto-electronic)
- Saturable absorption in 2D materials (MoTe2): ultra-broadband, low threshold (0.94 uW), ultra-fast (2.08 THz), ~50 um^2
- Periodically poled lithium niobate (PPLN): second-order nonlinearity, ~80% conversion efficiency
- Stimulated Brillouin scattering: coherent, frequency-selective, optically tunable
- Microring resonator optical bistability
- Q.ANT's lithium niobate: native nonlinearities in the material

**None of these are yet mature enough for production all-optical neural networks with arbitrary activation functions.**

### 5.3 Precision and Noise

- Analog photonic computation is fundamentally limited by signal-to-noise ratio (SNR)
- Bit precision = log2(number of separable optical power levels at output)
- Typical effective precision: **4-8 bits** for current photonic systems
- Increasing precision requires more laser power (to improve SNR), which consumes more energy
- Manufacturing variations (waveguide width, coupling gaps) add systematic errors
- Temperature fluctuations shift resonances and phase responses

**The saving grace:** Neural networks are tolerant of low precision. Inference at INT4-INT8 is increasingly standard. Research shows optical neural networks can achieve 99% accuracy on MNIST with ~3.1 detected photons per weight multiplication -- extreme noise tolerance.

**Hardware-aware training** (training the model to account for the specific noise profile of the photonic hardware) significantly improves effective precision.

### 5.4 Thermal Sensitivity

Silicon photonics components are extremely temperature-sensitive:
- Silicon microring resonators: ~80 pm/C resonance shift
- MZI phase shifters: continuous thermal drift
- Lightmatter's solution: "dedicated mixed-signal circuits" actively controlling ~1 million photonic elements
- This thermal management overhead eats into the energy efficiency advantage

### 5.5 Scaling

- MZI meshes: N^2 elements for N x N matrix, with cascading insertion loss
- Microring arrays: thermal crosstalk between adjacent rings becomes worse at density
- Free-space systems (LightGen, Lumai): inherently difficult to miniaturize and manufacture at scale
- Signal fan-out: splitting an optical signal to multiple destinations weakens it (unlike electronic signals that can be regenerated with buffers)
- No optical equivalent of SRAM -- you cannot store weights optically; they must be encoded in physical structures (phase shifters, ring tuning) or refreshed continuously

### 5.6 Manufacturing and Integration

- Silicon photonics can be made in existing CMOS foundries (GlobalFoundries, TSMC, Tower) -- this is the most mature path
- Lithium niobate (Q.ANT): niche foundry process, not mainstream
- Free-space optics (Lumai, LightGen): requires precision alignment, difficult to mass-produce
- Metamaterial modulators (Neurophos): claimed to be foundry-compatible but unproven at scale
- Co-packaging photonics with electronics (CPO) is an active R&D area with significant progress (NVIDIA, Lightmatter, Ayar Labs)

---

## 6. Photonic vs. Electronic Analog

Both photonic and electronic analog computing exploit continuous physical quantities for computation. How do they compare?

| Dimension | Electronic Analog (e.g., crossbar ReRAM/PCM) | Photonic Analog |
|-----------|----------------------------------------------|-----------------|
| **Compute medium** | Current/voltage through resistive elements | Light amplitude/phase through waveguides |
| **Speed** | Limited by RC time constants (~ns-us) | Speed of light (~ps for on-chip propagation) |
| **Energy per MAC** | ~fJ-pJ (very competitive) | ~fJ for optical part, but DAC/ADC adds pJ-nJ |
| **Precision** | 4-8 bits typical, limited by device variation | 4-8 bits typical, limited by SNR and noise |
| **Nonlinearity** | Naturally available (transistor characteristics) | Very difficult; requires special materials or O/E conversion |
| **Memory** | Weights stored in-situ (ReRAM/PCM/Flash) | No optical memory; weights encoded in tunable devices |
| **Programming** | Write resistance values (can be slow, has endurance limits) | Tune phase shifters or ring resonances (fast, unlimited) |
| **Temperature sensitivity** | Moderate (resistance drift) | Severe (resonance/phase drift in silicon photonics) |
| **Manufacturing** | Standard CMOS-compatible (for most) | Silicon photonics is CMOS-compatible; others are not |
| **Bandwidth scaling** | Limited by interconnect | WDM enables massive parallelism on single waveguide |
| **Biggest advantage** | In-memory compute eliminates data movement | Speed of light; WDM parallelism; no resistive heating |
| **Biggest limitation** | Write endurance; precision; stuck-at faults | DAC/ADC bottleneck; no memory; nonlinearity |

**Key insight:** Electronic analog (CIM) and photonic analog are complementary, not competing. The most likely winning architecture may combine:
- Photonic interconnect (data movement)
- Electronic analog or digital compute (the actual MAC operations)
- Or: photonic MAC with electronic nonlinearity and memory (hybrid)

Photonic compute has a theoretical speed advantage but a practical integration disadvantage. Electronic analog has worse speed but better integration with the rest of the digital system.

---

## 7. The Interconnect Story (Where Photonics Actually Wins Today)

While photonic compute is still proving itself, photonic interconnect is already commercially validated. This is the part of the photonic AI story that is real and shipping.

### The Problem Photonic Interconnect Solves

- FLOPS have improved 60,000x in 20 years; DRAM bandwidth only 100x; interconnect only 30x
- At 224 Gbps per lane (2024-2025), copper cable reach dropped below 1 meter -- the "Copper Wall"
- AI training clusters need thousands of GPUs communicating at high bandwidth
- Electrical interconnects: ~1-10 pJ/bit at rack scale
- Optical interconnects: ~0.05-0.2 pJ/bit -- **10-50x more efficient**

### What Is Shipping / Near-Shipping

| Company | Product | Bandwidth | Status |
|---------|---------|-----------|--------|
| NVIDIA | Quantum-X Photonics | 144x 800G ports | Late 2025 |
| NVIDIA | Spectrum-X Photonics | Ethernet CPO | 2026 |
| Lightmatter | Passage M1000 | 114 Tbps | Summer 2025 |
| Lightmatter | Passage L200 | 200+ Tbps per package | 2026 |
| Ayar Labs | TeraPHY UCIe | 8 Tbps per chiplet | Samples 2026, volume 2027-2028 |
| Celestial AI/Marvell | Photonic Fabric Module | 16 Tbps per chiplet | Revenue late 2028 |
| iPronics | ONE-32 OCS | Optical circuit switch | Shipping to first customers 2025-2026 |

### The Implications

Photonic interconnect enables larger AI training clusters by solving the bandwidth and power wall. This is not about computing with light -- it is about moving data with light. And it works.

The market (per Yole Group): $50M in 2027 -> $3B in 2034 for optical processors broadly. But photonic interconnect for data centers is already a multi-billion-dollar market.

---

## 8. Honest Assessment: Timeline and Viability

### What Is Real Today (2025-2026)

- **Photonic interconnect / CPO:** Commercially real. NVIDIA shipping switches. Lightmatter, Ayar Labs shipping or sampling products. Multiple hyperscalers evaluating. This will be standard infrastructure by 2028.
- **Photonic compute demonstrations:** Lab results are impressive (sub-nanosecond inference, high TOPS/W on narrow tasks). But no production deployment for real AI workloads.

### What Is 2-3 Years Away (2027-2028)

- **First commercial photonic compute products:** Q.ANT is shipping (at 8 GOPS -- toy scale). Neurophos targets pilot in 2027, systems in 2028. Lightmatter Envise has customer samples but no public production deployment.
- **Hybrid opto-electronic accelerators:** Most likely near-term path. Photonic MACs with electronic nonlinearity, memory, and control. This is what Lightmatter, Lightelligence, and Luminous Computing are building.

### What Is 5+ Years Away (2030+)

- **All-optical neural network inference:** Requires mature optical nonlinearities, optical memory (or at minimum elimination of per-layer O/E/O conversion), and manufacturing at scale. MIT's work is promising but still academic.
- **Photonic training:** Even harder than inference. Training requires higher precision, gradient computation, and weight updates -- all extremely challenging in the optical domain.

### What May Never Work

- **All-optical general-purpose AI compute** replacing GPUs: The DAC/ADC bottleneck, lack of optical memory, and nonlinearity problem may be fundamental rather than engineering challenges. Every time you need to interact with digital memory or perform a nonlinear operation, you lose the photonic advantage.
- **The "100x faster than GPU" claims** at system level for real workloads: These are almost always measured on narrow tasks, at low precision, excluding system overhead. For a complete LLM inference pipeline, the advantage is likely to be far smaller.

### The Smartest Bet

The photonic AI chip companies that will succeed are the ones that have **pivoted to interconnect first** (Lightmatter, Ayar Labs, Celestial AI). They generate revenue now while photonic compute matures. The pure-play photonic compute companies (Neurophos, Q.ANT, Lumai) carry much higher risk.

The industry consensus emerging in 2025-2026:
1. **Interconnect first** (2025-2028): Replace copper with photonic links between electronic AI chips
2. **Hybrid compute** (2028-2032): Photonic MACs with electronic control, memory, and nonlinearity
3. **All-optical compute** (2032+, if ever): Requires breakthroughs in optical nonlinearity and memory

### Key Quote

From the World Economic Forum (Aug 2025): *"While most interviewees expressed skepticism about near-term all-optical computing, some companies remain confident that fundamental barriers can be overcome, particularly through digital optical approaches rather than analog ones."*

From industry analysis: *"The main challenge for any photonic technology is to validate high enough reliability. You can make nice prototypes and proof of concepts, but to create a product, you need to demonstrate that your technology can operate for three to five years or more."*

---

## 9. Sources

### Company Sources
- [Lightmatter - A New Kind of Computer (blog)](https://lightmatter.co/blog/a-new-kind-of-computer/)
- [Lightmatter Passage M1000 Press Release](https://lightmatter.co/press-release/lightmatter-unveils-passage-m1000-photonic-superchip-worlds-fastest-ai-interconnect/)
- [Lightmatter Passage L200 Press Release](https://lightmatter.co/press-release/lightmatter-announces-passage-l200-the-fastest-co-packaged-optics-for-ai/)
- [Lightmatter Series D ($4.4B valuation)](https://lightmatter.co/press-release/lightmatter-raises-400m-series-d-quadruples-valuation-to-4-4b-as-photonics-leader-for-next-gen-ai-data-centers/)
- [Lightmatter Envise Product Page](https://lightmatter.co/products/envise/)
- [Ayar Labs UCIe Optical Chiplet](https://ayarlabs.com/news/ayar-labs-unveils-worlds-first-ucie-optical-chiplet-for-ai-scale-up-architectures/)
- [Ayar Labs $500M Series E](https://ayarlabs.com/news/ayar-labs-closes-500m-series-e-accelerates-volume-production-of-co-packaged-optics/)
- [Celestial AI Photonic Fabric Module at Hot Chips 2025](https://www.servethehome.com/celestial-ai-photonic-fabric-module-at-hot-chips-2025/)
- [Marvell acquires Celestial AI ($5.5B)](https://investor.marvell.com/news-events/press-releases/detail/1000/marvell-to-acquire-celestial-ai-accelerating-scale-up-connectivity-for-next-generation-data-centers)
- [NVIDIA Spectrum-X / Quantum-X Photonics](https://nvidianews.nvidia.com/news/nvidia-spectrum-x-co-packaged-optics-networking-switches-ai-factories)
- [NVIDIA Silicon Photonics Technical Blog](https://developer.nvidia.com/blog/a-new-era-in-data-center-networking-with-nvidia-silicon-photonics-based-network-switching/)
- [Q.ANT NPU 2](https://qant.com/photonic-computing/)
- [Q.ANT NPU 2 Press Release](https://qant.com/press-releases/q-ant-unveils-its-second-generation-photonic-processor-to-power-the-next-wave-of-ai-and-hpc/)
- [Neurophos $110M Series A (SiliconANGLE)](https://siliconangle.com/2026/01/22/chip-startup-neurophos-gets-110m-replace-electrons-photons-accelerate-ai-compute/)
- [Lightelligence (36kr profile)](https://eu.36kr.com/en/p/3452345776231816)
- [iPronics Series A](https://ipronics.com/ipronics-raises-20m-in-series-a-to-advance-optical-networking-for-next-gen-ai-data-centers/)
- [Lumai $10M funding](https://optics.org/news/16/4/7)

### Academic / Research Sources
- [Tsinghua Taichi: 160 TOPS/W photonic chiplet (Science, 2024)](https://www.science.org/doi/10.1126/science.adl1203)
- [MIT Photonic Processor (Nature Photonics, 2024)](https://news.mit.edu/2024/photonic-processor-could-enable-ultrafast-ai-computations-1202)
- [LightGen all-optical chip (TechXplore)](https://techxplore.com/news/2025-12-optical-chip-boost-tier-nvidia.html)
- [Complex-valued MVM on coherent photonic processor (Science Advances, 2025)](https://www.science.org/doi/10.1126/sciadv.ads7475)
- [Photonic matrix multiplication review (Nature Light: Sci & App)](https://www.nature.com/articles/s41377-022-00717-8)
- [Microring resonator neural networks (Intelligent Computing)](https://spj.science.org/doi/10.34133/icomputing.0067)
- [Silicon photonic deep learning engines with dynamic precision (Nanophotonics)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11501591/)
- [Photonic neural networks and optics-informed deep learning (APL Photonics)](https://pubs.aip.org/aip/app/article/9/1/011102/3161086)
- [Quantum-noise-limited optical neural networks (Nature Comms)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10635295/)
- [Photonic-Electronic Integrated Circuits for HPC and AI (arXiv)](https://arxiv.org/html/2403.14806v2)
- [Integrated PCM-based DAC/ADC for photonic computing (SPIE, 2025)](https://ui.adsabs.harvard.edu/abs/2025SPIE13581E..0BA/abstract)
- [MZI comprehensive model (Nature Comms Physics, 2025)](https://www.nature.com/articles/s42005-025-02176-0)
- [All-optical nonlinear activation via PPLN (eLight, 2026)](https://link.springer.com/article/10.1186/s43593-026-00125-0)
- [MoTe2 ultra-broadband optical nonlinear activation (Nature Comms, 2024)](https://www.nature.com/articles/s41467-024-53371-6)

### Industry Analysis
- [SPIE: Illuminating AI - Can optical neural networks deliver AGI? (2025)](https://spie.org/news/photonics-focus/julyaugust-2025/optical-computing-illuminating-ai)
- [WEF: How photonic computing can move towards commercialization (2025)](https://www.weforum.org/stories/2025/08/photonic-computing-promise-commercialization/)
- [IEEE: Silicon Photonics for Scalable and Sustainable AI Hardware (2025)](https://ieeephotonics.org/announcements/2025ieee-study-leverages-silicon-photonics-for-scalable-and-sustainable-ai-hardwareapril-3-2025/)
- [Nature: Photonic chips provide a processing boost for AI (2025)](https://www.nature.com/articles/d41586-025-00907-5)
- [Photonics21: AI desperately needs photonics (whitepaper, 2025)](https://www.photonics21.org/download/news/2025/Photonics_for_AI_final.pdf)
- [Photonic Computing Primer (State of the Future, Substack)](https://stateofthefuture.substack.com/p/the-state-of-photonic-computing)
- [Lightmatter Contrary Research report](https://research.contrary.com/company/lightmatter)
- [Photonic Chips Going Mainstream (Intelligent Living)](https://www.intelligentliving.co/photonic-chips-data-center-networking/)
- [Lam Research: Silicon Photonics for AI](https://newsroom.lamresearch.com/silicon-photonics-ai-energy-efficiency)
- [Nature npj Nanophotonics: Photonics to scale AI data centers (2025)](https://www.nature.com/articles/s44310-025-00105-1)

---

*Last updated: 2026-03-22*
