#!/usr/bin/env bash
# run_block.sh — Block 03: Compensation
# Usage: bash run_block.sh > run.log 2>&1

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 03: Compensation ==="
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

run_tb tb_comp_lstb.spice
run_tb tb_comp_pm_vs_load.spice
run_tb tb_comp_pvt.spice
run_tb tb_comp_bvdd_sweep.spice
run_tb tb_comp_load_step.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
