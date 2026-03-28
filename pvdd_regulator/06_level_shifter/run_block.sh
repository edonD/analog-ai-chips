#!/usr/bin/env bash
# run_block.sh — Block 06: Level Shifter
# Usage: bash run_block.sh > run.log 2>&1

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 06: Level Shifter ==="
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

run_tb tb_ls_logic.spice
run_tb tb_ls_delay.spice
run_tb tb_ls_bvdd_sweep.spice
run_tb tb_ls_power.spice
run_tb tb_ls_pvt.spice

echo "--- Running full PVT sweep (15 corners) ---"
python3 run_pvt_sweep.py
echo ""

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
