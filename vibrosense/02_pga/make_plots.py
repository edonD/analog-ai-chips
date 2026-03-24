#!/usr/bin/env python3
"""Final PGA verification plots from pre-generated ngspice data."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

colors = {'1x': '#1f77b4', '4x': '#ff7f0e', '16x': '#2ca02c', '64x': '#d62728'}
expected = {'1x': 0, '4x': 12.04, '16x': 24.08, '64x': 36.12}

# Load AC data
ac = {}
for g in ['1x', '4x', '16x', '64x']:
    d = np.loadtxt(f'plotdata_ac_{g}.csv')
    ac[g] = (d[:, 0], d[:, 1])  # freq, gain_dB (col2=imaginary=0)
    print(f"AC {g}: {len(d)} pts, midband(1kHz)={d[np.argmin(np.abs(d[:,0]-1000)),1]:.2f} dB")

# Load transient data
tran = {}
for sig in ['vout', 'vin', 'inn']:
    d = np.loadtxt(f'plotdata_tran_{sig}.csv')
    tran[sig] = (d[:, 0] * 1000, d[:, 1])  # time(ms), voltage
    print(f"Tran {sig}: range [{d[:,1].min():.4f}, {d[:,1].max():.4f}] V")

# ============================================================
# PLOT 1: AC Magnitude — All gains
# ============================================================
fig1, ax1 = plt.subplots(figsize=(10, 5.5))
for g in ['1x', '4x', '16x', '64x']:
    f, gdb = ac[g]
    idx_1k = np.argmin(np.abs(f - 1000))
    mid = gdb[idx_1k]
    ax1.semilogx(f, gdb, color=colors[g], linewidth=2,
                 label=f'{g}: {mid:.2f} dB (target {expected[g]:.1f})')

ax1.axvline(25000, color='gray', ls=':', alpha=0.5)
ax1.axvline(6000, color='gray', ls=':', alpha=0.3)
ax1.annotate('25 kHz\n(BW spec)', xy=(27000, -43), fontsize=8, color='gray')
ax1.set_ylabel('Gain (dB)', fontsize=12)
ax1.set_xlabel('Frequency (Hz)', fontsize=12)
ax1.set_ylim(-50, 42)
ax1.set_xlim(1, 1e8)
ax1.set_title('PGA AC Response — Real OTA (ota_pga_v2, SKY130A TT 27°C)',
              fontsize=13, fontweight='bold')
ax1.grid(True, which='both', alpha=0.3)
ax1.legend(loc='lower left', fontsize=10, framealpha=0.9)
plt.tight_layout()
plt.savefig('plot_ac_all_gains.png', dpi=150)
print("Saved: plot_ac_all_gains.png")

# ============================================================
# PLOT 2: Transient — input vs output + virtual ground error
# ============================================================
fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]})
fig2.suptitle('PGA Transient — 1x Gain, 1 kHz 500 mVpk Input (Real OTA)',
              fontsize=13, fontweight='bold')

t = tran['vout'][0]
ax2.plot(t, tran['vin'][1], 'b-', lw=1.2, alpha=0.5, label='V(in)')
ax2.plot(t, tran['vout'][1], 'r-', lw=1.8, label='V(out)')
ax2.axhline(0.9, color='gray', ls='--', alpha=0.3)
ax2.set_ylabel('Voltage (V)', fontsize=11)
ax2.set_ylim(0.2, 1.6)
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)

vinn_err = (tran['inn'][1] - 0.9) * 1e6  # uV
ax3.plot(t, vinn_err, 'g-', lw=1)
ax3.set_ylabel('V(inn) error (uV)', fontsize=10)
ax3.set_xlabel('Time (ms)', fontsize=11)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plot_transient_1x.png', dpi=150)
print("Saved: plot_transient_1x.png")

# ============================================================
# PLOT 3: Gain accuracy + BW summary
# ============================================================
fig3, (ax4, ax5) = plt.subplots(1, 2, figsize=(12, 4.5))

# Gain error bars
labels = list(expected.keys())
errors = []
bws = []
for g in labels:
    f, gdb = ac[g]
    idx = np.argmin(np.abs(f - 1000))
    mid = gdb[idx]
    errors.append(mid - expected[g])
    target = mid - 3
    bw_idx = np.where(gdb[idx:] < target)[0]
    bws.append(f[idx + bw_idx[0]] / 1000 if len(bw_idx) > 0 else f[-1] / 1000)

x = np.arange(len(labels))
bars = ax4.bar(x, errors, 0.5, color=[colors[g] for g in labels], alpha=0.8)
ax4.axhline(0.5, color='red', ls='--', alpha=0.5)
ax4.axhline(-0.5, color='red', ls='--', alpha=0.5)
ax4.axhline(0, color='black', lw=0.5)
ax4.fill_between([-0.5, 3.5], -0.5, 0.5, alpha=0.05, color='green')
ax4.set_xticks(x)
ax4.set_xticklabels(labels, fontsize=11)
ax4.set_ylabel('Gain Error (dB)', fontsize=11)
ax4.set_ylim(-0.6, 0.6)
ax4.set_title('Gain Accuracy (spec: ±0.5 dB)', fontsize=12)
ax4.grid(True, axis='y', alpha=0.3)
for i, e in enumerate(errors):
    ax4.annotate(f'{e:+.3f}', xy=(i, e), xytext=(0, 8 if e >= 0 else -15),
                 textcoords='offset points', ha='center', fontsize=9)

# Bandwidth bars
bw_specs = [25, 25, 25, 6]
bar_colors = ['green' if bws[i] > bw_specs[i] else 'red' for i in range(4)]
ax5.bar(x, bws, 0.5, color=bar_colors, alpha=0.6)
for i, spec in enumerate(bw_specs):
    ax5.plot([i-0.3, i+0.3], [spec, spec], 'r-', lw=2)
ax5.set_xticks(x)
ax5.set_xticklabels(labels, fontsize=11)
ax5.set_ylabel('Bandwidth (kHz)', fontsize=11)
ax5.set_title('-3dB Bandwidth (red line = spec)', fontsize=12)
ax5.grid(True, axis='y', alpha=0.3)
ax5.set_yscale('log')
for i, bw in enumerate(bws):
    ax5.annotate(f'{bw:.0f}k', xy=(i, bw), xytext=(0, 8),
                 textcoords='offset points', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('plot_gain_accuracy.png', dpi=150)
print("Saved: plot_gain_accuracy.png")

print("\nDone.")
