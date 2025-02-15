"""
This file contains the API for the Session model.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from config.database import get_session
from crud.crud_session import session as crud
from schemas.sessions import (
    SessionAll,
    SessionCreate,
    SessionResponse,
    SessionUpdate,
)

router = APIRouter()


@router.post("/", response_model=SessionResponse)
def create_session(session: SessionCreate, db=Depends(get_session)):
    """
    This function is used to create a new session.
    """
    sessions = crud.create_session(db, obj_in=session)
    return sessions


@router.get("/", response_model=SessionAll)
def get_all_sessions(db=Depends(get_session)):
    """
    This function is used to get all sessions.
    """
    sessions = crud.all(db)
    total = len(sessions)
    return SessionAll(total=total, data=sessions)


@router.get("/{session_id}", response_model=SessionResponse)
def get_session_by_id(session_id: int, db=Depends(get_session)):
    """
    This function is used to get a session.
    """
    session = crud.get(db=db, id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.patch("/{session_id}", response_model=SessionResponse)
def update_session(
    session_id: int, obj_in: SessionUpdate, db=Depends(get_session)
):
    """
    This function is used to update a session.
    """
    session = crud.get(db=db, id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session = crud.update(db, db_obj=session, obj_in=obj_in)
    return session


@router.delete("/{session_id}", response_model=SessionResponse)
def delete_session(session_id: int, db=Depends(get_session)):
    """
    This function is used to delete a session.
    """
    session = crud.get(db, id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session = crud.delete(db, id=session_id)
    return session
