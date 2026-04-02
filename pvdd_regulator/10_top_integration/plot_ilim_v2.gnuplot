#!/usr/bin/gnuplot
# Current limit foldback characteristic — discrete steady-state points
set terminal png size 1200,800 enhanced font 'Arial,14'
set output 'ilim_plot_v2.png'

set title "PVDD LDO Current Limit — Foldback Characteristic\n(Discrete steady-state points, 20ms settling per point)" font 'Arial,16'
set xlabel "Load Current I_{load} (mA)" font 'Arial,14'
set ylabel "Output Voltage PVDD (V)" font 'Arial,14'

set grid
set key top right box
set xrange [0:110]
set yrange [0:5.5]

set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.2
set style line 2 lc rgb '#dd181f' lt 1 lw 2 pt 5 ps 1.2
set style line 3 lc rgb '#00a000' lt 1 lw 2 pt 9 ps 1.2

# Spec lines
set arrow from 0,4.825 to 110,4.825 nohead lt 2 lw 1 lc rgb '#888888'
set arrow from 0,5.175 to 110,5.175 nohead lt 2 lw 1 lc rgb '#888888'
set label "4.825V min" at 85,4.7 font 'Arial,10' tc rgb '#888888'
set label "5.175V max" at 85,5.25 font 'Arial,10' tc rgb '#888888'

plot 'ilim_plot_data.txt' using ($4*1000):3 every ::1::23 with linespoints ls 1 title 'TT 27°C', \
     'ilim_plot_data.txt' using ($4*1000):3 every ::24::46 with linespoints ls 2 title 'SS 150°C', \
     'ilim_plot_data.txt' using ($4*1000):3 every ::47::69 with linespoints ls 3 title 'FF -40°C'
