"""
This file is use to define the User GraphQL queries.
"""

import strawberry

from config.database import get_session
from crud.crud_user import user as crud
from graphql_api.schemas.user import UserType


@strawberry.type
class UserQuery:
    """
    This class is used to define the User GraphQL queries.
    """

    @strawberry.field
    def get_user_by_username(self, username: str) -> UserType:
        """
        This function is used to get a user by username.
        """
        db = get_session()
        return crud.get_by_username(db, username)
