"""
This file is used to define the SessionUser GraphQL mutations.
"""

import strawberry

from config.database import get_session
from crud.crud_session_user import session_user as crud
from graphql_api.schemas.session_user import (
    SessionUserType,
    SessionUserWithUsers,
)
from graphql_api.schemas.user import UserResponseType


@strawberry.type
class SessionUserQuery:
    """
    This class is used to define the SessionUser GraphQL queries.
    """

    @strawberry.field
    def get_session_user(
        self, session_id: int, user_id: int
    ) -> SessionUserType:
        """
        This function is used to get a session user by id.
        """
        db = get_session()
        return crud.get_session_user(db, session_id, user_id)

    @strawberry.field
    def get_all_session_users(self, session_id: int) -> SessionUserWithUsers:
        """
        This function is used to get all users for a session.
        """
        db = get_session()
        session_user = crud.get_all_session_users(db, session_id)
        session_data = session_user["session"]
        users = [
            UserResponseType(id=user["id"], username=user["username"])
            for user in session_user["users"]
        ]
        return SessionUserWithUsers(session=session_data, users=users)
