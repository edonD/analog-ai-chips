# STMicroelectronics ISM330DHCX Machine Learning Core — The "Good Enough" Digital Competitor

*Last updated: 2026-03-22*

The ISM330DHCX is ST's industrial-grade 6-axis IMU with an embedded Machine Learning Core (MLC) that runs decision trees directly on the sensor die. At $6.80/unit, already in mass production, and integrated into a sensor customers already need, it is the single most dangerous competitor to any analog vibration preprocessing chip — not because it is better, but because it is *already there*.

This file dissects exactly what it can and cannot do.

---

## 1. What the ISM330DHCX Is

**Package:** LGA-14L, 2.5 x 3.0 x 0.83 mm — fits on any sensor node PCB.

**Core sensors:**
- 3-axis accelerometer: +/-2/4/8/16 g full scale, ODR up to 6.66 kHz
- 3-axis gyroscope: +/-125 to +/-4000 dps, ODR up to 6.66 kHz

**Embedded processing:**
- Machine Learning Core (MLC): up to 8 decision trees, 512 total nodes
- Finite State Machine (FSM): 16 independent programmable state machines
- 9 KB smart FIFO
- Sensor hub (connects external sensors via I2C auxiliary)

**Interfaces:** SPI (10 MHz), I2C, MIPI I3C

**Temperature range:** -40 to +105 deg C (industrial grade)

**Supply:** 1.71 V to 3.6 V

**Price:** ~$6.80 at unit quantity (DigiKey 2025), likely $3-5 in volume

**Status:** Mass production since ~2020. Widely available. Thousands of designs shipping.

---

## 2. How the Machine Learning Core Works

The MLC is a hardwired digital logic block on the sensor die that implements a specific processing pipeline. It is NOT a general-purpose processor. The pipeline is fixed:

```
Raw Sensor Data (accel XYZ, gyro XYZ)
        |
        v
  Internal Computation
  (norm, norm-squared from 3-axis data)
        |
        v
  Configurable Filters (up to 8)
  (2nd-order IIR: HP, BP, LP)
        |
        v
  Window Accumulation
  (N samples, configurable window size)
        |
        v
  Feature Computation (up to 32 features)
  (mean, variance, energy, peak-to-peak, etc.)
        |
        v
  Decision Tree Evaluation (up to 8 trees)
  (if-then-else on features, max 512 nodes total)
        |
        v
  Output Register (MLC0_SRC through MLC7_SRC)
  + Interrupt on INT1/INT2
```

### 2.1 Input Data

The MLC can process:
- Accelerometer X, Y, Z
- Gyroscope X, Y, Z
- Accelerometer norm (sqrt(X^2 + Y^2 + Z^2)) — computed internally
- Accelerometer norm-squared (X^2 + Y^2 + Z^2) — computed internally
- Gyroscope norm and norm-squared — computed internally
- External sensor data (via sensor hub)

### 2.2 Filters

Up to 8 configurable 2nd-order IIR filters can be applied to the input data before feature computation. Filter types:
- **High-pass (HP):** remove DC/low-frequency bias
- **Band-pass (BP):** isolate frequency bands
- **Low-pass (LP):** anti-alias before decimation

The user specifies filter coefficients (b0, b1, b2, a1, a2 in standard IIR form). ST provides a tool (Unico GUI / ST Edge AI Suite) to design these filters.

**Critical detail:** These are 2nd-order IIR filters, equivalent to a single biquad section. For vibration analysis, a single 2nd-order band-pass filter gives only 12 dB/octave rolloff — far less selective than the 5-channel Gm-C filter bank in VibroSense-1 (each also 2nd-order, but there are 5 of them covering different bands simultaneously). The MLC can run up to 8 filters, but each feature can only use one filter output, and there are only 32 feature slots total.

### 2.3 Window and Feature Computation

Features are statistical parameters computed over a window of N samples:

**Available features (confirmed from ST documentation):**
| Feature | Description |
|---------|------------|
| Mean | Average value in window |
| Variance | Statistical variance |
| Energy | Sum of squares |
| Peak-to-peak | Max minus min in window |
| Zero-crossing | Number of threshold crossings |
| Positive zero-crossing | Crossings in positive direction |
| Negative zero-crossing | Crossings in negative direction |
| Peak detector | Number of peaks (pos + neg) above threshold |
| Minimum | Minimum value in window |
| Maximum | Maximum value in window |
| Absolute minimum | Absolute minimum |
| Absolute maximum | Absolute maximum |

**Maximum features:** 32 per configuration (across all inputs and filters).

**Window size:** Configurable in samples. Example configurations:
- 16 samples at 26 Hz = 0.6 sec window (vibration monitoring example)
- 39 samples at 12.5 Hz = 3.1 sec window (motion intensity example)
- 208 samples at 104 Hz = 2.0 sec window (vehicle status example)

### 2.4 Decision Trees

- **Maximum trees:** 8 (running simultaneously and independently)
- **Maximum total nodes:** 512 (shared across all 8 trees)
- **Maximum results per tree:** 256 classes
- **Maximum subgroups per tree:** 4

Each node is a binary split: "if feature_X > threshold_Y, go left; else go right." This is a standard CART-style decision tree.

A tree with 512 nodes can have a maximum depth of 9 (2^9 = 512) but typically depth 5-8 is practical, giving 32-256 leaf nodes.

### 2.5 MLC Output Data Rate

The MLC output rate (how often it generates a classification result) is limited to:
- **12.5 Hz, 26 Hz, 52 Hz, or 104 Hz**

This is the classification rate, not the sensor sampling rate. The sensor can sample at up to 6.66 kHz, but the MLC only produces a new decision every 9.6 ms (at 104 Hz) at best.

---

## 3. Power Consumption — The Real Numbers

### 3.1 Sensor Power (from datasheet)

| Mode | Current (typical) | Power at 1.8V |
|------|-------------------|---------------|
| Power-down (interfaces active) | ~3 uA | ~5.4 uW |
| Accelerometer only, high-perf mode | ~0.55 mA | ~990 uW |
| Gyroscope only, high-perf mode | ~0.90 mA | ~1.62 mW |
| Accel + Gyro, high-perf mode | ~1.2 mA | ~2.16 mW |
| Accel only, low-power mode | ~0.13-0.17 mA | ~230-300 uW |

### 3.2 MLC Incremental Power

ST does not publish a separate MLC power number. The MLC is embedded logic that shares the sensor's digital core. Based on ST's marketing claims and community discussions:

- **MLC adds negligible incremental power** to the sensor's base consumption — estimated at 10-50 uW above the base accelerometer current.
- The dominant power cost is the **accelerometer itself** running at whatever ODR is needed for the MLC input.

**For vibration monitoring at 26 Hz ODR:**
- Accelerometer in low-power mode at 26 Hz: ~130-170 uA = ~230-300 uW
- MLC overhead: ~10-50 uW (estimated)
- **Total sensor + MLC: ~250-350 uW**

**For higher-frequency vibration at 6.66 kHz ODR (to capture bearing faults):**
- Accelerometer in high-performance mode: ~550 uA = ~990 uW
- MLC overhead: ~10-50 uW
- **Total sensor + MLC: ~1.0-1.05 mW**

### 3.3 Key Insight

The ISM330DHCX + MLC total power for basic vibration monitoring (250-350 uW) is **comparable to VibroSense-1's 300 uW target**. However, the MLC at that power level is limited to 26 Hz ODR, which means it can only analyze vibration content up to ~13 Hz — far below bearing fault frequencies.

To analyze frequencies relevant to bearing faults (100 Hz to 10 kHz), the sensor must run at high ODR (>= 1.66 kHz), pushing power to ~1 mW. And then the MLC is still limited to 104 Hz classification rate.

---

## 4. The Fundamental MLC Limitation for Vibration

**This is the single most important finding in this analysis.**

The MLC elaboration rate is limited to 104 Hz maximum. This means:

1. **The MLC processes data at most 104 times per second.** Each processing cycle, it takes a window of accumulated samples, computes features, and evaluates decision trees.

2. **The MLC does NOT do FFT.** It cannot compute a frequency spectrum. It computes time-domain statistical features (mean, variance, peak-to-peak, energy, zero-crossings) over a window.

3. **The sensor CAN sample at 6.66 kHz**, capturing high-frequency vibration content. But the MLC can only classify based on statistical features of those samples — not their frequency content.

4. **The IIR filters help but are limited.** You can configure up to 8 band-pass IIR filters to isolate frequency bands before feature computation. But with only 8 filters, 32 features max, and 2nd-order IIR (weak selectivity), the frequency decomposition is crude compared to:
   - A proper 512/1024/2048-point FFT
   - An analog 5-band filter bank (like VibroSense-1)

### What the MLC CAN Detect in Vibration

- **Vibration intensity levels** (low/medium/high) — ST's own example uses peak-to-peak on accelerometer norm at 26 Hz. Trivial classification.
- **Gross changes in vibration character** — if a machine goes from smooth to rough, variance and energy change dramatically. The MLC catches this.
- **Threshold exceedances** — "vibration RMS exceeded X" is essentially a comparator, and the MLC can do this easily.

### What the MLC CANNOT Do in Vibration

- **Identify specific fault types** (inner race vs outer race vs ball fault vs imbalance). These require frequency-domain analysis because each fault type has a characteristic defect frequency (BPFI, BPFO, BSF, FTF). The MLC has no FFT and only crude IIR filtering.
- **Detect incipient bearing faults.** Early bearing damage produces high-frequency impacts (2-10 kHz) with low amplitude. Envelope analysis (demodulation + frequency analysis) is the standard technique. The MLC cannot do envelope analysis.
- **Track bearing defect frequency harmonics.** Bearing defect frequencies shift with RPM. A proper diagnostic system tracks harmonics across speed changes. The MLC has no concept of harmonic tracking.
- **Perform order analysis.** Speed-normalized vibration analysis requires a tachometer reference and resampling. Completely outside MLC scope.

### The Honest Assessment

The MLC is excellent for **"something is wrong" detection** (anomaly detection, threshold monitoring, vibration level classification). It is **incapable of "here is what is wrong" diagnosis** (fault identification, root cause analysis). This is exactly the gap that VibroSense-1 targets with its 5-band analog filter bank.

---

## 5. The Finite State Machine (FSM) — What It Adds

The ISM330DHCX has 16 independent Finite State Machines alongside the MLC.

### FSM Architecture

- **16 independent programs** with dedicated memory areas
- Each FSM processes conditioned data from accelerometer, gyroscope, or external sensors
- Signal conditioning block converts and can compute norms
- Each FSM generates an interrupt when it reaches an end state or executes a specific command

### What the FSM Can Do That the MLC Cannot

| Capability | MLC | FSM |
|-----------|-----|-----|
| Pattern type | Statistical (features over window) | Sequential (state transitions over time) |
| Time awareness | Window-based only | True real-time state tracking |
| Gesture recognition | Poor | Designed for this |
| Event sequencing | No | Yes (state A then B then C) |
| Threshold with timing | Limited | Full (hold for N ms, then transition) |
| Wake-up conditions | Yes (via interrupt) | Yes (more flexible conditions) |
| Power | Shared with MLC | Shared with MLC |

### FSM for Vibration

The FSM is mainly useful for:
- **Wake-on-vibration:** transition from sleep to active when vibration exceeds threshold for N ms
- **Shock detection:** detect impact events with specific amplitude and duration
- **Activity/inactivity transitions:** state machine for duty-cycling the sensor node

The FSM is NOT useful for vibration frequency analysis or fault classification. It complements the MLC for system-level power management (e.g., "wake up the MCU only when vibration has been above threshold for 5 seconds").

---

## 6. ISM330BX — The Next Generation

The ISM330BX is ST's successor, announced 2024, adding several features:

### New in ISM330BX vs ISM330DHCX

| Feature | ISM330DHCX | ISM330BX |
|---------|-----------|---------|
| Accel current (HP mode) | ~0.55 mA | ~0.19 mA (accel only) |
| Combo current (HP mode) | ~1.2 mA | ~0.6 mA |
| MLC nodes | 512 | TBD (likely same or more) |
| Sensor Fusion Low-Power (SFLP) | No | Yes — on-chip 6-axis fusion |
| Adaptive Self-Configuration (ASC) | No | Yes — FSM/MLC can reconfigure sensor in real-time |
| Qvar sensing | No | Yes — 3 channels, electrostatic charge sensing |
| Exportable AI features/filters | No | Yes — features computed by MLC can be read out by host |

### ISM330BX Key Improvements

1. **~3x lower power** in high-performance mode (0.6 mA combo vs 1.2 mA). This is significant — it brings high-ODR vibration monitoring down to ~1.1 mW from ~2.2 mW.

2. **Adaptive Self-Configuration (ASC):** The FSM can automatically change sensor ODR, full scale, or MLC configuration based on detected conditions. This enables true duty-cycled operation: run at low ODR until the FSM detects something interesting, then automatically switch to high ODR for detailed analysis — without host processor intervention.

3. **Exportable AI features:** The MLC's computed features (mean, variance, energy, etc.) can be read out by the host MCU, not just the decision tree result. This lets the MCU do more sophisticated analysis (including FFT) on already-preprocessed data.

4. **Qvar:** Electrostatic charge sensing on 3 channels. Not directly relevant to vibration, but interesting for detecting human proximity or fluid levels.

### ISM330BX Implications for Competition

The ISM330BX is a harder competitor than the ISM330DHCX because:
- 3x lower power makes it closer to always-on analog power levels
- ASC enables intelligent duty-cycling without a host MCU
- Exportable features blur the line between on-sensor and on-MCU processing

**But the core MLC limitation remains:** decision trees on statistical features, no FFT, limited frequency decomposition. The ISM330BX does not add spectral analysis.

---

## 7. The Full Reference Design: STEVAL-STWINKT1B

ST's condition monitoring reference platform is the STEVAL-STWINKT1B ("SensorTile Wireless Industrial Node"). Priced at ~$80.

### Board Components

| Component | Part | Role |
|-----------|------|------|
| MCU | STM32L4R9ZI (Cortex-M4, 120 MHz, 2 MB Flash, 640 KB SRAM) | Main processor |
| Vibration sensor | IIS3DWB (3-axis, 26.7 kHz ODR, 6 kHz BW, 1.1 mA) | Wideband vibration |
| IMU | ISM330DHCX (6-axis, MLC + FSM) | Motion + on-sensor ML |
| Microphone | IMP34DT05 (digital MEMS, industrial grade) | Ultrasound/acoustic |
| Magnetometer | IIS2MDC (3-axis, ultra-low-power) | Magnetic field |
| Pressure | LPS22HH (absolute pressure) | Environmental |
| Humidity + Temp | HTS221 | Environmental |
| Temperature | STTS751 (local, 12-bit) | Board temperature |
| Connectivity | BLE module (on-board) + Wi-Fi plugin option | Wireless |
| Storage | MicroSD card slot | Data logging |
| Power | 480 mAh Li-Po battery + STBC02 charger | Battery operated |
| Debug | STLINK-V3MINI (included) | Programming |
| Interface | RS485, USB OTG | Industrial connectivity |

### Software Stack

| Layer | Product | What It Does |
|-------|---------|-------------|
| On-sensor ML | MLC configuration (Unico GUI / ST Edge AI Suite) | Decision trees on ISM330DHCX |
| Edge AI | NanoEdge AI Studio | AutoML for anomaly detection on MCU |
| Function pack | FP-AI-MONITOR1 / FP-AI-MONITOR2 | Vibration + ultrasound anomaly detection |
| Cloud | ST cloud dashboard | Remote monitoring |
| Model deployment | STM32Cube.AI | Neural network deployment on STM32 |

### How the Full System Works

1. **IIS3DWB** captures wideband vibration at 26.7 kHz ODR (1.1 mA)
2. **ISM330DHCX MLC** runs basic vibration level classification (always-on, ~300 uW)
3. **STM32L4R9** wakes up periodically or on MLC interrupt
4. MCU reads IIS3DWB FIFO, runs **FFT** (512 or 1024 point)
5. NanoEdge AI library runs **anomaly detection** on FFT features
6. Result transmitted via BLE

**Key insight:** ST's own reference design does NOT rely on the MLC for serious vibration diagnostics. The MLC is used for wake-on-event and basic classification. The real analysis happens on the MCU with FFT + AI. The IIS3DWB (dedicated vibration sensor, 1.1 mA) provides the high-bandwidth data that the ISM330DHCX MLC cannot properly analyze.

---

## 8. ST Edge AI Case Studies — Real Results

### Fan Anomaly Detection (Vibration-Based)
- **Sensor:** ISM330DHCX on STEVAL-STWINKT1B
- **Method:** NanoEdge AI Studio on MCU (not MLC alone)
- **Result:** Anomaly detection on fan vibration data, specific accuracy not published
- **Power:** MCU-based, not always-on

### Motor Anomaly Detection at Variable Speeds
- **Sensor:** MEMS accelerometer + STM32 MCU
- **Method:** NanoEdge AI Studio, on-device learning
- **Result:** Detects anomalies across different RPM settings
- **Key detail:** Variable speed handling requires MCU processing — MLC alone cannot adapt to speed changes

### Pump Anomaly Detection (Vibration-Based)
- **Method:** Vibration data collection + NanoEdge AI on MCU
- **Result:** Vibration-based anomaly detection for industrial pumps
- **Power:** MCU duty-cycled, not always-on

### ST's Own Vibration Monitoring MLC Example
- **Sensor:** ISM330DHCX at 26 Hz ODR, +/-4g
- **Feature:** Peak-to-peak on accelerometer norm-squared
- **Decision tree:** 1 tree, 2 nodes (trivial)
- **Classes:** 3 (no vibration / low vibration / high vibration)
- **Accuracy:** Not published (likely >95% for this trivial task)
- **Window:** 16 samples, ~0.6 sec

**The pattern is clear:** Every ST case study that does serious vibration analysis uses the MCU. The MLC handles only trivial classification (vibration present/absent, intensity level).

---

## 9. What the MLC Cannot Do That Analog Preprocessing Can

This is the competitive analysis section. Where VibroSense-1 has structural advantages:

### 9.1 Continuous Frequency Decomposition

| Capability | ISM330DHCX MLC | VibroSense-1 (Analog) |
|-----------|---------------|----------------------|
| Frequency bands | Up to 8 IIR filters, 2nd-order, configured once | 5 Gm-C BPFs, 2nd-order, continuously active |
| Simultaneous bands | Limited by 32 feature slots | All 5 bands always active |
| Frequency range | Effective to ~52 Hz (MLC rate limit) | 100 Hz - 20 kHz |
| Band energy | Computed digitally in window | Extracted continuously by envelope detectors |
| Latency | Window size (0.6 to 3 sec typical) | Analog settling (~100 ms) |
| Power for frequency analysis | ~1 mW (high ODR needed) | ~24 uW (filter bank) |

### 9.2 Always-On Operation at Full Bandwidth

The MLC at full bandwidth (6.66 kHz accelerometer ODR) consumes ~1 mW for the sensor alone, and the MLC still only classifies at 104 Hz maximum. VibroSense-1 processes the full 100 Hz - 20 kHz band continuously at 300 uW total.

**Power comparison for equivalent vibration analysis:**

| Configuration | ISM330DHCX System | VibroSense-1 |
|--------------|-------------------|-------------|
| Basic wake-on-vibration | ~300 uW (MLC at low ODR) | Overkill — simple comparator would do |
| 5-band energy monitoring | ~1 mW sensor + MCU wakes for FFT | ~300 uW always-on |
| Bearing fault detection | ~1 mW sensor + ~5-10 mW MCU for FFT | ~300 uW always-on |
| 4-class fault identification | ~1 mW sensor + ~5-10 mW MCU | ~300 uW always-on |

### 9.3 Envelope Detection

Bearing fault detection requires **envelope analysis** (amplitude demodulation of high-frequency resonance bands). The MLC has no envelope detection capability. VibroSense-1 has dedicated analog envelope detectors on each frequency band, consuming ~5 uW per channel.

### 9.4 Crest Factor and Kurtosis

These are key early-fault indicators:
- **Crest factor** (peak/RMS) catches impulsive events
- **Kurtosis** (4th moment) catches non-Gaussian tails

The MLC can compute peak-to-peak and variance (related to RMS), but cannot compute crest factor or kurtosis directly. VibroSense-1 computes crest factor in analog and kurtosis via a low-rate MCU wakeup (~10 uW incremental).

### 9.5 Fundamental Architectural Difference

```
ISM330DHCX approach:
  Analog sensor → ADC → Digital samples → Statistical features → Decision tree
  (high power)   (fixed)  (high ODR needed)  (time-domain only)   (limited)

VibroSense-1 approach:
  Analog sensor → Analog filters → Analog envelope → Analog classifier → Digital wake
  (shared)        (5 bands, 24uW)  (5 channels, 25uW) (MAC, 2uW)       (10uW idle)
```

The ISM330DHCX digitizes first, then tries to extract features digitally. VibroSense-1 extracts features in the analog domain before any digitization. The analog approach avoids the ADC power penalty entirely for the always-on path.

---

## 10. ISM330IS — The ISPU Evolution

ST also makes the ISM330IS with an Intelligent Sensor Processing Unit (ISPU) instead of MLC:

| Feature | ISM330DHCX (MLC) | ISM330IS (ISPU) |
|---------|-----------------|----------------|
| Processing | Hardwired decision tree engine | Programmable 32-bit RISC DSP |
| Model types | Decision trees only | Neural networks, decision trees, any C code |
| Memory | Decision tree config only | 8 KB data + 32 KB program SRAM |
| Precision | Integer features | 32-bit floating point |
| Flexibility | Fixed feature set | Arbitrary C algorithms |
| Power (combo HP) | ~1.2 mA | ~0.59 mA |
| FFT capability | No | Yes (can implement in C) |

The ISPU can theoretically run a small FFT and neural network for vibration classification. However:
- 32 KB program memory severely limits model complexity
- A 256-point FFT on a 32-bit DSP core at low clock rate still takes significant power
- No published vibration classification accuracy numbers

The ISPU is closer to what an analog preprocessor does, but at higher power and with software complexity. It represents ST's acknowledgment that decision trees alone are insufficient for serious edge AI.

---

## 11. Pricing and Market Position

| Part | DigiKey Unit Price | Est. Volume Price | Package |
|------|-------------------|-------------------|---------|
| ISM330DHCX (sensor + MLC + FSM) | $6.80 | $3-5 | LGA-14L, 2.5x3x0.83mm |
| ISM330BX (next-gen) | ~$7-9 | $4-6 | LGA-14L, 2.5x3x0.83mm |
| ISM330IS (ISPU) | ~$8-10 | $5-7 | LGA-14L |
| IIS3DWB (vibration sensor) | ~$9 | $5-7 | LGA-14L |
| STEVAL-STWINKT1B (full kit) | ~$80 | N/A | Dev board |

**The "free" argument:** If a customer already needs an IMU (for tilt compensation, orientation, or motion detection), the MLC comes free — it is embedded in the sensor they are already buying. No additional chip, no additional BOM cost, no additional PCB area. This is the MLC's strongest competitive advantage.

---

## 12. Competitive Summary: ISM330DHCX MLC vs VibroSense-1

| Dimension | ISM330DHCX MLC | VibroSense-1 |
|-----------|---------------|-------------|
| **Status** | Mass production, thousands of designs | Design phase (sky130) |
| **BOM cost** | $0 incremental (sensor already needed) | $5-15 additional chip |
| **Always-on power** | ~300 uW (at 26 Hz, useless for faults) | ~300 uW (full 100Hz-20kHz) |
| **Vibration bandwidth** | Sensor: 6.6 kHz. MLC: effectively ~52 Hz | 100 Hz - 20 kHz always-on |
| **Frequency decomposition** | 8 IIR filters, crude | 5 dedicated BPFs, ISO 10816 aligned |
| **Fault identification** | No (intensity only) | Yes (4-class: normal, imbalance, bearing, looseness) |
| **Envelope analysis** | No | Yes (5 channels, analog) |
| **FFT** | No (requires MCU wakeup) | Not needed (analog equivalent) |
| **Model type** | Decision trees (max 512 nodes) | Charge-domain MAC (128 caps, 4-bit weights) |
| **Reprogrammable** | Yes (MLC config via registers) | Yes (weights via SPI) |
| **Toolchain** | Excellent (ST Edge AI Suite, Unico GUI, NanoEdge) | None (open-source, custom) |
| **Ecosystem** | STM32 MCU, STWIN kit, cloud dashboard | Standalone |
| **Customer risk** | Zero (ST is $16B company) | High (unproven startup/project) |
| **Software** | Mature, documented, community | From scratch |

### Where ISM330DHCX MLC Wins
1. Zero incremental cost — it is already in the sensor
2. Zero design risk — production-proven
3. Excellent toolchain and ecosystem
4. "Good enough" for vibration level monitoring (not fault diagnosis)
5. Can wake MCU for deeper analysis when needed

### Where VibroSense-1 Wins
1. Real frequency decomposition at always-on power levels
2. Fault identification (4-class) without MCU wakeup
3. Envelope detection for incipient bearing faults
4. ISO 10816 aligned features that vibration analysts trust
5. 3-10x lower power than MCU-based FFT for equivalent analysis

### The Strategic Reality

The ISM330DHCX MLC is the **screening tool**. It answers: "Is there vibration? Is it getting worse?" at negligible cost.

VibroSense-1 is the **diagnostic tool**. It answers: "What kind of fault? Which frequency band? Is it bearing or imbalance?" at 300 uW always-on.

**For 80% of industrial vibration monitoring deployments, the ISM330DHCX MLC is good enough.** Most customers just want an alarm when vibration exceeds a threshold, then send an analyst with a handheld to diagnose. The MLC does this for $0 incremental.

**For the 20% that need always-on diagnostics** (remote/inaccessible equipment, hazardous areas, battery-powered nodes where MCU wakeup is too expensive), VibroSense-1 is structurally better. But that 20% is a smaller market: ~$40-100M TAM, not $500M.

The honest competitive threat is not that the MLC is technically better — it clearly is not for vibration diagnostics. The threat is that **"good enough" kills "better" when "good enough" is free.**

---

## 13. How to Compete Against the MLC

1. **Do not compete on basic vibration monitoring.** The MLC is free and good enough. Concede this market.

2. **Compete on diagnostic depth.** Emphasize 4-class fault ID, envelope analysis, ISO 10816 features — capabilities the MLC provably lacks.

3. **Compete on always-on power at full bandwidth.** The MLC at full bandwidth costs ~1 mW (sensor only) and still cannot do frequency analysis. VibroSense-1 does it at 300 uW.

4. **Target remote/inaccessible installations** where sending an analyst is impractical: offshore platforms, underground mines, remote pumping stations, wind turbines.

5. **Complement, do not replace.** Position VibroSense-1 alongside the ISM330DHCX, not instead of it. The ISM330DHCX provides the IMU data; VibroSense-1 provides the vibration diagnostics. They coexist on the same node.

6. **Publish accuracy comparisons.** Train a decision tree on the CWRU bearing dataset, run it on MLC-compatible features (mean, variance, peak-to-peak at low ODR), and compare accuracy to VibroSense-1's 5-band + MAC. The MLC will fail at multi-class bearing fault identification. Publish this openly.

---

## Sources

- [ISM330DHCX Product Page](https://www.st.com/en/mems-and-sensors/ism330dhcx.html)
- [ISM330DHCX Datasheet](https://www.st.com/resource/en/datasheet/ism330dhcx.pdf)
- [AN5392: ISM330DHCX Machine Learning Core](https://www.st.com/resource/en/application_note/an5392-ism330dhcx-machine-learning-core-stmicroelectronics.pdf)
- [AN5388: ISM330DHCX Finite State Machine](https://www.st.com/resource/en/application_note/an5388-ism330dhcx-finite-state-machine-stmicroelectronics.pdf)
- [MLC Settings for ISM330DHCX](https://stedgeai-dc.st.com/assets/embedded-docs/mlc_ism330dhcx_settings.html)
- [ST MLC GitHub Repository](https://github.com/STMicroelectronics/STMems_Machine_Learning_Core)
- [ISM330DHCX Vibration Monitoring Example](https://github.com/STMicroelectronics/STMems_Machine_Learning_Core/blob/master/application_examples/ism330dhcx/Vibration%20monitoring/README.md)
- [ISM330BX Product Page](https://www.st.com/en/mems-and-sensors/ism330bx.html)
- [ISM330IS (ISPU) Blog Post](https://blog.st.com/ism330is-onlife/)
- [STEVAL-STWINKT1B Product Page](https://www.st.com/en/evaluation-tools/steval-stwinkt1b.html)
- [FP-AI-MONITOR1](https://www.st.com/en/embedded-software/fp-ai-monitor1.html)
- [ST Condition Monitoring Reference Design SL-PREDMNT-S2C](https://www.st.com/en/solutions-reference-designs/sl-predmnt-s2c.html)
- [ST Fan Anomaly Detection Case Study](https://www.st.com/content/st_com/en/st-edge-ai-suite/case-studies/fan-anomaly-detection-based-on-vibrations.html)
- [ST Pump Anomaly Detection Case Study](https://www.st.com/content/st_com/en/st-edge-ai-suite/case-studies/pump-anomaly-detection-based-on-vibrations.html)
- [ST Motor Anomaly Detection Case Study](https://www.st.com/content/st_com/en/st-edge-ai-suite/case-studies/anomaly-detection-in-an-engine-running-at-different-speeds.html)
- [LSM6DSRX and ISM330DHCX Blog](https://blog.st.com/lsm6dsrx-ism330dhcx/)
- [ISPU vs MLC Community Discussion](https://community.st.com/t5/edge-ai/ispu-vs-mlc/td-p/693348)
- [ISM330DHCX vs ISM330BX vs LSM6DSV32X](https://community.st.com/t5/mems-sensors/ism330dhcx-vs-ism330bx-vs-lsm6dsv32x/td-p/696146)
- [ISM330DHCX Accelerometer Bandwidth Discussion](https://community.st.com/t5/mems-sensors/ism330dhcx-accelerometer-usable-bandwidth/td-p/50728)
- [NanoEdge AI Studio PdM Tutorial](https://wiki.st.com/stm32mcu/wiki/AI:How_to_Build_an_Anomaly_Detection_Project_for_Predictive_Maintenance_with_NanoEdge_AI_Studio)
- [DigiKey ISM330DHCXTR](https://www.digikey.com/en/products/detail/stmicroelectronics/ISM330DHCXTR/10409727) — $6.80 unit price
