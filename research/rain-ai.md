# Rain AI (Rain Neuromorphics) — Rise, Pivot, and Collapse

## Status: Exploring Sale / Likely Defunct (as of March 2026)

Rain AI, once one of the most hyped analog AI chip startups, is functionally insolvent. The company's $150M Series B collapsed in 2025, it secured a desperate $3M bridge round in May 2025, and it is exploring acquisition by OpenAI, NVIDIA, or Microsoft. No completed acquisition has been publicly announced as of March 2026. Key talent has already departed — Google DeepMind hired at least one senior engineer (Maxence Ernoult) from Rain's neuromorphic computing team.

---

## Company Timeline

| Date | Event |
|------|-------|
| 2017 | Founded in San Francisco by Jack Kendall and Will Passo (Y Combinator W18) |
| 2018 | Sam Altman leads seed round (~$1M personal investment) |
| 2021 | First prototype chip taped out (analog memristor crossbar array) |
| 2022 Feb | $25M Series A announced; Altman quoted saying Rain could "enable true AGI" |
| 2023 | Series A-II (extension); valuation estimated $250-350M |
| 2023 | OpenAI signs non-binding Letter of Intent to buy $51M of Rain chips |
| 2023 Nov | Altman fired from OpenAI; Rain deal cited as potential conflict of interest |
| 2023 Dec | Altman reinstated at OpenAI; OpenAI says it "hadn't progressed" with Rain |
| ~2024 | **Quiet pivot from analog/memristor to digital compute-in-memory (dCIM)** |
| 2024 | Puget Sound SoC taped out on TSMC 6nm (digital CIM + RISC-V) |
| 2024 | Will Passo (co-founder/CEO) steps down; Jack Kendall takes over as CEO |
| 2024 | J-D Allegrucci (ex-Apple semiconductor) hired as VP Engineering |
| 2025 | $150M Series B fundraise fails; Altman had pitched OpenAI investors at $600M valuation |
| 2025 May | Emergency $3M bridge round to sustain operations during acquisition talks |
| 2025+ | OpenAI, NVIDIA, Microsoft reportedly in acquisition discussions |
| 2025 | Google DeepMind hires Rain AI engineer Maxence Ernoult |
| 2026 Mar | No acquisition announced; company status unclear |

**Total funding raised:** ~$67M (across seed, Series A, Series A-II, bridge)

---

## The Technology: Three Phases

### Phase 1: Analog Memristor NPU (2017-2023)

Rain's original vision was a fully analog neuromorphic processing unit (NPU):

- **Memristor crossbar arrays** as artificial synapses — weights stored as resistances, activations as voltages
- **Equilibrium Propagation** algorithm for on-chip analog training (not just inference)
- Claimed to be the "world's first end-to-end analog, trainable AI circuit"
- Target: 125M INT8 parameters, <50W, for vision/speech/NLP workloads
- Samples expected 2024, commercial shipment 2025

**What actually happened:** The memristor approach hit the same walls every analog startup hits — device variability, yield issues, lack of foundry support for exotic memristor processes, and the ADC/DAC bottleneck that collapses theoretical efficiency gains. Rain never shipped a commercial analog chip.

### Phase 2: Digital CIM Pivot (2024)

Sometime around 2024, Rain quietly abandoned the analog memristor approach and pivoted to **digital compute-in-memory (dCIM)**:

- **Puget Sound SoC**: TSMC 6nm, integrating digital CIM, customized RISC-V core, and custom IP
- Software stack: models written in PyTorch, compiled to run on Puget Sound
- Positioned for "inference for AI agents, reasoning models, and AGI"
- Planned commercial chip: **Ocean Beach** (never taped out)

This pivot is significant: Rain went from "analog will revolutionize AI" to building a conventional digital CIM chip — the same approach as d-Matrix, Axelera, and others. By the time Rain pivoted, the digital CIM market was already crowded with better-funded competitors.

### Phase 3: Fire Sale (2025-present)

With the Series B collapse, Rain's technology portfolio became acquisition bait:
- Patent portfolio (analog + digital CIM)
- Puget Sound test chip and associated IP
- Talent (what remains of it)

---

## The Sam Altman Entanglement

The Rain AI story cannot be separated from Sam Altman's involvement, which created a web of conflicts:

1. **Personal investment:** Altman invested ~$1M in Rain's seed round (2018)
2. **OpenAI LOI:** OpenAI signed a non-binding $51M Letter of Intent to buy Rain chips — while Altman was both OpenAI CEO and a Rain investor
3. **Board firing:** The Rain deal was reportedly among the conflicts of interest that contributed to Altman's brief firing from OpenAI in November 2023
4. **Series B pitch:** After reinstatement, Altman reportedly pitched OpenAI's own investors to back Rain's $150M Series B at a $600M valuation
5. **LOI abandoned:** OpenAI publicly distanced itself, saying it "hadn't progressed" with Rain and the LOI was non-binding
6. **Acquisition talks:** OpenAI is now reportedly among entities considering acquiring Rain — potentially getting the IP at a fraction of the $600M Altman once proposed

The entire saga illustrates the danger of intertwined investor/customer relationships in hardware startups. When the single champion (Altman) became politically compromised, both the customer relationship (OpenAI LOI) and the fundraise (Series B) collapsed simultaneously.

---

## What Went Wrong

### 1. The Analog Dream Was Unfeasible at Scale
Rain bet on memristors — the most difficult analog technology to productize. Memristors suffer from device-to-device variability, read/write endurance limits, and lack of mature foundry support. No startup has successfully commercialized memristor-based compute. (See also: [rram-memristor-chips.md](rram-memristor-chips.md))

### 2. Equilibrium Propagation Was Academically Interesting, Commercially Irrelevant
On-chip analog training sounds revolutionary but solves a problem nobody urgently has. The AI industry trains in the cloud on GPUs and deploys inference at the edge. An analog training chip requires customers to rebuild their entire ML pipeline.

### 3. Single-Customer Dependency
The $51M OpenAI LOI was Rain's primary commercial validation. When that evaporated, no other major customer existed. Rain had no diversified order book.

### 4. The Pivot Came Too Late
By the time Rain pivoted to digital CIM (~2024), the market was already occupied by d-Matrix ($2B+ valuation, shipping product), Axelera ($450M raised), EnCharge (charge-domain CIM), and others. Rain entered the digital CIM race with less money, less maturity, and less credibility.

### 5. Capital Intensity vs. Capital Access
Chip development requires $50-200M to go from concept to commercial product. Rain raised ~$67M total across its entire life. The failed $150M Series B was supposed to fund the commercial Ocean Beach chip. Without it, Rain had a test chip (Puget Sound) but no path to production.

### 6. Governance and Optics
The Altman conflict of interest created a cloud over every Rain deal. Institutional investors could not cleanly evaluate Rain's commercial prospects separately from its political entanglement with OpenAI's leadership drama.

---

## Lessons for Analog/Neuromorphic Chip Startups

1. **Exotic devices (memristors, RRAM, PCM) are startup killers.** Stick to standard CMOS processes. EnCharge (capacitor-based CIM) and Mythic/Sagence (flash-based CIM) made this choice; Rain did not, and paid for it.

2. **A non-binding LOI from your investor's other company is not commercial validation.** Rain's entire commercial narrative rested on a single non-binding letter from an entity where its lead investor was CEO. Real validation = binding purchase orders from arms-length customers.

3. **Pivoting a chip company is nearly fatal.** Unlike software, you cannot pivot a chip design in 6 months. Rain's analog-to-digital pivot meant restarting the multi-year chip development cycle with depleted capital.

4. **Celebrity investors are a double-edged sword.** Altman's involvement gave Rain outsized visibility and initial fundraising power, but it also created governance risk that ultimately contributed to the company's demise.

5. **Analog training is a dead end (for now).** Every successful analog chip company focuses on inference. Training requires high precision, reproducibility, and massive scale — none of which analog excels at.

6. **The funding valley of death for chip startups is real.** $25M gets you a test chip. $200M+ gets you to production. The gap between those numbers kills companies. Rain fell into exactly this gap.

---

## Sources

- [Yahoo Finance: Sam Altman's $150M AI Chip Bet Crashes: Rain AI Faces Sale](https://finance.yahoo.com/news/sam-altmans-150m-ai-chip-123106283.html)
- [Benzinga: Rain AI Faces Sale As OpenAI, Nvidia, And Microsoft Circle The Wreckage](https://www.benzinga.com/news/25/05/45600321/sam-altmans-150m-ai-chip-bet-crashes-rain-ai-faces-sale-as-openai-nvidia-and-microsoft-circle-the-wreckage)
- [AIM Media House: Rain AI's Neuromorphic Vision Hits Financial Hurdles](https://aimmediahouse.com/market-industry/rain-ais-neuromorphic-vision-hits-financial-hurdles)
- [Computerworld: OpenAI signed $51M deal to buy chips from Sam Altman portfolio firm](https://www.computerworld.com/article/1611233/openai-signed-51m-deal-to-buy-brain-chips-from-sam-altman-portfolio-firm.html)
- [Data Center Dynamics: Google DeepMind hires Rain AI engineer](https://www.datacenterdynamics.com/en/news/google-deepmind-hires-rain-ai-engineer-for-growing-ai-hardware-design-team/)
- [Cerebral Valley: Agents need faster chips - enter Rain AI](https://cerebralvalley.beehiiv.com/p/agents-need-faster-chips-enter-rain-ai)
- [EE Times: Rain Demonstrates AI Training on Analog Chip](https://www.eetimes.com/rain-demonstrates-ai-training-on-analog-chip/)
- [EE Times: Rain Neuromorphics Tapes Out Demo Chip for Analog AI](https://www.eetimes.com/rain-neuromorphics-tapes-out-demo-chip-for-analog-ai/)
- [Design-Reuse: Rain Neuromorphics Raises $25M Series A](https://www.design-reuse.com/news/11707-rain-neuromorphics-raises-25m-series-a-to-transform-ai-hardware-landscape/)
- [Nasdaq: Chip designer mimicking brain, backed by Sam Altman, gets $25M funding](https://www.nasdaq.com/articles/chip-designer-mimicking-brain-backed-by-sam-altman-gets-$25-mln-funding)
- [Hacker News: OpenAI Committed to Buying $51M of AI Chips from Startup Backed by Sam Altman](https://news.ycombinator.com/item?id=38506660)
- [Gary Marcus: Not consistently candid](https://garymarcus.substack.com/p/not-consistently-candid)
- [Rain AI Official Website](https://rain.ai)
- [Crunchbase: Rain AI](https://www.crunchbase.com/organization/rain-neuromorphics)
