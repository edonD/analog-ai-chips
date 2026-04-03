#!/bin/bash
# Current limit DC characterization via transient simulation
# Each point: BVDD ramp from 0, settle 20ms, apply load, measure at 25ms
# This avoids the .OP bi-stable equilibrium bug

cd "$(dirname "$0")"
echo "# iload_ma pvdd_v" > ilim_tran_data.txt

for iload in 0 0.001 0.005 0.01 0.015 0.02 0.025 0.03 0.035 0.04 0.042 0.044 0.046 0.048 0.049 0.050 0.051 0.052 0.053 0.054 0.055 0.056 0.058 0.060 0.065 0.070 0.080 0.100; do
  iload_ma=$(echo "$iload * 1000" | bc -l | sed 's/0*$//' | sed 's/\.$//')

  cat > tb_ilim_pt.spice << SPEOF
* Current limit point: Iload=${iload}A
.title ILIM_PT
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
Iload pvdd 0 PWL(0 0 19.999m 0 20m ${iload} 100 ${iload})
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator
.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 5u 25m uic
.control
run
let pvdd_final = v(pvdd)[length(v(pvdd))-1]
echo "RESULT: \$&pvdd_final"
quit
.endc
.end
SPEOF

  pvdd=$(ngspice -b tb_ilim_pt.spice 2>&1 | grep "^RESULT:" | awk '{print $2}')

  # Clamp negative to 0
  if [ -z "$pvdd" ]; then
    pvdd="0"
  fi
  is_neg=$(echo "$pvdd < 0" | bc -l 2>/dev/null)
  if [ "$is_neg" = "1" ]; then
    pvdd="0"
  fi

  echo "${iload_ma} ${pvdd}" >> ilim_tran_data.txt
  echo "Iload=${iload_ma}mA -> PVDD=${pvdd}V"
done

echo "=== All points done ==="
rm -f tb_ilim_pt.spice
