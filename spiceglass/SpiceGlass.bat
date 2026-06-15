@echo off
title SpiceGlass  -  close this window to stop
rem Double-click to launch SpiceGlass (starts the server, opens the browser).
rem Closing this window stops it.

cd /d "%~dp0"

set "PY=python"
where python >nul 2>nul || set "PY=py"
where %PY% >nul 2>nul || (
  echo.
  echo   Python was not found. Install Python 3.10+ from
  echo   https://www.python.org/downloads/  (tick "Add to PATH").
  echo.
  pause
  exit /b 1
)

%PY% -m glass edit

echo.
echo   SpiceGlass stopped.
pause
