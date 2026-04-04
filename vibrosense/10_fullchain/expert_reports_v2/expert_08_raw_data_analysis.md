# Expert Report 08: Full-Chain Raw Data Analysis

## 1. Data Availability

- normal: 20.1 MB
  Parsed: 42 variables, 59739 time points
  Time range: 0.0 ms to 200.0 ms
- inner_race: 22.1 MB
  Parsed: 42 variables, 65865 time points
  Time range: 0.0 ms to 157.4 ms
- outer_race: 24.4 MB
  Parsed: 42 variables, 72740 time points
  Time range: 0.0 ms to 195.9 ms
- ball: 21.6 MB
  Parsed: 42 variables, 64268 time points
  Time range: 0.0 ms to 149.6 ms

## 2. Input Signal Analysis

| Test Case | Vin mean (V) | Vin pp (mV) | Vin min (V) | Vin max (V) |
|-----------|-------------|-------------|-------------|-------------|
| normal       | 0.9004 | 40.2 | 0.8815 | 0.9218 |
| inner_race   | 0.9011 | 167.6 | 0.8202 | 0.9879 |
| outer_race   | 0.9009 | 103.5 | 0.8573 | 0.9608 |
| ball         | 0.9009 | 91.0 | 0.8610 | 0.9520 |

## 3. PGA Output Analysis

| Test Case | PGA mean (V) | PGA pp (mV) | PGA min (V) | PGA max (V) | Gain |
|-----------|-------------|-------------|-------------|-------------|------|
| normal       | 0.9431 | 486.4 | 0.5343 | 1.0207 | 12.1x |
| inner_race   | 0.9420 | 729.1 | 0.5387 | 1.2678 | 4.3x |
| outer_race   | 0.9424 | 589.2 | 0.5327 | 1.1220 | 5.7x |
| ball         | 0.9419 | 567.1 | 0.5347 | 1.1019 | 6.2x |

## 4. BPF Output Analysis (per channel)

### BPF Channel 1

| Test Case | Mean (V) | Vpp (mV) | Std (mV) |
|-----------|----------|----------|----------|
| normal       | 0.9018 | 65.34 | 11.00 |
| inner_race   | 0.9016 | 78.63 | 11.78 |
| outer_race   | 0.9011 | 80.99 | 11.98 |
| ball         | 0.9025 | 71.52 | 12.04 |

### BPF Channel 2

| Test Case | Mean (V) | Vpp (mV) | Std (mV) |
|-----------|----------|----------|----------|
| normal       | 0.9017 | 99.83 | 17.21 |
| inner_race   | 0.9017 | 145.63 | 24.13 |
| outer_race   | 0.9018 | 142.47 | 23.88 |
| ball         | 0.9022 | 104.52 | 20.01 |

### BPF Channel 3

| Test Case | Mean (V) | Vpp (mV) | Std (mV) |
|-----------|----------|----------|----------|
| normal       | 0.9015 | 55.57 | 8.53 |
| inner_race   | 0.9014 | 182.68 | 31.89 |
| outer_race   | 0.9017 | 196.65 | 31.06 |
| ball         | 0.9010 | 141.11 | 25.00 |

### BPF Channel 4

| Test Case | Mean (V) | Vpp (mV) | Std (mV) |
|-----------|----------|----------|----------|
| normal       | 0.9016 | 32.55 | 4.96 |
| inner_race   | 0.9014 | 186.32 | 29.85 |
| outer_race   | 0.9018 | 177.68 | 25.54 |
| ball         | 0.9009 | 135.68 | 25.41 |

### BPF Channel 5

| Test Case | Mean (V) | Vpp (mV) | Std (mV) |
|-----------|----------|----------|----------|
| normal       | 0.9016 | 22.58 | 3.56 |
| inner_race   | 0.9015 | 218.62 | 26.74 |
| outer_race   | 0.9018 | 124.10 | 15.79 |
| ball         | 0.9015 | 126.75 | 18.63 |

## 5. Envelope Output Analysis (per channel)

Using last 50ms window for settled values:

### Envelope Channel 1

| Test Case | Mean (V) | Mean-VCM (mV) | Std (mV) | Final (V) |
|-----------|----------|---------------|----------|-----------|
| normal       | 0.904341 | +4.341 | 2.549 | 0.908100 |
| inner_race   | 0.904341 | +4.341 | 2.545 | 0.905966 |
| outer_race   | 0.904071 | +4.071 | 2.608 | 0.909778 |
| ball         | 0.904424 | +4.424 | 2.570 | 0.912415 |

### Envelope Channel 2

| Test Case | Mean (V) | Mean-VCM (mV) | Std (mV) | Final (V) |
|-----------|----------|---------------|----------|-----------|
| normal       | 0.906419 | +6.419 | 2.057 | 0.907911 |
| inner_race   | 0.908798 | +8.798 | 2.533 | 0.908540 |
| outer_race   | 0.908550 | +8.550 | 2.489 | 0.907649 |
| ball         | 0.907986 | +7.986 | 2.227 | 0.905857 |

### Envelope Channel 3

| Test Case | Mean (V) | Mean-VCM (mV) | Std (mV) | Final (V) |
|-----------|----------|---------------|----------|-----------|
| normal       | 0.903244 | +3.244 | 0.784 | 0.902831 |
| inner_race   | 0.909686 | +9.686 | 4.046 | 0.911688 |
| outer_race   | 0.909379 | +9.379 | 4.700 | 0.905039 |
| ball         | 0.908111 | +8.111 | 2.904 | 0.903853 |

### Envelope Channel 4

| Test Case | Mean (V) | Mean-VCM (mV) | Std (mV) | Final (V) |
|-----------|----------|---------------|----------|-----------|
| normal       | 0.901932 | +1.932 | 0.426 | 0.901627 |
| inner_race   | 0.908498 | +8.498 | 4.272 | 0.910563 |
| outer_race   | 0.906848 | +6.848 | 4.085 | 0.903120 |
| ball         | 0.907646 | +7.646 | 3.301 | 0.903009 |

### Envelope Channel 5

| Test Case | Mean (V) | Mean-VCM (mV) | Std (mV) | Final (V) |
|-----------|----------|---------------|----------|-----------|
| normal       | 0.901454 | +1.454 | 0.284 | 0.901237 |
| inner_race   | 0.906376 | +6.376 | 3.924 | 0.906580 |
| outer_race   | 0.904244 | +4.244 | 2.351 | 0.902051 |
| ball         | 0.905361 | +5.361 | 2.433 | 0.901974 |

## 6. Cross-Channel Envelope Comparison (Last 50ms)

### Deviations from VCM (mV)

| Test Case | ENV1 | ENV2 | ENV3 | ENV4 | ENV5 | Max-Min |
|-----------|------|------|------|------|------|---------|
| normal       | +4.34 | +6.42 | +3.24 | +1.93 | +1.45 | 4.97 |
| inner_race   | +4.34 | +8.80 | +9.69 | +8.50 | +6.38 | 5.35 |
| outer_race   | +4.07 | +8.55 | +9.38 | +6.85 | +4.24 | 5.31 |
| ball         | +4.42 | +7.99 | +8.11 | +7.65 | +5.36 | 3.69 |

### Per-Channel Spread Across Test Cases (mV)

- ENV1: spread = 0.35 mV (min=+4.07, max=+4.42)
- ENV2: spread = 2.38 mV (min=+6.42, max=+8.80)
- ENV3: spread = 6.44 mV (min=+3.24, max=+9.69)
- ENV4: spread = 6.57 mV (min=+1.93, max=+8.50)
- ENV5: spread = 4.92 mV (min=+1.45, max=+6.38)

## 7. RMS and Peak Output Analysis

| Test Case | RMS out (V) | RMS ref (V) | Peak out (V) | RMS-Ref diff (mV) |
|-----------|-------------|-------------|--------------|-------------------|
| normal       | 1.5678 | 1.6162 | 1.0133 | -48.4 |
| inner_race   | 1.5653 | 1.6162 | 1.1336 | -50.9 |
| outer_race   | 1.5664 | 1.6162 | 1.0883 | -49.7 |
| ball         | 1.5675 | 1.6162 | 1.0638 | -48.6 |

## 8. Classifier Score Analysis


| Test Case | Score0 (Normal) | Score1 (Inner) | Score2 (Ball) | Score3 (Outer) | Winner |
|-----------|----------------|----------------|---------------|----------------|--------|
| normal       | (scores N/A) | | | | Outer (V=1.350) |
| inner_race   | (scores N/A) | | | | Inner (V=0.450) |
| outer_race   | (scores N/A) | | | | Inner (V=0.450) |
| ball         | (scores N/A) | | | | Outer (V=1.350) |

## 9. Where Exactly Is Differentiation Lost?

### Stage-by-stage discrimination metric (max spread across 4 cases)

| Stage | Cross-case spread (mV) | Assessment |
|-------|----------------------|------------|
| Input (Vin std)           | 8.77 | MARGINAL |
| PGA (std spread)          | 33.78 | GOOD |
| BPF1 (std spread)         | 1.04 | MARGINAL |
| BPF2 (std spread)         | 6.92 | MARGINAL |
| BPF3 (std spread)         | 23.36 | GOOD |
| BPF4 (std spread)         | 24.89 | GOOD |
| BPF5 (std spread)         | 23.18 | GOOD |
| ENV1 (mean spread)        | 0.35 | POOR |
| ENV2 (mean spread)        | 2.38 | MARGINAL |
| ENV3 (mean spread)        | 6.44 | MARGINAL |
| ENV4 (mean spread)        | 6.57 | MARGINAL |
| ENV5 (mean spread)        | 4.92 | MARGINAL |

## 10. Key Findings

1. **Input signals DO differ**: The stimulus Vpp varies by test case
   (inner race > outer race > ball > normal)

2. **PGA preserves differentiation**: After PGA, the signal std still differs

3. **BPF channels show SOME differentiation**: The AC amplitude (std) differs
   across test cases, especially in channels 2-4

4. **Envelope detector COMPRESSES differentiation**: The DC envelope values
   are within ~7 mV of each other. The BPF amplitude differences (~10-50 mV)
   are reduced to ~1-7 mV DC offsets by the half-wave rectification + LPF.

5. **The classifier cannot distinguish 1-7 mV differences** because it divides
   by 1.8V, making the features all ~0.5 (normalized).

**The information EXISTS at the BPF outputs but is LOST in the envelope-to-classifier**
**mapping. The fix is either amplification after envelope or classifier retraining.**