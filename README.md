# Analog AI Chips Research & VibroSense-1 Chip Design

**32 research files. 23 design files. 25,000+ lines. One thesis.**

> Analog preprocessing at 300uW enables diagnostic-grade, batteryless industrial vibration sensing that digital approaches at 3-10mW cannot match. This is the one niche where analog wins definitively.

---

## Quick Navigation

| I want to... | Go to |
|--------------|-------|
| **Understand the analog AI landscape** | [Part 1: Research](#part-1-analog-ai-chip-research) |
| **See the chip we're building** | [Part 2: VibroSense-1](#part-2-vibrosense-1-chip-design) |
| **Launch parallel design agents** | [vibrosense/README.md](vibrosense/README.md) |
| **Read the competitive analysis** | [research/competitive-landscape-vibration.md](research/competitive-landscape-vibration.md) |
| **Understand the business case** | [research/market-and-investment.md](research/market-and-investment.md) |
| **Start designing (block specs)** | [vibrosense/00_bias/](vibrosense/00_bias/) through [vibrosense/10_fullchain/](vibrosense/10_fullchain/) |

---

# Part 1: Analog AI Chip Research

**Core question: can analog compute challenge digital for AI?**

**Short answer: yes, but only narrowly, and digital is closing the gap fast.**

### Where Analog Wins

1. **Always-on sensor edge (<1 mW):** The signal is already analog. Preprocessing before the ADC saves 10-30x power by keeping digital systems asleep. DARPA N-ZERO proved this with $30M of research.

2. **Moderate edge inference (1-10W):** Capacitor-based CIM (EnCharge: ~24 TOPS/W) and flash CIM (Mythic: ~8 TOPS/W) deliver real 2-7x gains over conventional NPUs.

### Where Analog Loses

1. **LLMs:** 250-1000x capacity gap. No analog chip has run a real LLM. Timeline: 2030+ if ever.
2. **Datacenter:** Digital CIM (d-Matrix: 38 TOPS/W, $2B valuation) matches analog with deterministic accuracy.
3. **ISSCC 2025:** Zero analog CIM papers in the CIM session. Digital SRAM CIM hit 192.3 TFLOPS/W.

### The Three Killers

1. **ADC/DAC overhead:** 40-85% of system power → [research/adc-dac-bottleneck.md](research/adc-dac-bottleneck.md)
2. **Precision ceiling:** 3-8 bits analog vs deterministic digital → [research/precision-noise-challenges.md](research/precision-noise-challenges.md)
3. **Software ecosystem:** No CUDA equivalent → [research/design-tradeoffs-synthesis.md](research/design-tradeoffs-synthesis.md)

### Key Pattern

**Every analog AI company claims 100x efficiency over GPUs. Every independent measurement shows 2-14x at the system level.**

---

## All 32 Research Files

### Synthesis & Design Guides

| # | File | What It Answers |
|---|------|----------------|
| 1 | [design-tradeoffs-synthesis.md](research/design-tradeoffs-synthesis.md) | How to design an analog AI chip (memory tech, ADC, precision, process node, software, failures) |
| 2 | [analog-for-llms.md](research/analog-for-llms.md) | Can analog run LLMs? (No. 2030+ if ever.) |
| 3 | [adc-dac-bottleneck.md](research/adc-dac-bottleneck.md) | Why 100x claims collapse to 2-10x (ADC/DAC eats 40-85%) |
| 4 | [precision-noise-challenges.md](research/precision-noise-challenges.md) | Physics limits: 8 noise sources, drift, temperature, memory tech ranking |

### Company Deep Dives (13 companies)

| # | File | Company | One-Line Verdict |
|---|------|---------|-----------------|
| 5 | [encharge-ai.md](research/encharge-ai.md) | EnCharge AI | Most promising analog CIM (capacitor, ~24 TOPS/W), no independent benchmarks |
| 6 | [mythic-ai.md](research/mythic-ai.md) | Mythic AI | Best-funded ($300M+), Gen 1 real (~8 TOPS/W), Gen 2 unverified |
| 7 | [ibm-analog-ai.md](research/ibm-analog-ai.md) | IBM Research | Strongest research (HERMES, 14x over digital), years from production |
| 8 | [brainchip-akida.md](research/brainchip-akida.md) | BrainChip | Tech works, business failing ($398K revenue on $274M cap) |
| 9 | [intel-loihi.md](research/intel-loihi.md) | Intel Loihi | Groundbreaking research, commercial dead end (8+ years, zero revenue) |
| 10 | [rain-ai.md](research/rain-ai.md) | Rain AI | Cautionary tale (memristor dream → fire sale, Altman conflict) |
| 11 | [edge-analog-ai.md](research/edge-analog-ai.md) | Aspinity, Syntiant, POLYN, Innatera | Syntiant won (10M+ shipped) but is digital; Aspinity purest analog |
| 12 | [emerging-startups.md](research/emerging-startups.md) | Sagence, TetraMem, d-Matrix, Axelera, Ceremorphic | Digital CIM ($2B d-Matrix, $450M Axelera) far ahead |
| 13 | [photonic-ai-chips.md](research/photonic-ai-chips.md) | Lightmatter, Ayar Labs | Interconnect shipping; compute pre-commercial (2028+) |
| 14 | [tsetlin-machines.md](research/tsetlin-machines.md) | Literal Labs, Anzyz | Logic-based AI (AND/OR/NOT), efficient for tiny tasks |
| 15 | [stm-ism330-ml-core.md](research/stm-ism330-ml-core.md) | STM ISM330DHCX | Primary digital competitor — ML Core limited to 104Hz, no FFT |
| 16 | [everactive-batteryless.md](research/everactive-batteryless.md) | Everactive | Batteryless sensors shipping, but only 1kHz — can't detect bearings |

### Market, Business & Competitive

| # | File | What It Answers |
|---|------|----------------|
| 17 | [market-and-investment.md](research/market-and-investment.md) | $251M analog CIM market, ~$1.5-2B VC invested, ~$8M total revenue |
| 18 | [competitive-landscape-vibration.md](research/competitive-landscape-vibration.md) | Every vibration monitoring player, why ADI/STM won't build this, 6 barriers |
| 19 | [energy-harvesting-sensors.md](research/energy-harvesting-sensors.md) | 300uW harvestable with 7-67x margin from motor bearing heat |
| 20 | [process-node-comparison.md](research/process-node-comparison.md) | sky130 prototype → GF 22FDX production (300uW → 60-100uW) |

### Landscape & Conferences

| # | File | What It Answers |
|---|------|----------------|
| 21 | [analog-cim-landscape-2025.md](research/analog-cim-landscape-2025.md) | Full landscape: 6 memory techs, 10+ companies, DARPA programs |
| 22 | [isscc-2025-ai-chips.md](research/isscc-2025-ai-chips.md) | Every AI paper at ISSCC 2025 (zero analog CIM in CIM session) |
| 23 | [rram-memristor-chips.md](research/rram-memristor-chips.md) | RRAM physics, NeuRRAM, TetraMem 11-bit, Chinese RRAM efforts |

### Academic, Regional & Historical

| # | File | What It Answers |
|---|------|----------------|
| 24 | [academic-research-labs.md](research/academic-research-labs.md) | Top 10 labs, university-to-startup pipeline, funding sources |
| 25 | [china-analog-ai.md](research/china-analog-ai.md) | China leads research (Tsinghua, Peking U), zero startups |
| 26 | [history-and-lessons.md](research/history-and-lessons.md) | Three waves of analog AI (1989, 2012, 2022), why it keeps failing |
| 27 | [practitioner-opinions.md](research/practitioner-opinions.md) | Engineers skeptical, VCs bullish, $475M seed vs $8M sector revenue |
| 28 | [novel-unconventional-approaches.md](research/novel-unconventional-approaches.md) | 12 exotic approaches: thermodynamic, spintronic, FeFET, reservoir |
| 29 | [darpa-nzero-sensors.md](research/darpa-nzero-sensors.md) | DARPA's $30M validation of always-on analog sensing |

### Chip Design Plans

| # | File | What It Answers |
|---|------|----------------|
| 30 | [build-plan-pragmatic.md](research/build-plan-pragmatic.md) | Original CIM chip plan (superseded by VibroSense-1) |
| 31 | [vibrosense-chip-architecture.md](research/vibrosense-chip-architecture.md) | VibroSense-1 system architecture, SPICE simulations, revenue model |

---

# Part 2: VibroSense-1 Chip Design

**Always-on analog vibration anomaly detection for industrial predictive maintenance.**

### The Product Thesis

> At 300uW, VibroSense-1 is the only chip that does diagnostic-grade vibration classification (4-class, 20kHz bandwidth, ISO 10816 features) within an energy-harvestable power budget. Everactive can't diagnose bearing faults (1kHz). STM's ML Core can't classify fault types (104Hz, no FFT). MCU+FFT can't be energy-harvested (3-10mW). **VibroSense-1 + thermoelectric harvester = zero-maintenance, diagnostic-grade, install-and-forget industrial sensor.**

### Architecture

```
MEMS Accel → PGA → 5 Gm-C Band-Pass Filters → 5 Envelope Detectors → 8-Feature Vector
                                                                            ↓
                                                            Charge-Domain MAC Classifier
                                                            (128 MIM caps, 4-bit weights)
                                                                            ↓
                                                                   4-Class Output
                                                            (Normal / Imbalance / Bearing / Looseness)
                                                                            ↓
                                                                    IRQ → Wake MCU → Transmit
```

### Key Specs

| Spec | Value | Comparison |
|------|-------|-----------|
| Always-on power | 300 uW (sky130), 60-100 uW (22FDX production) | STM ISM330 MLC: 300uW but can't diagnose |
| Bandwidth | 100 Hz - 20 kHz (5 ISO 10816 bands) | Everactive: 1 kHz only |
| Classification | 4-class (normal, imbalance, bearing, looseness) | Aspinity: binary only |
| Features | 8 (5 band RMS + broadband RMS + crest + kurtosis) | ISM330 MLC: no frequency decomposition |
| Weight precision | 4-bit (MIM capacitor ratios) | |
| Battery life (300mAh) | 3-5 years (sky130), 10+ years (22FDX) | MCU+FFT: 6-12 months |
| Energy harvestable? | **YES** (TEG delivers 7-67x margin) | MCU+FFT: NO |
| Process | Sky130 prototype → GF 22FDX production | |
| Tapeout cost | $700 (Tiny Tapeout) to $15K (chipIgnite) | |

### Design Blocks (11 parallel agents)

Full specifications in [vibrosense/README.md](vibrosense/README.md). Each block has its own `program.md` (500-1000 lines) and `requirements.md`.

| Block | Lines | What | Parallelism |
|-------|-------|------|-------------|
| [00_bias](vibrosense/00_bias/) | 1,054 | Beta-multiplier 500nA current reference | Wave 1 (independent) |
| [01_ota](vibrosense/01_ota/) | 973 | Folded-cascode OTA, 65dB gain, 50kHz UGB | Wave 1 (independent) |
| [02_pga](vibrosense/02_pga/) | 583 | Capacitive-feedback PGA, 4 gain settings | Wave 2 (needs OTA) |
| [03_filters](vibrosense/03_filters/) | 819 | 5-channel Gm-C Tow-Thomas BPF bank | Wave 2 (needs OTA) |
| [04_envelope](vibrosense/04_envelope/) | 918 | Precision rectifier + LPF envelope detectors | Wave 2 (needs OTA) |
| [05_rms_crest](vibrosense/05_rms_crest/) | 500 | Broadband RMS + peak detector + crest factor | Wave 2 (needs OTA) |
| [06_classifier](vibrosense/06_classifier/) | 598 | Charge-domain MAC, 128 MIM caps, 4-class | Wave 1 (independent) |
| [07_adc](vibrosense/07_adc/) | 803 | 8-bit SAR ADC (on-demand, adapted from JKU) | Wave 1 (independent) |
| [08_digital](vibrosense/08_digital/) | 702 | SPI + FSM + debounce (Verilog RTL) | Wave 1 (independent) |
| [09_training](vibrosense/09_training/) | 865 | CWRU Bearing Dataset + 4-bit quantization | Wave 1 (Python only) |
| [10_fullchain](vibrosense/10_fullchain/) | 986 | End-to-end integration + verification | Wave 3 (after all) |

### Competitive Position

| | VibroSense-1 | STM ISM330 MLC | Everactive | Aspinity AML100 | POLYN VibroSense |
|---|---|---|---|---|---|
| Fault diagnosis | **4-class** | Threshold only | Screening only | Binary only | Binary only |
| Bandwidth | **20 kHz** | Limited | 1 kHz | <10 kHz | Unknown |
| Energy harvestable | **Yes** | Borderline | Yes | Yes | Yes |
| Open source | **Yes** | No | No | No | No |
| Production status | Design | Shipping | Shipping | Shipping | Pre-production |
| Power | 300 uW | ~300 uW | 2 uW | 36 uW | 100 uW claimed |

### Business Path

1. **Sky130 prototype** ($700-15K) → proves architecture works
2. **DARPA/NSF SBIR** ($500K-2M) → funds 22FDX tapeout
3. **22FDX production** ($2-4M NRE) → 60-100uW, competitive power
4. **Sell sensor nodes** at $150-300 → 75-90% gross margin
5. **Or license IP** to Fluke/SKF/ADI → they sell nodes, you collect royalties

---

## Log

| Date | What |
|------|------|
| 2026-03-22 | **32 research + 23 design files.** Complete analog AI landscape research, VibroSense-1 chip design (11 blocks, 9,700 lines of specs), competitive analysis, energy harvesting validation, process roadmap, DARPA citation chain. |
| 2026-03-22 | Project initialized |
