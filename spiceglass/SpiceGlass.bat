@echo off
rem SpiceGlass launcher — double-click to open the GUI
cd /d "%~dp0"
start "" pythonw -m glass gui
