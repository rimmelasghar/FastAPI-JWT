from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.db.database import Base,get_db
from src.main import app
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///src/db/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/auth/",
        json={
            "username": "test",
            "email": "test@gmail.com",
            "role": "user",
            "firstName": "test",
            "lastName": "test",
            "password": "test123"
            },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@gmail.com"
    assert data["role"] == "user"
    assert data["firstName"] == "test"
    assert data["lastName"] == "test"
    assert data["password"] != "test123" # since it will be encrypted

def test_get_all_users():
    # Create a test user
    response_create_user = client.post(
        "/auth/",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "role": "user",
            "firstName": "Test",
            "lastName": "User",
            "password": "testpassword"
        },
    )
    assert response_create_user.status_code == 201

    # Get all users
    response_get_users = client.get('/auth/')
    assert response_get_users.status_code == 200

    # Check if the test user is in the list of users
    users = response_get_users.json()
    assert any(user['email'] == "testuser@example.com" for user in users)

def test_login():
    # Log in
    login_data = {
        "email": "test@gmail.com",
        "password": "test123"
    }
    response_login = client.post('/auth/login/', json=login_data)
    assert response_login.status_code == 200
    token_response = response_login.json()
    assert "access_token" in token_response

# Test the get_profile endpoint
def test_get_profile():

    # Log in to obtain an access token
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response_login = client.post('/auth/login', json=login_data)
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]

    # Get the user's profile
    headers = {"Authorization": f"Bearer {token}"}
    response_get_profile = client.get('/auth/profile', headers=headers)
    assert response_get_profile.status_code == 200
    profile_data = response_get_profile.json()
    assert profile_data['email'] == "testuser@example.com"