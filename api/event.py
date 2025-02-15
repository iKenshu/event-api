"""
This file is used to define the Event API.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from config.database import get_session
from crud.crud_event import event as crud
from schemas.event import Event, EventAll, EventCreate, EventFilter, EventUpdate
from services.elastic import index_event, search_events

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
    events = crud.get_all_events(db, filters)
    print(crud.get_all_events(db, filters))
    return events


@router.get("/search", response_model=EventAll)
def search_events_with_elasticsearch(
    query: str,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_session),
):
    """
    This function is used to search for events.
    """
    events = search_events(query, limit, offset)
    return events


@router.post("/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_session)):
    """
    This function is used to create a new event.
    Args:
        event (EventCreate): The event to create.
        db (Session, optional): The database session. Defaults to Depends(get_session).
    """
    event = crud.create(db, obj_in=event)
    index_event(event)
    return event


@router.patch("/{event_id}", response_model=Event)
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
    db_obj = crud.get(db, event_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Event not found")
    event = crud.update(db, db_obj=db_obj, obj_in=event)
    return event


@router.delete("/{id}", response_model=Event)
def delete_event(id: int, db: Session = Depends(get_session)):
    """
    This function is used to delete an event.
    Args:
        id (int): The id of the event to delete.
        db (Session, optional): The database session. Defaults to Depends(get_session).
    """
    event = crud.get(db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event = crud.delete(db, id=id)
    return event
