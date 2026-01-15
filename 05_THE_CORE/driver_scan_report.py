import subprocess
import json

def scan_drivers():
    print("Scanning for installed drivers...")
    # Use PowerShell to get driver info
    ps_cmd = (
        'Get-WmiObject Win32_PnPSignedDriver | '
        'Select-Object DeviceName, DriverVersion, DriverDate, Manufacturer | '
        'ConvertTo-Json'
    )
    result = subprocess.run([
        'powershell', '-Command', ps_cmd
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error scanning drivers.")
        return
    try:
        drivers = json.loads(result.stdout)
    except Exception as e:
        print("Error parsing driver info:", e)
        return
    print(f"Found {len(drivers)} drivers.")
    outdated = []
    for drv in drivers:
        # Example: flag drivers older than 2023-01-01
        try:
            date = drv['DriverDate']
            if date < '2023-01-01':
                outdated.append(drv)
        except:
            continue
    print(f"Outdated drivers: {len(outdated)}")
    for drv in outdated:
        print(f"Device: {drv['DeviceName']} | Version: {drv['DriverVersion']} | Date: {drv['DriverDate']} | Manufacturer: {drv['Manufacturer']}")
    print("\nReview these drivers and update from official sources if needed.")

if __name__ == "__main__":
    scan_drivers()
