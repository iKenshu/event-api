"""
This file is used to test the SessionUser model.
"""

import random
import string
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from auth.api import create_access_token
from config.database import get_session
from crud.crud_event import event as event_crud
from crud.crud_session import session as session_crud
from crud.crud_session_user import session_user as crud
from crud.crud_user import crud_user as user_crud
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


def random_string(length):
    """
    This function is used to generate a random string.
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


@pytest.fixture
def mock_session(mock_event):
    """
    This function is used to mock a session.
    """
    db = get_session()
    session = {
        "title": "Test Session",
        "speaker": "Test Speaker",
        "event_id": mock_event.id,
        "start_time": "2030-01-01T00:00:00",
        "end_time": "2030-01-02T00:00:00",
    }
    session = session_crud.create(db, obj_in=session)
    return session


@pytest.fixture
def mock_user_token(mock_user):
    """
    This function is used to mock a user token.
    """
    token = create_access_token(
        mock_user.username, mock_user.id, timedelta(days=1)
    )
    return token


def test_create_session_user(mock_user_token, mock_session, mock_user):
    """
    This TEST is used to create a session user.
    """
    session_user = {
        "user_id": mock_user.id,
        "session_id": mock_session.id,
    }
    response = client.post(
        f"/session/{mock_session.id}/register",
        json=session_user,
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == mock_user.id
    assert data["session_id"] == mock_session.id


def teste_create_session_user__session_not_found(mock_user_token, mock_user):
    """
    This TEST is used to create a session user.
    """
    random_id = random.randint(100, 1000)
    session_user = {
        "user_id": mock_user.id,
        "session_id": random_id,
    }
    response = client.post(
        f"/session/{random_id}/register",
        json=session_user,
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Session not found"


def test_create_session_user__session_full(
    mock_user_token, mock_user, mock_event
):
    """
    This TEST is used to create a session user.
    """
    session_full = session_crud.create(
        db=get_session(),
        obj_in={
            "title": "Test Session",
            "speaker": "Test Speaker",
            "event_id": mock_event.id,
            "start_time": "2030-01-01T00:00:00",
            "end_time": "2030-01-02T00:00:00",
            "event_id": mock_event.id,
            "current_capacity": 1,
            "max_capacity": 1,
            "status": "full",
        },
    )

    session_user = {
        "user_id": mock_user.id,
        "session_id": session_full.id,
    }
    response = client.post(
        f"/session/{session_full.id}/register",
        json=session_user,
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "Session is full"


def test_create_session_user__user_already_registered(
    mock_user_token, mock_session, mock_user
):
    """
    This TEST is used to create a session user.
    """
    crud.register_user_to_session(
        db=get_session(), session_id=mock_session.id, user_id=mock_user.id
    )

    session_user = {
        "user_id": mock_user.id,
        "session_id": mock_session.id,
    }
    response = client.post(
        f"/session/{mock_session.id}/register",
        json=session_user,
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "User already registered for this session"


def test_delete_session_user(mock_user_token, mock_session, mock_user):
    """
    This TEST is used to delete a session user.
    """
    crud.register_user_to_session(
        db=get_session(), session_id=mock_session.id, user_id=mock_user.id
    )
    response = client.delete(
        f"/session/{mock_session.id}/registrations",
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == mock_user.id


def test_delete_session_user__not_found(mock_user_token, mock_session):
    """
    This TEST is used to delete a session user.
    """
    random_id = random.randint(100, 1000)
    response = client.delete(
        f"/session/{random_id}/registrations",
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Session user not found"


def test_get_session_user(mock_user_token, mock_session, mock_user):
    """
    This TEST is used to get a session user.
    """
    crud.register_user_to_session(
        db=get_session(), session_id=mock_session.id, user_id=mock_user.id
    )
    response = client.get(
        f"/session/{mock_session.id}/registrations",
        headers={"Authorization": f"Bearer {mock_user_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data["users"]) > 0
