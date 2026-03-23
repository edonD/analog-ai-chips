# Schematic Generation Guide — SPICE to xschem via Inference API

## API Details

- **Endpoint:** `http://18.232.161.171:8000/v1` (OpenAI-compatible)
- **Model:** `cir2sch-fft-4b`
- **Python package:** `openai`

## Calling the API

```python
from openai import OpenAI

client = OpenAI(api_key="none", base_url="http://18.232.161.171:8000/v1")

with open("block_name.spice") as f:
    netlist_text = f.read()

response = client.chat.completions.create(
    model="cir2sch-fft-4b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are an expert analog circuit designer. Given a SPICE netlist, "
                "generate the corresponding xschem schematic (.sch) file with proper "
                "component placement and wire routing. The schematic should follow "
                "analog design conventions: signal flows left-to-right, power top-to-bottom, "
                "differential pairs symmetric, current mirrors vertical, clean wire routing."
            ),
        },
        {
            "role": "user",
            "content": f"Convert this SPICE netlist to an xschem schematic:\n\n{netlist_text}",
        },
    ],
    max_tokens=4096,
    temperature=0.1,
)

schematic = response.choices[0].message.content

with open("block_name.sch", "w") as f:
    f.write(schematic)
```

## SKY130 PDK Symbol Paths

```
NFET: /home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym
PFET: /home/ubuntu/pdk/volare/sky130/versions/6d4d11780c40b20ee63cc98e645307a9bf2b2ab8/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym
```

## Rules

1. Do NOT modify the SPICE netlist — the schematic must match it exactly
2. Every transistor must have the correct W, L, nf, model from the netlist
3. Every net name must match the netlist exactly
4. Use correct SKY130 PDK symbol paths (full paths above)
5. Follow analog conventions: VDD top, VSS bottom, PMOS upper half, NMOS lower half

## Validation Steps

### 1. Content check
Parse the .sch and count NFET/PFET symbols — must match netlist device count.
Check all port names are present.

### 2. Netlist round-trip
Extract SPICE from the schematic and compare with the original:
```bash
xvfb-run --auto-servernum xschem -n -q block_name.sch
# Compare extracted netlist with original — every device, net, W/L must match
```

### 3. Export SVG
```bash
xvfb-run --auto-servernum --server-args="-screen 0 3840x2160x24" \
  xschem --svg --plotfile block_name.svg -q block_name.sch
```

### 4. Convert SVG to high-res PNG
```python
import cairosvg
cairosvg.svg2png(
    url="block_name.svg",
    write_to="block_name.png",
    output_width=3200,
    output_height=2400,
    background_color="white",
)
```

### 5. If API output is bad, build the .sch manually
The xschem .sch format is text — you can construct it directly.

## xschem .sch Format Reference

```
v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N x1 y1 x2 y2 {lab=net_name}                          <- wires
T {text} x y 0 0 0.6 0.6 {}                           <- labels/titles
C {/full/path/to/nfet_01v8.sym} x y rot mirror \
  {name=M1 L=1u W=10u nf=1 mult=1 model=nfet_01v8 spiceprefix=X}   <- transistor
C {devices/lab_pin.sym} x y rot mirror {name=p1 lab=net_name}       <- net label
C {devices/iopin.sym} x y rot mirror {name=p1 lab=port_name}        <- I/O pin
```

### Coordinate conventions
- Units are arbitrary (typically 10-unit grid)
- Positive X = right, positive Y = down (screen coordinates)
- `rot`: 0=normal, 1=90°CW, 2=180°, 3=270°CW
- `mirror`: 0=normal, 1=mirrored

### Transistor pin order (SKY130 symbols)
- NFET: drain(top), gate(left), source(bottom), body(right)
- PFET: drain(bottom), gate(left), source(top), body(right)

## Prompt Template for New Blocks

Copy-paste this when starting a new schematic:

> I have a SPICE netlist at `vibrosense/XX_block/block_name.spice`. Generate an xschem schematic (.sch) from it using the cir2sch inference API. See `vibrosense/schematic_guide.md` for API details, symbol paths, validation steps, and the .sch format reference. Do NOT modify the SPICE netlist. Validate with netlist round-trip. Export high-res PNG. If API output is bad, build the .sch manually. Commit only this block's files.
