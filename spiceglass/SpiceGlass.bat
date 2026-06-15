@echo off
rem SpiceGlass — double-click to open the web app (starts the server,
rem then opens your browser at the in-app file picker).
cd /d "%~dp0"
start "" pythonw -m glass edit --no-browser
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8137/
