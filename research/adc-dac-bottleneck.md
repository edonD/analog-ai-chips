# The ADC/DAC Bottleneck: Why Analog AI Chips Underdeliver

**The single most important reason analog compute-in-memory (CIM) chips fail to deliver their theoretical efficiency advantage over digital: the analog-to-digital and digital-to-analog converters (ADCs/DACs) that surround the compute array consume 40-85% of total system power and up to 80% of chip area.**

This is the dirty secret of every "100x more efficient than GPU" claim. The matrix-vector multiply in the analog domain may be extraordinarily efficient, but the moment you need to get data in and out of the analog array — converting digital inputs to analog voltages (DAC) and converting analog results back to digital (ADC) — the power budget explodes.

---

## 1. Why ADC/DAC Is Such a Big Problem for Analog CIM

### The Fundamental Mismatch

Analog CIM exploits physics — Ohm's law (V = IR) and Kirchhoff's current law (sum of currents at a node = 0) — to perform matrix-vector multiplication in a single step. A crossbar array of resistive memory elements can multiply a 256-element input vector by a 256×256 weight matrix in one clock cycle, with near-zero energy for the compute itself.

But neural networks are digital systems. The inputs come from previous layers as digital numbers. The outputs must be digital numbers for the next layer. Between every analog compute step, you need:

1. **DAC** — Convert N-bit digital input activations to analog voltages or currents (one per row of the crossbar)
2. **Analog compute** — Physics does the multiply-accumulate (MAC) for free (nearly)
3. **ADC** — Convert the analog output current/voltage back to M-bit digital values (one per column of the crossbar)

The ADC problem is worse than the DAC problem because:
- **Resolution requirement grows with array size**: A 256-row crossbar accumulating 256 products needs an ADC with enough bits to represent the sum. For 8-bit inputs × 8-bit weights across 256 rows, the full-precision result is 24 bits. Even with reduced precision, you need 8-12 bit ADCs.
- **One ADC per column**: A 256-column array needs 256 ADCs operating in parallel — column-parallel ADC architecture is mandatory for throughput.
- **ADC power scales exponentially with bits**: Each additional bit of ADC resolution roughly doubles power consumption (Walden FOM scaling). Going from 4-bit to 8-bit ADCs increases power ~16×.

### The Numbers That Matter

| Metric | Reported Range | Source |
|--------|---------------|--------|
| ADC share of total system power | 40-85% | Multiple ISSCC papers, HCiM (2024), Science Advances (2025) |
| ADC share of total chip area | Up to 80% | arXiv:2404.06553 (2024) |
| ADC share of MAC macro power | ~40% | IEEE surveys of SRAM CIM |
| Flash ADC area vs. IMADC | 7.1× larger | Wiley Advanced Intelligent Systems (2025) |
| SAR ADC area vs. IMADC | 2.9× larger | Wiley Advanced Intelligent Systems (2025) |

The 85% figure is not an outlier — it represents the regime where high-resolution ADCs (8+ bit) are used with relatively small crossbar arrays. Even well-optimized designs with 4-5 bit ADCs see 40-60% of power going to conversion.

**This is why analog CIM energy efficiency numbers are always quoted at the "macro level" (just the array + ADC) rather than "system level" (full chip including data movement, control, and digital processing).** The gap between macro-level and system-level efficiency is typically 1.5-3×.

---

## 2. Real Chips: Power and Area Breakdown

### IBM HERMES (14nm, PCM-based)

- **ADC architecture**: 256 linearized current-controlled oscillator (CCO) based ADCs per core at 4μm pitch
- **ADC type**: Time-domain (oscillator-based) — frequency is proportional to input current
- **Innovation**: Novel frequency-linearization technique for CCOs, operating over 1 GHz
- **System efficiency**: 10.5-12.4 TOPS/W
- **Key insight**: IBM chose CCO-based (time-domain) ADCs specifically because they scale well in advanced CMOS nodes where voltage headroom is limited. Traditional voltage-domain ADCs struggle below 1V supply.

Source: [IBM Research — HERMES Core](https://research.ibm.com/publications/hermes-core-a-14nm-cmos-and-pcm-based-in-memory-compute-core-using-an-array-of-300pslsb-linearized-cco-based-adcs-and-local-digital-processing--1)

### EnCharge AI EN100 (Capacitor-based CIM)

- **ADC architecture**: Column-parallel SAR ADCs
- **ADC overhead**: 15-18% of total energy, ~20% of array area
- **Key innovation**: Because capacitor-based CIM outputs a *voltage* (not current), power-efficient SAR ADCs can be used directly without transimpedance amplifiers
- **System efficiency**: >40 TOPS/W (claimed)

This is one of the lowest reported ADC overheads in commercial analog CIM, enabled by the voltage-mode output of capacitive CIM. Most current-mode CIM designs (RRAM, PCM, flash) require transimpedance amplifiers before the ADC, adding power.

Source: [IEEE Spectrum — EnCharge's Analog AI Chip](https://spectrum.ieee.org/analog-ai-chip-architecture), [EE Times](https://www.eetimes.com/encharge-picks-the-pc-for-its-first-analog-ai-chip/)

### Mythic AI M1076 (40nm, Flash-based)

- **ADC architecture**: Column-parallel ADCs integrated into each Analog Compute Engine (ACE) tile
- **DAC**: 8-bit DACs for input encoding
- **Calibration**: DAC/ADC wrapper performs compensation and calibration for accurate 8-bit computation across operating conditions
- **System efficiency**: ~8 TOPS/W (Gen 1 measured), 120 TOPS/W (Gen 2 claimed, unverified)
- **Key insight**: The gap between Gen 1 and Gen 2 claims likely reflects ADC optimization as a major contributor

Source: [WikiChip Fuse — Mythic Analog AI](https://fuse.wikichip.org/news/2755/analog-ai-startup-mythic-to-compute-and-scale-in-flash/)

### PICO-RAM (65nm, SRAM-based, Academic)

- **Area breakdown**: Memory array 70.9%, drivers 14.7%, ADC only 4.6%
- **ADC type**: Compact 8.5-bit dual-threshold time-domain ADC with power gating
- **Key innovation**: ADC is power-gated most of the time, only active during conversion — significant energy reduction

Source: [arXiv:2407.12829](https://arxiv.org/html/2407.12829v1)

### CP-SRAM (40nm simulation, Charge-Pulsation SRAM CIM)

Demonstrates how precision directly controls efficiency:

| Precision | Energy Efficiency |
|-----------|------------------|
| 2-bit | ~2,950 TOPS/W |
| 4-bit | ~576 TOPS/W |
| 6-bit | ~111.7 TOPS/W |

The 26× efficiency drop from 2-bit to 6-bit is almost entirely due to ADC power scaling.

---

## 3. ADC Architectures Used in CIM

### Flash ADC

- **How it works**: 2^N-1 comparators in parallel, each comparing the input to a reference voltage from a resistor ladder. One-shot conversion in a single clock cycle.
- **Pros**: Fastest conversion — single cycle. Good for high-throughput CIM.
- **Cons**: Area and power scale exponentially with bit resolution. A 6-bit flash ADC needs 63 comparators. An 8-bit needs 255.
- **CIM usage**: Rare for high-resolution; sometimes used for 3-4 bit quantized networks
- **Typical overhead**: 15.28% area, 22% power of chip (when used)

### SAR (Successive Approximation Register) ADC

- **How it works**: Binary search — compares input to DAC output, adjusting one bit per cycle from MSB to LSB. N cycles for N bits.
- **Pros**: Area-efficient, moderate power. The capacitor DAC can potentially be reused for CIM computation.
- **Cons**: N clock cycles for N-bit conversion (slower than flash). Sequential nature limits throughput.
- **CIM usage**: Most common in commercial CIM chips. EnCharge uses SAR ADCs because their voltage-mode output is directly compatible.
- **Typical overhead**: 43.1% area, 24.1% power (conventional); 15-18% energy with optimized designs (EnCharge)
- **Key innovation at ISSCC 2025**: Capacitor-reconfigured CIM where the SAR ADC capacitor array is reused for computation, achieving 10-bit accuracy with zero additional ADC area overhead.

### CCO/VCO-Based (Time-Domain) ADC

- **How it works**: Input current/voltage controls the frequency of an oscillator. A counter measures the number of oscillations in a fixed time window, giving a digital output.
- **Pros**: Naturally digital output (counter). Scales beautifully with CMOS process — benefits from faster transistors in smaller nodes. No voltage headroom issues.
- **Cons**: Oscillator nonlinearity must be corrected. Conversion time depends on required precision.
- **CIM usage**: IBM HERMES (CCO-based, 300ps/LSB). Emerging as the preferred architecture for advanced-node CIM.
- **Key innovation**: IBM's frequency-linearization technique enables accurate MVM at >1 GHz operation.

### Time-to-Digital Converter (TDC)

- **How it works**: Analog result is encoded as a time delay; a digital circuit measures the delay.
- **Pros**: Fully digital measurement circuitry. Eliminates comparators and reference voltages.
- **Cons**: Delay-line matching, jitter sensitivity.
- **CIM usage**: Resonant time-domain CIM (rTD-CiM) architectures. TDC-based resonant CIM for INT8 CNNs demonstrated with layer-optimized SRAM mapping.

### Sigma-Delta (ΔΣ) ADC

- **How it works**: Oversamples at high rate with a 1-bit quantizer, shapes quantization noise to high frequencies, then decimation filter produces high-resolution output.
- **Pros**: Very high resolution achievable (16-24 bits). 75% digital circuitry — scales well with process.
- **Cons**: Slow — requires many oversampling cycles. Not suitable for column-parallel CIM where hundreds of ADCs must convert simultaneously.
- **CIM usage**: Rarely used in CIM. The oversampling requirement conflicts with the throughput needs of parallel MAC arrays. Some noise-shaping SAR hybrids at ISSCC 2025 (120 dB SNDR, 189 dB Schreier FOM).

### In-Memory ADC (IMADC)

- **How it works**: Uses the NVM devices themselves for both reference generation and voltage comparison, eliminating separate resistor ladders and comparators.
- **Pros**: Dramatically smaller (0.14× flash ADC area, 0.35× SAR ADC area). Energy: 0.01× flash, 0.03× SAR. Area: 45 μm², energy: 29.6 fJ.
- **Cons**: Depends on NVM device precision and stability. Early-stage research.
- **CIM usage**: Demonstrated in 2025, compatible with various NVM types. Reduces system energy and area by >57% and >30% respectively when integrated.

Source: [Wiley Advanced Intelligent Systems (2025)](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202400594)

---

## 4. State-of-the-Art Low-Power ADC Designs for CIM

### Compute-Aware SNR (CSNR) Optimization (2025)

A breakthrough from ETH Zurich/IBM: instead of optimizing ADC precision for signal-to-quantization-noise ratio (SQNR), optimize for **compute signal-to-noise ratio (CSNR)** — the metric that actually matters for neural network accuracy.

Key result: **ADC precision can be reduced by 3 bits** with 6 dB CSNR gain over SQNR-optimal choices, translating to **40-64× ADC energy savings**. For a 256-dimensional binary dot product, this means using a 5-bit ADC instead of 8-bit with no accuracy loss.

This is arguably the single most impactful ADC optimization for CIM because it attacks the problem at the system level — proving that conventional ADC precision requirements are over-specified for neural network computation.

Source: [arXiv:2507.09776 — Compute SNR-Optimal ADCs for Analog In-Memory Computing](https://arxiv.org/abs/2507.09776)

### Memristor-Based Adaptive ADC (Nature Communications, 2025)

HKU-led team demonstrated a memristor-based ADC with adaptive quantization:
- Uses analog content-addressable memory (CAM) cells with programmable overlapped boundaries
- Quantization thresholds adapt to output distribution (non-uniform quantization)
- **15.1× energy efficiency improvement, 12.9× area reduction** vs. state-of-the-art
- System-level: 57.2% energy reduction and 30.7% area reduction for VGG8 on CIFAR-10
- Achieved 89.55% accuracy on CIFAR-10 (VGG8) at 5-bit adaptive precision

Source: [Nature Communications (2025)](https://www.nature.com/articles/s41467-025-65233-w)

### 44.3 TOPS/W DAC/ADC-Less SRAM CIM (TSMC 55nm, 2024)

A design that largely eliminates both DAC and ADC through clever circuit techniques:
- **DAC elimination**: Binary-weighted bitline-precharge scheme using dedicated reference voltages for bit-serial multiplication in charge domain
- **ADC optimization**: Hybrid charge-sharing integrating ADCs leveraging the same reference voltages
- **Near-CIM analog memory and activation**: Nonlinear activation unit (NAU) operates in analog domain, eliminating inter-layer ADC/DAC
- **Result**: 76.0% energy reduction compared to conventional DAC/ADC solution
- **Peak efficiency**: 44.3 TOPS/W macro-level, 27.7 TOPS/W system-level (4-bit weight)

Source: [IEEE Solid-State Circuits Letters (2024)](https://ieeexplore.ieee.org/document/10569024/)

### 137.5 TOPS/W SRAM CIM with Memory-Cell-Embedded ADCs (2023)

Embeds ADC functionality directly into the memory cell array, using the memory cells themselves as part of the conversion process (9-bit resolution). Eliminates separate ADC column circuitry.

Source: [arXiv:2307.05944](https://arxiv.org/abs/2307.05944)

---

## 5. ADC-Free and ADC-Less Approaches

The most radical solution: eliminate the ADC entirely. Several approaches exist, each with trade-offs.

### Approach 1: Fully Analog Neural Network Hardware (FANCH)

Published in Science Advances (2025), FANCH keeps everything analog between layers:
- Uses transimpedance amplifiers (TIAs), differential voltage amplifiers (DFAs), fully analog activation function units (FAFUs), and voltage comparators
- **No ADC or DAC at intermediate nodes** — only at the very first input and very last output
- Accuracy: 0.36% reduction from software baseline on handwritten digit recognition
- **Limitation**: Only demonstrated on small networks. Analog noise accumulates across layers — the more layers, the worse the accuracy degradation. Scaling to deep networks (50+ layers) is an unsolved problem.

Source: [Science Advances (2025)](https://www.science.org/doi/10.1126/sciadv.adv7555)

### Approach 2: HCiM — Hybrid Analog-Digital CIM Without ADCs

Replaces ADCs with extreme low-precision quantization (binary or ternary partial sums):
- Analog CIM crossbars perform matrix-vector multiplication
- Digital CIM array processes scale factors
- Partial sums quantized to 1-bit (binary) or 1.5-bit (ternary)
- **Energy reduction**: Up to 28× vs. 7-bit ADC baseline, 11× vs. 2-bit ADC baseline
- **Trade-off**: Requires training with quantization-aware methods. Not applicable to all network architectures.

Source: [HCiM — ASP-DAC 2025](https://dl.acm.org/doi/10.1145/3658617.3697572), [arXiv:2403.13577](https://arxiv.org/abs/2403.13577)

### Approach 3: ADC-Free RRAM CIM with Inter-Array PWM (Shimeng Yu, Georgia Tech)

Eliminates ADCs by keeping data analog between sub-arrays:
- Pulse-width modulation (PWM) encodes inter-array data transfer — analog voltage is converted to a pulse whose width represents the value
- No explicit ADC between computation stages
- **Power savings**: 11.6× over conventional ADC approach
- **Energy efficiency**: 421.53 TOPS/W at 100 MHz (40nm TSMC RRAM)
- **Trade-off**: PWM introduces temporal overhead. Noise accumulation across multiple sub-arrays limits depth.

Source: [IEEE VLSI Symposium 2022](https://ieeexplore.ieee.org/document/9830211/)

### Approach 4: LINKAGE — Analog Data Transfer Between Arrays

Eliminates per-processing-element ADCs entirely. Uses an analog data transfer module for inter-array processing. Data stays analog throughout the pipeline.

### Approach 5: Pre-ADC Analog Processing (Aspinity Approach)

Aspinity's AML100/AML200 chips process raw sensor data *before* the ADC — performing classification in the analog domain to determine if digitization is even needed. This is not CIM for neural networks but represents the purest form of "ADC avoidance" at the system level.

### The Common Limitation

All ADC-free approaches share a fundamental problem: **analog noise accumulates**. Every time you pass an analog signal through another stage of computation without digitizing it, you add noise. After 3-5 cascaded analog stages, the accumulated noise destroys the signal-to-noise ratio needed for neural network accuracy. This is why FANCH works on MNIST but scaling to ImageNet-class networks is undemonstrated.

The ADC is not just overhead — it is a **noise firewall**. Converting to digital and back resets the noise floor at each layer boundary. Eliminating the ADC saves power but forces you to manage analog noise across the entire compute pipeline.

---

## 6. Time-Domain and Charge-Domain Computing as Alternatives

### Time-Domain Computing

Instead of encoding values as voltage or current amplitude, encode them as **time** — pulse width, delay, or oscillation frequency.

**Why it matters for CIM:**
- Information encoded in time naturally supports accumulation (longer pulse = larger value)
- Ultra-low-power operation — uses digital-like switching rather than linear amplifiers
- Scales with CMOS process — faster transistors = better time resolution = more bits
- The ADC becomes a simple counter or time-to-digital converter (TDC)

**Key proponent**: Anaflash (startup) argues time-domain CIM directly addresses shortcomings of voltage/current-domain approaches and aligns with advanced CMOS scaling trends.

**IBM's implementation**: HERMES uses CCO-based ADCs — essentially time-domain conversion. The current from the crossbar column controls an oscillator frequency, and a counter digitizes the result. This naturally handles the current-mode output of PCM crossbars.

**Academic results**: TDC-based resonant CIM (rTD-CiM) demonstrated for INT8 CNNs with layer-optimized SRAM mapping. Time-domain approaches show particular promise for advanced nodes (7nm and below) where voltage headroom is limited.

Source: [Anaflash blog](https://www.anaflash.com/post/the-time-for-time-domain-computing-is-now), [arXiv:2601.00434](https://arxiv.org/html/2601.00434)

### Charge-Domain Computing

Instead of summing currents on a wire (current-domain), accumulate charge on a capacitor.

**Advantages over current-domain:**
- **Lower power**: No static current paths. Charge is stored, not flowing.
- **Better linearity**: Capacitors are inherently linear (Q = CV). Resistive elements (RRAM, PCM) have nonlinear I-V curves.
- **Reduced variability**: Charge-domain MAC has less variation than current-domain MAC.
- **Compatible with SAR ADCs**: The accumulated charge/voltage can be directly sampled by a SAR ADC without a transimpedance amplifier.

**EnCharge AI** is the leading commercial implementation: capacitors formed from metal interconnect layers above SRAM cells store and accumulate charge. The voltage-mode output enables efficient SAR ADC conversion with only 15-18% energy overhead.

**Academic work**: CP-SRAM (charge-pulsation SRAM CIM) demonstrated configurable precision from 2-bit (2,950 TOPS/W) to 6-bit (111.7 TOPS/W). A 2024 SRAM charge-domain CIM with 7-bit hybrid ADC showed low-cost MAC operations.

Source: [Electronics 13(3):666 (2024)](https://www.mdpi.com/2079-9292/13/3/666), [Wiley Advanced Intelligent Discovery (2025)](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aidi.202500143)

---

## 7. How Bit Precision Affects ADC Requirements and Power

This is the crux of the analog CIM design trade-off.

### The Exponential Scaling Problem

ADC power scales as:

```
P_ADC ∝ 2^N × f_s
```

where N is the number of bits and f_s is the sampling rate (Walden FOM scaling). Each additional bit doubles the power. The thermal FOM is even worse: power scales as 4× per additional bit when kT/C noise dominates.

### What Precision Do You Need?

For a crossbar array with R rows, W-bit weights, and I-bit inputs:
- **Full precision output**: W + I + log₂(R) bits
- **Example**: 8-bit weights × 8-bit inputs × 256 rows = 8 + 8 + 8 = 24 bits
- **Practical requirement**: Neural networks tolerate quantization. 6-8 bit ADC output typically sufficient.
- **With CSNR optimization**: 3 fewer bits needed → 40-64× energy savings.

### Precision vs. Efficiency Across Real Designs

| Design | ADC Bits | Efficiency | Year |
|--------|----------|------------|------|
| CP-SRAM (2-bit) | 2 | 2,950 TOPS/W | 2022 |
| RRAM ADC-free (PWM) | 0 (analog) | 421.5 TOPS/W | 2022 |
| CP-SRAM (4-bit) | 4 | 576 TOPS/W | 2022 |
| CP-SRAM (6-bit) | 6 | 111.7 TOPS/W | 2022 |
| Near-CIM DAC/ADC-less | ~4 | 44.3 TOPS/W | 2024 |
| IBM HERMES (8-bit) | 8 | 12.4 TOPS/W | 2023 |
| EnCharge EN100 (8-bit) | 8 | >40 TOPS/W | 2025 |

The pattern is stark: **going from 2-bit to 8-bit ADC resolution costs 50-200× in energy efficiency**. This is why many CIM papers report impressive numbers at 2-4 bit precision that evaporate at 8-bit.

### The Precision Trap

Most real neural network workloads (especially transformer-based LLMs) require at minimum INT4-INT8 precision. The CIM papers showing 1,000+ TOPS/W at 1-2 bit precision are measuring efficiency on workloads that do not represent production AI inference. The efficiency at production-relevant precision (INT8) is 10-50 TOPS/W — competitive with but not dramatically better than digital accelerators.

**CNNs tolerate lower precision** and can operate at low CSNR, making them good targets for aggressive ADC optimization. **Transformers require higher precision**, limiting ADC power reduction.

---

## 8. Theoretical Minimum ADC Power for CIM

### The 100 fJ/Op Wall

Recent analysis (arXiv:2602.08081, February 2026) establishes a **practical upper limit of 100 fJ/Op (10 TOPS/W)** for analog CIM, which roughly coincides with the end of technology-limited ADC scaling.

This means:
- At current and near-future CMOS nodes, ADC technology imposes a floor on analog CIM efficiency
- Below ~100 fJ/Op, the ADC energy dominates regardless of how efficient the analog compute is
- This is why analog CIM papers showing >100 TOPS/W numbers invariably use low-bit precision (1-4 bit) or exclude ADC power

### Walden FOM Limits

The Walden figure of merit defines ADC efficiency as:

```
FOM_W = P / (2^ENOB × f_s)
```

State-of-the-art SAR ADCs achieve ~1 fJ/conversion-step. For a CIM array needing 256 column ADCs at 8-bit resolution converting at 1 GHz:

```
P_ADC = 256 × 1 fJ × 256 × 1 GHz = 65.5 mW (just ADC)
```

For the same array performing 256 × 256 = 65,536 MACs per cycle at 1 GHz:
```
Efficiency = 65,536 × 2 × 1 GHz / 0.0655 W ≈ 2,000 TOPS/W (compute only)
```

But adding 65.5 mW of ADC power to even 1 mW of compute power gives:
```
System efficiency = 131 GOPS / 66.5 mW ≈ 1,970 TOPS/W
```

This looks great — until you realize the 1 fJ/step is the *best-in-class* ADC, and real column ADCs in CIM macros are 10-100× worse due to area constraints, matching requirements, and the need for hundreds of identical ADCs on one chip.

### Gain-Ranging and Local Normalization

A promising theoretical approach: instead of designing the ADC for the worst-case dynamic range (full-scale accumulation of 256 products), use gain-ranging or local normalization to reduce the dynamic range that the ADC must handle.

Result: **SQNR-dominated scaling** — the required ADC energy increases with precision but not with array size. This potentially breaks the log₂(R) bits penalty and enables larger arrays without proportionally larger ADCs.

---

## 9. Circuit-Level Innovations to Reduce Conversion Overhead

### Innovation 1: Capacitor Reuse Between CIM and SAR ADC

At ISSCC 2025, a capacitor-reconfigured CIM structure was presented where the capacitor array used for SAR ADC conversion is the same physical structure used for CIM computation. During compute, capacitors perform charge-domain MAC. During conversion, the same capacitors implement the SAR binary search.

**Result**: 10-bit ADC conversion accuracy with zero additional area overhead for the ADC.

### Innovation 2: In-Memory ADC (IMADC)

Uses NVM devices themselves for ADC reference generation and comparison:
- **Area**: 0.14× flash ADC, 0.35× SAR ADC (45 μm²)
- **Energy**: 0.01× flash ADC, 0.03× SAR ADC (29.6 fJ)
- Single flash thin-film transistor performs both reference generation and comparison

### Innovation 3: Near-CIM Analog Activation

Instead of: analog output → ADC → digital ReLU → DAC → next layer
Do: analog output → analog ReLU → next analog input

The 44.3 TOPS/W SRAM CIM places analog nonlinear activation units (NAUs) adjacent to the CIM array, keeping the signal analog between layers and eliminating one ADC/DAC pair per layer. **76% energy reduction** vs. full ADC/DAC conversion.

### Innovation 4: Adaptive Quantization

The HKU memristor-based ADC uses non-uniform quantization thresholds that adapt to the actual output distribution of each layer. Neural network outputs are not uniformly distributed — most values cluster near zero. By concentrating quantization levels where the data actually is, fewer bits achieve the same effective precision.

### Innovation 5: Sparsity-Aware ADC

If the input vector is sparse (many zeros), many columns will have near-zero outputs. An 8-bit SAR ADC can detect zero outputs in 2 cycles instead of 8, effectively operating as a 6-bit converter on average. Exploiting natural sparsity in neural network activations (typically 50-90% for ReLU networks) reduces average ADC energy by 1.5-3×.

### Innovation 6: PWM Input Encoding (DAC Elimination)

Replace the input DAC with pulse-width modulation: apply a digital pulse whose width is proportional to the input value. The resistive crossbar integrates the current over time, and the accumulated charge represents the multiply-accumulate result. This eliminates DACs entirely but converts space efficiency into time efficiency (serial processing).

### Innovation 7: Bit-Serial Processing

Instead of converting the full N-bit result at once, process inputs one bit at a time and accumulate digitally with shift-and-add. Each bit-serial step only needs a 1-bit ADC (comparator). N cycles for N-bit input, but the ADC is trivial.

**Trade-off**: Throughput is reduced by N× (for N-bit input), but ADC power and area are reduced by orders of magnitude.

---

## 10. The System-Level Reality

### Why "Macro-Level" TOPS/W Is Misleading

Published CIM efficiency numbers are almost always macro-level (the CIM array + its peripheral ADC/DAC). A full system includes:

| Component | Typical Power Share |
|-----------|-------------------|
| CIM array (analog compute) | 5-15% |
| ADCs | 30-60% |
| DACs | 5-15% |
| Digital logic (accumulation, activation, control) | 10-20% |
| Data movement (on-chip buses, buffers) | 10-25% |
| I/O and DRAM interface | 5-15% |

The macro-to-system efficiency gap is typically **1.5-3×**. A CIM macro at 100 TOPS/W becomes 30-65 TOPS/W at the system level.

For comparison, NVIDIA's best inference GPUs (Blackwell B200) achieve ~2-5 TOPS/W at INT8 system-level. Digital CIM chips like Axelera Metis achieve 20-40 TOPS/W system-level. So analog CIM's advantage at the system level is **2-10× over digital accelerators**, not the 100× claimed in press releases.

### The Digital CIM Counterargument

d-Matrix and other digital in-memory compute (DIMC) companies argue: if you eliminate the ADC/DAC bottleneck entirely by staying digital, you get most of the memory-bandwidth benefit (150 TB/s internal bandwidth) without the analog noise, calibration, and conversion overhead problems. Digital CIM achieves 10-40 TOPS/W at INT8 with full programmability — and the gap to analog CIM's system-level numbers is surprisingly small.

This is the strongest argument against analog CIM: **the ADC/DAC overhead eats most of the theoretical advantage that analog compute provides.**

---

## 11. Summary: The ADC/DAC Bottleneck in One Table

| Aspect | Current State | Best-Case Trajectory |
|--------|--------------|---------------------|
| ADC share of power | 40-85% | 15-20% (with CSNR, IMADC, ADC reuse) |
| ADC share of area | 20-80% | 5-15% (with IMADC, capacitor reuse) |
| Dominant ADC type | SAR (commercial), CCO (IBM) | Time-domain / in-memory ADC |
| Best ADC-less efficiency | 421.5 TOPS/W (RRAM PWM) | Higher with scaled processes |
| Best with-ADC efficiency | >40 TOPS/W at INT8 (EnCharge) | 50-100 TOPS/W with optimized ADC |
| Theoretical floor | ~100 fJ/Op (10 TOPS/W) | May improve with 3nm+ ADC scaling |
| System-level vs. digital | 2-10× advantage | Narrowing as digital CIM improves |

### The Verdict

The ADC/DAC bottleneck is not a temporary engineering problem — it is a **fundamental architectural consequence** of bridging analog and digital domains. Every analog CIM chip must pay this tax. The question is not whether the tax exists but whether circuit innovations can reduce it enough that analog compute's inherent efficiency advantage survives at the system level.

The most promising paths forward:
1. **CSNR-optimal ADC design** — reducing required precision by 3 bits (40-64× energy savings)
2. **Charge-domain CIM** (EnCharge) — voltage-mode output enables efficient SAR ADCs (15-18% overhead)
3. **In-memory ADC** — using NVM devices for conversion (0.01-0.03× conventional ADC energy)
4. **Time-domain architectures** — scaling-friendly, no voltage headroom issues
5. **ADC-free cascading** — keeping data analog between layers for limited-depth networks

But the inconvenient truth remains: **at INT8 precision for production AI workloads, analog CIM's system-level advantage over optimized digital is 2-10×, not 100×.** The ADC/DAC bottleneck is the primary reason.

---

## Sources

- [FANCH — Science Advances (2025)](https://www.science.org/doi/10.1126/sciadv.adv7555)
- [44.3 TOPS/W DAC/ADC-Less SRAM CIM — IEEE SSC Letters](https://ieeexplore.ieee.org/document/10569024/)
- [HCiM ADC-Less Architecture — arXiv](https://arxiv.org/abs/2403.13577)
- [CSNR-Optimal ADCs — arXiv](https://arxiv.org/abs/2507.09776)
- [Energy Bounds of Analog CIM — arXiv](https://arxiv.org/abs/2602.08081)
- [Memristor Adaptive ADC — Nature Communications (2025)](https://www.nature.com/articles/s41467-025-65233-w)
- [In-Memory ADC (IMADC) — Wiley (2025)](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202400594)
- [ADC Energy/Area Modeling — arXiv](https://arxiv.org/abs/2404.06553)
- [SRAM CIM Review — arXiv](https://arxiv.org/html/2411.06079v2)
- [ADC-Free RRAM with PWM — IEEE VLSI 2022](https://ieeexplore.ieee.org/document/9830211/)
- [IBM HERMES — IBM Research](https://research.ibm.com/publications/hermes-core-a-14nm-cmos-and-pcm-based-in-memory-compute-core-using-an-array-of-300pslsb-linearized-cco-based-adcs-and-local-digital-processing--1)
- [EnCharge AI — IEEE Spectrum](https://spectrum.ieee.org/analog-ai-chip-architecture)
- [EnCharge AI — EE Times](https://www.eetimes.com/encharge-picks-the-pc-for-its-first-analog-ai-chip/)
- [Mythic AI — WikiChip Fuse](https://fuse.wikichip.org/news/2755/analog-ai-startup-mythic-to-compute-and-scale-in-flash/)
- [PICO-RAM — arXiv](https://arxiv.org/html/2407.12829v1)
- [Nature Electronics — Analog CIM Tile Design (2025)](https://www.nature.com/articles/s41928-025-01537-5)
- [Anaflash — Time-Domain Computing](https://www.anaflash.com/post/the-time-for-time-domain-computing-is-now)
- [d-Matrix DIMC — Vik's Newsletter](https://www.viksnewsletter.com/p/d-matrix-in-memory-compute)
- [137.5 TOPS/W CIM with Embedded ADC — arXiv](https://arxiv.org/abs/2307.05944)
- [Analog Computing Survey — MDPI Electronics (2025)](https://www.mdpi.com/2079-9292/14/16/3159)
- [High-Precision ADC Techniques ISSCC 2025 — Journal of Semiconductors](https://www.jos.ac.cn/article/doi/10.1088/1674-4926/25050012)
- [Achieving High Precision in Analog IMC — npj Unconventional Computing (2025)](https://www.nature.com/articles/s44335-025-00044-2)
