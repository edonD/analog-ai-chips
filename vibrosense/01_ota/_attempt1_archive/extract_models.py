#!/usr/bin/env python3
"""Extract BSIM4 .model definitions from SKY130 pm3 files.

Removes the .subckt wrapper and MC_MM_SWITCH mismatch expressions,
producing raw .model files usable directly with M-prefix MOSFET instances.
"""
import re
import os

PDK = "/home/ubuntu/pdk/sky130A/libs.ref/sky130_fd_pr/spice"
OUT = "/home/ubuntu/analog-ai-chips/vibrosense/01_ota/models"
os.makedirs(OUT, exist_ok=True)

def remove_mismatch(content):
    """Remove MC_MM_SWITCH mismatch terms from {value+MC_MM*...} expressions."""
    lines = content.split('\n')
    out_lines = []
    for line in lines:
        if 'MC_MM_SWITCH' in line.upper():
            result = []
            i = 0
            while i < len(line):
                if line[i] == '{':
                    depth = 1
                    j = i + 1
                    while j < len(line) and depth > 0:
                        if line[j] == '{': depth += 1
                        elif line[j] == '}': depth -= 1
                        j += 1
                    expr = line[i+1:j-1]
                    if 'MC_MM_SWITCH' in expr.upper():
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

def extract_models(src_path, model_name):
    """Extract .model definitions from a pm3.spice file, removing subcircuit wrappers."""
    with open(src_path) as f:
        content = f.read()

    # Remove mismatch expressions
    content = remove_mismatch(content)

    lines = content.split('\n')
    out_lines = []
    in_model = False
    skip_subckt = False

    for line in lines:
        stripped = line.strip().lower()

        # Skip .subckt/.ends and the MOSFET instance inside
        if stripped.startswith('.subckt'):
            skip_subckt = True
            continue
        if stripped.startswith('.ends'):
            skip_subckt = False
            continue
        if skip_subckt and not stripped.startswith('.model') and not stripped.startswith('+') and not stripped.startswith('.param'):
            # Skip lines inside subcircuit that aren't .model or continuation
            if not in_model:
                continue

        # Keep .param lines (parameter definitions)
        if stripped.startswith('.param'):
            out_lines.append(line)
            continue

        # Keep .model lines and their continuations
        if stripped.startswith('.model'):
            in_model = True
            out_lines.append(line)
            continue

        if in_model:
            if stripped.startswith('+') or stripped.startswith('*'):
                out_lines.append(line)
                continue
            else:
                in_model = False
                # Check if this line is also .model
                if stripped.startswith('.model'):
                    in_model = True
                    out_lines.append(line)
                    continue

    return '\n'.join(out_lines)

corners = ['tt', 'ss', 'ff', 'sf', 'fs']
devices = ['nfet_01v8', 'pfet_01v8']

for dev in devices:
    model_name = f'sky130_fd_pr__{dev}__model'

    for corner in corners:
        src = f"{PDK}/sky130_fd_pr__{dev}__{corner}.pm3.spice"
        dst = f"{OUT}/sky130_fd_pr__{dev}__{corner}_raw.spice"
        if os.path.exists(src):
            result = extract_models(src, model_name)
            with open(dst, 'w') as f:
                f.write(f"* Extracted BSIM4 models for {dev} ({corner} corner)\n")
                f.write(f"* Use model name: {model_name}\n")
                f.write(f"* Generated from: {src}\n\n")
                # Add missing parameter defaults
                if 'nfet' in dev:
                    f.write(".param sky130_fd_pr__nfet_01v8__ajunction_mult = 1.0\n")
                    f.write(".param sky130_fd_pr__nfet_01v8__pjunction_mult = 1.0\n")
                    f.write(".param sky130_fd_pr__nfet_01v8__dlc_rotweak = 0\n")
                else:
                    f.write(".param sky130_fd_pr__pfet_01v8__ajunction_mult = 1.0\n")
                    f.write(".param sky130_fd_pr__pfet_01v8__pjunction_mult = 1.0\n")
                    f.write(".param sky130_fd_pr__pfet_01v8__dlc_rotweak = 0\n")
                    f.write(".param sky130_fd_pr__pfet_01v8__overlap_mult = 1.0\n")
                    f.write(".param sky130_fd_pr__pfet_01v8__rshp_mult = 1.0\n")
                    f.write(".param sky130_fd_pr__pfet_01v8__toxe_mult = 1.0\n")
                f.write("\n")
                f.write(result)
            # Count models
            model_count = result.count('.model ')
            print(f"{dev}__{corner}: {model_count} model bins extracted -> {dst}")

# Verify
print("\nVerification on tt nfet:")
with open(f"{OUT}/sky130_fd_pr__nfet_01v8__tt_raw.spice") as f:
    content = f.read()
print(f"  MC_MM_SWITCH: {content.upper().count('MC_MM_SWITCH')}")
print(f"  .subckt: {content.lower().count('.subckt')}")
print(f"  .model: {content.lower().count('.model ')}")
print(f"  Lines: {len(content.split(chr(10)))}")
