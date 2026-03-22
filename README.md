# Analog AI Chips Research — 2025/2026

A deep-dive engineering reference on analog, neuromorphic, and mixed-signal AI chips. The core question: **can analog compute challenge digital for AI inference?**

**Short answer: yes, but only narrowly, and digital is closing the gap fast.**

---

## The Verdict (Updated After 23 Deep Dives)

### Where Analog Wins

1. **Always-on sensor edge (<1 mW):** Analog preprocessing before the ADC saves 90%+ power by keeping digital systems asleep. Aspinity AML200 achieves 300 TOPS/W at <100 uW. POLYN runs voice activity detection at 34 uW with zero clock. This is the one domain where analog has a structural, physics-based advantage that digital cannot match — because the signal is already analog.

2. **Moderate edge inference (1-10W):** Capacitor-based CIM (EnCharge EN100: ~24 TOPS/W system-level) and flash CIM (Mythic Gen 1: ~8 TOPS/W) deliver real, measured efficiency gains of 2-7x over conventional digital NPUs. Not 100x. But real.

### Where Analog Loses

1. **LLMs and large models:** The capacity gap (4M weights on-chip vs billions needed) is 250-1000x. No analog chip has run a real LLM. Digital quantization (1-4 bit) is solving the same efficiency problem with standard tooling. Analog LLM inference is a 2030+ prospect at best.

2. **Datacenter scale:** Digital CIM (d-Matrix: 38 TOPS/W, $2B valuation; Axelera: 214 TOPS, $450M raised) achieves comparable efficiency with deterministic accuracy and CUDA-like toolchains. Analog's 2-10x advantage evaporates against the software ecosystem gap.

3. **ISSCC 2025 signal:** Zero analog CIM papers in the dedicated CIM session. Digital SRAM CIM hit 192.3 TFLOPS/W. The academic community is voting with its submissions.

### The Three Killers

1. **ADC/DAC overhead:** Consumes 40-85% of system power. This single factor collapses "100x" claims to 2-10x reality. ([research/adc-dac-bottleneck.md](research/adc-dac-bottleneck.md))
2. **Precision ceiling:** Analog achieves 3-6 effective bits (PCM/RRAM) to 6-8 bits (capacitor). Each extra bit costs 4x signal power. Analog "4-bit" is stochastic, not deterministic like INT4. ([research/precision-noise-challenges.md](research/precision-noise-challenges.md))
3. **Software ecosystem:** No analog equivalent of CUDA/TensorRT. Mythic nearly died from underinvesting here. Budget 40-50% of engineering on software. ([research/design-tradeoffs-synthesis.md](research/design-tradeoffs-synthesis.md))

### If You're Designing a Chip

Read **[research/design-tradeoffs-synthesis.md](research/design-tradeoffs-synthesis.md)** first. The recommended architecture ranking:

1. **Charge-domain CIM (capacitor/SRAM)** — best precision, no drift, standard CMOS process. EnCharge's approach.
2. **Digital CIM** — deterministic, proven, shipping. d-Matrix and Axelera's approach.
3. **Flash CIM** — non-volatile, mature foundry support, moderate drift. Mythic/Sagence's approach.
4. **Avoid for new designs:** RRAM (variability), PCM (drift), pure neuromorphic (no killer app), photonic compute (2028+), analog training (commercially impossible).

---

## Research Files

### History & Context

| File | What It Covers |
|------|---------------|
| **[research/history-and-lessons.md](research/history-and-lessons.md)** | **Why analog failed before and what's different now.** Three waves of analog AI chips (1989-1997, 2012-2022, 2022-present). Intel ETANN (1989), AT&T ANNA chip, Carver Mead's neuromorphic vision, Synaptics pivot to touchpads, AI winter, memristor revival, DARPA SyNAPSE. Why digital always won (Moore's Law exponential vs analog constant-factor). 7 lessons for today's startups. Hype cycle pattern analysis. Syntiant's analog-to-digital pivot as key signal. |

### Synthesis & Design

| File | What It Covers |
|------|---------------|
| **[research/design-tradeoffs-synthesis.md](research/design-tradeoffs-synthesis.md)** | **The practical engineering guide.** Memory tech selection, ADC architecture, precision strategy, process node economics ($2-5M at 28nm vs $100M+ at 3nm), digital vs analog CIM, software stack, calibration, business case, 6 failure patterns from Mythic/Rain/BrainChip/Loihi, recommended architecture decision tree. |
| **[research/analog-for-llms.md](research/analog-for-llms.md)** | **Can analog run LLMs?** IBM's ALBERT on HERMES (first transformer on analog silicon, 7.1M params). Analog Foundation Models match W4A8 in simulation. But 250x capacity gap, no KV cache solution, digital quantization closing fast. Timeline: 2030+ if ever. |
| [research/adc-dac-bottleneck.md](research/adc-dac-bottleneck.md) | **THE bottleneck.** ADC/DAC eats 40-85% of power. 6 ADC architectures compared. CSNR-optimal design (40-64x savings). 100 fJ/Op theoretical floor. Why "100x" becomes "2-10x." |
| [research/precision-noise-challenges.md](research/precision-noise-challenges.md) | **The physics limits.** 8 noise sources, PCM drift (v=0.1-0.15), RRAM variability, temperature sensitivity. Memory tech ranking: Capacitor > Flash > SRAM > RRAM > PCM > MRAM. Noise-aware training essential but creates HW-SW coupling. |

### Company Deep Dives

| File | Company | Key Number | Status |
|------|---------|-----------|--------|
| [research/encharge-ai.md](research/encharge-ai.md) | EnCharge AI | ~24 TOPS/W (system), 200 TOPS | Most promising analog CIM. Capacitor physics. $144M raised. No independent benchmarks. |
| [research/mythic-ai.md](research/mythic-ai.md) | Mythic AI | ~8 TOPS/W (measured Gen 1) | Best-funded ($300M+). Flash CIM. Nearly died 2022. Gen 2 unverified. Honda/Lockheed. |
| [research/ibm-analog-ai.md](research/ibm-analog-ai.md) | IBM Research | 12.4 TOPS/W (HERMES), 14x over digital | Strongest research program. PCM-based. 4M weights. Years from production. |
| [research/brainchip-akida.md](research/brainchip-akida.md) | BrainChip | 76.9 FPS/W (50x vs embedded GPU) | Neuromorphic. Tech works, business failing ($398K revenue). |
| [research/intel-loihi.md](research/intel-loihi.md) | Intel Loihi | 1.15B neurons (Hala Point) | Groundbreaking research, commercial dead end. 8+ years, zero revenue. |
| [research/edge-analog-ai.md](research/edge-analog-ai.md) | Aspinity, Syntiant, POLYN, Innatera | 300 TOPS/W (Aspinity AML200) | Syntiant most successful (10M+ shipped) but is digital. Aspinity purest analog. |
| [research/emerging-startups.md](research/emerging-startups.md) | Sagence, TetraMem, Blumind, d-Matrix, Axelera, Ceremorphic | 38 TOPS/W (d-Matrix) | Digital CIM (d-Matrix $2B, Axelera $450M) far ahead of analog commercially. |
| [research/photonic-ai-chips.md](research/photonic-ai-chips.md) | Lightmatter, Ayar Labs, etc. | 8.19 TOPS best measured | Interconnect real and shipping. Compute pre-commercial (2028+). |
| [research/tsetlin-machines.md](research/tsetlin-machines.md) | Literal Labs, Anzyz | 8.6 nJ/frame (65nm ASIC) | Logic-based (AND/OR/NOT). Efficient for tiny tasks. Can't do LLMs. |
| **[research/rain-ai.md](research/rain-ai.md)** | **Rain AI** | **$67M raised, $3M bridge** | **Cautionary tale. Memristor NPU vision failed. Pivoted to digital CIM too late. $150M Series B collapsed. Exploring sale. Altman conflict of interest. Key lessons for analog startups.** |
| **[research/everactive-batteryless.md](research/everactive-batteryless.md)** | **Everactive** | **2.19 uW idle (PKS3000), $161M raised** | **Batteryless vibration sensors via energy harvesting. Fluke 3562 product shipping. 1 kHz bandwidth = screening only, cannot detect bearing faults. IMS division sold to Shoplogix Feb 2025. Complementary to VibroSense-1, not competitive — different market segment (screening vs. diagnosis).** |
| **[research/stm-ism330-ml-core.md](research/stm-ism330-ml-core.md)** | **STMicroelectronics ISM330DHCX** | **$6.80, 512-node MLC, ~300 uW** | **Primary digital competitor. On-sensor decision trees (8 trees, 512 nodes) but MLC limited to 104 Hz classification rate — cannot do FFT, envelope analysis, or frequency decomposition. At 26 Hz ODR (~300 uW), only detects vibration intensity. Full bandwidth requires ~1 mW + MCU for real analysis. ISM330BX successor 3x lower power. "Good enough" for 80% of use cases; VibroSense-1 wins on diagnostic depth for the remaining 20%.** |

### Academic Research Ecosystem

| File | What It Covers |
|------|---------------|
| **[research/academic-research-labs.md](research/academic-research-labs.md)** | **The research map.** Top 10 academic groups: Princeton (Verma → EnCharge), IBM/ETH Zurich (PCM + Analog Foundation Models), Tsinghua (Wu/Gao → Huawei-ByteDance RRAM), Julich (gain cell attention for LLMs — 70,000x energy claim), Stanford (Wong/Raina → NeuRRAM + 3D), Peking U (24-bit precision from 3-bit RRAM), UCSD (Cauwenberghs), Georgia Tech (Yu → NeuroSim benchmarking), Michigan (Lu → Mythic/Crossbar/MemryX), KU Leuven/imec (Verhelst → DIANA hybrid). University-to-startup pipeline. DARPA OPTIMA $78M, China $47.5B IC fund, EU Chips JU. |

### Practitioner Sentiment

| File | What It Covers |
|------|---------------|
| **[research/practitioner-opinions.md](research/practitioner-opinions.md)** | **What engineers actually think.** Chip designer skepticism ("none of these concepts have come to life"), the "pick two" trilemma (power/speed/accuracy), Naveen Verma's admission ("the capacitor is the easy part"), Mythic postmortem, HN/community recurring arguments, the VC-vs-engineering gap ($475M Unconventional AI seed vs $8M sector revenue), ML practitioner toolchain frustrations, bull vs bear case from practitioners. Engineering community significantly more skeptical than VC community. |

### Market & Business

| File | What It Covers |
|------|---------------|
| **[research/market-and-investment.md](research/market-and-investment.md)** | **The money story.** $251M analog CIM market vs $200B+ total AI chips. ~$1.5-2B VC invested, ~$8M total revenue. Unconventional AI $475M seed. DARPA OPTIMA $78M. Defense most receptive segment. Mythic $6.4M revenue is sector leader. Revenue-to-investment ratio: 0.5%. Honest timeline: $1B market by 2030-2031. |

### Regional Deep Dives

| File | What It Covers |
|------|---------------|
| **[research/china-analog-ai.md](research/china-analog-ai.md)** | **China's analog CIM ecosystem.** World's most active RRAM CIM research. Tsinghua LEMON lab (STELLAR on-chip learning, 28nm 576K macro, memCS 11x speedup), Peking U (24-bit precision RRAM solver, "1000x faster than GPU" for MIMO), Nanjing U (0.101% RMSE precision record via geometry-ratio encoding), ZJU Darwin Monkey (2.1B neuron neuromorphic computer), Tianjic (unified SNN+ANN), ACCEL/LightGen (optical analog). Huawei-ByteDance-Tsinghua ISSCC 2026 alliance. Big Fund III $47.5B. Export control implications. China leads in research, lags in commercialization (zero startups vs 5+ US). |

### Novel & Unconventional Approaches

| File | What It Covers |
|------|---------------|
| **[research/novel-unconventional-approaches.md](research/novel-unconventional-approaches.md)** | **The weird stuff.** 12 unconventional computing approaches ranked by readiness. Thermodynamic computing (Extropic X0/Z1 TSU, Normal Computing CN101 tape-out, Unconventional AI $475M/$4.5B seed). Probabilistic p-bit computing (UCSB/Tohoku DAC-free design at IEDM 2025, Northwestern ASIC). Reservoir computing (TDK 80µW prototype, 200 TOPS photonic RC). Spintronic CIM (lossless 112.3 TOPS/W STT-MRAM macro). FeFET/FeRAM CIM (FMC €100M raise, building fab). Coupled oscillator Ising machines (1440-node 28nm chip). In-sensor computing (PixArt/OmniVision shipping). Superconducting neural nets (80x efficiency incl. cooling). Electrochemical/ionic neurons. CNT 3D integration. Diffractive optical NNs. DNA computing. |

### Energy Harvesting & Self-Powered Sensing

| File | What It Covers |
|------|---------------|
| **[research/energy-harvesting-sensors.md](research/energy-harvesting-sensors.md)** | **Can VibroSense-1 run forever without batteries?** Yes. Thermoelectric harvesting from motor bearing surfaces delivers 1-20 mW continuous — 3x to 60x the 300 uW budget. Full comparison of 5 harvesting sources (TEG, piezo, EM vibration, indoor PV, RF). Energy harvesting ICs (LTC3108, e-peas AEM30940, Nowi NH2, BQ25570). Everactive PKS3000 SoC (2.19 uW idle, Hot Chips 2025). Perpetua Power Puck (400 mW from 1 in³). Motor bearing dT = 15-40°C guarantees harvesting. BOM cost $22-50 per node, break-even vs batteries in 2-3 years. The 300 uW analog design point crosses a threshold: it enables install-and-forget industrial sensing that MCU+FFT competitors at 3-10 mW cannot match. |

### Process & Fabrication

| File | What It Covers |
|------|---------------|
| **[research/process-node-comparison.md](research/process-node-comparison.md)** | **Commercialization roadmap: which process node for VibroSense-1 production?** Open PDK comparison (sky130 vs GF180 vs IHP SG13G2). Commercial analog AI chip process choices (Aspinity 22nm, Mythic 40nm, EnCharge 16nm, BrainChip 22FDX). NRE costs by node ($10K at 130nm shuttle to $100M+ at 3nm). FD-SOI vs bulk CMOS for analog (body biasing, subthreshold, matching). GF 22FDX recommended for production ($2-4M NRE, 3-5x power reduction). Foundry access for startups (Tower, X-FAB, Europractice, Muse/GSME). MEMS+CMOS integration options. Full migration timeline: sky130 prototype → 22FDX production. |

### Government Programs & Validation

| File | What It Covers |
|------|---------------|
| **[research/darpa-nzero-sensors.md](research/darpa-nzero-sensors.md)** | **DARPA N-ZERO: the US government program that validated always-on analog sensing.** $30M, 5 years (2015-2020). Proved analog/MEMS sensors operate at 0-10 nW standby (1,000x improvement). Battery life: 4 weeks to 4 years. Performers: Northeastern (zero-power IR, Nature Nanotech), UC Davis/Horsley ($1.8M piezoelectric MEMS accelerometer at 5.4 nW), Sandia (6 nW acoustic+vibration MEMS+CMOS), Draper (zero-power RF receiver <-70 dBm), Arm (M0N0 processor 10 nW sleep), UVA. Generator vibration classification demonstrated. Direct validation of VibroSense-1 analog-first architecture. Commercial influence: Vesper VM1010, Aspinity AML100, TDK InvenSense. |

### Landscape Overviews

| File | What It Covers |
|------|---------------|
| [research/analog-cim-landscape-2025.md](research/analog-cim-landscape-2025.md) | Full landscape: 6 memory technologies, 10+ companies, performance comparison table, DARPA programs, academic highlights. |
| [research/isscc-2025-ai-chips.md](research/isscc-2025-ai-chips.md) | Every AI paper at ISSCC 2025. CIM session (all digital), AI accelerators, LLM chips (Slim-Llama at 4.69mW), industry track. |
| [research/rram-memristor-chips.md](research/rram-memristor-chips.md) | RRAM physics (HfO2 filaments), NeuRRAM, Tsinghua STELLAR, Peking U solver, TetraMem 11-bit, Huawei-ByteDance collab. |

---

## The Numbers That Matter

| Metric | Analog CIM (Best Measured) | Digital CIM (Best) | Conventional GPU/NPU |
|--------|---------------------------|-------------------|---------------------|
| System TOPS/W (INT8) | ~24 (EnCharge, unverified) | 38 (d-Matrix) | 3-5 (Qualcomm/Apple NPU) |
| Macro TOPS/W | 150+ (various claims) | 192.3 (ISSCC 2025) | N/A |
| Effective precision | 3-8 bits (memory dependent) | 8-16 bits (deterministic) | 4-16 bits (deterministic) |
| Largest model on-chip | 80M params (Mythic) | Billions (d-Matrix, external DRAM) | Billions |
| Edge always-on power | 30-100 uW (Aspinity) | ~500 uW (Syntiant) | >1 mW |
| Commercial traction | $6.4M (Mythic 2025) | Shipping (d-Matrix, Axelera) | Dominant |

---

## Key Pattern

**Every analog AI company claims 100x efficiency over GPUs. Every independent measurement shows 2-14x at the system level.** The gap is explained by ADC/DAC overhead (40-85%), precision degradation, calibration costs, and comparison to outdated digital baselines. This is the single most important finding across 26 research files.

---

## Log

| Date | What |
|------|------|
| 2026-03-22 | **27 research files.** Added energy harvesting for always-on vibration sensors. TEG harvesting from motor bearings delivers 1-20 mW continuous — 3x to 60x VibroSense-1's 300 uW budget. Compared 5 sources (TEG, piezo, EM vibration, indoor PV, RF). Surveyed ICs (LTC3108, e-peas AEM30940, Nowi NH2). Everactive PKS3000 reference (2.19 uW idle). Motor bearing dT=15-40°C guarantees harvesting. BOM $22-50/node, 2-3 year payback. 300 uW analog design point enables install-and-forget sensing that 3-10 mW digital competitors cannot achieve. |
| 2026-03-22 | **26 research files.** Deep dive on STMicroelectronics ISM330DHCX Machine Learning Core — primary digital competitor to VibroSense-1. MLC runs 8 decision trees (512 nodes) on-sensor at ~300 uW but limited to 104 Hz classification rate. Cannot do FFT, envelope analysis, or frequency decomposition. At full bandwidth (~1 mW sensor + 5-10 mW MCU for FFT). ISM330BX successor 3x lower power. ST's own reference design (STEVAL-STWINKT1B) uses MCU for real vibration analysis, not MLC alone. "Good enough" for 80% (vibration level/threshold), VibroSense-1 wins on 20% needing always-on diagnostics. |
| 2026-03-22 | **25 research files.** Added DARPA N-ZERO deep dive: the US government's $30M validation of always-on analog sensing (2015-2020). 0-10 nW standby power (1,000x improvement). Battery life 4 weeks→4 years. 6 performers: Northeastern (zero-power IR, Nature Nanotech), UC Davis (5.4 nW piezoelectric accelerometer), Sandia (6 nW MEMS+CMOS), Draper (zero-power RF), Arm (M0N0 10 nW processor), UVA. Generator vibration classification demonstrated. Directly validates VibroSense-1 analog-first architecture. |
| 2026-03-22 | **24 research files.** Added process node comparison for VibroSense-1 commercialization: open PDK comparison (sky130/GF180/IHP SG13G2), commercial analog AI chip process nodes, NRE costs $10K-$400M by node, FD-SOI physics advantages for analog, GF 22FDX recommended for production (BrainChip validated at $2.3M NRE), foundry access for startups, MEMS integration options, full migration roadmap. |
| 2026-03-22 | **23 research files.** Added Everactive deep dive: batteryless vibration sensors via energy harvesting (TEG + PV). PKS3000 SoC at 2.19 uW idle (Hot Chips 2025). Fluke 3562 product shipping with 1 kHz bandwidth (screening only). $161M raised, IMS division sold. VibroSense-1's 20 kHz bandwidth is insurmountable advantage for bearing fault detection. |
| 2026-03-22 | **22 research files.** Added novel & unconventional approaches: 12 approaches ranked. Thermodynamic computing (Extropic TSU, Normal CN101, Unconventional AI $475M). P-bit computing (DAC-free IEDM 2025). Reservoir computing (TDK 80µW). Spintronic CIM (lossless 112.3 TOPS/W). FeFET CIM (FMC €100M). Ising machines. In-sensor computing (shipping). Superconducting, electrochemical, CNT, diffractive, DNA. |
| 2026-03-22 | **21 research files.** Added history and lessons: three waves of analog AI chips (1989-1997, 2012-2022, 2022-present), Intel ETANN, AT&T ANNA, Carver Mead, Synaptics pivot, AI winter, memristor revival, why digital always won, 7 lessons for today's startups, hype cycle analysis. |
| 2026-03-22 | **20 research files.** Added practitioner opinions: chip designer skepticism, HN/community recurring arguments, Mythic postmortem, VC-vs-engineering gap, ML practitioner toolchain frustrations, bull vs bear case. Engineering community significantly more skeptical than VCs. |
| 2026-03-22 | **19 research files.** Added China analog AI deep dive: Tsinghua LEMON lab (STELLAR, 28nm macro, memCS), Peking U (24-bit RRAM solver), Nanjing U (0.101% RMSE precision record), ZJU Darwin Monkey (2.1B neurons), Huawei-ByteDance-Tsinghua ISSCC 2026 alliance, export control analysis, Big Fund III. China leads research, zero commercial products. |
| 2026-03-22 | **17 research files completed.** Added market & investment analysis: $251M analog CIM market, ~$1.5-2B VC invested vs ~$8M revenue, DARPA OPTIMA $78M, Unconventional AI $475M seed anomaly, defense as most receptive segment. |
| 2026-03-22 | **17 research files.** Added academic research labs ecosystem map: top 10 groups, university-to-startup pipeline (Princeton→EnCharge, Michigan→Mythic/Crossbar/MemryX, IBM/ETH→Axelera, Delft→Innatera, Stanford/MIT→Unconventional AI), government funding (DARPA OPTIMA $78M, China $47.5B IC fund, EU Chips JU), imec benchmarking. |
| 2026-03-22 | **16 research files completed.** Full coverage: IBM, Mythic, EnCharge, BrainChip, Intel Loihi, Aspinity/Syntiant/POLYN, photonics, Tsetlin machines, RRAM, emerging startups (Sagence/TetraMem/Blumind/d-Matrix/Axelera/Ceremorphic), ISSCC 2025, ADC/DAC bottleneck, precision/noise, analog for LLMs, design tradeoffs synthesis. |
| 2026-03-22 | Project initialized |
