"""
This file is used to define the Event router.
"""

from fastapi import APIRouter
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from api import event
from api.event_user import router
from auth.api import router as auth_router
from graphql_api.mutations import Mutation
from graphql_api.queries import Query
from graphql_api.schemas import EventType

api_router = APIRouter()
schema = Schema(query=Query, mutation=Mutation)
graphlql_router = GraphQLRouter(schema)
api_router.include_router(event.router, prefix="/event", tags=["Event"])
api_router.include_router(graphlql_router, prefix="/graphql", tags=["GraphQL"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(router, prefix="/event-user", tags=["EventUser"])