"""
This file is used to define the GraphQL queries.
"""

import strawberry

from graphql_api.queries.event import EventQuery
from graphql_api.queries.event_user import EventUserQuery
from graphql_api.queries.session import SessionQuery
from graphql_api.queries.session_user import SessionUserQuery


@strawberry.type
class Query(EventQuery, SessionQuery, EventUserQuery, SessionUserQuery): ...
