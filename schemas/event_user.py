"""
This file is used to define the EventUser schema.
"""

from typing import Optional

from pydantic import BaseModel

from auth.schemas import UserResponse
from models.event import Event


class EventUserBase(BaseModel):
    """
    This schema class is used to define the EventUser base schema.
    """

    event_id: Optional[int] = None
    user_id: Optional[int] = None


class EventUserCreate(EventUserBase):
    """
    This schema class is used to define the EventUser create schema.
    """

    event_id: int


class EventUserUpdate(EventUserBase):
    """
    This schema class is used to define the EventUser update schema.
    """


class EventUser(EventUserBase):
    """
    This schema class is used to define the EventUser schema.
    """


class EventWithUsers(BaseModel):
    """
    This schema class is used to define the Event with users schema.
    """

    event: Event
    users: list[UserResponse]
