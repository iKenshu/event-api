"""
This file is used to test the EventUser model.
"""

import random
import string
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from auth.api import create_access_token
from config.database import get_session
from crud.crud_event import event as event_crud
from crud.crud_event_user import event_user as crud
from crud.crud_user import crud_user as user_crud
from main import app

client = TestClient(app)


@pytest.fixture
def mock_user():
    """
    This function is used to mock a user.
    """
    db = get_session()
    username = random_string(10)
    user = {
        "username": f"test_{username}",
        "hashed_password": "testpassword",
    }
    user = user_crud.create(db, obj_in=user)
    return user


@pytest.fixture
def mock_user_token(mock_user):
    """
    This function is used to mock a user token.
    """
    token = create_access_token(
        mock_user.username, mock_user.id, timedelta(days=1)
    )
    return token


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


def test_create_event_user(mock_user_token, mock_event, mock_user):
    """
    This TEST is used to create an event user.
    """
    event_user = {
        "user_id": mock_user.id,
        "event_id": mock_event.id,
    }
    response = client.post(
        f"/event/{mock_event.id}/register",
        json=event_user,
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == mock_user.id
    assert data["event_id"] == mock_event.id


def test_create_event_user__event_not_found(mock_user_token, mock_user):
    """
    This TEST is used to create an event user.
    """
    random_id = random.randint(100, 1000)
    event_user = {
        "user_id": mock_user.id,
        "event_id": random_id,
    }
    response = client.post(
        f"/event/{random_id}/register",
        json=event_user,
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Event not found"


def test_create_event_user__full_event(mock_user_token, mock_user):
    """
    This TEST is used to create an event user.
    """
    event_full = event_crud.create(
        db=get_session(),
        obj_in={
            "name": "Test Event",
            "description": "Test Description",
            "location": "Test Location",
            "category": "Other",
            "start_time": "2030-01-01T00:00:00",
            "end_time": "2030-01-02T00:00:00",
            "current_capacity": 1,
            "max_capacity": 1,
            "status": "full",
        },
    )

    event_user = {
        "user_id": mock_user.id,
        "event_id": event_full.id,
    }
    response = client.post(
        f"/event/{event_full.id}/register",
        json=event_user,
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "Event is full"


def test_get_event_user(mock_user_token, mock_event, mock_user):
    """
    This TEST is used to get an event user.
    """
    crud.add_user_to_event(
        db=get_session(), event_id=mock_event.id, user_id=mock_user.id
    )
    response = client.get(
        f"/event/{mock_event.id}/registrations",
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data["users"]) > 0


def test_delete_event_user(mock_user_token, mock_event, mock_user):
    """
    This TEST is used to delete an event user.
    """
    crud.add_user_to_event(
        db=get_session(), event_id=mock_event.id, user_id=mock_user.id
    )
    response = client.delete(
        f"/event/{mock_event.id}/registrations",
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == mock_user.id


def random_string(length: int) -> str:
    """
    This function is used to generate a random string.
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))
