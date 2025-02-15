"""
This file is used to configure the database connection.
"""

import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def init_db():
    """
    This function is used to initialize the database.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    This function is used to get a session to the database.
    """
    db = Session(engine)
    try:
        return db
    finally:
        db.close()
