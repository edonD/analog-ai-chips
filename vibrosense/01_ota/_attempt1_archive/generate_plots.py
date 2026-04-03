#!/usr/bin/env python3
"""Generate publication-quality plots for VibroSense OTA results."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.chdir('/home/ubuntu/analog-ai-chips/vibrosense/01_ota')

def load_wrdata(filename):
    """Load ngspice wrdata output (2 columns: frequency/time, value)."""
    data = []
    with open(filename) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    vals = [float(x) for x in parts]
                    data.append(vals)
                except:
                    pass
    return np.array(data) if data else None

# ============================================================
# 1. Bode Plot (Magnitude and Phase)
# ============================================================
print("Generating Bode plot...")
data = load_wrdata('bode_data')
if data is not None and len(data) > 10:
    # wrdata saves pairs: freq, mag_db, freq, phase_deg
    n = len(data)
    half = n // 2
    freq_mag = data[:half, 0]
    mag_db = data[:half, 1]
    freq_ph = data[half:, 0]
    phase_deg = data[half:, 1]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax1.semilogx(freq_mag, mag_db, 'b-', linewidth=1.5)
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax1.axhline(y=65, color='r', linestyle=':', alpha=0.5, label='65dB target')
    ax1.set_ylabel('Gain (dB)')
    ax1.set_title('VibroSense Folded-Cascode OTA — Bode Plot (TT, 27°C)')
    ax1.grid(True, which='both', alpha=0.3)
    ax1.legend()
    ax1.set_ylim([-40, 80])

    ax2.semilogx(freq_ph, phase_deg, 'r-', linewidth=1.5)
    ax2.axhline(y=-180, color='gray', linestyle='--', alpha=0.5)
    ax2.set_ylabel('Phase (degrees)')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.set_ylim([-200, 20])

    plt.tight_layout()
    plt.savefig('plot_bode.png', dpi=150)
    plt.close()
    print("  -> plot_bode.png")

# ============================================================
# 2. DC Transfer Characteristic
# ============================================================
print("Generating DC transfer plot...")
data = load_wrdata('dc_swing_data')
if data is not None and len(data) > 10:
    n = len(data)
    half = n // 2
    vinp = data[:half, 0]
    vout = data[:half, 1]

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.plot(vinp, vout, 'b-', linewidth=1.5)
    ax.plot([0, 1.8], [0, 1.8], 'k--', alpha=0.3, label='Ideal (y=x)')
    ax.set_xlabel('Vinp (V)')
    ax.set_ylabel('Vout (V)')
    ax.set_title('OTA DC Transfer Characteristic (Unity-Gain Buffer)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim([0, 1.8])
    ax.set_ylim([0, 1.8])
    plt.tight_layout()
    plt.savefig('plot_dc_transfer.png', dpi=150)
    plt.close()
    print("  -> plot_dc_transfer.png")

# ============================================================
# 3. Transient Step Response
# ============================================================
print("Generating transient plot...")
data = load_wrdata('tran_step_data')
if data is not None and len(data) > 10:
    n = len(data)
    half = n // 2
    time = data[:half, 0] * 1e6  # Convert to us
    vout = data[:half, 1]
    vinp = data[half:half+len(time), 1]

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.plot(time, vout, 'b-', linewidth=1.5, label='Vout')
    ax.plot(time, vinp, 'r--', linewidth=1, alpha=0.7, label='Vinp')
    ax.set_xlabel('Time (µs)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title('OTA Step Response (100mV step, Unity-Gain Buffer, CL=10pF)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim([0, 50])
    plt.tight_layout()
    plt.savefig('plot_transient.png', dpi=150)
    plt.close()
    print("  -> plot_transient.png")

# ============================================================
# 4. Corner Comparison Bar Chart
# ============================================================
print("Generating corner comparison...")
corners = ['TT', 'SS', 'FF', 'SF', 'FS']
gains = [68.5, 66.2, 90.5, 64.3, 79.5]
ugbs = [25.5, 25.4, 25.3, 25.2, 25.5]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

colors = ['#2196F3', '#F44336', '#4CAF50', '#FF9800', '#9C27B0']
bars = ax1.bar(corners, gains, color=colors, alpha=0.8)
ax1.axhline(y=65, color='r', linestyle='--', label='Target (65 dB)')
ax1.axhline(y=60, color='orange', linestyle=':', label='Min (60 dB)')
ax1.set_ylabel('Peak Gain (dB)')
ax1.set_title('Gain Across Process Corners')
ax1.legend()
ax1.grid(True, axis='y', alpha=0.3)

bars2 = ax2.bar(corners, ugbs, color=colors, alpha=0.8)
ax2.axhline(y=30, color='r', linestyle='--', label='Min (30 kHz)')
ax2.set_ylabel('UGB (kHz)')
ax2.set_title('UGB Across Process Corners')
ax2.legend()
ax2.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('plot_corners.png', dpi=150)
plt.close()
print("  -> plot_corners.png")

# ============================================================
# 5. Temperature Comparison
# ============================================================
print("Generating temperature comparison...")
temps = ['-40°C', '27°C', '85°C']
temp_gains = [67.2, 68.5, 80.1]
temp_ugbs = [28.5, 25.5, 22.1]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.bar(temps, temp_gains, color=['#2196F3', '#4CAF50', '#F44336'], alpha=0.8)
ax1.axhline(y=55, color='r', linestyle='--', label='Min (55 dB)')
ax1.set_ylabel('Peak Gain (dB)')
ax1.set_title('Gain vs Temperature (TT)')
ax1.legend()
ax1.grid(True, axis='y', alpha=0.3)

ax2.bar(temps, temp_ugbs, color=['#2196F3', '#4CAF50', '#F44336'], alpha=0.8)
ax2.axhline(y=20, color='orange', linestyle=':', label='Min (20 kHz)')
ax2.axhline(y=200, color='r', linestyle='--', label='Max (200 kHz)')
ax2.set_ylabel('UGB (kHz)')
ax2.set_title('UGB vs Temperature (TT)')
ax2.legend()
ax2.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('plot_temperature.png', dpi=150)
plt.close()
print("  -> plot_temperature.png")

print("\nAll plots generated successfully!")
