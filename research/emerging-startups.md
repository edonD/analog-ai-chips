# Emerging Analog/Mixed-Signal AI Chip Startups (2025-2026)

Beyond the well-known players (IBM, Mythic, EnCharge, Syntiant, Aspinity), a second wave of startups is attacking the analog/mixed-signal AI inference problem from different angles. This file covers Ceremorphic, Sagence AI, TetraMem, Blumind, Anaflash, d-Matrix, and Axelera AI.

---

## 1. Ceremorphic — The Most Secretive (and Most Suspicious)

### What They Claim to Be Building

Ceremorphic claims to be building an "AI supercomputing chip" — the **Hierarchical Learning Processor (HLP)** — on TSMC 5nm. Their first chip is called **QS1**. The architecture combines:

- **ThreadArch**: A patented multi-thread RISC-V processor macro-architecture (1 GHz)
- **Custom ML processor** running at 2 GHz
- **Custom floating-point unit** at 2 GHz
- **Arm M55 v1 core**
- **Custom video engines** for "metaverse processing" (1 GHz)
- **PCIe 6.0 / CXL 3.0** connectivity (64 Gbit)
- Mixed-signal analog and digital circuits

The pitch is a heterogeneous SoC that deploys "the right processing system for optimal power performance operation." They target AI training, HPC, automotive, drug discovery, and metaverse.

### Company Status

| Detail | Value |
|--------|-------|
| Founded | April 2020, San Jose, CA |
| Founder/CEO | Dr. Venkat Mattela (previously founded Redpine Signals, sold to Silicon Labs for $308M in 2020) |
| Funding | $50M Series A (Jan 2022) — **funded entirely by founders/ex-Redpine insiders** |
| Employees | ~223 (July 2024), 39% YoY growth |
| Engineering | Large team in Hyderabad, India (Ceremorphic Technologies Pvt Ltd) |
| Patents | 100+ claimed |
| Glassdoor | **2.6/5 stars**, 26% recommend, 21% positive business outlook |

Sources: [HPCwire](https://www.hpcwire.com/2022/01/25/ceremorphic-exits-stealth-touts-hpc-ai-silicon-technology/), [VentureBeat](https://venturebeat.com/technology/ceremorphic-addresses-ai-hpc-and-the-metaverse-with-qs-1-chip-lands-50m/), [Tracxn](https://tracxn.com/d/companies/ceremorphic/__X721AIfJKNl8OXch2W8Uwhu9HTVCLlpT4-XOImmBxCs)

### Timeline of Announcements

1. **Jan 2022**: Exited stealth, announced QS1 chip and $50M Series A
2. **Oct 2022**: Announced tapeout of 5nm chip with TSMC
3. **Jan 2023**: Announced custom silicon development services for customers
4. **Oct 2023**: Announced life sciences division, **BioCompDiscoverX** platform for drug discovery
5. **Dec 2023**: Demonstrated BioCompDiscoverX at AI Drug Discovery Summit in Boston
6. **2024-2025**: Pivoted messaging toward "sustainable compute infrastructure" and drug discovery; no chip benchmarks published

Sources: [BusinessWire tapeout](https://www.businesswire.com/news/home/20221019005629/en/Cerem-orphic-Tapes-Out-AI-Supercomputing-Chip-on-TSMC-5nm-Node-Featuring-Circuit-Technology-for-Unrivaled-Energy-Efficiency-Performance-and-Reliability), [EE Times drug discovery](https://www.eetimes.com/ai-chip-startup-ceremorphic-moves-into-drug-discovery/), [Ceremorphic news](https://ceremorphic.com/news/)

### The "Analog" Angle

Ceremorphic is **not** a pure analog compute-in-memory company. Their chip is a heterogeneous digital SoC that includes "reliable analog and digital circuits" and mixed-signal IP. The analog component appears to be supporting circuitry (SerDes, mixed-signal interfaces) rather than analog compute for MAC operations. Their BioCompDiscoverX platform claims to use "analog silicon" to accelerate cell/tissue emulation, but no architecture details, papers, or benchmarks have been published.

### Honest Assessment: Likely Vaporware

**Red flags are numerous:**

1. **No benchmarks ever published.** Taped out in Oct 2022. As of March 2026 — 3.5 years later — zero performance numbers, zero silicon characterization results, zero independent evaluation.

2. **Self-funded Series A.** The $50M came from founders and ex-Redpine insiders, not institutional VCs. No subsequent funding rounds have been announced. For a 5nm chip company with 223 employees, $50M is very thin (a single 5nm tapeout can cost $15-30M).

3. **Pivot to drug discovery.** When a chip startup pivots to a completely different vertical (life sciences) before showing chip results, it typically signals the chip is not competitive.

4. **Glassdoor paints a dire picture.** 2.6/5 stars, only 21% positive business outlook. Reviews mention "unrealistic vision," projects canceled after 6 months, underpay, and toxic culture.

5. **Buzzword overload.** "Metaverse processing," "quantum circuits," "exascale," "unrivaled energy efficiency" — without a single published number. The BioCompDiscoverX platform claims to leverage "analog, quantum, and AI technology" which is marketing, not engineering.

6. **No customers announced.** Three and a half years after tapeout, no customer wins, no design wins, no sampling announcements.

7. **Linley Group presentation (2022) revealed nothing.** CEO Mattela spoke at Linley Spring Processor Conference 2022 but no independent analyst endorsement or architecture review has emerged.

**Verdict: Ceremorphic has real silicon (they taped out at TSMC) and real engineers (223 employees), but has shown zero evidence that the chip works or is competitive. The pivot to drug discovery, lack of benchmarks, insider-only funding, and terrible Glassdoor reviews collectively suggest a company struggling to find product-market fit. Not in the same league as EnCharge, Mythic, or even Sagence in terms of technical credibility.**

---

## 2. Sagence AI (formerly Analog Inference) — NOR Flash Deep Subthreshold

### What They're Building

Sagence AI is building **analog in-memory compute chips using NOR flash cells operated in deep subthreshold mode** — a genuinely novel approach. Key technical innovations:

- **NOR flash cells** licensed in standard configuration (not custom memory)
- **8-bit precision per cell** via proprietary algorithms — critical threshold for LLM inference
- **Deep subthreshold operation**: flash cells are biased just barely on, producing tiny currents. This is where the power savings come from — orders of magnitude less current per operation than conventional flash reads
- **Multi-level non-volatile memory** stores multiple bits per cell without SRAM/DRAM power

### Performance Claims

- **10x lower power** vs. leading GPU (normalized to 666K tokens/sec on Llama2-70B)
- **20x lower cost**
- **20x smaller rack space**

### Product Roadmap

- **First product (2025)**: Vision systems (lighter workload, lower risk)
- **Second product**: Generative AI / LLM inference
- **Future architecture (Delphi)**: 3D-stacked analog chips linked via UCIe interposer to CPU and HBM DRAM

### Company Details

| Detail | Value |
|--------|-------|
| Founded | ~2018 (as Analog Inference, renamed to Sagence AI Nov 2024) |
| Founder/CEO | Vishal Sarin (25+ years semiconductors, 100+ patents, MSEE Michigan, MBA Berkeley) |
| Funding | ~$50-58M total (Seed through Series B; Series B $22.4M in May 2023) |
| Key investors | Vinod Khosla, Andy Bechtolsheim (Sun Microsystems founder), Atiq Raza (former AMD President/COO), TDK Ventures, Cambium Capital, Aramco Ventures |
| Status | Emerged from stealth Nov 2024; engaged with "multiple" customers |

Sources: [IEEE Spectrum](https://spectrum.ieee.org/analog-ai-2669898661), [TechCrunch](https://techcrunch.com/2024/11/18/sagence-is-building-analog-chips-to-run-ai/), [BusinessWire](https://www.businesswire.com/news/home/20241119609411/en/Sagence-AI-Emerges-from-Stealth-Tackling-Economic-Viability-of-Inference-Hardware-for-Generative-AI), [TDK Ventures](https://tdk-ventures.com/portfolio/computing-connectivity/sagence-ai/)

### Honest Assessment

**Strengths:**
- Deep subthreshold NOR flash is a genuinely differentiated approach — not just another RRAM/PCM/SRAM CIM play
- 8-bit per cell is the right precision target for transformer inference
- Investor quality is excellent (Khosla, Bechtolsheim, Raza know semiconductors)
- 6+ years in stealth suggests real R&D, not just a pitch deck
- NOR flash is a mature, manufacturable technology

**Weaknesses:**
- No silicon benchmarks published yet
- Claims of 10-20x improvements are unverified
- The 666K tokens/sec comparison methodology is unclear — what batch size? what hardware baseline?
- $50-58M total is modest funding for a company targeting datacenter AI inference
- Vision-first product is sensible but delays the LLM proof point
- Deep subthreshold operation raises questions about speed (low current = slow) and temperature sensitivity

**Verdict: More credible than Ceremorphic by a wide margin. Real technical differentiation, serious investors, appropriate stealth duration. But still pre-silicon-proof. The key question is whether deep subthreshold NOR flash can deliver claimed precision and speed at scale. Worth watching closely.**

---

## 3. TetraMem — RRAM with Record Precision

### What They're Building

TetraMem builds **RRAM (memristor) based compute-in-memory** chips with a breakthrough in per-cell precision. Their key technical achievement:

- **11 bits per cell (2,048 conductance levels)** in individual memristors — published in *Nature* (2023) and *Science* (2024)
- Memristor arrays (256x256) monolithically integrated on CMOS in a **commercial foundry**
- Demonstrated "arbitrarily high precision" programming technique that works across RRAM, PCM, FeRAM, and MRAM

### Products

- **MX100**: World's first 8-bit multi-level RRAM in-memory computing evaluation SoC. Supports INT4 and INT8. Paired with Andes RISC-V vector processor.
- Targets edge use cases: AR/VR headsets, health monitoring, voice recognition, IoT

### Company Details

| Detail | Value |
|--------|-------|
| Founded | 2018 |
| Co-founders | Prof. Joshua Yang (USC), Miao Hu (CTO), Prof. Qiangfei Xia, Glenn Ge (CEO) |
| Origin | University of Massachusetts / USC research |
| Investors | SAIC Capital, Foothill Ventures |
| Partnerships | **SK hynix** research partnership; SK Square invested in the company |
| Recognition | EE Times Silicon 100 "Startups to Watch" (2025) |

Sources: [Nature 2023](https://www.nature.com/articles/s41586-023-05759-5), [Science 2024](https://www.science.org/doi/10.1126/science.adi9405), [TetraMem](https://tetramem.com/), [Semiwiki](https://semiwiki.com/ip/349000-tetramem-integrates-energy-efficient-in-memory-computing-with-andes-risc-v-vector-processor/)

### Honest Assessment

**Strengths:**
- Strongest published precision of any analog memory technology — 11 bits in *Nature* and *Science* is world-class
- Commercial foundry fabrication (not just lab demos)
- SK hynix partnership adds serious manufacturing credibility
- MX100 SoC exists and is available for evaluation
- Academic pedigree is top-tier (Yang group is one of the most cited in memristor research)

**Weaknesses:**
- 11-bit is a research result; MX100 ships at INT4/INT8 commercially — the gap between research precision and production precision is real
- RRAM endurance and cycle-to-cycle variation remain ongoing challenges (not unique to TetraMem)
- Funding appears modest (no large rounds announced)
- Edge-only positioning limits near-term revenue potential
- No published system-level efficiency numbers (TOPS/W) for the MX100

**Verdict: The most scientifically credible RRAM CIM startup. The Nature/Science publications are not hype — they represent genuine breakthroughs in memristor programming precision. The SK hynix partnership suggests this could eventually be integrated into mainstream memory products. But the gap between 11-bit research demos and production-grade CIM at scale remains large. This is a long game.**

---

## 4. Blumind — Pure Analog Neural Networks at <1 uW

### What They're Building

Blumind builds **fully analog neural network processors** using their proprietary **AMPL (Analog Matrix Processing Logic)** architecture. This is pure analog — computations happen directly within memory cells, no clock cycles, no digital data movement.

### Key Specifications

- **BM110**: Keyword spotting (always-on audio). <1 uW for always-on KWD. Total system-level solution (chip + analog mic) ~30-60 uW
- **BM210**: Always-on video and image classification
- **Process**: Standard CMOS (no exotic memories)
- Claims **1000x lower power** than digital alternatives for equivalent inference

### Company Details

| Detail | Value |
|--------|-------|
| Founded | 2020, Ottawa, Canada |
| Founders | Niraj Mathur (CEO), John Gosson (CTO) |
| Funding | **$20M CAD Series A** (April 2025), co-led by Cycle Capital and BDC Capital; also Fusion Fund, Two Small Fish Ventures, Real Ventures, Ikigai Ventures, Morgan Creek Capital |
| Production | KWD chip production planned H2 2025 |
| Future | Vision CNNs, eventually small language models (SLMs) |

Sources: [Blumind](https://blumind.ai), [BetaKit](https://betakit.com/blumind-secures-20-million-series-a-to-build-the-ai-chip-wed-have-if-computers-didnt-exist/), [ARMdevices.net](https://armdevices.net/2026/03/15/blumind-ampl-analog-ai-at-60-microwatts-for-always-on-audio-edge-wearables-and-vision/), [EPT](https://www.ept.ca/features/blumind-reimagines-ai-processing-with-breakthrough-analog-chip/)

### Honest Assessment

**Strengths:**
- Sub-microwatt always-on inference is genuinely impressive and addresses a real market (billions of IoT sensors)
- Standard CMOS process — no exotic memory dependency
- <30 uW total system power for keyword spotting competes directly with Aspinity's AML100 (~30-100 uW) and outperforms Syntiant
- Fresh Series A funding (April 2025) suggests investor confidence
- Production timeline (H2 2025) is imminent

**Weaknesses:**
- $20M CAD (~$15M USD) is very modest funding for a chip company
- Model capacity for pure analog is inherently limited — keyword spotting and simple vision are achievable; LLMs are not
- Competing directly with Aspinity (shipping since 2024) and POLYN (34 uW analog neurons)
- No published accuracy or benchmark comparisons
- Canadian startup competing for attention against US-based, better-funded alternatives

**Verdict: A legitimate pure analog play at the sensor edge. Competes in the same space as Aspinity and POLYN. The <1 uW always-on claim needs independent verification, but if true, it would be best-in-class. The real question: is the always-on keyword spotting / simple vision market large enough to sustain a chip company? Production in H2 2025 will be the proof point.**

---

## 5. Anaflash — Flash-Based Edge AI MCU

### What They're Building

Anaflash builds **AI microcontrollers with embedded flash memory** that enables both compute-near-flash (CnF) and compute-in-flash (CiF) — all using **standard logic process** without any memory-specific process modifications.

### Key Technical Approach

- **Logic-EFLASH**: Proprietary embedded flash technology using only standard logic devices (no special flash process needed)
- **Samsung Foundry 28nm** process
- **4 bits/cell** embedded flash for AI model storage
- **Zero standby power** for weight memory (non-volatile)
- **Reflex Computing Unit (RCU)**: Always-on near-sensor AI compute

### Company Details

| Detail | Value |
|--------|-------|
| Founded | Silicon Valley startup |
| CEO/Co-Founder | Peter Song |
| CTO | Shahrzad Naraghi (joined via Legato Logic acquisition, Feb 2025) |
| Funding | $7.23M total over 5 rounds (Series A: Nov 2024, led by Stonebridge Ventures) |
| Subsidiary | SEMIBRAIN (Korea) — won Samsung fabless challenge contest (2022), received $4M Korean government grant |
| Key event | **Acquired Legato Logic** (Feb 2025) — gained time-based CIM technology and team |

Sources: [Anaflash](https://www.anaflash.com/), [BusinessWire](https://www.businesswire.com/news/home/20250205794984/en/ANAFLASH-and-Legato-Logic-Unite-to-Drive-Next-Generation-Edge-Computing), [Yahoo Finance](https://finance.yahoo.com/news/anaflash-advances-embedded-flash-memory-180000104.html), [EE Times podcast](https://www.eetimes.com/podcasts/anaflash-and-legato-logic-merge-forces/)

### Honest Assessment

**Strengths:**
- Standard logic process compatibility is a major advantage — means Samsung, TSMC, etc. can manufacture without custom memory modules
- Samsung Foundry partnership provides manufacturing credibility
- Zero standby power for weights is ideal for battery-powered edge devices
- Legato Logic acquisition adds compute-in-flash capability (complementing existing compute-near-flash)
- $4M Korean government grant validates the underlying technology

**Weaknesses:**
- $7.23M total funding is extremely thin — this is a very early-stage company
- 28nm process limits performance ceiling
- 4 bits/cell flash is low precision — will need multi-cell techniques for INT8
- No published benchmarks, TOPS/W numbers, or model accuracy data
- Competing against Mythic (flash CIM with $300M+ raised) and Sagence (NOR flash with $50M+)

**Verdict: Interesting technology (logic-compatible embedded flash CIM), but severely underfunded relative to competitors. The Samsung relationship and Legato Logic acquisition show strategic thinking. Could be an acquisition target for a larger MCU company wanting AI capability. Not yet a threat to established players.**

---

## 6. d-Matrix — Digital In-Memory Compute (Not Analog, but Important)

### What They're Building

d-Matrix builds **digital in-memory compute** inference accelerators. This is explicitly **not analog** — they use SRAM-based digital CIM. Included here because they represent the digital CIM alternative that analog CIM companies must beat.

### Corsair Platform (Shipping)

- **TSMC 6nm** chiplet-based architecture
- **2.4 PFLOPS INT8** per card (9.6 PFLOPS INT4)
- **38 TOPS/W** energy efficiency
- **2 GB SRAM** across chiplets + **256 GB LPDDR5X** per card
- **275W TDP** (at 800 MHz; 550W at 1.2 GHz)
- **60,000 tokens/sec** on Llama3-8B (single server)
- **30,000 tokens/sec** on Llama3-70B (single rack)
- **PCIe card form factor** — drop-in replacement for GPUs

### Next Generation: Raptor (2026)

- **TSMC 4nm** with **3DIMC** — 3D-stacked DRAM digital in-memory compute
- Claims **10x faster inference than HBM4-based solutions**
- Collaboration with Alchip on 3D DRAM integration

### Company Details

| Detail | Value |
|--------|-------|
| HQ | Santa Clara, CA |
| Funding | **$275M Series C** (Nov 2025) at **$2B valuation** |
| Total raised | ~$440M+ |
| Key backers | Microsoft, Playground Global |
| Status | Corsair available to early-access customers (broader availability Q2 2025) |
| Hot Chips | Presented Corsair architecture at Hot Chips 2025 |

Sources: [d-Matrix](https://www.d-matrix.ai/), [SiliconANGLE](https://siliconangle.com/2025/11/12/chip-startup-d-matrix-raises-275m-speed-inference-memory-compute/), [ServeTheHome](https://www.servethehome.com/d-matrix-corsair-in-memory-computing-for-ai-inference-at-hot-chips-2025/), [Chips and Cheese](https://chipsandcheese.com/p/d-matrix-corsair-256gb-of-lpddr-for)

### Why This Matters for Analog CIM

d-Matrix at 38 TOPS/W with digital SRAM CIM sets the bar that analog CIM must beat. If analog claims 100x better efficiency but d-Matrix delivers 38 TOPS/W digitally with deterministic precision and a standard software stack, the analog advantage must be measured against this baseline — not against 2022-era GPUs.

**Verdict: d-Matrix is the most commercially advanced CIM company (analog or digital). $2B valuation, Microsoft backing, real silicon at Hot Chips, and a clear product shipping timeline. This is what credible CIM commercialization looks like.**

---

## 7. Axelera AI — Digital CIM at the Edge (European Champion)

### What They're Building

Axelera AI builds **digital in-memory compute** edge AI chips using a RISC-V architecture. Like d-Matrix, this is digital CIM, not analog.

### Products

- **Metis AIPU**: 214 TOPS INT8, ~15 TOPS/W, quad-core RISC-V + digital IMC. **Shipping and available for purchase** (Metis Compute Board on their online store)
- **Europa AIPU** (2025): 629 TOPS INT8, 64 GB memory, 200 GB/s DRAM bandwidth, 128 MB on-chip L2 SRAM. 8 AI cores with 2nd-gen D-IMC
- **Titania** (future): AI inference chiplet funded by EU DARE project

### Company Details

| Detail | Value |
|--------|-------|
| HQ | Eindhoven, Netherlands |
| Founded | 2021 |
| Funding | **$250M+ round** (Feb 2026), total ~$450M including equity, debt, grants |
| Key investors | Innovation Industries, BlackRock, Samsung Catalyst Fund, European Investment Council |
| EU grants | **€61.6M** from EuroHPC DARE project (March 2025) |
| Status | Metis shipping; Europa announced |

Sources: [Axelera AI](https://axelera.ai/), [Sifted](https://sifted.eu/articles/axelera-ai-inference-250m-raise), [SiliconANGLE](https://siliconangle.com/2026/02/24/edge-ai-chip-startup-axelera-ai-raises-250m-funding-round/), [Wikipedia](https://en.wikipedia.org/wiki/Axelera_AI)

### Honest Assessment

**Verdict: Axelera is the European answer to edge AI inference. Metis at 214 TOPS / 15 TOPS/W is genuinely competitive with NVIDIA Jetson and Hailo. Europa at 629 TOPS would be best-in-class for edge. The EU funding (€61.6M DARE grant) reflects European chip sovereignty ambitions as much as technical merit, but the underlying digital CIM technology is real and shipping. Like d-Matrix, Axelera demonstrates that digital CIM can deliver competitive efficiency without the precision/noise/drift challenges of analog.**

---

## Comparative Summary

| Company | Approach | Precision | Funding | Product Status | Best Published Metric |
|---------|----------|-----------|---------|----------------|----------------------|
| **Ceremorphic** | Heterogeneous SoC (mixed-signal) | Unknown | $50M (self-funded) | Taped out 2022; no results | None published |
| **Sagence AI** | NOR flash deep subthreshold analog CIM | 8-bit/cell | ~$50-58M | Pre-silicon; vision chip 2025 | 10x lower power claim (unverified) |
| **TetraMem** | RRAM memristor analog CIM | 11-bit/cell (research), INT4/8 (product) | Undisclosed (modest) | MX100 eval SoC available | 2,048 levels/cell (Nature) |
| **Blumind** | Pure analog neural networks (AMPL) | Unknown | $20M CAD | Production H2 2025 | <1 uW always-on KWD |
| **Anaflash** | Flash CIM on standard logic process | 4-bit/cell | $7.23M | Development | Zero standby power |
| **d-Matrix** | Digital SRAM CIM (chiplet) | INT4/8/16 | ~$440M+ ($2B val) | Corsair shipping to early customers | 38 TOPS/W, 2.4 PFLOPS INT8 |
| **Axelera AI** | Digital CIM (RISC-V) | INT4/8 | ~$450M | Metis shipping | 214 TOPS, 15 TOPS/W |

---

## Key Takeaways

### 1. The Digital CIM Threat
d-Matrix (38 TOPS/W) and Axelera (15 TOPS/W, 214 TOPS) are shipping digital CIM products with deterministic precision and standard software stacks. Every analog CIM startup must demonstrate a clear advantage over these baselines — not over 3-year-old GPU comparisons.

### 2. Analog CIM is Fragmenting by Memory Technology
- **NOR flash**: Sagence AI (deep subthreshold, datacenter)
- **RRAM/memristor**: TetraMem (record precision, edge)
- **Standard flash**: Anaflash (logic-compatible, MCU), Mythic (40nm flash, edge/auto)
- **Capacitor/SRAM**: EnCharge AI (charge-domain, datacenter)
- **Pure analog**: Blumind (no NVM, standard CMOS, sensor edge)

Each approach has different precision/speed/endurance/cost tradeoffs. There will not be one winner.

### 3. Ceremorphic is an Outlier
Every other company on this list has either: published peer-reviewed results (TetraMem), shipped silicon (d-Matrix, Axelera, Mythic), demonstrated at conferences (EnCharge, Sagence), or has a clear technical differentiation explained in detail (Blumind, Anaflash). Ceremorphic has done none of these after 6 years and $50M. The QS1 chip may exist in silicon but has produced zero public evidence of working.

### 4. The Funding Gap is Telling
d-Matrix ($440M+, $2B valuation) and Axelera ($450M) dwarf the analog startups (Sagence $58M, Ceremorphic $50M, Blumind $15M, Anaflash $7M). This reflects investor skepticism about analog CIM's commercial viability relative to digital CIM, which offers similar efficiency gains without the precision/calibration headaches.

### 5. 2025-2026 is the Proof Window
Sagence (vision chip 2025), Blumind (KWD chip H2 2025), Anaflash (Samsung 28nm), and TetraMem (MX100 evaluations) all have near-term silicon milestones. By end of 2026, we will have real data on whether analog CIM delivers on its efficiency promises or whether digital CIM (d-Matrix, Axelera) has already captured the value.

---

## Sources

- [Ceremorphic exits stealth — HPCwire](https://www.hpcwire.com/2022/01/25/ceremorphic-exits-stealth-touts-hpc-ai-silicon-technology/)
- [Ceremorphic QS1 and $50M — VentureBeat](https://venturebeat.com/technology/ceremorphic-addresses-ai-hpc-and-the-metaverse-with-qs-1-chip-lands-50m/)
- [Ceremorphic tapeout — BusinessWire](https://www.businesswire.com/news/home/20221019005629/en/Ceremorphic-Tapes-Out-AI-Supercomputing-Chip-on-TSMC-5nm-Node-Featuring-Circuit-Technology-for-Unrivaled-Energy-Efficiency-Performance-and-Reliability)
- [Ceremorphic drug discovery — EE Times](https://www.eetimes.com/ai-chip-startup-ceremorphic-moves-into-drug-discovery/)
- [Ceremorphic about — bisinfotech](https://www.bisinfotech.com/an-exclusive-interaction-with-dr-venkat-mattela-ceremorphic/)
- [Sagence AI — IEEE Spectrum](https://spectrum.ieee.org/analog-ai-2669898661)
- [Sagence AI — TechCrunch](https://techcrunch.com/2024/11/18/sagence-is-building-analog-chips-to-run-ai/)
- [Sagence AI stealth exit — BusinessWire](https://www.businesswire.com/news/home/20241119609411/en/Sagence-AI-Emerges-from-Stealth-Tackling-Economic-Viability-of-Inference-Hardware-for-Generative-AI)
- [TetraMem Nature 2023 — 2048 levels](https://www.nature.com/articles/s41586-023-05759-5)
- [TetraMem Science 2024 — arbitrary precision](https://www.science.org/doi/10.1126/science.adi9405)
- [TetraMem MX100 — Semiwiki](https://semiwiki.com/ip/349000-tetramem-integrates-energy-efficient-in-memory-computing-with-andes-risc-v-vector-processor/)
- [Blumind Series A — BetaKit](https://betakit.com/blumind-secures-20-million-series-a-to-build-the-ai-chip-wed-have-if-computers-didnt-exist/)
- [Blumind AMPL 60 uW — ARMdevices](https://armdevices.net/2026/03/15/blumind-ampl-analog-ai-at-60-microwatts-for-always-on-audio-edge-wearables-and-vision/)
- [Anaflash Samsung — Yahoo Finance](https://finance.yahoo.com/news/anaflash-advances-embedded-flash-memory-180000104.html)
- [Anaflash + Legato Logic — BusinessWire](https://www.businesswire.com/news/home/20250205794984/en/ANAFLASH-and-Legato-Logic-Unite-to-Drive-Next-Generation-Edge-Computing)
- [d-Matrix $275M — SiliconANGLE](https://siliconangle.com/2025/11/12/chip-startup-d-matrix-raises-275m-speed-inference-memory-compute/)
- [d-Matrix Corsair Hot Chips — ServeTheHome](https://www.servethehome.com/d-matrix-corsair-in-memory-computing-for-ai-inference-at-hot-chips-2025/)
- [d-Matrix 3DIMC — SiliconANGLE](https://siliconangle.com/2025/08/25/d-matrix-reveals-plan-scale-ais-memory-wall-3d-dram-based-chip-architecture/)
- [Axelera $250M — Sifted](https://sifted.eu/articles/axelera-ai-inference-250m-raise)
- [Axelera Europa — Axelera AI](https://axelera.ai/news/axelera-announces-europa-aipu-setting-new-industry-benchmark-for-ai-accelerator-performance-power-efficiency-and-affordability)
- [Axelera DARE grant — Axelera AI](https://axelera.ai/eu-funding)
