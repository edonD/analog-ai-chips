# SAR ADC v3 — Overnight Simulation Results

Started: Wed Mar 25 22:53:50 UTC 2026

=== Launching TB3 and TB4 ===
TB3 PID: 704194, TB4 PID: 704195

## TB5: Active Power
```
iavg                =  -1.565594e-05 from=  2.000000e-05 to=  1.100100e-04
pavg                =  2.81807e-05
```
Power: 198.0 µW (target <100 µW)
**FAIL**

## TB6: Sleep Power
```
isleep              =  -1.917989e-08 from=  1.000000e-05 to=  9.028000e-05
psleep              =  3.45238e-08
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
Waiting started: Wed Mar 25 22:59:21 UTC 2026
