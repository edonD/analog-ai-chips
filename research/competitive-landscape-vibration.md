# Competitive Landscape: Always-On Vibration Monitoring Chips

*Last updated: 2026-03-22*

The vibration monitoring market is $1.5-2.0B (2025), growing 5-7% CAGR to $2.5-3.5B by 2034. The chip content per wireless sensor node is $10-30, making the total addressable chip market roughly $200-500M. This file maps every player, explains why the big companies haven't built what we're building, and identifies where VibroSense-1 fits.

---

## Direct Competitors (Analog Vibration Preprocessing)

Only **three companies** worldwide are building analog preprocessing chips for vibration. One is in production.

### POLYN Technology (Israel, ~$26.5M raised, est. 2019)

**Product:** VibroSense — neuromorphic analog signal processor (NASP)

**Status:** The VAD (voice activity detection) chip shipped in first silicon October 2025. The VibroSense vibration product **has NOT shipped in silicon** as of March 2026. POLYN announced VibroSense for IIoT in March 2023 as a chip *design*. They have an evaluation kit for tire monitoring (VibroSense-TMS) and are running POCs with tire makers.

**Architecture:** Fully asynchronous (no clock, no ADC). Op-amp neurons with thin-film resistor synapses. The analog portion is partially hardwired per application. Process-agnostic 40-90nm CMOS.

**Claimed specs:**
- VAD chip: 34 uW continuous, 50 us latency
- VibroSense (vibration): ~100 uW claimed — **not independently verified, not in silicon**
- No frequency resolution specifications published
- Binary classification only (normal vs fault) — no multi-class

**Pricing:** Not public. Contact-sales only. No Mouser/Digikey listing.

**Revenue:** Claims "$10M in sales contracts" — unclear if booked or pipeline.

**Patents:** 21+ filed, 5+ granted in US. Key patents cover NASP technology for vibration and tire monitoring. Claims are specific to neuromorphic (neural-network-based) analog processing — architecturally distinct from traditional filter bank + MAC approaches.

**Partnerships:** Infineon (joint tire health demo Q4 2024), unnamed tire makers.

**Honest assessment:** POLYN has proven the NASP concept works (VAD chip exists). But the vibration product is pre-production and may be 12-18 months from availability. Their 34 uW VAD number is real but their 100 uW VibroSense number is a claim, not a measurement. No independent benchmarks exist.

### Aspinity (Pittsburgh, ~$22-27M raised, est. ~2015)

**Product:** AML100 — Reconfigurable Analog Modular Processor (RAMP)

**Status:** Full production since Q1 2024. $1-2 at 1M+ quantities. 7×7mm QFN package. ~12 employees.

**Architecture:** Configurable Analog Blocks (CABs) with analog NVM weight storage. All-analog MAC and activation functions. Processes raw sensor data before the ADC.

**Specs:**
- Power: <20 uA always-on (~36 uW at 1.8V)
- Model capacity: ~10K parameters (AML100), ~125K parameters (AML200, sampling Q1 2025)
- AML200: 22nm, 2 TOPS, <100 uW, 300 TOPS/W claimed
- Supports: keyword spotting, glass break, vibration event detection, anomaly detection

**Pricing:** $1-2 at volume. AML200 pricing not announced.

**Customers:** Not named publicly. Markets listed: automotive, smart home, IoT. Strategic investor Unitrontech (automotive semiconductor distributor) signals auto traction.

**Limitations for vibration:** The AML100's ~10K parameter capacity limits the complexity of vibration models. It can detect "anomaly vs normal" but likely cannot do 4-class fault identification (bearing inner race vs outer race vs ball vs imbalance). The AML200 with 125K params would be more capable but is not yet in production.

**Honest assessment:** Aspinity is the only company shipping a pure analog ML chip in production. Their power numbers are real. But the model capacity is tiny — it's a wake-on-event detector, not a diagnostic classifier. For vibration, it can say "something is wrong" but not "the bearing outer race is pitting." That distinction matters for predictive maintenance.

### SemiQa (Early Stage)

Neuromorphic analog chip accepting multiple analog inputs (vibration, voice, video) without ADC. Too early to evaluate. No public specs or silicon.

---

## What The Big Companies Sell (And Why They Don't Build Analog Preprocessing)

### Analog Devices (ADI) — $12B Revenue

**What they sell for vibration:**

| Product | Type | Price | Notes |
|---------|------|-------|-------|
| ADXL1002 | Single-axis MEMS accel, ultra-low noise, 11kHz BW | $10-15 | Gold standard for CBM |
| ADXL355 | 3-axis MEMS accel, low power, digital SPI/I2C | $8-12 | Popular in wireless nodes |
| ADcmXL3021 | Complete module: 3× ADXL1002 + MCU + FFT + alarms | $300-350 | MCU inside doing digital FFT |
| ADIS16228 | Triaxial with 512-point FFT + storage | $343 | Discontinued/EOL |

**Why they don't build analog preprocessing:** An analog chip at $5-10 would cannibalize their $300+ module business. ADI makes more money selling components separately. Their analog expertise is in precision (low noise, low offset, high linearity), not analog computation.

**March 2025:** ADI announced a partnership with Siemens for digital twin integration — doubling down on digital, not analog.

### STMicroelectronics — $16B Revenue

**What they sell:**

| Product | Type | Price | Notes |
|---------|------|-------|-------|
| IIS3DWB | Wideband vibration MEMS, 26.7kHz ODR, 6kHz BW | $9 | Purpose-built for CBM |
| ISM330DHCX | 6-axis IMU with embedded ML Core + FSM | $5-10 | On-chip decision trees |
| ISM330BX | Newer ISM330 variant | ~$5-10 | |
| STM32L4+ | MCU for edge processing | $3-8 | |
| STEVAL-STWINKT1B | Full eval kit (IIS3DWB + ISM330 + MCU + BLE) | ~$80 | Reference platform |

**Why they don't build analog preprocessing:** STM already has a "good enough" answer. The ISM330DHCX has an embedded Machine Learning Core that runs decision trees directly on the MEMS sensor die, at minimal additional power. It's not as efficient as pure analog, but it's "free" — integrated into a sensor customers already buy. An analog preprocessing chip would destroy their MCU attach rate (every node that doesn't need an STM32 is lost MCU revenue).

### Texas Instruments

No MEMS accelerometers. Sells MCUs (MSP432P4, CC2652R7, AM2434) and ADCs. Published reference design TIDA-01469 (10-year battery, CR2032, 20 ksps, 2K FFT). Partners with TDK for i3 Micro Module.

**Why not analog:** No MEMS capability. Their business model is MCU + ADC + reference designs. An analog preprocessing chip would eliminate the need for their MCUs in this application.

### Infineon

Focuses on magnetic/acoustic sensing for motor monitoring (XENSIV Hall sensors, MEMS microphones). PSOC Edge MCU with Arm Ethos-U55 microNPU. No direct vibration MEMS.

### Bosch Semiconductors

SMA286/SMA285 high-bandwidth vibration MEMS (10kHz BW, TDM/SPI). Small product line sold through Bosch directly (not typical distribution). Their main MEMS business is consumer/automotive. Goal: 90% of products with on-sensor AI by 2027 — but that means Bosch building their own, not buying from startups.

### NXP

No significant vibration monitoring products identified.

---

## Complete Sensor Node Players ($200-1,000+ Per Unit)

These are the companies selling to end customers. They are our **potential customers** (they buy chips to put in nodes) or **competitors** (if we sell complete nodes).

### Tier 1 (Dominant Incumbents)

| Company | Products | Connectivity | Price Range | Notes |
|---------|----------|-------------|-------------|-------|
| SKF | Axios, Enlight Collect IMx-1, QuickCollect | LumenRadio proprietary, BLE | $300-800+ | Subscription model, cloud analytics |
| Fluke/Sensata | 3561, 3563 | BLE 4.1 + gateway | $600-800 starter kit | 2 MEMS + 1 piezo (analysis-grade) |
| Emerson | AMS9530 | WirelessHART mesh | $500-1000+ | 51.2 kHz sampling, highest in class |
| ABB | Ability Smart Sensor | BLE | $200-500 | Accel + magnetometer + ultrasonic mic, 5-15 year battery |
| Baker Hughes/Bently Nevada | Ranger Pro | Proprietary wireless | $1000+ | Oil & gas focus |
| Honeywell | Versatilis | LoRaWAN, BLE | $300-600 | 3-axis vib + temp + acoustics + ambient |

### Tier 2 (Disruptors)

| Company | Products | Connectivity | Price Range | Notes |
|---------|----------|-------------|-------------|-------|
| TRACTIAN | Smart Trac Ultra | Cellular | ~$100 mfg, $45/mo subscription | Avg customer: 60 sensors |
| Augury | Halo R4000 | BLE | Subscription | Edge AI, Baker Hughes partnership |
| Everactive | Batteryless sensor | BLE/gateway | Unknown | **Zero maintenance, 20-year life**, thermoelectric + PV harvesting, Fluke partnership |
| TE Connectivity | 8911 | LoRaWAN | $200-400 | Piezo, >10kHz, 5-year battery |
| Sensoteq | Kappa X | Unknown | Unknown | 25.6 kHz sampling, tiny 25mm footprint |
| Erbessd | Phantom | BLE 5.0 | $200-400 | 10kHz BW, 100K measurements/battery |
| Banner Engineering | QM42VT | Modbus RTU | $200-400 | RMS velocity + temp, IP67 zinc |

### Tier 3 (Software-First)

| Company | Approach | Notes |
|---------|----------|-------|
| Nanoprecise | Wireless sensors + analytics | Software differentiation |
| KCF Technologies | SmartDiagnostics platform | Analytics platform with sensors |
| Rockwell Automation | Dynamix | Integrated with Allen-Bradley PLCs |
| Siemens | Sitrans MS200 | Part of MindSphere/Xcelerator ecosystem |

---

## Typical Wireless Vibration Sensor Node BOM

Based on teardowns, reference designs, and component analysis:

| Component | Typical Parts | Cost |
|-----------|--------------|------|
| MEMS accelerometer (wideband) | ADXL1002 / IIS3DWB / SMA286 | $5-15 |
| Low-freq accel (optional 2nd axis) | ADXL355 / ISM330DHCX / ADXL362 | $3-10 |
| Piezo accel (optional, high-freq) | PCB 352C33 or similar | $30-80 |
| MCU/SoC | nRF52840 / Ambiq Apollo3 / STM32L4+ | $3-8 |
| External flash/SRAM (FFT buffer) | 384KB+ | $1-3 |
| Radio (if not in SoC) | SX1262 (LoRa) | $0-5 |
| ADC (if not in MCU) | ADS131M04 | $2-5 |
| Power management | LDO + battery management | $1-3 |
| Battery | CR2032 / 300-600mAh LiPo / 2×AA lithium | $1-5 |
| Antenna | Chip antenna | $0.50 |
| PCB + passives | Multi-layer, industrial grade | $3-8 |
| Enclosure | IP67, stainless steel or aluminum | $10-30 |
| Magnet/stud mount | Threaded or epoxy | $2-5 |
| **Total BOM** | | **$30-150** |
| **Selling price** | | **$200-1,000+** |

**Most common MCU + accelerometer combos:**
1. **nRF52840 + ADXL1002** — BLE vibration nodes (ADI provides Rust driver reference)
2. **nRF52840 + ADXL355** — low-power nodes, digital SPI interface
3. **Ambiq Apollo3 + ADXL1002** — ultra-low-power research designs
4. **STM32L4+ + IIS3DWB + ISM330DHCX** — STM's own reference platform
5. **TI CC2652R7 + TDK IIM-42352** — TDK i3 Micro Module

---

## Why Hasn't Someone Done This Already? (The Six Barriers)

### 1. Cannibalization Risk for Big Semis

ADI sells ADXL1002 ($10-15) AND ADcmXL3021 ($300+) per node. A $5-10 analog preprocessing chip would eliminate the need for the $300 module. Total revenue per node drops from $310 to $20. Same logic applies to STM: they sell MEMS ($9) + MCU ($3-8) = $12-17 per node. An analog chip that eliminates the MCU loses them $3-8 per node.

**Big semis won't cannibalize themselves. This is a startup opportunity.**

### 2. Analog ML Is a Different Competency

ADI employs the world's best precision analog designers. But "low noise, low offset, high linearity" is fundamentally different from "programmable analog classification." Analog ML is closer to neuromorphic computing than to amplifier design. It's a skill set that exists at Aspinity, POLYN, and a handful of academic labs — not in the product divisions of ADI or STM.

### 3. Market Size Is Too Small for Big Semis

Total chip TAM for vibration monitoring: ~$200-500M. That's a rounding error for ADI ($12B), STM ($16B), or TI ($18B). The minimum investment to develop, qualify, and sell a new analog ASIC is $10-50M. ROI doesn't justify it for a company with $10B+ revenue unless it's a platform that serves many markets.

### 4. Duty-Cycled Digital Is "Good Enough"

Most industrial customers tolerate 6-18 month battery life. They've been replacing batteries for years. The pain exists but it's manageable. The jump from "replace batteries yearly" to "never replace batteries" is compelling in theory but hard to sell when the customer's existing digital solution works and the vibration analysts trust FFT spectra.

### 5. Qualification Takes 2-5 Years

Industrial customers demand:
- Extended temperature range (-40 to +105°C)
- ATEX/IECEx certification (hazardous areas) for many applications
- IP67 environmental rating at the node level
- 2-5 year field trials before volume deployment
- Supply chain qualification (second source, longevity guarantee)

A startup needs 2-3 years of development + 2-5 years of qualification = 4-8 years to first real revenue.

### 6. Customer Inertia

Vibration analysts have been trained on FFT spectra for 30 years. An analog chip that outputs "anomaly/normal" without showing the frequency spectrum makes them uncomfortable. The education hurdle is real: you're not just selling a chip, you're changing how reliability engineers work.

Aspinity addresses this by outputting spectral bin data (not just binary). Our VibroSense-1 design does the same with 5 ISO 10816 band energies — giving analysts familiar features, not just a yes/no.

---

## Where VibroSense-1 Fits

| Dimension | POLYN | Aspinity AML100 | STM ISM330DHCX ML Core | **VibroSense-1** |
|-----------|-------|-----------------|----------------------|-----------------|
| Architecture | Neuromorphic (async op-amp neurons) | Configurable analog blocks | Digital decision tree on MEMS die | Gm-C filters + charge-domain MAC |
| Status | VAD shipped; vibration pre-production | Production Q1 2024 | Production | Design phase |
| Always-on power | 100 uW claimed (unverified) | ~36 uW | ~50-100 uW (MCU wakes) | **300 uW (honest, sky130)** |
| Classification | Binary (normal/fault) | Binary + basic anomaly | Decision tree (limited) | **4-class (normal, imbalance, bearing, looseness)** |
| Features extracted | Unknown | Proprietary analog | 6-axis motion features | **8 ISO 10816 features (5 bands + RMS + crest + kurtosis)** |
| Frequency range | Unknown | <10 kHz (AML100) | Limited by ODR | **100 Hz - 20 kHz (5 bands)** |
| Reprogrammable | Limited | Yes (RAMP) | Yes (firmware) | **Weights via SPI, tuning via SPI** |
| Price target | Unknown | $1-2 | $5-10 (sensor IC) | **$5-15 (chip), $150-300 (node)** |
| Model capacity | Unknown | ~10K params | <1K decisions | **128 caps (8×4-bit×4 classes)** |
| Process | 40-90nm | Proprietary | 28nm (ST) | **130nm sky130 (prototype)** |
| Open source | No | No | No | **Yes (fully open)** |

### Our Differentiators

1. **4-class fault identification** — not just "anomaly/normal." We tell you *what's wrong*: bearing damage, imbalance, looseness, gear fault. POLYN and Aspinity do binary only.

2. **ISO 10816 alignment** — the 5 frequency bands match what vibration analysts already use. This reduces the education barrier. Analysts see familiar features, not a black box.

3. **Fully open source** — first open-source analog AI sensor chip. Anyone can verify, reproduce, improve. This is a competitive moat against "trust us" proprietary chips.

4. **Honest specifications** — 300 uW, not a fantasy number. Verified on a real PDK with known model limitations documented.

5. **Node-level play** — sell sensor nodes at $150-300 with 75-90% margins, not chips at $1-2 with razor margins.

### Our Vulnerabilities

1. **Power is 3-9x worse than competitors' claims** (300 uW vs 36-100 uW). However, competitors' numbers are unverified or on proprietary processes.

2. **130nm sky130 is old.** Moving to 40nm or 28nm would cut power 2-4x but requires commercial PDK access.

3. **No piezoelectric support.** Analysis-grade sensors (Fluke 3563) use piezo for >10 kHz. Our MEMS-only chain tops out at 20 kHz with lower SNR than piezo.

4. **128-cap classifier is tiny.** More complex fault signatures (multi-fault, load-dependent patterns) may need more parameters.

5. **We're 4-8 years behind Aspinity** in production readiness and 2-3 years behind POLYN in silicon.

---

## The Strategic Bet

The bet is that **always-on + multi-class + ISO-aligned + open is worth 3-9x more power than always-on + binary + proprietary + black box.**

The market signal supporting this bet: **Everactive** (batteryless vibration sensor, energy harvesting, 20-year life, Fluke partnership) proves that customers DO pay a premium for maintenance-free sensing. If zero-maintenance matters, the jump from 12-month to 5-year battery life is worth the $5-15 chip premium.

The market signal against this bet: **STM's ISM330DHCX ML Core** is "good enough" for many customers, is already in production, costs $5-10, and doesn't require a new chip company. If on-sensor decision trees satisfy 80% of use cases, the remaining 20% may be too small to build a business on.

**The honest answer:** This is a niche play. The TAM for "always-on 4-class analog vibration classification" is probably $50-100M, not $500M. But at $5-15 ASP with 60-80% gross margins, $50M revenue on $100M TAM is a real business. And the node-level play ($150-300 per unit) can reach $75M revenue on 500K units/year.

---

## Sources

- ADI ADXL1002 datasheet: analog.com
- ADI ADcmXL3021: analog.com/en/products/adcmxl3021.html
- STM IIS3DWB datasheet: st.com
- STM ISM330DHCX: st.com/en/mems-and-sensors/ism330dhcx.html
- POLYN Technology: polyn.ai, CES 2026 announcements
- Aspinity AML100: aspinity.com/aml100
- Fluke 3563: fluke.com/en-us/product/condition-monitoring/vibration/3563
- SKF Enlight Collect: skf.com
- Emerson AMS9530: emerson.com
- ABB Ability Smart Sensor: new.abb.com
- Honeywell Versatilis: honeywell.com
- TRACTIAN: tractian.com
- Augury: augury.com
- Everactive: everactive.com
- TDK i3 Micro Module: invensense.tdk.com
- Bosch SMA286: bosch-semiconductors.com
- Coherent Market Insights: Predictive Maintenance Market 2025-2032
- Mordor Intelligence: Vibration Monitoring Market 2025-2030
