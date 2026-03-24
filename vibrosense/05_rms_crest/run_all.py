#!/usr/bin/env python3
"""
Block 05: Transistor-Level Simulation Suite
RMS + Peak Detector + Crest Factor — SKY130 PDK
All real MOSFETs, no behavioral models.
"""

import subprocess, numpy as np, os, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

WORKDIR = '/home/ubuntu/analog-ai-chips/vibrosense/05_rms_crest'
os.chdir(WORKDIR)

HEADER = """\
.include sky130_pdk_fixup.spice
.lib sky130.lib.spice tt
.include design.cir
VDD vdd gnd 1.8
VSS vss gnd 0
Vbn vbn gnd 0.65
Vcm vcm gnd 0.9
"""

def run_ngspice(fname, timeout=300):
    r = subprocess.run(['ngspice','-b',fname], capture_output=True, text=True, timeout=timeout, cwd=WORKDIR)
    if 'No. of Data Rows' in r.stdout:
        return True
    print(f"  FAIL: {fname}")
    for line in r.stdout.split('\n')[-10:]:
        if line.strip(): print(f"    {line.strip()}")
    return False

results = {}

# ================================================================
# TEST 1: RMS Linearity
# ================================================================
print("="*60)
print("TEST 1: RMS Linearity (10-300mVpk, 1kHz sine)")
print("="*60)

amplitudes = [0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3]
rms_meas = []; rms_ideal = []

for amp in amplitudes:
    fname = f'tb_rms_lin_{amp:.3f}.spice'
    with open(fname,'w') as f:
        f.write(f"""* RMS Linearity - Amp={amp}
{HEADER}
Vreset reset gnd PULSE(1.8 0 2m 1n 1n 10k 20k)
Vin inp gnd SIN(0.9 {amp} 1k)
Xdut inp rms_out peak_out vdd vss reset vbn vcm rms_crest_top
.options reltol=1e-3 abstol=1e-12
.tran 10u 200m
.control
run
wrdata tb_rms_lin_{amp:.3f}.csv v(rms_out) v(vcm)
quit
.endc
.end
""")
    if run_ngspice(fname):
        d = np.loadtxt(f'tb_rms_lin_{amp:.3f}.csv')
        t,vr,_,vc = d[:,0],d[:,1],d[:,2],d[:,3]
        mask = t > 0.15
        vrms_avg = np.mean(vr[mask])
        vcm_avg = np.mean(vc[mask])
        mav_meas = vrms_avg - vcm_avg  # positive sense (rect_out > Vcm)
        ideal_mav = amp * 2/np.pi
        rms_meas.append(mav_meas)
        rms_ideal.append(ideal_mav)
        ratio = mav_meas/ideal_mav if ideal_mav > 0 else 0
        print(f"  Amp={amp*1000:5.0f}mVpk: MAV_meas={mav_meas*1000:7.2f}mV  "
              f"MAV_ideal={ideal_mav*1000:6.2f}mV  ratio={ratio:.3f}")
    else:
        rms_meas.append(np.nan); rms_ideal.append(amp*2/np.pi)

rm = np.array(rms_meas); ri = np.array(rms_ideal)
valid = ~np.isnan(rm) & (rm > 0)
if np.sum(valid) >= 3:
    coeffs = np.polyfit(ri[valid], rm[valid], 1)
    pred = np.polyval(coeffs, ri[valid])
    ss_res = np.sum((rm[valid]-pred)**2)
    ss_tot = np.sum((rm[valid]-rm[valid].mean())**2)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
    results['rms_linearity_r2'] = float(r2)
    results['rms_linearity_slope'] = float(coeffs[0])
    results['rms_linearity_pass'] = r2 > 0.99
    print(f"\n  R2 = {r2:.6f}  Slope = {coeffs[0]:.3f}  "
          f"{'PASS' if r2>0.99 else 'FAIL'}")

    idx100 = amplitudes.index(0.1)
    if not np.isnan(rm[idx100]):
        rms_cal = rm[idx100] / coeffs[0] * np.pi / (2*np.sqrt(2))
        rms_id = 0.1/np.sqrt(2)
        err = abs(rms_cal - rms_id)/rms_id * 100
        results['rms_accuracy_pct'] = float(err)
        results['rms_accuracy_pass'] = err < 5
        print(f"  RMS accuracy @100mVpk (calibrated): {err:.2f}% {'PASS' if err<5 else 'FAIL'}")

    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(14,6))
    ax1.plot(ri[valid]*1000, rm[valid]*1000, 'bo-', ms=6, label='Measured MAV')
    fit_x = np.linspace(0, ri[valid].max(), 100)
    ax1.plot(fit_x*1000, np.polyval(coeffs, fit_x)*1000, 'r--', label=f'Fit (R2={r2:.5f})')
    ax1.set_xlabel('Ideal MAV (mV)'); ax1.set_ylabel('Measured MAV (mV)')
    ax1.set_title(f'RMS Linearity (SKY130 transistor-level)')
    ax1.legend(); ax1.grid(True,alpha=0.3)
    residual = (rm[valid] - np.polyval(coeffs, ri[valid])) / np.polyval(coeffs, ri[valid]) * 100
    ax2.plot(ri[valid]*1000, residual, 'ro-', ms=6)
    ax2.axhline(0, color='gray', ls='--', alpha=0.5)
    ax2.set_xlabel('Ideal MAV (mV)'); ax2.set_ylabel('Residual (%)')
    ax2.set_title('Linearity Residual Error'); ax2.grid(True,alpha=0.3)
    plt.tight_layout(); plt.savefig('plot_rms_linearity.png', dpi=150)
    print("  Saved plot_rms_linearity.png\n")

# ================================================================
# TEST 2: RMS Frequency Response
# ================================================================
print("="*60)
print("TEST 2: RMS Frequency Response (100mVpk, 10Hz-20kHz)")
print("="*60)

frequencies = [10, 50, 100, 500, 1000, 2000, 5000, 10000, 20000]
rms_freq = []

for freq in frequencies:
    sim_time = max(0.3, 10.0/freq + 0.1)
    meas_start = max(0.2, 5.0/freq)
    tstep = min(10e-6, 0.5/freq)
    fname = f'tb_rms_freq_{freq}.spice'
    with open(fname,'w') as f:
        f.write(f"""* RMS Freq Response - f={freq}Hz
{HEADER}
Vreset reset gnd PULSE(1.8 0 2m 1n 1n 10k 20k)
Vin inp gnd SIN(0.9 0.1 {freq})
Xdut inp rms_out peak_out vdd vss reset vbn vcm rms_crest_top
.options reltol=1e-3
.tran {tstep:.6e} {sim_time:.3f}
.control
run
wrdata tb_rms_freq_{freq}.csv v(rms_out) v(vcm)
quit
.endc
.end
""")
    if run_ngspice(fname, timeout=600):
        d = np.loadtxt(f'tb_rms_freq_{freq}.csv')
        t,vr,_,vc = d[:,0],d[:,1],d[:,2],d[:,3]
        mask = t > meas_start
        if np.sum(mask) > 10:
            mav = np.mean(vr[mask]) - np.mean(vc[mask])
            rms_freq.append(mav)
            print(f"  f={freq:6d}Hz: MAV={mav*1000:.2f}mV")
        else:
            rms_freq.append(np.nan)
    else:
        rms_freq.append(np.nan)

rf = np.array(rms_freq); freqs = np.array(frequencies)
vf = ~np.isnan(rf) & (rf > 0)
if np.sum(vf) >= 3:
    idx1k = list(frequencies).index(1000)
    if not np.isnan(rf[idx1k]):
        ref = rf[idx1k]
        db = 20*np.log10(np.maximum(rf[vf],1e-12)/ref)
        above = db > -3
        bw_f = freqs[vf][above]
        if len(bw_f) > 0:
            results['rms_bw_low'] = int(bw_f[0])
            results['rms_bw_high'] = int(bw_f[-1])
            results['rms_bw_pass'] = (bw_f[0] <= 20 and bw_f[-1] >= 10000)
            print(f"\n  -3dB BW: {bw_f[0]}Hz - {bw_f[-1]}Hz "
                  f"{'PASS' if results['rms_bw_pass'] else 'FAIL'}")

        fig, ax = plt.subplots(figsize=(10,6))
        ax.semilogx(freqs[vf], db, 'bo-', ms=8, lw=2)
        ax.axhline(-3, color='r', ls='--', alpha=0.7, label='-3dB')
        ax.fill_between([10,10000],-3,3,alpha=0.1,color='green')
        ax.set_xlabel('Frequency (Hz)'); ax.set_ylabel('dB re 1kHz')
        ax.set_title('RMS Frequency Response (SKY130 transistor-level)')
        ax.legend(); ax.grid(True,alpha=0.3); ax.set_ylim(-10,5)
        plt.tight_layout(); plt.savefig('plot_rms_freq_response.png', dpi=150)
        print("  Saved plot_rms_freq_response.png\n")

# ================================================================
# TEST 3: Peak Hold Time
# ================================================================
print("="*60)
print("TEST 3: Peak Hold Time")
print("="*60)

with open('tb_peak_hold.spice','w') as f:
    f.write(f"""* Peak Hold Test
{HEADER}
Vreset reset gnd PULSE(1.8 0 2m 1n 1n 10k 20k)
Venv env gnd PWL(0 0 2m 0 2.5m 0.1 12m 0.1 12.5m 0 100 0)
Bvin inp gnd V = 0.9 + V(env)*sin(2*3.14159*1000*time)
Xdut inp rms_out peak_out vdd vss reset vbn vcm rms_crest_top
.options reltol=1e-3
.tran 100u 2
.control
run
wrdata tb_peak_hold.csv v(peak_out) v(vcm)
quit
.endc
.end
""")

if run_ngspice('tb_peak_hold.spice', timeout=600):
    d = np.loadtxt('tb_peak_hold.csv')
    t,vp,_,vc = d[:,0],d[:,1],d[:,2],d[:,3]
    vcm = np.mean(vc[t>1])

    idx15m = np.argmin(abs(t-0.015))
    idx500m = np.argmin(abs(t-0.5))
    idx1s = np.argmin(abs(t-1.0))

    vp_init = vp[idx15m]
    sig = vp_init - vcm
    if sig > 0.001:
        decay500 = (vp_init - vp[idx500m]) / sig * 100
        decay1s = (vp_init - vp[idx1s]) / sig * 100
    else:
        decay500 = 999; decay1s = 999

    results['peak_hold_decay_500ms'] = float(decay500)
    results['peak_hold_pass'] = decay500 < 10
    print(f"  Peak @15ms: {vp_init*1000:.1f}mV ({sig*1000:.1f}mV above Vcm)")
    print(f"  Decay @500ms: {decay500:.1f}%  @1s: {decay1s:.1f}%")
    print(f"  {'PASS' if decay500<10 else 'FAIL'}")

    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(t*1000, (vp-vcm)*1000, 'r-', lw=2, label='V_peak - Vcm')
    ax.axhline(sig*1000, color='g', ls='--', alpha=0.5, label=f'Initial: {sig*1000:.1f}mV')
    ax.axhline(sig*1000*0.9, color='orange', ls='--', alpha=0.5, label='90%')
    ax.axvline(500, color='gray', ls=':', alpha=0.5, label='500ms')
    ax.set_xlabel('Time (ms)'); ax.set_ylabel('Peak - Vcm (mV)')
    ax.set_title('Peak Hold Time (SKY130 transistor-level)')
    ax.legend(); ax.grid(True,alpha=0.3); ax.set_xlim(0,2000)
    plt.tight_layout(); plt.savefig('plot_peak_hold.png', dpi=150)
    print("  Saved plot_peak_hold.png\n")

# ================================================================
# TEST 4: Peak Accuracy
# ================================================================
print("="*60)
print("TEST 4: Peak Accuracy")
print("="*60)

peak_amps = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3]
pk_meas = []; pk_ideal = []

for amp in peak_amps:
    fname = f'tb_peak_acc_{amp:.3f}.spice'
    with open(fname,'w') as f:
        f.write(f"""* Peak Accuracy - Amp={amp}
{HEADER}
Vreset reset gnd PULSE(1.8 0 2m 1n 1n 10k 20k)
Vin inp gnd SIN(0.9 {amp} 1k)
Xdut inp rms_out peak_out vdd vss reset vbn vcm rms_crest_top
.options reltol=1e-3
.tran 10u 50m
.control
run
wrdata tb_peak_acc_{amp:.3f}.csv v(peak_out) v(vcm)
quit
.endc
.end
""")
    if run_ngspice(fname):
        d = np.loadtxt(f'tb_peak_acc_{amp:.3f}.csv')
        t,vp,_,vc = d[:,0],d[:,1],d[:,2],d[:,3]
        vcm = np.mean(vc[t>0.03])
        pk = np.max(vp[t>0.01])
        # Use INPUT Vcm = 0.9V for ideal peak (not loaded Vcm_int)
        inp_vcm = 0.9
        pk_id = inp_vcm + amp
        err = abs(pk - pk_id)/amp*100
        pk_meas.append(pk-inp_vcm); pk_ideal.append(amp)
        print(f"  Amp={amp*1000:5.0f}mVpk: meas={pk*1000:.1f}mV  "
              f"ideal={pk_id*1000:.1f}mV  err={err:.1f}%")
    else:
        pk_meas.append(np.nan); pk_ideal.append(amp)

idx100 = peak_amps.index(0.1)
if not np.isnan(pk_meas[idx100]):
    err100 = abs(pk_meas[idx100] - pk_ideal[idx100])/pk_ideal[idx100]*100
    results['peak_accuracy_pct'] = float(err100)
    results['peak_accuracy_pass'] = err100 < 10
    print(f"\n  Peak accuracy @100mVpk: {err100:.1f}% {'PASS' if err100<10 else 'FAIL'}")

pm_a=np.array(pk_meas); pi_a=np.array(pk_ideal)
vld=~np.isnan(pm_a)
if np.sum(vld) > 0:
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(pi_a[vld]*1000, pm_a[vld]*1000, 'ro-', ms=8, label='Measured')
    ax.plot(pi_a[vld]*1000, pi_a[vld]*1000, 'b--', lw=2, label='Ideal')
    ax.set_xlabel('Input Amplitude (mVpk)'); ax.set_ylabel('Detected Peak (mV above Vcm)')
    ax.set_title('Peak Detector Accuracy (SKY130 transistor-level)')
    ax.legend(); ax.grid(True,alpha=0.3)
    plt.tight_layout(); plt.savefig('plot_peak_accuracy.png', dpi=150)
    print("  Saved plot_peak_accuracy.png\n")

# ================================================================
# TEST 5: Crest Factor
# ================================================================
print("="*60)
print("TEST 5: Crest Factor (known waveforms)")
print("="*60)

cf_tests = [
    ('Sine', 'SIN(0.9 0.1 1k)', 1.414),
    ('Square', 'PULSE(0.8 1.0 0 1u 1u 0.5m 1m)', 1.0),
    ('Triangle', 'PULSE(0.8 1.0 0 0.5m 0.5m 1n 1m)', 1.732),
]

cf_results = []
for name, src, cf_id in cf_tests:
    fname = f'tb_cf_{name.lower()}.spice'
    with open(fname,'w') as f:
        f.write(f"""* Crest Factor - {name}
{HEADER}
Vreset reset gnd PULSE(1.8 0 2m 1n 1n 10k 20k)
Vin inp gnd {src}
Xdut inp rms_out peak_out vdd vss reset vbn vcm rms_crest_top
.options reltol=1e-3
.tran 10u 200m
.control
run
wrdata tb_cf_{name.lower()}.csv v(rms_out) v(peak_out) v(vcm) v(inp)
quit
.endc
.end
""")
    if run_ngspice(fname):
        d = np.loadtxt(f'tb_cf_{name.lower()}.csv')
        t = d[:,0]; vr=d[:,1]; vp=d[:,3]; vc=d[:,5]; vi=d[:,7]
        mask = t > 0.15
        vcm = np.mean(vc[mask])
        mav_meas = np.mean(vr[mask]) - vcm
        pk_meas = np.max(vp[mask]) - vcm

        if 'rms_linearity_slope' in results:
            gain = results['rms_linearity_slope']
            mav_cal = mav_meas / gain
        else:
            mav_cal = mav_meas / 1.8

        rms_cal = mav_cal * np.pi / (2*np.sqrt(2))
        cf_meas = pk_meas / rms_cal if rms_cal > 1e-6 else float('inf')
        cf_err = abs(cf_meas - cf_id)/cf_id * 100

        vi_ac = vi[mask] - vcm
        true_rms = np.sqrt(np.mean(vi_ac**2))
        true_pk = np.max(np.abs(vi_ac))
        true_cf = true_pk / true_rms if true_rms > 1e-6 else 0

        cf_results.append({'name':name, 'cf_id':cf_id, 'cf_meas':float(cf_meas),
                          'cf_err':float(cf_err), 'mav':float(mav_meas*1000),
                          'peak':float(pk_meas*1000), 'true_cf':float(true_cf)})
        status = 'PASS' if cf_err < 15 else 'FAIL'
        print(f"  {name:10s}: CF={cf_meas:.3f} (ideal={cf_id:.3f}, err={cf_err:.1f}%) [{status}]")
    else:
        cf_results.append({'name':name, 'cf_id':cf_id, 'cf_meas':float('nan'), 'cf_err':999})

if len(cf_results) > 0 and not np.isnan(cf_results[0].get('cf_meas', np.nan)):
    results['cf_sine_err'] = cf_results[0]['cf_err']
    results['cf_sine_pass'] = cf_results[0]['cf_err'] < 15
results['crest_factor'] = cf_results

fig, ax = plt.subplots(figsize=(10,6))
names_v = [r['name'] for r in cf_results if not np.isnan(r.get('cf_meas',np.nan))]
cf_i = [r['cf_id'] for r in cf_results if not np.isnan(r.get('cf_meas',np.nan))]
cf_m = [r['cf_meas'] for r in cf_results if not np.isnan(r.get('cf_meas',np.nan))]
if len(names_v) > 0:
    x = np.arange(len(names_v)); w=0.35
    ax.bar(x-w/2, cf_i, w, label='Ideal', color='steelblue', alpha=0.8)
    ax.bar(x+w/2, cf_m, w, label='Measured', color='coral', alpha=0.8)
    ax.set_xticks(x); ax.set_xticklabels(names_v)
    ax.set_ylabel('Crest Factor'); ax.set_title('Crest Factor (SKY130 transistor-level)')
    ax.legend(); ax.grid(True,alpha=0.3,axis='y')
    for i in range(len(names_v)):
        err = abs(cf_m[i]-cf_i[i])/cf_i[i]*100
        ax.annotate(f'{err:.1f}%', xy=(i+w/2,cf_m[i]), xytext=(0,5),
                   textcoords='offset points', ha='center', fontsize=9)
plt.tight_layout(); plt.savefig('plot_crest_factor.png', dpi=150)
print("  Saved plot_crest_factor.png\n")

# ================================================================
# TEST 6: Power
# ================================================================
print("="*60)
print("TEST 6: Power")
print("="*60)

with open('tb_power.spice','w') as f:
    f.write(f"""* Power
{HEADER}
Vreset reset gnd 0
Vin inp gnd SIN(0.9 0.1 1k)
Xdut inp rms_out peak_out vdd vss reset vbn vcm rms_crest_top
.options reltol=1e-3
.tran 10u 20m
.control
run
wrdata tb_power.csv i(VDD)
quit
.endc
.end
""")
if run_ngspice('tb_power.spice'):
    d = np.loadtxt('tb_power.csv')
    t,idd = d[:,0],d[:,1]
    mask = t > 0.01
    avg_idd = np.mean(abs(idd[mask]))
    pwr = avg_idd * 1.8e6
    results['power_uw'] = float(pwr)
    results['power_idd_uA'] = float(avg_idd*1e6)
    results['power_pass'] = pwr < 25
    print(f"  IDD = {avg_idd*1e6:.2f} uA, Power = {pwr:.1f} uW {'PASS' if pwr<25 else 'FAIL'}")

# ================================================================
# TEST 7: Waveform Plot
# ================================================================
print("="*60)
print("TEST 7: Waveform Detail")
print("="*60)

with open('tb_basic.spice','w') as f:
    f.write(f"""* Waveform detail
{HEADER}
Vreset reset gnd PULSE(1.8 0 2m 1n 1n 10k 20k)
Vin inp gnd SIN(0.9 0.1 1k)
Xdut inp rms_out peak_out vdd vss reset vbn vcm rms_crest_top
.options reltol=1e-3
.tran 5u 100m
.control
run
wrdata tb_basic_out.csv v(inp) v(rms_out) v(peak_out) v(vcm)
quit
.endc
.end
""")
if run_ngspice('tb_basic.spice'):
    d = np.loadtxt('tb_basic_out.csv')
    t=d[:,0]; vi=d[:,1]; vr=d[:,3]; vp=d[:,5]; vc=d[:,7]
    vcm_v = np.mean(vc[t>0.05])
    fig, axes = plt.subplots(3,1, figsize=(14,10), sharex=True)
    t_ms = t*1000
    axes[0].plot(t_ms, (vi-vcm_v)*1000, 'b-', lw=0.5)
    axes[0].set_ylabel('Vin-Vcm (mV)')
    axes[0].set_title('Block 05: SKY130 Transistor-Level (100mVpk 1kHz)')
    axes[0].grid(True,alpha=0.3)
    axes[1].plot(t_ms, (vcm_v-vr)*1000, 'r-', lw=1)
    axes[1].set_ylabel('Vcm-Vrms (mV)\n(rectified MAV)')
    axes[1].grid(True,alpha=0.3); axes[1].axhline(0, color='gray', ls='--', alpha=0.3)
    axes[2].plot(t_ms, (vp-vcm_v)*1000, 'm-', lw=1.5)
    axes[2].set_ylabel('Vpeak-Vcm (mV)')
    axes[2].set_xlabel('Time (ms)'); axes[2].grid(True,alpha=0.3)
    plt.tight_layout(); plt.savefig('plot_basic_test.png', dpi=150)
    print("  Saved plot_basic_test.png\n")

# ================================================================
# SUMMARY
# ================================================================
print("\n" + "="*60)
print("SUMMARY: Block 05 Transistor-Level (SKY130)")
print("="*60)

summary = [
    ("RMS accuracy (calibrated, <5%)",
     f"{results.get('rms_accuracy_pct','?'):.1f}%" if 'rms_accuracy_pct' in results else '?',
     results.get('rms_accuracy_pass', False)),
    ("RMS linearity (R2>0.99)",
     f"{results.get('rms_linearity_r2','?'):.5f}" if 'rms_linearity_r2' in results else '?',
     results.get('rms_linearity_pass', False)),
    ("RMS bandwidth (10Hz-10kHz)",
     f"{results.get('rms_bw_low','?')}Hz-{results.get('rms_bw_high','?')}Hz",
     results.get('rms_bw_pass', False)),
    ("Peak accuracy (<10% @100mVpk)",
     f"{results.get('peak_accuracy_pct','?'):.1f}%" if 'peak_accuracy_pct' in results else '?',
     results.get('peak_accuracy_pass', False)),
    ("Peak hold (<10% @500ms)",
     f"{results.get('peak_hold_decay_500ms','?'):.1f}%" if 'peak_hold_decay_500ms' in results else '?',
     results.get('peak_hold_pass', False)),
    ("Crest factor sine (<15%)",
     f"{results.get('cf_sine_err','?'):.1f}%" if 'cf_sine_err' in results else '?',
     results.get('cf_sine_pass', False)),
    ("Power (<25uW)",
     f"{results.get('power_uw','?'):.1f}uW" if 'power_uw' in results else '?',
     results.get('power_pass', False)),
]

all_pass = True
for spec, value, passed in summary:
    s = "PASS" if passed else "FAIL"
    if not passed: all_pass = False
    print(f"  [{s}] {spec}: {value}")

print()
print("  >>> ALL SPECS PASS <<<" if all_pass else "  >>> SOME SPECS FAIL — see above <<<")

with open('results_summary.txt','w') as f:
    for spec, value, passed in summary:
        f.write(f"[{'PASS' if passed else 'FAIL'}] {spec}: {value}\n")
    f.write(f"\nCrest Factor Details:\n")
    for r in cf_results:
        cm = r.get('cf_meas', np.nan)
        if not np.isnan(cm):
            f.write(f"  {r['name']}: CF={cm:.3f} (ideal={r['cf_id']:.3f}, err={r['cf_err']:.1f}%)\n")
        else:
            f.write(f"  {r['name']}: FAILED\n")

with open('results_full.json','w') as fj:
    def ser(o):
        if isinstance(o, (np.floating, np.float64)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        if isinstance(o, float) and (np.isnan(o) or np.isinf(o)): return str(o)
        return str(o)
    json.dump(results, fj, indent=2, default=ser)

print(f"\nDone. Results saved.")
