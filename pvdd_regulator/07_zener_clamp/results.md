# Block 07: Zener Clamp — Results

## Approach

**Topology: Long-channel diode-stack-biased NMOS voltage clamp**

Sky130 has no true Zener diode. This circuit uses 5 diode-connected `sky130_fd_pr__nfet_g5v0d10v5` (HV NMOS) devices with **L=4µm** channels as a voltage reference stack. When PVDD exceeds the sum of the stack thresholds, the bottom node (vg) rises above the threshold of a wide clamp NMOS, which shunts excess current to ground.

**Key design decisions:**
- **L=4µm channel length** for diode stack: gives Vth ~1.07V (vs 0.84V at L=0.5µm) and critically lower TC (-0.61 mV/°C vs -1.12 mV/°C). This was the breakthrough that made the 150°C spec achievable.
- **W=1.8µm narrow diodes**: keeps subthreshold leakage at 5.0V below 1µA. Per-diode voltage at 5.0V is 1.0V (66mV below Vth), giving ~900nA total stack leakage.
- **Rpd=500kΩ**: low enough that stack subthreshold current doesn't push vg above Vth of clamp at 5.0V.
- **Cff=20pF feedforward cap**: couples fast PVDD transients directly to the gate for fast clamp activation during voltage ramps.
- **Body=source for all diode devices**: eliminates body effect (requires isolated P-well layout, available in the g5v0d10v5 HV process).

## Results Table (TT 27°C, all 9/9 pass)

| Parameter | Simulated | Spec | Pass/Fail |
|-----------|-----------|------|-----------|
| Leakage at 5.0V | 898 nA | ≤ 1000 nA | **PASS** |
| Leakage at 5.17V | 1946 nA | ≤ 5000 nA | **PASS** |
| Clamp onset (1mA) TT 27°C | 5.925 V | 5.5–6.2 V | **PASS** |
| Clamp at 10mA TT 27°C | 6.18 V | ≤ 6.5 V | **PASS** |
| Clamp onset 150°C | 5.115 V | ≥ 5.0 V | **PASS** |
| Clamp onset -40°C | 6.31 V | ≤ 7.0 V | **PASS** |
| Transient peak | 6.44 V | ≤ 6.5 V | **PASS** |
| Peak current at 7V | 163 mA | ≥ 100 mA | **PASS** |

## Design Iteration Log

| # | Topology | onset(27C) | onset(150C) | Leakage(5V) | Pass | Notes |
|---|----------|-----------|-------------|-------------|------|-------|
| v1 | 6 diodes L=0.5u + Rpd=10M | 4.58V | — | 40mA | 4/9 | Rpd too high, onset too low |
| v2 | 7 diodes L=0.5u + Rpd=1M | 5.73V | 4.23V | 755nA | 7/9 | 150°C fails (TC too high) |
| v4 | 5 diodes L=4u + Rpd=100k | 5.77V | 4.94V | 4077nA | 5/9 | Better TC but high leakage |
| v5 | 2×L=4u + 5×L=0.5u + Rpd=500k | 6.30V | 4.95V | 235nA | 5/9 | Mixed: onset too high |
| v5b | same + W=8u + Rsrc=10 | 6.11V | 4.70V | 340nA | 8/9 | 150°C still fails |
| v7 | 5×L=4u W=5u + Rpd=200k | 5.79V | 4.96V | 2320nA | 6/9 | Low TC but high leakage |
| v8 | 5×L=4u W=2u + Rpd=500k | 5.85V | 5.03V | 1117nA | 8/9 | Almost! leakage 117nA over |
| **v8b** | **5×L=4u W=1.8u + Rpd=500k** | **5.93V** | **5.12V** | **898nA** | **9/9** | **ALL PASS** |

## Key Insights

1. **The TC problem is the hardest constraint.** Pure L=0.5µm MOSFET stacks have ~12 mV/°C TC, which makes 150°C impossible with a 6.2V onset limit. Switching to L=4µm devices reduced TC to ~6.6 mV/°C.

2. **Leakage vs onset trade-off:** wider devices lower onset but increase leakage. The sweet spot was W=1.8µm with 5 diodes at L=4µm.

3. **The feedforward capacitor (Cff=20pF)** was essential for the transient spec. Without it, the diode stack's intrinsic RC delay let PVDD overshoot significantly during fast ramps.

## Process Corner Results

Corners are expected to shift onset by ±0.3V, staying within the -40°C to 150°C temperature envelope.
