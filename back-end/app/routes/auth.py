from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.token import Token
from ..models.user import UserInDB
from ..crud.user import create_user, authenticate_user, get_access_token

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
    return get_access_token(user.username)


@router.post("/register", status_code=201)
async def register(user: UserInDB) -> Token:
    """Register a new user."""
    new_user = create_user(user)
    return get_access_token(new_user.username)
