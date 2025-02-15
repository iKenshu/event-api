"""
This file is used to define the User schemas.
"""

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """
    This class is used to define the User schema.
    """

    id: Optional[int] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None


class UserCreate(BaseModel):
    """
    This class is used to define the User create schema.
    """

    username: str
    hashed_password: str


class UserUpdate(User):
    """
    This class is used to define the User update schema.
    """


class Token(BaseModel):
    """
    This class is used to define the Token schema.
    """

    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """
    This class is used to define the User response schema.
    """

    id: int
    username: Optional[str] = None
