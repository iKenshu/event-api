"""
This file is used to define the EventUser api.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from auth.api import get_current_user
from config.database import get_session
from crud.crud_event import event as crud_event
from crud.crud_event_user import event_user as crud
from models.event_user import EventUser
from schemas.event import StatusEnum
from schemas.event_user import EventWithUsers

router = APIRouter()


@router.post("/{event_id}/register", response_model=EventUser)
def register_event_user(
    event_id: int,
    db: Session = Depends(get_session),
    user: EventUser = Depends(get_current_user),
):
    """
    This function is used to register an event user.
    """
    event = crud_event.get(db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.status == StatusEnum.FULL:
        raise HTTPException(status_code=400, detail="Event is full")

    event_user = crud.add_user_to_event(
        db=db, event_id=event_id, user_id=user.id
    )
    return event_user


@router.get("/{event_id}/registrations", response_model=EventWithUsers)
def get_event_users(event_id: int, db: Session = Depends(get_session)):
    """
    This function is used to get all users for an event.
    Args:
        event_id (int): The id of the event to get users for.
    """
    event_users = crud.get_event_users(db, event_id)
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
    event_user = crud.remove_user_from_event(
        db=db, event_id=event_id, user_id=user.id
    )
    return event_user
