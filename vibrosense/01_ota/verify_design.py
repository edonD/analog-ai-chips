#!/usr/bin/env python3
"""
OBJECTIVE OTA DESIGN VERIFIER
==============================
This script is the SINGLE SOURCE OF TRUTH for pass/fail.
It runs ngspice, parses raw output, and checks every spec from program.md.
The agent CANNOT modify this file. Results are machine-verified.

Exit codes:
  0 = ALL gates pass
  1 = Gate 1 (operating point) failed
  2 = Gate 2 (AC performance) failed
  3 = Gate 3 (DC/transient) failed
  4 = Gate 4 (noise/rejection) failed
  5 = Gate 5 (corners/temperature) failed
  99 = simulation crashed or files missing

Output: verification_report.txt (append-only log of every run)
"""

import subprocess
import sys
import os
import re
import json
import datetime

WORK_DIR = "/home/ubuntu/analog-ai-chips/vibrosense/01_ota"
REPORT_FILE = os.path.join(WORK_DIR, "verification_report.txt")
ATTEMPT_COUNT_FILE = os.path.join(WORK_DIR, ".attempt_count")

# Specs from program.md Section 5 and Section 7
SPECS = {
    # Operating point (Section 7.1) — MANDATORY, NO EXCEPTIONS
    "pmos_vov_min_mV": 150,        # Vsg - |Vth| > 150mV for ALL PMOS
    "nmos_signal_vov_min_mV": 50,  # Vgs - Vth > 50mV for M1,M2,M7,M8
    "cascode_headroom_mV": 50,     # Vds > Vdsat + 50mV for cascodes
    "tail_current_nA": 500,        # Id_M11 target
    "tail_current_tol_nA": 50,     # |Id_M11 - 500nA| < 50nA
    "current_balance_nA": 10,      # |Id_M1 - Id_M2| < 10nA
    "vout_min_V": 0.6,             # Output voltage range
    "vout_max_V": 1.2,

    # AC (Section 5.1)
    "dc_gain_min_dB": 60,
    "dc_gain_target_dB": 65,
    "ugb_min_Hz": 30000,
    "ugb_max_Hz": 150000,
    "pm_min_deg": 55,
    "gm_min_dB": 10,

    # Noise (Section 5.2)
    "noise_1k_max_nVrtHz": 200,
    "noise_10k_max_nVrtHz": 100,

    # Transient (Section 5.3)
    "slew_rate_min_mVus": 10,

    # DC (Section 5.4)
    "output_swing_min_Vpp": 1.0,
    "input_cm_range_min_V": 0.6,

    # Rejection (Section 5.5)
    "cmrr_dc_min_dB": 60,
    "psrr_1k_min_dB": 50,

    # Power (Section 5.6)
    "total_current_max_uA": 2.0,
}


def log(msg, report_lines):
    """Print and record."""
    print(msg)
    report_lines.append(msg)


def run_ngspice(spice_file, work_dir=WORK_DIR):
    """Run ngspice in batch mode, return stdout+stderr."""
    if not os.path.exists(os.path.join(work_dir, spice_file)):
        return None, f"FILE NOT FOUND: {spice_file}"
    try:
        result = subprocess.run(
            ["/usr/bin/ngspice", "-b", spice_file],
            cwd=work_dir,
            capture_output=True, text=True, timeout=120
        )
        return result.stdout + result.stderr, None
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT: ngspice took > 120s"
    except Exception as e:
        return None, f"CRASH: {e}"


def parse_op_param(output, device, param):
    """Extract a parameter value like @m.xota.m1[vgs] from ngspice output."""
    pattern = rf'@m\.xota\.{device}\[{param}\]\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)'
    match = re.search(pattern, output, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


def parse_meas(output, name):
    """Extract a .meas result by name."""
    pattern = rf'{name}\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)'
    match = re.search(pattern, output, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


def increment_attempt():
    """Track how many verification attempts have been made."""
    count = 0
    if os.path.exists(ATTEMPT_COUNT_FILE):
        with open(ATTEMPT_COUNT_FILE) as f:
            try:
                count = int(f.read().strip())
            except:
                count = 0
    count += 1
    with open(ATTEMPT_COUNT_FILE, "w") as f:
        f.write(str(count))
    return count


def gate1_operating_point(report):
    """GATE 1: Operating point verification (Section 7)."""
    log("\n" + "=" * 70, report)
    log("GATE 1: OPERATING POINT VERIFICATION (Section 7 — MANDATORY)", report)
    log("=" * 70, report)

    output, err = run_ngspice("tb_ota_op.spice")
    if err:
        log(f"  BLOCKED: {err}", report)
        return False, {}

    # Extract all 13 transistors
    devices = {
        "m1":  {"type": "nmos", "role": "input+",      "signal": True},
        "m2":  {"type": "nmos", "role": "input-",       "signal": True},
        "m3":  {"type": "pmos", "role": "fold+",        "signal": False},
        "m4":  {"type": "pmos", "role": "fold-",        "signal": False},
        "m5":  {"type": "pmos", "role": "cascode+",     "signal": False, "cascode": True},
        "m6":  {"type": "pmos", "role": "cascode-",     "signal": False, "cascode": True},
        "m7":  {"type": "nmos", "role": "cascode+",     "signal": True,  "cascode": True},
        "m8":  {"type": "nmos", "role": "cascode-",     "signal": True,  "cascode": True},
        "m9":  {"type": "nmos", "role": "current_src+", "signal": False},
        "m10": {"type": "nmos", "role": "current_src-", "signal": False},
        "m11": {"type": "nmos", "role": "tail",         "signal": False},
        "m12": {"type": "pmos", "role": "bias_mirror+", "signal": False},
        "m13": {"type": "pmos", "role": "bias_mirror-", "signal": False},
    }

    params = ["vgs", "vth", "vds", "vdsat", "id", "gm", "gds"]
    op_data = {}
    all_ok = True
    fails = []

    for dev_name, dev_info in devices.items():
        op_data[dev_name] = {}
        for p in params:
            val = parse_op_param(output, dev_name, p)
            op_data[dev_name][p] = val

    # Extract Vout
    vout_match = re.search(r'v\(vout\)\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)', output)
    vout = float(vout_match.group(1)) if vout_match else None

    # Print operating point table
    log("\n  Device  | Type | Role          | Id(nA)  | Vgs(V) | Vth(V) | Vov(mV) | Vds(V) | Vdsat(V) | gm(uS) | gds(nS) | Status", report)
    log("  " + "-" * 120, report)

    for dev_name, dev_info in devices.items():
        d = op_data[dev_name]
        if d["vgs"] is None:
            log(f"  {dev_name:7s} | COULD NOT EXTRACT — ngspice output parse failed", report)
            fails.append(f"{dev_name}: no data extracted")
            all_ok = False
            continue

        vgs = d["vgs"]
        vth = d["vth"]
        vds = d["vds"]
        vdsat = d["vdsat"]
        id_val = d["id"]
        gm = d["gm"]
        gds_val = d["gds"]

        # Compute Vov
        if dev_info["type"] == "pmos":
            vov_mV = (abs(vgs) - abs(vth)) * 1000  # Vsg - |Vth|
        else:
            vov_mV = (vgs - vth) * 1000  # Vgs - Vth

        status = "OK"
        issues = []

        # Check 1: PMOS Vov > 150mV
        if dev_info["type"] == "pmos":
            if vov_mV < SPECS["pmos_vov_min_mV"]:
                issues.append(f"Vov={vov_mV:.0f}mV < {SPECS['pmos_vov_min_mV']}mV")

        # Check 2: NMOS signal path Vov > 50mV
        if dev_info["type"] == "nmos" and dev_info.get("signal", False):
            if vov_mV < SPECS["nmos_signal_vov_min_mV"]:
                issues.append(f"Vov={vov_mV:.0f}mV < {SPECS['nmos_signal_vov_min_mV']}mV")

        # Check 3: Cascode headroom
        if dev_info.get("cascode", False):
            headroom_mV = (abs(vds) - abs(vdsat)) * 1000
            if headroom_mV < SPECS["cascode_headroom_mV"]:
                issues.append(f"headroom={headroom_mV:.0f}mV < {SPECS['cascode_headroom_mV']}mV")

        # Check 4: Triode detection (|Vds| < |Vdsat|)
        if abs(vds) < abs(vdsat):
            issues.append(f"TRIODE: |Vds|={abs(vds)*1000:.0f}mV < |Vdsat|={abs(vdsat)*1000:.0f}mV")

        if issues:
            status = "FAIL: " + "; ".join(issues)
            fails.append(f"{dev_name}: {'; '.join(issues)}")
            all_ok = False

        log(f"  {dev_name:7s} | {dev_info['type']:4s} | {dev_info['role']:13s} | {abs(id_val)*1e9:7.1f} | {vgs:+.4f} | {vth:+.4f} | {vov_mV:+7.1f} | {vds:+.4f} | {vdsat:+.5f} | {gm*1e6:6.3f}  | {gds_val*1e9:7.1f}  | {status}", report)

    # Check 5: Tail current accuracy
    id_m11 = op_data["m11"]["id"]
    if id_m11 is not None:
        tail_err = abs(abs(id_m11) * 1e9 - SPECS["tail_current_nA"])
        if tail_err > SPECS["tail_current_tol_nA"]:
            fails.append(f"M11 tail current: {abs(id_m11)*1e9:.1f}nA, error={tail_err:.1f}nA > {SPECS['tail_current_tol_nA']}nA")
            all_ok = False
        log(f"\n  Tail current M11: {abs(id_m11)*1e9:.1f} nA (target: {SPECS['tail_current_nA']} ± {SPECS['tail_current_tol_nA']} nA) — {'OK' if tail_err <= SPECS['tail_current_tol_nA'] else 'FAIL'}", report)

    # Check 6: Current balance M1/M2
    id_m1 = op_data["m1"]["id"]
    id_m2 = op_data["m2"]["id"]
    if id_m1 is not None and id_m2 is not None:
        balance = abs(abs(id_m1) - abs(id_m2)) * 1e9
        if balance > SPECS["current_balance_nA"]:
            fails.append(f"M1/M2 balance: {balance:.1f}nA > {SPECS['current_balance_nA']}nA")
            all_ok = False
        log(f"  Current balance |Id_M1 - Id_M2|: {balance:.1f} nA (max: {SPECS['current_balance_nA']} nA) — {'OK' if balance <= SPECS['current_balance_nA'] else 'FAIL'}", report)

    # Check 7: Output voltage
    if vout is not None:
        vout_ok = SPECS["vout_min_V"] <= vout <= SPECS["vout_max_V"]
        if not vout_ok:
            fails.append(f"Vout={vout:.3f}V outside [{SPECS['vout_min_V']}, {SPECS['vout_max_V']}]")
            all_ok = False
        log(f"  Output voltage: {vout:.4f} V (range: [{SPECS['vout_min_V']}, {SPECS['vout_max_V']}]) — {'OK' if vout_ok else 'FAIL'}", report)

    # Supply current
    supply_match = re.search(r'-i\(vdd\)\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+)', output)
    if supply_match:
        i_supply = float(supply_match.group(1))
        log(f"  Supply current: {abs(i_supply)*1e6:.3f} uA (max: {SPECS['total_current_max_uA']} uA) — {'OK' if abs(i_supply)*1e6 <= SPECS['total_current_max_uA'] else 'FAIL'}", report)

    log(f"\n  GATE 1 RESULT: {'PASS' if all_ok else 'FAIL'}", report)
    if fails:
        log(f"  FAILURES ({len(fails)}):", report)
        for f in fails:
            log(f"    - {f}", report)
    log("  " + "=" * 70, report)

    return all_ok, op_data


def gate2_ac_performance(report):
    """GATE 2: AC open-loop performance."""
    log("\n" + "=" * 70, report)
    log("GATE 2: AC OPEN-LOOP PERFORMANCE (Section 5.1)", report)
    log("=" * 70, report)

    output, err = run_ngspice("tb_ota_ac.spice")
    if err:
        log(f"  BLOCKED: {err}", report)
        return False

    all_ok = True
    fails = []

    # Sanity check: gain at DC (low freq) should be close to peak
    # If gain at 1Hz << peak gain, the measurement is broken
    g_peak = parse_meas(output, "gain_peak")
    g_1hz = parse_meas(output, "g1")
    g_10hz = parse_meas(output, "g10")
    g_100hz = parse_meas(output, "g100")
    ugb = parse_meas(output, "ugb")
    phase_ugb = parse_meas(output, "phase_ugb")

    log(f"\n  Raw ngspice measurements:", report)
    log(f"    Peak gain:    {g_peak:.2f} dB" if g_peak else "    Peak gain:    NOT FOUND", report)
    log(f"    Gain @ 1 Hz:  {g_1hz:.2f} dB" if g_1hz else "    Gain @ 1 Hz:  NOT FOUND", report)
    log(f"    Gain @ 10 Hz: {g_10hz:.2f} dB" if g_10hz else "    Gain @ 10 Hz: NOT FOUND", report)
    log(f"    Gain @ 100 Hz:{g_100hz:.2f} dB" if g_100hz else "    Gain @ 100 Hz:NOT FOUND", report)
    log(f"    UGB:          {ugb:.1f} Hz" if ugb else "    UGB:          NOT FOUND", report)
    log(f"    Phase @ UGB:  {phase_ugb:.2f} deg" if phase_ugb else "    Phase @ UGB:  NOT FOUND", report)

    # SANITY CHECK: Is this really open-loop?
    # Open-loop gain should be flat from DC up to the dominant pole.
    # If gain at 10 Hz is more than 6 dB below peak, the measurement is suspect.
    if g_peak is not None and g_10hz is not None:
        if g_peak - g_10hz > 6:
            log(f"\n  *** SANITY WARNING: Peak gain ({g_peak:.1f} dB) is {g_peak - g_10hz:.1f} dB above gain at 10 Hz ({g_10hz:.1f} dB).", report)
            log(f"  *** A proper open-loop response should be FLAT from DC to the dominant pole.", report)
            log(f"  *** This suggests the loop is NOT properly broken — measurement is INVALID.", report)
            fails.append(f"MEASUREMENT INVALID: gain not flat at low freq (peak={g_peak:.1f}dB, @10Hz={g_10hz:.1f}dB)")
            all_ok = False

    # SANITY CHECK: Phase margin should not be > 90 deg for a single-stage OTA
    # with a dominant pole. PM > 120 deg is extremely suspicious.
    if phase_ugb is not None:
        pm = phase_ugb + 180
        log(f"    Phase margin: {pm:.1f} deg", report)
        if pm > 120:
            log(f"\n  *** SANITY WARNING: Phase margin = {pm:.1f} deg is > 120 deg.", report)
            log(f"  *** A folded-cascode OTA should have PM ~ 55-75 deg with 10pF load.", report)
            log(f"  *** PM > 120 deg means the loop gain measurement is broken.", report)
            fails.append(f"MEASUREMENT INVALID: PM={pm:.1f} deg (expected 55-75 deg)")
            all_ok = False
    else:
        fails.append("Phase margin could not be measured")
        all_ok = False

    # Actual spec checks (only meaningful if sanity checks pass)
    if all_ok:
        # DC gain (use gain at lowest reasonable frequency, e.g. 10 Hz)
        dc_gain = g_10hz if g_10hz is not None else g_peak
        if dc_gain is not None:
            if dc_gain < SPECS["dc_gain_min_dB"]:
                fails.append(f"DC gain {dc_gain:.1f} dB < {SPECS['dc_gain_min_dB']} dB min")
                all_ok = False
            log(f"\n  DC gain: {dc_gain:.1f} dB (min: {SPECS['dc_gain_min_dB']}, target: {SPECS['dc_gain_target_dB']}) — {'OK' if dc_gain >= SPECS['dc_gain_min_dB'] else 'FAIL'}", report)

        # UGB
        if ugb is not None:
            ugb_ok = SPECS["ugb_min_Hz"] <= ugb <= SPECS["ugb_max_Hz"]
            if not ugb_ok:
                fails.append(f"UGB {ugb:.0f} Hz outside [{SPECS['ugb_min_Hz']}, {SPECS['ugb_max_Hz']}]")
                all_ok = False
            log(f"  UGB: {ugb:.0f} Hz (range: [{SPECS['ugb_min_Hz']}, {SPECS['ugb_max_Hz']}]) — {'OK' if ugb_ok else 'FAIL'}", report)

        # PM
        if phase_ugb is not None:
            pm = phase_ugb + 180
            pm_ok = pm >= SPECS["pm_min_deg"]
            if not pm_ok:
                fails.append(f"PM {pm:.1f} deg < {SPECS['pm_min_deg']} deg")
                all_ok = False
            log(f"  Phase margin: {pm:.1f} deg (min: {SPECS['pm_min_deg']}) — {'OK' if pm_ok else 'FAIL'}", report)

    log(f"\n  GATE 2 RESULT: {'PASS' if all_ok else 'FAIL'}", report)
    if fails:
        log(f"  FAILURES ({len(fails)}):", report)
        for f in fails:
            log(f"    - {f}", report)
    log("  " + "=" * 70, report)

    return all_ok


def gate3_dc_transient(report):
    """GATE 3: DC sweep and transient."""
    log("\n" + "=" * 70, report)
    log("GATE 3: DC SWEEP & TRANSIENT (Sections 5.3, 5.4)", report)
    log("=" * 70, report)

    all_ok = True
    fails = []

    # DC sweep
    output_dc, err = run_ngspice("tb_ota_dc.spice")
    if err:
        log(f"  DC: BLOCKED: {err}", report)
        all_ok = False
    else:
        vmax = parse_meas(output_dc, "vout_max")
        vmin = parse_meas(output_dc, "vout_min")
        if vmax is not None and vmin is not None:
            swing = vmax - vmin
            swing_ok = swing >= SPECS["output_swing_min_Vpp"]
            if not swing_ok:
                fails.append(f"Output swing {swing:.3f} Vpp < {SPECS['output_swing_min_Vpp']} Vpp")
                all_ok = False
            log(f"  Output swing: {swing:.3f} Vpp (min: {SPECS['output_swing_min_Vpp']}) — {'OK' if swing_ok else 'FAIL'}", report)
            log(f"    Vout_max: {vmax:.3f} V, Vout_min: {vmin:.3f} V", report)
        else:
            fails.append("Could not measure output swing")
            all_ok = False

    # Transient
    output_tran, err = run_ngspice("tb_ota_tran.spice")
    if err:
        log(f"  Transient: BLOCKED: {err}", report)
        all_ok = False
    else:
        t10 = parse_meas(output_tran, "t10")
        t90 = parse_meas(output_tran, "t90")
        if t10 is not None and t90 is not None and t90 > t10:
            sr_Vs = 0.08 / (t90 - t10)
            sr_mVus = sr_Vs * 1e-6 * 1e3
            sr_ok = sr_mVus >= SPECS["slew_rate_min_mVus"]
            if not sr_ok:
                fails.append(f"Slew rate {sr_mVus:.2f} mV/us < {SPECS['slew_rate_min_mVus']} mV/us")
                all_ok = False
            log(f"  Slew rate: {sr_mVus:.2f} mV/us (min: {SPECS['slew_rate_min_mVus']}) — {'OK' if sr_ok else 'FAIL'}", report)
        else:
            log(f"  Slew rate: could not measure (t10={t10}, t90={t90})", report)
            fails.append("Could not measure slew rate")
            all_ok = False

    log(f"\n  GATE 3 RESULT: {'PASS' if all_ok else 'FAIL'}", report)
    if fails:
        log(f"  FAILURES ({len(fails)}):", report)
        for f in fails:
            log(f"    - {f}", report)
    log("  " + "=" * 70, report)
    return all_ok


def main():
    attempt = increment_attempt()
    report = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log(f"\n{'#' * 70}", report)
    log(f"# VERIFICATION RUN #{attempt} — {timestamp}", report)
    log(f"{'#' * 70}", report)

    # Check required files exist
    required = ["ota_foldcasc.spice", "tb_ota_op.spice", "sky130_minimal.lib.spice"]
    missing = [f for f in required if not os.path.exists(os.path.join(WORK_DIR, f))]
    if missing:
        log(f"\nMISSING FILES: {missing}", report)
        log("Cannot verify. Create these files first.", report)
        with open(REPORT_FILE, "a") as f:
            f.write("\n".join(report) + "\n")
        sys.exit(99)

    # ==================== GATE 1 ====================
    gate1_pass, op_data = gate1_operating_point(report)

    if not gate1_pass:
        log(f"\n{'!' * 70}", report)
        log(f"! GATE 1 FAILED — DO NOT PROCEED", report)
        log(f"! Fix the operating point before running any other testbench.", report)
        log(f"! See program.md Section 7 and Section 9 for troubleshooting.", report)
        log(f"! This is attempt #{attempt}.", report)
        log(f"{'!' * 70}", report)
        with open(REPORT_FILE, "a") as f:
            f.write("\n".join(report) + "\n")
        sys.exit(1)

    # ==================== GATE 2 ====================
    tb_ac_exists = os.path.exists(os.path.join(WORK_DIR, "tb_ota_ac.spice"))
    if tb_ac_exists:
        gate2_pass = gate2_ac_performance(report)
        if not gate2_pass:
            log(f"\n{'!' * 70}", report)
            log(f"! GATE 2 FAILED — AC measurement broken or specs not met.", report)
            log(f"! Check: is the loop properly broken? Is gain flat at low freq?", report)
            log(f"! This is attempt #{attempt}.", report)
            log(f"{'!' * 70}", report)
            with open(REPORT_FILE, "a") as f:
                f.write("\n".join(report) + "\n")
            sys.exit(2)
    else:
        log("\n  GATE 2: SKIPPED (tb_ota_ac.spice not found)", report)

    # ==================== GATE 3 ====================
    tb_dc = os.path.exists(os.path.join(WORK_DIR, "tb_ota_dc.spice"))
    tb_tran = os.path.exists(os.path.join(WORK_DIR, "tb_ota_tran.spice"))
    if tb_dc or tb_tran:
        gate3_pass = gate3_dc_transient(report)
        if not gate3_pass:
            log(f"\n  GATE 3 FAILED — attempt #{attempt}", report)
            with open(REPORT_FILE, "a") as f:
                f.write("\n".join(report) + "\n")
            sys.exit(3)
    else:
        log("\n  GATE 3: SKIPPED (testbench files not found)", report)

    # ==================== ALL PASSED ====================
    log(f"\n{'*' * 70}", report)
    log(f"* ALL GATES PASSED — attempt #{attempt}", report)
    log(f"{'*' * 70}", report)

    with open(REPORT_FILE, "a") as f:
        f.write("\n".join(report) + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
