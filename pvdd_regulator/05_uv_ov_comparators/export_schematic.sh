#!/usr/bin/env bash
# export_schematic.sh — Generate schematics and export to high-res PNG
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Block 05 Schematic Generator ==="
echo "Started: $(date)"

# Step 1: Generate .sch files
echo ">>> Generating .sch files..."
python3 gen_schematic.py

# Step 2: Export each schematic to SVG then PNG (high resolution)
export_sch() {
    local sch="$1"
    local svg="${sch%.sch}.svg"
    local png="${sch%.sch}.png"

    echo "--- Exporting $sch → $svg → $png ---"

    # Use xschem in batch mode with Xvfb for headless rendering
    # Export to SVG first (vector), then convert to high-res PNG
    xvfb-run -a xschem --svg --plotfile "$svg" -q "$sch" --no_x 2>&1 || {
        echo "  xschem SVG export failed, trying PNG directly..."
        xvfb-run -a xschem --png --plotfile "$png" -q "$sch" --no_x 2>&1 || {
            echo "  Direct PNG export also failed. Trying command mode..."
            xvfb-run -a xschem -q "$sch" --command "xschem svg $svg; exit" --no_x 2>&1 || true
        }
    }

    # Convert SVG to high-res PNG if SVG was generated
    if [ -f "$svg" ]; then
        echo "  Converting SVG to PNG (300 DPI)..."
        rsvg-convert -d 300 -p 300 -w 4000 "$svg" -o "$png" 2>&1 || {
            echo "  rsvg-convert failed, trying with zoom..."
            rsvg-convert -z 4 "$svg" -o "$png" 2>&1 || true
        }
        echo "  Generated: $png ($(du -h "$png" 2>/dev/null | cut -f1))"
    elif [ -f "$png" ]; then
        echo "  Generated: $png ($(du -h "$png" 2>/dev/null | cut -f1))"
    else
        echo "  WARNING: No output generated for $sch"
    fi
}

export_sch uv_comparator.sch
export_sch ov_comparator.sch
export_sch uvov_top.sch

echo ""
echo "=== Results ==="
ls -lh *.png 2>/dev/null || echo "No PNG files generated"
ls -lh *.svg 2>/dev/null || echo "No SVG files generated"

echo ""
echo "=== Checking quality ==="
for png in uv_comparator.png ov_comparator.png uvov_top.png; do
    if [ -f "$png" ]; then
        dims=$(python3 -c "
from PIL import Image
im = Image.open('$png')
print(f'{im.size[0]}x{im.size[1]}')
" 2>/dev/null || echo "unknown")
        echo "  $png: $dims pixels"
    else
        echo "  $png: MISSING"
    fi
done

echo ""
echo "Finished: $(date)"
