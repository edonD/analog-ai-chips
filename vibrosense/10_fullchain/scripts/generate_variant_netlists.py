#!/usr/bin/env python3
"""Generate per-variant netlist files for generalization testing.

Each variant gets its own netlist that differs only in the stimulus .include line.
"""

import os

NETLIST_DIR = '/home/ubuntu/analog-ai-chips/vibrosense/10_fullchain/netlists'
TEMPLATE = os.path.join(NETLIST_DIR, 'vibrosense1_peak_normal.spice')

# Read the template
with open(TEMPLATE, 'r') as f:
    template = f.read()

# Variants to generate netlists for
variants = [
    ('normal_v1', 'normal'),
    ('normal_v2', 'normal'),
    ('inner_race_v1', 'inner_race'),
    ('inner_race_v2', 'inner_race'),
    ('inner_race_v3', 'inner_race'),
    ('inner_race_mild', 'inner_race'),
    ('outer_race_v1', 'outer_race'),
    ('outer_race_v2', 'outer_race'),
    ('outer_race_v3', 'outer_race'),
    ('ball_v1', 'ball'),
    ('ball_v2', 'ball'),
    ('ball_v3', 'ball'),
]

for name, fault_type in variants:
    # Replace the stimulus include line
    netlist = template.replace(
        '.include ../../10_fullchain/stimuli/normal_stimulus.pwl',
        f'.include ../../10_fullchain/stimuli/{name}_stimulus.pwl'
    )
    # Update comment
    netlist = netlist.replace(
        '* Stimulus for test case: normal',
        f'* Stimulus for test case: {name} (fault type: {fault_type})'
    )

    outfile = os.path.join(NETLIST_DIR, f'vibrosense1_variant_{name}.spice')
    with open(outfile, 'w') as f:
        f.write(netlist)
    print(f"Generated: {outfile}")

print(f"\n{len(variants)} variant netlists generated")
