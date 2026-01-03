import webbrowser
import threading
import requests
import sys
from pathlib import Path

try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
except ImportError:
    print("Missing dependencies: pystray, pillow. Install with: pip install pystray pillow")
    sys.exit(1)

API_BASE = "http://127.0.0.1:8000"
DASH_URL = f"{API_BASE}/ui"


def create_image():
    # Simple blue circle icon
    img = Image.new("RGB", (64, 64), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((8, 8, 56, 56), fill=(59, 130, 246))
    d.ellipse((18, 18, 46, 46), fill=(255, 255, 255))
    return img


def open_dashboard(icon, item):
    webbrowser.open(DASH_URL)


def send_command(cmd: str):
    try:
        r = requests.post(f"{API_BASE}/command", json={"command": cmd}, timeout=5)
        if r.ok:
            return r.json()
        else:
            return {"error": r.text}
    except Exception as e:
        return {"error": str(e)}


def quick_command(icon, item, cmd):
    send_command(cmd)


def quit_app(icon, item):
    icon.stop()


def build_menu():
    return (
        item("Open Dashboard", open_dashboard),
        item("Begin Linux Assimilation", lambda icon, i: quick_command(icon, i, "Begin Linux Assimilation")),
        item("List USB", lambda icon, i: quick_command(icon, i, "list usb devices")),
        item("Refresh Handshake", lambda icon, i: quick_command(icon, i, "platform bridge status")),
        item("Quit", quit_app),
    )


def main():
    icon = pystray.Icon("SarahPrime", create_image(), "Sarah Prime", menu=pystray.Menu(*build_menu()))
    icon.run()


if __name__ == "__main__":
    main()
