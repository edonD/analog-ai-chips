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

The signal chain processes raw vibration data through analog stages, extracts features, classifies the fault type using a charge-domain neural network, and outputs a digital result — all within a 300 uW power budget.

#### Block 00: Bias Generator (`00_bias/`) — Wave 1
**Beta-multiplier current reference producing a stable 500 nA bias current.**
Uses a self-biased beta-multiplier topology with a startup circuit. The reference current feeds all downstream OTA stages. Designed for low sensitivity to supply voltage (high PSRR) and temperature (PTAT + CTAT cancellation). The 500 nA target keeps total bias power under 10 uW at 1.8 V.

#### Block 01: Operational Transconductance Amplifier (`01_ota/`) — Wave 1
**Folded-cascode OTA: 65 dB gain, 50 kHz unity-gain bandwidth, phase margin >60 degrees.**
The core analog building block reused by Blocks 02-05. Folded-cascode topology gives high gain in a single stage (no compensation capacitor needed), while the low UGB matches the vibration signal bandwidth (100 Hz - 20 kHz). Designed for 1.8 V supply, 0.9 V common-mode, rail-to-rail output not required (signals are ±250 mV around Vcm).

#### Block 02: Programmable Gain Amplifier (`02_pga/`) — Wave 2 (needs OTA)
**Capacitive-feedback PGA with 4 digitally selectable gain settings (6/12/24/48 dB).**
Matches the MEMS accelerometer output (1-100 mV) to the filter bank input range (±250 mV). Uses capacitor-ratio gain (C_in/C_fb) for accuracy independent of OTA open-loop gain. Gain is set by switching between 4 feedback cap values via NMOS/PMOS transmission gates controlled by 2-bit digital code from the SPI interface.

#### Block 03: Band-Pass Filter Bank (`03_filters/`) — Wave 2 (needs OTA)
**Five parallel Gm-C Tow-Thomas band-pass filters spanning 100 Hz - 20 kHz.**
Decomposes the vibration spectrum into 5 ISO 10816 frequency bands to separate fault signatures: Band 1 (100-300 Hz, imbalance), Band 2 (300-1 kHz, misalignment), Band 3 (1-5 kHz, bearing outer race BPFO), Band 4 (5-10 kHz, bearing inner race BPFI), Band 5 (10-20 kHz, ball spin BSF). Each filter uses the Block 01 OTA as its transconductor. Q factor ~5 per band.

#### Block 04: Envelope Detectors (`04_envelope/`) — Wave 2 (needs OTA)
**Five precision rectifier + low-pass filter circuits extracting the RMS envelope of each band.**
Bearing faults produce amplitude-modulated signatures at the ball-pass frequency. The envelope detector extracts this modulation. Uses a precision half-wave rectifier (OTA + diode-connected MOSFET) followed by a first-order Gm-C LPF with ~10 Hz cutoff. Output is a slowly varying DC level (0-500 mV) proportional to band energy — the feature input to the classifier.

#### Block 05: RMS / Crest Factor (`05_rms_crest/`) — Wave 2 (needs OTA)
**Broadband RMS detector, peak detector, and crest factor computation.**
Provides 3 additional features beyond the 5 band envelopes: broadband RMS (overall vibration level), peak amplitude (impulse detection), and crest factor (peak/RMS ratio — high crest indicates bearing spalling). The RMS circuit uses a squarer-divider feedback loop. Peak detector uses a fast-charge, slow-discharge capacitor circuit. These 3 features plus 5 band envelopes = 8-dimensional feature vector for classification.

#### Block 06: Charge-Domain MAC Classifier (`06_classifier/`) — Wave 1 — COMPLETE (10/10 PASS)
**Four 8-input × 4-bit-weight multiply-accumulate units using charge-domain computation, followed by a 3-comparator winner-take-all tree. Verified in ngspice with SKY130 BSIM4 models.**

This is the core "neural network" of the chip. It classifies the 8-feature input vector into one of 4 fault classes (Normal, Imbalance, Bearing, Looseness) using a single-layer dot-product + argmax architecture — entirely in the analog domain, with zero ADCs.

**How it works:**
- Each MAC unit has 32 MIM capacitors (8 inputs × 4 binary-weighted bits: 50/100/200/400 fF) with 10% bottom-plate parasitics.
- **Sample phase (phi_s):** Transmission gates charge each capacitor's top plate to the corresponding input voltage. Charge stored = C_weight × V_feature.
- **Evaluate phase (phi_e):** All capacitor top plates connect to a shared bitline. Charge redistribution produces Vbl = Sigma(C_wi × V_fi) / C_total — this IS the dot product.
- **Reset phase (phi_r):** All nodes discharged to ground.
- A binary tree of 3 StrongARM latch comparators (10 transistors each) identifies the MAC with the highest bitline voltage — the winning class.
- A NAND-based non-overlapping 3-phase clock generator (28 transistors) sequences the phases.

**Key results (ngspice-42, SKY130 BSIM4):**
| Metric | Spec | Result |
|--------|------|--------|
| MAC linearity | <2 LSB | 0.08 LSB |
| Charge injection | <1 LSB | 0.307 LSB |
| Multi-input error | <2% | 0.4% |
| WTA margin | >5 mV | 19.3 mV |
| Monte Carlo accuracy | >85% | 99.5% (200 runs) |
| Corner variation | <5% | 0.11% (5 corners) |
| Power @ 10 Hz | <5 uW | <0.001 uW |

Total: ~702 transistors, ~260 capacitors. Full design report: [06_classifier/README.md](vibrosense/06_classifier/README.md).

#### Block 07: SAR ADC (`07_adc/`) — Wave 1
**8-bit successive-approximation ADC for on-demand digital readout.**
Not on the always-on signal path — only activated when the MCU wakes up and requests a raw waveform snapshot. Uses a charge-redistribution DAC (binary-weighted caps, same MIM process as the classifier) and a StrongARM comparator (shared design with Block 06). Adapted from the JKU open-source SAR ADC. Target: 100 kS/s, ENOB > 7 bits, <50 uW when active.

#### Block 08: Digital Control (`08_digital/`) — Wave 1
**SPI slave interface, classification FSM, IRQ generation, and debounce logic in synthesizable Verilog RTL.**
The SPI interface loads 4-bit weights into the classifier (128 bits total = 4 classes × 8 inputs × 4 bits) and reads back classification results. The FSM sequences the classifier operation: (1) wait for trigger, (2) assert phi_s/phi_e/phi_r, (3) latch comparator outputs, (4) debounce over N consecutive classifications, (5) assert IRQ if fault detected. Debounce prevents false alarms from single noisy classifications.

#### Block 09: Training & Quantization (`09_training/`) — Wave 1 (Python only)
**Offline weight training on the CWRU Bearing Dataset with 4-bit quantization-aware training.**
The CWRU dataset (Case Western Reserve University) is the standard benchmark for bearing fault classification, containing vibration recordings from normal, inner-race, outer-race, and ball-fault bearings at multiple loads. This block trains a simple linear classifier (matching the single MAC-layer hardware), then quantizes the float32 weights to 4-bit integers (0-15) using quantization-aware fine-tuning to minimize accuracy loss. Output: 128 weight values loaded via SPI (Block 08) into the classifier caps.

#### Block 10: Full-Chain Integration (`10_fullchain/`) — Wave 3 (after all blocks)
**End-to-end SPICE simulation of the complete analog signal chain from MEMS input to digital class output.**
Connects all blocks in sequence and verifies: (1) signal integrity across block interfaces (voltage levels, common-mode, bandwidth), (2) total power budget stays within 300 uW, (3) classification accuracy on realistic vibration waveforms from the CWRU dataset, (4) stability under process corners (SS/FF/SF/FS/TT) and temperature (-40 to +125C industrial range). This is the final validation before layout.

#### Design Parallelism

```
Wave 1 (independent):  00_bias | 01_ota | 06_classifier* | 07_adc | 08_digital | 09_training
Wave 2 (needs OTA):    02_pga  | 03_filters | 04_envelope | 05_rms_crest
Wave 3 (needs all):    10_fullchain

* 06_classifier is COMPLETE with 10/10 specs PASS
```

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
| 2026-03-23 | **Block 06 Classifier COMPLETE.** Full 8×4-bit charge-domain MAC classifier verified in ngspice with SKY130 BSIM4 models. 10/10 specs PASS: 0.08 LSB linearity, 0.4% multi-input error, 19.3 mV WTA margin, 99.5% Monte Carlo accuracy, 0.11% corner variation, <0.001 uW at 10 Hz. ~702 transistors, ~260 caps. |
| 2026-03-22 | **32 research + 23 design files.** Complete analog AI landscape research, VibroSense-1 chip design (11 blocks, 9,700 lines of specs), competitive analysis, energy harvesting validation, process roadmap, DARPA citation chain. |
| 2026-03-22 | Project initialized |
