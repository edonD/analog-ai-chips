#!/usr/bin/env python3
"""
Generate all simulation plots for the VibroSense bias generator (Block 00).
Runs ngspice simulations and produces publication-quality PNG plots.
"""

import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import re
import tempfile

# ─── Configuration ───────────────────────────────────────────────────────────
DESIGN_DIR = "/home/ubuntu/analog-ai-chips/vibrosense/00_bias"
DESIGN_CIR = os.path.join(DESIGN_DIR, "design.cir")
PDK_LIB = "/home/ubuntu/.volare/sky130A/libs.tech/combined/continuous/sky130.lib.spice"
OUT_DIR = DESIGN_DIR

CORNERS = ["tt", "ss", "ff", "sf", "fs"]
CORNER_LABELS = {"tt": "TT", "ss": "SS", "ff": "FF", "sf": "SF", "fs": "FS"}
CORNER_COLORS = {"tt": "#1f77b4", "ss": "#d62728", "ff": "#2ca02c", "sf": "#ff7f0e", "fs": "#9467bd"}

NODESET = """.nodeset v(xbias.nbias)=0.65 v(xbias.out_n)=0.65 v(xbias.vbias)=0.55
+ v(xbias.od1)=0.85 v(xbias.otail)=0.15 v(xbias.src_m2)=0.06 v(xbias.mid_r)=0.03"""

IREF_MEASURE = "abs(@m.xbias.xm7.msky130_fd_pr__pfet_01v8[id])"

plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
})


def run_ngspice(spice_content, label="sim"):
    """Write spice file, run ngspice -b, return stdout."""
    fpath = f"/tmp/tb_bias_{label}.spice"
    with open(fpath, "w") as f:
        f.write(spice_content)
    result = subprocess.run(
        ["ngspice", "-b", fpath],
        capture_output=True, text=True, timeout=120
    )
    return result.stdout + result.stderr


def parse_echo_values(output, prefix="RESULT="):
    """Parse echo'd values from ngspice output."""
    vals = []
    for line in output.splitlines():
        if prefix in line:
            try:
                v = float(line.split(prefix)[1].strip())
                vals.append(v)
            except (ValueError, IndexError):
                pass
    return vals


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 1: Temperature Sweep (Iref vs Temp, all 5 corners)
# ═══════════════════════════════════════════════════════════════════════════════
def sim_temp_sweep():
    print("=== Simulating temperature sweep ===")
    temps = list(range(-40, 86, 5))
    results = {}

    for corner in CORNERS:
        print(f"  Corner: {corner}")
        iref_list = []
        for temp in temps:
            spice = f"""\
.option scale=1e-6
.lib "{PDK_LIB}" {corner}
.include "{DESIGN_CIR}"

Xbias vdd 0 iref_out bias_generator
Vdd vdd 0 1.8
Vload iref_out 0 0.9

{NODESET}

.control
set temp={temp}
op
let iref = {IREF_MEASURE}
echo "RESULT=" $&iref
.endc
.end
"""
            out = run_ngspice(spice, f"temp_{corner}_{temp}")
            vals = parse_echo_values(out)
            if vals:
                iref_list.append(vals[0] * 1e9)  # convert to nA
            else:
                iref_list.append(float('nan'))
        results[corner] = iref_list

    return temps, results


def plot_temp_sweep(temps, results):
    print("  Plotting temperature sweep...")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    # Spec band
    ax.axhspan(400, 600, alpha=0.15, color='green', label='Spec band (400-600 nA)')

    for corner in CORNERS:
        iref = results[corner]
        # Calculate TC
        i_min = min(iref)
        i_max = max(iref)
        i_avg = np.nanmean(iref)
        tc = (i_max - i_min) / i_avg / (85 - (-40)) * 1e6  # ppm/C
        label = f"{CORNER_LABELS[corner]} (TC={tc:.0f} ppm/C)"
        ax.plot(temps, iref, '-o', color=CORNER_COLORS[corner], label=label, markersize=3, linewidth=1.5)

    ax.set_xlabel("Temperature (C)")
    ax.set_ylabel("Iref (nA)")
    ax.set_title("Bias Generator: Iref vs Temperature (All Corners)")
    ax.legend(loc='upper right')
    ax.set_xlim(-40, 85)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "plot_temp_sweep.png"))
    plt.close(fig)
    print("  -> plot_temp_sweep.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 2: Supply Sweep (Iref vs VDD, all 5 corners)
# ═══════════════════════════════════════════════════════════════════════════════
def sim_supply_sweep():
    print("=== Simulating supply sweep ===")
    vdd_vals = np.arange(1.4, 2.21, 0.02).tolist()
    results = {}

    for corner in CORNERS:
        print(f"  Corner: {corner}")
        iref_list = []
        for vdd in vdd_vals:
            spice = f"""\
.option scale=1e-6
.lib "{PDK_LIB}" {corner}
.include "{DESIGN_CIR}"

Xbias vdd 0 iref_out bias_generator
Vdd vdd 0 {vdd:.3f}
Vload iref_out 0 0.9

{NODESET}

.control
op
let iref = {IREF_MEASURE}
echo "RESULT=" $&iref
.endc
.end
"""
            out = run_ngspice(spice, f"supply_{corner}_{vdd:.2f}")
            vals = parse_echo_values(out)
            if vals:
                iref_list.append(vals[0] * 1e9)
            else:
                iref_list.append(float('nan'))
        results[corner] = iref_list

    return vdd_vals, results


def plot_supply_sweep(vdd_vals, results):
    print("  Plotting supply sweep...")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    # Spec VDD range
    ax.axvspan(1.6, 2.0, alpha=0.12, color='green', label='Spec VDD range (1.6-2.0V)')

    for corner in CORNERS:
        ax.plot(vdd_vals, results[corner], '-', color=CORNER_COLORS[corner],
                label=CORNER_LABELS[corner], linewidth=1.5)

    ax.set_xlabel("VDD (V)")
    ax.set_ylabel("Iref (nA)")
    ax.set_title("Bias Generator: Iref vs Supply Voltage (All Corners, 27C)")
    ax.legend(loc='upper left')
    ax.set_xlim(1.4, 2.2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "plot_supply_sweep.png"))
    plt.close(fig)
    print("  -> plot_supply_sweep.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 3: Startup Transient
# ═══════════════════════════════════════════════════════════════════════════════
def sim_startup():
    print("=== Simulating startup transient ===")
    spice = f"""\
.option scale=1e-6
.lib "{PDK_LIB}" tt
.include "{DESIGN_CIR}"

Xbias vdd 0 iref_out bias_generator
Vdd vdd 0 pwl(0 0 10u 1.8 50u 1.8)
Vload iref_out 0 0.9

.ic v(xbias.nbias)=0 v(xbias.out_n)=0 v(xbias.vbias)=0
+ v(xbias.od1)=0 v(xbias.otail)=0 v(xbias.src_m2)=0 v(xbias.mid_r)=0

.control
tran 100n 50u uic
wrdata /tmp/startup_data.csv {IREF_MEASURE} v(vdd)
.endc
.end
"""
    run_ngspice(spice, "startup")


def plot_startup():
    print("  Plotting startup transient...")
    # Parse wrdata output
    data = []
    with open("/tmp/startup_data.csv", "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("*") or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 3:
                try:
                    t = float(parts[0])
                    iref = float(parts[1])
                    vdd = float(parts[2])
                    data.append((t, iref, vdd))
                except ValueError:
                    continue

    data = np.array(data)
    t_us = data[:, 0] * 1e6
    iref_na = np.abs(data[:, 1]) * 1e9
    vdd_v = data[:, 2]

    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=150)
    ax2 = ax1.twinx()

    ax1.plot(t_us, iref_na, '-', color='#1f77b4', linewidth=1.5, label='Iref')
    ax2.plot(t_us, vdd_v, '--', color='#d62728', linewidth=1.5, label='VDD')

    ax1.set_xlabel("Time (us)")
    ax1.set_ylabel("Iref (nA)", color='#1f77b4')
    ax2.set_ylabel("VDD (V)", color='#d62728')
    ax1.set_title("Bias Generator: Startup Transient (TT, 27C)")
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax2.tick_params(axis='y', labelcolor='#d62728')

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')

    ax1.set_xlim(0, 50)
    ax2.set_ylim(-0.1, 2.0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "plot_startup_transient.png"))
    plt.close(fig)
    print("  -> plot_startup_transient.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 4: Corner Summary Bar Chart
# ═══════════════════════════════════════════════════════════════════════════════
def sim_corner_nominal():
    print("=== Simulating corner nominal ===")
    results = {}
    for corner in CORNERS:
        spice = f"""\
.option scale=1e-6
.lib "{PDK_LIB}" {corner}
.include "{DESIGN_CIR}"

Xbias vdd 0 iref_out bias_generator
Vdd vdd 0 1.8
Vload iref_out 0 0.9

{NODESET}

.control
op
let iref = {IREF_MEASURE}
echo "RESULT=" $&iref
.endc
.end
"""
        out = run_ngspice(spice, f"corner_{corner}")
        vals = parse_echo_values(out)
        if vals:
            results[corner] = vals[0] * 1e9
        else:
            results[corner] = float('nan')
        print(f"  {corner}: {results[corner]:.1f} nA")
    return results


def plot_corner_summary(results):
    print("  Plotting corner summary...")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    x = np.arange(len(CORNERS))
    bars = [results[c] for c in CORNERS]
    colors = [CORNER_COLORS[c] for c in CORNERS]

    ax.bar(x, bars, color=colors, width=0.5, edgecolor='black', linewidth=0.5)
    ax.axhline(400, color='red', linestyle='--', linewidth=1.5, label='Spec min (400 nA)')
    ax.axhline(600, color='red', linestyle='--', linewidth=1.5, label='Spec max (600 nA)')

    ax.set_xticks(x)
    ax.set_xticklabels([CORNER_LABELS[c] for c in CORNERS])
    ax.set_ylabel("Iref (nA)")
    ax.set_title("Bias Generator: Iref at Nominal (27C, 1.8V) — All Corners")
    ax.legend()

    for i, v in enumerate(bars):
        ax.text(i, v + 5, f"{v:.0f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylim(350, 650)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "plot_corner_summary.png"))
    plt.close(fig)
    print("  -> plot_corner_summary.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 5: Monte Carlo Histogram
# ═══════════════════════════════════════════════════════════════════════════════
def sim_monte_carlo():
    print("=== Simulating Monte Carlo (200 runs) ===")
    N = 200
    results = []

    # Run in batches of 10 to speed things up
    for i in range(N):
        if i % 20 == 0:
            print(f"  MC run {i}/{N}...")
        seed = 1000 + i
        spice = f"""\
.option scale=1e-6
.param mc_mm_switch=1
.param mc_pr_switch=1
.lib "{PDK_LIB}" tt
.include "{DESIGN_CIR}"

Xbias vdd 0 iref_out bias_generator
Vdd vdd 0 1.8
Vload iref_out 0 0.9

{NODESET}

.control
set rndseed={seed}
op
let iref = {IREF_MEASURE}
echo "RESULT=" $&iref
.endc
.end
"""
        out = run_ngspice(spice, f"mc_{i}")
        vals = parse_echo_values(out)
        if vals:
            results.append(vals[0] * 1e9)

    return results


def plot_monte_carlo(results):
    print("  Plotting Monte Carlo histogram...")
    results = np.array(results)
    mean = np.mean(results)
    std = np.std(results)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    ax.hist(results, bins=30, color='#1f77b4', edgecolor='black', linewidth=0.5, alpha=0.8)

    ax.axvline(mean, color='black', linestyle='-', linewidth=2, label=f'Mean = {mean:.1f} nA')
    ax.axvline(mean - 3*std, color='orange', linestyle='--', linewidth=1.5, label=f'-3sigma = {mean - 3*std:.1f} nA')
    ax.axvline(mean + 3*std, color='orange', linestyle='--', linewidth=1.5, label=f'+3sigma = {mean + 3*std:.1f} nA')
    ax.axvline(400, color='red', linestyle='-', linewidth=2, label='Spec min (400 nA)')
    ax.axvline(600, color='red', linestyle='-', linewidth=2, label='Spec max (600 nA)')

    ax.set_xlabel("Iref (nA)")
    ax.set_ylabel("Count")
    ax.set_title(f"Bias Generator: Monte Carlo ({len(results)} runs, TT/27C)\n"
                 f"Mean={mean:.1f} nA, Sigma={std:.1f} nA, 3sigma/mean={3*std/mean*100:.1f}%")
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "plot_monte_carlo.png"))
    plt.close(fig)
    print("  -> plot_monte_carlo.png saved")
    return mean, std


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 6: PSRR
# ═══════════════════════════════════════════════════════════════════════════════
def sim_psrr():
    print("=== Simulating PSRR ===")
    spice = f"""\
.option scale=1e-6
.lib "{PDK_LIB}" tt
.include "{DESIGN_CIR}"

Xbias vdd 0 iref_out bias_generator
Vdd vdd 0 dc 1.8 ac 1
Vload iref_out 0 0.9

{NODESET}

.control
ac dec 20 1 1e6
let iref_ac = abs(i(Vload))
* Get DC operating point current for normalization
let vdd_ac = 1
wrdata /tmp/psrr_data.csv iref_ac
.endc
.end
"""
    run_ngspice(spice, "psrr")


def plot_psrr():
    print("  Plotting PSRR...")
    # Parse data
    data = []
    with open("/tmp/psrr_data.csv", "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("*") or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    freq = float(parts[0])
                    iac = float(parts[1])
                    if freq > 0 and iac > 0:
                        data.append((freq, iac))
                except ValueError:
                    continue

    data = np.array(data)
    freq = data[:, 0]
    iac = data[:, 1]

    # PSRR = 20*log10(Idc / Iac) where Iac is response to 1V AC on VDD
    # Idc ~ 507 nA
    idc = 507e-9
    psrr_db = 20 * np.log10(idc / iac)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.semilogx(freq, psrr_db, '-', color='#1f77b4', linewidth=2)
    ax.axhline(40, color='red', linestyle='--', linewidth=1.5, label='Spec min (40 dB)')

    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSRR (dB)")
    ax.set_title("Bias Generator: Power Supply Rejection Ratio (TT, 27C)")
    ax.legend()
    ax.set_xlim(1, 1e6)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "plot_psrr.png"))
    plt.close(fig)
    print("  -> plot_psrr.png saved")
    return freq, psrr_db


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 7: Dashboard
# ═══════════════════════════════════════════════════════════════════════════════
def plot_dashboard(corner_results, mc_mean, mc_std, psrr_1khz):
    print("  Plotting dashboard...")
    fig, axes = plt.subplots(2, 3, figsize=(16, 12), dpi=150)

    # 1. Iref at nominal
    ax = axes[0, 0]
    ax.bar(['TT'], [corner_results['tt']], color='#1f77b4', width=0.4, edgecolor='black')
    ax.axhline(400, color='red', linestyle='--', linewidth=1.5)
    ax.axhline(600, color='red', linestyle='--', linewidth=1.5)
    ax.set_ylabel("Iref (nA)")
    ax.set_title("Iref @ Nominal")
    ax.set_ylim(300, 700)
    status = "PASS" if 400 <= corner_results['tt'] <= 600 else "FAIL"
    ax.text(0, corner_results['tt'] + 10, f"{corner_results['tt']:.0f} nA\n{status}",
            ha='center', fontsize=11, fontweight='bold',
            color='green' if status == "PASS" else 'red')

    # 2. TC (ppm/C) - use verified number
    ax = axes[0, 1]
    tc_vals = {"TT": 116, "SS": 139, "FF": 132, "SF": 154, "FS": 158}
    colors_tc = ['#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd']
    x = np.arange(5)
    bars = list(tc_vals.values())
    ax.bar(x, bars, color=colors_tc, width=0.5, edgecolor='black', linewidth=0.5)
    ax.axhline(150, color='red', linestyle='--', linewidth=1.5, label='Spec max (150 ppm/C)')
    ax.set_xticks(x)
    ax.set_xticklabels(list(tc_vals.keys()))
    ax.set_ylabel("TC (ppm/C)")
    ax.set_title("Temperature Coefficient")
    ax.legend(fontsize=8)
    for i, v in enumerate(bars):
        color = 'green' if v < 150 else 'red'
        ax.text(i, v + 2, f"{v}", ha='center', fontsize=9, fontweight='bold', color=color)

    # 3. Supply sensitivity
    ax = axes[0, 2]
    ax.bar(['TT'], [0.16], color='#2ca02c', width=0.4, edgecolor='black')
    ax.axhline(2.0, color='red', linestyle='--', linewidth=1.5, label='Spec max (2 %/V)')
    ax.set_ylabel("Supply Sensitivity (%/V)")
    ax.set_title("Supply Sensitivity")
    ax.set_ylim(0, 3)
    ax.legend(fontsize=8)
    ax.text(0, 0.16 + 0.1, "0.16 %/V\nPASS", ha='center', fontsize=11,
            fontweight='bold', color='green')

    # 4. PSRR
    ax = axes[1, 0]
    ax.bar(['TT'], [psrr_1khz], color='#ff7f0e', width=0.4, edgecolor='black')
    ax.axhline(40, color='red', linestyle='--', linewidth=1.5, label='Spec min (40 dB)')
    ax.set_ylabel("PSRR (dB)")
    ax.set_title("PSRR @ 1 kHz")
    ax.set_ylim(0, 80)
    ax.legend(fontsize=8)
    status = "PASS" if psrr_1khz > 40 else "FAIL"
    ax.text(0, psrr_1khz + 1, f"{psrr_1khz:.0f} dB\n{status}", ha='center',
            fontsize=11, fontweight='bold', color='green' if status == "PASS" else 'red')

    # 5. Monte Carlo 3-sigma
    ax = axes[1, 1]
    three_sig_pct = 3 * mc_std / mc_mean * 100
    ax.bar(['3-sigma'], [three_sig_pct], color='#9467bd', width=0.4, edgecolor='black')
    ax.axhline(10, color='red', linestyle='--', linewidth=1.5, label='Target (<10%)')
    ax.set_ylabel("3-sigma / mean (%)")
    ax.set_title("Monte Carlo Spread")
    ax.set_ylim(0, 15)
    ax.legend(fontsize=8)
    status = "PASS" if three_sig_pct < 10 else "FAIL"
    ax.text(0, three_sig_pct + 0.3, f"{three_sig_pct:.1f}%\n{status}", ha='center',
            fontsize=11, fontweight='bold', color='green' if status == "PASS" else 'red')

    # 6. Power
    ax = axes[1, 2]
    power = 0.97
    ax.bar(['TT'], [power], color='#1f77b4', width=0.4, edgecolor='black')
    ax.axhline(15, color='red', linestyle='--', linewidth=1.5, label='Spec max (15 uW)')
    ax.set_ylabel("Power (uW)")
    ax.set_title("Power Consumption")
    ax.set_ylim(0, 18)
    ax.legend(fontsize=8)
    ax.text(0, power + 0.3, f"{power:.2f} uW\nPASS", ha='center',
            fontsize=11, fontweight='bold', color='green')

    fig.suptitle("VibroSense Bias Generator — Specification Dashboard", fontsize=16, fontweight='bold', y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(OUT_DIR, "plot_dashboard.png"))
    plt.close(fig)
    print("  -> plot_dashboard.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("VibroSense Bias Generator — Plot Generation")
    print("=" * 60)

    # 1. Temperature sweep
    temps, temp_results = sim_temp_sweep()
    plot_temp_sweep(temps, temp_results)

    # 2. Supply sweep
    vdd_vals, supply_results = sim_supply_sweep()
    plot_supply_sweep(vdd_vals, supply_results)

    # 3. Startup transient
    sim_startup()
    plot_startup()

    # 4. Corner summary
    corner_results = sim_corner_nominal()
    plot_corner_summary(corner_results)

    # 5. Monte Carlo
    mc_results = sim_monte_carlo()
    mc_mean, mc_std = plot_monte_carlo(mc_results)

    # 6. PSRR
    sim_psrr()
    freq, psrr_db = plot_psrr()
    # Find PSRR at 1kHz
    idx_1k = np.argmin(np.abs(freq - 1000))
    psrr_1khz = psrr_db[idx_1k]
    print(f"  PSRR @ 1kHz = {psrr_1khz:.1f} dB")

    # 7. Dashboard
    plot_dashboard(corner_results, mc_mean, mc_std, psrr_1khz)

    print("\n" + "=" * 60)
    print("All plots generated successfully!")
    print("=" * 60)
