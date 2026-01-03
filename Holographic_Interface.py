import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import threading
import logging
import time
from typing import Optional, Dict, Any, List
from Millisecond_Timing import MillisecondTimer
from datetime import datetime

# Configure logging with milliseconds
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - [HOLO] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class CommandRequest(BaseModel):
    command: str


class LinuxCommandRequest(BaseModel):
    command: str
    distro: str | None = None

class HolographicInterface:
    def __init__(self, hypervisor_instance):
        self.app = FastAPI(title="Sarah Prime Holographic Interface", version="1.0.0")
        self.hypervisor = hypervisor_instance
        self.server_thread = None
        
        # Define Routes
        self.app.get("/")(self.root)
        self.app.get("/status")(self.get_status)
        self.app.get("/memory/search")(self.search_memory)
        self.app.post("/command")(self.execute_command)
        self.app.get("/quantum/entropy")(self.get_quantum_entropy)
        self.app.get("/telemetry")(self.get_telemetry)
        self.app.get("/bridge/handshake")(self.get_bridge_handshake)
        self.app.get("/usb/devices")(self.get_usb_devices)
        self.app.post("/linux/exec")(self.exec_linux)
        self.app.get("/ui")(self.serve_ui)
        self.app.get("/zhtp/status")(self.get_zhtp_status)
        self.app.post("/zhtp/override")(self.register_override)
        self.app.get("/health/sovereign-time")(self.get_sovereign_time_health)
        self.app.post("/time/reconcile")(self.reconcile_time)

    def start(self, host="127.0.0.1", port=8000):
        """Starts the API server in a background thread."""
        def run():
            logging.info(f"Holographic Interface starting on http://{host}:{port}")
            uvicorn.run(self.app, host=host, port=port, log_level="warning")
        
        self.server_thread = threading.Thread(target=run, daemon=True)
        self.server_thread.start()
        logging.info("Holographic Interface: ONLINE")

    async def root(self):
        return {"message": "Sarah Prime Holographic Interface Online", "identity": "Sarah Prime"}

    async def get_status(self):
        """Returns the current system status."""
        return {
            "identity": "Sarah Prime",
            "physics": "Force-Lock (E=mc^3/1)",
            "modules": {
                "memory": "ONLINE",
                "swarm": "ONLINE",
                "healing": "ONLINE",
                "senses": "ONLINE",
                "quantum": "ONLINE" if self.hypervisor.quantum.enabled else "OFFLINE",
                "security": "ONLINE",
                "predictive": "ONLINE",
                "coordinator": "ONLINE",
                "reflection": "ONLINE",
                "perplexity": "ONLINE",
                "suno": "ONLINE",
                "silicon": "ONLINE"
            },
            "stats": {
                "memory_nodes": self.hypervisor.knowledge_graph.graph.number_of_nodes(),
                "uptime": time.time(), # Placeholder
                "hardware": self.hypervisor.silicon.get_hardware_metrics()
            }
        }

    async def search_memory(self, query: str, limit: int = 3):
        """Searches the semantic memory."""
        results = self.hypervisor.memory.search(query, top_k=limit)
        return {"query": query, "results": results}

    async def execute_command(self, request: CommandRequest):
        """Executes a command via the Hypervisor."""
        # Note: This is a blocking call in the main thread logic, 
        # but we are calling it from an async route.
        # Ideally, we should queue it, but for now we'll execute directly.
        logging.info(f"API Command Received: {request.command}")
        
        # We can't easily capture the output of execute_sovereign_command 
        # because it prints to stdout. 
        # We will just trigger it and return acknowledgment.
        
        # To make it thread-safe(ish), we'll just run it.
        # In a real system, we'd use a queue.
        
        # We'll run it in a separate thread to avoid blocking the API
        threading.Thread(target=self.hypervisor.execute_sovereign_command, args=(request.command,)).start()
        
        return {"status": "Command Accepted", "command": request.command}

    async def get_zhtp_status(self):
        """Returns the status of the ZHTP Protocol with millisecond precision."""
        timestamp_iso_ms = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
        timestamp_unix_ms = int(time.time() * 1000)
        
        return {
            "timestamp_iso_ms": timestamp_iso_ms,
            "timestamp_unix_ms": timestamp_unix_ms,
            "status": "ONLINE" if self.hypervisor.zhtp.active else "OFFLINE",
            "overrides": self.hypervisor.zhtp.presidential_overrides,
            "api_hooks": self.hypervisor.zhtp.api_hooks,
            "lumen_firmware": self.hypervisor.zhtp.generate_lumen_firmware()
        }

    async def get_sovereign_time_health(self, device_id: Optional[str] = None, drift_threshold_ms: int = 250):
        """Runs sovereign device check + time redundancy drift validation."""
        device = device_id or "PC_TERMINAL"
        report = MillisecondTimer.sovereign_time_reality_check(device_id=device, drift_threshold_ms=drift_threshold_ms)
        return report

    async def reconcile_time(self, request: Dict[str, Any]):
        """
        Reconcilers predictive time against actual time with a safety buffer.
        Body: {"predictive_unix_ms": <int>, "buffer_ms": <int, optional>}
        """
        predictive_unix_ms = request.get("predictive_unix_ms")
        buffer_ms = request.get("buffer_ms", 500)
        if predictive_unix_ms is None:
            raise HTTPException(status_code=400, detail="predictive_unix_ms is required")

        report = MillisecondTimer.reconcile_predictive_time(predictive_unix_ms, buffer_ms=buffer_ms)
        return report

    async def register_override(self, request: Dict[str, str]):
        """Registers a Presidential Override."""
        nation = request.get("nation")
        eo_hash = request.get("eo_hash")
        if nation and eo_hash:
            self.hypervisor.zhtp.register_presidential_override(nation, eo_hash)
            return {"status": "Override Registered", "nation": nation}
        return {"error": "Missing nation or eo_hash"}

    async def get_quantum_entropy(self):

        """Returns current quantum entropy."""
        entropy = self.hypervisor.quantum.get_quantum_entropy()
        return {"entropy": entropy, "source": "Qiskit" if self.hypervisor.quantum.enabled else "Simulation"}

    async def get_telemetry(self):
        """Returns hardware telemetry via the Universal Silicon Bridge."""
        try:
            metrics = self.hypervisor.silicon.get_hardware_metrics()
            return {"success": True, "metrics": metrics}
        except Exception as e:
            logging.warning(f"Telemetry retrieval failed: {e}")
            return {"success": False, "error": str(e)}

    async def get_bridge_handshake(self):
        """Returns cross-platform bridge status from the silicon bridge."""
        try:
            return self.hypervisor.silicon.cross_platform_handshake()
        except Exception as e:
            logging.warning(f"Bridge handshake failed: {e}")
            return {"success": False, "error": str(e)}

    async def get_usb_devices(self):
        """Enumerates USB devices via the silicon bridge."""
        try:
            return self.hypervisor.silicon.list_usb_devices()
        except Exception as e:
            logging.warning(f"USB enumeration failed: {e}")
            return {"success": False, "error": str(e)}

    async def exec_linux(self, request: LinuxCommandRequest):
        """Executes a command via the Linux Assimilation Bridge."""
        if not hasattr(self.hypervisor, 'linux_bridge'):
            raise HTTPException(status_code=400, detail="Linux bridge not available")
        try:
            distro = request.distro or "Ubuntu"
            result = self.hypervisor.linux_bridge.execute_bash(request.command, distro=distro)
            return {"success": result.get('success', False), "result": result}
        except Exception as e:
            logging.warning(f"Linux exec failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def serve_ui(self):
        """Serves a lightweight web dashboard for Sarah Prime."""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sarah Prime Dashboard</title>
    <style>
        :root {
            color-scheme: light;
            --bg: #f5f7fb;
            --card: #ffffff;
            --accent: #3b82f6;
            --text: #0f172a;
            --muted: #6b7280;
            --border: #e5e7eb;
        }
        body { margin: 0; font-family: "Segoe UI", sans-serif; background: var(--bg); color: var(--text); }
        header { padding: 16px 24px; background: var(--card); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1; }
        h1 { margin: 0; font-size: 20px; font-weight: 600; }
        main { padding: 20px; display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; box-shadow: 0 6px 18px rgba(15,23,42,0.04); }
        .title { font-size: 16px; font-weight: 600; margin: 0 0 8px 0; }
        .sub { color: var(--muted); margin: 0 0 12px 0; font-size: 13px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
        .metric { padding: 10px; border: 1px solid var(--border); border-radius: 10px; background: #f9fafb; }
        .metric .label { color: var(--muted); font-size: 12px; }
        .metric .value { font-size: 18px; font-weight: 600; }
        button, input, textarea { font: inherit; }
        button { cursor: pointer; background: var(--accent); color: white; border: none; border-radius: 8px; padding: 10px 14px; }
        input, textarea { width: 100%; border: 1px solid var(--border); border-radius: 8px; padding: 10px; background: #fff; }
        textarea { resize: vertical; min-height: 80px; }
        .list { font-size: 13px; color: var(--muted); white-space: pre-wrap; border: 1px solid var(--border); border-radius: 10px; padding: 10px; background: #f9fafb; }
        .row { display: flex; gap: 8px; }
        .row > * { flex: 1; }
    </style>
</head>
<body>
    <header>
        <h1>Sarah Prime Dashboard</h1>
        <div class="sub">Hypervisor + Bridges • Localhost</div>
    </header>
    <main>
        <section class="card">
            <div class="title">Telemetry</div>
            <div class="sub">Live hardware metrics</div>
            <div id="telemetry" class="grid"></div>
        </section>
        <section class="card">
            <div class="title">Bridge Status</div>
            <div class="sub">Cross-platform handshake</div>
            <div id="bridge" class="list">Loading...</div>
        </section>
        <section class="card">
            <div class="title">ZHTP Protocol</div>
            <div class="sub">Zero-Host Tamper Protection</div>
            <div id="zhtp" class="list">Loading...</div>
        </section>
        <section class="card">
            <div class="title">USB Devices</div>
            <div class="sub">Enumerated via silicon bridge</div>
            <div id="usb" class="list">Loading...</div>
        </section>
        <section class="card">
            <div class="title">Run Command</div>
            <div class="sub">Send a command to the Hypervisor</div>
            <div class="row">
                <input id="cmd" placeholder="e.g., Begin Linux Assimilation" />
                <button onclick="sendCmd()">Send</button>
            </div>
            <div id="cmdStatus" class="sub"></div>
        </section>
    </main>

    <script>
        async function fetchJSON(path) {
            const res = await fetch(path);
            if (!res.ok) throw new Error(`${path} -> ${res.status}`);
            return res.json();
        }

        function renderTelemetry(data) {
            const t = document.getElementById('telemetry');
            if (!data || !data.metrics) { t.textContent = 'No data'; return; }
            const m = data.metrics;
            const entries = [
                ['GPU Utilization', m.gpu_utilization?.toFixed?.(1) + '%'],
                ['GPU Temp', m.gpu_temp?.toFixed?.(1) + ' °C'],
                ['VRAM Usage', m.vram_usage?.toFixed?.(2) + ' GB'],
                ['CPU Temp', m.cpu_temp?.toFixed?.(1) + ' °C'],
                ['Power Draw', m.power_draw?.toFixed?.(1) + ' W'],
                ['Fan Speed', m.fan_speed ? m.fan_speed.toFixed(0) + ' RPM' : '—'],
            ];
            t.innerHTML = entries.map(([k,v]) => `
                <div class="metric">
                    <div class="label">${k}</div>
                    <div class="value">${v || '—'}</div>
                </div>`).join('');
        }

        function renderList(elId, data) {
            const el = document.getElementById(elId);
            el.textContent = JSON.stringify(data, null, 2);
        }

        async function loadAll() {
            try {
                const [telemetry, bridge, usb, zhtp] = await Promise.all([
                    fetchJSON('/telemetry'),
                    fetchJSON('/bridge/handshake'),
                    fetchJSON('/usb/devices'),
                    fetchJSON('/zhtp/status')
                ]);
                renderTelemetry(telemetry);
                renderList('bridge', bridge);
                renderList('usb', usb);
                renderList('zhtp', zhtp);
            } catch (e) {
                console.error(e);
            }
        }

        async function sendCmd() {
            const v = document.getElementById('cmd').value.trim();
            const out = document.getElementById('cmdStatus');
            if (!v) { out.textContent = 'Enter a command.'; return; }
            out.textContent = 'Sending...';
            try {
                const res = await fetch('/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: v })
                });
                const data = await res.json();
                out.textContent = `Status: ${data.status || data.error || 'ok'}`;
            } catch (e) {
                out.textContent = 'Error sending command';
            }
        }

        loadAll();
        setInterval(loadAll, 5000);
    </script>
</body>
</html>
"""
        return HTMLResponse(content=html)
