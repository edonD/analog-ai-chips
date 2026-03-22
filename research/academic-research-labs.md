# Academic Research Labs in Analog/CIM AI Chips

The academic ecosystem driving analog and compute-in-memory (CIM) AI is concentrated in roughly a dozen world-class groups. This file maps the research landscape: who is doing what, which labs spawned companies, what the benchmarks actually show, and where the government funding flows.

---

## Top 10 Academic Groups

### 1. Princeton University — Naveen Verma (Capacitor CIM)

**The group that spawned EnCharge AI.**

Naveen Verma's lab spent six years developing switched-capacitor analog in-memory computing before co-founding EnCharge AI in 2022 with Kailash Gopalakrishnan (former IBM Fellow) and Echere Iroaga. Two former graduate students (Jinseok Lee, Murat Ozatay) joined the company directly from the lab.

- **Key contribution:** Charge-domain CIM using standard CMOS capacitors — no exotic memory needed, best precision among analog approaches (6-8 effective bits), no drift.
- **Funding:** DARPA OPTIMA program awarded $18.6M to Princeton + EnCharge AI in 2024. Princeton's IP Accelerator Fund (2019) was critical early-stage support.
- **Status:** Verma is still a Princeton professor while serving as EnCharge CEO. The lab continues CIM research under DARPA funding.
- **Why it matters:** The cleanest university-to-startup pipeline in analog AI. Capacitor CIM is the architecture most likely to ship at scale.

Sources: [Princeton Engineering](https://engineering.princeton.edu/news/2023/01/27/encharge-ai-reimagines-computing-meet-needs-cutting-edge-ai), [DARPA OPTIMA award](https://www.princeton.edu/news/2024/03/06/new-chip-built-ai-workloads-attracts-18m-government-funding-revolutionary-tech)

---

### 2. IBM Research Zurich + ETH Zurich (PCM-based CIM)

**The strongest corporate-academic partnership in analog AI.**

IBM Research and ETH Zurich co-develop phase-change memory (PCM) based analog in-memory computing. Key personnel include Abu Sebastian (IBM), Manuel Le Gallo (IBM), and Julian Buchel (IBM/ETH). The collaboration produced:

- **HERMES chip** (2023): 64-core PCM CIM chip, 14nm, 35 million PCM devices, 12.4 TOPS/W. Published in Nature Electronics. First large-scale analog CIM demonstration.
- **Analog Foundation Models** (2025): Phi-3-mini and Llama-3.2-1B adapted to tolerate analog noise through noise-injected training and iterative weight clipping. Match W4A8 digital baselines under realistic AIMC conditions. First systematic demonstration that large LLMs can run on analog hardware without catastrophic accuracy loss.
- **Near-Memory Digital Processing Unit (NMPU):** Precision-optimized fixed-point processing co-designed with analog IMC arrays.

- **Key limitation:** PCM suffers from conductance drift (v=0.1-0.15 exponent). This is a physics problem, not an engineering problem — it sets a floor on how good PCM CIM can get.
- **Spinoff connection:** Axelera AI's CTO and co-founder Evangelos Eleftheriou spent 35+ years at IBM Research Zurich. Axelera's scientific advisors include Prof. Marian Verhelst (imec/KU Leuven) and Prof. Luca Benini (ETH Zurich). The company's Leuven office fosters direct collaboration with imec and KU Leuven.

Sources: [IBM & ETH Zurich Analog Foundation Models](https://www.marktechpost.com/2025/09/21/ibm-and-eth-zurich-researchers-unveil-analog-foundation-models-to-tackle-noise-in-in-memory-ai-hardware/), [Semiengineering](https://semiengineering.com/llms-on-analog-in-memory-computing-based-hardware-ibm-research-eth-zurich/)

---

### 3. Tsinghua University — Wu Huaqiang & Gao Bin (RRAM CIM)

**China's leading RRAM CIM group and the force behind the Huawei-ByteDance RRAM chip.**

Wu Huaqiang and Gao Bin at the School of Integrated Circuits lead China's most prolific RRAM CIM program:

- **STELLAR framework** (Science, 2023): World's first fully system-integrated memristor CIM chip supporting efficient on-chip learning. Consumes only 3% of the energy of an equivalent ASIC for on-chip learning.
- **28nm 576K RRAM CIM macro** (2025): Hybrid programming scheme achieving 2.82 TOPS/mm2 area efficiency, 4.67x faster programming, 0.15x power saving vs. prior work.
- **Huawei-ByteDance collaboration** (ISSCC 2026): Joint RRAM AI acceleration chip developed with Tsinghua and Beijing research institutions. Rare corporate alliance presented at ISSCC 2026.

- **Key limitation:** RRAM variability remains the fundamental challenge — cycle-to-cycle and device-to-device variation limits effective precision to 3-5 bits without calibration.
- **Government funding:** Tsinghua benefits from China's massive semiconductor investment: $47.5B Phase III National IC Investment Fund (2024), $8.2B National AI Industry Investment Fund (January 2025), and ~400 billion yuan in government AI capex for 2025.

Sources: [CGTN](https://news.cgtn.com/news/2023-10-11/China-makes-major-breakthrough-in-memristor-computing-in-memory-chips-1nOqlLtvMgE/index.html), [Journal of Semiconductors](https://www.jos.ac.cn/en/article/doi/10.1088/1674-4926/24100017)

---

### 4. Forschungszentrum Julich + RWTH Aachen (Gain Cell CIM for LLMs)

**The group that demonstrated analog attention for LLMs — the most provocative result of 2025.**

Published in Nature Computational Science (September 2025), this team introduced a custom self-attention in-memory computing architecture based on gain cells:

- **Architecture:** Gain cells are CMOS-compatible charge-based memories that can be efficiently written (important for storing new tokens during autoregressive generation) and enable parallel analog dot-product computation for attention.
- **Claimed results:** Up to 70,000x reduction in energy consumption and 100x speed-up vs. GPUs for attention computation on a 1.5B-parameter model. Some reports cite 90,000x energy reduction and 300x latency reduction.
- **Approach:** Designed an initialization algorithm achieving text-processing performance comparable to GPT-2 without training from scratch, working around the non-idealities of analog gain-cell circuits.

- **The catch:** These are simulation results, not silicon measurements. The 70,000x number is for the attention mechanism alone, not full end-to-end inference. The gap between simulation and silicon in analog CIM is typically 10-100x. Still, the approach of using gain cells for attention (where weights change every token, unlike static-weight CIM) is genuinely novel.
- **Funding:** Julich operates Europe's exascale supercomputer JUPITER. The group has EU-level funding and a strong photonic computing collaboration with Q.ANT.

Sources: [Nature Computational Science](https://www.nature.com/articles/s43588-025-00854-1), [FZJ announcement](https://www.fz-juelich.de/en/pgi/news/news/2025/analog_in-memory_computing_attention_mechanism)

---

### 5. Stanford University — H.-S. Philip Wong & Priyanka Raina (RRAM CIM + 3D Integration)

**NeuRRAM and the monolithic 3D future.**

- **NeuRRAM** (Nature, 2022): Co-led with UCSD (Gert Cauwenberghs, Weier Wan). First RRAM CIM chip demonstrating a wide range of AI applications with near-digital accuracy. 99% on MNIST, 85.7% on CIFAR-10 classification, 84.7% on Google speech commands. 1.6-2.3x lower energy-delay product than prior CIM chips, 7-13x higher computational density.
- **Monolithic 3D chip** (December 2025): Stanford, CMU, Penn, MIT, and SkyWater built the first monolithic 3D chip at a US foundry. Carbon nanotube transistors and RRAM stacked vertically. 4x performance gains in hardware tests, simulated potential for 1000x improvement in energy-delay product. Key insight: building layers on top of each other (vs. bonding separate chips) enables far denser vertical interconnects.

- **Philip Wong's broader influence:** Willard R. and Inez Kerr Bell Professor of EE. Research spans RRAM, gain cell memory, oxide semiconductor transistors, and 3D integration. One of the most cited researchers in the field.
- **Priyanka Raina:** Leads Stanford's Agile Hardware Lab focused on accelerator design and generator methodologies.

Sources: [Stanford Report](https://news.stanford.edu/stories/2022/08/new-chip-ramps-ai-computing-efficiency), [Stanford 3D chip](https://news.stanford.edu/stories/2025/12/monolithic-3d-chip-foundry-breakthrough-ai)

---

### 6. Peking University — Sun Zhong & Bonan Yan (High-Precision RRAM)

**Solved the precision problem that haunted analog computing for a century — at least for matrix equations.**

- **Nature Electronics (October 2025):** Demonstrated 24-bit fixed-point precision (comparable to FP32) from 3-bit RRAM devices by combining low-precision matrix inversion with high-precision matrix-vector multiplication and a block matrix algorithm. Improved analog precision by five orders of magnitude (~100,000x) over raw device precision.
- **Performance:** 1,000x faster than Nvidia/AMD GPUs, ~100x less energy. Applied to signal detection in massive MIMO systems, matching FP32 digital processors in 3 iterations.
- **Bonan Yan:** Assistant Professor at PKU's Institute for Artificial Intelligence. Focus on CIM design and AGI processor chips. Also affiliated with Duke University's Center for Computational Evolutionary Intelligence.

- **The catch:** This is a matrix equation solver, not a general-purpose neural network accelerator. The 1,000x claim is for a specific linear algebra workload (Ax=b) where analog's physics advantage is strongest. Generalization to full DNN inference is non-trivial. The "1,000x faster than GPUs" headlines are misleading — it's 1,000x for this specific task.
- **Significance:** Demonstrates that algorithmic techniques can overcome analog's raw precision limits. The iterative refinement approach may be applicable to broader CIM workloads.

Sources: [Nature Electronics](https://www.nature.com/articles/s41928-025-01477-0), [TechXplore](https://techxplore.com/news/2025-10/rram-based-analog-rapidly-matrix.html)

---

### 7. UC San Diego — Gert Cauwenberghs (Neuromorphic + NeuRRAM)

**The bioengineering approach to analog AI.**

Gert Cauwenberghs in UCSD's Department of Bioengineering co-led the NeuRRAM project and leads broader neuromorphic computing research:

- **NeuRRAM** (with Stanford): See entry #5 above. Weier Wan (Stanford PhD, co-advised by Cauwenberghs at UCSD) was lead author.
- **Scaling up neuromorphic computing:** UCSD has announced work on scaling neuromorphic architectures for "efficient and effective AI everywhere and anytime."
- **Research direction:** Brain-inspired computing architectures that maintain accuracy while operating in the analog domain. Strong focus on edge AI applications.

- **University-to-industry pipeline:** NeuRRAM demonstrated the multi-university collaboration model (Stanford + UCSD + multiple others) that is becoming the norm for large CIM chip tapeouts.

Sources: [UCSD Jacobs School](https://jacobsschool.ucsd.edu/news/release/3499), [IEEE Spectrum](https://spectrum.ieee.org/ai-chip)

---

### 8. Georgia Tech — Shimeng Yu (CIM Modeling & Benchmarking)

**The benchmarking standard-setter for CIM.**

Shimeng Yu's Laboratory for Emerging Devices and Circuits provides the most widely used tools for evaluating CIM designs:

- **NeuroSim** (V1.5, 2025): Open-source software framework for benchmarking CIM accelerators with device- and circuit-level non-idealities. Includes case studies with various devices (RRAM, PCM, SRAM, Flash) and compute circuits. Used by dozens of research groups worldwide. This is the closest thing to a standard benchmarking tool in the field.
- **3D integration for CIM** (2025): Co-optimization of power delivery networks for 3D heterogeneous integration of RRAM-based CIM accelerators.
- **DARPA OPTIMA performer:** Georgia Tech is one of the universities awarded under DARPA's $78M OPTIMA program (alongside Princeton/EnCharge, IBM, UCLA, Infineon).

- **Key role:** Yu's group is less about building individual chips and more about creating the modeling infrastructure that the entire field relies on. If you're designing a CIM accelerator, you're probably using NeuroSim.

Sources: [NeuroSim](https://shimeng.ece.gatech.edu/downloads/), [DARPA OPTIMA](https://www.src.org/newsroom/article/2024/1066/)

---

### 9. University of Michigan — Wei Lu (Memristors + Industry Pipeline)

**The lab that spawned Mythic, Crossbar, and MemryX.**

Wei Lu (James R. Mellor Professor of Engineering) has the most productive university-to-startup pipeline in memory-based computing:

- **Mythic AI** (2012): Founded by Dave Fick and Mike Henry as Isocline, a direct spin-out from Michigan's Integrated Circuits Lab. Laura Fick developed Mythic's analog compute technology as part of her Michigan PhD thesis. Renamed Mythic in 2017. Raised $300M+, nearly died in 2022, restructured, now shipping Gen 2.
- **Crossbar Inc.:** Co-founded by Wei Lu. Leader in resistive memory (RRAM) technology.
- **MemryX Inc.:** Co-founded by Wei Lu. Focuses on AI chip acceleration.
- **TetraMem connection:** Fuxi Cai (University of Michigan affiliated) is connected to TetraMem Inc., which develops 11-bit RRAM CIM.

- **Research focus:** RRAM/memristor devices, programmable memristor computers, neuromorphic circuits. Lu's group demonstrated the first programmable memristor computer running three standard ML algorithms.
- **Key insight:** Michigan's Integrated Circuits Lab (MICL) is a repeated source of chip startups — not just in analog AI but across low-power chip design.

Sources: [Michigan MICL](https://micl.engin.umich.edu/), [Mythic origins](https://www.caproasia.com/2025/12/18/united-states-ai-processing-unit-company-mythic-raised-125-million-in-new-funding-founded-in-2012-by-dave-fick-mike-henry-as-isocline-spin-out-from-university-of-michigan-and-renamed-to-mythic-i/)

---

### 10. KU Leuven / imec — Marian Verhelst (Hybrid Digital-Analog + DIANA)

**Where Europe's research infrastructure meets chip design.**

Marian Verhelst holds a dual role as professor at KU Leuven's MICAS laboratory and research director at imec:

- **DIANA chip** (ISSCC 2022): DIgital and ANalog Accelerator — the first hybrid chip combining a precision-scalable digital NN accelerator (16x16 core) with an analog in-memory computing core (1152x512 AiMC array), controlled by a RISC-V host processor. Fabricated by GlobalFoundries. The analog accelerator achieves 10-100x better energy efficiency than the digital accelerator for most operations.
- **imec's broader CIM work:** imec demonstrated an Analog Inference Accelerator (AnIA) reaching 2,900 TOPS/W for vector-matrix multiplications. Projected optimized analog CIM could reach 10,000 TOPS/W.
- **IGZO-based DRAM for CIM:** imec is exploring indium gallium zinc oxide (IGZO) transistor-based DRAM as an alternative memory technology for energy- and area-efficient analog in-memory computing.
- **ISSCC 2026:** imec presented a record 7-bit, 175 GS/s ADC with record-small footprint — relevant to CIM because ADC is the dominant power bottleneck.

- **Current direction:** Verhelst's group is moving toward neuro-symbolic AI hardware that combines neural networks with symbolic reasoning on a single chip. 2025 projects include "Preparing the next wave of AI with integrated neuro-symbolic AI hardware acceleration."
- **Industry pipeline:** Axelera AI (digital CIM, $450M+ raised, $2B+ valuation) has Verhelst as scientific advisor and maintains a Leuven office for direct imec/KU Leuven collaboration.

Sources: [DIANA at ISSCC](https://www.esat.kuleuven.be/micas/index.php/news/465-micas-presents-its-diana-chip-at-isscc2022-paper-15-6), [imec accelerators](https://www.imec-int.com/en/expertise/cmos-advanced/compute/accelerators)

---

## Honorable Mentions

| Group | Key Person | Focus | Notable Result |
|-------|-----------|-------|---------------|
| **UC Santa Barbara** | Dmitri Strukov | Memristor wafer-scale integration | 95% yield on 4-inch memristor crossbar wafer (Nature Communications 2025, with DGIST) |
| **KAIST** | Multiple faculty | STT-MRAM CIM, edge accelerators | STT-MRAM CIM classifier: 94.76% accuracy, <16 us latency for neural implant applications (AICAS 2025) |
| **Delft University** | (Innatera founders) | Neuromorphic analog-mixed-signal | Spin-out Innatera Nanosystems (2018): 500x less energy, 100x faster than conventional for sensor data. $21M raised |
| **Stanford/MIT** | Sara Achour (Stanford), Michael Carbin (MIT) | Programming unconventional substrates | Co-founded Unconventional AI (Sept 2025): $475M seed at $4.5B valuation from Bezos, a16z. Analog chips for biology-scale efficiency |
| **University of Macau** | Sai-Weng Sin, Chi-Hang Chan | Analog/mixed-signal VLSI | 11 papers accepted at ISSCC 2026 as primary affiliation — prolific in data converters relevant to CIM |
| **BUAA (Beihang)** | CI-LAB | SRAM-based CIM | Maintain the most comprehensive curated literature collection on SRAM CIM research |

---

## University-to-Startup Pipeline

This is the most important table in this file. It shows which academic research actually turned into companies:

| University | Lab / Professor | Company | Founded | Tech | Funding | Status |
|-----------|----------------|---------|---------|------|---------|--------|
| **Princeton** | Naveen Verma | **EnCharge AI** | 2022 | Capacitor CIM | $144M+ | Most promising analog CIM startup |
| **U. Michigan** | Dave Fick, Mike Henry (MICL) | **Mythic AI** | 2012 | Flash CIM | $300M+ | Shipping Gen 2, recovered from near-death |
| **U. Michigan** | Wei Lu | **Crossbar Inc.** | — | RRAM | — | RRAM IP licensing |
| **U. Michigan** | Wei Lu | **MemryX Inc.** | — | AI accelerator | — | AI chip company |
| **IBM Zurich / ETH** | Evangelos Eleftheriou | **Axelera AI** | 2021 | Digital CIM | $450M+ | Shipping, $2B+ valuation |
| **Delft University** | (founders) | **Innatera** | 2018 | Neuromorphic analog | $21M+ | Neuromorphic processor |
| **Stanford / MIT** | Sara Achour, Michael Carbin | **Unconventional AI** | 2025 | Analog neuromorphic | $475M | Pre-silicon, $4.5B valuation |
| **KU Leuven / imec** | Marian Verhelst (advisor) | **Axelera AI** | 2021 | Digital CIM | $450M+ | Scientific advisor role |

**Pattern:** The most successful companies come from labs with strong circuits/systems expertise (Michigan MICL, Princeton EE), not from device-physics labs. Knowing how to build a chip matters more than inventing a new memory device.

**The Michigan anomaly:** Three separate companies from one lab. MICL's culture of low-power chip design + entrepreneurship is unique in the field.

---

## imec's Benchmarking Work

imec occupies a unique position as both a research organization and the world's leading semiconductor R&D center (6,600+ employees, 600+ industry partners):

### What Their Comparisons Show

1. **Analog Inference Accelerator (AnIA):** Demonstrated 2,900 TOPS/W for vector-matrix multiplications — but this is a macro-level number, not system-level. At system level, ADC/DAC overhead collapses this dramatically.

2. **Projected ceiling:** imec's analysis projects optimized analog CIM could reach 10,000 TOPS/W. This would be beyond the best digital implementations. However, this is a theoretical projection, not a measured result.

3. **DIANA hybrid approach:** By combining digital and analog on one chip, DIANA showed that 10-100x energy efficiency gains are achievable for the analog portions — but the chip automatically routes operations to whichever coprocessor is best suited. The implication: pure analog is not optimal; hybrid is the practical architecture.

4. **ADC as the bottleneck:** imec's ISSCC 2026 presentation of a 7-bit, 175 GS/s ADC with record-small footprint directly addresses the biggest power bottleneck in analog CIM. Better ADCs = more of the theoretical analog advantage actually reaches the system level.

5. **IGZO-DRAM exploration:** imec is investigating oxide semiconductor (IGZO) transistor-based DRAM as an alternative to SRAM/RRAM for CIM — potentially combining the writability of DRAM with better retention and lower leakage.

### imec's verdict (implicit):
imec invests in both analog and digital CIM but hedges toward hybrid architectures. Their DIANA chip proves the hybrid thesis. Their continued ADC research acknowledges that analog CIM's real-world advantage is gated by data converter efficiency.

---

## Government Funding Sources

### United States

| Program | Agency | Amount | Recipients | Focus |
|---------|--------|--------|-----------|-------|
| **OPTIMA** | DARPA | $78M (max) | IBM, Georgia Tech, UCLA, Princeton/EnCharge, Infineon | CIM accelerators for AI |
| **ERI / ERI 2.0** | DARPA | $1.5B → $3B+ over 5 years | Broad university + industry | Electronics resurgence, includes CIM |
| **NSF Microelectronics** | NSF | Varies | Universities | Advanced microprocessors for AI, ultra-low power edge |
| **EnCharge DARPA grant** | DARPA | $18.6M | Princeton + EnCharge AI | Capacitor CIM for AI workloads |

### Europe

| Program | Agency | Amount | Focus |
|---------|--------|--------|-------|
| **ANIMATE** | ERC (Horizon Europe) | EU-funded | Closed-loop in-memory computing (CL-IMC). 5,000x less energy than digital. Device → circuit → system validation |
| **Chips JU** | EU | Multi-billion EUR (2023-2027) | Next-gen semiconductor R&D including neuromorphic computing, heterogeneous integration |
| **Horizon Europe AI** | EU | EUR 8B+ since 2021 | Broad AI R&D; EUR 1.6B in 2025 work programme |
| **RIGOLETTO** | Chips JU | 3-year (2025-2028) | Automotive computing platform; consortium includes Axelera, NXP, STMicro, Infineon |
| **RAISE** | Horizon Europe | EUR 107M | Virtual AI research institute |

### China

| Program | Amount | Focus |
|---------|--------|-------|
| **National IC Investment Fund Phase III** (2024) | $47.5B | Semiconductor industry broadly; includes AI chip R&D |
| **National AI Industry Investment Fund** (Jan 2025) | $8.2B | AI-specific investment including hardware |
| **National Venture Capital Guidance Fund** | $138B | Broader fund targeting AI, robotics, semiconductors |
| **Total government AI capex (2025)** | ~$56-67B (400B yuan) | Of 600-700B yuan total national AI capex |

**The funding gap:** China's raw dollar commitment to semiconductor R&D dwarfs US and EU programs. However, DARPA's targeted programs (OPTIMA) are more focused on CIM specifically. China's funding is spread across the entire semiconductor value chain.

### South Korea

South Korea has announced a $518B AI strategy that includes semiconductor development, with KAIST as a primary beneficiary for AI chip research.

---

## Key Professors and Research Directions

| Professor | Institution | Direction | Why Watch |
|-----------|------------|-----------|-----------|
| **Naveen Verma** | Princeton / EnCharge | Capacitor CIM, system-level optimization | Most likely to produce a commercially successful analog CIM chip |
| **H.-S. Philip Wong** | Stanford | RRAM, 3D integration, oxide semiconductors | Defining the device physics foundation for next-gen CIM |
| **Shimeng Yu** | Georgia Tech | CIM benchmarking, RRAM modeling, 3D integration | NeuroSim is the field's standard benchmarking tool |
| **Wu Huaqiang** | Tsinghua | RRAM CIM, on-chip learning | Strongest RRAM CIM program; Huawei/ByteDance collaboration |
| **Gert Cauwenberghs** | UCSD | Neuromorphic computing, brain-inspired architectures | NeuRRAM co-lead; bridges bioengineering and chip design |
| **Marian Verhelst** | KU Leuven / imec | Hybrid digital-analog AI, neuro-symbolic HW | DIANA architect; moving toward symbolic+neural fusion |
| **Wei Lu** | U. Michigan | Memristors, programmable analog computers | Three startup spin-outs; fundamental memristor research |
| **Sun Zhong** | Peking University | High-precision analog computing, RRAM | 24-bit precision from 3-bit devices — breakthrough algorithm |
| **Dmitri Strukov** | UC Santa Barbara | Memristor wafer integration, mixed-signal circuits | Wafer-scale memristor fabrication (95% yield) |
| **Sara Achour** | Stanford → Unconventional AI | Programming analog/quantum/neuromorphic substrates | $475M to build analog chips for datacenter-scale AI |
| **Bonan Yan** | Peking University | CIM design for AGI processors | Rising star in CIM architecture; PKU + Duke affiliation |
| **Priyanka Raina** | Stanford | Agile hardware design, accelerator generators | Monolithic 3D chip; automated design for CIM |

---

## Upcoming Results to Watch

### Chips in Fabrication / Papers in Preparation

1. **Huawei-ByteDance-Tsinghua RRAM chip** — Presented at ISSCC 2026. Details on 66x CPU speed claims need independent verification. Watch for the full paper.

2. **Unconventional AI first silicon** — $475M seed round (Dec 2025) with zero silicon. First tapeout expected 2026-2027. If Sara Achour and Michael Carbin can translate their programming-language approach to analog substrates into real chips, it could change the field. If not, it's the most expensive vaporware in analog AI history.

3. **EnCharge EN200 / next-gen products** — DARPA OPTIMA funding supports continued Princeton-EnCharge collaboration. Watch for system-level benchmarks that can be independently verified.

4. **Stanford monolithic 3D + CIM** — The December 2025 SkyWater tapeout demonstrated 3D integration with RRAM. The logical next step is combining this with CIM architectures for orders-of-magnitude density improvement.

5. **Julich gain cell CIM silicon** — The Nature Computational Science paper (2025) was simulation. Watch for actual silicon results. If even 1% of the 70,000x energy claim survives in hardware, it's transformative.

6. **Peking University follow-up** — Sun Zhong's 24-bit precision from 3-bit devices was for matrix equations. Can the iterative algorithm work for neural network inference? Papers expected in 2026.

7. **imec IGZO-DRAM CIM** — Early-stage exploration of oxide semiconductor memory for CIM. Could combine DRAM's writability with better analog CIM properties.

8. **DARPA OPTIMA deliverables** — Program runs 4.5 years. First milestone results from IBM, Georgia Tech, UCLA, Princeton expected 2025-2026.

---

## The Academic Research Ecosystem Map

```
DEVICE PHYSICS                    CIRCUITS/SYSTEMS                  BENCHMARKING
    │                                    │                              │
    ├── Stanford (Wong)                  ├── Princeton (Verma)          ├── Georgia Tech (Yu)
    ├── UCSB (Strukov)                   ├── KU Leuven/imec (Verhelst)  │   └── NeuroSim
    ├── Tsinghua (Wu/Gao)                ├── Michigan (Lu/Fick)         ├── imec (AnIA, DIANA)
    ├── Peking U (Sun/Yan)               ├── UCSD (Cauwenberghs)        └── BUAA (literature DB)
    └── Michigan (Lu)                    ├── Julich/RWTH (gain cell)
                                         └── KAIST (edge/implant)
                                              │
                                              ▼
                                    STARTUP PIPELINE
                                    ├── EnCharge AI ← Princeton
                                    ├── Mythic AI ← Michigan
                                    ├── Crossbar ← Michigan
                                    ├── MemryX ← Michigan
                                    ├── Axelera ← IBM Zurich/ETH/imec
                                    ├── Innatera ← Delft
                                    └── Unconventional AI ← Stanford/MIT
```

---

## Key Takeaways

1. **The field is consolidating around three memory technologies:** Capacitors (Princeton/EnCharge), RRAM (Tsinghua, Peking U, Stanford, UCSB), and gain cells (Julich). PCM (IBM/ETH) is strong in research but faces drift challenges. Flash CIM (Mythic/Michigan) is the only one shipping.

2. **China is ascendant:** Tsinghua and Peking University are publishing in Nature and Nature Electronics with results that match or exceed Western labs. Government funding is 10-100x larger than DARPA programs. The Huawei-ByteDance-Tsinghua collaboration at ISSCC 2026 signals that Chinese academic CIM research is transitioning to industry.

3. **The precision barrier is falling:** Peking University's 24-bit precision from 3-bit devices and IBM/ETH's Analog Foundation Models both show that algorithmic techniques can overcome raw analog noise. This was the biggest objection to analog AI — and it's being addressed.

4. **The university-to-startup pipeline favors circuits groups over device groups.** Michigan's MICL (three spin-outs) and Princeton EE (EnCharge) produce companies. Stanford's device physics group (Wong) produces influential papers but not companies. The implication: if you want to start an analog AI company, hire circuits engineers, not materials scientists.

5. **imec is the Switzerland of analog AI** — collaborating with everyone, benchmarking everything, not competing with anyone. Their hybrid digital-analog DIANA architecture is probably the most honest assessment of where analog CIM fits: powerful for specific operations, but you need digital backup for everything else.

6. **The $475M elephant:** Unconventional AI's seed round at $4.5B valuation with no silicon is either the most confident bet in chip history or the biggest bubble. Their Stanford/MIT pedigree in programming abstractions for analog substrates is real research, but translating it to competitive silicon is a multi-year, multi-billion-dollar challenge.

7. **DARPA OPTIMA is the most targeted Western funding program.** $78M across IBM, Georgia Tech, UCLA, Princeton, and Infineon. Results from this program (2025-2027) will be the most important Western academic CIM results to watch.
