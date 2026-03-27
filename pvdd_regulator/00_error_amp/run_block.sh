#!/usr/bin/env bash
# run_block.sh — Block 00: Error Amplifier
# Runs all testbenches and aggregates output into run.log.
#
# Usage:
#   bash run_block.sh 2>&1 | tee run.log
# Or (captures both stdout and stderr):
#   bash run_block.sh > run.log 2>&1
#
# After running, evaluate results:
#   python3 evaluate.py
#
# Note: The program.md shows "ngspice -b run_block.sh > run.log 2>&1"
#       which is shorthand for running this shell script.

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 00: Error Amplifier ==="
echo "Run started: $(date)"
echo ""

run_tb() {
    local tb="$1"
    if [ -f "$tb" ]; then
        echo "--- Running $tb ---"
        ngspice -b "$tb"
        local rc=$?
        if [ $rc -ne 0 ]; then
            echo "WARNING: $tb exited with code $rc"
        fi
        echo ""
    else
        echo "WARNING: $tb not found — skipping"
        echo ""
    fi
}

run_tb tb_ea_dc.spice
run_tb tb_ea_ac.spice
run_tb tb_ea_swing.spice
run_tb tb_ea_offset.spice
run_tb tb_ea_cmrr.spice
run_tb tb_ea_psrr.spice
run_tb tb_ea_pvt.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
