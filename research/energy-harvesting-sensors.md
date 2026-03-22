# Energy Harvesting for Always-On Vibration Sensors

**Date:** 2026-03-22
**Question:** Can energy harvesting eliminate battery replacement for VibroSense-1 (300 uW always-on budget)?
**Bottom line: Yes. Thermoelectric harvesting from a motor bearing surface can continuously deliver 1-20 mW — 3x to 60x our 300 uW requirement. VibroSense-1 + a small TEG = truly zero-maintenance sensing.**

---

## 1. Energy Harvesting Source Comparison

### Power Available from Each Source

| Source | Typical Power Density | Realistic Harvested Power | Best Case | Notes |
|--------|----------------------|--------------------------|-----------|-------|
| **Vibration (piezoelectric)** | 10-300 uW/cm² | 100-500 uW | 1-5 mW | Tuned to machine frequency (60/120 Hz). MEMS: ~15 uW/cm². Macro PZT: 100-374 uW. |
| **Vibration (electromagnetic)** | 50 uW - 5 mW per device | 1-5 mW | 20 mW | Perpetuum PMG7: 5 mW. PMG FSH: 20 mW. Requires bulkier device (~50 cm³). |
| **Thermoelectric (TEG)** | 25-50 uW/cm²·K² | 1-20 mW | 400 mW | At dT=10-20°C typical on motors. Perpetua Power Puck: 400 mW continuous in 1 in³. |
| **Indoor photovoltaic** | 10-100 uW/cm² | 50-500 uW | 1 mW | At 200-500 lux (factory floor). Needs ~5-10 cm² panel. Varies with lighting. |
| **RF harvesting** | 0.1-10 uW/cm² | 1-40 uW | 100 uW | Ambient RF (WiFi/cellular): 1-10 uW. Dedicated TX at 1m: ~100 uW. Unreliable. |

### Source-by-Source Analysis

#### Vibration / Kinetic Energy

**Piezoelectric:**
- MEMS piezo harvesters (e.g., MicroGen BOLT): ~15 uW per 100 mm² chip, up to ~1 mW peak at resonance
- Macro PZT diaphragms on motors: 100-374 uW demonstrated at motor frequencies (30-120 Hz)
- Must be frequency-tuned to the target machine; bandwidth is narrow (Q ~10-50)
- Industrial motors vibrate at line frequency harmonics: 25/50 Hz (Europe) or 30/60 Hz (US) plus bearing defect frequencies
- **Catch:** Narrow bandwidth means a single harvester only captures one frequency. Broadband techniques (frequency-up conversion, nonlinear oscillators) reduce peak power

**Electromagnetic:**
- Perpetuum PMG7: up to 5 mW continuous from machinery vibration
- Perpetuum PMG FSH (free-standing): up to 20 mW
- ReVibe Model-D: commercial electromagnetic harvester for industrial use
- Larger form factor than piezoelectric (~50 cm³ vs ~1 cm³)
- Better suited to low frequencies (10-200 Hz) typical of rotating machinery
- **Verdict:** 5 mW from vibration alone is 16x our 300 uW budget. Proven technology, shipping commercially.

#### Thermoelectric Energy (Temperature Differential)

**Motor bearing surface temperatures:**
- Normal operating bearing temp: 60-70°C (140-160°F)
- Ambient factory temperature: 20-25°C
- **Typical dT = 20-50°C on the bearing housing surface**
- Even "warm" pipes, pumps, compressors: dT = 10-30°C above ambient
- Standard alarm threshold: bearing temp rise > 40°C above ambient = investigation needed
- SKF and reliability engineering standards confirm these ranges

**TEG power at these differentials:**
- Small TEG (40x40 mm, ~$10): at dT=20°C → ~50-200 mW open circuit, ~10-50 mW delivered after PMIC losses
- At dT=10°C → ~3-10 mW delivered (power scales as dT²)
- At dT=5°C → ~0.5-2 mW delivered
- Perpetua Power Puck: 400 mW continuous from 1 cubic inch, works from dT as low as 8-10°C
- LTC3108 with 40x40mm TEG at dT=10°C: ~4 mW output
- **Verdict:** Even pessimistic 5°C dT delivers 500-2000 uW — still exceeds our 300 uW target. At typical 20°C dT, we get 10-50 mW, which is 30-150x our budget.

#### Indoor Photovoltaic

**Factory floor illumination:**
- General factory areas: 200-300 lux (IES standards)
- Detailed work areas: 300-750 lux
- Loading/storage areas: 100-200 lux
- Near windows or under direct overhead lighting: 500-1000 lux

**Harvested power:**
- Amorphous silicon PV at 200 lux: ~10-15 uW/cm²
- GaAs or organic PV (new generation, >25% indoor efficiency): 20-50 uW/cm²
- Practical: a 5 cm² cell at 300 lux → 50-150 uW
- A 10 cm² cell at 500 lux → 200-500 uW
- **Catch:** Power drops dramatically below 100 lux. Sensors mounted on dark machine surfaces or in enclosed areas may see <50 lux. Factory lighting schedules (nights/weekends) create gaps.
- **Verdict:** Can supplement TEG/vibration but unreliable as sole source in industrial settings. Useful as secondary input in multi-source systems.

#### RF Energy Harvesting

**Ambient RF:**
- WiFi (2.4 GHz) at 5m: typically 1-10 uW harvested
- Cellular (900 MHz/1800 MHz) in factory: 0.1-5 uW
- Bluetooth at 1m: ~1 uW
- Dedicated RF power transmitter at 1m (915 MHz, 1W EIRP): ~50-100 uW

**Practical assessment:**
- Conversion efficiency: 10-50% depending on input power level
- Below -20 dBm input (~10 uW), most rectifiers fail to produce useful DC
- **Verdict:** Ambient RF alone cannot sustain 300 uW continuously. Only viable as supplementary source or with dedicated transmitter infrastructure (which defeats the "maintenance-free" goal).

---

## 2. Best Source for Industrial / Factory Environments

**Ranking for motor/pump/bearing monitoring:**

| Rank | Source | Why |
|------|--------|-----|
| **1** | **Thermoelectric (TEG)** | Motors/bearings always run hot. dT=10-50°C is reliable. 1-50 mW continuous. No moving parts. Works 24/7 while machine runs. |
| **2** | **Electromagnetic vibration** | Motors always vibrate. 1-20 mW proven. Slightly bulky. Only works when machine is running. |
| **3** | **Piezoelectric vibration** | 100-500 uW proven. Compact. Narrow bandwidth is a limitation. |
| **4** | **Indoor photovoltaic** | 50-500 uW at factory lighting. Unreliable in dark corners. Good as backup. |
| **5** | **RF harvesting** | 1-10 uW ambient. Insufficient alone. Supplementary only. |

**The clear winner for our application is thermoelectric:**
- A motor that needs vibration monitoring is, by definition, a running motor
- A running motor's bearings are always warm (dT > 10°C guaranteed)
- TEG requires physical contact with the warm surface — exactly where you'd mount a vibration sensor anyway
- Continuous power as long as the machine runs — which is exactly when you need monitoring
- No mechanical wear (solid-state), no sensitivity to frequency tuning

---

## 3. Energy Harvesting ICs

### Key Components

| IC | Manufacturer | Input Range | Key Feature | Quiescent | Price (est.) |
|----|-------------|------------|-------------|-----------|-------------|
| **LTC3108** | Analog Devices | 20 mV - 500 mV | Ultralow voltage step-up for TEGs | <1 uA | ~$5-7 (qty 100) |
| **LTC3109** | Analog Devices | ±30 mV - 500 mV | Bipolar input (TEG polarity insensitive) | <1 uA | ~$5-7 |
| **AEM10941** | e-peas | 50 mV - 5V | Solar/PV optimized, cold-start at 380 mV/3 uW | ~400 nA | ~$3-5 |
| **AEM30940** | e-peas | 50 mV - 5V | Multi-source (vibration/RF/TEG/PV), cold-start at 380 mV | ~400 nA | ~$4-6 |
| **NH2** | Nowi (Nexperia) | PV optimized | World's smallest footprint (3x3 mm), indoor PV | <1 uA | ~$2-4 |
| **BQ25570** | Texas Instruments | 100 mV - 5.1V | Nano-power boost charger, MPPT | 488 nA | ~$3-5 |
| **MAX20361** | Maxim/ADI | 225 mV - 5V | Solar with integrated MPPT, 330 nA IQ | 330 nA | ~$2-3 |
| **SPV1050** | STMicroelectronics | 150 mV - 18V | PV/TEG, dual storage, MPPT | 1.4 uA | ~$2-3 |

### LTC3108 Deep Dive (Most Relevant for TEG + VibroSense-1)

- **Minimum input voltage:** 20 mV (with 1:100 transformer)
- **Output voltages:** 2.35V, 3.3V, 4.1V, 5.0V selectable + 2.2V LDO
- **Efficiency:** 20-40% (low due to ultralow voltage boost; but input power is free)
- **Output power:** ~25 uW per °K·cm² of TEG. At dT=10°C with 40x40mm TEG → ~4 mW output
- **Power Good indicator:** signals when output is regulated (for wake-up logic)
- **Storage capacitor:** charges a large storage cap for burst transmissions
- **Quiescent current:** <1 uA — negligible vs. our 300 uW budget (< 2 uW at 1.8V)

**For VibroSense-1:** LTC3108 + 40x40mm TEG delivers 4 mW at dT=10°C. Our chip needs 300 uW. That's **13x margin** even at minimal temperature differential.

### e-peas AEM30940 Deep Dive (Best for Multi-Source)

- **Multi-source:** Can harvest from vibration (piezoelectric), RF, and DC sources
- **Cold start:** 380 mV, 3 uW — can start from tiny photovoltaic or TEG
- **MPPT:** Configurable ratio (50%-90%) for optimal power extraction
- **Dual regulated outputs:** 1.2/1.8V (MCU) + 1.8-4.1V (radio/sensor)
- **Boost converter:** 50 mV to 5V input range
- **Primary battery feature:** Can manage backup battery for guaranteed uptime
- **Protection:** Overvoltage, overcurrent, supercap balancing

### Everactive PKS3000 SoC (State of the Art Reference)

Presented at Hot Chips 2025 — the most advanced self-powered SoC for industrial IoT:
- **Process:** 55 nm ULP, 6.7 mm²
- **Power floor:** 2.19 uW idle
- **Active power:** 12 uW at 5 MHz (Arm Cortex-M0+)
- **Wake-up radio:** <1 uW passive, <6 uW active (-92 dBm sensitivity, 1000m+ range)
- **Memory:** 128 KB SRAM, 256 KB flash
- **Energy harvesting PMU:** MISIMO (Multiple Input, Single Inductor, Multiple Output)
- **Sources:** PV + TEG simultaneously, configurable for vibration/RF
- **Cold start:** 60 lux + 8°C differential

**Key insight:** Everactive proves that a complete SoC (processor + radio + sensors + PMIC) can run from harvested energy at ~10-50 uW total. Our VibroSense-1 analog front-end at 300 uW is well within harvesting range.

---

## 4. Can 300 uW Be Harvested Continuously?

### Definitive Answer: **Yes, with comfortable margin.**

| Source | Conditions | Continuous Power | Margin vs 300 uW |
|--------|-----------|-----------------|-------------------|
| TEG (40x40mm) + LTC3108 | dT = 5°C (cold motor) | 500-1000 uW | 1.7-3.3x |
| TEG (40x40mm) + LTC3108 | dT = 10°C (warm motor) | 2-4 mW | 7-13x |
| TEG (40x40mm) + LTC3108 | dT = 20°C (normal motor) | 10-20 mW | 33-67x |
| Perpetua Power Puck | dT = 10°C | up to 400 mW | 1,333x |
| Piezo harvester (macro) | 0.1-0.5g vibration, tuned | 100-500 uW | 0.3-1.7x |
| EM harvester (Perpetuum PMG7) | Standard industrial vibration | 5 mW | 17x |
| Indoor PV (5 cm²) | 300 lux factory floor | 50-150 uW | 0.2-0.5x |
| Indoor PV (10 cm²) | 500 lux workbench | 200-500 uW | 0.7-1.7x |

**Thermoelectric is the only source that guarantees 300 uW continuously** in all realistic industrial scenarios. Even the worst case (dT = 5°C on a barely warm surface) delivers enough power.

Piezoelectric alone is marginal. Indoor PV alone is insufficient. RF alone is far insufficient.

### Multi-Source Strategy

The optimal approach combines thermoelectric (primary) with photovoltaic (secondary):
- TEG: provides reliable baseline power whenever machine is running
- PV: supplements during work hours when factory lights are on
- Supercapacitor: bridges short machine-off gaps (nights, weekends)
- Small backup battery (optional): bridges extended shutdowns

Modern ICs like the e-peas AEM30940 and Everactive PKS3000 support dual-source harvesting natively.

---

## 5. Temperature Differential on Motor Bearings

### Measured Data from Industry Standards

| Condition | Bearing Surface Temp | Ambient | dT |
|-----------|---------------------|---------|-----|
| Normal operation (small motor) | 50-60°C | 20-25°C | **25-40°C** |
| Normal operation (large motor) | 60-80°C | 20-25°C | **35-60°C** |
| Elevated (needs monitoring) | 80-95°C | 20-25°C | **55-75°C** |
| Alarm threshold | >95°C | 20-25°C | **>70°C** |
| Standard rise limit | bearing + 40°C above ambient max | — | **>40°C typical** |

**Key standards:**
- Rolling bearing max temperature: 95°C (per motor bearing standards)
- Sliding bearing max temperature: 80°C
- Normal bearing temperature rise: 20-50°C above ambient
- Housing surface is ~10-15°C cooler than actual bearing temperature

**For TEG energy harvesting:**
- The sensor is mounted on the bearing housing surface
- Measured surface-to-ambient dT = 15-40°C in normal operation
- Even accounting for thermal resistance of TEG mounting: effective dT across TEG = 10-30°C
- This is **well above** the minimum 5°C needed for reliable harvesting

**Critical insight:** The very condition that requires vibration monitoring (a running motor with bearings) is exactly the condition that provides ample thermal energy for harvesting. The physics are perfectly aligned.

---

## 6. VibroSense-1 + Energy Harvesting = Indefinite Battery Life?

### System Architecture

```
                    ┌─────────────────────┐
  Motor Bearing     │   TEG (40x40mm)     │  dT=10-30°C → 2-20 mW
  Housing ──────────│   $10-15 module      │
  (50-80°C surface) │                     │
                    └──────────┬──────────┘
                               │ 20-200 mV
                    ┌──────────┴──────────┐
                    │   LTC3108 PMIC      │  20mV cold start
                    │   + step-up xfmr    │  Quiescent: <1 uA
                    │   ~$6                │
                    └──────┬───────┬───────┘
                           │       │
                     1.8V LDO    Storage Cap
                     (regulated)  (0.1-1F supercap)
                           │       │
                    ┌──────┴───────┴───────┐
                    │   VibroSense-1 ASIC  │  300 uW always-on
                    │   Analog vibration   │  Anomaly detection
                    │   classifier         │  IRQ on fault
                    └──────────┬───────────┘
                               │ IRQ (wake on anomaly)
                    ┌──────────┴──────────┐
                    │   MCU + Radio        │  Sleep: 1-5 uW
                    │   (nRF52/ESP32-C6)   │  Active: 5-30 mW
                    │   Duty-cycled        │  Burst: 10ms/minute
                    └─────────────────────┘
```

### Power Budget Analysis

| Component | Always-On | Duty-Cycled (avg) | Total Average |
|-----------|-----------|-------------------|---------------|
| VibroSense-1 ASIC | 300 uW | — | 300 uW |
| MCU (sleep, wake on IRQ) | 2 uW | — | 2 uW |
| MCU (active, 10ms every 60s) | — | ~5 uW avg | 5 uW |
| Radio TX (10ms every 60s) | — | ~50 uW avg | 50 uW |
| LTC3108 quiescent | 2 uW | — | 2 uW |
| Leakage / overhead | 10 uW | — | 10 uW |
| **System Total** | | | **~370 uW** |

### Energy Budget vs Harvesting

| Scenario | Harvested | Consumed | Surplus | Battery Life |
|----------|-----------|----------|---------|-------------|
| TEG, dT=10°C (minimum) | 2,000 uW | 370 uW | +1,630 uW | **Indefinite** |
| TEG, dT=20°C (typical) | 10,000 uW | 370 uW | +9,630 uW | **Indefinite** |
| TEG, dT=5°C (marginal) | 500 uW | 370 uW | +130 uW | **Indefinite (barely)** |
| Machine OFF, supercap only | 0 | 370 uW | -370 uW | ~7-75 hours* |

*With 0.1F supercap charged to 3.3V: E = 0.5 × 0.1 × 3.3² = 0.54 J. At 370 uW: 0.54/370e-6 = 1,460 sec ≈ 24 min. With 1F supercap: ~4 hours. With 10F supercap: ~40 hours. With small LiPo backup (100 mAh): ~500 hours (3 weeks).

### Answer: Yes — Indefinite Battery Life While Machine Is Running

- **Machine running:** TEG harvests 5-50x more power than needed. Surplus charges supercapacitor/backup battery.
- **Machine stopped (short, <4 hours):** Supercapacitor (1-10F) sustains operation. Charges back quickly when machine restarts.
- **Machine stopped (long, days/weeks):** Small backup LiPo (100 mAh, coin cell size) carries through. Never needs replacement because TEG recharges it during operation.
- **True zero-maintenance:** Supercapacitor-only systems (no battery at all) work for machines with <4 hour stop cycles. This covers most 24/7 industrial operations.

---

## 7. Existing Products: Harvesting + Sensing Combined

### Shipping Commercial Products

| Company | Product | Harvesting Source | Sensing | Power Budget | Status |
|---------|---------|------------------|---------|-------------|--------|
| **Everactive** | Eversensor MHM | TEG + PV (dual) | Triaxial accel, temp, magnetic | ~10-50 uW (PKS3000 SoC) | **Shipping, ABB partnership** |
| **Perpetua Power** | Power Puck + WirelessHART | TEG only | Temp, pressure, vibration (via partner sensors) | 400 mW available | **Shipping, Class I Div 1 certified** |
| **EnOcean** | Self-powered sensors | Light + thermal + motion | Temp, humidity, occupancy | ~10-50 uW | **Shipping, 1M+ deployed** |
| **Perpetuum** | PMG7 + sensor node | EM vibration | Vibration, temp (via ABB/Emerson) | 5-20 mW | **Shipping** (now part of HBK) |

### Key Observations

**Everactive** is the most relevant reference point:
- Battery-free machine health monitoring with TEG + PV
- Transmits data every 60 seconds
- Triaxial accelerometer for vibration screening
- IP66 rated, -40 to +200°C operating range
- 800 ft wireless range (sub-GHz)
- Partnered with Fluke Reliability for vibration programs
- PKS3000 SoC presented at Hot Chips 2025 — proves the architecture works

**However, Everactive does coarse vibration screening, not real-time analog classification.** Their accelerometer samples periodically and transmits raw data or simple statistics to the cloud. VibroSense-1 would do continuous, always-on, real-time bearing fault detection locally — a qualitatively different capability at only 300 uW.

---

## 8. Cost of Energy Harvesting Components

### Bill of Materials for TEG-Powered VibroSense-1

| Component | Description | Est. Unit Cost (qty 1000) |
|-----------|------------|--------------------------|
| TEG module | 40x40mm Bi₂Te₃, e.g., TEC1/SP1848-27145 | $3-8 |
| Heat sink | Small aluminum fins, thermal paste | $1-2 |
| LTC3108 | PMIC, DFN-12 | $4-6 |
| Step-up transformer | 1:100, e.g., Coilcraft LPR6235 | $2-3 |
| Supercapacitor | 1F, 3.3V, e.g., AVX BestCap | $1-3 |
| Input/output capacitors | Ceramic, 10uF + 100uF | $0.20 |
| PCB + assembly | Simple 2-layer board | $1-2 |
| **Subtotal (harvesting)** | | **$12-24** |
| VibroSense-1 ASIC | Custom analog chip (at volume) | $2-5 |
| MEMS accelerometer | e.g., Bosch BMA400 (12 uA) | $1-2 |
| MCU + Radio | e.g., Nordic nRF52810 | $1-2 |
| Antenna + passives | Sub-GHz PCB antenna, misc | $1-2 |
| **Total BOM** | | **$17-35** |
| **Enclosure + mounting** | IP67, magnetic mount for bearing housing | $5-15 |
| **Total sensor node** | | **$22-50** |

### Cost Comparison vs Battery-Powered Alternative

| | TEG-Powered (Zero Maintenance) | Battery-Powered |
|---|---|----|
| Initial node cost | $30-50 | $20-35 |
| Battery replacement cost | $0 | $5-10/year (labor + battery) |
| 5-year total cost | $30-50 | $45-85 |
| 10-year total cost | $30-50 | $70-135 |
| Downtime / missed readings | Zero (while machine runs) | Risk during battery swap |
| Hazardous area install | TEG is intrinsically safe | Battery requires certification |

**Break-even:** 2-3 years. After that, pure savings. For large installations (100+ sensors), the labor savings from eliminating battery replacement dominate — often $50-100 per sensor per year when accounting for technician time, scaffolding, confined space permits, etc.

---

## 9. Critical Assessment: The Catches

### What Can Go Wrong

1. **TEG thermal resistance:** If the TEG is poorly mounted (air gap, no thermal paste), effective dT drops to 2-3°C → power drops below 300 uW. **Mitigation:** Thermal compound + spring-loaded mounting clip. Proven by Perpetua and Everactive.

2. **Machine cold-start:** When a machine starts from ambient temperature, the TEG produces zero power until thermal equilibrium develops (5-30 minutes). **Mitigation:** Supercapacitor or small backup battery bridges the gap.

3. **Seasonal ambient variation:** In hot factories (ambient 40°C in summer), dT across TEG is smaller. A bearing at 60°C surface → dT = 20°C is still fine. But in extreme cases (50°C ambient, 55°C bearing), dT = 5°C is marginal. **Mitigation:** Over-engineer for worst case; 300 uW is still achievable at dT=5°C.

4. **TEG aging:** Bi₂Te₃ thermoelectric modules degrade very slowly (<1%/year at operating temperatures). At 10 years, you have ~90% of initial power. Not a practical concern.

5. **Vibration sensor mounting conflict:** The best location for vibration sensing (directly on bearing housing, rigid mount) is also the best for TEG (maximum thermal contact). This is actually an advantage — same mounting point serves both purposes.

6. **Form factor:** A 40x40mm TEG + heat sink adds ~50x50x30mm to the sensor node. Acceptable for industrial (Everactive's sensor is similar size) but rules out tiny form factors.

7. **Cost premium:** $10-20 extra BOM for harvesting components. Pays back in 2-3 years from eliminated battery maintenance.

### What the Data Actually Proves

The energy harvesting story for VibroSense-1 is unusually clean because of three aligned facts:

1. **Vibration monitoring requires mounting on running machinery** — exactly where thermal and kinetic energy is available
2. **300 uW is extraordinarily low** for a complete bearing fault detector — 10-30x below competing MCU+FFT solutions
3. **Motor bearings always run 10-50°C above ambient** — providing reliable, continuous thermal energy

This is not a case of stretching to make harvesting work. The physics strongly favor this application.

---

## 10. Recommended System Architecture for VibroSense-1

### Minimum Viable (TEG Only)

```
Component                       Cost    Power
TEG (30x30mm) on bearing        $5      → 1-10 mW harvested
LTC3108 + transformer           $7      → 1.8V regulated, <1 uA Iq
1F supercapacitor               $2      → 24 min backup at 370 uW
VibroSense-1 ASIC               $3      → 300 uW always-on sensing
MCU + radio (duty-cycled)       $2      → ~55 uW average
Total system average power:     —       370 uW consumed, 1000+ uW harvested
```

### Recommended (Dual-Source, Robust)

```
Component                       Cost    Power
TEG (40x40mm) on bearing        $8      → 2-20 mW harvested (primary)
Small PV cell (2x3 cm)          $2      → 50-200 uW (secondary)
e-peas AEM30940 PMIC            $5      → Dual-source MPPT, 50mV cold start
1F supercapacitor               $2      → 24 min backup
Optional: CR2032 backup         $1      → 3 week deep backup
VibroSense-1 ASIC               $3      → 300 uW always-on
MCU + radio (duty-cycled)       $2      → ~55 uW average
Total system average power:     —       370 uW consumed, 2000-20000 uW harvested
```

### Premium (Maximum Reliability)

For critical rotating equipment where missed faults cost >$100K:
- Perpetua Power Puck ($50-100) delivers 400 mW — massive surplus
- Charges a full Li-ion cell for weeks of backup
- Powers VibroSense-1 + high-rate radio (every second if needed)
- Intrinsically safe certified for hazardous areas

---

## 11. Implications for VibroSense-1 Product Strategy

### The 300 uW Design Point Was Better Than We Knew

When we set 300 uW as the VibroSense-1 power target, the goal was "long battery life." But 300 uW unlocks something much more valuable: **true energy autonomy.**

- At 3-10 mW (MCU + FFT approach): Energy harvesting is marginal. You need large TEGs, ideal mounting, and are on the edge of the power budget. Battery backup measured in hours.
- At 300 uW (VibroSense-1 approach): Energy harvesting has 5-50x margin. Small TEGs work. Imperfect mounting works. Supercapacitors provide hours of backup. The system is robust.

**The analog approach doesn't just save power — it crosses a threshold that enables a fundamentally different product category: install-and-forget industrial sensing.**

### Market Positioning

| Approach | Power | Battery Life | Harvesting Viable? | Maintenance |
|----------|-------|-------------|-------------------|-------------|
| MCU + FFT (competitor) | 3-10 mW | 1-6 months | Barely, with large TEG | Replace battery 2-4x/year |
| VibroSense-1 (battery) | 300 uW | 5-10 years (coin cell) | Yes, easily | Maybe once ever |
| VibroSense-1 + TEG | 300 uW | **Indefinite** | **Yes, 10-50x margin** | **Zero** |

### Competitive Moat

The combination of ultra-low-power analog signal processing + energy harvesting creates a defensible advantage:
1. **Digital competitors cannot match 300 uW** for equivalent vibration classification — the physics of ADC + FFT + digital processing sets a floor around 3 mW
2. **Energy harvesting competitors (Everactive)** do coarse vibration screening, not real-time fault classification
3. **The TEG + VibroSense-1 combination** delivers always-on, real-time, continuous bearing fault detection with zero maintenance — a capability that does not exist today

---

## Sources

### Energy Harvesting General
- [Energy Harvesting IoT Reaching Scale in 2026](https://iotbusinessnews.com/2025/11/26/energy-harvesting-iot-practical-applications-finally-reaching-scale-in-2026/)
- [Energy Harvesting for Machine Condition Monitoring (MDPI)](https://www.mdpi.com/1424-8220/18/12/4113)
- [DOE: Low-Cost Vibration Power Harvesting](https://www1.eere.energy.gov/manufacturing/industries_technologies/sensors_automation/pdfs/kcf_vibrationpower.pdf)

### Piezoelectric / Vibration
- [Piezoelectric Energy Harvesting for Induction Motors (MDPI)](https://www.mdpi.com/2227-7080/13/5/194)
- [Piezoelectric Energy Harvesting for Rolling Bearings (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0360544221020181)
- [MEMS Energy Harvesting Review (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S2590123023003912)
- [MicroGen Piezo-MEMS + Analog Devices SmartMesh](https://www.analog.com/en/resources/technical-articles/microgen-s-piezo-mems-vibration-energy-harvesters-enable-linear-technology-smartmesh-ip-wireless.html)
- [Millimeter-Scale Energy Harvester (Michigan)](https://ece.engin.umich.edu/stories/most-powerful-millimeter-scale-energy-harvester-generates-electricity-from-vibrations)
- [Vibration Energy Harvesting to Power Condition Monitoring (Waterbury & Wright)](https://journals.sagepub.com/doi/10.1177/0954406212457895)

### Thermoelectric
- [TEG Energy Harvesting for Industrial Motor Monitoring (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S2213138823005659)
- [LTC3108 FAQ (Analog Devices)](https://www.analog.com/en/resources/technical-articles/frequently-asked-questions-thermoelectric-energy-harvesting-with-the-ltc3108-ltc3109.html)
- [LTC3108 Datasheet (Analog Devices)](https://www.analog.com/en/products/ltc3108.html)
- [Fraunhofer Thermoelectric Power Supply](https://www.iis.fraunhofer.de/en/ff/lv/iot-system/tech/energy-harvesting/thermo.html)
- [Low-Temperature TEG Modules (TecTeg)](https://tecteg.com/low-dt-thermoelectric-harvesting-teg-power-module/)

### Motor Bearing Temperatures
- [Managing Hot Bearings (Machinery Lubrication)](https://www.machinerylubrication.com/Read/30608/manage-hot-bearings)
- [SKF: Role of Temperature in Bearings](https://evolution.skf.com/us/whats-normalthe-role-of-temperature-in-bearing-applications-3/)
- [Motor Bearing Temperature Standards](https://www.zoompumps.com/article/motor_and_pump_bearing_temperature_standards.html)

### Indoor Photovoltaic
- [Indoor PV Energy Harvesting System (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0045790626001187)
- [Indoor Light Energy Harvesting (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10395376/)
- [Indoor Photovoltaics (Nature Polymer Journal)](https://www.nature.com/articles/s41428-022-00727-8)

### RF Harvesting
- [RF Energy Harvesting for IoT (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11644274/)
- [RF Energy Harvesting for Smart Buildings](https://www.buildings.com/smart-buildings/iot/article/55270496/rf-energy-harvesting-delivering-power-to-the-next-generation-of-smart-building-iot)

### Energy Harvesting ICs
- [e-peas AEM10941](https://e-peas.com/product/aem10941/)
- [e-peas AEM30940](https://e-peas.com/product/aem30940/)
- [Nowi (Nexperia) NH2](https://www.nowi-energy.com/products-nh2/)
- [Analog Devices Energy Harvesting](https://www.analog.com/en/product-category/energy-harvesting.html)

### Commercial Products
- [Everactive Machine Health Monitoring](https://everactive.com/applications/machine-vibration-monitoring/)
- [Everactive PKS3000 at Hot Chips 2025 (Chips & Cheese)](https://chipsandcheese.com/p/everactives-self-powered-soc-at-hot)
- [Perpetua Power](https://perpetuapower.com/)
- [Perpetuum PMG7 Microgenerator](https://eepower.com/new-industry-products/perpetuum-releases-vibration-energy-harvesting-microgenerator/)
- [EnOcean Energy Harvesting](https://www.enocean.com/en/technology/energy-harvesting/)
- [ReVibe Energy](https://revibeenergy.com/energy-harvesting/)

### Multi-Source Harvesting
- [Multi-Source Energy Harvesting in Silicon (MDPI)](https://www.mdpi.com/2079-9292/14/10/1951)
- [Hybrid Energy Harvesters (Frontiers)](https://www.frontiersin.org/journals/materials/articles/10.3389/fmats.2018.00065/full)
- [Triple-Source Energy Harvesting (SPIE)](https://ui.adsabs.harvard.edu/abs/2023SPIE12615E..13L/abstract)

### Factory Lighting Standards
- [IES Industrial Recommended Light Levels](https://www.superbrightleds.com/blog/industrial-commercial-recommended-lighting-levels.html)
- [Lux Level Standards in Industry](https://www.ppsthane.com/blog/lux-level-standards-industry)
