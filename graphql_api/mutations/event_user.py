"""
This file contains the EventUser GraphQL mutations.
"""

import strawberry

from config.database import get_session
from crud.crud_event_user import event_user as crud
from graphql_api.schemas.event_user import EventUserType


@strawberry.type
class EventUserMutation:
    """
    This class is used to define the Event User GraphQL mutations.
    """

    @strawberry.mutation
    def register_user_to_event(
        self, event_id: int, user_id: int
    ) -> EventUserType:
        """
        This function is used to add a user to an event.
        """
        db = get_session()
        return crud.add_user_to_event(db, event_id, user_id)

    @strawberry.mutation
    def unregister_user_from_event(
        self, event_id: int, user_id: int
    ) -> EventUserType:
        """
        This function is used to remove a user from an event.
        """
        db = get_session()
        return crud.remove_user_from_event(db, event_id, user_id)
