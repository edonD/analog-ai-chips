#!/usr/bin/env bash
# run_block.sh — Block 09: Startup Circuit
# Usage: bash run_block.sh > run.log 2>&1
#
# NOTE: Startup simulations are the most convergence-challenging in the project.
# Allow up to 45 minutes for the full suite.
# Run tb_su_basic.spice first (5 min) to verify basic startup before adding closed loop.

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 09: Startup Circuit ==="
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

run_tb tb_su_basic.spice
run_tb tb_su_handoff.spice
run_tb tb_su_50mA.spice
run_tb tb_su_fast_ramp.spice
run_tb tb_su_slow_ramp.spice
run_tb tb_su_cold_crank.spice
run_tb tb_su_leakage.spice
run_tb tb_su_pvt.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
