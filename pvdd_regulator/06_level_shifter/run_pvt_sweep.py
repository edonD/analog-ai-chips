#!/usr/bin/env python3
"""run_pvt_sweep.py — Full 15-corner PVT sweep for Block 06 Level Shifter.

Generates a per-corner netlist, runs ngspice, extracts metrics, and prints
worst-case results in the format expected by the evaluator.
"""

import subprocess
import tempfile
import re
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

PDK_LIB = "/home/ubuntu/pdk/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/ngspice/sky130.lib.spice"

CORNERS = ["tt", "ss", "ff", "sf", "fs"]
TEMPS = [-40, 27, 150]
BVDD = 5.4  # worst-case supply for up-shifter


def make_netlist(corner, temp):
    """Generate a PVT testbench netlist for the given corner and temperature."""
    return f"""\
* PVT sweep: {corner} {temp}C BVDD={BVDD}V
.include {SCRIPT_DIR}/design.cir
.lib {PDK_LIB} {corner}

.option method=gear reltol=1e-6
.temp {temp}

Vsvdd svdd 0 2.2
Vbvdd bvdd 0 {BVDD}
Vpvdd pvdd 0 5.0

Cload_up out_up 0 1p
Cload_dn out_dn 0 1p

Vin_up in_up 0 PULSE(0 2.2 50n 1n 1n 200n 400n)
Vin_dn in_dn 0 PULSE(0 5.0 50n 1n 1n 200n 400n)

Xup in_up out_up bvdd svdd 0 level_shifter_up
Xdn in_dn out_dn pvdd svdd 0 level_shifter_down

.tran 0.1n 800n

.control
run

* Output levels
meas tran lth_high MAX v(out_up) FROM=150n TO=240n
meas tran lth_low  MIN v(out_up) FROM=350n TO=440n
meas tran htl_high MAX v(out_dn) FROM=150n TO=240n
meas tran htl_low  MIN v(out_dn) FROM=350n TO=440n

* Delays
meas tran tplh_up TRIG v(in_up) VAL=1.1 RISE=1 TARG v(out_up) VAL=2.7 RISE=1
meas tran tphl_up TRIG v(in_up) VAL=1.1 FALL=1 TARG v(out_up) VAL=2.7 FALL=1
meas tran tplh_dn TRIG v(in_dn) VAL=2.5 RISE=1 TARG v(out_dn) VAL=1.1 RISE=1
meas tran tphl_dn TRIG v(in_dn) VAL=2.5 FALL=1 TARG v(out_dn) VAL=1.1 FALL=1

* Metastability
meas tran lth_at_150n FIND v(out_up) AT=150n
meas tran lth_at_350n FIND v(out_up) AT=350n
meas tran htl_at_150n FIND v(out_dn) AT=150n
meas tran htl_at_350n FIND v(out_dn) AT=350n

* Static power (measure supply current in settled region)
meas tran ibvdd_ss AVG i(Vbvdd) FROM=200n TO=240n
meas tran ipvdd_ss AVG i(Vpvdd) FROM=200n TO=240n

* Compute
let d1 = tplh_up * 1e9
let d2 = tphl_up * 1e9
let d3 = tplh_dn * 1e9
let d4 = tphl_dn * 1e9
let dmax = d1
if d2 > dmax
  let dmax = d2
end
if d3 > dmax
  let dmax = d3
end
if d4 > dmax
  let dmax = d4
end

let lth_margin_raw = lth_high - {BVDD - 0.2}
let htl_margin_raw = htl_high - 2.0
let lth_margin = floor(lth_margin_raw * 1e4 + 0.5) / 1e4
let htl_margin = floor(htl_margin_raw * 1e4 + 0.5) / 1e4

let pwr_bvdd = abs(ibvdd_ss) * 1e6
let pwr_pvdd = abs(ipvdd_ss) * 1e6
let pwr_worst = pwr_bvdd
if pwr_pvdd > pwr_worst
  let pwr_worst = pwr_pvdd
end

echo "PVT_RESULT {corner} {temp}C"
echo "pvt_dmax:" "$&dmax"
echo "pvt_lth_margin:" "$&lth_margin"
echo "pvt_htl_margin:" "$&htl_margin"
echo "pvt_lth_low:" "$&lth_low"
echo "pvt_htl_low:" "$&htl_low"
echo "pvt_lth_high:" "$&lth_high"
echo "pvt_htl_high:" "$&htl_high"
echo "pvt_power_uA:" "$&pwr_worst"
echo "pvt_tplh_up_ns:" "$&d1"
echo "pvt_tphl_up_ns:" "$&d2"
echo "pvt_tplh_dn_ns:" "$&d3"
echo "pvt_tphl_dn_ns:" "$&d4"

* Metastability check
let meta = 1
if lth_at_150n < 4.9
  let meta = 0
end
if lth_at_350n > 0.5
  let meta = 0
end
if htl_at_150n < 1.7
  let meta = 0
end
if htl_at_350n > 0.5
  let meta = 0
end
echo "pvt_meta:" "$&meta"

quit
.endc

.end
"""


def run_corner(corner, temp):
    """Run a single PVT corner and return parsed results."""
    netlist = make_netlist(corner, temp)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.spice', dir=SCRIPT_DIR,
                                      delete=False) as f:
        f.write(netlist)
        fname = f.name

    try:
        result = subprocess.run(
            ["/usr/bin/ngspice", "-b", fname],
            capture_output=True, text=True, timeout=120,
            cwd=SCRIPT_DIR
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {corner} {temp}C", file=sys.stderr)
        return None
    finally:
        os.unlink(fname)

    # Parse results
    data = {}
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("pvt_"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                val_str = parts[1].strip()
                try:
                    data[key] = float(val_str)
                except ValueError:
                    data[key] = None

    return data


def main():
    print("=== Full PVT Sweep (5 corners x 3 temps = 15 runs) ===")
    print(f"BVDD = {BVDD}V (worst case for up-shifter)")
    print()

    all_results = {}
    worst_delay = 0
    worst_lth_margin = 999
    worst_htl_margin = 999
    worst_lth_low = 0
    worst_htl_low = 0
    worst_power = 0
    all_meta = True
    all_work = True
    ss_150c_works = False

    for corner in CORNERS:
        for temp in TEMPS:
            label = f"{corner.upper()} {temp}C"
            sys.stdout.write(f"  Running {label}... ")
            sys.stdout.flush()
            data = run_corner(corner, temp)

            if data is None:
                print("FAILED (timeout or error)")
                all_work = False
                continue

            dmax = data.get("pvt_dmax")
            lth_m = data.get("pvt_lth_margin")
            htl_m = data.get("pvt_htl_margin")
            lth_l = data.get("pvt_lth_low")
            htl_l = data.get("pvt_htl_low")
            lth_h = data.get("pvt_lth_high")
            htl_h = data.get("pvt_htl_high")
            pwr = data.get("pvt_power_uA")
            meta = data.get("pvt_meta")

            # Check if this corner works
            corner_ok = True
            if dmax is None or dmax > 100:
                corner_ok = False
            if lth_h is not None and lth_h < (BVDD - 0.2):
                corner_ok = False
            if lth_l is not None and lth_l > 0.2:
                corner_ok = False
            if htl_h is not None and htl_h < 2.0:
                corner_ok = False
            if htl_l is not None and htl_l > 0.2:
                corner_ok = False

            status = "OK" if corner_ok else "FAIL"
            delay_str = f"{dmax:.2f}ns" if dmax is not None else "???"
            print(f"delay={delay_str}  lth_margin={lth_m}  meta={meta}  [{status}]")

            all_results[(corner, temp)] = data

            # Track worst case
            if dmax is not None and dmax > worst_delay:
                worst_delay = dmax
            if lth_m is not None and lth_m < worst_lth_margin:
                worst_lth_margin = lth_m
            if htl_m is not None and htl_m < worst_htl_margin:
                worst_htl_margin = htl_m
            if lth_l is not None and lth_l > worst_lth_low:
                worst_lth_low = lth_l
            if htl_l is not None and htl_l > worst_htl_low:
                worst_htl_low = htl_l
            if pwr is not None and pwr > worst_power:
                worst_power = pwr
            if meta is not None and meta < 1:
                all_meta = False
            if not corner_ok:
                all_work = False

            # Special check for SS 150C
            if corner == "ss" and temp == 150 and corner_ok:
                ss_150c_works = True

    print()
    print("=== PVT Sweep Summary ===")
    print(f"Worst delay:       {worst_delay:.2f} ns (spec <= 100)")
    print(f"Worst LTH margin:  {worst_lth_margin:.4f} V (spec >= 0.2)")
    print(f"Worst HTL margin:  {worst_htl_margin:.4f} V (spec >= 0.2)")
    print(f"Worst LTH low:     {worst_lth_low:.2e} V (spec <= 0.2)")
    print(f"Worst HTL low:     {worst_htl_low:.2e} V (spec <= 0.2)")
    print(f"Worst power:       {worst_power:.4f} uA (spec <= 5)")
    print(f"All metastable-free: {all_meta}")
    print(f"All corners work:  {all_work}")
    print(f"SS 150C works:     {ss_150c_works}")
    print()

    # Print per-corner delays for plotting
    print("=== Per-corner delays ===")
    for corner in CORNERS:
        for temp in TEMPS:
            d = all_results.get((corner, temp), {})
            dmax = d.get("pvt_dmax", "???")
            d_up_lh = d.get("pvt_tplh_up_ns", "???")
            d_up_hl = d.get("pvt_tphl_up_ns", "???")
            d_dn_lh = d.get("pvt_tplh_dn_ns", "???")
            d_dn_hl = d.get("pvt_tphl_dn_ns", "???")
            print(f"corner_{corner}_{temp}C_delay_ns: {dmax}")
            print(f"corner_{corner}_{temp}C_up_tplh_ns: {d_up_lh}")
            print(f"corner_{corner}_{temp}C_up_tphl_ns: {d_up_hl}")
            print(f"corner_{corner}_{temp}C_dn_tplh_ns: {d_dn_lh}")
            print(f"corner_{corner}_{temp}C_dn_tphl_ns: {d_dn_hl}")
    print()

    # Print final metrics for the evaluator (these are the LAST values it sees)
    print("=== Final metrics (worst-case across all 15 PVT corners) ===")
    print(f"delay_max_ns: {worst_delay:.4f}")
    print(f"lth_out_high_margin_V: {worst_lth_margin:.4f}")
    print(f"lth_out_low_V: {worst_lth_low:.6e}")
    print(f"htl_out_high_margin_V: {worst_htl_margin:.4f}")
    print(f"htl_out_low_V: {worst_htl_low:.6e}")
    print(f"static_power_uA: {worst_power:.4f}")
    print(f"works_ss_150c: {1 if ss_150c_works else 0}")
    print(f"no_metastable: {1 if all_meta else 0}")


if __name__ == "__main__":
    main()
