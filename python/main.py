#!/usr/bin/env python3

import sys


def main() -> None:
    print("Hello from Python on Windows!")
    print(f"Python: {sys.version.split()[0]}")

    # Optional: demonstrate an HTTP call if 'requests' is installed
    try:
        import requests  # type: ignore
        print(f"requests: {requests.__version__}")
        try:
            r = requests.get("https://httpbin.org/get", timeout=5)
            print(f"HTTP GET ok: {r.status_code}")
        except Exception:
            # Network issues are fine; the script still works
            pass
    except Exception:
        print("requests not installed yet (that's okay).")


if __name__ == "__main__":
    main()
