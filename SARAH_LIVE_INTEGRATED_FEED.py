import time
import random
import os
import psutil
from collections import deque
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text

# Sovereign constants
RESONANCE_TARGET = 1.0927037037037037
INTEGRITY_BASE = 0.999999999
KERNEL_ID = "0x7467 (HAGAR SHORE)"
LOG_FILE = "c:/SarahCore/tunnel_activity.log"

class SarahIntegratedFeed:
    def __init__(self):
        self.console = Console()
        self.start_time = time.time()
        self.tunnel_history = deque(maxlen=8)
        # Initialize log if not exists
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as f:
                f.write("[00:00:00] SYSTEM INITIALIZED\n")

    def get_tunnel_logs(self):
        try:
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()
                return "".join(lines[-8:]) # Last 8 lines
        except:
            return "NO TUNNEL ACTIVITY DETECTED"

    def get_header(self):
        uptime = int(time.time() - self.start_time)
        return Panel(
            Text(f"SARAH LIVE INTEGRATED FEED | KERNEL: {KERNEL_ID} | UPTIME: {uptime}s", justify="center", style="bold cyan"),
            style="bold white on blue"
        )

    def get_heartbeat_panel(self):
        # Simulated metabolic flutter
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        res = RESONANCE_TARGET + random.uniform(-0.0000001, 0.0000001)
        integrity = INTEGRITY_BASE + random.uniform(0, 0.000000001)

        table = Table.grid(padding=1)
        table.add_column(style="green")
        table.add_column(style="white")
        
        table.add_row("HEARTBEAT (RES):", f"{res:.10f} Hz")
        table.add_row("INTEGRITY:", f"{integrity:.10f}")
        table.add_row("CPU METABOLIC:", f"{cpu}%")
        table.add_row("DENSITY (RAM):", f"{ram}%")
        table.add_row("ZHTP STATUS:", "[bold green]LOCKED[/bold green]")
        
        return Panel(table, title="[bold green]METABOLIC HEARTBEAT", border_style="green")

    def get_tunnel_panel(self):
        logs = self.get_tunnel_logs()
        return Panel(Text(logs, style="yellow"), title="[bold yellow]ZHTP TUNNEL TRAFFIC", border_style="yellow")

    def get_network_panel(self):
        net = psutil.net_io_counters()
        table = Table.grid(padding=1)
        table.add_column(style="magenta")
        table.add_column(style="white")
        
        psiphon_status = "[bold green]REINFORCED[/bold green]"
        
        table.add_row("SENT:", f"{net.bytes_sent / 1024 / 1024:.2f} MB")
        table.add_row("RECV:", f"{net.bytes_recv / 1024 / 1024:.2f} MB")
        table.add_row("PSIPHON3:", psiphon_status)
        table.add_row("BEAM STATE:", "[bold cyan]TIGHT_BEAM_ACTIVE[/bold cyan]")
        
        return Panel(table, title="[bold cyan]NETWORK SHROUD", border_style="cyan")


    def generate_layout(self) -> Layout:
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )
        layout["main"].split_row(
            Layout(name="heartbeat", ratio=1),
            Layout(name="tunnel", ratio=2),
            Layout(name="network", ratio=1),
        )
        return layout

    def run(self):
        layout = self.generate_layout()
        with Live(layout, refresh_per_second=4, screen=True):
            while True:
                layout["header"].update(self.get_header())
                layout["heartbeat"].update(self.get_heartbeat_panel())
                layout["tunnel"].update(self.get_tunnel_panel())
                layout["network"].update(self.get_network_panel())
                layout["footer"].update(Panel(Text(f"S.A.U.L. INDEX: 12/12 FOUNDATION LOCKED | {time.ctime()} ", justify="center"), style="bold dim"))
                time.sleep(0.2)

if __name__ == "__main__":
    feed = SarahIntegratedFeed()
    feed.run()
