"""
This file is used to test the Session API.
"""

import random

import pytest
from fastapi.testclient import TestClient

from config.database import get_session
from crud.crud_event import event as event_crud
from crud.crud_session import session as crud
from main import app

client = TestClient(app)


@pytest.fixture
def mock_event():
    """
    This function is used to mock an event.
    """
    db = get_session()
    event = {
        "name": "Test Event",
        "description": "Test Description",
        "location": "Test Location",
        "category": "Other",
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
    }
    event = event_crud.create(db, obj_in=event)
    return event


def test_create_session(mock_event):
    """
    This TEST is used to create a session.
    """
    session = {
        "title": "Test Session",
        "speaker": "Test Speaker",
        "event_id": mock_event.id,
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
    }
    response = client.post("/session/", json=session)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Session"
    assert data["speaker"] == "Test Speaker"


def test_get_all_sessions(mock_event):
    """
    This TEST is used to get all sessions.
    """
    response = client.get("/session/")
    assert response.status_code == 200

    data = response.json()
    assert len(data["data"]) > 0


def test_get_session(mock_event):
    """
    This TEST is used to get a session.
    """
    db = get_session()
    session = {
        "title": "Test Session",
        "speaker": "Test Speaker",
        "event_id": mock_event.id,
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
    }
    session = crud.create(db=db, obj_in=session)
    response = client.get(f"/session/{session.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Session"
    assert data["speaker"] == "Test Speaker"
    assert data["id"] == session.id


def test_get_session_not_found():
    """
    This TEST is used to get a session that does not exist.
    """
    random_id = random.randint(100, 1000)
    response = client.get(f"/session/{random_id}")
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Session not found"


def test_update_session(mock_event):
    """
    This TEST is used to update a session.
    """
    session = {
        "title": "Test Session",
        "speaker": "Test Speaker",
        "event_id": mock_event.id,
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
    }
    session = crud.create(db=get_session(), obj_in=session)
    updated_session = {
        "title": "Updated Test Session",
        "speaker": "Updated Test Speaker",
    }
    response = client.patch(f"/session/{session.id}", json=updated_session)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Test Session"
    assert data["speaker"] == "Updated Test Speaker"


def test_update_session_not_found():
    """
    This TEST is used to update a session that does not exist.
    """
    random_id = random.randint(100, 1000)

    updated_session = {
        "title": "Updated Test Session",
        "speaker": "Updated Test Speaker",
    }
    response = client.patch(f"/session/{random_id}", json=updated_session)
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Session not found"


def test_delete_session(mock_event):
    """
    This TEST is used to delete a session.
    """
    session = {
        "title": "Test Session",
        "speaker": "Test Speaker",
        "event_id": mock_event.id,
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
    }
    session = crud.create(db=get_session(), obj_in=session)
    response = client.delete(f"/session/{session.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == session.id


def test_delete_session_not_found():
    """
    This TEST is used to delete a session that does not exist.
    """
    random_id = random.randint(100, 1000)
    response = client.delete(f"/session/{random_id}")
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Session not found"
