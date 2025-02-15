"""
This file is used to define the Session GraphQL mutations.
"""

import strawberry
from fastapi import HTTPException

from config.database import get_session
from crud.crud_session import session as crud
from graphql_api.schemas.session import SessionCreateType, SessionType


@strawberry.type
class SessionMutation:
    """
    This class is used to define the Session GraphQL mutations.
    """

    @strawberry.mutation
    def create_session(self, session: SessionCreateType) -> SessionType:
        """
        This function is used to create a new session.
        """
        db = get_session()
        session = crud.create(db, obj_in=session)
        return session

    @strawberry.mutation
    def update_session(self, id: int, obj_in: SessionCreateType) -> SessionType:
        """
        This function is used to update a session.
        """
        db = get_session()
        db_obj = crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Session not found")
        session = crud.update(db, db_obj=db_obj, obj_in=obj_in)
        return session
