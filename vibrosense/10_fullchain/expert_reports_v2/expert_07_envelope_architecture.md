# Expert Report 07: Envelope Detector Architecture Analysis

## 1. Current Architecture (envelope_det_fixed.spice)

### Block Diagram
```
vin --+--[OTA1]--[PMOS1]--+-- rect --[Gm-C LPF]-- vout
      |                    |
vcm --+--[OTA2]--[PMOS2]--+
                           |
                    [NMOS discharge]
                           |
                          vcm
```

### Stage 1: Precision Half-Wave Rectifier

**OTA1** (ota_pga_v2): Two-stage Miller compensated OTA
- inp = vin, inn = rect (negative feedback)
- When vin > rect: OTA1 output goes low, turns on PMOS1, rect charges up toward vin
- When vin < rect: OTA1 output goes high, PMOS1 turns off

**OTA2** (ota_pga_v2): Same topology
- inp = vcm, inn = rect
- When rect > vcm: OTA2 output goes low, turns on PMOS2, clamps rect toward vcm
- When rect < vcm: OTA2 output goes high, PMOS2 turns off

**PMOS output transistors**: W=2u L=1u each
- These are the charge-up devices
- Ron ~ 1/(mu_p * Cox * W/L * Vov) ~ several kOhm

**NMOS discharge**: W=0.42u L=100u, gate=VDD, source=vcm
- Operating in deep triode (Vgs=0.9V, Vth~0.5V, Vov=0.4V)
- Effective R ~ 6.85 MOhm (from design comments)
- At Vds=10mV: I = 10mV/6.85M = 1.46 nA
- tau with ~1pF parasitic = 6.85us

### Stage 2: Gm-C Low-Pass Filter

**5T OTA** with 5nF cap:
- Diff pair: W=2u L=4u NFET
- Tail: W=1u L=8u NFET, biased at vbn_lpf=0.70V
- PMOS mirror: W=4u L=4u

**gm estimation:**
- vbn_lpf = 0.70V, tail W/L = 1/8
- SKY130 NFET Vth ~ 0.5V, Vov = 0.70 - 0.5 = 0.2V
- In saturation: Id_tail ~ (1/2) * mu_n * Cox * (W/L) * Vov^2
- mu_n*Cox for SKY130 ~ 270 uA/V^2
- Id_tail ~ 0.5 * 270e-6 * (1/8) * 0.04 = 675 nA
- Each side: Id = 337 nA
- gm = 2*Id/Vov = 2*337n/0.2 = 3.37 uS (if in strong inversion)
- gm = Id/nVt = 337n/(1.3*26m) = 10 uS (if in weak inversion)
- Likely moderate inversion: gm ~ 2-5 uS

**Cutoff frequency:**
- fc = gm / (2*pi*C) = 3 uS / (2*pi*5nF) = 95 Hz
- This matches the design target of ~92 Hz

**Settling time:**
- tau = C/gm = 5nF/3uS = 1.67 ms
- 5*tau = 8.3 ms (to 99% of final value)
- With 200ms simulation, the LPF has >20 time constants to settle

## 2. Rectification Efficiency Analysis

For a sine wave input at amplitude A above VCM:
- Ideal half-wave rectifier: DC = A/pi = 0.318*A
- With OTA feedback: approaches ideal for A >> dead zone

Dead zone of OTA-based rectifier:
- OTA gain ~ 75 dB = 5623 V/V
- Minimum detectable signal: Vdd/gain = 1.8/5623 = 0.32 mV
- For 10 mVpp sine (5mV amplitude): well above dead zone

**Estimated conversion:**
- Input: 50 mVpp sine on top of VCM -> Amplitude = 25 mV
- Rectified peak: ~25 mV above VCM
- After LPF averaging: ~25/pi = 8 mV above VCM
- This matches the observed ~4-10 mV offsets in the full-chain!

## 3. Performance Issues

### Issue 1: Low Rectification Output for Small Signals

The rectifier works correctly but the OUTPUT RANGE is limited by physics:
- A half-wave rectifier's DC output is always less than the peak input
- For 10 mVpp BPF output: DC envelope = ~3 mV
- For 50 mVpp BPF output: DC envelope = ~16 mV
- For 100 mVpp BPF output: DC envelope = ~32 mV

To get 500 mV DC envelope (needed for good classifier spread),
we'd need ~1.6 Vpp at the BPF output -- which uses most of the rail.

### Issue 2: NMOS Discharge vs Signal Current

The NMOS discharge transistor provides ~1.5 nA per mV above VCM.
The OTA output current through PMOS: gm * Vdiff
- OTA gm ~ 30 uS, for 10 mV input: I_ota = 300 nA >> 1.5 nA
- The discharge doesn't compete with charge-up
- But between pulses, the discharge slowly pulls rect back to VCM
- tau_discharge = 6.85 MOhm * ~1 pF = 6.85 us
- At BPF3 freq (3162 Hz), period = 316 us >> tau
- So rect fully discharges between positive half-cycles
- This is correct half-wave rectifier behavior

### Issue 3: Competition Between OTA1 and OTA2

When vin ~ VCM (zero crossing), both OTAs are active simultaneously.
OTA1 tries to follow vin, OTA2 tries to clamp to vcm.
The PMOS transistors act as pass devices, so the lower OTA output
(more negative gate) wins (turns PMOS harder).

This is the correct behavior: at vin > vcm, OTA1 pulls rect up;
at vin < vcm, OTA2 clamps rect at vcm. The crossover is smooth
due to the high OTA gain.

## 4. Comparison with Block 04 Behavioral Model

The original Block 04 `design.cir` uses a behavioral model:
- B_hw1: I = max(0, 2.5e-6 * (vin - vcm))
- B_hw2: I = max(0, 2.5e-6 * (vcm - vin))
- R_rect = 400k -> V(rect) = |vin - vcm| (full-wave)
- G_lpf: gm = 6.28 nS, C = 10 pF -> fc = 100 Hz

**The full-chain uses a DIFFERENT envelope detector** (envelope_det_fixed.spice)
which is transistor-level with a HALF-wave rectifier, not full-wave.

| Feature | Behavioral (design.cir) | Transistor-level (fixed) |
|---------|------------------------|-------------------------|
| Rectification | Full-wave | Half-wave |
| Dead zone | 0 (ideal) | ~0.3 mV |
| DC output | (2/pi)*A = 0.637*A | (1/pi)*A = 0.318*A |
| LPF cutoff | 100 Hz | ~92 Hz |
| LPF settling | ~8 ms | ~8 ms |

**The transistor-level half-wave rectifier produces HALF the DC output
compared to the behavioral full-wave model.** This is another factor
contributing to the small envelope values.

## 5. Architectural Improvements

### Improvement 1: Full-Wave Rectification
Add a second OTA pair that handles the negative half-cycle:
- OTA3: inp=vcm, inn=vin (inverts the input)
- OTA4: same clamp function
- Sum the outputs
- **Effect**: 2x DC output

### Improvement 2: Post-Envelope Gain Stage
Add an amplifier after the LPF:
- Differential: amplify (Venv - VCM)
- Gain = 50-100x
- Output: VCM + 50*(Venv - VCM)
- 5 mV envelope -> 250 mV signal
- Can use same capacitive-feedback PGA topology
- **Effect**: Directly maps millivolt features to hundreds of millivolts

### Improvement 3: Chopper-Stabilized Rectifier
For ultra-low-signal applications:
- Chop the BPF output to baseband
- Amplify at baseband (avoid 1/f noise)
- Low-pass filter
- Higher complexity but much better for sub-millivolt signals

### Improvement 4: Peak-and-Hold Instead of Average
Replace LPF with peak detector (like the RMS block's peak_detector):
- Captures the PEAK of the rectified signal, not the average
- For impulsive signals (bearing faults), peak >> average
- Would produce 3-10x larger feature values
- Tradeoff: more sensitive to noise spikes

## 6. Recommended Priority

1. **Post-envelope gain** (simplest, most impactful): Add 50x gain after LPF
2. **Full-wave rectification**: Convert from half-wave to full-wave (2x improvement)
3. **Retrain classifier**: Adapt weights to actual voltage range (software-only fix)
4. **Peak-and-hold**: Consider for v2 if averaging doesn't suffice