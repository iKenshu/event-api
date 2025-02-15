"""
This file contains the EventUser GraphQL mutations.
"""

import strawberry

from config.database import get_session
from crud.crud_session_user import session_user as crud
from graphql_api.schemas.session_user import SessionUserType


@strawberry.type
class SessionUserMutation:
    """
    This class is used to define the SessionUser GraphQL mutations.
    """

    @strawberry.mutation
    def register_user_to_session(
        self, session_id: int, user_id: int
    ) -> SessionUserType:
        """
        This function is used to add a user to a session.
        """
        db = get_session()
        return crud.register_user_to_session(db, session_id, user_id)

    @strawberry.mutation
    def unregister_user_from_session(
        self, session_id: int, user_id: int
    ) -> SessionUserType:
        """
        This function is used to remove a user from a session.
        """
        db = get_session()
        return crud.remove_user_from_session(db, session_id, user_id)
