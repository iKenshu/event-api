"""
This file is used to define the Event API.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

import crud
from config.database import get_session
from schemas.event import Event, EventAll, EventCreate, EventFilter, EventUpdate

router = APIRouter()


@router.get("/", response_model=EventAll)
def get_all_events(
    filters: Annotated[
        EventFilter,
        Query(
            title="Filters",
            description="Filters to apply to the events.",
            example={},
        ),
    ],
    db: Session = Depends(get_session),
):
    """
    This function is used to get all events.
    """
    filters = filters.dict()
    events = crud.get_events(db, filters)
    return events


@router.post("/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_session)):
    """
    This function is used to create a new event.
    Args:
        event (EventCreate): The event to create.
        db (Session, optional): The database session. Defaults to Depends(get_session).
    """
    event = crud.create_event(event, db)
    return event


@router.put("/{event_id}", response_model=Event)
def update_event(
    event_id: int, event: EventUpdate, db: Session = Depends(get_session)
):
    """
    This function is used to update an event.
    Args:
        id (int): The id of the event to update.
        event (EventUpdate): The event to update.
        db (Session, optional): The database session. Defaults to Depends(get_session).
    """
    event = crud.update_event(event_id, event, db)
    return event


@router.delete("/{id}", response_model=Event)
def delete_event(id: int, db: Session = Depends(get_session)):
    """
    This function is used to delete an event.
    Args:
        id (int): The id of the event to delete.
        db (Session, optional): The database session. Defaults to Depends(get_session).
    """
    event = crud.get_event(id, db)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event = crud.delete_event(event.id, db)
    return event
