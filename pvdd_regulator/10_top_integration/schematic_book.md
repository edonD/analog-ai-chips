# PVDD 5V LDO Regulator — Schematic Book

## SkyWater SKY130A — All 11 Blocks

---

## Table of Contents

1. [Top-Level System Diagram](#1-top-level-system-diagram)
2. [Block 00: Error Amplifier](#2-block-00-error-amplifier)
3. [Block 01: Pass Device](#3-block-01-pass-device)
4. [Block 02: Feedback Network](#4-block-02-feedback-network)
5. [Block 03: Compensation Network](#5-block-03-compensation-network)
6. [Block 04: Current Limiter](#6-block-04-current-limiter)
7. [Block 05: UV/OV Comparators](#7-block-05-uvov-comparators)
8. [Block 06: Level Shifters](#8-block-06-level-shifters)
9. [Block 07: MOS Voltage Clamp](#9-block-07-mos-voltage-clamp)
10. [Block 08: Mode Control](#10-block-08-mode-control)
11. [Block 09: Startup Circuit](#11-block-09-startup-circuit)
12. [Block 10: Top-Level Wiring](#12-block-10-top-level-wiring)

---

## 1. Top-Level System Diagram

```
  ┌─────────────────────────────────────────────────────────────────────────────────────────┐
  │                          PVDD 5V LDO REGULATOR (pvdd_regulator)                         │
  │                                                                                         │
  │  BVDD (5.4–10.5V)────────┬──────────┬──────────┬──────────┬──────┬──────┬──────────────│
  │                           │          │          │          │      │      │               │
  │                     ┌─────┴────┐┌────┴─────┐┌──┴───┐┌────┴────┐ │  ┌───┴──────────┐   │
  │                     │ BLOCK 08 ││ BLOCK 09 ││ BLK  ││ BLOCK  │ │  │  BLOCK 07    │   │
  │                     │   MODE   ││ STARTUP  ││  00  ││   04   │ │  │  MOS CLAMP   │   │
  │                     │ CONTROL  ││          ││ ERR  ││ CURRENT│ │  │              │   │
  │                     │          ││          ││ AMP  ││ LIMITER│ │  │ Prec. stack  │   │
  │                     │ Ladder   ││ Rgate    ││      ││        │ │  │ + Fast stack │   │
  │                     │ 4×Comp   ││ 1kΩ      ││2-stg ││ Sense  │ │  │ + Clamp FET  │   │
  │                     │ Logic    ││ ea_en    ││ OTA  ││ Mirror │ │  │              │   │
  │                     └──┬───┬───┘└──┬───┬───┘└──┬───┘└───┬────┘ │  └──────┬───────┘   │
  │                        │   │       │   │       │        │      │         │            │
  │  pass_off──────────────┘   │       │   │    ea_out      │      │         │            │
  │        │                   │       │   │       │        │      │         │            │
  │  ┌─────┴──────────┐       │    Rgate=1kΩ      │     gate ─────┤         │            │
  │  │ POR Gate Pullup │       │       │   │       │        │      │         │            │
  │  │                 │       │       │   gate────┼────────┘      │         │            │
  │  │ INV + PFET      │       │       │           │               │         │            │
  │  │ W=40u/2u (P)    │       │       │     ┌─────┴──────┐       │         │            │
  │  │ W=2u/2u  (N)    │───────┼───────┼─────│ BLOCK 01   │       │         │            │
  │  │ XMgate_pu       │       │       │     │ PASS DEVICE│       │         │            │
  │  │ W=4u/2u  (P)    │       │       │     │ 10× PMOS   │       │         │            │
  │  └─────────────────┘       │       │     │ W=50u/0.5u │       │         │            │
  │                            │       │     │ m=2 each   │       │         │            │
  │                            │       │     │ Total 1mm  │       │         │            │
  │                            │       │     └─────┬──────┘       │         │            │
  │                            │       │           │              │         │            │
  │  PVDD (5.0V regulated)────┼───────┼───────────┴──────────────┼─────────┤            │
  │        │                   │       │                          │         │            │
  │   ┌────┴────────┐    ┌────┴───┐   │                          │         │            │
  │   │ BLOCK 02    │    │BLK 05  │   │                          │         │            │
  │   │ FEEDBACK    │    │UV/OV   │   │                          │         │            │
  │   │ R_TOP 364kΩ │    │Comps   │   │                          │         │            │
  │   │ R_BOT 118kΩ │    │        │   │                          │         │            │
  │   │ Cff=22pF    │    │SVDD pwr│   │                          │         │            │
  │   └────┬────────┘    └──┬──┬──┘   │                          │         │            │
  │        │                │  │      │                          │         │            │
  │   vfb──┼────────────────┼──┼──────┘                          │         │            │
  │        │                │  │                                  │         │            │
  │   ┌────┴────────┐      │  │    avbg──────XRss──────vref_ss   │         │            │
  │   │ BLOCK 03    │      │  │    (1.226V)  100kΩ     ──┤├──    │         │            │
  │   │ COMP (empty)│      │  │                         Css=22nF │         │            │
  │   └─────────────┘      │  │                                  │         │            │
  │                         │  │                                  │         │            │
  │   Cload=200pF ─┤├─ GND │  │    ┌────────────────────┐       │         │            │
  │   Cout_ext=1µF ─┤├─GND │  │    │ BLOCK 06           │       │         │            │
  │                         │  │    │ LEVEL SHIFTER UP   │       │         │            │
  │   en(SVDD)──────────────┼──┼────│ en → en_bvdd       │       │         │            │
  │                         │  │    └────────────────────┘       │         │            │
  │                         │  │                                  │         │            │
  │  Ren_ea=100Ω ──────────┼──┼─── bvdd→ea_en (always HIGH)     │         │            │
  │                         │  │                                  │         │            │
  │   SVDD (2.2V)───────────┘  │    ibias───→ EA, Clamp          │         │            │
  │                            │    Iibias_ilim=1µA ─────────────┘         │            │
  │   GND ─────────────────────┴───────────────────────────────────────────┘            │
  │                                                                                     │
  │  PORTS: bvdd pvdd gnd avbg ibias svdd en en_ret uv_flag ov_flag startup_done        │
  └─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Block 00: Error Amplifier

**Two-stage OTA, BVDD-powered. Ports: vref, vfb, vout_gate, gnd, ibias, en, bvdd**

### Enable & Bias Section

```
                        bvdd
                         │
                 ┌───────┴───────┐
                 │  XMpu (PFET)  │
                 │  W=4u  L=2u   │
                 │  S=bvdd B=bvdd│
                 └───────┬───────┘
                    D    │
              vout_gate──┘
                    G────── en


     ibias ─────────┬──────────────────────────────────────────
                    │
            ┌───────┴───────┐
            │ XMen (NFET)   │
            │ W=20u  L=1u   │
            │ G=en  S=ibias │
            │ D=ibias_en    │
            └───────┬───────┘
                    │
               ibias_en
                    │
            ┌───────┴───────┐
            │ XMbn0 (NFET)  │         Diode-connected
            │ W=2u   L=8u   │         (G=D=ibias_en)
            │ S=gnd  B=gnd  │         Reference: 1µA
            └───────┬───────┘
                    │
                   gnd
```

### PMOS Tail Bias Mirror (BVDD domain)

```
             bvdd                              bvdd
              │                                 │
      ┌───────┴───────┐               ┌────────┴────────┐
      │ XMbp0 (PFET)  │               │ XMtail (PFET)   │
      │ W=20u  L=4u   │  ┌── pb_tail──│ W=20u  L=4u     │
      │ m=4            │  │            │ m=4              │
      │ Diode: G=D     │──┘            │ G=pb_tail        │
      └───────┬───────┘               └────────┬────────┘
              │                                 │
           pb_tail                           tail_s
              │                          (to diff pair)
      ┌───────┴───────┐
      │ XMbn_pb (NFET)│
      │ W=20u  L=8u   │
      │ m=4            │
      │ G=ibias_en     │
      │ S=gnd  B=gnd   │
      └───────┬───────┘
              │
             gnd
```

### Stage 1: PMOS Differential Pair + NMOS Mirror Load

```
                                  bvdd
                                   │
                           ┌───────┴───────┐
                           │ XMtail (PFET)  │
                           │ W=20u L=4u m=4 │
                           │ G=pb_tail      │
                           └───────┬───────┘
                                   │
                                tail_s
                            ┌──────┴──────┐
                            │             │
                    ┌───────┴──────┐ ┌────┴───────┐
                    │ XM1 (PFET)   │ │ XM2 (PFET) │
                    │ W=80u L=4u   │ │ W=80u L=4u │
                    │ m=2          │ │ m=2         │
                    │ G=vref (+)   │ │ G=vfb  (−) │
                    │ S=tail_s     │ │ S=tail_s   │
                    │ B=bvdd       │ │ B=bvdd     │
                    └───────┬──────┘ └────┬───────┘
                            │             │
                     d1 ────┘             └──── d2 ───── → to Stage 2
                     │(diode side)             │(output)
              ┌──────┴───────┐          ┌──────┴───────┐
              │ XMn_l (NFET) │          │ XMn_r (NFET) │
              │ W=20u L=8u   │   d1     │ W=20u L=8u   │
              │ m=2           │───┤G     │ m=2          │
              │ Diode: G=D=d1│          │ G=d1 (mirror)│
              └──────┬───────┘          └──────┬───────┘
                     │                         │
                    gnd                       gnd
```

### Stage 2: NFET Common-Source + PFET Load + Miller Compensation

```
             bvdd
              │
      ┌───────┴───────┐
      │ XMcs_p (PFET)  │
      │ W=20u  L=4u    │
      │ m=2             │
      │ G=pb_tail       │
      │ S=bvdd B=bvdd   │
      └───────┬────────┘
              │
         vout_gate ──────────────────────────────── OUTPUT
              │                                    (to pass device gate)
              │         ┌─── Rc=5kΩ ───┬─── Cc=40pF ───┐
              │         │   comp_mid   │               │
              │         └──────────────┘               │
              │                                        d2 (from Stage 1)
      ┌───────┴───────┐                    Miller compensation
      │ XMcs_n (NFET)  │                    across Stage 2
      │ W=20u  L=2u    │
      │ G=d2            │
      │ S=gnd  B=gnd    │
      └───────┬────────┘
              │
             gnd
```

### Complete Error Amplifier — Unified View

```
                                           bvdd
         ┌───────────────────────────────────┼─────────────────────────────────┐
         │                                   │                                 │
    XMpu(P)                           XMbp0(P)                          XMcs_p(P)
    W=4u/2u                          W=20u/4u m=4                      W=20u/4u m=2
    G=en──┐                          Diode─┐                           G=pb_tail
         │                                │                                 │
    vout_gate                          pb_tail ──────────────────┐     vout_gate
         │                                │                      │          │
         │                         XMbn_pb(N)                 XMtail(P)     │
         │                         W=20u/8u m=4              W=20u/4u m=4   │
         │                         G=ibias_en                G=pb_tail      │
         │                                │                      │          │
    XMen(N)                              gnd                  tail_s        │
    W=20u/1u                                              ┌──────┴──────┐   │
    G=en                                                  │             │   │
         │                                          XM1(P)         XM2(P)   │
    ibias_en                                       W=80u/4u m=2  W=80u/4u m=2
         │                                         G=vref         G=vfb     │
    XMbn0(N)                                              │             │   │
    W=2u/8u                                        d1─────┘      d2────┘   │
    Diode                                          │              │         │
         │                                    XMn_l(N)       XMn_r(N)      │
        gnd                                   W=20u/8u m=2  W=20u/8u m=2  │
                                              Diode(d1)     G=d1           │
                                                   │              │        │
                                                  gnd       Cc=40pF       │
                                                             Rc=5kΩ       │
                                                              │────────────┘
                                                              d2     vout_gate
                                                                    XMcs_n(N)
                                                                    W=20u/2u
                                                                    G=d2
                                                                        │
                                                                       gnd
```

---

## 3. Block 01: Pass Device

**10 parallel PMOS instances. Ports: gate, bvdd, pvdd**

```
                                    bvdd (Source, Bulk)
           ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
           │      │      │      │      │      │      │      │      │      │
       ┌───┴──┐┌──┴───┐┌─┴──┐┌──┴──┐┌──┴──┐┌──┴──┐┌──┴──┐┌──┴──┐┌──┴──┐┌──┴──┐
       │ XM1  ││ XM2  ││XM3 ││ XM4 ││ XM5 ││ XM6 ││ XM7 ││ XM8 ││ XM9 ││XM10 │
       │(PFET)││(PFET)││    ││     ││     ││     ││     ││     ││     ││     │
       │W=50u ││W=50u ││    ││     ││     ││     ││     ││     ││     ││     │
       │L=0.5u││L=0.5u││ ×8 ││same ││     ││     ││     ││     ││     ││     │
       │m=2   ││m=2   ││more││     ││     ││     ││     ││     ││     ││     │
       └───┬──┘└──┬───┘└─┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘
           │      │      │      │      │      │      │      │      │      │
           └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
                                          │
                                        pvdd (Drain) ── regulated output
                                          │
     gate ────────────────────────────────┘ (all 10 gates tied together)

     Device: sky130_fd_pr__pfet_g5v0d10v5
     Each instance: W=50µm, L=0.5µm, m=2 → 100µm effective
     10 instances → Total Weff = 1.0 mm
```

### Single Instance Detail

```
            bvdd (S,B)
             │
     ┌───────┴───────┐
     │    PMOS HV    │
     │  g5v0d10v5    │
     │               │
     │  W = 50µm     │
     │  L = 0.5µm    │
     │  m = 2        │
     │               │
     │  ┌─G          │
     │  │            │
     └──┼────────────┘
        │       │
      gate    pvdd (D)
```

---

## 4. Block 02: Feedback Network

**Resistive voltage divider. Ports: pvdd, vfb, gnd**

```
     pvdd (5.0V regulated)
      │
      │            ┌──────────────────────────┐
      ├────────────┤       Cff = 22pF         │   (FIX-25: feedforward cap
      │            │   (added in Block 10)     │    across R_TOP, zero @20kHz)
      │            └──────────────────────────┤
      │                                        │
     ┌┴────────────────────────┐               │
     │  XR_TOP                 │               │
     │  sky130_fd_pr__         │               │
     │    res_xhigh_po         │               │
     │                         │               │
     │  W = 3.0 µm            │               │
     │  L = 536 µm            │               │
     │  R ≈ 364 kΩ            │               │
     │  (Rsh ≈ 2kΩ/sq)        │               │
     └┬────────────────────────┘               │
      │                                        │
      ├────────────────────────────────────────┘
      │
     vfb ≈ 1.226V ─────────────────── to EA (−) input
      │
     ┌┴────────────────────────┐
     │  XR_BOT                 │
     │  sky130_fd_pr__         │
     │    res_xhigh_po         │
     │                         │
     │  W = 3.0 µm            │
     │  L = 174.30 µm         │
     │  R ≈ 118 kΩ            │
     └┬────────────────────────┘
      │
     gnd

     Ratio: R_BOT/(R_TOP+R_BOT) = 118k/482k = 0.2448
     vfb = 5.0V × 0.2448 = 1.224V ≈ 1.226V (bandgap)
     Idiv = 5.0V / 482kΩ ≈ 10.4µA
```

---

## 5. Block 03: Compensation Network

**Empty placeholder — all compensation handled internally.**

```
     ┌──────────────────────────────────────────────┐
     │          BLOCK 03: COMPENSATION              │
     │                                              │
     │   ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐   │
     │     STATUS: EMPTY — NO COMPONENTS          │
     │   └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘   │
     │                                              │
     │   Actual compensation lives in:              │
     │                                              │
     │   Block 00 (EA inner):                       │
     │     Cc = 40pF,  Rc = 5kΩ  (Miller)         │
     │                                              │
     │   Block 10 (top-level):                      │
     │     Cout_ext = 1µF  (external bypass)       │
     │     Cff = 22pF  (feedforward, FIX-25)       │
     │                                              │
     │   Ports: vout_gate, pvdd, gnd  (pass-thru)  │
     └──────────────────────────────────────────────┘
```

---

## 6. Block 04: Current Limiter

**Sense-mirror with current-mode comparator. Ports: gate, bvdd, pvdd, gnd, ilim_flag, ibias**

### Cascode Bias Divider

```
         bvdd (7V nom)
          │
     ┌────┴──────────────┐
     │ XRcas_top          │
     │ res_xhigh_po       │
     │ W=1µm  L=300µm    │
     │ R ≈ 600kΩ         │
     └────┬──────────────┘
          │
       cas_bias ≈ 4.0V
          │
     ┌────┴──────────────┐
     │ XRcas_bot          │
     │ res_xhigh_po       │
     │ W=1µm  L=400µm    │
     │ R ≈ 800kΩ         │
     └────┬──────────────┘
          │
         gnd

     cas_bias = 7V × 800k/(600k+800k) = 4.0V
     Iq ≈ 7V / 1.4MΩ ≈ 5µA
```

### Sense Mirror + Cascode

```
         bvdd                                          bvdd
          │ (Source, Bulk)                               │
     ┌────┴────────┐                              (pass device
     │ XMs (PFET)  │                               also here)
     │ W=1u L=0.5u │
     │ G=gate       │─────────── gate ──────────── (shared)
     └────┬────────┘
          │
       cas_mid
          │
     ┌────┴────────┐
     │XMcas (PFET) │
     │ W=10u L=0.5u│
     │ G=cas_bias   │
     │ S=cas_mid    │
     │ B=cas_mid    │
     └────┬────────┘
          │
       sense_out ──── Isense = Ipass / 1000
          │
          ├────────────────────────────── → to inverter
          │
     ┌────┴──────────┐
     │XMref_m (NFET) │
     │ W=100u  L=8u  │         50:1 mirror
     │ G=ibias        │─────┐   Sinks 50µA from sense_out
     └────┬──────────┘     │
          │                 │
         gnd           ┌───┴──────────┐
                       │XMref_d (NFET)│
                       │ W=2u   L=8u  │  Diode-connected
                       │ G=D=ibias    │  Receives 1µA ibias
                       └───┬──────────┘
                           │
                          gnd
```

### Comparator Inverter + Clamp + Flag

```
       bvdd                    bvdd     bvdd     bvdd     bvdd
        │                       │        │        │        │
   ┌────┴─────┐           ┌────┴───┐┌───┴───┐┌───┴───┐┌───┴───┐
   │XMinv_p   │           │XMclamp1││Mclamp2││Mclamp3││Mclamp4│
   │(PFET)    │           │(PFET)  ││(PFET) ││(PFET) ││(PFET) │
   │W=20u L=1u│           │W=50u   ││W=50u  ││W=50u  ││W=50u  │
   │G=sense_  │           │L=0.5u  ││L=0.5u ││L=0.5u ││L=0.5u │
   │  out     │           │G=det_n ││G=det_n││G=det_n││G=det_n│
   └────┬─────┘           └───┬────┘└───┬───┘└───┬───┘└───┬───┘
        │                     │         │        │        │
     det_n ───────────────────┼─────────┼────────┼────────┘
        │                     └─────────┴────────┘
        │                              │
   ┌────┴─────┐                      gate ──── (clamped toward bvdd
   │XMinv_n   │                                  when overcurrent)
   │(NFET)    │
   │W=10u L=1u│
   │G=sense_  │
   │  out     │
   └────┬─────┘
        │
       gnd

   bvdd ────┐
            ┌┴───────────┐
            │ XRpu        │
            │ res_xhigh_po│
            │ W=1 L=500   │     Pullup on det_n
            │ R ≈ 1MΩ    │     (keeps det_n HIGH when no OC)
            └┬───────────┘
             │
          det_n
```

### Flag Output

```
       pvdd                        det_n
        │                           │
   ┌────┴───────┐             ┌─────┴──────┐
   │ XMfp(PFET) │             │            │
   │ W=2u L=1u  │──── det_n   │            │
   └────┬───────┘             │            │
        │                     │            │
    ilim_flag ────────────────┘            │
        │                            ┌─────┴──────┐
   ┌────┴───────┐                    │ XMfn(NFET) │
   │ XMfn(NFET) │                    │ W=2u L=1u  │
   │ W=2u L=1u  │                    └─────┬──────┘
   │ G=det_n    │                          │
   └────┬───────┘                         gnd
        │
       gnd

   Normal:    det_n=HIGH → ilim_flag=LOW  (no overcurrent)
   Overcurrent: det_n=LOW  → ilim_flag=HIGH (flag asserted)
```

### Current Limiter — Complete Signal Flow

```
                bvdd
                 │
         ┌───────┤
         │       │
      XMs(P)   XRcas_top        Trip point: 50mA
     W=1u/0.5u  600kΩ           (Isense > 50µA → flag)
     G=gate      │
         │    cas_bias ≈ 4V     Signal flow:
      cas_mid    │               1. XMs mirrors 1/1000 of Ipass
         │    XRcas_bot          2. XMcas ensures Vds matching
      XMcas(P)   800kΩ          3. XMref_m sinks 50µA (50:1 of ibias)
     W=10u/0.5u  │               4. If Isense > 50µA: sense_out HIGH
     G=cas_bias gnd              5. Inverter: det_n goes LOW
         │                       6. 4× Clamp PFETs pull gate → BVDD
      sense_out                  7. Pass device turns OFF
         │
    ┌────┼────┐
    │    │    │
  XMref_m  XMinv ──→ det_n ──→ 4×XMclamp ──→ gate
  (N)100u/8u              │            │
  G=ibias              XRpu         XMfp/XMfn
    │                  1MΩ          → ilim_flag
   gnd
```

---

## 7. Block 05: UV/OV Comparators

### UV Comparator (trips at PVDD < 4.3V)

**Ports: pvdd, vref, uv_flag, vdd_comp (1.8V), gnd, en**

```
       pvdd
        │
   ┌────┴──────────┐
   │ XR_top         │
   │ res_xhigh_po   │
   │ W=2µm L=500µm │
   │ R ≈ 500kΩ     │
   └────┬──────────┘
        │
     mid_uv ≈ 1.226V at PVDD=4.3V
        │
        ├──────────────────────── XR_hyst ──── out_n
        │                        W=1 L=1250
   ┌────┴──────────┐             R ≈ 2.5MΩ
   │ XR_bot         │             (hysteresis feedback)
   │ res_xhigh_po   │
   │ W=2µm L=199.4µm│
   │ R ≈ 199.4kΩ   │
   └────┬──────────┘
        │
       gnd

   Ratio = 199.4/(500+199.4) = 0.2851
   Trip: mid_uv = vref → PVDD = 1.226/0.2851 = 4.30V
```

### UV Comparator Core (1.8V domain)

```
                    vdd_comp (1.8V)
                         │
              ┌──────────┼──────────┐
              │          │          │
         ┌────┴───┐ ┌───┴────┐    │
         │ XM3(P) │ │ XM4(P) │    │
         │W=2u L=1u│ │W=2u L=1u│    │   PMOS current mirror load
         │Diode   │ │G=out_p │    │
         └───┬────┘ └───┬────┘    │
             │          │         │
          out_p      out_n ───────┼───── → to NOR gate
             │          │         │
         ┌───┴────┐ ┌───┴────┐   │
         │ XM1(N) │ │ XM2(N) │   │
         │W=2u L=1u│ │W=2u L=1u│   │   NMOS differential pair
         │G=mid_uv│ │G=vref  │   │
         └───┬────┘ └───┬────┘   │
             │          │         │
             └────┬─────┘         │
                  │               │
         ┌────────┴────────┐     │
         │ XMtail (NFET)   │     │
         │ W=1u  L=4u      │     │
         │ G=bias_n         │     │   Tail current source
         └────────┬────────┘     │
                  │               │
                 gnd              │
                              ┌───┴──────────┐
                              │ XR_bias       │
                              │ W=2 L=800     │
                              │ R ≈ 800kΩ    │
                              └───┬──────────┘
                                  │
                              ┌───┴────┐
                              │XMbias  │
                              │(NFET)  │  Diode, ~1µA
                              │W=1u L=4u│
                              └───┬────┘
                                  │
                                 gnd
```

### NOR Output Gate (UV)

```
         vdd_comp                           en
          │                                  │
     ┌────┴──────┐                    ┌──────┴──────┐
     │XMnor_p1(P)│                    │XMen_n (NFET)│
     │W=4u L=0.15u│                    │W=0.42u      │    Enable
     │G=out_n    │                    │L=0.15u      │    Inverter
     └────┬──────┘                    └──────┬──────┘
          │                                  │
       nor_mid                            en_bar
          │                                  │
     ┌────┴──────┐                    ┌──────┴──────┐
     │XMnor_p2(P)│                    │XMen_p (PFET)│
     │W=4u L=0.15u│                    │W=0.84u      │
     │G=en_bar   │                    │L=0.15u      │
     └────┬──────┘                    └──────┬──────┘
          │                                  │
       uv_flag ──────────── OUTPUT        vdd_comp
          │
     ┌────┴──────┐  ┌────────────┐
     │XMnor_n1(N)│  │XMnor_n2(N)│
     │W=1u       │  │W=1u       │     NMOS in parallel
     │L=0.15u    │  │L=0.15u    │
     │G=out_n    │  │G=en_bar   │
     └────┬──────┘  └────┬──────┘
          │              │
          └──────┬───────┘
                 │
                gnd

     NOR truth table:
     out_n=L, en_bar=L → uv_flag = HIGH (UV detected, enabled)
     out_n=H, en_bar=L → uv_flag = LOW  (no UV)
     en_bar=H           → uv_flag = LOW  (disabled)
```

### OV Comparator (trips at PVDD > 5.5V)

**Same topology as UV but with swapped diff pair inputs and different divider ratio.**

```
       pvdd                             vdd_comp (1.8V)
        │                                    │
   ┌────┴──────────┐              ┌──────────┼──────────┐
   │ XR_top         │              │          │          │
   │ W=2 L=500      │         ┌───┴────┐ ┌───┴────┐    │
   │ R ≈ 500kΩ     │         │ XM3(P) │ │ XM4(P) │    │
   └────┬──────────┘         │W=2u L=1u│ │W=2u L=1u│    │  Mirror
        │                    │Diode   │ │G=out_p │    │
     mid_ov                  └───┬────┘ └───┬────┘    │
        │                       │          │         │
        ├─── XR_hyst ── ov_flag  out_p    out_n ──→ NOR → ov_flag
        │    W=1 L=4000          │          │
        │    R ≈ 8MΩ        ┌───┴────┐ ┌───┴────┐
   ┌────┴──────────┐        │ XM1(N) │ │ XM2(N) │
   │ XR_bot         │        │W=2u L=1u│ │W=2u L=1u│
   │ W=2 L=146      │        │G=vref  │ │G=mid_ov│    ← inputs SWAPPED
   │ R ≈ 146kΩ     │        └───┬────┘ └───┬────┘      vs UV comparator
   └────┬──────────┘             └────┬─────┘
        │                             │
       gnd                       XMtail(N)
                                 W=1u L=4u
   Trip: 1.226V / (146/(500+146))                │
       = 1.226 / 0.2260 = 5.43V                 gnd
   (compensated to ~5.5V with Rhyst)
```

---

## 8. Block 06: Level Shifters

### Level Shifter Up: SVDD (2.2V) → BVDD (5.4–10.5V)

**Ports: in, out, bvdd, svdd, gnd**

```
                 bvdd                               bvdd
                  │                                  │
          ┌───────┴───────┐                  ┌───────┴───────┐
          │ XMP1 (PFET)   │    cross-coupled │ XMP2 (PFET)   │
          │ W=4u  L=0.5u  │←─────┐    ┌────→│ W=5u  L=0.5u  │
          │ G=out          │      │    │     │ G=n1           │
          └───────┬───────┘      │    │     └───────┬───────┘
                  │               │    │             │
               n1 ────────────────┘    └──────── out ──── OUTPUT
                  │                                  │    (BVDD level)
          ┌───────┴───────┐                  ┌───────┴───────┐
          │ XMN1 (NFET)   │                  │ XMN2 (NFET)   │
          │ W=15u  L=1u   │                  │ W=15u  L=1u   │
          │ G=in           │                  │ G=in_b         │
          └───────┬───────┘                  └───────┬───────┘
                  │                                  │
                 gnd                                gnd

          ┌─────────────────────────┐
          │ Input Inverter (SVDD)   │
          │                         │
          │    svdd                  │
          │     │                   │
          │  XMP_INV(P) W=4u/0.5u  │
          │     │                   │
     in ──┤── in_b                  │
          │     │                   │
          │  XMN_INV(N) W=2u/0.5u  │
          │     │                   │
          │    gnd                  │
          └─────────────────────────┘

     Zero static current (cross-coupled latch)
     Asymmetric PMOS: XMP2 wider (5u vs 4u) for stronger output drive
```

### Level Shifter Down: PVDD (5.0V) → SVDD (2.2V)

**Ports: in, out, pvdd, svdd, gnd**

```
                 svdd                               svdd
                  │                                  │
          ┌───────┴───────┐                  ┌───────┴───────┐
          │ XMP1 (PFET)   │    cross-coupled │ XMP2 (PFET)   │
          │ W=4u  L=0.5u  │←─────┐    ┌────→│ W=4u  L=0.5u  │
          │ G=out          │      │    │     │ G=n1           │
          └───────┬───────┘      │    │     └───────┬───────┘
                  │               │    │             │
               n1 ────────────────┘    └──────── out ──── OUTPUT
                  │                                  │    (SVDD level)
          ┌───────┴───────┐                  ┌───────┴───────┐
          │ XMN1 (NFET)   │                  │ XMN2 (NFET)   │
          │ W=2u  L=1u    │                  │ W=2u  L=1u    │
          │ G=in           │                  │ G=in_b         │
          └───────┬───────┘                  └───────┬───────┘
                  │                                  │
                 gnd                                gnd

          ┌─────────────────────────┐
          │ Input Inverter (PVDD)   │
          │                         │
          │    pvdd                  │
          │     │                   │
          │  XMP_INV(P) W=4u/0.5u  │
          │     │                   │
     in ──┤── in_b                  │
          │     │                   │
          │  XMN_INV(N) W=2u/0.5u  │
          │     │                   │
          │    gnd                  │
          └─────────────────────────┘

     Same topology as UP shifter, symmetric PMOS (both W=4u)
     Pull-down NMOS smaller (W=2u vs 15u) — less current needed
```

---

## 9. Block 07: MOS Voltage Clamp

**Hybrid clamp: precision stack + fast stack + clamp FET. Ports: pvdd, gnd, ibias**

### Precision Stack (N-P-N-P, 4 devices + Rstack)

```
       pvdd ───────────────────────────────────────────────┐
        │                                                   │
   ┌────┴────────────┐                                     │
   │ XMd1 (NFET)     │  Diode: G=D=pvdd                   │
   │ W=2.2u  L=4u    │  Body=n3                            │
   └────┬────────────┘                                     │
        │                                                   │
       n3                                                   │
        │                                                   │
   ┌────┴────────────┐                                     │
   │ XMd2 (PFET)     │  Diode: G=D=n2                     │
   │ W=20u   L=4u    │  Body=n3                            │
   └────┬────────────┘                                     │
        │                                                   │
       n2                                                   │
        │                                                   │
   ┌────┴────────────┐                                     │
   │ XMd3 (NFET)     │  Diode: G=D=n2                     │
   │ W=2.2u  L=4u    │  Body=n1                            │
   └────┬────────────┘                                     │
        │                                                   │
       n1                                                   │
        │                                                   │
   ┌────┴────────────┐                                     │
   │ XMd4 (PFET)     │  Diode: G=D=n1                     │
   │ W=20u   L=4u    │  Body=ns                            │
   └────┬────────────┘                                     │
        │                                                   │
       ns                                                   │
        │                                                   │
   ┌────┴────────────┐                                     │
   │ XRstack          │                                     │
   │ res_xhigh_po     │                                     │
   │ W=2µm  L=190µm  │                                     │
   │ R ≈ 190kΩ       │                                     │
   └────┬────────────┘                                     │
        │                                                   │
       vg ─────────────────────────────────────── G ────────┤
        │                                                   │
        ├──── XRpd (res_xhigh_po W=2 L=500, R≈500kΩ) ─── gnd
        │     (gate pulldown)                               │
        │                                                   │
        ├──── XMptat_m (NFET W=5u L=8u, G=ibias)          │
        │     (PTAT compensation: sinks ~2.5µA)            │
        │                                                   │
   ┌────┴────────────┐                              ┌──────┴──────────┐
   │ XMptat_d (NFET) │                              │ XMclamp (NFET)  │
   │ W=2u  L=8u      │  Diode: receives ibias       │ W=50u  L=0.5u   │
   │ G=D=ibias        │                              │ m=4 (200µm tot) │
   └────┬────────────┘                              │ G=vg             │
        │                                            │ Body=gnd         │
       gnd                                           └──────┬──────────┘
                                                            │
                                                           gnd
```

### Fast Parallel Diode Stack (7× NFET)

```
       pvdd
        │
   ┌────┴──────────┐
   │ XMf1 (NFET)   │  Diode: G=D=pvdd
   │ W=10u  L=0.5u │  Body=gnd
   └────┬──────────┘
        │
       nf6
        │
   ┌────┴──────────┐
   │ XMf2 (NFET)   │  Diode: G=D=nf6
   │ W=10u  L=0.5u │  Body=gnd
   └────┬──────────┘
        │
       nf5
        │
   ┌────┴──────────┐
   │ XMf3 (NFET)   │  Diode: G=D=nf5
   │ W=10u  L=0.5u │  Body=gnd
   └────┬──────────┘
        │
       nf4
        │
   ┌────┴──────────┐
   │ XMf4 (NFET)   │  Diode: G=D=nf4
   │ W=10u  L=0.5u │  Body=gnd
   └────┬──────────┘
        │
       nf3
        │
   ┌────┴──────────┐
   │ XMf5 (NFET)   │  Diode: G=D=nf3
   │ W=10u  L=0.5u │  Body=gnd
   └────┬──────────┘
        │
       nf2
        │
   ┌────┴──────────┐
   │ XMf6 (NFET)   │  Diode: G=D=nf2
   │ W=10u  L=0.5u │  Body=gnd
   └────┬──────────┘
        │
       nf1
        │
   ┌────┴──────────┐
   │ XMf7 (NFET)   │  Diode: G=D=nf1
   │ W=10u  L=0.5u │  Body=gnd
   └────┬──────────┘
        │
       gnd

   Fast stack Vonset ≈ 7 × Vth(short-L) ≈ 7 × 0.7V ≈ 4.9V
   Catches fast transients before precision stack engages
```

### MOS Clamp — Combined View

```
           pvdd ──────────────────────┬─────────────────────────────────
            │                         │                                 │
    ┌───────┴───────┐         ┌───────┴──────┐                  ┌──────┴──────┐
    │  PRECISION     │         │ FAST DIODE   │                  │ CLAMP NFET  │
    │  STACK         │         │ STACK        │                  │             │
    │  4× FET        │         │ 7× NFET     │                  │ XMclamp     │
    │  (N-P-N-P)     │         │ L=0.5u      │                  │ W=50u/0.5u  │
    │  L=4u each     │         │ W=10u each  │                  │ m=4         │
    │  + Rstack      │         │              │                  │ G=vg        │
    │    190kΩ       │         │ Vonset≈4.9V  │                  │             │
    │                │         │ (fast)       │                  │             │
    │  Sets vg via   │         │              │                  │             │
    │  Vth sum +     │         │              │                  │             │
    │  IR drop       │         │              │                  │             │
    └───────┬───────┘         └───────┬──────┘                  └──────┬──────┘
            │                         │                                 │
           vg                        gnd                               gnd
            │
    ┌───────┼──────────┐
    │       │          │
  XRpd    XMptat_m   XMptat_d
  500kΩ   W=5u/8u    W=2u/8u
    │     G=ibias    Diode
    │       │          │
   gnd     gnd        gnd

   Clamp onset ≈ sum(4×Vth) + Istack×190kΩ − Iptat×500kΩ
   PTAT compensation: hot → Iptat↑ → vg↓ → onset↑ (tracks Vth drop)
```

---

## 10. Block 08: Mode Control

**BVDD-powered resistor ladder + 4 Schmitt comparators + combinational logic.**
**Ports: bvdd, pvdd, svdd, gnd, en_ret, bypass_en, ea_en, ref_sel, uvov_en, ilim_en, pass_off**

### Resistor Ladder

```
       bvdd (5.4–10.5V)
        │
   ┌────┴──────────┐
   │ XRtop          │  W=1 L=37    R ≈ 74kΩ
   └────┬──────────┘
        │
      tap1 ──────────────→ COMP1  (TH1 = 2.5V BVDD)
        │                   ratio = tap1/bvdd = (62+6+17+69)/(37+62+6+17+69) = 0.806
   ┌────┴──────────┐
   │ XR12           │  W=1 L=62    R ≈ 124kΩ
   └────┬──────────┘
        │
      tap2 ──────────────→ COMP2  (TH2 = 4.2V BVDD)
        │                   ratio = (6+17+69)/(37+62+6+17+69) = 0.482
   ┌────┴──────────┐
   │ XR23           │  W=1 L=6     R ≈ 12kΩ
   └────┬──────────┘
        │
      tap3 ──────────────→ COMP3  (TH3 = 4.5V BVDD)
        │                   ratio = (17+69)/(37+62+6+17+69) = 0.450
   ┌────┴──────────┐
   │ XR34           │  W=1 L=17    R ≈ 34kΩ
   └────┬──────────┘
        │
      tap4 ──────────────→ COMP4  (TH4 = 5.6V BVDD)
        │                   ratio = 69/(37+62+6+17+69) = 0.361
   ┌────┴──────────┐
   │ XRbot          │  W=1 L=69    R ≈ 138kΩ
   └────┬──────────┘
        │
       gnd

   Total R ≈ 382kΩ (all res_xhigh_po, Rsh≈2kΩ/sq)
   Iq ≈ BVDD / 382kΩ = 7V / 382k ≈ 18.3µA
```

### Schmitt Trigger Comparator (one of four — COMP1 shown)

```
       pvdd                              pvdd
        │                                 │
   ┌────┴───────┐                   ┌─────┴──────┐
   │XMc1ivp (P) │                   │XMc1iv2p (P)│
   │ W=2u L=2u  │                   │ W=4u  L=2u │
   │ G=tap1     │                   │ G=c1inv    │
   └────┬───────┘                   └─────┬──────┘
        │                                 │
     c1inv ───────────────────────────── comp1 ──── OUTPUT
        │                                 │
   ┌────┴───────┐                   ┌─────┴──────┐
   │XMc1ivn (N) │                   │XMc1iv2n (N)│
   │ W=2u L=2u  │                   │ W=2u  L=2u │
   │ G=tap1     │                   │ G=c1inv    │
   └────┬───────┘                   └─────┬──────┘
        │                                 │
       gnd                               gnd

   Hysteresis NFET:
   ┌─────────────────────┐
   │ XMhf1 (NFET)        │
   │ W=1.6u  L=100u      │  Very long L → weak pull
   │ G=comp1  S=gnd       │  When comp1=HIGH: pulls c1inv LOW
   │ D=c1inv              │  → raises effective trip point
   └─────────────────────┘

   All 4 comps identical topology, only W(hf) differs:
     COMP1: XMhf1 W=1.6u  (ΔVtrip ≈ 161mV)
     COMP2: XMhf2 W=1.05u (ΔVtrip ≈ 96mV)
     COMP3: XMhf3 W=0.9u  (ΔVtrip ≈ 90mV)
     COMP4: XMhf4 W=0.73u (ΔVtrip ≈ 72mV)
```

### Output Logic

```
   Inverter bank (all P: W=4u/2u, N: W=2u/2u):

     comp1 ──→ INV ──→ comp1b          comp3 ──→ INV ──→ comp3b
     comp2 ──→ INV ──→ comp2b          comp4 ──→ INV ──→ comp4b

   ┌──────────────────────────────────────────────────────────────────────┐
   │                         LOGIC EQUATIONS                              │
   │                                                                      │
   │  pass_off  = INV(comp1)         comp1 direct → buffer               │
   │              → HIGH when BVDD < 2.5V (pass device OFF)              │
   │                                                                      │
   │  bypass_en = INV(                                                    │
   │    NAND(comp1,comp2b) · NAND(comp3,comp4b)                          │
   │  )                                                                   │
   │              → controls bypass mode transition                       │
   │                                                                      │
   │  ea_en     = INV(                                                    │
   │    OR( AND(comp2,comp3b), comp4 )                                    │
   │  )                                                                   │
   │              → HIGH when BVDD > ~4.2V (error amp enabled)           │
   │                                                                      │
   │  ref_sel   = INV( NAND(comp1,comp3b) )                              │
   │              → selects reference source                              │
   │                                                                      │
   │  uvov_en   = INV(INV(comp4)) = comp4                                │
   │              → HIGH when BVDD > 5.6V (UV/OV monitoring active)      │
   │                                                                      │
   │  ilim_en   = INV(INV(comp4)) = comp4                                │
   │              → HIGH when BVDD > 5.6V (current limiter enable)       │
   └──────────────────────────────────────────────────────────────────────┘
```

### pass_off Buffer Detail

```
       pvdd                              pvdd
        │                                 │
   ┌────┴───────┐                   ┌─────┴──────┐
   │XMpo_bufp(P)│                   │             │
   │ W=4u L=2u  │                   │  (unused)   │
   │ G=comp1    │                   │             │
   └────┬───────┘                   └─────────────┘
        │
    pass_off ──────────────── to Block 10 (POR gate pullup)
        │
   ┌────┴───────┐
   │XMpo_bufn(N)│
   │ W=2u L=2u  │
   │ G=comp1    │
   └────┬───────┘
        │
       gnd

   pass_off = INV(comp1)
   BVDD < 2.5V → comp1=LOW → pass_off=HIGH → gate pulled to BVDD
   BVDD > 2.5V → comp1=HIGH → pass_off=LOW → gate free (EA controls)
```

### BVDD Threshold Sequencing

```
   BVDD ──→  0V    2.5V     4.2V    4.5V    5.6V     7V
              │      │        │       │       │        │
   pass_off  │ HIGH  │  LOW   │       │       │        │
              │      │        │       │       │        │
   ea_en     │ LOW   │        │ HIGH  │       │        │
              │      │        │       │       │        │
   ref_sel   │ LOW   │        │       │ HIGH  │        │
              │      │        │       │       │        │
   uvov_en   │ LOW   │        │       │       │ HIGH   │
              │      │        │       │       │        │
   ilim_en   │ LOW   │        │       │       │ HIGH   │
              │      │        │       │       │        │
   bypass_en │ (transition zone)      │       │        │
```

---

## 11. Block 09: Startup Circuit

**Direct gate drive with startup_done detector. Ports: bvdd, pvdd, gate, gnd, vref, startup_done, ea_en, ea_out**

### Gate Drive

```
     ea_out (from EA, BVDD domain)
        │
   ┌────┴──────────┐
   │ Rgate = 1kΩ   │   FIX-27: 1kΩ (reverted from 200Ω)
   │ (discrete R)   │   Damps gate oscillation during startup
   └────┬──────────┘   EA slew = 0.575 V/µs (Cc=40pF) is bottleneck
        │
      gate ──────────────────────── to pass device + current limiter
```

### EA Enable (Always ON)

```
      bvdd
       │
   ┌───┴──────────┐
   │ Ren = 100Ω   │   Low-R pullup → ea_en ≈ bvdd
   └───┬──────────┘   (always HIGH once BVDD present)
       │
     ea_en ─────────────────────── to error amplifier enable
```

### Startup Done Detector

```
       pvdd
        │
   ┌────┴──────────────┐
   │ XR_top              │
   │ res_xhigh_po        │
   │ W=2µm  L=788µm     │
   │ R ≈ 788kΩ          │
   └────┬──────────────┘
        │
     sense_mid = pvdd × 212/(788+212) = pvdd × 0.212
        │
        │         Trip when sense_mid > Vth ≈ 0.7V
        │         → pvdd > 0.7/0.212 = 3.3V
        │
   ┌────┴──────────────┐
   │ XR_bot              │
   │ res_xhigh_po        │
   │ W=2µm  L=212µm     │
   │ R ≈ 212kΩ          │
   └────┬──────────────┘
        │
       gnd

     sense_mid ──────────┐
                          │
                  ┌───────┴───────┐
                  │ XMN_det (NFET)│
                  │ W=4u  L=1u    │
                  │ G=sense_mid   │
                  │ S=gnd  D=det_n│
                  └───────┬───────┘
                          │
      bvdd ─── XR_pu ─── det_n
               W=1 L=2000          When pvdd < 3.3V:
               R ≈ 4MΩ             sense_mid < Vth → XMN_det OFF
               (pullup)            → det_n pulled HIGH by XR_pu
                  │                 → startup_done = LOW
                  │
          ┌───────┴───────┐        When pvdd > 3.3V:
          │               │        sense_mid > Vth → XMN_det ON
     ┌────┴────┐    ┌─────┴────┐   → det_n pulled LOW
     │XMP_inv1 │    │XMN_inv1  │   → startup_done = HIGH
     │(PFET)   │    │(NFET)    │
     │W=4u L=1u│    │W=2u L=1u │
     │G=det_n  │    │G=det_n   │
     └────┬────┘    └─────┬────┘
          │               │
      startup_done ───────┘ ──── OUTPUT
          │
      (bvdd/gnd)
```

---

## 12. Block 10: Top-Level Wiring

**Complete interconnect of all blocks within pvdd_regulator subcircuit.**

### Signal Flow Diagram

```
  ═══════════════════════════════════════════════════════════════════════════
                              SIGNAL FLOW
  ═══════════════════════════════════════════════════════════════════════════

     avbg ─── XRss(100kΩ) ───┬─── vref_ss ─── EA(+)
     (1.226V bandgap)         │
                           Css=22nF
                              │
                             gnd

     EA(−) ←── vfb ←── FEEDBACK(pvdd) ←── PVDD
                │
             Cff=22pF ←── PVDD  (feedforward, FIX-25)

     EA(out) = ea_out ─── Rgate(1kΩ) ─── gate
                                           │
                               ┌───────────┼───────────┐
                               │           │           │
                          PASS_DEVICE  CURR_LIMITER  POR_PULLUP
                          (S=bvdd      (sense mirror)  (pass_off)
                           D=pvdd)

     PVDD ──┬── FEEDBACK ── vfb
            ├── UV_COMP ── uv_flag
            ├── OV_COMP ── ov_flag
            ├── MOS_CLAMP (overvoltage)
            ├── Cload (200pF)
            └── Cout_ext (1µF)

     MODE_CTRL(bvdd) ──→ pass_off ──→ POR gate pullup
                     ──→ mc_ea_en  (unused, ea_en from BVDD pullup)
                     ──→ uvov_en   ──→ UV/OV comparators
                     ──→ bypass_en, ref_sel, ilim_en (routed to ports)

     LEVEL_SHIFT_UP: en(svdd) → en_bvdd (for enable gating)
```

### Top-Level Wiring — Detailed Netlist View

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  pvdd_regulator                                                             │
  │  Ports: bvdd pvdd gnd avbg ibias svdd en en_ret uv_flag ov_flag            │
  │         startup_done                                                        │
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────┐        │
  │  │                    SUPPLY RAILS                                 │        │
  │  │                                                                 │        │
  │  │  bvdd ───── 5.4V to 10.5V input supply                        │        │
  │  │  pvdd ───── 5.0V regulated output                              │        │
  │  │  svdd ───── 2.2V (for UV/OV comparators)                      │        │
  │  │  gnd  ───── ground reference                                   │        │
  │  └─────────────────────────────────────────────────────────────────┘        │
  │                                                                             │
  │  ═══════════════ INSTANTIATIONS ═══════════════                            │
  │                                                                             │
  │  XM_pass:  pass_device                                                      │
  │    .gate    = gate                                                          │
  │    .bvdd    = bvdd                                                          │
  │    .pvdd    = pvdd                                                          │
  │                                                                             │
  │  XRss:  res_xhigh_po W=2 L=100 (R≈100kΩ)                                 │
  │    avbg ──→ vref_ss                                                        │
  │  Css:  22nF                                                                │
  │    vref_ss ──→ gnd                                                         │
  │                                                                             │
  │  XEA:  error_amp                                                            │
  │    .vref      = vref_ss                                                     │
  │    .vfb       = vfb                                                         │
  │    .vout_gate = ea_out                                                      │
  │    .gnd       = gnd                                                         │
  │    .ibias     = ibias                                                       │
  │    .en        = ea_en                                                       │
  │    .bvdd      = bvdd                                                        │
  │                                                                             │
  │  XFB:  feedback_network                                                     │
  │    .pvdd = pvdd                                                             │
  │    .vfb  = vfb                                                              │
  │    .gnd  = gnd                                                              │
  │  Cff:  22pF  pvdd ──→ vfb  (feedforward zero, FIX-25)                     │
  │                                                                             │
  │  XCOMP: compensation  (empty placeholder)                                  │
  │    .vout_gate = ea_out                                                      │
  │    .pvdd      = pvdd                                                        │
  │    .gnd       = gnd                                                         │
  │                                                                             │
  │  Iibias_ilim: 1µA current source  (0 → ibias_ilim)                        │
  │  XILIM: current_limiter                                                     │
  │    .gate      = gate                                                        │
  │    .bvdd      = bvdd                                                        │
  │    .pvdd      = pvdd                                                        │
  │    .gnd       = gnd                                                         │
  │    .ilim_flag = ilim_flag                                                   │
  │    .ibias     = ibias_ilim                                                  │
  │                                                                             │
  │  XUV:  uv_comparator                                                        │
  │    .pvdd     = pvdd                                                         │
  │    .vref     = avbg                                                         │
  │    .uv_flag  = uv_flag                                                      │
  │    .vdd_comp = svdd                                                         │
  │    .gnd      = gnd                                                          │
  │    .en       = uvov_en                                                      │
  │                                                                             │
  │  XOV:  ov_comparator                                                        │
  │    .pvdd     = pvdd                                                         │
  │    .vref     = avbg                                                         │
  │    .ov_flag  = ov_flag                                                      │
  │    .vdd_comp = svdd                                                         │
  │    .gnd      = gnd                                                          │
  │    .en       = uvov_en                                                      │
  │                                                                             │
  │  XZC:  zener_clamp  (MOS voltage clamp)                                    │
  │    .pvdd  = pvdd                                                            │
  │    .gnd   = gnd                                                             │
  │    .ibias = ibias                                                           │
  │                                                                             │
  │  XMC:  mode_control                                                         │
  │    .bvdd      = bvdd                                                        │
  │    .pvdd      = pvdd                                                        │
  │    .svdd      = svdd                                                        │
  │    .gnd       = gnd                                                         │
  │    .en_ret    = en_ret                                                      │
  │    .bypass_en = bypass_en                                                   │
  │    .ea_en     = mc_ea_en   (NOT used — ea_en from BVDD pullup)             │
  │    .ref_sel   = ref_sel                                                     │
  │    .uvov_en   = uvov_en                                                     │
  │    .ilim_en   = ilim_en                                                     │
  │    .pass_off  = pass_off                                                    │
  │                                                                             │
  │  XSU:  startup                                                              │
  │    .bvdd         = bvdd                                                     │
  │    .pvdd         = pvdd                                                     │
  │    .gate         = gate                                                     │
  │    .gnd          = gnd                                                      │
  │    .vref         = avbg                                                     │
  │    .startup_done = startup_done                                             │
  │    .ea_en        = su_ea_en  (internal, not used for actual ea_en)         │
  │    .ea_out       = ea_out                                                   │
  │                                                                             │
  │  ═══════════════ DISCRETE COMPONENTS ═══════════════                       │
  │                                                                             │
  │  Ren_ea:  100Ω  bvdd → ea_en  (always-ON enable)                          │
  │                                                                             │
  │  POR Gate Pullup:                                                           │
  │    XMpo_invp (PFET) W=40u L=2u  pass_off → pass_off_b (inverter)          │
  │    XMpo_invn (NFET) W=2u  L=2u                                            │
  │    XMgate_pu (PFET) W=4u  L=2u  pass_off_b → gate pullup to bvdd         │
  │                                                                             │
  │  Level Shifter:                                                             │
  │    XLS_EN: level_shifter_up  en(svdd) → en_bvdd                           │
  │                                                                             │
  │  Output Caps:                                                               │
  │    Cload:    200pF  pvdd → gnd  (on-chip)                                 │
  │    Cout_ext: 1µF    pvdd → gnd  (EXTERNAL — load transient filter)        │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘
```

### Critical Nets Summary

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │  NET           │ DRIVEN BY            │ LOADS                       │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  gate          │ Rgate (from ea_out)  │ XM_pass (10×PMOS)          │
  │                │ + POR pullup         │ XILIM sense FET            │
  │                │ + XILIM clamp FETs   │ XMgate_pu                  │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  ea_out        │ XEA.vout_gate        │ Rgate, XCOMP               │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  vfb           │ XFB divider mid      │ XEA(−), Cff                │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  vref_ss       │ XRss + Css           │ XEA(+)                     │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  pvdd          │ XM_pass drain        │ XFB, XUV, XOV, XZC, XMC   │
  │                │                      │ Cload, Cout_ext, Cff       │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  ea_en         │ Ren_ea (bvdd, 100Ω) │ XEA.en                     │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  pass_off      │ XMC.pass_off         │ POR inverter               │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  pass_off_b    │ POR inverter         │ XMgate_pu gate             │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  uvov_en       │ XMC.uvov_en          │ XUV.en, XOV.en            │
  ├────────────────┼──────────────────────┼────────────────────────────┤
  │  ibias_ilim    │ Iibias_ilim (1µA)    │ XILIM.ibias               │
  └─────────────────────────────────────────────────────────────────────┘
```

### POR Gate Pullup Detail

```
       bvdd                          bvdd
        │                             │ (S,B)
        │                      ┌──────┴───────┐
        │                      │XMgate_pu (P)  │
        │                      │ W=4u  L=2u    │
        │                      │ G=pass_off_b  │
        │                      └──────┬───────┘
        │                             │
        │                           gate ─── (pulls to bvdd during POR)
        │
   ┌────┴───────┐
   │XMpo_invp(P)│          pass_off ──→ [INV] ──→ pass_off_b
   │W=40u  L=2u │                │              │
   │G=pass_off  │         ┌──────┴──────┐ ┌─────┴──────┐
   └────┬───────┘         │XMpo_invp(P) │ │            │
        │                 │W=40u L=2u   │ │XMpo_invn(N)│
    pass_off_b            └──────┬──────┘ │W=2u  L=2u  │
        │                       │         └─────┬──────┘
   ┌────┴───────┐          pass_off_b           │
   │XMpo_invn(N)│               │              gnd
   │W=2u   L=2u │               │
   │G=pass_off  │         During POR (BVDD < 2.5V):
   └────┬───────┘           pass_off = HIGH
        │                   pass_off_b = LOW
       gnd                  XMgate_pu ON → gate = BVDD → pass OFF

                          Normal operation (BVDD > 2.5V):
                            pass_off = LOW
                            pass_off_b = HIGH
                            XMgate_pu OFF → gate free (EA controls)
```

---

## Device Summary Table

```
  ┌────────────────┬──────────────────────────────────────────────────────────┐
  │ BLOCK          │ KEY DEVICES                                              │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 00 Error Amp   │ Diff pair: PFET W=80u/4u m=2                            │
  │                │ Mirror:    NFET W=20u/8u m=2                             │
  │                │ CS stage:  NFET W=20u/2u + PFET W=20u/4u m=2            │
  │                │ Miller:    Cc=40pF, Rc=5kΩ                              │
  │                │ Tail:      PFET W=20u/4u m=4 (~40µA)                    │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 01 Pass Device │ 10× PFET W=50u/0.5u m=2, Total Weff=1mm                │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 02 Feedback    │ R_TOP: xhigh_po W=3/L=536 (364kΩ)                      │
  │                │ R_BOT: xhigh_po W=3/L=174.3 (118kΩ)                    │
  │                │ Cff=22pF (in Block 10)                                   │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 03 Comp        │ Empty (all comp in EA + Block 10)                        │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 04 Curr Limit  │ Sense: PFET W=1u/0.5u (1/1000 mirror)                  │
  │                │ Cascode: PFET W=10u/0.5u                                │
  │                │ Ref mirror: NFET W=100u/8u (50:1)                       │
  │                │ 4× Clamp: PFET W=50u/0.5u each                         │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 05 UV/OV       │ Diff pair: NFET W=2u/1u (nfet_01v8)                    │
  │                │ Mirror: PFET W=2u/1u (pfet_01v8)                        │
  │                │ NOR output: P W=4u/0.15u, N W=1u/0.15u                 │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 06 Lvl Shift   │ UP:   Cross PFET W=4u,5u/0.5u, Pull NFET W=15u/1u    │
  │                │ DOWN: Cross PFET W=4u/0.5u, Pull NFET W=2u/1u         │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 07 MOS Clamp   │ Prec stack: N(2.2u/4u), P(20u/4u) × 4                 │
  │                │ Rstack: 190kΩ, Rpd: 500kΩ                              │
  │                │ Fast stack: 7× NFET W=10u/0.5u                          │
  │                │ Clamp: NFET W=50u/0.5u m=4                              │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 08 Mode Ctrl   │ Ladder: 5× xhigh_po (382kΩ total)                      │
  │                │ 4× Schmitt comps: PFET/NFET W=2u/2u + hyst NFET       │
  │                │ Logic: all W=4u/2u (P), W=2u/2u (N)                    │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 09 Startup     │ Rgate=1kΩ, Ren=100Ω                                    │
  │                │ Detector: R divider 788kΩ/212kΩ, NFET W=4u/1u         │
  │                │ Inverter: PFET W=4u/1u, NFET W=2u/1u                   │
  ├────────────────┼──────────────────────────────────────────────────────────┤
  │ 10 Top Wiring  │ XRss: 100kΩ, Css: 22nF (ext), Cload: 200pF            │
  │                │ Cout_ext: 1µF (ext), Cff: 22pF                         │
  │                │ POR inv: PFET W=40u/2u, NFET W=2u/2u                   │
  │                │ Pullup: PFET W=4u/2u, Ren_ea: 100Ω                     │
  │                │ Iibias_ilim: 1µA current source                         │
  └────────────────┴──────────────────────────────────────────────────────────┘

  PDK: SkyWater SKY130A
  HV devices: sky130_fd_pr__pfet_g5v0d10v5, sky130_fd_pr__nfet_g5v0d10v5
  LV devices: sky130_fd_pr__pfet_01v8, sky130_fd_pr__nfet_01v8 (UV/OV only)
  Resistors:  sky130_fd_pr__res_xhigh_po (~2kΩ/sq)
```

---

*Generated from design.cir files — Blocks 00 through 10*
*PVDD 5V LDO Regulator, SkyWater SKY130A*
