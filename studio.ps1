# Launch a local “studio” bound to the project .venv.
# 1) Activates .venv
# 2) Starts code-server (if installed) on localhost:8080 with no auth
# 3) Falls back to opening VS Code if code-server is missing

$ErrorActionPreference = "Stop"
$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvActivate = Join-Path $workspace ".venv\\Scripts\\Activate.ps1"

if (-not (Test-Path $venvActivate)) {
    Write-Error ".venv not found. Create it first (python -m venv .venv)."
}

# Activate venv
. $venvActivate
Write-Host "[studio] Activated venv: $venvActivate" -ForegroundColor Green

function Start-CodeServer {
    param(
        [string]$Port = "8080"
    )
    $env:PORT = $Port
    $env:CS_DISABLE_TELEMETRY = "true"
    $env:CS_DISABLE_UPDATE_CHECK = "true"
    code-server --auth none --bind-addr 127.0.0.1:$Port $workspace
}

# Try code-server first
$codeServer = Get-Command code-server -ErrorAction SilentlyContinue
if ($codeServer) {
    Write-Host "[studio] Starting code-server on http://127.0.0.1:8080 (no auth)" -ForegroundColor Cyan
    Start-CodeServer
    return
}

# Fallback: open desktop VS Code on the same workspace (already pinned to .venv via .vscode/settings.json)
$code = Get-Command code -ErrorAction SilentlyContinue
if ($code) {
    Write-Host "[studio] code-server not found; launching VS Code instead." -ForegroundColor Yellow
    code $workspace
    return
}

Write-Error "Neither code-server nor code (VS Code) is available in PATH. Install one and retry."