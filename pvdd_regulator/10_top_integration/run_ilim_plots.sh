#!/bin/bash
# run_ilim_plots.sh — Sweep Rload across 3 PVT corners, collect PVDD & gate voltage
# Each Rload value gets its own ngspice transient sim (25ms settle)

set -e
WORKDIR="/home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration"
cd "$WORKDIR"

# Output CSV
CSV="$WORKDIR/ilim_sweep_data.csv"
echo "corner,temp,rload,pvdd,iload,gate" > "$CSV"

# Rload values (reduced set — 36 points covering regulation through short circuit)
RLOADS="100000 50000 20000 10000 5000 2000 1000 500 200 150 120 110 100 95 92 90 88 85 82 80 75 70 60 50 40 30 20 15 10 7 5 3 2 1 0.5 0.2 0.1"

# Corners: "name temp"
CORNERS=("tt 27" "ss 150" "ff -40")

TMPDIR="$WORKDIR/tmp_ilim_sweep"
mkdir -p "$TMPDIR"

total=0
done_count=0
for corner_spec in "${CORNERS[@]}"; do
    for r in $RLOADS; do
        total=$((total + 1))
    done
done

echo "=== ILIM sweep: $total simulations ==="

for corner_spec in "${CORNERS[@]}"; do
    CORNER=$(echo "$corner_spec" | awk '{print $1}')
    TEMP=$(echo "$corner_spec" | awk '{print $2}')
    echo "--- Corner: $CORNER  Temp: ${TEMP}C ---"

    for RVAL in $RLOADS; do
        done_count=$((done_count + 1))
        TB="$TMPDIR/tb_${CORNER}_${TEMP}_r${RVAL}.spice"
        LOG="$TMPDIR/log_${CORNER}_${TEMP}_r${RVAL}.log"

        cat > "$TB" <<SPICEOF
.title ILIM_point_${CORNER}_${TEMP}_r${RVAL}
.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "../sky130.lib.spice" ${CORNER}
.temp ${TEMP}

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
SPICEOF

        # Run with timeout
        timeout 120 ngspice -b "$TB" > "$LOG" 2>&1 || true

        # Parse vpvdd
        VPVDD=$(grep -i "^vpvdd" "$LOG" | head -1 | awk '{print $NF}' | sed 's/[^0-9.eE+-]//g')
        VGATE=$(grep -i "^vgate" "$LOG" | head -1 | awk '{print $NF}' | sed 's/[^0-9.eE+-]//g')

        if [ -z "$VPVDD" ] || [ "$VPVDD" = "" ]; then
            VPVDD="NaN"
            ILOAD="NaN"
        else
            # Compute iload = vpvdd / rload (in amps)
            ILOAD=$(python3 -c "v=$VPVDD; r=$RVAL; print(f'{v/r:.8e}')" 2>/dev/null || echo "NaN")
        fi
        if [ -z "$VGATE" ] || [ "$VGATE" = "" ]; then
            VGATE="NaN"
        fi

        echo "$CORNER,$TEMP,$RVAL,$VPVDD,$ILOAD,$VGATE" >> "$CSV"
        printf "  [%3d/%d] R=%-8s  PVDD=%-10s  Iload=%-12s  Gate=%-10s\n" "$done_count" "$total" "$RVAL" "$VPVDD" "$ILOAD" "$VGATE"
    done
done

echo ""
echo "=== Data saved to $CSV ==="
echo "=== Rows: $(wc -l < "$CSV") ==="
cat "$CSV"
