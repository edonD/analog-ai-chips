#!/usr/bin/env python3
"""TB4: CRITICAL — Tuning Range Verification across PVT.

For each channel, for each of 15 PVT conditions, sweep DAC codes 1-15
and verify that some code brings f0 to within ±10% of nominal.

Since behavioral OTA is linear (gm directly set), PVT is modeled by
scaling gm by a factor. The filter f0 scales linearly with gm (for
symmetric Tow-Thomas with C1=C2): f0 = gm/(2πC).

So f0_actual = f0_nominal × pvt_factor × dac_code/8
We need: |f0_actual/f0_nominal - 1| < 10%
  → |pvt_factor × dac_code/8 - 1| < 0.10
  → dac_code ≈ 8 / pvt_factor (within ±10%)
"""

import numpy as np
import subprocess
import json
import os
import tempfile

channels = {
    1: {'f0': 224,   'gm_nom': 14.07e-9,  'gm3_nom': 18.76e-9},
    2: {'f0': 1000,  'gm_nom': 62.83e-9,  'gm3_nom': 93.78e-9},
    3: {'f0': 3162,  'gm_nom': 198.7e-9,  'gm3_nom': 189.2e-9},
    4: {'f0': 7071,  'gm_nom': 444.3e-9,  'gm3_nom': 315.1e-9},
    5: {'f0': 14142, 'gm_nom': 888.6e-9,  'gm3_nom': 630.2e-9},
}

# PVT gm scale factors (realistic for SKY130 subthreshold)
# gm = Ibias/(n*Vt), Vt = kT/q
# Process: FF +25%, SS -25%, FS -10%, SF +10% (NMOS-dominated OTA)
# Temperature: Vt scales with T → gm inversely proportional to T
pvt_conditions = {
    'TT_n40': 1.0 * (300.15 / 233.15),   # 1.287
    'TT_27':  1.0,                          # 1.000
    'TT_85':  1.0 * (300.15 / 358.15),     # 0.838
    'FF_n40': 1.25 * (300.15 / 233.15),    # 1.609
    'FF_27':  1.25,                          # 1.250
    'FF_85':  1.25 * (300.15 / 358.15),     # 1.048
    'SS_n40': 0.75 * (300.15 / 233.15),    # 0.965
    'SS_27':  0.75,                          # 0.750
    'SS_85':  0.75 * (300.15 / 358.15),     # 0.629
    'FS_n40': 0.90 * (300.15 / 233.15),    # 1.158
    'FS_27':  0.90,                          # 0.900
    'FS_85':  0.90 * (300.15 / 358.15),     # 0.754
    'SF_n40': 1.10 * (300.15 / 233.15),    # 1.416
    'SF_27':  1.10,                          # 1.100
    'SF_85':  1.10 * (300.15 / 358.15),     # 0.922
}

def measure_f0_analytical(ch_num, pvt_factor, dac_code):
    """Analytical f0 for behavioral model.

    For linear behavioral OTA, f0 = gm/(2*pi*C) scales exactly with gm.
    gm_effective = gm_nominal * pvt_factor * dac_code/8
    f0_effective = f0_nominal * pvt_factor * dac_code/8
    """
    spec = channels[ch_num]
    scale = pvt_factor * dac_code / 8.0
    return spec['f0'] * scale

def run_ngspice_verification(ch_num, pvt_factor, dac_code):
    """Run actual ngspice sim to verify one point."""
    spec = channels[ch_num]
    gm_scale = pvt_factor * dac_code / 8.0

    spice_content = f"""* TB4 verification: Ch{ch_num} PVT={pvt_factor:.3f} DAC={dac_code}
.include bpf_ch{ch_num}.spice

Vdd vdd 0 1.8
Vss vss 0 0
Vcm vcm 0 0.9
Vin in 0 DC 0.9 AC 1

Xbpf in bp_out vdd vss vcm bpf_ch{ch_num} gm_scale={gm_scale}

.control
ac dec 300 1 200k
wrdata tb4_verify.txt v(bp_out)
.endc
.end
"""
    with open('tb4_temp.spice', 'w') as f:
        f.write(spice_content)

    result = subprocess.run(['ngspice', '-b', 'tb4_temp.spice'],
                          capture_output=True, text=True, timeout=30)

    data = np.loadtxt('tb4_verify.txt')
    freq = data[:, 0]
    re = data[:, 1]
    im = data[:, 2]
    mag = np.sqrt(re**2 + im**2)
    mag_db = 20 * np.log10(mag + 1e-30)
    peak_idx = np.argmax(mag_db)
    return freq[peak_idx]


# ======================== MAIN ANALYSIS ========================
print("=" * 90)
print("TB4: CRITICAL — 4-Bit Tuning DAC PVT Compensation Verification")
print("=" * 90)
print(f"\nPVT Conditions: {len(pvt_conditions)}")
print(f"DAC Codes: 1-15 (nominal=8)")
print(f"Channels: 5")
print(f"Total sweep points: {len(pvt_conditions) * 15 * 5}")

all_results = {}
overall_pass = True

# For each channel
for ch in range(1, 6):
    spec = channels[ch]
    f0_nom = spec['f0']
    ch_results = {}
    ch_pass = True
    worst_corner = None
    worst_residual = 0

    print(f"\n{'─'*90}")
    print(f"Channel {ch}: f0_nominal = {f0_nom} Hz")
    print(f"{'─'*90}")
    print(f"{'Corner':<12} {'PVT Factor':>10} {'f0@code8':>10} {'Shift%':>8} "
          f"{'BestCode':>8} {'f0_tuned':>10} {'Residual%':>10} {'PASS':>6}")

    for pvt_name, pvt_factor in sorted(pvt_conditions.items()):
        # f0 at nominal code (code=8)
        f0_nominal_code = measure_f0_analytical(ch, pvt_factor, 8)
        shift_pct = (f0_nominal_code - f0_nom) / f0_nom * 100

        # Sweep all DAC codes to find best
        best_code = 8
        best_f0 = f0_nominal_code
        best_error = abs(shift_pct)

        for code in range(1, 16):
            f0_test = measure_f0_analytical(ch, pvt_factor, code)
            error = abs((f0_test - f0_nom) / f0_nom * 100)
            if error < best_error:
                best_error = error
                best_code = code
                best_f0 = f0_test

        residual_pct = (best_f0 - f0_nom) / f0_nom * 100
        passes = abs(residual_pct) < 10.0

        if not passes:
            ch_pass = False
            overall_pass = False

        if abs(residual_pct) > abs(worst_residual):
            worst_residual = residual_pct
            worst_corner = pvt_name

        ch_results[pvt_name] = {
            'pvt_factor': round(pvt_factor, 4),
            'f0_untuned': round(f0_nominal_code, 1),
            'shift_pct': round(shift_pct, 1),
            'best_code': best_code,
            'f0_tuned': round(best_f0, 1),
            'residual_pct': round(residual_pct, 2),
            'pass': passes,
        }

        print(f"{pvt_name:<12} {pvt_factor:>10.4f} {f0_nominal_code:>10.1f} "
              f"{shift_pct:>+7.1f}% {best_code:>8d} {best_f0:>10.1f} "
              f"{residual_pct:>+9.2f}% {'PASS' if passes else 'FAIL':>6}")

    status = "PASS" if ch_pass else "FAIL"
    print(f"  Channel {ch} Result: {status} | Worst corner: {worst_corner} ({worst_residual:+.2f}%)")

    all_results[ch] = {
        'pvt_data': ch_results,
        'worst_corner': worst_corner,
        'worst_residual_pct': round(worst_residual, 2),
        'pass': ch_pass,
    }

# Verify a few critical points with actual ngspice sims
print(f"\n{'='*90}")
print("Ngspice Verification of Critical Points")
print(f"{'='*90}")

verify_points = [
    (2, 'SS_85', 0.629),   # Worst case low
    (2, 'FF_n40', 1.609),  # Worst case high
    (5, 'SS_85', 0.629),   # Highest freq + worst corner
]

for ch, pvt_name, pvt_factor in verify_points:
    spec = channels[ch]
    # Find best code analytically
    best_code = 8
    best_err = 100
    for code in range(1, 16):
        f0_est = spec['f0'] * pvt_factor * code / 8
        err = abs(f0_est / spec['f0'] - 1) * 100
        if err < best_err:
            best_err = err
            best_code = code

    # Run ngspice
    f0_sim = run_ngspice_verification(ch, pvt_factor, best_code)
    f0_analytical = spec['f0'] * pvt_factor * best_code / 8
    sim_err = (f0_sim - spec['f0']) / spec['f0'] * 100

    print(f"  Ch{ch} {pvt_name} code={best_code}: "
          f"analytical={f0_analytical:.1f}Hz, ngspice={f0_sim:.1f}Hz, "
          f"residual={sim_err:+.2f}%")

print(f"\n{'='*90}")
print(f"TB4 OVERALL: {'ALL PASS — DAC covers all PVT corners' if overall_pass else 'FAIL'}")
print(f"{'='*90}")

# Summary table
print(f"\n{'='*90}")
print("Tuning Summary per Channel")
print(f"{'='*90}")
print(f"{'Ch':<4} {'f0_nom':>8} {'Worst Corner':<12} {'Untuned Shift':>14} "
      f"{'Best Code':>10} {'Residual':>10} {'PASS':>6}")
for ch in range(1, 6):
    r = all_results[ch]
    wc = r['worst_corner']
    wd = r['pvt_data'][wc]
    print(f"{ch:<4} {channels[ch]['f0']:>8} {wc:<12} {wd['shift_pct']:>+13.1f}% "
          f"{wd['best_code']:>10} {wd['residual_pct']:>+9.2f}% "
          f"{'PASS' if r['pass'] else 'FAIL':>6}")

with open('tb4_results.json', 'w') as f:
    json.dump(all_results, f, indent=2, default=str)
