# Practitioner Opinions on Analog AI Chips

What do chip designers, ML engineers, and semiconductor veterans actually think about analog compute-in-memory (CIM)? Not press releases — real opinions from people who build, deploy, and evaluate these systems.

**Bottom line: The engineering community is significantly more skeptical than the VC community. Practitioners see analog CIM as a narrow niche tool, not a GPU replacement. The recurring theme: "the physics works, but the system doesn't."**

---

## 1. The Skeptics: Chip Designers Who Don't Buy It

### The "Never Seen the Light of Day" Argument

The most devastating critique comes from senior chip architects at established semiconductor companies. A CTO at Alphawave Semi stated bluntly in a Semiconductor Engineering interview:

> "Practically speaking, none of these in-memory compute concepts have come to life... hundreds of millions of dollars poured into solutions that have never seen the light of day."

The core of this argument: building non-digital compute in memory requires a separate chip with separate technology, creating what he calls "a very hard partitioning of the algorithm with strong limitations." His conclusion:

> "Pure in-memory computing in SRAM with something different, esoteric and partitioned? That's never going to happen."

He also pointed out that even if you deployed analog CIM for convolutions, evolving model architectures make it obsolete:

> "You'd never be able to map modern vision transformers to it because of the amount of data transfer needed back and forth between the different chip types."

**Source:** [The Uncertain Future of In-Memory Compute](https://semiengineering.com/the-uncertain-future-of-in-memory-compute/), Semiconductor Engineering, Jan 2024

### The "IMC Isn't Even on the Radar" Problem

In another Semiconductor Engineering roundtable, an industry observer noted:

> "IMC isn't even on the radar for most designers. We don't see it at our customers' sites."

This matters because it reflects the gap between academic demonstrations and commercial design flows. Engineers designing real products at real companies are not reaching for analog CIM.

**Source:** [Is In-Memory Compute Still Alive?](https://semiengineering.com/is-in-memory-compute-still-alive/), Semiconductor Engineering, Dec 2024

### The Precision Problem — From Practitioners

Multiple engineers point to effective bit precision as the fundamental deal-breaker:

> "I have not heard of anything getting above, say, four-bit effective accuracy."

In a world where digital INT4 quantization is deterministic, well-tooled, and runs on standard hardware, analog's stochastic 4-bit equivalent is a hard sell. The precision floor is set by device physics, not by engineering effort.

### The Aging and Drift Problem

Customer-facing engineers report that device reliability concerns are a real barrier to adoption:

> "When I ask potential customers about analog, aging is one of the things they're not sure how to handle, and it tends to scare them away."

This isn't theoretical. PCM devices exhibit conductance drift with v=0.1-0.15, meaning stored weights shift over weeks and months. RRAM has cycle-to-cycle variability. Flash is the most stable but still needs periodic recalibration.

---

## 2. The "Pick Two" Trilemma

A recurring engineering maxim appears across multiple practitioner discussions:

> "It's power, speed, or accuracy with analog. Pick two."

This captures the fundamental constraint that analog CIM designers face. You can get extreme power efficiency (sub-milliwatt), but you sacrifice precision. You can get high throughput, but the ADC/DAC overhead eats your power budget. You can get reasonable accuracy (6-8 effective bits), but at the cost of both power and speed.

Digital systems don't face this trilemma — they get deterministic accuracy for free with any digital representation.

---

## 3. The Insiders Who Admit the Hard Parts

### Naveen Verma, CEO of EnCharge AI (the most credible analog CIM startup)

Even the strongest advocate acknowledges that the analog compute part is not the real challenge:

> "When it comes down to it, the capacitor part is the easy part — it is making the rest of the architecture as efficient as the accelerator, and developing a software stack that has kept the company busy for seven or eight years."

This is a remarkable admission from the CEO of the leading analog CIM company: the hard problem isn't analog compute, it's everything around it — data movement, digital peripherals, ADC/DAC, compiler, runtime, model conversion tools.

Verma also directly criticized digital CIM approaches:

> "The fundamental technology you have still looks the same as a digital accelerator... by inserting [adders] inside memory, all you've really done is blown the memory up, and the energy is the same as what you would have had had you done it outside the memory. The benefits are incremental compared to standard digital computing."

**Source:** [EnCharge Picks The PC For Its First Analog AI Chip](https://www.eetimes.com/encharge-picks-the-pc-for-its-first-analog-ai-chip/), EE Times; [Is In-Memory Compute Still Alive?](https://semiengineering.com/is-in-memory-compute-still-alive/), Semiconductor Engineering

### Ty Garibay, VP of Engineering at Mythic (during the 2022 crisis)

When Mythic ran out of money in November 2022, Garibay gave a candid assessment:

> "We ran out of runway with the investors before we could get to revenue."

The lesson from Mythic's near-death: having working analog silicon is necessary but not sufficient. You also need a software stack, a toolchain, customer design wins, and enough runway to survive the 5-7 year hardware development cycle. Mythic had raised $165M and still ran out of money before generating meaningful revenue.

**Source:** [Analog AI chip startup Mythic runs out of money](https://www.theregister.com/2022/11/09/mythic_analog_ai_chips/), The Register, Nov 2022

### Chan Carusone (Industry Expert)

Carusone offered a balanced but cautious view:

> "Most rational interest is focused on low-power or niche edge inference applications... the key challenge is finding applications with enough volume and market potential to justify the tailored hardware solution, which is why the idea has been hanging around for a long time while waiting for a big impact opportunity."

This is the pragmatic engineer's view: the technology works in the lab, but the market may not exist at the scale needed to justify the investment.

**Source:** [Is In-Memory Compute Still Alive?](https://semiengineering.com/is-in-memory-compute-still-alive/), Semiconductor Engineering

---

## 4. Hacker News and Community Discussions

### The Recurring Skeptical Arguments

Across multiple HN threads on analog AI chips ("Analog computing may be coming back," "The Zombie Comeback of Analog Computing," "China's analog AI chip 1000x faster"), several arguments recur:

1. **"We've seen this before."** Commenters regularly cite Carver Mead's work at Caltech in the 1980s-90s on analog VLSI neural networks. He co-founded Synaptics with analog compute ideas, but "making working chips proved too difficult and the company pivoted to other hardware." Analog AI has been 5 years away for 30 years.

2. **"The 1000x claims are always against straw men."** When Chinese researchers claimed an analog chip 1000x faster than NVIDIA H100 (Peking University, Nature Electronics, Oct 2025), HN commenters immediately questioned: What workload? What precision? Which H100 configuration? Analog efficiency claims are almost always on narrow, cherry-picked benchmarks.

3. **"Analog is great for specific problems, terrible for general compute."** The community distinguishes between analog preprocessing (sensible — the signal is already analog) and analog general compute (questionable). "Digital computers support general programming, while analog computers are limited to solving specific types of problems."

4. **"The software gap is the real moat."** Even sympathetic commenters note that CUDA's ecosystem took 15+ years to build. Analog chips don't just need hardware — they need compilers, debuggers, profilers, model conversion tools, and a community of developers. No analog startup has this.

**Sources:**
- [Analog computing may be coming back](https://news.ycombinator.com/item?id=34585958), HN, Feb 2023
- [The Zombie Comeback of Analog Computing](https://news.ycombinator.com/item?id=35373930), HN, Apr 2023
- [China's analog AI chip 1000x faster](https://news.ycombinator.com/item?id=45675710), HN, 2025

---

## 5. The VC vs. Engineering Gap

### The $475M Seed Round That Broke the Internet

Unconventional AI, founded by Naveen Rao (who previously sold Nervana to Intel and MosaicML to Databricks), raised $475M in seed funding at a $4.5B valuation — two months after incorporation, with no product, no prototype, and no revenue.

A viral Medium article captured the engineering community's reaction:

> "A company that's about two months old just raised $475 million with no product, no revenue, no prototype."

> "The old rule was 'build something — prove it works — raise money.' Now it's closer to 'prove you are the kind of person who could build something — raise everything — figure it out later.'"

> "It might burn through half a billion dollars and quietly shut down after a few impressive research updates and no commercial path."

On X/Twitter, one commenter posted: "$475m valuation seems steep for a seed but it is AI" — then corrected himself: "Oh my" when he realized it was $475M in *funding*, not valuation.

Rao himself acknowledged the skepticism:

> "Some even label them 'madness.'"

But he defended the approach by noting that "machine learning is often nondeterministic in nature and so you don't necessarily need a deterministic compute platform."

This captures the core tension: VCs bet on people and narratives; engineers bet on working silicon. The $475M seed round is either visionary or the purest expression of AI hype — and the engineering community leans toward the latter.

**Sources:**
- [Someone Just Raised $475 Million for a Startup That Barely Exists](https://medium.com/@celestineriza/someone-just-raised-475-million-for-a-startup-that-barely-exists-22b73971a657), Medium, Dec 2025
- [Unconventional AI raises $475 million](https://www.axios.com/2025/12/09/unconventional-ai-475-million), Axios, Dec 2025
- [Unconventional AI confirms its massive $475M seed round](https://techcrunch.com/2025/12/09/unconventional-ai-confirms-its-massive-475m-seed-round/), TechCrunch, Dec 2025

### The Revenue-to-Investment Ratio

The numbers tell the story of the VC-engineering gap:

| Metric | Value |
|--------|-------|
| Total VC invested in analog AI chips | ~$1.5-2B |
| Total sector revenue (all companies combined) | ~$8M |
| Revenue-to-investment ratio | 0.4-0.5% |
| Mythic revenue (sector leader) | $6.4M (2025) |
| Unconventional AI seed round (no product) | $475M |

When a company with no product raises more capital than the entire sector has generated in revenue, the engineering community notices.

---

## 6. What ML Practitioners Think

### The Toolchain Problem

ML engineers who have evaluated analog hardware consistently cite the software ecosystem as the deal-breaker:

> "Programming analog computers and calibrating them is very difficult. Compared to digital systems which have well-established software flows, analog computer softwarization is in its infancy and forms the biggest hurdle in the commercial deployment of analog computer approaches."

Practitioners ask practical questions that analog startups struggle to answer:

- **"Can the hardware run the ops my model needs?"** Many analog chips support matrix-multiply but not attention, dynamic shapes, or certain activations.
- **"Is the toolchain mature enough to deploy without heroic engineering?"** The answer is almost always no.
- **"What happens when I update my model?"** On a GPU, you just load new weights. On an analog chip, you may need to recalibrate, retrain with hardware-aware quantization, or even retape the chip.
- **"Can I debug accuracy problems?"** On a GPU, every intermediate value is deterministic and inspectable. On analog hardware, values are stochastic and drift over time.

### The Digital Quantization Threat

The biggest threat to analog AI is not better digital chips — it's better digital quantization. INT4 and NF4 quantization on standard GPUs/NPUs now achieves near-full-precision accuracy with 4x memory reduction and proportional speedups. FP4 (2025) is designed specifically for neural network weight distributions and achieves ~0.2% error to full precision.

This matters because analog CIM's main efficiency advantage comes from low-precision compute. If digital can do 4-bit with deterministic accuracy, standard toolchains, and zero recalibration, analog's 4-bit with stochastic noise becomes much harder to justify.

---

## 7. The Bull Case vs. Bear Case (From Practitioners)

### The Bull Case

Practitioners who are bullish on analog CIM make these arguments:

1. **Physics wins at the edge.** Below 1 mW, analog preprocessing is the only option that keeps the digital subsystem asleep. Aspinity's AML200 at 300 TOPS/W and <100 uW demonstrates this. No digital chip can compete because the signal is already analog.

2. **The energy crisis is real.** Hyperscalers spent $380B+ on AI infrastructure in 2025. Power consumption is unsustainable. A 1000x efficiency improvement, even if only achievable for narrow workloads, could matter enormously.

3. **Digital scaling is ending.** Moore's Law delivers ~15% efficiency gains per node. Analog CIM delivers 2-10x in one architectural shift. As digital improvements slow, analog's advantage grows relatively.

4. **The capacitor approach works.** EnCharge's charge-domain CIM avoids the drift, noise, and variability problems of RRAM/PCM. Capacitors are standard CMOS devices. The EN100 at ~24 TOPS/W (system-level) is a real data point.

5. **IBM proved transformers on analog.** The HERMES chip ran ALBERT (7.1M params) on analog PCM with software-equivalent accuracy, proving that analog inference is not limited to simple CNNs.

### The Bear Case

Practitioners who are bearish make these arguments:

1. **The 100x claim always collapses to 2-10x.** Every analog company claims 100x over GPUs. Every independent measurement shows 2-14x at the system level. The ADC/DAC overhead (40-85% of system power) is the immovable object.

2. **Digital quantization is eating analog's lunch.** INT4, NF4, and FP4 quantization on standard hardware achieves comparable efficiency gains with deterministic accuracy and standard toolchains. The window for analog's advantage is closing fast.

3. **No software ecosystem.** There is no CUDA for analog. No TensorRT. No ONNX Runtime. Every analog chip requires bespoke model conversion. This is not a temporary problem — it's structural, because analog compute is fundamentally different from digital and cannot share the same compiler infrastructure.

4. **Models change faster than hardware.** Analog chips are optimized for specific model architectures. But ML models evolve every 6-12 months. A chip taped out for CNNs in 2022 was obsolete by 2024 when transformers took over. Analog hardware cannot adapt as fast as digital.

5. **The Mythic cautionary tale.** $165M raised. Near-bankruptcy. Ten years to get to $6.4M revenue. This is the *success story* of analog AI. The typical outcome is worse.

6. **ISSCC 2025 voted with its papers.** Zero analog CIM papers in the dedicated CIM session at the world's premier circuits conference. Digital SRAM CIM hit 192.3 TFLOPS/W. The academic community — which has no VC incentive structure — is moving to digital CIM.

---

## 8. The Mythic Experience: What People Who Used the Chip Think

Mythic is the only analog CIM company that has shipped real silicon to real customers. The picture is mixed:

**What works:**
- Defense and DoD customers validated the technology. Lockheed Martin and Honda are real customers.
- The chip actually runs inference. It's not vaporware.
- Power efficiency is genuinely better than comparable digital solutions for the supported workloads.
- Using mature process nodes (40nm) gives supply chain advantages and lower cost.

**What doesn't work:**
- The first generation delivered ~8 TOPS/W at the system level — good, but not the 100x claimed in marketing.
- Nearly died in 2022 after burning through $165M.
- Had to radically restructure: new CEO, new strategy, pivoted to defense/public safety from broad consumer market.
- The Gen 2 claims (120 TOPS/W, 750x more tokens/watt than NVIDIA for 1T parameter LLMs) are unverified by independent benchmarks.
- Software toolchain was reportedly underdeveloped, a key factor in the company's struggles.

The Mythic experience is the single most important data point for practitioners evaluating analog AI. It proves the technology works. It also proves that working technology is not enough.

**Sources:**
- [AI chip startup Mythic rises from the ashes](https://techcrunch.com/2023/03/09/ai-chip-startup-mythic-rises-from-the-ashes-with-13m-new-ceo/), TechCrunch, Mar 2023
- [Mythic to Challenge AI's GPU Pantheon](https://mythic.ai/whats-new/mythic-to-challenge-ais-gpu-pantheon-with-100x-energy-advantage-and-oversubscribed-125m-raise/), Mythic, Dec 2025

---

## 9. BrainChip Akida: The Developer Experience

BrainChip takes a different approach (neuromorphic/spiking neural networks rather than analog CIM), but developer feedback is relevant:

**Positives:**
- Standard ML frameworks (TensorFlow) supported via MetaTF conversion tool.
- Cloud access available for prototyping without physical hardware.
- Edge Impulse integration simplifies deployment.
- Akida 2 (2025) claims 4x performance/efficiency over Akida 1.

**Negatives:**
- Revenue of $398K suggests almost no real deployments despite years on market.
- The neuromorphic/SNN approach requires model conversion that loses accuracy.
- Limited to specific model architectures that can be converted to spiking form.
- Public stock (ASX: BRN) trades largely on retail investor speculation, not engineering validation.

The BrainChip experience reinforces the practitioner consensus: novel AI hardware needs a much larger software investment than hardware companies typically budget for.

---

## 10. Verdict: The Engineering Community's Consensus

After surveying chip designers, ML practitioners, semiconductor industry veterans, and community discussions, the consensus is:

1. **Analog CIM works in the lab.** Nobody disputes the physics. Multiply-accumulate in the analog domain is genuinely more power-efficient than digital for low-precision operations.

2. **Analog CIM mostly fails in the market.** The gap between lab demonstrations and commercial products is enormous. Software ecosystem, calibration overhead, precision limitations, and fast-evolving model architectures create barriers that pure hardware innovation cannot overcome.

3. **The engineering community is much more skeptical than the VC community.** Engineers who design chips and deploy models see analog CIM as a niche tool for specific edge applications. VCs see it as a potential platform shift worth billions. The $475M Unconventional AI seed round is the clearest example of this gap.

4. **The one domain where analog wins unambiguously is always-on sensor edge (<1 mW).** Here, keeping the signal in the analog domain and avoiding the ADC entirely provides a structural advantage that digital cannot match.

5. **For everything else, digital is winning.** Digital CIM, digital quantization (INT4/NF4/FP4), and conventional NPU improvements are closing the efficiency gap while maintaining deterministic accuracy and standard toolchains.

6. **The smart money inside the engineering community is on charge-domain CIM (EnCharge's approach)** as the most likely analog technology to achieve commercial success — but even EnCharge has no independent benchmarks and has spent 7-8 years on software alone.

---

## Sources

- [The Uncertain Future of In-Memory Compute](https://semiengineering.com/the-uncertain-future-of-in-memory-compute/) — Semiconductor Engineering, Jan 2024
- [Is In-Memory Compute Still Alive?](https://semiengineering.com/is-in-memory-compute-still-alive/) — Semiconductor Engineering, Dec 2024
- [Analog AI chip startup Mythic runs out of money](https://www.theregister.com/2022/11/09/mythic_analog_ai_chips/) — The Register, Nov 2022
- [AI chip startup Mythic rises from the ashes](https://techcrunch.com/2023/03/09/ai-chip-startup-mythic-rises-from-the-ashes-with-13m-new-ceo/) — TechCrunch, Mar 2023
- [Mythic to Challenge AI's GPU Pantheon with 100x Energy Advantage](https://mythic.ai/whats-new/mythic-to-challenge-ais-gpu-pantheon-with-100x-energy-advantage-and-oversubscribed-125m-raise/) — Mythic, Dec 2025
- [EnCharge Picks The PC For Its First Analog AI Chip](https://www.eetimes.com/encharge-picks-the-pc-for-its-first-analog-ai-chip/) — EE Times
- [EnCharge's Analog AI Chip Promises Low-Power and Precision](https://spectrum.ieee.org/analog-ai-chip-architecture) — IEEE Spectrum
- [Someone Just Raised $475 Million for a Startup That Barely Exists](https://medium.com/@celestineriza/someone-just-raised-475-million-for-a-startup-that-barely-exists-22b73971a657) — Medium, Dec 2025
- [Unconventional AI raises $475 million](https://www.axios.com/2025/12/09/unconventional-ai-475-million) — Axios, Dec 2025
- [Unconventional AI confirms its massive $475M seed round](https://techcrunch.com/2025/12/09/unconventional-ai-confirms-its-massive-475m-seed-round/) — TechCrunch, Dec 2025
- [Unconventional AI Wants to Solve AI Scaling Crunch with Analog Chips](https://www.hpcwire.com/2025/12/08/unconventional-ai-aims-wants-to-solve-ai-scaling-crunch-with-analog-chips-will-it-work/) — HPCwire, Dec 2025
- [Analog computing may be coming back](https://news.ycombinator.com/item?id=34585958) — Hacker News, Feb 2023
- [The Zombie Comeback of Analog Computing](https://news.ycombinator.com/item?id=35373930) — Hacker News, Apr 2023
- [China's analog AI chip 1000x faster](https://news.ycombinator.com/item?id=45675710) — Hacker News, 2025
- [11 Myths About Analog Compute](https://www.electronicdesign.com/technologies/analog/article/21180871/mythic-11-myths-about-analog-compute) — Electronic Design / Mythic
- [A Look at Akida - BrainChip](https://open-neuromorphic.org/neuromorphic-computing/hardware/akida-brainchip/) — Open Neuromorphic
- [The Femtojoule Promise of Analog AI](https://spectrum.ieee.org/analog-ai) — IEEE Spectrum
- [Closing the accuracy gap between analog and digital AI](https://communities.springernature.com/posts/closing-the-accuracy-gap-between-analog-and-digital-ai) — Springer Nature
