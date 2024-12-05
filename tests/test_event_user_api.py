"""
This file is used to test the EventUser API.
"""

import random
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session

import crud
from auth.api import ALGORITHM, SECRET_KEY, create_access_token
from config.database import get_session
from main import app
from models.event_user import EventUser
from models.user import User

client = TestClient(app)


def create_test_token(user_id: int, username: str):
    """
    This function is used to create a test token.
    """
    payload = {"sub": username, "id": user_id}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@pytest.fixture
def mock_user():
    """
    This function is used to mock a user.
    """
    random_number = random.randint(1, 1000)
    user = User(
        username=f"test_user_{random_number}",
        hashed_password="test_password",
    )

    db = get_session()
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user

    db.delete(user)
    db.commit()


@pytest.fixture
def mock_event_user(mock_user: mock_user):
    """
    This function is used to mock an event user.
    """
    db = get_session()
    event_user = EventUser(event_id=1, user_id=mock_user.id)
    db.add(event_user)
    db.commit()
    db.refresh(event_user)
    yield event_user

    db.delete(event_user)
    db.commit()


def test_register_event_user(mock_user):
    """
    This test is used to register an event user.
    """
    token = create_test_token(mock_user.id, mock_user.username)
    event_data = {"event_id": 1}
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/event-user/register", headers=headers, json=event_data
    )
    assert response.status_code == 200

    db = get_session()
    crud.remove_user_from_event(
        event_id=event_data["event_id"], user_id=mock_user.id, db=db
    )


def test_unregister_event_user(mock_user):
    """
    This test is used to unregister an event user.
    """
    crud.add_user_to_event(event_id=1, user_id=mock_user.id, db=get_session())
    token = create_test_token(mock_user.id, mock_user.username)

    event_data = {"event_id": 1}

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(
        f"/event-user/{event_data['event_id']}/registrations", headers=headers
    )
    assert response.status_code == 200

    data = response.json()
    assert data["event_id"] == event_data["event_id"]


def test_get_event_users(mock_event_user: mock_event_user):
    """
    This test is used to get all users for an event.
    """
    response = client.get(
        f"/event-user/{mock_event_user.event_id}/registrations"
    )
    assert response.status_code == 200
    data = response.json()

    assert len(data["users"]) > 0
