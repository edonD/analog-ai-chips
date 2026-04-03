#!/bin/bash
# Sweep current source loads to characterize current limit
# Usage: ./run_ilim_char.sh [corner] [temp]

CORNER=${1:-tt}
TEMP=${2:-27}

# Load currents in mA
ILOADS_MA="0 1 5 10 15 20 25 30 35 40 45 48 50 52 55 60 70 80 100 120 150"

OUTFILE="ilim_char_${CORNER}_${TEMP}.dat"
echo "# Iload(mA) PVDD(V)" > "$OUTFILE"

for IMA in $ILOADS_MA; do
    # Convert mA to Amps
    IAMPS=$(echo "$IMA" | awk '{printf "%.6f", $1/1000}')

    TBFILE="tb_ilim_char_run.spice"
    sed -e "s/ILOAD_AMPS/$IAMPS/g" \
        -e "s/ILOAD_MA/$IMA/g" \
        -e "s/CORNER_VAL/$CORNER/g" \
        -e "s/TEMP_LINE/.temp $TEMP/g" \
        tb_ilim_char.spice > "$TBFILE"

    OUTPUT=$(timeout 180 ngspice -b "$TBFILE" 2>&1)

    PVDD=$(echo "$OUTPUT" | grep "pvdd_final" | tail -1 | awk '{print $NF}')

    if [ -z "$PVDD" ]; then
        echo "  ${IMA}mA: FAILED"
        continue
    fi

    PVDD_FMT=$(echo "$PVDD" | awk '{printf "%.4f", $1}')
    echo "  ${IMA}mA: PVDD=${PVDD_FMT}V"
    echo "$IMA $PVDD" >> "$OUTFILE"
done

echo ""
echo "=== Results ==="
cat "$OUTFILE"
