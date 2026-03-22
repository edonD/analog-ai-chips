# ISSCC 2025: AI Chips, Compute-in-Memory, and Accelerators

**Conference:** 2025 IEEE International Solid-State Circuits Conference (ISSCC)
**Dates:** February 16-20, 2025, San Francisco, CA
**Theme:** "The Silicon Engine Driving the AI Revolution"
**Submissions:** ~914 papers submitted; ~255 accepted (~28% acceptance rate) across 37 technical sessions

ISSCC is the premier venue for chip design disclosure. The 2025 edition was dominated by AI -- from CIM macros to LLM-specific ASIC processors to diffusion-model accelerators. This file catalogs every AI-related paper and result found through extensive search, organized by topic.

---

## 1. Compute-in-Memory (Session 14)

Session 14 was the dedicated CIM session. Papers 14.4-14.7 are confirmed; papers 14.1-14.3 exist but their titles were not publicly accessible outside the IEEE paywall at time of research.

### Paper 14.4: 51.6 TFLOPS/W Full-Datapath CIM Macro
- **Title:** "A 51.6TFLOPs/W Full-Datapath CIM Macro Approaching Sparsity Bound and <2^-30 Loss for Compound AI"
- **Authors:** Zhiheng Yue, Xujiang Xiang, Yang Wang, et al.
- **Key result:** 51.6 TFLOPS/W energy efficiency
- **Key innovation:** Full-datapath CIM design that approaches the theoretical sparsity bound with extremely low numerical loss (<2^-30)
- **Significance:** Targeted at "compound AI" workloads -- multi-model pipelines combining LLMs with retrieval, tool use, etc.
- **DOI:** 10.1109/ISSCC49661.2025.10904702

### Paper 14.5: 192.3 TFLOPS/W Dual-Mode SRAM CIM
- **Title:** "A 28nm 192.3TFLOPS/W Accurate/Approximate Dual-Mode-Transpose Digital 6T-SRAM CIM Macro for Floating-Point Edge Training and Inference"
- **Authors:** Yiyang Yuan, Bingxin Zhang, Yiming Yang, et al.
- **Process:** 28nm
- **Key result:** 192.3 TFLOPS/W -- one of the highest CIM efficiencies reported at ISSCC
- **Key innovation:** Dual-mode operation supporting both accurate and approximate computation; transpose capability; supports **floating-point** operations for on-device training
- **Significance:** Floating-point CIM for training is rare. Most CIM is inference-only, fixed-point. This expands CIM's applicability.
- **DOI:** 10.1109/ISSCC49661.2025.10904659

### Paper 14.6: Bit-Rotated Hybrid-CIM Macro
- **Title:** "A 28nm 64kb Bit-Rotated Hybrid-CIM Macro with an Embedded Sign-Bit-Processing Array and a Multi-Bit-Fusion Dual-Granularity Cooperative Quantizer"
- **Authors:** Xi Chen, Shaochen Li, Zhican Zhang, et al.
- **Process:** 28nm, 64kb macro
- **Key innovation:** Hybrid CIM combining bit rotation, sign-bit processing, and multi-bit fusion quantization for flexible precision
- **DOI:** 10.1109/ISSCC49661.2025.10904646

### Paper 14.7: NeuroPilot CIM Macro
- **Title:** "NeuroPilot: A 28nm, 69.4fJ/node and 0.22ns/node, 32x32 Mimetic-Path-Searching CIM-Macro with Dynamic-Logic Pilot PE and Dual-Direction Searching"
- **Authors:** An Guo, Jingmin Zhang, Xingyu Pu, et al.
- **Process:** 28nm
- **Key result:** 69.4 fJ/node energy, 0.22 ns/node latency
- **Key innovation:** Not a standard MAC-array CIM -- this is a path-searching accelerator using CIM techniques, with dynamic logic pilot processing elements
- **DOI:** 10.1109/ISSCC49661.2025.10904805

### CIM Session Analysis

| Paper | TFLOPS/W | Process | Type |
|-------|----------|---------|------|
| 14.4 | 51.6 | -- | SRAM CIM, sparsity-aware |
| 14.5 | 192.3 | 28nm | Digital 6T-SRAM CIM, FP training+inference |
| 14.6 | -- | 28nm | Hybrid CIM, multi-precision |
| 14.7 | -- (69.4 fJ/node) | 28nm | Path-searching CIM |

**Key trend:** All confirmed CIM papers are digital or hybrid CIM, not analog. The field has moved decisively toward digital SRAM CIM at ISSCC 2025. Analog CIM (RRAM, PCM, flash) was notably absent from the dedicated CIM session.

**The 192.3 TFLOPS/W number** from paper 14.5 is extraordinary but needs context: this is a macro-level metric (not system-level), and the "approximate mode" likely uses very low precision. System-level efficiency with data movement included would be far lower. Still, as a macro benchmark, it represents a new high watermark.

---

## 2. AI Accelerators (Session 23)

Session 23 was the main AI accelerator session, containing ~10 papers. The session covered transformers, diffusion models, point cloud processing, LLMs, social AI agents, and text-to-motion generation -- reflecting the broadening scope of AI hardware beyond image classification.

### Paper 23.1: T-REX Transformer Accelerator
- **Title:** "T-REX: A 68-to-567us/Token 0.41-to-3.95uJ/Token Transformer Accelerator with Reduced External Memory Access and Enhanced Hardware Utilization in 16nm FinFET"
- **Authors:** Seunghyun Moon, Mao Li, Gregory K. Chen, Phil C. Knag, Ram Kumar Krishnamurthy, Mingoo Seok
- **Institutions:** Columbia University, Intel
- **Process:** 16nm FinFET
- **Key results:**
  - 68-567 us/token latency across 4 transformer workloads
  - 0.41-3.95 uJ/token energy
  - 31-65.9x reduction in external memory access (EMA)
  - 1.2-3.4x improvement in hardware utilization
- **Architecture:** RISC-V controller, 4 dense matrix-multiplication (DMM) cores, 4 sparse matrix-multiplication (SMM) cores, 2 auxiliary function units
- **Key innovation:** Factorized weight matrices (shared dense + per-layer sparse) reduce EMA dramatically. 16b-to-4b non-uniform quantization of weight scale matrices with negligible accuracy loss.
- **Significance:** Addresses the biggest bottleneck in transformer inference: external memory access dominates energy (up to 81% of total). T-REX's factorization approach is a strong architectural contribution.

### Paper 23.2: AC-Transformer (First Hong Kong AI Chip at ISSCC)
- **Title:** "A 28nm 0.22uJ/Token Memory-Compute-Intensity-Aware CNN-Transformer Accelerator with Hybrid-Attention-Based Layer-Fusion and Cascaded Pruning for Semantic-Segmentation"
- **Authors:** P. Dong, Y. Tan, X. Liu, P. Luo, Y. Liu, L. Liang, Y. Zhou, D. Pang, M. Yung, D. Zhang, X. Huang, S-Y. Liu, Y. Wu, F. Tian, C-Y. Tsui, F. Tu, K-T. Cheng
- **Institution:** ACCESS (AI Chip Center for Emerging Smart Systems), Hong Kong
- **Process:** 28nm
- **Key results:**
  - 0.22 uJ/token on SegFormerB0
  - 3.86-10.91x better energy efficiency than prior state-of-the-art
  - 22.05x EMA reduction via hybrid attention
  - 76.1% feature map sparsity via cascaded pruning (6x computation reduction)
  - 1.45x efficiency boost from layer-fusion scheduler
- **Significance:** First AI chip from Hong Kong at ISSCC. Targets semantic segmentation for autonomous driving -- a real, demanding workload. Supports both CNN and Transformer models on a single reconfigurable processor.

### Paper 23.3: EdgeDiff Diffusion Model Accelerator
- **Title:** "EdgeDiff: 418.4mJ/Inference Multi-Modal Few-Step Diffusion Model Accelerator with Mixed-Precision and Reordered Group Quantization"
- **Authors:** Sangjin Kim, Jungjun Oh, Jeonggyu So, Yuseon Choi, Sangyeob Kim, Dongseok Im, Gwangtae Park, Hoi-Jun Yoo
- **Institution:** KAIST, Yonsei University
- **Key results:**
  - 418.4 mJ/inference for text-to-image generation
  - 22.0x computation reduction, 42.3x EMA reduction via few-step diffusion
- **Key innovation:** Condition-aware Reordered Group Mixed Precision (CRMP), Compress-and-Add PE with Bit Shuffle Tree
- **Significance:** One of the first silicon demonstrations of on-device diffusion model inference. Targets mobile image generation -- a commercially hot workload in 2025.

### Paper 23.4: Nebula 3D Point Cloud Accelerator
- **Title:** "Nebula: A 28nm 109.8TOPS/W 3D PNN Accelerator Featuring Adaptive Partition, Multi-Skipping, and Block-Wise Aggregation"
- **Authors:** Changchun Zhou et al.
- **Process:** 28nm
- **Key result:** 109.8 TOPS/W
- **Significance:** Point cloud neural networks (PNNs) are critical for autonomous driving, robotics, and AR/VR. This addresses the irregular memory access patterns that make PNNs hard to accelerate.

### Paper 23.5-23.6: Diffusion Model Accelerators (Titles Not Publicly Available)
- Based on session analysis, 3 of 10 papers in Session 23 targeted diffusion model acceleration, indicating the field's strong interest in generative AI hardware.

### Paper 23.7: BROCA Social Agent SoC
- **Title:** "BROCA: A 52.4-to-559.2mW Mobile Social Agent System-on-Chip with Adaptive Bit-Truncate Unit and Acoustic-Cluster Bit Grouping"
- **Authors:** Wooyoung Jo, Seongyon Hong, Jiwon Choi, Beomseok Kwon, Haoyang Sang, Dongseok Im, Sangyeob Kim, et al.
- **Institution:** KAIST
- **Key result:** 52.4-559.2 mW power range
- **Architecture:** Multi-stage pipeline: user perception (multimodal encoder) -> RAG retrieval -> transformer-based response generation -> emotion generation + voice feedback
- **Significance:** Full social AI agent on a single chip. Integrates multimodal understanding, retrieval-augmented generation, and emotional response -- essentially a complete conversational AI system in silicon.

### Paper 23.10: HuMoniX Text-to-Motion Processor
- **Title:** "HuMoniX: A 57.3fps 12.8TFLOPS/W Text-to-Motion Processor with Inter-Iteration Output Sparsity and Inter-Frame Joint Similarity"
- **Authors:** Jaehoon Heo et al.
- **Institution:** KAIST CastLab
- **Key results:** 57.3 fps, 12.8 TFLOPS/W
- **Significance:** Accelerates transformer-based diffusion models for 3D human motion generation from text. Targets film, AR/VR, and gaming.

### Session 23 Composition
Per analysis, the 10 papers in Session 23 broke down as:
- 5 papers on **Transformer** architecture acceleration
- 3 papers on **Diffusion model** acceleration
- 1 paper on **general generative AI** processor design
- 1 paper on **3D point cloud** (PNN) acceleration

**Key trend:** Generative AI hardware (diffusion models, LLMs) now dominates the AI accelerator session. The CNN-era classification/detection accelerators of previous ISSCCs are being displaced.

---

## 3. LLM-Specific Hardware

### Slim-Llama: 4.69mW Billion-Parameter LLM Processor
- **Title:** "Slim-Llama: A 4.69mW Large-Language-Model Processor with Binary/Ternary Weights for Billion-Parameter Llama Model"
- **Authors:** Sangyeob Kim, Jungwan Lee, Hoi-Jun Yoo
- **Institution:** KAIST
- **Process:** Samsung 28nm CMOS
- **Die area:** 20.25 mm^2
- **On-chip SRAM:** 500 KB
- **Key results:**
  - **4.69 mW power** for billion-parameter Llama inference
  - 9 pJ/param energy
  - 489 ms latency for 1-bit Llama model
  - Supports up to **3 billion parameters**
  - 4.59x better energy efficiency than prior state-of-the-art
- **Key innovation:** Binary/ternary quantization (1-2 bit weights) + sparsity-aware look-up table eliminates most multiply operations. Output reuse scheme + index vector reordering.
- **Significance:** This is remarkable. Running a 3B-parameter LLM at under 5mW opens the door to always-on LLM inference on battery-powered devices. The catch: binary/ternary quantization causes significant accuracy loss compared to FP16 or INT8. The paper does not report perplexity or task accuracy, which is the critical missing metric. A 1-bit Llama model is fundamentally different from a full-precision Llama model.
- **The catch:** 489ms latency means ~2 tokens/second -- usable but not fast. And the quality of a 1-bit 3B model vs. a 16-bit 7B model is dramatically different. The headline "LLM at 5mW" needs the asterisk "with extreme quantization."

### IBM Telum II: Mainframe AI Acceleration
- **Title:** "IBM Telum II: Next Generation 5.5GHz Microprocessor with On-Die Data Processing Unit and Improved AI Accelerator"
- **Institution:** IBM
- **Process:** Samsung 5nm
- **Die:** 600 mm^2, 43 billion transistors, 18 metal layers
- **Key results:**
  - 5.5 GHz clock speed
  - 24 TOPS per chip (INT8 AI acceleration)
  - 768 TOPS per system (32 chips)
  - 30x higher AI TOPS/thread vs. prior generation
  - 40% more L2 cache (36MB per instance, 10 instances)
  - Only 5% power increase over Telum I
- **Significance:** Not a standalone AI accelerator -- this is a general-purpose mainframe processor with integrated AI. IBM's approach is to put AI inference right next to the data in the transaction processing path, avoiding data movement to external accelerators. The 24 TOPS/chip is modest by GPU standards but significant for inline inference during transaction processing.

---

## 4. Industry Presentations (Session 16: Industry Track)

Session 16 featured invited industry presentations from companies showcasing production or near-production chips.

### SambaNova SN40L
- **Architecture:** Dataflow accelerator with three-tier memory (on-chip SRAM + HBM + DDR)
- **Process:** TSMC 5nm
- **Key specs:**
  - 688 FP16 TFLOPS per chip
  - 102 billion transistors, 1,040 cores
  - 520 MB on-chip SRAM
  - 64 GB HBM + 1.5 TB DDR
  - 16-chip system: 10.2 BF16 PFLOPS for 70B model inference
- **Significance:** Dataflow architecture specifically designed for LLM inference at scale. The massive memory hierarchy (1.5TB DDR directly attached) targets the memory wall problem for large models.

### FuriosaAI RNGD (Renegade)
- **Architecture:** Tensor Contraction Processor (TCP) -- not standard matrix multiplication, uses tensor contraction as the fundamental primitive
- **Process:** TSMC 5nm, 1.0 GHz
- **Key specs:**
  - 512 TFLOPS (FP8)
  - 48 GB HBM3, 1.5 TB/s bandwidth
  - 150W TDP
  - 8 processing elements, each with 64 slices
- **Performance claims:**
  - 3x better perf/watt vs. NVIDIA H100 for LLMs
  - 2.25x better perf/watt in LG AI Research testing
- **Business context:** Reportedly acquired by Meta. Originally from South Korea. LG partnership.
- **Significance:** 512 TFLOPS at 150W = 3.4 TFLOPS/W (FP8) -- competitive with NVIDIA's latest. The tensor contraction approach is architecturally novel, presented at ISCA 2024.

### Samsung: Memory Technology for AI
- Samsung's plenary focused on the "memory wall" and HBM roadmap, processing-in-memory, hybrid bonding, and 3D-stacked DRAM. Not a specific AI chip but directly relevant to AI hardware scaling.

### Broadcom Tomahawk 5
- 51 Tbps networking ASIC -- not an AI compute chip but critical infrastructure for AI data centers. Next-gen Tomahawk 6 will be chiplet-based.

---

## 5. Vision/3D Processing Accelerators (Session 2 and others)

### National Tsing Hua University / TSMC: 8K Display Processor
- **Paper 2.9:** 16nm CNN processor for 8K-UHD 60fps display/streaming
- **Key result:** 10.2 TOPS, 1425 mW at 400MHz
- **Process:** 16nm, 8 mm^2

### Fudan University: Super-Resolution Processor
- **Paper 2.10:** 22nm low-power super-resolution
- **Key result:** 1K@107fps, 0.52 mJ/frame
- **Innovations:** Channel-number-adaptive caching (90% memory reduction), workload-balance engine (64% cycle reduction), hybrid data flow (75% utilization improvement)
- **Process:** 22nm, 6 mm^2

### National Tsing Hua University: Small-Object Detection CNN
- 16nm CNN processor for small-object detection
- **Key result:** 5.7 TOPS at 26.6 fps (896x896 inputs), 1.37W

### Tsinghua University: 3D Gaussian Splatting
- 28nm shape-aware architecture
- **Key result:** 6.65 TOPS/W peak at 150MHz from 0.65V

### KAIST IRIS: 3D Gaussian Splatting SoC
- **Title:** "IRIS: A 8.55mJ/frame Spatial Computing SoC for Interactable Rendering and Surface-Aware Modeling with 3D Gaussian Splatting"
- **Authors:** Seokchan Song et al. (KAIST)
- **Process:** 28nm
- **Key result:** 8.55 mJ/frame, 373 fps rendering, 664 mW
- **Significance:** 3D Gaussian splatting is emerging as the dominant approach for neural 3D scene rendering, replacing NeRF. Multiple ISSCC 2025 papers target it.

---

## 6. Chiplet and Heterogeneous Integration for AI

### Intel: 20-Chiplet AI Inference System
- **Title:** "A 300MB SRAM, 20Tb/s Bandwidth Scalable Heterogenous 2.5D System Inferencing Simultaneous Streams Across 20 Chiplets with Workload-Dependent Configurations"
- **Institution:** Intel
- **Key specs:**
  - 20 chiplets from 2 foundries (TSMC 16nm + Intel 4nm)
  - 300 MB total SRAM
  - 20 Tb/s bandwidth
  - Chiplet types: Tensilica LX7 processor (2 INT8 TOPS), memory (8 INT8 TOPS), PCIe4 PHY, H.264 decoder, debug logic
  - Passive silicon substrate: 22x19 mm (UMC 130nm)
- **Key innovation:** Standardized bump patterns ("chiplet slots") enabling mix-and-match assembly from multiple foundries. On-chiplet routers for dynamic runtime reconfiguration.
- **Significance:** Proof-of-concept for disaggregated AI inference using UCIe. Not competitive on raw TOPS, but architecturally important: demonstrates that chiplet-based AI systems from multiple foundries can work together.

---

## 7. Plenary and Special Sessions

### Plenary: Intel "AI Era Innovation Matrix"
- **Speaker:** Navid Shahriari, SVP Intel Foundry Technology Development
- Focused on Intel 18A process (nanosheet transistors + back-side power delivery via PowerVias)

### Plenary: Samsung "Memory Wall"
- **Speaker:** Jaihyuk Song, Corporate President and CTO
- HBM roadmap, processing-in-memory, hybrid bonding, 4F2 and 3D-stacked DRAM

### Plenary: Liquid AI / MIT
- **Speaker:** Prof. Daniela Rus (MIT / Liquid AI)
- **Topic:** "Building Physical Intelligence into Robotic Systems"
- Liquid Neural Networks: differential equation-based neurons instead of standard MACs. Claim: "under 20 liquid neurons can do the work of 10,000+ MAC operations"
- **Significance for analog compute:** Liquid Neural Networks are fundamentally a different compute paradigm. If validated in silicon, they could reduce the compute requirements so dramatically that the analog vs. digital efficiency debate becomes less relevant.

### Evening Event EE4: "The Next Decade of AI -- Barriers, Opportunities, & Directions"
### Evening Event: "Future of Analog Design: Still Magical or Mostly Digital?"
- The framing of this panel title is telling -- the industry is debating whether analog design has a future.

### Tutorial T9: "Generative AI on Edge Devices: Models, Hardware and Systems"
- **Instructor:** Paul Whatmough
- Covered challenges of deploying generative AI at the edge, including quantization, pruning, knowledge distillation, and hardware-specific optimization.

---

## 8. Key Trends and Analysis

### Trend 1: Digital CIM Dominates, Analog CIM Absent
The most striking observation from ISSCC 2025's CIM session is what was **not** there. All confirmed CIM papers (14.4-14.7) use **digital or hybrid SRAM-based** approaches. There were no RRAM, PCM, flash, or MRAM CIM papers in the dedicated CIM session. This is significant because ISSCC is where real silicon results are shown -- and the absence of analog/NVM CIM papers suggests:
- Analog CIM remains difficult to fabricate reliably at competitive process nodes
- The precision limitations of analog CIM are a barrier for the increasingly demanding accuracy requirements of modern models
- Digital SRAM CIM has improved so rapidly (192.3 TFLOPS/W!) that the motivation for going analog is shrinking

### Trend 2: Generative AI Hardware is the New Frontier
Session 23 (AI Accelerators) was dominated by generative AI: transformers, diffusion models, LLMs, text-to-motion, social AI agents. The CNN-era classification/detection chips of 5 years ago are now a small minority. The hardware community is following the model community into generative AI.

### Trend 3: LLM-Specific Silicon Has Arrived
Slim-Llama (KAIST) and the industry presentations (SambaNova SN40L, FuriosaAI RNGD) show that LLM-specific hardware is no longer theoretical. The approaches range from extreme quantization (1-bit weights at 5mW) to massive dataflow architectures (10 PFLOPS at rack scale). The diversity of approaches suggests the field has not converged on a single "right" architecture for LLMs.

### Trend 4: Memory Access is the Central Problem
Multiple papers (T-REX, AC-Transformer, Slim-Llama, Samsung plenary) identify external memory access (EMA) as the dominant energy cost. T-REX achieves 31-65x EMA reduction; AC-Transformer gets 22x. This validates the core thesis behind compute-in-memory -- bringing computation to the data. But notably, the most successful EMA-reduction papers at ISSCC 2025 use algorithmic techniques (weight factorization, sparsity, quantization) rather than analog CIM.

### Trend 5: KAIST Dominates Academic AI Accelerator Design
KAIST presented an extraordinary number of AI accelerator papers: Slim-Llama, EdgeDiff, BROCA, HuMoniX, IRIS -- at least 5 papers in a single ISSCC. Prof. Hoi-Jun Yoo's group and KAIST CastLab are the most prolific academic labs in AI chip design.

### Trend 6: 3D Gaussian Splatting is the New Target
Multiple papers (Tsinghua, KAIST IRIS, KAIST surface-aware) target 3D Gaussian Splatting (3DGS) acceleration. This is a new workload that barely existed 2 years ago but is now driving dedicated silicon -- evidence of how fast the hardware community responds to ML model innovations.

### Trend 7: Chiplets Are Coming to AI
Intel's 20-chiplet demo and Broadcom's chiplet-based Tomahawk 6 announcement signal that disaggregated AI hardware is approaching production. UCIe standardization enables multi-foundry assembly.

---

## 9. Comparison: CIM vs. Digital Accelerators at ISSCC 2025

| Metric | Best CIM (14.5) | Best Digital Accel (23.4) | LLM-Specific (Slim-Llama) | Industry (FuriosaAI) |
|--------|-----------------|---------------------------|---------------------------|---------------------|
| Efficiency | 192.3 TFLOPS/W | 109.8 TOPS/W | 9 pJ/param | 3.4 TFLOPS/W (FP8) |
| Process | 28nm | 28nm | 28nm | 5nm |
| Scope | Macro only | Full chip | Full chip | Full product |
| Model support | Fixed-point MAC | 3D point clouds | 1-bit Llama 3B | Any LLM up to 70B+ |
| Maturity | Research macro | Research chip | Research chip | Production chip |

**Critical note on comparing these numbers:** CIM macro efficiency (192.3 TFLOPS/W) cannot be directly compared to full-chip or product-level numbers. Macro measurements exclude data movement between macros, control overhead, I/O, and all the system-level costs that dominate real workloads. A realistic system-level CIM efficiency would be 10-50x lower than the macro number.

---

## 10. What This Means for Analog AI

ISSCC 2025 is not good news for analog compute-in-memory advocates:

1. **Digital CIM is achieving extraordinary efficiency numbers** (192.3 TFLOPS/W) at the macro level, closing the theoretical gap that motivated analog CIM
2. **No analog CIM papers** in the dedicated CIM session suggests the technology is not producing competitive silicon results
3. **Algorithmic approaches** (quantization, sparsity, weight factorization) are proving more effective at reducing memory access energy than changing the compute substrate
4. **The workloads have moved on:** Generative AI models (LLMs, diffusion) require higher precision and more complex operations than the fixed-point MAC arrays that analog CIM excels at
5. **Industry is investing in digital:** SambaNova, FuriosaAI, IBM Telum II are all digital architectures. No analog CIM company presented at ISSCC 2025.

However, ISSCC is not the only venue, and absence of evidence is not evidence of absence. Analog CIM startups (Mythic, EnCharge, Tetramem) may be presenting elsewhere or keeping results proprietary. And the sensor-edge space (always-on wake word, event detection) -- where analog's power advantage is most compelling -- is not well represented at ISSCC.

---

## Sources

- [ISSCC 2025 Advance Program](https://submissions.mirasmart.com/ISSCC2025/PDF/ISSCC2025AdvanceProgram.pdf)
- [First Impressions from 2025 ISSCC - Vikram Sekar](https://www.viksnewsletter.com/p/first-impressions-from-2025-isscc)
- [BUAA-CI-LAB SRAM CIM Literature List](https://github.com/BUAA-CI-LAB/Literatures-on-SRAM-based-CIM)
- [T-REX Paper (arXiv/ISSCC 23.1)](https://arxiv.org/pdf/2503.00322)
- [ACCESS Hong Kong AI Chip Announcement](https://inno-access.hk/news/research-paper-accepted-isscc-marking-innovative-breakthrough-empowers-intelligent-computing)
- [Slim-Llama (IEEE Xplore)](https://ieeexplore.ieee.org/document/10904761/)
- [Slim-Llama (MarkTechPost)](https://www.marktechpost.com/2024/12/20/slim-llama-an-energy-efficient-llm-asic-processor-supporting-3-billion-parameters-at-just-4-69mw/)
- [IBM Telum II (IBM Research)](https://research.ibm.com/publications/ibm-telum-ii-next-generation-55ghz-microprocessor-with-on-die-data-processing-unit-and-improved-ai-accelerator)
- [EdgeDiff (IEEE Xplore)](https://ieeexplore.ieee.org/document/10904594/)
- [Nebula (IEEE Xplore)](https://ieeexplore.ieee.org/document/10904703/)
- [HuMoniX (KAIST CastLab)](https://castlab.kaist.ac.kr/2024/10/11/isscc-2025-jaehoon-heos-paper-on-humonix-a-57-3-fps-12-8-tflops-w-text-to-motion-processor-with-inter-iteration-output-sparsity-and-inter-frame-joint-similarity-is-accepted/)
- [IRIS (IEEE Xplore)](https://ieeexplore.ieee.org/document/10904521/)
- [Intel Chiplet at ISSCC 2025](https://www.allaboutcircuits.com/news/isscc-2025-intel-propels-chiplet-interconnect-speed-and-flexibility/)
- [Intel at ISSCC 2025](https://community.intel.com/t5/Blogs/Tech-Innovation/Edge-5G/Intel-at-ISSCC-2025-Navid-Shahriari-Invited-Talk-Eight-Papers/post/1667592)
- [ISSCC 2025 CPUs and Image Processors (Electronics Weekly)](https://www.electronicsweekly.com/news/design/isscc-cpus-and-image-processors-2025-02/)
- [SambaNova SN40L (arXiv)](https://arxiv.org/html/2405.07518v1)
- [FuriosaAI RNGD](https://furiosa.ai/blog/rngd-preview-furiosa-ai)
- [KAIST SSL Publications](https://ssl.kaist.ac.kr/Paper_Conference.php)
- [Fengbin Tu Publications](https://fengbintu.github.io/publications/)
