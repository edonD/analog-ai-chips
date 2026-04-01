#!/bin/bash
# PVT Corner Verification — TRANSIENT method
# .op finds wrong convergence at non-TT corners (vfb=-1774V, PVDD=6.5V)
# Using .tran with BVDD ramp instead — correct approach from Task 6a
set -e
cd "$(dirname "$0")"

CORNERS="tt ss ff sf fs"
PASS_MIN=4.825
PASS_MAX=5.175
TIMEOUT=180

echo "============================================="
echo " PVT Corner Verification — TRANSIENT method"
echo " Load: 1mA (Rload=5kΩ)"
echo " PASS range: ${PASS_MIN}V – ${PASS_MAX}V"
echo "============================================="
echo ""

declare -A RESULTS

for CORNER in $CORNERS; do
    TB="tb_pvt_${CORNER}.spice"

    cat > "$TB" <<EOF
* PVT Corner: ${CORNER} — transient ramp method
.title PVDD LDO PVT Corner ${CORNER}

.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "../sky130.lib.spice" ${CORNER}

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

* Stimuli: fast ramp to give circuit time to settle
Vbvdd bvdd 0 PWL(0 0 1u 7)
Vavbg avbg 0 PWL(0 0 1u 1.226)
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 2.2
Ven_ret en_ret 0 0
Rload pvdd 0 5000

XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag pvdd_regulator

.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4

.ic V(pvdd)=0 V(bvdd)=0
.tran 10u 2000u uic

.control
run
meas tran pvdd_final FIND v(pvdd) AT=2000u
echo "@@@ PVDD_RESULT @@@"
print pvdd_final
echo "@@@ END_RESULT @@@"
quit
.endc

.end
EOF

    echo -n "Running corner ${CORNER} (transient 2ms)... "
    if timeout ${TIMEOUT} ngspice -b "$TB" > "pvt_${CORNER}.log" 2>&1; then
        # Extract PVDD value from measure result
        VPVDD=$(grep -i "pvdd_final" "pvt_${CORNER}.log" | grep -oE '[-]?[0-9]+\.[0-9]+e[+-][0-9]+|[-]?[0-9]+\.[0-9]+' | head -1)

        if [ -z "$VPVDD" ]; then
            echo "PARSE ERROR"
            tail -30 "pvt_${CORNER}.log"
            RESULTS[$CORNER]="PARSE_ERROR"
            continue
        fi

        VDEC=$(python3 -c "v=float('$VPVDD'); print(f'{v:.4f}')")
        PASS=$(python3 -c "v=float('$VPVDD'); print('PASS' if $PASS_MIN <= v <= $PASS_MAX else 'FAIL')")
        echo "V(PVDD) = ${VDEC}V => ${PASS}"
        RESULTS[$CORNER]="${VDEC}|${PASS}"
    else
        echo "TIMEOUT/ERROR"
        RESULTS[$CORNER]="TIMEOUT"
    fi
done

echo ""
echo "============================================="
echo " RESULTS SUMMARY — TRANSIENT METHOD"
echo "============================================="
printf "%-8s %-14s %-6s\n" "Corner" "V(PVDD)" "Status"
printf "%-8s %-14s %-6s\n" "------" "--------" "------"
ALL_PASS=true
for CORNER in $CORNERS; do
    R="${RESULTS[$CORNER]}"
    if [[ "$R" == *"|"* ]]; then
        V=$(echo "$R" | cut -d'|' -f1)
        S=$(echo "$R" | cut -d'|' -f2)
        printf "%-8s %-14s %-6s\n" "$CORNER" "${V}V" "$S"
        [ "$S" != "PASS" ] && ALL_PASS=false
    else
        printf "%-8s %-14s %-6s\n" "$CORNER" "N/A" "$R"
        ALL_PASS=false
    fi
done
echo "============================================="
if $ALL_PASS; then
    echo "ALL CORNERS PASS"
else
    echo "SOME CORNERS FAILED — see logs for details"
fi
echo ""
