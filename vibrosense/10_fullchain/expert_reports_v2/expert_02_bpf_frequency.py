#!/usr/bin/env python3
"""Expert 2: BPF Frequency Response Analysis"""

import os
import json
import numpy as np

REPORT = os.path.join(os.path.dirname(__file__), 'expert_02_bpf_frequency.md')
VIBROSENSE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    lines = []
    L = lines.append

    L("# Expert Report 02: BPF Frequency Response Analysis")
    L("")
    L("## 1. BPF Architecture")
    L("")
    L("Each BPF channel uses a Tow-Thomas biquad topology with 3 OTAs per path")
    L("(pseudo-differential = 6 OTAs per channel, 30 total for 5 channels).")
    L("")
    L("Topology per half-circuit:")
    L("- OTA1: gm-integrator (vinp -> C1 through int2p)")
    L("- OTA2: gm-integrator (int1p -> C2 through vcm)")
    L("- OTA3: positive feedback (vcm -> int1p, sets Q)")
    L("- Pseudo-resistors for DC bias")
    L("")
    L("Transfer function: H(s) = (gm1/C1) * s / [s^2 + (gm3/C1)*s + gm1*gm2/(C1*C2)]")
    L("- Center freq: f0 = (1/2pi) * sqrt(gm1*gm2/(C1*C2))")
    L("- Q = sqrt(gm1*gm2*C1*C2) / (gm3*C1) = sqrt(C2/C1) when all gm equal")
    L("- Passband gain: gm1/gm3 = 1 (unity) when OTAs are identical")
    L("")

    L("## 2. OTA Characteristics")
    L("")
    L("The BPF uses `ota_foldcasc` with these bias conditions:")
    L("- VBN = 0.5973V, VBCN = 0.8273V, VBP = 0.81V, VBCP = 0.555V")
    L("- Tail current: ~500 nA (from bias generator design)")
    L("- Input pair: W=5u L=14u NMOS")
    L("- gm estimated: ~6-10 uS at 250nA per side (conservative)")
    L("")
    L("**CRITICAL**: All 5 BPF channels share the SAME bias voltages in the full-chain netlist.")
    L("However, BPF ch4 and ch5 were tuned with DIFFERENT bias voltages:")
    L("- Ch4: VBN=0.6399, VBP=0.745, VBCN=0.8699, VBCP=0.49 (Iref=440nA)")
    L("- Ch5: VBN=0.6914, VBP=0.66, VBCN=0.9214, VBCP=0.405 (Iref=870nA)")
    L("")
    L("**This is a significant error**: Ch4 and Ch5 require higher OTA gm (via higher")
    L("bias current) to reach their target frequencies. Using the Ch1 bias (200nA)")
    L("will make Ch4 and Ch5 center frequencies too LOW.")
    L("")

    L("## 3. Channel Specifications vs Actual")
    L("")

    channels = [
        {"ch": 1, "f0_target": 224, "Q_target": 0.75, "C1": 586.0, "C2": 1042.0,
         "f0_tuned": 226.6, "Q_tuned": 0.79, "Iref": 200},
        {"ch": 2, "f0_target": 1000, "Q_target": 0.67, "C1": 118.0, "C2": 260.0,
         "f0_tuned": 1001.4, "Q_tuned": 0.707, "Iref": 200},
        {"ch": 3, "f0_target": 3162, "Q_target": 1.05, "C1": 58.0, "C2": 53.0,
         "f0_tuned": 3162.0, "Q_tuned": 1.108, "Iref": 200},
        {"ch": 4, "f0_target": 7071, "Q_target": 1.41, "C1": 59.0, "C2": 29.7,
         "f0_tuned": 7235.8, "Q_tuned": 1.42, "Iref": 440},
        {"ch": 5, "f0_target": 14142, "Q_target": 1.41, "C1": 41.8, "C2": 21.0,
         "f0_tuned": 14639.4, "Q_tuned": 1.408, "Iref": 870},
    ]

    L("| Ch | f0 target | f0 tuned | Q   | C1 (pF) | C2 (pF) | Iref (nA) | Bias match? |")
    L("|----|-----------|----------|-----|---------|---------|-----------|-------------|")
    for c in channels:
        match = "YES" if c["Iref"] == 200 else "**NO**"
        L(f"| {c['ch']}  | {c['f0_target']} Hz | {c['f0_tuned']} Hz | {c['Q_tuned']} | {c['C1']} | {c['C2']} | {c['Iref']} | {match} |")
    L("")

    L("## 4. Impact of Wrong Bias on Ch4 and Ch5")
    L("")
    L("When Ch4 is biased at 200nA instead of 440nA:")
    L("- gm drops by factor of sqrt(440/200) = 1.48x (subthreshold)")
    L("- f0 proportional to gm -> f0 drops from 7236 Hz to ~4900 Hz")
    L("- This is now overlapping with Ch3 (3162 Hz) territory")
    L("")
    L("When Ch5 is biased at 200nA instead of 870nA:")
    L("- gm drops by factor of sqrt(870/200) = 2.09x")
    L("- f0 drops from 14639 Hz to ~7000 Hz")
    L("- This now overlaps with Ch4's intended band")
    L("")
    L("**Result**: Channels 3, 4, and 5 may all be sensing similar frequency ranges,")
    L("destroying the spectral decomposition that the classifier relies on.")
    L("")

    L("## 5. Do the BPF Center Frequencies Match Bearing Fault Frequencies?")
    L("")
    L("Bearing fault characteristic frequencies (6205 bearing at 1797 RPM):")
    L("- FTF (cage): ~12 Hz")
    L("- BSF (ball): ~70.6 Hz")
    L("- BPFO (outer race): ~107.4 Hz")
    L("- BPFI (inner race): ~162.2 Hz")
    L("")
    L("These are FUNDAMENTAL fault frequencies. In real bearings, faults excite")
    L("**structural resonances** at much higher frequencies (1-10 kHz), modulated")
    L("at the fault frequency. The BPF should capture these resonances, not the")
    L("fundamental fault frequencies directly.")
    L("")
    L("Training config band definitions:")
    L("- Band 1: 100-500 Hz (structural, low-freq)")
    L("- Band 2: 500-1500 Hz (mid-freq bearing tones)")
    L("- Band 3: 1500-3000 Hz (high-freq defect harmonics)")
    L("- Band 4: 3000-4500 Hz (very high-freq early fault)")
    L("- Band 5: 4500-5900 Hz (near-Nyquist)")
    L("")
    L("BPF center frequencies vs band centers:")
    L("")
    L("| Band | Config range | Config center | BPF f0 (tuned) | Match? |")
    L("|------|-------------|--------------|----------------|--------|")
    L("| 1    | 100-500 Hz  | 224 Hz       | 226.6 Hz       | Good   |")
    L("| 2    | 500-1500 Hz | 866 Hz       | 1001 Hz        | Fair   |")
    L("| 3    | 1500-3000 Hz| 2121 Hz      | 3162 Hz        | High   |")
    L("| 4    | 3000-4500 Hz| 3674 Hz      | 7236 Hz        | **Way too high** |")
    L("| 5    | 4500-5900 Hz| 5153 Hz      | 14639 Hz       | **Way too high** |")
    L("")
    L("**CRITICAL FINDING**: BPF channels 4 and 5 are centered WAY above the")
    L("training config bands. Ch4 should be ~3674 Hz but is 7236 Hz.")
    L("Ch5 should be ~5153 Hz but is 14639 Hz. This means:")
    L("1. The analog filters don't match what the classifier was trained on")
    L("2. With wrong bias, they shift even further down, but still wrong")
    L("3. The spectral features are scrambled vs training expectations")
    L("")

    L("## 6. BPF Bandwidth and Q Analysis")
    L("")
    L("For the Tow-Thomas biquad, BW = f0/Q:")
    L("")
    L("| Ch | f0 (Hz) | Q    | BW (Hz) | -3dB range (Hz) |")
    L("|----|---------|------|---------|-----------------|")
    for c in channels:
        bw = c['f0_tuned'] / c['Q_tuned']
        f_lo = c['f0_tuned'] - bw/2
        f_hi = c['f0_tuned'] + bw/2
        L(f"| {c['ch']}  | {c['f0_tuned']:.0f} | {c['Q_tuned']:.2f} | {bw:.0f} | {f_lo:.0f} - {f_hi:.0f} |")
    L("")
    L("The bandwidths are quite wide (low Q). This means significant overlap")
    L("between channels, reducing discrimination ability.")
    L("")

    L("## 7. Conclusions and Recommendations")
    L("")
    L("### Major Issues Found")
    L("")
    L("1. **Bias voltage mismatch**: Ch4 and Ch5 need different bias voltages than Ch1-3.")
    L("   The full-chain uses only one set of bias voltages, detuning Ch4/Ch5.")
    L("")
    L("2. **Center frequency mismatch**: Even with correct bias, Ch4 (7236 Hz) and")
    L("   Ch5 (14639 Hz) don't match the training config bands (3000-4500 Hz and")
    L("   4500-5900 Hz respectively). The BPF was designed with logarithmically-spaced")
    L("   centers (224, 1000, 3162, 7071, 14142) but training uses linear-ish bands.")
    L("")
    L("3. **The envelope detector only sees differences in BPF outputs**. If the BPFs")
    L("   don't correctly decompose the spectrum, the envelope features are meaningless.")
    L("")
    L("### Recommendations")
    L("")
    L("1. **Retune BPF channels 4 and 5** to match training config: f0=3674 Hz and f0=5153 Hz")
    L("2. **Add per-channel bias** or redesign to work with single bias at correct current")
    L("3. **Alternatively, retrain classifier** with the actual BPF center frequencies")
    L("4. **Priority: HIGH** -- This is likely a major contributor to classification failure")

    with open(REPORT, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Expert 02 report written to {REPORT}")

if __name__ == '__main__':
    main()
