# Block 10 — Full-Chain Integration and Verification: Program

## Overview

This is the **final deliverable** of the VibroSense-1 project. It connects
every analog and digital block into a complete chip-level simulation, applies
real bearing vibration data, and measures the system's actual performance.

The numbers produced here are the chip's **proven specifications**. They go
into the top-level README. No rounding up, no marketing language — just
measured results from a transistor-level simulation on a real PDK.

---

## SOTA Context: Where We Sit

### Commercial Always-On Vibration / Analog ML Chips

| Chip | Vendor | Power | Accuracy | Status | Notes |
|------|--------|-------|----------|--------|-------|
| AML100 | Aspinity | <100 uA (~180 uW) | "high" (no published number) | Shipping 2024 | RAMP architecture, general-purpose analog ML |
| VibroSense | POLYN | 34 uW | >90% (marketing) | Low-volume 2024 | Vibration-specific, analog neural network |
| MAX78000 | Analog Devices | ~500 uW (CNN active) | 99%+ (digital CNN) | Shipping | Not always-on, wakes for inference |
| MCU + FFT | Various | 1-10 mW | 95-99% | Standard approach | ARM Cortex-M4 + DSP, always-on impossible |

### Our VibroSense-1 Target

| Metric | Target | Honest expectation |
|--------|--------|--------------------|
| Total power | <300 uW | 200-400 uW |
| Classification accuracy | >80% (analog) | 80-88% |
| Detection latency | <500 ms | 100-300 ms |
| False alarm rate | <1 per hour | 0 over 10s simulation |
| Technology | SkyWater 130nm | Real, open-source PDK |

### Why 300 uW and Not 34 uW Like POLYN?

Honest reasons our power is 6-9x worse than POLYN's claim:

1. **130nm vs custom process.** POLYN likely uses a more advanced node or
   custom analog process. SkyWater 130nm is an older, general-purpose CMOS
   process not optimized for ultra-low-power analog.

2. **No proprietary circuit techniques.** POLYN has patents on their analog
   neuron implementation. We use standard textbook circuits (Tow-Thomas
   filters, Gilbert cell multipliers, etc.).

3. **Conservative design margins.** Every block was designed with margin
   for process variation, temperature, and supply noise. POLYN's published
   number may be a typical-case measurement.

4. **First silicon.** This is a paper design verified in simulation. POLYN
   has iterated through multiple silicon runs.

5. **We show our work.** Every transistor, every bias current, every
   capacitor value is documented and simulatable. POLYN's 34 uW is a
   datasheet number with no published circuit details.

300 uW at 130nm for a complete analog ML vibration classifier is a legitimate
result. It is 10-30x better than the MCU+FFT approach and demonstrates that
the analog computing paradigm provides real power savings for this application.

---

## Integration Architecture

### Top-Level Block Diagram

```
                    VDD (1.8V)                     VSSA (0V)
                      |                               |
                 +----+----+                          |
                 |  BIAS   | (Block 00)               |
                 | Generator|                          |
                 +----+----+                          |
                      | Ibias (1uA, 5uA, 10uA)       |
           +----------+----------+----------+         |
           |          |          |          |         |
      +----+----+ +---+---+ +---+---+ +----+---+    |
      |   PGA   | | BPF1  | | BPF2  | | BPF3   |   |
      |(Block 02)| |(Blk03)| |(Blk03)| |(Blk03) |   |
      +----+----+ +---+---+ +---+---+ +----+---+    |
           |          |          |          |         |
    VIN -->+          |          |          |     +---+---+ +---+---+
           |     +----+----+----+----+     |     | BPF4  | | BPF5  |
           |     |    |    |    |    |     |     |(Blk03)| |(Blk03)|
           |  +--+--+ | +--+--+ | +--+--+ |     +---+---+ +---+---+
           |  |ENV1 | | |ENV2 | | |ENV3 | |         |         |
           |  |(B04)| | |(B04)| | |(B04)| |     +---+---+ +---+---+
           |  +--+--+ | +--+--+ | +--+--+ |     |ENV4   | |ENV5   |
           |     |     |    |    |    |    |     |(B04)  | |(B04)  |
           |     |     |    |    |    |    |     +---+---+ +---+---+
           |     |     |    |    |    |    |         |         |
      +----+----+|     |    |    |    |    +---------+---------+
      |  RMS    ||     |    |    |    |    |
      | (Blk05)||     |    |    |    |    |
      +----+----+     |    |    |    |    |
           |     |     |    |    |    |    |
      +----+----+     |    |    |    |    |
      | CREST  |      |    |    |    |    |
      | (Blk05)|      |    |    |    |    |
      +----+----+     |    |    |    |    |
           |     |     |    |    |    |    |
           +-----+-----+----+----+----+----+
           |  8 feature voltages (0-1.8V)  |
           +-------------------------------+
                          |
                   +------+------+
                   | CLASSIFIER  | (Block 06)
                   | 32 MACs +   |
                   | comparator  |<-- weights from registers
                   +------+------+
                          |
                    class_result[3:0]
                    class_valid
                          |
                   +------+------+
                   |   DIGITAL   | (Block 08)
                   | SPI + regs  |<---> SPI bus (external MCU)
                   | + FSM +     |
                   | debounce    |---> IRQ_N
                   +------+------+
                          |
                   +------+------+
                   |    ADC      | (Block 07)
                   | (debug/     |---> ADC_DATA to digital regs
                   |  monitoring)|
                   +-------------+
```

### Netlist Hierarchy

```spice
* vibrosense1_top.spice — Top-level netlist

.include ../00_bias/bias_generator.spice
.include ../01_ota/ota.spice
.include ../02_pga/pga.spice
.include ../03_filters/bpf.spice
.include ../04_envelope/envelope.spice
.include ../05_rms_crest/rms.spice
.include ../05_rms_crest/crest.spice
.include ../06_classifier/classifier.spice
.include ../07_adc/adc.spice
.include ./netlists/digital_wrapper.spice

.lib /path/to/sky130A/libs.tech/ngspice/sky130.lib.spice tt

* Supply
Vdd vdd gnd 1.8
Vss vss gnd 0

* Bias generator
Xbias vdd vss ibias_1u ibias_5u ibias_10u bias_generator

* PGA
Xpga vin vout_pga ibias_5u vdd vss gain[1] gain[0] pga

* Band-pass filters (5 instances)
Xbpf1 vout_pga vbpf1 ibias_1u vdd vss tune1[3:0] bpf params: fc=300 bw=400
Xbpf2 vout_pga vbpf2 ibias_1u vdd vss tune2[3:0] bpf params: fc=1000 bw=1000
Xbpf3 vout_pga vbpf3 ibias_1u vdd vss tune3[3:0] bpf params: fc=2250 bw=1500
Xbpf4 vout_pga vbpf4 ibias_1u vdd vss tune4[3:0] bpf params: fc=3750 bw=1500
Xbpf5 vout_pga vbpf5 ibias_1u vdd vss tune5[3:0] bpf params: fc=5200 bw=1400

* Envelope detectors (5 instances)
Xenv1 vbpf1 venv1 ibias_1u vdd vss envelope
Xenv2 vbpf2 venv2 ibias_1u vdd vss envelope
Xenv3 vbpf3 venv3 ibias_1u vdd vss envelope
Xenv4 vbpf4 venv4 ibias_1u vdd vss envelope
Xenv5 vbpf5 venv5 ibias_1u vdd vss envelope

* RMS-to-DC converter
Xrms vout_pga vrms ibias_5u vdd vss rms_converter

* Crest factor
Xcrest vout_pga vrms vcrest ibias_1u vdd vss crest_detector

* Classifier (8 inputs: 5 envelopes + rms + crest + kurtosis_approx)
Xclass venv1 venv2 venv3 venv4 venv5 vrms vcrest vkurt
+       class_result[3:0] class_valid
+       weights[31:0] thresh[7:0]
+       fsm_sample fsm_evaluate fsm_compare
+       ibias_10u vdd vss classifier

* Digital control (behavioral SPICE wrapper around Verilog)
Xdigital sck mosi cs_n miso irq_n
+         gain[1:0] tune1[3:0] tune2[3:0] tune3[3:0] tune4[3:0] tune5[3:0]
+         weights[31:0] thresh[7:0] debounce[3:0]
+         class_result[3:0] class_valid
+         fsm_sample fsm_evaluate fsm_compare
+         clk rst_n vdd vss digital_wrapper
```

---

## Stimulus Generation

### Converting CWRU Data to Analog Waveforms

The CWRU dataset contains digital accelerometer samples at 12 kHz. To drive
the analog input of VibroSense-1, we must convert these to time-domain voltage
waveforms.

```python
# generate_stimuli.py

import numpy as np
import scipy.io

def cwru_to_pwl(mat_file, output_file, fs=12000, v_scale=0.1,
                v_offset=0.9, duration=2.0):
    """Convert CWRU .mat data to SPICE PWL stimulus.

    v_scale: volts per g (accelerometer sensitivity)
    v_offset: DC bias (mid-supply for 1.8V supply)
    duration: seconds of data to export
    """
    mat = scipy.io.loadmat(mat_file)
    de_key = [k for k in mat.keys() if 'DE_time' in k][0]
    signal = mat[de_key].flatten()

    n_samples = int(duration * fs)
    signal = signal[:n_samples]

    # Scale to voltage: sensor output in g, convert to volts
    # Typical bearing vibration: 0.1-10 g
    # With v_scale=0.1 V/g and v_offset=0.9V: signal stays in 0-1.8V
    voltage = signal * v_scale + v_offset

    # Clip to supply rails
    voltage = np.clip(voltage, 0.0, 1.8)

    with open(output_file, 'w') as f:
        f.write(f"* CWRU bearing data: {mat_file}\n")
        f.write(f"* {n_samples} samples at {fs} Hz, {duration} sec\n")
        f.write(f"* v_scale={v_scale} V/g, v_offset={v_offset} V\n")
        f.write(f"Vin vin gnd PWL(\n")
        for i in range(n_samples):
            t = i / fs
            f.write(f"+  {t:.9f} {voltage[i]:.6f}\n")
        f.write(f"+  {duration:.9f} {v_offset:.6f})\n")

# Generate 4 test cases
cwru_to_pwl('data/normal.mat', 'stimuli/normal_stimulus.pwl', duration=2.0)
cwru_to_pwl('data/inner_race.mat', 'stimuli/inner_race_stimulus.pwl', duration=2.0)
cwru_to_pwl('data/outer_race.mat', 'stimuli/outer_race_stimulus.pwl', duration=2.0)
cwru_to_pwl('data/ball.mat', 'stimuli/ball_stimulus.pwl', duration=2.0)
```

### Stimulus Parameters

| Test Case | CWRU File | Duration | Expected Class | Expected IRQ |
|-----------|-----------|----------|----------------|--------------|
| Normal | 97.mat (normal, 0hp) | 2.0 s | 0 (normal) | never asserts |
| Inner Race | 105.mat (IR007, 0hp) | 2.0 s | 1 (inner race) | asserts <500ms |
| Outer Race | 130.mat (OR007, 0hp) | 2.0 s | 3 (outer race) | asserts <500ms |
| Ball | 118.mat (B007, 0hp) | 2.0 s | 2 (ball) | asserts <500ms |

Each test case runs for at least 1 second of real-time simulation (2 seconds
for margin). At 1 ms classifier period, this gives 1000-2000 classification
cycles per test case.

---

## Simulation Procedure

### Step 1: Assemble Top-Level Netlist

```python
# run_fullchain.py — Step 1

def assemble_netlist():
    """Assemble the full-chain SPICE netlist from block netlists."""
    # Verify all block netlists exist
    required_files = [
        '../00_bias/bias_generator.spice',
        '../01_ota/ota.spice',
        '../02_pga/pga.spice',
        '../03_filters/bpf.spice',
        '../04_envelope/envelope.spice',
        '../05_rms_crest/rms.spice',
        '../05_rms_crest/crest.spice',
        '../06_classifier/classifier.spice',
        '../07_adc/adc.spice',
    ]
    for f in required_files:
        if not os.path.exists(f):
            raise FileNotFoundError(f"Missing block netlist: {f}")

    # Load trained weights from Block 09
    with open('../09_training/results/trained_weights.json') as f:
        weights = json.load(f)

    # Generate weight .param file inclusion
    # (already done by Block 09, just verify it exists)
    assert os.path.exists('../09_training/results/weights_spice.txt')
```

### Step 2: Configure Digital Block

The digital block must be initialized via SPI before simulation. In SPICE,
this is done with a piecewise-linear SPI stimulus that writes all configuration
registers at the start of simulation.

```python
def generate_spi_config_stimulus(weights_json, output_file):
    """Generate SPI write sequence as SPICE stimulus.

    Writes all 14 registers via SPI at simulation start (t=0 to t=1ms).
    After 1ms, the chip is configured and real test data begins.
    """
    with open(weights_json) as f:
        w = json.load(f)

    # Register writes needed:
    # 0x00: GAIN = 2 (16x)
    # 0x01-0x05: TUNE1-5 = center values
    # 0x06-0x09: WEIGHT0-3 from training
    # 0x0A: THRESH from training
    # 0x0B: DEBOUNCE = 3

    writes = [
        (0x00, 0x02),  # GAIN = 16x
        (0x01, 0x08),  # TUNE1 = center
        (0x02, 0x08),  # TUNE2 = center
        (0x03, 0x08),  # TUNE3 = center
        (0x04, 0x08),  # TUNE4 = center
        (0x05, 0x08),  # TUNE5 = center
    ]

    # Pack quantized weight indices into register bytes
    q_idx = w['quantized_indices']  # 4x8 array
    for reg in range(4):
        byte_val = (q_idx[reg][2*0+1] << 4) | q_idx[reg][2*0]
        # Actually: WEIGHT0 = weights[0] and weights[1] packed
        # q_idx is [class][feature], we pack as [feat1_nibble:feat0_nibble]
        # This packing must match the digital register file spec
        hi = q_idx[reg // 2][(reg % 2) * 2 + 1] & 0xF
        lo = q_idx[reg // 2][(reg % 2) * 2] & 0xF
        # Simplification: just write the raw bytes from training
        pass  # actual packing depends on register file bit mapping

    # ... generate PWL waveforms for SCK, MOSI, CS_N
```

### Step 3: Run SPICE Simulation

```bash
# For each test case:
ngspice -b -o results/fullchain_normal.log \
  -r results/fullchain_normal.raw \
  netlists/vibrosense1_top.spice \
  stimuli/normal_stimulus.pwl

ngspice -b -o results/fullchain_inner.log \
  -r results/fullchain_inner.raw \
  netlists/vibrosense1_top.spice \
  stimuli/inner_race_stimulus.pwl

ngspice -b -o results/fullchain_outer.log \
  -r results/fullchain_outer.raw \
  netlists/vibrosense1_top.spice \
  stimuli/outer_race_stimulus.pwl

ngspice -b -o results/fullchain_ball.log \
  -r results/fullchain_ball.raw \
  netlists/vibrosense1_top.spice \
  stimuli/ball_stimulus.pwl
```

**Expected simulation time:** Each 2-second real-time simulation with full
transistor-level models will take approximately 2-8 hours on a modern machine,
depending on convergence. Total: 8-32 hours for all 4 test cases.

**Convergence tips:**

- Use `.option method=gear` for better convergence with switched-capacitor circuits
- Set `.option reltol=1e-3` (relaxed tolerance, acceptable for this analysis)
- Use `.option gmin=1e-12` to help with floating nodes
- Set `.option itl1=500 itl2=200` for more iterations before giving up
- If convergence fails: add small parasitic capacitors (1fF) on high-impedance nodes

### Step 4: Parse SPICE Results

```python
# analyze_results.py

import numpy as np

def parse_ngspice_raw(raw_file):
    """Parse ngspice binary raw file and extract node voltages."""
    # Use PySpice or custom parser
    # Extract: time, v(vin), v(venv1)-v(venv5), v(vrms), v(vcrest),
    #          v(class_result), v(irq_n), i(vdd)
    pass

def extract_classifications(time, class_result, class_valid, fs_class=1000):
    """Extract classification results at each FSM cycle.

    class_result is a 4-bit bus represented as a voltage (digital).
    class_valid is a strobe pulse.
    Returns: list of (time, class) tuples.
    """
    classifications = []
    # Find rising edges of class_valid
    valid_edges = np.where(np.diff(class_valid > 0.9) > 0)[0]
    for edge in valid_edges:
        t = time[edge]
        # Decode 4-bit class_result voltage to integer
        # In a real mixed-signal sim, this would be a digital bus
        cls = int(np.round(class_result[edge] / 0.45))  # 0.45V per level
        classifications.append((t, cls))
    return classifications

def measure_detection_latency(classifications, expected_class, t_fault_onset):
    """Measure time from fault onset to first correct detection."""
    for t, cls in classifications:
        if t > t_fault_onset and cls == expected_class:
            return t - t_fault_onset
    return float('inf')  # never detected

def measure_irq_latency(time, irq_n, t_fault_onset):
    """Measure time from fault onset to IRQ assertion."""
    # Find first falling edge of irq_n after t_fault_onset
    idx_start = np.searchsorted(time, t_fault_onset)
    irq_after = irq_n[idx_start:]
    time_after = time[idx_start:]
    falling = np.where(np.diff(irq_after < 0.9) > 0)[0]
    if len(falling) > 0:
        return time_after[falling[0]] - t_fault_onset
    return float('inf')
```

### Step 5: Power Measurement

```python
def measure_power(raw_data, t_start, t_end):
    """Measure average power consumption over a time window.

    Power = average(Vdd * Idd) over [t_start, t_end].
    """
    time = raw_data['time']
    mask = (time >= t_start) & (time <= t_end)

    vdd = 1.8  # volts
    idd = -raw_data['i(vdd)'][mask]  # ngspice convention: current into supply is negative

    power = vdd * np.mean(idd)
    return power

def measure_block_power(raw_data, t_start, t_end):
    """Measure per-block power by monitoring each supply branch.

    Each block has its own Vdd connection with a 0-ohm sense resistor
    (or separate voltage source) for current measurement.
    """
    blocks = {
        'bias':       'i(v_vdd_bias)',
        'pga':        'i(v_vdd_pga)',
        'bpf1':       'i(v_vdd_bpf1)',
        'bpf2':       'i(v_vdd_bpf2)',
        'bpf3':       'i(v_vdd_bpf3)',
        'bpf4':       'i(v_vdd_bpf4)',
        'bpf5':       'i(v_vdd_bpf5)',
        'env1':       'i(v_vdd_env1)',
        'env2':       'i(v_vdd_env2)',
        'env3':       'i(v_vdd_env3)',
        'env4':       'i(v_vdd_env4)',
        'env5':       'i(v_vdd_env5)',
        'rms':        'i(v_vdd_rms)',
        'crest':      'i(v_vdd_crest)',
        'classifier': 'i(v_vdd_class)',
        'adc':        'i(v_vdd_adc)',
        'digital':    'i(v_vdd_dig)',
    }

    time = raw_data['time']
    mask = (time >= t_start) & (time <= t_end)
    vdd = 1.8

    breakdown = {}
    total = 0
    for name, probe in blocks.items():
        current = -raw_data[probe][mask]
        power = vdd * np.mean(current)
        breakdown[name] = power
        total += power

    breakdown['total'] = total
    return breakdown
```

### Expected Power Breakdown

| Block | Expected Power | Notes |
|-------|---------------|-------|
| Bias generator | 5-10 uW | Always on, reference currents |
| PGA | 15-30 uW | Single OTA, moderate bias |
| BPF1-5 (total) | 50-100 uW | 5 x Tow-Thomas = 10 OTAs |
| ENV1-5 (total) | 25-50 uW | 5 x rectifier + LPF |
| RMS converter | 10-20 uW | Squarer + filter |
| Crest detector | 5-10 uW | Peak detector / RMS |
| Classifier | 30-60 uW | 32 MACs + comparator |
| ADC | 20-40 uW | SAR ADC, intermittent |
| Digital | 1-3 uW | Synthesis estimate |
| **Total** | **161-323 uW** | **Target: <300 uW** |

The power budget is tight but achievable. The biggest consumers are the
BPF bank (10 OTAs) and the classifier (32 multipliers). If power exceeds
300 uW, the first optimization targets are:

1. Reduce OTA bias currents (trade bandwidth for power)
2. Duty-cycle the classifier (run at 100 Hz instead of 1000 Hz)
3. Power-gate the ADC (only turn on for debug reads)

---

## Golden Model Comparison

### Purpose

The Python golden model (Block 09) processes the same input data using
ideal digital filters and floating-point arithmetic. By comparing the SPICE
results to the golden model, we quantify the accuracy loss from:

- Analog filter non-idealities (finite Q, passband ripple)
- Envelope detector errors (rectifier dead zone, LPF droop)
- Capacitor mismatch in classifier weights
- Comparator offset
- Noise

### Comparison Procedure

```python
# compare_golden.py

def run_golden_model(cwru_file, weights_json, fs=12000):
    """Run Python golden model on raw CWRU data.

    Returns: list of (time, class) for each 1ms classification window.
    """
    from feature_extraction import extract_features
    import json

    mat = scipy.io.loadmat(cwru_file)
    signal = mat[[k for k in mat if 'DE_time' in k][0]].flatten()

    with open(weights_json) as f:
        w = json.load(f)

    W = np.array(w['quantized_weights'])
    B = np.array(w['quantized_biases'])
    norm_min = np.array(w['normalization']['min'])
    norm_max = np.array(w['normalization']['max'])

    # Process in 1ms windows (12 samples at 12kHz)
    # But feature extraction needs longer windows — use 0.5s sliding window
    # with 1ms step
    window_size = int(0.5 * fs)  # 6000 samples
    step_size = int(0.001 * fs)  # 12 samples (1ms)

    classifications = []
    for start in range(0, len(signal) - window_size, step_size):
        window = signal[start : start + window_size]
        features = extract_features(window, fs)
        # Normalize
        features_norm = (features - norm_min) / (norm_max - norm_min + 1e-10)
        features_norm = np.clip(features_norm, 0, 1)
        # Classify
        logits = features_norm @ W.T + B
        cls = np.argmax(logits)
        t = (start + window_size) / fs  # time of classification
        classifications.append((t, cls))

    return classifications

def compare_spice_to_golden(spice_results, golden_results, tolerance_ms=5):
    """Compare SPICE classification to golden model.

    tolerance_ms: allowed time offset between SPICE and golden results.
    """
    # Align by time
    matches = 0
    total = 0
    disagreements = []

    for t_g, cls_g in golden_results:
        # Find nearest SPICE result
        t_diffs = [abs(t_s - t_g) for t_s, _ in spice_results]
        nearest_idx = np.argmin(t_diffs)
        t_s, cls_s = spice_results[nearest_idx]

        if t_diffs[nearest_idx] < tolerance_ms / 1000:
            total += 1
            if cls_s == cls_g:
                matches += 1
            else:
                disagreements.append((t_g, cls_g, cls_s))

    agreement = matches / total if total > 0 else 0
    return agreement, disagreements
```

---

## Accuracy Measurement

### End-to-End Classification Accuracy

For each test case, compare the SPICE classification output to the known
ground truth:

```python
def compute_accuracy(classifications, expected_class, t_start, t_end):
    """Compute classification accuracy over a time window.

    classifications: list of (time, class) from SPICE
    expected_class: ground truth class for this test case
    t_start, t_end: evaluation window (exclude startup transient)
    """
    correct = 0
    total = 0
    for t, cls in classifications:
        if t_start <= t <= t_end:
            total += 1
            if cls == expected_class:
                correct += 1
    return correct / total if total > 0 else 0
```

### Expected Accuracy Budget

| Stage | Accuracy | Cumulative Loss | Notes |
|-------|----------|-----------------|-------|
| Python float | 88-93% | baseline | Block 09 result |
| 4-bit quantization | 85-90% | -3 pp | Block 09 result |
| Analog noise (2%) | 82-88% | -3 pp | Block 09 noise sim |
| Filter mismatch | -1 to -2 pp | -1.5 pp | Gm-C vs ideal Butterworth |
| Envelope error | -0.5 to -1 pp | -0.75 pp | Dead zone, droop |
| Capacitor mismatch | -0.5 to -1 pp | -0.75 pp | Weight errors |
| **End-to-end** | **80-85%** | **~-8 pp total** | **Target: >80%** |

If end-to-end accuracy falls below 80%, investigate which stage causes the
most loss. The block-by-block comparison (SPICE node voltages vs Python
intermediate values) will pinpoint the culprit.

---

## Detection Latency Measurement

### Definition

Detection latency = time from fault onset to IRQ_N assertion.

Components:
1. **Signal propagation:** input signal propagates through PGA, filters,
   envelope detectors. The envelope LPF has a 10 Hz cutoff (tau=16ms),
   so the envelope takes ~50ms to settle after a step change.
2. **Classifier settling:** the analog MAC needs one FSM cycle (1ms) to
   produce a result after features are stable.
3. **Debounce:** with DEBOUNCE=3, need 3 consecutive anomaly detections.
   At 1ms classifier period, this adds 3ms.
4. **Total expected: 50ms (envelope) + 1ms (classifier) + 3ms (debounce) = ~54ms**

But the actual latency is longer because:
- The fault signal ramps up gradually (not a step)
- The envelope detector has a tail response
- Some classifier cycles may misclassify during the transient

**Realistic expected latency: 100-300ms.**

### Measurement

```python
def measure_all_latencies(results):
    """Measure detection latency for all fault test cases."""
    latencies = {}

    # For fault test cases, the fault is present from t=0
    # But we add a 100ms settling time for the analog chain
    t_fault_onset = 0.1  # seconds (after initial transient)

    for case in ['inner_race', 'outer_race', 'ball']:
        spice_data = parse_ngspice_raw(f'results/fullchain_{case}.raw')
        time = spice_data['time']
        irq_n = spice_data['v(irq_n)']

        latency = measure_irq_latency(time, irq_n, t_fault_onset)
        latencies[case] = latency
        print(f"{case}: IRQ latency = {latency*1000:.1f} ms")

    return latencies
```

---

## False Alarm Measurement

### Normal Signal Test

Run the normal test case for the full 2 seconds. IRQ_N must never assert.

```python
def check_false_alarms(raw_file, t_start=0.1, t_end=2.0):
    """Verify zero false alarms on normal signal."""
    data = parse_ngspice_raw(raw_file)
    time = data['time']
    irq_n = data['v(irq_n)']

    mask = (time >= t_start) & (time <= t_end)
    irq_window = irq_n[mask]

    # IRQ_N should be high (>1.6V) for the entire window
    false_alarms = np.sum(irq_window < 0.9)  # count samples where IRQ asserted
    if false_alarms > 0:
        # Find when
        time_window = time[mask]
        fa_times = time_window[irq_window < 0.9]
        print(f"FALSE ALARM: {false_alarms} samples, first at {fa_times[0]:.6f}s")
        return False, false_alarms, fa_times
    else:
        print("Normal test: PASS — zero false alarms")
        return True, 0, []
```

---

## Reporting

### Power Breakdown Report

```python
def generate_power_report(breakdown, filename):
    """Generate formatted power breakdown report."""
    with open(filename, 'w') as f:
        f.write("=" * 50 + "\n")
        f.write("VibroSense-1 Power Breakdown\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"{'Block':<20s} {'Power (uW)':>12s} {'% Total':>10s}\n")
        f.write("-" * 42 + "\n")

        total = breakdown['total']
        for name, power in sorted(breakdown.items()):
            if name == 'total':
                continue
            pct = 100 * power / total if total > 0 else 0
            f.write(f"{name:<20s} {power*1e6:>12.1f} {pct:>9.1f}%\n")

        f.write("-" * 42 + "\n")
        f.write(f"{'TOTAL':<20s} {total*1e6:>12.1f} {'100.0':>9s}%\n")
        f.write("\n")
        f.write(f"Supply voltage: 1.8 V\n")
        f.write(f"Total current:  {total/1.8*1e6:.1f} uA\n")

        if total * 1e6 < 300:
            f.write(f"\nPASS: Total power {total*1e6:.1f} uW < 300 uW target\n")
        else:
            f.write(f"\nFAIL: Total power {total*1e6:.1f} uW > 300 uW target\n")
```

### Comparison Table

```python
def generate_comparison_table(our_results, filename):
    """Generate honest comparison with competing approaches."""
    with open(filename, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("VibroSense-1 vs. Competing Approaches\n")
        f.write("=" * 80 + "\n\n")

        headers = ['Metric', 'VibroSense-1', 'POLYN', 'Aspinity AML100',
                    'MCU+FFT']
        widths = [25, 15, 15, 15, 15]

        # Header
        f.write('|')
        for h, w in zip(headers, widths):
            f.write(f" {h:<{w}s}|")
        f.write('\n')
        f.write('|' + '|'.join(['-' * (w+1) for w in widths]) + '|\n')

        # Rows
        rows = [
            ('Power',
             f"{our_results['power_uw']:.0f} uW",
             '34 uW', '<180 uW', '1-10 mW'),
            ('Accuracy',
             f"{our_results['accuracy']:.0f}%",
             '>90%*', 'unpublished', '95-99%'),
            ('Latency',
             f"{our_results['latency_ms']:.0f} ms",
             'unpublished', 'unpublished', '<10 ms'),
            ('Technology',
             'SKY130 (130nm)', 'custom', 'custom', '40-90nm'),
            ('Verification',
             'SPICE sim', 'silicon', 'silicon', 'silicon'),
            ('Open source',
             'YES', 'no', 'no', 'partial'),
            ('Always-on',
             'YES', 'YES', 'YES', 'NO'),
            ('Gate count (digital)',
             f"~{our_results['gates']} gates",
             'unpublished', 'unpublished', '>100k gates'),
        ]

        for row in rows:
            f.write('|')
            for val, w in zip(row, widths):
                f.write(f" {val:<{w}s}|")
            f.write('\n')

        f.write('\n')
        f.write("* POLYN 90% accuracy is a marketing claim with no published\n")
        f.write("  methodology or test conditions. Our accuracy is measured on\n")
        f.write("  the CWRU bearing dataset with a defined test/train split.\n\n")

        f.write("Key takeaways:\n")
        f.write("1. VibroSense-1 is 10-30x more power-efficient than MCU+FFT\n")
        f.write("2. VibroSense-1 is 6-9x worse than POLYN's claim, but on a\n")
        f.write("   general-purpose 130nm process vs POLYN's custom process\n")
        f.write("3. VibroSense-1 is the ONLY design with full open-source\n")
        f.write("   transistor-level verification\n")
        f.write("4. Accuracy trade-off is intentional: 80-88% with 32 capacitors\n")
        f.write("   vs 99% with a CNN that needs 1000x more power\n")
```

### Final Specifications

```python
def generate_final_specs(results, filename):
    """Generate the final chip specifications for the top-level README."""
    with open(filename, 'w') as f:
        f.write("# VibroSense-1 — Proven Specifications\n\n")
        f.write("All numbers from transistor-level SPICE simulation on\n")
        f.write("SkyWater SKY130A PDK. Not estimated — measured.\n\n")

        f.write("## Performance\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Classification accuracy (CWRU) | "
                f"{results['accuracy']:.1f}% |\n")
        f.write(f"| Detection latency (fault to IRQ) | "
                f"{results['latency_ms']:.0f} ms |\n")
        f.write(f"| False alarm rate (10s normal) | "
                f"{results['false_alarms']} |\n")
        f.write(f"| Classification rate | 1000 Hz |\n")
        f.write(f"| Number of classes | 4 (normal + 3 fault types) |\n\n")

        f.write("## Power\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total power (active) | "
                f"{results['power_uw']:.0f} uW |\n")
        f.write(f"| Supply voltage | 1.8 V |\n")
        f.write(f"| Supply current | "
                f"{results['power_uw']/1.8:.0f} uA |\n\n")

        f.write("## Technology\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Process | SkyWater 130nm CMOS |\n")
        f.write(f"| PDK | SKY130A (open source) |\n")
        f.write(f"| Digital gates | ~{results['gates']} |\n")
        f.write(f"| Analog blocks | 17 (bias+PGA+5xBPF+5xENV+RMS+CREST+CLASS+ADC) |\n")
        f.write(f"| Classifier weights | 32 x 4-bit (capacitor array) |\n\n")

        f.write("## Verification Status\n\n")
        f.write("- [x] Each block individually verified in SPICE\n")
        f.write("- [x] Digital block synthesized and simulated with cocotb\n")
        f.write("- [x] Training pipeline validated on CWRU dataset\n")
        f.write("- [x] Full-chain SPICE simulation with real bearing data\n")
        f.write("- [ ] Layout (future work)\n")
        f.write("- [ ] Tape-out (future work)\n")
        f.write("- [ ] Silicon measurement (future work)\n")
```

---

## Execution Plan

### Prerequisites

1. All blocks 00-09 must be complete with passing testbenches
2. Trained weights exported from Block 09
3. CWRU dataset available for stimulus generation
4. Sufficient compute (8-32 hours of SPICE simulation)

### Run Order

```bash
cd vibrosense/10_fullchain

# Step 1: Generate stimuli from CWRU data
python scripts/generate_stimuli.py

# Step 2: Assemble top-level netlist
python scripts/run_fullchain.py --assemble

# Step 3: Run all 4 SPICE simulations (can be parallelized)
python scripts/run_fullchain.py --simulate normal &
python scripts/run_fullchain.py --simulate inner_race &
python scripts/run_fullchain.py --simulate outer_race &
python scripts/run_fullchain.py --simulate ball &
wait

# Step 4: Analyze results
python scripts/analyze_results.py

# Step 5: Compare to golden model
python scripts/compare_golden.py

# Step 6: Generate all reports and plots
python scripts/plot_results.py

# Step 7: Check pass/fail
python scripts/run_fullchain.py --check
```

---

## Waveform Plots to Generate

1. **Input stimulus:** raw CWRU waveform at chip input for each test case
2. **Filter outputs:** 5 BPF outputs showing frequency decomposition
3. **Envelope outputs:** 5 envelopes showing energy in each band
4. **Feature comparison:** SPICE feature voltages vs Python golden model
5. **Classification output:** class_result over time for each test case
6. **IRQ timing:** IRQ_N assertion/deassertion with latency annotation
7. **Power waveform:** instantaneous Idd over time, showing idle vs active
8. **Comparison bar chart:** VibroSense-1 vs POLYN vs Aspinity vs MCU+FFT

---

## PASS/FAIL Criteria

| Criterion | Target | Hard Fail |
|-----------|--------|-----------|
| End-to-end accuracy (all 4 classes) | >= 80% | < 70% |
| Normal class: zero false IRQs in 10s | 0 false alarms | >= 1 false alarm |
| Inner race detection | correct class | wrong class |
| Outer race detection | correct class | wrong class |
| Ball fault detection | correct class | wrong class |
| Detection latency (any fault) | < 500 ms | > 1000 ms |
| Total power | < 300 uW | > 600 uW |
| Total power (absolute max) | < 600 uW | > 600 uW |
| SPICE convergence | all 4 cases | any case fails to converge |
| Simulation duration | >= 1s real-time per case | < 0.5s |
| Golden model agreement | > 90% | < 75% |
| Power breakdown available | all blocks measured | any block missing |
| Comparison table generated | present | missing |
| Final specs generated | present | missing |

---

## What Happens If We Fail

If any hard-fail criterion is triggered, the response depends on which one:

| Failure | Root Cause Investigation | Fix |
|---------|------------------------|-----|
| Accuracy < 70% | Check feature extraction match, check weight loading | Re-verify Block 03-06 individually |
| False alarms | Check debounce logic, check classifier threshold | Increase DEBOUNCE, adjust THRESH |
| Wrong class detected | Check weight signs, check feature ordering | Verify Block 09 export matches Block 06 input |
| Latency > 1s | Check envelope time constant, check FSM period | Reduce LPF cutoff, increase classifier rate |
| Power > 600 uW | Check bias currents, look for shorts | Reduce OTA bias, power-gate ADC |
| Convergence failure | Check for floating nodes, check initial conditions | Add parasitic caps, set .ic on all nodes |
| Golden model disagree | Analog chain has non-ideality not modeled in Python | Update Python model or accept delta |

---

## This Is the Final Deliverable

The results from this block are not intermediate data. They are the
**proven specifications** of the VibroSense-1 chip. They go directly into
the project's top-level README with no modification, no rounding, no
marketing language.

If the chip achieves 82% accuracy at 280 uW, that is what we report.
If it achieves 78% at 350 uW, that is what we report — along with an
honest analysis of why it fell short and what would fix it.

The value of this project is not in achieving a specific number. It is in
having a **fully transparent, reproducible, open-source design** where every
transistor is accounted for and every claim can be verified by running the
simulation.
