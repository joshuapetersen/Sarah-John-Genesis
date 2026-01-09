import requests
import os

def main():
    api_key = os.environ.get("GENESIS_API_KEY", "REPLACE_WITH_STRONG_KEY")
    url = "http://127.0.0.1:8765/terminal"
    print("Genesis Terminal Client. Type 'exit' to quit.")
    while True:
        cmd = input("$ ")
        if cmd.strip().lower() == "exit":
            break
        resp = requests.post(url, json={"cmd": cmd}, headers={"x-api-key": api_key})
        if resp.status_code == 200:
            out = resp.json()
            print(out.get("stdout", ""), end="")
            if out.get("stderr"):
                print(out["stderr"], end="")
        else:
            print(f"[ERROR] {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    main()
