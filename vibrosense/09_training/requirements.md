# Block 09 — Training Pipeline: Requirements

## Software Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Python 3 | >= 3.10 | Runtime |
| numpy | >= 1.24 | Numerical computation |
| scipy | >= 1.11 | Signal processing (Butterworth filters, .mat file loading) |
| scikit-learn | >= 1.3 | LogisticRegression, metrics, preprocessing |
| matplotlib | >= 3.7 | Confusion matrix, weight histograms, plots |
| pandas | >= 2.0 | Data organization and export |

## Analog / SPICE Dependencies

**None.** This is a pure software block. No SPICE simulator, no PDK, no
analog models are needed. The training pipeline runs entirely in Python.

## Data Dependency

| Dataset | Source | Required |
|---------|--------|----------|
| CWRU Bearing Dataset | https://engineering.case.edu/bearingdatacenter | YES |

The CWRU (Case Western Reserve University) Bearing Data Center dataset must
be downloaded before running the pipeline. Required files:

- 12 kHz drive-end accelerometer data
- All fault sizes (0.007", 0.014", 0.021")
- Normal baseline recordings
- Inner race fault recordings
- Outer race fault recordings (centered, orthogonal, opposite)
- Ball fault recordings

Files are in MATLAB .mat format. scipy.io.loadmat handles these directly.

## Installation

```bash
pip install numpy>=1.24 scipy>=1.11 scikit-learn>=1.3 matplotlib>=3.7 pandas>=2.0
```

## File Structure (expected output)

```
09_training/
  requirements.md              # this file
  program.md                   # pipeline specification
  train.py                     # main training script
  feature_extraction.py        # analog-matched feature extraction
  quantize.py                  # weight quantization utilities
  export_spice.py              # export weights/vectors for SPICE simulation
  data/                        # CWRU dataset .mat files (not committed)
  results/
    trained_weights.json       # full-precision + quantized weights
    weights_spice.txt          # SPICE .param file for Block 06
    feature_vectors_spice.txt  # SPICE PWL stimuli for Block 10
    confusion_matrix.png       # confusion matrix visualization
    classification_report.txt  # per-class precision/recall/F1
    weight_histogram.png       # weight distribution visualization
    noise_analysis.txt         # accuracy vs analog noise level
```
