#!/bin/bash
# Overnight simulation runner for SAR ADC v3
# Runs TB3 (DNL/INL), TB4 (ENOB), TB5-TB8 and writes results
set -e
cd /home/ubuntu/analog-ai-chips/vibrosense/07_adc_v3

RESULTS="RESULTS_OVERNIGHT.md"
echo "# SAR ADC v3 — Overnight Simulation Results" > $RESULTS
echo "" >> $RESULTS
echo "Started: $(date)" >> $RESULTS
echo "" >> $RESULTS

# Kill any stale ngspice
killall ngspice 2>/dev/null || true
rm -f v3_tb3_dnl_inl.dat v3_tb4_enob.dat

##############################################
# STEP 1: Launch long sims in parallel
##############################################
echo "=== Launching TB3 and TB4 ===" | tee -a $RESULTS
nohup ngspice -b v3_tb3_dnl_inl.spice > /tmp/tb3_overnight.log 2>&1 &
TB3_PID=$!
nohup ngspice -b v3_tb4_enob.spice > /tmp/tb4_overnight.log 2>&1 &
TB4_PID=$!
echo "TB3 PID: $TB3_PID, TB4 PID: $TB4_PID" | tee -a $RESULTS

##############################################
# STEP 2: While waiting, run the quick tests
##############################################

# TB5: Power
echo "" >> $RESULTS
echo "## TB5: Active Power" >> $RESULTS
TB5_OUT=$(ngspice -b v3_tb5_power.spice 2>&1)
PAVG=$(echo "$TB5_OUT" | grep -i "pavg\|iavg" | head -2)
echo '```' >> $RESULTS
echo "$PAVG" >> $RESULTS
echo '```' >> $RESULTS
IAVG_VAL=$(echo "$TB5_OUT" | grep -i "iavg" | head -1 | awk '{print $NF}')
POWER_UW=$(python3 -c "print(f'{abs(float(\"$IAVG_VAL\"))*1.8*1e6:.1f}')" 2>/dev/null || echo "?")
echo "Power: ${POWER_UW} µW (target <100 µW)" >> $RESULTS
if python3 -c "exit(0 if float('$POWER_UW') < 100 else 1)" 2>/dev/null; then
    echo "**PASS**" >> $RESULTS
else
    echo "**FAIL**" >> $RESULTS
fi

# TB6: Sleep Power
echo "" >> $RESULTS
echo "## TB6: Sleep Power" >> $RESULTS
TB6_OUT=$(ngspice -b v3_tb6_sleep.spice 2>&1)
SLEEP_MEAS=$(echo "$TB6_OUT" | grep -i "isleep\|psleep" | head -2)
echo '```' >> $RESULTS
echo "$SLEEP_MEAS" >> $RESULTS
echo '```' >> $RESULTS

# TB7: Wakeup
echo "" >> $RESULTS
echo "## TB7: Wakeup Time" >> $RESULTS
TB7_OUT=$(ngspice -b v3_tb7_wakeup.spice 2>&1)
WAKEUP_MEAS=$(echo "$TB7_OUT" | grep -iE "wake|valid|sleep" | head -5)
echo '```' >> $RESULTS
echo "$WAKEUP_MEAS" >> $RESULTS
echo '```' >> $RESULTS

# TB8: Corners
echo "" >> $RESULTS
echo "## TB8: Corner Analysis" >> $RESULTS
echo '```' >> $RESULTS
for corner in tt ss ff sf fs; do
    sed "s/\.lib sky130_v3.lib.spice tt/.lib sky130_v3.lib.spice $corner/" v3_tb1b_two_conv.spice > /tmp/tb8_${corner}.spice
    COUT=$(ngspice -b /tmp/tb8_${corner}.spice 2>&1)

    c1=0; c2=0
    for bit in 7 6 5 4 3 2 1 0; do
        val=$(echo "$COUT" | grep "c1_b${bit} " | grep -oP '[\-\d\.eE\+]+$' | head -1)
        if python3 -c "exit(0 if float('$val') > 0.9 else 1)" 2>/dev/null; then
            c1=$((c1 + (1 << bit)))
        fi
        val=$(echo "$COUT" | grep "c2_b${bit} " | grep -oP '[\-\d\.eE\+]+$' | head -1)
        if python3 -c "exit(0 if float('$val') > 0.9 else 1)" 2>/dev/null; then
            c2=$((c2 + (1 << bit)))
        fi
    done

    e1=$((c1 - 156)); e2=$((c2 - 64))
    s1="PASS"; s2="PASS"
    [ ${e1#-} -gt 5 ] && s1="FAIL"
    [ ${e2#-} -gt 5 ] && s2="FAIL"
    printf "%s: Conv1=%3d (err %+d %s) Conv2=%3d (err %+d %s)\n" "$corner" "$c1" "$e1" "$s1" "$c2" "$e2" "$s2" >> $RESULTS
done
echo '```' >> $RESULTS

##############################################
# STEP 3: Wait for TB3/TB4
##############################################
echo "" >> $RESULTS
echo "## Waiting for TB3/TB4..." >> $RESULTS
echo "Waiting started: $(date)" >> $RESULTS

# Wait for both processes to finish (no polling, just wait)
wait $TB3_PID 2>/dev/null
wait $TB4_PID 2>/dev/null

echo "Waiting finished: $(date)" >> $RESULTS

##############################################
# STEP 4: Analyze TB3 (DNL/INL)
##############################################
echo "" >> $RESULTS
echo "## TB3: DNL/INL (Code Density)" >> $RESULTS
if [ -f v3_tb3_dnl_inl.dat ]; then
    echo '```' >> $RESULTS
    python3 v3_analyze_tb3.py v3_tb3_dnl_inl.dat 2>&1 | tee -a $RESULTS
    echo '```' >> $RESULTS
else
    echo "**TB3 FAILED — no output file**" >> $RESULTS
    echo "Log tail:" >> $RESULTS
    echo '```' >> $RESULTS
    tail -20 /tmp/tb3_overnight.log >> $RESULTS 2>&1
    echo '```' >> $RESULTS
fi

##############################################
# STEP 5: Analyze TB4 (ENOB)
##############################################
echo "" >> $RESULTS
echo "## TB4: ENOB (FFT)" >> $RESULTS
if [ -f v3_tb4_enob.dat ]; then
    echo '```' >> $RESULTS
    python3 v3_analyze_tb4.py v3_tb4_enob.dat 2>&1 | tee -a $RESULTS
    echo '```' >> $RESULTS
else
    echo "**TB4 FAILED — no output file**" >> $RESULTS
    echo "Log tail:" >> $RESULTS
    echo '```' >> $RESULTS
    tail -20 /tmp/tb4_overnight.log >> $RESULTS 2>&1
    echo '```' >> $RESULTS
fi

##############################################
# STEP 6: Summary
##############################################
echo "" >> $RESULTS
echo "## Completed" >> $RESULTS
echo "Finished: $(date)" >> $RESULTS
echo "" >> $RESULTS
echo "Check RESULTS_OVERNIGHT.md for all results." >> $RESULTS

##############################################
# STEP 7: Commit
##############################################
cd /home/ubuntu/analog-ai-chips
git add vibrosense/07_adc_v3/
git commit -m "design(sar_adc_v3): overnight TB3/TB4/TB5-TB8 results — Cunit=200fF, 4x switches

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>" || true

echo ""
echo "=== ALL DONE ==="
echo "Results in: vibrosense/07_adc_v3/RESULTS_OVERNIGHT.md"
