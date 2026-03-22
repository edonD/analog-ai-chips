# Can Analog CIM Run LLMs? The Frontier Question

*Last updated: 2026-03-22*

This is the most important question in the analog AI field: can compute-in-memory hardware, designed around tiny crossbar arrays doing matrix-vector multiplies in physics, handle the enormous scale and architectural complexity of large language models? The honest answer is nuanced, rapidly evolving, and mostly unfavorable -- but not hopeless.

---

## Table of Contents

1. [The Scale Problem: Millions vs. Billions](#1-the-scale-problem)
2. [Weight Tiling: How You Spread an LLM Across Analog Arrays](#2-weight-tiling)
3. [The Attention Mechanism Challenge](#3-the-attention-mechanism)
4. [KV Cache on Analog Hardware](#4-kv-cache-on-analog-hardware)
5. [The Precision Question: Can Analog's 4-6 Bits Run LLMs?](#5-the-precision-question)
6. [IBM's Analog Foundation Models: The State of the Art](#6-ibm-analog-foundation-models)
7. [IBM ALBERT on HERMES: First Transformer on Analog Silicon](#7-ibm-albert-on-hermes)
8. [IBM 3D Analog MoE: The Scaling Architecture](#8-ibm-3d-analog-moe)
9. [Analog Attention in Hardware: The Jülich Gain-Cell Breakthrough](#9-julich-gain-cell-attention)
10. [Mythic's LLM Claims: 750x Better Than GPUs?](#10-mythic-llm-claims)
11. [Multi-Chip Scaling: Chiplet Architectures for Analog LLMs](#11-multi-chip-scaling)
12. [The Operations Analog Cannot Do](#12-operations-analog-cannot-do)
13. [Prefill vs. Decode: Where Analog Fits in LLM Inference](#13-prefill-vs-decode)
14. [Digital LLM Quantization Context: What Precision Do LLMs Actually Need?](#14-digital-quantization-context)
15. [The Honest Assessment: Will Analog Ever Run LLMs Competitively?](#15-honest-assessment)
16. [Sources](#16-sources)

---

## 1. The Scale Problem: Millions vs. Billions {#1-the-scale-problem}

This is the single biggest obstacle. The numbers are unforgiving.

### What analog CIM chips hold today

| Chip | Weight Capacity | Technology | Status |
|------|----------------|------------|--------|
| IBM HERMES (64-core) | ~4M weights (16M PCM devices, 4 per weight) | PCM, 14nm | Research silicon |
| IBM HERMES (5-chip system) | ~45M weights (140M PCM devices) | PCM, 14nm | Research demo |
| Mythic M1076 | 80M weights | Flash, 40nm | Shipping (Gen 1) |
| Mythic M1108 | ~108M weights (estimated) | Flash, 40nm | Sampling |
| EnCharge EN100 | Undisclosed on-chip SRAM capacity + 32GB LPDDR5 | Capacitor/SRAM, 16nm | Early access |

### What LLMs require

| Model | Parameters | Weight Storage (INT4) | Weight Storage (INT8) |
|-------|-----------|----------------------|----------------------|
| Llama-3.2-1B | 1.2B | ~600 MB | ~1.2 GB |
| Phi-3-mini | 3.8B | ~1.9 GB | ~3.8 GB |
| Llama-3-8B | 8B | ~4 GB | ~8 GB |
| Llama-3-70B | 70B | ~35 GB | ~70 GB |
| GPT-4 (rumored MoE) | ~1.8T | ~900 GB | ~1.8 TB |

**The gap**: IBM's best analog chip holds 4M weights. A 1B-parameter LLM needs 1,000M weights. That is a **250x gap** to the smallest useful LLM. For a 70B model, the gap is **17,500x**. For frontier models, it is over **400,000x**.

This is not a minor engineering challenge. It is a fundamental mismatch between the technology's current capacity and the workload's requirements.

### Why analog arrays are small

Analog crossbar arrays are typically 256x256 or 512x512 because:

- **IR drop**: As array size increases, voltage drops along resistive wires cause position-dependent errors. A 1024x1024 array has substantially worse accuracy at its corners than its center.
- **Parasitic capacitance**: Larger arrays have more wire capacitance, slowing computation and increasing power.
- **ADC precision**: Larger arrays sum more analog currents, requiring higher-precision (and exponentially more expensive) ADCs to distinguish the result.
- **Noise floor**: More cells contributing current means the signal-to-noise ratio degrades with array size.

These are physics constraints, not engineering laziness. The maximum practical array size has been roughly stable at 256x256 to 512x512 for a decade.

---

## 2. Weight Tiling: How You Spread an LLM Across Analog Arrays {#2-weight-tiling}

Since a single array cannot hold an entire layer (let alone an entire model), weight matrices must be **tiled** -- split into chunks that map onto individual arrays, with results combined digitally.

### Spatial tiling (across arrays on one chip)

A weight matrix of size MxN is partitioned into sub-matrices of size rxc (where r and c match the array dimensions, typically 256x256). Each sub-matrix maps to one crossbar array. For a single layer:

- A 4096x4096 weight matrix (common in LLMs) requires (4096/256) x (4096/256) = **256 tiles**
- Each tile performs its partial MVM independently
- Partial results are accumulated digitally with high-precision adders

This works and is well-understood. IBM's HERMES chip already uses a Network-on-Chip (NoC) to route partial results between its 64 tiles. The overhead is:
- Digital accumulation energy (typically small)
- NoC routing latency and power
- Synchronization between tiles

### Temporal tiling (reloading arrays over time)

When the on-chip arrays cannot hold all weights simultaneously, weights must be swapped in and out from external memory (DRAM). This is the more painful form of tiling:

- **For NVM-based CIM (PCM, RRAM, Flash)**: Reprogramming is slow (microseconds to milliseconds per cell). Temporal tiling is effectively impossible at inference speed. The entire model must fit on-chip or across a multi-chip system.
- **For SRAM-based CIM (EnCharge)**: SRAM rewrites in nanoseconds, making temporal tiling feasible. But every reload costs DRAM access energy (~10-50 pJ/bit), which partially or fully negates the analog compute savings.

### The math on weight reloading

For a 1B-parameter model at INT8 on an SRAM-based CIM chip:
- Total weights: 1 GB
- Assume 10 MB on-chip SRAM compute capacity
- Requires ~100 reload cycles per full inference pass
- At LPDDR5 bandwidth of 50 GB/s: ~20 ms just for weight loading
- At LPDDR5 energy of ~10 pJ/bit: ~80 mJ just for weight movement

This weight-movement energy can exceed the energy saved by doing the MAC in analog. The advantage of analog CIM -- eliminating data movement -- is ironically undermined by the very data movement needed to reload the arrays.

**Key insight from Nature Electronics (2025)**: A comprehensive survey of AIMC tile design confirms that "larger weight matrices must be split into smaller chunks and mapped onto different tiles" with "partial results aggregated using higher-precision digital circuitry." The tiling overhead is an intrinsic architectural cost, not a bug to be fixed.

---

## 3. The Attention Mechanism Challenge {#3-the-attention-mechanism}

Attention is the operation that makes transformers work -- and it is fundamentally different from the dense weight-times-activation matrix multiplies that analog CIM excels at.

### What attention requires

For each token in a sequence of length L, with embedding dimension d and h attention heads:

1. **QKV projection**: Multiply activations by weight matrices to produce Q, K, V vectors. This is a standard matrix-vector multiply -- analog CIM can do this.

2. **Attention score computation**: Q * K^T -- a matrix multiply between two **activation** tensors (not weight times activation). The K matrix changes with every new token. This is **not** a static weight multiply.

3. **Softmax**: exp(x_i) / sum(exp(x_j)) -- a non-linear function involving exponentials and division. **Analog cannot do this**. Must be digital.

4. **Score-weighted value aggregation**: Attention_scores * V -- another dynamic matrix multiply with changing operands.

5. **Layer normalization**: Mean, variance, normalization -- **digital only**.

6. **Output projection**: Another weight-times-activation multiply -- analog can do this.

### The hybrid reality

Of the six operations above, analog CIM can directly accelerate only three (the weight projections and possibly the QK^T and score*V multiplies if the arrays can be dynamically loaded). Softmax, layer norm, residual connections, and position encoding must all be digital.

In a typical transformer layer, the weight-projection MVM operations account for roughly 60-70% of the FLOPs but only 20-30% of the latency in modern GPU implementations (because GPUs are compute-bound on attention but memory-bound on weight loading). Analog CIM's advantage is strongest where digital is weakest: weight loading. But attention's dynamic matrix multiplies are neither.

### Hardware accelerator approaches

Recent work (2025) has developed dedicated hardware for the non-linear operations:
- **Softmax approximation**: Piecewise linear approximation of the exponential, using lookup tables and Newton-Raphson iteration for the normalization. Achievable in compact digital circuits.
- **Layer normalization**: Approximated via mean/variance computation in fixed-point digital logic.
- **HCiM (ADC-Less Hybrid CIM)**: Combines analog CIM arrays with digital processing units, routing results between analog MAC and digital non-linear units. Demonstrated at ASP-DAC 2025.

The consensus architecture is a **hybrid analog-digital pipeline**: analog arrays handle the heavy weight-projection MVMs, digital units handle attention scoring, softmax, layer norm, and all control flow. This is how IBM's HERMES chip already works (8 Global Digital Processing Units alongside 64 analog cores).

---

## 4. KV Cache on Analog Hardware {#4-kv-cache-on-analog-hardware}

The KV cache is the mechanism that makes autoregressive LLM generation efficient. Instead of recomputing all previous tokens' key and value vectors at each step, you store them and only compute the new token's Q, K, V.

### The problem for analog

The KV cache has properties that are hostile to traditional analog CIM:

1. **Dynamic content**: New K and V entries are appended with every generated token. NVM-based CIM (PCM, Flash, RRAM) writes too slowly for this -- programming a PCM cell takes microseconds, but token generation needs to happen in milliseconds.

2. **Sequence-length dependent size**: For a 7B model with 4096 context length, 32 heads, and 128 dim/head, the KV cache at FP16 is ~2 GB. This grows linearly with sequence length.

3. **Random access pattern**: Attention needs to read all previous K/V entries for each new token. This is a read-intensive, random-access workload -- very different from the structured, static-weight MVM that analog CIM is designed for.

4. **KV cache dominates decode-phase energy**: On GPUs, 70-80% of LLM inference energy during decode is spent on KV cache data transfers, not weight loading. This is the exact bottleneck CIM should solve -- but only if the KV cache can be stored in the compute arrays.

### The Jülich gain-cell solution (see Section 9)

The most significant breakthrough here is the 2025 Nature Computational Science paper from Forschungszentrum Jülich and RWTH Aachen, which proposed storing the KV cache **directly in analog gain-cell crossbar arrays**. Gain cells use a capacitor + transistor structure that:
- Writes in nanoseconds (fast enough for token-by-token updates)
- Retains data for milliseconds-to-seconds (long enough for inference)
- Enables non-destructive parallel read (enabling analog dot-product computation)
- Uses oxide semiconductor FETs (IGZO/ITO) that can be fabricated in BEOL

This is the first credible proposal for an analog KV cache. But it is simulation only -- no silicon demonstration yet.

### SRAM-based CIM for KV cache

EnCharge-style SRAM/capacitor CIM could theoretically store KV cache entries, since SRAM writes are fast (nanoseconds). The challenge is capacity: the KV cache for even moderate-length sequences exceeds realistic on-chip SRAM budgets. Tiling the KV cache from DRAM defeats the purpose.

### The honest answer

As of early 2026, **no analog hardware has demonstrated KV cache storage and computation in silicon**. The Jülich gain-cell proposal is the most promising path, but it remains theoretical. In all current and near-term analog LLM architectures, the KV cache must be managed digitally (in SRAM or DRAM), with only the weight-projection MVMs offloaded to analog.

---

## 5. The Precision Question: Can Analog's 4-6 Bits Run LLMs? {#5-the-precision-question}

This is where analog CIM's case for LLMs gets complicated. LLMs are both more and less precision-sensitive than you might expect.

### What digital quantization tells us

The digital quantization community has established clear accuracy boundaries:

| Precision | Typical LLM Accuracy Impact | Notes |
|-----------|---------------------------|-------|
| FP16/BF16 | Baseline (0% loss) | Standard training/inference precision |
| FP8 (W8A8) | ~0% loss | Essentially lossless; NVIDIA Blackwell native |
| INT8 (W8A8) | 0.04-1% loss | Excellent with proper calibration |
| INT4 weights, FP16 activations (W4A16) | 1-2% loss | Good; widely deployed (GPTQ, AWQ) |
| INT4 weights, INT8 activations (W4A8) | 2-4% loss | Competitive; IBM's AFM target |
| INT4 weights and activations (W4A4) | 3-8% loss | Challenging; needs careful QAT |
| INT2 / binary | 10-30% loss | Catastrophic for most tasks without specialized training |

**The key finding**: LLMs can run well at INT4 weights with INT8 activations. This is the precision regime that analog CIM might be able to match.

### But analog 4-bit is not digital INT4

As documented in detail in [research/precision-noise-challenges.md](precision-noise-challenges.md), analog precision has fundamentally different characteristics:

- **Digital INT4**: Deterministic, uniform quantization. Every inference with the same input produces the same output. Errors are bounded and predictable.
- **Analog ~4-bit effective**: Stochastic, non-uniform noise. Each inference produces slightly different results. Errors vary with temperature, device age, position in array, and random noise. The distribution of errors is Gaussian-like, not uniform.

For LLMs, this matters because:
- **Reasoning tasks** are sensitive to precise token probabilities. A small perturbation in logits can change which token is selected, cascading through the entire generation.
- **Long sequences** accumulate errors. Each layer's output is the next layer's input. With 32-80 layers in modern LLMs, stochastic noise compounds.
- **Attention patterns** are sensitive to the relative magnitudes of QK^T scores. Small noise can redirect attention to wrong tokens.

### IBM's measured results

The Analog Foundation Models paper (NeurIPS 2025) provides the most rigorous data:

- **Phi-3-mini-4k-instruct** (3.8B params) adapted for AIMC: retains accuracy comparable to W4A8 digital baselines on reasoning benchmarks. Outperforms QAT and SpinQuant by up to 11.35%.
- **Llama-3.2-1B-Instruct** adapted for AIMC: similarly competitive with W4A8 baselines. Outperforms alternatives by up to 9.72%.

**Critical caveat**: These results are from **simulation** using IBM's calibrated PCM noise models in aihwkit, not from running the LLMs on actual HERMES chips. The simulations are realistic (calibrated on millions of real device measurements), but simulation-to-silicon gaps always exist.

### The precision verdict for LLMs

Analog CIM at 4-6 effective bits can likely run LLMs at quality comparable to INT4 digital quantization -- **if** the model is specifically trained with hardware-aware noise injection. Off-the-shelf quantized models will catastrophically fail on analog hardware. This hardware-software coupling is a significant deployment burden.

---

## 6. IBM's Analog Foundation Models: The State of the Art {#6-ibm-analog-foundation-models}

The "Analog Foundation Models" (AFM) work from IBM Research and ETH Zurich, presented at NeurIPS 2025, represents the most systematic effort to make LLMs work on analog hardware.

### The problem they solved

Standard LLMs catastrophically fail when deployed on AIMC hardware. Even models carefully quantized to INT4 using state-of-the-art methods (GPTQ, AWQ, SpinQuant) cannot handle analog noise because:
- Digital quantization assumes deterministic rounding; analog adds stochastic noise
- Weight distributions in standard models are not optimized for the limited dynamic range of PCM/RRAM devices
- Input/output quantization ranges are misaligned with hardware ADC/DAC characteristics

### The three-step pipeline

1. **Noise injection during training**: Simulate AIMC noise (device variability, read noise, programming errors) during the forward pass of fine-tuning. The model learns to place weights in noise-robust configurations.

2. **Iterative weight clipping**: Constrain weight distributions to fit within the dynamic range of the target NVM device (e.g., PCM conductance window). Standard LLMs have occasional large-magnitude weights that would saturate analog devices.

3. **Learned static quantization ranges**: Rather than using fixed quantization ranges, learn per-layer input and output ranges that minimize quantization error given the hardware constraints.

Additionally, the AFM pipeline uses **distillation from pre-trained LLMs** with 20 billion tokens of synthetic data, avoiding the need to train from scratch.

### Results

| Model | Method | MMLU-Pro | GSM8K | TruthfulQA | ARC-C |
|-------|--------|---------|-------|------------|-------|
| Phi-3-mini | FP16 baseline | Reference | Reference | Reference | Reference |
| Phi-3-mini | SpinQuant W4A8 | Competitive | Competitive | Competitive | Competitive |
| Phi-3-mini | LLM-QAT W4A8 | Lower | Lower | Lower | Lower |
| Phi-3-mini | **AFM (analog)** | **Best among quantized** | **Best among quantized** | Competitive | **Best among quantized** |

The AFM models outperform both post-training quantization and quantization-aware training on the hardest tasks (reasoning, factual accuracy). The margin is significant: up to 11.35% better than LLM-QAT on Phi-3-mini.

### Why AFMs are significant

1. **First demonstration** that billion-parameter LLMs can match W4A8 digital quality under analog noise conditions
2. **Scales better** than quantized models as test-time compute increases -- suggesting AIMC is well-suited for inference-time scaling (a growing trend)
3. **Cross-platform benefit**: AFMs also perform better on low-precision digital hardware, since noise robustness helps with simple round-to-nearest quantization
4. **Open methodology**: Pipeline uses IBM's open-source aihwkit

### What it does not prove

- No silicon validation. All results are simulated.
- Tested only on 1B and 3.8B models. Scaling to 7B+ is undemonstrated.
- The training pipeline requires knowledge of the target hardware's noise characteristics. Changing hardware means retraining.
- The energy and latency benefits are projected, not measured.

---

## 7. IBM ALBERT on HERMES: First Transformer on Analog Silicon {#7-ibm-albert-on-hermes}

Published in Nature Communications (2025), this is the **first demonstration of a transformer architecture running on analog in-memory computing silicon** -- a genuine milestone.

### What they did

- Mapped **ALBERT** (A Lite BERT) onto the IBM HERMES 64-core analog chip
- ALBERT uses **weight sharing** across all 12 transformer layers -- the same set of weights is reused 12 times. This is critical because it means the model's unique weights (~7.1M) fit within HERMES's capacity.
- Programmed 7.1M unique analog weights into the conductance of 28.3M PCM devices (4 devices per weight, differential configuration)
- Ran inference on the **General Language Understanding Evaluation (GLUE)** benchmark -- 7 tasks covering sentiment analysis, textual entailment, paraphrase detection, etc.

### Results

- Average hardware accuracy across 7 GLUE tasks: **only 1.8% below floating-point reference**
- This is despite weight-programming errors, PCM drift, readout noise, and error propagation through 12 layers
- Also demonstrated on the **Long Range Arena** benchmark: within **2% accuracy** of floating-point operations

### Why ALBERT and not GPT?

The choice of ALBERT was driven by practical constraints:
- ALBERT's weight sharing means 7.1M unique weights (fits on HERMES)
- GPT-2-small has 124M unique weights (30x too large for HERMES)
- ALBERT is bidirectional (BERT-style), not autoregressive, so no KV cache management needed
- ALBERT is still a real transformer with real self-attention -- it validates the core compute patterns

### Significance

This proves three things:
1. Analog CIM can execute transformer attention patterns (QKV projections, multi-head computation) at near-software accuracy
2. Error propagation through multiple transformer layers does not cause catastrophic degradation (1.8% loss across 12 layers is acceptable)
3. The hybrid analog-digital pipeline works: analog arrays do MVMs, digital units do softmax/LayerNorm/attention scoring

### What it does not prove

- ALBERT is 7.1M parameters. LLMs are 1B-1T parameters. The scale gap remains.
- ALBERT uses weight sharing (same weights reused). LLMs have distinct weights per layer.
- Bidirectional models do not need autoregressive KV cache management.
- The chip runs one model at a time with no multi-tenancy or batching.

---

## 8. IBM 3D Analog MoE: The Scaling Architecture {#8-ibm-3d-analog-moe}

Published in Nature Computational Science (January 2025), this paper proposes the most credible architecture for scaling analog CIM to LLM-class parameter counts.

### The core idea

Mixture-of-Experts (MoE) models activate only a subset of "expert" sub-networks per token (typically 2 of 8, or 2 of 16). This conditional computation means:
- Total parameters can be very large (hundreds of billions) while active parameters per token remain modest
- Each expert is a relatively small feedforward network

IBM's insight: **map each expert to a separate physical layer in a 3D-stacked NVM stack**. Since only a few experts are active per token, only those physical layers need to be read. This creates a natural alignment between MoE's computational sparsity and 3D memory's layer-selective access.

### Simulated results

Using their 3D-CiM-LLM-Inference-Simulator (open-sourced on GitHub), IBM compared their architecture against GPUs:

- **Higher throughput** than commercial GPUs for equivalent MoE models
- **Significantly higher energy efficiency** -- the advantage is largest for energy because GPUs waste enormous energy on weight fetching from HBM, which is eliminated by CIM
- **Better scaling** with model size: as models get larger, the ratio of MoE active parameters to total parameters stays constant, keeping the analog arrays efficiently utilized

### Why MoE is the right fit for analog CIM

1. **Small active weight set**: A 100B total parameter MoE model with 8 experts and top-2 routing has ~25B active parameters per token -- much more manageable than a dense 100B model
2. **Static expert weights**: Expert weights do not change during inference (unlike KV cache). They can be programmed once into NVM and used for millions of inferences.
3. **Natural partitioning**: Each expert maps cleanly to a hardware partition (3D layer, chiplet, or tile group), avoiding complex weight-tiling strategies
4. **Sparsity = power savings**: Inactive experts (inactive layers) can be power-gated

### The catch

This is **simulation only**. No 3D-stacked analog CIM chip exists. Key unresolved challenges:
- 3D NVM stacking introduces thermal issues (upper layers heat lower layers)
- Inter-layer routing bandwidth for partial sums
- Router logic (which experts to activate) must be digital and fast
- Manufacturing cost of multi-layer NVM stacks is unknown
- The simulation uses ideal analog noise models; real 3D-stacked devices may have worse variability

---

## 9. Analog Attention in Hardware: The Jülich Gain-Cell Breakthrough {#9-julich-gain-cell-attention}

Published in Nature Computational Science (September 2025) by researchers at Forschungszentrum Jülich and RWTH Aachen, this is arguably the most creative analog-for-LLM paper to date.

### The problem they addressed

The attention mechanism's KV cache is the primary bottleneck for LLM decode -- not the weight MVMs. On an A100 GPU, loading KV cache data accounts for 70-80% of decode-phase energy. Previous analog CIM work focused on weight MVMs and ignored this.

### The solution: gain-cell crossbar arrays as analog KV cache

**Gain cells** are capacitor-based memory elements using oxide semiconductor transistors (IGZO or ITO). Unlike SRAM (6 transistors) or DRAM (1 transistor + 1 capacitor), a gain cell uses 2 transistors + 1 capacitor, offering:
- **Fast write**: Nanosecond-scale (fast enough to store new K/V projections each token)
- **Non-destructive read**: Can be read in parallel without losing stored data
- **Multi-level storage**: Capacitor voltage is inherently analog -- can store multi-bit values
- **BEOL-compatible**: Oxide semiconductor FETs can be fabricated in the metal layers above CMOS logic
- **Retention**: Milliseconds to seconds (sufficient for inference-time KV cache)

### Architecture

The proposed architecture:
1. Stores **K and V projection matrices** directly in gain-cell crossbar arrays
2. New tokens' K and V entries are **written into the arrays** as they are generated
3. For each new query Q, the **dot product Q*K^T is computed in the analog domain** by applying Q as voltages and reading the summed currents
4. Softmax is computed digitally
5. The **attention-weighted sum over V** is similarly computed in analog

For arrays larger than a single crossbar can hold, **sub-tiling** stacks multiple 64x64 gain-cell arrays, each storing a portion of the KV cache.

### Hardware-aware model initialization

Pre-trained GPT-2 models cannot be directly mapped because gain-cell non-idealities (charge leakage, read noise, capacitor mismatch) corrupt the computations. The researchers designed an initialization algorithm that achieves **text-processing performance comparable to GPT-2** without training from scratch.

### Results (simulated)

For a single attention head in GPT-2:
- **Latency**: 65 ns per token
- **Energy**: 6.1 nJ per token
- **Speedup vs. A100 GPU**: up to **7,000x** per attention head
- **Energy reduction vs. A100 GPU**: up to **90,000x** per attention head

For a 1.5B-parameter model:
- Up to **100x speed-up** and **70,000x energy reduction** vs. GPUs

### The catches (and they are significant)

1. **These are per-head, per-operation numbers.** A full LLM has 32-128 attention heads, 32-80 layers, plus all the non-attention operations. The system-level advantage will be orders of magnitude smaller.

2. **No silicon.** These are circuit-level simulations, not chip measurements. The gain-cell arrays have been fabricated in other contexts but not in this attention-specific configuration.

3. **Gain cells are a nascent technology.** IGZO/ITO transistors are used in display drivers but not yet in high-performance computing chips. Manufacturing variability, yield, and reliability at scale are unknown.

4. **Retention time.** Gain cells retain data for milliseconds-to-seconds. For short sequences, this is fine. For long-context LLMs (100K+ tokens), the early KV cache entries may decay before they are needed. Periodic refresh would be required, adding overhead.

5. **The comparison baseline.** Comparing a single analog operation to a full GPU system (including memory hierarchy, OS overhead, framework overhead) inflates the advantage. A fair comparison would be against a custom digital ASIC optimized for the same operation.

### Why it matters despite the caveats

This is the first paper to seriously address the **decode-phase bottleneck** with analog hardware. Previous work focused on weight projections (which GPUs handle reasonably well). By targeting the KV cache -- the actual bottleneck -- this work points toward where analog could make the biggest difference.

---

## 10. Mythic's LLM Claims: 750x Better Than GPUs? {#10-mythic-llm-claims}

Mythic's December 2025 press release made the most aggressive LLM-on-analog claims in the field. They deserve careful dissection.

### The claims

| Claim | Number | Basis |
|-------|--------|-------|
| LLM throughput efficiency | 750x more tokens/s/W | "vs NVIDIA's highest-end GPUs for 1T parameter LLMs" |
| Cost per token | 80x lower | "$0.005/M tokens for 100B LLMs" |
| Scaling | Up to 1,024 chiplets | "Data center LLM inference" |
| Energy efficiency | 120 TOPS/W per chiplet | Gen 2 architecture |

### The problems

**Problem 1: No silicon.** Mythic's Gen 2 chiplet (the one these claims are based on) has not been independently demonstrated. Gen 1 delivered ~8 TOPS/W at system level -- good, but 15x lower than the Gen 2 claim.

**Problem 2: "Internal benchmarks."** No methodology disclosed. No model specified. No batch size, precision, or comparison methodology. No MLPerf submission after 14 years. The 750x number should be treated as a marketing figure until independently validated.

**Problem 3: The 1T parameter scaling question.** A trillion-parameter model at INT8 requires ~1 TB of weight storage. Even at 1,024 chiplets, each chiplet would need to hold ~1 GB of weights. At 80M weights per Gen 1 chip, that requires ~12x more capacity per chiplet. The Gen 2 chiplet's weight capacity has not been disclosed.

**Problem 4: Inter-chiplet communication.** LLM inference requires high-bandwidth communication between chips for:
- Tensor parallelism (splitting layers across chips)
- Pipeline parallelism (splitting layers sequentially across chips)
- Attention score aggregation
- KV cache sharing

NVIDIA uses NVLink (900 GB/s on Blackwell). Mythic has not disclosed its inter-chiplet interconnect technology, bandwidth, or latency. This is not a minor detail -- communication overhead typically dominates multi-chip LLM inference performance.

**Problem 5: The KV cache.** Flash memory (Mythic's technology) cannot be rewritten fast enough to serve as KV cache. Each chiplet would need substantial SRAM for KV cache storage, which is not part of the disclosed architecture.

**Problem 6: Attention and non-linear operations.** Mythic's per-tile digital SIMD engines and RISC-V processors must handle softmax, layer norm, and attention scoring. The efficiency of these digital components at LLM scale is unknown.

### Credibility assessment

Mythic's Gen 1 silicon proved the core technology works for vision CNNs at ~8 TOPS/W. The LLM claims for Gen 2 represent a leap from proven (CNNs on real chips) to projected (LLMs on unbuilt chiplets). The 750x number specifically lacks any supporting evidence. Even if Mythic's analog MAC efficiency is as claimed, the system-level LLM performance depends on dozens of factors (interconnect, KV cache, attention, softmax, batching, scheduling) that Mythic has not addressed publicly.

**Verdict**: The claims are aspirational marketing from a company that needs to justify $125M in new funding. Wait for independent benchmarks.

---

## 11. Multi-Chip Scaling: Chiplet Architectures for Analog LLMs {#11-multi-chip-scaling}

Several research groups have proposed chiplet-based architectures to bridge the capacity gap between small analog arrays and large LLMs.

### 3D-CIMlet (Purdue, DAC 2025)

A co-design framework for heterogeneous CIM chiplets targeting edge LLM inference:
- Combines **RRAM chiplets** (40nm, non-volatile, for static weights) with **capacitor-less eDRAM chiplets** (14/16nm FinFET, for dynamic data)
- Supports both 2.5D (side-by-side on interposer) and 3D (vertically stacked) configurations
- **Results**: 2.5D designs achieve 9.3x energy efficiency improvement over 2D baselines; 3D designs achieve 12x improvement with 92.5% energy-delay product reduction
- Includes thermal-aware optimization (critical for 3D stacks)
- Targets edge LLMs (1-3B parameters) plus continual learning

### PICNIC (NUS, 2025)

Silicon Photonic Interconnected Chiplets with In-memory Computing:
- Uses **3D-stacked chiplets** with RRAM-based CIM processing elements
- **Silicon photonic interconnect** between chiplets (solving the communication bottleneck)
- Inter-PE Computational Network (IPCN) performs dataflow control and dynamic matrix multiplies
- Chiplet Clustering with Power Gating (CCPG) enables scaling to large models
- **Results**: 57x efficiency improvement over NVIDIA H100 at similar throughput (after CCPG)

### CHIME (2025)

Chiplet-based Heterogeneous Near-Memory Acceleration for Edge Multimodal LLM Inference:
- Targets multimodal LLMs (vision + language)
- Heterogeneous chiplets for different modalities and operations
- Near-memory (not in-memory) computation

### The common pattern

All three architectures share key features:
1. **Heterogeneous chiplets**: Different chiplet types for different operations (weight MVMs, attention, non-linear functions, KV cache)
2. **High-bandwidth interconnect**: UCIe, silicon photonics, or 3D TSVs to move data between chiplets
3. **Hybrid compute**: Analog for dense MVMs, digital for everything else
4. **Targeting edge LLMs first**: 1-3B parameter models, not frontier 100B+ models

### The gap to production

These are all **simulation-based academic proposals**. No multi-chiplet analog LLM system has been fabricated. The challenges include:
- Chiplet-to-chiplet interface standardization
- Yield and test of heterogeneous chiplet stacks
- Thermal management in 3D configurations
- System-level software stack (compilers, schedulers, memory managers)
- Cost of advanced packaging (2.5D/3D)

---

## 12. The Operations Analog Cannot Do {#12-operations-analog-cannot-do}

A transformer-based LLM requires many operations beyond matrix-vector multiplication. Several are fundamentally incompatible with analog computation:

| Operation | Required for | Why Analog Cannot Do It | Must Be |
|-----------|-------------|------------------------|---------|
| **Softmax** | Attention scoring | Requires exponentials and normalization (division) -- no analog equivalent | Digital |
| **Layer normalization** | Every transformer layer | Requires mean, variance, division, square root | Digital |
| **RMSNorm** | Llama-style models | Requires square root and division | Digital |
| **Positional encoding** (RoPE) | Token position awareness | Complex trigonometric functions applied to Q/K | Digital |
| **Token embedding lookup** | Input processing | Table lookup, not matrix multiply | Digital |
| **Sampling / top-k / top-p** | Output token selection | Sorting, probability manipulation | Digital |
| **KV cache management** | Autoregressive generation | Dynamic memory allocation, token-by-token updates | Digital (or gain-cell) |
| **Residual connections** | Skip connections | Element-wise addition of tensors from different stages | Digital (simple, low cost) |
| **GeLU / SiLU activation** | After FFN layers | Non-linear functions; some can be approximated in analog but typically done digitally | Digital |

The fraction of LLM compute that is pure matrix-vector multiplication (what analog CIM does) versus "everything else" depends on the model:
- **For the feedforward blocks**: ~95% is MVM (analog-friendly)
- **For the attention blocks**: ~40-60% is MVM, rest is QK^T, softmax, score*V, LayerNorm
- **Overall for a full transformer layer**: ~60-70% is MVM

This means analog CIM can potentially accelerate **60-70% of transformer compute** while the remaining 30-40% must run on digital hardware. The achievable system speedup is therefore bounded by Amdahl's law: even if analog makes the MVM infinitely fast, the digital 30-40% limits total speedup to ~2-3x unless the digital portions are also optimized.

---

## 13. Prefill vs. Decode: Where Analog Fits in LLM Inference {#13-prefill-vs-decode}

LLM inference has two distinct phases with very different computational characteristics, and analog CIM has different value propositions for each.

### Prefill phase

- **What happens**: All input tokens are processed in parallel to generate the initial KV cache
- **Bottleneck**: Compute-bound (large matrix multiplies with high parallelism)
- **Analog advantage**: Moderate. Weight MVMs are parallelized well, but GPUs also handle prefill efficiently because it is compute-dense. The analog energy advantage exists but is less dramatic.

### Decode phase

- **What happens**: Tokens are generated one at a time, each requiring attention over all previous tokens
- **Bottleneck**: Memory-bound (loading weights and KV cache for each single-token computation)
- **Analog advantage**: Potentially large. This is where CIM's core value proposition (eliminating weight loading from off-chip memory) matters most. Each token requires reading the entire weight matrix but performing only one vector's worth of computation -- exactly the scenario where memory bandwidth dominates and CIM helps.

### The decode-phase opportunity

In digital systems, decode-phase efficiency is dominated by:
1. **Weight loading**: Bringing model weights from HBM to compute units (~70% of energy for weight-only operations)
2. **KV cache access**: Reading and updating the KV cache (~70-80% of energy for attention operations)

Analog CIM eliminates #1 (weights are in the compute arrays). If gain-cell or fast-write CIM can handle #2 (per the Jülich proposal), analog could dramatically accelerate the decode phase.

However, decode is also the phase where **latency per token matters most** (users are waiting for each word). Analog CIM's latency depends on array readout time, ADC conversion, digital post-processing, and inter-tile communication -- not just the analog MAC speed. A single token generation pass through all layers of a 7B model would require thousands of tile-level MVMs, each requiring ADC readout, digital accumulation, and routing.

### Disaggregated prefill/decode

A trend in digital LLM serving is disaggregating prefill (on compute-optimized chips) and decode (on memory-bandwidth-optimized chips). Analog CIM is naturally suited to the **decode role** in such a disaggregated system -- handling the memory-bound single-token generation while digital accelerators handle compute-bound prefill.

---

## 14. Digital LLM Quantization Context: What Precision Do LLMs Actually Need? {#14-digital-quantization-context}

To assess analog CIM's viability, we need to understand the precision floor established by digital quantization research.

### State of the art (2025-2026)

| Method | Weight Bits | Activation Bits | Accuracy vs. FP16 | Notes |
|--------|-----------|----------------|-------------------|-------|
| GPTQ | 4 | 16 | -1 to -2% | Post-training, widely deployed |
| AWQ | 4 | 16 | -0.5 to -1.5% | Activation-aware, better on hard tasks |
| SpinQuant | 4 | 8 | -1 to -3% | Rotation-based quantization |
| LLM-QAT | 4 | 8 | -2 to -4% | Quantization-aware training |
| QuIP# | 2 | 16 | -3 to -5% | Aggressive; random rotation |
| AQLM | 2 | 16 | -2 to -4% | Additive quantization |
| 1-bit (KAIST Slim-Llama) | 1.58 | 8 | -3 to -6% | ISSCC 2025; 3B Llama at 4.69 mW |
| NVIDIA FP4 | 4 (FP) | 4 (FP) | ~-1% | Blackwell native; ~1.32x speedup vs. FP8 |

### What this means for analog CIM

1. **W4A8 is the target.** If analog CIM can match W4A8 quality (4-bit weights, 8-bit activations), it is competitive with the best digital quantization. IBM's AFMs demonstrate this is achievable in simulation.

2. **Sub-4-bit is being explored digitally.** KAIST's 1.58-bit LLM at ISSCC 2025 runs a 3B Llama model at 4.69 mW -- purely digital. The 31-65x energy reduction from algorithmic quantization approaches what analog CIM promises, without any analog hardware.

3. **The moving target problem.** Digital quantization is improving faster than analog hardware. By the time analog CIM chips scale to LLM capacity, digital quantization may have achieved equivalent efficiency gains through algorithmic means on standard digital hardware.

4. **FP4 on Blackwell.** NVIDIA's native FP4 support in Blackwell (2025) delivers ~2x throughput improvement over FP8 with minimal accuracy loss. This continuously raises the bar that analog must clear.

---

## 15. The Honest Assessment: Will Analog Ever Run LLMs Competitively? {#15-honest-assessment}

### What has been proven (in silicon)

1. **Transformers run on analog hardware.** IBM's ALBERT on HERMES (Nature Communications 2025) demonstrated a transformer model at 1.8% accuracy loss on actual analog chips. This is a real milestone.

2. **The hybrid architecture works.** Analog MVMs + digital non-linear operations + digital control is a viable pipeline for transformer inference.

3. **Error propagation is manageable.** 12 transformer layers on analog hardware without catastrophic accuracy loss.

### What has been proven (in simulation)

4. **Billion-parameter LLMs can be adapted for analog noise.** IBM's AFMs match W4A8 digital baselines for Phi-3-mini (3.8B) and Llama-3.2-1B in simulation.

5. **MoE models are a natural fit.** IBM's 3D analog MoE architecture shows favorable scaling in simulation.

6. **Analog attention (KV cache in gain cells) could be transformative.** The Jülich proposal achieves orders-of-magnitude energy reduction in simulation.

7. **Chiplet scaling paths exist.** 3D-CIMlet, PICNIC, and CHIME show 10-60x efficiency gains over GPUs in simulation.

### What remains unproven

8. **No analog chip has run an LLM.** The largest transformer demonstrated on analog silicon is ALBERT at 7.1M parameters. The smallest useful LLM is ~1B parameters. That is a 140x gap.

9. **No multi-chip analog system for LLMs exists.** All chiplet architectures are paper designs.

10. **KV cache on analog is theoretical.** Gain cells for attention are promising but undemonstrated in silicon for this purpose.

11. **System-level efficiency is unknown.** Every claim of 100x or 1000x efficiency is either (a) per-operation, not system-level, (b) simulated, not measured, or (c) comparing against a suboptimal baseline. The measured system-level advantage of analog CIM is 2-14x (IBM HERMES speech: 14x; Mythic Gen 1: ~2x). Whether LLM workloads fall closer to 2x or 14x is unknown.

### The structural challenges

12. **The capacity gap is closing slowly.** Going from 4M to 1B weights requires either much larger chips, multi-chip systems, or 3D stacking -- all of which are years away.

13. **Digital is a moving target.** While analog researchers work on scaling, digital quantization (1-4 bit), digital near-memory architectures (NorthPole, Groq), and custom digital LLM ASICs (SambaNova, Cerebras, Groq) are improving rapidly. NorthPole already demonstrated 72.7x energy efficiency improvement over GPUs for a 3B LLM -- using purely digital near-memory compute.

14. **Software ecosystem gap.** LLM deployment requires compilers, serving frameworks, batching schedulers, KV cache managers, speculative decoding, and continuous batching. None of these exist for analog hardware. NVIDIA has vLLM, TensorRT-LLM, and CUDA. This gap takes years to close.

15. **The analog precision tax.** Every model must be retrained or fine-tuned for the specific analog hardware. You cannot just deploy a HuggingFace model on an analog chip. This is a structural disadvantage that no amount of hardware improvement can eliminate.

### The realistic timeline

| Milestone | Earliest Realistic Date | Confidence |
|-----------|------------------------|------------|
| First LLM (1B+) on analog silicon | 2027-2028 | Medium |
| Multi-chip analog system for 7B+ LLM | 2029-2030 | Low |
| Analog LLM inference competitive with digital at system level | 2030+ | Very low |
| Analog LLM inference commercially deployed | 2031+ | Speculative |

### Where analog CIM can win for LLMs

Despite all the challenges, there are specific scenarios where analog CIM could find a niche:

1. **Edge LLM decode acceleration**: Small models (1-3B) in power-constrained environments (mobile, automotive, IoT). The decode phase is memory-bound and benefits most from CIM. This is where analog's value is highest.

2. **MoE model inference**: The natural alignment between MoE's conditional computation and analog CIM's array architecture could enable efficient scaling. If MoE becomes the dominant LLM architecture (which trends suggest), analog benefits.

3. **Analog attention acceleration**: If gain-cell KV cache technology matures, it could be combined with digital weight-projection accelerators in a heterogeneous system -- analog for attention, digital for weights. This inverts the current assumption and targets the actual bottleneck.

4. **Supplementary acceleration**: Analog CIM chiplets as add-on accelerators for the heaviest MVM operations, while a digital host handles everything else. The M.2/PCIe form factor (EnCharge) supports this model.

### Where analog CIM will likely lose

1. **Data center LLM serving at scale**: The software ecosystem, flexibility, multi-tenancy, continuous batching, and rapid model deployment requirements overwhelmingly favor digital. NVIDIA's moat is software, not hardware.

2. **Frontier model inference (100B+)**: The capacity, interconnect, and precision requirements are beyond any foreseeable analog system.

3. **Training**: Analog CIM for training remains largely theoretical. Backward passes require higher precision than analog can provide.

### The bottom line

Analog CIM for LLMs is in the **"promising research, no product"** phase. IBM has demonstrated that transformers work on analog silicon (ALBERT) and that LLMs can be adapted for analog noise (AFMs). The Jülich gain-cell attention work opens a genuinely new direction. But the gap between a 7M-parameter demonstration and a 1B-parameter product is enormous, and digital alternatives are improving faster than analog is scaling.

The most likely outcome is not "analog replaces GPUs for LLMs" but rather **"analog becomes a specialized accelerator for specific LLM operations (decode-phase MVM, possibly attention) in power-constrained edge devices, deployed alongside digital processors."** This is a smaller market than "replace NVIDIA" but potentially a real and valuable one.

The question is whether analog can reach this niche before digital near-memory architectures (NorthPole, Groq) and extreme quantization (1-4 bit digital) get there first. The race is tighter than analog advocates admit.

---

## 16. Sources {#16-sources}

### Key Papers

- "Demonstration of transformer-based ALBERT model on a 14nm analog AI inference chip," *Nature Communications*, 2025. [Nature](https://www.nature.com/articles/s41467-025-63794-4)
- "Analog in-memory computing attention mechanism for fast and energy-efficient large language models," *Nature Computational Science*, September 2025. [Nature](https://www.nature.com/articles/s43588-025-00854-1) | [arXiv](https://arxiv.org/abs/2409.19315)
- "Analog Foundation Models," IBM Research & ETH Zurich, NeurIPS 2025. [arXiv](https://arxiv.org/abs/2505.09663) | [OpenReview](https://openreview.net/forum?id=zo4zYTR8vn)
- "Efficient scaling of large language models with mixture of experts and 3D analog in-memory computing," *Nature Computational Science*, January 2025. [Nature](https://www.nature.com/articles/s43588-024-00753-x)
- "Analog AI Accelerators for Transformer-based Language Models: Hardware, Workload, and Power Performance," IBM Research, IMW 2025. [IBM](https://research.ibm.com/publications/analog-ai-accelerators-for-transformer-based-language-models-hardware-workload-and-power-performance)
- "The design of analogue in-memory computing tiles," *Nature Electronics*, 2025. [Nature](https://www.nature.com/articles/s41928-025-01537-5)
- "Overcoming computational bottlenecks in large language models through analog in-memory computing," *Nature Computational Science*, 2025. [Nature](https://www.nature.com/articles/s43588-025-00860-3)
- "An analog and digital hybrid attention accelerator for transformers with charge-based in-memory computing," 2024. [arXiv](https://arxiv.org/abs/2409.04940)
- "Memory Is All You Need: An Overview of Compute-in-Memory Architectures for Accelerating Large Language Model Inference," 2024. [arXiv](https://arxiv.org/abs/2406.08413)
- "3D-CIMlet: A Chiplet Co-Design Framework for Heterogeneous In-Memory Acceleration of Edge LLM Inference and Continual Learning," Purdue, DAC 2025. [PDF](https://engineering.purdue.edu/NanoX/assets/pdf/2025_DAC_3D-CIMlet_AAM.pdf)
- "PICNIC: Silicon Photonic Interconnected Chiplets with Computational Network and In-memory Computing for LLM Inference Acceleration," NUS, 2025. [arXiv](https://arxiv.org/abs/2511.04036)
- "CHIME: Chiplet-based Heterogeneous Near-Memory Acceleration for Edge Multimodal LLM Inference," 2025. [arXiv](https://arxiv.org/abs/2601.19908)

### IBM Research

- [Analog in-memory computing could power tomorrow's AI models](https://research.ibm.com/blog/how-can-analog-in-memory-computing-power-transformer-models) -- IBM Research Blog
- [3D-CiM-LLM-Inference-Simulator](https://github.com/IBM/3D-CiM-LLM-Inference-Simulator) -- GitHub
- [IBM aihwkit](https://github.com/IBM/aihwkit) -- GitHub

### Analysis and News

- [LLMs on Analog In-Memory Computing Based Hardware](https://semiengineering.com/llms-on-analog-in-memory-computing-based-hardware-ibm-research-eth-zurich/) -- Semiconductor Engineering
- [Analog IMC Attention Mechanism For Fast And Energy-Efficient LLMs](https://semiengineering.com/analog-imc-attention-mechanism-for-fast-and-energy-efficient-llms-fzj-rwth-aachen/) -- Semiconductor Engineering
- [Silicon Photonic Interconnected Chiplets With In-memory Computing Accelerate LLM Inference](https://quantumzeitgeist.com/computing-efficiency-silicon-photonic-chiplets-memory-accelerate-llm-inference-surpassing/) -- QuantumZeitgeist
- [Four Architectural Opportunities for LLM Inference Hardware (Google)](https://semiengineering.com/four-architectural-opportunities-for-llm-inference-hardware-google/) -- Semiconductor Engineering
- [Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective](https://arxiv.org/abs/2410.04466)
- [On-Device LLMs: State of the Union, 2026](https://v-chandra.github.io/on-device-llms/)
- [Mythic December 2025 Press Release](https://mythic.ai/whats-new/mythic-to-challenge-ais-gpu-pantheon-with-100x-energy-advantage-and-oversubscribed-125m-raise/)
- [Analog in-memory Computing Attention Mechanism -- NextBigFuture](https://www.nextbigfuture.com/2025/09/analog-in-memory-computing-attention-mechanism-for-fast-and-energy-efficient-large-language-models.html)
- [Challenges and Research Directions for Large Language Model Inference Hardware](https://arxiv.org/abs/2601.05047)
- [Analogue in-memory computing coming of age](https://communities.springernature.com/posts/analogue-in-memory-computing-coming-of-age) -- Springer Nature Research Communities
