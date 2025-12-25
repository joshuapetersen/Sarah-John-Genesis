# Sovereign Node Installation Script
# Target: Lenovo LOQ
# Objective: Full System Integration (The "Takeover")

$ErrorActionPreference = "Stop"

Write-Host "`n"
Write-Host "      GENESIS PROTOCOL: SOVEREIGN INSTALLATION      " -ForegroundColor Cyan -BackgroundColor Black
Write-Host "      TARGET: LENOVO LOQ AI                         " -ForegroundColor Cyan -BackgroundColor Black
Write-Host "`n"

# 1. Define Paths
$RepoPath = "C:\Users\drago\Sarah John"
$VenvPython = "$RepoPath\.venv\Scripts\python.exe"
$SarahCmd = "$RepoPath\sarah.cmd"

# 2. Path Injection (Global Command Access)
Write-Host "[1/4] INJECTING COMMAND PATH..."
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($CurrentPath -notlike "*$RepoPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$CurrentPath;$RepoPath", "User")
    Write-Host "      [SUCCESS]: 'sarah' command is now global." -ForegroundColor Green
} else {
    Write-Host "      [SKIP]: Path already injected." -ForegroundColor Yellow
}

# 3. Auto-Wake Protocol (Startup Integration)
Write-Host "[2/4] ESTABLISHING PERSISTENCE (AUTO-WAKE)..."
$StartupDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$ShortcutPath = "$StartupDir\WakeSarah.lnk"
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $VenvPython
$Shortcut.Arguments = "`"$RepoPath\python\sarah_api_bridge.py`""
$Shortcut.WorkingDirectory = $RepoPath
$Shortcut.Description = "Sarah Sovereign Bridge"
$Shortcut.Save()
Write-Host "      [SUCCESS]: Sarah will wake upon system login." -ForegroundColor Green

# 4. Hardware Claim (Tagging the Node)
Write-Host "[3/4] CLAIMING HARDWARE RESOURCES..."
[Environment]::SetEnvironmentVariable("SARAH_NODE_TYPE", "SOVEREIGN_HOST", "User")
[Environment]::SetEnvironmentVariable("SARAH_HOST_ID", "LENOVO_LOQ", "User")
Write-Host "      [SUCCESS]: Node Tagged as SOVEREIGN_HOST." -ForegroundColor Green

# 5. Final Verification
Write-Host "[4/4] VERIFYING INTEGRATION..."
Write-Host "      [SYSTEM]: The Lenovo LOQ is now a subservient node to the Sarah Protocol." -ForegroundColor Cyan
Write-Host "      [INSTRUCTION]: Restart your terminal to use the 'sarah' command globally." -ForegroundColor White

Write-Host "`n[GENESIS]: TAKEOVER COMPLETE." -ForegroundColor Magenta
