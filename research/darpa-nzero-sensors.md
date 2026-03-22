# DARPA N-ZERO: Near Zero Power RF and Sensor Operations

## The Program That Validated Always-On Analog Sensing

**Bottom line:** DARPA spent ~$30M over 5 years (2015-2020) to prove that analog/MEMS sensors can operate at 0-10 nanowatts in standby — 1,000x below state-of-the-art. They succeeded. Battlefield sensor lifetime jumped from weeks to 4+ years on a coin-cell battery. The core insight — use the signal's own energy to detect events, keeping digital systems asleep — is exactly the architecture our VibroSense-1 chip implements for vibration monitoring.

---

## 1. Program Overview

| Detail | Value |
|--------|-------|
| **Full name** | Near Zero Power RF and Sensor Operations (N-ZERO) |
| **Sponsoring office** | DARPA Microsystems Technology Office (MTO) |
| **Program manager** | Dr. Troy (Roy) H. Olsson III |
| **BAA number** | DARPA-BAA-15-14 |
| **Estimated budget** | ~$30M total |
| **Timeline** | 2015 (BAA issued January 2015) — May 2020 (program concluded) |
| **Status** | Complete. Content maintained for reference. |

### Three Phases

| Phase | Duration | Goal |
|-------|----------|------|
| Phase 1 | Oct 2015 — Dec 2016 (15 months) | Demonstrate sensor concepts, <10 nW standby, deliver to Lincoln Lab for evaluation |
| Phase 2 | 2017 (12 months) | Classify targets at >5 meter range |
| Phase 3 | 2018 (12 months) | Classify targets at >10 meter range, field demonstration |

### The Core Problem

Unattended ground sensors (UGS) deployed for military surveillance consumed milliwatts in standby — meaning coin-cell batteries lasted weeks, not years. Replacing batteries in hostile territory is dangerous and expensive. The sensors were always on, always listening, always draining power — even when nothing interesting was happening.

### The Core Insight

**Don't power the sensor. Let the signal power the sensor.**

N-ZERO called for "exploitation of the energy in the signal signature itself to detect and discriminate the events of interest while rejecting noise and interference." This requires passive or event-powered sensors and signal-processing circuitry — fundamentally analog approaches.

### Performance Targets

| Metric | Target | Achieved |
|--------|--------|----------|
| Standby power | <10 nW | 0–6 nW (Sandia achieved 6 nW, 40% better than goal) |
| Power reduction vs. state-of-art | 1,000x | >1,000x demonstrated |
| False alarm rate | <1/hour in urban environment | Demonstrated in field tests |
| Battery lifetime (coin cell) | Years | Up to 4 years (vs. 4 weeks prior) |
| RF receiver sensitivity | — | <-70 dBm (better than expected) |

---

## 2. Key Performers and Their Contributions

### Northeastern University — Zero-Power Infrared Sensing

**Lead:** Prof. Matteo Rinaldi, Department of Electrical and Computer Engineering

**Breakthrough:** Plasmonically Enhanced Micromechanical Photoswitches (PMPs)
- Published in *Nature Nanotechnology* 12, 969–973 (September 2017)
- Authors: Zhenyun Qian, Sungho Kang, Vageeswar Rajaram, Cristian Cassella, Nicol E. McGruer, Matteo Rinaldi

**How it works:**
1. Nanoscale plasmonic patches absorb specific infrared wavelengths
2. Absorbed IR energy creates plasmons (charge-based excitations) that trap light
3. Resulting heat causes physical deformation of micromechanical elements
4. Deformation closes an otherwise open circuit — a purely mechanical switch
5. **Zero standby power** — no current flows until IR target is detected

**Capabilities:**
- Detects specific IR signatures from heat sources (vehicle tailpipes, fires, humans)
- Multiple wavelength-tuned sensing elements enable complex logic analysis
- Can distinguish between vehicle types, fires, and persons based on infrared emission spectra
- Zero power consumption when target IR wavelengths are not present

**Significance:** This is a truly zero-power sensor — not "near zero," but actually zero. The energy comes entirely from the infrared signal being detected.

### UC Davis — Piezoelectric MEMS Accelerometer & Microphone

**Lead:** Prof. David Horsley, Department of Mechanical and Aerospace Engineering
**Co-PIs:** Xiaoguang "Leo" Liu, Rajeevan Amirtharajah (Electrical and Computer Engineering)
**DARPA grant:** $1.8M
**Project title:** "Ultralow Power Microsystems Via an Integrated Piezoelectric MEMS-CMOS Platform"
**Industry partner:** InvenSense (smartphone motion sensor company, now TDK InvenSense)

**Key achievements:**
- Sensors running at below 10 nanowatts — ~1,000,000x less power than smartphone sensors
- Delivered very-low-power acceleration sensor and microphone to Lincoln Lab (MIT) for independent evaluation
- Partnership with InvenSense ensured rapid transition path to production for DoD use

**Direct relevance to vibration monitoring:** The UC Davis team built exactly the kind of ultra-low-power piezoelectric MEMS accelerometer that could serve as a front-end for always-on vibration monitoring. Their 10 nW power target is 30,000x lower than our VibroSense-1 target of 300 uW.

### Sandia National Laboratories — MEMS + CMOS Wake-Up Sensor

**Key achievement:** Wakeup sensor consuming 6 nanowatts — 40% better than the 10 nW project goal
**Fabrication:** MESA-fabricated devices integrating MEMS and low-power CMOS
**Capability:** Detects acoustic and/or vibration signatures of interest, remains dormant otherwise

**Significance:** Sandia demonstrated that you can integrate MEMS sensing with CMOS decision-making at the 6 nW level. This is the purest validation that analog front-ends can operate at power levels that are essentially free — below the self-discharge rate of the battery.

### Charles Stark Draper Laboratory — Zero Power RF Receiver

**Contract:** HR0011-15-C-0138 (DARPA N-ZERO)
**Technology:** Zero-power RF wake-up receiver using high-Q MEMS demodulator
**How it works:**
1. High-Q MEMS demodulator filters an amplitude-modulated RF tone of interest from the spectrum
2. Produces a higher voltage signal suitable to trigger a high-Q MEMS resonant switch
3. Switch activates only on the specific RF signature of interest

**Achievement:** Zero-power receivers detecting signals below -70 dBm — better than originally expected by DARPA.

### Arm Research — M0N0 Ultra-Low-Power Processor

**Purpose:** Provide a processor capable of running alongside N-ZERO sensors
**Process node:** 65nm
**Architecture:** Cortex-M33 core (selected for SIMD extensions and dual memory buses)

| Parameter | Value |
|-----------|-------|
| Sleep power | 10 nW target |
| Active power | 20–60 uW/MHz depending on application |
| Keyword spotting power | ~50 mW at 2.5 MHz |
| Memory | Subthreshold mask ROM + custom low-leakage SRAM (fA/bit leakage) |
| Security | 256-bit AES encryption engine |
| Demonstration | 10-word keyword spotter, 1 classification/second |
| Battery life demo | 200 days continuous on LR44 coin cell (keyword spotting) |

**Key innovation:** Continuous voltage adaptation maintaining fixed minimum clock frequency for deterministic real-time response. Dynamic hardware power-gating with wake-on-access ROM.

**Commercial availability:** Arm made 1,000 M0N0 licenses available to U.S. government and government contractors.

### University of Virginia — VENUS System

**Project:** "Asleep Yet Aware, Awake on Declare — Virginia Efficient Near-zero Ultra-low-power System" (VENUS)
- Presented at DARPA ERI Summit
- Details in poster form (ERI Summit archives)

### Other Confirmed Performers

Based on contract numbers and publications:
- **Technion (Israel Institute of Technology)** — Listed in DARPA N-ZERO collaborations
- Multiple other university and industry teams (full performer list not publicly disclosed)

---

## 3. Sensor Modalities Demonstrated

N-ZERO demonstrated near-zero-power sensing across five modalities:

| Modality | Power Achieved | Key Demonstration | Performer |
|----------|---------------|-------------------|-----------|
| **Infrared (IR)** | Zero power | Vehicle/person classification by IR signature | Northeastern (Rinaldi) |
| **RF wake-up** | Zero power (passive) | <-70 dBm receiver sensitivity | Draper Laboratory |
| **Acoustic** | <10 nW | Resonant MEMS acoustic switch, 80 Hz @ 48 dB SPL | Multiple teams |
| **Vibration/Acceleration** | 5.4 nW | 26 V/g sensitivity at 160 Hz, generator detection | UC Davis (Horsley), Sandia |
| **Magnetic field** | Near-zero | 31 mV/Gauss sensitivity | Program teams |

### Acoustic MEMS Wake-Up Switch (Key Result)

A novel MEMS resonant acoustic wake-up switch was demonstrated:
- **Power:** Zero power while waiting; <10 nW when signal detected
- **Sensitivity:** Detected 80 Hz sound as low as 0.005 Pa rms (48 dB SPL)
- **Design:** Rotational design — insensitive to linear vibration and static gravity
- **Fabrication:** Silicon-on-insulator bonded wafers with metal-metal electrical contacts
- **Contract:** HR0011-15-C-0138

### Near-Zero Power Accelerometer Wake-Up System (Key Result for Vibration)

A piezoelectric MEMS accelerometer coupled with a CMOS comparator:
- **Power:** 5.4 nW before and after latching
- **Sensitivity:** 26 V/g at target frequency of 160 Hz
- **Material:** Aluminum nitride (AlN) for piezoelectric transduction
- **Demonstrated capability:** Wakes up to target frequency signature of a generator while rejecting background noise and non-target frequency signatures
- **Sensor bandwidth:** Physical signals from 5 Hz to 1.5 kHz
- **Load capacitance:** Up to 200 pF

### Zero-Power MEMS Vibration Switch

A complementary zero-power approach:
- **Power:** Absolute zero standby power
- **Mechanism:** Low-g triggered MEMS resonant acceleration switch
- **Actuation:** Ambient low-g vibration at resonant frequency
- **Threshold:** Closes under vibration at frequency as low as 39.3 Hz, acceleration threshold of 0.074 g
- **Application:** Wake-up trigger for more complex sensing systems

---

## 4. Program Results Summary

### What Succeeded

1. **1,000x power reduction validated.** Multiple teams demonstrated <10 nW standby — the original goal. Sandia hit 6 nW (40% better).

2. **Battery lifetime: 4 weeks to 4 years.** On a standard coin-cell battery, sensor lifetime extended by ~50x. This was the headline result.

3. **RF sensitivity exceeded expectations.** Zero-power receivers detected signals below -70 dBm — better than DARPA's original target.

4. **Multi-modal sensing proven.** RF, acoustic, IR, vibration, and magnetic field sensors all demonstrated at or near zero power.

5. **Vehicle classification at range.** Phase 1 demonstrated classification of cars, trucks, and generators at close range. Phase 2/3 targeted 5–10 meter range.

6. **Nature Nanotechnology publication.** Northeastern's IR sensor work was published in one of the world's highest-impact nanotechnology journals.

### What Was Most Successful

Per DARPA's own assessment: **"RF, acoustic, and infrared (IR) wake-up capabilities were the most successful sensing systems developed by the N-ZERO program."**

### The Fundamental Validation

N-ZERO proved that the "asleep-yet-aware" paradigm works:
- Analog/MEMS sensors can detect and classify events using near-zero or zero power
- The signal's own energy can trigger detection (IR, acoustic, vibration)
- Digital systems need only wake up when something interesting happens
- This extends battery lifetime by orders of magnitude

---

## 5. Follow-On Programs and Technology Transitions

### Direct Follow-On: No Single Named Successor

N-ZERO concluded in May 2020. Unlike some DARPA programs, there is no single named follow-on program. Instead, the technology transitioned in several directions:

### DARPA POWER (Persistent Optical Wireless Energy Relay)

While not a direct successor, POWER addresses the complementary problem: wirelessly delivering energy to remote sensors. In 2025, POWER achieved a record of 800+ watts delivered via laser over 8.6 km (5.3 miles). Combined with N-ZERO-class sensors, this could enable perpetual sensor networks.

### Technology Transitions Identified by DARPA

DARPA identified several transition paths for N-ZERO technology:
1. **IoT sensor networks** — Anticipated as the largest commercial use case
2. **Critical infrastructure monitoring** — Bridges, buildings, pipelines
3. **Agricultural monitoring** — Crop and soil sensors
4. **Structural health monitoring** — Untethered health monitoring of mechanical systems
5. **Medical devices** — Implantable and wearable sensors
6. **Climate monitoring** — Remote environmental stations
7. **Industrial control systems** — Equipment condition monitoring
8. **Automotive systems** — Vehicle health and security

### Commercial Products Influenced by N-ZERO

While not directly funded by N-ZERO, several commercial products embody its principles:

**Vesper Technologies — VM1010 ZeroPower Listening Microphone**
- Piezoelectric MEMS microphone with zero-power wake-on-sound
- 10 uA supply current (~18 uW) in listening mode
- Uses piezoelectric effect as acoustic switch — sound moves cantilever, generates voltage via piezoelectric effect, triggers wake-up comparator
- Received Alexa Voice Service certification
- Immune to dust, water, oils, humidity (piezoelectric advantage)
- Directly commercializes the N-ZERO concept for voice wake-up

**Aspinity AML100 — Analog Machine Learning Chip**
- Near-zero power always-on analog AI processing
- Reduces always-on system power by 95% (to <100 uA)
- Configurable analog blocks (CABs) for sensor interfacing + ML
- Keeps digital components in low-power mode until important data detected
- Applications: automotive security, biomedical, voice activation
- Embodies the N-ZERO principle: process in analog, wake digital only when needed

**TDK InvenSense** — Horsley's N-ZERO industry partner InvenSense (acquired by TDK) has integrated ultra-low-power wake-on-motion into commercial accelerometers used in billions of smartphones.

---

## 6. Direct Relevance to Vibration Monitoring (VibroSense-1)

### The N-ZERO Paradigm IS Our Architecture

The VibroSense-1 chip architecture directly implements the N-ZERO "asleep-yet-aware" paradigm:

| N-ZERO Principle | VibroSense-1 Implementation |
|-----------------|---------------------------|
| Analog front-end processes raw signal | MEMS accelerometer → analog PGA → Gm-C filter bank |
| Signal energy used for detection | Piezoelectric accelerometer generates voltage from vibration |
| Classification before digitization | Analog envelope detectors + charge-domain MAC classifier |
| Digital wakes only on event | MCU sleeps until anomaly flag asserts |
| Near-zero standby power | 300 uW always-on analog (vs. 3-10 mW for MCU+FFT) |

### Key N-ZERO Results Directly Applicable to Vibration

1. **5.4 nW accelerometer wake-up system at 160 Hz** — Falls within our BPF1 band (100-500 Hz). Proves piezoelectric MEMS can detect vibration signatures at nanowatt power levels.

2. **26 V/g sensitivity** — Extremely high sensitivity enables detection of small vibration anomalies without amplification power.

3. **Generator detection demonstrated** — N-ZERO teams demonstrated detection and classification of different operational modes (On/Off/Eco) of a portable electrical generator. This is exactly vibration-based equipment monitoring.

4. **0.074 g threshold at 39.3 Hz** — Zero-power MEMS switch that triggers on low-frequency vibration. This is in the range of industrial rotating machinery (motors, pumps, fans).

5. **Acoustic classification at range** — Vehicles classified by acoustic signature at 5-10 meters. The same principle applies to classifying machine faults by vibration signature.

6. **5 Hz to 1.5 kHz sensor bandwidth** — Covers the critical ISO 10816 vibration frequency range for rotating machinery.

### Power Budget Comparison

| Approach | Always-On Power | Battery Life (CR2032) |
|----------|----------------|----------------------|
| N-ZERO sensor (nanowatt wake-up) | 5-10 nW | 10+ years (limited by self-discharge) |
| VibroSense-1 (analog signal chain) | ~300 uW | ~3 months |
| MCU + FFT (digital approach) | 3-10 mW | 1-3 days |
| Conventional wireless vibration sensor | 50-100 mW | Hours (duty-cycled to weeks) |

Our 300 uW target is 30,000x higher than N-ZERO's nanowatt sensors — but that's because we do continuous spectral decomposition and classification, not just wake-up detection. The point is that N-ZERO proved the fundamental principle: analog processing before the ADC saves orders of magnitude of power.

---

## 7. How to Cite N-ZERO to Validate Our Approach

### The Argument Chain

1. **DARPA validated the principle** (2015-2020, ~$30M): Analog/MEMS front-ends can detect and classify physical signals at 0-10 nW, extending battery life by 50-100x.

2. **The key insight is universal:** Processing signals in the analog domain before digitization eliminates the power cost of ADC + DSP for the vast majority of uninteresting data.

3. **N-ZERO demonstrated this for vibration specifically:** Piezoelectric MEMS accelerometers at 5.4 nW detected generator operational modes. MEMS switches triggered on vibration at 39.3 Hz and 0.074 g.

4. **VibroSense-1 extends this to continuous classification:** Rather than simple wake-up, we perform spectral decomposition and multi-class fault detection — all in analog, at 300 uW.

5. **The power hierarchy is validated:**
   - Zero-power wake-up: N-ZERO (0-10 nW) — detects presence of vibration
   - Always-on analog classification: VibroSense-1 (300 uW) — classifies fault type
   - Digital processing: MCU+FFT (3-10 mW) — full spectral analysis on demand
   - Each tier adds capability at ~100-1,000x power cost

### Citable Claims

- "DARPA's N-ZERO program (2015-2020, ~$30M) demonstrated that analog/MEMS sensors can maintain always-on awareness at 0-10 nW standby power, extending unattended sensor lifetime from weeks to 4+ years on coin-cell batteries." (Source: DARPA program page, EE Times)

- "N-ZERO specifically demonstrated piezoelectric MEMS accelerometer wake-up at 5.4 nW with 26 V/g sensitivity at 160 Hz, including classification of generator operational modes." (Source: IEEE Sensors 2017)

- "The N-ZERO principle — analog sensing and classification before digitization — is the same architectural approach used in always-on vibration monitoring, where analog filter banks and envelope detectors replace power-hungry FFT computations." (Our synthesis)

- "Sandia National Laboratories achieved 6 nW standby power (40% below the 10 nW target) using integrated MEMS + CMOS sensors that detect acoustic and vibration signatures of interest." (Source: Sandia Labs Accomplishments 2017)

### Key Publications to Reference

1. Z. Qian, S. Kang, V. Rajaram, C. Cassella, N.E. McGruer, M. Rinaldi, "Zero-power infrared digitizers based on plasmonically enhanced micromechanical photoswitches," *Nature Nanotechnology* 12, 969–973 (2017).

2. R.H. Olsson III et al., "Zero and Near Zero Power Intelligent Microsystems," *J. Phys.: Conf. Ser.* 1407, 012042 (2019).

3. Near-zero power accelerometer wakeup system, *IEEE Sensors 2017* (UC Davis / Sandia teams).

4. B. Griffin, "Near Zero Power Sensor Operations (N-ZERO)," Sandia National Laboratories, SAND2017-11531D (2017).

---

## 8. The Catch: What N-ZERO Did NOT Solve

### Wake-Up vs. Continuous Monitoring

N-ZERO sensors are **event detectors**, not continuous monitors. They answer "is something happening?" not "what kind of fault is developing?" The gap between a 10 nW wake-up trigger and a 300 uW continuous classifier is where the engineering challenge lives.

### Limited Classification Capability

N-ZERO sensors classify simple events (vehicle type, generator on/off). They do not perform the kind of multi-class fault detection (imbalance vs. bearing fault vs. looseness vs. misalignment) that industrial vibration monitoring requires. That requires our more complex analog signal chain.

### Environment and Reliability

N-ZERO was demonstrated in controlled field tests. Industrial environments have:
- Continuous vibration (not infrequent events)
- Multiple simultaneous sources
- Temperature extremes and electromagnetic interference
- Requirements for quantitative severity assessment, not just detection

### Precision vs. Power Tradeoff

N-ZERO's nanowatt sensors achieve detection but not measurement. They can tell you a vehicle is present but not its speed. They can detect vibration but not measure its amplitude with precision. Our VibroSense-1 needs to quantify vibration severity with enough precision to trigger maintenance actions — that requires more power.

### No Commercial Vibration Products Yet

Despite N-ZERO concluding in 2020, no commercial always-on vibration monitoring product has emerged directly from the program. The technology has influenced designs (Vesper, Aspinity, TDK InvenSense) but the specific application to industrial predictive maintenance remains an open opportunity.

---

## 9. The Bigger Picture: DARPA's Sensor Power Programs

| Program | Focus | Timeline | Budget | Key Result |
|---------|-------|----------|--------|------------|
| **N-ZERO** | Near-zero-power sensors | 2015-2020 | ~$30M | 0-10 nW standby, 4-year battery life |
| **POWER** | Wireless power beaming | 2023-present | — | 800W over 8.6 km via laser |
| **OPTIMA** | Analog AI accelerators | 2023-present | $78M | Analog compute-in-memory for inference |
| **ERI** | Electronics Resurgence Initiative | 2017-present | $1.5B+ | Broad microelectronics R&D |

N-ZERO sits at the foundation of DARPA's vision for persistent, autonomous sensing:
1. **N-ZERO** proved you can sense at near-zero power (the front-end)
2. **OPTIMA** is proving you can compute at ultra-low power (analog CIM for inference)
3. **POWER** is solving the energy delivery problem (wireless power to remote nodes)
4. Together, they enable a future of perpetual, intelligent, autonomous sensors

---

## 10. Summary: What N-ZERO Means for Us

**N-ZERO is the strongest government validation that analog-first sensing works.**

The U.S. Department of Defense invested ~$30M and 5 years to answer the question: "Can analog/MEMS sensors eliminate the power cost of always-on digital processing?" The answer was an unambiguous yes. Multiple independent teams at Northeastern, UC Davis, Sandia, Draper, Arm, and UVA demonstrated sensors operating at 0-10 nW — a 1,000x improvement over digital alternatives.

For our VibroSense-1 chip:
- N-ZERO validates the fundamental principle (analog before digital saves power)
- N-ZERO demonstrated vibration sensing specifically (5.4 nW accelerometer, generator classification)
- N-ZERO showed the technology is production-viable (InvenSense partnership, Arm processor, Sandia fabrication)
- Our 300 uW target sits in the validated power regime between N-ZERO wake-up (nW) and digital processing (mW)

**The question is no longer "does analog sensing work?" — DARPA answered that. The question is "can we build a commercially viable product around it?" That's what VibroSense-1 aims to answer.**

---

## Sources

- [DARPA N-ZERO Program Page](https://www.darpa.mil/research/programs/near-zero-rf-and-sensor-operations)
- [DARPA: "N-ZERO Envisions Asleep-yet-Aware Electronics" (2015)](https://www.darpa.mil/news/2015/n-zero-aware-electronics)
- [DARPA: "Dormant, Yet Always-Alert Sensor" (2017)](https://www.darpa.mil/news-events/2017-09-11)
- [EE Times: "DARPA Research Advances for Near-Zero-Power Sensors"](https://www.eetimes.com/darpa-research-advances-for-near-zero-power-sensors/)
- [FedTech: "Military IoT: DARPA's N-ZERO Initiative"](https://fedtechmagazine.com/article/2017/06/military-iot-darpas-n-zero-initiative-aims-conserve-power-iot-sensors)
- [Sandia Labs: Microsystems Accomplishments 2017](https://www.sandia.gov/news/publications/labs-accomplishments/article/2017/microsystems/)
- [UC Davis MEMS Lab: N-ZERO Grant](https://memslab.ucdavis.edu/research-team-secures-darpa-n-zero-grant/)
- [The Aggie: "DARPA Grants UC Davis Researchers $1.8 Million"](https://theaggie.org/2015/11/24/darpa-grants-uc-davis-researchers-1-8-million-to-innovate-sensor-technology/)
- [Nature Nanotechnology: Zero-Power IR Digitizers (2017)](https://www.nature.com/articles/nnano.2017.147)
- [Northeastern University: "Sensing Without Consuming Power"](https://coe.northeastern.edu/news/sensing-without-consuming-power-groundbreaking-work-showcased-in-nature-nanotechnology/)
- [Arm Research: M0N0 Platform for N-ZERO Sensors](https://developer.arm.com/community/arm-research/b/articles/posts/m0n0-an-arm-research-platform-for-n-zero-sensors)
- [DTIC: M0N0 Ultra Low Power Sub-threshold Microcontroller](https://apps.dtic.mil/sti/pdfs/AD1076258.pdf)
- [Olsson et al., "Zero and Near Zero Power Intelligent Microsystems," J. Phys.: Conf. Ser. 1407, 012042 (2019)](https://iopscience.iop.org/article/10.1088/1742-6596/1407/1/012042)
- [Federal Grants Wire: N-ZERO BAA-15-14](https://www.federalgrantswire.com/near-zero-power-rf-and-sensor-operations-darpa-baa-15-14.html)
- [Vesper VM1010 ZeroPower Listening](https://www.digikey.com/en/product-highlight/v/vesper/vm1010-zeropower-listening-piezoelectric-mems-microphones)
- [Aspinity AML100 Analog ML Chip](https://www.aspinity.com/aml100/)
- [OSTI: Sandia N-ZERO Publication SAND2017-11531D](https://www.osti.gov/biblio/1480176)
- [USPTO: Zero Power RF Receiver (Draper Laboratory)](https://uspto.report/patent/app/20170126263)
- [ResearchGate: Resonant Acoustic MEMS Wake-Up Switch](https://www.researchgate.net/publication/325055341_Resonant_Acoustic_MEMS_Wake-Up_Switch)
- [IEEE: Near-Zero Power Accelerometer Wakeup System](https://ieeexplore.ieee.org/document/8234277/)
- [MDPI: Broadband Zero-Power Wakeup MEMS Device](https://www.mdpi.com/2072-666X/13/3/407)
