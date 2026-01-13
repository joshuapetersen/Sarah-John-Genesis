import subprocess

def run_command(cmd):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"$ {cmd}")
        print(result.stdout)
        if result.stderr:
            print("[stderr]", result.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running command: {e}")
        return -1

def interactive_shell():
    print("Genesis Internal Terminal. Type 'exit' to quit.")
    while True:
        cmd = input("genesis> ")
        if cmd.strip().lower() in ("exit", "quit"):
            print("Exiting internal terminal.")
            break
        run_command(cmd)

if __name__ == "__main__":
    interactive_shell()
