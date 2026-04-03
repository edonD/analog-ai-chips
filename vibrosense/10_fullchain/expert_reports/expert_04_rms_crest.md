# Expert 04: Block 05 (RMS/Crest Factor) Analysis

## File Status
- `design.cir`: EXISTS (120 lines) — full transistor-level
- `rms.spice`: MISSING — program.md expects this
- `crest.spice`: MISSING — program.md expects this

## Subcircuit Interfaces
```
.subckt ota5 vip vim vout vdd vss vbn
.subckt rms_squarer inp vcm sq_sig sq_ref vdd vss
.subckt lpf_rc inp out vdd vss
.subckt peak_detector inp out vdd vss vbn vcm reset
.subckt rms_crest_top inp rms_out rms_ref peak_out vdd vss reset vbn vcm
```

## Architecture
The design has 4 subcircuits:
1. **ota5** — 5T OTA for peak detector (ports: vip vim vout vdd vss vbn)
2. **rms_squarer** — Single-pair MOSFET square-law (ports: inp vcm sq_sig sq_ref vdd vss)
3. **lpf_rc** — Passive R-C LPF at 50Hz (ports: inp out vdd vss)
4. **peak_detector** — Active peak with OTA + hold cap (ports: inp out vdd vss vbn vcm reset)
5. **rms_crest_top** — Top level (ports: inp rms_out rms_ref peak_out vdd vss reset vbn vcm)

## Interface Compatibility

### What program.md expects:
- `rms.spice` with subckt `rms_converter`: ports `vout_pga vrms ibias_5u vdd vss`
- `crest.spice` with subckt `crest_detector`: ports `vout_pga vrms vcrest ibias_1u vdd vss`

### What actually exists:
- `design.cir` with subckt `rms_crest_top`: ports `inp rms_out rms_ref peak_out vdd vss reset vbn vcm`

### Mismatches:
1. **Single combined subcircuit** vs two separate (rms + crest)
2. **Port names** differ: inp vs vout_pga, rms_out vs vrms, etc.
3. **Bias type**: actual needs `vbn vcm` (voltage), program.md passes `ibias_5u` (current)
4. **Reset pin**: actual has reset, program.md doesn't mention it
5. **Crest factor**: NOT computed in analog — the subcircuit provides peak and RMS^2,
   crest = peak/RMS would be computed digitally

## Results Summary
```
[PASS] RMS accuracy (calibrated, <5%): 1.6%
[PASS] RMS linearity (R2>0.99): 0.99992
[PASS] RMS bandwidth (10Hz-10kHz): 10Hz-20000Hz
[PASS] Peak accuracy (<10% @100mVpk): 5.2%
[PASS] Peak hold (<10% @500ms): 3.1%
[PASS] Crest factor sine (<15%): 3.6%
[PASS] Crest factor square (<15%): 3.8%
[PASS] Crest factor triangle (<15%): 4.5%
[PASS] Power (<25uW): 8.0uW
[PASS] PVT all corners pass: YES

Crest Factor Details (TT/27C):
  Sine: CF=1.363 (ideal=1.414, err=3.6%)
  Square: CF=0.962 (ideal=1.000, err=3.8%)
  Triangle: CF=1.655 (ideal=1.732, err=4.5%)

PVT Summary:
  tt/-40C: RMS=0.4% CF_sin=6.3% CF_sqr=6.3% CF_tri=7.0% Pwr=7.4uW
  tt/27C: RMS=1.6% CF_sin=3.6% CF_sqr=3.8% CF_tri=4.5% Pwr=8.0uW
  tt/85C: RMS=2.6% CF_sin=1.5% CF_sqr=2.0% CF_tri=2.5% Pwr=8.6uW
  ss/-40C: RMS=0.3% CF_sin=6.7% CF_sqr=6.7% CF_tri=7.6% Pwr=5.7uW
  ss/27C: RMS=1.8% CF_sin=3.8% CF_sqr=4.1% CF_tri=4.7% Pwr=6.2uW
  ss/85C: RMS=2.8% CF_sin=1.6% CF_sqr=2.0% CF_tri=2.6% Pwr=6.7uW
  ff/-40C: RMS=0.3% CF_sin=5.9% CF_sqr=6.0% CF_tri=6.7% Pwr=9.5uW
  ff/27C: RMS=1.2% CF_sin=3.5% CF_sqr=3.5% CF_tri=4.4% Pwr=10.2uW
  ff/85C: RMS=2.1% CF_sin=1.6% CF_sqr=2.1% CF_tri=2.6% Pwr=10.8uW
  sf/-40C: RMS=0.3% CF_sin=6.5% CF_sqr=6.6% CF_tri=7.3% Pwr=10.3uW
  sf/27C: RMS=1.1% CF_sin=4.3% CF_sqr=4.7% CF_tri=5.2% Pwr=10.9uW
  sf/85C: RMS=1.9% CF_sin=2.5% CF_sqr=3.0% CF_tri=3.6% Pwr=11.4uW
  fs/-40C: RMS=0.2% CF_sin=6.3% CF_sqr=6.2% CF_tri=7.1% Pwr=5.2uW
  fs/27C: RMS=1.8% CF_sin=3.3% CF_sqr=3.4% CF_tri=4.2% Pwr=5.7uW
  fs/85C: RMS=2.7% CF_sin=1.1% CF_sqr=1.4% CF_tri=2.1% Pwr=6.2uW

ALL PVT PASS

```

## Integration Approach

1. **Use rms_crest_top directly** in the top-level netlist
2. Create adapter wrappers:
   - `rms_converter` wrapper: takes ibias, generates vbn internally, maps rms_out
   - `crest_detector` wrapper: computes crest from peak/rms (or use behavioral)
3. The actual crest factor is peak_out / sqrt(rms_out - rms_ref), which needs
   analog division — in practice, both voltages go to the classifier as separate features
4. For integration, the 8 features can be remapped: use rms_out and peak_out directly

## Recommendation
The simplest integration path:
1. Include design.cir in the top netlist
2. Instantiate rms_crest_top with correct port mapping
3. Wire rms_out to classifier feature input (broadband_rms)
4. Wire peak_out / rms to crest factor feature (or approximate behaviorally)
5. Tie reset to a digital control signal or hardwire low
