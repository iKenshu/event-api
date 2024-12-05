"""
This file is used to define the GraphQL mutations.
"""

import strawberry
from sqlmodel import select

from config.database import get_session
from graphql_api.schemas import EventCreateType, EventType, EventUpdateType
from models.event import Event


@strawberry.type
class Mutation:
    """
    This class is used to define the GraphQL mutations.
    """

    @strawberry.mutation
    def create_event(self, event: EventCreateType) -> EventType:
        """
        This function is used to create a new event.
        """
        db = get_session()
        event = Event(
            name=event.name,
            description=event.description,
            category=event.category,
            start_time=event.start_time,
            end_time=event.end_time,
            location=event.location,
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @strawberry.mutation
    def delete_event(self, id: int) -> EventType:
        """
        This function is used to delete an event.
        """
        db = get_session()
        query = select(Event).where(Event.id == id)
        result = db.exec(query)
        event = result.one_or_none()
        db.delete(event)
        db.commit()

        return

    @strawberry.mutation
    def update_event(self, id: int, event: EventUpdateType) -> EventType:
        """
        This function is used to update an event.
        """
        db = get_session()
        query = select(Event).where(Event.id == id)
        result = db.exec(query)
        event = result.one_or_none()
        event.name = event.name if event.name is not None else event.name
        event.description = (
            event.description
            if event.description is not None
            else event.description
        )
        event.category = (
            event.category if event.category is not None else event.category
        )
        event.start_time = (
            event.start_time
            if event.start_time is not None
            else event.start_time
        )
        event.end_time = (
            event.end_time if event.end_time is not None else event.end_time
        )
        event.location = (
            event.location if event.location is not None else event.location
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
