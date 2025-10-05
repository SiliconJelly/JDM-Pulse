"""
In-process API test using FastAPI TestClient to avoid running a long-lived server
"""

from fastapi.testclient import TestClient
from app.main import app

# Use context manager to ensure startup events run
with TestClient(app) as client:
    # Health check
    resp = client.get("/health")
    print("/health:", resp.status_code, resp.json())

    # Predict test payload
    payload = {
        "make": "Toyota",
        "model": "Land Cruiser 300",
        "year": 2022,
        "mileage_km": 15000,
        "engine_cc": 3500,
        "auction_grade": 4.5,
        "user_bid_jpy": None
    }

    resp = client.post("/predict", json=payload)
    print("/predict status:", resp.status_code)
    print("/predict json keys:", list(resp.json().keys()) if resp.status_code == 200 else resp.text)
