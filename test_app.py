from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_primary_contact():
    response = client.post("/identify", json={
        "email": "alpha@example.com",
        "phoneNumber": "1234567890"
    })
    assert response.status_code == 200
    assert "primaryContactId" in response.json()["contact"]

def test_create_secondary_contact():
    # Must be linked to previous
    response = client.post("/identify", json={
        "email": "alpha@example.com",
        "phoneNumber": "9999999999"
    })
    data = response.json()["contact"]
    assert "alpha@example.com" in data["emails"]
    # Make sure both numbers are present
    assert "1234567890" in data["phoneNumbers"]
    assert "9999999999" in data["phoneNumbers"]
    # There should be at least 1 secondary ID now
    assert len(data["secondaryContactIds"]) >= 1
