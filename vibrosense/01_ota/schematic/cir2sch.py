#!/usr/bin/env python3
"""
cir2sch.py — Convert OTA SPICE netlist to xschem schematic via inference API.

Usage:
    python3 cir2sch.py <netlist.spice> [output.sch]

Calls the cir2sch-fft-4b model to generate xschem .sch from SPICE.
"""

import sys
import os
from openai import OpenAI

API_BASE = os.environ.get("CIR2SCH_API", "http://18.232.161.171:8000/v1")
MODEL_ID = "cir2sch-fft-4b"

SYSTEM_MSG = (
    "You are an expert analog circuit designer. Given a SPICE netlist, "
    "generate the corresponding xschem schematic (.sch) file with proper "
    "component placement and wire routing. The schematic should follow "
    "analog design conventions: signal flows left-to-right, power top-to-bottom, "
    "differential pairs symmetric, current mirrors vertical, clean wire routing."
)


def generate(client, netlist):
    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": f"Convert this SPICE netlist to an xschem schematic:\n\n{netlist}"},
        ],
        max_tokens=4096,
        temperature=0.1,
    )
    return resp.choices[0].message.content or ""


def validate(schematic):
    lines = schematic.strip().split("\n")
    return {
        "has_header":     any("xschem version" in l.lower() or "v {" in l for l in lines[:5]),
        "num_components": sum(1 for l in lines if l.strip().startswith("C {")),
        "num_wires":      sum(1 for l in lines if l.strip().startswith("N ")),
        "num_texts":      sum(1 for l in lines if l.strip().startswith("T {")),
        "total_lines":    len(lines),
    }


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <netlist.spice> [output.sch]")
        sys.exit(1)

    netlist_path = sys.argv[1]
    with open(netlist_path) as f:
        netlist = f.read()

    output_path = sys.argv[2] if len(sys.argv) > 2 else netlist_path.rsplit(".", 1)[0] + ".sch"

    print(f"Input:  {netlist_path}")
    print(f"Output: {output_path}")
    print(f"API:    {API_BASE}")
    print(f"Model:  {MODEL_ID}")
    print()

    client = OpenAI(api_key="none", base_url=API_BASE)
    print("Generating schematic...")
    schematic = generate(client, netlist)

    v = validate(schematic)
    print(f"\nValidation:")
    for k, val in v.items():
        print(f"  {k}: {val}")

    with open(output_path, "w") as f:
        f.write(schematic)
    print(f"\nSaved -> {output_path}")

    ok = v["num_components"] > 0 or v["total_lines"] > 5
    print(f"Status: {'OK' if ok else 'NEEDS REVIEW'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
