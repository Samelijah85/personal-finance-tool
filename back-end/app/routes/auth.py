from datetime import timedelta
from typing import Any, Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.token import Token
from ..models.user import User, UserInDB
from ..crud.user import create_user, authenticate_user
from ..core.security import create_access_token
from ..core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        404: {"description": "Not found"},
        201: {"description": "Created"},
        400: {"description": "Bad request"},
    },
)


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=User, status_code=201)
async def register(user: UserInDB) -> Any:
    """Register a new user."""
    return create_user(user)
