#!/bin/bash
# Task 6a: DC regulation, line regulation, load regulation, dropout tests
# Uses transient simulation for robust convergence
cd "$(dirname "$0")"

HEADER='.param mc_mm_switch = 0
.param MC_MM_SWITCH = 0
.subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
c0 r0 sub {0.1e-15*w*l}
c1 r1 sub {0.1e-15*w*l}
.ends sky130_fd_pr__model__parasitic__res_po
.lib "../sky130.lib.spice" tt

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
.include design.cir'

SUPPLIES_7V='Vbvdd bvdd 0 PWL(0 0 10u 7 100m 7)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Ven_ret en_ret 0 0'

DUT='XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag pvdd_regulator'

OPTS='.option reltol=1e-4 abstol=1e-12 vntol=1e-6
.option method=gear maxord=2
.option itl1=500 itl2=500 itl4=500
.ic V(pvdd)=0 V(bvdd)=0'

echo "============================================"
echo "TASK 6a: REGULATION TESTS"
echo "============================================"

#############################
# TEST 1: DC Regulation
#############################
echo ""
echo ">>> TEST 1: DC REGULATION (BVDD=7V) <<<"

run_dc_point() {
    local rload=$1
    local label=$2
    local tmpfile="/tmp/tb_dc_${label}.spice"
    cat > "$tmpfile" << SPICEOF
* DC Reg: ${label}
.title DC Reg ${label}
${HEADER}
${SUPPLIES_7V}
Rload pvdd 0 ${rload}
${DUT}
${OPTS}
.tran 10u 100m uic
.meas tran vpvdd avg V(pvdd) from=80m to=100m
.control
run
echo "RESULT_${label} ="
print vpvdd
quit
.endc
.end
SPICEOF
    timeout 120 ngspice -b "$tmpfile" 2>&1
}

# Run all 4 load points
R0=$(run_dc_point 1e6 "0mA")
R1=$(run_dc_point 5000 "1mA")
R2=$(run_dc_point 500 "10mA")
R3=$(run_dc_point 100 "50mA")

V0=$(echo "$R0" | grep -oP 'vpvdd\s*=\s*\K[0-9eE.+-]+')
V1=$(echo "$R1" | grep -oP 'vpvdd\s*=\s*\K[0-9eE.+-]+')
V2=$(echo "$R2" | grep -oP 'vpvdd\s*=\s*\K[0-9eE.+-]+')
V3=$(echo "$R3" | grep -oP 'vpvdd\s*=\s*\K[0-9eE.+-]+')

echo "  0mA:  PVDD = ${V0} V"
echo "  1mA:  PVDD = ${V1} V"
echo " 10mA:  PVDD = ${V2} V"
echo " 50mA:  PVDD = ${V3} V"
echo "SPEC: All between 4.825V and 5.175V"

# Check pass/fail
python3 -c "
vals = {'0mA': $V0, '1mA': $V1, '10mA': $V2, '50mA': $V3}
ok = True
for label, v in vals.items():
    status = 'PASS' if 4.825 <= v <= 5.175 else 'FAIL'
    if status == 'FAIL': ok = False
    print(f'  {label}: {v:.6f}V  [{status}]')
print(f'TEST 1 DC REGULATION: {\"PASS\" if ok else \"FAIL\"} ')
"

#############################
# TEST 2: LINE REGULATION
#############################
echo ""
echo ">>> TEST 2: LINE REGULATION (Iload=10mA) <<<"

# Run at BVDD=5.4V and BVDD=10.5V
run_line_point() {
    local bvdd=$1
    local label=$2
    local tmpfile="/tmp/tb_line_${label}.spice"
    cat > "$tmpfile" << SPICEOF
* Line Reg: BVDD=${bvdd}V
.title Line Reg ${label}
${HEADER}
Vbvdd bvdd 0 PWL(0 0 10u ${bvdd} 100m ${bvdd})
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Ven_ret en_ret 0 0
Rload pvdd 0 500
${DUT}
${OPTS}
.tran 10u 100m uic
.meas tran vpvdd avg V(pvdd) from=80m to=100m
.control
run
echo "RESULT_${label} ="
print vpvdd
quit
.endc
.end
SPICEOF
    timeout 120 ngspice -b "$tmpfile" 2>&1
}

L1=$(run_line_point 5.4 "5p4")
L2=$(run_line_point 10.5 "10p5")

VL1=$(echo "$L1" | grep -oP 'vpvdd\s*=\s*\K[0-9eE.+-]+')
VL2=$(echo "$L2" | grep -oP 'vpvdd\s*=\s*\K[0-9eE.+-]+')

python3 -c "
v54 = $VL1
v105 = $VL2
delta_v = abs(v105 - v54)
delta_bvdd = 10.5 - 5.4
line_reg = 1000 * delta_v / delta_bvdd  # mV/V
print(f'  PVDD at BVDD=5.4V:  {v54:.6f}V')
print(f'  PVDD at BVDD=10.5V: {v105:.6f}V')
print(f'  dVPVDD = {delta_v*1000:.3f} mV over {delta_bvdd}V range')
print(f'  Line Reg = {line_reg:.3f} mV/V')
status = 'PASS' if line_reg < 5.0 else 'FAIL'
print(f'TEST 2 LINE REGULATION: {status} ({line_reg:.3f} mV/V < 5 mV/V)')
"

#############################
# TEST 3: LOAD REGULATION
#############################
echo ""
echo ">>> TEST 3: LOAD REGULATION (BVDD=7V) <<<"

# Reuse V0 (0mA) and V3 (50mA) from Test 1
python3 -c "
v_noload = $V0
v_50ma = $V3
delta_v = abs(v_noload - v_50ma)
delta_i = 50  # mA
load_reg = 1000 * delta_v / delta_i  # mV/mA
print(f'  PVDD at 0mA:  {v_noload:.6f}V')
print(f'  PVDD at 50mA: {v_50ma:.6f}V')
print(f'  dVPVDD = {delta_v*1000:.3f} mV over 50mA range')
print(f'  Load Reg = {load_reg:.3f} mV/mA')
status = 'PASS' if load_reg < 2.0 else 'FAIL'
print(f'TEST 3 LOAD REGULATION: {status} ({load_reg:.3f} mV/mA < 2 mV/mA)')
"

#############################
# TEST 10: DROPOUT
#############################
echo ""
echo ">>> TEST 10: DROPOUT (Iload=50mA, BVDD=5.4V) <<<"

# Reuse line reg result at BVDD=5.4V with Rload=100
run_dropout() {
    local tmpfile="/tmp/tb_dropout.spice"
    cat > "$tmpfile" << SPICEOF
* Dropout: BVDD=5.4V, Iload=50mA
.title Dropout Test
${HEADER}
Vbvdd bvdd 0 PWL(0 0 10u 5.4 200m 5.4)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Ven_ret en_ret 0 0
Rload pvdd 0 100
${DUT}
${OPTS}
.tran 10u 200m uic
.meas tran vpvdd avg V(pvdd) from=150m to=200m
.control
run
echo "RESULT_dropout ="
print vpvdd
quit
.endc
.end
SPICEOF
    timeout 180 ngspice -b "$tmpfile" 2>&1
}

D1=$(run_dropout)
VD=$(echo "$D1" | grep -oP 'vpvdd\s*=\s*\K[0-9eE.+-]+')

python3 -c "
v = $VD
pct = 100 * (v - 5.0) / 5.0
print(f'  PVDD at BVDD=5.4V, 50mA: {v:.6f}V')
print(f'  Error from 5.0V: {pct:.3f}%')
status = 'PASS' if abs(pct) < 3.5 else 'FAIL'
print(f'TEST 10 DROPOUT: {status} ({pct:+.3f}% vs +/-3.5%)')
"

echo ""
echo "============================================"
echo "ALL TASK 6a TESTS COMPLETE"
echo "============================================"
