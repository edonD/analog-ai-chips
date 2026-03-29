# Block 07: Zener Clamp — Results

## Approach

**Topology: Long-channel diode-stack-biased NMOS voltage clamp**

Sky130 has no true Zener diode. This circuit uses 5 diode-connected `sky130_fd_pr__nfet_g5v0d10v5` (HV NMOS) devices with **L=4µm** channels as a voltage reference stack. When PVDD exceeds the sum of the stack thresholds, the bottom node (vg) rises above the threshold of a wide clamp NMOS, which shunts excess current to ground.

**Key design decisions:**
- **L=4µm channel length** for diode stack: gives Vth ~1.07V (vs 0.84V at L=0.5µm) and critically lower TC (-0.61 mV/°C vs -1.12 mV/°C). This was the breakthrough that made the 150°C spec achievable.
- **W=1.5µm narrow diodes** (v9): keeps subthreshold leakage at 5.0V to 653nA (35% margin). Per-diode voltage at 5.0V is 1.0V (~70mV below Vth).
- **Rpd=500kΩ**: balanced to give good margins at both TT and 150C.
- **Cff=20pF feedforward cap**: couples fast PVDD transients directly to the gate for fast clamp activation during voltage ramps.
- **Body=source for all diode devices**: eliminates body effect (requires isolated P-well layout, available in the g5v0d10v5 HV process).

## Results Table (v9, TT 27C, all 9/9 pass)

| Parameter | Simulated | Spec | Margin | Pass/Fail |
|-----------|-----------|------|--------|-----------|
| Leakage at 5.0V | 653 nA | <= 1000 nA | 35% | **PASS** |
| Leakage at 5.17V | 1161 nA | <= 5000 nA | 77% | **PASS** |
| Clamp onset (1mA) TT 27C | 6.075 V | 5.5-6.2 V | 125mV | **PASS** |
| Clamp at 10mA TT 27C | 6.34 V | <= 6.5 V | 160mV | **PASS** |
| Clamp onset 150C | 5.28 V | >= 5.0 V | 280mV | **PASS** |
| Clamp onset -40C | 6.45 V | <= 7.0 V | 550mV | **PASS** |
| Transient peak | 6.45 V | <= 6.5 V | 50mV | **PASS** |
| Peak current at 7V | 163 mA | >= 100 mA | 63% | **PASS** |

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
| v8b | 5xL=4u W=1.8u + Rpd=500k | 5.93V | 5.12V | 898nA | 9/9 | ALL PASS (thin margins) |
| **v9** | **5xL=4u W=1.5u + Rpd=500k** | **6.08V** | **5.28V** | **653nA** | **9/9** | **ALL PASS (improved margins)** |

## Key Insights

1. **The TC problem is the hardest constraint.** Pure L=0.5µm MOSFET stacks have ~12 mV/°C TC, which makes 150°C impossible with a 6.2V onset limit. Switching to L=4µm devices reduced TC to ~6.6 mV/°C.

2. **Leakage vs onset trade-off:** wider devices lower onset but increase leakage. The sweet spot was W=1.5um with 5 diodes at L=4um (v9).

3. **The feedforward capacitor (Cff=20pF)** was essential for the transient spec. Without it, the diode stack's intrinsic RC delay let PVDD overshoot significantly during fast ramps.

## Process Corner Results (v9)

Full 15-point PVT sweep: **9/15 PASS, 6/15 FAIL.**
The onset spread across corners (1.05V at 27C) exceeds the 700mV spec window.
This is a fundamental limitation of the Vth-based topology. See `readme_v2.md` for
detailed PVT data and recommended mitigations (Rpd trimming).

## Monte Carlo Results (v9)

50-point MC with estimated Avt=12 mV*um (PDK does not publish mismatch data):
- Onset sigma = 13 mV (3-sigma range: 6.036V to 6.115V -- within spec)
- Leakage mean+3sigma = 720 nA (below 1000 nA spec)
- 100% yield at TT 27C
