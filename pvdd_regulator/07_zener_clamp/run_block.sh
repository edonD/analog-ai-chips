#!/usr/bin/env bash
# run_block.sh — Block 07: Zener Clamp
# Usage: bash run_block.sh > run.log 2>&1

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 07: Zener Clamp ==="
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

# Main testbenches
run_tb tb_zc_iv.spice
run_tb tb_zc_temp.spice
run_tb tb_zc_transient.spice

# Corner testbenches
run_tb tb_zc_corners.spice
run_tb tb_zc_corner_ss.spice
run_tb tb_zc_corner_ff.spice
run_tb tb_zc_corner_sf.spice
run_tb tb_zc_corner_fs.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
