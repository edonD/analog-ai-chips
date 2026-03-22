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

---

## Key Verdict

IBM proves analog CIM works for real neural networks with real energy savings, but the path from 4M-weight research chips to billion-parameter production systems is years long. NorthPole (digital near-memory) is closer to production and arguably more impactful in the near term. The 100x efficiency claims in press are aspirational; 14x is the measured reality.

Mythic AI is the best-funded commercial attempt at flash-based analog CIM. Gen 1 silicon delivered ~8 TOPS/W at 40nm -- genuinely good, but not the claimed 100x over GPUs. Gen 2 claims 120 TOPS/W but lacks independent verification. The pattern across all analog AI: headline claims of 100x efficiency, measured reality of 2-14x at the system level. The ADC/DAC overhead and software ecosystem gap remain the dominant unsolved problems.

---

## Log

| Date | What |
|------|------|
| 2026-03-22 | Mythic AI deep dive: flash-based analog CIM, $300M+ raised, near-death in 2022, Gen 1 at ~8 TOPS/W, Gen 2 claims 120 TOPS/W unverified, Honda/Lockheed partnerships |
| 2026-03-22 | BrainChip Akida: neuromorphic edge AI chip with real silicon but near-zero revenue; technology works, business case unproven |
| 2026-03-22 | Tsetlin machines: logic-based AI with silicon-proven 8.6 nJ/frame efficiency; Literal Labs (UK) and Anzyz (Norway) commercializing |
| 2026-03-22 | IBM analog AI deep dive: HERMES chips, NorthPole, aihwkit, drift mitigation, LLM scaling |
| 2026-03-22 | Project initialized |
