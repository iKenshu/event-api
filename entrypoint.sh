#! /bin/sh

echo "----- Running migrations -----"
alembic upgrade head

echo "----- Starting server -----"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
