#!/usr/bin/env python3
"""Run PVT corners for mode control threshold verification.

Generates per-corner SPICE netlists, runs them with ngspice, parses results,
and prints worst-case metrics.
"""
import subprocess
import re
import os
import sys
import tempfile

CORNERS = ['tt', 'ss', 'ff', 'sf', 'fs']
NOMINALS = {'thresh_por_v': 2.5, 'thresh_ret_v': 4.2,
            'thresh_pup_v': 4.5, 'thresh_act_v': 5.6}

NETLIST_TEMPLATE = """\
* Testbench: Mode Control — PVT ({corner} corner)
.include "parasitic_res_po.spice"
.lib "../sky130.lib.spice" {corner}
.include "design.cir"
.option method=gear reltol=1e-3 abstol=1e-12 vntol=1e-6 gmin=1e-12
.option itl1=300 itl2=200 itl4=50
Vbvdd bvdd gnd PWL(0 0 10.5u 10.5)
Vpvdd pvdd gnd 5.0
Vsvdd svdd gnd 2.2
Vref  vref gnd 1.226
Ven   en_ret gnd 0
XDUT bvdd pvdd svdd gnd vref en_ret bypass_en ea_en ref_sel uvov_en ilim_en pass_off mode_control
.tran 10n 12u uic
.control
run
meas tran thresh_por_v FIND v(bvdd) WHEN v(bypass_en)=0.5 RISE=1 TD=2u
meas tran thresh_ret_v FIND v(bvdd) WHEN v(ea_en)=0.5 RISE=1 TD=2u
meas tran thresh_pup_v FIND v(bvdd) WHEN v(bypass_en)=0.5 RISE=2 TD=2u
meas tran thresh_act_v FIND v(bvdd) WHEN v(uvov_en)=0.5 RISE=1 TD=2u
echo "PVT_{corner}_thresh_por_v: $&thresh_por_v"
echo "PVT_{corner}_thresh_ret_v: $&thresh_ret_v"
echo "PVT_{corner}_thresh_pup_v: $&thresh_pup_v"
echo "PVT_{corner}_thresh_act_v: $&thresh_act_v"
.endc
.end
"""


def run_corner(corner, workdir):
    """Run a single PVT corner and return parsed thresholds."""
    netlist = NETLIST_TEMPLATE.format(corner=corner)
    spice_file = os.path.join(workdir, f'tb_pvt_{corner}.spice')
    with open(spice_file, 'w') as f:
        f.write(netlist)

    result = subprocess.run(
        ['ngspice', '-b', spice_file],
        capture_output=True, text=True, timeout=120,
        cwd=workdir
    )
    output = result.stdout + result.stderr

    thresholds = {}
    for key in NOMINALS:
        pattern = rf'PVT_{corner}_{key}:\s+([\d.eE+-]+)'
        m = re.search(pattern, output)
        if m:
            thresholds[key] = float(m.group(1))
    return thresholds


def main():
    workdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(workdir)

    all_results = {}
    for corner in CORNERS:
        print(f'Running {corner.upper()} corner...', file=sys.stderr)
        thresholds = run_corner(corner, workdir)
        if len(thresholds) < 4:
            print(f'ERROR: {corner} corner failed — only got {len(thresholds)}/4 thresholds',
                  file=sys.stderr)
            print(f'thresh_max_error_pct: 99.0')
            return
        all_results[corner] = thresholds

    # Find worst-case max error across all corners
    worst_max_err = 0.0

    for corner, thresholds in all_results.items():
        por = thresholds['thresh_por_v']
        ret = thresholds['thresh_ret_v']
        pup = thresholds['thresh_pup_v']
        act = thresholds['thresh_act_v']

        e1 = abs(por - 2.5) / 2.5 * 100
        e2 = abs(ret - 4.2) / 4.2 * 100
        e3 = abs(pup - 4.5) / 4.5 * 100
        e4 = abs(act - 5.6) / 5.6 * 100
        corner_max = max(e1, e2, e3, e4)

        print(f'  {corner.upper()}: POR={por:.3f}V  RET={ret:.3f}V  PUP={pup:.3f}V  ACT={act:.3f}V  max_err={corner_max:.2f}%',
              file=sys.stderr)

        if corner_max > worst_max_err:
            worst_max_err = corner_max

    # Only print thresh_max_error_pct — individual thresholds come from
    # tb_mc_ramp_normal.spice (TT corner). Printing them here would override
    # those values since evaluate.py takes the last occurrence.
    print(f'thresh_max_error_pct: {worst_max_err:.4f}')


if __name__ == '__main__':
    main()
