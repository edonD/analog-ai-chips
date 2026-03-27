#!/usr/bin/env bash
# run_block.sh — Block 01: Pass Device
# Usage: bash run_block.sh > run.log 2>&1

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 01: Pass Device ==="
echo "Run started: $(date)"
echo ""

run_tb() {
    local tb="$1"
    if [ -f "$tb" ]; then
        echo "--- Running $tb ---"
        ngspice -b "$tb"
        local rc=$?
        [ $rc -ne 0 ] && echo "WARNING: $tb exited with code $rc"
        echo ""
    else
        echo "WARNING: $tb not found — skipping"
        echo ""
    fi
}

run_tb tb_pass_idvds.spice
run_tb tb_pass_idvgs.spice
# tb_pass_idvgs_ss150 is called by tb_pass_idvgs
run_tb tb_pass_cgs.spice
run_tb tb_pass_gm.spice
run_tb tb_pass_rds.spice
run_tb tb_pass_leakage.spice
run_tb tb_pass_pvt.spice
# tb_pass_pvt_ss and _ff are called by tb_pass_pvt
run_tb tb_pass_soa.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
