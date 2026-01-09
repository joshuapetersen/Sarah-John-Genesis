import os
import sys

class SystemRootBridge:
    """
    Bridge for secure, programmatic access to the C:/ root directory.
    Provides basic directory listing, file read, and file write (with caution).
    """
    def __init__(self, root_path="C:/"):
        self.root_path = os.path.abspath(root_path)
        if not os.path.exists(self.root_path):
            raise FileNotFoundError(f"Root path {self.root_path} does not exist.")

    def list_dir(self, subdir=""):
        path = os.path.join(self.root_path, subdir)
        return os.listdir(path)

    def read_file(self, rel_path):
        path = os.path.join(self.root_path, rel_path)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def write_file(self, rel_path, content):
        path = os.path.join(self.root_path, rel_path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

if __name__ == "__main__":
    bridge = SystemRootBridge()
    print("--- SYSTEM ROOT BRIDGE ---")
    print("Listing C:/ directory:")
    for item in bridge.list_dir():
        print("-", item)
    # Example: Read a file (uncomment to use)
    # print(bridge.read_file("Windows/System32/drivers/etc/hosts"))
    # Example: Write a file (uncomment to use, be careful!)
    # bridge.write_file("test_bridge.txt", "Hello from Sarah bridge!")
    print("--- BRIDGE READY ---")
