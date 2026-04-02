#!/bin/bash
# Full PVT verification v2 — fixed measurement for load transient
# Uses meas tran ... FROM= TO= for correct undershoot measurement
set -e

WD="/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration"
cd "$WD"

CORNERS="tt ss ff sf fs"
TEMPS="-40 27 150"
RESULTS_DIR="$WD/pvt_v2_results"
mkdir -p "$RESULTS_DIR"

gen_header() {
    local corner=$1 temp=$2
    cat <<'SPICE'
.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
SPICE
    echo ".lib \"../sky130.lib.spice\" ${corner}"
    echo ".temp ${temp}"
    cat <<'SPICE'
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
SPICE
}

# Test A: DC + Startup (same as before, works correctly)
gen_test_a() {
    local corner=$1 temp=$2
    local fname="$RESULTS_DIR/tb_a_${corner}_${temp}.spice"
    cat > "$fname" <<EOF
* Test A: DC + Startup — ${corner} ${temp}C
.title PVT_A_${corner}_${temp}
$(gen_header $corner $temp)
Vbvdd bvdd 0 PWL(0 0 10u 7 100m 7)
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven_ret en_ret 0 0
Rload pvdd 0 5000
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator
.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 2u 20m uic
.control
run
meas tran pvdd_final FIND v(pvdd) AT=20m
meas tran pvdd_peak MAX v(pvdd)
quit
.endc
.end
EOF
    echo "$fname"
}

# Test B: Load transient — FIXED: measure MIN only from 10ms to 20ms
gen_test_b() {
    local corner=$1 temp=$2
    local fname="$RESULTS_DIR/tb_b_${corner}_${temp}.spice"
    cat > "$fname" <<EOF
* Test B: Load Transient — ${corner} ${temp}C
.title PVT_B_${corner}_${temp}
$(gen_header $corner $temp)
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
meas tran pvdd_pre FIND v(pvdd) AT=9.5m
meas tran pvdd_min MIN v(pvdd) FROM=10m TO=20m
quit
.endc
.end
EOF
    echo "$fname"
}

# Test C: Current limit (unchanged)
gen_test_c() {
    local corner=$1 temp=$2
    local fname="$RESULTS_DIR/tb_c_${corner}_${temp}.spice"
    cat > "$fname" <<EOF
* Test C: Current Limit — ${corner} ${temp}C
.title PVT_C_${corner}_${temp}
$(gen_header $corner $temp)
Vbvdd bvdd 0 PWL(0 0 10u 7 100m 7)
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven_ret en_ret 0 0
Rload pvdd 0 0.1
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator
.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 2u 20m uic
.control
run
meas tran pvdd_final FIND v(pvdd) AT=20m
quit
.endc
.end
EOF
    echo "$fname"
}

echo "==== Generating testbenches ===="
for corner in $CORNERS; do
    for temp in $TEMPS; do
        gen_test_a $corner $temp > /dev/null
        gen_test_b $corner $temp > /dev/null
        gen_test_c $corner $temp > /dev/null
    done
done

echo "==== Running Test A (15 corners) ===="
for corner in $CORNERS; do
    for temp in $TEMPS; do
        fname="$RESULTS_DIR/tb_a_${corner}_${temp}.spice"
        echo -n "  ${corner} ${temp}C... "
        timeout 180 ngspice -b "$fname" > "$RESULTS_DIR/a_${corner}_${temp}.log" 2>&1 && echo "OK" || echo "ERR"
    done
done

echo "==== Running Test B (15 corners) ===="
for corner in $CORNERS; do
    for temp in $TEMPS; do
        fname="$RESULTS_DIR/tb_b_${corner}_${temp}.spice"
        echo -n "  ${corner} ${temp}C... "
        timeout 180 ngspice -b "$fname" > "$RESULTS_DIR/b_${corner}_${temp}.log" 2>&1 && echo "OK" || echo "ERR"
    done
done

echo "==== Running Test C (15 corners) ===="
for corner in $CORNERS; do
    for temp in $TEMPS; do
        fname="$RESULTS_DIR/tb_c_${corner}_${temp}.spice"
        echo -n "  ${corner} ${temp}C... "
        timeout 180 ngspice -b "$fname" > "$RESULTS_DIR/c_${corner}_${temp}.log" 2>&1 && echo "OK" || echo "ERR"
    done
done

echo "==== All simulations complete ===="
