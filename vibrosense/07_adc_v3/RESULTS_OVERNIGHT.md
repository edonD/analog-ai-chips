# SAR ADC v3 — Overnight Simulation Results

Started: Thu Mar 26 11:00:21 UTC 2026

=== Launching TB3 and TB4 ===
TB3 PID: 745911, TB4 PID: 745912

## TB5: Active Power
```
iavg                =  -1.565917e-05 from=  2.000000e-05 to=  1.100100e-04
pavg                =  2.81865e-05
```
Power: 198.0 µW (target <100 µW)
**FAIL**

## TB6: Sleep Power
```
isleep              =  -1.918672e-08 from=  1.000000e-05 to=  9.028000e-05
psleep              =  3.45361e-08
```

## TB7: Wakeup Time
```
Circuit: * tb7: wakeup time measurement
sleep_n                                      0
xadc.xcomp.sleep_bar                       1.8
valid                                        0
a.xadc.xsar.adc_valid#branch_1_0               0
```

## TB8: Corner Analysis
```
tt: Conv1=155 (err -1 PASS) Conv2= 63 (err -1 PASS)
ss: Conv1=155 (err -1 PASS) Conv2= 63 (err -1 PASS)
ff: Conv1=156 (err +0 PASS) Conv2= 64 (err +0 PASS)
sf: Conv1=156 (err +0 PASS) Conv2= 63 (err -1 PASS)
fs: Conv1=155 (err -1 PASS) Conv2= 64 (err +0 PASS)
```

## Waiting for TB3/TB4...
Waiting started: Thu Mar 26 11:05:45 UTC 2026
Waiting finished: Thu Mar 26 14:07:40 UTC 2026

## TB3: DNL/INL (Code Density)
```
Loading v3_tb3_dnl_inl.dat...
  Read 2112757 data points, found 1284 conversions

=== TB3: DNL/INL Analysis ===
Total conversions: 1284
Code range: 99 to 255
Ideal hits per bin: 5.01

Histogram (first/last 10 codes):
  Code   0:    0 hits
  Code   1:    0 hits
  Code   2:    0 hits
  Code   3:    0 hits
  Code   4:    0 hits
  Code   5:    0 hits
  Code   6:    0 hits
  Code   7:    0 hits
  Code   8:    0 hits
  Code   9:    0 hits
  ...
  Code 246:    8 hits
  Code 247:    8 hits
  Code 248:    9 hits
  Code 249:    9 hits
  Code 250:    6 hits
  Code 251:    9 hits
  Code 252:   10 hits
  Code 253:    6 hits
  Code 254:    8 hits
  Code 255:   11 hits

--- DNL Results ---
Max DNL:  +1.1948 LSB (at code 115)
Min DNL:  -1.0000 LSB (at code 1)
Max |DNL|: 1.1948 LSB
Target: < 0.5 LSB → FAIL

--- INL Results ---
Max INL:  +0.0000 LSB (at code 1)
Min INL:  -97.5892 LSB (at code 99)
Max |INL|: 97.5892 LSB
Target: < 0.5 LSB → FAIL

--- Missing Codes ---
Missing codes: 98 → FAIL
  Codes with zero hits: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98]

=== Summary for README ===
Total conversions: 1284
Max |DNL|: 1.195 LSB FAIL
Max |INL|: 97.589 LSB FAIL
Missing codes: 98 FAIL
```

## TB4: ENOB (FFT)
```
Loading v3_tb4_enob.dat...
  Read 888994 data points, found 549 conversions

=== TB4: ENOB via FFT ===
FFT length N = 512
Signal cycles M = 43 (prime)
Sample rate fs = 500.0 kSPS
Signal freq fin = 41992.19 Hz
Total conversions available: 549
Using conversions 10 to 522
Code range: 1 to 255
Code mean: 127.8, std: 89.6

--- FFT Results (raw codes) ---
SNDR:  32.42 dB
ENOB:  5.09 bits
SFDR:  35.23 dB
THD:   -32.80 dB

--- FFT Results (with digital LSB correction: code>>1<<1) ---
SNDR:  32.21 dB
ENOB:  5.06 bits
SFDR:  35.23 dB
THD:   -32.81 dB

Target ENOB >= 7.0 bits → FAIL

Ideal 8-bit SNDR: 49.92 dB (ENOB = 8.00)

=== Summary for README ===
ENOB (raw):           5.09 bits (bit 0 stuck at 1)
ENOB (LSB corrected): 5.06 bits FAIL
SNDR (LSB corrected): 32.21 dB
SFDR (LSB corrected): 35.23 dB
```

## Completed
Finished: Thu Mar 26 14:07:48 UTC 2026

Check RESULTS_OVERNIGHT.md for all results.
