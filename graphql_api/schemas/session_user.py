"""
This file is used to define the Session User GraphQL schemas.
"""

from typing import List, Optional

import strawberry

from graphql_api.schemas.session import SessionType
from graphql_api.schemas.user import UserResponseType


@strawberry.type
class SessionUserType:
    """
    This class is used to define the Session User type.
    """

    id: Optional[int]
    session_id: Optional[int]
    user_id: Optional[int]


@strawberry.type
class SessionUserResponseType:
    """
    This class is used to define the Session User response type.
    """

    id: int
    session_id: int
    user_id: int


@strawberry.input
class SessionUserCreateType:
    """
    This class is used to define the Session User create type.
    """

    session_id: int
    user_id: int


@strawberry.input
class SessionUserUpdateType:
    """
    This class is used to define the Session User update type.
    """

    session_id: Optional[int]
    user_id: Optional[int]


@strawberry.type
class SessionUserWithUsers:
    """
    This class is used to define the Session User with users type.
    """

    session: SessionType
    users: List[UserResponseType]
