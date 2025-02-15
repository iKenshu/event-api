"""
This file is used to define the User CRUD.
"""

from sqlmodel import Session, select

from auth.schemas import UserCreate, UserUpdate
from core.crud.base import CRUDBase
from models.user import User


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    A class to perform CRUD operations on the User model.
    """

    def get_user_by_username(self, db: Session, username: str) -> User:
        """
        This function is used to get a user by username.
        """
        return db.exec(
            select(User).where(
                User.username == username, User.is_active == True
            )
        ).one_or_none()


crud_user = CRUDUser(User)
