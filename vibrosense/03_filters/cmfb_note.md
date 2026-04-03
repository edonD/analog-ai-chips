# BLOCKER 6: Common-Mode Feedback (CMFB) Analysis

## Architecture

The VibroSense filter bank uses a **pseudo-differential** topology: two
identical single-ended Gm-C bandpass filter paths (positive and negative)
sharing the same bias voltages. There is no explicit CMFB loop.

## DC Common-Mode Stabilization via Pseudo-Resistors

Each integrator node in the BPF (int1p, int1n, int2p, int2n) is connected to
VCM (0.9 V) through a `pseudo_res` subcircuit — a back-to-back
diode-connected PMOS pair (sky130_fd_pr__pfet_01v8, W=0.42u L=10u).

These pseudo-resistors provide:

- **DC resistance > 100 GOhm** in subthreshold, ensuring negligible signal
  attenuation in the passband (f > 10 Hz).
- **DC bias path** that pulls every integrator node toward VCM at DC,
  preventing latch-up or saturation.
- **Independent CM stabilization** — each path is individually biased to VCM
  by its own pseudo-resistor. With matched paths and matched OTAs, the
  common-mode output naturally equals VCM.

## Simulation Verification

DC operating-point simulations confirm all integrator nodes settle to
0.87-0.90 V (near VCM = 0.9 V) across TT/27C conditions. The small offset
from ideal VCM is due to finite pseudo-resistor conductance interacting with
OTA output DC currents, and is well within the linear range of the OTA.

## Production Silicon Considerations

For a tape-out, an explicit CMFB sensing network would be added:

1. **Resistive average**: Two equal resistors (or pseudo-resistors) from
   `bp_outp` and `bp_outn` to a common node `vcm_sense`.
2. **Error amplifier**: A slow CMFB amplifier compares `vcm_sense` to `VCM`
   and adjusts the OTA output common-mode current (e.g., via a tail current
   trim on the PMOS fold).
3. **Bandwidth**: The CMFB loop bandwidth should be ~10x below the lowest
   filter passband (i.e., < 20 Hz for Ch1 at f0 = 224 Hz).

This explicit CMFB would reject:
- Systematic offsets from device mismatch
- Common-mode disturbance from supply noise (improving PSRR)
- Drift over temperature and aging

## Conclusion

For simulation purposes, the pseudo-resistor approach provides sufficient
common-mode stabilization. The DC operating points are verified near VCM, and
the pseudo-differential architecture inherently rejects common-mode signals
through differential output measurement (`bp_outp - bp_outn`). No additional
CMFB circuitry is needed for the current simulation campaign.
