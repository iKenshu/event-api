"""
This file is used to define the EventUser CRUD.
"""

from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from core.crud.base import CRUDBase
from crud.crud_event import event as crud_event
from models.event_user import EventUser
from schemas.event_user import EventUserCreate, EventUserUpdate


class CRUDEventUser(CRUDBase[EventUser, EventUserCreate, EventUserUpdate]):
    """
    A class to perform CRUD operations on the EventUser model.
    """

    def add_user_to_event(self, db: Session, event_id: int, user_id: int):
        """
        This function is used to add a user to an event.
        """
        event = crud_event.get(db, id=event_id)
        event_user = EventUser(event_id=event_id, user_id=user_id)
        db.add(event_user)
        event.current_capacity += 1
        if event.current_capacity == event.max_capacity:
            event.status = "full"
        db.commit()
        db.refresh(event_user)
        return event_user

    def get_event_user(self, db: Session, event_id: int, user_id: int):
        """
        This function is used to get an event user by id.
        """
        return db.exec(
            select(EventUser).where(
                EventUser.event_id == event_id, EventUser.user_id == user_id
            )
        ).one_or_none()

    def remove_user_from_event(self, db: Session, event_id: int, user_id: int):
        """
        This function is used to remove a user from an event.
        """
        event = crud_event.get(db, id=event_id)
        event_user = self.get_event_user(db, event_id, user_id)
        if not event_user:
            raise HTTPException(status_code=404, detail="Event user not found")
        event.current_capacity -= 1
        db.delete(event_user)
        db.commit()
        return event_user

    def get_event_users(self, db: Session, event_id: int):
        """
        This function is used to get all users for an event.
        """
        event = crud_event.get(db, id=event_id)
        statement = select(EventUser).where(EventUser.event_id == event_id)
        result = db.exec(statement)
        event_users = result.all()
        users = [
            {
                "id": user.user_id,
                "username": user.user.username,
            }
            for user in event_users
        ]
        return {"event": event, "users": users}


event_user = CRUDEventUser(EventUser)
