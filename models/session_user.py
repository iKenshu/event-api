"""
This file is used to define the SessionUser model.
"""

from sqlmodel import Field, Relationship, SQLModel


class SessionUser(SQLModel, table=True):
    """
    A class used to represent the SessionUser model.
    """

    __tablename__ = "session_user"

    session_id: int = Field(foreign_key="session.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)

    session: "Session" = Relationship(back_populates="users")
    user: "User" = Relationship(back_populates="sessions")
