import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from main import app
from database.database import get_session
from models.user import User
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client with a clean database for each test function"""
    # Create tables
    SQLModel.metadata.create_all(bind=engine)

    def get_test_session():
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()
    # Drop all tables to ensure clean state for next test
    SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture
def valid_user_data():
    """Valid user data for testing"""
    return {
        "email": "test@example.com",
        "password": "ValidPass123",
        "first_name": "Test",
        "last_name": "User"
    }


def test_successful_user_signup(client, valid_user_data):
    """Test successful user signup"""
    response = client.post("/users/signup", json=valid_user_data)

    assert response.status_code == 201
    data = response.json()

    # Check that the response contains expected fields
    assert "id" in data
    assert data["email"] == valid_user_data["email"]
    assert data["first_name"] == valid_user_data["first_name"]
    assert data["last_name"] == valid_user_data["last_name"]
    assert "created_at" in data

    # Verify the user was actually created in the database
    with TestingSessionLocal() as session:
        user = session.get(User, data["id"])
        assert user is not None
        assert user.email == valid_user_data["email"]
        assert user.first_name == valid_user_data["first_name"]
        assert user.last_name == valid_user_data["last_name"]

        # Verify the password was hashed
        ph = PasswordHash([Argon2Hasher()])
        assert ph.verify(valid_user_data["password"], user.hashed_password)


def test_duplicate_email_signup(client, valid_user_data):
    """Test that signup with duplicate email returns 409 Conflict"""
    # First signup should succeed
    response1 = client.post("/users/signup", json=valid_user_data)
    assert response1.status_code == 201

    # Second signup with same email should fail
    response2 = client.post("/users/signup", json=valid_user_data)
    assert response2.status_code == 409
    assert response2.json()["detail"] == "Email already registered"


def test_password_too_short(client, valid_user_data):
    """Test that signup with too short password fails validation"""
    invalid_data = valid_user_data.copy()
    invalid_data["password"] = "short"

    response = client.post("/users/signup", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_password_missing_uppercase(client, valid_user_data):
    """Test that signup with password missing uppercase fails validation"""
    invalid_data = valid_user_data.copy()
    invalid_data["password"] = "alllowercase123"

    response = client.post("/users/signup", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_password_missing_lowercase(client, valid_user_data):
    """Test that signup with password missing lowercase fails validation"""
    invalid_data = valid_user_data.copy()
    invalid_data["password"] = "ALLUPPERCASE123"

    response = client.post("/users/signup", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_password_missing_number(client, valid_user_data):
    """Test that signup with password missing number fails validation"""
    invalid_data = valid_user_data.copy()
    invalid_data["password"] = "NoNumbersHere"

    response = client.post("/users/signup", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_invalid_email_format(client, valid_user_data):
    """Test that signup with invalid email format fails validation"""
    invalid_data = valid_user_data.copy()
    invalid_data["email"] = "not-an-email"

    response = client.post("/users/signup", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_signup_with_missing_required_fields(client):
    """Test that signup with missing required fields fails"""
    # Missing email
    response = client.post("/users/signup", json={
        "password": "ValidPass123",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 422

    # Missing password
    response = client.post("/users/signup", json={
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 422


def test_signup_with_optional_fields_only(client, valid_user_data):
    """Test that signup works with optional fields not provided"""
    minimal_data = {
        "email": "minimal@example.com",
        "password": "ValidPass123"
    }

    response = client.post("/users/signup", json=minimal_data)
    assert response.status_code == 201
    data = response.json()

    assert data["email"] == minimal_data["email"]
    # Optional fields should be None if not provided
    assert data["first_name"] is None
    assert data["last_name"] is None


def test_signup_with_empty_optional_fields(client, valid_user_data):
    """Test that signup works with empty optional fields"""
    data_with_empty_optional = {
        "email": "empty@example.com",
        "password": "ValidPass123",
        "first_name": "",
        "last_name": ""
    }

    response = client.post("/users/signup", json=data_with_empty_optional)
    assert response.status_code == 201
    data = response.json()

    assert data["email"] == data_with_empty_optional["email"]
    assert data["first_name"] == ""
    assert data["last_name"] == ""