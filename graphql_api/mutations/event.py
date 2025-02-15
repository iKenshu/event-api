"""
This file is used to define the GraphQL mutations.
"""

import strawberry
from fastapi import HTTPException
from sqlmodel import select

from config.database import get_session
from crud.crud_event import event as crud
from graphql_api.schemas.event import (
    EventCreateType,
    EventType,
    EventUpdateType,
)
from models.event import Event


@strawberry.type
class EventMutation:
    """
    This class is used to define the GraphQL mutations.
    """

    @strawberry.mutation
    def create_event(self, event: EventCreateType) -> EventType:
        """
        This function is used to create a new event.
        """
        db = get_session()
        event = crud.create(db, obj_in=event)
        return event

    @strawberry.mutation
    def delete_event(self, id: int) -> EventType:
        """
        This function is used to delete an event.
        """
        db = get_session()
        event = crud.delete(db, id=id)
        return event

    @strawberry.mutation
    def update_event(self, id: int, obj_in: EventUpdateType) -> EventType:
        """
        This function is used to update an event.
        """
        db = get_session()
        db_obj = crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Event not found")

        event = crud.update(db, db_obj=db_obj, obj_in=obj_in)
        return event
