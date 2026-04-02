# plot_ilim_char.gnuplot — Foldback current limit characterization
# Input: ilim_plot_data.txt (corner Rload PVDD Iload)
# Output: ilim_plot.png

set terminal pngcairo size 1200,800 enhanced font 'Arial,14'
set output 'ilim_plot.png'

set title "PVDD LDO Current Limit Characterization — Foldback Characteristic" font ',16'
set xlabel "Load Current I_{load} (mA)" font ',14'
set ylabel "Output Voltage PVDD (V)" font ',14'

set grid lw 0.5
set key top right font ',12' box

# Target regulation voltage
set arrow from graph 0, first 5.0 to graph 1, first 5.0 nohead dt 2 lc rgb "gray50" lw 1
set label "V_{target} = 5.0V" at graph 0.02, first 5.1 font ',10' tc rgb "gray50"

set xrange [0:*]
set yrange [0:6]

# Convert Iload from A to mA in the plot
plot \
  'ilim_plot_data.txt' using ($4*1000):3 every ::0 index 0 \
    with linespoints title "TT 27°C" lc rgb "#0060C0" lw 2 pt 7 ps 1.2, \
  '' using ($4*1000):3 every ::0 index 0 \
    with linespoints title "" lc rgb "#0060C0" lw 2 pt 7 ps 1.2, \
  NaN title "" # placeholder

# Since all corners are in one file with labels, filter by corner name
set output 'ilim_plot.png'
replot

# Better approach: use awk-filtered data
set output 'ilim_plot.png'

plot \
  '< awk ''$1=="tt_27"{print $4*1000, $3}'' ilim_plot_data.txt' \
    using 1:2 with linespoints title "TT 27°C" lc rgb "#0060C0" lw 2.5 pt 7 ps 1.3, \
  '< awk ''$1=="ss_150"{print $4*1000, $3}'' ilim_plot_data.txt' \
    using 1:2 with linespoints title "SS 150°C" lc rgb "#C00000" lw 2.5 pt 5 ps 1.3, \
  '< awk ''$1=="ff_m40"{print $4*1000, $3}'' ilim_plot_data.txt' \
    using 1:2 with linespoints title "FF -40°C" lc rgb "#00A000" lw 2.5 pt 9 ps 1.3

set output
