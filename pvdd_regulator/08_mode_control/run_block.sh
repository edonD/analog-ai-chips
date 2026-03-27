#!/usr/bin/env bash
# run_block.sh — Block 08: Mode Control
# Usage: bash run_block.sh > run.log 2>&1

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 08: Mode Control ==="
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

run_tb tb_mc_ramp_normal.spice
run_tb tb_mc_fast_ramp.spice
run_tb tb_mc_slow_ramp.spice
run_tb tb_mc_power_down.spice
run_tb tb_mc_hysteresis.spice
run_tb tb_mc_iq.spice
run_tb tb_mc_pvt.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
