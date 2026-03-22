# Everactive: The Batteryless Vibration Sensor Company

*Last updated: 2026-03-22*

Everactive (formerly PsiKick) represents a fundamentally different approach to the "maintenance-free sensing" problem. Instead of making the chip ultra-low-power and stretching battery life (the VibroSense-1 approach), Everactive eliminates the battery entirely by harvesting energy from the environment. Both approaches target the same customer pain point — the $500K-1M/year cost of replacing batteries on thousands of industrial sensors — but they arrive at the solution from opposite directions.

**The verdict: Everactive's approach works, is shipping, and has real customers. But the 1 kHz bandwidth ceiling imposed by its power budget makes it a screening tool, not a diagnostic tool. VibroSense-1's analog preprocessing approach can deliver 10-20x more bandwidth within the same harvested power envelope, making "batteryless + diagnostic-grade" possible in theory.**

---

## Company Overview

| Field | Detail |
|-------|--------|
| **Founded** | 2012 (as PsiKick), rebranded Everactive 2019 |
| **Headquarters** | Santa Clara, CA (chip); Ann Arbor, MI (IMS division, now sold) |
| **Founders** | Benton Calhoun (UVA prof), David Wentzloff (U Michigan prof) |
| **Academic roots** | Both founders PhD students of Anantha Chandrakasan at MIT |
| **Total funding** | ~$161M over 11 rounds |
| **Key investors** | Fluke Corporation (led Series C), New Enterprise Associates, 40 North Ventures, TOP Ventures, Asahi Kasei |
| **Employees** | ~80-120 (estimated) |
| **Products** | Eversensors (batteryless), Evercloud (analytics platform), Evernet (wireless protocol) |
| **Applications** | Machine health monitoring (vibration), steam trap monitoring, environmental monitoring |
| **Customers** | 3M, Colgate-Palmivle, Hershey's, Merck, U.S. government, universities |
| **Key partnerships** | Fluke Reliability (Fluke 3562 sensor), Rockwell Automation (FactoryTalk integration) |

### Major Events Timeline

| Date | Event |
|------|-------|
| 2012 | PsiKick founded by Calhoun & Wentzloff |
| 2014 | Brendan Richardson joins as CEO |
| 2018 | First product: Steam Trap Monitor (STM) |
| 2019 | Rebranded to Everactive; raised $30M |
| 2020 | Machine Health Monitoring product launched; Fluke leads Series C |
| 2021 | $35M oversubscribed Series C extension; Fluke partnership (3562 sensor); Rockwell Automation partnership |
| Aug 2024 | $10.9M additional funding round |
| Sep 2025 | PKS3000 SoC presented at Hot Chips 2025 |
| Feb 2025 | Shoplogix acquires Everactive's Industrial Monitoring Services (IMS) division |

**The IMS sale is notable.** Everactive sold its services/deployment arm to Shoplogix (part of Juniper Group) while retaining its semiconductor IP. This suggests either a strategic refocus on chip sales, or financial pressure requiring asset sales. Either way, the company is now primarily a silicon + platform company, not a full-stack IoT services company.

---

## The Chip: PKS3000 SoC

Presented at Hot Chips 2025, the PKS3000 is Everactive's third-generation self-powered SoC. This is the core technology that makes batteryless sensing possible.

### PKS3000 Specifications

| Parameter | PKS3000 (Gen 3) | PKS2001 (Gen 2) |
|-----------|-----------------|-----------------|
| **Process** | 55 nm ULP | 55 nm ULP |
| **Die size** | 6.7 mm² | — |
| **CPU** | ARM Cortex-M0+ | ARM Cortex-M0+ |
| **Clock speed** | 5 MHz | — |
| **SRAM** | 128 KB | — |
| **Flash** | 256 KB | — |
| **Power floor (idle)** | 2.19 uW | 30 uW |
| **Power with wake-up radio** | <4 uW | — |
| **Active power (5 MHz)** | 12 uW | 89.1 uW |
| **EH-PMU topology** | MISIMO (Multiple Input, Single Inductor, Multiple Output) | — |
| **EH inputs** | 2 simultaneous (PV + TEG) | — |
| **Output voltage rails** | 4 (1.8V, 1.2V, 0.9V, adj) | — |
| **Cold-start** | 60 lux + 8 deg C delta with PV/TEG combo | — |
| **Wake-up radio (passive)** | -63 dBm, <1 uW, ~200m range | — |
| **Wake-up radio (active)** | -92 dBm, <6 uW avg, >1000m range | — |
| **Radio frequency** | 300 MHz to 3 GHz (sub-GHz proprietary Evernet) | — |

**Key insight:** The 14x reduction from PKS2001 idle (30 uW) to PKS3000 idle (2.19 uW) is the generational improvement that makes batteryless vibration monitoring viable. At 30 uW idle, you need a large TEG or bright light. At 2.19 uW idle, you can start from dim indoor light (60 lux) or a small temperature differential (8 deg C).

### Energy Harvesting Power Management Unit (EH-PMU)

The PKS3000 integrates the power management on-die with a MISIMO (Multiple Input, Single Inductor, Multiple Output) converter. This is significant — most energy harvesting designs use discrete PMIC chips (e.g., from e-peas or Texas Instruments). Integrating the PMU on-chip:

1. Eliminates board-level power conversion losses
2. Reduces BOM cost
3. Allows tighter control of power state transitions
4. Enables rapid switching between harvesting sources

The EH-PMU accepts two simultaneous DC inputs (photovoltaic cell + thermoelectric generator) and produces four regulated output rails. This dual-source approach is critical: TEGs work when the machine is running (hot surface), PV works in lit areas. Together, they provide better availability than either alone.

---

## How Energy Harvesting Works (And Its Limits)

### Thermoelectric Generators (TEGs)

**Principle:** Seebeck effect — a temperature differential across two dissimilar conductors generates a voltage. In industrial settings, the "hot" side is the machine surface (motor housing, pump casing, bearing housing), and the "cold" side is ambient air.

**Typical harvested power:**

| Temperature Delta | Typical TEG Output |
|------|------|
| 5 deg C | ~5-20 uW/cm² |
| 10 deg C | ~20-80 uW/cm² |
| 20 deg C | ~80-300 uW/cm² |
| 50 deg C | ~500-2000 uW/cm² |

**Industrial reality:** Most rotating equipment runs 10-30 deg C above ambient. A 2-3 cm² TEG module on a motor housing typically yields **20-200 uW**. This is the fundamental power budget that constrains what Everactive's sensor can do.

**The catch:** TEG output drops if:
- The machine is idle (no heat) — sensor has 8 hours of stored energy to ride through
- Ambient temperature is high (summer, hot climates) — reduced delta
- The mounting surface has poor thermal conductivity
- Dust/insulation covers the cold side (reduced heat sinking)

### Photovoltaic (PV) Cells

**Indoor light harvesting** at typical industrial lighting (200-500 lux):
- ~10-50 uW/cm² (amorphous silicon cells)
- Higher efficiency GaAs cells can reach ~100 uW/cm² at 500 lux

**The catch:** Many industrial environments have:
- Intermittent lighting (night shifts, weekends)
- Oil/dust film on PV cells reducing output
- Sensor mounted inside enclosures with no light

### Combined Power Budget

**Realistic total harvest: 20-300 uW**, depending on environment. The Fluke 3562 spec confirms this implicitly: the TEG harvester requires a minimum -9 deg C temperature differential, and the PV harvester needs minimum 200 lux.

**Energy storage:** The Fluke 3562 has 8 hours of stored energy at 60-second sample rate when no power source is available. This means a supercapacitor or thin-film battery buffer — likely storing ~0.5-2 J.

---

## Vibration Monitoring Specifications

### Fluke 3562 (Powered by Everactive Edge)

This is the shipping product — the best public source for Everactive's actual vibration capabilities.

| Parameter | Specification |
|-----------|--------------|
| **Accelerometer** | Triaxial MEMS |
| **Frequency range** | 6 Hz to 1,000 Hz |
| **Sampling frequency** | 3,200 Hz (Nyquist: 1,600 Hz, effective to ~1 kHz) |
| **Amplitude range** | Auto-range: +/- 2g; extended: 4g, 16g |
| **Vibration output** | Velocity (IPS peak) per axis |
| **FFT processing** | On-device; transmits 9 highest peaks per axis |
| **Sampling interval** | 60 seconds (configurable) |
| **Additional sensors** | Ambient temp, remote temp, magnetic field, humidity |
| **Operating temp (sensor)** | -40 deg C to 85 deg C |
| **TEG operating temp** | -40 deg C to 75 deg C |
| **PV operating temp** | -10 deg C to 60 deg C |
| **Wireless range (NLOS)** | 250 m (820 ft) |
| **Wireless range (LOS)** | 1 km (0.6 mi) |
| **Sensors per gateway** | Up to 1,000 |
| **Ingress protection** | IP66 |
| **Hazardous area** | Class 1, Division 2 |
| **Dimensions** | 53 x 48 x 81 mm |
| **Weight** | 180 g |
| **Power source** | TEG (min -9 deg C delta) or PV (min 200 lux) |
| **Energy reserve** | 8 hours at 60-second sample rate |

### What the Specs Mean

**The 1 kHz bandwidth is the critical limitation.**

ISO 10816 measures overall vibration severity in the 10-1,000 Hz band. For machine "screening" — answering "is this machine getting worse?" — 1 kHz is sufficient. This is what Everactive does: it's a screening tool that identifies machines needing attention.

**What 1 kHz cannot do:**

| Fault Type | Characteristic Frequency | Detectable at 1 kHz? |
|------------|------------------------|---------------------|
| Shaft imbalance | 1x RPM (10-100 Hz) | YES |
| Misalignment | 2x-3x RPM (20-300 Hz) | YES |
| Looseness | Harmonics of RPM (<500 Hz) | YES |
| Gear mesh | Teeth x RPM (500-5,000 Hz) | PARTIAL |
| Bearing outer race | BPFO (typically 2-10 kHz) | NO |
| Bearing inner race | BPFI (typically 3-15 kHz) | NO |
| Bearing ball | BSF (typically 5-20 kHz) | NO |
| Lubrication issues | Ultrasonic range (>20 kHz) | NO |

**Bearing faults are the #1 cause of rotating equipment failure.** Early bearing defect detection requires envelope analysis of high-frequency impulse signatures, typically in the 2-20 kHz range. The sampling rate needed is 25.6 kS/s or higher. Everactive's 3.2 kS/s sampling rate is an order of magnitude too low.

**Everactive's positioning is honest about this.** They market the sensor as a "screening" tool that complements (not replaces) traditional vibration analysis. The Fluke partnership is strategic: Fluke sells both the batteryless 3562 screening sensor AND the battery-powered 3563 analysis sensor (which samples at 51.2 kS/s, bandwidth to 20 kHz). The intended workflow:

1. Deploy 1,000 Everactive 3562 sensors on every motor in the plant (screening)
2. When a sensor flags a machine as trending bad, send a tech with a Fluke 810 analyzer or install a Fluke 3563 on that specific machine (diagnosis)
3. This is the "pyramid" monitoring strategy: cheap broad screening at the base, expensive deep analysis at the top

### Data Transmission: 9 FFT Peaks Per Axis

The sensor doesn't transmit raw waveforms or full FFT spectra. It runs an on-device FFT and transmits only the 9 highest-magnitude peaks per axis per 60-second sample. This is aggressive compression driven by the radio power budget:

- Full 1,600-point FFT spectrum = ~6,400 bytes
- 9 peaks x 3 axes x (frequency + magnitude) = ~108 bytes
- ~60x data reduction

This means the cloud analytics platform works with sparse spectral data, not raw vibration signals. Sufficient for trending and alarm-setting, insufficient for detailed spectral analysis.

---

## The Fluke Partnership

### Structure

- **Fluke led Everactive's Series C** ($35M, September 2020)
- **Fluke CEO Marc Tremblay** joined Everactive's board
- **Product integration:** Fluke 3562 Screening Vibration Sensor is powered by Everactive Edge technology
- **Distribution:** Sold through Fluke's existing industrial sales channels
- **Cloud integration:** Data feeds into Fluke's condition monitoring platform

### Strategic Logic

Fluke is the dominant brand in industrial test & measurement. Their traditional vibration business is handheld analyzers and route-based monitoring — expensive tools used by skilled technicians. Everactive gives them entry into the wireless continuous monitoring market without competing with their own high-end analysis tools:

- **Fluke 3562** (Everactive-powered): $XXX per sensor, batteryless, screening, 1 kHz
- **Fluke 3563**: ~$1,000+ per sensor, battery-powered, analysis-grade, 20 kHz, waveform + spectrum
- **Fluke 810 Vibration Tester**: ~$8,000, handheld, route-based

The 3562 doesn't cannibalize the 3563 because it targets different assets (non-critical motors vs. critical machinery) and different use cases (screening vs. diagnosis).

### Rockwell Automation Partnership

Everactive's data integrates with Rockwell's FactoryTalk MaintenanceSuite. This is significant because Rockwell has the largest installed base of industrial automation systems. Integration with FactoryTalk means Everactive data shows up in the same dashboard plant operators already use, reducing adoption friction.

---

## Customer Traction & Business

### Known Customers

| Customer | Application | Scale |
|----------|------------|-------|
| 3M | Machine health | Multi-site |
| Colgate-Palmolive | Machine health | Multi-site |
| Hershey's | Machine health | Multi-site |
| Merck | Machine health / pharma | Multi-site |
| U.S. Government | Multiple | Unknown |
| Multiple universities | Research / pilot | Small |

### Revenue

Not publicly disclosed. Given $161M raised and no profitability announcement, the company is likely pre-profitable. The IMS division sale to Shoplogix (Feb 2025) suggests either strategic refocus or capital needs.

**Comparison to sector:** Mythic AI (analog CIM) reported $6.4M revenue with $300M+ raised. Analog sensor/edge companies are uniformly pre-revenue or early-revenue relative to funding.

### The IMS Division Sale

In February 2025, Shoplogix (part of Juniper Group's Smart Factory portfolio) acquired Everactive's Industrial Monitoring Services division. This was the team that deployed, managed, and serviced sensor networks for customers. After the sale:

- **Everactive retains:** SoC design, chip IP, Evernet protocol, cloud platform
- **Shoplogix gets:** Customer relationships, field deployment team, services revenue

This split could mean Everactive is pivoting to a pure semiconductor/platform licensing model (selling chips + cloud to OEMs like Fluke) rather than doing end-to-end deployments. Or it could mean the services business wasn't profitable enough to sustain.

---

## Technical Assessment: Batteryless vs. Always-On Analog

### The Fundamental Tradeoff

| Dimension | Everactive (Batteryless) | VibroSense-1 (Always-On Analog) |
|-----------|------------------------|-------------------------------|
| **Power source** | Harvested (TEG + PV), 20-300 uW | Battery, 300-600 uW (from chip) + sensor + radio |
| **Battery life** | Infinite (no battery) | 5+ years (with duty cycling of radio) |
| **Maintenance** | Zero | Near-zero (battery swap every 5-10 years) |
| **Vibration bandwidth** | 1 kHz | 20 kHz (5 filter bands to 20 kHz) |
| **Sampling** | 3.2 kS/s, periodic (every 60s) | Continuous, always-on |
| **Signal processing** | Digital FFT on ARM Cortex-M0+ | Analog filter bank + envelope detection |
| **Classification** | Cloud-based (data sent to cloud) | On-chip (charge-domain MAC classifier) |
| **Latency to detection** | 60 seconds + cloud processing | <100 ms (analog processing) |
| **Bearing fault detection** | NO (below Nyquist) | YES (BPF4: 5-10 kHz, BPF5: 10-20 kHz) |
| **Process** | 55 nm ULP | 130 nm (Sky130) |
| **Chip cost** | ~$3-8 (estimated, 55nm, 6.7mm²) | ~$1-3 (130nm, ~4mm² target) |
| **System cost** | Higher (TEG + PV harvester modules) | Lower (standard battery) |
| **Deployment constraint** | Needs heat source or light | None (battery works everywhere) |
| **Data richness** | 9 FFT peaks per axis per minute | 8 analog features + anomaly flag, continuous |

### Where Everactive Wins

1. **True zero maintenance.** No battery means no battery replacement. For 10,000+ sensor deployments, this eliminates a massive operational cost. VibroSense-1's 5-10 year battery is great, but eventually someone has to change it.

2. **Proven and shipping.** The Fluke 3562 is a real product with real customers. VibroSense-1 is a design in simulation. This is the most important advantage.

3. **Fluke + Rockwell ecosystem.** Everactive has distribution through the two most important names in industrial maintenance. Channel access is worth more than technical specifications.

4. **Scalable deployment.** 1,000 sensors per gateway, no wiring, no batteries. Install and forget. This enables covering every motor in a plant, not just the critical ones.

### Where Everactive Loses

1. **1 kHz bandwidth is a diagnostic dead end.** Cannot detect bearing faults, the #1 failure mode. Can only screen for low-frequency problems (imbalance, misalignment, looseness). This is by design — it's a screening tool — but it means Everactive can never replace traditional vibration analysis, only supplement it.

2. **60-second sampling interval.** Intermittent monitoring misses transient events. A bearing that produces impulse signatures for 2 seconds every 5 minutes will be caught by a continuous always-on system but might be missed by periodic sampling that captures 1 second every 60 seconds.

3. **Cloud-dependent classification.** The sensor sends raw FFT peaks to the cloud; intelligence lives in the cloud analytics platform. This means: (a) latency of minutes to hours for anomaly alerts, (b) ongoing cloud subscription revenue dependency, (c) doesn't work offline. VibroSense-1 classifies on-chip with <100 ms latency.

4. **Deployment constraints.** TEG requires a machine that runs warm. PV requires light. In a dark, ambient-temperature environment (e.g., cold warehouse, underground, inside a cabinet), the sensor doesn't work. Battery-powered sensors work everywhere.

5. **Sparse data.** 9 FFT peaks per axis per minute is extremely compressed. Trending works; root cause analysis doesn't. The cloud analytics can identify "this machine is getting worse" but can't always tell you why.

6. **System cost.** The TEG module, PV cell, and enclosure with IP66/Class 1 Div 2 rating add significant BOM cost. The Fluke 3562 likely costs $300-800 per sensor node (pricing not public but comparable to high-end wireless vibration sensors). A VibroSense-1 node with a coin cell could be built for $50-150.

---

## Could VibroSense-1 + Energy Harvesting = Best of Both Worlds?

This is the key strategic question. If VibroSense-1 consumes 300 uW (target) to 600 uW (hard limit), and energy harvesting yields 20-300 uW, there's an apparent gap. But let's look more carefully.

### Power Budget Analysis

**Everactive's power breakdown (estimated from PKS3000 specs):**

| Function | Power |
|----------|-------|
| SoC idle (always-on) | ~2-4 uW |
| Wake-up radio (listening) | ~2-6 uW |
| Accelerometer (active during sample) | ~10-50 uW |
| ARM M0+ running FFT (active, 1 sec) | ~12-50 uW |
| Radio transmit (burst, ~100 ms) | ~500-2000 uW |
| **Average power (60s cycle)** | **~10-30 uW** |

Everactive achieves low average power by duty cycling: sense for ~1 second, compute for ~0.5 second, transmit for ~0.1 second, sleep for ~58 seconds. The **peak power during active sensing + FFT + transmit is milliwatts**, but averaged over the 60-second cycle, it's tens of microwatts.

**VibroSense-1's power breakdown:**

| Function | Power |
|----------|-------|
| Analog front-end (continuous) | ~50 uW |
| Filter bank (5 BPFs, continuous) | ~24 uW |
| Envelope detectors (continuous) | ~25 uW |
| RMS/crest/kurtosis (continuous) | ~30 uW |
| Classifier (continuous) | ~20 uW |
| Bias + references | ~30 uW |
| Digital control (idle) | ~10 uW |
| Leakage | ~65 uW |
| **Total always-on** | **~300 uW** |

### The Gap and How to Close It

VibroSense-1 at 300 uW continuous is ~10x more than what a typical energy harvester provides (20-50 uW in dim/cool conditions). But:

**Option A: Duty-cycle the analog chain (defeats the purpose)**

If we duty-cycle VibroSense-1 to 10% duty cycle (1 second on, 9 seconds off), average power drops to ~30 uW — within harvesting range. But this loses the "always-on" advantage and becomes similar to Everactive's approach, just with better bandwidth during the active window.

**Option B: Larger harvesters**

A 10 cm² TEG module on a warm machine (delta-T = 20 deg C) can provide ~300-500 uW. This matches VibroSense-1's continuous budget. But 10 cm² is a large harvester — the sensor node becomes bulky.

**Option C: Hybrid approach (most promising)**

- VibroSense-1 runs in "light sleep" mode: only BPF1-BPF2 active (low-frequency screening, ~30 uW) — detects imbalance and misalignment
- When BPF1-BPF2 detect anomalous energy, wake up BPF3-BPF5 (high-frequency analysis) for 5-10 seconds (~300 uW burst)
- Average power in normal operation: ~35-50 uW (within harvesting budget)
- Average power when fault detected: ~100-150 uW (short bursts, still within budget of moderate TEG)

This "hierarchical wake-up" approach gives:
- Continuous low-frequency monitoring (better than Everactive's 60-second sampling)
- On-demand high-frequency bearing analysis (which Everactive cannot do at all)
- Average power compatible with energy harvesting

**Option D: Next-generation process (future)**

VibroSense-1 on Sky130 (130 nm) targets 300 uW. On 55 nm ULP (Everactive's process), the same design could achieve 100-150 uW through:
- Lower supply voltage (0.9V vs 1.8V, ~4x power reduction in digital, ~2x in analog)
- Smaller transistors with lower capacitance
- More aggressive subthreshold operation (better models at 55nm)

At 100-150 uW continuous, VibroSense-1 would be within range of a moderately-sized TEG on a warm machine.

### Verdict on Combination

A batteryless VibroSense-1 is theoretically possible but requires:
1. Process migration to 55 nm ULP or similar (~$2-5M mask set)
2. Hierarchical wake-up architecture (adds design complexity)
3. Larger TEG module than Everactive uses (adds BOM cost)
4. Careful thermal design to maintain temperature differential

**Timeline: 2-3 years of additional development beyond VibroSense-1's initial design.** The right strategy is:
1. First: Ship VibroSense-1 on Sky130 with battery (5+ year life, proven market)
2. Then: If customers demand batteryless, port to 55nm with harvesting support
3. Meanwhile: VibroSense-1's 20 kHz bandwidth is an insurmountable advantage over Everactive for bearing fault detection

---

## Market Positioning Summary

```
                    Bandwidth (diagnostic capability)
                    ↑
                    |
        20 kHz ──  |                    VibroSense-1 (battery)
                    |                    ●
                    |
                    |                         VibroSense-1 + harvesting
                    |                         ○ (future, 2028+)
                    |
         5 kHz ──  |
                    |
                    |
         1 kHz ──  |  Everactive/Fluke 3562
                    |  ●
                    |
                    +──────────────────────────────────── →
                  Battery        5-yr battery      Batteryless
                  (1-2yr)        (low maint.)      (zero maint.)
                              Maintenance burden
```

**Everactive owns the bottom-right corner:** zero maintenance, limited bandwidth. Good enough for screening non-critical assets.

**VibroSense-1 targets the top-center:** diagnostic-grade bandwidth, very low maintenance. Can detect bearing faults that Everactive misses entirely.

**The open question** is whether the top-right corner (diagnostic-grade + batteryless) is achievable. Physics says yes, with the right process node and architecture. Economics says the market for this may be small — most customers who need diagnostic-grade monitoring will accept a 5-year battery, and most customers who need zero maintenance will accept screening-grade bandwidth.

---

## Key Takeaways

1. **Everactive is real.** $161M raised, Fluke partnership, Fortune 500 customers, PKS3000 presented at Hot Chips 2025. This is not vaporware.

2. **The 1 kHz bandwidth ceiling is structural, not just a current limitation.** Energy harvesting provides 20-300 uW. Running a high-bandwidth ADC + DSP at 50 kS/s costs milliwatts. Everactive's digital FFT approach fundamentally cannot reach diagnostic-grade bandwidth on harvested power. Analog preprocessing (VibroSense-1's approach) is the only path to high bandwidth at low power.

3. **Screening vs. diagnosis is the key market segmentation.** Everactive plays in screening. VibroSense-1 plays in diagnosis. They're complementary, not directly competitive — unless VibroSense-1 also targets the screening market with a lower-power variant.

4. **The IMS division sale is a warning sign.** Selling the services arm while keeping the chip IP could be smart refocusing, or it could signal that the full-stack IoT business model isn't working. Watch for further signs of financial stress.

5. **Everactive's real moat is the SoC, not the sensor.** The PKS3000 with 2.19 uW idle power and integrated energy harvesting PMU is genuinely impressive silicon. The vibration sensor application is just one use case. Everactive could license the SoC platform to other IoT verticals (environmental monitoring, asset tracking, structural health).

6. **For VibroSense-1, the lesson is: don't compete on maintenance, compete on capability.** Everactive will always win on zero-maintenance messaging. VibroSense-1 should win on "we detect bearing faults 6 months before failure, they can't." Different value proposition, different buyer.

---

## Sources

- [Everactive's Self-Powered SoC at Hot Chips 2025 — Chips and Cheese](https://chipsandcheese.com/p/everactives-self-powered-soc-at-hot)
- [Fluke 3562 Screening Vibration Sensor — Fluke](https://www.fluke.com/en-us/product/condition-monitoring/vibration/3562)
- [Fluke Reliability and Everactive Partnership — BusinessWire](https://www.businesswire.com/news/home/20211006005085/en/Fluke-Reliability-and-Everactive-Partner-on-Batteryless-Machine-Condition-Monitoring-Solutions)
- [Everactive $35M Series C — BusinessWire](https://www.businesswire.com/news/home/20210113005317/en/Everactive-Raises-Oversubscribed-35-Million-Series-C-Financing)
- [Shoplogix Acquires Everactive IMS Division — Everactive](https://everactive.com/f/shoplogix-acquires-everactive-ims-division)
- [PsiKick Rebrands to Everactive — BusinessWire](https://www.businesswire.com/news/home/20190619005091/en/PsiKick-Rebrands-to-Everactive)
- [Rockwell Automation Partners with Everactive — Rockwell](https://www.rockwellautomation.com/en-us/company/news/press-releases/rockwell-automation-partners-with-everactive-increasing-customer-productivity-sustainability.html)
- [The Factory of the Future, Batteries Not Included — MIT News](https://news.mit.edu/2020/everactive-sensors-0820)
- [Batteryless Sensors — UVA Engineering](https://engineering.virginia.edu/news-events/news/batteryless-sensors-empower-people-information-and-insight)
- [Why Sampling Rate Matters in Bearing Vibration Monitoring — IoT Bearings](https://iotbearings.com/why-sampling-rate-matters-bearing-vibration-monitoring/)
- [Everactive Batteryless Machine Health Monitoring — Empowering Pumps](https://empoweringpumps.com/everactive-batteryless-machine-health-monitoring-cost-effective-24-7-insight-for-all-rotating-equipment/)
- [Everactive — Tracxn Company Profile](https://tracxn.com/d/companies/everactive/__v2JOIr6i8V5Z3vQfLhY-tiHxxjrwv_fjJ4AzYJ7ihF8)
- [Everactive — Nanalyze](https://www.nanalyze.com/2021/08/everactive-battery-free-iot-sensors/)
