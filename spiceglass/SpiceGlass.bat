@echo off
title SpiceGlass  -  close this window to stop
rem Double-click to launch SpiceGlass. Starts the local server and opens
rem your browser. Close this window to stop it.

cd /d "%~dp0"

rem find a Python: prefer the py launcher, then plain python
set "PY="
where py >nul 2>nul
if not errorlevel 1 set "PY=py"
if defined PY goto run
where python >nul 2>nul
if not errorlevel 1 set "PY=python"
if defined PY goto run

echo.
echo   Python was not found on this PC.
echo   Install Python 3.10+ from https://www.python.org/downloads/
echo   and tick "Add python.exe to PATH" during setup.
echo.
pause
exit /b 1

:run
%PY% -m glass edit

echo.
echo   SpiceGlass stopped.
pause
