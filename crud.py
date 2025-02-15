"""
This file is used to define the CRUD operations for the Event model.
"""

from fastapi import HTTPException
from sqlmodel import Session, select

from models.event_user import EventUser
from models.user import User
