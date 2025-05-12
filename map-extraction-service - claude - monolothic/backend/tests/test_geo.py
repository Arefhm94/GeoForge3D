from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_geo_extraction():
    # Test the geo extraction endpoint with a valid rectangle
    response = client.post("/geo/extract", json={"rectangle": [[-10, -10], [10, 10]]})
    assert response.status_code == 200
    assert "geojson" in response.json()

def test_geo_extraction_invalid_rectangle():
    # Test the geo extraction endpoint with an invalid rectangle
    response = client.post("/geo/extract", json={"rectangle": [[-10, -10], [10, "invalid"]]})
    assert response.status_code == 422  # Unprocessable Entity

def test_geo_extraction_area_limit():
    # Test the area limit for free extraction
    response = client.post("/geo/extract", json={"rectangle": [[-1000, -1000], [1000, 1000]]})
    assert response.status_code == 403  # Forbidden, exceeds free limit

def test_geo_extraction_fee():
    # Test the fee calculation for area beyond free limit
    response = client.post("/geo/extract", json={"rectangle": [[-100, -100], [100, 100]]})
    assert response.status_code == 200
    assert response.json()["fee"] == 0  # Free for 1 km²

    response = client.post("/geo/extract", json={"rectangle": [[-2000, -2000], [2000, 2000]]})
    assert response.status_code == 200
    assert response.json()["fee"] > 0  # Should return a fee for area beyond 1 km²