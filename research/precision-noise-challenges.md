# Precision and Noise Challenges in Analog Compute-in-Memory

*The core technical challenge that determines whether analog can work for AI.*

Last updated: 2026-03-22

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [What Precision Can Analog CIM Realistically Achieve?](#what-precision-can-analog-cim-realistically-achieve)
3. [Sources of Noise and Variability](#sources-of-noise-and-variability)
4. [Weight Drift: How Precision Degrades Over Time](#weight-drift-how-precision-degrades-over-time)
5. [Temperature Sensitivity](#temperature-sensitivity)
6. [Calibration Requirements](#calibration-requirements)
7. [Noise-Aware Training: Does Training-for-Noise Work?](#noise-aware-training-does-training-for-noise-work)
8. [Analog 4-bit vs Digital INT4: Are They Equivalent?](#analog-4-bit-vs-digital-int4-are-they-equivalent)
9. [The ADC/DAC Bottleneck](#the-adcdac-bottleneck)
10. [IR Drop and Array Scaling](#ir-drop-and-array-scaling)
11. [On-Chip Training vs Inference-Only](#on-chip-training-vs-inference-only)
12. [Memory Technology Comparison on Precision](#memory-technology-comparison-on-precision)
13. [Fundamental Physics Limits](#fundamental-physics-limits)
14. [Techniques to Boost Precision Beyond Device Limits](#techniques-to-boost-precision-beyond-device-limits)
15. [The Bottom Line](#the-bottom-line)
16. [Sources](#sources)

---

## Executive Summary

**The precision problem is the central challenge of analog compute-in-memory (CIM).** Every advantage analog has in energy efficiency and parallelism is gated by a single question: can it compute accurately enough?

The honest answers, based on measured silicon as of early 2026:

- **Raw analog MVM precision is typically 3-6 effective bits.** IBM's HERMES chip (the most impressive analog CIM demonstration) achieves 3-4 effective bits per matrix-vector multiply across all 64 cores. NeuRRAM achieves accuracy comparable to 4-bit quantized software models. EnCharge AI's capacitor-based approach claims software-equivalent accuracy at 91% CIFAR-10 -- but uses charge-domain techniques that are fundamentally more precise than resistive approaches.

- **Analog "4-bit" is not the same as digital INT4.** Digital INT4 has deterministic, uniform quantization noise. Analog 4-bit has stochastic, non-uniform noise that varies with temperature, time, device position in the array, and individual device history. This distinction matters enormously for deployment.

- **Noise-aware training works, but is not magic.** Hardware-aware training (IBM's approach) can recover accuracy lost to analog non-idealities. IBM demonstrated iso-accuracy (within 1% of FP32 reference) on 5 of 11 AI workloads with their PCM model. The NeuRRAM team showed noise injection training improved CIFAR-10 accuracy from 25.34% to 85.99% on their hardware. But this means the training pipeline must model the specific hardware -- you cannot just deploy a standard quantized model.

- **Drift is manageable but never solved.** PCM conductance drifts following a power law with drift coefficient 0.1-0.15. IBM's new SiSbTe material reduces this to ~0.04, maintaining BERT accuracy within 2% loss for 7+ days at 65C. Flash and capacitor-based approaches largely avoid this problem.

- **The ADC is the enemy.** ADCs consume up to 60% of total system energy in state-of-the-art analog CIM designs. Higher precision ADCs cost exponentially more energy. This single component often eliminates the energy advantage that analog compute was supposed to provide.

- **"Power, speed, or accuracy -- pick two"** remains the fundamental law. No analog CIM system has broken this tradeoff.

---

## What Precision Can Analog CIM Realistically Achieve?

### Measured Silicon Results

| Chip / System | Technology | Effective Precision | Key Metric | Source |
|---|---|---|---|---|
| IBM HERMES (64-core) | PCM, 14nm | **3-4 bits** effective MVM | BLEU score matches FP32 baseline (with multi-core tiling + digital correction) | Nature Electronics, 2023 |
| NeuRRAM | RRAM, 130nm | **~4 bits** equivalent | 85.7% CIFAR-10 (matches 4-bit quantized software) | Nature, 2022 |
| EnCharge AI IMAGINE | Capacitor/SRAM, 22nm | **Up to 8 bits** input, charge-domain | 91% CIFAR-10 (matches software baseline) | ISSCC / arXiv, 2024 |
| Mythic M1076 | Flash, 40nm | **8-bit** weight storage (256 levels) | 8-bit claimed with internal calibration | Mythic product docs |
| ISSCC 2020 RRAM CIM | RRAM | **~4-5 bits** | 78.4 TOPS/W | ISSCC 2020 |
| Peking Univ. RRAM | RRAM | **Up to 24-bit** (via bit slicing + iterative refinement) | 1000x vs GPU on matrix equations | Nature Electronics, 2025 |
| Adaptive memristor ADC | RRAM, memristive | **5-bit** | 89.55% CIFAR-10 (VGG8) | Nature Communications, 2025 |
| Charge-domain CIM macro | SRAM capacitor | **8-bit** with <0.79% error | Charge-based accumulation | Various ISSCC papers |

### The Precision Hierarchy

Based on all available data, the realistic precision hierarchy for analog CIM is:

1. **Capacitor/charge-domain (EnCharge-style): 6-8 effective bits.** Capacitors have values determined by geometry (wire spacing), which foundries control extremely well. Charge-domain accumulation avoids the current-summation noise of resistive approaches. This is the most precise analog CIM approach.

2. **Flash memory (Mythic-style): 5-8 bits stored, ~5-6 effective bits in compute.** Flash cells can store 256 levels (8 bits), but read noise, charge leakage over time, and temperature sensitivity reduce effective compute precision. Mythic claims 8-bit with calibration.

3. **SRAM-based analog CIM: 4-6 effective bits.** Volatile (loses weights on power-off), but excellent endurance and speed. Best ISSCC results show 4-6 bit effective compute precision.

4. **RRAM/Memristor: 3-5 effective bits.** Filament-based switching is inherently stochastic. Device-to-device variability is high. NeuRRAM demonstrates 4-bit equivalent accuracy is achievable with careful co-design.

5. **PCM: 3-4 effective bits.** IBM HERMES achieves 3-4 bits per MVM across all 64 cores. PCM drift and the limited number of reliable conductance states constrain precision.

6. **MRAM (STT/SOT): 1-2 bits for analog, but excellent binary.** MTJ resistance ratio is too low for multi-level analog. Best for binary or ternary neural networks. Ultra-low cycle-to-cycle variation (~0.3-0.5%) is a major advantage for what it can do.

### The Critical Insight

**Effective compute precision is always lower than storage precision.** Mythic stores 8-bit weights but the effective precision of the MAC output is lower due to accumulated noise from read operations, IR drop, ADC quantization, and thermal effects. IBM stores multi-level PCM values but gets only 3-4 effective bits per MVM. The gap between storage precision and compute precision is the defining challenge of analog CIM.

---

## Sources of Noise and Variability

Analog CIM systems face noise from multiple independent sources that compound during computation. Understanding each source is essential.

### 1. Device-to-Device (D2D) Variability
**What it is:** Manufacturing variations cause nominally identical devices to have different electrical characteristics.

- **RRAM:** Filament formation is fundamentally stochastic. The shape, diameter, and composition of the conductive filament vary from device to device. This is a physics problem, not an engineering problem. Forming, SET, and RESET operations all exhibit broad resistance distributions.
- **PCM:** Heater geometry variations affect the volume of phase-change material that switches. Typical D2D variability in conductance: 5-15%.
- **Flash:** Threshold voltage variation due to random dopant fluctuation and oxide thickness variation. Relatively well-controlled in mature processes.
- **SRAM:** Vt mismatch in transistors. Well-characterized in CMOS foundries.
- **Capacitor (EnCharge-style):** Geometry-dependent. "The only thing they depend on is geometry -- the space between wires -- which is the one thing you can control very, very well in CMOS technologies." Lowest D2D variability of all CIM approaches.

### 2. Cycle-to-Cycle (C2C) Variability
**What it is:** The same device gives slightly different results each time it is read or programmed.

- This is true stochastic noise -- random both spatially and temporally.
- **Magnitude:** Read noise standard deviation is typically 5-10% of the mean conductance for resistive devices (RRAM, PCM).
- **MRAM:** Ultra-low C2C variation. Experimentally verified over 1 million mass-produced MTJ devices.
- **Impact:** For a 512x512 analog tile with standard PCM settings, the reported L2 error of a single MVM is ~13% at 1 second post-programming (IBM aihwkit simulation).

### 3. Thermal Noise (Johnson-Nyquist Noise)
**What it is:** Random voltage/current fluctuations from thermal agitation of charge carriers in any conductor. Present in every resistor, transistor, and wire.

- Fundamental: V_noise = sqrt(4kTR * BW), where k is Boltzmann's constant, T is temperature, R is resistance, BW is bandwidth.
- At room temperature (300K), kT = 26 meV = 4.1 x 10^-21 J.
- Thermal noise power scales linearly with temperature. Going from 25C to 85C increases thermal noise by ~20%.
- **In CIM:** Thermal noise affects every readout. It sets a floor on achievable SNR for a given resistance and bandwidth.

### 4. Shot Noise
**What it is:** Discrete nature of electron flow causes current fluctuations. Especially significant at low currents.

- I_noise = sqrt(2qI * BW), where q is electron charge, I is DC current.
- **In CIM:** Matters most for low-conductance (high-resistance) memory states, which carry the least current. This means the noise is worst for small weight values -- exactly where precision matters most for neural networks.
- Research has shown inference is possible even at SNR ~1 (extremely high shot noise) by using physics-based probabilistic models during training.

### 5. 1/f (Flicker) Noise
**What it is:** Low-frequency noise that is inversely proportional to frequency. Dominant at low frequencies.

- Caused by carrier trapping/de-trapping at oxide interfaces.
- Particularly problematic for slow read operations in CIM, where integration times are long.
- More severe in scaled devices with smaller gate areas.

### 6. Random Telegraph Noise (RTN)
**What it is:** Discrete switching between two or more resistance/current levels due to individual trap states.

- Can cause abrupt jumps in conductance, mimicking a weight change.
- Especially problematic in deeply scaled RRAM and flash devices.
- Not Gaussian -- cannot be simply averaged away.

### 7. Programming Noise
**What it is:** The deviation of actual conductance from the target value when programming a weight.

- Iterative verify-and-program schemes reduce this but cost time and energy.
- PCM: Crystallization is a stochastic nucleation process. Programming the same target conductance repeatedly gives a distribution, not a point.
- RRAM: Filament formation is probabilistic. Each SET/RESET cycle produces a slightly different filament.

### 8. How Noise Sources Compound

In a crossbar MVM operation computing y = W*x:
- Each weight w_ij has D2D variability + programming noise + drift.
- Each read of w_ij * x_i adds C2C read noise + thermal noise + shot noise + 1/f noise.
- Currents from all rows in a column are summed (analog accumulation) -- noise from each row adds.
- For a column of N rows, total noise power grows as ~N (noise adds in quadrature if independent), but signal grows as N. So SNR improves as sqrt(N). This means **larger arrays have better SNR per MAC but more absolute noise in the output.**
- The column current is then digitized by an ADC, which adds quantization noise.

**The result: noise from 8+ independent sources compounds at every step of the computation.**

---

## Weight Drift: How Precision Degrades Over Time

### PCM Drift: The Most Studied Problem

PCM conductance drifts over time due to structural relaxation of the amorphous phase. This is a fundamental material physics phenomenon, not a manufacturing defect.

**The drift model:**
```
G(t) = G_prog * (t / t_c)^(-v)
```
Where:
- G_prog is the programmed conductance
- t_c is a reference time
- v is the drift exponent (drift coefficient)

**Quantitative drift characteristics:**
- **Standard GST (Ge2Sb2Te5):** Drift coefficient v = 0.1-0.15. This means conductance drops by ~30-40% over the first hour, then continues to slowly decay.
- **IBM's SiSbTe material (2024):** Drift coefficient v ≈ 0.04 (state-independent across the entire analog range). Maintains BERT accuracy within 2% loss for >7 days at 65C. This is a significant improvement.
- **Projected PCM:** Using a metallic liner to "project" the resistance, drift can be suppressed. But this reduces the dynamic range of conductance states.

**Drift is state-dependent:** Higher resistance (more amorphous) states drift more than lower resistance (more crystalline) states. This means drift is non-uniform across weights, which is worse than uniform degradation.

**Temporal behavior:** Drift follows a power law (approximately logarithmic over practical timescales). Most drift happens early -- the first seconds to minutes after programming see the largest changes. After hours, the rate slows but never stops.

### Flash Memory Drift

- Flash cells experience charge loss over time (electrons tunneling out of the floating gate).
- Rate: ~0.1-1 mV/decade of time for threshold voltage shift.
- Much slower than PCM drift. Mythic's flash approach benefits from this.
- Temperature accelerates charge loss significantly.

### RRAM Drift

- RRAM exhibits retention-related drift, though mechanisms differ from PCM.
- Filament dissolution or growth can cause gradual resistance changes.
- High-resistance states (thin filaments) are more vulnerable.
- Typical retention: 10 years at 85C for binary states, but multi-level (analog) retention is much shorter.

### Capacitor-Based (EnCharge-style): Minimal Drift

- Capacitor values are set by geometry -- they do not drift.
- If weights are stored as charges on capacitors (like DRAM), they leak and require refresh.
- If weights are stored in SRAM latches controlling capacitor networks, no drift occurs.
- **This is a fundamental advantage of the capacitor-based approach.**

### MRAM: Effectively Zero Drift

- Magnetic states in MTJ devices are extremely stable at room temperature.
- Retention: >10 years at 85C for properly designed devices.
- Thermal stability factor determines retention -- well-understood and designable.
- For binary CIM, MRAM is the most stable option.

---

## Temperature Sensitivity

Temperature is a critical and often underreported challenge for analog CIM.

### Why Temperature Matters

1. **Thermal noise increases linearly with T:** A chip at 85C (automotive grade) has ~20% more thermal noise than at 25C.
2. **Device characteristics shift with temperature:**
   - Transistor threshold voltage: ~-1 to -2 mV/C.
   - RRAM: Resistance changes with temperature (thermally-activated conduction).
   - PCM: Conductance drift accelerates exponentially with temperature (Arrhenius-like behavior). Drift that takes hours at 25C can happen in minutes at 85C.
   - Flash: Charge loss accelerates with temperature.
3. **ADC/DAC accuracy degrades with temperature:** Reference voltages shift, comparator offsets change.
4. **IR drop changes:** Wire resistance increases with temperature (~0.3-0.4%/C for copper), worsening IR drop in crossbar arrays.

### Measured Temperature Effects

- **IBM PCM temperature study (IEDM 2021):** Investigated impact of temperature on multi-level PCM conductance states. The time-temperature dependence of conductance states is complex -- both the initial conductance and the drift rate change with temperature.
- **Sub-threshold analog circuits:** "The main drawback of analog sub-threshold electronic circuits is their dramatic temperature sensitivity." Subthreshold current has exponential temperature dependence.
- **Flash-based analog CIM:** Research on 55nm NOR flash showed "temperature-insensitive" vector-by-matrix multiplication is achievable but requires specific circuit design techniques.
- **Neuromorphic chips:** Techniques exist to adapt driving signals in response to temperature variation to compensate for temperature sensitivity.

### The Automotive Problem

Edge AI deployment often requires -40C to +125C operation (automotive grade). Most analog CIM demonstrations are at room temperature (25C). The gap between lab demonstrations and automotive-grade operation is enormous. No analog CIM chip has demonstrated full automotive temperature range operation with acceptable accuracy, to our knowledge.

---

## Calibration Requirements

### What Needs Calibration

1. **ADC calibration:** Remove nonlinear response, offset, and gain errors. IBM HERMES uses on-chip ADC calibration circuits -- this is credited as key to achieving 3-4 bit effective precision.
2. **Weight calibration:** Periodically verify that stored weights match intended values. Essential for PCM (drift), helpful for RRAM (retention), less critical for flash and capacitor approaches.
3. **Drift compensation:** IBM's global scaling calibration reads a subset of columns at constant voltage to track drift and apply correction factors.
4. **Temperature compensation:** On-chip temperature sensors + lookup tables or analog compensation circuits.

### Calibration Frequency

- **PCM:** Most drift happens in the first seconds to minutes. IBM's global scaling calibration can maintain accuracy for >1 hour post-programming. With SiSbTe material, 7+ days between recalibrations.
- **Flash:** Calibration every hours to days, depending on temperature and precision requirements.
- **SRAM/Capacitor:** Minimal calibration needed for the compute elements. ADC calibration at startup typically sufficient.
- **RRAM:** Programming verification (iterative write-verify) needed at weight programming time. Read calibration periodically.

### The Calibration Tax

Every calibration cycle:
- Takes the chip offline (no inference during calibration) or requires redundant compute units.
- Consumes energy.
- Adds system complexity.

**This is a hidden cost that efficiency claims often omit.** A chip that achieves 100 TOPS/W but needs to recalibrate every hour, spending 10 minutes on calibration, effectively delivers only 83 TOPS/W over its duty cycle.

---

## Noise-Aware Training: Does Training-for-Noise Work?

### The Approach

Instead of trying to eliminate noise in hardware (expensive, often impossible), train the neural network to be robust to the specific noise characteristics of the target hardware.

**IBM's Hardware-Aware Training (HWA Training):**
1. Train the DNN in FP32 as usual.
2. Retrain by injecting hardware-calibrated noise into the forward pass: read noise, programming errors, conductance drift, ADC quantization, IR drop.
3. Use SGD to make the network robust to these non-idealities.

### Results

**IBM (Nature Communications, 2023):**
- Tested 11 diverse AI workloads (CNNs, RNNs, Transformers).
- Achieved iso-accuracy (within 1% of FP32 reference) on **5 of 11 workloads** after 1+ hour of PCM drift.
- The other 6 workloads showed degradation beyond 1%.
- Conclusion: HWA training is effective but not universal. Some network architectures are inherently more robust to analog noise than others.

**NeuRRAM (Nature, 2022):**
- Without noise injection training: 25.34% accuracy on CIFAR-10 (essentially random).
- With noise injection training: 85.99% accuracy on CIFAR-10.
- **This is the most dramatic demonstration of how critical noise-aware training is.** A model that works perfectly in software simulation is useless on analog hardware without hardware-aware retraining.

**IBM aihwkit Framework:**
- Open-source toolkit for simulating analog hardware non-idealities during training.
- Models: programming noise, read noise (normal distribution, std = 5-10% of conductance), conductance drift (power law), temperature effects, ADC/DAC quantization.
- Allows pre-deployment accuracy estimation before taping out silicon.

### Limitations of Noise-Aware Training

1. **Requires hardware-specific models.** A model trained for PCM noise characteristics will not work on RRAM hardware. There is no "universal analog noise resilience."
2. **Training cost increases.** Forward pass must simulate hardware noise at every step -- typically 2-5x training cost.
3. **Not all architectures are equally amenable.** Transformers and attention mechanisms are more sensitive to noise than simple CNNs.
4. **Noise characteristics may change over device lifetime.** The noise model used during training must remain valid for the deployed hardware's actual behavior.
5. **Does not eliminate the precision gap.** Even with perfect noise-aware training, the effective precision is bounded by the hardware's SNR. You are training the network to tolerate lower precision, not increasing the precision.

### The Deeper Issue

Noise-aware training is powerful but shifts the problem from hardware to software. It creates a tight coupling between the neural network and the specific hardware platform. This is the opposite of the digital world's greatest strength: hardware-software abstraction. **Every analog CIM platform needs its own training pipeline, its own noise models, its own deployment flow.** This is a major barrier to adoption.

---

## Analog 4-bit vs Digital INT4: Are They Equivalent?

**No. They are fundamentally different, and conflating them is one of the most common mistakes in analog CIM evaluation.**

### Digital INT4

- **Deterministic:** The same input always produces the same output.
- **Uniform quantization:** All levels are equally spaced. The quantization error is bounded and predictable.
- **Reproducible:** Run the same model on any INT4 hardware, get the same result (within rounding).
- **Well-characterized:** Extensive literature on INT4 model accuracy. The case for 4-bit precision is strong -- recent work shows 4-bit quantized LLMs retain most accuracy.
- **Hardware support:** NVIDIA Blackwell GPUs natively support FP4; extensive INT4 support across hardware.

### Analog "4-bit equivalent"

- **Stochastic:** Each computation has random noise. Running the same input twice gives slightly different outputs.
- **Non-uniform noise:** Noise magnitude depends on the specific weight values, array position (IR drop), temperature, time since programming (drift), and device history.
- **Position-dependent:** Weights at the edges of a crossbar array experience different IR drop than weights at the center. This means the "effective precision" varies by physical location.
- **Time-dependent:** Precision degrades over time due to drift (PCM, RRAM) or charge leakage (flash).
- **Temperature-dependent:** Precision changes with operating temperature.
- **Not directly comparable to INT4 benchmarks.** When a paper says an analog chip achieves "accuracy comparable to 4-bit quantized software," this means the end-to-end inference accuracy (on a specific benchmark) is similar -- but the error characteristics are completely different.

### What This Means in Practice

A digital INT4 model that achieves 90% accuracy on a benchmark will achieve 90% accuracy every time, on every chip, at every temperature, forever.

An analog "4-bit equivalent" model might achieve:
- 90% accuracy right after programming at 25C.
- 88% accuracy after 1 hour (drift).
- 85% accuracy at 85C.
- 87% accuracy on chip #2 (different device characteristics).
- 91% accuracy on a different run (stochastic noise helping rather than hurting).

**The variance is the problem, not the mean.** For safety-critical applications (automotive, medical), this variance is potentially disqualifying.

### The Effective Bits Comparison

| Property | Digital INT4 | Analog "4-bit equivalent" |
|---|---|---|
| Noise type | Deterministic quantization | Stochastic, multi-source |
| Error bound | Bounded (max 0.5 LSB) | Unbounded (tails of noise distribution) |
| Reproducibility | Exact | Statistical |
| Temperature stability | Excellent | Poor to moderate |
| Temporal stability | Permanent | Degrades (drift) |
| Position independence | Yes | No (IR drop varies) |
| Deployability | Standard toolchain | Hardware-specific pipeline |

---

## The ADC/DAC Bottleneck

**The ADC is the Achilles' heel of analog CIM.** This single component can dominate the area, energy, and precision of the entire system.

### The Energy Problem

- **ADCs consume up to 60% of total energy** in state-of-the-art analog CIM systems.
- ADC energy scales as ~4^ENOB (exponential in effective bits). Going from 4-bit to 8-bit ADC increases energy by ~256x.
- A single high-precision ADC can consume more energy than the entire analog MAC array it serves.

### The Precision-Energy Tradeoff

- Lowering ADC precision reduces energy but degrades computational accuracy.
- Raising ADC precision captures more of the analog signal but may be wasted if the analog computation itself is only 4-bit precise.
- **Optimal ADC precision should match the compute SNR**, not exceed it. Compute-aware SNR models show ADC precision can often be reduced by 3 bits (vs naive SQNR matching) with only 6 dB loss -- saving 40-64x in ADC energy.

### The Area Problem

- High-resolution ADCs are physically large.
- Analog CIM needs one ADC per column (or shared among a few columns).
- For a 256-column array with 8-bit ADCs, the ADC area can exceed the memory array area.
- Mythic had to design ADCs "smaller than anyone thought possible" to fit on their chip.

### Approaches to Mitigate

1. **ADC-less designs:** Quantize partial sums to 1-1.5 bits (binary/ternary), eliminating ADCs entirely. Accuracy loss: 1.9-4.7% on CIFAR-10/MNIST -- acceptable for some edge applications.
2. **Adaptive ADC precision:** Use lower precision where the signal is clean, higher where noise is high.
3. **Memristive ADC:** Use the RRAM array itself as the ADC -- achieved 89.55% CIFAR-10 at 5-bit precision with 15.1x energy improvement and 12.9x area reduction vs conventional ADCs.
4. **Partial-sum quantization:** Data-driven optimization of quantization ranges per layer.
5. **Time-domain ADC (IBM HERMES):** Current-controlled oscillator (CCO) based ADCs that are compact and can be placed on each unit-cell row. 300 ps/LSB linearized CCO-based ADCs.

---

## IR Drop and Array Scaling

### The Problem

In a resistive crossbar array, wire resistance causes voltage drops along the rows and columns. The actual voltage across a memory device differs from the applied input voltage. This error:

- **Gets worse with larger arrays** -- wire resistance becomes comparable to device ON-state resistance.
- **Is position-dependent** -- devices far from the input drivers experience more IR drop.
- **Is input-dependent** -- IR drop changes based on what other devices in the same row/column are doing.
- **Is nonlinear** -- the error is data-dependent, making it hard to calibrate.

### Impact on Accuracy

- For a typical 256x256 RRAM crossbar, IR drop can cause 5-15% output error depending on conductance states.
- For 512x512 or larger arrays, IR drop becomes a dominant source of error, potentially worse than device noise.
- This limits practical crossbar sizes to ~256x256 for resistive devices without mitigation.

### Mitigation Strategies

1. **Smaller arrays with digital accumulation between tiles.** Trade parallelism for accuracy. Most practical implementations use 128x128 or 256x256 tiles.
2. **Low-conductance programming.** Reduce total current to reduce IR drop. But this worsens SNR (less signal, same thermal noise).
3. **Hierarchical partitioning and 3D-NAND-style segmentation.**
4. **IR drop de-embedding:** Use linear network models to computationally compensate for IR drop. Fast algorithms exist but add digital overhead.
5. **Capacitor-based CIM avoids this entirely.** Charge-domain accumulation does not suffer from resistive IR drop. This is another fundamental advantage of EnCharge's approach.

---

## On-Chip Training vs Inference-Only

### The Precision Asymmetry

- **Inference:** Can tolerate 4-8 bit precision. Most neural networks maintain acceptable accuracy at INT4 or INT8.
- **Training:** Requires much higher precision for gradient computation. Standard SGD needs FP32 or at minimum FP16 for stable convergence. Gradients are often very small numbers that require high dynamic range.

### Why On-Chip Analog Training Is So Hard

1. **Backpropagation requires symmetric read/write:** Analog devices have asymmetric, nonlinear switching. The stochastic characteristics of analog devices directly conflict with the deterministic weight updates that backpropagation assumes.
2. **Gradient precision:** Weight updates during training are tiny (learning rate * gradient). Representing these precisely in analog is extremely challenging -- often sub-LSB of the device's programming precision.
3. **The auxiliary digital compute problem:** Many proposed analog training algorithms require significant digital compute for gradient accumulation (floating-point precision), limiting the actual speedup. You end up with a hybrid that may not be faster than pure digital.
4. **Endurance:** Training requires millions of weight updates. PCM endurance: ~10^8 cycles. RRAM: ~10^6-10^12 depending on technology. Flash: ~10^4-10^5 cycles. Only MRAM (>10^15) and SRAM (unlimited) have sufficient endurance for serious training.

### Current State

- On-chip analog training remains largely a research topic.
- A few demonstrations exist: IBM's Tiki-Taka algorithm, sign-backpropagation on RRAM, progressive gradient descent.
- Recent work (Nature Communications, 2024) showed "fast and robust analog in-memory DNN training" but required dedicated algorithms that differ significantly from standard training.
- **Practical implication:** For the foreseeable future, analog CIM is an inference accelerator. Models are trained digitally (possibly with noise-aware techniques) and deployed to analog hardware.

---

## Memory Technology Comparison on Precision

| Property | SRAM | Flash | RRAM | PCM | MRAM | FeCAP/Capacitor |
|---|---|---|---|---|---|---|
| **Effective compute bits** | 4-6 | 5-8 (claimed) | 3-5 | 3-4 | 1-2 (analog) | 6-8 |
| **D2D variability** | Low (mature CMOS) | Low-moderate | **High** (stochastic filament) | Moderate | Low | **Very low** (geometric) |
| **C2C variation** | Low | Low-moderate | **High** | Moderate (5-10% of G) | **Very low** (~0.3-0.5%) | Low |
| **Drift** | None (volatile) | Slow charge loss | Moderate | **Severe** (v=0.1-0.15) | None | None (if SRAM-stored) |
| **Temperature sensitivity** | Moderate | Moderate | High | **Very high** | Low | Moderate |
| **Endurance** | Unlimited | 10^4-10^5 | 10^6-10^12 | 10^8 | >10^15 | >10^11 (FeCAP) |
| **Retention** | None (volatile) | 10+ years | Years (binary), shorter analog | Hours-days (drifts) | >10 years | >10 years |
| **IR drop issue** | Moderate | Moderate | **Severe** | **Severe** | Moderate | **Minimal** (charge domain) |
| **Multi-level storage** | Via DAC | 256 levels (8-bit) | 4-16 levels | 4-16 levels | 2 levels typical | Continuous (FeCAP) |
| **Maturity** | Production | Production | Early production | Research/pilot | Production (binary) | Research |

### Key Observations

1. **No single technology wins on all dimensions.** SRAM is mature but volatile. Flash is precise but low-endurance. RRAM is dense but noisy. PCM drifts. MRAM is stable but limited to binary. Capacitors are precise but area-intensive.

2. **Capacitor/charge-domain approaches (EnCharge, IMAGINE) have the best precision profile** -- low variability, no drift, no IR drop issue, good temperature stability. The main cost is area (capacitors are larger than resistive devices).

3. **MRAM is the most reliable** for what it can do (binary/ternary), but its limited multi-level capability restricts it to low-precision applications.

4. **PCM has the worst drift problem** but IBM is making material-level progress (SiSbTe). The question is whether drift can be reduced enough for practical deployment without constant recalibration.

5. **RRAM has the worst variability** due to the fundamental stochasticity of filament formation. This may be an irreducible physics limitation. Recent work on "forming-free" and "filament-free" RRAM (e.g., trilayer bulk switching) shows promise for reducing variability, with cycle-to-cycle variation reduced by >50% using optimized pulse schemes.

6. **FeCAP (ferroelectric capacitor) is emerging** as a potentially excellent CIM device: high endurance (>10^11 read, >10^12 cycles), long retention (>10 years), ultra-low variation (~0.3% D2D, ~0.5% C2C), high on/off ratio (>10^7). Still early in development.

---

## Fundamental Physics Limits

### The Thermodynamic Floor

**Landauer's principle:** The minimum energy to erase one bit of information is kT * ln(2) ≈ 2.9 x 10^-21 J at room temperature. This is the absolute floor for any irreversible computation.

Current digital computers operate ~10^9 (1 billion) times above this limit. Analog computers face the same thermodynamic floor but reach different practical limits.

### The SNR-Precision Relationship

For an ideal analog system:
```
ENOB = (SNR_dB - 1.76) / 6.02
```

Each additional bit of precision requires 6 dB more SNR, which means 4x more signal power (at constant noise) or 4x less noise (at constant signal).

**Practical implications:**
- 4-bit precision needs SNR ≈ 26 dB
- 6-bit precision needs SNR ≈ 38 dB
- 8-bit precision needs SNR ≈ 50 dB
- 10-bit precision needs SNR ≈ 62 dB

Going from 4-bit to 8-bit precision requires ~24 dB more SNR -- that is 250x more signal-to-noise ratio. This is why 4-bit analog is common and 8-bit analog is hard.

### The kT/C Limit

For capacitor-based systems (switched-capacitor circuits, charge-domain CIM):
```
SNR_max = C * V^2 / (2kT)
```

For 8-bit precision at room temperature with a 1V signal swing, you need capacitors of at least ~0.1 pF. This sets a minimum area per compute element.

### The Energy-Precision Tradeoff in Analog

The energy cost of an analog multiply-accumulate operation scales roughly as:
```
E_MAC ∝ 2^(2*ENOB) * kT
```

This means doubling the precision quadruples the energy. An 8-bit analog MAC costs ~16x more energy than a 4-bit analog MAC. At some precision level (roughly 8-10 bits for current technology), analog loses its energy advantage over digital -- digital MAC energy scales more favorably at higher precision.

### The Theoretical Maximum

Given:
- A 256x256 crossbar array
- 1V signal swing
- Room temperature (300K)
- 100 MHz operation (10 ns per MAC)
- Well-designed capacitive readout

The theoretical maximum precision is approximately **10-12 bits** before fundamental thermal noise limits are reached. But this assumes:
- Perfect devices (no variability, no drift)
- No IR drop
- Perfect ADCs
- Zero programming noise

In practice, with real devices, 6-8 bits appears to be the realistic ceiling for single-pass analog computation. Higher precision requires multi-pass techniques (bit slicing, iterative refinement) that trade throughput for accuracy.

---

## Techniques to Boost Precision Beyond Device Limits

Several techniques allow analog CIM systems to achieve higher effective precision than the raw device precision. All trade something (usually throughput or energy) for precision.

### 1. Bit Slicing
- Decompose high-precision operands into multiple low-precision components.
- Perform low-precision analog MACs on each slice.
- Combine results digitally.
- **Cost:** N slices reduce throughput by N and increase energy proportionally.
- **Result:** Peking University achieved 24-bit fixed-point accuracy using bit slicing + iterative refinement on RRAM, but at the cost of many iterations.

### 2. Residue Number System (RNS)
- Decompose operands as modulo of coprime numbers before multiplication.
- Perform modular arithmetic in analog.
- Reconstruct results using the Chinese Remainder Theorem.
- **Result:** Achieves ≥99% of FP32 accuracy with 6-bit integer arithmetic for inference and 7-bit for training.

### 3. Multi-Phase Reads (IBM HERMES approach)
- Read each MVM result multiple times with different input phases.
- Average or combine results to reduce noise.
- IBM HERMES uses 4-phase reads in high-precision mode (at 4x throughput cost).
- Increases effective precision by ~1 bit per doubling of read phases.

### 4. Differential Conductance
- Store each weight as the difference between two conductance values (G+ - G-).
- Inherently compensates for drift (both devices drift similarly).
- Doubles the device count per weight.
- Standard practice in PCM-based CIM (IBM uses 4 PCM devices per weight).

### 5. Redundant Computation (Spatial or Temporal Averaging)
- Perform the same computation multiple times and average.
- Reduces stochastic noise by sqrt(N) for N repetitions.
- Direct trade of throughput/energy for precision.

### 6. Error Correction Codes (ECC)
- Apply error correction to the analog computation.
- Can detect and correct a limited number of errors.
- Adds digital overhead.

### 7. Digital Post-Correction
- Use digital processing units adjacent to analog tiles to correct systematic errors (IR drop, nonlinearity).
- IBM HERMES includes local digital processing per core.
- This is what enabled IBM to achieve FP32-matching BLEU scores despite only 3-4 bit MVM precision.

### The General Principle

**All precision-boosting techniques convert analog CIM's parallelism advantage into a precision advantage.** The more precision you need, the less throughput advantage analog retains over digital. At some crossover point, a fully digital implementation becomes more efficient. The question is where that crossover is -- and the answer depends on the application's precision requirements.

---

## The Bottom Line

### What Analog CIM Can Do Today (Measured Silicon, 2026)

1. **4-bit effective precision inference:** Proven. Multiple chips (IBM HERMES, NeuRRAM) demonstrate this on real workloads. Sufficient for many edge AI tasks -- image classification, keyword spotting, object detection.

2. **6-8 bit effective precision inference:** Achievable with capacitor-based approaches (EnCharge) or flash-based with calibration (Mythic). Sufficient for most CNN and smaller transformer inference.

3. **Software-matching accuracy on specific workloads:** IBM achieved BLEU scores matching FP32 on machine translation using 64 analog cores + digital correction. But this required: hardware-aware training, differential weights (4 PCM devices per weight), multi-phase reads, digital post-processing, and on-chip calibration.

### What Analog CIM Cannot Do Today

1. **High-precision computation (>8 bits) without digital assistance:** No analog CIM system achieves >8 effective bits in a single pass. Bit slicing or iterative methods can extend this but at the cost of the efficiency advantage.

2. **On-chip training:** Remains a research problem. Device asymmetry, limited endurance, and gradient precision requirements are fundamental barriers.

3. **Temperature-stable operation across automotive range:** No demonstrated solution for -40C to +125C with acceptable accuracy stability.

4. **Hardware-agnostic deployment:** Every analog CIM platform requires its own training pipeline and noise-aware toolchain. There is no equivalent of ONNX or TensorRT for analog hardware.

5. **Long-term deployment without recalibration (for PCM/RRAM):** Drift and retention issues mean periodic recalibration is required. How periodic depends on the technology and the precision requirement.

### The Verdict on Whether Analog Can Work for AI

**Analog CIM works for AI inference in the regime where 4-6 bit precision is sufficient and the application can tolerate stochastic output variation.** This covers a large fraction of edge AI workloads.

**Analog CIM does not work (yet) for applications requiring:**
- High precision (>8 bits)
- Deterministic, reproducible outputs
- Wide temperature range operation
- General-purpose deployment without hardware-specific training
- On-chip training or fine-tuning

**The trajectory matters.** EnCharge's capacitor-based approach and IBM's material improvements (SiSbTe for PCM) are pushing the boundaries. FeCAP technology shows exceptional potential (~0.3% variability, >10^12 endurance). The precision ceiling is rising, slowly but measurably.

**The fundamental question is not "can analog reach 8 bits?" but "does it need to?"** If neural network quantization research continues to show that 4-bit inference is sufficient for most workloads (as current trends suggest), then analog CIM's 4-6 bit natural precision may be exactly what the market needs -- with a 10x+ energy efficiency advantage at that precision level.

---

## Sources

### Key Papers and Publications

- [Achieving high precision in analog in-memory computing systems, npj Unconventional Computing, Jan 2026](https://www.nature.com/articles/s44335-025-00044-2) - Comprehensive review of precision enhancement techniques (bit slicing, RNS, ECC)
- [A 64-core mixed-signal in-memory compute chip based on phase-change memory, Nature Electronics, 2023](https://www.nature.com/articles/s41928-023-01010-1) - IBM HERMES chip, 3-4 bit effective MVM precision
- [A compute-in-memory chip based on resistive random-access memory, Nature, 2022](https://www.nature.com/articles/s41586-022-04992-8) - NeuRRAM, 4-bit equivalent accuracy across diverse AI tasks
- [Hardware-aware training for large-scale and diverse deep learning inference workloads using in-memory computing-based accelerators, Nature Communications, 2023](https://www.nature.com/articles/s41467-023-40770-4) - IBM's HWA training achieving iso-accuracy on 5/11 workloads
- [Fast and robust analog in-memory deep neural network training, Nature Communications, 2024](https://www.nature.com/articles/s41467-024-51221-z) - On-chip analog training challenges and algorithms
- [Phase-Change Memory for In-Memory Computing, Chemical Reviews, 2024](https://pubs.acs.org/doi/10.1021/acs.chemrev.4c00670) - Comprehensive PCM CIM review
- [Collective Structural Relaxation in Phase-Change Memory Devices, Adv. Electronic Materials, 2018](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aelm.201700627) - PCM drift physics and quantitative model
- [State-Independent Low Resistance Drift SiSbTe Phase Change Memory, VLSI Technology and Circuits, 2024](https://research.ibm.com/publications/state-independent-low-resistance-drift-sisbte-phase-change-memory-for-analog-in-memory-computing-applications) - IBM's improved PCM material (drift coefficient ~0.04)
- [Temperature sensitivity of analog in-memory computing using phase-change memory, IEDM 2021](https://ieeexplore.ieee.org/document/9720519/) - IBM PCM temperature study
- [Toward Capacitive In-Memory Computing, Advanced Intelligent Discovery, 2025](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aidi.202500143) - Capacitor CIM advantages over resistive approaches
- [Memristor-based adaptive analog-to-digital conversion for efficient and accurate compute-in-memory, Nature Communications, 2025](https://www.nature.com/articles/s41467-025-65233-w) - Adaptive memristor ADC, 5-bit precision, 15x energy improvement
- [Causes and consequences of the stochastic aspect of filamentary RRAM, Microelectronic Engineering, 2015](https://www.sciencedirect.com/science/article/abs/pii/S0167931715002348) - RRAM fundamental variability
- [Adapting magnetoresistive memory devices for accurate and on-chip-training-free in-memory computing, Science Advances, 2024](https://www.science.org/doi/10.1126/sciadv.adp3710) - MRAM ultra-low variation for CIM
- [Ferroelectric capacitive memories: devices, arrays, and applications, Nano Convergence, 2024](https://nanoconvergencejournal.springeropen.com/articles/10.1186/s40580-024-00463-0) - FeCAP memory for CIM

### Industry Sources

- [EnCharge's Analog AI Chip Promises Low-Power and Precision, IEEE Spectrum](https://spectrum.ieee.org/analog-ai-chip-architecture) - Capacitor CIM precision advantages
- [Mythic AI: How An Analog Processor Could Revolutionize Edge AI, HPE Pathfinder](https://pathfinder.hpe.com/news/mythic-how-an-analog-processor-could-revolutionize-edge-ai) - Flash CIM 8-bit weight storage
- [Meet Mythic AI's Soon-to-be-Legendary Analog AI, EE Journal](https://www.eejournal.com/article/meet-mythic-ais-soon-to-be-legendary-analog-ai/) - M1076 precision details
- [IBM Analog Hardware Acceleration Kit (aihwkit) documentation](https://aihwkit.readthedocs.io/en/latest/hwa_training.html) - HWA training framework
- [IBM aihwkit PCM inference model](https://aihwkit.readthedocs.io/en/latest/pcm_inference.html) - PCM noise and drift quantitative models
- [NeuroSim V1.5: Benchmarking Compute-in-Memory Accelerators, arXiv 2025](https://arxiv.org/html/2505.02314v1) - CIM non-ideality modeling
- [IMAGINE: An 8-to-1b 22nm FD-SOI Compute-In-Memory CNN Accelerator, arXiv 2024](https://arxiv.org/html/2412.19750) - EnCharge/charge-domain CIM macro
- [Investigating Energy Bounds of Analog Compute-in-Memory, arXiv 2026](https://arxiv.org/html/2602.08081) - ADC energy analysis and bounds
