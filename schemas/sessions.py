"""
This file contains schemas for the Session model.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field, model_validator

from models.sessions import Session
from schemas.event import StatusEnum


class SessionBase(BaseModel):
    """
    This class contains the base schema for the Session model.
    """

    title: Optional[str] = None
    speaker: Optional[str] = None
    start_time: Optional[datetime] = Field(default=datetime.now())
    end_time: Optional[datetime] = Field(
        default=datetime.now() + timedelta(hours=2)
    )
    event_id: Optional[int] = None
    status: Optional[StatusEnum] = Field(default=StatusEnum.ACTIVE)
    max_capacity: Optional[int] = None
    current_capacity: Optional[int] = None


class SessionCreate(BaseModel):
    """
    This class contains the schema for creating a Session.
    """

    title: str
    speaker: str
    start_time: datetime
    end_time: datetime
    max_capacity: int = Field(default=100)
    current_capacity: int = Field(default=0)
    event_id: int

    @model_validator(mode="before")
    def validate_end_time(cls, values):
        """
        This function is used to validate the end time.
        """
        end_time = values.get("end_time")
        start_time = values.get("start_time")

        values["end_time"] = datetime.fromisoformat(end_time)
        values["start_time"] = datetime.fromisoformat(start_time)

        if values["end_time"] < values["start_time"]:
            raise HTTPException(
                status_code=400, detail="end time cannot be before start time"
            )
        if values["end_time"] < datetime.now():
            raise HTTPException(
                status_code=400, detail="end time must be a future date"
            )
        if values["start_time"] < datetime.now():
            raise HTTPException(
                status_code=400, detail="start time must be a future date"
            )
        return values


class SessionUpdate(SessionBase):
    """
    This class contains the schema for updating a Session.
    """


class SessionResponse(SessionBase):
    """
    This class contains the schema for the Session model.
    """

    id: Optional[int] = None


class SessionAll(BaseModel):
    """
    This class contains the schema for the Session model.
    """

    total: int
    data: list[Session]
