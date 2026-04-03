#!/usr/bin/env python3
"""VibroSense Block 04: Envelope Detector v2 — Verification Suite
Runs amplitude sweep, 5-corner analysis, ripple, and power tests.
Outputs results_summary.json."""

import subprocess, json, re, os, math

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SPICE_TEMPLATE = """* TB: Envelope Detector v2 — {test_name}
.option scale=1e-6
.lib "sky130_minimal_v2.lib.spice" {corner}
.include "ota_pga_v2.spice"
.include "envelope_det.spice"

.param vdd_val = 1.8
.param vcm_val = 0.9
.param amp_val = {amp}
.param freq_val = {freq}

Vdd vdd 0 dc {{vdd_val}}
Ibias_n vdd vbn dc {ibias_n}
Xbias_n vbn vbn 0 0 sky130_fd_pr__nfet_01v8 w=11.4 l=14 nf=1
Cbn vbn 0 100p
Ibias_lpf vdd vbn_lpf dc 100n
Xbias_lpf vbn_lpf vbn_lpf 0 0 sky130_fd_pr__nfet_01v8 w=1 l=8 nf=1
Cbn_lpf vbn_lpf 0 100p

Vin vin 0 sin({{vcm_val}} {{amp_val}} {{freq_val}})
Vcm vcm 0 dc {{vcm_val}}
Xenv vin vcm vout vdd 0 vbn vbn_lpf envelope_det

.tran 1u {tran_stop}

.control
run
meas tran vout_avg AVG v(vout) from={meas_from} to={meas_to}
meas tran vout_min MIN v(vout) from={meas_from} to={meas_to}
meas tran vout_max MAX v(vout) from={meas_from} to={meas_to}
meas tran rect_avg AVG v(xenv.rect) from={meas_from} to={meas_to}
meas tran rect_min MIN v(xenv.rect) from={meas_from} to={meas_to}
meas tran rect_max MAX v(xenv.rect) from={meas_from} to={meas_to}
meas tran idd AVG i(Vdd) from={meas_from} to={meas_to}
let pwr = -idd * 1.8 * 1e6
echo "RESULT vout_avg=$&vout_avg rect_avg=$&rect_avg rect_min=$&rect_min rect_max=$&rect_max vout_min=$&vout_min vout_max=$&vout_max power_uw=$&pwr"
quit
.endc
.end
"""

def run_sim(test_name, corner="tt", amp="50m", freq="3162", ibias_n="1500n",
            tran_stop="500m", meas_from="400m", meas_to="500m"):
    spice = SPICE_TEMPLATE.format(
        test_name=test_name, corner=corner, amp=amp, freq=freq,
        ibias_n=ibias_n, tran_stop=tran_stop, meas_from=meas_from, meas_to=meas_to)
    fname = f"tb_auto_{test_name.replace(' ','_').replace('/','_')}.spice"
    with open(fname, 'w') as f:
        f.write(spice)
    try:
        r = subprocess.run(["ngspice", "-b", fname], capture_output=True, text=True, timeout=300)
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {test_name}")
        return None
    m = re.search(r'RESULT (.+)', out)
    if not m:
        print(f"  WARN: no RESULT from {test_name}")
        return None
    pairs = re.findall(r'(\w+)=([\d.eE+\-]+)', m.group(1))
    return {k: float(v) for k, v in pairs}

results = {}

# 1. Amplitude sweep
print("=== AMPLITUDE SWEEP (TT, 3162Hz) ===")
amps = [("2.5m", 5), ("5m", 10), ("10m", 20), ("25m", 50),
        ("50m", 100), ("100m", 200), ("250m", 500)]
for amp_str, vpp in amps:
    A = vpp / 2000.0
    expected = A / math.pi * 1000
    r = run_sim(f"amp_{vpp}mVpp", amp=amp_str)
    if r:
        delta = (r['vout_avg'] - 0.9) * 1000
        rect_delta = (r['rect_avg'] - 0.9) * 1000
        err = (rect_delta - expected) / expected * 100 if expected > 0.01 else None
        spec = 5 if vpp >= 100 else 15
        status = "PASS" if err is not None and abs(err) <= spec else "FAIL"
        print(f"  {vpp:4d}mVpp: rect_delta={rect_delta:7.2f}mV  expected={expected:7.2f}mV  "
              f"err={err:+.1f}%  vout={delta:7.2f}mV  {status}" if err else
              f"  {vpp:4d}mVpp: rect_delta={rect_delta:7.2f}mV  vout={delta:7.2f}mV")
        results[f"accuracy_{vpp}mVpp"] = {
            "vout_delta_mV": round(delta, 3), "rect_delta_mV": round(rect_delta, 3),
            "expected_mV": round(expected, 3), "rect_error_pct": round(err, 1) if err else None,
            "spec_pct": spec, "status": status}

# 2. Power
print("\n=== POWER ===")
r = run_sim("power", amp="50m")
if r:
    pwr = r.get('power_uw', 0)
    status = "PASS" if pwr <= 10 else "MARGINAL" if pwr <= 12 else "FAIL"
    print(f"  Power = {pwr:.2f} uW  (spec: <10 uW)  {status}")
    results["power_uw"] = {"value": round(pwr, 2), "spec": 10, "status": status}

# 3. Five corners
print("\n=== 5-CORNER (100mVpp @ 3162Hz) ===")
for corner in ["tt", "ss", "ff", "sf", "fs"]:
    r = run_sim(f"corner_{corner}", corner=corner, amp="50m")
    if r:
        delta = (r['vout_avg'] - 0.9) * 1000
        rect_delta = (r['rect_avg'] - 0.9) * 1000
        pwr = r.get('power_uw', 0)
        print(f"  {corner.upper()}: rect_delta={rect_delta:.2f}mV  vout={delta:.2f}mV  power={pwr:.1f}uW")
        results[f"corner_{corner}"] = {
            "rect_delta_mV": round(rect_delta, 3), "vout_delta_mV": round(delta, 3),
            "power_uw": round(pwr, 2)}

# 4. Ripple
print("\n=== RIPPLE ===")
r = run_sim("ripple", amp="50m", freq="3162")
if r:
    vout_pp = (r['vout_max'] - r['vout_min']) * 1000
    vout_dc = (r['vout_avg'] - 0.9) * 1000
    ripple = vout_pp / max(vout_dc, 0.001) * 100
    status = "PASS" if ripple <= 5 else "FAIL"
    print(f"  Vout_pp={vout_pp:.3f}mV  DC={vout_dc:.2f}mV  Ripple={ripple:.1f}%  {status}")
    results["ripple_3162Hz"] = {"ripple_pct": round(ripple, 1), "status": status}

# Save
with open("results_summary.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n=== SUMMARY ===")
for k, v in results.items():
    if "status" in v:
        print(f"  {k:30s}: {v['status']}")
print("\nDone. Results in results_summary.json")
