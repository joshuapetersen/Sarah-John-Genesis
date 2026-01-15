@echo off
setlocal
cd /d %~dp0
if not exist .venv\Scripts\python.exe (
  echo [.venv] not found. Please create/activate the venv first.
  pause
  exit /b 1
)
set PY=.venv\Scripts\python.exe
%PY% -m pip install --quiet pystray pillow requests
%PY% sarah_tray.py
endlocal
