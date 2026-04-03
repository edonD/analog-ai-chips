#!/bin/bash
# Re-run Test B with wrdata output for proper post-step min measurement
WD="/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration"
cd "$WD"

CORNERS="tt ss ff sf fs"
TEMPS="-40 27 150"
RESULTS_DIR="$WD/pvt_full_results"

for corner in $CORNERS; do
    for temp in $TEMPS; do
        fname="$WD/tb_pvt_b2_${corner}_${temp}.spice"
        datafile="$RESULTS_DIR/b2_${corner}_${temp}_data.txt"
        cat > "$fname" <<EOF
* Test B2: Load transient — ${corner} ${temp}C
.title PVT_B2_${corner}_${temp}

.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "../sky130.lib.spice" ${corner}
.temp ${temp}

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

Vbvdd bvdd 0 PWL(0 0 10u 7 100m 7)
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven_ret en_ret 0 0

Iload pvdd 0 PWL(0 1m 10m 1m 10.001m 10m 20m 10m)

XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator

.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 2u 20m uic

.control
run
wrdata ${datafile} v(pvdd)
quit
.endc
.end
EOF
        echo -n "Running ${corner} ${temp}C ... "
        timeout 180 ngspice -b "$fname" > "$RESULTS_DIR/b2_${corner}_${temp}.log" 2>&1
        if [ $? -eq 0 ]; then
            # Extract pre-step value (~9.99ms) and min after step (>10ms)
            pre=$(awk '$1 >= 9.99e-3 && $1 <= 10.0e-3 { v=$2 } END { print v }' "$datafile")
            post_min=$(awk '$1 >= 10.0e-3 { print $2 }' "$datafile" | sort -g | head -1)
            echo "pre=$pre min=$post_min"
        else
            echo "FAILED"
        fi
    done
done
