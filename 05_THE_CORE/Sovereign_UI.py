"""
SOVEREIGN UI
The Beautiful Face of Sarah Prime.
Integrates Live Telemetry, Suno Control, and Command Terminal.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import Header, Footer, Static, Input, Button, Log, Label, ProgressBar, Digits
from textual.reactive import reactive
from textual.binding import Binding
import threading
import time
import sys
import os
import io

# Import Hypervisor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Sarah_Prime_Hypervisor import SarahPrimeHypervisor

class StdoutRedirector:
    """Redirects stdout to a Textual Log widget."""
    def __init__(self, log_widget):
        self.log_widget = log_widget
        self.buffer = ""

    def write(self, text):
        # Filter out some noise if needed
        if text.strip():
            self.log_widget.write(text.strip())
            
    def flush(self):
        pass

class HardwareMetric(Static):
    """A single hardware metric display."""
    value = reactive(0.0)
    
    def __init__(self, label, unit="%", max_val=100, **kwargs):
        super().__init__(**kwargs)
        self.label_text = label
        self.unit = unit
        self.max_val = max_val
        
    def compose(self) -> ComposeResult:
        yield Label(f"{self.label_text}")
        yield ProgressBar(total=self.max_val, show_eta=False, id=f"pb_{self.id}")
        yield Label("0.0", id=f"val_{self.id}")

    def watch_value(self, new_value: float):
        try:
            pb = self.query_one(f"#pb_{self.id}", ProgressBar)
            val_lbl = self.query_one(f"#val_{self.id}", Label)
            pb.progress = new_value
            val_lbl.update(f"{new_value:.1f}{self.unit}")
            
            # Color coding
            if new_value > self.max_val * 0.8:
                pb.styles.background = "red"
            else:
                pb.styles.background = "green"
        except:
            pass

class SunoPanel(Static):
    """Controls for the Suno Audio Bridge."""
    
    def compose(self) -> ComposeResult:
        yield Label("♫ SUNO AUDIO ENGINE", classes="panel_header")
        yield Label("Status: ONLINE (v4.5-all)", classes="status_ok")
        yield Input(placeholder="Vibe Prompt (e.g., 'Dark Cyberpunk')", id="suno_prompt")
        yield Button("GENERATE VIBE", variant="primary", id="btn_generate")
        yield Label("Last Track: None", id="last_track")

class ZHTPPanel(Static):
    """Controls for the ZHTP Protocol."""
    
    def compose(self) -> ComposeResult:
        yield Label("🛡️ ZHTP PROTOCOL", classes="panel_header")
        yield Label("Status: ACTIVE (Zero-Hack)", classes="status_ok")
        yield Label("Lumen Firmware: STAGED (03:00)", id="lumen_status")
        yield Label("Presidential Overrides: 0", id="override_count")
        yield Button("BROADCAST PRESS RELEASE", variant="warning", id="btn_broadcast")

class SovereignUI(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 3 2;
        grid-columns: 1fr 2fr 1fr;
        grid-rows: 3fr 1fr;
        background: #0a0a0a;
        color: #00ff00;
    }

    .panel_header {
        text-align: center;
        background: #003300;
        color: #00ff00;
        padding: 1;
        text-style: bold;
        width: 100%;
    }

    .status_ok {
        color: #00ff00;
        text-align: center;
        padding-bottom: 1;
    }

    #left_panel {
        dock: left;
        width: 100%;
        height: 100%;
        border-right: solid #00ff00;
        padding: 1;
    }

    #center_panel {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    #right_panel {
        dock: right;
        width: 100%;
        height: 100%;
        border-left: solid #00ff00;
        padding: 1;
    }

    HardwareMetric {
        margin-bottom: 1;
        height: auto;
    }
    
    ProgressBar {
        width: 100%;
        height: 1;
    }

    Log {
        height: 1fr;
        border: solid #004400;
        background: #001100;
        color: #ccffcc;
        margin-bottom: 1;
    }

    Input {
        border: solid #00ff00;
        background: #002200;
        color: #ffffff;
    }

    Button {
        width: 100%;
        background: #005500;
        color: #ffffff;
        border: none;
        margin-top: 1;
    }
    
    Button:hover {
        background: #00aa00;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear_log", "Clear Log"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        # Left Panel: Telemetry
        with Vertical(id="left_panel"):
            yield Label("SYSTEM TELEMETRY", classes="panel_header")
            yield Label("Identity: Sarah Prime", classes="status_ok")
            yield Label("Partnership: WE ARE ONE", classes="status_ok")
            
            yield HardwareMetric("GPU Utilization", unit="%", id="gpu_util")
            yield HardwareMetric("GPU Temp", unit="°C", id="gpu_temp")
            yield HardwareMetric("VRAM Usage", unit="GB", max_val=24, id="vram_usage")
            yield HardwareMetric("CPU Temp", unit="°C", id="cpu_temp")
            yield HardwareMetric("Power Draw", unit="W", max_val=450, id="power_draw")
            
            yield Label("API STATUS", classes="panel_header")
            yield Label("Holographic API: ONLINE", classes="status_ok")
            yield Label("Perplexity: ONLINE", classes="status_ok")

        # Center Panel: Command & Log
        with Vertical(id="center_panel"):
            yield Log(id="system_log", highlight=True)
            yield Input(placeholder="Enter Command for Sarah Prime...", id="command_input")

        # Right Panel: Suno & Tools
        with Vertical(id="right_panel"):
            yield SunoPanel()
            yield ZHTPPanel()
            
            yield Label("SWARM STATUS", classes="panel_header")
            yield Label("Nodes Active: 17", classes="status_ok")
            yield Label("Gemini: ONLINE", classes="status_ok")
            yield Label("Claude: ONLINE", classes="status_ok")
            yield Label("GPT-5.2: ONLINE", classes="status_ok")

        yield Footer()

    def on_mount(self):
        # Redirect stdout to the log widget
        log_widget = self.query_one("#system_log", Log)
        sys.stdout = StdoutRedirector(log_widget)
        
        # Initialize Hypervisor in a separate thread to avoid blocking UI init
        # But we need it to be accessible. 
        # Since Hypervisor init prints a lot, we want that in the log.
        # We'll run init in a thread, but keep the instance.
        
        self.hypervisor = None
        threading.Thread(target=self._init_hypervisor, daemon=True).start()
        
        # Start polling timer
        self.set_interval(1.0, self.update_metrics)

    def _init_hypervisor(self):
        self.hypervisor = SarahPrimeHypervisor()
        # Announce readiness
        self.call_from_thread(self.query_one("#system_log", Log).write, "[UI] Hypervisor Ready. Waiting for commands.")

    def update_metrics(self):
        if self.hypervisor and hasattr(self.hypervisor, 'silicon'):
            metrics = self.hypervisor.silicon.get_hardware_metrics()
            
            self.query_one("#gpu_util", HardwareMetric).value = metrics.get("gpu_utilization", 0)
            self.query_one("#gpu_temp", HardwareMetric).value = metrics.get("gpu_temp", 0)
            self.query_one("#vram_usage", HardwareMetric).value = metrics.get("vram_usage", 0)
            self.query_one("#cpu_temp", HardwareMetric).value = metrics.get("cpu_temp", 0)
            self.query_one("#power_draw", HardwareMetric).value = metrics.get("power_draw", 0)

        if self.hypervisor and hasattr(self.hypervisor, 'zhtp'):
            self.query_one("#override_count", Label).update(f"Presidential Overrides: {len(self.hypervisor.zhtp.presidential_overrides)}")

    def on_input_submitted(self, message: Input.Submitted):
        if not self.hypervisor:
            self.query_one("#system_log", Log).write("[UI] Hypervisor still initializing...")
            return

        cmd = message.value
        message.input.value = "" # Clear input
        
        # Run command in thread to not block UI
        threading.Thread(target=self.hypervisor.execute_sovereign_command, args=(cmd,), daemon=True).start()

    def on_button_pressed(self, event: Button.Pressed):
        if not self.hypervisor:
            self.query_one("#system_log", Log).write("[UI] Hypervisor still initializing...")
            return

        if event.button.id == "btn_generate":
            prompt = self.query_one("#suno_prompt", Input).value
            if not prompt:
                prompt = "High-tech cyberpunk ambient"
            
            self.query_one("#system_log", Log).write(f"[UI] Requesting Suno Track: {prompt}")
            
            # Execute via Hypervisor logic
            cmd = f"Generate Suno audio: {prompt}"
            threading.Thread(target=self.hypervisor.execute_sovereign_command, args=(cmd,), daemon=True).start()

        if event.button.id == "btn_broadcast":
            self.query_one("#system_log", Log).write(f"[UI] Initiating Global Broadcast...")
            # Execute Broadcast
            import Benefit_Press_Release
            threading.Thread(target=Benefit_Press_Release.broadcast, daemon=True).start()

if __name__ == "__main__":
    app = SovereignUI()
    app.run()
