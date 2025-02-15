"""
This file is used to define the Event User GraphQL schemas.
"""

from typing import List, Optional

import strawberry

from graphql_api.schemas.event import EventType
from graphql_api.schemas.user import UserResponseType


@strawberry.type
class EventUserType:
    """
    This class is used to define the Event User type.
    """

    id: Optional[int]
    event_id: Optional[int]
    user_id: Optional[int]


@strawberry.input
class EventUserCreateType:
    """
    This class is used to define the Event User create type.
    """

    event_id: int
    user_id: int


@strawberry.type
class EventUserWithUsers:
    """
    This class is used to define the Event User with User type.
    """

    event: EventType
    users: List[UserResponseType]
