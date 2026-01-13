# Registers a user-level scheduled task to auto-start SarahCore at logon.
# It runs go.bat (which starts the stack and then the tray helper).

$ErrorActionPreference = "Stop"
$taskName = "SarahCore_AutoStart"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$goPath = Join-Path $scriptDir "go.bat"

if (-not (Test-Path $goPath)) {
    Write-Error "go.bat not found at $goPath"
}

# Define action: launch PowerShell that runs go.bat
$action = New-ScheduledTaskAction -Execute "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -Argument "-NoLogo -NoProfile -ExecutionPolicy Bypass -File `"$goPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn

# Register or update
try {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
} catch {}
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Description "Auto-start SarahCore and tray at logon" -RunLevel LeastPrivilege

Write-Host "Scheduled task '$taskName' registered. It will run go.bat at user logon." -ForegroundColor Green
