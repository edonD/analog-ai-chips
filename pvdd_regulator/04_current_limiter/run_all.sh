#!/usr/bin/env bash
# run_all.sh — Run all current limiter testbenches and extract metrics
set -o pipefail
cd "$(dirname "$0")"

echo "=== Block 04: Current Limiter — Full Run ==="
echo "Run started: $(date)"
echo ""

# Function to run a corner
run_corner() {
    local corner=$1
    local temp=$2
    local label="${corner}_${temp}C"

    sed -e "s/CORNER_PLACEHOLDER/$corner/g" -e "s/TEMP_PLACEHOLDER/$temp/g" \
        tb_ilim_pvt.spice > "tb_pvt_${label}.spice"

    local result=$(ngspice -b "tb_pvt_${label}.spice" 2>&1 | grep "ilim_" | tail -1 | awk '{print $2}')
    echo "ilim_${label}_mA: $result"
    rm -f "tb_pvt_${label}.spice"
}

echo "--- Trip Point: TT 27C ---"
ngspice -b tb_ilim_trip.spice 2>&1 | grep "ilim_tt27_mA"

echo ""
echo "--- PVT Corners ---"
for corner in tt ss ff sf fs; do
    for temp in -40 27 150; do
        run_corner "$corner" "$temp"
    done
done

echo ""
echo "--- Transient Response ---"
ngspice -b tb_ilim_transient.spice 2>&1 | grep -E "response_time|no_oscillation|Peak|Final"

echo ""
echo "--- Normal Operation ---"
ngspice -b tb_ilim_normal.spice 2>&1 | grep -E "pvdd_impact|sense_quiescent|Rpu current"

echo ""
echo "--- Summary ---"
# Extract key metrics for evaluate.py
# These will be in run.log when piped

echo ""
echo "Run finished: $(date)"
