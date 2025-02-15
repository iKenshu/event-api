"""
This file is used to define the User GraphQL mutations.
"""

from datetime import timedelta

import strawberry

from auth.api import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    create_user,
    get_current_user,
)
from config.database import get_session
from graphql_api.schemas.user import Token, UserCreateType, UserResponseType


@strawberry.type
class UserMutation:
    """
    This class is used to define the User GraphQL mutations.
    """

    @strawberry.mutation
    def create_user(self, user: UserCreateType) -> UserResponseType:
        """
        This function is used to create a new user.
        """
        db = get_session()
        return create_user(user, db)

    @strawberry.mutation
    def login(self, username: str, password: str) -> Token:
        """
        This function is used to login a user.
        """
        db = get_session()
        user = authenticate_user(username, password, db)
        if not user:
            raise Exception("Incorrect username or password")
        token = create_access_token(
            user.username,
            user.id,
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return Token(access_token=token, token_type="bearer")

    @strawberry.mutation
    def get_current_user(self) -> UserResponseType:
        """
        This function is used to get the current user.
        """
        return get_current_user()
