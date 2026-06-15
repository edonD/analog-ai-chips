@echo off
title SpiceGlass  -  close this window to stop
rem One-click launcher: double-click this file. It starts the local
rem SpiceGlass server and opens your browser. Close the window to stop.

cd /d "%~dp0spiceglass"

rem find a Python: prefer "python", fall back to the "py" launcher
set "PY=python"
where python >nul 2>nul || set "PY=py"
where %PY% >nul 2>nul || (
  echo.
  echo   Python was not found on this PC.
  echo   Install Python 3.10+ from https://www.python.org/downloads/
  echo   and tick "Add python.exe to PATH" during setup.
  echo.
  pause
  exit /b 1
)

%PY% -m glass edit

echo.
echo   SpiceGlass stopped.
pause
