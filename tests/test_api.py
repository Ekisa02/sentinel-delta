import pytest
from fastapi.testclient import TestClient
from sentinel_delta.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_predict_endpoint():
    payload = {
        "events": [
            {"contract": "0xabc", "nonce": 1, "value": 3.0, "gas_used": 21000, "timestamp": 1},
            {"contract": "0xabc", "nonce": 2, "value": 7.0, "gas_used": 22000, "timestamp": 2}
        ]
    }
    r = client.post("/api/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "anomalies" in data
    assert isinstance(data["anomalies"], list)
