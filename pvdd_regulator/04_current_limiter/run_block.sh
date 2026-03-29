#!/usr/bin/env bash
# run_block.sh — Block 04: Current Limiter (v3 — honest testbench methodology)
# Runs all testbenches and outputs metrics for evaluate.py
# v3 fixes: real pvdd_impact A/B, fair short-circuit, 3-window oscillation, rgate sweep
set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 04: Current Limiter (v3) ==="
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

# ===== Transient Test (v3: three oscillation windows) =====
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

# Print all ripple data from all three windows
echo "$tran_out" | grep -E "^(early_|mid_|gate_ripple|current_ripple|WARNING)" || true
echo ""

# ===== Normal Operation Test (v3: real A/B pvdd_impact measurement) =====
echo "--- Running tb_ilim_normal.spice + tb_ilim_normal_nolim.spice ---"
normal_out=$(ngspice -b tb_ilim_normal.spice 2>&1)

quiescent=$(echo "$normal_out" | grep "^sense_quiescent_uA:" | tail -1 | awk '{print $2}')
if [ -n "$quiescent" ]; then
    echo "sense_quiescent_uA: $quiescent"
else
    echo "sense_quiescent_uA: UNMEASURED"
fi

# Run no-limiter variant for A/B comparison
ngspice -b tb_ilim_normal_nolim.spice 2>&1 > /dev/null

# Compute pvdd_impact from actual with/without data
impact_out=$(python3 parse_pvdd_impact.py 2>&1)
impact_val=$(echo "$impact_out" | grep "^pvdd_impact_mV:" | awk '{print $2}')
if [ -n "$impact_val" ]; then
    echo "pvdd_impact_mV: $impact_val"
    # Print detail line too
    echo "$impact_out" | grep "Vgate_ref" || true
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

# ===== Short Circuit Test (v3: fair A/B, pvdd=0.1V, same Rgate) =====
echo "--- Running tb_ilim_short.spice (with limiter, pvdd=0.1V) ---"
short_with_out=$(ngspice -b tb_ilim_short.spice 2>&1)
short_with=$(echo "$short_with_out" | grep "^short_circuit_mA:" | tail -1 | awk '{print $2}')
if [ -n "$short_with" ]; then
    echo "short_circuit_with_limiter_mA: $short_with"
else
    echo "short_circuit_with_limiter_mA: UNMEASURED"
fi
echo "$short_with_out" | grep -E "^gate_int|^ilim_flag" || true

echo "--- Running tb_ilim_short_nolim.spice (without limiter, pvdd=0.1V) ---"
short_nolim_out=$(ngspice -b tb_ilim_short_nolim.spice 2>&1)
short_without=$(echo "$short_nolim_out" | grep "^short_circuit_mA:" | tail -1 | awk '{print $2}')
if [ -n "$short_without" ]; then
    echo "short_circuit_without_limiter_mA: $short_without"
else
    echo "short_circuit_without_limiter_mA: UNMEASURED"
fi

# Compute ratio
if [ -n "$short_with" ] && [ -n "$short_without" ]; then
    ratio=$(python3 -c "w=float('$short_with'); wo=float('$short_without'); print(f'{w/wo:.4f}' if wo != 0 else 'INF')")
    echo "short_circuit_reduction_ratio: $ratio"
fi
echo ""

# ===== I-V Curve =====
echo "--- Running tb_ilim_iv.spice ---"
ngspice -b tb_ilim_iv.spice 2>&1 | grep -E "ilim|iv" || true
echo ""

# ===== Rgate Dependence Sweep (v3: informational) =====
echo "--- Running tb_ilim_rgate_sweep.spice ---"
ngspice -b tb_ilim_rgate_sweep.spice 2>&1 | grep "^rgate_" || true
echo ""

echo "--- Evaluation ---"
python3 evaluate.py
echo ""
echo "Run finished: $(date)"
