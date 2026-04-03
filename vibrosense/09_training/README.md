# Block 09 — Training Pipeline

## What This Does

This block is the bridge between software and silicon. It takes real vibration
data, trains a classifier in Python, and outputs **32 capacitor values** that
get programmed into the analog MAC array (Block 06). Without this, the chip's
capacitors would have arbitrary values and classify nothing.

The pipeline:
1. Downloads real bearing vibration recordings (CWRU dataset)
2. Splits each recording into frequency bands — matching exactly what the
   analog filters (Block 03) do in hardware
3. Measures the energy in each band — matching what the envelope detectors
   (Block 04) and RMS converter (Block 05) do in hardware
4. Trains a linear classifier to distinguish 4 conditions:
   Normal, Inner Race fault, Ball fault, Outer Race fault
5. Quantizes the learned weights from float32 down to 4-bit (16 levels) —
   because that's the resolution you can reliably match with MIM capacitors
   at 130nm
6. Exports the weights as physical capacitor values in SPICE format

## How Detection Works

A bearing fault changes the vibration spectrum. Each fault type excites
a different frequency range:

```
Normal:      quiet across all bands
Inner Race:  loud in BPF3 (1500-3000 Hz) — defect on inner ring
Ball:        loud in BPF4 (3000-4500 Hz) — defect on rolling element
Outer Race:  loud in BPF5 (4500-5900 Hz) — defect on outer ring
```

The chip has 5 analog band-pass filters that separate these frequencies,
followed by envelope detectors that convert each band's AC signal into a
steady DC voltage proportional to the energy in that band. Three more
features (broadband RMS, crest factor, kurtosis) capture overall signal
characteristics. That gives 8 DC voltages sitting on 8 wires.

Four "neurons" — one per class — each multiply those 8 voltages by 8
capacitors and sum the result. The neuron with the highest sum wins.
A big capacitor on a loud band produces a large product. Training decides
which caps should be big and which should be small.

The result for CWRU bearing data:

```
              BPF1   BPF2   BPF3   BPF4   BPF5    RMS  Crest   Kurt
Normal:       90fF   70fF   40fF   20fF   10fF   40fF   40fF   60fF
Inner Race:   30fF   80fF  130fF   60fF   70fF   50fF   80fF   90fF
Ball:         60fF   50fF   90fF  110fF   20fF   50fF   80fF   40fF
Outer Race:   80fF   50fF    0fF   70fF  150fF  110fF   60fF   60fF
```

Inner Race has the biggest cap (130fF) on BPF3. Outer Race has the max
(150fF) on BPF5 and zero on BPF3. These values directly encode the physics
of which fault excites which frequency band.

## Results — CWRU Bearing Dataset

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Float accuracy | 99.33% | >= 88% | PASS |
| 4-bit quantized accuracy | 98.00% | >= 85% | PASS |
| Quantization loss | 1.3 pp | < 5 pp | PASS |
| Accuracy with 2% analog noise | 95.85% | >= 82% | PASS |
| 10-fold CV quantized accuracy | 97.3% ± 3.3% | — | Stable |

## Robustness Analysis

We tested whether the cap values are stable or just an artifact of one
lucky train/test split:

- **20 random splits**: Mean cap variation = 0.22 levels out of 16.
  Zero caps vary more than 2 levels. The values are rock solid.
- **Leave-one-motor-load-out**: Accuracy stays 92-99% across all 4 loads
  (0, 1, 2, 3 HP). Cap values barely change.
- **10-fold cross-validation**: 97.3% ± 3.3% quantized accuracy.
  Worst fold still 89%.

### Known Limitation

**Leave-one-fault-size-out fails.** Train on 0.014" and 0.021" faults,
test on 0.007" — accuracy drops to 66%. Train on two sizes, test on the
third — as low as 6%. The model learns absolute vibration amplitudes
rather than relative frequency patterns.

This is a property of the CWRU dataset and the absolute-energy features,
not of the capacitor network itself. For real deployment:
- The PGA (Block 02) should auto-normalize amplitude
- Band ratios (BPF3/BPF1) would be more robust than absolute energies
- Field calibration with known-good and known-bad examples is required

The cap values are reliable for the conditions trained on. They should not
be treated as universal constants — they are a starting point that may
need site-specific tuning via SPI.

## Multi-Use-Case Support

The same 32-capacitor MAC array handles different vibration classification
problems. The pipeline is config-driven — swap the JSON config file and
you get different cap values and filter band settings for a different
application.

Four configs are included:

| Config | Application | Filter Bands |
|--------|------------|--------------|
| `bearing_cwru.json` | Bearing fault detection | 100-5900 Hz, 5 bands |
| `gearbox.json` | Gearbox tooth/shaft faults | 20-5900 Hz, 5 bands |
| `motor_stator.json` | Motor stator/rotor faults | 25-5900 Hz, 5 bands |
| `pump_cavitation.json` | Pump cavitation detection | 10-5900 Hz, 5 bands |

Each config defines different filter band edges (matching different
fault physics), different PGA gain, and different accuracy targets.

To switch applications, the MCU sends 4 SPI writes (~10 µs) with the
new weight register values. The Block 03 filter bands are tuned by
adjusting Gm-C bias currents. Same chip, different "brain."

## How SPI Weight Loading Works

The cap values are not fixed in silicon. They are set by digital switches
controlled via SPI from the register file (Block 08):

1. MCU sends 4 x 16-bit SPI transactions to WEIGHT0-3 registers
2. Each register packs two 4-bit weight indices per byte
3. The digital weight bits directly control transmission gates on binary-
   weighted MIM capacitors (50fF, 100fF, 200fF, 400fF per bit)
4. If a weight bit = 1, that cap's sample switch opens and it charges
   to the input voltage. If 0, the switch stays closed and the cap
   contributes nothing.

No DAC, no analog memory — pure digital switch control of physical caps.

## File Structure

```
09_training/
├── train.py                  # Main pipeline: load → train → quantize → export
├── download_cwru.py          # Downloads 40 CWRU .mat files (134 MB)
├── visualize_detection.py    # Generates explanation plots
├── robustness_test.py        # Cap stability analysis (20 splits, CV, LOLO)
├── configs/
│   ├── bearing_cwru.json     # Primary: CWRU bearing fault detection
│   ├── gearbox.json          # Gearbox tooth/shaft faults
│   ├── motor_stator.json     # Motor stator/rotor faults
│   └── pump_cavitation.json  # Pump cavitation monitoring
├── data/                     # CWRU .mat files (gitignored, 134 MB)
├── results/
│   ├── trained_weights.json  # Float + quantized weights, biases, normalization
│   ├── weights_spice.txt     # .param cap values for Block 06
│   ├── feature_vectors_spice.txt  # PWL test vectors for Block 10
│   ├── classification_report.txt  # Per-class precision/recall + PASS/FAIL
│   ├── confusion_matrix.png       # Float vs quantized vs noisy
│   ├── weight_histogram.png       # Float and quantized weight distributions
│   ├── noise_sensitivity.png      # Accuracy vs analog noise level
│   ├── feature_importance.png     # Which features matter per class
│   ├── capacitor_map.png          # 4x8 heatmap of cap values in fF
│   ├── how_detection_works.png    # End-to-end signal flow visualization
│   ├── band_signatures.png        # What each filter band sees per fault
│   ├── capacitor_scoring.png      # Feature x weight products per neuron
│   ├── robustness_analysis.png    # Cap stability across splits/loads/folds
│   ├── gearbox/                   # Results for gearbox config (synthetic)
│   ├── motor_stator/              # Results for motor stator config (synthetic)
│   └── pump_cavitation/           # Results for pump config (synthetic)
├── program.md                # Detailed specification (from design phase)
├── requirements.md           # Requirements traceability
├── specs.json                # Pass/fail measurement targets
└── design.cir                # Placeholder (this block is pure software)
```

## How to Run

```bash
# First time: download CWRU data
python3 download_cwru.py

# Train on CWRU bearing data (default)
python3 train.py

# Train for a different application
python3 train.py --config configs/gearbox.json --output-dir results/gearbox --synthetic

# Run robustness analysis
python3 robustness_test.py

# Generate visualization plots
python3 visualize_detection.py
```

Runtime: ~30 seconds for feature extraction + training. The dataset is small
(134 MB, 1000 windows) and the model is trivial (36 parameters).

## Dependencies

- Python 3.10+
- numpy, scipy, scikit-learn, matplotlib
- scipy.io for loading MATLAB .mat files

## Outputs Consumed by Other Blocks

| File | Consumer | Purpose |
|------|----------|---------|
| `weights_spice.txt` | Block 06 (classifier) | .param cap values for SPICE simulation |
| `feature_vectors_spice.txt` | Block 10 (fullchain) | PWL stimulus for end-to-end test |
| `trained_weights.json` | Block 08 (digital) | SPI register hex values for weight loading |
| `classification_report.txt` | Top-level README | Accuracy numbers for chip specifications |

## Key Design Decision: Quantization-Aware Tuning

The first training run picked regularization C=100 (weak regularization)
because it maximized float accuracy at 100%. But the weights blew up to
range [-29, +41], and cramming that into 16 levels caused 14 percentage
points of accuracy loss — failing the <5pp target.

The fix: tune C to maximize *quantized* accuracy, not float accuracy.
This picked C=10, keeping weights in [-13.5, +18.2] — a tighter range
that quantizes with only 1.3pp loss. Slightly lower float accuracy (99.3%
vs 100%), dramatically better quantized accuracy (98% vs 86%).

This is the right tradeoff for analog hardware. A model that's perfect in
float but breaks when quantized is useless. A model that's slightly less
perfect but survives quantization and noise is what goes into silicon.
