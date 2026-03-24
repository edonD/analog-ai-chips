#!/usr/bin/env python3
"""Blockers 3-5: PVT corners, THD, and Noise verification for pseudo-diff BPF channels."""

import subprocess, json, re, os, math, numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return super().default(obj)

WORK = "/home/ubuntu/analog-ai-chips/vibrosense/03_filters"
os.chdir(WORK)

# Channel parameters
CH_CAPS = {
    1: {"C1": 586.0, "C2": 1042.0, "f0": 226.6},
    2: {"C1": 118.0, "C2": 260.0,  "f0": 1001.4},
    3: {"C1": 58.0,  "C2": 53.0,   "f0": 3162.0},
    4: {"C1": 59.0,  "C2": 29.7,   "f0": 7235.8},
    5: {"C1": 41.8,  "C2": 21.0,   "f0": 14639.4},
}

# Per-channel calibrated bias
CH_BIAS = {
    1: {"VBN": 0.5973, "VBP": 0.8100, "VBCN": 0.8273, "VBCP": 0.5550},
    2: {"VBN": 0.5973, "VBP": 0.8100, "VBCN": 0.8273, "VBCP": 0.5550},
    3: {"VBN": 0.5973, "VBP": 0.8100, "VBCN": 0.8273, "VBCP": 0.5550},
    4: {"VBN": 0.6399, "VBP": 0.7450, "VBCN": 0.8699, "VBCP": 0.4900},
    5: {"VBN": 0.6914, "VBP": 0.6600, "VBCN": 0.9214, "VBCP": 0.4050},
}

def gen_inline_filter(ch, suffix=""):
    """Generate inline pseudo-diff BPF netlist for a channel."""
    c = CH_CAPS[ch]
    C1 = c["C1"]
    C2 = c["C2"]
    s = suffix  # suffix for unique node names when multiple channels
    return f"""
* Positive path
Xota1p{s} vinp int2p{s} int1p{s} vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1p{s} int1p{s} 0 {C1}p
Xpr1p{s} int1p{s} vcm pseudo_res
Xota2p{s} int1p{s} vcm int2p{s} vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2p{s} int2p{s} 0 {C2}p
Xpr2p{s} int2p{s} vcm pseudo_res
Xota3p{s} vcm int1p{s} int1p{s} vdd 0 vbn vbcn vbp vbcp ota_foldcasc

* Negative path
Xota1n{s} vinn int2n{s} int1n{s} vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C1n{s} int1n{s} 0 {C1}p
Xpr1n{s} int1n{s} vcm pseudo_res
Xota2n{s} int1n{s} vcm int2n{s} vdd 0 vbn vbcn vbp vbcp ota_foldcasc
C2n{s} int2n{s} 0 {C2}p
Xpr2n{s} int2n{s} vcm pseudo_res
Xota3n{s} vcm int1n{s} int1n{s} vdd 0 vbn vbcn vbp vbcp ota_foldcasc
"""

def run_ngspice(spice_file, out_file=None):
    """Run ngspice and return stdout."""
    cmd = ["ngspice", "-b", spice_file]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return result.stdout + result.stderr

def parse_ac_data(filename):
    """Parse wrdata AC output: freq, vdb, vphase."""
    freqs, vdbs = [], []
    with open(filename) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    freq = float(parts[0])
                    vdb = float(parts[1])
                    if freq > 0:
                        freqs.append(freq)
                        vdbs.append(vdb)
                except ValueError:
                    continue
    return np.array(freqs), np.array(vdbs)

def find_peak(freqs, vdbs):
    """Find peak frequency and dB from AC sweep."""
    idx = np.argmax(vdbs)
    return freqs[idx], vdbs[idx]

def find_f0_Q(freqs, vdbs):
    """Find f0 (peak) and Q from -3dB bandwidth."""
    pk_idx = np.argmax(vdbs)
    f0 = freqs[pk_idx]
    pk = vdbs[pk_idx]
    thr = pk - 3.0
    # Find -3dB points
    fl, fh = freqs[0], freqs[-1]
    for i in range(pk_idx, 0, -1):
        if vdbs[i] < thr:
            fl = freqs[i] + (freqs[i+1]-freqs[i]) * (thr-vdbs[i])/(vdbs[i+1]-vdbs[i])
            break
    for i in range(pk_idx, len(vdbs)-1):
        if vdbs[i] < thr:
            fh = freqs[i-1] + (freqs[i]-freqs[i-1]) * (thr-vdbs[i-1])/(vdbs[i]-vdbs[i-1])
            break
    bw = fh - fl
    Q = f0 / bw if bw > 0 else 0
    return f0, Q, pk


# ============================================================
# BLOCKER 3: PVT Corners (Ch2 only)
# ============================================================
print("=" * 70)
print("BLOCKER 3: PVT Corner Sweep — Ch2 (f0_nom=1001Hz)")
print("=" * 70)

pvt_corners = [
    ("tt", 27), ("ss", 27), ("ff", 27), ("sf", 27), ("fs", 27),
    ("tt", -40), ("tt", 85),
]

b = CH_BIAS[2]
c = CH_CAPS[2]

pvt_results = []

for corner, temp in pvt_corners:
    tag = f"{corner}_{temp}C"
    spice_file = f"{WORK}/tb_b3_pvt_{tag}.spice"
    data_file = f"{WORK}/b3_pvt_{tag}.txt"

    spice = f"""* BLOCKER 3: PVT sweep Ch2 — {corner} @ {temp}C
.lib "../01_ota/sky130_minimal.lib.spice" {corner}
.include "../01_ota/ota_foldcasc.spice"
.include "pseudo_res.spice"

.temp {temp}

Vdd vdd 0 dc 1.8
Vcm vcm 0 dc 0.9

* Fixed calibrated bias voltages (uncorrected)
Vvbn vbn 0 dc {b['VBN']}
Vvbp vbp 0 dc {b['VBP']}
Vvbcn vbcn 0 dc {b['VBCN']}
Vvbcp vbcp 0 dc {b['VBCP']}

* Differential AC input
Vinp vinp 0 dc 0.9 ac 0.5
Vinn vinn 0 dc 0.9 ac -0.5

{gen_inline_filter(2)}

.nodeset v(int1p)=0.9 v(int2p)=0.9
+ v(int1n)=0.9 v(int2n)=0.9

.control
op
ac dec 200 10 100k
wrdata {data_file} vdb(int1p,int1n) vp(int1p,int1n)
.endc
.end
"""
    with open(spice_file, 'w') as f:
        f.write(spice)

    print(f"  Running {tag}...", end=" ", flush=True)
    out = run_ngspice(spice_file)

    try:
        freqs, vdbs = parse_ac_data(data_file)
        f0, Q, pk = find_f0_Q(freqs, vdbs)
        shift_pct = (f0 - c["f0"]) / c["f0"] * 100
        functional = pk > -10.0
        print(f"f0={f0:.1f}Hz Q={Q:.3f} pk={pk:.2f}dB shift={shift_pct:+.1f}% {'PASS' if functional else 'FAIL'}")
        pvt_results.append({
            "corner": corner, "temp": temp, "tag": tag,
            "f0_Hz": round(float(f0), 1), "Q": round(float(Q), 3), "pk_dB": round(float(pk), 2),
            "f0_shift_pct": round(float(shift_pct), 1), "functional": bool(functional)
        })
    except Exception as e:
        print(f"PARSE ERROR: {e}")
        pvt_results.append({
            "corner": corner, "temp": temp, "tag": tag,
            "f0_Hz": None, "Q": None, "pk_dB": None,
            "f0_shift_pct": None, "functional": False, "error": str(e)
        })

# Save Blocker 3 results
all_functional = all(r["functional"] for r in pvt_results)
b3_out = {
    "blocker": 3, "test": "PVT_corners", "channel": 2,
    "nominal_f0_Hz": c["f0"],
    "bias_fixed": b,
    "pass_criteria": "pk > -10dB at all corners",
    "overall_pass": all_functional,
    "corners": pvt_results
}
with open(f"{WORK}/blocker3_pvt.json", 'w') as f:
    json.dump(b3_out, f, indent=2, cls=NpEncoder)

print(f"\nBLOCKER 3 OVERALL: {'PASS' if all_functional else 'FAIL'}")
print(f"  Max f0 shift: {max(abs(r['f0_shift_pct']) for r in pvt_results if r['f0_shift_pct'] is not None):.1f}%")


# ============================================================
# BLOCKER 4: THD (Ch1, Ch2, Ch5)
# ============================================================
print("\n" + "=" * 70)
print("BLOCKER 4: THD Verification — Ch1, Ch2, Ch5")
print("=" * 70)

thd_channels = [1, 2, 5]
thd_results = []

for ch in thd_channels:
    b = CH_BIAS[ch]
    c = CH_CAPS[ch]
    f0 = c["f0"]

    # Transient duration: ensure at least 20 cycles at f0 for FFT resolution
    min_cycles = 25
    period = 1.0 / f0
    settle_time = max(10e-3, 10 * period)  # 10ms or 10 cycles, whichever larger
    analysis_time = max(20e-3, min_cycles * period)
    dur = settle_time + analysis_time
    tstep = min(1.0 / (f0 * 100), 1e-6)  # at least 100 pts per cycle

    spice_file = f"{WORK}/tb_b4_thd_ch{ch}.spice"
    data_file = f"{WORK}/b4_thd_ch{ch}.txt"

    spice = f"""* BLOCKER 4: THD — Ch{ch} f0={f0:.1f}Hz, 200mVpp diff
.lib "../01_ota/sky130_minimal.lib.spice" tt
.include "../01_ota/ota_foldcasc.spice"
.include "pseudo_res.spice"

Vdd vdd 0 dc 1.8
Vcm vcm 0 dc 0.9

Vvbn vbn 0 dc {b['VBN']}
Vvbp vbp 0 dc {b['VBP']}
Vvbcn vbcn 0 dc {b['VBCN']}
Vvbcp vbcp 0 dc {b['VBCP']}

* Differential sinusoidal input: 200mVpp = +/-50mV around 0.9V
Vinp vinp 0 SIN(0.9 0.05 {f0})
Vinn vinn 0 SIN(0.9 -0.05 {f0})

{gen_inline_filter(ch)}

.nodeset v(int1p)=0.9 v(int2p)=0.9
+ v(int1n)=0.9 v(int2n)=0.9

.control
tran {tstep} {dur} 0 uic
* Save differential output for FFT analysis
let vdiff = v(int1p) - v(int1n)
wrdata {data_file} vdiff
.endc
.end
"""
    with open(spice_file, 'w') as f:
        f.write(spice)

    print(f"  Running Ch{ch} (f0={f0:.1f}Hz)...", end=" ", flush=True)
    out = run_ngspice(spice_file)

    try:
        # Parse transient data
        times, vals = [], []
        with open(data_file) as f2:
            for line in f2:
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        t = float(parts[0])
                        v = float(parts[1])
                        times.append(t)
                        vals.append(v)
                    except ValueError:
                        continue

        times = np.array(times)
        vals = np.array(vals)

        # Skip settling time
        mask = times >= settle_time
        t_ss = times[mask]
        v_ss = vals[mask]

        if len(v_ss) < 100:
            raise ValueError(f"Only {len(v_ss)} samples after settling")

        # Compute FFT
        N = len(v_ss)
        dt = (t_ss[-1] - t_ss[0]) / (N - 1)
        fs = 1.0 / dt

        # Window
        window = np.hanning(N)
        v_win = v_ss * window

        fft_vals = np.fft.rfft(v_win)
        fft_mag = np.abs(fft_vals) * 2.0 / np.sum(window)
        fft_freqs = np.fft.rfftfreq(N, dt)

        # Find fundamental
        f0_idx = np.argmin(np.abs(fft_freqs - f0))
        # Search around expected f0 for actual peak
        search_lo = max(0, f0_idx - 10)
        search_hi = min(len(fft_mag), f0_idx + 10)
        fund_idx = search_lo + np.argmax(fft_mag[search_lo:search_hi])
        fund_mag = fft_mag[fund_idx]
        fund_freq = fft_freqs[fund_idx]

        # HD2, HD3
        h2_idx = np.argmin(np.abs(fft_freqs - 2 * fund_freq))
        h3_idx = np.argmin(np.abs(fft_freqs - 3 * fund_freq))

        # Search around harmonics
        for hidx_var in [h2_idx, h3_idx]:
            pass

        search_lo2 = max(0, h2_idx - 5)
        search_hi2 = min(len(fft_mag), h2_idx + 5)
        h2_mag = np.max(fft_mag[search_lo2:search_hi2])

        search_lo3 = max(0, h3_idx - 5)
        search_hi3 = min(len(fft_mag), h3_idx + 5)
        h3_mag = np.max(fft_mag[search_lo3:search_hi3])

        hd2_dbc = 20 * np.log10(h2_mag / fund_mag) if h2_mag > 0 and fund_mag > 0 else -999
        hd3_dbc = 20 * np.log10(h3_mag / fund_mag) if h3_mag > 0 and fund_mag > 0 else -999

        # THD = sqrt(H2^2 + H3^2 + ...) / H1 — use up to H5
        harm_sum_sq = h2_mag**2 + h3_mag**2
        for hn in [4, 5]:
            hn_idx = np.argmin(np.abs(fft_freqs - hn * fund_freq))
            slo = max(0, hn_idx - 5)
            shi = min(len(fft_mag), hn_idx + 5)
            hn_mag = np.max(fft_mag[slo:shi])
            harm_sum_sq += hn_mag**2

        thd_ratio = math.sqrt(harm_sum_sq) / fund_mag if fund_mag > 0 else 999
        thd_dbc = 20 * np.log10(thd_ratio) if thd_ratio > 0 else -999

        passed = thd_dbc < -30.0

        print(f"HD2={hd2_dbc:.1f}dBc HD3={hd3_dbc:.1f}dBc THD={thd_dbc:.1f}dBc "
              f"fund={fund_mag*1e3:.2f}mV {'PASS' if passed else 'FAIL'}")

        thd_results.append({
            "channel": ch, "f0_Hz": round(f0, 1),
            "fund_freq_Hz": round(fund_freq, 1),
            "fund_mag_mV": round(fund_mag * 1e3, 3),
            "HD2_dBc": round(hd2_dbc, 1), "HD3_dBc": round(hd3_dbc, 1),
            "THD_dBc": round(thd_dbc, 1),
            "pass": passed
        })
    except Exception as e:
        print(f"ERROR: {e}")
        thd_results.append({
            "channel": ch, "f0_Hz": round(f0, 1),
            "error": str(e), "pass": False
        })

thd_all_pass = all(r["pass"] for r in thd_results)
b4_out = {
    "blocker": 4, "test": "THD",
    "input": "200mVpp differential",
    "pass_criteria": "THD < -30 dBc",
    "overall_pass": thd_all_pass,
    "channels": thd_results
}
with open(f"{WORK}/blocker4_thd.json", 'w') as f:
    json.dump(b4_out, f, indent=2, cls=NpEncoder)

print(f"\nBLOCKER 4 OVERALL: {'PASS' if thd_all_pass else 'FAIL'}")


# ============================================================
# BLOCKER 5: Noise (all 5 channels)
# ============================================================
print("\n" + "=" * 70)
print("BLOCKER 5: Noise Verification — All 5 Channels")
print("=" * 70)

noise_results = []

for ch in range(1, 6):
    b = CH_BIAS[ch]
    c = CH_CAPS[ch]

    spice_file = f"{WORK}/tb_b5_noise_ch{ch}.spice"

    # For noise, run on positive path only and multiply by sqrt(2) for pseudo-diff
    spice = f"""* BLOCKER 5: Noise — Ch{ch} f0={c['f0']:.1f}Hz (positive path only, x sqrt2)
.lib "../01_ota/sky130_minimal.lib.spice" tt
.include "../01_ota/ota_foldcasc.spice"
.include "pseudo_res.spice"

Vdd vdd 0 dc 1.8
Vcm vcm 0 dc 0.9

Vvbn vbn 0 dc {b['VBN']}
Vvbp vbp 0 dc {b['VBP']}
Vvbcn vbcn 0 dc {b['VBCN']}
Vvbcp vbcp 0 dc {b['VBCP']}

* AC input for noise analysis
Vinp vinp 0 dc 0.9 ac 0
Vinn vinn 0 dc 0.9 ac 0

{gen_inline_filter(ch)}

* Diff-to-single via VCVS for noise measurement
Ediff ndiff 0 int1p int1n 1.0
Rdiff ndiff 0 1G

.nodeset v(int1p)=0.9 v(int2p)=0.9
+ v(int1n)=0.9 v(int2n)=0.9

.control
op
noise v(ndiff) Vinp dec 50 1 100k
setplot noise2
print onoise_total
.endc
.end
"""
    with open(spice_file, 'w') as f:
        f.write(spice)

    print(f"  Running Ch{ch} (f0={c['f0']:.1f}Hz)...", end=" ", flush=True)
    out = run_ngspice(spice_file)

    # Parse onoise_total from output
    onoise = None
    for line in out.split('\n'):
        if 'onoise_total' in line.lower() and '=' in line:
            # Extract value
            m = re.search(r'=\s*([0-9eE.+\-]+)', line)
            if m:
                onoise = float(m.group(1))
                break

    if onoise is not None:
        onoise_uv = onoise * 1e6
        onoise_mv = onoise * 1e3
        passed = onoise_mv < 1.0
        print(f"onoise_total={onoise_uv:.1f}uVrms ({onoise_mv:.4f}mVrms) {'PASS' if passed else 'FAIL'}")
        noise_results.append({
            "channel": ch, "f0_Hz": round(c["f0"], 1),
            "onoise_total_Vrms": onoise,
            "onoise_uVrms": round(onoise_uv, 1),
            "onoise_mVrms": round(onoise_mv, 4),
            "pass": passed
        })
    else:
        print(f"PARSE ERROR — could not find onoise_total")
        # Print relevant output for debugging
        for line in out.split('\n'):
            if 'noise' in line.lower() or 'error' in line.lower():
                print(f"    {line.strip()}")
        noise_results.append({
            "channel": ch, "f0_Hz": round(c["f0"], 1),
            "error": "Could not parse onoise_total",
            "pass": False
        })

noise_all_pass = all(r["pass"] for r in noise_results)
b5_out = {
    "blocker": 5, "test": "Noise",
    "analysis": ".noise v(int1p,int1n) dec 50 1 100k",
    "pass_criteria": "onoise_total < 1 mVrms",
    "overall_pass": noise_all_pass,
    "channels": noise_results
}
with open(f"{WORK}/blocker5_noise.json", 'w') as f:
    json.dump(b5_out, f, indent=2, cls=NpEncoder)

print(f"\nBLOCKER 5 OVERALL: {'PASS' if noise_all_pass else 'FAIL'}")


# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY TABLE — BLOCKERS 3-5")
print("=" * 70)

print("\n--- BLOCKER 3: PVT Corners (Ch2, fixed bias) ---")
print(f"{'Corner':<12} {'Temp':>6} {'f0 (Hz)':>10} {'Q':>8} {'Peak(dB)':>10} {'Shift%':>8} {'Pass':>6}")
print("-" * 62)
for r in pvt_results:
    f0s = f"{r['f0_Hz']:.1f}" if r['f0_Hz'] else "N/A"
    qs = f"{r['Q']:.3f}" if r['Q'] else "N/A"
    pks = f"{r['pk_dB']:.2f}" if r['pk_dB'] is not None else "N/A"
    shs = f"{r['f0_shift_pct']:+.1f}" if r['f0_shift_pct'] is not None else "N/A"
    ps = "PASS" if r['functional'] else "FAIL"
    print(f"{r['corner']:<12} {r['temp']:>4}C {f0s:>10} {qs:>8} {pks:>10} {shs:>8} {ps:>6}")
print(f"Overall: {'PASS' if all_functional else 'FAIL'}")

print("\n--- BLOCKER 4: THD (200mVpp differential) ---")
print(f"{'Channel':<10} {'f0 (Hz)':>10} {'HD2(dBc)':>10} {'HD3(dBc)':>10} {'THD(dBc)':>10} {'Pass':>6}")
print("-" * 58)
for r in thd_results:
    if "error" not in r:
        print(f"Ch{r['channel']:<8} {r['f0_Hz']:>10.1f} {r['HD2_dBc']:>10.1f} {r['HD3_dBc']:>10.1f} {r['THD_dBc']:>10.1f} {'PASS' if r['pass'] else 'FAIL':>6}")
    else:
        print(f"Ch{r['channel']:<8} {r['f0_Hz']:>10.1f} {'ERROR':>10} {'ERROR':>10} {'ERROR':>10} {'FAIL':>6}")
print(f"Overall: {'PASS' if thd_all_pass else 'FAIL'}  (criteria: THD < -30 dBc)")

print("\n--- BLOCKER 5: Noise ---")
print(f"{'Channel':<10} {'f0 (Hz)':>10} {'Noise(uVrms)':>14} {'Noise(mVrms)':>14} {'Pass':>6}")
print("-" * 58)
for r in noise_results:
    if "error" not in r:
        print(f"Ch{r['channel']:<8} {r['f0_Hz']:>10.1f} {r['onoise_uVrms']:>14.1f} {r['onoise_mVrms']:>14.4f} {'PASS' if r['pass'] else 'FAIL':>6}")
    else:
        print(f"Ch{r['channel']:<8} {r['f0_Hz']:>10.1f} {'ERROR':>14} {'ERROR':>14} {'FAIL':>6}")
print(f"Overall: {'PASS' if noise_all_pass else 'FAIL'}  (criteria: < 1 mVrms)")

print("\n" + "=" * 70)
b3p = "PASS" if all_functional else "FAIL"
b4p = "PASS" if thd_all_pass else "FAIL"
b5p = "PASS" if noise_all_pass else "FAIL"
print(f"BLOCKER 3 (PVT):   {b3p}")
print(f"BLOCKER 4 (THD):   {b4p}")
print(f"BLOCKER 5 (Noise): {b5p}")
all_pass = all_functional and thd_all_pass and noise_all_pass
print(f"ALL BLOCKERS:      {'PASS' if all_pass else 'FAIL'}")
print("=" * 70)
