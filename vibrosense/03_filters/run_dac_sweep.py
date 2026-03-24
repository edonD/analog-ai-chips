#!/usr/bin/env python3
"""Sweep bias_dac_real codes 1-15, measure Iout, compute DNL."""

import subprocess, os, re, json

WORKDIR = "/home/ubuntu/analog-ai-chips/vibrosense/03_filters"

def run_code(code):
    """Run one OP at the given DAC code, return Iout in amps."""
    b3 = 1.8 if code >= 8 else 0.0
    b2 = 1.8 if (code % 8) >= 4 else 0.0
    b1 = 1.8 if (code % 4) >= 2 else 0.0
    b0 = 1.8 if (code % 2) == 1 else 0.0

    spice = f"""* DAC sweep — code {code}
.lib "../01_ota/sky130_minimal.lib.spice" tt
.include "bias_dac_real.spice"

Vdd vdd 0 dc 1.8
Iref vdd iref_node 25n
Vout iout_node 0 dc 0.9
Xdac iref_node iout_node vdd 0 b0 b1 b2 b3 bias_dac_real

Vb0 b0 0 dc {b0}
Vb1 b1 0 dc {b1}
Vb2 b2 0 dc {b2}
Vb3 b3 0 dc {b3}

.control
op
let iout = -i(vout)
let iout_na = iout * 1e9
echo "IOUT_NA=$&iout_na"
.endc
.end
"""
    fname = os.path.join(WORKDIR, f"_dac_code_{code}.spice")
    with open(fname, "w") as f:
        f.write(spice)

    result = subprocess.run(
        ["ngspice", "-b", fname],
        capture_output=True, text=True, cwd=WORKDIR, timeout=60
    )
    os.unlink(fname)

    for line in (result.stdout + result.stderr).splitlines():
        m = re.search(r"IOUT_NA=([-\d.eE+]+)", line)
        if m:
            return float(m.group(1)) * 1e-9  # convert nA back to A
    print(f"WARNING: could not parse code {code}")
    print(result.stdout[-500:])
    return None

# Sweep
results = {}
print("Code  Iout(nA)     Expected(nA)  Error(%)")
print("-" * 50)
for code in range(1, 16):
    iout = run_code(code)
    if iout is None:
        continue
    expected = code * 25e-9
    err_pct = 100 * (iout - expected) / expected
    results[code] = iout
    print(f"  {code:2d}   {iout*1e9:10.3f}    {expected*1e9:8.1f}     {err_pct:+6.2f}%")

# DNL analysis
print("\n=== DNL Analysis ===")
codes = sorted(results.keys())
lsb = results[codes[0]]  # code 1 current = 1 LSB
print(f"LSB (code 1): {lsb*1e9:.3f} nA")

max_dnl = 0
dnl_list = []
for i in range(1, len(codes)):
    step = results[codes[i]] - results[codes[i-1]]
    dnl = (step / lsb) - 1.0
    dnl_list.append(dnl)
    if abs(dnl) > max_dnl:
        max_dnl = abs(dnl)
    print(f"  Code {codes[i]:2d}: step={step*1e9:.3f}nA  DNL={dnl:+.4f} LSB")

print(f"\nMax |DNL| = {max_dnl:.4f} LSB")
if max_dnl < 0.5:
    print("PASS: DNL < 0.5 LSB")
else:
    print(f"FAIL: DNL = {max_dnl:.4f} >= 0.5 LSB")

# INL analysis
print("\n=== INL Analysis ===")
max_inl = 0
for code in codes:
    ideal = code * lsb
    inl = (results[code] - ideal) / lsb
    if abs(inl) > max_inl:
        max_inl = abs(inl)
    print(f"  Code {code:2d}: INL={inl:+.4f} LSB")
print(f"Max |INL| = {max_inl:.4f} LSB")

# Save results
summary = {
    "iunit_nA": lsb * 1e9,
    "max_dnl_lsb": max_dnl,
    "max_inl_lsb": max_inl,
    "pass_dnl": max_dnl < 0.5,
    "codes": {str(c): results[c] * 1e9 for c in codes}
}
with open(os.path.join(WORKDIR, "blocker7_dac.json"), "w") as f:
    json.dump(summary, f, indent=2)
print(f"\nResults saved to blocker7_dac.json")
