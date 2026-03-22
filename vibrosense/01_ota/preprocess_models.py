#!/usr/bin/env python3
"""Preprocess SKY130 model files to remove MC mismatch expressions for ngspice."""
import re
import os
import shutil

PDK = "/home/ubuntu/pdk/sky130A/libs.ref/sky130_fd_pr/spice"
OUT = "/home/ubuntu/analog-ai-chips/vibrosense/01_ota/models"
os.makedirs(OUT, exist_ok=True)

def remove_mismatch(content):
    """Remove MC_MM_SWITCH mismatch terms from BSIM model expressions.

    Transforms: {base_value+MC_MM_SWITCH*AGAUSS(...)*(complex_expr))}
    Into:        base_value
    """
    lines = content.split('\n')
    out_lines = []
    for line in lines:
        if 'MC_MM_SWITCH' in line.upper():
            # Find the {value+MC_MM_SWITCH...} pattern
            # Strategy: find each {...} expression containing MC_MM_SWITCH
            # and replace it with just the base value
            result = []
            i = 0
            while i < len(line):
                if line[i] == '{':
                    # Find matching closing brace
                    depth = 1
                    j = i + 1
                    while j < len(line) and depth > 0:
                        if line[j] == '{': depth += 1
                        elif line[j] == '}': depth -= 1
                        j += 1
                    expr = line[i+1:j-1]  # content inside {...}

                    if 'MC_MM_SWITCH' in expr.upper():
                        # Extract base value (before +MC_MM_SWITCH)
                        mc_idx = expr.upper().find('+MC_MM_SWITCH')
                        if mc_idx == -1:
                            mc_idx = expr.upper().find('+ MC_MM_SWITCH')
                        if mc_idx > 0:
                            base_val = expr[:mc_idx].strip()
                        else:
                            base_val = '0'
                        result.append('{' + base_val + '}')
                    else:
                        result.append(line[i:j])
                    i = j
                else:
                    result.append(line[i])
                    i += 1
            out_lines.append(''.join(result))
        else:
            out_lines.append(line)
    return '\n'.join(out_lines)

def process_file(src, dst):
    with open(src, 'r') as f:
        content = f.read()
    content_out = remove_mismatch(content)
    with open(dst, 'w') as f:
        f.write(content_out)
    return content != content_out

corners = ['tt', 'ss', 'ff', 'sf', 'fs']
devices = ['nfet_01v8', 'pfet_01v8']

for dev in devices:
    # Base pm3 file (subcircuit definition)
    src = f"{PDK}/sky130_fd_pr__{dev}.pm3.spice"
    dst = f"{OUT}/sky130_fd_pr__{dev}.pm3.spice"
    shutil.copy(src, dst)

    for corner in corners:
        # Corner pm3 file (has mismatch expressions)
        src = f"{PDK}/sky130_fd_pr__{dev}__{corner}.pm3.spice"
        dst = f"{OUT}/sky130_fd_pr__{dev}__{corner}.pm3.spice"
        if os.path.exists(src):
            changed = process_file(src, dst)
            print(f"{dev}__{corner}: {'MODIFIED' if changed else 'unchanged'}")

        # Corner file (parameter values, no mismatch)
        src = f"{PDK}/sky130_fd_pr__{dev}__{corner}.corner.spice"
        dst = f"{OUT}/sky130_fd_pr__{dev}__{corner}.corner.spice"
        if os.path.exists(src):
            shutil.copy(src, dst)

# Verify
print("\nVerification:")
for dev in devices:
    test_file = f"{OUT}/sky130_fd_pr__{dev}__tt.pm3.spice"
    with open(test_file) as f:
        content = f.read()
    mc_count = content.upper().count('MC_MM_SWITCH')
    # Show toxe lines
    for line in content.split('\n'):
        if '+ toxe =' in line.lower():
            print(f"  {dev}: {line.strip()}")
            break
    print(f"  {dev}: MC_MM_SWITCH occurrences = {mc_count}")
