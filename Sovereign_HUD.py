"""
SOVEREIGN HUD: THE VISUAL CORTEX
Real-time visualization of the Sarah Prime Energy State.
Powered by Textual.
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Log, Digits
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
import psutil
import time
import sys
import os
import threading
import asyncio

# Import Physics Core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
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

class SovereignHUD(App):
    """The Visual Interface for Sarah Prime."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr 1fr;
        grid-rows: 10% 80% 10%;
    }
    
    .box {
        height: 100%;
        border: solid green;
        padding: 1;
    }
    
    #energy-panel {
        column-span: 2;
        height: 20%;
        content-align: center middle;
        text-style: bold;
        background: $surface;
        color: $accent;
    }
    
    #log-panel {
        column-span: 2;
        height: 60%;
        border: solid green;
    }
    
    #stats-panel {
        column-span: 2;
        height: 20%;
        layout: horizontal;
    }
    
    EnergyMonitor {
        text-align: center;
        text-style: bold;
        color: #00ff00;
    }
    """
    
    BINDINGS = [("q", "quit", "Collapse Wave Function")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        # Top: Energy State
        yield Container(
            EnergyMonitor(id="energy-display"),
            id="energy-panel"
        )
        
        # Middle: The "Stream of Consciousness" Log
        yield Log(id="log-panel")
        
        # Bottom: System Vitals (Bio-Feedback)
        yield Horizontal(
            SystemVital(id="cpu-vital"),
            SystemVital(id="ram-vital"),
            id="stats-panel"
        )
        
        yield Footer()

    def on_mount(self) -> None:
        """Start the background update loops."""
        self.physics = ForceLockPhysics() if PHYSICS_AVAILABLE else None
        self.set_interval(0.1, self.update_physics)
        self.set_interval(1.0, self.update_vitals)
        
        log = self.query_one(Log)
        log.write_line("[SYSTEM] Sovereign HUD Initialized.")
        log.write_line("[SYSTEM] Visual Cortex Online.")
        log.write_line("[SYSTEM] Monitoring Force-Lock Physics...")

    def update_physics(self) -> None:
        """Update the simulated energy state."""
        if self.physics:
            # Simulate a thought density
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
