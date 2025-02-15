"""
This file contains the CRUD operations for the SessionUser model.
"""

from typing import Optional

from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from core.crud.base import CRUDBase
from crud.crud_session import session as session_crud
from models.session_user import SessionUser
from schemas.session_user import SessionUserCreate, SessionUserUpdate


class CRUDSessionUser(
    CRUDBase[SessionUser, SessionUserCreate, SessionUserUpdate]
):
    """
    This class contains the CRUD operations for the SessionUser model.
    """

    def register_user_to_session(
        self,
        db: Session,
        session_id: int,
        user_id: int,
    ) -> SessionUser:
        """
        Register a new user to a session.
        Args:
            session_user (SessionUserCreate): The session user to be created.
            session (Session): The database session.
        """
        session = session_crud.get(db, id=session_id)
        statement = select(SessionUser).where(
            SessionUser.session_id == session_id,
            SessionUser.user_id == user_id,
        )
        result = db.exec(statement).one_or_none()
        if result:
            raise HTTPException(
                status_code=400, detail="User already registered to session"
            )

        session_user = SessionUser(session_id=session_id, user_id=user_id)
        db.add(session_user)
        session.current_capacity += 1
        if session.current_capacity == session.max_capacity:
            session.status = "full"
        db.commit()
        db.refresh(session_user)

        return session_user

    def get_session_user(self, db: Session, session_id: int, user_id: int):
        """
        Get a session user by id.
        Args:
            db: The database session.
            session_id: The id of the session to get.
            user_id: The id of the user to get.
        """
        return db.exec(
            select(SessionUser).where(
                SessionUser.session_id == session_id,
                SessionUser.user_id == user_id,
            )
        ).one_or_none()

    def remove_user_from_session(
        self, db: Session, session_id: int, user_id: int
    ):
        """
        This function is used to remove a user from a session.
        """
        session = session_crud.get(db, id=session_id)
        session_user = self.get_session_user(db, session_id, user_id)
        if not session_user:
            raise HTTPException(
                status_code=404, detail="Session user not found"
            )
        session.current_capacity -= 1
        db.delete(session_user)
        db.commit()
        return session_user

    def get_all_session_users(self, db: Session, session_id: int):
        """
        Get all users for a session.
        Args:
            db: The database session.
            session_id: The id of the session to get users for.
        """
        session = session_crud.get(db, id=session_id)
        statement = select(self.model).where(
            self.model.session_id == session_id
        )
        result = db.exec(statement)
        session_users = result.all()
        users = [
            {"id": user.user_id, "username": user.user.username}
            for user in session_users
        ]
        return {"session": session, "users": users}


session_user = CRUDSessionUser(SessionUser)
