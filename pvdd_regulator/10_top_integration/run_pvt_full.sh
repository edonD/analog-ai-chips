#!/bin/bash
# Full PVT verification campaign — 15 corners × 3 tests
# Uses ../sky130.lib.spice which has all corners + proper LV device params

WD="/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration"
cd "$WD"

CORNERS="tt ss ff sf fs"
TEMPS="-40 27 150"
RESULTS_DIR="$WD/pvt_full_results"
mkdir -p "$RESULTS_DIR"

# Common header for all testbenches
gen_header() {
    local corner=$1
    local temp=$2
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

# ============================================================
# Test A: Startup + DC regulation (measures PVDD_final, PVDD_peak)
# ============================================================
gen_test_a() {
    local corner=$1
    local temp=$2
    local fname="$RESULTS_DIR/tb_a_${corner}_${temp}.spice"
    cat > "$fname" <<EOF
* Test A: Startup + DC reg — ${corner} ${temp}C
.title PVT_A_${corner}_${temp}

$(gen_header $corner $temp)

* Supplies — startup ramp
Vbvdd bvdd 0 PWL(0 0 10u 7 100m 7)
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven_ret en_ret 0 0

* Load: 5k (1mA)
Rload pvdd 0 5000

* DUT
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator

.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 2u 20m uic

.control
run
let pvdd_final = v(pvdd)[length(v(pvdd))-1]
let pvdd_peak = vecmax(v(pvdd))
echo "RESULT_A_FINAL ${corner} ${temp} ="
print pvdd_final
echo "RESULT_A_PEAK ${corner} ${temp} ="
print pvdd_peak
quit
.endc
.end
EOF
    echo "$fname"
}

# ============================================================
# Test B: Load transient (1mA → 10mA step)
# ============================================================
gen_test_b() {
    local corner=$1
    local temp=$2
    local fname="$RESULTS_DIR/tb_b_${corner}_${temp}.spice"
    cat > "$fname" <<EOF
* Test B: Load transient — ${corner} ${temp}C
.title PVT_B_${corner}_${temp}

$(gen_header $corner $temp)

* Supplies
Vbvdd bvdd 0 PWL(0 0 10u 7 100m 7)
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven_ret en_ret 0 0

* Load: current step from 1mA to 10mA at 10ms
Iload pvdd 0 PWL(0 1m 10m 1m 10.001m 10m 20m 10m)

* DUT
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator

.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 2u 20m uic

.control
run
* Steady state before step: sample at ~9.5ms (index ~4750 out of 10000)
let n = length(v(pvdd))
let idx_pre = n * 48 / 100
let pvdd_pre = v(pvdd)[idx_pre]
* Min PVDD in second half (after step)
let half = n / 2
let pvdd_post_vec = v(pvdd)[half]
let pvdd_min = vecmin(v(pvdd))
echo "RESULT_B_PRE ${corner} ${temp} ="
print pvdd_pre
echo "RESULT_B_MIN ${corner} ${temp} ="
print pvdd_min
quit
.endc
.end
EOF
    echo "$fname"
}

# ============================================================
# Test C: Current limit (tran with Rload=0.1)
# ============================================================
gen_test_c() {
    local corner=$1
    local temp=$2
    local fname="$RESULTS_DIR/tb_c_${corner}_${temp}.spice"
    cat > "$fname" <<EOF
* Test C: Current limit — ${corner} ${temp}C
.title PVT_C_${corner}_${temp}

$(gen_header $corner $temp)

* Supplies — DC via ramp
Vbvdd bvdd 0 PWL(0 0 10u 7 100m 7)
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven_ret en_ret 0 0

* Near-short load
Rload pvdd 0 0.1

* DUT
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator

.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 2u 20m uic

.control
run
let pvdd_final = v(pvdd)[length(v(pvdd))-1]
let iout = pvdd_final / 0.1
echo "RESULT_C_PVDD ${corner} ${temp} ="
print pvdd_final
echo "RESULT_C_IOUT ${corner} ${temp} ="
print iout
quit
.endc
.end
EOF
    echo "$fname"
}

# ============================================================
# Phase 1: Test A for all 15 corners
# ============================================================
echo "==== Phase 1: Test A (Startup + DC Reg) — 15 corners ===="
for corner in $CORNERS; do
    for temp in $TEMPS; do
        fname=$(gen_test_a $corner $temp)
        echo "Running $fname ..."
        timeout 180 ngspice -b "$fname" > "$RESULTS_DIR/a_${corner}_${temp}.log" 2>&1
        rc=$?
        if [ $rc -ne 0 ]; then
            echo "  WARN: exit code $rc"
        else
            echo "  OK"
        fi
    done
done

# ============================================================
# Phase 2: Test B for all 15 corners
# ============================================================
echo "==== Phase 2: Test B (Load Transient) — 15 corners ===="
for corner in $CORNERS; do
    for temp in $TEMPS; do
        fname=$(gen_test_b $corner $temp)
        echo "Running $fname ..."
        timeout 180 ngspice -b "$fname" > "$RESULTS_DIR/b_${corner}_${temp}.log" 2>&1
        rc=$?
        if [ $rc -ne 0 ]; then
            echo "  WARN: exit code $rc"
        else
            echo "  OK"
        fi
    done
done

# ============================================================
# Phase 3: Test C for all 15 corners
# ============================================================
echo "==== Phase 3: Test C (Current Limit) — 15 corners ===="
for corner in $CORNERS; do
    for temp in $TEMPS; do
        fname=$(gen_test_c $corner $temp)
        echo "Running $fname ..."
        timeout 180 ngspice -b "$fname" > "$RESULTS_DIR/c_${corner}_${temp}.log" 2>&1
        rc=$?
        if [ $rc -ne 0 ]; then
            echo "  WARN: exit code $rc"
        else
            echo "  OK"
        fi
    done
done

echo "==== All simulations complete ===="
