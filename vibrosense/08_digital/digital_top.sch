v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -200 -880 0 -880 {lab=sck}
N -200 -840 0 -840 {lab=mosi}
N -200 -800 0 -800 {lab=cs_n}
N -200 -640 0 -640 {lab=clk}
N -200 -600 0 -600 {lab=rst_n}
N -200 -560 0 -560 {lab=adc_data_in[7:0]}
N -200 -520 0 -520 {lab=adc_done}
N -200 -700 0 -700 {lab=class_result[3:0]}
N -200 -660 0 -660 {lab=class_valid}
N 0 -760 -200 -760 {lab=miso_data}
N 0 -720 -200 -720 {lab=miso_oe_n}
N 1450 -880 1650 -880 {lab=fsm_sample}
N 1450 -850 1650 -850 {lab=fsm_evaluate}
N 1450 -820 1650 -820 {lab=fsm_compare}
N 1450 -650 1650 -650 {lab=irq_n}
N 1450 -440 1650 -440 {lab=clk_div2}
N 1450 -420 1650 -420 {lab=clk_div4}
N 1450 -400 1650 -400 {lab=clk_div8}
N 1450 -380 1650 -380 {lab=clk_div16}
N 350 -860 550 -860 {lab=spi_wr_en}
N 350 -830 550 -830 {lab=spi_wr_addr[6:0]}
N 350 -800 550 -800 {lab=spi_wr_data[7:0]}
N 350 -770 550 -770 {lab=spi_status_rd}
N 550 -740 350 -740 {lab=shadow_data_bus[127:0]}
N 350 -710 550 -710 {lab=snapshot_req}
N 900 -600 1100 -860 {lab=fsm_enable}
N 1275 -730 1275 -680 {lab=fsm_done}
N 900 -630 1100 -630 {lab=rf_debounce_val[3:0]}
N 900 -660 1100 -660 {lab=rf_debounce_wr}
N 0 -700 -20 -700 {lab=class_result[3:0]}
N 0 -700 0 -650 {lab=class_result[3:0]}
N 0 -650 1100 -650 {lab=class_result[3:0]}
N 0 -560 550 -560 {lab=adc_data_in[7:0]}
N 0 -520 550 -520 {lab=adc_done}
T {VibroSense Block 08: Digital Control} -200 -1100 0 0 1.0 1.0 {layer=15}
T {SPI slave + 16-reg file + classifier FSM + debounce/IRQ + clk divider  |  SKY130 sky130_fd_sc_hd} -200 -1040 0 0 0.5 0.5 {layer=15}
T {744 cells  |  10,259 um^2  |  ~1.6 uW @ 1 MHz  |  28/28 tests PASS} -200 -990 0 0 0.4 0.4 {layer=15}
B 4 0 -900 350 -520 {}
T {spi_slave} 139 -885 0 0 0.4 0.4 {layer=4}
T {SPI Mode 0} 10 -860 0 0 0.25 0.25 {layer=8}
T {Toggle CDC} 10 -835 0 0 0.25 0.25 {layer=8}
T {Shadow Registers} 10 -810 0 0 0.25 0.25 {layer=8}
T {Split MISO} 10 -785 0 0 0.25 0.25 {layer=8}
B 4 550 -900 900 -520 {}
T {reg_file} 693 -885 0 0 0.4 0.4 {layer=4}
T {16 x 8-bit regs} 560 -860 0 0 0.25 0.25 {layer=8}
T {0x00-0x0F} 560 -835 0 0 0.25 0.25 {layer=8}
T {CTRL[0]=FSM_EN} 560 -810 0 0 0.25 0.25 {layer=8}
T {Shadow data bus} 560 -785 0 0 0.25 0.25 {layer=8}
B 4 1100 -900 1450 -730 {}
T {fsm_classifier} 1219 -885 0 0 0.4 0.4 {layer=4}
T {Counter FSM} 1110 -860 0 0 0.25 0.25 {layer=8}
T {S/E/C/W phases} 1110 -835 0 0 0.25 0.25 {layer=8}
B 4 1100 -680 1450 -510 {}
T {debounce} 1243 -665 0 0 0.4 0.4 {layer=4}
T {Consecutive-match} 1110 -640 0 0 0.25 0.25 {layer=8}
T {IRQ generation} 1110 -615 0 0 0.25 0.25 {layer=8}
B 4 1100 -460 1450 -340 {}
T {clk_divider} 1231 -445 0 0 0.4 0.4 {layer=4}
T {/2, /4, /8, /16} 1110 -420 0 0 0.25 0.25 {layer=8}
T {(clock enables)} 1110 -395 0 0 0.25 0.25 {layer=8}
C {devices/iopin.sym} -200 -880 0 1 {name=p1 lab=sck}
C {devices/iopin.sym} -200 -840 0 1 {name=p2 lab=mosi}
C {devices/iopin.sym} -200 -800 0 1 {name=p3 lab=cs_n}
C {devices/iopin.sym} -200 -640 0 1 {name=p4 lab=clk}
C {devices/iopin.sym} -200 -600 0 1 {name=p5 lab=rst_n}
C {devices/iopin.sym} -200 -560 0 1 {name=p6 lab=adc_data_in[7:0]}
C {devices/iopin.sym} -200 -520 0 1 {name=p7 lab=adc_done}
C {devices/iopin.sym} -200 -700 0 1 {name=p8 lab=class_result[3:0]}
C {devices/iopin.sym} -200 -660 0 1 {name=p9 lab=class_valid}
C {devices/iopin.sym} -200 -760 0 0 {name=p10 lab=miso_data}
C {devices/iopin.sym} -200 -720 0 0 {name=p11 lab=miso_oe_n}
C {devices/iopin.sym} 1650 -880 0 0 {name=p12 lab=fsm_sample}
C {devices/iopin.sym} 1650 -850 0 0 {name=p13 lab=fsm_evaluate}
C {devices/iopin.sym} 1650 -820 0 0 {name=p14 lab=fsm_compare}
C {devices/iopin.sym} 1650 -650 0 0 {name=p15 lab=irq_n}
C {devices/iopin.sym} 1650 -440 0 0 {name=p16 lab=clk_div2}
C {devices/iopin.sym} 1650 -420 0 0 {name=p17 lab=clk_div4}
C {devices/iopin.sym} 1650 -400 0 0 {name=p18 lab=clk_div8}
C {devices/iopin.sym} 1650 -380 0 0 {name=p19 lab=clk_div16}
C {devices/lab_pin.sym} 900 -870 0 0 {name=p20 lab=gain[1:0]}
C {devices/lab_pin.sym} 900 -850 0 0 {name=p21 lab=tune1[3:0]}
C {devices/lab_pin.sym} 900 -830 0 0 {name=p22 lab=tune2[3:0]}
C {devices/lab_pin.sym} 900 -810 0 0 {name=p23 lab=tune3[3:0]}
C {devices/lab_pin.sym} 900 -790 0 0 {name=p24 lab=tune4[3:0]}
C {devices/lab_pin.sym} 900 -770 0 0 {name=p25 lab=tune5[3:0]}
C {devices/lab_pin.sym} 900 -750 0 0 {name=p26 lab=weights[31:0]}
C {devices/lab_pin.sym} 900 -730 0 0 {name=p27 lab=thresh[7:0]}
C {devices/lab_pin.sym} 900 -710 0 0 {name=p28 lab=debounce_val[3:0]}
C {devices/lab_pin.sym} 900 -690 0 0 {name=p29 lab=adc_chan[1:0]}
C {devices/lab_pin.sym} 900 -670 0 0 {name=p30 lab=adc_start}
C {devices/iopin.sym} 1650 -890 0 0 {name=p31 lab=gain[1:0]}
C {devices/lab_pin.sym} 1620 -890 0 1 {name=p32 lab=gain[1:0]}
C {devices/iopin.sym} 1650 -870 0 0 {name=p33 lab=tune1[3:0]}
C {devices/lab_pin.sym} 1620 -870 0 1 {name=p34 lab=tune1[3:0]}
C {devices/iopin.sym} 1650 -850 0 0 {name=p35 lab=tune2[3:0]}
C {devices/lab_pin.sym} 1620 -850 0 1 {name=p36 lab=tune2[3:0]}
C {devices/iopin.sym} 1650 -830 0 0 {name=p37 lab=tune3[3:0]}
C {devices/lab_pin.sym} 1620 -830 0 1 {name=p38 lab=tune3[3:0]}
C {devices/iopin.sym} 1650 -810 0 0 {name=p39 lab=tune4[3:0]}
C {devices/lab_pin.sym} 1620 -810 0 1 {name=p40 lab=tune4[3:0]}
C {devices/iopin.sym} 1650 -790 0 0 {name=p41 lab=tune5[3:0]}
C {devices/lab_pin.sym} 1620 -790 0 1 {name=p42 lab=tune5[3:0]}
C {devices/iopin.sym} 1650 -770 0 0 {name=p43 lab=weights[31:0]}
C {devices/lab_pin.sym} 1620 -770 0 1 {name=p44 lab=weights[31:0]}
C {devices/iopin.sym} 1650 -750 0 0 {name=p45 lab=thresh[7:0]}
C {devices/lab_pin.sym} 1620 -750 0 1 {name=p46 lab=thresh[7:0]}
C {devices/iopin.sym} 1650 -730 0 0 {name=p47 lab=debounce_val[3:0]}
C {devices/lab_pin.sym} 1620 -730 0 1 {name=p48 lab=debounce_val[3:0]}
C {devices/iopin.sym} 1650 -710 0 0 {name=p49 lab=adc_chan[1:0]}
C {devices/lab_pin.sym} 1620 -710 0 1 {name=p50 lab=adc_chan[1:0]}
C {devices/iopin.sym} 1650 -690 0 0 {name=p51 lab=adc_start}
C {devices/lab_pin.sym} 1620 -690 0 1 {name=p52 lab=adc_start}
C {devices/lab_pin.sym} 450 -865 0 0 {name=p53 lab=spi_wr_en}
C {devices/lab_pin.sym} 450 -835 0 0 {name=p54 lab=spi_wr_addr[6:0]}
C {devices/lab_pin.sym} 450 -805 0 0 {name=p55 lab=spi_wr_data[7:0]}
C {devices/lab_pin.sym} 450 -775 0 0 {name=p56 lab=spi_status_rd}
C {devices/lab_pin.sym} 450 -735 0 0 {name=p57 lab=shadow_data_bus[127:0]}
C {devices/lab_pin.sym} 450 -705 0 0 {name=p58 lab=snapshot_req}
C {devices/lab_pin.sym} 950 -600 0 0 {name=p59 lab=fsm_enable}
C {devices/lab_pin.sym} 1280 -705 0 0 {name=p60 lab=fsm_done}
C {devices/lab_pin.sym} 1000 -625 0 0 {name=p61 lab=rf_debounce_val[3:0]}
C {devices/lab_pin.sym} 1000 -655 0 0 {name=p62 lab=rf_debounce_wr}
C {devices/lab_pin.sym} 200 -645 0 0 {name=p63 lab=class_result[3:0]}
C {devices/lab_pin.sym} 5 -540 0 1 {name=p64 lab=clk}
C {devices/lab_pin.sym} 5 -525 0 1 {name=p65 lab=rst_n}
C {devices/lab_pin.sym} 555 -540 0 1 {name=p66 lab=clk}
C {devices/lab_pin.sym} 555 -525 0 1 {name=p67 lab=rst_n}
C {devices/lab_pin.sym} 1105 -750 0 1 {name=p68 lab=clk}
C {devices/lab_pin.sym} 1105 -735 0 1 {name=p69 lab=rst_n}
C {devices/lab_pin.sym} 1105 -530 0 1 {name=p70 lab=clk}
C {devices/lab_pin.sym} 1105 -515 0 1 {name=p71 lab=rst_n}
C {devices/lab_pin.sym} 1105 -360 0 1 {name=p72 lab=clk}
C {devices/lab_pin.sym} 1105 -345 0 1 {name=p73 lab=rst_n}
