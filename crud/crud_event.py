"""
This file is used to define the CRUD operations for the Event model.
"""

from sqlmodel import Session, select

from core.crud.base import CRUDBase
from models.event import Event
from schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    """
    A class to perform CRUD operations on the Event model.
    """

    def get_all_events(
        self, db: Session, filters: dict = {}, alive_only: bool = True
    ) -> dict[list, int]:
        """
        Get all events.
        Args:
            db: The database session.
            filters: The filters to apply to the query.
        """
        statement = select(Event)

        if filters.get("location"):
            location = filters["location"].strip().lower()
            statement = statement.where(Event.location.like(f"%{location}%"))
        if filters.get("category"):
            statement = statement.where(Event.category == filters["category"])
        if filters.get("status"):
            statement = statement.where(Event.status == filters["status"])

        if alive_only:
            statement = statement.where(Event.is_active == True)

        order_by = filters.get("order_by", "name")
        if hasattr(Event, order_by):
            statement = statement.order_by(getattr(Event, order_by))

        results = db.exec(statement).all()
        total = len(results)
        return {"total": total, "data": results}


event = CRUDEvent(Event)
