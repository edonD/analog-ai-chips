#!/usr/bin/env python3
"""plot_all.py — Generate PNG plots for Block 01: Pass Device"""
import numpy as np
import os

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("No matplotlib — skipping plots")

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load(fname):
    """Load ngspice wrdata file."""
    try:
        return np.loadtxt(fname)
    except Exception:
        return None


if HAS_MPL:
    # ============================================================
    # 1. IdVds family curves
    # ============================================================
    fig, ax = plt.subplots(figsize=(8, 6))
    for f, label in [('idvds_vgs1', 'Vgs = -1.0V'),
                      ('idvds_vgs3', 'Vgs = -3.0V'),
                      ('idvds_vgs5p4', 'Vgs = -5.4V (full)')]:
        d = load(f)
        if d is not None and d.ndim == 2:
            vdrain = d[:, 0]
            id_ma = np.abs(d[:, 1]) * 1000
            vds_abs = 5.4 - vdrain
            ax.plot(vds_abs, id_ma, label=label)

    ax.set_xlabel('|Vds| (V)')
    ax.set_ylabel('Id (mA)')
    ax.set_title('Block 01: Pass Device — Id vs Vds Family Curves\n'
                 'W=100µm x10 parallel, L=0.5µm, TT 27°C')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5.5)
    fig.tight_layout()
    fig.savefig('idvds_family.png', dpi=150)
    plt.close()
    print('idvds_family.png')

    # ============================================================
    # 2. IdVgs at dropout
    # ============================================================
    fig, ax = plt.subplots(figsize=(8, 6))
    d = load('idvgs_dropout')
    if d is not None and d.ndim == 2:
        vgate = d[:, 1]
        vgs_abs = 5.4 - vgate
        id_ma = np.abs(d[:, 3]) if d.shape[1] > 3 else np.abs(d[:, 1])
        ax.plot(vgs_abs, id_ma, 'b-', label='TT 27°C, Vds=-0.4V')

    ax.axhline(y=50, color='r', linestyle='--', linewidth=2, label='50 mA spec')
    ax.set_xlabel('|Vgs| (V)')
    ax.set_ylabel('Id (mA)')
    ax.set_title('Block 01: Pass Device — Id vs Vgs at Dropout\n'
                 'BVDD=5.4V, PVDD=5.0V')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig('idvgs_dropout.png', dpi=150)
    plt.close()
    print('idvgs_dropout.png')

    # ============================================================
    # 3. Cgs vs frequency
    # ============================================================
    d = load('cgs_vs_freq')
    if d is not None and d.ndim == 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        freq = d[:, 1]
        cgs_pf = np.abs(d[:, -1])
        ax.semilogx(freq, cgs_pf, 'b-', linewidth=2)
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Cgs (pF)')
        ax.set_title('Block 01: Pass Device — Gate Capacitance\n'
                     'Vgs=-1V bias, TT 27°C')
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig('cgs_vs_vgs.png', dpi=150)
        plt.close()
        print('cgs_vs_vgs.png')

    # ============================================================
    # 4. gm vs Id
    # ============================================================
    d = load('gm_vs_id')
    if d is not None and d.ndim == 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        # Columns: sweep, v(gate), v(gate), id_ma, v(gate), gm_mav
        id_ma = np.abs(d[:, 3]) if d.shape[1] > 5 else np.abs(d[:, 1])
        gm = np.abs(d[:, 5]) if d.shape[1] > 5 else np.abs(d[:, 2])
        mask = id_ma > 0.1
        ax.plot(id_ma[mask], gm[mask], 'b-', linewidth=2)
        ax.axvline(x=10, color='r', linestyle='--', alpha=0.7, label='10 mA op. point')
        ax.set_xlabel('Id (mA)')
        ax.set_ylabel('gm (mA/V)')
        ax.set_title('Block 01: Pass Device — Transconductance\n'
                     'Vds=-0.4V, TT 27°C')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 90)
        fig.tight_layout()
        fig.savefig('gm_vs_id.png', dpi=150)
        plt.close()
        print('gm_vs_id.png')

    # ============================================================
    # 5. PVT bar chart
    # ============================================================
    pvt = {}
    if os.path.exists('run.log'):
        for line in open('run.log'):
            s = line.strip()
            if s.startswith('pvt_id_'):
                parts = s.split(':')
                if len(parts) == 2:
                    try:
                        pvt[parts[0].strip()] = float(parts[1].strip().split()[0])
                    except ValueError:
                        pass

    if pvt:
        fig, ax = plt.subplots(figsize=(10, 6))
        labels = []
        vals = []
        colors = []
        cm = {'tt': 'steelblue', 'ss': 'indianred', 'ff': 'seagreen'}

        for corner in ['ss', 'tt', 'ff']:
            for temp, suffix in [(-40, '_m40'), (27, '27'), (150, '150')]:
                key = f'pvt_id_{corner}{suffix}_mA'
                if key in pvt:
                    labels.append(f'{corner.upper()} {temp}°C')
                    vals.append(pvt[key])
                    colors.append(cm.get(corner, 'gray'))

        bars = ax.bar(range(len(labels)), vals, color=colors, alpha=0.8,
                      edgecolor='black')
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.axhline(y=50, color='r', linestyle='--', linewidth=2, label='50 mA spec')

        for i, v in enumerate(vals):
            ax.text(i, v + 1, f'{v:.1f}', ha='center', va='bottom', fontsize=8)

        ax.set_ylabel('Id at Dropout (mA)')
        ax.set_title('Block 01: Pass Device — PVT Corners\n'
                     'BVDD=5.4V, PVDD=5.0V, Gate=0V (full drive)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()
        fig.savefig('pvt_id_dropout.png', dpi=150)
        plt.close()
        print('pvt_id_dropout.png')

    # ============================================================
    # 6. SOA overlay
    # ============================================================
    d = load('soa_data')
    if d is not None and d.ndim == 2:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        vbvdd = d[:, 0]
        vds_abs = np.abs(d[:, 1])
        id_ma = np.abs(d[:, 3]) if d.shape[1] > 3 else np.abs(d[:, 1])
        power_mw = np.abs(d[:, 5]) if d.shape[1] > 5 else np.abs(d[:, 2])

        ax1.plot(vds_abs, id_ma, 'b-o', markersize=3, label='Operating')
        ax1.axvline(x=5.5, color='r', linestyle='--', alpha=0.5, label='Vds max = 5.5V')
        ax1.set_xlabel('|Vds| (V)')
        ax1.set_ylabel('Id (mA)')
        ax1.set_title('SOA: Id vs Vds\nBVDD sweep 5-10.5V, 150°C')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2.plot(vds_abs, power_mw, 'r-o', markersize=3)
        ax2.set_xlabel('|Vds| (V)')
        ax2.set_ylabel('Power (mW)')
        ax2.set_title('SOA: Power Dissipation\nBVDD sweep 5-10.5V, 150°C')
        ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        fig.savefig('soa_overlay.png', dpi=150)
        plt.close()
        print('soa_overlay.png')

print('Done')
