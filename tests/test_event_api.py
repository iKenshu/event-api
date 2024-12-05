"""
This file is used to test the Event API.
"""

import random

from fastapi.testclient import TestClient

import crud
from config.database import get_session
from main import app
from schemas.event import Event

client = TestClient(app)


def test_get_all_events():
    """
    This TEST is used to get all events.
    """
    db = get_session()
    event = Event(
        name="Test Event",
        description="Test Description",
        location="Test Location",
        category="Other",
        start_date="2023-01-01",
        end_date="2023-01-01",
    )
    crud.create_event(event, db)

    response = client.get("/event/")
    assert response.status_code == 200


def test_create_event():
    """
    This TEST is used to create an event.
    """
    event = {
        "name": "Test Event",
        "description": "Test Description",
        "location": "Test Location",
        "category": "Other",
        "start_date": "2023-01-01",
        "end_date": "2023-01-01",
    }
    response = client.post("/event/", json=event)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Test Event"
    assert data["location"] == "Test Location"


def test_update_event():
    """
    This TEST is used to update an event.
    """
    event = {
        "name": "Test Event",
        "description": "Test Description",
        "location": "Test Location",
        "category": "Other",
        "start_date": "2023-01-01",
        "end_date": "2023-01-01",
    }
    response = client.post("/event/", json=event)
    assert response.status_code == 200

    data = response.json()

    updated_event = {
        "name": "Updated Test Event",
        "location": "Updated Test Location",
    }

    response = client.put(f"/event/{data['id']}", json=updated_event)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Test Event"
    assert data["location"] == "Updated Test Location"


def test_update_event_not_found():
    """
    This TEST is used to update an event that does not exist.
    """
    event = {
        "name": "Test Event",
        "description": "Test Description",
        "location": "Test Location",
        "category": "Other",
        "start_date": "2023-01-01",
        "end_date": "2023-01-01",
    }
    random_id = random.randint(100, 1000)

    response = client.put(f"/event/{random_id}", json=event)
    assert response.status_code == 404


def test_delete_event():
    """
    This TEST is used to delete an event.
    """
    event = {
        "name": "Test Event",
        "description": "Test Description",
        "location": "Test Location",
        "category": "Other",
        "start_date": "2023-01-01",
        "end_date": "2023-01-01",
    }
    response = client.post("/event/", json=event)
    assert response.status_code == 200

    data = response.json()

    response = client.delete(f"/event/{data['id']}")
    assert response.status_code == 200


def test_delete_event_not_found():
    """
    This TEST is used to delete an event that does not exist.
    """
    random_id = random.randint(100, 1000)

    response = client.delete(f"/event/{random_id}")
    assert response.status_code == 404
