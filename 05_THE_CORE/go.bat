@echo off
setlocal
cd /d %~dp0
:: Launch PowerShell with ExecutionPolicy bypass and keep window open to display any errors
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -NoExit -File "%~dp0oneclick.ps1"

:: Launch ZHTP Protocol Daemon
start "ZHTP_Daemon" cmd /c "python %~dp0ZHTP_Protocol.py"

:: After the main stack starts, offer to start the tray helper (in a separate window)
start "SarahTray" cmd /c "cd /d %~dp0 && .\run_sarah_tray.bat"
endlocal
