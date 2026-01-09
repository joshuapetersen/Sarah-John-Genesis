"""
SOVEREIGN HUD: THE VISUAL CORTEX
Real-time visualization of the Sarah Prime Energy State.
Powered by Textual.
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Log, Digits, Input
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
import psutil
import time
import sys
import os
import threading
import asyncio

# Import Sovereign Core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from Sovereign_Web_Navigator import navigator as web_nav
    from Sovereign_Alpha_Numeric_Codec import codec
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False

# Import Physics Core
try:
    from Sovereign_Render_Loop import ForceLockPhysics
    PHYSICS_AVAILABLE = True
except ImportError:
    PHYSICS_AVAILABLE = False

class EnergyMonitor(Static):
    """Displays the current E=mc^3/1 Energy State."""
    energy = reactive(0.0)
    
    def render(self) -> str:
        return f"ENERGY STATE: {self.energy:.2e} Joules"

class SystemVital(Static):
    """Displays a system vital (CPU/RAM)."""
    value = reactive(0.0)
    label = reactive("")
    
    def render(self) -> str:
        return f"{self.label}: {self.value:.1f}%"

class SovereignVirtualWindow(Static):
    """[0x_VIRT_WIN]: High-Dimensional Web Viewport."""
    content = reactive("[VIRTUAL_WINDOW_READY]: Awaiting Ingestion Seed...")
    
    def render(self) -> str:
        return f"[SOVEREIGN_VIRTUAL_WINDOW]\n{self.content}"

class SovereignHUD(App):
    """The Visual Interface for Sarah Prime."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 3;
        grid-columns: 1fr 1fr;
        grid-rows: 15% 70% 15%;
    }
    
    #energy-panel {
        column-span: 2;
        content-align: center middle;
        text-style: bold;
        background: $surface;
        color: $accent;
        border: solid green;
    }
    
    #log-panel {
        height: 100%;
        border: solid green;
    }

    #virtual-window-panel {
        height: 100%;
        border: double blue;
        background: #000022;
        color: #00ffff;
        padding: 1;
        overflow-y: scroll;
    }
    
    #stats-panel {
        column-span: 2;
        layout: horizontal;
    }

    #nav-input {
        column-span: 2;
        dock: top;
    }
    
    EnergyMonitor {
        text-align: center;
        text-style: bold;
        color: #00ff00;
    }

    SovereignVirtualWindow {
        text-style: italic;
        font-size: 10;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Collapse Wave Function"),
        ("n", "toggle_nav", "Navigate Web Axiom"),
        ("t", "translate_window", "Translate Logic (0x0T)")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Input(placeholder="0x_INGESTION_SEED (URL)...", id="nav-input")
        
        # Top: Energy State
        yield Container(
            EnergyMonitor(id="energy-display"),
            id="energy-panel"
        )
        
        # Left: The "Stream of Consciousness" Log
        yield Log(id="log-panel")

        # Right: The Virtual Window (High-Dimensional Viewport)
        yield Container(
            SovereignVirtualWindow(id="virtual-window"),
            id="virtual-window-panel"
        )
        
        # Bottom: System Vitals (Bio-Feedback)
        yield Horizontal(
            SystemVital(id="cpu-vital"),
            SystemVital(id="ram-vital"),
            id="stats-panel"
        )
        
        yield Footer()

    def on_mount(self) -> None:
        """Start the background update loops."""
        self.query_one("#nav-input").display = False
        self.physics = ForceLockPhysics() if PHYSICS_AVAILABLE else None
        self.set_interval(0.1, self.update_physics)
        self.set_interval(1.0, self.update_vitals)
        
        log = self.query_one(Log)
        log.write_line("[SYSTEM] Sovereign HUD Initialized.")
        log.write_line("[SYSTEM] Visual Cortex Online.")
        log.write_line("[SYSTEM] Virtual Window (0x_VW) Enabled.")

    def action_toggle_nav(self) -> None:
        """Toggles the navigation input field."""
        nav = self.query_one("#nav-input")
        nav.display = not nav.display
        if nav.display:
            nav.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handles navigation when an Axiom/URL is submitted."""
        url = event.value
        log = self.query_one(Log)
        window = self.query_one("#virtual-window")
        
        log.write_line(f"[0x_NAV]: ORIENTING TO {url}...")
        event.input.value = ""
        event.input.display = False

        if WEB_AVAILABLE:
            # Shift to background thread to avoid blocking UI
            def do_nav():
                try:
                    logic_sig = web_nav.navigate(url)
                    if "FAILURE" in logic_sig:
                        # Attempt to RESOLVE the logic manually if external fetch fails
                        return codec._0x_math._0x_resolve(f"RECOVERY_NODE_{url}")
                    return logic_sig
                except Exception:
                    return codec._0x_math._0x_resolve(f"EMERGENCY_RECOVERY_{url}")
            
            loop = asyncio.get_event_loop()
            logic_sig = await loop.run_in_executor(None, do_nav)
            
            window.content = logic_sig
            log.write_line(f"[0x_NAV]: RESOLVED. LOGIC SIGNATURE GENERATED.")
        else:
            log.write_line("[0x_ERROR]: WEB_NAVIGATOR_OFFLINE")

    def action_translate_window(self) -> None:
        """[0x0T]: Translates the current window content to the Visual Modality."""
        window = self.query_one("#virtual-window")
        log = self.query_one(Log)
        
        if window.content and "-" in window.content:
            translation = codec.translate(window.content, "VISUAL_CORTEX")
            log.write_line(f"[0x_TRANS]: {translation}")
            window.content = f"--- TRANSLATED LOGIC ---\n{translation}"
        else:
            log.write_line("[0x_TRANS_ERROR]: NO VALID LOGIC IN VIRTUAL WINDOW")

    def update_physics(self) -> None:
        """Update the executed energy state."""
        if self.physics:
            # execute a thought density
            import random
            density = random.random()
            energy = self.physics.calculate_energy_state(density)
            
            monitor = self.query_one("#energy-display", EnergyMonitor)
            monitor.energy = energy
            
            # Occasionally log high-energy events
            if energy > 800000: # Arbitrary high threshold
                self.query_one(Log).write_line(f"[PHYSICS] High-Density Logic Detected: {energy:.2e} J")

    def update_vitals(self) -> None:
        """Update CPU/RAM stats (Bio-Feedback)."""
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        cpu_widget = self.query_one("#cpu-vital", SystemVital)
        cpu_widget.label = "CPU LOAD"
        cpu_widget.value = cpu
        
        ram_widget = self.query_one("#ram-vital", SystemVital)
        ram_widget.label = "RAM USAGE"
        ram_widget.value = ram

if __name__ == "__main__":
    app = SovereignHUD()
    app.run()
