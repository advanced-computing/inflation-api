import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for Flask."""
    app.testing = True
    return app.test_client()

def test_home(client):
    """Test home route response."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the 2025 Fed Inflation Newscast Data API" in response.data

def test_add_numbers(client):
    """Test adding two numbers."""
    response = client.get("/add?a=5&b=10")
    assert response.status_code == 200
    assert response.get_json()["sum"] == 15

def test_filter_valid_month(client):
    """Test filtering for a valid month (1 or 2)."""
    response = client.get("/filter?month=1")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)  # Expect list of records

def test_filter_invalid_month(client):
    """Test filtering for an invalid month (e.g., 5)."""
    response = client.get("/filter?month=5")
    assert response.status_code == 404
