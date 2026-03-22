# The History of Analog Computing for AI: Why It Failed Before and What's Different Now

> "Those who cannot remember the past are condemned to repeat it." — George Santayana
>
> The analog AI chip industry has attempted to replace digital computing for neural networks at least three times since 1989. Each wave followed the same pattern: a genuine physics advantage, early excitement, massive investment, and then collapse when digital scaling outpaced analog's efficiency gains. Understanding this history is essential context for evaluating the 2020s wave.

---

## The Prehistory: Analog Computing's First Life (1940s-1970s)

Before there were neural network chips, there were analog computers. The distinction matters because today's "analog AI" inherits both the promise and the baggage.

**Key facts:**
- Analog computers dominated scientific computation from the 1940s through the 1960s. They solved differential equations, simulated flight dynamics, and controlled industrial processes.
- RCA produced the first reliable fully electronic analog computer in the early 1950s.
- By the 1970s, analog computers were effectively dead for general-purpose computation. Digital computers had become faster, more accurate, cheaper, and — critically — programmable.

**Why analog lost the first time:**
1. **Precision.** Analog circuits achieved roughly 0.01-0.1% accuracy (3-4 significant digits). Digital circuits could achieve arbitrary precision.
2. **Programmability.** Rewiring an analog computer to solve a different problem could take days. Digital computers ran software.
3. **Noise.** Analog signals degrade with every operation. Digital signals regenerate perfectly.
4. **Scaling.** Moore's Law made digital exponentially better every two years. Analog had no equivalent scaling law.

These same four problems — precision, programmability, noise, scaling — would haunt every subsequent attempt to bring analog back.

---

## The First Wave: Analog Neural Network Chips (1982-1997)

### The Intellectual Foundation

The first wave was born from a convergence of three developments in the early 1980s:

**1. Hopfield Networks (1982)**
John Hopfield at Caltech published his landmark paper applying statistical mechanics to neural networks. His "Hopfield network" was an associative memory that could be naturally implemented as an analog circuit — neurons were amplifiers, synapses were resistors. The continuous Hopfield net could be directly realized as an electronic circuit using non-linear amplifiers and resistive interconnects. This was the theoretical spark: neural computation mapped naturally onto analog hardware.

**2. Backpropagation Rediscovered (1986)**
Rumelhart, Hinton, and Williams popularized backpropagation for training multi-layer neural networks. Suddenly there was a practical algorithm that could train networks to do useful things — but it was computationally expensive on the digital hardware of the era. Analog, with its natural parallelism, seemed like an obvious accelerator.

**3. Carver Mead's Vision (1986-1989)**
Carver Mead, already famous for co-authoring the foundational VLSI design textbook (1978), became interested in treating MOS transistors as analog devices rather than digital switches. He noticed that transistors operated in subthreshold (weak inversion) mode behaved remarkably like biological ion channels in neurons — both followed exponential current-voltage relationships.

In 1986, Mead and Federico Faggin (inventor of the first commercial microprocessor at Intel, then the Z80 at Zilog) founded **Synaptics Inc.** to commercialize analog neural network circuits for vision and speech recognition.

In 1989, Mead published *Analog VLSI and Neural Systems*, the first book on what he called **neuromorphic engineering** — building silicon circuits that mimicked neural architectures. He coined the term "neuromorphic" and launched an entirely new field.

Also in 1986, Caltech established the **Computation and Neural Systems (CNS)** program with John Hopfield as its first chair. During the decade spanning 1985-1995, Mead and his students at Caltech's Physics of Computation Lab pioneered:
- First integrated silicon retinas
- Silicon cochleas
- Silicon neurons and synapses
- Non-volatile floating gate synaptic memories
- Central pattern generators
- First address-event representation (AER) inter-chip communication

**Misha Mahowald** (1963-1996), one of Mead's most brilliant PhD students, created the silicon retina — an analog VLSI circuit that replicated retinal processing using analog circuits to mimic rod cells, cone cells, and other excitable cells. Her work earned articles in Scientific American and Nature, and she is credited with starting the field of neuromorphic engineering. Her silicon retina's descendants are now commercial products at companies like iniVation and Prophesee (event cameras). Tragically, Mahowald died by suicide at age 33, and the field's highest honor — the Mead-Mahowald Prize — bears her name.

### The Commercial Chips

Between 1989 and 1995, multiple companies built analog and hybrid neural network chips:

#### Intel ETANN (80170NX) — 1989
- **The first commercial analog neural network chip**
- Announced at the International Joint Conference on Neural Networks (IJCNN) in 1989
- 64 analog neurons, 10,240 analog synapses
- 1.0 um CHMOS-III nonvolatile memory process
- Floating-gate technology (analog weights stored as charge)
- 2,000 MCPS (million connections per second)
- Intel provided a training system (iNNTS) and PC software
- Up to 8 ETANNs could be wired together
- **Applications:** Fermilab used it for particle physics triggers; military explored it for missile seekers
- **What happened:** Neural networks fell out of favor by the mid-1990s, and Intel abandoned the product line. At the time, "neural networks were pretty much a dead end in terms of applications, as there was neither the computing power nor the understanding to deploy them at scale" (Computer History Museum).

#### AT&T Bell Labs ANNA Chip — 1991
- **Mixed analog/digital neural network processor**
- Designed by Hans Peter Graf, Eduard Sackinger, Bernhard Boser, Jane Bromley, Yann LeCun, and Lawrence Jackel
- Over 2,000 multiplications and additions simultaneously
- 6-bit weight precision, 3-bit neuron state precision
- Analog processing internally, digital I/O for system integration
- Specialized for convolutional network topologies
- **Applications:** Handwritten character recognition at 1,000 characters/second — "50 to 500x speed advantage over conventional hardware" (1992 paper). Used for reading address blocks on mail, rail car ID numbers, and discriminating handwritten vs. machine-printed text.
- **What happened:** LeCun's convolutional networks on the ANNA chip were deployed by AT&T for check reading. By 1998, this technology was reading more than 10% of all checks in the United States. But Bell Labs' neural network research group was dispersed during the AT&T breakup (1996), and the work migrated to purely digital implementations.

This is a crucial data point: **the most commercially successful analog neural network application — AT&T check reading — eventually moved to digital hardware**, because digital processors became fast enough to run the same algorithms in software.

#### Other Notable 1990s Neurochips

| Chip/System | Organization | Type | Notes |
|---|---|---|---|
| CNAPS (N6400) | Adaptive Solutions | Digital SIMD | 64 processing elements per chip, multiple chips cascadable |
| SYNAPSE-1 (MA-16) | Siemens | Digital | 4x4 matrix operations, 16-bit fixed point, systolic array |
| NETSIM | Texas Instruments / Cambridge | Digital | UK-US collaboration |
| SNAP | HNC (now FICO) | Hybrid | Used for fraud detection |
| Ni1000 | Intel / Nestor | Digital | Intel's second neural chip — significantly, they went digital |
| Various | Philips, Hughes, IBM Japan | Mixed | Research prototypes |

**Key observation:** Even within the first wave, there was a clear trend from analog toward digital. Intel's second neural chip (Ni1000, with Nestor) was all-digital. The most successful systems (CNAPS, SYNAPSE) were digital. The analog advantage in density was real but couldn't compensate for the precision, noise, and calibration problems.

### Synaptics: The Pivot That Worked

Synaptics, founded by Mead and Faggin in 1986 to build analog neural network chips for pattern recognition, spent 12 years (1986-1998) on R&D including the silicon retina. But the company's breakthrough product was not a neural network — it was the **laptop touchpad** (1992), which used analog sensing technology derived from their neural network work.

This is perhaps the most telling lesson from the first wave: **the most successful company to emerge from 1980s analog neural network research succeeded by pivoting away from neural networks entirely.** Synaptics IPO'd in 2001 and is now a $3B+ company — but it sells human interface devices, not AI chips.

---

## Why Analog Neural Networks Failed in the 1990s

The collapse of analog neural network hardware in the 1990s had both technical and ecosystem causes:

### Technical Causes

**1. Precision was inadequate for the algorithms of the era**
- Analog chips achieved 3-8 effective bits of precision
- The neural network algorithms of the 1990s (pre-deep learning) were small networks that needed every bit of precision to converge
- Unlike modern deep networks with millions of redundant parameters, 1990s networks with hundreds or thousands of weights couldn't tolerate quantization noise

**2. Calibration and yield were nightmares**
- Analog circuit performance varied chip-to-chip and over temperature
- Each chip needed individual calibration
- Manufacturing yield was poor — analog mismatch between nominally identical transistors degraded network accuracy
- No algorithmic techniques existed to compensate for hardware variation (noise-aware training wasn't invented until the 2010s)

**3. ADC/DAC overhead was already a known problem**
- Converting between analog compute domains and digital I/O consumed significant power
- This collapsed the theoretical efficiency advantage
- The problem was understood but unsolved — and remains the central challenge today (see [adc-dac-bottleneck.md](adc-dac-bottleneck.md))

**4. Analog didn't scale with Moore's Law**
- Digital circuits doubled in performance every ~2 years
- Analog circuits gained little from process shrinks — in fact, smaller transistors had worse analog properties (more mismatch, less voltage headroom)
- "The artisanal style of circuit design for analog systems ultimately struggled to keep pace with the rapid advances in synthesizable digital electronics"
- A digital neural network implementation that was 10x slower than analog in 1990 would be faster than analog by 1996, with no hardware redesign needed

### Ecosystem Causes

**5. The AI Winter killed the market**
- The second AI winter (1987-2000) devastated funding for all AI research
- Over 300 AI companies shut down, went bankrupt, or were acquired by the end of 1993
- The specialized AI hardware market collapsed suddenly in 1987 when desktop PCs became more powerful than expensive Lisp machines
- "Since neural networks had fallen out of favor in artificial intelligence circles by the 1990s, there was little financial incentive to invest in a technology that could be upstaged by the next, twice-as-efficient generation of computers a mere two years later"

**6. No software ecosystem**
- Each analog chip required custom programming
- No equivalent of compilers, debuggers, or standard libraries
- When digital GPPs became fast enough, researchers preferred running networks in MATLAB or C on standard hardware
- The software portability of digital was an overwhelming advantage

**7. The algorithms didn't need specialized hardware**
- 1990s neural networks were small enough to run on general-purpose CPUs
- Support vector machines and other "shallow" methods outperformed neural networks for most practical tasks
- There was no computational demand that justified custom neural hardware
- This changed only after 2012 (AlexNet), when deep networks became too large for CPUs

### The Fundamental Pattern

**Analog offered a constant-factor advantage (maybe 10-100x for a given task at a given moment). Digital offered exponential improvement over time (Moore's Law). Exponential always wins.**

This is the single most important lesson from the first wave.

---

## The Quiet Period: 1997-2012

For roughly 15 years, analog neural network hardware was a backwater. A few developments kept the thread alive:

**Academic neuromorphic research continued:**
- Giacomo Indiveri (ETH Zurich), Kwabena Boahen (Stanford), and other Mead students maintained active labs
- The Telluride Neuromorphic Cognition Engineering Workshop (founded 1994) continued annually
- The Institute of Neuroinformatics in Zurich became a center for neuromorphic engineering

**The memristor revival (2008):**
- Leon Chua had theoretically predicted the memristor in 1971 as a fourth fundamental circuit element
- In 2008, HP Labs (Strukov, Snider, Stewart, Williams) published in Nature linking thin-film TiO2 resistance switching to Chua's memristor concept
- This ignited interest in resistive memory devices for analog computing
- The memristor provided a potential path to dense, non-volatile analog synaptic storage
- However, the initial excitement was overblown — memristors turned out to have severe variability, endurance, and yield problems that would take another decade+ to partially address (see [rram-memristor-chips.md](rram-memristor-chips.md))

**DARPA SyNAPSE program (2008-2014):**
- DARPA committed over $100M to neuromorphic computing
- IBM received ~$42M, HRL received ~$34M
- Produced IBM's TrueNorth chip (2014): 5.4B transistors, 4096 cores, 1M neurons, 256M synapses, 28nm CMOS
- TrueNorth was digital, not analog — a significant signal that even DARPA-funded neuromorphic research moved away from analog
- TrueNorth demonstrated impressive energy efficiency (400 GSOPS/W) but had limited practical applications

**Intel's Loihi program (2017):**
- Intel Research developed Loihi, a neuromorphic research chip
- Also digital, not analog
- Now in its second generation (Loihi 2) with the massive Hala Point system (1.15 billion neurons)
- 8+ years of development, zero commercial revenue (see [intel-loihi.md](intel-loihi.md))

The quiet period confirmed a pattern: **serious, well-funded neuromorphic programs (DARPA SyNAPSE, Intel Loihi) chose digital implementations**, suggesting that even believers in brain-inspired computing found analog's practical challenges too severe.

---

## The Second Wave: Analog In-Memory Computing (2012-2020)

### What Changed

Several developments converged to make analog computing for AI seem viable again:

**1. Deep learning created a compute crisis (2012+)**
- AlexNet (2012) showed that large neural networks trained on GPUs could dramatically outperform all other approaches
- Model sizes exploded: from millions of parameters to billions
- GPU power consumption became a major concern (300W+ per chip)
- The compute demand for AI was growing faster than Moore's Law could provide — the historical "exponential beats constant factor" argument was weakening

**2. Moore's Law was slowing (2015+)**
- Dennard scaling ended around 2006 — smaller transistors no longer consumed less power
- Moore's Law itself slowed to ~2-3 year doubling
- Each new process node became exponentially more expensive ($100M+ for 7nm masks, $300M+ for 3nm)
- This narrowed the gap: digital was no longer getting exponentially cheaper every 2 years

**3. Deep learning was tolerant of low precision (2015+)**
- Researchers discovered that neural networks with millions of parameters were remarkably robust to quantization
- INT8 inference worked nearly as well as FP32 for most tasks (NVIDIA's TensorRT, 2017)
- 4-bit and even binary networks showed surprising accuracy (DoReFa-Net 2016, XNOR-Net 2016)
- This was transformative for analog: **the 3-8 bit precision that killed analog in the 1990s was now sufficient for the dominant AI workload**
- In the 1990s, small networks needed high precision. In the 2020s, huge networks tolerated low precision.

**4. New memory devices matured (2016+)**
- Resistive RAM (RRAM/ReRAM) improved dramatically in reliability and uniformity
- Phase-change memory (PCM) moved from lab to foundry (IBM, Samsung)
- Flash memory became dense and cheap enough for analog weight storage
- Foundry-compatible processes meant startups could fabricate analog AI chips without captive fabs

**5. In-memory computing theory developed (2016+)**
- The ISAAC architecture (2016) showed how crossbar arrays could accelerate neural network inference
- Key papers demonstrated analog matrix-vector multiplication using Ohm's law and Kirchhoff's current law
- The compute-in-memory paradigm avoided the von Neumann bottleneck (data movement between memory and processor)
- Academic groups at Princeton, Michigan, Stanford, and Tsinghua published foundational results

### The Second-Wave Startups

| Company | Founded | Technology | Funding | Status (March 2026) |
|---|---|---|---|---|
| **Mythic AI** | 2012 | Flash-based analog CIM | $300M+ | Recovered from 2022 near-death. $125M in Dec 2025. ~$6.4M revenue. |
| **Rain Neuromorphics** | 2017 | Memristor-based analog | ~$40M + OpenAI $51M LOI | Sam Altman-backed. No shipping product. |
| **Syntiant** | 2017 | Started analog, pivoted digital | $100M+ | 10M+ chips shipped — **but abandoned analog** |
| **Aspinity** | 2015 | Pure analog preprocessing | ~$20M | AML200 shipping. <100 uW. Niche but real. |
| **EnCharge AI** | 2022 | Capacitor-based analog CIM | $144M | Most promising. Princeton origins. No independent benchmarks. |
| **POLYN Technology** | 2019 | Neuromorphic analog | Modest | First silicon 2025. 34 uW voice detection. |
| **Blumind** | 2020 | Analog edge AI | Early | Keyword recognition chip, 2025 mass production target. |

**The Syntiant pivot is the most important data point of the second wave.** Syntiant started with analog neural network technology in 2017, then abandoned analog for a digital architecture — and became the most commercially successful company in the group (10M+ chips shipped). Their VP of engineering stated in 2018 that "a trio of startups went after a version of flash-based analog AI. Syntiant eventually abandoned the analog approach for a digital scheme."

---

## The Third Wave: The Current Moment (2020-2026)

### What's Genuinely Different This Time

**1. The energy crisis is real and urgent**
- Training GPT-4 consumed an estimated 50 GWh
- Data center power consumption for AI is projected to exceed 100 TWh/year by 2027
- This creates genuine economic pressure that didn't exist in the 1990s or 2010s
- Even a 2-5x efficiency gain has multi-billion dollar value at scale

**2. Noise-aware training exists**
- Modern algorithms can be trained to compensate for analog hardware non-idealities
- Hardware-in-the-loop training maps network weights to specific device characteristics
- This partially addresses the calibration nightmare that killed the first wave
- But it creates tight hardware-software coupling that limits portability

**3. Foundry processes are mature**
- TSMC, Samsung, and GlobalFoundries offer analog-compatible process options
- Startups don't need their own fabs
- Standard CMOS can support capacitor-based or flash-based CIM without exotic materials

**4. The precision argument flipped**
- In the 1990s: small networks needed high precision, and analog couldn't provide it
- In the 2020s: large networks tolerate low precision, and analog is naturally low-precision
- 4-bit and 8-bit quantized inference is mainstream
- Analog's 3-8 effective bits match the precision that modern networks need

**5. The workload is right**
- Matrix-vector multiplication (the core of neural network inference) maps perfectly onto analog crossbar arrays
- This is a narrow, well-defined operation — unlike the general-purpose computation that analog lost to digital in the 1970s
- Inference is more tolerant of noise than training

### What Hasn't Changed (The Persistent Problems)

**1. ADC/DAC overhead still dominates**
- Consumes 40-85% of system power in every measured analog CIM chip
- This single factor collapses "100x better than GPU" claims to 2-10x reality
- The problem was known in 1991 and remains unsolved in 2026

**2. Precision is still a ceiling**
- Analog achieves 3-6 effective bits (PCM/RRAM) to 6-8 bits (capacitor)
- Each additional bit costs 4x power
- Digital CIM achieves 8-16 deterministic bits
- Analog "4-bit" is stochastic; digital INT4 is deterministic

**3. The software ecosystem is still missing**
- No analog equivalent of CUDA, TensorRT, or PyTorch hardware backends
- Every analog chip requires custom mapping, calibration, and deployment tools
- Mythic nearly died partly from underinvesting in software
- This was the #1 ecosystem problem in 1991 and remains so in 2026

**4. Digital keeps improving**
- Digital CIM (d-Matrix, Axelera) achieves comparable efficiency with deterministic accuracy
- ISSCC 2025's CIM session had zero analog papers — all digital
- Digital SRAM CIM hit 192.3 TFLOPS/W at ISSCC 2025
- 4-bit digital quantization delivers most of analog's efficiency benefit with none of the noise

**5. Analog doesn't scale with process shrinks**
- Moving from 28nm to 7nm improves digital CIM dramatically
- Analog CIM gains little — analog transistor properties often worsen at smaller nodes
- The same dynamic that killed analog in the 1990s (digital scales, analog doesn't) is still operative

---

## The Hype Cycle Pattern

The analog AI chip space has followed a remarkably consistent pattern across all three waves:

### Wave 1 (1986-1997): Analog Neural Networks
1. **Trigger:** Hopfield networks, backpropagation, Mead's vision
2. **Peak hype:** ~1989-1991 (Intel ETANN, ANNA chip, DARPA funding)
3. **Trough:** 1993-1997 (AI winter, over 300 AI companies dead)
4. **Outcome:** Zero surviving analog neural network chip companies. Synaptics pivoted to touchpads. AT&T moved check reading to digital.

### Wave 2 (2012-2022): Analog In-Memory Computing
1. **Trigger:** Deep learning compute crisis, memristor revival, Moore's Law slowdown
2. **Peak hype:** ~2018-2020 (Mythic $85M raise, Rain/OpenAI $51M LOI)
3. **Trough:** 2022-2023 (Mythic near-bankruptcy, Rain no product, Syntiant abandons analog)
4. **Outcome:** No analog chip company achieved significant revenue. Syntiant succeeded by going digital.

### Wave 3 (2022-present): Analog CIM for Edge + Efficiency
1. **Trigger:** LLM energy crisis, DARPA OPTIMA ($78M), Unconventional AI ($475M seed)
2. **Peak hype:** ~2025-2026 (we are here)
3. **Trough:** ???
4. **Outcome:** TBD

The pattern suggests we are currently near or at peak hype for the third wave. The $475M Unconventional AI seed round (late 2025, $4.5B valuation, no product) has all the hallmarks of peak-cycle exuberance.

---

## Lessons From History for Today's Analog AI Startups

### Lesson 1: The 100x Claim Is Always Wrong

Every generation of analog AI chips has claimed 100-1000x efficiency over digital. Every independent measurement has shown 2-14x at the system level. The gap is explained by ADC/DAC overhead, precision degradation, calibration costs, and comparison to outdated digital baselines.

- **1991:** ANNA chip claimed "50-500x" over conventional hardware
- **2019:** Mythic claimed "10x efficiency, 100x compute density"
- **2024:** Various startups claim "100x over GPU"
- **Reality across all eras:** 2-14x at system level, when measured honestly

### Lesson 2: Digital Is the Real Competition, Not GPUs

Analog startups benchmark against NVIDIA GPUs because the comparison looks favorable. But the real competition is digital CIM and quantized digital accelerators, which are closing the gap without analog's noise, calibration, and software problems.

- In the 1990s, digital neural chips (CNAPS, SYNAPSE) outcompeted analog neural chips
- In 2025, digital CIM (d-Matrix at 38 TOPS/W, ISSCC 2025 at 192 TFLOPS/W) outcompetes analog CIM
- The pattern is consistent: digital implementations of the same idea win on practicality

### Lesson 3: The Software Ecosystem Is Not Optional

Every failed analog AI chip company underinvested in software.

- Intel ETANN had a basic PC training system but no deployment ecosystem
- Mythic nearly died partly because it built great silicon but inadequate software tools
- No analog chip company has anything approaching CUDA

Budget at least 40-50% of engineering resources for software. This is the lesson the field refuses to learn.

### Lesson 4: Pivoting Away From Analog May Be the Best Outcome

- Synaptics (1986): pivoted from analog neural networks to touchpads. Now worth $3B+.
- Syntiant (2017): pivoted from analog to digital neural processing. 10M+ chips shipped.
- Intel (1989-1993): abandoned ETANN, pivoted to digital Ni1000, then abandoned neural chips entirely.

The companies that recognized analog's limitations and pivoted were more successful than those that persisted.

### Lesson 5: The Niche Where Analog Wins Is Smaller Than the Vision

Every wave of analog AI promises to challenge digital across all of computing. Every wave ends with analog succeeding only in a narrow niche:

- **1990s:** Analog's real contribution was analog signal processing (touchpads, sensors), not neural computation.
- **2020s:** Analog's real value is in always-on edge sensing (<1 mW) — exactly where Aspinity and POLYN operate.
- The niche is real but small. The $251M analog CIM market vs. $200B+ total AI chip market tells the story.

### Lesson 6: The Exponential Problem Persists

In the 1990s, Moore's Law (exponential digital improvement) crushed analog's constant-factor advantage. Today, Moore's Law has slowed — but digital CIM, quantization, and architectural innovation continue to improve digital efficiency at a faster rate than analog CIM improves.

- Digital SRAM CIM went from ~50 TFLOPS/W (2023) to 192 TFLOPS/W (2025)
- Analog CIM system-level efficiency has barely moved from ~8-24 TOPS/W
- The gap is widening, not narrowing

### Lesson 7: Follow the Conference Papers

- ISSCC 2025 CIM session: **zero analog papers, all digital**
- The academic community — which has no commercial bias — is voting with its submissions
- When the most prestigious circuit design conference stops publishing analog CIM, it's a signal

---

## Timeline Summary

| Year | Event | Significance |
|---|---|---|
| 1971 | Leon Chua predicts the memristor | Theoretical foundation for resistive analog memory |
| 1982 | Hopfield network published | Neural computation maps to analog circuits |
| 1986 | Backpropagation popularized | Trainable neural networks create demand for acceleration |
| 1986 | Mead & Faggin found Synaptics | First analog neural network startup |
| 1986 | Caltech CNS program established | Academic center for neuromorphic engineering |
| 1989 | Intel ETANN announced | First commercial analog neural network chip |
| 1989 | Mead publishes *Analog VLSI and Neural Systems* | The field's foundational text |
| 1991 | AT&T Bell Labs ANNA chip | Most successful analog neural chip application (check reading) |
| 1992 | Synaptics releases first touchpad | The pivot that saved the company |
| ~1993 | AI winter kills neural network hardware market | 300+ AI companies die |
| 1996 | Misha Mahowald dies | Tragic loss of neuromorphic pioneer |
| 1996 | AT&T breakup disperses Bell Labs neural network group | End of the most productive analog neural research lab |
| 2008 | HP Labs demonstrates memristor | Reignites interest in analog resistive memory |
| 2008 | DARPA SyNAPSE program launches | $100M+ for neuromorphic computing (produces digital TrueNorth) |
| 2012 | AlexNet / deep learning revolution | Creates the compute demand that justifies specialized hardware |
| 2012 | Mythic founded | First major second-wave analog AI startup |
| 2014 | IBM TrueNorth chip | Neuromorphic success, but digital — not analog |
| 2016 | ISAAC crossbar architecture paper | Academic foundation for in-memory computing |
| 2017 | Rain Neuromorphics founded | Sam Altman backing for memristor AI |
| 2017 | Syntiant founded (starts analog) | Will later abandon analog for digital |
| 2018 | Syntiant abandons analog for digital | The signal nobody wanted to hear |
| 2022 | Mythic nearly goes bankrupt | Runs out of money before reaching revenue |
| 2022 | EnCharge AI founded | Most promising third-wave analog startup |
| 2023 | IBM HERMES analog chip published | 12.4 TOPS/W, first transformer on analog silicon (7.1M params) |
| 2025 | ISSCC CIM session: zero analog papers | Academic community votes digital |
| 2025 | Unconventional AI raises $475M seed | Peak third-wave hype signal |
| 2025 | Mythic raises $125M, reports $6.4M revenue | First significant analog CIM revenue |

---

## The Honest Assessment

**Is this time different?** Partially. The energy crisis is real. Low-precision tolerance is a genuine shift. But the core technical problems (ADC/DAC overhead, noise, calibration, software) are the same problems that defeated analog in 1993. They have been partially mitigated, not solved.

**Is analog AI a bubble?** The investment-to-revenue ratio (~$1.5-2B invested, ~$8M revenue) is consistent with bubble dynamics. The Unconventional AI $475M seed at $4.5B valuation with no product echoes the most speculative moments of the dot-com era.

**Will analog computing challenge digital for AI?** In the narrow niche of always-on edge sensing (<1 mW), yes — it already does, and the physics advantage is structural. For moderate edge inference (1-10W), analog CIM offers a real but modest (2-7x) efficiency advantage that digital CIM is rapidly closing. For datacenter-scale AI, no — digital solutions are already more practical and improving faster.

**The most likely outcome for the current wave mirrors history:** a few niche analog products succeed in ultra-low-power edge applications, the "100x better than GPU" datacenter vision fails to materialize, and the most commercially successful companies either pivot to digital or find sustainable niches far smaller than their investors envisioned.

---

## Sources

- [WikiChip: Intel ETANN](https://en.wikichip.org/wiki/intel/etann)
- [Computer History Museum: Neural Network Chip](https://computerhistory.org/blog/neural-network-chip-joins-the-collection/)
- [The Chip Letter: John C. Dvorak on Intel's First Neural Network Chip](https://thechipletter.substack.com/p/john-c-dvorak-on-intels-first-neural)
- [Cambridge: Bell Labs and the 'neural' network, 1986-1996](https://www.cambridge.org/core/journals/bjhs-themes/article/bell-labs-and-the-neural-network-19861996/C2A8100FB79523DE3D3A0435A2300128)
- [SIGARCH: Neurochips from the 90s](https://www.sigarch.org/neurochips-from-the-90s/)
- [Caltech: Carver Mead Lifetime Contribution Award](https://www.caltech.edu/about/news/carver-mead-earns-lifetime-contribution-award-for-neuromorphic-engineering)
- [Caltech Magazine: The Roots of Neural Networks](https://magazine.caltech.edu/post/ai-machine-learning-history)
- [Wikipedia: Carver Mead](https://en.wikipedia.org/wiki/Carver_Mead)
- [Wikipedia: Misha Mahowald](https://en.wikipedia.org/wiki/Misha_Mahowald)
- [MIT Press: Neuromorphic Engineering — In Memory of Misha Mahowald](https://direct.mit.edu/neco/article/35/3/343/113812/Neuromorphic-Engineering-In-Memory-of-Misha)
- [Synaptics: Machine Learning Pioneers](https://www.synaptics.com/company/blog/machine-learning-pioneers)
- [Wikipedia: Computation and Neural Systems](https://en.wikipedia.org/wiki/Computation_and_Neural_Systems)
- [Wikipedia: AI Winter](https://en.wikipedia.org/wiki/AI_winter)
- [Wikipedia: Memristor](https://en.wikipedia.org/wiki/Memristor)
- [HP Labs: Engineering Memristor (2008)](https://www.hpl.hp.com/news/2008/apr-jun/engineering_memristor.html)
- [Wikipedia: SyNAPSE](https://en.wikipedia.org/wiki/SyNAPSE)
- [IEEE Spectrum: How IBM Got Brainlike Efficiency From TrueNorth](https://spectrum.ieee.org/how-ibm-got-brainlike-efficiency-from-the-truenorth-chip)
- [PMC: Neuromorphic engineering — Artificial brains for artificial intelligence](https://pmc.ncbi.nlm.nih.gov/articles/PMC11668493/)
- [Semi Engineering: Developers Turn to Analog for Neural Nets](https://semiengineering.com/developers-turn-to-analog-for-neural-nets/)
- [Semi Engineering: Can Analog Make a Comeback?](https://semiengineering.com/can-analog-make-a-comeback/)
- [Frontiers: Neuromorphic artificial intelligence systems](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.959626/full)
- [IEEE: Application of the ANNA Neural Network Chip](https://ieeexplore.ieee.org/document/129422/)
- [Fermilab: Study of the Intel ETANN](https://lss.fnal.gov/archive/test-tm/1000/fermilab-tm-1798.pdf)
- [The Register: Mythic runs out of money (2022)](https://www.theregister.com/2022/11/09/mythic_analog_ai_chips/)
- [TechCrunch: Mythic rises from the ashes (2023)](https://techcrunch.com/2023/03/09/ai-chip-startup-mythic-rises-from-the-ashes-with-13m-new-ceo/)
- [Rain AI: About](https://rain.ai/about)
- [Yann LeCun: ACM Turing Award](https://amturing.acm.org/award_winners/lecun_6017366.cfm)
