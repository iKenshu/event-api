"""
This file is used to define the Event API for GraphQL.
"""

from strawberry.fastapi import GraphQLRouter

from graphql_api.schemas import EventType

graphql_router = GraphQLRouter(EventType)
