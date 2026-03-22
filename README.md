# Analog AI Chips Research — 2025/2026

A deep-dive engineering reference on analog, neuromorphic, and mixed-signal AI chips. The core question: **can analog compute challenge digital for AI inference?**

---

## What Has Been Found

**IBM** has the strongest analog AI research program. Their HERMES chip (14nm, 64-core PCM-based) achieves 92.81% on CIFAR-10, 12.4 TOPS/W, and 14x energy efficiency over digital for speech tasks. But it holds only ~4M weights -- orders of magnitude from LLM scale. Their NorthPole chip (digital near-memory, not analog) is more mature: 72.7x more energy-efficient than GPUs on a 3B-parameter LLM. The gap between IBM's analog research prototypes and production hardware remains enormous. PCM drift is manageable but not solved. Scaling from millions to billions of weights is the central unsolved challenge.

---

## Research Files

| File | Topic | Key Finding |
|------|-------|-------------|
| [research/ibm-analog-ai.md](research/ibm-analog-ai.md) | IBM Analog AI (HERMES, NorthPole, aihwkit) | Strongest analog AI research program; 14x efficiency proven in silicon but scaling to LLM-class workloads undemonstrated |
| [research/tsetlin-machines.md](research/tsetlin-machines.md) | Tsetlin Machines: Logic-Based AI Hardware | 65nm ASIC achieves 8.6 nJ/frame MNIST (lowest digital ASIC); purely bitwise inference; not applicable to generative AI or LLMs |
| [research/brainchip-akida.md](research/brainchip-akida.md) | BrainChip Akida Neuromorphic Processor | Event-driven digital neuromorphic chip; 76.9 FPS/W (50x vs embedded GPU) on small models; but ~$400K revenue on $274M market cap; no volume customers after 4 years shipping |
| [research/mythic-ai.md](research/mythic-ai.md) | Mythic AI: Flash-Based Analog Compute-in-Memory | Best-funded analog CIM startup ($300M+ raised); Gen 1 delivers ~8 TOPS/W (40nm, real silicon); Gen 2 claims 120 TOPS/W (unverified); nearly died in 2022 pre-revenue; $125M raised Dec 2025; Honda and Lockheed partnerships; headline 100x claims need independent validation |
| [research/photonic-ai-chips.md](research/photonic-ai-chips.md) | Photonic AI Chips: Optical Computing for Neural Networks | Photonic interconnect is real and shipping (NVIDIA, Lightmatter, Ayar Labs, Celestial AI/Marvell $5.5B). Photonic compute remains pre-commercial: best measured result is 8.19 TOPS at 2.38 TOPS/W; claims of 160-300 TOPS/W exclude system overhead. DAC/ADC bottleneck, lack of optical nonlinearity, and no optical memory are fundamental barriers. Timeline: interconnect now, hybrid compute 2028+, all-optical 2032+ if ever. |
| [research/edge-analog-ai.md](research/edge-analog-ai.md) | Analog/Mixed-Signal Edge AI (Aspinity, Syntiant, POLYN, Innatera, et al.) | Analog strongest at sensor edge (30-100 uW always-on); Syntiant most successful (10M+ shipped, ~$300M rev) but uses digital near-memory, not analog; Aspinity pure analog ML (AML100 shipping, AML200 at 300 TOPS/W); market ~$250M growing to $2.5B by 2035 |
| [research/analog-cim-landscape-2025.md](research/analog-cim-landscape-2025.md) | Full Analog CIM Landscape 2025-2026 | Broadest overview: 6 memory technologies (SRAM, Flash, RRAM, PCM, MRAM, FeRAM), 10+ companies with silicon or near-silicon, ISSCC 2025 papers, performance comparisons. EnCharge AI (200 TOPS, capacitor CIM) and Mythic (25 TOPS, flash CIM) are the two commercial analog CIM products. Digital CIM (Axelera 214 TOPS) is closing the efficiency gap. "Power, speed, or accuracy -- pick two" remains the fundamental law. |

---

## Key Verdict

IBM proves analog CIM works for real neural networks with real energy savings, but the path from 4M-weight research chips to billion-parameter production systems is years long. NorthPole (digital near-memory) is closer to production and arguably more impactful in the near term. The 100x efficiency claims in press are aspirational; 14x is the measured reality.


At the sensor edge, analog makes its strongest case. Aspinity's AML100 (pure analog ML, shipping since Q1 2024) and AML200 (22nm, 300 TOPS/W, sampling Q1 2025) process raw sensor data before the ADC at 30-100 uW -- enabling always-on sensing impossible with digital power budgets. But model capacity is tiny (125K params max), limiting workloads to keyword spotting and event detection. Syntiant, the most commercially successful edge AI chip company (10M+ shipped, ~$300M projected 2025 revenue after Knowles acquisition), achieved this with digital near-memory architecture -- proving extreme efficiency is possible without going analog. The real power savings from analog preprocessing come from keeping digital systems asleep, not from analog compute being fundamentally faster.
Mythic AI is the best-funded commercial attempt at flash-based analog CIM. Gen 1 silicon delivered ~8 TOPS/W at 40nm -- genuinely good, but not the claimed 100x over GPUs. Gen 2 claims 120 TOPS/W but lacks independent verification. The pattern across all analog AI: headline claims of 100x efficiency, measured reality of 2-14x at the system level. The ADC/DAC overhead and software ecosystem gap remain the dominant unsolved problems.

---

## Log

| Date | What |
|------|------|
| 2026-03-22 | Analog CIM landscape: comprehensive overview of 6 memory techs, 10+ companies, ISSCC 2025 papers, EnCharge EN100 (200 TOPS), Mythic M1076, Axelera Metis (digital CIM), IBM HERMES, Peking/Nanjing precision records, Sagence/TetraMem/Rain AI status |
| 2026-03-22 | Edge analog AI: Aspinity (pure analog ML, AML100 shipping, AML200 at 300 TOPS/W), Syntiant (10M+ digital near-memory chips shipped, $300M rev), POLYN (34uW analog neurons), Innatera (spiking neuromorphic MCU), plus AONDevices, Ambient Scientific, TDK reservoir computing, SemiQa |
| 2026-03-22 | Mythic AI deep dive: flash-based analog CIM, $300M+ raised, near-death in 2022, Gen 1 at ~8 TOPS/W, Gen 2 claims 120 TOPS/W unverified, Honda/Lockheed partnerships |
| 2026-03-22 | BrainChip Akida: neuromorphic edge AI chip with real silicon but near-zero revenue; technology works, business case unproven |
| 2026-03-22 | Tsetlin machines: logic-based AI with silicon-proven 8.6 nJ/frame efficiency; Literal Labs (UK) and Anzyz (Norway) commercializing |
| 2026-03-22 | IBM analog AI deep dive: HERMES chips, NorthPole, aihwkit, drift mitigation, LLM scaling |
| 2026-03-22 | Project initialized |
