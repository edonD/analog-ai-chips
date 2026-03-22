# BrainChip Akida: Neuromorphic Edge AI Processor

## Company Overview

**BrainChip Holdings Ltd** (ASX: BRN, OTC: BRCHF) is an Australian-headquartered fabless semiconductor company focused on neuromorphic computing. Founded in 2004, the company went public on the ASX and trades as a penny stock (around $0.12 USD as of late 2025, market cap ~$274M). BrainChip's core product is the **Akida** family of neuromorphic processors -- the name comes from the Greek word for "spike."

BrainChip is notable as one of the very few companies attempting to **commercialize** neuromorphic hardware, as opposed to Intel's Loihi (research-only) and IBM's TrueNorth (research/defense only). Whether they have actually succeeded at commercialization is a different question.

---

## Product Line and Roadmap (as of March 2026)

### AKD1000 (Akida 1.0) -- Shipping since 2022

The first-generation commercial chip. Key specs:

| Parameter | Value |
|-----------|-------|
| Process node | TSMC 28nm CMOS |
| Clock | 300 MHz |
| NPUs | 80 (organized as 20 nodes of 4 NPUs each) |
| NPEs per NPU | 8 Neural Processing Engines |
| Neuron fabric | 1.2 million neurons, 10 billion synapses |
| On-chip SRAM | 8 MB total (40KB weights + 60KB spike data per NPU) |
| Weight precision | 1, 2, 4, or 8-bit |
| Activation precision | 1, 2, 4, or 8-bit |
| Host CPU | Embedded Cortex-M4 |
| Interfaces | USB 3.0, PCIe 2.1, I2S, I3C, UART, JTAG, SPI Flash, LPDDR4 |
| Power | ~30 mW typical (model-dependent; up to ~250 mW under heavy load) |
| Performance | 1.5 TOPS (peak) |
| Supported layers | CNN, DNN (limited); no direct Conv2D-to-Dense connections |
| On-chip learning | Last layer only, binary weights, binary inputs |

Available as bare die, on PCIe cards, on Raspberry Pi HATs, and on an M.2 module ($799 for the Edge AI Box dev kit). This is the only chip that has actually been manufactured and shipped in volume.

### AKD1500 (Akida 2.0 co-processor) -- Taped out, volume production Q3 2026

Second-generation co-processor unveiled at Embedded World North America (November 2025):

| Parameter | Value |
|-----------|-------|
| Process node | GlobalFoundries 22nm FD-SOI |
| Clock | 5-400 MHz (configurable) |
| On-chip SRAM | 1 MB local memory |
| Performance | 800 effective GOPS (~0.8 TOPS) |
| Power | 250 mW typical at 400 MHz; <300 mW in PCIe mode |
| Efficiency | ~3.3 TOPS/W (PCIe), ~5 TOPS/W (serial mode) |
| Interfaces | PCIe Gen2, SPI (S/D/Q/O), SPI memory expansion |
| Package | 7x7 mm MFCTFBGA169, 0.5 mm pitch |
| Target unit cost | $10-20 at scale |
| New features | 8-bit processing, TENNs support, Vision Transformer acceleration |

Tape-out cost: ~$2.3M. Samples available for evaluation; volume production targeted Q3 2026. Neuromorphyx announced as strategic customer/go-to-market partner (March 2026).

### Akida Pico -- IP core, available for FPGA evaluation (February 2026)

Ultra-low-power variant for always-on sensing:

| Parameter | Value |
|-----------|-------|
| Transistor count | 150,000 (without memory) |
| Die area | 0.18 mm^2 (with 50KB SRAM) |
| Power | <1 mW under load; micro-watt standby |
| Architecture | Based on Akida 2.0, single NPU |
| Target apps | Keyword spotting, vital sign monitoring, always-on audio |

Available for remote evaluation via Akida FPGA Cloud. No standalone chip -- this is licensable IP.

### AKD2500 -- In development, prototype Q3 2026

Next-generation silicon project initiated February 2026:

| Parameter | Value |
|-----------|-------|
| Process node | TSMC 12nm |
| Budget | ~$2.5M |
| Development partner | ASICLAND (design, fabrication coordination, packaging, testing) |
| Structure | Multi-project wafer pilot |
| Target | Validate Akida 2.0 on advanced node for defense, industrial, consumer |

### Akida GenAI -- Software/model capability

BrainChip claims a 1.2-billion-parameter LLM running on Akida hardware using TENNs-based architecture. Demonstrated at CES 2026 for on-device mobile/embedded GenAI. Technical details are sparse -- this appears to be more of a demonstration/research capability than a production-ready product.

---

## Architecture Deep Dive

### Event-Driven Processing

Akida is a **fully digital** neuromorphic processor. Unlike analog compute-in-memory chips (Mythic, Analog Devices, IBM AIU), Akida uses standard CMOS digital logic. The "neuromorphic" aspect is the **event-driven processing model**:

1. **Spike-based communication**: Data flows between nodes as binary spikes, not continuous activations. Neurons only fire (and consume energy) when input exceeds a threshold.
2. **Sparsity exploitation**: When input data is sparse (many zeros), most neurons remain idle. Power consumption scales with activity, not clock cycles.
3. **No global synchronization**: NPU nodes communicate asynchronously via event-based messages, without CPU intervention.

This is fundamentally different from conventional digital accelerators (which clock through every MAC operation regardless of data) and from analog CIM (which performs computation in the analog domain using device physics).

### Neural Processing Unit (NPU) Architecture

Each of the 80 NPUs contains:
- 8 Neural Processing Engines (NPEs) -- the actual compute units
- 100KB local SRAM (40KB weights, 60KB spike buffer)
- Event routing logic

Four NPUs form a "node." Twenty nodes comprise the full fabric. The architecture is a mesh where spikes propagate between nodes without centralized scheduling.

### Supported Neural Network Types

**Akida 1.0:**
- Convolutional Neural Networks (CNNs) -- via AkidaNet (MobileNet v1-inspired)
- Deep Neural Networks (standard feedforward)
- Limited on-chip learning (binary weights, last layer only)

**Akida 2.0 additions:**
- Temporal Event-based Neural Networks (TENNs) -- BrainChip's proprietary architecture
- Vision Transformers (ViTs) -- with 8-bit processing
- State Space Models (SSMs)
- Recurrent Neural Networks (RNNs)

### Temporal Event-based Neural Networks (TENNs)

TENNs are BrainChip's key architectural innovation for Akida 2.0. They combine spatial and temporal convolutions to process streaming sequential data:

- **Spatial convolutions** (like standard CNNs) for feature extraction
- **Temporal convolutions** (1D convolutions along the time axis) for sequence modeling
- Replaces the need for RNNs (LSTM, GRU) for time-series tasks
- Claims "orders of magnitude fewer operations" vs. traditional recurrent models
- Particularly suited to: video analytics, audio classification, sensor fusion, predictive maintenance

TENNs are not spiking neural networks in the biological sense. They are a compact convolutional architecture optimized for the event-driven processing model.

### CNN-to-SNN Conversion (MetaTF Toolchain)

The developer workflow:
1. Train a standard Keras/TensorFlow model
2. Quantize using **QuantizeML** (8-bit, 4-bit, 2-bit, or 1-bit)
3. Convert to Akida-executable format using **CNN2SNN**
4. Deploy to hardware

Key limitations of this pipeline:
- Layer mapping is **not one-to-one** with standard Keras layers
- Many layer combinations are unsupported (e.g., Conv2D cannot directly precede Dense)
- Quantization introduces accuracy loss, especially at 4-bit and below
- Quantization-aware training (QAT) is often required to recover accuracy
- API incompatibilities between chip versions cause developer friction
- The ecosystem is young -- debugging requires deep knowledge of both TensorFlow and SNN concepts

---

## Real Benchmark Numbers

### Inference Performance on AKD1000

From academic benchmarking (arXiv:2504.00957) and BrainChip's model zoo:

| Task | Model | Accuracy | Latency | Power | Energy/Inference |
|------|-------|----------|---------|-------|-----------------|
| Image classification | AkidaNet_0.5_224 | 80.0% (top-1) | 41 ms | 215 mW | 9 mJ |
| Object detection | Spiking-YOLOv2 | 94.4% (VOC subset) | 160 ms | 78 mW | 13 mJ |
| Keyword spotting | Spiking-DSCNN | 91.7% | 0.72 ms | 68 mW | 49 uJ |
| On-chip learning | 3 new keywords | 94.7% | 1.5 ms | 41 mW | 62 uJ |
| X-ray classification | Custom | -- | 100-150 ms | -- | -- |
| Traffic monitoring | YOLO variant | -- | 40 ms (24 FPS) | -- | -- |

### ImageNet Accuracy (Model Zoo -- honest numbers)

**Akida 1.0:**
| Model | Resolution | Top-1 Accuracy |
|-------|-----------|---------------|
| AkidaNet 0.25 | 224 | 46.71% |
| AkidaNet 0.5 | 224 | 61.30% |
| AkidaNet 1.0 | 224 | 69.65% |
| MobileNetV1 0.25 | 160 | 36.05% |
| MobileNetV1 1.0 | 160 | 65.47% |

**Akida 2.0 (8-bit PTQ / 4-bit QAT):**
| Model | Resolution | 8-bit Acc. | 4-bit Acc. |
|-------|-----------|-----------|-----------|
| AkidaNet 0.25 | 160 | 48.61% | 40.69% |
| AkidaNet 0.5 | 160 | 61.92% | 57.42% |
| AkidaNet 1.0 | 224 | 72.23% | 69.21% |
| MobileNetV1 1.0 | 224 | 71.31% | 67.72% |

**Context**: MobileNetV1 1.0 at 224px achieves ~70.6% on ImageNet in float32. Akida 2.0 at 8-bit gets 71.31% -- competitive. At 4-bit, it drops to 67.72% -- meaningful but not catastrophic loss.

### Object Detection (PASCAL-VOC)

| Model | Akida 1.0 | Akida 2.0 (8-bit) | Akida 2.0 (4-bit) |
|-------|----------|-------------------|-------------------|
| YOLOv2 | 41.51% mAP | 51.41% mAP | 46.74% mAP |

### Energy Efficiency Comparison

From the academic paper (arXiv:2504.00957), FPS/Watt for object detection:

| Platform | FPS/W |
|----------|-------|
| Akida AKD1000 | 76.92 |
| Embedded GPU (Jetson-class) | 1.34 |
| Desktop CPU | 2.62 |

This is the core value proposition: **~50x better FPS/Watt than embedded GPU** for small models. The catch is that Akida runs much simpler models than what a Jetson can handle.

---

## Commercial Traction -- The Hard Truth

### Revenue

| Period | Revenue (USD) |
|--------|--------------|
| FY2023 | $232,004 |
| FY2024 | $398,011 |
| H1 FY2025 | ~$1,000,000 |
| Q4 FY2025 (quarter) | $1,400,000 (incl. $1.3M engineering revenue) |

These are **not product revenue numbers**. The vast majority is engineering services revenue from government contracts and IP licensing support. Total cumulative revenue through 2024 is under $1M -- for a company with a $274M market cap.

### Cash Position and Burn Rate

- End of 2024: $20M cash
- Quarterly cash burn: ~$3.8M (operating)
- Annual operating cash outflow (2024): $15.9M
- Cash runway: ~4 quarters at burn rate (before the $25M raise)
- **December 2025**: Raised $25M via placement to fund development

BrainChip is a **pre-revenue company** that has been burning cash for years and relies on periodic capital raises to survive.

### Announced Customers and Partners

| Customer/Partner | Nature | Revenue Impact |
|-----------------|--------|---------------|
| **Renesas Electronics** | IP license (Akida 1.0), royalty-bearing, worldwide | License fee (undisclosed); royalties if Renesas ships products |
| **Frontgrade Gaisler** | IP license for space-grade rad-hard SoCs | Engineering revenue (~part of $1.5M from 3 customers) |
| **AFRL (US Air Force)** | $1.8M R&D contract for neuromorphic radar | Government contract revenue |
| **NASA/Ames** | Evaluation kit purchase | Nominal |
| **Neuromorphyx** | Strategic customer for AKD1500 (March 2026) | Evaluation stage |
| **Chelpis Quantum** | AKD1000 purchase for robotic security | Small chip purchase |
| **Parsons/Blue Ridge** | Integration into defense edge-AI platforms | Partnership (no revenue disclosed) |
| **Raytheon** | Sponsor of autonomous vehicle competition | Sponsorship, not a purchase |
| **Nordic Semiconductor** | AkidaTag reference platform | Development partnership |

### Honest Assessment of Commercial Status

The Renesas IP deal (July 2023) is the most significant commercial milestone -- it validates the IP with a major semiconductor company. However, Renesas has not yet announced any product incorporating Akida IP. The AFRL contract is real government R&D money. Everything else is evaluation-stage, partnerships, or sponsorships.

**No volume product incorporating Akida has shipped.** The AKD1000 sells in small quantities to developers. The AKD1500 is not yet in production. The AKD2500 is still in development.

---

## Comparison: Akida vs. Intel Loihi vs. Analog CIM

### Akida vs. Intel Loihi 2

| Dimension | BrainChip Akida (AKD1000) | Intel Loihi 2 |
|-----------|--------------------------|---------------|
| Availability | Commercial (you can buy it) | Research only (INRC members) |
| Process | 28nm CMOS | Intel 4 (7nm-class) |
| Neuron model | Event-based (not LIF) | LIF with programmable dynamics |
| Neurons | 1.2M | 128 neuromorphic cores, ~1M neurons |
| On-chip learning | Last layer, binary only | Full programmable learning engine |
| Software | MetaTF (TensorFlow-based) | Lava framework |
| Target | Commercial edge AI products | Neuroscience research, algorithm development |
| Power (cybersecurity benchmark) | 1 W | 2.5 W |
| Model flexibility | Limited to supported layers | Highly programmable |

Key distinction: Loihi 2 is a **research platform** with much richer neuroscience-inspired features (programmable neuron dynamics, spike-timing-dependent plasticity). Akida trades biological fidelity for **deployment simplicity** -- it is optimized to run quantized CNNs efficiently, not to explore novel SNN algorithms.

Intel announced Loihi 3 (late 2025/2026) with claims of 75x lower latency and 1000x better energy efficiency vs. Jetson Orin Nano on SSM workloads -- but this remains a research chip.

### Neuromorphic (SNN) vs. Analog Compute-in-Memory

| Dimension | SNN/Neuromorphic (Akida) | Analog CIM (e.g., Mythic, IBM AIU) |
|-----------|--------------------------|-------------------------------------|
| Compute domain | Digital, event-driven | Analog (current/voltage) |
| Power scaling | Scales with activity/sparsity | Scales with array utilization |
| Precision | 1-8 bit digital | Typically 4-8 bit analog (noise-limited) |
| Calibration | Not needed (digital) | Required (drift, temperature, device variation) |
| Model support | Limited (custom architectures) | Standard DNNs (often MobileNet, ResNet) |
| Manufacturing | Standard CMOS, high yield | Requires analog design, tighter tolerances |
| Key advantage | Ultra-low power on sparse/event data | High throughput MAC operations in-memory |
| Key weakness | Small model capacity, limited ops | Analog noise, calibration overhead, yield |

The fundamental difference: Akida saves energy by **not computing** (event-driven sparsity). Analog CIM saves energy by **computing more efficiently** (in-memory dot products). These are complementary strategies, and in principle could be combined (SNN on analog CIM hardware).

---

## Circuit-Level Innovations

1. **Pure CMOS digital design**: Unlike many neuromorphic proposals that require exotic devices (memristors, floating-gate transistors), Akida uses standard digital logic. This ensures high yields, low cost, and foundry portability (TSMC 28nm, GF 22nm FD-SOI, TSMC 12nm).

2. **Event-driven power gating**: NPU nodes that receive no spikes consume near-zero dynamic power. Power scales linearly with spike activity rather than clock frequency.

3. **Local SRAM weight storage**: Each NPU stores its own weights locally (40KB), eliminating the memory bandwidth bottleneck that plagues von Neumann architectures. The 8MB total across 80 NPUs is small but sufficient for the compact models Akida targets.

4. **Asynchronous inter-node communication**: Spike messages between nodes propagate without global synchronization, reducing clock distribution power and enabling independent node operation.

5. **Rank Order Coding (ROC)**: Instead of biological LIF neurons, Akida uses a simpler coding scheme where pixel intensities are converted to spike timing order. This is more hardware-efficient than true LIF but less biologically faithful.

6. **GlobalFoundries 22nm FD-SOI** (AKD1500): FD-SOI enables body biasing for dynamic voltage/frequency scaling, further improving energy efficiency at low clock speeds (the chip can run as low as 5 MHz).

---

## Limitations and Red Flags

### Technical Limitations

1. **Small model capacity**: 8MB SRAM (AKD1000) or 1MB (AKD1500) severely limits model size. These chips run MobileNet-class models at best. No chance of running anything resembling a modern transformer or diffusion model.

2. **Accuracy gap**: ImageNet top-1 of 69.65% (Akida 1.0) or 72.23% (Akida 2.0, 8-bit) is well below state-of-the-art (~90%+ for modern architectures). The models Akida can run are 3-5 years behind the accuracy frontier.

3. **No LIF neuron support**: Despite being marketed as "neuromorphic," Akida does not implement the standard Leaky Integrate-and-Fire neuron model used in SNN research. This limits compatibility with the broader SNN research ecosystem.

4. **Severe layer restrictions**: Many standard layer combinations are unsupported. Developers must restructure their models to fit Akida's constraints, which requires significant expertise.

5. **On-chip learning is minimal**: Only the last layer, only binary weights, only binary inputs. This is not general-purpose on-device learning -- it is a very limited few-shot classification trick.

6. **Quantization accuracy loss**: Moving from 8-bit to 4-bit drops accuracy significantly (e.g., 72.23% to 69.21% on AkidaNet). At 2-bit or 1-bit, losses are much worse.

7. **1.2B parameter LLM claim is dubious**: Running a 1.2B parameter model on hardware with 1-8 MB of SRAM is physically impossible without massive external memory and streaming, which would negate the low-power advantage. The CES 2026 demo details are vague.

### Business Red Flags

1. **Revenue is essentially zero**: $398K in FY2024 for a $274M market cap company. Revenue-to-market-cap ratio is ~0.001.

2. **Chronic cash burn**: $15.9M/year operating outflow with no path to profitability visible. The company has been pre-revenue for over 20 years.

3. **Serial capital raising**: The company survives on periodic share placements (LDA Capital, institutional investors). Each raise dilutes existing shareholders.

4. **No volume product shipments**: Despite shipping the AKD1000 since 2022, there are no disclosed volume customers. The Renesas IP deal has not resulted in a shipping product.

5. **Marketing vs. substance gap**: Press releases announce "partnerships" and "strategic customers" that turn out to be evaluation agreements or small purchases. The Raytheon "sponsorship" is marketing, not a design win.

6. **Pattern of delayed timelines**: The AKD1000 was announced years before it shipped. The AKD1500 was unveiled in 2023 but will not reach volume production until Q3 2026. The AKD2500 is budgeted at $2.5M with prototype in Q3 2026 -- extremely optimistic.

---

## Verdict: Real Product or Hype?

**The technology is real.** The AKD1000 exists, it works, independent benchmarks confirm impressive FPS/Watt numbers for small models. The event-driven architecture genuinely delivers ultra-low power for sparse inference tasks. Academic papers corroborate the performance claims. The Renesas IP license and AFRL contract validate that serious organizations see value in the technology.

**The business is not real yet.** After 20+ years of operation and 4+ years with a shipping chip, BrainChip has generated essentially zero product revenue. The company survives on government R&D contracts, IP licensing fees, and capital raises. The market cap of $274M reflects speculative retail investor enthusiasm (particularly on the ASX), not commercial fundamentals.

**The niche is narrow.** Akida excels at one thing: running small neural networks (keyword spotting, simple image classification, anomaly detection) at extremely low power (<250 mW). This is a real market need (IoT, wearables, always-on sensing), but it competes with:
- Microcontroller-based TinyML (ARM Cortex-M with CMSIS-NN)
- Dedicated low-power NPUs from major vendors (Qualcomm, MediaTek, NXP)
- Other neuromorphic startups and research chips

The question is whether Akida's power advantage is large enough to justify the ecosystem switching costs and model limitations. So far, the market has not said yes.

**Watch for**: AKD1500 volume production (Q3 2026) and whether Neuromorphyx or any other customer places meaningful orders. The Renesas product pipeline -- if Renesas ships an SoC with Akida IP, that changes everything. The AKD2500 on TSMC 12nm would demonstrate process portability and potentially much higher performance.

---

## Sources

- [BrainChip Akida IP product page](https://brainchip.com/ip/)
- [BrainChip Akida generations roadmap](https://brainchip.com/akida-generations/)
- [Open Neuromorphic: A Look at Akida](https://open-neuromorphic.org/neuromorphic-computing/hardware/akida-brainchip/)
- [arXiv:2504.00957 - SNN on Commodity Neuromorphic Processors](https://arxiv.org/html/2504.00957v1)
- [BrainChip model zoo performance](https://doc.brainchipinc.com/model_zoo_performance.html)
- [BrainChip AKD1500 co-processor announcement (HPCwire)](https://www.hpcwire.com/aiwire/2025/11/05/brainchip-unveils-akd1500-edge-ai-co-processor-at-embedded-world-north-america/)
- [AKD1500 technical details (CNX Software)](https://www.cnx-software.com/2025/11/18/brainchip-akd1500-pcie-spi-edge-ai-co-processor-to-power-battery-operated-wearables-and-iot-devices/)
- [BrainChip AKD1500 tape-out (Stocks Down Under)](https://stocksdownunder.com/brainchip-2/)
- [AKD1500 volume production announcement (TipRanks)](https://www.tipranks.com/news/company-announcements/brainchip-initiates-akd1500-volume-production-in-response-to-market-demand)
- [BrainChip AKD2500 project announcement (SmallCaps)](https://smallcaps.com.au/article/brainchip-initiates-akd2500-next-generation-silicon-project-development)
- [BrainChip $25M funding (EdgeIR)](https://www.edgeir.com/brainchip-secures-25m-to-push-neuromorphic-ai-into-real-world-edge-devices-20251215)
- [BrainChip Neuromorphyx partnership (BusinessWire)](https://www.businesswire.com/news/home/20260305665563/en/BrainChip-Announces-Neuromorphyx-as-Strategic-Customer-and-Go-to-Market-Partner-for-AKD1500-Neuromorphic-Processor)
- [BrainChip AkidaTag reference platform (Morningstar)](https://www.morningstar.com/news/business-wire/20260310277598/brainchip-enables-the-next-generation-of-always-on-wearables-with-the-akidatag-reference-platform)
- [BrainChip Akida Cloud launch (BusinessWire)](https://www.businesswire.com/news/home/20250805783156/en/BrainChip-Launches-Akida-Cloud-for-Instant-Access-to-Latest-Akida-Neuromorphic-Technology)
- [BrainChip AFRL radar contract (EdgeIR)](https://www.edgeir.com/brainchip-secures-1-8m-afrl-contract-to-advance-neuromorphic-radar-for-edge-military-systems-20241211)
- [Frontgrade Gaisler Akida IP license for space (StockTitan)](https://www.stocktitan.net/news/BRCHF/frontgrade-gaisler-licenses-brain-chip-s-akida-ip-to-deploy-ai-chips-zpyet2oe51f0.html)
- [BrainChip Renesas IP agreement (SmallCaps)](https://smallcaps.com.au/brainchip-akida-nasa-renesas-electronics-america-signs-ip-agreement/)
- [BrainChip Raytheon sponsorship (Robotics & Automation News)](https://roboticsandautomationnews.com/2026/03/08/brainchip-named-official-technology-sponsor-for-raytheons-autonomous-vehicle-competition/99363/)
- [BrainChip financial data (StockAnalysis)](https://stockanalysis.com/quote/otc/BRCHF/)
- [BrainChip quarterly report Q4 FY25](https://investor.brainchip.com/wp-content/uploads/2025/09/Quarterly-Activities-Report-June-2025.pdf)
- [Akida Pico announcement (Hackster.io)](https://www.hackster.io/news/brainchip-shrinks-the-akida-targets-sub-milliwatt-edge-ai-with-the-neuromorphic-akida-pico-c27bce786d2d)
- [Akida Pico specifications (Tom's Hardware)](https://www.tomshardware.com/tech-industry/artificial-intelligence/brainchip-unveils-an-ai-npu-that-consumes-less-than-a-milliwatt)
- [BrainChip TENNs introduction](https://brainchip.com/temporal-event-based-neural-networks-a-new-approach-to-temporal-processing/)
- [Edge Impulse Akida benchmarking](https://www.edgeimpulse.com/blog/brainchip-akida-and-edge-impulse/)
- [BrainChip MetaTF developer tools](https://brainchip.com/metatf-dev-tools/)
- [CNN2SNN toolkit documentation](https://doc.brainchipinc.com/user_guide/cnn2snn.html)
- [Neuromorphic chip comparison (ElProCus)](https://www.elprocus.com/top-neuromorphic-chips-in-2025/)
- [SNN vs analog CIM review (Frontiers in Neuroscience)](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2025.1676570/full)
- [SNN meets in-memory computing (Applied Physics Reviews)](https://pubs.aip.org/aip/apr/article/11/3/031325/3313713/When-in-memory-computing-meets-spiking-neural)
- [Equity.guru critical analysis of BrainChip](https://equity.guru/2025/11/21/brainchip-asx-brn-big-promises-marketing-slop-and-an-ai-company-that-missed-the-ai-boom/)
