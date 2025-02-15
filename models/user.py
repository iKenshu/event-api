"""
This file is used to define the User model.
"""

from sqlmodel import Field, Relationship, SQLModel

from core.models.base import BaseModel


class User(BaseModel, table=True):
    """
    This class is used to define the User model.
    """

    username: str = Field(unique=True)
    hashed_password: str
    events: list["EventUser"] = Relationship(back_populates="user")
    sessions: list["SessionUser"] = Relationship(back_populates="user")
