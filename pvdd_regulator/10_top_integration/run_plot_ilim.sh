#!/bin/bash
# Generate current limit plot data for all 3 corners
# Each point is a separate steady-state simulation

CORNERS="tt:27 ss:150 ff:-40"

for CT in $CORNERS; do
    CORNER=$(echo $CT | cut -d: -f1)
    TEMP=$(echo $CT | cut -d: -f2)
    OUTFILE="ilim_plot_${CORNER}_${TEMP}.dat"
    echo "# Iload_mA PVDD_V" > "$OUTFILE"
    echo "=== Generating ${CORNER} ${TEMP}C ==="

    for IMA in 0 1 2 5 10 15 20 25 30 35 40 42 44 46 48 50 51 52 53 54 55 56 57 58 59 60 62 65 70 75 80 85 90 95 100 110 120 130 140 150; do
        IAMPS=$(echo "$IMA" | awk '{printf "%.6f", $1/1000}')
        sed -e "s/ILOAD_AMPS/$IAMPS/g" -e "s/ILOAD_MA/$IMA/g" -e "s/CORNER_VAL/$CORNER/g" -e "s/TEMP_LINE/.temp $TEMP/g" tb_ilim_char.spice > tb_ilim_char_run.spice
        PVDD=$(timeout 300 ngspice -b tb_ilim_char_run.spice 2>&1 | grep "pvdd_final" | tail -1 | awk '{print $NF}')
        PVDD_V=$(echo "$PVDD" | awk '{v=$1; if(v<0) v=0; printf "%.4f", v}')
        echo "$IMA $PVDD_V" >> "$OUTFILE"
        echo -n "."
    done
    echo ""
done

# Generate gnuplot script
cat > plot_ilim.gnuplot << 'GNUEOF'
set terminal pngcairo size 1200,800 enhanced font "Sans,14"
set output "plot_current_limit.png"

set title "PVDD 5V LDO — Current Limit Characteristic (v6 fix)" font "Sans,18"
set xlabel "Load Current I_{load} (mA)" font "Sans,15"
set ylabel "Output Voltage PVDD (V)" font "Sans,15"

set xrange [0:150]
set yrange [0:6]
set grid

# Spec lines
set arrow from 0,4.825 to 150,4.825 nohead dt 2 lc rgb "gray50" lw 1
set arrow from 0,5.175 to 150,5.175 nohead dt 2 lc rgb "gray50" lw 1
set label "4.825V (-3.5%)" at 105,4.65 font "Sans,10" tc rgb "gray50"
set label "5.175V (+3.5%)" at 105,5.35 font "Sans,10" tc rgb "gray50"

# 50mA marker
set arrow from 50,0 to 50,5.5 nohead dt 3 lc rgb "gray70" lw 1
set label "50mA spec" at 51,0.4 font "Sans,10" tc rgb "gray70"

plot "ilim_plot_tt_27.dat" using 1:2 with linespoints lw 2 pt 7 ps 0.8 lc rgb "#0066CC" title "TT 27°C", \
     "ilim_plot_ss_150.dat" using 1:2 with linespoints lw 2 pt 5 ps 0.8 lc rgb "#CC3300" title "SS 150°C", \
     "ilim_plot_ff_-40.dat" using 1:2 with linespoints lw 2 pt 9 ps 0.8 lc rgb "#009933" title "FF -40°C"
GNUEOF

gnuplot plot_ilim.gnuplot 2>&1
echo "Plot saved: plot_current_limit.png"
