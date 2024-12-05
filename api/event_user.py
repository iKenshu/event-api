"""
This file is used to define the EventUser api.
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

import crud
from auth.api import get_current_user
from config.database import get_session
from models.event_user import EventUser
from schemas.event_user import EventUserCreate, EventWithUsers

router = APIRouter()


@router.post("/register", response_model=EventUser)
def register_event_user(
    event_user: EventUserCreate,
    db: Session = Depends(get_session),
    user: EventUser = Depends(get_current_user),
):
    """
    This function is used to register an event user.
    """
    event_user = crud.add_user_to_event(
        event_id=event_user.event_id, user_id=user.id, db=db
    )
    return event_user


@router.get("/{event_id}/registrations", response_model=EventWithUsers)
def get_event_users(event_id: int, db: Session = Depends(get_session)):
    """
    This function is used to get all users for an event.
    Args:
        event_id (int): The id of the event to get users for.
    """
    event_users = crud.get_event_users(event_id, db)
    return event_users


@router.delete("/{event_id}/registrations", response_model=EventUser)
def unregister_event_user(
    event_id: int,
    db: Session = Depends(get_session),
    user: EventUser = Depends(get_current_user),
):
    """
    This function is used to unregister an event user.
    """
    event_user = crud.remove_user_from_event(event_id, user.id, db)
    return event_user
