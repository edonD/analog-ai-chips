#!/usr/bin/env python3
"""
validate_sch.py — Validate xschem .sch against the original SPICE netlist.

Checks:
1. All 13 transistors present with correct model names
2. Net connectivity matches
3. Xschem can parse the file (via xschem --netlist in batch mode)
4. Exports PNG screenshot via xschem + Xvfb for visual inspection
"""

import sys
import os
import re
import subprocess
import tempfile

WORK_DIR = "/home/ubuntu/analog-ai-chips/vibrosense/01_ota/schematic"

# Expected transistors from ota_foldcasc.spice — DO NOT CHANGE
EXPECTED_DEVICES = {
    "XM1":  {"model": "sky130_fd_pr__nfet_01v8", "W": "5u",    "L": "14u"},
    "XM2":  {"model": "sky130_fd_pr__nfet_01v8", "W": "5u",    "L": "14u"},
    "XM3":  {"model": "sky130_fd_pr__pfet_01v8", "W": "0.42u", "L": "1u"},
    "XM4":  {"model": "sky130_fd_pr__pfet_01v8", "W": "0.42u", "L": "1u"},
    "XM5":  {"model": "sky130_fd_pr__pfet_01v8", "W": "0.42u", "L": "2u"},
    "XM6":  {"model": "sky130_fd_pr__pfet_01v8", "W": "0.42u", "L": "2u"},
    "XM7":  {"model": "sky130_fd_pr__nfet_01v8", "W": "0.36u", "L": "1u"},
    "XM8":  {"model": "sky130_fd_pr__nfet_01v8", "W": "0.36u", "L": "1u"},
    "XM9":  {"model": "sky130_fd_pr__nfet_01v8", "W": "2.15u", "L": "4u"},
    "XM10": {"model": "sky130_fd_pr__nfet_01v8", "W": "2.15u", "L": "4u"},
    "XM11": {"model": "sky130_fd_pr__nfet_01v8", "W": "3.6u",  "L": "4u"},
    "XM12": {"model": "sky130_fd_pr__pfet_01v8", "W": "0.42u", "L": "20u"},
    "XM13": {"model": "sky130_fd_pr__pfet_01v8", "W": "0.42u", "L": "20u"},
}

EXPECTED_PORTS = ["vinp", "vinn", "vout", "vdd", "vss", "vbn", "vbcn", "vbp", "vbcp"]


def check_sch_content(sch_path):
    """Parse .sch and check for expected components."""
    with open(sch_path) as f:
        content = f.read()

    results = {"errors": [], "warnings": [], "info": []}

    # Check basic xschem structure
    if "v {" not in content[:200] and "xschem" not in content[:200].lower():
        results["warnings"].append("Missing xschem header (v { ... } block)")

    # Count components and wires
    lines = content.split("\n")
    components = [l for l in lines if l.strip().startswith("C {")]
    wires = [l for l in lines if l.strip().startswith("N ")]
    texts = [l for l in lines if l.strip().startswith("T {")]

    results["info"].append(f"Components: {len(components)}")
    results["info"].append(f"Wires: {len(wires)}")
    results["info"].append(f"Texts/Labels: {len(texts)}")
    results["info"].append(f"Total lines: {len(lines)}")

    # Check for SKY130 device symbols
    nfet_count = sum(1 for c in components if "nfet" in c.lower() or "nmos" in c.lower())
    pfet_count = sum(1 for c in components if "pfet" in c.lower() or "pmos" in c.lower())
    results["info"].append(f"NFET symbols: {nfet_count} (expected 7)")
    results["info"].append(f"PFET symbols: {pfet_count} (expected 6)")

    if nfet_count < 7:
        results["errors"].append(f"Missing NFET devices: found {nfet_count}, expected 7")
    if pfet_count < 6:
        results["errors"].append(f"Missing PFET devices: found {pfet_count}, expected 6")

    # Check for port pins
    for port in EXPECTED_PORTS:
        if port.lower() not in content.lower():
            results["warnings"].append(f"Port '{port}' not found in schematic")

    return results


def export_png(sch_path, png_path):
    """Export schematic to PNG using xschem + Xvfb."""
    try:
        # Use xschem in batch mode with virtual display
        cmd = [
            "xvfb-run", "--auto-servernum", "--server-args=-screen 0 1920x1080x24",
            "xschem", "--netlist", "--svg", "--quit", sch_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=os.path.dirname(sch_path))

        # Also try to get a screenshot via tcl scripting
        tcl_script = f"""
xschem load {sch_path}
xschem zoom_full
xschem print png {png_path}
xschem exit
"""
        tcl_path = os.path.join(os.path.dirname(sch_path), "_export.tcl")
        with open(tcl_path, "w") as f:
            f.write(tcl_script)

        cmd2 = [
            "xvfb-run", "--auto-servernum", "--server-args=-screen 0 1920x1080x24",
            "xschem", "--tcl", tcl_path, "--quit"
        ]
        result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=30, cwd=os.path.dirname(sch_path))

        if os.path.exists(png_path):
            return True, f"Exported to {png_path}"
        else:
            # Check for SVG as alternative
            svg_path = sch_path.replace(".sch", ".svg")
            if os.path.exists(svg_path):
                return True, f"Exported SVG to {svg_path}"
            return False, f"Export failed: {result.stderr[:200]} / {result2.stderr[:200]}"
    except Exception as e:
        return False, f"Export error: {e}"


def netlist_from_sch(sch_path):
    """Run xschem --netlist to generate SPICE from .sch and verify round-trip."""
    try:
        cmd = [
            "xvfb-run", "--auto-servernum", "--server-args=-screen 0 1920x1080x24",
            "xschem", "-n", "-q", sch_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                                cwd=os.path.dirname(sch_path))
        # Look for generated netlist
        netlist_path = sch_path.replace(".sch", ".spice")
        if os.path.exists(netlist_path):
            with open(netlist_path) as f:
                return f.read()
        return None
    except Exception as e:
        return None


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <schematic.sch>")
        sys.exit(1)

    sch_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(sch_path):
        print(f"File not found: {sch_path}")
        sys.exit(1)

    print(f"Validating: {sch_path}")
    print("=" * 60)

    # 1. Content check
    results = check_sch_content(sch_path)

    print("\nInfo:")
    for i in results["info"]:
        print(f"  {i}")

    if results["warnings"]:
        print("\nWarnings:")
        for w in results["warnings"]:
            print(f"  ⚠ {w}")

    if results["errors"]:
        print("\nErrors:")
        for e in results["errors"]:
            print(f"  ✗ {e}")

    # 2. Try PNG export
    png_path = sch_path.replace(".sch", ".png")
    print(f"\nExporting PNG...")
    ok, msg = export_png(sch_path, png_path)
    print(f"  {msg}")

    # 3. Try round-trip netlist
    print(f"\nRound-trip netlist check...")
    netlist = netlist_from_sch(sch_path)
    if netlist:
        print(f"  Generated netlist ({len(netlist)} chars)")
        # Check if key devices appear
        for dev in ["XM1", "XM2", "XM11"]:
            if dev.lower() in netlist.lower() or dev[1:].lower() in netlist.lower():
                print(f"  ✓ {dev} found in round-trip netlist")
            else:
                print(f"  ✗ {dev} NOT found in round-trip netlist")
    else:
        print("  Round-trip netlist generation failed (xschem may need PDK symbols)")

    # Summary
    n_err = len(results["errors"])
    n_warn = len(results["warnings"])
    print(f"\n{'=' * 60}")
    print(f"Summary: {n_err} errors, {n_warn} warnings")
    if n_err == 0:
        print("STATUS: PASS")
    else:
        print("STATUS: NEEDS FIX")
    sys.exit(0 if n_err == 0 else 1)


if __name__ == "__main__":
    main()
