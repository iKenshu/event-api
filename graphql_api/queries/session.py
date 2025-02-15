"""
This file is used to define the Session GraphQL queries.
"""

from typing import Optional

import strawberry

from config.database import get_session
from crud.crud_session import session as crud
from graphql_api.schemas.session import SessionAllType, SessionType


@strawberry.type
class SessionQuery:
    @strawberry.field
    def get_session(self, id: int) -> SessionType:
        """
        This function is used to get a session by id.
        """
        db = get_session()
        return crud.get(db, id=id)

    @strawberry.field
    def get_all_sessions(
        self,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
        alive_only: bool = True,
    ) -> SessionAllType:
        """
        This function is used to get all sessions.
        """
        db = get_session()
        result = crud.all(
            db,
            skip=offset,
            limit=limit,
            alive_only=alive_only,
        )
        total = len(result)
        return SessionAllType(total=total, data=result)
