from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from app.auth.router import router as auth_router
from app.auth.models import User
from app.database import get_db
from sqlalchemy.orm import Session

app = FastAPI()
app.include_router(auth_router)

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user():
    client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user():
    response = client.post("/auth/login", data={"username": "invaliduser", "password": "wrongpass"})
    assert response.status_code == 401

def test_get_user_profile():
    client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    login_response = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    response = client.get("/auth/profile", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"