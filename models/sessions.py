"""
This file contains the Session model.
"""

from sqlmodel import Field, Relationship

from core.models.base import BaseModel


class Session(BaseModel, table=True):
    """
    This class contains the Session model.
    """

    title: str = Field(max_length=100)
    speaker: str = Field(max_length=100)
    start_time: str
    end_time: str
    max_capacity: int = Field(default=100, nullable=True)
    current_capacity: int = Field(default=0, nullable=True)
    status: str = Field(default="active", nullable=True)
    event_id: int = Field(foreign_key="event.id", nullable=True)

    event: "Event" = Relationship(back_populates="sessions")
    users: list["SessionUser"] = Relationship(back_populates="session")
