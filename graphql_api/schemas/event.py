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
    max_capacity: int
    current_capacity: int
    status: str


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

    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    max_capacity: Optional[int] = None
    current_capacity: Optional[int] = None


@strawberry.type
class EventAllType:
    """
    This class is used to define the EventAll type.
    """

    total: str
    data: List[EventType]
