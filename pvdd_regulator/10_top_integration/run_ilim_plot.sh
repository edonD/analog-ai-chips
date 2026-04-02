#!/bin/bash
# run_ilim_plot.sh — Current limit characterization across 3 PVT corners
# Sweeps load resistance from 10k (light load) to 0.1 ohm (near short circuit)
# Runs discrete transient simulations, measures steady-state PVDD and Iload

set -e
cd "$(dirname "$0")"

RLOADS="10000 5000 2000 1000 500 200 150 120 110 100 95 90 85 80 75 50 30 20 10 5 1 0.5 0.1"

# Corner definitions: name, lib_corner, temperature
CORNERS="tt_27:tt:27 ss_150:ss:150 ff_m40:ff:-40"

OUTFILE="ilim_plot_data.txt"
rm -f "$OUTFILE"
echo "# corner Rload(ohm) PVDD(V) Iload(A)" > "$OUTFILE"

for CORNER_DEF in $CORNERS; do
    IFS=':' read -r CNAME LIB_CORNER TEMP <<< "$CORNER_DEF"
    echo "=== Corner: $CNAME (lib=$LIB_CORNER, T=$TEMP) ==="

    for RVAL in $RLOADS; do
        TBFILE="tb_ilim_plot_${CNAME}_r${RVAL}.spice"
        LOGFILE="log_ilim_plot_${CNAME}_r${RVAL}.log"

        cat > "$TBFILE" << SPICE_EOF
* Current limit characterization — R=$RVAL ohm, corner=$CNAME
.title ILIM_PLOT_${CNAME}_R${RVAL}

.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po

.lib "../sky130.lib.spice" $LIB_CORNER
.temp $TEMP

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

* Supplies
Vbvdd bvdd 0 PWL(0 0 10u 7 100 7)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Ven_ret en_ret 0 0

* Resistive load
Rload pvdd 0 $RVAL

* DUT
XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator

.option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4
.ic V(pvdd)=0 V(bvdd)=0
.tran 10u 20m uic

.control
run
let pvdd_end = v(pvdd)[length(v(pvdd))-1]
let iload_end = pvdd_end / $RVAL
echo "${CNAME} ${RVAL} \$&pvdd_end \$&iload_end"
quit
.endc
.end
SPICE_EOF

        echo -n "  R=$RVAL ... "
        if ngspice -b "$TBFILE" > "$LOGFILE" 2>&1; then
            # Extract the data line from the log
            LINE=$(grep "^${CNAME} " "$LOGFILE" | tail -1)
            if [ -n "$LINE" ]; then
                echo "$LINE" >> "$OUTFILE"
                PVDD_VAL=$(echo "$LINE" | awk '{print $3}')
                ILOAD_VAL=$(echo "$LINE" | awk '{print $4}')
                echo "PVDD=${PVDD_VAL}V, Iload=${ILOAD_VAL}A"
            else
                echo "WARN: no data extracted"
                # Try alternate extraction: look for numeric output
                PVDD_VAL=$(grep -oP 'pvdd_end\s*=\s*\K[0-9.e+-]+' "$LOGFILE" | tail -1)
                if [ -n "$PVDD_VAL" ]; then
                    ILOAD_VAL=$(python3 -c "print(${PVDD_VAL}/${RVAL})")
                    echo "${CNAME} ${RVAL} ${PVDD_VAL} ${ILOAD_VAL}" >> "$OUTFILE"
                    echo "  (fallback) PVDD=${PVDD_VAL}V, Iload=${ILOAD_VAL}A"
                fi
            fi
        else
            echo "FAIL (sim error)"
        fi
        # Clean up temp testbench
        rm -f "$TBFILE"
    done
done

echo ""
echo "=== Data written to $OUTFILE ==="
cat "$OUTFILE"
echo ""
echo "Generating plot..."
gnuplot plot_ilim_char.gnuplot
echo "Plot saved to ilim_plot.png"
