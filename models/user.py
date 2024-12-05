"""
This file is used to define the User model.
"""

from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """
    This class is used to define the User model.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    events: list["EventUser"] = Relationship(back_populates="user")
