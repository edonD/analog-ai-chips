import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Load data - ngspice wrdata format: pairs of (time, value) columns for each signal
data = np.loadtxt('startup_data.txt')

# Extract columns: each signal has (time, value) pair
time = data[:, 0]
pvdd = data[:, 1]
gate = data[:, 3]
vref_ss = data[:, 5]
bvdd = data[:, 7]
ea_en = data[:, 9]
pass_off = data[:, 11]
mc_ea_en = data[:, 13]
ea_out = data[:, 15]

time_ms = time * 1e3

# Plot 1: Startup transient
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(time_ms, pvdd, color='blue', linewidth=2.5, label='PVDD')
ax.plot(time_ms, gate, color='red', linewidth=1.5, label='Gate')
ax.plot(time_ms, vref_ss, color='green', linewidth=1.5, linestyle='--', label='VREF_SS')

ax.set_xlabel('Time (ms)', fontsize=12)
ax.set_ylabel('Voltage (V)', fontsize=12)
ax.set_title('PVDD LDO Startup Transient \u2014 TT 27\u00b0C', fontsize=14, fontweight='bold')
ax.set_xlim(0, 20)
ax.set_ylim(0, 8)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3)
ax.tick_params(labelsize=10)

plt.tight_layout()
plt.savefig('plot_startup.png', dpi=150)
plt.close()
print("Saved plot_startup.png")

# Plot 2: Internal signal sequencing
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(time_ms, bvdd, color='black', linewidth=1.5, linestyle='--', label='BVDD')
ax.plot(time_ms, ea_en, color='orange', linewidth=1.5, label='EA_EN')
ax.plot(time_ms, pass_off, color='purple', linewidth=1.5, label='PASS_OFF')
ax.plot(time_ms, mc_ea_en, color='cyan', linewidth=1.5, label='MC_EA_EN')
ax.plot(time_ms, gate, color='red', linewidth=1.5, label='Gate')
ax.plot(time_ms, pvdd, color='blue', linewidth=2.5, label='PVDD')

ax.set_xlabel('Time (ms)', fontsize=12)
ax.set_ylabel('Voltage (V)', fontsize=12)
ax.set_title('Internal Signal Sequencing During Startup', fontsize=14, fontweight='bold')
ax.set_xlim(0, 5)
ax.set_ylim(0, 8)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3)
ax.tick_params(labelsize=10)

plt.tight_layout()
plt.savefig('plot_internal_startup.png', dpi=150)
plt.close()
print("Saved plot_internal_startup.png")
