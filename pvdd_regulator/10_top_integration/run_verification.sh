#!/bin/bash
# Master verification script — post FIX-19/FIX-20
# Runs: PVT DC (15 corners), current limit (3 corners), line reg, UV/OV
set -e
WD="/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration"
cd "$WD"

CORNERS="tt ss ff sf fs"
TEMPS="-40 27 150"
RESDIR="$WD/pvt_v2_results"
TMPDIR="$WD/tmp_ilim_sweep"
mkdir -p "$RESDIR" "$TMPDIR"

gen_header() {
    local corner=$1 temp=$2
    cat <<SPICE
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
SPICE
}

# ============================================================
# PHASE 1: PVT DC regulation — 15 corners, 1mA load
# ============================================================
echo "==== PHASE 1: PVT DC Regulation (15 corners) ===="
for corner in $CORNERS; do
    for temp in $TEMPS; do
        TB="$RESDIR/tb_a_${corner}_${temp}.spice"
        LOG="$RESDIR/a_${corner}_${temp}.log"
        cat > "$TB" <<EOF
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
        echo -n "  ${corner} ${temp}C ... "
        timeout 180 ngspice -b "$TB" > "$LOG" 2>&1 && echo "OK" || echo "WARN"
    done
done

# ============================================================
# PHASE 2: Current limit sweep — 3 corners, 22 load points
# ============================================================
echo ""
echo "==== PHASE 2: Current Limit Sweep (3 corners x 22 points) ===="
CSV="$WD/ilim_sweep_data.csv"
echo "corner,temp,rload,pvdd,iload,gate" > "$CSV"

RLOADS="100000 10000 5000 1000 500 200 150 120 110 100 95 90 85 80 75 70 60 50 30 10 5 1"
ILIM_CORNERS=("tt 27" "ss 150" "ff -40")

count=0
for corner_spec in "${ILIM_CORNERS[@]}"; do
    CORNER=$(echo "$corner_spec" | awk '{print $1}')
    TEMP=$(echo "$corner_spec" | awk '{print $2}')
    echo "--- Corner: $CORNER ${TEMP}C ---"
    for RVAL in $RLOADS; do
        count=$((count + 1))
        TB="$TMPDIR/tb_${CORNER}_${TEMP}_r${RVAL}.spice"
        LOG="$TMPDIR/log_${CORNER}_${TEMP}_r${RVAL}.log"
        cat > "$TB" <<EOF
.title ILIM_${CORNER}_${TEMP}_r${RVAL}
$(gen_header $CORNER $TEMP)
Vbvdd bvdd 0 PWL(0 0 10u 7 100m 7)
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven_ret en_ret 0 0
Rload pvdd 0 ${RVAL}
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator
.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 2u 25m uic
.control
run
meas tran vpvdd FIND v(pvdd) AT=25m
meas tran vgate FIND v(xdut.gate) AT=25m
quit
.endc
.end
EOF
        timeout 120 ngspice -b "$TB" > "$LOG" 2>&1 || true
        VPVDD=$(grep -i "^vpvdd" "$LOG" | head -1 | awk '{print $NF}' | sed 's/[^0-9.eE+-]//g')
        VGATE=$(grep -i "^vgate" "$LOG" | head -1 | awk '{print $NF}' | sed 's/[^0-9.eE+-]//g')
        [ -z "$VPVDD" ] && VPVDD="NaN"
        [ -z "$VGATE" ] && VGATE="NaN"
        if [ "$VPVDD" != "NaN" ]; then
            ILOAD=$(python3 -c "v=$VPVDD; r=$RVAL; print(f'{v/r:.8e}')" 2>/dev/null || echo "NaN")
        else
            ILOAD="NaN"
        fi
        echo "$CORNER,$TEMP,$RVAL,$VPVDD,$ILOAD,$VGATE" >> "$CSV"
        printf "  [%3d] R=%-8s PVDD=%-10s I=%-12s\n" "$count" "$RVAL" "$VPVDD" "$ILOAD"
    done
done

# ============================================================
# PHASE 3: Line regulation — 5mA and 10mA
# ============================================================
echo ""
echo "==== PHASE 3: Line Regulation ===="

for LOAD_LABEL in "5ma 1000" "10ma 500"; do
    LABEL=$(echo "$LOAD_LABEL" | awk '{print $1}')
    RVAL=$(echo "$LOAD_LABEL" | awk '{print $2}')
    TB="$TMPDIR/tb_linereg_${LABEL}.spice"
    LOG="$TMPDIR/log_linereg_${LABEL}.log"
    cat > "$TB" <<EOF
.title LineReg_${LABEL}
$(gen_header tt 27)
Vbvdd bvdd 0 PWL(0 0 10u 7 20m 7 30m 5.4 80m 10.5)
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven_ret en_ret 0 0
Rload pvdd 0 ${RVAL}
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator
.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 10u 80m uic
.control
run
set filetype = ascii
wrdata line_reg_${LABEL}.txt v(bvdd) v(pvdd)
quit
.endc
.end
EOF
    echo -n "  Line reg ${LABEL} ... "
    timeout 300 ngspice -b "$TB" > "$LOG" 2>&1 && echo "OK" || echo "WARN"
done

# ============================================================
# PHASE 4: UV/OV thresholds
# ============================================================
echo ""
echo "==== PHASE 4: UV/OV Thresholds ===="
cat > "$TMPDIR/tb_uvov.spice" <<'EOF'
* UV/OV Thresholds — PVDD ramp 0-7V
.title UVOV_Thresholds
.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "../sky130.lib.spice" tt
.include ../05_uv_ov_comparators/design.cir
Vpvdd pvdd 0 PWL(0 0 100m 7)
Vref vref 0 1.226
Vsvdd svdd 0 2.2
Ven en 0 2.2
XUV pvdd vref uv_flag svdd 0 en uv_comparator
XOV pvdd vref ov_flag svdd 0 en ov_comparator
.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.tran 10u 100m
.control
run
set filetype = ascii
wrdata uvov_data.txt v(pvdd) v(uv_flag) v(ov_flag)
quit
.endc
.end
EOF
echo -n "  UV/OV sim ... "
timeout 120 ngspice -b "$TMPDIR/tb_uvov.spice" > "$TMPDIR/log_uvov.log" 2>&1 && echo "OK" || echo "WARN"

echo ""
echo "==== All simulations complete ===="
