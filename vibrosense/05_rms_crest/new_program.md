# Block 05 RMS/Crest Factor — Fix Remaining Failures

## Current State

The design (`design.cir`) uses a MOSFET square-law squarer architecture with 17 MOSFETs, 10 resistors, 3 capacitors. The simulation suite (`run_all.py`) runs full PVT sweeps across 5 corners x 3 temperatures.

6 of 10 specs PASS. 4 specs FAIL and need fixing.

## Failing Specs

### 1. RMS Accuracy: 17.8% (target <5%)
- The squarer gain (alpha) calibration is inaccurate at the 100mVpk test point
- Squarer transistors (W=0.42u, L=6u) operate near edge of strong inversion
- Vov ≈ 0.4V, signal is ~25% of Vov — higher-order terms cause systematic error
- Fix approach: increase squarer W/L for deeper strong inversion, OR add a second-order calibration in run_all.py that accounts for nonlinearity, OR bias the squarer transistors with more headroom

### 2. Crest Factor Sine: 15.3% (target <15%)
- Direct consequence of RMS being underestimated (measured CF=1.631 vs ideal 1.414)
- Fixing RMS accuracy will fix this

### 3. Crest Factor Triangle: 21.0% (target <15%)
- Same root cause as sine CF — RMS underestimate inflates CF
- Fixing RMS accuracy will fix this

### 4. PVT All Corners Pass: NO
- SF corner is worst: RMS=25.8%, CF_tri=44.1%
- Vth shift in slow-NMOS process reduces Vov, killing squarer gain
- Fix approach: make squarer less sensitive to Vth variation by:
  - Using larger L (better matching, more predictable Vth)
  - Using larger W (more current, deeper into strong inversion)
  - Adding source degeneration resistors to linearize
  - Or: implement per-corner alpha calibration in the test (the MCU would do this with a known reference signal in real use)

## Passing Specs (DO NOT BREAK)
- RMS linearity R² = 0.997 (target >0.99)
- RMS bandwidth = 10Hz-20kHz (target 10Hz-10kHz)
- Peak accuracy = 5.2% (target <10%)
- Peak hold decay = 3.1% @500ms (target <10%)
- CF square = 8.8% (target <15%)
- Power = 9.2 uW (target <25 uW)

## Files
- `design.cir` — the circuit netlist (modify this to fix the squarer)
- `run_all.py` — simulation suite (may need calibration improvements)
- `sky130.lib.spice` — PDK models (do not modify)
- `sky130_pdk_fixup.spice` — PDK fixup (do not modify)
- `results_summary.txt` — results output
- `results_full.json` — detailed results

## Instructions

1. Read `design.cir` and `run_all.py` fully to understand the current implementation
2. Identify the best fix strategy — prefer circuit-level fixes in `design.cir` over test/calibration hacks
3. Modify `design.cir` to improve squarer accuracy and PVT robustness
4. If needed, update the calibration approach in `run_all.py` (e.g., per-corner alpha, or polynomial calibration)
5. Run `python3 run_all.py` to validate ALL specs pass
6. Iterate until all 10 specs pass, especially:
   - RMS accuracy < 5%
   - CF sine < 15%
   - CF triangle < 15%
   - All 15 PVT corners pass
7. Do NOT regress any currently passing specs (power <25uW, peak hold, peak accuracy, linearity, bandwidth, CF square)

## Key Constraints
- Stay transistor-level — no behavioral models
- SKY130 PDK only
- Keep power under 25 uW
- The MCU does the final CF division digitally — you only need accurate RMS and peak analog outputs
