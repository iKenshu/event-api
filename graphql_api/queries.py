"""
This file is used to define the GraphQL queries.
"""

import strawberry

import crud
from graphql_api.schemas import EventAllType, EventType


@strawberry.type
class Query:
    """
    This class is used to define the GraphQL queries.
    """

    @strawberry.field
    def get_all_events(self) -> EventAllType:
        """
        This function is used to get all events.
        """
        return crud.get_events()

    @strawberry.field
    def get_event(self, id: int) -> EventType:
        """
        This function is used to get an event by id.
        """
        return crud.get_event(id)
