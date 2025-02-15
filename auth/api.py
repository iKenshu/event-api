"""
This file is used to define the authentication logic for the FastAPI application.
"""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session

from auth.schemas import UserCreate, UserResponse
from config.database import get_session
from crud.crud_user import crud_user
from models.user import User

router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    """
    This function is used to create a new user.
    """
    user = User(
        username=user.username,
        hashed_password=bcrypt_context.hash(user.hashed_password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_session),
):
    """
    This function is used to login for an access token.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )
    token = create_access_token(
        user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db: Session):
    """
    This function is used to authenticate a user.
    """
    user = crud_user.get_user_by_username(db, username)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    """
    This function is used to create an access token.
    """
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
) -> UserResponse:
    """
    This function is used to get the current user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return UserResponse(username=username, id=user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
