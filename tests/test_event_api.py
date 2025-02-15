"""
This file is used to test the Event API.
"""

import random
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from config.database import get_session
from crud.crud_event import event as crud
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
        start_time="2030-01-01T00:00:00",
        end_time="2030-01-02T00:00:00",
    )
    crud.create(db, event)

    response = client.get("/event/")
    assert response.status_code == 200

    data = response.json()
    assert len(data["data"]) > 0


def test_get_events_with_elasticsearch():
    """
    This TEST is used to get all events with Elasticsearch.
    """
    db = get_session()
    event = Event(
        name="Test Event",
        description="Test Description",
        location="Test Location",
        category="Other",
        start_time="2030-01-01T00:00:00",
        end_time="2030-01-02T00:00:00",
    )
    crud.create(db, event)

    response = client.get("/event/search?query=Test")
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
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
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
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
    }
    response = client.post("/event/", json=event)
    assert response.status_code == 200

    data = response.json()

    updated_event = {
        "name": "Updated Test Event",
        "location": "Updated Test Location",
    }

    response = client.patch(f"/event/{data['id']}", json=updated_event)
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
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
    }
    random_id = random.randint(100, 1000)

    response = client.patch(f"/event/{random_id}", json=event)
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
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
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
