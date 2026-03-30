#!/usr/bin/env bash
# generate_plot_data.sh — Run all simulations needed for README plots
# Saves data files in plots/ directory for plot_all.py
set -e
cd "$(dirname "$0")"
mkdir -p plots

# Common preamble for all testbenches
PREAMBLE='
.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "../sky130.lib.spice" tt
.include "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/ngspice/parameters/invariant.spice"
.include "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__nfet_01v8__tt.pm3.spice"
.include "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__pfet_01v8__tt.corner.spice"
.include ../00_error_amp/design.cir
.include ../01_pass_device/design.cir
.include ../02_feedback_network/design.cir
.include ../03_compensation/design.cir
.include ../04_current_limiter/design.cir
.include ../05_uv_ov_comparators/design.cir
.include ../06_level_shifter/design.cir
.include ../07_zener_clamp/design.cir
.include ../08_mode_control/design.cir
.include ../09_startup/design.cir
'

CIRCUIT='
XM_pass gate bvdd pvdd pass_device
Rss avbg vref_ss 200k
Css vref_ss 0 30n
XEA vref_ss vfb ea_out pvdd 0 ibias ea_en error_amp
XFB pvdd vfb 0 feedback_network
XCOMP ea_out pvdd 0 compensation
XILIM gate bvdd pvdd 0 ilim_flag current_limiter
XUV pvdd avbg uv_flag svdd 0 uvov_en uv_comparator
XOV pvdd avbg ov_flag svdd 0 uvov_en ov_comparator
XZC pvdd 0 zener_clamp
XMC bvdd pvdd svdd 0 avbg en_ret bypass_en mc_ea_en ref_sel uvov_en ilim_en pass_off mode_control
XSU bvdd pvdd gate 0 avbg startup_done ea_en ea_out startup
XLS_EN en en_bvdd bvdd svdd 0 level_shifter_up
Cint pvdd 0 200e-12
'

STIM='
Vavbg avbg 0 1.226
Ibias ibias 0 DC 1u
Vsvdd svdd 0 2.2
Ven en 0 DC 2.2
Ven_ret en_ret 0 0
'

OPTS='.option reltol=1e-4 abstol=1e-12 vntol=1e-6
.option method=gear maxord=2
.option itl1=500 itl2=500 itl4=500'

# ============================================================
# 1. DC REGULATION: PVDD vs load (multiple Rload sims)
# ============================================================
echo "--- 1. DC Regulation ---"
for R in 100000 10000 5000 2000 1000 500 250 100; do
  iload=$(awk "BEGIN{printf \"%.4f\", 5.0/$R*1000}")
  cat > /tmp/tb_dc_${R}.spice << EOF
${PREAMBLE}
${CIRCUIT}
Vbvdd bvdd 0 PWL(0 0 7u 7 200m 7)
${STIM}
Rload pvdd 0 ${R}
Cout pvdd 0 1u
${OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 1u 80m uic
.meas tran vpvdd avg V(pvdd) from=60m to=80m
.control
run
quit
.endc
.end
EOF
  v=$(ngspice -b /tmp/tb_dc_${R}.spice 2>&1 | grep "vpvdd" | awk '{print $3}')
  echo "${iload} ${v}" >> plots/dc_regulation.dat
  echo "  Rload=${R} (${iload}mA): PVDD=${v}"
done

# ============================================================
# 2. STARTUP WAVEFORM
# ============================================================
echo "--- 2. Startup Waveform ---"
cat > /tmp/tb_startup_plot.spice << EOF
${PREAMBLE}
${CIRCUIT}
Vbvdd bvdd 0 PWL(0 0 7u 7 200m 7)
${STIM}
Rload pvdd 0 500
Cout pvdd 0 1u
${OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 0.5u 2m uic
.control
run
wrdata plots/startup_waveform v(bvdd) v(pvdd) v(gate) v(ea_en)
quit
.endc
.end
EOF
ngspice -b /tmp/tb_startup_plot.spice 2>&1 | tail -3

# ============================================================
# 3. LINE TRANSIENT: BVDD step ±500mV
# ============================================================
echo "--- 3. Line Transient ---"
cat > /tmp/tb_line_tran.spice << EOF
${PREAMBLE}
${CIRCUIT}
Vbvdd bvdd 0 PWL(0 0 7u 7 50m 7 50.001m 7.5 55m 7.5 55.001m 6.5 60m 6.5 60.001m 7 80m 7)
${STIM}
Rload pvdd 0 500
Cout pvdd 0 1u
${OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 0.5u 80m uic
.control
run
wrdata plots/line_transient v(bvdd) v(pvdd)
quit
.endc
.end
EOF
ngspice -b /tmp/tb_line_tran.spice 2>&1 | tail -3

# ============================================================
# 4. PVDD vs TEMPERATURE
# ============================================================
echo "--- 4. Temperature Coefficient ---"
> plots/pvdd_tc.dat
for temp in -40 -20 0 20 27 40 60 85 100 125 150; do
  cat > /tmp/tb_tc_${temp}.spice << EOF
${PREAMBLE}
${CIRCUIT}
Vbvdd bvdd 0 PWL(0 0 7u 7 200m 7)
${STIM}
Rload pvdd 0 500
Cout pvdd 0 1u
${OPTS}
.temp ${temp}
.ic V(pvdd)=0 V(bvdd)=0
.tran 1u 80m uic
.meas tran vpvdd avg V(pvdd) from=60m to=80m
.control
run
quit
.endc
.end
EOF
  v=$(ngspice -b /tmp/tb_tc_${temp}.spice 2>&1 | grep "vpvdd" | awk '{print $3}')
  echo "${temp} ${v}" >> plots/pvdd_tc.dat
  echo "  ${temp}°C: ${v}V"
done

# ============================================================
# 5. PVT SUMMARY: 5 corners × 3 temperatures
# ============================================================
echo "--- 5. PVT Summary ---"
> plots/pvt_summary.dat
for corner in tt ss ff; do
  for temp in -40 27 150; do
    cornerlabel="${corner}_${temp}"
    # Use the right 01v8 corner file
    if [ "$corner" = "tt" ]; then c01v8n="tt.pm3"; c01v8p="tt.corner"; fi
    if [ "$corner" = "ss" ]; then c01v8n="ss.corner"; c01v8p="ss.corner"; fi
    if [ "$corner" = "ff" ]; then c01v8n="ff.corner"; c01v8p="ff.corner"; fi
    cat > /tmp/tb_pvt_${cornerlabel}.spice << EOF
.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "../sky130.lib.spice" ${corner}
.include "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/ngspice/parameters/invariant.spice"
.include "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__nfet_01v8__${c01v8n}.spice"
.include "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.ref/sky130_fd_pr/spice/sky130_fd_pr__pfet_01v8__${c01v8p}.spice"
.include ../00_error_amp/design.cir
.include ../01_pass_device/design.cir
.include ../02_feedback_network/design.cir
.include ../03_compensation/design.cir
.include ../04_current_limiter/design.cir
.include ../05_uv_ov_comparators/design.cir
.include ../06_level_shifter/design.cir
.include ../07_zener_clamp/design.cir
.include ../08_mode_control/design.cir
.include ../09_startup/design.cir
${CIRCUIT}
Vbvdd bvdd 0 PWL(0 0 7u 7 200m 7)
${STIM}
Rload pvdd 0 500
Cout pvdd 0 1u
${OPTS}
.temp ${temp}
.ic V(pvdd)=0 V(bvdd)=0
.tran 1u 80m uic
.meas tran vpvdd avg V(pvdd) from=60m to=80m
.control
run
quit
.endc
.end
EOF
    v=$(ngspice -b /tmp/tb_pvt_${cornerlabel}.spice 2>&1 | grep "vpvdd" | awk '{print $3}')
    echo "${corner} ${temp} ${v}" >> plots/pvt_summary.dat
    echo "  ${cornerlabel}: ${v}V"
  done
done

# ============================================================
# 6. COLD CRANK: BVDD dip and recovery
# ============================================================
echo "--- 6. Cold Crank ---"
cat > /tmp/tb_cold_crank.spice << EOF
${PREAMBLE}
${CIRCUIT}
Vbvdd bvdd 0 PWL(0 0 7u 7 40m 7 40.5m 4.0 41m 3.5 42m 4.0 43m 7 80m 7)
${STIM}
Rload pvdd 0 500
Cout pvdd 0 1u
${OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 0.5u 80m uic
.control
run
wrdata plots/cold_crank v(bvdd) v(pvdd)
quit
.endc
.end
EOF
ngspice -b /tmp/tb_cold_crank.spice 2>&1 | tail -3

# ============================================================
# 7. MODE TRANSITIONS: BVDD ramp up and down
# ============================================================
echo "--- 7. Mode Transitions ---"
cat > /tmp/tb_modes.spice << EOF
${PREAMBLE}
${CIRCUIT}
Vbvdd bvdd 0 PWL(0 0 20m 10.5 40m 10.5 60m 0)
${STIM}
Rload pvdd 0 500
Cout pvdd 0 1u
${OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 5u 60m uic
.control
run
wrdata plots/mode_transitions v(bvdd) v(pvdd) v(ea_en) v(bypass_en) v(uvov_en)
quit
.endc
.end
EOF
ngspice -b /tmp/tb_modes.spice 2>&1 | tail -3

# ============================================================
# 8. AVBG sweep: PVDD vs reference voltage
# ============================================================
echo "--- 8. AVBG sweep ---"
> plots/avbg_sweep.dat
for avbg in 1.15 1.18 1.20 1.226 1.25 1.28 1.30; do
  cat > /tmp/tb_avbg_${avbg}.spice << EOF
${PREAMBLE}
${CIRCUIT}
Vbvdd bvdd 0 PWL(0 0 7u 7 200m 7)
Vavbg avbg 0 ${avbg}
Ibias ibias 0 DC 1u
Vsvdd svdd 0 2.2
Ven en 0 DC 2.2
Ven_ret en_ret 0 0
Rload pvdd 0 500
Cout pvdd 0 1u
${OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 1u 80m uic
.meas tran vpvdd avg V(pvdd) from=60m to=80m
.control
run
quit
.endc
.end
EOF
  v=$(ngspice -b /tmp/tb_avbg_${avbg}.spice 2>&1 | grep "vpvdd" | awk '{print $3}')
  echo "${avbg} ${v}" >> plots/avbg_sweep.dat
  echo "  AVBG=${avbg}V: PVDD=${v}V"
done

# ============================================================
# 9. PSRR vs frequency (transient method at multiple freqs)
# ============================================================
echo "--- 9. PSRR vs frequency ---"
> plots/psrr_vs_freq.dat
for freq in 100 1000 10000 100000; do
  period=$(awk "BEGIN{printf \"%.8f\", 1.0/$freq}")
  cat > /tmp/tb_psrr_${freq}.spice << EOF
${PREAMBLE}
${CIRCUIT}
Vbvdd bvdd 0 DC 7.0 SIN(7 0.01 ${freq} 60m)
${STIM}
Rload pvdd 0 500
Cout pvdd 0 1u
${OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran ${period} 70m uic
.meas tran vpmax MAX V(pvdd) from=64m to=70m
.meas tran vpmin MIN V(pvdd) from=64m to=70m
.control
run
quit
.endc
.end
EOF
  result=$(ngspice -b /tmp/tb_psrr_${freq}.spice 2>&1 | grep -E "vpmax|vpmin")
  vpmax=$(echo "$result" | grep "vpmax" | awk '{print $3}')
  vpmin=$(echo "$result" | grep "vpmin" | awk '{print $3}')
  psrr=$(awk "BEGIN{vp=$vpmax-$vpmin; if(vp>0) printf \"%.1f\", 20*log(0.02/vp)/log(10); else print 99}")
  echo "${freq} ${psrr}" >> plots/psrr_vs_freq.dat
  echo "  ${freq}Hz: PSRR=${psrr}dB"
done

echo ""
echo "=== All plot data generated ==="
