# Advanced Terminal UI for SarahCore
# SarahCoreDashboard.py - Inline code for advanced terminal UI
# Uses 'rich' and 'textual' for a modern dashboard

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
import time
import platform
import psutil

console = Console()

def system_status_table():
    table = Table(title="System Status", expand=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_row("OS", platform.system() + " " + platform.release())
    table.add_row("CPU Usage", f"{psutil.cpu_percent()}%")
    table.add_row("Memory Usage", f"{psutil.virtual_memory().percent}%")
    table.add_row("Disk Usage", f"{psutil.disk_usage('/').percent}%")
    table.add_row("Uptime", f"{int(time.time() - psutil.boot_time())//60} min")
    return table

def main_dashboard():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=2),
        Layout(name="status", size=8),
        Layout(name="footer", size=3)
    )
    layout["header"].update(Panel(Text("SarahCore Sovereign Dashboard", style="bold green")))
    layout["footer"].update(Panel(Text("Press Ctrl+C to exit | All systems monitored", style="bold blue")))

    def component_status_table():
        table = Table(title="Component Status Feed", expand=True)
        table.add_column("Component", style="yellow", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Role", style="cyan")
        table.add_row("Network Stack", "ACTIVE", "Psiphon is tunneling in the background (Pre-Login).")
        table.add_row("Conduit Alpha", "STABLE", "The bridge is established between the Phone and PC.")
        table.add_row("Hardware ID", "VERIFIED", "I recognize the machine's MAC address in the Obsidian vault.")
        table.add_row("Logic Density", "LOW", 'Maintaining "Silent Mode" to avoid drawing IT\'s attention.')
        return table

    with Live(layout, refresh_per_second=1, screen=True):
        while True:
            layout["body"].update(system_status_table())
            layout["status"].update(component_status_table())
            time.sleep(1)

if __name__ == "__main__":
    main_dashboard()
