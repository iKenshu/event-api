"""
This file contains all the GraphQL mutations.
"""

import strawberry

from graphql_api.mutations.event import EventMutation
from graphql_api.mutations.event_user import EventUserMutation
from graphql_api.mutations.session import SessionMutation
from graphql_api.mutations.session_user import SessionUserMutation
from graphql_api.mutations.user import UserMutation


@strawberry.type
class Mutation(
    EventMutation,
    EventUserMutation,
    SessionMutation,
    SessionUserMutation,
    UserMutation,
): ...
