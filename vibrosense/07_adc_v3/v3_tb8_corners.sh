#!/bin/bash
# TB8: Corner Analysis — run TB1b (two consecutive conversions) at all 5 corners
# This verifies both correct code AND DAC reset at every corner

echo "=== TB8: Corner Analysis ==="

for corner in tt ss ff sf fs; do
    echo "--- Corner: $corner ---"

    # Create corner-specific testbench
    sed "s/\.lib sky130_v3.lib.spice tt/.lib sky130_v3.lib.spice $corner/" v3_tb1b_two_conv.spice \
        | sed "s/v3_tb1b_two_conv.dat/v3_tb8_${corner}.dat/" > v3_tb8_${corner}.spice

    # Run and extract results
    result=$(ngspice -b v3_tb8_${corner}.spice 2>&1)

    # Extract conversion 1 bits
    c1_code=0
    for bit in 7 6 5 4 3 2 1 0; do
        val=$(echo "$result" | grep "c1_b${bit} " | head -1 | awk '{print $NF}')
        if [ "$(echo "$val > 0.9" | bc -l 2>/dev/null)" = "1" ]; then
            c1_code=$((c1_code + (1 << bit)))
        fi
    done

    # Extract conversion 2 bits
    c2_code=0
    for bit in 7 6 5 4 3 2 1 0; do
        val=$(echo "$result" | grep "c2_b${bit} " | head -1 | awk '{print $NF}')
        if [ "$(echo "$val > 0.9" | bc -l 2>/dev/null)" = "1" ]; then
            c2_code=$((c2_code + (1 << bit)))
        fi
    done

    # Check against expected (conv1: Vin=0.47V→~156, conv2: Vin=0.9V→~64)
    err1=$((c1_code - 156))
    err2=$((c2_code - 64))

    status1="PASS"
    status2="PASS"
    [ ${err1#-} -gt 5 ] && status1="FAIL"
    [ ${err2#-} -gt 5 ] && status2="FAIL"

    printf "  Conv1 (Vin=0.47V): code=%3d ideal=156 error=%+3d %s\n" $c1_code $err1 $status1
    printf "  Conv2 (Vin=0.90V): code=%3d ideal= 64 error=%+3d %s\n" $c2_code $err2 $status2
done
