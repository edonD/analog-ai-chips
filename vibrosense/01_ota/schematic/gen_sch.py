#!/usr/bin/env python3
"""Generate xschem schematic for folded-cascode OTA from netlist specification."""

PDK = "/home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A"
NFET_SYM = f"{PDK}/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym"
PFET_SYM = f"{PDK}/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym"

# Pin offsets for rot=0 flip=0
# NFET: D=(+20,-30) G=(-20,0) S=(+20,+30) B=(+20,0)
# PFET: D=(+20,+30) G=(-20,0) S=(+20,-30) B=(+20,0)

# For flip=1: negate x offsets
# NFET flip=1: D=(-20,-30) G=(+20,0) S=(-20,+30) B=(-20,0)

def nfet_pins(cx, cy, flip=0):
    sx = -1 if flip else 1
    return {
        'D': (cx + sx*20, cy - 30),
        'G': (cx - sx*20, cy),
        'S': (cx + sx*20, cy + 30),
        'B': (cx + sx*20, cy),
    }

def pfet_pins(cx, cy, flip=0):
    sx = -1 if flip else 1
    return {
        'D': (cx + sx*20, cy + 30),
        'G': (cx - sx*20, cy),
        'S': (cx + sx*20, cy - 30),
        'B': (cx + sx*20, cy),
    }

# Transistor definitions: name, type, x, y, flip, W, L, nets(D,G,S,B)
devices = [
    # PMOS loads - top row
    ('M3',  'pfet', -600, -1400, 0, '6u',    '14u', 'fold_p', 'vbp',  'vdd',    'vdd'),
    ('M12', 'pfet', -350, -1400, 0, '0.42u', '20u', 'fold_p', 'vbp',  'vdd',    'vdd'),
    ('M4',  'pfet',  350, -1400, 0, '6u',    '14u', 'fold_n', 'vbp',  'vdd',    'vdd'),
    ('M13', 'pfet',  550, -1400, 0, '0.42u', '20u', 'fold_n', 'vbp',  'vdd',    'vdd'),

    # PMOS cascodes
    ('M5',  'pfet', -500, -1000, 0, '0.42u', '2u',  'cas_p',  'vbcp', 'fold_p', 'vdd'),
    ('M6',  'pfet',  500, -1000, 0, '0.42u', '2u',  'vout',   'vbcp', 'fold_n', 'vdd'),

    # NMOS cascodes
    ('M7',  'nfet', -500, -600, 0, '0.36u', '1u',  'cas_p', 'vbcn', 'src7', 'vss'),
    ('M8',  'nfet',  500, -600, 0, '0.36u', '1u',  'vout',  'vbcn', 'src8', 'vss'),

    # NMOS current sources
    ('M9',  'nfet', -500, -200, 0, '6u',   '11u', 'src7', 'vbn', 'vss', 'vss'),
    ('M10', 'nfet',  500, -200, 0, '6u',   '11u', 'src8', 'vbn', 'vss', 'vss'),

    # Input differential pair
    ('M1',  'nfet', -150, -800, 1, '5u',   '14u', 'fold_p', 'vinp', 'tail', 'vss'),
    ('M2',  'nfet',  150, -800, 0, '5u',   '14u', 'fold_n', 'vinn', 'tail', 'vss'),

    # Tail current source
    ('M11', 'nfet',    0, -400, 0, '3.8u', '4u',  'tail',   'vbn',  'vss',  'vss'),
]

# I/O port pin locations (for iopin symbols)
ports = {
    'vinp':  (-300, -800),
    'vinn':  ( 300, -800),
    'vout':  ( 750, -800),
    'vdd':   (   0, -1650),
    'vss':   (   0,   100),
    'vbn':   (-800, -300),
    'vbcn':  (-800, -600),
    'vbp':   (-800, -1400),
    'vbcp':  (-800, -1000),
}

lines = []
wires = []
pin_counter = [0]

def next_pin():
    pin_counter[0] += 1
    return pin_counter[0]

def add_component(sym, cx, cy, rot, flip, attrs):
    lines.append(f'C {{{sym}}} {cx} {cy} {rot} {flip} {{{attrs}}}')

def add_wire(x1, y1, x2, y2, lab):
    wires.append(f'N {x1} {y1} {x2} {y2} {{lab={lab}}}')

def add_lab_pin(x, y, rot, flip, lab):
    n = next_pin()
    lines.append(f'C {{devices/lab_pin.sym}} {x} {y} {rot} {flip} {{name=p{n} lab={lab}}}')

def add_iopin(x, y, rot, flip, lab):
    n = next_pin()
    lines.append(f'C {{devices/iopin.sym}} {x} {y} {rot} {flip} {{name=p{n} lab={lab}}}')

def build():
    # Header
    header = """v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}"""

    # Title
    lines.append('T {VibroSense Folded-Cascode OTA} -800 -1800 0 0 0.6 0.6 {}')
    lines.append('T {SKY130A - 13 Transistors} -800 -1750 0 0 0.35 0.35 {layer=8}')

    # Place transistors
    for name, typ, cx, cy, flip, W, L, d_net, g_net, s_net, b_net in devices:
        sym = NFET_SYM if typ == 'nfet' else PFET_SYM
        model = 'nfet_01v8' if typ == 'nfet' else 'pfet_01v8'
        attrs = f'name={name} L={L} W={W} nf=1 mult=1 model={model} spiceprefix=X'
        add_component(sym, cx, cy, 0, flip, attrs)

        # Get pin positions
        if typ == 'nfet':
            pins = nfet_pins(cx, cy, flip)
        else:
            pins = pfet_pins(cx, cy, flip)

        # Connect each pin with a short wire + lab_pin
        # Drain
        dx, dy = pins['D']
        if typ == 'nfet':
            # Drain at top, extend upward
            add_wire(dx, dy, dx, dy - 30, d_net)
            add_lab_pin(dx, dy - 30, 1, 0, d_net)  # rot=1 for upward
        else:
            # Drain at bottom, extend downward
            add_wire(dx, dy, dx, dy + 30, d_net)
            add_lab_pin(dx, dy + 30, 3, 0, d_net)  # rot=3 for downward

        # Gate
        gx, gy = pins['G']
        if flip:
            # Gate on right side
            add_wire(gx, gy, gx + 40, gy, g_net)
            add_lab_pin(gx + 40, gy, 0, 0, g_net)  # text to left
        else:
            # Gate on left side
            add_wire(gx, gy, gx - 40, gy, g_net)
            add_lab_pin(gx - 40, gy, 0, 1, g_net)  # rot=0 flip=1: text to right

        # Source
        sx, sy = pins['S']
        if typ == 'nfet':
            # Source at bottom, extend downward
            add_wire(sx, sy, sx, sy + 30, s_net)
            add_lab_pin(sx, sy + 30, 3, 0, s_net)
        else:
            # Source at top, extend upward
            add_wire(sx, sy, sx, sy - 30, s_net)
            add_lab_pin(sx, sy - 30, 1, 0, s_net)

        # Body
        bx, by = pins['B']
        if flip:
            add_wire(bx, by, bx - 20, by, b_net)
            add_lab_pin(bx - 20, by, 0, 1, b_net)
        else:
            add_wire(bx, by, bx + 20, by, b_net)
            add_lab_pin(bx + 20, by, 0, 0, b_net)

    # Also add direct wire connections for key paths where transistors stack vertically

    # Left branch: M3/M12 drain (fold_p) → M5 source (fold_p)
    # M3 drain (PFET): (-600+20, -1400+30) = (-580, -1370)
    # M12 drain (PFET): (-350+20, -1400+30) = (-330, -1370)
    # M5 source (PFET): (-500+20, -1000-30) = (-480, -1030)
    # Connect via fold_p bus
    add_wire(-580, -1370, -580, -1200, 'fold_p')
    add_wire(-330, -1370, -330, -1200, 'fold_p')
    add_wire(-580, -1200, -330, -1200, 'fold_p')
    add_wire(-480, -1200, -480, -1030, 'fold_p')

    # Right branch: M4/M13 drain (fold_n) → M6 source (fold_n)
    add_wire(370, -1370, 370, -1200, 'fold_n')
    add_wire(570, -1370, 570, -1200, 'fold_n')
    add_wire(370, -1200, 570, -1200, 'fold_n')
    add_wire(520, -1200, 520, -1030, 'fold_n')

    # Left: M5 drain (cas_p) → M7 drain (cas_p)
    # M5 drain (PFET): (-500+20, -1000+30) = (-480, -970)
    # M7 drain (NFET): (-500+20, -600-30) = (-480, -630)
    add_wire(-480, -970, -480, -630, 'cas_p')

    # Right: M6 drain (vout) → M8 drain (vout)
    add_wire(520, -970, 520, -630, 'vout')

    # Left: M7 source (src7) → M9 drain (src7)
    # M7 source: (-480, -570)
    # M9 drain: (-480, -230)
    add_wire(-480, -570, -480, -230, 'src7')

    # Right: M8 source (src8) → M10 drain (src8)
    add_wire(520, -570, 520, -230, 'src8')

    # Input pair tail connection
    # M1 source (flip=1): (-150-20, -800+30) = (-170, -770)
    # M2 source (flip=0): (150+20, -800+30) = (170, -770)
    # M11 drain: (0+20, -400-30) = (20, -430)
    add_wire(-170, -770, -170, -500, 'tail')
    add_wire(170, -770, 170, -500, 'tail')
    add_wire(-170, -500, 170, -500, 'tail')
    add_wire(20, -500, 20, -430, 'tail')

    # M1 drain (fold_p) connection: (-170, -830) -- extend up
    add_wire(-170, -830, -170, -860, 'fold_p')
    # M2 drain (fold_n): (170, -830) -- extend up
    add_wire(170, -830, 170, -860, 'fold_n')

    # VDD rail
    add_wire(-700, -1600, 700, -1600, 'vdd')
    # M3 source to VDD: (-580, -1430)
    add_wire(-580, -1430, -580, -1600, 'vdd')
    # M12 source to VDD: (-330, -1430)
    add_wire(-330, -1430, -330, -1600, 'vdd')
    # M4 source to VDD: (370, -1430)
    add_wire(370, -1430, 370, -1600, 'vdd')
    # M13 source to VDD: (570, -1430)
    add_wire(570, -1430, 570, -1600, 'vdd')

    # VSS rail
    add_wire(-700, 50, 700, 50, 'vss')
    # M9 source to VSS: (-480, -170)
    add_wire(-480, -170, -480, 50, 'vss')
    # M10 source to VSS: (520, -170)
    add_wire(520, -170, 520, 50, 'vss')
    # M11 source to VSS: (20, -370)
    add_wire(20, -370, 20, 50, 'vss')

    # Output label on right side
    add_wire(520, -800, 700, -800, 'vout')
    add_lab_pin(700, -800, 0, 0, 'vout')

    # I/O port pins
    for port_name, (px, py) in ports.items():
        if port_name == 'vout':
            add_iopin(750, -800, 0, 0, port_name)
        elif port_name == 'vdd':
            add_iopin(0, -1650, 3, 0, port_name)
        elif port_name == 'vss':
            add_iopin(0, 100, 1, 0, port_name)
        elif port_name in ('vinp', 'vinn'):
            add_iopin(px, py, 2, 0, port_name)
        else:
            # Bias pins on left
            add_iopin(px, py, 2, 0, port_name)

    # Connect iopin to net via wires
    add_wire(0, -1650, 0, -1600, 'vdd')
    add_wire(0, 100, 0, 50, 'vss')
    add_wire(-300, -800, -190, -800, 'vinp')  # to M1 gate
    add_wire(300, -800, 190, -800, 'vinn')    # to M2 gate

    # Bias iopins to nets
    add_wire(-800, -300, -560, -300, 'vbn')
    add_wire(-560, -300, -560, -200, 'vbn')
    add_wire(-800, -600, -540, -600, 'vbcn')
    add_wire(-800, -1400, -640, -1400, 'vbp')
    add_wire(-800, -1000, -540, -1000, 'vbcp')

    # Assemble
    output = header + '\n'
    for w in wires:
        output += w + '\n'
    for l in lines:
        output += l + '\n'
    return output

sch = build()
with open('ota_foldcasc.sch', 'w') as f:
    f.write(sch)
print(f"Generated ota_foldcasc.sch ({len(sch)} bytes, {len(lines)} components, {len(wires)} wires)")
