#!/usr/bin/env bash
# run_pvt_corners.sh — Run PM at all 5 corners × 3 temps at 10mA load
# Each corner needs a separate ngspice run with different .lib

set -e
cd "$(dirname "$0")"

# Template testbench
create_tb() {
  local corner=$1
  local temp=$2
  local rload=$3
  local tbname="tb_pvt_${corner}_${temp}.spice"

  cat > "$tbname" <<SPICE_EOF
* PVT: corner=$corner temp=$temp Rload=$rload

.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub 0.05f
c1 r1 sub 0.05f
.ends sky130_fd_pr__model__parasitic__res_po

.lib "../sky130.lib.spice" $corner
.temp $temp

.include "../00_error_amp/design.cir"
.include "../01_pass_device/design.cir"
.include "design.cir"

Vbvdd bvdd 0 DC 7.0
Vavbg avbg 0 DC 1.226
Ven   en   0 DC 5.0
Ibias bvdd ibias DC 1u
Xea avbg vfb vout_gate bvdd 0 ibias en error_amp
Xcomp vout_gate pvdd 0 compensation
Xpass vout_gate bvdd pvdd pass_device
Cload pvdd 0 200p
Rload pvdd 0 $rload
Rtop pvdd vfb_dc 314.75k
Rbot vfb_dc 0 102.25k
Rdc vfb_dc vfb 100Meg
Cinj ac_src vfb 1
Vac ac_src 0 AC 1

.nodeset v(pvdd)=5.0 v(vout_gate)=5.5 v(vfb)=1.226
.option reltol=1e-4 abstol=1e-12 vntol=1e-6 gmin=1e-12

.control
  op
  ac dec 200 1 100Meg
  let beta = 0.2452
  let T_db = 20*log10(abs(v(pvdd))+1e-30) + 20*log10(beta)
  let T_ph = 180/PI * cph(v(pvdd)) + 180
  let npts = length(T_db)
  let i = 0
  dowhile i < npts
    if T_ph[i] > 180
      let T_ph[i] = T_ph[i] - 360
    end
    let i = i + 1
  end
  let ugb = 0
  let pm = 0
  let i = 1
  dowhile i < npts
    if ugb = 0
      if T_db[i-1] > 0
        if T_db[i] <= 0
          let ugb = frequency[i]
          let pm = T_ph[i] + 180
        end
      end
    end
    let i = i + 1
  end
  echo "PVT ${corner}_${temp}C_Rload${rload}: PM=\$&pm UGB=\$&ugb"
  quit
.endc
.end
SPICE_EOF

  echo "$tbname"
}

echo "=== PVT Corner Sweep ==="
pm_min=999

for corner in tt ss ff sf fs; do
  for temp in -40 27 150; do
    for rload in 10G 500 100; do
      tbname=$(create_tb "$corner" "$temp" "$rload")
      result=$(ngspice -b "$tbname" 2>&1 | grep "^PVT " || echo "PVT ${corner}_${temp}_${rload}: FAILED")
      echo "$result"
      # Extract PM
      pm_val=$(echo "$result" | grep -oP 'PM=\K[0-9.]+' || echo "0")
      if [ -n "$pm_val" ]; then
        is_lower=$(echo "$pm_val < $pm_min" | bc -l 2>/dev/null || echo "0")
        if [ "$is_lower" = "1" ]; then
          pm_min=$pm_val
        fi
      fi
      rm -f "$tbname"
    done
  done
done

echo "=== PVT Summary ==="
echo "pm_pvt_min_deg: $pm_min"
