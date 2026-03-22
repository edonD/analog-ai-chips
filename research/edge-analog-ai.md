# Analog and Mixed-Signal Edge AI Chips: The Always-On Frontier

*Research date: 2026-03-22*

The sensor edge is where analog AI has its strongest case. While datacenter analog inference (IBM, Mythic, EnCharge) fights for relevance against NVIDIA's juggernaut, a different class of chips is quietly shipping in millions of devices -- processing audio, vibration, and vision data in the analog domain at microwatt power levels that digital architectures simply cannot match. This file covers the companies, architectures, and hard numbers.

---

## 1. Aspinity: Pure Analog ML Before the ADC

**Company:** Aspinity (Pittsburgh, PA). Founded ~2015, spun out of Carnegie Mellon research. Amazon Alexa Fund investor. Ecosystem partners include STMicroelectronics, Infineon, Renesas.

### The Core Idea: Analyze First, Digitize Later

Aspinity's fundamental insight is that most always-on sensor systems waste enormous power digitizing irrelevant data. A voice-activated device that is listening 24/7 spends the vast majority of its energy digitizing silence. Aspinity's chips process raw analog sensor signals *before* the ADC, identifying relevant events (speech, glass breaking, vibration anomalies) and only waking the digital system when something interesting happens.

This is not analog inference in the datacenter sense (replacing GPU matrix math). This is analog *preprocessing and classification* at the very front of the signal chain.

### Architecture: RAMP and AnalogML

**RAMP (Reconfigurable Analog Modular Processor):** The underlying platform. An array of Configurable Analog Blocks (CABs) -- modular, parallel, continuously-operating analog circuits that can be software-programmed for:
- Signal conditioning and noise reduction
- Feature extraction (spectral analysis, envelope detection)
- Neural network inference (MAC operations in analog)

**Key circuit-level details:**
- MAC operations use a small number of transistors exploiting their nonlinear characteristics -- far fewer transistors than a digital MAC
- Analog non-volatile memory (NVM) stores neural network weights and operating parameters *alongside* the compute elements (true in-memory computing)
- High-precision analog parameters (10+ bit) stored at the compute circuit location
- All-analog MAC and activation functions in each CAB -- no digital conversions between layers
- No interlayer data buffering needed
- Dynamic software-driven trimming compensates for manufacturing and environmental variations on-the-fly

**Supported model types:** CNN, RNN, and other common layer types. Simple and quick compilation from standard ML frameworks to AnalogML hardware.

### AML100 (First Generation -- Shipping)

| Spec | Value |
|------|-------|
| Status | Full production since Q1 2024 |
| Process node | Not publicly disclosed |
| Always-sensing current | <20 uA |
| System power (typical) | <50 uA for most applications |
| Voice activity detection power | ~25 uA (AML100 + microphone: ~125 uW) |
| Compute efficiency | >20 TOPS/W equivalent |
| Operations | 400 MOPS at 40 uW = 10 TOPS/W (customer designs) |
| Sensor inputs | Up to 4 analog sensors (MEMS mic, accelerometer, PIR, ECG, radar, etc.) |
| Package | 7mm x 7mm 48-pin QFN |
| Pricing | $1-2 at million-unit quantities |
| Always-on power reduction vs. digital | >95% |

**Real-world applications demonstrated:**
- **Glass break detection:** >5-year battery life with few to no false alarms to common household sounds. Claimed as industry-best battery life/accuracy combination.
- **Automotive security:** Acoustic-only trigger using analogML algorithms trained to identify car door jiggling, shopping cart impacts, neighboring door dings. Demonstrated at CES 2024 as outperforming g-sensor-based dashcam triggers.
- **Voice activity detection:** Keeps digital processors asleep ~80% of the time when no voice activity present.

### AML200 (Second Generation -- Sampling Q1 2025)

| Spec | Value |
|------|-------|
| Process node | 22nm |
| Peak performance | Up to 2 TOPS |
| Model capacity | 125,000 parameters (scalable beyond) |
| Power consumption | <100 uW typical in battery-operated configurations |
| Precision | 10-bit analog |
| Compute density | 0.86 TOPS/mm^2 |
| Power efficiency | 300 TOPS/W |
| Available as | Chip, die, and licensable IP |

The AML200 represents a significant scale-up. Moving analog circuits to 22nm is non-trivial -- smaller geometries amplify manufacturing variations that compound across analog operations. Aspinity's solution: high-precision analog parameter storage integrated within computational circuits, with stored values functioning as trim mechanisms to compensate for variations. This is an important engineering achievement if the numbers hold in production.

**New workloads enabled by AML200:** RF processing, image processing, broader edge AI inference beyond audio/vibration.

### The Catch with Aspinity

- Model capacity is still small (125K parameters in AML200). This handles keyword spotting, event detection, and simple classification, but not anything resembling a language model or complex vision task.
- The 300 TOPS/W number for AnalogML technology is impressive, but the *absolute* throughput is modest (2 TOPS peak for AML200). These chips are not competing with Hailo or Qualcomm on raw inference performance.
- Commercial traction is unclear. No named OEM customers publicly announced as of early 2026. The automotive demos are promising but no shipping products confirmed.
- Analog variability handling is claimed to be solved, but independent verification (ISSCC paper, third-party teardown) of the trimming approach's long-term reliability is limited.

---

## 2. Syntiant: Digital Near-Memory (Not Analog, Despite the Narrative)

**Company:** Syntiant (Irvine, CA). Founded 2017. Over 10 million chips shipped by 2021. Acquired Knowles Consumer MEMS Microphone division for $150M in December 2024, growing from ~70 to ~1,600 employees and projecting ~$300M revenue for 2025.

### The Architecture Story: From Analog to Digital

Syntiant's origin story involved analog processing -- early descriptions mentioned arrays of hundreds of thousands of multiply-accumulate units linked to NOR flash cells for analog domain inference. But the actual shipping products (NDP100, NDP101, and all subsequent chips) use **digital** techniques.

This pivot is significant. EE Times noted that "this release of digital parts suggests the company realized both the value of pruning neural networks and the challenges of analog computing." Syntiant's success validates that **near-memory digital compute** can achieve extreme efficiency without going analog.

### Architecture: At-Memory Digital Compute

Syntiant's key innovation is **at-memory architecture**: instead of a central processing engine pulling weights from distant memory (the von Neumann bottleneck), Syntiant distributes memory among multiple processing engines. Data movement is minimized because computation happens right next to where weights are stored.

This delivers:
- ~100x efficiency improvement over stored-program architectures (CPUs, DSPs)
- ~10x improvement on streaming audio/video data
- Native neural network processing -- no intermediate compilers

**This is NOT analog computing.** It is highly optimized digital compute with excellent memory architecture. But it achieves similar power efficiency goals for edge AI workloads.

### Product Line

| Chip | Architecture | Performance | Power | Key Feature | Status |
|------|-------------|-------------|-------|-------------|--------|
| NDP100/101 | Core 1 | Baseline | <200 uW | Keyword spotting | Shipped 10M+ |
| NDP120 | Core 2 | 25x Core 1 throughput | <1 mW (280 uW for Google Assistant wake) | Audio + sensor fusion, HiFi3 DSP | Shipping |
| NDP115 | Core 2 variant | Similar to NDP120 | Sub-mW | Ultra-thin package for hearing aids, earbuds | New packages Dec 2025 |
| NDP200 | Core 2T | 6.4 GOPS | <1 mW | Adds vision (DVP interface) | Shipping |
| NDP250 | Core 3 | 30 GOPS | Sub-mW envelope | 6MB on-chip memory, 6M parameters (8-bit), vision + audio + ASR + TTS | Sampling |

**NDP250 details:**
- 120 MHz internal frequency
- HiFi3 DSP with 1.5MB SRAM
- Arm Cortex-M0 with 512KB SRAM
- 6MB total on-chip memory (6x the previous generation)
- Supports CNN, RNN, LSTM, GRU, attention layers, 1D/2D/depthwise convolution
- 2x digital video interfaces, 3x stereo PDM mic/I2S/TDM inputs
- 6.1mm x 5.1mm eWLB package, 120-ball
- 1.8V/3.3V supply with integrated PMU

**MLPerf Tiny benchmark (NDP120):** At low-energy setting, 35.29 uJ and 4.3 ms per keyword spotting inference -- **17x more energy efficient than any other submission** in the category.

### Knowles Acquisition and Vertical Integration

The $150M Knowles CMM acquisition is transformative. Syntiant now owns the MEMS microphone (SiSonic) and the neural processor, enabling end-to-end AI audio solutions. Within 100 days post-acquisition, the team identified 100+ opportunities to deploy Syntiant's AI hardware and software. Revenue projection jumped to ~$300M for 2025.

Syntiant is now positioned as a sensor-to-inference platform, not just a chip company.

### What Syntiant Is and Is Not

**Is:** The most commercially successful ultra-low-power edge AI chip company. Millions of units shipped in earbuds, laptops, phones, smart speakers. Real revenue. Real products.

**Is not:** An analog computing company. The architecture is digital near-memory compute. The "analog" narrative from early days was abandoned. Syntiant proves you can hit microwatt-class power for edge AI workloads with clever digital architecture.

**Workloads:** Primarily keyword spotting, wake word detection, voice commands, acoustic event detection. NDP200/250 extend to vision (person detection, gesture recognition). NDP250's 30 GOPS and attention layer support hint at on-device ASR and even basic TTS.

---

## 3. POLYN Technology: Hardwired Analog Neurons

**Company:** POLYN Technology (Israel). First silicon-proven NASP chip announced October 2025. Available for ordering at CES 2026.

### Architecture: Neuromorphic Analog Signal Processing (NASP)

POLYN's approach is the most radically analog of the companies covered here:

- **Neurons** are implemented with operational amplifiers
- **Axons** (synaptic connections) use thin-film resistors
- The chip operates in **true parallel asynchronous mode** -- no clock, no sequential processing
- Calculations happen without CPU usage or memory access
- Sensor data flow is reduced ~1000x through analog embeddings

**Hybrid architecture:**
- **Fixed portion:** Hardwired analog circuitry for embedding extraction from raw sensor data (feature extractor)
- **Flexible portion:** Standard digital logic or low-power MCU for classification based on the analog embeddings

**Design flow:** Pre-trained networks (from Keras, TensorFlow, PyTorch, MXNet) are converted through POLYN's D-MVP compiler into physical chip layouts. Transfer learning is used -- the first 80-90% of deep network layers maintain fixed weights/structure as the analog feature extractor, with only the final classification layers being flexible.

This means **each NASP chip is partially application-specific** -- the analog portion is physically laid out for a particular feature extraction task. This is fundamentally different from Aspinity's reconfigurable approach.

### First Product: NASP VAD (Voice Activity Detection)

| Spec | Value |
|------|-------|
| Power consumption | ~34 uW continuous operation |
| Inference latency | 50 microseconds |
| Function | Voice activity detection |
| Status | Silicon-proven Oct 2025, ordering at CES 2026 |

### The Catch with POLYN

- The hardwired analog portion limits flexibility. Changing the feature extraction task may require a new chip layout.
- Only VAD demonstrated so far. The technology's extensibility to more complex tasks is unproven in silicon.
- Very early stage commercially -- no volume production, no named customers.
- The 34 uW number is excellent but applies to a very simple task (VAD). Power will increase for more complex workloads.

---

## 4. Innatera: Spiking Neural Networks in Mixed-Signal

**Company:** Innatera (Delft, Netherlands). Spun out of TU Delft research. Over a decade of neuromorphic research behind the product.

### Architecture: Pulsar Neuromorphic MCU

Innatera's Pulsar is the world's first commercial neuromorphic microcontroller, combining:
- **Spiking Neural Network (SNN) engine:** 12 digital cores + 4 analog cores for spiking neurons and synapses
- **RISC-V processor core** for general computation
- **CNN acceleration** for conventional neural network tasks

SNNs operate through **event-driven spikes** -- neurons activate only when new information appears, not on a fixed clock cycle. This is inherently more efficient for sparse, time-varying sensor data.

### Performance

| Application | Power | Latency |
|-------------|-------|---------|
| Radar-based presence detection | 600 uW | Sub-millisecond |
| Audio scene classification | 400 uW | Sub-millisecond |

Claims: 100x lower latency and 500x lower energy than conventional AI processors.

### Key Partnership

Innatera + Socionext: Developing a radar-based sensor for human presence detection that can detect stationary people by their breathing, while ignoring environmental motion (bushes in wind). This is a compelling application that conventional motion sensors (PIR) cannot do.

### Development Tools

Talamo SDK supports building spiking models from scratch (PyTorch-based) or porting existing TensorFlow/PyTorch models to SNN format.

### Status

- Demonstrated at CES 2025 and CES 2026
- Sampling/early production phase
- No volume shipment numbers disclosed

---

## 5. Other Notable Players

### AONDevices (San Jose, CA)

Digital edge AI, not analog, but competing in the same microwatt always-on space.

- **AON1100 M3:** <260 uW for full inference, 20 uA acoustic activity detection idle mode
- **AON1120:** RISC-V core + DSP + 2 NPU coprocessors. <80 uW listening mode, <260 uW at 100% AI processing
- Partnered with TDK InvenSense for always-on voice/sound detection platform
- Demonstrated at CES 2026 with P-Logic for safety tags and wearables

### Ambient Scientific (GPX10 / GPX10 Pro)

Uses **DigAn** silicon architecture -- a hybrid analog-digital approach with configurable matrix computing.

- **GPX10 Pro:** 10 DigAn cores + Arm Cortex-M4F + multi-channel ADC
- **Peak AI performance:** 512 GOPS at ~80 uW (claimed)
- **Comparison:** 100x improvement in power/performance/area over 32-bit MCUs
- 2MB on-chip SRAM, supports up to 8 analog + 20 digital sensors
- Compatible with TensorFlow, Keras, ONNX via Nebula AI toolchain
- Mass production Q1 2026

The 512 GOPS at 80 uW claim is extraordinary -- 6.4 TOPS/W -- and needs independent verification. If real, this would be the highest efficiency in the edge AI class.

### TDK / Hokkaido University: Analog Reservoir Computing

A fundamentally different approach to analog AI:

- **Reservoir computing** uses a fixed, nonlinear dynamical system (the "reservoir") to project input signals into a high-dimensional space, then trains only a simple linear readout layer
- TDK's prototype uses analog electronic circuits mimicking the cerebellum
- Each node: nonlinear resistor + MOS capacitor (memory) + buffer amplifier
- The circuit has **short-term memory** -- temporarily retains input influence for subsequent processing
- Claims: 10x better power consumption and speed than conventional AI
- Won CEATEC 2025 Innovation Award
- Application: Real-time learning of finger movements paired with TDK accelerometers

This is research-stage, not a product. But reservoir computing is a natural fit for analog hardware because the reservoir is fixed (no weight updates needed) and the readout is simple linear algebra.

### SemiQa

- Analog neural network processor using a custom analog memory material (cheaper/more scalable than traditional memristors)
- Matrix of analog memory cells stores sensor data and NN weights
- Processes multiple analog inputs (voice, vibration, video) without ADC conversion
- Demonstrated live analog memory writes/reads at Computex 2025
- Pre-product stage

### Renesas

Not doing analog AI inference, but relevant as an ecosystem partner. Renesas offers digital edge AI MCUs (RA8P1 with Ethos-U55 NPU at 256 GOPS, RZ/V2H at 100 TOPS) and hosts Aspinity's AML100 application board on its Quick-Connect IoT platform. Represents the digital baseline that analog chips are compared against.

### Analog Devices (ADI)

Despite the name, ADI is not making analog AI inference chips. Their AI strategy focuses on intelligent sensing -- extracting data from high-performance analog signal chains for AI training and inference, using NVIDIA-based platforms. ADI sees the future as AI-capable sensor systems, not analog compute replacing digital inference.

---

## 6. Power Consumption Comparison

| Chip | Architecture | Task | Power | Status |
|------|-------------|------|-------|--------|
| POLYN NASP VAD | Analog neuromorphic | Voice activity detection | 34 uW | Silicon-proven 2025 |
| Aspinity AML100 | Analog ML | Always-on sensing (general) | <50 uA (~100 uW @ 1.8V) | Production Q1 2024 |
| Aspinity AML200 | Analog ML (22nm) | Edge AI inference | <100 uW | Sampling Q1 2025 |
| AONDevices AON1120 | Digital (RISC-V + NPU) | Listening mode | 80 uW | Shipping |
| Ambient Scientific GPX10 | Hybrid (DigAn) | Peak AI (512 GOPS) | 80 uW (claimed) | Mass prod Q1 2026 |
| Aspinity AML100 | Analog ML | Voice activity detection | ~45 uW (25 uA) | Production |
| Syntiant NDP100/101 | Digital near-memory | Keyword spotting | <200 uW | Shipped 10M+ |
| AONDevices AON1100 M3 | Digital | Full inference | <260 uW | Shipping |
| Syntiant NDP120 | Digital near-memory | Google Assistant wake | 280 uW | Shipping |
| Innatera Pulsar | Neuromorphic mixed-signal | Audio scene classification | 400 uW | Early production |
| Innatera Pulsar | Neuromorphic mixed-signal | Radar presence detection | 600 uW | Early production |
| Syntiant NDP200 | Digital near-memory | Vision + audio (6.4 GOPS) | <1 mW | Shipping |
| Syntiant NDP250 | Digital near-memory | Multi-modal (30 GOPS) | Sub-mW | Sampling |

**Key observation:** The truly analog chips (Aspinity, POLYN) operate at 30-100 uW. The best digital near-memory chips (Syntiant, AONDevices) operate at 80-300 uW for similar tasks. The gap is real but not as dramatic as marketing suggests -- roughly 2-5x, not 100x. The 95% power savings Aspinity claims come from system-level analysis (keeping the digital processor asleep), not from the analog compute itself being 20x more efficient than digital compute.

---

## 7. What Workloads Can These Handle?

### Proven in Silicon and Shipping

- **Keyword spotting / wake word detection** -- Syntiant (millions shipped), Aspinity, AONDevices
- **Voice activity detection** -- POLYN (34 uW), Aspinity, all others
- **Acoustic event detection** -- Glass break (Aspinity), alarm tones, coughing, snoring
- **Simple voice commands** -- Syntiant NDP120 (local command recognition)

### Demonstrated but Not Yet in Volume

- **Automotive acoustic security** -- Aspinity AML100 (CES 2024 demo)
- **Radar-based presence detection** -- Innatera + Socionext
- **Person detection / simple vision** -- Syntiant NDP200/250
- **Vibration monitoring / predictive maintenance** -- Aspinity AML100
- **Motion prediction** -- TDK reservoir computing prototype

### Beyond Current Capability

- **Automatic speech recognition** -- NDP250 hints at this with attention layer support
- **Text-to-speech** -- NDP250 spec mentions TTS but unclear if practical at sub-mW
- **Complex image classification** -- Beyond simple person detection
- **Any model >125K-6M parameters** -- Model capacity is the hard limit

### The Honest Assessment

These chips handle **simple, narrow classification tasks** -- the kind that can be solved with small CNNs or RNNs with 10K-6M parameters. They are not running anything resembling a foundation model. The primary value proposition is not "analog does better inference" but "analog enables *always-on* inference that would be impossible with digital power budgets."

---

## 8. Circuit-Level Innovations in Analog Feature Extraction

### Aspinity's Approach
- **Analog MAC:** Uses nonlinear characteristics of small transistor clusters. An analog MAC requires "only a handful of transistors" vs. hundreds for a digital equivalent.
- **Weight storage:** Patented analog NVM stores weights as analog values (10+ bit precision) co-located with compute. This eliminates the data movement energy that dominates digital inference (a digital MAC ~250 fJ, but data transfer ~50-100 pJ -- 200-400x more).
- **Activation functions:** Implemented in analog using transistor nonlinearities. No ADC/DAC conversion between layers.
- **Variability compensation:** High-precision stored analog parameters serve as trim values. Dynamic software-driven calibration corrects for process/voltage/temperature variation.

### POLYN's Approach
- **Op-amp neurons:** Each neuron is an operational amplifier circuit implementing the mathematical model of a biological neuron.
- **Resistor synapses:** Thin-film resistors implement synaptic weights. Fixed at fabrication time for the feature extraction layers.
- **Asynchronous operation:** No clock -- signals propagate through the network continuously, enabling 50 us inference latency.
- **Sparse connectivity:** Only necessary connections are physically implemented, reducing chip area and power.

### Innatera's Approach
- **Spiking neurons in silicon:** Analog circuits that generate and propagate spikes, mimicking biological neurons.
- **Event-driven processing:** Computation only occurs when input changes (spikes), making it naturally efficient for sparse sensor data.
- **Hybrid digital-analog:** 12 digital SNN cores + 4 analog cores, combining programmability with analog efficiency.

### TDK Reservoir Computing
- **Nonlinear resistor + MOS capacitor + buffer amplifier** nodes
- **Short-term memory** through capacitor charge/discharge dynamics
- **Fixed reservoir** (no weight training needed for the main network) -- only the linear readout layer is trained

---

## 9. The Fundamental Limitations of Analog Edge AI

### Precision
Analog circuits practically achieve 8-10 bit precision. Aspinity claims 10+ bit. This is sufficient for edge classification tasks but marginal for anything requiring higher numerical accuracy. Digital systems can trivially do 16-32 bit.

### Noise and Drift
Conductance values drift with temperature and time. PCM devices show structural drift; RRAM filaments relax. Even well-designed analog circuits show PVT (process, voltage, temperature) variation. Aspinity's dynamic trimming and POLYN's fixed-weight approach are two different answers to this problem, neither fully validated over multi-year deployment.

### Non-Determinism
Analog inference is inherently non-deterministic -- the same input can produce slightly different outputs due to thermal noise and environmental factors. For edge classification (is this speech? y/n), this is acceptable. For safety-critical applications, it raises qualification concerns.

### Model Size
Current analog edge chips support 10K-6M parameters. This is adequate for keyword spotting but insufficient for modern NLP, complex vision, or any task where the digital world has moved to million-to-billion parameter models.

### Programmability vs. Efficiency Trade-off
POLYN's hardwired approach is extremely efficient but inflexible. Aspinity's reconfigurable approach is more flexible but less efficient. Neither approaches the arbitrary programmability of a digital processor. Changing the feature extraction task may require significant effort (Aspinity) or a new chip (POLYN).

### Calibration Overhead
Robust calibration circuits add complexity, area, and power -- potentially eroding the efficiency advantage. Long-term reliability of analog calibration across industrial temperature ranges (-40 to +85C) and 10+ year lifetimes remains an open question for most of these chips.

---

## 10. Analog at the Sensor Edge vs. Analog for Datacenter Inference

These are fundamentally different propositions:

### Sensor Edge (Aspinity, POLYN, Innatera)
- **Power budget:** 10-1000 uW
- **Model size:** 10K-125K parameters
- **Task:** Simple classification (is this speech? is this a glass breaking? is someone present?)
- **Value proposition:** Enable always-on sensing that is impossible with digital power budgets. Eliminate unnecessary digitization. Extend battery life from months to years.
- **Competition:** Ultra-low-power digital chips (Syntiant, AONDevices) that are already very efficient
- **Market reality:** Niche but real. Glass break sensors, hearing aids, automotive security, IoT sensors. Market ~$250M in 2025, growing at 25.6% CAGR to ~$2.5B by 2035.

### Datacenter / High-Performance Edge (IBM, Mythic, EnCharge)
- **Power budget:** 1-100 W
- **Model size:** Millions to billions of parameters
- **Task:** Complex inference (LLMs, large vision models, recommendation systems)
- **Value proposition:** Replace GPU/TPU inference with 10-100x better energy efficiency
- **Competition:** NVIDIA, AMD, custom ASICs (Google TPU, Amazon Inferentia)
- **Market reality:** Much larger TAM but much harder to compete. Precision, software ecosystem, and reliability requirements are dramatically higher.

### The Verdict

Analog makes its strongest, most defensible case at the sensor edge. The power savings are real (2-5x over best digital, 10-100x over conventional MCUs), the precision requirements are low (8-10 bit is fine for binary classification), and the always-on use case is a genuine capability gap that digital struggles to fill.

For datacenter inference, analog remains a harder sell. The precision requirements are higher, the software ecosystem demands are enormous, the competition is fierce, and digital architectures keep improving. IBM's 2023 analog inference chip showed promise but has not displaced any GPU workloads in production.

The most commercially successful company in this space -- Syntiant, with 10M+ chips shipped and ~$300M projected revenue -- achieved its success by using **digital** near-memory architecture, not analog. That is perhaps the most telling data point about where analog's true advantages lie: not in replacing digital compute, but in preprocessing and filtering sensor data before it ever reaches a digital processor.

---

## 11. Commercial Success Scorecard

| Company | Chips Shipped | Revenue | Named Customers | Production Status |
|---------|--------------|---------|-----------------|-------------------|
| Syntiant | 10M+ (by 2021, likely much higher now) | ~$300M projected 2025 | Google (Assistant wake word), Arduino (Nicla Voice), Amazon, laptop/earbud OEMs | Volume production, multiple generations |
| Aspinity | Not disclosed | Not disclosed | No named OEMs; STMicro, Infineon, Renesas as ecosystem partners | AML100 in production; AML200 sampling |
| AONDevices | Not disclosed | Not disclosed | TDK InvenSense partnership, P-Logic | Shipping |
| Innatera | Not disclosed | Not disclosed | Socionext partnership | Early production/sampling |
| POLYN | Not disclosed | Not disclosed | None announced | Just reached silicon; CES 2026 ordering |
| Ambient Scientific | Not disclosed | Not disclosed | None announced | GPX10 Pro mass prod Q1 2026 |

Syntiant is the clear leader by a wide margin. Everyone else is in various stages of early commercialization.

---

## Sources

- [Aspinity AML100 Product Page](https://www.aspinity.com/aml100/)
- [Aspinity AnalogML Technology](https://www.aspinity.com/technology/)
- [Aspinity AML200 Product Page](https://www.aspinity.com/aml200/)
- [Aspinity AML200 Blog Post](https://www.aspinity.com/blog/scaling-the-next-generation-analogml-the-aml200/)
- [Aspinity AML100 Glass Break Detection](https://www.aspinity.com/press-releases/aspinity-aml100-solution-delivers-industry-best-battery-life-accuracy-combo-for-glass-break-sensors/)
- [Aspinity Automotive Security (BusinessWire, March 2024)](https://www.businesswire.com/news/home/20240327176420/en/Aspinity-Launches-New-AML100-Near-Zero-Power-Monitoring-Solutions-for-Automotive-Security)
- [Aspinity Tackles Analog Variability (TechInsights)](https://www.techinsights.com/blog/aspinity-tackles-analog-variability)
- [Aspinity RAMP Technology](https://www.aspinity.com/RAMP-Technology)
- [Aspinity Analog Neural Net Wake-Up Call (SemiEngineering)](https://semiengineering.com/aspinitys-analog-neural-net-wake-up-call/)
- [Aspinity Puts Neural Networks Back to Analog (EE Times)](https://www.eetimes.com/aspinity-puts-neural-networks-back-to-analog/)
- [Syntiant NDP250 Product Page](https://www.syntiant.com/ndp250)
- [Syntiant NDP250 Launch (GlobeNewsWire, April 2024)](https://www.globenewswire.com/en/news-release/2024/04/09/2859793/0/en/Syntiant-Unveils-NDP250-Neural-Decision-Processor-with-Next-Gen-Core-3-Architecture.html)
- [Syntiant NDP250 At-Memory Architecture (XPU.pub)](https://xpu.pub/2024/04/18/syntiant-ndp250/)
- [Syntiant Ships 10M Processors (Design-Reuse)](https://www.design-reuse.com/news/49292/syntiant-10-million-processors-shipped.html)
- [Syntiant NDP120 MLPerf Tiny Results](https://www.edge-ai-vision.com/2022/04/syntiant-ndp120-achieves-outstanding-results-in-latest-mlperf-tiny-v0-7-benchmark-suite/)
- [Syntiant Knowles Acquisition Completed (GlobeNewsWire, Dec 2024)](https://www.globenewswire.com/news-release/2024/12/30/3002608/0/en/Syntiant-Completes-Acquisition-of-Knowles-Consumer-MEMS-Microphone-Division.html)
- [Syntiant Rolls AI Chips for Audio (EE Times)](https://www.eetimes.com/startup-rolls-ai-chips-for-audio/)
- [Syntiant NDP115 New Packages (Dec 2025)](https://www.manilatimes.net/2025/12/29/tmt-newswire/globenewswire/syntiant-expands-ndp115-portfolio-with-new-ewlb-and-ultra-thin-packages-bringing-advanced-edge-ai-to-ultra-compact-devices/2250445)
- [POLYN NASP Technology](https://polyn.ai/technology-3/)
- [POLYN First Silicon NASP Chip (Oct 2025)](https://polyn.ai/polyn-technology-announces-first-silicon-implemented-nasp-chip/)
- [POLYN CES 2026 Demo](https://polyn.ai/ultra-low-power-ai-voice-detection-demo-by-polyn-at-ces-2026/)
- [POLYN Silicon Implementation (EDN)](https://www.edn.com/polyn-delivers-silicon-implementation-of-its-nasp-chip/)
- [Innatera Pulsar Product Page](https://innatera.com/pulsar)
- [Innatera Pulsar (IEEE Spectrum)](https://spectrum.ieee.org/innatera-neuromorphic-chip)
- [Innatera CES 2025 (PRNewsWire)](https://www.prnewswire.com/news-releases/innatera-showcases-revolutionary-neuromorphic-processor-enabling-next-generation-ambient-intelligence-at-ces-2025-302344581.html)
- [Innatera CES 2026](https://innatera.com/press-releases/redefining-the-cutting-edge-innatera-debuts-real-world-neuromorphic-edge-ai-at-ces-2026)
- [AONDevices AON1100 M3 (GlobeNewsWire, Jan 2026)](https://www.globenewswire.com/news-release/2026/01/02/3212166/0/en/AONDevices-and-TDK-InvenSense-Unveil-Super-Low-Power-Always-On-Voice-and-Sound-Detection-Platform-Powered-by-the-AON1100-M3-Processor.html)
- [AONDevices AON1120 (Hackster.io)](https://www.hackster.io/news/aondevices-promises-ultra-low-power-always-on-edge-ai-with-its-aon1120-risc-v-chip-fc9a63eaa595)
- [Ambient Scientific GPX10 Pro (Embedded Computing Design)](https://embeddedcomputing.com/technology/processing/chips-and-socs/ambient-scientific-launches-gpx10-pro-ai-native-soc-for-battery-powered-edge-devices)
- [TDK Analog Reservoir AI Chip (Oct 2025)](https://www.tdk.com/en/news_center/press/20251002_01.html)
- [TDK Reservoir Computing (IEEE Spectrum)](https://spectrum.ieee.org/analog-reservoir-computer)
- [SemiQa Analog AI Chip (Hackster.io)](https://www.hackster.io/news/analog-ai-the-neuromorphic-chip-from-semiqa-563e23d9d894)
- [Analog AI Chip Market Size (Precedence Research)](https://www.precedenceresearch.com/analog-ai-chip-market)
- [Analog vs Digital In-Sensor Computing (GLSVLSI 2025)](https://dl.acm.org/doi/10.1145/3716368.3735297)
- [AI at the Edge: Low Power, High Stakes (Edge AI Vision Alliance, Nov 2025)](https://www.edge-ai-vision.com/2025/11/ai-at-the-edge-low-power-high-stakes/)
