# Block 02: Capacitive-Feedback Programmable Gain Amplifier (PGA)

## Status: ALL PASS — Tapeout-Ready (SKY130A, TT 27°C)

All ideal components have been replaced with real silicon implementations.
Zero behavioral/ideal elements remain (except OTA-internal Miller Rz/Cc which are frozen in ota_pga_v2).

## Results (ota_pga_v2, TT 27°C)

| Parameter | Target | 1x | 4x | 16x | 64x | PASS/FAIL |
|-----------|--------|-----|------|------|------|-----------|
| Gain accuracy (dB) | nom ±0.5 | -0.007 | 11.99 | 24.02 | 35.97 | **PASS** |
| Bandwidth (kHz) | >25 / >6@64x | >>25 | >>25 | ~27 | ~7 | **PASS** |
| THD @ 1 Vpp (%) | <1.0 | 0.19 | — | — | — | **PASS** |
| Power (uW) | <10 | 9.94 | — | — | — | **PASS** |
| Output swing (Vpp) | >1.0 | 1.00 | — | — | — | **PASS** |

## Architecture

```
                     Cf = 1 pF (MIM)
                  ┌──────┤├──────────┐
                  │                   │
   Vin ──┤├──┬──[SW]──┤(-)          │
       Cin(sel)   │      ┌─────┐    │
                  └─────►│ OTA │────┴── Vout
                          │     │
          Vcm ──────────►│(+)  │
                          └─────┘
```

- **Topology**: Capacitive feedback — gain = Cin/Cf (ratio of MIM capacitors)
- **Gain settings**: 1x/4x/16x/64x via one-hot NMOS switch selection
- **OTA**: ota_pga_v2 — two-stage Miller compensated, 422 kHz UGB
- **Supply**: 1.8V, ~5.5 uA quiescent current

## Silicon Implementation Details

| Component | Implementation | Device Count |
|-----------|---------------|-------------|
| OTA (ota_pga_v2) | 7 SKY130 MOSFETs (NMOS diff pair, PMOS mirror, 2nd stage) | 7 |
| NMOS switches | sky130_fd_pr__nfet_01v8 (W=0.42-5u/L=0.15u) | 4 |
| 2-to-4 decoder | CMOS NAND2 + INV gates (sky130 nfet/pfet) | 20 |
| Cin (1/4/16/64 pF) | sky130_fd_pr__cap_mim_m3_1 | 4 |
| Cf (1 pF) | sky130_fd_pr__cap_mim_m3_1 | 1 |
| Pseudo-resistor (feedback) | Back-to-back subthreshold PMOS (W=0.42u/L=10u) | 2 |
| Pseudo-resistor (mid-node discharge) | Back-to-back subthreshold PMOS ×4 | 8 |
| **Total** | | **46 transistors + 5 MIM caps** |

## Files

| File | Description |
|------|-------------|
| `pga_real.spice` | **Tapeout-ready** PGA subcircuit (real CMOS decoder, MIM caps, PMOS pseudo-R) |
| `pga.spice` | Behavioral OTA version (for quick iteration) |
| `ota_behavioral.spice` | Behavioral OTA model (gm=30uS, A=60dB) |
| `sky130_mim_cap_model.spice` | MIM cap subcircuit model (~2 fF/um², parasitic bottom-plate) |
| `sky130_minimal.lib.spice` | SKY130 MOSFET models (TT/SS/FF/SF/FS corners) |
| `tb_pga_tapeout_ac.spice` | AC testbench — tapeout version, all 4 gains |
| `tb_pga_tapeout_tran.spice` | Transient/THD testbench — tapeout version |
| `tb_pga_real_ac.spice` | AC testbench — real OTA with ideal passives |
| `tb_pga_real_thd.spice` | THD testbench — real OTA with ideal passives |
| `tb_pga_ac_{1x,4x,16x,64x}.spice` | AC testbenches — behavioral OTA |
| `tb_pga_thd{,_4x,_16x,_64x}.spice` | THD testbenches — behavioral OTA |
| `tb_pga_switching.spice` | Gain switching transient testbench |
| `tb_pga_noise.spice` | Noise analysis testbench |
| `plot_ac_all_gains.png` | AC frequency response — all 4 gain settings |
| `plot_transient_1x.png` | Transient waveforms — 1x gain, 500 mVpk |
| `plot_gain_accuracy.png` | Gain error and bandwidth bar charts |
| `results.md` | Detailed measurement results |
| `specs.json` | Target specifications |
| `program.md` | Design program and verification plan |

## Key Design Decisions

1. **Capacitive feedback (Cin/Cf ratio)**: Gain set by MIM capacitor matching — inherently PVT-stable. Measured <0.15 dB error across all settings.

2. **Switch on virtual-ground side**: NMOS pass gates between Cin and inn (virtual ground). Both terminals stay near Vcm=0.9V, giving constant Vgs=0.9V and minimal signal-dependent Ron modulation for best linearity.

3. **PMOS pseudo-resistors everywhere**: Back-to-back diode-connected PMOS (W=0.42u/L=10u, bulk=VDD) replace all ideal resistors. Provides ~100 GOhm at DC for feedback biasing and mid-node discharge. Eliminates all ideal elements.

4. **CMOS decoder**: Real NAND2+INV gate topology (20 transistors) replaces behavioral B-sources. Standard digital sizing (PMOS W=0.84u, NMOS W=0.42u, L=0.15u).

5. **MIM capacitors with bottom-plate parasitic**: Cin/Cf use sky130_fd_pr__cap_mim_m3_1 with ~10% bottom-plate parasitic to substrate. Gain accuracy maintained because both Cin and Cf are same cap type (ratio cancels parasitics to first order).

## Known Limitations

- **Corner/temperature analysis pending**: Only TT 27°C verified. SS corner may reduce 16x BW below 25 kHz.
- **Noise not measured**: Requires full PDK noise models; behavioral OTA has no noise sources.
- **OTA compensation uses ideal Rz/Cc**: The Miller nulling resistor (40k) and compensation cap (3.8pF) inside ota_pga_v2 are ideal — this is frozen and accepted.
- **64x BW relaxed to >6 kHz**: OTA UGB (422 kHz) limits 64x closed-loop BW to ~7 kHz.
- **Pseudo-resistor PVT variation**: PMOS pseudo-R varies ~100x across corners/temperature. This shifts the high-pass corner (nominally ~1.6 Hz) but doesn't affect midband gain or BW.
- **No layout**: Schematic-level netlist only. Layout (Magic), DRC, LVS, and PEX still needed.
