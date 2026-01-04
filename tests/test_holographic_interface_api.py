import os

import pytest
from fastapi.testclient import TestClient

from Holographic_Interface import HolographicInterface
from Millisecond_Timing import MillisecondTimer


class _DummyQuantum:
    enabled = True

    def get_quantum_entropy(self):
        return 0.42


class _DummySilicon:
    def get_hardware_metrics(self):
        return {
            "gpu_utilization": 0.0,
            "gpu_temp": 35.0,
            "vram_usage": 0.1,
            "cpu_temp": 40.0,
            "power_draw": 10.0,
        }

    def cross_platform_handshake(self):
        return {"status": "ok"}

    def list_usb_devices(self):
        return []


class _DummyZHTP:
    def __init__(self):
        self.active = True
        self.presidential_overrides = []
        self.api_hooks = []

    def generate_lumen_firmware(self):
        return "firmware"

    def register_presidential_override(self, nation, eo_hash):
        self.presidential_overrides.append({"nation": nation, "eo_hash": eo_hash})


class _DummyGraph:
    class _G:
        @staticmethod
        def number_of_nodes():
            return 0

    def __init__(self):
        self.graph = self._G()


class _DummyMemory:
    def search(self, query, top_k=3):
        return [f"result-{i}" for i in range(top_k)]


class _DummyHypervisor:
    def __init__(self):
        self.quantum = _DummyQuantum()
        self.silicon = _DummySilicon()
        self.zhtp = _DummyZHTP()
        self.memory = _DummyMemory()
        self.knowledge_graph = _DummyGraph()


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("SARAH_API_KEYS", "test-key:admin|read|write")
    hv = _DummyHypervisor()
    interface = HolographicInterface(hv)
    return TestClient(interface.app)


@pytest.fixture
def limited_client(monkeypatch):
    monkeypatch.setenv("SARAH_API_KEYS", "test-key:read")
    monkeypatch.setenv("SARAH_RATE_LIMIT_PER_MIN", "1")
    monkeypatch.setenv("SARAH_RATE_LIMIT_WINDOW", "60")
    hv = _DummyHypervisor()
    interface = HolographicInterface(hv)
    return TestClient(interface.app)


@pytest.fixture
def jwt_client(monkeypatch):
    monkeypatch.setenv("SARAH_API_KEYS", "")
    monkeypatch.setenv("SARAH_JWT_ENABLED", "true")
    monkeypatch.setenv("SARAH_JWT_SECRET", "supersecret")
    monkeypatch.setenv("SARAH_JWT_ALGORITHMS", "HS256")
    hv = _DummyHypervisor()
    interface = HolographicInterface(hv)
    return TestClient(interface.app)


def test_health_requires_api_key(client):
    resp = client.get("/health/sovereign-time")
    assert resp.status_code == 401


def test_health_allows_with_api_key(client):
    resp = client.get("/health/sovereign-time", headers={"x-api-key": "test-key"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["device_allowed"] is True
    assert "drift_report" in body


def test_reconcile_prefers_predictive_within_buffer(client):
    actual = MillisecondTimer.get_unix_ms()
    payload = {"predictive_unix_ms": actual + 100, "buffer_ms": 200}
    resp = client.post("/time/reconcile", json=payload, headers={"x-api-key": "test-key"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["authoritative_source"] == "predictive"


def test_reconcile_prefers_actual_outside_buffer(client):
    actual = MillisecondTimer.get_unix_ms()
    payload = {"predictive_unix_ms": actual + 2000, "buffer_ms": 200}
    resp = client.post("/time/reconcile", json=payload, headers={"x-api-key": "test-key"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["authoritative_source"] == "actual"


def test_rate_limit_exceeded(limited_client):
    headers = {"x-api-key": "test-key"}
    first = limited_client.get("/health/sovereign-time", headers=headers)
    assert first.status_code == 200
    second = limited_client.get("/health/sovereign-time", headers=headers)
    assert second.status_code == 429


def test_metrics_available(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "holo_time_reconcile_total" in resp.text


def test_jwt_auth_allows_read(jwt_client):
    import jwt as pyjwt  # type: ignore

    token = pyjwt.encode({"sub": "tester", "scope": "read"}, "supersecret", algorithm="HS256")
    resp = jwt_client.get("/status", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
