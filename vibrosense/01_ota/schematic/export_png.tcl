xschem set netlist_dir [pwd]
xschem load [pwd]/ota_foldcasc.sch
xschem zoom_full
xschem set svg_colors 1
xschem print svg [pwd]/ota_foldcasc.svg
after 1000
exit
