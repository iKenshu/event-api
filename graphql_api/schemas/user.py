"""
This file is used to define the User GraphQL schemas.
"""

from typing import Optional

import strawberry


@strawberry.type
class UserType:
    """
    This class is used to define the User response type.
    """

    id: int
    username: Optional[str]
    hashed_password: Optional[str]


@strawberry.type
class User:
    """
    This class is used to define the User type.
    """

    id: Optional[int]
    username: Optional[str]


@strawberry.input
class UserCreateType:
    """
    This class is used to define the User create type.
    """

    username: str
    hashed_password: str


@strawberry.input
class UserUpdateType:
    """
    This class is used to define the User update type.
    """

    username: Optional[str]


@strawberry.type
class Token:
    """
    This class is used to define the Token type.
    """

    access_token: str
    token_type: str


@strawberry.type
class UserResponseType:
    """
    This class is used to define the User response type.
    """

    id: int
    username: Optional[str]
