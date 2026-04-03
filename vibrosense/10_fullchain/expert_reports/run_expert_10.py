#!/usr/bin/env python3
"""Expert 10: Stimulus Expert — CWRU data and stimulus generation"""
import os, glob

BASE = "/home/ubuntu/analog-ai-chips/vibrosense"
OUT = f"{BASE}/10_fullchain/expert_reports/expert_10_stimulus.md"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return f"[FILE NOT FOUND: {path}]"

# Check for CWRU data in various locations
data_dirs = [
    f"{BASE}/09_training/data",
    f"{BASE}/09_training/cwru_data",
    f"{BASE}/data",
    "/home/ubuntu/cwru_data",
    f"{BASE}/10_fullchain/data",
]
found_data = None
for d in data_dirs:
    if os.path.isdir(d):
        found_data = d
        break

# Check what data files exist
mat_files = []
if found_data:
    mat_files = sorted(glob.glob(f"{found_data}/*.mat"))

# Check download script
download_script = read_file(f"{BASE}/09_training/download_cwru.py")

# Check existing stimuli
existing_stimuli = sorted(glob.glob(f"{BASE}/10_fullchain/stimuli/*.pwl"))

# Check feature vectors (can be used as alternative stimulus)
feature_vectors = os.path.exists(f"{BASE}/09_training/results/feature_vectors_spice.txt")

# Check for scipy (needed for .mat files)
try:
    import scipy
    scipy_available = True
except:
    scipy_available = False

try:
    import numpy
    numpy_available = True
except:
    numpy_available = False

report = f"""# Expert 10: Stimulus and CWRU Data Analysis

## CWRU Data Status
- Data directory found: {found_data if found_data else 'NOT FOUND anywhere'}
- .mat files found: {len(mat_files)}
{chr(10).join(['  - ' + os.path.basename(f) for f in mat_files[:20]]) if mat_files else '  None'}

## Required CWRU Files (per program.md)
| Test Case | CWRU File | Status |
|-----------|-----------|--------|
| Normal | 97.mat (normal, 0hp) | {'CHECK' if mat_files else 'NEED DOWNLOAD'} |
| Inner Race | 105.mat (IR007, 0hp) | {'CHECK' if mat_files else 'NEED DOWNLOAD'} |
| Ball | 118.mat (B007, 0hp) | {'CHECK' if mat_files else 'NEED DOWNLOAD'} |
| Outer Race | 130.mat (OR007, 0hp) | {'CHECK' if mat_files else 'NEED DOWNLOAD'} |

## Download Script
- `download_cwru.py`: {'EXISTS' if '[FILE NOT FOUND' not in download_script else 'MISSING'}

## Python Dependencies
- numpy: {'AVAILABLE' if numpy_available else 'NOT INSTALLED'}
- scipy: {'AVAILABLE' if scipy_available else 'NOT INSTALLED — needed for .mat files'}

## Existing Stimuli
{chr(10).join(['- ' + os.path.basename(f) for f in existing_stimuli]) if existing_stimuli else 'No stimuli generated yet'}

## Feature Vector Test Stimulus
- feature_vectors_spice.txt: {'EXISTS' if feature_vectors else 'MISSING'}
- Can be used for quick classifier validation without full analog chain

## Stimulus Generation Strategy

### Option A: Full CWRU Data (preferred)
1. Download CWRU .mat files
2. Convert to PWL using generate_stimuli.py (per program.md)
3. Parameters: 12kHz sample rate, 0.1 V/g scale, 0.9V offset, 2s duration
4. Each PWL file: ~24,000 time-voltage pairs

### Option B: Synthetic Stimulus (fallback)
If CWRU data unavailable:
1. Generate synthetic bearing vibration signals
2. Normal: low-amplitude broadband noise
3. Inner race: periodic impulses at BPFI frequency (~5.42x shaft speed)
4. Outer race: periodic impulses at BPFO frequency (~3.58x shaft speed)
5. Ball: periodic impulses at BSF frequency (~2.36x shaft speed)
6. For a typical motor at 1797 RPM (29.95 Hz):
   - BPFI = 162.2 Hz, BPFO = 107.4 Hz, BSF = 70.7 Hz

### Option C: Feature-Level Test (quickest)
Use feature_vectors_spice.txt to test classifier only:
1. Bypass PGA, filters, envelope, RMS/crest
2. Drive classifier directly with pre-computed feature voltages
3. Validates classifier + digital + weight loading
4. Does NOT validate analog signal chain

## Recommendation
1. **Start with Option C** — validate classifier works with known vectors
2. **Then Option B** — generate synthetic stimuli for full-chain test
3. **Then Option A** — download CWRU data for final accuracy measurement

### Synthetic Stimulus Generator (ready to implement)
```python
import numpy as np

def generate_bearing_signal(fault_type, duration=0.2, fs=12000,
                            shaft_rpm=1797, amplitude=1.0):
    t = np.arange(0, duration, 1/fs)
    f_shaft = shaft_rpm / 60  # ~29.95 Hz

    # Base vibration (broadband noise)
    signal = 0.1 * np.random.randn(len(t))

    if fault_type == 'normal':
        pass  # just noise
    elif fault_type == 'inner_race':
        f_fault = 5.42 * f_shaft  # BPFI
        impulses = np.zeros(len(t))
        period = int(fs / f_fault)
        impulses[::period] = amplitude
        # Convolve with decaying sinusoid
        decay = np.exp(-np.arange(100)/10) * np.sin(2*np.pi*3000*np.arange(100)/fs)
        signal += np.convolve(impulses, decay, mode='same')
    elif fault_type == 'outer_race':
        f_fault = 3.58 * f_shaft  # BPFO
        impulses = np.zeros(len(t))
        period = int(fs / f_fault)
        impulses[::period] = amplitude
        decay = np.exp(-np.arange(100)/10) * np.sin(2*np.pi*2500*np.arange(100)/fs)
        signal += np.convolve(impulses, decay, mode='same')
    elif fault_type == 'ball':
        f_fault = 2.36 * f_shaft  # BSF
        impulses = np.zeros(len(t))
        period = int(fs / f_fault)
        impulses[::period] = amplitude * 0.7
        decay = np.exp(-np.arange(100)/10) * np.sin(2*np.pi*3500*np.arange(100)/fs)
        signal += np.convolve(impulses, decay, mode='same')

    # Scale to voltage
    voltage = signal * 0.1 + 0.9  # 0.1 V/g, 0.9V offset
    voltage = np.clip(voltage, 0.0, 1.8)
    return t, voltage
```
"""

with open(OUT, 'w') as f:
    f.write(report)
print(f"Expert 10 report written to {OUT}")
