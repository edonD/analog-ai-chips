#!/bin/bash
# Sweep dummy cap value to find optimal offset correction
# Tests with 5 voltages: 0.0V, 0.3V, 0.6V, 0.9V, 1.2V
# Ideal codes:           255,  192,  128,   64,    0

decode_code() {
    local prefix=$1
    local result=$2
    local code=0
    for bit in 7 6 5 4 3 2 1 0; do
        val=$(echo "$result" | grep "${prefix}_b${bit} " | head -1 | awk '{print $NF}')
        if python3 -c "exit(0 if float('$val') > 0.9 else 1)" 2>/dev/null; then
            code=$((code + (1 << bit)))
        fi
    done
    echo $code
}

echo "Dummy  V=0.0 V=0.3 V=0.6 V=0.9 V=1.2  AvgErr  EvenCodes"
echo "-----  ----- ----- ----- ----- -----  ------  ---------"

for dummy_mult in "0.01" "0.25" "0.5" "0.75" "1.0" "1.5"; do
    # Create modified DAC with different dummy cap
    sed "s/Cdummy top gnd_node {1\*Cunit}/Cdummy top gnd_node {${dummy_mult}*Cunit}/" v3_cap_dac.spice > /tmp/v3_cap_dac_cal.spice

    # Create calibration testbench using modified DAC
    sed "s|.include v3_cap_dac.spice|.include /tmp/v3_cap_dac_cal.spice|" v3_tb_calibrate.spice > /tmp/v3_cal.spice

    result=$(ngspice -b /tmp/v3_cal.spice 2>&1)

    c1=$(decode_code "c1" "$result")
    c2=$(decode_code "c2" "$result")
    c3=$(decode_code "c3" "$result")
    c4=$(decode_code "c4" "$result")
    c5=$(decode_code "c5" "$result")

    # Ideal: 255, 192, 128, 64, 0
    e1=$((c1-255)); e2=$((c2-192)); e3=$((c3-128)); e4=$((c4-64)); e5=$((c5-0))
    avg_err=$(python3 -c "print(f'{(abs($e1)+abs($e2)+abs($e3)+abs($e4)+abs($e5))/5:.1f}')")

    # Count even codes
    even=0
    for c in $c1 $c2 $c3 $c4 $c5; do
        [ $((c % 2)) -eq 0 ] && even=$((even+1))
    done

    printf "%5s  %3d(%+d) %3d(%+d) %3d(%+d) %3d(%+d) %3d(%+d)  %5s    %d/5\n" \
        "${dummy_mult}C" $c1 $e1 $c2 $e2 $c3 $e3 $c4 $e4 $c5 $e5 "$avg_err" $even
done
