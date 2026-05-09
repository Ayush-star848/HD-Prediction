"""tests/test_routes.py — Run: python -m pytest tests/ -v"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest
from backend.app import create_app

VALID = dict(age=55,sex=1,cp=3,trestbps=140,chol=250,fbs=0,
             restecg=1,thalach=140,exang=1,oldpeak=2.3,slope=1,ca=1,thal=3)

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c: yield c

def test_health(client):
    r = client.get("/api/health"); assert r.status_code in (200, 503)

def test_models(client):
    r = client.get("/api/models"); d = r.get_json()
    assert r.status_code == 200 and "models" in d

def test_predict_missing_fields(client):
    r = client.post("/api/predict", data=json.dumps({"age":55}), content_type="application/json")
    assert r.status_code == 422 and not r.get_json()["success"]

def test_predict_invalid_json(client):
    r = client.post("/api/predict", data="bad", content_type="application/json")
    assert r.status_code == 400

def test_index(client):
    r = client.get("/"); assert r.status_code == 200 and b"CardioSense" in r.data

def test_bulk_no_file(client):
    r = client.post("/api/bulk"); assert r.status_code == 400
