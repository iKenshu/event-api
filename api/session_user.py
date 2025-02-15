"""
This file is used to define the SessionUser model.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from auth.api import get_current_user
from config.database import get_session
from crud.crud_session import session as session_crud
from crud.crud_session_user import session_user as crud
from models.user import User
from schemas.session_user import (
    SessionUser,
    SessionUserCreate,
    SessionUserUpdate,
    SessionWithUsers,
)

router = APIRouter()


@router.post("/{session_id}/register", response_model=SessionUser)
def create_event_user(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """
    Register a new user to a session.
    Args:
        session_user (SessionUserCreate): The session user to be created.
        session (Session): The database session.
        current_user (User): The current user.
    """
    session = session_crud.get(db, id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status == "full":
        raise HTTPException(status_code=400, detail="Session is full")

    session_user = crud.get_session_user(
        db=db, session_id=session_id, user_id=current_user.id
    )
    if session_user:
        raise HTTPException(
            status_code=400, detail="User already registered for this session"
        )

    session_user = crud.register_user_to_session(
        db=db, session_id=session_id, user_id=current_user.id
    )
    return session_user


@router.delete("/{session_id}/registrations", response_model=SessionUser)
def unregister_event_user(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """
    This function is used to unregister an event user.
    Args:
        session_user (SessionUserCreate): The session user to be created.
        session (Session): The database session.
        current_user (User): The current user.
    """
    session_user = crud.get_session_user(
        db=db, session_id=session_id, user_id=current_user.id
    )
    if not session_user:
        raise HTTPException(status_code=404, detail="Session user not found")
    session_user = crud.remove_user_from_session(
        db=db, session_id=session_id, user_id=current_user.id
    )
    return session_user


@router.get("/{session_id}/registrations", response_model=SessionWithUsers)
def get_session_users(
    db: Session = Depends(get_session), session_id: int = None
):
    """
    This function is used to get all users for a session.
    Args:
        session_id (int): The id of the session to get users for.
        db (Session, optional): The database session. Defaults to Depends(get_session).
    """
    session_user = crud.get_all_session_users(db=db, session_id=session_id)
    return session_user
