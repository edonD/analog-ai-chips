# Novel & Unconventional Analog AI Approaches (2025-2026)

Beyond the established analog compute-in-memory paradigm (RRAM, PCM, flash, capacitor), a constellation of radically different computing substrates is being explored for AI workloads. This file covers the weird, the wild, and the potentially transformative.

**Bottom line:** Most of these are 5-15 years from production. But thermodynamic/probabilistic computing has real silicon, reservoir computing has a working prototype from TDK, and FeFET CIM is on the cusp of commercial viability. The $475M bet on Unconventional AI signals that serious money believes analog's second wave is coming.

---

## 1. Thermodynamic Computing — The Hottest "Cool" Idea

### The Core Concept

Instead of fighting thermal noise (as conventional chips do), thermodynamic computing *harnesses* it. The physics of thermal fluctuations, dissipation, and stochastic transitions become the computation itself. This is fundamentally suited to probabilistic AI workloads — diffusion models, Bayesian inference, generative sampling — where you *want* randomness.

### Extropic AI

- **Founded:** 2023 by Guillaume Verdon (ex-Alphabet X quantum tech lead)
- **Funding:** $14.1M seed (Dec 2023), led by Kindred Ventures. Angel investors include Shopify CEO Tobias Lutke, Cohere co-founders, Y Combinator CEO Garry Tan
- **Location:** Austin, TX

**Hardware: Thermodynamic Sampling Unit (TSU)**

The TSU is built from networks of **p-bits** (probabilistic bits) — circuits whose output voltage randomly wanders between two states with programmable probability. Higher-order circuits include:
- **p-dit:** categorical sampler
- **p-mode:** Gaussian sampler
- **p-MoG:** mixture-of-Gaussians generator

Communication is purely local (physically adjacent circuits only), minimizing data movement energy.

**Roadmap:**
| Chip | Timeline | Description |
|------|----------|-------------|
| X0 | Q1 2025 | Silicon prototype — validates physics of all-transistor probabilistic circuits |
| XTR-0 | Q3 2025 | Dev platform — CPU + FPGA motherboard with two TSU sockets |
| Z1 | Early 2026 | First production-scale TSU — hundreds of thousands of sampling cells/chip |

**Claimed efficiency:** ~10,000x lower energy per sample vs. GPU on Fashion-MNIST-scale generation tasks. This is based on simulations/models and prototype micro-measurements, *not* system-level benchmarks.

**The catch:** The 10,000x claim compares energy-per-flip of a p-bit against a floating-point add on a GPU. This is not an apples-to-apples workload comparison. A sampling "flip" and a FP32 multiply-accumulate do fundamentally different things. Until Extropic runs the same generative model end-to-end on TSU vs. GPU and publishes wall-clock time and total energy, the 10,000x number is a physics comparison, not a system benchmark. They have working silicon (X0 exists), but no published real-world benchmarks as of early 2026.

### Normal Computing

- **Founded:** 2022
- **Funding:** $8.5M seed (Jun 2023) from Celesta Capital, Samsung NEXT, Micron Ventures, Drive Capital
- **Location:** New York

**Hardware: CN101 — "World's First Thermodynamic Computing Chip"**

Taped out August 2025 (announced). Implements Normal's **Carnot architecture** — uses physical dynamics (thermal fluctuations, controlled dissipation, stochastic transitions) to compute.

**Target workloads:**
1. Linear algebra / matrix operations
2. Stochastic sampling with lattice random walk

**Claimed efficiency:** Up to 1,000x on targeted AI and scientific workloads.

**Roadmap:**
| Chip | Timeline |
|------|----------|
| CN101 | 2025 (tape-out, entering characterization) |
| CN201 | 2026 |
| CN301 | 2028 (targeting higher-resolution diffusion/video models) |

**The catch:** CN101 is in characterization — no published benchmarks yet. The 1,000x claim is a design target, not a measured result. Normal has an interesting dual business: they also sell EDA software using probabilistic methods, which generates revenue while the hardware matures. Smarter business model than pure-play chip startups.

### Unconventional AI — The $475M Elephant

- **Founded:** September 2025 by Naveen Rao (ex-Databricks VP AI, ex-Intel/Nervana founder, Brown PhD in neuroscience)
- **Funding:** $475M seed at $4.5B valuation (Dec 2025). Co-led by a16z and Lightspeed. Jeff Bezos, Sequoia, Lux Capital, DCVC also participated. Rao personally invested $10M.
- **Location:** San Francisco

**Approach:** Building "a computer as efficient as biology" — silicon circuits that exhibit non-linear dynamics similar to biological neurons, running neural networks "on the physics directly" rather than simulating them digitally.

**Target:** 1,000x improvement in energy efficiency. Neuromorphic/analog hybrid, fabbed in standard silicon.

**Status as of March 2026:** Pre-silicon. Building a "silicon wind tunnel" — a software interface to their hardware physics. Research prototypes expected mid-2026.

**The catch:** This is the most overfunded pre-silicon company in the history of chip design. $475M seed with zero hardware, zero benchmarks, and only a vague description of the technology. Rao's track record (Nervana sold to Intel for $408M, MosaicML to Databricks for $1.3B) is why investors wrote checks. But the technology description — "leverage the intrinsic physics of circuits" — could describe anything from analog CIM to thermodynamic computing to neuromorphic. No published architecture, no papers, no prototypes. The $4.5B valuation is 100% founder premium.

**Why it matters anyway:** If this attracts top talent and actually produces silicon that works, it could validate the entire unconventional computing space. And $475M buys a *lot* of tape-outs.

---

## 2. Probabilistic Computing with P-bits

### The Concept

P-bits are the probabilistic counterpart to classical bits (deterministic 0/1) and qubits (quantum superposition). A p-bit rapidly fluctuates between 0 and 1 with tunable probability. Networks of interacting p-bits can naturally perform:
- Boltzmann machine sampling
- Combinatorial optimization (Ising model)
- Bayesian inference
- Integer factorization

The key insight: p-bits need *no* cryogenic cooling (unlike qubits) and operate at room temperature in standard CMOS or MRAM.

### Academic Progress (UCSB + Tohoku + TSMC)

**Kerem Camsari** (UCSB, formerly Purdue) is the leading academic researcher. Key 2025 milestones:

1. **DAC-free p-bit design (IEDM 2025, Dec 2025):** Collaboration with Tohoku University and TSMC. Eliminates digital-to-analog converters from p-bit circuits using stochastic magnetic tunnel junctions (MTJs) + digital timing circuits. This is huge — DACs were the scalability bottleneck.

2. **Scalable ASIC (Northwestern, Nature Electronics 2025):** Voltage-controlled MTJs as entropy source. Demonstrated synchronized architecture where all p-bits update in lockstep, matching performance of asynchronous designs while being far more manufacturable.

3. **P-computers beating quantum annealers:** Published results showing probabilistic computers matching or exceeding quantum annealer performance on hard combinatorial optimization problems — at room temperature, with standard fab processes.

### Hardware Implementations

| Implementation | Technology | Key Metric |
|---|---|---|
| MTJ-based p-bit (Tohoku/UCSB) | Stochastic MRAM | Millions of flips/sec at fJ/flip |
| Digital CMOS p-bit (IEDM 2025) | Standard CMOS + MTJ | DAC-free, foundry-compatible |
| Chaotic oscillator p-bit | CMOS ring oscillator | True random, correlation-free |
| RRAM-based p-computer | HfO2 RRAM | Demonstrated molecular docking |
| MoS2 + MTJ hybrid | 2D material + spintronics | On-chip p-bit core demonstrated |

**The catch:** No commercial product exists. The MTJ-based designs require MRAM-capable foundries (available at Samsung, TSMC, GlobalFoundries). The main limitation is scale — demonstrations are at 8-48 p-bits. Useful probabilistic computers need thousands to millions. The DAC-free IEDM 2025 result is the key enabler for scaling.

**Assessment:** This is real physics with working hardware. The question is whether it finds a killer app before digital GPUs just get better at running probabilistic algorithms in software (which is what's happening with diffusion models today).

---

## 3. Reservoir Computing Chips

### The Concept

Reservoir computing exploits the complex, nonlinear dynamics of a physical system (the "reservoir") to transform temporal input signals into a high-dimensional feature space. Only the output layer needs training — the reservoir itself is fixed. This means:
- No backpropagation through the reservoir
- Extremely fast training (seconds, not hours)
- Ideal for time-series processing at ultra-low power

### TDK — First Commercial Prototype

- **Announced:** October 2025, exhibited at CEATEC 2025 (won Innovation Award)
- **Collaboration:** Hokkaido University

**Specifications:**
| Parameter | Value |
|-----------|-------|
| Cores | 4 |
| Nodes per core | 121 (484 total) |
| Topology | Simple cycle (nodes in one big loop) |
| Node components | Nonlinear resistor + MOS capacitor (memory) + buffer amplifier |
| Power per core | **20 µW** |
| Total power | **80 µW** |

**Demonstration:** Predicts human hand motion (rock-paper-scissors) in real-time when paired with TDK accelerometer sensors. The chip learns individual motion patterns on-device, without cloud processing.

**The catch:** 484 nodes is tiny. This handles simple time-series classification, not computer vision or language. But for wearable/IoT applications where you need real-time adaptation to individual users at micropower budgets, this is genuinely useful. The 80 µW total power is competitive with Aspinity's AML200 for always-on sensing.

### Other Physical Reservoir Substrates

The diversity of materials being explored as reservoirs is remarkable:

| Substrate | Key Property | Status |
|-----------|-------------|--------|
| **Memristor networks** | Nonlinear I-V + memory | 1000x lower power than digital RC (Nature Electronics 2022) |
| **Spintronic oscillators** | Magnetization dynamics follow tanh function | Analytical nonlinearity control (PhysRev 2025) |
| **Photonic reservoirs** | 200 TOPS, >60 GHz processing | Silicon photonic RC processor demonstrated |
| **Carbon nanotube networks** | Random percolation network = rich dynamics | Lab-scale only |
| **Atomic switch networks** | Self-organizing nanowire junctions | Lab-scale only |
| **FeFET devices** | Ferroelectric hysteresis as reservoir | Demonstrated on silicon platform |
| **VO2 phase-change oscillators** | Metal-insulator transition at 68°C | CMOS-compatible, coupled oscillator networks |

**Photonic reservoir standout:** An ultrafast silicon photonic reservoir computing engine achieved **200 TOPS** at processing speeds over 60 GHz — two orders of magnitude more energy-efficient than digital processors. This is the highest-performance reservoir computing result published.

**Assessment:** Reservoir computing is perfectly matched to always-on edge sensing. TDK bringing this to a chip validates the concept. The limitation is that reservoir computing cannot handle the complex models (transformers, diffusion) that dominate modern AI. It's a niche technology for a niche (but large) market: time-series processing in wearables, robotics, and industrial IoT.

---

## 4. Spintronics for AI — Compute with Magnets

### The Core Idea

Magnetic tunnel junctions (MTJs) — the same devices used in MRAM — can perform computation, not just storage. The key properties:
- Non-volatile (retains state without power)
- Sub-nanosecond switching
- Endurance >10^15 cycles
- CMOS-compatible (Samsung, TSMC, GlobalFoundries all have MRAM processes)

### Lossless Spintronic CIM Macro (Nature Electronics 2025)

The most significant 2025 result: researchers at Southern University of Science and Technology / Xi'an Jiaotong University demonstrated a **64-kb STT-MRAM digital CIM macro** in 40nm:

| Parameter | Value |
|-----------|-------|
| Technology | 40nm STT-MRAM |
| Capacity | 64 kb |
| Precision | 4, 8, 12, and 16 bits (flexible) |
| Computation | **Lossless** matrix-vector multiplication |
| Latency | 7.4-29.6 ns |
| Energy efficiency | **112.3 TOPS/W** |
| Key innovation | Fully parallel, lossless (no accuracy degradation) |

**Why this matters:** "Lossless" means the analog computation introduces zero error — the results are bit-exact with digital computation. This eliminates the precision penalty that plagues RRAM and PCM CIM. At 112.3 TOPS/W, this is competitive with the best SRAM CIM results from ISSCC 2025.

### Spintronic Neuromorphic Computing

Beyond CIM, spintronics enables:
- **Stochastic MTJs as p-bits** (see Section 2 above)
- **Spin-orbit torque (SOT) devices** for ultra-fast synaptic weight updates
- **Domain wall motion devices** for multi-level analog storage
- **Skyrmion-based computing** for topologically protected information processing

A 2025 review in npj Spintronics estimates spintronic neuromorphic systems can achieve **20 TOPS/W** with 3x energy efficiency improvement over conventional accelerators.

### Commercial Status

| Company | MRAM Product | AI CIM Status |
|---------|-------------|---------------|
| Everspin | STT-MRAM (shipping) | No CIM product |
| Samsung | eMRAM at 28nm, 14nm | CIM demo (2022), no product |
| TSMC | eMRAM process available | Foundry service only |
| GlobalFoundries | eMRAM at 22nm FDX | No CIM product |
| Chinese startups | Emerging STT-MRAM fabs | Active CIM research |

**The catch:** Despite excellent CIM macro results, no company is shipping a spintronic CIM product. The 64-kb macro is academic — commercial chips need megabytes. MRAM's primary commercial use remains embedded non-volatile memory (replacing eFlash), not compute. The bit cell is larger than SRAM (making arrays expensive), and write energy is higher than SRAM (though read energy is lower).

**Assessment:** Spintronics is the sleeper technology. The lossless CIM result at 112.3 TOPS/W is genuinely impressive. The MRAM manufacturing ecosystem already exists at major foundries. If someone builds a proper CIM chip (not just a macro) using the existing MRAM processes, this could be the dark horse of analog CIM. The fact that it's *lossless* (digital-equivalent accuracy) while being *non-volatile* (instant-on, zero leakage) is a unique combination no other CIM technology offers.

---

## 5. FeFET/FeRAM Compute-in-Memory — The RRAM Alternative

### Why Ferroelectric?

Ferroelectric FETs (FeFETs) and capacitors (FeCAPs) based on hafnium oxide (HfO2) offer:
- **CMOS compatibility:** HfO2 is already used in every modern transistor as a gate dielectric
- **Low write energy:** femtojoules per bit (fJ/bit)
- **Fast writes:** ~50 ns (10x faster than flash, 100x faster than RRAM)
- **High endurance:** 10^12-10^15 cycles (vs. 10^6-10^8 for RRAM)
- **Non-volatile:** Retains state without power
- **Multi-level capability:** 22+ programmable conductance states demonstrated

### Key 2025 Developments

**FMC (Ferroelectric Memory Company) — Dresden, Germany:**
- Founded 2016 as TU Dresden/NaMLab spinout
- **Raised €100M Series C** (Nov 2025), led by HV Capital + European Innovation Council
- Technology: HfO2-based FeFET and FeCAP memory
- Product lines: **DRAM+** (persistent DRAM replacement) and **Cache+** (SRAM replacement)
- Claims: >100% faster and more efficient than DRAM/SRAM
- Scaling: HfO2 compatibility enables sub-10nm nodes, potentially gigabit-scale FeRAM
- **Building a new fab** in Sulzetal, Saxony-Anhalt (announced Jul 2025)

**Academic CIM Results:**
- FeFET-based CIM annealers for combinatorial optimization (Nature Communications 2024)
- 2D ferroelectric-gated hybrid CIM for high-precision dynamic tracking (Science Advances 2024)
- Thermal expansion-engineered FeFET arrays for edge AI (ACS Nano 2025)
- FeFET reservoir computing on silicon platform demonstrated

### Comparison to Other CIM Technologies

| Property | FeFET | RRAM | Flash | SRAM CIM | STT-MRAM |
|----------|-------|------|-------|----------|----------|
| Write energy | fJ/bit | pJ/bit | nJ/bit | fJ/bit | pJ/bit |
| Write speed | ~50 ns | ~100 ns | ~µs | sub-ns | ~10 ns |
| Endurance | 10^12-10^15 | 10^6-10^8 | 10^4-10^5 | Unlimited | >10^15 |
| Non-volatile | Yes | Yes | Yes | No | Yes |
| CMOS compat. | Excellent (HfO2) | Moderate | Excellent | Native | Good |
| Multi-level | 22+ states | 4-8 states | 16+ states | N/A | 2-4 states |
| Variability | Moderate | High | Low | None | Low |
| Maturity | Pre-commercial | Pre-commercial | Commercial (Mythic) | Commercial | Commercial (memory only) |

**The catch:** Despite excellent properties on paper, FeFET CIM has not been commercialized. The "uncontrolled variations from device to device in nano-scale ferroelectric devices" remain the primary impediment. FMC is focused on memory (DRAM/SRAM replacement), not CIM — though the technology could enable CIM as a second act. The €100M raise and fab plans suggest FMC is the most serious commercial effort.

**Assessment:** FeFET is arguably the best CIM technology on paper — it combines the CMOS compatibility of flash, the endurance of MRAM, the speed approaching SRAM, and non-volatility. If the variability problem is solved at scale, FeFET CIM could leapfrog all current approaches. FMC building a fab is the most bullish signal. Watch for CIM-specific products from FMC or academic spin-outs by 2027-2028.

---

## 6. Coupled Oscillator Networks & Ising Machines

### The Concept

Networks of coupled oscillators naturally minimize energy, which maps directly to solving optimization problems formulated as Ising models. The phase relationships between oscillators encode the solution. This is *not* general-purpose AI — it's specifically for combinatorial optimization (scheduling, routing, portfolio optimization, drug discovery).

### Hardware Implementations

**CMOS Coupled Oscillator Chips:**

| Chip | Technology | Scale | Power | Key Result |
|------|-----------|-------|-------|------------|
| 1440-oscillator chip | 28nm CMOS | 1,440 spins | 319 µW/node | Solves optimization in 950 ns |
| 48-node all-to-all | 65nm CMOS | 48 spins | Low (logic-based coupling) | Arbitrary graphs, integer weights -14 to +14 |
| 65nm Ising chip (2025) | 65nm CMOS | All-to-all connected | Room temperature | More time/energy efficient than quantum annealers |

**VO2 (Vanadium Dioxide) Oscillators:**
- Exploit the metal-insulator phase transition at 68°C
- CMOS-compatible fabrication demonstrated
- Projected power: **13 µW/oscillator**
- Demonstrated on Graph Coloring, Max-cut, Max-3SAT problems
- Converge within 25 oscillation cycles
- Highly reproducible when using HfO2 buffer layer

### Comparison to Other Optimization Approaches

| Approach | Speed | Power | Temperature | Scale |
|----------|-------|-------|-------------|-------|
| Coupled oscillator Ising | ~µs | µW/node | Room temp | ~1,500 spins (current) |
| D-Wave quantum annealer | ~µs | kW (cryogenic) | 15 mK | 5,000+ qubits |
| Simulated annealing (CPU) | ms-s | Watts | Room temp | Millions of variables |
| Coherent Ising Machine (photonic) | ~ms | Watts | Room temp | 100,000 spins |

**The catch:** Current oscillator chips max out at ~1,500 nodes. Real-world optimization problems have millions of variables. Scaling all-to-all connectivity is quadratic in wiring — the same problem that limits crossbar arrays. The 65nm chip beating quantum annealers is notable but at small problem sizes where quantum advantage doesn't exist anyway.

**Assessment:** Interesting physics, real chips, but the scaling problem is unsolved. Photonic Coherent Ising Machines (100,000 spins) and digital simulated annealing are far more practical today. Oscillator Ising machines are a neat academic result, not a commercial path — unless someone cracks the connectivity scaling problem.

---

## 7. In-Sensor Computing — AI at the Pixel

### The Concept

Instead of capturing raw sensor data, digitizing it, and sending it to a processor, in-sensor computing embeds AI directly into the sensor — processing at the pixel level before data ever leaves the chip. This eliminates the sensor-to-processor data bottleneck and enables microsecond-latency, microwatt-power AI.

### Commercial Products (2025)

**PixArt PAC9001 ("Magic Sensor"):**
- AI-driven pixels that perform raw data processing at pixel level
- Reduces data transmission by processing visual information before readout
- Privacy-focused: raw images never leave the sensor
- Targets gesture recognition, presence detection, smart home

**OmniVision OAX8000/OA8000:**
- AI-enabled ASIC for automotive driver monitoring
- Stacked-die: NPU + ISP + 1GB DDR3 on-chip
- Ultra-low-power video AI for battery-powered cameras

**Sony & Samsung (ISSCC 2025):**
- Sony: 25.2MP full-frame global shutter with pixel-parallel ADC (Cu-Cu bonded stacked die)
- Samsung: 3-stacked hybrid-shutter sensor
- Both enabling near-sensor processing through 3D stacking, though not yet "in-sensor computing" in the purest sense

### Academic In-Sensor Computing

Two main architectural approaches:
1. **Heterogeneous integration:** Discrete sensing + computing elements co-located per pixel
2. **Monolithic computational sensors:** Single device that simultaneously senses and computes (using 2D semiconductors, organic materials, perovskites, metal oxides)

**Key materials being explored:**
- 2D transition metal dichalcogenides (MoS2, WSe2)
- Organic electrochemical transistors
- Perovskite photosensitive devices
- Metal oxide memristors with photoelectric properties

### Assessment

In-sensor computing is the *most commercially mature* unconventional approach on this list. PixArt and OmniVision are shipping products. Sony and Samsung are iterating toward it with stacked sensor architectures. The physics advantage is undeniable: if you can make a decision *before* digitizing the full image, you save orders of magnitude in data movement and power.

**The limitation:** Pixel-level compute is limited to simple operations (thresholding, filtering, basic classification). Complex AI still requires a downstream processor. The sweet spot is "wake-on-event" — the sensor detects something interesting and only then activates the full processing pipeline.

---

## 8. Superconducting Neural Networks

### The Concept

Superconducting circuits based on Josephson junctions operate at cryogenic temperatures (4K) but switch at tens to hundreds of GHz with femtojoule energy per operation. Two main logic families:

- **RSFQ (Rapid Single Flux Quantum):** Up to 770 GHz switching, but switching energy only 50x below CMOS
- **AQFP (Adiabatic Quantum Flux Parametron):** Lower speed but extremely low switching energy — 80x better than CMOS *even accounting for cooling overhead*

### Key Results

| System | Technology | Performance |
|--------|-----------|-------------|
| MANA processor | 2.5 GHz AQFP | 80x energy efficiency vs. semiconductor (including cooling) |
| Bistable Vortex Memory arrays | SFQ | 20 GHz matrix-vector multiplication |
| AQFP binary neural network | AQFP + in-memory computing | Reduced memory usage in non-von Neumann architecture |
| 32-bit SFQ processor | SFQ | First 32-bit parallel superconducting chip |

### NSF DISCOVER Program

The NSF is funding the "Design and Integration of Superconducting Computation for Ventures beyond Exascale Realization" (DISCOVER) expedition, specifically targeting superconducting spiking neural networks (SuperSNN).

### Assessment

Superconducting computing is *real and measurably better* on energy efficiency — but the cryogenic requirement (4K = liquid helium) limits it to datacenters willing to invest in cooling infrastructure. The 80x efficiency claim for AQFP (including cooling) is impressive if validated at system scale. The natural fit is HPC/datacenter AI where cooling infrastructure already exists (e.g., quantum computing facilities).

**The catch:** Fabrication is limited to specialized foundries (MIT Lincoln Lab, SeeQC, HYPRES). No TSMC or Samsung equivalent exists for superconducting circuits. Josephson junction density is orders of magnitude below CMOS transistor density. This is a 2030+ technology at best.

---

## 9. Electrochemical & Ionic Computing

### The Concept

Biological brains compute with ions, not electrons. Electrochemical computing attempts to replicate this using devices where ionic motion (Li+, H+, Ag+, etc.) modulates conductance — creating artificial synapses that work like biological ones.

### Key 2025 Result: USC Diffusive Memristors (Nature Electronics)

Researchers at USC developed artificial neurons using **ion-based diffusive memristors** that replicate biological electrochemical behavior:
- Use atomic motion (silver ions) instead of electron flow
- Single device replaces an entire neuron circuit (vs. billions of transistors)
- "Orders of magnitude" reduction in chip size and energy claimed

### Electrochemical Ionic Synapses (EIS)

- Lithium-ion and proton-based devices gaining attention
- High tunability, fast response, energy efficient
- Organic electrochemical transistors (OECTs) enable neural interface + computing in one device

### Assessment

This is the most biologically faithful approach to neural computing — and the furthest from commercial reality. Silver is not CMOS-compatible. Ionic diffusion is inherently slow (milliseconds, vs. nanoseconds for electronic devices). The energy advantage exists but is theoretical until someone builds a system, not a single device.

**Potential:** Medical/biological interfaces where the computing substrate needs to be biocompatible. Brain-computer interfaces. Drug screening. Not general AI compute.

---

## 10. Carbon Nanotubes & 2D Materials

### 3D Integrated CNT Compute (IEDM 2025)

A Stanford-led team built a true 3D integrated circuit combining:
- Silicon CMOS logic (bottom)
- Analog RRAM layer (middle)
- Digital RRAM layers powered by carbon nanotube FETs (top)

**Results:**
- 4x throughput improvement over 2D implementation at same footprint
- Projections: up to 12x with additional tiers
- Potential: 1/17th energy and 119x speed vs. conventional chips
- Fabricated at a US foundry using low-temperature processes

### Why CNTs Matter for Analog AI

Carbon nanotube transistors can be fabricated at low temperature (~200°C vs. >1000°C for silicon), enabling true 3D stacking of compute and memory layers without damaging underlying circuitry. This directly addresses the memory wall that limits all CIM approaches.

### 2D Materials for CIM

- **MoS2 transistors:** Used in MTJ-based p-bit cores (see Section 2)
- **2D ferroelectric-gated devices:** High-precision CIM with dangling-bond-free surfaces
- **Black phosphorus, WSe2:** Explored for in-sensor computing and synaptic devices

### Assessment

CNT 3D integration is the most practical near-term application — it enables denser, more efficient CIM by stacking memory and compute vertically. The IEDM 2025 demo is real hardware from a real foundry. But CNT transistor performance still lags silicon at equivalent nodes, and manufacturing yield remains a challenge. This is a 2028-2030 technology for commercial products.

---

## 11. Diffractive Optical Neural Networks

### The Concept

Instead of using lenses and modulators to perform matrix multiplication (as Lightmatter et al. do), diffractive neural networks use layers of patterned material to transform light as it propagates. Each "layer" diffracts the optical wavefront, performing a nonlinear transformation. Stacking layers creates a deep neural network that operates *at the speed of light* with *zero electronic energy for computation*.

### Key 2025 Results

- **Phase-change metasurfaces:** Programmable diffractive deep neural networks using phase-change materials (PCMs), enabling non-volatile reprogramming
- **Ultra-compact in-memory diffraction chips:** >60,000 parameters/mm², hard parameter sharing across tasks
- **CMOS-compatible fabrication:** Eliminates calibration, enables mass manufacturing
- **10x reduction** in footprint and energy vs. traditional photonic approaches (linear scaling with input dimension instead of quadratic)

### Assessment

Diffractive neural networks are elegant physics but face the same challenges as all optical computing: limited precision (typically 4-6 effective bits from fabrication tolerances), no efficient nonlinear activation function (the biggest unsolved problem), and difficulty interfacing with electronic systems for training and data I/O. The programmable PCM metasurface is a step forward, but this remains firmly academic.

---

## 12. DNA & Molecular Computing

### Status in 2025

- Caltech's DNA-based neural networks classify handwritten digits using strand displacement reactions
- MIT Media Lab developing bio-hybrid CRISPR-DNA logic + neural network platforms
- DARPA Biocomputing Program funding hybrid molecular-electronic devices

### The Hard Truth

DNA reactions take minutes to hours. AI inference takes milliseconds. This is a 6-orders-of-magnitude speed gap that no architectural innovation can close. DNA computing's future is *in vivo* applications — diagnostic circuits running inside cells, molecular controllers for drug delivery — not replacing GPUs.

---

## Ranking: What's Most Promising?

Combining technical readiness, commercial viability, and potential impact:

| Rank | Approach | TRL | Why |
|------|----------|-----|-----|
| 1 | **FeFET/FeRAM CIM** | 4-5 | Best CIM properties on paper. FMC has €100M and building a fab. HfO2 is CMOS-native. If variability is solved, this leapfrogs everything. |
| 2 | **Spintronic (MRAM) CIM** | 4-5 | Lossless 112.3 TOPS/W demonstrated. Manufacturing ecosystem exists at Samsung/TSMC. Missing: a startup willing to build a CIM chip. |
| 3 | **In-sensor computing** | 7-8 | Already shipping (PixArt, OmniVision). Natural analog advantage. Limited to simple tasks but the market (IoT, automotive) is huge. |
| 4 | **Probabilistic/p-bit computing** | 3-4 | Real physics, working demos, DAC-free design solved (IEDM 2025). Extropic and Normal have silicon. No killer app yet beyond optimization. |
| 5 | **Reservoir computing** | 4 | TDK prototype at 80 µW is real. Perfect for time-series edge AI. Too simple for complex models. |
| 6 | **Thermodynamic computing** | 3 | Extropic X0 and Normal CN101 exist in silicon. Claims are extraordinary but unverified. Could be transformative for generative AI if benchmarks hold. |
| 7 | **CNT 3D integration** | 3-4 | IEDM 2025 demo is compelling. Enables better CIM through 3D stacking. Manufacturing readiness is the bottleneck. |
| 8 | **Coupled oscillators/Ising** | 3-4 | Real chips, real results, but scaling to useful problem sizes is unsolved. Photonic CIMs are more practical. |
| 9 | **Superconducting neural nets** | 2-3 | 80x efficiency (incl. cooling) is real. Cryogenic requirement limits to HPC. No commercial fab ecosystem. |
| 10 | **Diffractive optical NNs** | 2-3 | Elegant physics. Precision and nonlinearity unsolved. Academic only. |
| 11 | **Electrochemical/ionic** | 2 | Beautiful biology, terrible engineering. Slow, not CMOS-compatible. Good for bio-interfaces. |
| 12 | **DNA/molecular** | 1-2 | Minutes per operation. Fascinating science, not computing hardware. |

---

## The Meta-Pattern

Every unconventional approach claims to be "inspired by the brain" or "leverage physics instead of fighting it." The pattern that separates real from hype:

1. **Working silicon > simulations.** Extropic, Normal, TDK, the spintronic CIM macro, the oscillator Ising chips — these have hardware. Everything else is projections.

2. **The ADC/DAC problem doesn't go away.** Even unconventional analog approaches need to interface with a digital world. The IEDM 2025 DAC-free p-bit is important precisely because it eliminates this bottleneck.

3. **Manufacturing ecosystem matters more than physics.** FeFET and MRAM CIM are less exotic than thermodynamic computing but are buildable at Samsung and TSMC *today*. The gap between a Nature paper and a commercial chip is 5-10 years and $100M+.

4. **The $475M question.** Unconventional AI's massive funding could either validate the entire space (if they produce working hardware) or become the most expensive lesson in chip design history (if analog's fundamental limits haven't changed). Either way, it attracts talent and attention to the field.

5. **Niche wins before general-purpose.** In-sensor computing is already shipping. Reservoir computing works for time-series. P-bits work for optimization. None of these replace GPUs for training LLMs — but they don't need to. The edge AI market alone is worth $30B+ by 2028.

---

## Sources

- [Extropic — Thermodynamic Computing: From Zero to One](https://extropic.ai/writing/thermodynamic-computing-from-zero-to-one)
- [Extropic TSU deep dive (Vastkind)](https://www.vastkind.com/extropic-thermodynamic-computing-tsu-deep-dive/)
- [Normal Computing CN101 tape-out announcement](https://www.normalcomputing.com/blog/normal-computing-announces-tape-out-of-worlds-first-thermodynamic-computing-chip)
- [Normal Computing CN101 (Tom's Hardware)](https://www.tomshardware.com/tech-industry/semiconductors/worlds-first-thermodynamic-computing-chip-reaches-tape-out-normal-computings-physics-based-asic-changes-lanes-to-train-more-ai)
- [Unconventional AI $475M seed (TechCrunch)](https://techcrunch.com/2025/12/09/unconventional-ai-confirms-its-massive-475m-seed-round/)
- [Unconventional AI technology details (HPCwire)](https://www.hpcwire.com/bigdatawire/2025/12/11/unconventional-ai-wants-to-solve-ai-scaling-crunch-with-analog-chips-will-it-work/)
- [Lightspeed on Unconventional AI](https://lsvp.com/stories/investing-in-unconventional-ai-biology-scale-efficiency-for-the-ai-era/)
- [TDK Analog Reservoir AI Chip](https://www.tdk.com/en/news_center/press/20251002_01.html)
- [TDK Reservoir Chip (IEEE Spectrum)](https://spectrum.ieee.org/analog-reservoir-computer)
- [Lossless spintronic CIM macro (Nature Electronics 2025)](https://www.nature.com/articles/s41928-025-01479-y)
- [Spintronic neuromorphic computing review (npj Spintronics)](https://www.nature.com/articles/s44306-024-00019-2)
- [FMC €100M raise (DCD)](https://www.datacenterdynamics.com/en/news/fmc-raises-100m-for-its-hafnium-oxide-based-memory-chips/)
- [Ferroelectric devices for AI chips (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S2709472325000036)
- [What happened to ferroelectric memories? (Lapedus)](https://marklapedus.substack.com/p/what-ever-happened-to-next-gen-ferroelectric)
- [DAC-free p-bit design (IEDM 2025)](https://techxplore.com/news/2025-12-fully-digital-paves-scalable-probabilistic.html)
- [Northwestern scalable p-computer (Nature Electronics)](https://www.mccormick.northwestern.edu/news/articles/2025/08/a-scalable-probabilistic-computer/)
- [P-computers beating quantum (Nature Communications 2025)](https://www.nature.com/articles/s41467-025-64235-y)
- [RRAM-based probabilistic computer for molecular docking (Nature Communications)](https://www.nature.com/articles/s41467-025-67309-z)
- [Coupled oscillator Ising chip (Nature Electronics 2025)](https://www.nature.com/articles/s41928-025-01393-3)
- [VO2 Ising machine solver (Nature Communications)](https://www.nature.com/articles/s41467-024-47642-5)
- [Silicon photonic reservoir computing 200 TOPS (Nature Communications)](https://www.nature.com/articles/s41467-024-55172-3)
- [Physical reservoir computing tutorial (Natural Computing)](https://link.springer.com/article/10.1007/s11047-024-09997-y)
- [USC electrochemical neurons (Nature Electronics)](https://viterbischool.usc.edu/news/2025/10/artificial-neurons-developed-by-usc-team-replicate-biological-function-for-improved-computer-chips/)
- [CNT 3D chip (Tom's Hardware / IEDM 2025)](https://www.tomshardware.com/tech-industry/semiconductors/stanford-led-team-builds-3d-ai-chip-at-us-foundry-reports-4x-performance-gains)
- [Programmable diffractive neural networks (Scientific Reports 2025)](https://www.nature.com/articles/s41598-025-19638-8)
- [Ultra-compact optical in-memory computing (Light: Science & Applications 2025)](https://www.nature.com/articles/s41377-025-01814-0)
- [Superconducting SNN framework (SuperSNN)](https://arxiv.org/html/2509.05532)
- [AQFP neural network processing unit (IEEE)](https://ieeexplore.ieee.org/document/10014162/)
- [Superconducting computing overview (Frontiers 2025)](https://www.frontiersin.org/journals/materials/articles/10.3389/fmats.2025.1618615/full)
- [Thermodynamic computing (Wikipedia)](https://en.wikipedia.org/wiki/Thermodynamic_computing)
- [Thermodynamic computing (ACM)](https://cacm.acm.org/news/thermodynamic-computing-becomes-cool/)
- [In-sensor computing survey (npj Unconventional Computing 2025)](https://www.nature.com/articles/s44335-025-00040-6)
- [PixArt Magic Sensor](https://cioinfluence.com/machine-learning/pixart-transforms-ai-driven-sensor-technology-with-magic-sensor/)
- [OmniVision OAX8000](https://embeddedcomputing.com/application/consumer/omnivision-announces-release-of-the-oax8000-ai-enabled-asic)
