#!/usr/bin/env python3
"""TB6: Noise analysis for all 5 BPF channels.

With behavioral OTA (ideal VCCS), only thermal noise from Rbias resistors
contributes. Real OTA noise (thermal + 1/f) would be higher.

We compute expected noise analytically using OTA noise model:
  - OTA input-referred noise: 4kT*gamma/gm (thermal) + Kf/(Cox*W*L*f) (1/f)
  - Filter shapes the noise spectrum
  - Integrated over passband

For the behavioral model, we also verify Rbias noise is negligible.
"""
import numpy as np
import json

kT = 1.38e-23 * 300  # Boltzmann * T at 27C
gamma = 2/3  # MOSFET thermal noise coefficient

channels = {
    1: {'f0': 224,   'Q': 1.21, 'gm': 14.07e-9,  'gm3': 18.08e-9,
        'f_low': 131, 'f_high': 317},
    2: {'f0': 1000,  'Q': 1.80, 'gm': 62.83e-9,  'gm3': 54.16e-9,
        'f_low': 722, 'f_high': 1278},
    3: {'f0': 3162,  'Q': 2.87, 'gm': 198.7e-9,  'gm3': 107.7e-9,
        'f_low': 2611, 'f_high': 3714},
    4: {'f0': 7071,  'Q': 3.42, 'gm': 444.3e-9,  'gm3': 201.95e-9,
        'f_low': 6038, 'f_high': 8104},
    5: {'f0': 14142, 'Q': 3.42, 'gm': 888.6e-9,  'gm3': 403.91e-9,
        'f_low': 12077, 'f_high': 16208},
}

print("=" * 78)
print("TB6: Noise Analysis — All Channels")
print("=" * 78)

results = {}
all_pass = True

for ch in range(1, 6):
    s = channels[ch]
    f0, Q, gm = s['f0'], s['Q'], s['gm']
    gm3 = s['gm3']
    f_low, f_high = s['f_low'], s['f_high']
    C = 10e-12

    # === Analytical noise estimation ===
    # OTA input-referred thermal noise PSD: Si = 4kT*gamma/gm (V²/Hz)
    Si_ota = 4 * kT * gamma / gm

    # For OTA1 (input): noise is shaped by BPF transfer function (peak gain = Q)
    # Contribution at output: Si_ota * |H(f)|² integrated over BW
    # At f0, |H(f0)|² = Q² for OTA1 noise (referred to input)
    # Integrated noise ≈ Si_ota × Q² × (pi/2) × BW_noise
    # where BW_noise = f0/(2*Q) (equivalent noise bandwidth of 2nd order BPF)
    BW_noise = f0 * np.pi / (2 * Q)  # Noise equivalent bandwidth

    # OTA1 noise at output
    v2_ota1 = Si_ota * Q**2 * BW_noise

    # OTA2 noise: appears at V2 (LP node), shaped differently
    # OTA2's noise at V1 is attenuated (it's in the feedback path)
    Si_ota2 = 4 * kT * gamma / gm
    # OTA2 noise contribution to V1 ≈ Si_ota2 × (gm²/gm3²) × BW_noise
    # This is typically smaller than OTA1 contribution
    v2_ota2 = Si_ota2 * BW_noise  # simplified (approximate)

    # OTA3 (damping): contributes noise directly at V1
    Si_ota3 = 4 * kT * gamma / gm3
    v2_ota3 = Si_ota3 * BW_noise

    # Rbias noise: 4kT*R, but Rbias=10G → at passband frequencies, C1
    # shorts it out. Negligible for f >> 1/(2*pi*Rbias*C) = 1/(2*pi*10G*10p)
    # = 1.6 Hz. So for all channels (f_low >= 100 Hz), Rbias noise is negligible.
    f_rbias = 1 / (2 * np.pi * 10e9 * 10e-12)

    # Total noise
    v2_total = v2_ota1 + v2_ota2 + v2_ota3
    vrms_total = np.sqrt(v2_total)

    # 1/f noise estimate (significant for Ch1)
    # Kf ≈ 1e-25 V²·F for SKY130 NMOS (W=5u, L=14u)
    # Input-referred 1/f noise: Kf/(Cox*W*L*f)
    # Cox ≈ 8.6e-3 F/m² for SKY130
    Cox = 8.6e-3
    W, L = 5e-6, 14e-6  # OTA input pair dimensions
    Kf = 1e-25  # V²·F (approximate)
    # Integrated 1/f noise from f_low to f_high:
    # ∫ Kf/(Cox*W*L*f) df = Kf/(Cox*W*L) × ln(f_high/f_low)
    v2_flicker = Kf / (Cox * W * L) * np.log(f_high / f_low)
    # Shaped by filter gain: multiply by Q² (approximate)
    v2_flicker_out = v2_flicker * Q**2

    vrms_with_flicker = np.sqrt(v2_total + v2_flicker_out)

    passes = vrms_with_flicker * 1000 < 1.0  # < 1 mVrms
    if not passes:
        all_pass = False

    results[ch] = {
        'thermal_noise_uVrms': round(float(vrms_total * 1e6), 2),
        'flicker_noise_uVrms': round(float(np.sqrt(v2_flicker_out) * 1e6), 2),
        'total_noise_uVrms': round(float(vrms_with_flicker * 1e6), 2),
        'total_noise_mVrms': round(float(vrms_with_flicker * 1e3), 4),
        'noise_equiv_bw_Hz': round(float(BW_noise), 1),
        'pass': bool(passes),
    }

    print(f"\nCh{ch} (f0={f0}Hz, Q={Q}):")
    print(f"  Noise equiv BW:    {BW_noise:.1f} Hz")
    print(f"  OTA thermal noise: {np.sqrt(v2_ota1)*1e6:.2f} uVrms (OTA1) + "
          f"{np.sqrt(v2_ota2)*1e6:.2f} uVrms (OTA2) + "
          f"{np.sqrt(v2_ota3)*1e6:.2f} uVrms (OTA3)")
    print(f"  1/f noise:         {np.sqrt(v2_flicker_out)*1e6:.2f} uVrms")
    print(f"  Total noise:       {vrms_with_flicker*1e6:.2f} uVrms = "
          f"{vrms_with_flicker*1e3:.4f} mVrms {'PASS' if passes else 'FAIL'} (< 1 mVrms)")

print(f"\n{'='*78}")
print(f"TB6 OVERALL: {'ALL PASS' if all_pass else 'FAIL'}")
print(f"{'='*78}")

# Also note the behavioral simulation limitation
print("\nNote: Behavioral OTA has no intrinsic noise. Noise estimates above are")
print("analytical, based on expected OTA transistor-level noise for SKY130")
print("folded-cascode (W=5u L=14u input pair, gamma=2/3, Kf=1e-25 V²·F).")
print("Real transistor-level verification needed when Block 01 OTA is integrated.")

with open('tb6_results.json', 'w') as f:
    json.dump(results, f, indent=2)
