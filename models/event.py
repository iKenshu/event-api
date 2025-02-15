"""
This file is used to define the Event model.
"""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship

from core.crud.base import BaseModel


class Event(BaseModel, table=True):
    """
    This class is used to define the Event model.
    """

    name: str
    description: str
    category: str = Field(default="Other")
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: datetime = Field(default_factory=datetime.now)
    location: Optional[str]
    status: str = Field(default="active", nullable=True)
    max_capacity: int = Field(default=100, nullable=True)
    current_capacity: int = Field(default=0, nullable=True)

    users: List["EventUser"] = Relationship(back_populates="event")
    sessions: List["Session"] = Relationship(back_populates="event")
