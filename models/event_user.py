"""
This file is used to define the EventUser model.
"""

from sqlmodel import Field, Relationship, SQLModel

from models.event import Event
from models.user import User


class EventUser(SQLModel, table=True):
    """
    This class is used to define the EventUser model.
    """

    __tablename__ = "event_user"

    event_id: int = Field(foreign_key="event.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)

    event: Event = Relationship(
        back_populates="users",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )
    user: User = Relationship(
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
        back_populates="events",
    )
