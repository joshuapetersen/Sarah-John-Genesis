import subprocess

def run_powershell(cmd):
    """Run a PowerShell command and return its output."""
    try:
        result = subprocess.run([
            'powershell', '-Command', cmd
        ], capture_output=True, text=True)
        print(f"PS> {cmd}")
        print(result.stdout)
        if result.stderr:
            print("[stderr]", result.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running PowerShell command: {e}")
        return -1

def interactive_shell():
    print("Genesis PowerShell Terminal (Local Only). Type 'exit' to quit.")
    while True:
        cmd = input("genesis-ps> ")
        if cmd.strip().lower() in ("exit", "quit"):
            print("Exiting Genesis PowerShell terminal.")
            break
        run_powershell(cmd)

if __name__ == "__main__":
    interactive_shell()
