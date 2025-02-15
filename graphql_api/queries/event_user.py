"""
This file contains the EventUser GraphQL queries.
"""

import strawberry

from config.database import get_session
from crud.crud_event_user import event_user as crud
from graphql_api.schemas.event_user import EventUserType, EventUserWithUsers


@strawberry.type
class EventUserQuery:
    """
    This class is used to define the EventUser GraphQL queries.
    """

    @strawberry.field
    def get_event_user(self, event_id: int, user_id: int) -> EventUserType:
        """
        This function is used to get an event user by id.
        """
        db = get_session()
        return crud.get_event_user(db, event_id, user_id)

    @strawberry.field
    def get_all_event_users(self, event_id: int) -> EventUserWithUsers:
        """
        This function is used to get all users for an event.
        """
        db = get_session()
        return crud.get_event_users(db, event_id)
