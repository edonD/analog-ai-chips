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
# Generate design_noise.cir (adds nrd/nrs for clean noise analysis)
sed 's/sky130_fd_pr__nfet_g5v0d10v5 \(.*\)$/sky130_fd_pr__nfet_g5v0d10v5 \1 nrd=0.1 nrs=0.1/' design.cir | \
sed 's/sky130_fd_pr__pfet_g5v0d10v5 \(.*\)$/sky130_fd_pr__pfet_g5v0d10v5 \1 nrd=0.1 nrs=0.1/' > design_noise.cir

run_tb tb_ea_noise.spice "$NOISE_OUT"

# =================================================================
# PVT: All 15 corners (5 process x 3 temperature)
# =================================================================
echo "--- Running PVT: 15 corners (5 process x 3 temp) ---"
PVT_ALL_PASS=1
PVT_RESULTS=""

for corner in tt ss ff sf fs; do
    # Generate corner-specific testbench
    sed "s/CORNER_PLACEHOLDER/$corner/g" tb_ea_pvt_template.spice > "$TMPDIR/tb_ea_pvt_${corner}.spice"
    ngspice -b "$TMPDIR/tb_ea_pvt_${corner}.spice" > "$TMPDIR/pvt_${corner}.out" 2>&1

    # Print output
    cat "$TMPDIR/pvt_${corner}.out"

    # Check each temperature for this corner
    while IFS= read -r line; do
        if echo "$line" | grep -q "^PVT "; then
            echo "$line"
            PVT_RESULTS="$PVT_RESULTS$line
"
            # Extract gain and PM
            gain=$(echo "$line" | sed 's/.*gain=//; s/ dB.*//')
            pm=$(echo "$line" | sed 's/.*PM=//; s/ deg.*//')

            # Check pass/fail (gain >= 60 dB AND PM >= 55 deg)
            fail=$(python3 -c "
g = float('$gain')
p = float('$pm')
if g < 60 or p < 55 or p <= 0:
    print('FAIL')
else:
    print('PASS')
" 2>/dev/null)
            if [ "$fail" = "FAIL" ]; then
                PVT_ALL_PASS=0
                echo "  ^^^ FAIL (gain >= 60 dB AND PM >= 55 deg required)"
            fi
        fi
    done < "$TMPDIR/pvt_${corner}.out"
done

echo "pvt_all_pass: $PVT_ALL_PASS"
echo ""

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
