import pytest
from fastapi.testclient import TestClient

import app.tickets as tickets_module
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tickets():
    tickets_module.tickets.clear()
    tickets_module.next_id = 1


def test_create_ticket():
    response = client.post(
        "/tickets",
        json={
            "title": "VPN not working",
            "description": "VPN fails when I try to connect",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "VPN not working"
    assert data["priority"] == "high"
    assert data["status"] == "open"


def test_get_ticket():
    client.post(
        "/tickets",
        json={
            "title": "Password reset",
            "description": "User forgot password",
            "priority": "medium",
        },
    )

    response = client.get("/tickets/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Password reset"


def test_update_ticket():
    client.post(
        "/tickets",
        json={
            "title": "Laptop issue",
            "description": "Laptop will not boot",
            "priority": "high",
        },
    )

    response = client.patch(
        "/tickets/1",
        json={"status": "closed"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "closed"


def test_invalid_priority():
    response = client.post(
        "/tickets",
        json={
            "title": "Bad ticket",
            "description": "Testing validation",
            "priority": "banana",
        },
    )

    assert response.status_code == 422


def test_delete_ticket():
    client.post(
        "/tickets",
        json={
            "title": "Delete me",
            "description": "Temporary ticket",
            "priority": "low",
        },
    )

    response = client.delete("/tickets/1")

    assert response.status_code == 204

    response = client.get("/tickets/1")

    assert response.status_code == 404