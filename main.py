"""
This file is used to run the application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.database import init_db
from router import api_router
from services.elastic import create_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.title = "Events API"
app.include_router(api_router)
create_index()


@app.get("/")
async def root():
    return {"message": "Hello World"}
