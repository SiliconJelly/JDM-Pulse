from fastapi.testclient import TestClient
from backend.app.main import app

def test_health_ok():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert data.get("status") == "ok"
        assert data.get("is_model_loaded") in (True, False)