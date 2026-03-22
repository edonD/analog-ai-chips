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

---

## Key Verdict

IBM proves analog CIM works for real neural networks with real energy savings, but the path from 4M-weight research chips to billion-parameter production systems is years long. NorthPole (digital near-memory) is closer to production and arguably more impactful in the near term. The 100x efficiency claims in press are aspirational; 14x is the measured reality.

---

## Log

| Date | What |
|------|------|
| 2026-03-22 | IBM analog AI deep dive: HERMES chips, NorthPole, aihwkit, drift mitigation, LLM scaling |
| 2026-03-22 | Project initialized |
