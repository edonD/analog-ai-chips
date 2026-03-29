#!/usr/bin/env bash
# run_block.sh — Block 04: Current Limiter (v2 — no hardcoded metrics)
# Runs all testbenches and outputs metrics for evaluate.py
# EVERY metric comes from ngspice simulation output. NO hardcoded values.
set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 04: Current Limiter (v2) ==="
echo "Run started: $(date)"
echo ""

# ===== Trip Point Test (TT 27C) =====
echo "--- Running tb_ilim_trip.spice ---"
result=$(ngspice -b tb_ilim_trip.spice 2>&1 | grep "ilim_tt27_mA" | tail -1 | awk '{print $2}')
if [ -n "$result" ]; then
    echo "ilim_tt27_mA: $result"
else
    echo "ilim_tt27_mA: UNMEASURED"
fi
echo ""

# ===== PVT Corner Tests (SS 150C, FF -40C) =====
echo "--- Running PVT corners ---"
run_corner() {
    local corner=$1
    local temp=$2
    local label="${corner}_${temp}"
    sed -e "s/CORNER_PLACEHOLDER/$corner/g" -e "s/TEMP_PLACEHOLDER/$temp/g" \
        tb_ilim_pvt.spice > "tb_pvt_tmp_${label}.spice"
    local val=$(ngspice -b "tb_pvt_tmp_${label}.spice" 2>&1 | grep "ilim_" | tail -1 | awk '{print $2}')
    rm -f "tb_pvt_tmp_${label}.spice"
    if [ -n "$val" ]; then
        echo "ilim_${label}_mA: $val"
    else
        echo "ilim_${label}_mA: UNMEASURED"
    fi
}

# Key corners for specs.tsc
ss150=$(ngspice -b tb_corner_ss.spice 2>&1 | grep "_mA" | tail -1 | awk '{print $2}')
if [ -n "$ss150" ]; then
    echo "ilim_ss150_mA: $ss150"
else
    echo "ilim_ss150_mA: UNMEASURED"
fi

ffm40=$(ngspice -b tb_corner_ff.spice 2>&1 | grep "_mA" | tail -1 | awk '{print $2}')
if [ -n "$ffm40" ]; then
    echo "ilim_ff_m40_mA: $ffm40"
else
    echo "ilim_ff_m40_mA: UNMEASURED"
fi

# Full 15-corner PVT sweep
for corner in tt ss ff sf fs; do
    for temp in -40 27 150; do
        run_corner "$corner" "$temp"
    done
done
echo ""

# ===== Transient Test =====
echo "--- Running tb_ilim_transient.spice ---"
tran_out=$(ngspice -b tb_ilim_transient.spice 2>&1)

resp=$(echo "$tran_out" | grep "^response_time_us:" | tail -1 | awk '{print $2}')
if [ -n "$resp" ]; then
    echo "response_time_us: $resp"
else
    echo "response_time_us: UNMEASURED"
fi

osc=$(echo "$tran_out" | grep "^no_oscillation:" | tail -1 | awk '{print $2}')
if [ -n "$osc" ]; then
    echo "no_oscillation: $osc"
else
    echo "no_oscillation: UNMEASURED"
fi

# Print additional transient info
echo "$tran_out" | grep -E "ripple_mV|gate_ripple" || true
echo ""

# ===== Normal Operation Test =====
echo "--- Running tb_ilim_normal.spice ---"
normal_out=$(ngspice -b tb_ilim_normal.spice 2>&1)

quiescent=$(echo "$normal_out" | grep "^sense_quiescent_uA:" | tail -1 | awk '{print $2}')
if [ -n "$quiescent" ]; then
    echo "sense_quiescent_uA: $quiescent"
else
    echo "sense_quiescent_uA: UNMEASURED"
fi

impact=$(echo "$normal_out" | grep "^pvdd_impact_mV:" | tail -1 | awk '{print $2}')
if [ -n "$impact" ]; then
    echo "pvdd_impact_mV: $impact"
else
    echo "pvdd_impact_mV: UNMEASURED"
fi
echo ""

# ===== Loop Stability =====
echo "--- Running tb_ilim_lstb.spice ---"
lstb_out=$(ngspice -b tb_ilim_lstb.spice 2>&1)

pm=$(echo "$lstb_out" | grep "^loop_pm_with_limiter_deg:" | tail -1 | awk '{print $2}')
if [ -n "$pm" ]; then
    echo "loop_pm_with_limiter_deg: $pm"
else
    echo "loop_pm_with_limiter_deg: UNMEASURED"
fi
echo ""

# ===== Short Circuit Test =====
echo "--- Running tb_ilim_short.spice ---"
short_out=$(ngspice -b tb_ilim_short.spice 2>&1)
echo "$short_out" | grep -E "^short_circuit|^gate_int|^ilim_flag" || true
echo ""

# ===== I-V Curve =====
echo "--- Running tb_ilim_iv.spice ---"
ngspice -b tb_ilim_iv.spice 2>&1 | grep -E "ilim|iv" || true
echo ""

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
