#!/usr/bin/env bash
# run_block.sh — Block 05: UV/OV Comparators
# Usage: bash run_block.sh > run.log 2>&1

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 05: UV/OV Comparators ==="
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

run_tb tb_uv_trip.spice
run_tb tb_ov_trip.spice
run_tb tb_comp_response.spice
run_tb tb_comp_power.spice
run_tb tb_comp_output_swing.spice
run_tb tb_comp_pvt.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
