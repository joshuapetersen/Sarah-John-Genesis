import subprocess
import platform
import shutil

def get_cpu():
    return platform.processor()

def get_ram():
    try:
        import psutil
        return f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
    except ImportError:
        return "psutil not installed"

def get_disk():
    total, used, free = shutil.disk_usage("/")
    return f"Total: {total // (2**30)} GB, Free: {free // (2**30)} GB"

def get_os():
    return platform.platform()

def main():
    print("Genesis System Spec Check:\n")
    print(f"CPU: {get_cpu()}")
    print(f"RAM: {get_ram()}")
    print(f"Disk: {get_disk()}")
    print(f"OS: {get_os()}")
    print("\nIf RAM shows 'psutil not installed', run 'pip install psutil' and re-run this script for full details.")

if __name__ == "__main__":
    main()
