import subprocess

def interpret_request(request):
    """Very basic mapping from natural language to PowerShell commands."""
    request = request.strip().lower()
    if request in ("list files", "show files", "what's here", "ls", "dir"):
        return "Get-ChildItem"
    if request in ("show processes", "list processes", "what's running"):
        return "Get-Process"
    if request.startswith("find file "):
        filename = request.replace("find file ", "").strip()
        return f"Get-ChildItem -Recurse -Filter {filename}"
    if request in ("system info", "show system info"):
        return "Get-ComputerInfo"
    if request in ("disk usage", "show disk usage"):
        return "Get-PSDrive"
    # Fallback: treat as direct PowerShell
    return request

def run_powershell(cmd):
    try:
        result = subprocess.run([
            'powershell', '-Command', cmd
        ], capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", f"Error: {e}"

def conversational_shell():
    print("Genesis Conversational Terminal (Two-Way, Local Only). Type 'exit' to quit.")
    context = ""
    while True:
        user_input = input("LTO> ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Exiting Genesis Conversational Terminal.")
            break
        ps_cmd = interpret_request(user_input)
        print(f"[Genesis] Executing: {ps_cmd}")
        stdout, stderr = run_powershell(ps_cmd)
        if stdout:
            print(f"[LTO]:\n{stdout}")
        if stderr:
            print(f"[LTO][error]:\n{stderr}")
        # Two-way: allow user to reply, clarify, or chain commands
        while True:
            followup = input("Reply, clarify, or new command (Enter to continue, 'exit' to quit): ")
            if followup.strip().lower() in ("exit", "quit"):
                print("Exiting Genesis Conversational Terminal.")
                return
            if followup.strip() == "":
                break
            ps_cmd = interpret_request(followup)
            print(f"[Genesis] Executing: {ps_cmd}")
            stdout, stderr = run_powershell(ps_cmd)
            if stdout:
                print(f"[LTO]:\n{stdout}")
            if stderr:
                print(f"[LTO][error]:\n{stderr}")

if __name__ == "__main__":
    conversational_shell()
