# Tsetlin Machines: Logic-Based AI and Hardware Implementations

*Research date: 2026-03-22*

---

## Executive Summary

The Tsetlin Machine (TM) is a fundamentally different approach to machine learning that replaces arithmetic (multiply-accumulate) with propositional logic (AND, OR, NOT). Invented by Ole-Christoffer Granmo at the University of Agder, Norway, in 2018, it achieves competitive accuracy with neural networks on many benchmarks while requiring only bitwise operations for inference. This makes it exceptionally hardware-friendly: a 65nm ASIC achieves **8.6 nJ per MNIST classification** -- the lowest reported for any fully-digital manufactured accelerator at comparable accuracy. Two commercial efforts (Literal Labs in the UK, Anzyz Technologies in Norway) are attempting to bring TM-based products to market.

**The catch**: Tsetlin machines handle classification and structured pattern recognition well, but they have not demonstrated capability for generative AI, transformers, or LLM-scale tasks. They are a fundamentally different tool aimed at a different problem space -- edge inference, IoT, wearables, keyword spotting, and interpretable classification.

---

## 1. What Is a Tsetlin Machine?

### Origins

Named after Soviet mathematician Michael Lvovitch Tsetlin (1924-1966), who invented the Tsetlin automaton for solving the multi-armed bandit problem. Ole-Christoffer Granmo published the foundational paper in 2018: "The Tsetlin Machine -- A Game Theoretic Bandit Driven Approach to Optimal Pattern Recognition with Propositional Logic" ([arXiv:1804.01508](https://arxiv.org/abs/1804.01508)). Granmo received the AI Research Paper of the Decade award from the Norwegian AI Consortium (NORA) in 2022.

### Core Mechanism

A Tsetlin Machine learns patterns as **conjunctive clauses in propositional logic** -- essentially AND-rules over binary input features and their negations. Here is how it works:

1. **Binary Input**: All inputs must be Boolean (binary). Continuous data is booleanized via thresholding.

2. **Tsetlin Automata**: The fundamental learning unit. Each automaton is a finite-state machine with a single integer as memory. It decides whether to **include** or **exclude** a specific literal (input feature or its negation) in a clause. States above a threshold mean "include"; below means "exclude." Learning happens through simple increment/decrement operations.

3. **Clauses**: A clause is formed by ANDing a subset of literals together. Each clause is controlled by a team of Tsetlin automata that decide which literals participate. For example: `x1 AND (NOT x3) AND x7`.

4. **Polarity**: Half the clauses have positive polarity (vote FOR a class), half have negative polarity (vote AGAINST). The final classification is determined by summing clause votes and thresholding.

5. **Reinforcement Learning**: Two types of feedback during training:
   - **Type I feedback**: Reinforces frequent, representative patterns (encourages inclusion of relevant features)
   - **Type II feedback**: Increases discrimination power (forces clauses to differentiate between classes)

### Why This Matters for Hardware

The entire inference path requires only:
- **Bitwise AND** (evaluate clauses against input)
- **Bitwise NOT** (negate literals)
- **Integer addition** (sum clause votes)
- **Comparison/threshold** (final classification)

**No floating-point arithmetic. No multiplication. No matrix operations.** This is the fundamental hardware advantage. Every operation maps directly to the simplest digital logic gates.

### Key Variants

| Variant | What It Adds |
|---------|-------------|
| **Convolutional TM (CTM)** | Sliding-window convolution over 2D inputs; clauses act as interpretable logic filters |
| **Coalesced TM (CoTM)** | Multiple TMs share clauses; reduces redundancy |
| **Regression TM** | Continuous output via aggregated clause responses; targets nonlinear regression |
| **Relational TM** | Handles relational/graph-structured data |
| **Graph TM** | Extends to graph-based pattern recognition |
| **Omni TM** | Attempts to scale interpretable embeddings |

---

## 2. Hardware Implementations

### 2.1 The 65nm CoTM ASIC (2025) -- The Flagship Result

**Paper**: "An All-digital 8.6-nJ/Frame 65-nm Tsetlin Machine Image Classification Accelerator" ([arXiv:2501.19347](https://arxiv.org/abs/2501.19347))

This is the most significant TM silicon to date. Key specifications:

| Parameter | Value |
|-----------|-------|
| **Process** | 65nm low-leakage CMOS (UMC) |
| **Core area** | 2.7 mm^2 (3.5 mm^2 die) |
| **Gate count** | 201k cells (including 52k DFFs) |
| **Model storage** | 45,056-bit register file (34,816 for TA actions, 10,240 for clause weights) |
| **Clauses** | 128, fully parallel |
| **Clock frequency** | 27.8 MHz |
| **Classification rate** | 60.3k frames/sec |
| **Single-image latency** | 25.4 us |
| **Power (0.82V)** | 0.52 mW |
| **Power (1.2V)** | 1.15 mW |
| **Energy per classification (0.82V)** | **8.6 nJ** |
| **Energy per classification (1.2V)** | 19.1 nJ |

**Accuracy**:
- MNIST: **97.42%**
- Fashion-MNIST: **84.54%**
- Kuzushiji-MNIST: **82.55%**

**Comparison with other manufactured ASICs**:

| Design | Energy/Classification | Notes |
|--------|----------------------|-------|
| **This TM ASIC (0.82V)** | **8.6 nJ** | Fully digital, 65nm |
| Mixed-signal SNN (2023) | 12.92 nJ | Analog, 0.7V |
| Ternary CNN (2023) | 0.18 uJ | ~21x worse |
| Binary NN SoC (2020) | 43.8 uJ | ~5,000x worse |

**Critical advantage over analog**: Being fully digital, this chip avoids sensitivity to process variation, supply voltage drift, and temperature (PVT) -- issues that plague analog compute-in-memory approaches. It also enables straightforward frequency/voltage scaling.

### 2.2 TsetlinKWS: Keyword Spotting ASIC (2025)

**Paper**: "TsetlinKWS: A 65nm 16.58uW, 0.63mm^2 State-Driven Convolutional Tsetlin Machine-Based Accelerator For Keyword Spotting" ([arXiv:2510.24282](https://arxiv.org/abs/2510.24282))

| Parameter | Value |
|-----------|-------|
| **Process** | 65nm |
| **Core area** | 0.63 mm^2 |
| **Power** | 16.58 uW at 0.7V |
| **Accuracy** | 87.35% (12-keyword spotting) |
| **Operations per inference** | 907k logic ops |

This is a 10x reduction in logic operations compared to state-of-the-art neural-network-based KWS accelerators. The 16.58 uW power consumption is in always-on territory for battery-powered devices.

### 2.3 FPGA Implementations

**Dynamic Tsetlin Machine (DTM) Accelerator** ([arXiv:2504.19797](https://arxiv.org/abs/2504.19797)):
- Platforms: Xilinx Zynq-7020 and Ultrascale+ ZU-7EV
- Supports **on-chip training** (not just inference)
- 2.54x better energy efficiency (GOP/s/W) than comparable DNN FPGA designs
- 6x less power than next-best comparable design
- Runtime reconfigurable: switch datasets/architectures without resynthesis
- Training latency: ~50-60 us for MNIST-like datasets
- IP core power: 0.424 W for small configurations

**Earlier FPGA work** (Xilinx Zynq XC7Z020, 40 MHz):
- 4.4 million classifications per second
- 0.6 uJ per classification
- High power mainly due to FPGA interconnect overhead

**eFPGA accelerator** ([arXiv:2502.07823](https://arxiv.org/html/2502.07823)):
- Targets embedded FPGAs in SoCs
- 129x energy savings vs. low-power microcontroller implementations
- Runtime tunable model size and architecture

### 2.4 Flexible Electronics Implementation (2025)

**Paper**: "A Tsetlin Machine Image Classification Accelerator on a Flexible Substrate" ([arXiv:2510.15519](https://arxiv.org/abs/2510.15519))

Using Pragmatic Semiconductor's 600nm IGZO-based FlexIC technology:

| Version | Accuracy | Gates (NAND2 equiv.) | Area |
|---------|----------|---------------------|------|
| Full | 98.5% | ~6,800 | 8x8 mm^2 |
| Compact | 93% | ~1,420 | 4x4 mm^2 |

This demonstrates that Tsetlin machines are simple enough to run on **flexible plastic substrates** -- something impossible for neural network accelerators. Opens the door to skin-mounted health monitors, smart bandages, and conformable IoT sensors.

### 2.5 Superconducting Tsetlin Machine (Berkeley Lab)

**Source**: [Berkeley Lab IPO](https://ipo.lbl.gov/2024/12/03/superconducting-tsetlin-machines-for-efficient-deep-neural-networks/)

Using Rapid Single-Flux Quantum (RSFQ) superconducting technology:
- Demonstrated on XOR task with 8 clauses
- Estimated dynamic power: <0.5 mW for 8 clauses, 4 automata/clause
- Combines ultra-low power of superconducting circuits with TM interpretability
- Early-stage research; not yet demonstrated on realistic workloads

### 2.6 SoC Design Automation: MATADOR

**Source**: [Literal Labs / Newcastle University](https://www.literal-labs.ai/research/tsetlin-machine-system-on-chip.html)

MATADOR is an automated design tool that:
1. Takes trained TM logic expressions
2. Generates custom compute units per classification task
3. Integrates into SoC architecture
4. Outputs edge-optimized inference accelerators

The bitwise nature of TM inference makes this automation significantly simpler than neural network HLS flows -- the design search space is much smaller.

---

## 3. Performance vs. Neural Networks

### Accuracy Benchmarks

| Dataset/Task | TM Accuracy | NN Comparison | Notes |
|-------------|------------|---------------|-------|
| MNIST digits | 99.51% (CTM) | ~99.7% (CNN) | Within 0.2% of best CNNs; single interpretable layer |
| MNIST (ASIC) | 97.42% | -- | Hardware-constrained (128 clauses) |
| Fashion-MNIST (ASIC) | 84.54% | ~93% (ResNet) | Significant gap on harder variants |
| Iris | Comparable | Comparable | Classic ML benchmark |
| Chinese sentiment | Beats BERT | BERT, ERNIE | On ChnSentiCorp, Weibo-Senti, Douban |
| Fake news detection | Higher F1 | BERT, XLNet | PolitiFact, GossipCop datasets |
| 12-keyword spotting | 87.35% | ~95%+ (DNNs) | Trade-off: 10x fewer operations |
| Recommendation systems | Competitive | Deep NNs | Comparable quality |
| Intrusion detection | Superior | MLP, SVM, RF, kNN | Cybersecurity application |

### Inference Speed

Literal Labs reports benchmarks on standard CPUs and MCUs (not custom hardware):
- **54x faster inference** than neural networks
- **52x less energy** per output
- **+/-2% accuracy variance** vs. neural networks
- Up to **1,000x faster** in optimized configurations

On the 65nm ASIC: **3.3 million inferences per second at 20 mW**.

### The Honest Assessment

**Where TMs win clearly**:
- Small-to-medium classification tasks (MNIST, tabular data, keyword spotting)
- Tasks where interpretability matters (medical, legal, cybersecurity)
- Ultra-low-power edge inference
- Hardware simplicity and area efficiency

**Where TMs struggle or have not been demonstrated**:
- ImageNet-scale image classification (no published results competitive with modern CNNs)
- Generative AI (no TM equivalent of GANs, diffusion models, or autoregressive generation)
- Large language models (no TM equivalent of transformers)
- Complex sequential tasks (limited RNN/LSTM equivalents)
- Any task requiring continuous-valued intermediate representations

**The fundamental limitation**: TMs operate on binary features. Converting continuous data to binary via booleanization loses information. Designing effective feature spaces for complex, high-dimensional data "is notoriously challenging, since the features must be natural building blocks for creating AND-rules that are both interpretable and accurate."

---

## 4. Power Efficiency Analysis -- Are the Claims Real?

### The "10,000x" Claim

Tsetlin.no and various sources claim "up to 10,000x lower energy consumption." This needs context:

**What is being compared**:
- TM inference on a CPU/MCU vs. neural network inference on a GPU
- This is not an apples-to-apples comparison. A GPU is designed for massive parallelism on large models. Comparing a simple TM classifier against a GPU-hosted DNN on a small task will always favor the TM.

**What is credible**:
- The 65nm ASIC achieves 8.6 nJ/classification on MNIST. This genuinely is the lowest reported for a digital ASIC at comparable accuracy.
- The 129x energy savings of eFPGA TM vs. MCU-based inference is a fair comparison for edge scenarios.
- The 2.54x GOP/s/W advantage of TM FPGA over DNN FPGA is a credible, normalized comparison.
- The 54x inference speed advantage on the same CPU hardware is a fair comparison.

**What is not credible**:
- Claiming 10,000x advantage without specifying what the comparison is against
- Comparing a 128-clause TM on MNIST against a transformer with 632 million parameters
- Extrapolating small-task advantages to claim TMs can replace neural networks broadly

### Why the Hardware Efficiency Is Real (at the Circuit Level)

The efficiency advantage is genuine for the tasks TMs handle, and it comes from:

1. **No multiply-accumulate (MAC) operations**: Neural networks require O(n^2) or O(n*m) MACs per layer. A single MAC in 65nm costs ~1 pJ. TMs replace all MACs with bitwise AND operations costing ~1 fJ -- three orders of magnitude less per operation.

2. **No floating-point datapath**: A 32-bit FP multiplier occupies ~10,000 gates. A 32-bit AND gate occupies 32 gates. TMs use the latter exclusively.

3. **No weight memory bottleneck**: Neural networks suffer from the "memory wall" -- moving weights from SRAM/DRAM to compute units dominates energy. TM clause states are single bits, so the entire model fits in registers. The 65nm ASIC stores everything in a 45,056-bit register file.

4. **No activation functions**: Neural networks require nonlinear activation functions (sigmoid, ReLU, softmax) that need lookup tables or approximation circuits. TMs use threshold comparisons (a single comparator).

5. **Deterministic compute**: No stochastic rounding, no batch normalization, no dropout at inference. The compute path is fixed and simple.

---

## 5. Commercial Efforts

### Literal Labs (Newcastle, UK)

- **Founded**: 2023 (trading name of Mignon Technologies Ltd.)
- **Founders**: Professor Alex Yakovlev and Professor Rishad Shafik (Newcastle University)
- **CEO**: Noel Hurley (former Arm executive)
- **Non-executive Director**: Jem Davies (former Arm Fellow)
- **Funding**: GBP 4.6 million raised
- **Product**: Logic-Based Networks (LBN) platform -- early access, training platform for TM models
- **Target**: Edge AI customers who need to replace GPU-intensive algorithms
- **Website**: [literal-labs.ai](https://www.literal-labs.ai/)
- **Key claims**: 50x AI performance improvement, 1000x faster inferencing

### Anzyz Technologies (Grimstad, Norway)

- **Co-founded by**: Ole-Christoffer Granmo
- **Product**: Text analytics platform using Tsetlin machines
- **Application**: Automated invoicing, reimbursement code classification (near-100% accuracy when combined with CCL language algorithm)
- **Website**: [anzyz.com](https://anzyz.com/products/tsetlin/)

### Tsense Intelligent Healthcare (Norway)

- **Co-founded by**: Ole-Christoffer Granmo
- **Focus**: Healthcare AI applications using Tsetlin machines
- **Status**: Limited public information available

### Academic Centers

- **CAIR (Centre for AI Research)**, University of Agder -- Granmo's group, primary TM research
- **Microsystems Group**, Newcastle University -- Hardware implementations (Yakovlev, Shafik)
- **GitHub**: [github.com/cair](https://github.com/cair/TsetlinMachine) -- Open-source TM implementations

### The ISTM Conference Series

The International Symposium on the Tsetlin Machine (ISTM) has been held annually since 2022:
- ISTM 2022: Grimstad, Norway
- ISTM 2023: (IEEE-sponsored)
- ISTM 2024: University of Pittsburgh
- ISTM 2025: Sapienza University of Rome (October 8-10)

---

## 6. What Workloads Are TMs Good/Bad At?

### Good Fit

| Workload | Why |
|----------|-----|
| **Image classification (small)** | MNIST-class: 97-99%+ accuracy, nanojoule energy |
| **Keyword spotting** | Always-on at 16 uW; 10x fewer ops than DNNs |
| **Text classification** | Competitive with BERT on sentiment, spam, fake news |
| **Intrusion detection** | Interpretable rules, beats traditional ML |
| **Medical text categorization** | Interpretable, critical for regulatory compliance |
| **Tabular data classification** | Matches or beats random forests, SVMs |
| **Wearable/IoT sensors** | Runs on flexible substrates, sub-mW power |
| **Anomaly detection** | Binary feature space maps well to threshold-based anomalies |

### Bad Fit

| Workload | Why |
|----------|-----|
| **ImageNet-scale vision** | No competitive results published; booleanization loses too much information |
| **Generative AI** | No generation mechanism; TMs are classifiers/regressors |
| **Large language models** | No attention mechanism, no sequence-to-sequence capability |
| **Speech synthesis** | Requires continuous-valued output generation |
| **Video understanding** | Temporal modeling is limited |
| **Reinforcement learning (complex)** | Basic bandit problems only; not Atari/robotics-scale |
| **Graph neural networks (large)** | Graph TM exists but early-stage |

### The Niche

Tsetlin machines occupy a specific and valuable niche: **small, interpretable, ultra-low-power classification at the edge**. They are not competing with GPT or Stable Diffusion. They are competing with:
- Small CNNs deployed on microcontrollers
- Random forests and SVMs in embedded systems
- Binary neural networks on FPGAs
- TinyML models on Cortex-M processors

In this niche, TMs have a genuine and significant advantage.

---

## 7. Circuit-Level Analysis: Why TMs Could Be More Efficient Than NNs in Hardware

### Operation Cost Comparison (65nm CMOS estimates)

| Operation | Energy | Used By |
|-----------|--------|---------|
| 8-bit integer MAC | ~0.2 pJ | Binary NNs |
| 32-bit FP MAC | ~4.6 pJ | Standard NNs |
| 32-bit bitwise AND | ~0.01 pJ | Tsetlin machines |
| SRAM read (32-bit) | ~5 pJ | NN weight fetch |
| Register read (1-bit) | ~0.001 pJ | TM clause state |

The TM advantage compounds because:
1. Each "operation" is cheaper (AND vs. MAC)
2. Fewer operations per inference (no deep layer chains)
3. Model storage is cheaper (register bits vs. SRAM words)
4. No data conversion overhead (everything is binary)

### Area Comparison

The 65nm TM ASIC uses 2.7 mm^2 for a complete MNIST classifier. For reference:
- A comparable BNN accelerator in 28nm uses ~4 mm^2
- An analog CIM macro in 65nm uses ~1-2 mm^2 but requires ADCs/DACs adding ~1-3 mm^2
- The TM needs no ADCs, no DACs, no analog calibration circuits

### The Digital Advantage

Unlike analog compute-in-memory approaches that also target low-energy inference:
- **No PVT sensitivity**: Digital logic is robust to process, voltage, temperature variation
- **No calibration needed**: Analog CIM requires periodic recalibration
- **Standard EDA flow**: Uses conventional synthesis, place-and-route, DFT
- **Technology portable**: Can be retargeted to any CMOS node without redesign
- **Deterministic**: Same input always gives same output (no analog noise)

---

## 8. Open Questions and Future Directions

1. **Scaling**: Can TMs handle CIFAR-10 or CIFAR-100 with competitive accuracy? The 84.54% on Fashion-MNIST suggests a gap on harder vision tasks.

2. **Booleanization**: The requirement for binary inputs is the fundamental bottleneck. Better booleanization schemes could expand the applicable domain.

3. **Training efficiency**: On-chip TM training exists (DTM FPGA), but training is slower than inference. Can it be made competitive for continual learning at the edge?

4. **Integration**: Will Literal Labs ship a commercial product? The GBP 4.6M funding is modest; they need to demonstrate real customer traction.

5. **Hybrid architectures**: TM front-end for feature extraction + small NN for final classification could combine advantages.

6. **Superconducting TMs**: Berkeley's RSFQ work is interesting but decades from practical deployment.

7. **Standardization**: No standard TM instruction set, no standard model format, no ecosystem equivalent to ONNX/TFLite.

---

## 9. Verdict

Tsetlin machines are **real, silicon-proven, and genuinely efficient** for the specific task of small-scale classification at the edge. The 8.6 nJ/frame MNIST result is not hype -- it is a manufactured chip with measured results that beats every other fully-digital ASIC on record for that task.

However, TMs are **not a general replacement for neural networks**. They cannot do generation, attention, or any task requiring deep feature hierarchies. The "10,000x more efficient" claims, while directionally true for narrow comparisons, are misleading when stated without context.

**For the analog AI chip landscape**: TMs are interesting because they achieve ultra-low-power inference through **digital simplicity** rather than analog tricks. They represent a third path -- not analog CIM, not conventional digital MAC arrays, but logic-based classification that happens to be extremely hardware-efficient. If your workload fits (classification, keyword spotting, anomaly detection, text classification at the edge), a TM accelerator may genuinely be the most efficient option available.

The biggest risk is market size. The workloads TMs handle well are exactly the workloads that existing TinyML solutions (Cortex-M + quantized NNs) handle "well enough." Literal Labs and Anzyz need to prove that the efficiency advantage translates to products people will actually buy.

---

## Sources

- [Granmo, 2018. "The Tsetlin Machine" (arXiv:1804.01508)](https://arxiv.org/abs/1804.01508)
- [65nm CoTM ASIC (arXiv:2501.19347)](https://arxiv.org/abs/2501.19347)
- [TsetlinKWS Keyword Spotting ASIC (arXiv:2510.24282)](https://arxiv.org/abs/2510.24282)
- [Dynamic TM FPGA Accelerator (arXiv:2504.19797)](https://arxiv.org/abs/2504.19797)
- [eFPGA Edge Inference (arXiv:2502.07823)](https://arxiv.org/html/2502.07823)
- [Flexible Substrate TM (arXiv:2510.15519)](https://arxiv.org/abs/2510.15519)
- [Superconducting TM -- Berkeley Lab](https://ipo.lbl.gov/2024/12/03/superconducting-tsetlin-machines-for-efficient-deep-neural-networks/)
- [Super-Tsetlin IEEE Paper](https://ieeexplore.ieee.org/document/10480350/)
- [Literal Labs](https://www.literal-labs.ai/)
- [Literal Labs -- Tsetlin Machines Explained](https://www.literal-labs.ai/tsetlin-machines/)
- [Literal Labs -- Energy Efficiency](https://www.literal-labs.ai/press/tsetlin-machine-energy-consumption.html)
- [Literal Labs -- SoC Automation (MATADOR)](https://www.literal-labs.ai/research/tsetlin-machine-system-on-chip.html)
- [Literal Labs -- Keyword Spotting](https://www.literal-labs.ai/research/low-power-keyword-spotting.html)
- [Literal Labs -- GBP 4.6M Funding](https://www.literal-labs.ai/press/literal-labs-arm-team.html)
- [Anzyz Technologies -- Tsetlin Product](https://anzyz.com/products/tsetlin/)
- [Tsetlin.no -- Sustainable AI](https://tsetlin.no/)
- [Wikipedia -- Tsetlin Machine](https://en.wikipedia.org/wiki/Tsetlin_machine)
- [Wikipedia -- Ole-Christoffer Granmo](https://en.wikipedia.org/wiki/Ole-Christoffer_Granmo)
- [CAIR GitHub -- TsetlinMachine](https://github.com/cair/TsetlinMachine)
- [ScienceNorway -- Can a Norwegian invention revolutionise AI?](https://www.sciencenorway.no/artificial-intelligence/can-a-norwegian-invention-revolutionise-artificial-intelligence/2318511)
- [Unite.AI -- Tsetlin Machine Energy Consumption](https://www.unite.ai/a-game-changer-for-ai-the-tsetlin-machines-role-in-reducing-energy-consumption/)
- [ISTM 2025 Conference](https://istm.no/)
- [ConvTextTM NLP Paper (ACL Anthology)](https://aclanthology.org/2022.lrec-1.401/)
- [Tsetlin Machine Chinese Sentiment Analysis (MDPI)](https://www.mdpi.com/1999-4893/16/2/93)
- [Intrusion Detection with TM (IEEE)](https://ieeexplore.ieee.org/document/9308206/)
- [360-Degree Review of Tsetlin Machines (TechRxiv)](https://www.techrxiv.org/users/925454/articles/1297260-a-360-degree-review-of-tsetlin-machines-concepts-applications-analysis-and-the-future)
- [Fast TM Inference on CPUs (arXiv:2510.15653)](https://arxiv.org/abs/2510.15653)
