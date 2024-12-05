"""
This file is used to run the application.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from router import api_router

from config.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.title = "Events API"
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
