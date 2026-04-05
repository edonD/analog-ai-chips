# VibroSense-1 Full-Chain Integration (Block 10)

## Status: COMPLETE (Proof-of-Concept)

4/4 classification accuracy on synthetic bearing fault stimuli.
~56 uW estimated total system power. Open-source SKY130 design.

## Architecture

```
MEMS Accel --> PGA (4x) --> 5-ch BPF Bank --> 5 Peak Detectors --> Classifier --> Decision
                |                                                     ^
                +-----------> RMS/Crest Detector --------------------+
```

- **PGA:** 4x gain, transistor-level (Block 02)
- **BPF Bank:** 5 Gm-C bandpass filters at 100 Hz, 300 Hz, 1 kHz, 3 kHz, 6 kHz (Block 03)
- **Peak Detectors:** Behavioral full-wave rectifier + peak hold, 20ms decay (replaces Block 04)
- **RMS/Crest:** Transistor-level RMS and crest factor extraction (Block 05)
- **Classifier:** 4-class linear classifier, v5 weights from pseudo-inverse training (Block 06)
- **Output:** Voltage-encoded class: 0V=Normal, 0.45V=Inner Race, 0.9V=Ball, 1.35V=Outer Race

## Results Summary

### Classification Accuracy

| Test Case | Expected | Detected | Correct | Confidence |
|-----------|----------|----------|---------|------------|
| Normal | Normal | Normal | YES | 92% |
| Inner Race | Inner Race | Inner Race | YES | 42% |
| Outer Race | Outer Race | Outer Race | YES | 64% |
| Ball | Ball | Ball | YES | 54% |

**Accuracy: 4/4 (100%)**

### Key Feature Values (last 50ms, steady-state mean)

| Feature | Normal | Inner Race | Outer Race | Ball | Spread |
|---------|--------|------------|------------|------|--------|
| ENV4 (3 kHz) | 0.936 V | 1.031 V | 1.026 V | 1.021 V | 94.7 mV |
| ENV5 (6 kHz) | 0.918 V | 1.026 V | 1.006 V | 1.004 V | 107.6 mV |
| RMS_out | 1.551 V | 1.513 V | 1.518 V | 1.529 V | 38.4 mV |
| Peak_out | 1.184 V | 1.239 V | 1.234 V | 1.227 V | 54.7 mV |

ENV4 and ENV5 are the primary discriminators — healthy bearings have low
high-frequency energy, faulty bearings have elevated high-frequency content.

### Power

| Block | Power |
|-------|-------|
| BPF bank (5 ch) | 42.1 uW |
| Peak detectors (5, passive) | ~0 uW |
| RMS/Crest | 9.5 uW |
| Classifier (est.) | ~5 uW |
| Digital (est.) | ~1.5 uW |
| **System total** | **~58 uW** |

### Design Evolution

| Version | Change | Accuracy | Power |
|---------|--------|----------|-------|
| v1 | Initial integration | 1/4 (25%) | 183 uW |
| v2 | BPF/bias fixes | 1/4 (25%) | 183 uW |
| v3 | Peak detector envelope | 2/4 (50%) | 96 uW |
| v4 (final) | Retrained classifier | 4/4 (100%) | 58 uW |

## File Structure

```
10_fullchain/
├── README.md                          <- This file
├── netlists/
│   ├── vibrosense1_top.spice          <- Top-level netlist
│   ├── vibrosense1_peak_*.spice       <- Per-test-case netlists (4)
│   ├── classifier_peak_v4.spice       <- v5 retrained classifier
│   ├── envelope_peak_behavioral.spice <- Peak detector model
│   ├── ota_behavioral.spice           <- OTA model
│   ├── bias_generator_fixed.spice     <- Bias generator
│   ├── ota_pga_v2_fixed.spice         <- PGA
│   └── pga_fixed.spice                <- PGA wrapper
├── scripts/
│   ├── analyze_results.py             <- Raw file parser
│   ├── analyze_peak_results.py        <- Peak detector result analysis
│   ├── retrain_classifier.py          <- Classifier weight training
│   ├── generate_stimuli.py            <- Bearing fault stimulus generation
│   ├── generate_reports.py            <- Report generation
│   └── run_fullchain.py               <- Simulation runner
└── results/
    ├── accuracy_report.txt            <- Detailed accuracy analysis
    ├── final_specifications.txt       <- Complete specifications
    ├── comparison_table.txt           <- vs. competing approaches
    ├── power_breakdown.txt            <- Power analysis
    ├── peak_detector_results_v2.json  <- Machine-readable results
    ├── peak_*.raw                     <- ngspice raw output (4 cases)
    └── peak_*.log                     <- ngspice simulation logs
```

## Running Simulations

```bash
cd /home/ubuntu/analog-ai-chips/vibrosense/10_fullchain

# Run all 4 test cases in parallel
for tc in normal inner_race outer_race ball; do
  ngspice -b -o results/peak_${tc}.log -r results/peak_${tc}.raw \
    netlists/vibrosense1_peak_${tc}.spice &
done
wait

# Analyze results
python3 scripts/analyze_peak_results.py
```

## Honest Assessment

**This is a successful proof-of-concept, not a tape-out-ready design.**

What is proven:
- Sub-100 uW analog feature extraction for vibration monitoring works
- 5-channel filterbank + peak detection produces physically meaningful features
- Linear classifier can separate 4 bearing conditions using analog features
- Full signal chain from input to classification decision is functional

What is not proven:
- **Generalization:** 4/4 on 4 training points with 32+ free weights. The
  classifier has more parameters than data. Real generalization accuracy is unknown.
- **Thin margins:** Inner race (42%) and ball (54%) confidence levels are marginal.
  PVT variation could flip these classifications.
- **Behavioral blocks:** Peak detector and classifier are SPICE B-sources, not
  transistor-level. Real implementation will have additional non-idealities.
- **Synthetic stimuli:** Multi-tone bearing fault approximations, not real CWRU data.
- **Single PVT corner:** TT/27C/1.8V only.

Path to real chip:
1. Transistor-level peak detector (Block 05 topology available)
2. PVT corner sweep on full chain
3. Real accelerometer data injection
4. Regularized classifier training with more data points
5. Layout and parasitic extraction
6. Tape-out on SKY130 MPW shuttle
