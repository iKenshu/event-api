"""
This file is used to define the CRUD operations for the Event model.
"""

from fastapi import HTTPException
from sqlmodel import Session, select

from models.event import Event
from models.event_user import EventUser
from models.user import User
from schemas.event import EventCreate


def create_event(event: EventCreate, db: Session):
    """
    This function is used to create a new event.
    """
    event = Event(**event.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_event(id: int, db: Session):
    """
    This function is used to get an event by id.
    """
    statement = select(Event).where(Event.id == id)
    result = db.exec(statement)
    event = result.one_or_none()
    return event


def get_events(db: Session, filters: dict = {}):
    """
    This function is used to get all events.
    """
    statement = select(Event)

    if filters.get("location"):
        location = filters["location"].strip().lower()
        statement = statement.where(Event.location.like(f"%{location}%"))
    if filters.get("category"):
        statement = statement.where(Event.category == filters["category"])
    if filters.get("status"):
        statement = statement.where(Event.status == filters["status"])

    order_by = filters.get("order_by", "name")
    if hasattr(Event, order_by):
        statement = statement.order_by(getattr(Event, order_by))

    limit = filters.get("limit", 100)
    offset = filters.get("offset", 0)
    statement = statement.limit(limit).offset(offset)

    results = db.exec(statement)
    events = results.all()
    total = len(events)
    return {"total": total, "data": events}


def update_event(event_id: int, event_data: EventCreate, db: Session):
    """
    This function is used to update an event.
    """
    statement = select(Event).where(Event.id == event_id)
    result = db.exec(statement)
    event = result.one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.name = event_data.name if event_data.name is not None else event.name
    event.description = (
        event_data.description
        if event_data.description is not None
        else event.description
    )
    event.category = (
        event_data.category
        if event_data.category is not None
        else event.category
    )
    event.start_time = (
        event_data.start_time
        if event_data.start_time is not None
        else event.start_time
    )
    event.end_time = (
        event_data.end_time
        if event_data.end_time is not None
        else event.end_time
    )
    event.location = (
        event_data.location
        if event_data.location is not None
        else event.location
    )
    event.status = (
        event_data.status if event_data.status is not None else event.status
    )

    db.commit()
    db.refresh(event)

    return event


def delete_event(id: int, db: Session):
    """
    This function is used to delete an event.
    """
    statement = select(Event).where(Event.id == id)
    result = db.exec(statement)
    event = result.one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return event


def get_event_by_id(id: int, db: Session):
    """
    This function is used to get an event by id.
    """
    statement = select(Event).where(Event.id == id)
    result = db.exec(statement)
    event = result.one_or_none()
    return event


def get_user_by_username(username: str, db: Session):
    """
    This function is used to get a user by username.
    """
    statement = select(User).where(User.username == username)
    result = db.exec(statement)
    user = result.one_or_none()
    return user


def add_user_to_event(event_id: int, user_id: int, db: Session):
    """
    This function is used to add a user to an event.
    """
    event_user = EventUser(event_id=event_id, user_id=user_id)
    db.add(event_user)
    db.commit()
    db.refresh(event_user)
    return event_user


def remove_user_from_event(event_id: int, user_id: int, db: Session):
    """
    This function is used to remove a user from an event.
    """
    statement = select(EventUser).where(
        EventUser.event_id == event_id, EventUser.user_id == user_id
    )
    result = db.exec(statement)
    event_user = result.one_or_none()
    if not event_user:
        raise HTTPException(status_code=404, detail="Event user not found")
    db.delete(event_user)
    db.commit()
    return event_user


def get_event_users(event_id: int, db: Session):
    """
    This function is used to get all users for an event.
    """
    event = get_event_by_id(event_id, db)
    statement = select(EventUser).where(EventUser.event_id == event_id)
    result = db.exec(statement)
    event_users = result.all()
    users = [
        {
            "id": user.user_id,
            "username": user.user.username,
        }
        for user in event_users
    ]
    return {"event": event, "users": users}
