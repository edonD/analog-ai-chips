# STUCK_REPORT — Gate 3: Slew Rate

## Failing Spec
- **Slew rate**: measured 6.87 mV/µs, required ≥ 10 mV/µs
- Gate 3 fails due to this single spec

## What was tried

1. **100mV step in unity-gain** (standard approach): SR = 6.87 mV/µs
2. **200mV step**: SR = 5.80 mV/µs (worse — larger step, same formula)
3. **500mV step**: SR = 3.68 mV/µs (even worse)
4. **Finer timestep (1ns)**: No change from 10ns timestep
5. **M1/M2 L=0.8u** for higher gm: Vov dropped below 50mV (Gate 1 fails)
6. **M1/M2 L=0.7u**: Vov=44mV (below 50mV, fails Gate 1)
7. **M1/M2 L=1.5u**: gm decreased 10%, worse bandwidth

## Root Cause Analysis

The verifier computes: `SR = 0.08 / (t90 - t10)` where t10/t90 are 10%/90% crossing times of a unity-gain step response.

For a first-order unity-gain buffer: `t90 - t10 = 2.2 × τ` where `τ = 1/(2π × BW)`.

The OTA bandwidth with 10pF load: BW = gm₁/(2π×C_total) ≈ 33 kHz.

This gives: `t90 - t10 = 2.2/(2π×33kHz) = 10.6 µs`
SR_measured = 0.08/10.6µs = 7.5 mV/µs < 10 mV/µs.

**To achieve SR ≥ 10 mV/µs**: BW ≥ 44 kHz → gm₁ ≥ 5.5 µS.

**Current gm₁ = 4.84 µS** (at M1: W=0.36u L=1u, Id=274nA, Vov=53mV).

**Why gm can't be increased:**
- Increasing current → M11 exceeds 500±50nA tail current spec
- Increasing M1 width → Vov drops below 50mV (fails Gate 1)
- Decreasing M1 L → Vth increases (reverse DIBL in SKY130 model at this geometry), Vov drops below 50mV

**The theoretical current-limited slew rate is 55 mV/µs** (548nA/10pF). The 10-90% method in unity-gain feedback measures the bandwidth-limited rise time, not the current-limited slew rate.

## Suggested path forward

1. **Relax the tail current spec** to 700nA: gives M1=350nA, gm≈5.7µS, BW≈45kHz, SR≈10.7 mV/µs ✓
2. **Relax M1/M2 Vov to 40mV**: allows W=0.42u, higher gm at same current
3. **Use DERIV measurement** at the step midpoint instead of 10-90% method
4. **Accept 6.87 mV/µs** as a process/power-budget limitation in SKY130 at sub-µA

## Current design passes
- Gate 1: ALL 13 transistors in correct operating region ✓
- Gate 2: DC gain 63.5dB, UGB 32.8kHz, PM 90° ✓
- Gate 3 DC sweep: Output swing 1.009 Vpp ✓
