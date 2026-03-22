#!/usr/bin/env python3
"""Build self-contained model files for each device/corner.

Resolves all .include directives, removes mismatch expressions,
and produces standalone files with no external dependencies.
"""
import re
import os

PDK = "/home/ubuntu/pdk/sky130A/libs.ref/sky130_fd_pr/spice"
OUT = "/home/ubuntu/analog-ai-chips/vibrosense/01_ota/models"
os.makedirs(OUT, exist_ok=True)

def remove_mismatch(content):
    """Remove MC_MM_SWITCH mismatch terms."""
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

def resolve_includes(filepath, base_dir):
    """Recursively resolve .include directives."""
    with open(filepath) as f:
        lines = f.readlines()

    result = []
    for line in lines:
        stripped = line.strip().lower()
        if stripped.startswith('.include'):
            # Extract filename
            m = re.search(r'"([^"]+)"', line)
            if m:
                inc_file = m.group(1)
                # Try to find the file
                candidates = [
                    os.path.join(base_dir, inc_file),
                    os.path.join(PDK, inc_file),
                    inc_file,
                ]
                found = None
                for c in candidates:
                    if os.path.exists(c):
                        found = c
                        break
                if found:
                    result.append(f"* [resolved include: {inc_file}]\n")
                    result.extend(resolve_includes(found, os.path.dirname(found)))
                else:
                    result.append(f"* [include not found, skipped: {inc_file}]\n")
            else:
                result.append(line)
        else:
            result.append(line)
    return result

def extract_models_only(content):
    """Extract .model definitions and .param lines, remove .subckt wrapper."""
    lines = content.split('\n')
    out_lines = []
    in_subckt = False
    in_model = False

    for line in lines:
        stripped = line.strip().lower()

        if stripped.startswith('.subckt'):
            in_subckt = True
            continue
        if stripped.startswith('.ends'):
            in_subckt = False
            continue

        # Always keep .param lines
        if stripped.startswith('.param') or (stripped.startswith('+') and not in_model and not in_subckt):
            # Check if this is a param continuation
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
            else:
                in_model = False
                if stripped.startswith('.model'):
                    in_model = True
                    out_lines.append(line)
                elif stripped.startswith('.param'):
                    out_lines.append(line)

    return '\n'.join(out_lines)

corners = ['tt', 'ss', 'ff', 'sf', 'fs']
devices = ['nfet_01v8', 'pfet_01v8']

# Missing params that need defaults
NFET_DEFAULTS = """
.param sky130_fd_pr__nfet_01v8__ajunction_mult = 1.0
.param sky130_fd_pr__nfet_01v8__pjunction_mult = 1.0
.param sky130_fd_pr__nfet_01v8__dlc_rotweak = 0
"""
PFET_DEFAULTS = """
.param sky130_fd_pr__pfet_01v8__dlc_rotweak = 0
.param sky130_fd_pr__pfet_01v8__overlap_mult = 1.0
.param sky130_fd_pr__pfet_01v8__rshp_mult = 1.0
.param sky130_fd_pr__pfet_01v8__toxe_mult = 1.0
.param sky130_fd_pr__pfet_01v8__ku0_diff = 0
.param sky130_fd_pr__pfet_01v8__kvsat_diff = 0
.param sky130_fd_pr__pfet_01v8__kvth0_diff = 0
.param sky130_fd_pr__pfet_01v8__lku0_diff = 0
.param sky130_fd_pr__pfet_01v8__lkvth0_diff = 0
.param sky130_fd_pr__pfet_01v8__wku0_diff = 0
.param sky130_fd_pr__pfet_01v8__wkvth0_diff = 0
.param sky130_fd_pr__pfet_01v8__wlod_diff = 0
"""

for dev in devices:
    defaults = NFET_DEFAULTS if 'nfet' in dev else PFET_DEFAULTS

    for corner in corners:
        # Start with the corner file (which may include the pm3)
        corner_file = f"{PDK}/sky130_fd_pr__{dev}__{corner}.corner.spice"
        pm3_file = f"{PDK}/sky130_fd_pr__{dev}__{corner}.pm3.spice"

        dst = f"{OUT}/sky130_fd_pr__{dev}__{corner}_standalone.spice"

        content_parts = []
        content_parts.append(f"* Self-contained {dev} model ({corner} corner)\n")
        content_parts.append(f"* Model name: sky130_fd_pr__{dev}__model\n\n")

        # Add defaults first (will be overridden by corner file if redefined)
        content_parts.append("* Default parameters\n")
        content_parts.append(defaults + "\n")

        # Resolve and include the corner file (which includes the pm3)
        if os.path.exists(corner_file):
            resolved = resolve_includes(corner_file, PDK)
            content_parts.extend(resolved)

        full_content = ''.join(content_parts)

        # Remove mismatch expressions
        full_content = remove_mismatch(full_content)

        # Extract only .model and .param (remove .subckt wrapper)
        final_content = extract_models_only(full_content)

        with open(dst, 'w') as f:
            f.write(f"* Self-contained {dev} model ({corner} corner)\n")
            f.write(f"* Model name: sky130_fd_pr__{dev}__model\n\n")
            f.write(final_content)

        # Count
        model_count = final_content.count('.model ')
        param_count = final_content.count('.param ')
        print(f"{dev}__{corner}: {model_count} models, {param_count} params -> {os.path.basename(dst)}")

# Verify
print("\nVerification:")
for dev in devices:
    f = f"{OUT}/sky130_fd_pr__{dev}__tt_standalone.spice"
    with open(f) as fh:
        c = fh.read()
    print(f"  {dev}: MC_MM={c.upper().count('MC_MM_SWITCH')}, .subckt={c.lower().count('.subckt')}, .include={c.lower().count('.include')}")
    # Check vth0 values
    vth0_lines = [l for l in c.split('\n') if 'vth0 =' in l.lower() and 'vth0_diff' not in l.lower() and 'vth0_slope' not in l.lower() and 'dvt0' not in l.lower() and 'kvth0' not in l.lower() and 'llodvth' not in l.lower()]
    if vth0_lines:
        print(f"  {dev} sample vth0: {vth0_lines[0].strip()[:80]}")
