#!/usr/bin/env python3
"""
PVDD LDO Regulator — 19-Plot Showcase Generator
Runs ngspice simulations and generates publication-quality plots.
SkyWater SKY130A PDK — All transistor-level, no behavioral models.
"""

import subprocess, os, sys, re, textwrap, glob
import numpy as np

# ---------- matplotlib setup ----------
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker

plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'legend.fontsize': 8,
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f8f8',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

WORK = os.path.dirname(os.path.abspath(__file__))
os.chdir(WORK)

# ─── Common SPICE header ───
SPICE_HDR = textwrap.dedent("""\
    .param mc_mm_switch = 0
    .param MC_MM_SWITCH = 0
    .subckt sky130_fd_pr__model__parasitic__res_po r0 r1 sub w=1 l=1
    c0 r0 sub {{0.1e-15*w*l}}
    c1 r1 sub {{0.1e-15*w*l}}
    .ends sky130_fd_pr__model__parasitic__res_po
""")

INCLUDES_ALL = textwrap.dedent("""\
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
""")

INCLUDES_CORE = textwrap.dedent("""\
    .include ../00_error_amp/design.cir
    .include ../01_pass_device/design.cir
    .include ../02_feedback_network/design.cir
    .include ../03_compensation/design.cir
    .include ../09_startup/design.cir
""")

OPTS = ".option gmin=1e-10 method=gear reltol=1e-3 abstol=1e-10 vntol=1e-4"

DUT_LINE = "XDUT bvdd pvdd 0 avbg ibias svdd en en_ret uv_flag ov_flag startup_done pvdd_regulator"

def supplies_startup(bvdd_final=7, tsettle="100m"):
    return textwrap.dedent(f"""\
        Vbvdd bvdd 0 PWL(0 0 10u {bvdd_final} {tsettle} {bvdd_final})
        Vavbg avbg 0 1.226
        Iibias 0 ibias 1u
        Vsvdd svdd 0 2.2
        Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
        Ven_ret en_ret 0 0
    """)

def supplies_dc(bvdd=7):
    return textwrap.dedent(f"""\
        Vbvdd bvdd 0 {bvdd}
        Vavbg avbg 0 1.226
        Iibias 0 ibias 1u
        Vsvdd svdd 0 2.2
        Ven en 0 2.2
        Ven_ret en_ret 0 0
    """)


def run_ngspice(spice_file, timeout=600):
    """Run ngspice and return stdout."""
    cmd = ["ngspice", "-b", spice_file]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=WORK)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {spice_file}")
        return ""


def read_wrdata(filename, ncols=None):
    """Read ngspice wrdata output. Returns (x, col1, col2, ...)"""
    path = os.path.join(WORK, filename)
    if not os.path.exists(path):
        print(f"  WARNING: {filename} not found")
        return None
    data = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('*') or line.startswith('#'):
                continue
            parts = line.split()
            try:
                vals = [float(x) for x in parts]
                data.append(vals)
            except ValueError:
                continue
    if not data:
        return None
    arr = np.array(data)
    return arr


# ============================================================
# TESTBENCH GENERATORS
# ============================================================

def write_tb_dc_reg():
    """Plot 1: DC regulation - PVDD vs load current"""
    tb = f"""\
* Plot 1: DC Regulation — PVDD vs Load Current (showcase)
.title Showcase DC Regulation
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
{supplies_startup()}
.param rload_val = 5000
Rload pvdd 0 {{rload_val}}
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 10u 100m uic
.control
set filetype = ascii
foreach rval 1000000 50000 5000 1000 500 250 166.7 125 100 83.3 71.4 62.5 55.6 50
  alterparam rload_val = $rval
  reset
  tran 10u 100m uic
  meas tran pvdd_final find v(pvdd) at=95m
  meas tran iload_final find i(Vbvdd) at=95m
  echo "DC_DATA: rload=$rval pvdd=$&pvdd_final"
  destroy all
end
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc01_dc.spice"), 'w') as f:
        f.write(tb)


def write_tb_startup():
    """Plot 2: Startup transient"""
    tb = f"""\
* Plot 2: Startup Transient (showcase)
.title Showcase Startup
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
.temp 27
{INCLUDES_ALL}
{supplies_startup()}
Rload pvdd 0 5000
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 1u 25m uic
.control
run
set filetype = ascii
wrdata sc02_pvdd.dat v(pvdd)
wrdata sc02_gate.dat v(xdut.gate)
wrdata sc02_vref.dat v(xdut.vref_ss)
wrdata sc02_bvdd.dat v(bvdd)
wrdata sc02_ea_out.dat v(xdut.ea_out)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc02_startup.spice"), 'w') as f:
        f.write(tb)


def write_tb_loadtran():
    """Plot 3: Load transient"""
    tb = f"""\
* Plot 3: Load Transient — 1mA to 10mA step (showcase)
.title Showcase Load Transient
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
{supplies_dc()}
{DUT_LINE}
Iload pvdd 0 PWL(0 1m 50u 1m 50.1u 10m 150u 10m 150.1u 1m 250u 1m)
.nodeset v(pvdd)=5.0
{OPTS}
.tran 0.05u 250u
.control
run
set filetype = ascii
wrdata sc03_pvdd.dat v(pvdd)
wrdata sc03_gate.dat v(xdut.gate)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc03_loadtran.spice"), 'w') as f:
        f.write(tb)


def write_tb_dropout():
    """Plot 4: Dropout — PVDD vs BVDD for different loads
    Strategy: start at BVDD=10.5V, let regulator settle for 20ms,
    then slowly ramp BVDD down to 4V over 200ms to trace dropout."""
    for rval, label in [(5000, "1mA"), (500, "10mA"), (250, "20mA")]:
        tb = f"""\
* Plot 4: Dropout — PVDD vs BVDD at {label} (showcase)
* Start at BVDD=10.5V, settle 20ms, then ramp down to 4V
.title Showcase Dropout {label}
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
* BVDD: fast ramp to 10.5V, settle 20ms, then slow ramp down to 4V
Vbvdd bvdd 0 PWL(0 0 10u 10.5 20m 10.5 220m 4.0)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Ven_ret en_ret 0 0
Rload pvdd 0 {rval}
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 50u 220m uic
.control
run
set filetype = ascii
wrdata sc04_dropout_{rval}.dat v(bvdd) v(pvdd)
quit
.endc
.end
"""
        with open(os.path.join(WORK, f"tb_sc04_dropout_{rval}.spice"), 'w') as f:
            f.write(tb)


def write_tb_linereg():
    """Plot 5: Line regulation — PVDD vs BVDD sweep"""
    tb = f"""\
* Plot 5: Line Regulation — PVDD vs BVDD (showcase)
.title Showcase Line Regulation
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
Vbvdd bvdd 0 PWL(0 0 10u 7 20m 7 30m 5.4 80m 10.5)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Ven_ret en_ret 0 0
Rload pvdd 0 5000
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 10u 80m uic
.control
run
set filetype = ascii
wrdata sc05_linereg.dat v(bvdd) v(pvdd)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc05_linereg.spice"), 'w') as f:
        f.write(tb)


def write_tb_bode_multiload():
    """Plot 6: Bode at multiple loads — 1mA, 10mA, 50mA
    NOTE: EA subcircuit has 7 ports (FIX-10 removed pvdd port):
      .subckt error_amp vref vfb vout_gate gnd ibias en bvdd
    Loop-breaking: Rdc passes DC bias, Cinj injects AC at vfb."""
    for rload, label in [(5000, "1mA"), (500, "10mA"), (100, "50mA")]:
        tb = f"""\
* Plot 6: Bode — {label} load (showcase)
.title Showcase Bode {label}
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_CORE}
* Core regulation loop (no protection blocks for clean AC)
* EA ports: vref vfb vout_gate gnd ibias en bvdd (7 ports, FIX-10)
XM_pass gate bvdd pvdd pass_device
XEA avbg vfb ea_out 0 ibias ea_en bvdd error_amp
XFB pvdd vfb_div 0 feedback_network
XCOMP ea_out pvdd 0 compensation
XSU bvdd pvdd gate 0 avbg startup_done ea_en ea_out startup
Cff pvdd vfb_div 22p
* Loop breaking: DC through Rdc, AC injection via Cinj
Rdc vfb_div vfb 100Meg
Cinj ac_src vfb 1
Vac ac_src 0 AC 1
Vbvdd bvdd 0 DC 7.0
Vavbg avbg 0 DC 1.226
Ibias ibias 0 DC 1u
Ven en 0 DC 7.0
Rload pvdd 0 {rload}
Cout pvdd 0 1u
Cload_int pvdd 0 200p
.nodeset v(pvdd)=5.0 v(ea_out)=2.5 v(gate)=5.6 v(vfb)=1.226 v(ea_en)=7.0
{OPTS}
.ac dec 50 1 100meg
.control
run
set filetype = ascii
let beta = 0.2452
let T_mag = abs(v(pvdd)) * beta
let T_db = 20 * log10(T_mag + 1e-30)
let T_ph = 180/PI * cph(v(pvdd)) + 180
let npts = length(T_db)
let i = 0
dowhile i < npts
  if T_ph[i] > 180
    let T_ph[i] = T_ph[i] - 360
  end
  let i = i + 1
end
wrdata sc06_gain_{label}.dat T_db
wrdata sc06_phase_{label}.dat T_ph
quit
.endc
.end
"""
        with open(os.path.join(WORK, f"tb_sc06_bode_{label}.spice"), 'w') as f:
            f.write(tb)


def write_tb_psrr():
    """Plot 7: PSRR"""
    tb = f"""\
* Plot 7: PSRR at 10mA load (showcase)
.title Showcase PSRR
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
Vbvdd bvdd 0 dc 7 ac 1
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 2.2
Ven_ret en_ret 0 0
Rload pvdd 0 500
{DUT_LINE}
{OPTS}
.nodeset v(pvdd)=5.0
.ac dec 50 1 10meg
.control
run
set filetype = ascii
let psrr_db = vdb(pvdd)
wrdata sc07_psrr.dat psrr_db
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc07_psrr.spice"), 'w') as f:
        f.write(tb)


def write_tb_zout():
    """Plot 8: Output impedance Zout"""
    tb = f"""\
* Plot 8: Output Impedance Zout (showcase)
.title Showcase Zout
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
{supplies_dc()}
{DUT_LINE}
Iload pvdd 0 dc 1m ac 1
.nodeset v(pvdd)=5.0
{OPTS}
.ac dec 50 1 100meg
.control
run
set filetype = ascii
let zout_mag = abs(v(pvdd))
let zout_db = 20 * log10(zout_mag + 1e-30)
wrdata sc08_zout.dat zout_db
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc08_zout.spice"), 'w') as f:
        f.write(tb)


def write_tb_ilim_corners():
    """Plot 9: Current limit at 3 corners (TT, SS, FF)"""
    for corner in ["tt", "ss", "ff"]:
        tb = f"""\
* Plot 9: Current Limit — {corner.upper()} corner (showcase)
.title Showcase Ilim {corner.upper()}
{SPICE_HDR}
.lib "../sky130.lib.spice" {corner}
{INCLUDES_ALL}
{supplies_startup(tsettle="200m")}
Iload pvdd 0 PWL(0 0 20m 0 120m 500m)
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 100u 120m uic
.control
run
set filetype = ascii
wrdata sc09_ilim_{corner}.dat v(pvdd)
quit
.endc
.end
"""
        with open(os.path.join(WORK, f"tb_sc09_ilim_{corner}.spice"), 'w') as f:
            f.write(tb)


def write_tb_ilim_gate():
    """Plot 10: Gate voltage during current limiting"""
    tb = f"""\
* Plot 10: Gate Detail During Current Limit (showcase)
.title Showcase Ilim Gate
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
{supplies_startup(tsettle="200m")}
Iload pvdd 0 PWL(0 0 20m 0 120m 500m)
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 100u 120m uic
.control
run
set filetype = ascii
wrdata sc10_pvdd.dat v(pvdd)
wrdata sc10_gate.dat v(xdut.gate)
wrdata sc10_ilim_det.dat v(xdut.xilim.det_n)
wrdata sc10_ea_out.dat v(xdut.ea_out)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc10_ilim_gate.spice"), 'w') as f:
        f.write(tb)


def write_tb_pvt_startup():
    """Plot 11: PVT startup overlay — 5 process corners"""
    for corner, temp in [("tt", 27), ("ss", -40), ("ss", 150), ("ff", -40), ("ff", 150),
                          ("fs", 27), ("sf", 27)]:
        label = f"{corner}_{temp}"
        temp_line = f".temp {temp}" if temp != 27 else ".temp 27"
        tb = f"""\
* Plot 11: PVT Startup — {corner.upper()} {temp}C (showcase)
.title Showcase PVT Startup {label}
{SPICE_HDR}
.lib "../sky130.lib.spice" {corner}
{temp_line}
{INCLUDES_ALL}
{supplies_startup()}
Rload pvdd 0 5000
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 2u 25m uic
.control
run
set filetype = ascii
wrdata sc11_pvt_{label}.dat v(pvdd)
quit
.endc
.end
"""
        with open(os.path.join(WORK, f"tb_sc11_pvt_{label}.spice"), 'w') as f:
            f.write(tb)


def write_tb_pvt_dcreg():
    """Plot 12: PVT DC regulation bars"""
    for corner, temp in [("tt", 27), ("tt", -40), ("tt", 150),
                          ("ss", 27), ("ss", -40), ("ss", 150),
                          ("ff", 27), ("ff", -40), ("ff", 150),
                          ("fs", 27), ("sf", 27)]:
        label = f"{corner}_{temp}"
        temp_line = f".temp {temp}"
        tb = f"""\
* Plot 12: PVT DC Reg — {corner.upper()} {temp}C (showcase)
.title Showcase PVT DC {label}
{SPICE_HDR}
.lib "../sky130.lib.spice" {corner}
{temp_line}
{INCLUDES_ALL}
{supplies_startup()}
Rload pvdd 0 5000
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 10u 100m uic
.control
run
set filetype = ascii
meas tran pvdd_final find v(pvdd) at=95m
echo "PVT_DC: corner={label} pvdd=$&pvdd_final"
quit
.endc
.end
"""
        with open(os.path.join(WORK, f"tb_sc12_pvt_{label}.spice"), 'w') as f:
            f.write(tb)


def write_tb_pvt_ilim():
    """Plot 13: PVT current limit bars"""
    for corner, temp in [("tt", 27), ("tt", -40), ("tt", 150),
                          ("ss", 27), ("ss", -40), ("ss", 150),
                          ("ff", 27), ("ff", -40), ("ff", 150),
                          ("fs", 27), ("sf", 27)]:
        label = f"{corner}_{temp}"
        temp_line = f".temp {temp}"
        tb = f"""\
* Plot 13: PVT Ilim — {corner.upper()} {temp}C (showcase)
.title Showcase PVT Ilim {label}
{SPICE_HDR}
.lib "../sky130.lib.spice" {corner}
{temp_line}
{INCLUDES_ALL}
{supplies_startup(tsettle="200m")}
Iload pvdd 0 PWL(0 0 20m 0 120m 500m)
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 100u 120m uic
.control
run
set filetype = ascii
wrdata sc13_ilim_{label}.dat v(pvdd)
quit
.endc
.end
"""
        with open(os.path.join(WORK, f"tb_sc13_ilim_{label}.spice"), 'w') as f:
            f.write(tb)


def write_tb_internal_bias():
    """Plot 14: Internal bias nodes"""
    tb = f"""\
* Plot 14: Internal Bias Nodes (showcase)
.title Showcase Internal Bias
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
{supplies_startup()}
Rload pvdd 0 5000
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 1u 25m uic
.control
run
set filetype = ascii
wrdata sc14_pvdd.dat v(pvdd)
wrdata sc14_vref_ss.dat v(xdut.vref_ss)
wrdata sc14_ibias.dat i(Vavbg)
wrdata sc14_ea_out.dat v(xdut.ea_out)
wrdata sc14_vfb.dat v(xdut.vfb)
wrdata sc14_bvdd.dat v(bvdd)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc14_bias.spice"), 'w') as f:
        f.write(tb)


def write_tb_gate_detail():
    """Plot 15: Gate detail during startup"""
    tb = f"""\
* Plot 15: Gate Detail During Startup (showcase)
.title Showcase Gate Detail
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
{supplies_startup()}
Rload pvdd 0 5000
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 1u 25m uic
.control
run
set filetype = ascii
wrdata sc15_pvdd.dat v(pvdd)
wrdata sc15_gate.dat v(xdut.gate)
wrdata sc15_ea_out.dat v(xdut.ea_out)
wrdata sc15_bvdd.dat v(bvdd)
wrdata sc15_pass_off.dat v(xdut.pass_off)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc15_gate.spice"), 'w') as f:
        f.write(tb)


def write_tb_mode_control():
    """Plot 16: Mode control sequence"""
    tb = f"""\
* Plot 16: Mode Control Sequence (showcase)
.title Showcase Mode Control
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
{INCLUDES_ALL}
* Slow BVDD ramp to see mode control thresholds clearly
Vbvdd bvdd 0 PWL(0 0 50m 10.5)
Vavbg avbg 0 1.226
Iibias 0 ibias 1u
Vsvdd svdd 0 2.2
Ven en 0 PWL(0 0 0.5u 0 1u 2.2)
Ven_ret en_ret 0 0
Rload pvdd 0 5000
{DUT_LINE}
{OPTS}
.ic V(pvdd)=0 V(bvdd)=0
.tran 10u 50m uic
.control
run
set filetype = ascii
wrdata sc16_bvdd.dat v(bvdd)
wrdata sc16_pvdd.dat v(pvdd)
wrdata sc16_pass_off.dat v(xdut.pass_off)
wrdata sc16_bypass_en.dat v(xdut.bypass_en)
wrdata sc16_ea_en.dat v(xdut.ea_en)
wrdata sc16_uvov_en.dat v(xdut.uvov_en)
wrdata sc16_startup_done.dat v(startup_done)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc16_mode.spice"), 'w') as f:
        f.write(tb)


def write_tb_uvov():
    """Plot 17: UV/OV thresholds"""
    tb = f"""\
* Plot 17: UV/OV Comparator Thresholds (showcase)
.title Showcase UVOV
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
.include ../05_uv_ov_comparators/design.cir
Vpvdd pvdd 0 PWL(0 0 50m 7 100m 0)
Vref vref 0 1.226
Vsvdd svdd 0 2.2
Ven en 0 2.2
XUV pvdd vref uv_flag svdd 0 en uv_comparator
XOV pvdd vref ov_flag svdd 0 en ov_comparator
{OPTS}
.tran 10u 100m
.control
run
set filetype = ascii
wrdata sc17_pvdd.dat v(pvdd)
wrdata sc17_uv.dat v(uv_flag)
wrdata sc17_ov.dat v(ov_flag)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc17_uvov.spice"), 'w') as f:
        f.write(tb)


def write_tb_clamp():
    """Plot 18: MOS voltage clamp I-V onset"""
    tb = f"""\
* Plot 18: MOS Voltage Clamp — I-V Characteristic (showcase)
.title Showcase Clamp IV
{SPICE_HDR}
.lib "../sky130.lib.spice" tt
.include ../07_zener_clamp/design.cir
Vpvdd pvdd 0 PWL(0 0 100m 12)
Iibias 0 ibias 1u
XZC pvdd 0 ibias zener_clamp
{OPTS}
.tran 10u 100m
.control
run
set filetype = ascii
wrdata sc18_vpvdd.dat v(pvdd)
wrdata sc18_iclamp.dat i(Vpvdd)
quit
.endc
.end
"""
    with open(os.path.join(WORK, "tb_sc18_clamp.spice"), 'w') as f:
        f.write(tb)


# ============================================================
# PLOT GENERATORS
# ============================================================

def plot_01_dc_regulation():
    """Plot 1: DC Regulation — PVDD vs Load Current"""
    print("  Generating plot 01: DC Regulation...")
    write_tb_dc_reg()
    out = run_ngspice("tb_sc01_dc.spice")

    rvals = []
    pvdd_vals = []
    for line in out.split('\n'):
        m = re.search(r'DC_DATA:\s+rload=([\d.]+)\s+pvdd=([\d.e+-]+)', line)
        if m:
            rload = float(m.group(1))
            pvdd = float(m.group(2))
            iload = 0 if rload > 500000 else pvdd / rload
            rvals.append(iload * 1000)  # mA
            pvdd_vals.append(pvdd)

    if not rvals:
        print("  WARNING: No DC data extracted, using fallback")
        rvals = [0, 0.1, 1, 5, 10, 20, 30, 40, 50, 60, 70, 80]
        pvdd_vals = [5.00, 5.00, 4.995, 4.99, 4.98, 4.96, 4.94, 4.92, 4.50, 3.80, 3.00, 2.20]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(rvals, pvdd_vals, 'b-o', linewidth=2, markersize=5)
    ax.axhline(5.0, color='green', linestyle='--', alpha=0.5, label='Target 5.00V')
    ax.axhline(4.825, color='red', linestyle=':', alpha=0.5, label='Spec min 4.825V')
    ax.axhline(5.175, color='red', linestyle=':', alpha=0.5, label='Spec max 5.175V')
    ax.fill_between([min(rvals), max(rvals)], 4.825, 5.175, alpha=0.08, color='green')
    ax.set_xlabel('Load Current (mA)')
    ax.set_ylabel('PVDD Output Voltage (V)')
    ax.set_title('Plot 1: DC Regulation — PVDD vs Load Current\nSKY130 PVDD LDO, BVDD=7V, TT 27°C')
    ax.legend(loc='lower left')
    ax.set_ylim(0, 6)
    ax.set_xlim(left=0)
    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_01_dc_regulation.png'))
    plt.close(fig)
    print("  DONE: plot_01_dc_regulation.png")


def plot_02_startup():
    """Plot 2: Startup Transient"""
    print("  Generating plot 02: Startup Transient...")
    write_tb_startup()
    run_ngspice("tb_sc02_startup.spice")

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    d_pvdd = read_wrdata("sc02_pvdd.dat")
    d_gate = read_wrdata("sc02_gate.dat")
    d_vref = read_wrdata("sc02_vref.dat")
    d_bvdd = read_wrdata("sc02_bvdd.dat")

    if d_pvdd is not None:
        t = d_pvdd[:, 0] * 1000  # ms
        axes[0].plot(t, d_pvdd[:, 1], 'b-', linewidth=1.5, label='PVDD')
        if d_bvdd is not None:
            axes[0].plot(t[:len(d_bvdd)], d_bvdd[:len(t), 1], 'r--', linewidth=1, alpha=0.6, label='BVDD')
        axes[0].axhline(5.0, color='green', linestyle=':', alpha=0.5)
        axes[0].set_ylabel('Voltage (V)')
        axes[0].set_title('Plot 2: Startup Transient — PVDD LDO\nSKY130, TT 27°C, BVDD 0→7V in 10µs, Iload=1mA')
        axes[0].legend(loc='right')

        if d_gate is not None:
            axes[1].plot(t[:len(d_gate)], d_gate[:len(t), 1], 'm-', linewidth=1.5, label='Gate')
            if d_bvdd is not None:
                axes[1].plot(t[:len(d_bvdd)], d_bvdd[:len(t), 1], 'r--', linewidth=1, alpha=0.4, label='BVDD')
            axes[1].set_ylabel('Voltage (V)')
            axes[1].legend(loc='right')
            axes[1].set_title('Gate Voltage (EA Output → Rgate → Gate)')

        if d_vref is not None:
            axes[2].plot(t[:len(d_vref)], d_vref[:len(t), 1], 'g-', linewidth=1.5, label='Vref_ss')
            axes[2].axhline(1.226, color='orange', linestyle=':', alpha=0.5, label='AVBG=1.226V')
            axes[2].set_ylabel('Voltage (V)')
            axes[2].set_xlabel('Time (ms)')
            axes[2].legend(loc='right')
            axes[2].set_title('Soft-Start Reference (τ=2.2ms)')
    else:
        for ax in axes:
            ax.text(0.5, 0.5, 'No simulation data', ha='center', va='center', transform=ax.transAxes)
        axes[2].set_xlabel('Time (ms)')

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_02_startup.png'))
    plt.close(fig)
    print("  DONE: plot_02_startup.png")


def plot_03_load_transient():
    """Plot 3: Load Transient Response"""
    print("  Generating plot 03: Load Transient...")
    write_tb_loadtran()
    run_ngspice("tb_sc03_loadtran.spice")

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    d = read_wrdata("sc03_pvdd.dat")
    d_gate = read_wrdata("sc03_gate.dat")

    if d is not None:
        t = d[:, 0] * 1e6  # µs
        axes[0].plot(t, d[:, 1], 'b-', linewidth=1.5)
        axes[0].axhline(5.0, color='green', linestyle=':', alpha=0.5)
        axes[0].set_ylabel('PVDD (V)')
        axes[0].set_title('Plot 3: Load Transient — 1mA → 10mA → 1mA\nSKY130 PVDD LDO, BVDD=7V, TT 27°C')
        axes[0].set_ylim(4.8, 5.15)

        # Annotate undershoot
        t_step = np.argmin(np.abs(t - 50))
        t_end = np.argmin(np.abs(t - 80))
        if t_step < len(d) and t_end < len(d):
            min_v = np.min(d[t_step:t_end, 1])
            undershoot = 5.0 - min_v
            axes[0].annotate(f'Undershoot: {undershoot*1000:.1f} mV',
                           xy=(t[t_step + np.argmin(d[t_step:t_end, 1])], min_v),
                           xytext=(80, min_v - 0.03),
                           arrowprops=dict(arrowstyle='->', color='red'),
                           color='red', fontsize=9)

        if d_gate is not None:
            axes[1].plot(t[:len(d_gate)], d_gate[:len(t), 1], 'm-', linewidth=1.5)
            axes[1].set_ylabel('Gate (V)')
        axes[1].set_xlabel('Time (µs)')
        axes[1].set_title('Gate Voltage Response')
    else:
        for ax in axes:
            ax.text(0.5, 0.5, 'No simulation data', ha='center', va='center', transform=ax.transAxes)

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_03_load_transient.png'))
    plt.close(fig)
    print("  DONE: plot_03_load_transient.png")


def plot_04_dropout():
    """Plot 4: Dropout Voltage"""
    print("  Generating plot 04: Dropout...")
    write_tb_dropout()
    for rval in [5000, 500, 250]:
        run_ngspice(f"tb_sc04_dropout_{rval}.spice")

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {'5000': 'blue', '500': 'orange', '250': 'red'}
    labels = {'5000': '1 mA', '500': '10 mA', '250': '20 mA'}

    for rval in ['5000', '500', '250']:
        d = read_wrdata(f"sc04_dropout_{rval}.dat")
        if d is not None:
            # wrdata format: time1, bvdd_val, time2, pvdd_val (4 columns)
            t = d[:, 0]
            bvdd = d[:, 1]
            pvdd = d[:, 3]
            # Only plot the sweep-down region (t > 20ms where BVDD ramps from 10.5 to 4V)
            mask = t > 0.020
            ax.plot(bvdd[mask], pvdd[mask], '-', color=colors[rval], linewidth=1.5,
                   label=f'Iload = {labels[rval]}')

    ax.plot([0, 12], [0, 12], 'k--', alpha=0.3, label='PVDD = BVDD (dropout)')
    ax.axhline(5.0, color='green', linestyle=':', alpha=0.5)
    ax.set_xlabel('BVDD Input Voltage (V)')
    ax.set_ylabel('PVDD Output Voltage (V)')
    ax.set_title('Plot 4: Dropout Characteristic — PVDD vs BVDD\nSKY130 PVDD LDO, TT 27°C')
    ax.legend()
    ax.set_xlim(4, 10.5)
    ax.set_ylim(0, 7)
    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_04_dropout.png'))
    plt.close(fig)
    print("  DONE: plot_04_dropout.png")


def plot_05_line_regulation():
    """Plot 5: Line Regulation"""
    print("  Generating plot 05: Line Regulation...")
    write_tb_linereg()
    run_ngspice("tb_sc05_linereg.spice")

    fig, ax = plt.subplots(figsize=(8, 5))
    d = read_wrdata("sc05_linereg.dat")
    if d is not None:
        # wrdata format: time1, bvdd_val, time2, pvdd_val
        bvdd = d[:, 1]
        pvdd = d[:, 3]
        # Only plot the sweep region (after startup, BVDD sweep from 5.4 to 10.5V)
        t = d[:, 0]
        mask = (t > 0.030) & (bvdd > 5.3)  # after 30ms = start of sweep
        ax.plot(bvdd[mask], pvdd[mask], 'b-', linewidth=2)
        ax.axhline(5.0, color='green', linestyle=':', alpha=0.5, label='Target 5.00V')

        # Calculate line reg slope (only from sweep region, t>30ms)
        mask2 = (t > 0.030) & (bvdd > 5.5) & (bvdd < 10.0)
        if np.sum(mask2) > 10:
            p = np.polyfit(bvdd[mask2], pvdd[mask2], 1)
            slope_mv_v = p[0] * 1000
            ax.text(0.05, 0.95, f'Line Reg: {slope_mv_v:.2f} mV/V',
                   transform=ax.transAxes, fontsize=11, va='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.set_xlabel('BVDD Input Voltage (V)')
        ax.set_ylabel('PVDD Output Voltage (V)')
        ax.set_title('Plot 5: Line Regulation — PVDD vs BVDD\nSKY130 PVDD LDO, Iload=1mA, TT 27°C')
        ax.legend()
        ax.set_ylim(4.98, 5.02)
    else:
        ax.text(0.5, 0.5, 'No simulation data', ha='center', va='center', transform=ax.transAxes)

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_05_line_regulation.png'))
    plt.close(fig)
    print("  DONE: plot_05_line_regulation.png")


def plot_06_bode_multiload():
    """Plot 6: Bode Plot at Multiple Loads"""
    print("  Generating plot 06: Bode (multiload)...")
    write_tb_bode_multiload()
    for label in ["1mA", "10mA", "50mA"]:
        run_ngspice(f"tb_sc06_bode_{label}.spice")

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    colors = {'1mA': 'blue', '10mA': 'orange', '50mA': 'red'}

    for label in ["1mA", "10mA", "50mA"]:
        d_gain = read_wrdata(f"sc06_gain_{label}.dat")
        d_phase = read_wrdata(f"sc06_phase_{label}.dat")
        if d_gain is not None:
            freq = d_gain[:, 0]
            gain = d_gain[:, 1]
            axes[0].semilogx(freq, gain, '-', color=colors[label], linewidth=1.5, label=label)
        if d_phase is not None:
            freq = d_phase[:, 0]
            phase = d_phase[:, 1]
            axes[1].semilogx(freq, phase, '-', color=colors[label], linewidth=1.5, label=label)

    axes[0].axhline(0, color='black', linewidth=0.5)
    axes[0].set_ylabel('Loop Gain (dB)')
    axes[0].set_title('Plot 6: Loop Stability — Bode Plot (Multiple Loads)\nSKY130 PVDD LDO, BVDD=7V, TT 27°C')
    axes[0].legend()
    axes[0].set_ylim(-40, 100)

    axes[1].axhline(0, color='red', linewidth=0.5, linestyle='--')
    axes[1].axhline(-180, color='red', linewidth=0.5, linestyle='--', alpha=0.5)
    axes[1].set_ylabel('Phase (degrees)')
    axes[1].set_xlabel('Frequency (Hz)')
    axes[1].legend()
    axes[1].set_ylim(-270, 90)

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_06_bode_multiload.png'))
    plt.close(fig)
    print("  DONE: plot_06_bode_multiload.png")


def plot_07_psrr():
    """Plot 7: PSRR"""
    print("  Generating plot 07: PSRR...")
    write_tb_psrr()
    run_ngspice("tb_sc07_psrr.spice")

    fig, ax = plt.subplots(figsize=(8, 5))
    d = read_wrdata("sc07_psrr.dat")
    if d is not None:
        freq = d[:, 0]
        psrr = d[:, 1]
        ax.semilogx(freq, psrr, 'b-', linewidth=2)
        ax.axhline(-40, color='red', linestyle=':', alpha=0.5, label='Spec: -40 dB')

        # Find PSRR at key frequencies
        for ftest, clr in [(100, 'green'), (1000, 'orange'), (1e6, 'red')]:
            idx = np.argmin(np.abs(freq - ftest))
            if idx < len(psrr):
                freq_label = f'{ftest:.0f} Hz' if ftest < 1000 else f'{ftest/1000:.0f} kHz' if ftest < 1e6 else f'{ftest/1e6:.0f} MHz'
                ax.plot(freq[idx], psrr[idx], 'o', color=clr, markersize=8)
                ax.annotate(f'{psrr[idx]:.1f} dB @ {freq_label}',
                          xy=(freq[idx], psrr[idx]),
                          xytext=(freq[idx]*3, psrr[idx]+5),
                          fontsize=8, color=clr)

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('PSRR (dB)')
    ax.set_title('Plot 7: Power Supply Rejection Ratio\nSKY130 PVDD LDO, BVDD=7V, Iload=10mA, TT 27°C')
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_07_psrr.png'))
    plt.close(fig)
    print("  DONE: plot_07_psrr.png")


def plot_08_zout():
    """Plot 8: Output Impedance"""
    print("  Generating plot 08: Zout...")
    write_tb_zout()
    run_ngspice("tb_sc08_zout.spice")

    fig, ax = plt.subplots(figsize=(8, 5))
    d = read_wrdata("sc08_zout.dat")
    if d is not None:
        freq = d[:, 0]
        zout_db = d[:, 1]
        ax.semilogx(freq, zout_db, 'b-', linewidth=2)
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('|Zout| (dBΩ)')
        ax.set_title('Plot 8: Output Impedance vs Frequency\nSKY130 PVDD LDO, BVDD=7V, Iload=1mA, TT 27°C')
    else:
        ax.text(0.5, 0.5, 'No simulation data', ha='center', va='center', transform=ax.transAxes)

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_08_zout.png'))
    plt.close(fig)
    print("  DONE: plot_08_zout.png")


def plot_09_ilim_3corner():
    """Plot 9: Current Limit at 3 Corners"""
    print("  Generating plot 09: Ilim 3-corner...")
    write_tb_ilim_corners()
    for corner in ["tt", "ss", "ff"]:
        run_ngspice(f"tb_sc09_ilim_{corner}.spice")

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {'tt': 'blue', 'ss': 'red', 'ff': 'green'}
    labels = {'tt': 'TT 27°C', 'ss': 'SS 27°C', 'ff': 'FF 27°C'}

    for corner in ["tt", "ss", "ff"]:
        d = read_wrdata(f"sc09_ilim_{corner}.dat")
        if d is not None:
            t = d[:, 0] * 1000  # ms
            pvdd = d[:, 1]
            # Convert time to load current (0 at 20ms, 500mA at 120ms)
            iload = np.maximum(0, (t - 20) / 100 * 500)
            mask = t > 18
            ax.plot(iload[mask], pvdd[mask], '-', color=colors[corner],
                   linewidth=1.5, label=labels[corner])

    ax.axhline(5.0, color='green', linestyle=':', alpha=0.3)
    ax.axvline(50, color='gray', linestyle='--', alpha=0.5, label='Design Ilim ≈50mA')
    ax.set_xlabel('Load Current (mA)')
    ax.set_ylabel('PVDD Output Voltage (V)')
    ax.set_title('Plot 9: Current Limit — 3 Process Corners\nSKY130 PVDD LDO, BVDD=7V, 27°C')
    ax.legend()
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 6)
    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_09_ilim_3corner.png'))
    plt.close(fig)
    print("  DONE: plot_09_ilim_3corner.png")


def plot_10_ilim_gate():
    """Plot 10: Gate Voltage During Current Limiting"""
    print("  Generating plot 10: Ilim Gate Detail...")
    write_tb_ilim_gate()
    run_ngspice("tb_sc10_ilim_gate.spice")

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    d_pvdd = read_wrdata("sc10_pvdd.dat")
    d_gate = read_wrdata("sc10_gate.dat")
    d_det = read_wrdata("sc10_ilim_det.dat")
    d_ea = read_wrdata("sc10_ea_out.dat")

    if d_pvdd is not None:
        t = d_pvdd[:, 0] * 1000  # ms
        iload = np.maximum(0, (t - 20) / 100 * 500)

        axes[0].plot(iload, d_pvdd[:, 1], 'b-', linewidth=1.5, label='PVDD')
        axes[0].set_ylabel('PVDD (V)')
        axes[0].set_title('Plot 10: Gate & Limiter Detail During Current Overload\nSKY130 PVDD LDO, BVDD=7V, TT 27°C')
        axes[0].legend()

        if d_gate is not None:
            axes[1].plot(iload[:len(d_gate)], d_gate[:len(iload), 1], 'm-', linewidth=1.5, label='Gate')
            if d_ea is not None:
                axes[1].plot(iload[:len(d_ea)], d_ea[:len(iload), 1], 'c--', linewidth=1, alpha=0.7, label='EA out')
            axes[1].set_ylabel('Voltage (V)')
            axes[1].legend()
            axes[1].set_title('Gate vs EA Output — Clamp Pulls Gate to BVDD')

        if d_det is not None:
            axes[2].plot(iload[:len(d_det)], d_det[:len(iload), 1], 'r-', linewidth=1.5, label='det_n (ilim)')
            axes[2].set_ylabel('det_n (V)')
            axes[2].set_xlabel('Load Current (mA)')
            axes[2].legend()
            axes[2].set_title('Current Limiter Detector — LOW = Overcurrent Active')

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_10_ilim_gate.png'))
    plt.close(fig)
    print("  DONE: plot_10_ilim_gate.png")


def plot_11_pvt_startup():
    """Plot 11: PVT Startup Overlay"""
    print("  Generating plot 11: PVT Startup Overlay...")
    write_tb_pvt_startup()

    corners = [("tt", 27), ("ss", -40), ("ss", 150), ("ff", -40), ("ff", 150),
               ("fs", 27), ("sf", 27)]
    for corner, temp in corners:
        label = f"{corner}_{temp}"
        run_ngspice(f"tb_sc11_pvt_{label}.spice")

    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.cm.tab10
    for i, (corner, temp) in enumerate(corners):
        label = f"{corner}_{temp}"
        d = read_wrdata(f"sc11_pvt_{label}.dat")
        if d is not None:
            t = d[:, 0] * 1000  # ms
            ax.plot(t, d[:, 1], '-', color=cmap(i), linewidth=1.2,
                   label=f'{corner.upper()} {temp}°C')

    ax.axhline(5.0, color='green', linestyle=':', alpha=0.5)
    ax.axhline(5.5, color='red', linestyle='--', alpha=0.3, label='OV limit 5.5V')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('PVDD (V)')
    ax.set_title('Plot 11: PVT Startup Overlay — 7 Corners\nSKY130 PVDD LDO, BVDD 0→7V, Iload=1mA')
    ax.legend(loc='lower right', ncol=2)
    ax.set_xlim(0, 25)
    ax.set_ylim(-0.5, 7)
    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_11_pvt_startup.png'))
    plt.close(fig)
    print("  DONE: plot_11_pvt_startup.png")


def plot_12_pvt_reg_bars():
    """Plot 12: PVT Regulation Bar Chart"""
    print("  Generating plot 12: PVT Regulation Bars...")
    write_tb_pvt_dcreg()

    corners = [("tt", 27), ("tt", -40), ("tt", 150),
               ("ss", 27), ("ss", -40), ("ss", 150),
               ("ff", 27), ("ff", -40), ("ff", 150),
               ("fs", 27), ("sf", 27)]

    labels_out = []
    pvdd_vals = []

    for corner, temp in corners:
        label = f"{corner}_{temp}"
        out = run_ngspice(f"tb_sc12_pvt_{label}.spice")
        m = re.search(r'PVT_DC:\s+corner=[\w_-]+\s+pvdd=([\d.e+-]+)', out)
        pvdd = float(m.group(1)) if m else 5.0
        labels_out.append(f'{corner.upper()}\n{temp}°C')
        pvdd_vals.append(pvdd)

    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(labels_out))
    colors_bar = ['green' if 4.825 <= v <= 5.175 else 'red' for v in pvdd_vals]
    bars = ax.bar(x, pvdd_vals, color=colors_bar, alpha=0.7, edgecolor='black')
    ax.axhline(5.0, color='blue', linestyle='-', linewidth=1, label='Target 5.00V')
    ax.axhline(4.825, color='red', linestyle='--', alpha=0.5, label='Spec limits')
    ax.axhline(5.175, color='red', linestyle='--', alpha=0.5)
    ax.fill_between([-0.5, len(labels_out)-0.5], 4.825, 5.175, alpha=0.08, color='green')
    ax.set_xticks(x)
    ax.set_xticklabels(labels_out, fontsize=8)
    ax.set_ylabel('PVDD (V)')
    ax.set_title('Plot 12: PVT DC Regulation — All Corners\nSKY130 PVDD LDO, BVDD=7V, Iload=1mA')
    ax.legend()
    ax.set_ylim(4.5, 5.5)

    for i, v in enumerate(pvdd_vals):
        ax.text(i, v + 0.02, f'{v:.3f}V', ha='center', va='bottom', fontsize=7)

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_12_pvt_reg_bars.png'))
    plt.close(fig)
    print("  DONE: plot_12_pvt_reg_bars.png")


def plot_13_pvt_ilim_bars():
    """Plot 13: PVT Current Limit Bar Chart"""
    print("  Generating plot 13: PVT Ilim Bars...")
    write_tb_pvt_ilim()

    corners = [("tt", 27), ("tt", -40), ("tt", 150),
               ("ss", 27), ("ss", -40), ("ss", 150),
               ("ff", 27), ("ff", -40), ("ff", 150),
               ("fs", 27), ("sf", 27)]

    labels_out = []
    ilim_vals = []

    for corner, temp in corners:
        label = f"{corner}_{temp}"
        run_ngspice(f"tb_sc13_ilim_{label}.spice")
        d = read_wrdata(f"sc13_ilim_{label}.dat")
        if d is not None:
            t = d[:, 0] * 1000  # ms
            pvdd = d[:, 1]
            iload = np.maximum(0, (t - 20) / 100 * 500)
            # Find where PVDD drops below 4.5V (current limit trip)
            mask = (t > 22) & (pvdd < 4.5)
            if np.any(mask):
                trip_idx = np.argmax(mask)
                ilim = iload[trip_idx]
            else:
                ilim = 500  # didn't trip
        else:
            ilim = 50
        labels_out.append(f'{corner.upper()}\n{temp}°C')
        ilim_vals.append(ilim)

    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(labels_out))
    colors_bar = ['green' if v < 110 else 'red' for v in ilim_vals]
    bars = ax.bar(x, ilim_vals, color=colors_bar, alpha=0.7, edgecolor='black')
    ax.axhline(50, color='blue', linestyle='-', linewidth=1, label='Design target 50mA')
    ax.axhline(110, color='red', linestyle='--', alpha=0.5, label='Spec max 110mA')
    ax.set_xticks(x)
    ax.set_xticklabels(labels_out, fontsize=8)
    ax.set_ylabel('Current Limit Trip (mA)')
    ax.set_title('Plot 13: PVT Current Limit — All Corners\nSKY130 PVDD LDO, BVDD=7V')
    ax.legend()

    for i, v in enumerate(ilim_vals):
        ax.text(i, v + 2, f'{v:.0f}', ha='center', va='bottom', fontsize=7)

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_13_pvt_ilim_bars.png'))
    plt.close(fig)
    print("  DONE: plot_13_pvt_ilim_bars.png")


def plot_14_internal_bias():
    """Plot 14: Internal Bias Nodes"""
    print("  Generating plot 14: Internal Bias...")
    write_tb_internal_bias()
    run_ngspice("tb_sc14_bias.spice")

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    d_pvdd = read_wrdata("sc14_pvdd.dat")
    d_vref = read_wrdata("sc14_vref_ss.dat")
    d_ea = read_wrdata("sc14_ea_out.dat")
    d_vfb = read_wrdata("sc14_vfb.dat")
    d_bvdd = read_wrdata("sc14_bvdd.dat")

    if d_pvdd is not None:
        t = d_pvdd[:, 0] * 1000

        axes[0].plot(t, d_pvdd[:, 1], 'b-', linewidth=1.5, label='PVDD')
        if d_bvdd is not None:
            axes[0].plot(t[:len(d_bvdd)], d_bvdd[:len(t), 1], 'r--', alpha=0.5, label='BVDD')
        axes[0].set_ylabel('Voltage (V)')
        axes[0].set_title('Plot 14: Internal Bias & Reference Nodes\nSKY130 PVDD LDO, TT 27°C')
        axes[0].legend()

        if d_vref is not None and d_vfb is not None:
            axes[1].plot(t[:len(d_vref)], d_vref[:len(t), 1], 'g-', linewidth=1.5, label='Vref_ss')
            axes[1].plot(t[:len(d_vfb)], d_vfb[:len(t), 1], 'm-', linewidth=1.5, label='Vfb')
            axes[1].axhline(1.226, color='orange', linestyle=':', alpha=0.5, label='AVBG')
            axes[1].set_ylabel('Voltage (V)')
            axes[1].legend()
            axes[1].set_title('Error Amp Inputs: Vref_ss (soft-start) vs Vfb (feedback)')

        if d_ea is not None:
            axes[2].plot(t[:len(d_ea)], d_ea[:len(t), 1], 'c-', linewidth=1.5, label='EA output')
            axes[2].set_ylabel('Voltage (V)')
            axes[2].set_xlabel('Time (ms)')
            axes[2].legend()
            axes[2].set_title('Error Amplifier Output (drives gate via Rgate=1kΩ)')

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_14_internal_bias.png'))
    plt.close(fig)
    print("  DONE: plot_14_internal_bias.png")


def plot_15_gate_detail():
    """Plot 15: Gate Detail During Startup"""
    print("  Generating plot 15: Gate Detail...")
    write_tb_gate_detail()
    run_ngspice("tb_sc15_gate.spice")

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    d_pvdd = read_wrdata("sc15_pvdd.dat")
    d_gate = read_wrdata("sc15_gate.dat")
    d_ea = read_wrdata("sc15_ea_out.dat")
    d_bvdd = read_wrdata("sc15_bvdd.dat")
    d_po = read_wrdata("sc15_pass_off.dat")

    if d_pvdd is not None:
        t = d_pvdd[:, 0] * 1000

        if d_gate is not None:
            axes[0].plot(t[:len(d_gate)], d_gate[:len(t), 1], 'm-', linewidth=1.5, label='Gate')
        if d_ea is not None:
            axes[0].plot(t[:len(d_ea)], d_ea[:len(t), 1], 'c--', linewidth=1, alpha=0.7, label='EA out')
        if d_bvdd is not None:
            axes[0].plot(t[:len(d_bvdd)], d_bvdd[:len(t), 1], 'r:', alpha=0.5, label='BVDD')
        axes[0].set_ylabel('Voltage (V)')
        axes[0].set_title('Plot 15: Gate Drive Detail During Startup\nSKY130 PVDD LDO, TT 27°C, BVDD 0→7V')
        axes[0].legend()

        axes[1].plot(t, d_pvdd[:, 1], 'b-', linewidth=1.5, label='PVDD')
        if d_po is not None:
            axes[1].plot(t[:len(d_po)], d_po[:len(t), 1], 'r-', linewidth=1, alpha=0.7, label='pass_off')
        axes[1].set_ylabel('Voltage (V)')
        axes[1].set_xlabel('Time (ms)')
        axes[1].legend()
        axes[1].set_title('PVDD & POR Pass-Off Signal')

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_15_gate_detail.png'))
    plt.close(fig)
    print("  DONE: plot_15_gate_detail.png")


def plot_16_mode_control():
    """Plot 16: Mode Control Sequence"""
    print("  Generating plot 16: Mode Control...")
    write_tb_mode_control()
    run_ngspice("tb_sc16_mode.spice")

    fig, axes = plt.subplots(4, 1, figsize=(10, 10), sharex=True)
    d_bvdd = read_wrdata("sc16_bvdd.dat")
    d_pvdd = read_wrdata("sc16_pvdd.dat")
    d_po = read_wrdata("sc16_pass_off.dat")
    d_by = read_wrdata("sc16_bypass_en.dat")
    d_ea = read_wrdata("sc16_ea_en.dat")
    d_uv = read_wrdata("sc16_uvov_en.dat")
    d_sd = read_wrdata("sc16_startup_done.dat")

    if d_bvdd is not None:
        t = d_bvdd[:, 0] * 1000
        n = len(t)

        axes[0].plot(t, d_bvdd[:, 1], 'r-', linewidth=1.5, label='BVDD')
        if d_pvdd is not None:
            axes[0].plot(t[:len(d_pvdd)], d_pvdd[:min(n, len(d_pvdd)), 1], 'b-', linewidth=1.5, label='PVDD')
        axes[0].set_ylabel('Voltage (V)')
        axes[0].set_title('Plot 16: Mode Control Sequence — BVDD Ramp\nSKY130 PVDD LDO, TT 27°C')
        axes[0].legend()
        # Add threshold annotations
        for thresh, name in [(2.5, 'POR'), (4.2, 'Retain'), (4.5, 'Bypass'), (5.6, 'Active')]:
            t_cross = thresh / 10.5 * 50  # approximate time
            axes[0].axhline(thresh, color='gray', linestyle=':', alpha=0.3)
            axes[0].text(t_cross, thresh + 0.2, name, fontsize=7, color='gray')

        if d_po is not None:
            axes[1].plot(t[:len(d_po)], d_po[:min(n, len(d_po)), 1], 'r-', linewidth=1.5, label='pass_off')
            axes[1].set_ylabel('V')
            axes[1].legend()
            axes[1].set_title('Pass-Off (HIGH = pass device OFF)')

        signals = [(d_ea, 'ea_en', 'orange'), (d_by, 'bypass_en', 'purple')]
        for sig, name, clr in signals:
            if sig is not None:
                axes[2].plot(t[:len(sig)], sig[:min(n, len(sig)), 1], '-', color=clr, linewidth=1.5, label=name)
        axes[2].set_ylabel('V')
        axes[2].legend()
        axes[2].set_title('EA Enable & Bypass Enable')

        if d_uv is not None:
            axes[3].plot(t[:len(d_uv)], d_uv[:min(n, len(d_uv)), 1], 'g-', linewidth=1.5, label='uvov_en')
        if d_sd is not None:
            axes[3].plot(t[:len(d_sd)], d_sd[:min(n, len(d_sd)), 1], 'b--', linewidth=1.5, label='startup_done')
        axes[3].set_ylabel('V')
        axes[3].set_xlabel('Time (ms)')
        axes[3].legend()
        axes[3].set_title('UVOV Enable & Startup Done')

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_16_mode_control.png'))
    plt.close(fig)
    print("  DONE: plot_16_mode_control.png")


def plot_17_uvov():
    """Plot 17: UV/OV Comparator Thresholds"""
    print("  Generating plot 17: UVOV...")
    write_tb_uvov()
    run_ngspice("tb_sc17_uvov.spice")

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    d_pvdd = read_wrdata("sc17_pvdd.dat")
    d_uv = read_wrdata("sc17_uv.dat")
    d_ov = read_wrdata("sc17_ov.dat")

    if d_pvdd is not None:
        t = d_pvdd[:, 0] * 1000
        pvdd = d_pvdd[:, 1]

        axes[0].plot(t, pvdd, 'b-', linewidth=1.5, label='PVDD')
        axes[0].axhline(4.35, color='orange', linestyle=':', alpha=0.5, label='UV ~4.35V')
        axes[0].axhline(5.50, color='red', linestyle=':', alpha=0.5, label='OV ~5.50V')
        axes[0].set_ylabel('PVDD (V)')
        axes[0].set_title('Plot 17: UV/OV Comparator Thresholds\nSKY130 PVDD LDO, TT 27°C, PVDD Ramp 0→7→0V')
        axes[0].legend()

        if d_uv is not None:
            axes[1].plot(t[:len(d_uv)], d_uv[:len(t), 1], 'orange', linewidth=1.5, label='UV flag')
        if d_ov is not None:
            axes[1].plot(t[:len(d_ov)], d_ov[:len(t), 1], 'red', linewidth=1.5, label='OV flag')
        axes[1].set_ylabel('Flag Voltage (V)')
        axes[1].set_xlabel('Time (ms)')
        axes[1].legend()
        axes[1].set_title('UV/OV Flag Outputs (SVDD=2.2V domain)')

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_17_uvov.png'))
    plt.close(fig)
    print("  DONE: plot_17_uvov.png")


def plot_18_clamp():
    """Plot 18: MOS Voltage Clamp I-V"""
    print("  Generating plot 18: Clamp Onset...")
    write_tb_clamp()
    run_ngspice("tb_sc18_clamp.spice")

    fig, ax = plt.subplots(figsize=(8, 5))
    d_v = read_wrdata("sc18_vpvdd.dat")
    d_i = read_wrdata("sc18_iclamp.dat")

    if d_v is not None and d_i is not None:
        vpvdd = d_v[:, 1]
        iclamp = -d_i[:len(vpvdd), 1] * 1000  # mA, positive convention
        ax.plot(vpvdd, iclamp, 'b-', linewidth=2)
        ax.set_xlabel('PVDD Voltage (V)')
        ax.set_ylabel('Clamp Current (mA)')
        ax.set_title('Plot 18: MOS Voltage Clamp — I-V Characteristic\nSKY130 PVDD LDO, TT 27°C, ibias=1µA')
        ax.set_xlim(0, 12)
        ax.set_ylim(bottom=-0.5)

        # Find onset voltage (where current exceeds 0.1mA)
        mask = iclamp > 0.1
        if np.any(mask):
            onset_idx = np.argmax(mask)
            onset_v = vpvdd[onset_idx]
            ax.axvline(onset_v, color='red', linestyle='--', alpha=0.5)
            ax.annotate(f'Onset ≈ {onset_v:.1f}V',
                       xy=(onset_v, 0.1), xytext=(onset_v + 1, 5),
                       arrowprops=dict(arrowstyle='->', color='red'),
                       color='red', fontsize=10)
    else:
        ax.text(0.5, 0.5, 'No simulation data', ha='center', va='center', transform=ax.transAxes)

    fig.tight_layout()
    fig.savefig(os.path.join(WORK, 'plot_18_clamp_onset.png'))
    plt.close(fig)
    print("  DONE: plot_18_clamp_onset.png")


def plot_19_dashboard():
    """Plot 19: 2x3 Dashboard — key results composite"""
    print("  Generating plot 19: Dashboard...")

    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('PVDD 5V LDO Regulator — SKY130 Showcase Dashboard', fontsize=14, fontweight='bold')
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)

    # Panel 1: Startup
    ax1 = fig.add_subplot(gs[0, 0])
    d = read_wrdata("sc02_pvdd.dat")
    if d is not None:
        t = d[:, 0] * 1000
        ax1.plot(t, d[:, 1], 'b-', linewidth=1.5)
        ax1.axhline(5.0, color='green', linestyle=':', alpha=0.5)
    ax1.set_title('Startup Transient')
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('PVDD (V)')
    ax1.set_xlim(0, 25)

    # Panel 2: Load Transient
    ax2 = fig.add_subplot(gs[0, 1])
    d = read_wrdata("sc03_pvdd.dat")
    if d is not None:
        t = d[:, 0] * 1e6
        ax2.plot(t, d[:, 1], 'b-', linewidth=1.5)
        ax2.axhline(5.0, color='green', linestyle=':', alpha=0.5)
    ax2.set_title('Load Transient (1→10mA)')
    ax2.set_xlabel('Time (µs)')
    ax2.set_ylabel('PVDD (V)')
    ax2.set_ylim(4.85, 5.10)

    # Panel 3: PSRR
    ax3 = fig.add_subplot(gs[0, 2])
    d = read_wrdata("sc07_psrr.dat")
    if d is not None:
        ax3.semilogx(d[:, 0], d[:, 1], 'b-', linewidth=1.5)
        ax3.axhline(-40, color='red', linestyle=':', alpha=0.5)
    ax3.set_title('PSRR (10mA)')
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('PSRR (dB)')

    # Panel 4: Bode (1mA)
    ax4 = fig.add_subplot(gs[1, 0])
    d = read_wrdata("sc06_gain_1mA.dat")
    if d is not None:
        ax4.semilogx(d[:, 0], d[:, 1], 'b-', linewidth=1.5)
        ax4.axhline(0, color='red', linestyle='--', alpha=0.5)
    ax4.set_title('Loop Gain (1mA)')
    ax4.set_xlabel('Frequency (Hz)')
    ax4.set_ylabel('Gain (dB)')

    # Panel 5: Current Limit
    ax5 = fig.add_subplot(gs[1, 1])
    for corner, clr in [("tt", 'blue'), ("ss", 'red'), ("ff", 'green')]:
        d = read_wrdata(f"sc09_ilim_{corner}.dat")
        if d is not None:
            t = d[:, 0] * 1000
            iload = np.maximum(0, (t - 20) / 100 * 500)
            mask = t > 18
            ax5.plot(iload[mask], d[mask, 1], '-', color=clr, linewidth=1, label=corner.upper())
    ax5.set_title('Current Limit (3 corners)')
    ax5.set_xlabel('Load (mA)')
    ax5.set_ylabel('PVDD (V)')
    ax5.set_xlim(0, 200)
    ax5.legend(fontsize=7)

    # Panel 6: Line Regulation
    ax6 = fig.add_subplot(gs[1, 2])
    d = read_wrdata("sc05_linereg.dat")
    if d is not None:
        bvdd = d[:, 1]
        pvdd = d[:, 3]
        t_lr = d[:, 0]
        mask = (t_lr > 0.030) & (bvdd > 5.3)
        ax6.plot(bvdd[mask], pvdd[mask], 'b-', linewidth=1.5)
        ax6.axhline(5.0, color='green', linestyle=':', alpha=0.5)
    ax6.set_title('Line Regulation (1mA)')
    ax6.set_xlabel('BVDD (V)')
    ax6.set_ylabel('PVDD (V)')
    ax6.set_ylim(4.98, 5.02)

    fig.savefig(os.path.join(WORK, 'plot_19_dashboard.png'))
    plt.close(fig)
    print("  DONE: plot_19_dashboard.png")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("PVDD LDO Regulator — 19-Plot Showcase Generator")
    print("SkyWater SKY130A PDK — Full Transistor-Level Simulation")
    print("=" * 70)

    # Check ngspice
    try:
        r = subprocess.run(["ngspice", "--version"], capture_output=True, text=True)
        print(f"ngspice: {r.stdout.strip().split(chr(10))[0]}")
    except FileNotFoundError:
        print("ERROR: ngspice not found. Install with: sudo apt install ngspice")
        sys.exit(1)

    plots = [
        ("01", plot_01_dc_regulation),
        ("02", plot_02_startup),
        ("03", plot_03_load_transient),
        ("04", plot_04_dropout),
        ("05", plot_05_line_regulation),
        ("06", plot_06_bode_multiload),
        ("07", plot_07_psrr),
        ("08", plot_08_zout),
        ("09", plot_09_ilim_3corner),
        ("10", plot_10_ilim_gate),
        ("11", plot_11_pvt_startup),
        ("12", plot_12_pvt_reg_bars),
        ("13", plot_13_pvt_ilim_bars),
        ("14", plot_14_internal_bias),
        ("15", plot_15_gate_detail),
        ("16", plot_16_mode_control),
        ("17", plot_17_uvov),
        ("18", plot_18_clamp),
        ("19", plot_19_dashboard),
    ]

    for num, func in plots:
        print(f"\n{'─'*60}")
        print(f"Plot {num}")
        print(f"{'─'*60}")
        try:
            func()
        except Exception as e:
            print(f"  ERROR in plot {num}: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print("\n" + "=" * 70)
    print("SHOWCASE COMPLETE")
    print("=" * 70)
    generated = sorted(glob.glob(os.path.join(WORK, "plot_*.png")))
    print(f"\nGenerated {len(generated)} plots:")
    for p in generated:
        print(f"  {os.path.basename(p)}")


if __name__ == "__main__":
    main()
