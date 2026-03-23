#!/usr/bin/env python3
"""
PGA OTA v2 DESIGN VERIFIER (Two-Stage Miller)
================================================
5-gate sequential verification for the two-stage Miller OTA.

Exit codes:
  0 = ALL gates pass
  1 = Gate 1 (operating point) failed
  2 = Gate 2 (AC performance) failed
  3 = Gate 3 (DC/transient) failed
  4 = Gate 4 (rejection) failed
  5 = Gate 5 (corners/temperature) failed
  99 = simulation crashed or files missing
"""

import subprocess
import sys
import os
import re
import datetime

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_FILE = os.path.join(WORK_DIR, "verification_report_pga_v2.txt")
ATTEMPT_COUNT_FILE = os.path.join(WORK_DIR, ".attempt_count")

# ── PGA OTA v2 Specs (from program.md Section 8) ──
SPECS = {
    # Gate 1 — Operating point
    "vov_min_mV": 100,
    "tail_current_nA": 1500,
    "tail_current_tol_pct": 15,
    "id_stage2_min_nA": 2500,
    "id_stage2_max_nA": 5000,
    "vout_min_V": 0.6,
    "vout_max_V": 1.2,
    "total_current_max_uA": 6.5,  # stage1 + stage2

    # Gate 2 — AC
    "dc_gain_min_dB": 65,
    "ugb_min_Hz": 400_000,
    "ugb_max_Hz": 2_000_000,
    "pm_min_deg": 60,

    # Gate 3 — Transient
    "slew_rate_min_mVus": 50,
    "output_swing_min_Vpp": 1.0,

    # Gate 4 — Rejection
    "cmrr_dc_min_dB": 70,
    "psrr_1k_min_dB": 50,

    # Gate 5 — Corners
    "corner_gain_min_dB": 55,
    "corner_ugb_min_Hz": 250_000,
    "corner_ugb_max_Hz": 3_000_000,
    "corner_pm_min_deg": 55,
    "temp_gain_min_dB": 55,
    "temp_ugb_min_Hz": 250_000,
    "temp_ugb_max_Hz": 3_000_000,
}


def log(msg, report):
    print(msg)
    report.append(msg)


def run_ngspice(spice_file, work_dir=WORK_DIR):
    path = os.path.join(work_dir, spice_file)
    if not os.path.exists(path):
        return None, f"FILE NOT FOUND: {spice_file}"
    try:
        result = subprocess.run(
            ["/usr/bin/ngspice", "-b", spice_file],
            cwd=work_dir,
            capture_output=True, text=True, timeout=300
        )
        return result.stdout + result.stderr, None
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT: ngspice took > 300s"
    except Exception as e:
        return None, f"CRASH: {e}"


def parse_op_param(output, device, param):
    pattern = rf'@m\.xota\.{device}\[{param}\]\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)'
    match = re.search(pattern, output, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


def parse_meas(output, name):
    pattern = rf'{name}\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)'
    match = re.search(pattern, output, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


def increment_attempt():
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
    """GATE 1: Operating point verification for two-stage Miller OTA."""
    log("\n" + "=" * 70, report)
    log("GATE 1: OPERATING POINT VERIFICATION", report)
    log("=" * 70, report)

    output, err = run_ngspice("tb_pga_v2_op.spice")
    if err:
        log(f"  BLOCKED: {err}", report)
        return False, {}

    # Two-stage OTA has 7 devices: M1, M2, M3, M4, M5, M7, M11
    devices = {
        "m1":  {"type": "nmos", "role": "input+"},
        "m2":  {"type": "nmos", "role": "input-"},
        "m3":  {"type": "pmos", "role": "mirror_diode"},
        "m4":  {"type": "pmos", "role": "mirror_out"},
        "m5":  {"type": "pmos", "role": "stage2_cs"},
        "m7":  {"type": "nmos", "role": "stage2_sink"},
        "m11": {"type": "nmos", "role": "tail"},
    }

    params = ["vgs", "vth", "vds", "vdsat", "id", "gm", "gds"]
    op_data = {}
    all_ok = True
    fails = []

    for dev_name in devices:
        op_data[dev_name] = {}
        for p in params:
            val = parse_op_param(output, dev_name, p)
            op_data[dev_name][p] = val

    # Extract Vout and v_s1
    vout_match = re.search(r'v\(out\)\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)', output)
    vout = float(vout_match.group(1)) if vout_match else None
    vs1_match = re.search(r'v\(xota\.v_s1\)\s*=\s*([+-]?\d+\.?\d*[eE][+-]?\d+|[+-]?\d+\.?\d*)', output)
    vs1 = float(vs1_match.group(1)) if vs1_match else None

    # Print operating point table
    log("\n  Device  | Type | Role          | Id(nA)  | Vgs(V) | Vth(V) | Vov(mV) | Vds(V) | Vdsat(V) | gm(uS) | gds(nS) | Status", report)
    log("  " + "-" * 120, report)

    for dev_name, dev_info in devices.items():
        d = op_data[dev_name]
        if d["vgs"] is None:
            log(f"  {dev_name:7s} | COULD NOT EXTRACT", report)
            fails.append(f"{dev_name}: no data")
            all_ok = False
            continue

        vgs = d["vgs"]
        vth = d["vth"]
        vds = d["vds"]
        vdsat = d["vdsat"]
        id_val = d["id"]
        gm = d["gm"]
        gds_val = d["gds"]

        if dev_info["type"] == "pmos":
            vov_mV = (abs(vgs) - abs(vth)) * 1000
        else:
            vov_mV = (vgs - vth) * 1000

        status = "OK"
        issues = []

        # Check Vov > minimum
        if vov_mV < SPECS["vov_min_mV"]:
            issues.append(f"Vov={vov_mV:.0f}mV < {SPECS['vov_min_mV']}mV")

        # Triode detection
        if abs(vds) < abs(vdsat):
            issues.append(f"TRIODE: |Vds|={abs(vds)*1000:.0f}mV < |Vdsat|={abs(vdsat)*1000:.0f}mV")

        if issues:
            status = "FAIL: " + "; ".join(issues)
            fails.append(f"{dev_name}: {'; '.join(issues)}")
            all_ok = False

        log(f"  {dev_name:7s} | {dev_info['type']:4s} | {dev_info['role']:13s} | {abs(id_val)*1e9:7.1f} | {vgs:+.4f} | {vth:+.4f} | {vov_mV:+7.1f} | {vds:+.4f} | {vdsat:+.5f} | {gm*1e6:6.3f}  | {gds_val*1e9:7.1f}  | {status}", report)

    # Tail current accuracy
    id_m11 = op_data["m11"]["id"]
    if id_m11 is not None:
        tail_nA = abs(id_m11) * 1e9
        tol_nA = SPECS["tail_current_nA"] * SPECS["tail_current_tol_pct"] / 100.0
        tail_err = abs(tail_nA - SPECS["tail_current_nA"])
        if tail_err > tol_nA:
            fails.append(f"M11 tail: {tail_nA:.1f}nA, error={tail_err:.1f}nA > {tol_nA:.0f}nA")
            all_ok = False
        log(f"\n  Tail current M11: {tail_nA:.1f} nA (target: {SPECS['tail_current_nA']} +/- {tol_nA:.0f} nA) — {'OK' if tail_err <= tol_nA else 'FAIL'}", report)

    # Stage 2 current check
    id_m7 = op_data["m7"]["id"]
    if id_m7 is not None:
        id2_nA = abs(id_m7) * 1e9
        id2_ok = SPECS["id_stage2_min_nA"] <= id2_nA <= SPECS["id_stage2_max_nA"]
        if not id2_ok:
            fails.append(f"Stage2 current {id2_nA:.1f}nA outside [{SPECS['id_stage2_min_nA']}, {SPECS['id_stage2_max_nA']}]")
            all_ok = False
        log(f"  Stage 2 current M7: {id2_nA:.1f} nA (range: [{SPECS['id_stage2_min_nA']}, {SPECS['id_stage2_max_nA']}]) — {'OK' if id2_ok else 'FAIL'}", report)

    # Output voltage
    if vout is not None:
        vout_ok = SPECS["vout_min_V"] <= vout <= SPECS["vout_max_V"]
        if not vout_ok:
            fails.append(f"Vout={vout:.3f}V outside [{SPECS['vout_min_V']}, {SPECS['vout_max_V']}]")
            all_ok = False
        log(f"  Output voltage: {vout:.4f} V (range: [{SPECS['vout_min_V']}, {SPECS['vout_max_V']}]) — {'OK' if vout_ok else 'FAIL'}", report)

    # Internal node v_s1
    if vs1 is not None:
        log(f"  Stage 1 output (v_s1): {vs1:.4f} V", report)

    # Power check
    if id_m11 is not None and id_m7 is not None:
        i_total_uA = (abs(id_m11) + abs(id_m7)) * 1e6
        power_uW = i_total_uA * 1.8
        pwr_ok = i_total_uA <= SPECS["total_current_max_uA"]
        if not pwr_ok:
            fails.append(f"Total current {i_total_uA:.3f} uA > {SPECS['total_current_max_uA']} uA")
            all_ok = False
        log(f"  Total supply current: {i_total_uA:.3f} uA (max: {SPECS['total_current_max_uA']}) — {'OK' if pwr_ok else 'FAIL'}", report)
        log(f"  Power: {power_uW:.2f} uW", report)

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
    log("GATE 2: AC OPEN-LOOP PERFORMANCE", report)
    log("=" * 70, report)

    output, err = run_ngspice("tb_pga_v2_ac.spice")
    if err:
        log(f"  BLOCKED: {err}", report)
        return False

    all_ok = True
    fails = []

    g_peak = parse_meas(output, "gain_peak")
    g_1hz = parse_meas(output, "g1")
    g_10hz = parse_meas(output, "g10")
    g_100hz = parse_meas(output, "g100")
    ugb = parse_meas(output, "ugb")
    phase_ugb = parse_meas(output, "phase_ugb")

    log(f"\n  Raw measurements:", report)
    log(f"    Peak gain:    {g_peak:.2f} dB" if g_peak else "    Peak gain:    NOT FOUND", report)
    log(f"    Gain @ 1 Hz:  {g_1hz:.2f} dB" if g_1hz else "    Gain @ 1 Hz:  NOT FOUND", report)
    log(f"    Gain @ 10 Hz: {g_10hz:.2f} dB" if g_10hz else "    Gain @ 10 Hz: NOT FOUND", report)
    log(f"    UGB:          {ugb:.1f} Hz" if ugb else "    UGB:          NOT FOUND", report)
    log(f"    Phase @ UGB:  {phase_ugb:.2f} deg" if phase_ugb else "    Phase @ UGB:  NOT FOUND", report)

    # Sanity: gain should be flat at low freq
    if g_peak is not None and g_10hz is not None:
        if g_peak - g_10hz > 6:
            log(f"\n  *** SANITY WARNING: Peak gain ({g_peak:.1f} dB) is {g_peak - g_10hz:.1f} dB above @10Hz ({g_10hz:.1f} dB).", report)
            fails.append(f"MEASUREMENT INVALID: gain not flat (peak={g_peak:.1f}dB, @10Hz={g_10hz:.1f}dB)")
            all_ok = False

    if phase_ugb is not None:
        pm = phase_ugb + 180
        log(f"    Phase margin: {pm:.1f} deg", report)
        if pm > 120:
            log(f"\n  *** SANITY WARNING: PM = {pm:.1f} deg > 120 deg.", report)
            fails.append(f"MEASUREMENT INVALID: PM={pm:.1f} deg")
            all_ok = False
    else:
        fails.append("Phase margin could not be measured")
        all_ok = False

    if all_ok:
        dc_gain = g_10hz if g_10hz is not None else g_peak
        if dc_gain is not None:
            if dc_gain < SPECS["dc_gain_min_dB"]:
                fails.append(f"DC gain {dc_gain:.1f} dB < {SPECS['dc_gain_min_dB']} dB")
                all_ok = False
            log(f"\n  DC gain: {dc_gain:.1f} dB (min: {SPECS['dc_gain_min_dB']}) — {'OK' if dc_gain >= SPECS['dc_gain_min_dB'] else 'FAIL'}", report)

        if ugb is not None:
            ugb_ok = SPECS["ugb_min_Hz"] <= ugb <= SPECS["ugb_max_Hz"]
            if not ugb_ok:
                fails.append(f"UGB {ugb:.0f} Hz outside [{SPECS['ugb_min_Hz']}, {SPECS['ugb_max_Hz']}]")
                all_ok = False
            log(f"  UGB: {ugb:.0f} Hz (range: [{SPECS['ugb_min_Hz']}, {SPECS['ugb_max_Hz']}]) — {'OK' if ugb_ok else 'FAIL'}", report)

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
    log("GATE 3: DC SWEEP & TRANSIENT", report)
    log("=" * 70, report)

    all_ok = True
    fails = []

    # DC sweep
    output_dc, err = run_ngspice("tb_pga_v2_dc.spice")
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

    # Transient — slew rate
    output_tran, err = run_ngspice("tb_pga_v2_tran.spice")
    if err:
        log(f"  Transient: BLOCKED: {err}", report)
        all_ok = False
    else:
        sr_direct = parse_meas(output_tran, "sr_meas")
        t_low = parse_meas(output_tran, "t_low")
        t_high = parse_meas(output_tran, "t_high")
        t10 = parse_meas(output_tran, "t10")
        t90 = parse_meas(output_tran, "t90")

        sr_mVus = None
        method = None

        if sr_direct is not None and sr_direct > 0:
            sr_mVus = sr_direct * 1e-3  # V/s -> mV/us
            method = "direct derivative"
        elif t_low is not None and t_high is not None and t_high > t_low:
            delta_v = 0.2
            sr_Vs = delta_v / (t_high - t_low)
            sr_mVus = sr_Vs * 1e-6 * 1e3
            method = "two-crossing"
        elif t10 is not None and t90 is not None and t90 > t10:
            v_before = parse_meas(output_tran, "v_before")
            v_after = parse_meas(output_tran, "v_after")
            if v_before is not None and v_after is not None:
                delta_v = abs(v_after - v_before) * 0.8
            else:
                delta_v = 0.08
            sr_Vs = delta_v / (t90 - t10)
            sr_mVus = sr_Vs * 1e-6 * 1e3
            method = "10-90%"

        if sr_mVus is not None:
            sr_ok = sr_mVus >= SPECS["slew_rate_min_mVus"]
            if not sr_ok:
                fails.append(f"Slew rate {sr_mVus:.2f} mV/us < {SPECS['slew_rate_min_mVus']} mV/us ({method})")
                all_ok = False
            log(f"  Slew rate: {sr_mVus:.2f} mV/us (min: {SPECS['slew_rate_min_mVus']}, method: {method}) — {'OK' if sr_ok else 'FAIL'}", report)
        else:
            log(f"  Slew rate: could not measure", report)
            fails.append("Could not measure slew rate")
            all_ok = False

    log(f"\n  GATE 3 RESULT: {'PASS' if all_ok else 'FAIL'}", report)
    if fails:
        log(f"  FAILURES ({len(fails)}):", report)
        for f in fails:
            log(f"    - {f}", report)
    log("  " + "=" * 70, report)
    return all_ok


def gate4_rejection(report):
    """GATE 4: PSRR and CMRR."""
    log("\n" + "=" * 70, report)
    log("GATE 4: REJECTION (PSRR, CMRR)", report)
    log("=" * 70, report)

    all_ok = True
    fails = []

    # PSRR
    if os.path.exists(os.path.join(WORK_DIR, "tb_pga_v2_psrr.spice")):
        output, err = run_ngspice("tb_pga_v2_psrr.spice")
        if err:
            log(f"  PSRR: BLOCKED: {err}", report)
            all_ok = False
        else:
            psrr_1k = parse_meas(output, "psrr_1k")
            if psrr_1k is not None:
                ok = psrr_1k >= SPECS["psrr_1k_min_dB"]
                if not ok:
                    fails.append(f"PSRR@1kHz {psrr_1k:.1f} dB < {SPECS['psrr_1k_min_dB']} dB")
                    all_ok = False
                log(f"  PSRR @ 1kHz: {psrr_1k:.1f} dB (min: {SPECS['psrr_1k_min_dB']}) — {'OK' if ok else 'FAIL'}", report)
            else:
                log(f"  PSRR @ 1kHz: NOT MEASURED", report)
                fails.append("psrr_1k not found")
                all_ok = False

    # CMRR
    if os.path.exists(os.path.join(WORK_DIR, "tb_pga_v2_cmrr.spice")):
        output, err = run_ngspice("tb_pga_v2_cmrr.spice")
        if err:
            log(f"  CMRR: BLOCKED: {err}", report)
            all_ok = False
        else:
            cmrr_dc = parse_meas(output, "cmrr_dc")
            if cmrr_dc is not None:
                ok = cmrr_dc >= SPECS["cmrr_dc_min_dB"]
                if not ok:
                    fails.append(f"CMRR@DC {cmrr_dc:.1f} dB < {SPECS['cmrr_dc_min_dB']} dB")
                    all_ok = False
                log(f"  CMRR @ DC: {cmrr_dc:.1f} dB (min: {SPECS['cmrr_dc_min_dB']}) — {'OK' if ok else 'FAIL'}", report)
            else:
                log(f"  CMRR @ DC: NOT MEASURED", report)
                fails.append("cmrr_dc not found")
                all_ok = False

    log(f"\n  GATE 4 RESULT: {'PASS' if all_ok else 'FAIL'}", report)
    if fails:
        log(f"  FAILURES ({len(fails)}):", report)
        for f in fails:
            log(f"    - {f}", report)
    log("  " + "=" * 70, report)
    return all_ok


def gate5_corners_temperature(report):
    """GATE 5: Corner and temperature sweep."""
    log("\n" + "=" * 70, report)
    log("GATE 5: CORNERS & TEMPERATURE", report)
    log("=" * 70, report)

    all_ok = True
    fails = []

    # Corner sweep
    corner_files = [f"tb_pga_v2_corner_{c}.spice" for c in ["tt", "ss", "ff", "sf", "fs"]]
    existing = [f for f in corner_files if os.path.exists(os.path.join(WORK_DIR, f))]

    if existing:
        corners_data = {}
        for cf in existing:
            corner_name = cf.replace("tb_pga_v2_corner_", "").replace(".spice", "").upper()
            output, err = run_ngspice(cf)
            if err:
                log(f"  Corner {corner_name}: BLOCKED: {err}", report)
                fails.append(f"Corner {corner_name} failed")
                all_ok = False
                continue
            gain = parse_meas(output, "gain_peak") or parse_meas(output, "gain_db")
            g10 = parse_meas(output, "g10")
            if g10 is not None and gain is not None and gain - g10 < 6:
                gain = g10
            ugb_val = parse_meas(output, "ugb")
            phase_raw = parse_meas(output, "phase_ugb")
            pm_val = phase_raw + 180 if phase_raw is not None else None
            corners_data[corner_name] = {"gain": gain, "ugb": ugb_val, "pm": pm_val}

        if corners_data:
            log(f"\n  Corner Results:", report)
            log(f"  {'Corner':8s} | {'Gain (dB)':10s} | {'UGB (kHz)':10s} | {'PM (deg)':10s} | Status", report)
            log(f"  {'-'*65}", report)

            gains = [v["gain"] for v in corners_data.values() if v["gain"] is not None]
            if len(gains) >= 3:
                gain_range = max(gains) - min(gains)
                if gain_range < 1.0:
                    log(f"\n  *** SANITY WARNING: Gain varies only {gain_range:.1f} dB across corners.", report)
                    fails.append(f"SUSPICIOUS: gain range {gain_range:.1f} dB")
                    all_ok = False
                else:
                    log(f"\n  Corner gain range: {gain_range:.1f} dB (OK, >1 dB)", report)

            for corner, data in sorted(corners_data.items()):
                g = data["gain"]
                u = data["ugb"]
                pm = data["pm"]
                issues_c = []
                if g is not None and g < SPECS["corner_gain_min_dB"]:
                    issues_c.append(f"gain {g:.1f} < {SPECS['corner_gain_min_dB']} dB")
                if u is not None and not (SPECS["corner_ugb_min_Hz"] <= u <= SPECS["corner_ugb_max_Hz"]):
                    issues_c.append(f"UGB {u:.0f} outside [{SPECS['corner_ugb_min_Hz']}, {SPECS['corner_ugb_max_Hz']}]")
                if pm is not None and pm < SPECS["corner_pm_min_deg"]:
                    issues_c.append(f"PM {pm:.1f} < {SPECS['corner_pm_min_deg']} deg")
                status = "OK" if not issues_c else "FAIL: " + "; ".join(issues_c)
                if issues_c:
                    fails.extend([f"Corner {corner}: {i}" for i in issues_c])
                    all_ok = False
                g_str = f"{g:.1f}" if g else "N/A"
                u_str = f"{u/1000:.1f}" if u else "N/A"
                pm_str = f"{pm:.1f}" if pm else "N/A"
                log(f"  {corner:8s} | {g_str:>10s} | {u_str:>10s} | {pm_str:>10s} | {status}", report)

    # Temperature sweep
    temp_map = {"m40": "-40C", "27": "27C", "85": "85C"}
    temp_files = [f"tb_pga_v2_temp_{t}.spice" for t in ["m40", "27", "85"]]
    existing_temps = [f for f in temp_files if os.path.exists(os.path.join(WORK_DIR, f))]

    if existing_temps:
        temp_data = {}
        for tf in existing_temps:
            temp_key = tf.replace("tb_pga_v2_temp_", "").replace(".spice", "")
            temp_name = temp_map.get(temp_key, temp_key + "C")
            output, err = run_ngspice(tf)
            if err:
                log(f"  Temp {temp_name}: BLOCKED: {err}", report)
                fails.append(f"Temp {temp_name} failed")
                all_ok = False
                continue
            gain = parse_meas(output, "gain_peak") or parse_meas(output, "gain_db")
            g10 = parse_meas(output, "g10")
            if g10 is not None and gain is not None and gain - g10 < 6:
                gain = g10
            ugb_val = parse_meas(output, "ugb")
            phase_raw = parse_meas(output, "phase_ugb")
            pm_val = phase_raw + 180 if phase_raw is not None else None
            temp_data[temp_name] = {"gain": gain, "ugb": ugb_val, "pm": pm_val}

        if temp_data:
            log(f"\n  Temperature Results:", report)
            log(f"  {'Temp':8s} | {'Gain (dB)':10s} | {'UGB (kHz)':10s} | {'PM (deg)':10s} | Status", report)
            log(f"  {'-'*65}", report)

            for temp, data in sorted(temp_data.items()):
                g = data["gain"]
                u = data["ugb"]
                pm = data["pm"]
                issues_t = []
                if g is not None and g < SPECS["temp_gain_min_dB"]:
                    issues_t.append(f"gain {g:.1f} < {SPECS['temp_gain_min_dB']} dB")
                if u is not None and not (SPECS["temp_ugb_min_Hz"] <= u <= SPECS["temp_ugb_max_Hz"]):
                    issues_t.append(f"UGB {u:.0f} outside [{SPECS['temp_ugb_min_Hz']}, {SPECS['temp_ugb_max_Hz']}]")
                if pm is not None and pm < SPECS["corner_pm_min_deg"]:
                    issues_t.append(f"PM {pm:.1f} < {SPECS['corner_pm_min_deg']} deg")
                status = "OK" if not issues_t else "FAIL: " + "; ".join(issues_t)
                if issues_t:
                    fails.extend([f"Temp {temp}: {i}" for i in issues_t])
                    all_ok = False
                g_str = f"{g:.1f}" if g else "N/A"
                u_str = f"{u/1000:.1f}" if u else "N/A"
                pm_str = f"{pm:.1f}" if pm else "N/A"
                log(f"  {temp:8s} | {g_str:>10s} | {u_str:>10s} | {pm_str:>10s} | {status}", report)

    log(f"\n  GATE 5 RESULT: {'PASS' if all_ok else 'FAIL'}", report)
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
    log(f"# PGA OTA v2 VERIFICATION RUN #{attempt} -- {timestamp}", report)
    log(f"{'#' * 70}", report)

    required = ["ota_pga_v2.spice", "tb_pga_v2_op.spice"]
    missing = [f for f in required if not os.path.exists(os.path.join(WORK_DIR, f))]
    if missing:
        log(f"\nMISSING FILES: {missing}", report)
        with open(REPORT_FILE, "a") as f:
            f.write("\n".join(report) + "\n")
        sys.exit(99)

    # Gate 1
    gate1_pass, op_data = gate1_operating_point(report)
    if not gate1_pass:
        log(f"\n! GATE 1 FAILED — Attempt #{attempt}.", report)
        with open(REPORT_FILE, "a") as f:
            f.write("\n".join(report) + "\n")
        sys.exit(1)

    # Gate 2
    if os.path.exists(os.path.join(WORK_DIR, "tb_pga_v2_ac.spice")):
        gate2_pass = gate2_ac_performance(report)
        if not gate2_pass:
            log(f"\n! GATE 2 FAILED — Attempt #{attempt}.", report)
            with open(REPORT_FILE, "a") as f:
                f.write("\n".join(report) + "\n")
            sys.exit(2)

    # Gate 3
    tb_dc = os.path.exists(os.path.join(WORK_DIR, "tb_pga_v2_dc.spice"))
    tb_tran = os.path.exists(os.path.join(WORK_DIR, "tb_pga_v2_tran.spice"))
    if tb_dc or tb_tran:
        gate3_pass = gate3_dc_transient(report)
        if not gate3_pass:
            log(f"\n  GATE 3 FAILED — Attempt #{attempt}", report)
            with open(REPORT_FILE, "a") as f:
                f.write("\n".join(report) + "\n")
            sys.exit(3)

    # Gate 4
    tb_psrr = os.path.exists(os.path.join(WORK_DIR, "tb_pga_v2_psrr.spice"))
    tb_cmrr = os.path.exists(os.path.join(WORK_DIR, "tb_pga_v2_cmrr.spice"))
    if tb_psrr or tb_cmrr:
        gate4_pass = gate4_rejection(report)
        if not gate4_pass:
            log(f"\n  GATE 4 FAILED — Attempt #{attempt}", report)
            with open(REPORT_FILE, "a") as f:
                f.write("\n".join(report) + "\n")
            sys.exit(4)

    # Gate 5
    corner_files = [f"tb_pga_v2_corner_{c}.spice" for c in ["tt", "ss", "ff", "sf", "fs"]]
    temp_files = [f"tb_pga_v2_temp_{t}.spice" for t in ["m40", "27", "85"]]
    has_corners = any(os.path.exists(os.path.join(WORK_DIR, f)) for f in corner_files)
    has_temps = any(os.path.exists(os.path.join(WORK_DIR, f)) for f in temp_files)
    if has_corners or has_temps:
        gate5_pass = gate5_corners_temperature(report)
        if not gate5_pass:
            log(f"\n  GATE 5 FAILED — Attempt #{attempt}", report)
            with open(REPORT_FILE, "a") as f:
                f.write("\n".join(report) + "\n")
            sys.exit(5)

    # All passed
    log(f"\n{'*' * 70}", report)
    log(f"* ALL GATES PASSED — attempt #{attempt}", report)
    log(f"{'*' * 70}", report)

    with open(REPORT_FILE, "a") as f:
        f.write("\n".join(report) + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
