import hashlib
import json
import logging
import os
import threading
import time
import uuid
import uvicorn
from datetime import datetime
from pathlib import Path
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Callable

import jwt  # type: ignore
from jwt import PyJWKClient  # type: ignore
import requests  # type: ignore
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST  # type: ignore

from Millisecond_Timing import MillisecondTimer

# Configure logging with milliseconds
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - [HOLO] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


REQUESTS_TOTAL = Counter('holo_requests_total', 'Total requests', ['endpoint', 'status'])
TIME_RECONCILE_TOTAL = Counter('holo_time_reconcile_total', 'Time reconciliation outcomes', ['authoritative'])
SOVEREIGN_HEALTH_TOTAL = Counter('holo_sovereign_health_total', 'Sovereign time health results', ['drift_ok', 'device_allowed'])


class Settings(BaseModel):
    api_keys: Dict[str, List[str]]  # key -> scopes
    api_key_header: str = "x-api-key"
    rate_limit_per_min: int = 60
    rate_limit_window_seconds: int = 60
    use_redis_rate_limit: bool = False
    redis_url: Optional[str] = None
    audit_log_path: Path = Path("integrity_logs/audit_log.jsonl")
    jwt_enabled: bool = False
    jwt_algorithms: List[str] = ["HS256"]
    jwt_secret: Optional[str] = None
    jwt_issuer: Optional[str] = None
    jwt_audience: Optional[str] = None
    jwt_jwks_url: Optional[str] = None

    @staticmethod
    def from_env() -> "Settings":
        raw_keys = os.getenv("SARAH_API_KEYS", "local-dev-key:admin|read|write")
        api_keys: Dict[str, List[str]] = {}
        # Expect semicolon-separated keys; each key scopes separated by |
        for part in raw_keys.split(';'):
            chunk = part.strip()
            if not chunk:
                continue
            if ':' in chunk:
                key, scopes_str = chunk.split(':', 1)
                scopes = [s.strip() for s in scopes_str.replace(',', '|').split('|') if s.strip()]
            else:
                key, scopes = chunk, ["admin", "read", "write"]
            api_keys[key] = scopes or ["admin", "read", "write"]

        return Settings(
            api_keys=api_keys,
            api_key_header=os.getenv("SARAH_API_KEY_HEADER", "x-api-key"),
            rate_limit_per_min=int(os.getenv("SARAH_RATE_LIMIT_PER_MIN", "60")),
            rate_limit_window_seconds=int(os.getenv("SARAH_RATE_LIMIT_WINDOW", "60")),
            use_redis_rate_limit=os.getenv("SARAH_RATE_LIMIT_REDIS", "false").lower() in {"1", "true", "yes"},
            redis_url=os.getenv("SARAH_REDIS_URL"),
            audit_log_path=Path(os.getenv("SARAH_AUDIT_LOG", "integrity_logs/audit_log.jsonl")),
            jwt_enabled=os.getenv("SARAH_JWT_ENABLED", "false").lower() in {"1", "true", "yes"},
            jwt_algorithms=[a.strip() for a in os.getenv("SARAH_JWT_ALGORITHMS", "HS256").split(',') if a.strip()],
            jwt_secret=os.getenv("SARAH_JWT_SECRET"),
            jwt_issuer=os.getenv("SARAH_JWT_ISSUER"),
            jwt_audience=os.getenv("SARAH_JWT_AUDIENCE"),
            jwt_jwks_url=os.getenv("SARAH_JWT_JWKS_URL"),
        )


class SimpleRateLimiter:
    """Naive in-memory fixed-window rate limiter keyed by client id."""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def check(self, client_id: str) -> None:
        now = time.time()
        with self._lock:
            window_start = now - self.window_seconds
            entries = [ts for ts in self._requests.get(client_id, []) if ts >= window_start]
            if len(entries) >= self.max_requests:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            entries.append(now)
            self._requests[client_id] = entries


class RedisRateLimiter:
    """Redis-backed fixed-window limiter; falls back to in-memory if Redis missing."""

    def __init__(self, redis_client, max_requests: int = 60, window_seconds: int = 60):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def check(self, client_id: str) -> None:
        key = f"rate:{client_id}:{int(time.time() // self.window_seconds)}"
        try:
            pipe = self.redis.pipeline()
            pipe.incr(key, 1)
            pipe.expire(key, self.window_seconds)
            count, _ = pipe.execute()
            if count > self.max_requests:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
        except Exception as exc:  # pragma: no cover - redis optional
            raise HTTPException(status_code=503, detail="Rate limiter unavailable") from exc


class AuditLogger:
    """Append-only audit logger with hash chaining."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _last_hash(self) -> str:
        if not self.path.exists():
            return "0" * 64
        try:
            with self.path.open("rb") as f:
                f.seek(0, os.SEEK_END)
                pos = f.tell()
                if pos == 0:
                    return "0" * 64
                # read last line
                while pos > 0:
                    pos -= 1
                    f.seek(pos)
                    if f.read(1) == b"\n" and pos != f.tell():
                        break
                line = f.readline().decode("utf-8").strip()
                if not line:
                    return "0" * 64
                obj = json.loads(line)
                return obj.get("hash", "0" * 64)
        except Exception:
            return "0" * 64

    def log(self, event: str, payload: Dict[str, Any]) -> None:
        entry = {
            "event": event,
            "timestamp": MillisecondTimer.get_iso_ms(),
            **payload,
        }
        last_hash = self._last_hash()
        entry_bytes = json.dumps(entry, sort_keys=True).encode("utf-8")
        entry_hash = hashlib.sha256(last_hash.encode("utf-8") + entry_bytes).hexdigest()
        entry["prev_hash"] = last_hash
        entry["hash"] = entry_hash

        line = json.dumps(entry)
        with self._lock:
            with self.path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")

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
        self.settings = Settings.from_env()
        self.api_keys = self.settings.api_keys
        self.api_key_header = self.settings.api_key_header
        self.rate_limiter = self._init_rate_limiter()
        self.audit_logger = AuditLogger(self.settings.audit_log_path)

        if "local-dev-key" in self.api_keys:
            logging.warning("SARAH_API_KEYS includes default local-dev-key. Replace with strong keys for production.")
        
        # Define Routes
        self.app.get("/")(self.root)
        self.app.get("/status", dependencies=[Depends(self.require_api_key_with_scope("read"))])(self.get_status)
        self.app.get("/memory/search", dependencies=[Depends(self.require_api_key_with_scope("read"))])(self.search_memory)
        self.app.post("/command", dependencies=[Depends(self.require_api_key_with_scope("write"))])(self.execute_command)
        self.app.get("/quantum/entropy", dependencies=[Depends(self.require_api_key_with_scope("read"))])(self.get_quantum_entropy)
        self.app.get("/telemetry")(self.get_telemetry)  # intentionally open for local dashboard
        self.app.get("/bridge/handshake")(self.get_bridge_handshake)
        self.app.get("/usb/devices", dependencies=[Depends(self.require_api_key_with_scope("read"))])(self.get_usb_devices)
        self.app.post("/linux/exec", dependencies=[Depends(self.require_api_key_with_scope("admin"))])(self.exec_linux)
        self.app.get("/ui")(self.serve_ui)
        self.app.get("/zhtp/status", dependencies=[Depends(self.require_api_key_with_scope("read"))])(self.get_zhtp_status)
        self.app.post("/zhtp/override", dependencies=[Depends(self.require_api_key_with_scope("admin"))])(self.register_override)
        self.app.get("/health/sovereign-time", dependencies=[Depends(self.require_api_key_with_scope("read"))])(self.get_sovereign_time_health)
        self.app.post("/time/reconcile", dependencies=[Depends(self.require_api_key_with_scope("write"))])(self.reconcile_time)
        
        # Google Drive Endpoints
        self.app.get("/drive/files", dependencies=[Depends(self.require_api_key_with_scope("read"))])(self.list_drive_files)
        self.app.get("/drive/read/{file_id}", dependencies=[Depends(self.require_api_key_with_scope("read"))])(self.read_drive_file)
        
        self.app.get("/metrics")(self.metrics)

    def start(self, host="127.0.0.1", port=8000):
        """Starts the API server in a background thread."""
        def run():
            logging.info(f"Holographic Interface starting on http://{host}:{port}")
            uvicorn.run(self.app, host=host, port=port, log_level="warning")
        
        self.server_thread = threading.Thread(target=run, daemon=True)
        self.server_thread.start()
        logging.info("Holographic Interface: ONLINE")

    async def metrics(self):
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    def _get_client_id(self, request: Request) -> str:
        if request and request.client:
            return request.client.host or "unknown"
        return "unknown"

    def _init_rate_limiter(self):
        if self.settings.use_redis_rate_limit and self.settings.redis_url:
            try:  # pragma: no cover - optional dependency
                import redis  # type: ignore
                client = redis.Redis.from_url(self.settings.redis_url)
                client.ping()
                logging.info("Using Redis rate limiter")
                return RedisRateLimiter(client, max_requests=self.settings.rate_limit_per_min, window_seconds=self.settings.rate_limit_window_seconds)
            except Exception as exc:
                logging.warning(f"Redis rate limiter unavailable, falling back to in-memory: {exc}")
        return SimpleRateLimiter(max_requests=self.settings.rate_limit_per_min, window_seconds=self.settings.rate_limit_window_seconds)

    def _jwt_scopes(self, claims: Dict[str, Any]) -> List[str]:
        scopes: List[str] = []
        if "scope" in claims and isinstance(claims["scope"], str):
            scopes.extend(claims["scope"].split())
        if "scopes" in claims and isinstance(claims["scopes"], list):
            scopes.extend([str(s) for s in claims["scopes"]])
        return scopes

    def _verify_jwt(self, token: str, required_scope: Optional[str], client_id: str) -> Dict[str, Any]:
        if not self.settings.jwt_enabled:
            raise HTTPException(status_code=401, detail="JWT auth disabled")
        try:
            if self.settings.jwt_jwks_url:
                jwk_client = PyJWKClient(self.settings.jwt_jwks_url)
                signing_key = jwk_client.get_signing_key_from_jwt(token).key
                decoded = jwt.decode(
                    token,
                    signing_key,
                    algorithms=self.settings.jwt_algorithms,
                    audience=self.settings.jwt_audience,
                    issuer=self.settings.jwt_issuer,
                )
            else:
                if not self.settings.jwt_secret:
                    raise HTTPException(status_code=401, detail="Missing JWT secret")
                decoded = jwt.decode(
                    token,
                    self.settings.jwt_secret,
                    algorithms=self.settings.jwt_algorithms,
                    audience=self.settings.jwt_audience,
                    issuer=self.settings.jwt_issuer,
                )
        except HTTPException:
            raise
        except Exception as exc:
            logging.warning(json.dumps({"event": "auth_failed", "client": client_id, "reason": "invalid_jwt", "error": str(exc)}))
            raise HTTPException(status_code=401, detail="Invalid JWT") from exc

        scopes = self._jwt_scopes(decoded)
        if required_scope and required_scope not in scopes and "admin" not in scopes:
            logging.warning(json.dumps({"event": "auth_failed", "client": client_id, "reason": "jwt_insufficient_scope", "required_scope": required_scope}))
            raise HTTPException(status_code=403, detail="Insufficient scope")
        return decoded

    def _auth_key(self, key: Optional[str], required_scope: Optional[str], client_id: str) -> str:
        if not key or key not in self.api_keys:
            logging.warning(json.dumps({"event": "auth_failed", "client": client_id, "reason": "missing_or_invalid_api_key"}))
            raise HTTPException(status_code=401, detail="Invalid or missing API key")

        scopes = self.api_keys.get(key, [])
        if required_scope and required_scope not in scopes and "admin" not in scopes:
            logging.warning(json.dumps({"event": "auth_failed", "client": client_id, "reason": "insufficient_scope", "required_scope": required_scope}))
            raise HTTPException(status_code=403, detail="Insufficient scope")
        return key

    def require_api_key(self, request: Request, x_api_key: Optional[str] = Header(None), authorization: Optional[str] = Header(None)) -> str:
        client_id = self._get_client_id(request)
        self.rate_limiter.check(client_id)
        if x_api_key:
            return self._auth_key(x_api_key, required_scope="read", client_id=client_id)
        if authorization and authorization.lower().startswith("bearer "):
            token = authorization.split(None, 1)[1]
            claims = self._verify_jwt(token, required_scope="read", client_id=client_id)
            return claims.get("sub", "jwt")
        raise HTTPException(status_code=401, detail="Invalid or missing credentials")

    def require_api_key_with_scope(self, scope: str) -> Callable:
        def dependency(request: Request, x_api_key: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
            client_id = self._get_client_id(request)
            self.rate_limiter.check(client_id)
            if x_api_key:
                return self._auth_key(x_api_key, required_scope=scope, client_id=client_id)
            if authorization and authorization.lower().startswith("bearer "):
                token = authorization.split(None, 1)[1]
                claims = self._verify_jwt(token, required_scope=scope, client_id=client_id)
                return claims.get("sub", "jwt")
            raise HTTPException(status_code=401, detail="Invalid or missing credentials")

        return dependency

    def _get_correlation_id(self, correlation_id: Optional[str]) -> str:
        return correlation_id or str(uuid.uuid4())

    def _log_security_event(self, event: str, correlation_id: str, payload: Dict[str, Any]) -> None:
        enriched = {
            "event": event,
            "correlation_id": correlation_id,
            **payload
        }
        logging.info(json.dumps(enriched))
        try:
            self.audit_logger.log(event, enriched)
        except Exception as exc:  # pragma: no cover - audit failures should not break API
            logging.warning(f"Audit logging failed: {exc}")

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

    async def execute_command(self, request: CommandRequest, request_obj: Request, x_correlation_id: Optional[str] = Header(None)):
        """Executes a command via the Hypervisor."""
        # Note: This is a blocking call in the main thread logic, 
        # but we are calling it from an async route.
        # Ideally, we should queue it, but for now we'll execute directly.
        correlation_id = self._get_correlation_id(x_correlation_id)
        logging.info(f"API Command Received: {request.command} :: {correlation_id}")
        
        # We can't easily capture the output of execute_sovereign_command 
        # because it prints to stdout. 
        # We will just trigger it and return acknowledgment.
        
        # To make it thread-safe(ish), we'll just run it.
        # In a real system, we'd use a queue.
        
        # We'll run it in a separate thread to avoid blocking the API
        threading.Thread(target=self.hypervisor.execute_sovereign_command, args=(request.command,)).start()
        self._log_security_event(
            "command_received",
            correlation_id,
            {
                "command": request.command,
                "client": self._get_client_id(request_obj)
            }
        )

        return {"status": "Command Accepted", "command": request.command, "correlation_id": correlation_id}

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

    async def get_sovereign_time_health(
        self,
        request: Request,
        device_id: Optional[str] = None,
        drift_threshold_ms: int = 250,
        x_correlation_id: Optional[str] = Header(None)
    ):
        """Runs sovereign device check + time redundancy drift validation."""
        device = device_id or "PC_TERMINAL"
        report = MillisecondTimer.sovereign_time_reality_check(device_id=device, drift_threshold_ms=drift_threshold_ms)
        correlation_id = self._get_correlation_id(x_correlation_id)
        self._log_security_event(
            "sovereign_time_health",
            correlation_id,
            {
                "device_id": device,
                "drift_ok": report.get("drift_report", {}).get("drift_ok"),
                "device_allowed": report.get("device_allowed"),
                "client": self._get_client_id(request)
            }
        )
        try:
            SOVEREIGN_HEALTH_TOTAL.labels(
                drift_ok=str(report.get("drift_report", {}).get("drift_ok")),
                device_allowed=str(report.get("device_allowed"))
            ).inc()
        except Exception:
            pass
        return report

    async def reconcile_time(self, payload: Dict[str, Any], request_obj: Request, x_correlation_id: Optional[str] = Header(None)):
        """
        Reconcilers predictive time against actual time with a safety buffer.
        Body: {"predictive_unix_ms": <int>, "buffer_ms": <int, optional>}
        """
        predictive_unix_ms = payload.get("predictive_unix_ms")
        buffer_ms = payload.get("buffer_ms", 500)
        if predictive_unix_ms is None:
            raise HTTPException(status_code=400, detail="predictive_unix_ms is required")

        report = MillisecondTimer.reconcile_predictive_time(predictive_unix_ms, buffer_ms=buffer_ms)
        correlation_id = self._get_correlation_id(x_correlation_id)
        self._log_security_event(
            "time_reconcile",
            correlation_id,
            {
                "predictive_unix_ms": predictive_unix_ms,
                "buffer_ms": buffer_ms,
                "authoritative_source": report.get("authoritative_source"),
                "client": self._get_client_id(request_obj)
            }
        )
        try:
            TIME_RECONCILE_TOTAL.labels(authoritative=report.get("authoritative_source", "unknown")).inc()
        except Exception:
            pass
        return report

    async def register_override(self, request: Dict[str, str], request_obj: Request, x_correlation_id: Optional[str] = Header(None)):
        """Registers a Presidential Override."""
        nation = request.get("nation")
        eo_hash = request.get("eo_hash")
        if nation and eo_hash:
            self.hypervisor.zhtp.register_presidential_override(nation, eo_hash)
            correlation_id = self._get_correlation_id(x_correlation_id)
            self._log_security_event(
                "override_registered",
                correlation_id,
                {
                    "nation": nation,
                    "eo_hash": eo_hash,
                    "client": self._get_client_id(request_obj)
                }
            )
            return {"status": "Override Registered", "nation": nation, "correlation_id": correlation_id}
        raise HTTPException(status_code=400, detail="Missing nation or eo_hash")

    async def get_quantum_entropy(self):

        """Returns current quantum entropy."""
        entropy = self.hypervisor.quantum.get_quantum_entropy()
        return {"entropy": entropy, "source": "Qiskit" if self.hypervisor.quantum.enabled else "execution"}

    async def list_drive_files(self, q: Optional[str] = None):
        """Lists files from Google Drive."""
        if not hasattr(self.hypervisor, 'drive'):
            raise HTTPException(status_code=503, detail="Google Drive Bridge not initialized")
        
        if q:
            return self.hypervisor.drive.search_files(q)
        return self.hypervisor.drive.list_files()

    async def read_drive_file(self, file_id: str):
        """Reads content of a Google Drive file."""
        if not hasattr(self.hypervisor, 'drive'):
            raise HTTPException(status_code=503, detail="Google Drive Bridge not initialized")
            
        content = self.hypervisor.drive.read_file_content(file_id)
        if content.startswith("Error"):
             raise HTTPException(status_code=500, detail=content)
        return {"content": content}

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
            <div class="title">API Access</div>
            <div class="sub">Provide API key or JWT for protected routes</div>
            <div class="row">
                <select id="authMode">
                    <option value="key">API Key</option>
                    <option value="jwt">JWT</option>
                </select>
                <input id="apiKey" placeholder="x-api-key or JWT" />
                <button onclick="saveKey()">Save</button>
                <button onclick="testAuth()">Test</button>
            </div>
            <div id="apiKeyStatus" class="sub"></div>
        </section>
        <section class="card">
            <div class="title">Telemetry</div>
            <div class="sub">Live hardware metrics</div>
            <div id="telemetry" class="grid"></div>
        </section>
        <section class="card">
            <div class="title">Health Strip</div>
            <div class="sub">Sovereign time & reconciliation status</div>
            <div id="health" class="list">Loading...</div>
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
        function headers() {
            const key = localStorage.getItem('sarah_api_key');
            const mode = localStorage.getItem('sarah_auth_mode') || 'key';
            if (!key) return {};
            if (mode === 'jwt') return { 'Authorization': `Bearer ${key}` };
            return { 'x-api-key': key };
        }

        async function fetchJSON(path) {
            const res = await fetch(path, { headers: headers() });
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
                const [telemetry, bridge, usb, zhtp, health] = await Promise.all([
                    fetchJSON('/telemetry'),
                    fetchJSON('/bridge/handshake'),
                    fetchJSON('/usb/devices'),
                    fetchJSON('/zhtp/status'),
                    fetchJSON('/health/sovereign-time')
                ]);
                renderTelemetry(telemetry);
                renderList('bridge', bridge);
                renderList('usb', usb);
                renderList('zhtp', zhtp);
                renderList('health', health);
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
                    headers: { 'Content-Type': 'application/json', ...headers() },
                    body: JSON.stringify({ command: v })
                });
                const data = await res.json();
                out.textContent = `Status: ${data.status || data.error || 'ok'}`;
            } catch (e) {
                out.textContent = 'Error sending command';
            }
        }

        function saveKey() {
            const key = document.getElementById('apiKey').value.trim();
            const mode = document.getElementById('authMode').value;
            const status = document.getElementById('apiKeyStatus');
            if (!key) {
                status.textContent = 'Enter a key to save.';
                return;
            }
            localStorage.setItem('sarah_api_key', key);
            localStorage.setItem('sarah_auth_mode', mode);
            status.textContent = mode === 'jwt' ? 'Saved. Requests will include Authorization: Bearer.' : 'Saved. Requests will include x-api-key.';
        }

        (function preloadKey(){
            const k = localStorage.getItem('sarah_api_key');
            const mode = localStorage.getItem('sarah_auth_mode') || 'key';
            if (k) {
                document.getElementById('apiKey').value = k;
                document.getElementById('apiKeyStatus').textContent = 'Key loaded from storage.';
            }
            document.getElementById('authMode').value = mode;
        })();

        async function testAuth() {
            const status = document.getElementById('apiKeyStatus');
            status.textContent = 'Testing...';
            try {
                const res = await fetch('/status', { headers: headers() });
                status.textContent = res.ok ? 'Auth OK' : `Auth failed (${res.status})`;
            } catch (e) {
                status.textContent = 'Auth test error';
            }
        }

        loadAll();
        setInterval(loadAll, 5000);
    </script>
</body>
</html>
"""
        return HTMLResponse(content=html)
