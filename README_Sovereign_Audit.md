# Sovereign System Audit & ROI Assessment

## Terminal Commands Reference

Use these commands in your terminal to run and manage the Sovereign System Audit procedure and related Python operations.

---


### 1. Run the Sovereign Audit Procedure (Single Run)
```
C:/SarahCore/.venv/Scripts/python.exe Sovereign_Audit_Procedure.py
```
Runs the hardcoded audit and displays the full report and resonance scan output.

---

### 1a. Run the Sovereign Audit Procedure Automatically Every 30 Seconds
```
C:/SarahCore/.venv/Scripts/python.exe Sovereign_Audit_Procedure.py --loop
```
Runs the audit and resonance scan in a continuous loop, updating every 30 seconds.

---

### 2. Run Any Python Script in the Virtual Environment
```
C:/SarahCore/.venv/Scripts/python.exe <script_name.py>
```
Replace `<script_name.py>` with the name of your Python file to execute it using the configured environment.

---

### 3. Run Inline Python Code
```
C:/SarahCore/.venv/Scripts/python.exe -c "<python_code>"
```
Replace `<python_code>` with your Python code in quotes. Example:
```
C:/SarahCore/.venv/Scripts/python.exe -c "import sys; print(sys.executable)"
```

---

### 4. Install Python Packages (if needed)
```
C:/SarahCore/.venv/Scripts/python.exe -m pip install <package_name>
```
Replace `<package_name>` with the package you want to install.

---

### 5. List Installed Packages
```
C:/SarahCore/.venv/Scripts/python.exe -m pip list
```
Shows all Python packages installed in your virtual environment.

---

### 6. Activate the Virtual Environment (PowerShell)
```
. .venv/Scripts/Activate.ps1
```
Activates the Python virtual environment for your session.

---

## Notes
- Always use the full path to the Python executable for consistent results.
- For audit and reporting, use the Sovereign_Audit_Procedure.py script.
- Update this README as you add new scripts or commands.

---

**Prepared for: Sarah Hypervisor & Sovereign System Operations**
