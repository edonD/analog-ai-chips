## Export high-resolution PNG from xschem
## Run: xvfb-run xschem --rcfile export_hires.tcl ota_foldcasc.sch -q

# Wait for schematic to load
after 500

# Zoom to fit all content
xschem zoom_full

# Set a large window for high-res export
xschem windowsize 3200 2400

after 200

# Zoom full again after resize
xschem zoom_full

after 200

# Export PNG
xschem print png ota_foldcasc_hires.png

after 500

xschem exit closewindow
