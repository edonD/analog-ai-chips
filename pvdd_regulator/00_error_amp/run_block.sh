#!/usr/bin/env bash
# run_block.sh — Block 00: Error Amplifier
# Runs all testbenches and aggregates output into run.log.
#
# Usage:
#   bash run_block.sh > run.log 2>&1
#
# After running, evaluate results:
#   python3 evaluate.py

set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 00: Error Amplifier ==="
echo "Run started: $(date)"
echo ""

TMPDIR=$(mktemp -d)
DC_OUT="$TMPDIR/dc.out"
AC_OUT="$TMPDIR/ac.out"
SWING_OUT="$TMPDIR/swing.out"
OFFSET_OUT="$TMPDIR/offset.out"
CMRR_OUT="$TMPDIR/cmrr.out"
PSRR_OUT="$TMPDIR/psrr.out"
PVT_OUT="$TMPDIR/pvt.out"
NOISE_OUT="$TMPDIR/noise.out"

run_tb() {
    local tb="$1"
    local out="$2"
    if [ -f "$tb" ]; then
        echo "--- Running $tb ---"
        ngspice -b "$tb" > "$out" 2>&1
        local rc=$?
        cat "$out"
        if [ $rc -ne 0 ]; then
            echo "WARNING: $tb exited with code $rc"
        fi
        echo ""
    else
        echo "WARNING: $tb not found — skipping"
        echo ""
    fi
}

run_tb tb_ea_dc.spice "$DC_OUT"
run_tb tb_ea_ac.spice "$AC_OUT"
run_tb tb_ea_swing.spice "$SWING_OUT"
run_tb tb_ea_offset.spice "$OFFSET_OUT"
run_tb tb_ea_cmrr.spice "$CMRR_OUT"
run_tb tb_ea_psrr.spice "$PSRR_OUT"
run_tb tb_ea_pvt.spice "$PVT_OUT"
run_tb tb_ea_noise.spice "$NOISE_OUT"

# Post-process CMRR: CMRR_dB = dc_gain_dB - acm_dc_dB
echo "--- Post-processing CMRR and PSRR ---"
DC_GAIN=$(grep "^dc_gain:" "$AC_OUT" 2>/dev/null | awk '{print $2}')
ACM_DC=$(grep "^acm_dc_dB:" "$CMRR_OUT" 2>/dev/null | awk '{print $2}')
APS_DC=$(grep "^aps_dc_dB:" "$PSRR_OUT" 2>/dev/null | awk '{print $2}')

if [ -n "$DC_GAIN" ] && [ -n "$ACM_DC" ]; then
    CMRR=$(python3 -c "print(f'{abs($DC_GAIN) - ($ACM_DC):.1f}')" 2>/dev/null || echo "0")
    echo "cmrr_dB: $CMRR"
else
    echo "cmrr_dB: 0"
fi

if [ -n "$DC_GAIN" ] && [ -n "$APS_DC" ]; then
    PSRR=$(python3 -c "print(f'{abs($DC_GAIN) - ($APS_DC):.1f}')" 2>/dev/null || echo "0")
    echo "psrr_dB: $PSRR"
else
    echo "psrr_dB: 0"
fi

echo ""

# Clean up
rm -rf "$TMPDIR"

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
