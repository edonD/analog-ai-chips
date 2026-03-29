#!/usr/bin/env python3
"""
run_monte_carlo.py — Monte Carlo mismatch analysis for Block 07: Zener Clamp

IMPORTANT LIMITATION: The open-source SKY130 PDK does not publish mismatch
coefficients (Avt, Atox) for the nfet_g5v0d10v5 device. The vth0_slope and
toxe_slope1 parameters are set to 0 in all corners.

This script uses ESTIMATED mismatch coefficients based on literature values
for similar 130nm thick-oxide HV NFET devices:
  - Avt (vth0_slope) = 12 mV*um  (typical range: 8-15 for 130nm HV)
  - toxe_slope1 = 5e-9           (tox mismatch, scaled for SPICE units)

The MC results are ESTIMATES and should be validated against silicon data.

Methodology: We run N independent DC IV sims, each with mc_mm_switch=1
and the estimated slope values. ngspice's AGAUSS provides the random
variation per instance.

UNITS: In the BSIM4 model, vth0 = nom + MC_MM_SWITCH*AGAUSS(0,1,1)*vth0_slope/sqrt(L*W)
where L,W are in METERS. So vth0_slope must be in V*m (not mV*um).
  Avt = 12 mV*um = 12e-3 V * 1e-6 m = 12e-9 V*m
  For W=1.5u L=4u: sigma_vth = 12e-9/sqrt(6e-12) = 4.9 mV per device.
"""
import subprocess, re, os, sys, random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

N_RUNS = 50  # Monte Carlo iterations
AVT = 12e-9  # 12 mV*um = 12e-9 V*m (SPICE units, L and W in meters)
TOXE_SLOPE1 = 5e-9  # tox mismatch coefficient (scaled for meters)

TB_TEMPLATE = """\
* tb_mc_{run_id}.spice — Monte Carlo run {run_id}/{n_total}
.lib "../sky130.lib.spice" tt

* Override mismatch parameters to enable MC
.param mc_mm_switch = 1
.param sky130_fd_pr__nfet_g5v0d10v5__vth0_slope = {avt}
.param sky130_fd_pr__nfet_g5v0d10v5__toxe_slope1 = {toxe_slope1}

.include "design.cir"

Vpvdd pvdd 0 DC 0
Xclamp pvdd 0 zener_clamp

.option reltol=1e-4 seed={seed}

.control
dc Vpvdd 0 8 0.005
let i_clamp = -i(Vpvdd)

* --- Leakage at 5.0V ---
let idx = 0
let leak_5v = 0
dowhile idx < length(i_clamp)
  if v(pvdd)[idx] >= 4.998 & v(pvdd)[idx] <= 5.002
    let leak_5v = i_clamp[idx]
    let idx = length(i_clamp)
  end
  let idx = idx + 1
end
let leak_5v_nA = leak_5v * 1e9

* --- Onset at 1mA ---
let idx = 0
let v_1ma = 0
dowhile idx < length(i_clamp)
  if i_clamp[idx] >= 1m
    let v_1ma = v(pvdd)[idx]
    let idx = length(i_clamp)
  end
  let idx = idx + 1
end

echo "mc_onset_1mA_V: $&v_1ma"
echo "mc_leakage_nA: $&leak_5v_nA"

quit
.endc
.end
"""

print("=" * 72)
print(f"Monte Carlo Analysis: {N_RUNS} runs at TT 27C")
print(f"  Estimated Avt = {AVT*1e3*1e6:.1f} mV*um  (vth0_slope = {AVT:.1e} V*m)")
print(f"  Estimated toxe_slope1 = {TOXE_SLOPE1}")
print(f"  NOTE: Open-source SKY130 PDK does not publish mismatch coefficients.")
print(f"        These are estimates based on literature for similar 130nm HV devices.")
print("=" * 72)

onsets = []
leakages = []

for i in range(N_RUNS):
    seed = random.randint(1, 999999)
    tb_name = f"tb_mc_{i:03d}.spice"
    tb_content = TB_TEMPLATE.format(
        run_id=i+1, n_total=N_RUNS,
        avt=AVT, toxe_slope1=TOXE_SLOPE1,
        seed=seed
    )
    with open(tb_name, "w") as f:
        f.write(tb_content)

    proc = subprocess.run(
        ["ngspice", "-b", tb_name],
        capture_output=True, text=True, timeout=120
    )
    output = proc.stdout + proc.stderr

    onset = None
    leakage = None
    for line in output.split("\n"):
        m = re.search(r"mc_onset_1mA_V:\s+([\d.e+-]+)", line)
        if m:
            onset = float(m.group(1))
        m = re.search(r"mc_leakage_nA:\s+([\d.e+-]+)", line)
        if m:
            leakage = float(m.group(1))

    if onset is not None:
        onsets.append(onset)
    if leakage is not None:
        leakages.append(leakage)

    os.remove(tb_name)

    if (i + 1) % 10 == 0:
        print(f"  Completed {i+1}/{N_RUNS}...")

# Statistics
import statistics

print()
print("=" * 72)
print("Monte Carlo Results")
print("=" * 72)

if len(onsets) >= 2:
    onset_mean = statistics.mean(onsets)
    onset_std = statistics.stdev(onsets)
    onset_min = min(onsets)
    onset_max = max(onsets)
    onset_3sig_lo = onset_mean - 3 * onset_std
    onset_3sig_hi = onset_mean + 3 * onset_std

    print(f"\nOnset Voltage (1mA, TT 27C):")
    print(f"  N = {len(onsets)} samples")
    print(f"  Mean = {onset_mean:.4f} V")
    print(f"  Std  = {onset_std*1000:.2f} mV")
    print(f"  Min  = {onset_min:.4f} V, Max = {onset_max:.4f} V")
    print(f"  3-sigma range: {onset_3sig_lo:.4f} V to {onset_3sig_hi:.4f} V")
    print(f"  Spec: 5.5 - 6.2 V")
    if onset_3sig_lo >= 5.5 and onset_3sig_hi <= 6.2:
        print(f"  3-sigma: PASS")
    else:
        print(f"  3-sigma: FAIL (spread exceeds spec window)")

if len(leakages) >= 2:
    leak_mean = statistics.mean(leakages)
    leak_std = statistics.stdev(leakages)
    leak_min = min(leakages)
    leak_max = max(leakages)
    leak_3sig = leak_mean + 3 * leak_std

    print(f"\nLeakage at 5.0V (TT 27C):")
    print(f"  N = {len(leakages)} samples")
    print(f"  Mean = {leak_mean:.1f} nA")
    print(f"  Std  = {leak_std:.1f} nA")
    print(f"  Min  = {leak_min:.1f} nA, Max = {leak_max:.1f} nA")
    print(f"  Mean + 3-sigma = {leak_3sig:.1f} nA")
    print(f"  Spec: <= 1000 nA")
    if leak_3sig <= 1000:
        print(f"  3-sigma: PASS")
    else:
        print(f"  3-sigma: FAIL ({leak_3sig:.0f} nA > 1000 nA)")

print()
print("=" * 72)
print(f"Yield estimate (onset in 5.5-6.2V AND leakage < 1000nA):")
n_yield = sum(1 for o, l in zip(onsets, leakages) if 5.5 <= o <= 6.2 and l <= 1000)
print(f"  {n_yield}/{min(len(onsets), len(leakages))} = {100*n_yield/min(len(onsets), len(leakages)):.1f}%")
