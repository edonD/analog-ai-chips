#!/usr/bin/env python3
"""parse_pvdd_impact.py — Compute pvdd_impact_mV from with/without limiter data.

Reads wrdata output from tb_ilim_normal.spice (with limiter) and
tb_ilim_normal_nolim.spice (without limiter).

wrdata format: 4 columns per line: Vg_drive, i(Vpvdd), Vg_drive(dup), v(gate_int)

Approach (gate_int-level comparison — what the pass device actually sees):
  1. From no-limiter data, find gate_int voltage that gives 50mA
  2. From with-limiter data, find the current at that same gate_int voltage
  3. delta_mA = |I_with - I_without| at the same gate_int
  4. Convert to mV: pvdd_impact_mV = delta_mA * (Vpvdd/Iload) = delta_mA * 100

This measures the intrinsic impact of the limiter subcircuit on the pass device
current, isolated from the gate driver impedance. In the real LDO, the error amp
loop maintains gate_int at the required voltage through feedback.

Also reports the open-loop impact (at same Vg_drive through 10k Rgate) for
documentation — this shows the gate loading effect that the error amp must reject.
"""
import sys
import numpy as np

def read_wrdata(filename):
    """Read ngspice wrdata file. Returns (vg_drive, current, gate_int) arrays."""
    data = np.loadtxt(filename)
    if data.ndim == 1:
        return None, None, None
    vg_drive = data[:, 0]
    current = data[:, 1]
    gate_int = data[:, 3] if data.shape[1] >= 4 else data[:, 0]
    return vg_drive, current, gate_int

def find_crossing(x, y, target):
    """Find x value where y crosses target via linear interpolation."""
    for j in range(len(y) - 1):
        if (y[j] - target) * (y[j+1] - target) <= 0:
            if abs(y[j+1] - y[j]) < 1e-20:
                return x[j]
            frac = (target - y[j]) / (y[j+1] - y[j])
            return x[j] + frac * (x[j+1] - x[j])
    return None

def main():
    try:
        vg_with, i_with, gi_with = read_wrdata('ilim_normal_with_data')
        vg_nolim, i_nolim, gi_nolim = read_wrdata('ilim_normal_nolim_data')
    except Exception as e:
        print("pvdd_impact_mV: UNMEASURED", flush=True)
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(0)

    if vg_with is None or vg_nolim is None:
        print("pvdd_impact_mV: UNMEASURED", flush=True)
        sys.exit(0)

    target_A = 0.05  # 50mA

    # --- Gate_int level comparison (intrinsic limiter impact) ---
    # Sort by gate_int for interpolation
    idx_n = np.argsort(gi_nolim)
    gi_50_nolim = find_crossing(gi_nolim[idx_n], i_nolim[idx_n], target_A)

    if gi_50_nolim is None:
        print("pvdd_impact_mV: UNMEASURED", flush=True)
        print("ERROR: Could not find 50mA crossing in no-limiter data", file=sys.stderr)
        sys.exit(0)

    # At the same gate_int voltage, find current with limiter
    idx_w = np.argsort(gi_with)
    i_with_at_gi = np.interp(gi_50_nolim, gi_with[idx_w], i_with[idx_w])

    delta_mA = abs(i_with_at_gi - target_A) * 1000
    pvdd_impact_mV = delta_mA * 100.0  # Rload_eff = 100 ohm

    print(f"pvdd_impact_mV: {pvdd_impact_mV:.6g}", flush=True)
    print(f"  (gate_int_ref={gi_50_nolim:.5f}V, I_with={i_with_at_gi*1000:.4f}mA, "
          f"I_without={target_A*1000:.1f}mA, delta={delta_mA:.6f}mA)", flush=True)

    # --- Also report open-loop impact (at same Vg_drive) ---
    idx_n2 = np.argsort(vg_nolim)
    vg_50_nolim = find_crossing(vg_nolim[idx_n2], i_nolim[idx_n2], target_A)
    if vg_50_nolim is not None:
        idx_w2 = np.argsort(vg_with)
        i_w_ol = np.interp(vg_50_nolim, vg_with[idx_w2], i_with[idx_w2])
        ol_delta_mA = abs(i_w_ol - target_A) * 1000
        ol_impact_mV = ol_delta_mA * 100.0
        print(f"  open_loop_impact_mV: {ol_impact_mV:.1f} "
              f"(at Vg_drive={vg_50_nolim:.4f}V through 10k Rgate)", flush=True)
        print(f"  NOTE: open_loop impact = {ol_impact_mV:.0f}mV is the gate loading "
              f"effect through Rgate that the error amp feedback rejects", flush=True)

if __name__ == '__main__':
    main()
