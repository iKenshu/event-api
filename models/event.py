"""
This file is used to define the Event model.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Event(SQLModel, table=True):
    """
    This class is used to define the Event model.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    category: str = Field(default="Other")
    start_time: datetime = Field(default=datetime.now())
    end_time: datetime = Field(default=datetime.now())
    location: Optional[str]
    status: str = Field(default="active", nullable=True)
    users: list["EventUser"] = Relationship(back_populates="event")
