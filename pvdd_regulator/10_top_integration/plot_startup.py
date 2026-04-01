#!/usr/bin/env python3
"""Plot 2: Startup Transient — PVDD, gate, vref_ss vs time"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

pvdd_data = np.loadtxt('plot2_pvdd.dat')
gate_data = np.loadtxt('plot2_gate.dat')
vref_data = np.loadtxt('plot2_vref.dat')

time_ms = pvdd_data[:, 0] * 1e3  # s -> ms
pvdd = pvdd_data[:, 1]
gate = gate_data[:, 1]
vref_ss = vref_data[:, 1]

fig, ax = plt.subplots(figsize=(8, 4.5))

ax.plot(time_ms, pvdd, 'b-', linewidth=2.0, label='PVDD')
ax.plot(time_ms, gate, 'r-', linewidth=1.2, label='Gate')
ax.plot(time_ms, vref_ss, 'g--', linewidth=1.2, label='Vref_SS')

ax.set_xlabel('Time (ms)', fontsize=11)
ax.set_ylabel('Voltage (V)', fontsize=11)
ax.set_title('Startup Transient (BVDD 0\u21927V in 10\u00b5s, Rload=5k\u03a9)',
             fontsize=12, fontweight='bold')
ax.set_xlim(0, 20)
ax.legend(fontsize=10, loc='right')
ax.tick_params(axis='both', which='major', labelsize=10)

plt.tight_layout()
plt.savefig('plot_startup.png', dpi=150, bbox_inches='tight')
print('Saved plot_startup.png')
