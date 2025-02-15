"""
This file is used to define the SessionUser schemas.
"""

from typing import Optional

from pydantic import BaseModel

from auth.schemas import UserResponse
from models.sessions import Session


class SessionUserBase(BaseModel):
    """
    A class used to represent the SessionUser base schema.
    """

    session_id: Optional[int] = None
    user_id: Optional[int] = None


class SessionUserCreate(SessionUserBase):
    """
    A class used to represent the SessionUser create schema.
    """

    session_id: int


class SessionUserUpdate(SessionUserBase):
    """
    A class used to represent the SessionUser update schema.
    """


class SessionUser(SessionUserBase):
    """
    A class used to represent the SessionUser schema.
    """


class SessionWithUsers(BaseModel):
    """
    A class used to represent the Session with users schema.
    """

    session: Session
    users: list[UserResponse]
