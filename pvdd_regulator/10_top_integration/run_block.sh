#!/usr/bin/env bash
# run_block.sh — Block 10: Top Integration
# Usage: bash run_block.sh > run.log 2>&1
#
# NOTE: Full integration simulations can take up to 2 hours.
# Build incrementally: start with tb_top_regulation.spice (steady-state DC),
# then add transient, then startup, then all corners.
#
# Recommended order (by dependency tier):
#   Tier 1: regulation accuracy, DC operating point
#   Tier 2: line/load regulation, transient response
#   Tier 3: stability (phase margin), PSRR
#   Tier 4: startup, current limit, UV/OV
#   Tier 5: full PVT corners

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 10: Top Integration ==="
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

# Tier 1: DC accuracy
run_tb tb_top_dc_reg.spice

# Tier 2: Line and load regulation, transient
run_tb tb_top_line_reg.spice
run_tb tb_top_load_reg.spice
run_tb tb_top_load_tran.spice

# Tier 3: Stability and noise
run_tb tb_top_lstb.spice
run_tb tb_top_psrr.spice

# Tier 4: Startup
run_tb tb_top_startup.spice
run_tb tb_top_startup_fast.spice

# Tier 5: Dropout
run_tb tb_top_dropout.spice

# Tier 6: Protection
run_tb tb_top_ilim.spice
run_tb tb_top_uv.spice
run_tb tb_top_ov.spice

# Tier 7: Modes and quiescent
run_tb tb_top_modes.spice
run_tb tb_top_iq.spice
run_tb tb_top_retention.spice
run_tb tb_top_power.spice

# Tier 8: Full PVT corners
run_tb tb_top_pvt.spice

# Tier 9: Extended transient and line tests
run_tb tb_top_load_tran_full.spice
run_tb tb_top_line_tran.spice
run_tb tb_top_cold_crank.spice

# Tier 10: Reference and supply variation
run_tb tb_top_avbg_sweep.spice
run_tb tb_top_avbg_pvt.spice
run_tb tb_top_en.spice

# Tier 11: Frequency-domain characterization
run_tb tb_top_psrr_freq.spice
run_tb tb_top_noise.spice

# Tier 12: Stability robustness
run_tb tb_top_pm_fine.spice
run_tb tb_top_cload.spice

# Tier 13: Cross-parameter and TC
run_tb tb_top_ldr_bvdd.spice
run_tb tb_top_tc.spice

# Tier 14: Device reliability
run_tb tb_top_soa.spice

# Tier 15: Monte Carlo (500 runs — run last, takes longest)
run_tb tb_top_mc.spice

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
