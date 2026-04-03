#!/bin/bash
# Master simulation runner for all 19 plots
cd /home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration

# --- Plot 1: DC regulation sweep ---
echo "=== SIM: Plot 1 DC sweep ==="
ngspice -b tb_plt_dc_sweep.spice > log_plt1.log 2>&1 &
PID1=$!

# --- Plot 4: Dropout at 10mA ---
echo "=== SIM: Plot 4 dropout 10mA ==="
sed 's/ILOAD_VAL/10m/g' tb_plt_dropout.spice > tb_plt_dropout_10m.spice
sed -i 's/plt4_dropout_bvdd/plt4_do10_bvdd/; s/plt4_dropout_pvdd/plt4_do10_pvdd/' tb_plt_dropout_10m.spice
ngspice -b tb_plt_dropout_10m.spice > log_plt4_10m.log 2>&1 &
PID4a=$!

# --- Plot 4: Dropout at 50mA ---
echo "=== SIM: Plot 4 dropout 50mA ==="
sed 's/ILOAD_VAL/50m/g' tb_plt_dropout.spice > tb_plt_dropout_50m.spice
sed -i 's/plt4_dropout_bvdd/plt4_do50_bvdd/; s/plt4_dropout_pvdd/plt4_do50_pvdd/' tb_plt_dropout_50m.spice
ngspice -b tb_plt_dropout_50m.spice > log_plt4_50m.log 2>&1 &
PID4b=$!

# --- Plot 5: Line reg at 1mA ---
echo "=== SIM: Plot 5 line reg 1mA ==="
sed 's/ILOAD_VAL/1m/g' tb_plt_linereg.spice > tb_plt_linereg_1m.spice
sed -i 's/plt5_linereg_bvdd/plt5_lr1m_bvdd/; s/plt5_linereg_pvdd/plt5_lr1m_pvdd/' tb_plt_linereg_1m.spice
ngspice -b tb_plt_linereg_1m.spice > log_plt5_1m.log 2>&1 &
PID5a=$!

# --- Plot 5: Line reg at 10mA ---
echo "=== SIM: Plot 5 line reg 10mA ==="
sed 's/ILOAD_VAL/10m/g' tb_plt_linereg.spice > tb_plt_linereg_10m.spice
sed -i 's/plt5_linereg_bvdd/plt5_lr10m_bvdd/; s/plt5_linereg_pvdd/plt5_lr10m_pvdd/' tb_plt_linereg_10m.spice
ngspice -b tb_plt_linereg_10m.spice > log_plt5_10m.log 2>&1 &
PID5b=$!

# --- Plot 6: Bode at 0mA (10Meg), 1mA (5k), 10mA (500), 50mA (100) ---
for rval_label in "10000000:0mA" "5000:1mA" "500:10mA" "100:50mA"; do
  rval=${rval_label%%:*}
  label=${rval_label##*:}
  echo "=== SIM: Bode $label ==="
  sed "s/RLOAD_VAL/$rval/g; s/GAIN_FILE/plt6_gain_$label/; s/PHASE_FILE/plt6_phase_$label/" tb_plt_bode_Xma.spice > tb_plt_bode_${label}.spice
  ngspice -b tb_plt_bode_${label}.spice > log_plt6_${label}.log 2>&1 &
done

# --- Plot 7: PSRR at 10mA (reuse existing plot4 data if good, but also run fresh) ---
echo "=== SIM: PSRR 10mA (fresh) ==="
sed "s/RLOAD_VAL/500/; s/PSRR_FILE/plt7_psrr_10mA/" tb_plt_psrr_Xma.spice > tb_plt_psrr_10mA.spice
ngspice -b tb_plt_psrr_10mA.spice > log_plt7.log 2>&1 &

# --- Plot 8: Output impedance ---
echo "=== SIM: Output impedance ==="
ngspice -b tb_plt_zout.spice > log_plt8.log 2>&1 &

# --- Plot 16: Mode control sequence ---
echo "=== SIM: Mode control ==="
ngspice -b tb_plt_mode_ctrl.spice > log_plt16.log 2>&1 &

# --- Plot 17: UV/OV ---
echo "=== SIM: UV/OV ==="
ngspice -b tb_plt_uvov.spice > log_plt17.log 2>&1 &

# --- Plot 18: Clamp IV ---
echo "=== SIM: Clamp IV ==="
ngspice -b tb_plt_clamp.spice > log_plt18.log 2>&1 &

# --- Plot 11: PVT startup (6 corners) ---
for corner_temp in "tt:27" "ss:150" "ff:-40" "ss:27" "ff:150" "fs:150"; do
  corner=${corner_temp%%:*}
  temp=${corner_temp##*:}
  echo "=== SIM: PVT startup ${corner}_${temp} ==="
  sed "s/CORNER/$corner/; s/TEMPVAL/$temp/; s|OUTFILE|plt11_su_${corner}_${temp}.dat|" tb_plt_pvt_startup.spice > tb_plt_pvtsu_${corner}_${temp}.spice
  ngspice -b tb_plt_pvtsu_${corner}_${temp}.spice > log_plt11_${corner}_${temp}.log 2>&1 &
done

# --- PVT DC regulation (15 corners) for Plot 12 bar chart ---
# Use existing tb but with different corners — run quick tran sims
echo "=== SIM: PVT DC reg sweep ==="
cat > tb_plt_pvt_dcreg.spice << 'SPEOF'
* PVT DC Reg — measure PVDD at 10mA for each corner
.title PVT DC Regulation

.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "../sky130.lib.spice" CORNER_PH
.temp TEMP_PH

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
.include design.cir

Vbvdd bvdd 0 7
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 2.2
Ven_ret en_ret 0 0
Iload pvdd 0 10m
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator
.nodeset v(pvdd)=5.0
.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.tran 10u 30m
.control
run
let pvdd_final = v(pvdd)[length(v(pvdd))-1]
echo "PVT_DCREG: CORNER_PH TEMP_PH $&pvdd_final"
quit
.endc
.end
SPEOF

for corner in tt ss ff sf fs; do
  for temp in -40 27 150; do
    sed "s/CORNER_PH/$corner/g; s/TEMP_PH/$temp/g" tb_plt_pvt_dcreg.spice > tb_plt_pvtdc_${corner}_${temp}.spice
    ngspice -b tb_plt_pvtdc_${corner}_${temp}.spice > log_pvtdc_${corner}_${temp}.log 2>&1 &
  done
done

# Wait for everything
echo "Waiting for all simulations..."
wait
echo "=== ALL SIMULATIONS COMPLETE ==="
