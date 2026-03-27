#!/usr/bin/env bash
# run_block.sh — Block 02: Feedback Network
# Usage: bash run_block.sh > run.log 2>&1

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 02: Feedback Network ==="
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

run_tb tb_fb_dc_ratio.spice
run_tb tb_fb_temp.spice
run_tb tb_fb_corners.spice
run_tb tb_fb_noise.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
