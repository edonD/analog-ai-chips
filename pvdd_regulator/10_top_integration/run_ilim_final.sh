#!/bin/bash
# Final current limit characterization: pure resistive loads, 50ms settle
cd "$(dirname "$0")"
echo "# rload_ohm pvdd_v iload_ma" > ilim_final_data.txt

for rload in 100000 10000 5000 2000 1000 500 333 250 200 167 143 125 111 105 100 95 91 88 83 77 71 67 63 56 50 45 40 30 20 10 5 1 0.5 0.1; do
  cat > tb_ilim_pt.spice << SPEOF
.title ILIM_FINAL
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "sky130_top.lib.spice" tt
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
Vbvdd bvdd 0 PWL(0 0 10u 7 100 7)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Ven_ret en_ret 0 0
Rload pvdd 0 ${rload}
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator
.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 5u 50m uic
.control
run
let pf = v(pvdd)[length(v(pvdd))-1]
echo "RESULT: \$&pf"
quit
.endc
.end
SPEOF

  pvdd=$(ngspice -b tb_ilim_pt.spice 2>&1 | grep "^RESULT:" | awk '{print $2}')
  if [ -z "$pvdd" ]; then pvdd="0"; fi
  is_neg=$(echo "$pvdd < 0" | bc -l 2>/dev/null)
  if [ "$is_neg" = "1" ]; then pvdd="0"; fi
  iload_ma=$(echo "scale=4; $pvdd / $rload * 1000" | bc -l 2>/dev/null || echo "0")
  echo "${rload} ${pvdd} ${iload_ma}" >> ilim_final_data.txt
  echo "R=${rload} -> PVDD=${pvdd}V I=${iload_ma}mA"
done
echo "=== DONE ==="
rm -f tb_ilim_pt.spice
