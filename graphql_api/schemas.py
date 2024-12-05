"""
This file is used to define the GraphQL schemas.
"""

from typing import List, Optional

import strawberry


@strawberry.type
class EventType:
    """
    This class is used to define the Event type.
    """

    id: int
    name: str
    description: str
    category: str
    start_time: str
    end_time: str
    location: str
    location: str


@strawberry.input
class EventCreateType:
    """
    This class is used to define the Event create type.
    """

    name: str
    description: str
    category: str
    start_time: str
    end_time: str
    location: Optional[str]


@strawberry.input
class EventUpdateType:
    """
    This class is used to define the Event update type.
    """

    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    location: Optional[str]


@strawberry.type
class EventAllType:
    """
    This class is used to define the EventAll type.
    """

    total: int
    data: List[EventType]
