from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from ..core.db import user_collection
from ..core.config import settings
from ..core.security import get_password_hash, verify_password
from ..models.token import TokenData
from ..models.user import User, UserInDB
from ..schemas.user import usersEntity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user_by_username(username: str) -> UserInDB | None:
    user = user_collection.find_one({"username": username})
    if user:
        return UserInDB(**user)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_all_users() -> list[User]:
    users = usersEntity(user_collection.find())
    return users


def create_user(user: UserInDB) -> User:
    existing_user = get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.password = get_password_hash(user.password)
    user_collection.insert_one(user.model_dump())
    return user


def update_user(username: str, user: UserInDB) -> User:
    user_collection.find_one_and_update({"username": username}, {"$set": user.model_dump()})
    return user_collection.find_one({"username": username})


def delete_user(username: str) -> User | None:
    user = user_collection.find_one_and_delete({"username": username})
    if user:
        return User(**user)


def authenticate_user(username: str, password: str) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = get_user_by_username(username)
    if not user:
        raise credentials_exception
    if not verify_password(password, user.password):
        raise credentials_exception
    return user
