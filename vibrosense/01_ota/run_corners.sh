#!/bin/bash
# Run AC analysis across all 5 process corners
cd /home/ubuntu/analog-ai-chips/vibrosense/01_ota

echo "======================================================"
echo "  Corner Analysis - VibroSense OTA"
echo "======================================================"

for corner in tt ss ff sf fs; do
    # Create corner-specific testbench
    sed "s/\.lib \"sky130_minimal.lib.spice\" tt/.lib \"sky130_minimal.lib.spice\" $corner/" tb_ota_corners.spice > tb_corner_${corner}.spice
    sed -i "s/CORNER=TT/CORNER=${corner^^}/" tb_corner_${corner}.spice

    # Run
    result=$(/usr/bin/ngspice -b tb_corner_${corner}.spice 2>&1 | grep "^CORNER=")
    echo "$result"
done

echo ""
echo "======================================================"
echo "  Temperature Sweep (TT corner)"
echo "======================================================"

for temp in -40 27 85; do
    # Create temp-specific testbench
    cp tb_ota_corners.spice tb_temp_${temp}.spice
    sed -i "s/CORNER=TT/TEMP=${temp}C/" tb_temp_${temp}.spice
    # Add .temp before .ac
    sed -i "/^\.ac/i .temp $temp" tb_temp_${temp}.spice

    result=$(/usr/bin/ngspice -b tb_temp_${temp}.spice 2>&1 | grep "^TEMP=")
    echo "$result"
done

echo "======================================================"
