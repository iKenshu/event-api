"""
This file contains the CRUD operations for the Session model.
"""

from sqlalchemy import DateTime, cast
from sqlmodel import Session, select

from core.crud.base import CRUDBase
from models.sessions import Session as SessionModel
from schemas.sessions import SessionCreate, SessionUpdate


class CRUDSession(CRUDBase[SessionModel, SessionCreate, SessionUpdate]):
    """
    A class to perform CRUD operations on the Session model.
    """

    def create_session(self, db: Session, *, obj_in: SessionCreate):
        """
        This method is used to create a new session and check if the session already exists.
        """
        statement = select(self.model)
        statement = statement.where(
            self.model.event_id == obj_in.event_id,
            cast(self.model.start_time, DateTime) < obj_in.end_time,
            cast(self.model.end_time, DateTime) > obj_in.start_time,
        )
        existing_session = db.exec(statement).first()

        if existing_session:
            raise ValueError("Session already exists at this time")

        session = SessionModel(**obj_in.dict())
        db.add(session)
        db.commit()
        db.refresh(session)
        return session


session = CRUDSession(SessionModel)
