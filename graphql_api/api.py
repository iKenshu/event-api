"""
This file is used to define the Event API for GraphQL.
"""

from strawberry.fastapi import GraphQLRouter

from graphql_api.mutations import Mutation
from graphql_api.queries import Query

graphql_router = GraphQLRouter(Query, Mutation)
