"""
This file is used to define the Event schema.
"""

from datetime import datetime
from enum import StrEnum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from models.event import Event


class CategoryEnum(StrEnum):
    """
    This class is used to define the Event category enum.
    """

    OTHER = "Other"
    CONFERENCE = "Conference"
    WORKSHOP = "Workshop"
    MEETUP = "Meetup"


class StatusEnum(StrEnum):
    """
    This class is used to define the Event status enum.
    """

    ACTIVE = "active"
    CLOSED = "closed"


class EventBase(BaseModel):
    """
    This class is used to define the Event schema.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[CategoryEnum] = Field(default=CategoryEnum.OTHER)
    status: Optional[StatusEnum] = Field(default=StatusEnum.ACTIVE)
    start_time: Optional[datetime] = Field(default=datetime.now())
    end_time: Optional[datetime] = Field(default=datetime.now())
    location: Optional[str] = None


class EventCreate(EventBase):
    """
    This class is used to define the Event create schema.
    """

    name: str
    description: str
    category: CategoryEnum = Field(default=CategoryEnum.OTHER)
    start_time: datetime = Field(default=datetime.now())
    end_time: datetime = Field(default=datetime.now())


class EventUpdate(EventBase):
    """
    This class is used to define the Event update schema.
    """


class EventAll(BaseModel):
    """
    This class is used to define the Event all schema.
    """

    total: int
    data: list[Event]


class EventFilter(BaseModel):
    """
    This class is used to define the Event filter schema.
    """

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["name", "category", "start_time"] = "name"
    status: Optional[StatusEnum] = None
    location: Optional[str] = None
    category: Optional[CategoryEnum] = None
