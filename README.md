# Analog AI Chips Research — 2025/2026

A deep-dive engineering reference on analog, neuromorphic, and mixed-signal AI chips. The core question: **can analog compute challenge digital for AI inference?**

**Short answer: yes, but only narrowly, and digital is closing the gap fast.**

---

## The Verdict (Updated After 16 Deep Dives)

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

### Market & Business

| File | What It Covers |
|------|---------------|
| **[research/market-and-investment.md](research/market-and-investment.md)** | **The money story.** $251M analog CIM market vs $200B+ total AI chips. ~$1.5-2B VC invested, ~$8M total revenue. Unconventional AI $475M seed. DARPA OPTIMA $78M. Defense most receptive segment. Mythic $6.4M revenue is sector leader. Revenue-to-investment ratio: 0.5%. Honest timeline: $1B market by 2030-2031. |

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

**Every analog AI company claims 100x efficiency over GPUs. Every independent measurement shows 2-14x at the system level.** The gap is explained by ADC/DAC overhead (40-85%), precision degradation, calibration costs, and comparison to outdated digital baselines. This is the single most important finding across 16 research files.

---

## Log

| Date | What |
|------|------|
| 2026-03-22 | **17 research files completed.** Added market & investment analysis: $251M analog CIM market, ~$1.5-2B VC invested vs ~$8M revenue, DARPA OPTIMA $78M, Unconventional AI $475M seed anomaly, defense as most receptive segment. |
| 2026-03-22 | **16 research files completed.** Full coverage: IBM, Mythic, EnCharge, BrainChip, Intel Loihi, Aspinity/Syntiant/POLYN, photonics, Tsetlin machines, RRAM, emerging startups (Sagence/TetraMem/Blumind/d-Matrix/Axelera/Ceremorphic), ISSCC 2025, ADC/DAC bottleneck, precision/noise, analog for LLMs, design tradeoffs synthesis. |
| 2026-03-22 | Project initialized |
