"""
This file is used to define the GraphQL queries.
"""

from typing import Optional

import strawberry

from config.database import get_session
from crud.crud_event import event as crud
from graphql_api.schemas.event import EventAllType, EventType


@strawberry.type
class EventQuery:
    """
    This class is used to define the GraphQL queries.
    """

    @strawberry.field
    def get_all_events(
        self,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
        alive_only: bool = True,
    ) -> EventAllType:
        """
        This function is used to get all events.
        """
        db = get_session()
        result = crud.get_all_events(
            db,
            filters={"limit": limit, "offset": offset},
            alive_only=alive_only,
        )
        total = result.get("total")
        events = result.get("data")
        return EventAllType(total=total, data=events)

    @strawberry.field
    def get_event(self, id: int) -> EventType:
        """
        This function is used to get an event by id.
        """
        db = get_session()
        return crud.get(db, id=id)
