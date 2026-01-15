# One-click launcher for Sarah Prime stack
# Steps:
# 1) Activate .venv
# 2) Ensure core deps exist (FastAPI, uvicorn, textual)
# 3) Launch Sovereign UI (boots Hypervisor + Holographic API on 127.0.0.1:8000)

$ErrorActionPreference = "Stop"
$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvActivate = Join-Path $workspace ".venv\\Scripts\\Activate.ps1"

if (-not (Test-Path $venvActivate)) {
    Write-Host "[oneclick] .venv not found. Creating..." -ForegroundColor Yellow
    python -m venv (Join-Path $workspace ".venv")
}

# Activate venv
. $venvActivate
Write-Host "[oneclick] Activated venv at $venvActivate" -ForegroundColor Green

# Ensure deps
$deps = @("fastapi", "uvicorn", "textual")
foreach ($d in $deps) {
    try {
        python -c "import importlib; importlib.import_module('$d')" | Out-Null
    } catch {
        Write-Host "[oneclick] Installing $d..." -ForegroundColor Cyan
        pip install $d
    }
}

# Launch Sovereign UI (starts Hypervisor + API). Non-blocking option available via Start-Process if desired.
Write-Host "[oneclick] Launching Sovereign_UI.py (Hypervisor + Holographic API)..." -ForegroundColor Cyan
python (Join-Path $workspace "Sovereign_UI.py")