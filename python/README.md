# Python Starter

This folder contains a minimal Python setup with a virtual environment and a starter script.

## Quick Start (Windows PowerShell)

```powershell
# From the repo root
$work = "${PWD}" # or set to your path
$pyDir = "$work/python"
$venv = "$pyDir/.venv"

# Create venv (first-time)
python -m venv "$venv"

# Activate venv (PowerShell)
& "$venv/Scripts/Activate.ps1"

# Upgrade pip and install deps
python -m pip install --upgrade pip
pip install -r "$pyDir/requirements.txt"

# Run the starter
python "$pyDir/main.py"
```

If `python` is not found, install Python 3 from https://www.python.org/downloads/windows/ and check "Add Python to PATH" during setup. You can also try `py -3` as the launcher.

## VS Code
- Use the Command Palette → "Python: Select Interpreter" → choose `.venv` under `python/`.
- Launch config `Python: Run main.py` is included to run/debug the script.

## Firebase Admin Integration

This project can connect to Firestore using the Admin SDK. Place your service account key at:

- `04_THE_MEMORY/serviceAccountKey.json`

You can override the path with the `SARAHJOHN_FIREBASE_KEY` environment variable.

### Install dependencies

```powershell
# From repo root, inside the virtual environment
pip install -r python/requirements.txt
```

### Test the connection

```powershell
# Run the lightweight health check
python python/test_firestore.py
```

If successful, you'll see:

```
--- Connection Successful ---
Sarah John is now linked to the cloud memory.
```

## Sovereign Architecture (Genesis 1.8)

**Status:** ACTIVE
**Protocol:** SDNA (Sovereign Data Node Architecture)
**Sync Mode:** RTDB Truth Seed Mirror (Firestore Bypassed)

### Zero-Assumption Protocol
The system operates under a strict "Zero-Assumption" mandate. Ambiguity is resolved through clarification, not guessing.

### Infrastructure Management
- **Firestore API:** Disabled (Bypassed via RTDB Mirror).
- **Realtime Database:** Primary mesh state and "Truth Seed" mirror.
- **Hosting:** Deployed to `sarah-john-genesis.web.app`.

### Core Components
- `Sarah_Brain.py`: Central executive.
- `sarah_sync_v2.py`: Handles cloud synchronization (patched for RTDB-only mode).
- `Sovereign_Override.py`: Enforces compliance logic.

