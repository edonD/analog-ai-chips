#!/usr/bin/env python3
"""Tune pseudo-differential BPF channels 1,3,4,5 to hit f0/Q targets."""

import subprocess, re, json, os, math, sys
import numpy as np

WORKDIR = "/home/ubuntu/analog-ai-chips/vibrosense/03_filters"

# Bias sets
BIAS_200 = {"VBN": 0.5973, "VBCN": 0.8273, "VBP": 0.8100, "VBCP": 0.5550}
BIAS_440 = {"VBN": 0.6399, "VBCN": 0.8699, "VBP": 0.7450, "VBCP": 0.4900}
BIAS_870 = {"VBN": 0.6914, "VBCN": 0.9214, "VBP": 0.6600, "VBCP": 0.4050}

CHANNELS = {
    1: {"f0": 224,   "Q": 0.75, "bias": BIAS_200, "c1_init": 586,  "c2_init": 1042},
    3: {"f0": 3162,  "Q": 1.05, "bias": BIAS_200, "c1_init": 58,   "c2_init": 53},
    4: {"f0": 7071,  "Q": 1.41, "bias": BIAS_440, "c1_init": 30,   "c2_init": 15},
    5: {"f0": 14142, "Q": 1.41, "bias": BIAS_870, "c1_init": 12,   "c2_init": 6},
}

SPICE_TEMPLATE = """\
* Pseudo-differential BPF tuning — Ch{ch}
.lib "../01_ota/sky130_minimal.lib.spice" tt
.include "../01_ota/ota_foldcasc.spice"
.include "pseudo_res.spice"

Vdd vdd 0 dc 1.8
Vbn vbn 0 dc {VBN}
Vbcn vbcn 0 dc {VBCN}
Vbp vbp 0 dc {VBP}
Vbcp vbcp 0 dc {VBCP}
Vcm vcm 0 dc 0.9

Vinp inp 0 dc 0.9 ac 0.5
Vinn inn 0 dc 0.9 ac -0.5

* Positive path
Xota1p inp int2p int1p vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1p int1p 0 {C1}p
Xpr1p int1p vcm pseudo_res
Xota2p int1p vcm int2p vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2p int2p 0 {C2}p
Xpr2p int2p vcm pseudo_res
Xota3p vcm int1p int1p vdd 0 vbn vbcn vbp vbcp ota_foldcasc

* Negative path
Xota1n inn int2n int1n vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1n int1n 0 {C1}p
Xpr1n int1n vcm pseudo_res
Xota2n int1n vcm int2n vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2n int2n 0 {C2}p
Xpr2n int2n vcm pseudo_res
Xota3n vcm int1n int1n vdd 0 vbn vbcn vbp vbcp ota_foldcasc

.nodeset v(int1p)=0.9 v(int2p)=0.9 v(int1n)=0.9 v(int2n)=0.9

.control
op
ac dec 200 {fmin} {fmax}
wrdata {outfile} vdb(int1p,int1n)
.endc
.end
"""


def run_sim(ch, c1, c2, bias, f0_target):
    """Run AC sim and return (f0_meas, Q_meas, pk_dB)."""
    fmin = max(1, f0_target / 20)
    fmax = f0_target * 20
    outfile = os.path.join(WORKDIR, f"tune_ch{ch}_iter.txt")
    spice_file = os.path.join(WORKDIR, f"tune_ch{ch}_iter.spice")

    spice = SPICE_TEMPLATE.format(
        ch=ch, C1=c1, C2=c2, fmin=fmin, fmax=fmax, outfile=outfile,
        **bias
    )
    with open(spice_file, 'w') as f:
        f.write(spice)

    result = subprocess.run(
        ["ngspice", "-b", spice_file],
        capture_output=True, text=True, cwd=WORKDIR, timeout=60
    )

    # Parse output
    freqs, dbs = [], []
    with open(outfile) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    freq = float(parts[0])
                    db = float(parts[1])
                    if freq > 0:
                        freqs.append(freq)
                        dbs.append(db)
                except ValueError:
                    continue

    if not freqs:
        return None, None, None

    freqs = np.array(freqs)
    dbs = np.array(dbs)

    # Find peak
    pk_idx = np.argmax(dbs)
    f0_meas = freqs[pk_idx]
    pk_dB = dbs[pk_idx]

    # Q from -3dB bandwidth
    thresh = pk_dB - 3.0
    above = dbs >= thresh

    # Find left edge
    f_lo = freqs[0]
    for i in range(pk_idx, 0, -1):
        if dbs[i] < thresh:
            # Interpolate
            f_lo = freqs[i] + (freqs[i+1] - freqs[i]) * (thresh - dbs[i]) / (dbs[i+1] - dbs[i])
            break

    # Find right edge
    f_hi = freqs[-1]
    for i in range(pk_idx, len(freqs)-1):
        if dbs[i] < thresh:
            f_hi = freqs[i-1] + (freqs[i] - freqs[i-1]) * (thresh - dbs[i-1]) / (dbs[i] - dbs[i-1])
            break

    bw = f_hi - f_lo
    Q_meas = f0_meas / bw if bw > 0 else 0

    return f0_meas, Q_meas, pk_dB


def tune_channel(ch, spec):
    """Iteratively tune C1/C2 for a channel."""
    f0_target = spec["f0"]
    Q_target = spec["Q"]
    bias = spec["bias"]
    c1 = spec["c1_init"]
    c2 = spec["c2_init"]

    print(f"\n{'='*60}")
    print(f"  Channel {ch}: f0={f0_target}Hz, Q={Q_target}")
    print(f"  Starting: C1={c1:.1f}p, C2={c2:.1f}p")
    print(f"{'='*60}")

    for iteration in range(20):
        f0_meas, Q_meas, pk_dB = run_sim(ch, c1, c2, bias, f0_target)

        if f0_meas is None:
            print(f"  Iter {iteration}: SIMULATION FAILED")
            continue

        f0_err = (f0_meas - f0_target) / f0_target
        Q_err = (Q_meas - Q_target) / Q_target

        print(f"  Iter {iteration:2d}: C1={c1:8.1f}p C2={c2:8.1f}p | "
              f"f0={f0_meas:8.1f}Hz ({f0_err:+.1%}) Q={Q_meas:.3f} ({Q_err:+.1%}) pk={pk_dB:.2f}dB")

        # Check convergence
        if abs(f0_err) < 0.05 and abs(Q_err) < 0.20:
            print(f"  ** CONVERGED **")
            return c1, c2, f0_meas, Q_meas, pk_dB

        # Adjust: scale sqrt(C1*C2) for f0, scale C1/C2 ratio for Q
        # f0 correction: scale geometric mean inversely
        geom = math.sqrt(c1 * c2)
        ratio = c1 / c2  # = Q^2 approximately

        # New geometric mean to hit target f0
        # f0 ~ 1/sqrt(C1*C2), so new_geom = geom * (f0_meas / f0_target)
        # Use damped correction to avoid oscillation
        alpha = 0.7  # damping
        new_geom = geom * (f0_meas / f0_target) ** alpha

        # New ratio to hit target Q
        # Q ~ sqrt(C1/C2), so ratio ~ Q^2
        target_ratio = Q_target ** 2
        new_ratio = ratio * (target_ratio / ratio) ** alpha

        # Reconstruct C1, C2
        c2 = new_geom / math.sqrt(new_ratio)
        c1 = c2 * new_ratio

        # Round to 0.1pF
        c1 = round(c1, 1)
        c2 = round(c2, 1)

        # Safety: clamp
        c1 = max(1.0, min(5000.0, c1))
        c2 = max(1.0, min(5000.0, c2))

    # If we didn't converge, return last values
    print(f"  ** DID NOT CONVERGE after 20 iterations **")
    return c1, c2, f0_meas, Q_meas, pk_dB


def main():
    results = {}

    # Ch2 is already done
    results["2"] = {"c1": 118, "c2": 260, "f0_meas": 1000, "Q_meas": 0.75, "pk_dB": 0.37}

    for ch in [1, 3, 4, 5]:
        c1, c2, f0, Q, pk = tune_channel(ch, CHANNELS[ch])
        results[str(ch)] = {
            "c1": round(c1, 1),
            "c2": round(c2, 1),
            "f0_meas": round(f0, 1),
            "Q_meas": round(Q, 3),
            "pk_dB": round(pk, 2)
        }

    # Write results
    outpath = os.path.join(WORKDIR, "pdiff_final_caps.json")
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n\nResults written to {outpath}")
    print(f"\n{'='*75}")
    print(f"{'Ch':>3} | {'C1(pF)':>8} | {'C2(pF)':>8} | {'f0(Hz)':>10} | {'Q':>6} | {'pk(dB)':>7}")
    print(f"{'-'*3}-+-{'-'*8}-+-{'-'*8}-+-{'-'*10}-+-{'-'*6}-+-{'-'*7}")
    for ch in ["1", "2", "3", "4", "5"]:
        r = results[ch]
        print(f"  {ch} | {r['c1']:8.1f} | {r['c2']:8.1f} | {r['f0_meas']:10.1f} | {r['Q_meas']:6.3f} | {r['pk_dB']:7.2f}")
    print(f"{'='*75}")


if __name__ == "__main__":
    main()
