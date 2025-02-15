"""
This file is used to define the Session GraphQL schemas.
"""

from datetime import datetime
from typing import List, Optional

import strawberry


@strawberry.type
class SessionType:
    """
    This class is used to define the Session type.
    """

    id: int
    title: Optional[str]
    speaker: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    event_id: Optional[int]
    status: Optional[str]
    max_capacity: Optional[int]
    current_capacity: Optional[int]


@strawberry.type
class SessionAllType:
    """
    This class is used to define the SessionAll type.
    """

    total: int
    data: List[SessionType]


@strawberry.input
class SessionCreateType:
    """
    This class is used to define the Session create type.
    """

    title: str
    speaker: str
    start_time: datetime
    end_time: datetime
    event_id: int


@strawberry.input
class SessionUpdateType:
    """
    This class is used to define the Session update type.
    """

    title: Optional[str] = None
    speaker: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    event_id: Optional[int] = None
    max_capacity: Optional[int] = None
    current_capacity: Optional[int] = None
    status: Optional[str] = None


@strawberry.type
class SessionResponseType:
    """
    This class is used to define the Session response type.
    """

    id: int
