#!/usr/bin/env python3
"""
Template-based parameter optimization for startup circuit design.cir
"""
import subprocess, re, os, sys, json, random, time
from pathlib import Path

WORKDIR = Path(__file__).parent.resolve()
os.chdir(WORKDIR)
TEMPLATE = (WORKDIR / 'design.cir.bak').read_text()

FAST_TESTS = ['tb_su_basic.spice', 'tb_su_fast_ramp.spice',
              'tb_su_50mA.spice', 'tb_su_ff_m40.spice']
EXTRA_TESTS = ['tb_su_slow_ramp.spice', 'tb_su_ss150.spice',
               'tb_su_cold_crank.spice']

BASELINE = dict(mn_cg_l=4, mn_cg_w=0.42, n_diodes=5, r_delay_l=10000,
                c_delay_pf=120, sf_w=20, r_load_l=50, r_lb1_l=1000,
                r_lb2_l=6000, diode_w=1.0)


def _diodes(nd, dw):
    if dw == int(dw): ws = f'{int(dw)}e-6'
    else: ws = f'{dw}e-6'
    d = f'sky130_fd_pr__nfet_g5v0d10v5 w={ws} l=1e-6'
    if nd == 1: return f'XMD1 ls_bias ls_bias gnd gnd {d}'
    L = [f'XMD1 ls_bias ls_bias d1 gnd {d}']
    for i in range(2, nd):
        L.append(f'XMD{i} d{i-1} d{i-1} d{i} gnd {d}')
    L.append(f'XMD{nd} d{nd-1} d{nd-1} gnd gnd {d}')
    return '\n'.join(L)


def gen(p):
    c = TEMPLATE
    c = c.replace('w=20e-6 l=1e-6\nXMN_sf2 bvdd inv_det gate gnd sky130_fd_pr__nfet_g5v0d10v5 w=20e-6',
                   f"w={p['sf_w']}e-6 l=1e-6\nXMN_sf2 bvdd inv_det gate gnd sky130_fd_pr__nfet_g5v0d10v5 w={p['sf_w']}e-6")
    c = c.replace(f'w=2 l=1000\nXR_lb2 ls_bias gnd gnd sky130_fd_pr__res_xhigh_po w=2 l=6000',
                   f"w=2 l={int(p['r_lb1_l'])}\nXR_lb2 ls_bias gnd gnd sky130_fd_pr__res_xhigh_po w=2 l={int(p['r_lb2_l'])}")
    old_d = """XMD1 ls_bias ls_bias d1 gnd sky130_fd_pr__nfet_g5v0d10v5 w=1e-6 l=1e-6
XMD2 d1 d1 d2 gnd sky130_fd_pr__nfet_g5v0d10v5 w=1e-6 l=1e-6
XMD3 d2 d2 d3 gnd sky130_fd_pr__nfet_g5v0d10v5 w=1e-6 l=1e-6
XMD4 d3 d3 d4 gnd sky130_fd_pr__nfet_g5v0d10v5 w=1e-6 l=1e-6
XMD5 d4 d4 gnd gnd sky130_fd_pr__nfet_g5v0d10v5 w=1e-6 l=1e-6"""
    c = c.replace(old_d, _diodes(int(p['n_diodes']), p['diode_w']))
    c = c.replace('w=0.42e-6 l=4e-6', f"w={p['mn_cg_w']}e-6 l={p['mn_cg_l']}e-6")
    c = c.replace('sky130_fd_pr__res_xhigh_po w=1 l=50\n',
                   f"sky130_fd_pr__res_xhigh_po w=1 l={int(p['r_load_l'])}\n")
    c = c.replace('sky130_fd_pr__res_xhigh_po w=1 l=10000\n',
                   f"sky130_fd_pr__res_xhigh_po w=1 l={int(p['r_delay_l'])}\n")
    c = c.replace('C_delay ea_en gnd 120p', f"C_delay ea_en gnd {p['c_delay_pf']:.0f}p")
    return c


def run1(tb):
    try:
        r = subprocess.run(['ngspice', '-b', tb], capture_output=True,
                           text=True, timeout=120, cwd=str(WORKDIR))
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return {}
    except Exception:
        return {}
    m = {}
    for line in out.split('\n'):
        line = line.strip()
        match = re.match(r'^(\w+):\s+([-\d.eE+]+)', line)
        if match:
            try: m[match.group(1)] = float(match.group(2))
            except ValueError: pass
    return m


def ev(p, tests=None):
    if tests is None: tests = FAST_TESTS
    (WORKDIR / 'design.cir').write_text(gen(p))
    am = {}
    for tb in tests:
        m = run1(tb)
        k = tb.replace('tb_su_', '').replace('.spice', '')
        for mk, mv in m.items(): am[f"{k}.{mk}"] = mv

    s, mo, d = 0, 0, {}
    for name, os_key, pf_key, check_os in [
        ('basic', 'basic.pvdd_overshoot_mV', 'basic.pvdd_final_V', True),
        ('fast_ramp', 'fast_ramp.pvdd_overshoot_mV', 'fast_ramp.pvdd_final_V', True),
        ('50mA', None, '50mA.pvdd_final_V', False),
        ('ff_m40', 'ff_m40.pvdd_overshoot_mV', 'ff_m40.pvdd_final_V', True),
        ('slow_ramp', 'slow_ramp.pvdd_overshoot_mV', 'slow_ramp.pvdd_final_V', False),
        ('ss150', None, 'ss150.pvdd_final_V', False),
        ('cold_crank', None, 'cold_crank.pvdd_post_recovery_V', False),
    ]:
        pf = am.get(pf_key)
        if pf is None: continue
        os_v = am.get(os_key, 0) if os_key else 0
        ok = 4.9 < pf < 5.2
        if check_os and os_v >= 200: ok = False
        if ok: s += 1
        if os_v < 9000: mo = max(mo, os_v)
        d[name] = f"{'os='+str(int(os_v))+' ' if os_key else ''}pf={pf:.3f} {'P' if ok else 'F'}"

    return {'score': s, 'max_os': mo, 'details': d, 'metrics': am, 'params': dict(p)}


def main():
    random.seed(42)
    t0 = time.time()
    best = None
    n = 0

    def try_it(p, label, tests=None):
        nonlocal best, n
        n += 1
        r = ev(p, tests)
        nb = ""
        if best is None or r['score'] > best['score'] or \
           (r['score'] == best['score'] and r['max_os'] < best['max_os']):
            best = r; nb = " ***BEST***"
        nt = 4 if tests is None else len(tests)
        print(f"[{n:3d}] {label:35s} {r['score']}/{nt} os={r['max_os']:.0f} "
              f"{time.time()-t0:.0f}s{nb}", flush=True)
        for k, v in r['details'].items():
            print(f"      {k}: {v}", flush=True)
        return r

    try_it(BASELINE, "baseline")

    # Phase 1: single sweeps
    print("\n--- Phase 1: Single sweeps ---", flush=True)
    for l in [6, 8, 10, 12, 15, 20]:
        try_it({**BASELINE, 'mn_cg_l': l}, f"cg_l={l}")
    for nd in [3, 4, 6]:
        try_it({**BASELINE, 'n_diodes': nd}, f"nd={nd}")
    for rl in [3000, 5000, 7000, 8000]:
        try_it({**BASELINE, 'r_delay_l': rl}, f"rd={rl}")
    for c in [40, 60, 80]:
        try_it({**BASELINE, 'c_delay_pf': c}, f"cd={c}")
    for sw in [5, 10, 15]:
        try_it({**BASELINE, 'sf_w': sw}, f"sf={sw}")
    for rl in [30, 80, 120]:
        try_it({**BASELINE, 'r_load_l': rl}, f"rl={rl}")

    # Phase 2: combos
    print("\n--- Phase 2: Combos ---", flush=True)
    combos = []
    for cg in [6, 8, 10, 12]:
        for rd in [5000, 7000, 8000]:
            combos.append({**BASELINE, 'mn_cg_l': cg, 'r_delay_l': rd})
    for cg in [8, 10, 12]:
        for nd in [4, 5, 6]:
            combos.append({**BASELINE, 'mn_cg_l': cg, 'n_diodes': nd})
    for cg in [8, 10, 12]:
        for sf in [10, 15]:
            combos.append({**BASELINE, 'mn_cg_l': cg, 'sf_w': sf})
    for cg in [8, 10, 12]:
        for rl in [80, 120]:
            combos.append({**BASELINE, 'mn_cg_l': cg, 'r_load_l': rl})
    random.shuffle(combos)
    for c in combos[:25]:
        try_it(c, f"cg={c['mn_cg_l']} rd={c.get('r_delay_l',10000)} nd={int(c.get('n_diodes',5))}")

    # Phase 3: fine-tune around best
    print("\n--- Phase 3: Fine-tune ---", flush=True)
    bp = best['params']
    for i in range(15):
        p = dict(bp)
        for k in random.sample(['mn_cg_l', 'r_delay_l', 'c_delay_pf', 'n_diodes', 'sf_w', 'r_load_l'], 3):
            if k == 'mn_cg_l': p[k] = max(4, min(20, p[k] + random.choice([-2, -1, 0, 1, 2])))
            elif k == 'r_delay_l': p[k] = max(2000, min(12000, p[k] + random.choice([-2000, -1000, 0, 1000, 2000])))
            elif k == 'c_delay_pf': p[k] = max(20, min(200, p[k] + random.choice([-30, -15, 0, 15, 30])))
            elif k == 'n_diodes': p[k] = max(3, min(6, p[k] + random.choice([-1, 0, 1])))
            elif k == 'sf_w': p[k] = max(5, min(30, p[k] + random.choice([-5, 0, 5])))
            elif k == 'r_load_l': p[k] = max(25, min(200, p[k] + random.choice([-20, 0, 20])))
        try_it(p, f"fine-{i+1}")

    # Phase 4: full eval
    print(f"\n--- Phase 4: Full eval (best={best['score']}/4) ---", flush=True)
    full = try_it(best['params'], "FULL", tests=FAST_TESTS + EXTRA_TESTS)

    (WORKDIR / 'design.cir').write_text(gen(best['params']))
    print(f"\nDONE: {n} iters, {time.time()-t0:.0f}s", flush=True)
    print(f"Best: {best['score']}/4 fast, {full['score']}/7 full, os={best['max_os']:.0f}", flush=True)
    print(f"Params: {best['params']}", flush=True)


if __name__ == '__main__':
    main()
